#!/bin/bash
# Save your slot in STATE.md. Only the "## <SLOT> — latest save" section is replaced (appended if missing);
# a legacy "## Latest Save" section is left alone. Safe to run from several agents at once.
#   save-state.sh [ROLE] "summary"      ROLE defaults to your identity (COORD_ROLE, session map, sole claim)
set -euo pipefail
. "$(dirname "$0")/_lib.sh"
role=""
if [ "$#" -ge 2 ] && role="$(role_of "$1")"; then shift; else role="$(my_role)" || { echo "usage: $0 [ROLE] \"summary\" (cannot tell which role you are; pass ROLE)" >&2; exit 2; }; fi
summary="$(oneline "$*")"
[ -n "${summary// /}" ] || { echo "usage: $0 [ROLE] \"summary\"" >&2; exit 2; }
do_save() {
  python3 - "$base/STATE.md" "$role" "$summary" "$(utc)" "$$" <<'PY' || return 1
import os, re, sys
p, role, summary, now, pid = sys.argv[1:6]
try:
    with open(p, newline='') as f: s = f.read()
except FileNotFoundError:
    s = ''
header = '## %s — latest save' % role
block = '%s\n\n- Time: %s\n- Summary: %s\n\n' % (header, now, summary.strip())
section = re.compile(r'(?ms)^' + re.escape(header) + r'[ \t]*\n.*?(?=^## |\Z)')
if section.search(s):
    s = section.sub(lambda m: block, s, count=1)
else:
    if s and not s.endswith('\n'): s += '\n'
    if s and not s.endswith('\n\n'): s += '\n'
    s += block
tmp = '%s.tmp.%s' % (p, pid)
with open(tmp, 'w', newline='') as f: f.write(s)
os.replace(tmp, p)
PY
}
with_lock state do_save
echo "state saved: $role"
