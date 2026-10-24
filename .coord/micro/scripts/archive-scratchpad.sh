#!/bin/bash
# Move the oldest scratchpad entries into .coord/micro/scratchpad-archive/SCRATCHPAD-<UTC date>.md once the
# file passes MAX_LINES; the header and the newest entries stay live.
#   archive-scratchpad.sh [MAX_LINES=1500] [KEEP_LINES=MAX_LINES/2]
# (a leading ROLE from the pre-1.1 form is accepted and ignored)
# Appenders (post, plain >>) never take the lock, so the live file is never copied-then-truncated: it is renamed
# aside, split, and the kept part swapped in; lines that raced onto a fresh file are pinned and appended after it.
set -euo pipefail
. "$(dirname "$0")/_lib.sh"
if [ "$#" -gt 0 ] && role_of "$1" >/dev/null 2>&1; then echo "archive-scratchpad.sh: ROLE argument is deprecated and ignored (removal in 2.0.0)" >&2; shift; fi
max="${1:-1500}"; keep="${2:-$((max / 2))}"
case "$max$keep" in ''|*[!0-9]*) echo "usage: $0 [MAX_LINES] [KEEP_LINES] (whole numbers)" >&2; exit 2;; esac
adir="$base/scratchpad-archive"; arch="$adir/SCRATCHPAD-$(date -u +%Y-%m-%d).md"
aside=""; new=""; race=""; xs=0
size() { wc -c < "$1" | tr -d ' '; }
# append_range SRC FROM TO: append bytes [FROM,TO) of SRC to the live file in ONE write(2), so concurrent >> lines
# can land before or after it but never inside it (head/tail/cat write in chunks and would split lines).
append_range() {
  python3 -c 'import os, sys
src, a, b, dst = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
with open(src, "rb") as f: f.seek(a); d = f.read(b - a)
fd = os.open(dst, os.O_WRONLY | os.O_APPEND | os.O_CREAT, 0o644)
while d: d = d[os.write(fd, d):]
os.close(fd)' "$1" "$2" "$3" "$pad"
}
# install_live SRC: make SRC the live scratchpad without ever clobbering lines appenders already wrote. Try an
# atomic no-clobber link; if appenders recreated the file meanwhile, pin its inode, swap SRC in with rename, then
# append the pinned lines after it. Loops (bounded) if the file vanishes in between. SRC is only removed by the caller.
# Returns 0 installed, 1 not installed, 2 installed but the pinned lines could not be appended ($race keeps them).
install_live() {
  local src="$1" i=0
  while [ "$i" -lt 100 ]; do
    i=$((i + 1))
    if ln "$src" "$pad" 2>/dev/null; then return 0; fi
    if ln "$pad" "$race" 2>/dev/null; then
      mv -f "$src" "$pad" || { rm -f "$race"; return 1; }
      xs="$(size "$race")"; append_range "$race" 0 "$xs" || { xs=0; return 2; }
      return 0
    fi
  done
  return 1
}
do_archive() {
  aside="$pad.aside.$$"; new="$pad.new.$$"; race="$pad.race.$$"; xs=0
  local got now rc n src msg chk failed kept f
  [ -f "$pad" ] || { echo "no scratchpad to archive"; return 0; }
  grep -qx '## Log' "$pad" || { echo "refused: SCRATCHPAD.md has no '## Log' heading" >&2; return 3; }
  [ "$(wc -l < "$pad" | tr -d ' ')" -gt "$max" ] || { echo "scratchpad within $max lines; no archive needed"; return 0; }
  mkdir -p "$adir" || return 1
  mv "$pad" "$aside" || return 1
  got="$(size "$aside")"
  python3 - "$aside" "$new" "$arch" "$keep" "$(utc)" "${arch#"$base"/}" "$got" <<'PY' && rc=0 || rc=$?
import os, sys
aside, new, arch, keep, now, rel, got = sys.argv[1:8]; keep = int(keep)
E = dict(encoding='utf-8', errors='surrogateescape', newline='')
with open(aside, 'rb') as f: raw = f.read(int(got))   # exactly what was measured; later bytes are re-appended below
lines = raw.decode('utf-8', 'surrogateescape').splitlines(keepends=True)
log = next(i for i, l in enumerate(lines) if l.strip() == '## Log')
head, body = lines[:log + 1], lines[log + 1:]
cut = max(0, len(body) - keep)
while cut < len(body) and not (body[cut].startswith('- ') or body[cut].startswith('### ')): cut += 1
old = [l for l in body[:cut] if not l.startswith('Older entries archived to')]
while old and old[0].strip() == '': old.pop(0)
if not old: sys.exit(10)   # nothing older than the kept tail
fresh = not os.path.exists(arch)
with open(arch, 'a', **E) as f:
    if fresh: f.write('# Scratchpad archive\n\nOldest entries moved out of SCRATCHPAD.md, oldest first.\n')
    f.write('\n## Archived %s\n\n' % now); f.write(''.join(old))
    if old and not old[-1].endswith('\n'): f.write('\n')
    f.flush(); os.fsync(f.fileno())
note = ['\nOlder entries archived to `%s`.\n' % rel]
with open(new, 'w', **E) as f: f.write(''.join(head + note + ['\n'] + body[cut:]))
PY
  src="$new"; msg="archived to ${arch#"$repo"/}"
  if [ "$rc" -eq 10 ]; then src="$aside"; msg="nothing older than the newest $keep lines to archive"; rc=0   # nothing to move: put the file back
  elif [ "$rc" -ne 0 ]; then src="$aside"; msg=""; fi                                                       # failed: put the live file back
  [ -z "${COORD_TEST_HOOK:-}" ] || bash -c "$COORD_TEST_HOOK" || true   # test seam: act as a lock-free appender here
  failed=0; install_live "$src" || failed=$?
  [ "$failed" -ne 1 ] || { echo "archive: could not restore scratchpad; data kept in $aside and $new" >&2; return 1; }
  chk="$aside"; if [ "$src" = "$aside" ]; then chk=""; fi   # now the live inode (or gone): never re-append it onto itself
  # A writer that opened the old file before the rename may land late: re-check the old inodes a few times.
  # (This runs under with_lock, where set -e is off: every append is checked by hand.)
  for n in 1 2 3; do
    [ "$failed" -eq 0 ] || break
    sleep 0.05
    if [ -n "$chk" ]; then now="$(size "$chk")"; [ "$now" -le "$got" ] || { append_range "$chk" "$got" "$now" && got="$now" || failed=2; }; fi
    [ "$failed" -eq 0 ] || break
    [ ! -f "$race" ] || { now="$(size "$race")"; [ "$now" -le "$xs" ] || { append_range "$race" "$xs" "$now" && xs="$now" || failed=2; }; }
  done
  if [ "$failed" -ne 0 ]; then
    # Never delete the only copy of lines that missed the live file: keep the pinned/old files and say where.
    rm -f "$new"
    kept=""; for f in "$race" "$aside"; do [ ! -f "$f" ] || kept="$kept ${f#"$repo"/}"; done
    echo "archive: could not append late scratchpad lines to the live file; they are kept in:$kept (merge them by hand, then delete)" >&2
    return 1
  fi
  rm -f "$aside" "$new" "$race"
  [ "$rc" -eq 0 ] || return "$rc"
  [ -z "$msg" ] || echo "$msg"
}
with_lock scratchpad do_archive
