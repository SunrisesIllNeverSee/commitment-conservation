#!/bin/bash
# Per-slot, never-overwritten handoffs in .coord/micro/handoffs/active/<SLOT>-<UTC YYYYMMDDTHHMMSSZ>[-N].md
#   handoff.sh generate [ROLE]   write a new handoff skeleton and print its path
#   handoff.sh current [ROLE]    print the newest handoff for the slot (falls back to legacy flat handoffs/*.md)
# ROLE defaults to your identity (COORD_ROLE, session map, sole claim); rep1/rep2/slotN aliases work.
set -euo pipefail
. "$(dirname "$0")/_lib.sh"
dir="$base/handoffs"; act="$dir/active"
# Newest handoff for slot $1: order by stamp, then by -N suffix (plain name sorts before -2 in time, not in ls).
newest() {
  local n; n="$(ls -1 "$act" 2>/dev/null | grep -E "^$1-[0-9]{8}T[0-9]{6}Z(-[0-9]+)?\.md\$" | awk -v p="$1-" '
    { s = substr($0, length(p) + 1); suf = 1
      if (length(s) > 19) { x = substr(s, 18); sub(/\.md$/, "", x); suf = x + 0 }
      printf "%s %06d %s\n", substr(s, 1, 16), suf, $0 }' | sort | tail -1 | cut -d' ' -f3-)" || true
  [ -z "$n" ] || printf '%s/%s' "$act" "$n"
}
# Pre-1.1 handoffs (HANDOFF_<ROLE>_<date>.md, flat or in active/): with a role, that role's newest by mtime (as 1.0.0
# did); only if there is none, the newest of any role. Without a role, the newest of any.
legacy() {
  local f=""
  if [ -n "${1:-}" ]; then f="$(ls -1t "$dir"/HANDOFF_"$1"_*.md "$act"/HANDOFF_"$1"_*.md 2>/dev/null | head -1 || true)"; fi
  [ -n "$f" ] || f="$(ls -1t "$dir"/HANDOFF_*.md "$act"/HANDOFF_*.md 2>/dev/null | head -1 || true)"
  printf '%s' "$f"
}
cmd="${1:-current}"
case "$cmd" in
 generate)
   role="$(my_role "${2:-}")" || { echo "usage: $0 generate [ROLE] (cannot tell which role you are; pass ROLE)" >&2; exit 2; }
   mkdir -p "$act"
   stamp="$(date -u +%Y%m%dT%H%M%SZ)"; n=1; file="$act/$role-$stamp.md"
   # noclobber makes creation atomic: whoever creates the name owns it, everyone else takes the next suffix.
   until ( set -C; : > "$file" ) 2>/dev/null; do n=$((n + 1)); file="$act/$role-$stamp-$n.md"; [ "$n" -lt 1000 ] || { echo "handoff: cannot find a free name" >&2; exit 1; }; done
   branch="$(git -C "$repo" branch --show-current 2>/dev/null || echo '?')"
   head="$(git -C "$repo" rev-parse --short HEAD 2>/dev/null || echo '?')"
   dirty="$(git -C "$repo" status --porcelain 2>/dev/null | wc -l | tr -d ' ')"
   cat > "$file" <<HANDOFF
---
type: Handoff
title: ${role} Handoff ${stamp}
description: Handoff from the ${role} session; read before resuming ${role} work.
tags: [repo-standard, coordination, handoff]
timestamp: $(date -u '+%Y-%m-%d')
---

# ${role} Handoff — ${stamp}

Git at generation: branch \`${branch}\` @ \`${head}\`, ${dirty} uncommitted path(s).

## Read this first
- (fill in: files the next ${role} must read, in order)

## Current state
- (fill in)

## Completed
- (fill in)

## Next
- (fill in)

## Blockers / cautions
- (fill in)

## Key files
- (fill in)
HANDOFF
   echo "$file" ;;
 current)
   if role="$(my_role "${2:-}")"; then roles="$role"
   elif [ -n "${2:-}" ]; then echo "usage: $0 current [ROLE]" >&2; exit 2
   else roles="$(slots)"; fi
   shown=0
   for r in $roles; do
     f="$(newest "$r")"; [ -n "$f" ] || continue; shown=1
     [ "$(printf '%s\n' "$roles" | wc -l | tr -d ' ')" -le 1 ] || echo "=== $r: ${f#"$repo"/}"
     cat "$f"
   done
   if [ $shown = 0 ]; then
     f="$(legacy "${role:-}")"
     if [ -n "$f" ]; then echo "(no per-slot handoff yet; newest legacy handoff: ${f#"$repo"/})"; cat "$f"; else echo '(no active handoff)'; fi
   fi ;;
 *) echo "usage: $0 generate [ROLE] | current [ROLE]" >&2; exit 2;;
esac
