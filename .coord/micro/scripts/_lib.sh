# Shared helpers for the micro coordination scripts. Sourced, not run.
# Agents hold the slots in .coord/micro/ROLES (default LEAD, ASSIST); the role is the identity. OWNER is the human and never claims.
# Paths come from this file's location, so running the kit from another repo's cwd still targets this repo.
base="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"; repo="$(cd "$base/../.." && pwd)"
state="$base/state"; pad="$base/SCRATCHPAD.md"
mkdir -p "$state"
utc() { date -u '+%Y-%m-%d %H:%M UTC'; }
# Collapse newlines so a label, lane or summary cannot forge claim lines or scratchpad headings.
oneline() { printf '%s' "$1" | tr '\r\n' '  '; }
# Append one scratchpad entry: post <FROM> <TO> <message>
post() { printf '\n- %s | %s → %s: %s\n' "$(date -u +%Y-%m-%d)" "$1" "$2" "$(oneline "$3")" >> "$pad"; }
# Read one key from a claim file (key=value lines).
claim_get() { sed -n "s/^$2=//p" "$1" | head -1; }

# Roster: print "slotN=NAME" lines parsed from ROLES (or the defaults), warning on stderr for lines it ignores.
_roster_rows() {
  if [ -f "$base/ROLES" ]; then cat "$base/ROLES"; fi | awk '
    { gsub(/\r/, ""); sub(/^[ \t]+/, ""); sub(/[ \t]+$/, "") }
    $0 == "" || /^#/ { next }
    {
      i = index($0, "="); key = ""; val = ""
      if (i > 0) { key = substr($0, 1, i - 1); val = substr($0, i + 1); sub(/[ \t]+$/, "", key); sub(/^[ \t]+/, "", val) }
      name = toupper(val)
      if (key !~ /^slot[1-9]$/) { print "roster: ignoring line: " $0 > "/dev/stderr"; next }
      n = substr(key, 5, 1)
      if (name == "OWNER") { print "roster: OWNER is reserved, ignoring " key > "/dev/stderr"; next }
      if (name !~ /^[A-Z0-9_-]+$/) { print "roster: invalid name for " key ", ignoring" > "/dev/stderr"; next }
      if (n in seen) { print "roster: duplicate " key ", ignoring" > "/dev/stderr"; next }
      if (name in used) { print "roster: " name " already has a slot, ignoring " key > "/dev/stderr"; next }
      seen[n] = name; used[name] = 1; count++
    }
    END {
      if (count == 0) { print "slot1=LEAD"; print "slot2=ASSIST"; exit }
      for (n = 1; n <= 9; n++) if (n in seen) print "slot" n "=" seen[n]
    }'
}
# Slot names, one per line, in slot order.
slots() { _roster_rows | sed 's/^slot[1-9]=//'; }
# Canonical slot name for NAME (case-insensitive; rep<N>/slot<N> alias slot N); fails for OWNER or unknown names.
role_of() {
  local r n; r="$(printf '%s' "${1:-}" | tr '[:lower:]' '[:upper:]')"
  case "$r" in ''|OWNER) return 1;; esac
  case "$r" in *[!A-Z0-9_-]*) return 1;; esac
  case "$r" in
    REP[1-9]|SLOT[1-9]) n="${r#REP}"; n="${n#SLOT}"; r="$(_roster_rows 2>/dev/null | sed -n "s/^slot$n=//p")"; [ -n "$r" ] || return 1; printf '%s' "$r"; return 0;;
  esac
  slots 2>/dev/null | grep -qx -- "$r" || return 1
  printf '%s' "$r"
}
# Slot names that currently have a claim file.
held_roles() { local s; for s in $(slots 2>/dev/null); do [ -f "$state/.active-$s" ] && printf '%s\n' "$s"; done; return 0; }
# Session id as a plain filename token: prints VALUE if it is [A-Za-z0-9._-]+ (and not . or ..), else nothing.
clean_sid() {
  case "${1:-}" in *[!A-Za-z0-9._-]*|.|..) return 0;; esac
  printf '%s' "${1:-}"
}
# Identity: explicit arg, then $COORD_ROLE, then the session map, then the sole held claim. Prints the slot or fails.
my_role() {
  local r sid held
  if [ -n "${1:-}" ]; then role_of "$1"; return; fi
  if [ -n "${COORD_ROLE:-}" ]; then role_of "$COORD_ROLE"; return; fi
  sid="$(clean_sid "${COORD_SESSION_ID:-}")"
  if [ -n "$sid" ] && [ -f "$state/.sid-$sid" ]; then r="$(head -1 "$state/.sid-$sid" | tr -d '[:space:]')"; role_of "$r"; return; fi
  held="$(held_roles)"
  case "$held" in ''|*$'\n'*) return 1;; esac
  printf '%s' "$held"
}
# Run CMD under a mkdir lock: with_lock NAME CMD... Waits up to 30 s; breaks a lock older than 120 s.
# Breaking AND releasing both go through a short-lived guard dir ($lock.break). A breaker re-judges staleness under
# the guard, then moves the lock aside atomically with mv before removing it; an owner checks its token and rmdirs
# under the guard. So a lock cannot be released and re-acquired while a breaker is between "stale?" and "mv", and a
# slow owner can never release a lock that was broken and re-acquired by someone else.
_guard_take() {  # _guard_take LOCK: take $LOCK.break, waiting briefly; a guard older than 2 min is moved aside first
  local g="$1.break" k=0 d
  until mkdir "$g" 2>/dev/null; do
    if [ -n "$(find "$g" -maxdepth 0 -mmin +2 2>/dev/null)" ]; then
      d="$g.dead.$$.$RANDOM.$k"
      if mv "$g" "$d" 2>/dev/null; then
        if [ -n "$(find "$d" -maxdepth 0 -mmin +2 2>/dev/null)" ]; then rm -rf "$d"
        elif [ ! -e "$g" ]; then mv "$d" "$g" 2>/dev/null || rm -rf "$d"; else rm -rf "$d"; fi
      fi
    fi
    k=$((k + 1)); [ "$k" -le "${2:-100}" ] || return 1
    sleep 0.02
  done
}
with_lock() {
  local lock="$state/.lock-$1" i=0 rc tok="$$.$RANDOM.$RANDOM" dead got; shift
  until mkdir "$lock" 2>/dev/null; do
    if [ -n "$(find "$lock" -maxdepth 0 -mmin +2 2>/dev/null)" ] && _guard_take "$lock" 5; then
      dead="$lock.stale.$tok.$i"
      if [ -n "$(find "$lock" -maxdepth 0 -mmin +2 2>/dev/null)" ] && mv "$lock" "$dead" 2>/dev/null; then rm -rf "$dead"; rmdir "$lock.break" 2>/dev/null || true; continue; fi
      rmdir "$lock.break" 2>/dev/null || true
    fi
    i=$((i + 1)); [ "$i" -le 300 ] || { echo "with_lock: timed out waiting for $lock" >&2; return 1; }
    sleep 0.1
  done
  printf '%s' "$tok" > "$lock/owner" 2>/dev/null
  "$@" && rc=0 || rc=$?
  _guard_take "$lock" 250 && got=1 || got=0
  if [ "$(cat "$lock/owner" 2>/dev/null)" = "$tok" ]; then rm -f "$lock/owner"; rmdir "$lock" 2>/dev/null || true; fi
  [ "$got" = 0 ] || rmdir "$lock.break" 2>/dev/null || true
  return "$rc"
}
