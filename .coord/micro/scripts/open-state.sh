#!/bin/bash
set -euo pipefail
. "$(dirname "$0")/_lib.sh"
cat "$base/STATE.md"; echo; tail -60 "$base/SCRATCHPAD.md"; echo; bash "$base/scripts/handoff.sh" current || true
