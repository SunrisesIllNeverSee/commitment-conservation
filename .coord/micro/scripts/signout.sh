#!/bin/bash
# Release your role and post the signout line to the scratchpad.
#   signout.sh [ROLE] ["summary"] [--force] [--takeover]
# No ROLE: your role is found from COORD_ROLE, the session map or the single held claim (one non-role argument is then the summary).
# --force posts a signout even when the role is not claimed. --takeover releases a claim owned by another session.
set -euo pipefail
. "$(dirname "$0")/_lib.sh"
force=0; takeover=0; args=()
for a in "$@"; do
  case "$a" in
    --force) force=1 ;;
    --takeover) takeover=1 ;;
    *) args+=("$a") ;;
  esac
done
role=""; summary=""
if [ "${#args[@]}" -gt 0 ] && role="$(role_of "${args[0]}")"; then
  summary="${args[*]:1}"
else
  role="$(my_role 2>/dev/null)" || { echo "usage: $0 [ROLE] [\"summary\"] [--force] [--takeover]   (could not tell which role is yours; pass it explicitly)" >&2; exit 2; }
  summary="${args[*]:-}"
  echo "deprecated: pass the role explicitly (signout.sh $role \"summary\")" >&2
fi
claim="$state/.active-$role"
mysid="$(clean_sid "${COORD_SESSION_ID:-}")"
# Check, release and map cleanup run under the claim lock so a new holder's claim is never deleted.
do_signout() {
  local csid=""
  if [ ! -f "$claim" ] && [ "$force" = 0 ]; then
    echo "refused: $role is not claimed, so there is nothing to release (add --force to post a signout line anyway)" >&2; return 4
  fi
  [ -f "$claim" ] && csid="$(clean_sid "$(claim_get "$claim" sid)")"
  if [ -n "$csid" ] && [ "$csid" != "$mysid" ] && [ "$takeover" = 0 ]; then
    echo "refused: $role is held by another session ($csid); add --takeover only if that session has ended" >&2; return 4
  fi
  printf '\n### ⤷ %s → ALL: signout (%s)\n%s\n' "$role" "$(utc)" "$(oneline "${summary:-session complete}")" >> "$pad"
  rm -f "$claim"
  [ -z "$csid" ] || rm -f "$state/.sid-$csid"
  local m
  for m in "$state"/.sid-*; do
    if [ -f "$m" ] && [ "$(head -1 "$m" | tr -d '[:space:]')" = "$role" ]; then rm -f "$m"; fi
  done
  return 0
}
rc=0; with_lock "claim-$role" do_signout || rc=$?
[ "$rc" = 0 ] || exit "$rc"
echo "signed out: $role"
