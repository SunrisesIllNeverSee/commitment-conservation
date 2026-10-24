#!/bin/bash
# Sign in: claim a role, then show repo health and the coordination board.
#   start.sh [ROLE] ["agent label"] ["writing in"] [--takeover]
# No ROLE: uses $COORD_ROLE, else slot 1 (deprecated; pass the role explicitly).
set -euo pipefail
repo="$(cd "$(dirname "$0")/../.." && pwd)"
scripts="$repo/.coord/micro/scripts"
. "$scripts/_lib.sh"
takeover=0; pos=()
for a in "$@"; do
  case "$a" in --takeover) takeover=1 ;; *) pos+=("$a") ;; esac
done
if [ "${#pos[@]}" -eq 0 ]; then
  if [ -n "${COORD_ROLE:-}" ]; then role="$COORD_ROLE"; else role="slot1"; fi
  echo "deprecated: pass the role explicitly (start.sh ROLE \"label\")" >&2
  pos=("$role")
fi
role="$(role_of "${pos[0]}")" || { echo "usage: start.sh ROLE [\"agent label\"] [\"writing in\"] [--takeover]   (roles: $(slots 2>/dev/null | tr '\n' ' '))" >&2; exit 2; }
pos[0]="$role"
claim="$state/.active-$role"
args=("${pos[@]}"); [ "$takeover" = 1 ] && args+=(--takeover)
# Same role + same label is a no-op only for the same session (or, with no session ids, an explicit label).
noop=0
if [ "$takeover" = 0 ] && [ -f "$claim" ] && [ "$(claim_get "$claim" label)" = "$(oneline "${pos[1]:-agent}")" ]; then
  csid="$(clean_sid "$(claim_get "$claim" sid)")"; mysid="$(clean_sid "${COORD_SESSION_ID:-}")"
  if [ -n "$csid" ] && [ "$csid" = "$mysid" ]; then noop=1
  elif [ -z "$csid" ] && [ -z "$mysid" ] && [ -n "${pos[1]:-}" ]; then noop=1; fi
fi
if [ "$noop" = 1 ]; then
  echo "role=$role already claimed ($(claim_get "$claim" label)); nothing to do"
else
  bash "$scripts/set-role.sh" "${args[@]}"
fi
if [ -f "$repo/.repo/scripts/repo_doctor.py" ]; then
  python3 "$repo/.repo/scripts/repo_doctor.py" || echo "(repo_doctor reported a problem; see above)"
fi
bash "$scripts/status.sh"
echo; echo '--- MACRO ---'; bash "$repo/.coord/bin/macro-status.sh" || true
