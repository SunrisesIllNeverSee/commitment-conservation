#!/bin/bash
# SessionStart hook (Claude Code: .claude/settings.json; Devin: .devin/hooks.v1.json; Codex: its hook config).
# Prints who holds which role and how to sign in. Writes no shared pointer (no .session-current): each session
# is identified by its own COORD_SESSION_ID. When the host provides CLAUDE_ENV_FILE and no id is set yet, a fresh id
# (the hook payload's session_id, else generated; [A-Za-z0-9._-] only) is exported through it so later commands
# in this session can be mapped to their role. Never fails the session.
set +e
payload="$(cat 2>/dev/null)"
. "$(dirname "$0")/../_lib.sh" 2>/dev/null || exit 0
sid="$(clean_sid "${COORD_SESSION_ID:-}")"
if [ -z "$sid" ] && [ -n "${CLAUDE_ENV_FILE:-}" ]; then
  sid="$(printf '%s' "$payload" | python3 -c 'import json,sys
try: print(json.load(sys.stdin).get("session_id") or "")
except Exception: pass' 2>/dev/null | head -1)"
  sid="$(clean_sid "$sid")"
  [ -n "$sid" ] || sid="session-$(date -u +%Y%m%d%H%M%S)-$$-$RANDOM"
  printf 'export COORD_SESSION_ID=%s\n' "$sid" >> "$CLAUDE_ENV_FILE" 2>/dev/null
fi
held="$(held_roles | tr '\n' ' ')"
echo "Coordination: roles held: ${held:-none}. Sign in with: bash .coord/bin/start.sh <ROLE> \"label\" \"writing in\" (roles: $(slots 2>/dev/null | tr '\n' ' ')). Read .coord/micro/handoffs/ONBOARDING.md."
exit 0
