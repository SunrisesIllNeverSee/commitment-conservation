#!/bin/bash
# Claim a role slot from the roster. One agent per slot; the claim also records where you are writing.
#   set-role.sh ROLE ["agent label"] ["writing in"] [--takeover]
# Exit 3 when the slot is held by someone else. --takeover replaces a claim left by a session that ended without signing out.
set -euo pipefail
. "$(dirname "$0")/_lib.sh"
takeover=0; role=""; label=""; lane=""; n=0
for a in "$@"; do
  case "$a" in
    --takeover) takeover=1 ;;
    *) n=$((n+1)); case $n in 1) role="$a";; 2) label="$a";; 3) lane="$a";; esac ;;
  esac
done
role="$(role_of "$role")" || { echo "usage: $0 ROLE [\"agent label\"] [\"writing in\"] [--takeover]   (roles: $(slots 2>/dev/null | tr '\n' ' '))" >&2; exit 2; }
label="$(oneline "${label:-agent}")"; lane="$(oneline "${lane:-not stated}")"
sid="$(clean_sid "${COORD_SESSION_ID:-}")"
claim="$state/.active-$role"
# Takeover is compare-and-swap: remember the claim being replaced, and refuse if it changed before we hold the lock.
observed=""; [ "$takeover" = 1 ] && [ -f "$claim" ] && observed="$(cat "$claim" 2>/dev/null)" || true
# Takeover and create run under the claim lock so concurrent claimers and signouts cannot interleave.
do_claim() {
  local prev="" psid=""
  if [ "$takeover" = 1 ] && [ "$(cat "$claim" 2>/dev/null)" != "$observed" ]; then return 5; fi
  if [ "$takeover" = 1 ] && [ -f "$claim" ]; then
    prev="$(tr '\n' ' ' < "$claim")"; psid="$(clean_sid "$(claim_get "$claim" sid)")"
    rm -f "$claim"
    [ -z "$psid" ] || rm -f "$state/.sid-$psid"
  fi
  # noclobber makes the claim atomic even against writers that skip the lock.
  if ! ( set -o noclobber; printf 'label=%s\nlane=%s\nsince=%s\nsid=%s\n' "$label" "$lane" "$(utc)" "$sid" > "$claim" ) 2>/dev/null; then
    return 3
  fi
  # Map the session to its role so later scripts and hooks know who is acting.
  if [ -n "$sid" ]; then printf '%s\n' "$role" > "$state/.sid-$sid"; fi
  if [ -n "$prev" ]; then post "$role" ALL "took over a stale $role claim (${prev% })"; fi
  post "$role" ALL "signed in ($label). Writing in: $lane"
}
rc=0; with_lock "claim-$role" do_claim || rc=$?
if [ "$rc" = 3 ]; then
  echo "refused: $role is already held — $(tr '\n' ' ' < "$claim" 2>/dev/null)" >&2
  echo "  check bash .coord/micro/scripts/status.sh first. Take over only if that session has ended" >&2
  echo "  (flagged STALE after 24h, or OWNER says so): bash .coord/bin/start.sh $role \"$label\" \"$lane\" --takeover" >&2
  exit 3
fi
if [ "$rc" = 5 ]; then echo "refused: claim changed while taking over $role — re-check status" >&2; exit 3; fi
[ "$rc" = 0 ] || exit "$rc"
echo "role=$role claimed ($label); writing in: $lane"
