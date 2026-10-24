#!/bin/bash
# Update where your role is writing, so the other agent can see it in status.sh. Never creates a claim.
#   lane.sh ROLE "paths or area"
set -euo pipefail
. "$(dirname "$0")/_lib.sh"
role="$(role_of "${1:-}")" && [ -n "${2:-}" ] || { echo "usage: $0 ROLE \"paths or area\"" >&2; exit 2; }
claim="$state/.active-$role"
lane="$(oneline "$2")"
# Under the claim lock so a concurrent signout cannot be undone by this rewrite.
update_lane() {
  [ -f "$claim" ] || return 4
  L="$lane" awk '/^lane=/ { print "lane=" ENVIRON["L"]; next } { print }' "$claim" > "$claim.tmp" && mv "$claim.tmp" "$claim"
}
rc=0; with_lock "claim-$role" update_lane || rc=$?
if [ "$rc" = 4 ]; then echo "refused: $role is not claimed; run start.sh $role first" >&2; exit 4; fi
[ "$rc" = 0 ] || exit "$rc"
post "$role" ALL "now writing in: $lane"
echo "$role writing in: $lane"
