#!/usr/bin/env bash
set -euo pipefail

PID_DIR="${XDG_RUNTIME_DIR:-/tmp}"
PID_FILE="$PID_DIR/emachination_prompt_rig_linux.pid"

if [[ ! -f "$PID_FILE" ]]; then
  echo "No eMachination Prompt-Rig Linux hotkey-board PID file found: $PID_FILE"
  exit 0
fi

PID="$(python3 - <<PY
import json
from pathlib import Path
p = Path('$PID_FILE')
try:
    print(json.loads(p.read_text()).get('pid', ''))
except Exception:
    print('')
PY
)"

if [[ -z "$PID" ]]; then
  echo "PID file was unreadable; removing stale file: $PID_FILE"
  rm -f "$PID_FILE"
  exit 0
fi

if ! kill -0 "$PID" 2>/dev/null; then
  echo "Runtime PID is not active; removing stale file: $PID_FILE"
  rm -f "$PID_FILE"
  exit 0
fi

CMDLINE="$(tr '\0' ' ' < "/proc/$PID/cmdline" 2>/dev/null || true)"
if [[ "$CMDLINE" != *"hotkey_board_runtime.py"* ]] || [[ "$CMDLINE" != *"board_spec.json"* ]]; then
  echo "Refusing to stop PID $PID because it does not look like this hotkey-board runtime."
  echo "Command line: $CMDLINE"
  exit 1
fi

kill "$PID"
sleep 1
if kill -0 "$PID" 2>/dev/null; then
  kill -TERM "$PID" 2>/dev/null || true
fi
rm -f "$PID_FILE"
echo "Stopped eMachination CAD Patent Prompt-Rig Linux runtime PID $PID."
