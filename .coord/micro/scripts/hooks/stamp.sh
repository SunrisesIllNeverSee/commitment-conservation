#!/bin/bash
# PostToolUse edit hook (Claude Code, Devin, Codex adapters). Reads the hook JSON on stdin and appends
#   <UTC> <ROLE|UNKNOWN> <path>
# to state/ACTIVITY.log. It NEVER edits any other file: no frontmatter stamping, shared files stay untouched.
# --log-only is accepted for adapter compatibility; logging is the only mode. A hook must never break the agent's edit,
# so every failure path exits 0 silently. Runs under macOS bash 3.2 (no readarray).
set +e
payload="$(cat 2>/dev/null)"
[ -n "$payload" ] || exit 0
. "$(dirname "$0")/../_lib.sh" 2>/dev/null || exit 0
parsed="$(printf '%s' "$payload" | python3 -c '
import json, os, sys
try:
    d = json.load(sys.stdin)
    ti = d.get("tool_input") or {}
    f = ti.get("file_path") or d.get("file_path") or (d.get("tool_response") or {}).get("filePath") or ""
    sid = d.get("session_id") or ""
    if not isinstance(f, str) or not isinstance(sid, str) or not f:
        raise ValueError
    repo = os.path.realpath(sys.argv[1])
    a = f if os.path.isabs(f) else os.path.join(repo, f)
    a = os.path.realpath(a)
    if a != repo and not a.startswith(repo + os.sep):
        raise ValueError
    print(os.path.relpath(a, repo).replace("\n", " "))
    print(sid.replace("\n", " "))
except Exception:
    pass
' "$repo" 2>/dev/null)"
rel="$(printf '%s\n' "$parsed" | sed -n 1p)"; sid="$(printf '%s\n' "$parsed" | sed -n 2p)"
[ -n "$rel" ] || exit 0
[ -n "${COORD_SESSION_ID:-}" ] || COORD_SESSION_ID="$sid"
role="$(my_role 2>/dev/null)"
if [ -z "$role" ]; then
  held="$(held_roles | tr '\n' '|')"; held="${held%|}"
  role="${held:-UNKNOWN}"
fi
printf '%s %s %s\n' "$(date -u '+%Y-%m-%d %H:%M UTC')" "$role" "$rel" >> "$state/ACTIVITY.log" 2>/dev/null
exit 0
