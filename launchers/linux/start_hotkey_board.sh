#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
SPEC_PATH="$REPO_ROOT/build/linux_hotkey_board/board_spec.json"
RUNTIME="$REPO_ROOT/src/linux/hotkey_board_runtime.py"
COMPILER="$REPO_ROOT/tools/compile_hotkey_board_linux.py"
PID_DIR="${XDG_RUNTIME_DIR:-/tmp}"
PID_FILE="$PID_DIR/emachination_prompt_rig_linux.pid"
LOG_FILE="$PID_DIR/emachination_prompt_rig_linux.log"

# Default to provider auto mode so Copy Terminal Buffer prefers a live eMachination Prompt-Rig
# transcript/registry session and only reports full/history copies by default.
# Explicit visible/current fallback remains available when the operator chooses it:
#   VEYDRANET_TERMINAL_COPY_MODE=konsole bash launchers/linux/start_hotkey_board.sh
export VEYDRANET_TERMINAL_COPY_MODE="${VEYDRANET_TERMINAL_COPY_MODE:-auto}"

if [[ -f "$PID_FILE" ]]; then
  OLD_PID="$(python3 - <<PY 2>/dev/null || true
import json
from pathlib import Path
p = Path("$PID_FILE")
try:
    print(json.loads(p.read_text()).get("pid", ""))
except Exception:
    print("")
PY
)"
  if [[ -n "$OLD_PID" ]] && kill -0 "$OLD_PID" 2>/dev/null; then
    echo "eMachination CAD Patent Prompt-Rig Linux runtime is already running: PID $OLD_PID"
    echo "PID file: $PID_FILE"
    exit 0
  fi
  rm -f "$PID_FILE"
fi

cd "$REPO_ROOT"

python3 "$COMPILER" --repo-root "$REPO_ROOT"

: >"$LOG_FILE"

nohup python3 "$RUNTIME" \
  --repo-root "$REPO_ROOT" \
  --spec "$SPEC_PATH" \
  --open-board \
  --gui-backend auto \
  --pid-file "$PID_FILE" \
  >"$LOG_FILE" 2>&1 &

NEW_PID="$!"

python3 - <<PY
import json
from pathlib import Path
Path("$PID_FILE").write_text(json.dumps({"pid": int("$NEW_PID")}) + "\n", encoding="utf-8")
PY

sleep 1

if ! kill -0 "$NEW_PID" 2>/dev/null; then
  echo "ERROR: eMachination CAD Patent Prompt-Rig Linux runtime exited immediately."
  echo "PID: $NEW_PID"
  echo "PID file: $PID_FILE"
  echo "Log file: $LOG_FILE"
  sed -n '1,240p' "$LOG_FILE" 2>/dev/null || true
  rm -f "$PID_FILE"
  exit 1
fi

echo "Started eMachination CAD Patent Prompt-Rig Linux runtime."
echo "PID: $NEW_PID"
echo "PID file: $PID_FILE"
echo "Log file: $LOG_FILE"
echo "Spec: $SPEC_PATH"
echo "Terminal copy mode: $VEYDRANET_TERMINAL_COPY_MODE"
