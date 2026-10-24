#!/bin/bash
# Who is working, where they are writing, active handoffs, roster, recent edits, scratchpad tail. Read-only.
set -euo pipefail
. "$(dirname "$0")/_lib.sh"
echo '--- WHO IS WORKING ---'
found=0
for r in $(slots 2>/dev/null); do
  c="$state/.active-$r"; [ -f "$c" ] || continue; found=1
  since="$(claim_get "$c" since)"; label="$(claim_get "$c" label)"; lane="$(claim_get "$c" lane)"
  age="$(python3 -c 'import sys,datetime as d
try:
 t=d.datetime.strptime(sys.argv[1],"%Y-%m-%d %H:%M UTC").replace(tzinfo=d.timezone.utc); h=(d.datetime.now(d.timezone.utc)-t).total_seconds()/3600
 print(f"{h:.1f}h"+(" — STALE? no signout after 24h" if h>24 else ""))
except Exception: print("?")' "$since" 2>/dev/null || echo '?')"
  printf '%-6s %s | writing in: %s | since %s (%s)\n' "$r" "${label:-?}" "${lane:-not stated}" "${since:-?}" "$age"
done
[ $found = 1 ] || echo '(no role claimed)'
echo; echo '--- ACTIVE HANDOFFS ---'
ls -1 "$base/handoffs/active"/*.md 2>/dev/null || echo '(none)'
echo; echo '--- ROSTER ---'; sed -n '/^| /p' "$state/ROSTER.md" 2>/dev/null || true
echo; echo '--- RECENT EDITS (ACTIVITY.log) ---'; tail -15 "$state/ACTIVITY.log" 2>/dev/null || echo '(none yet)'
echo; echo '--- SCRATCHPAD (last 40) ---'; tail -40 "$pad" 2>/dev/null || true
