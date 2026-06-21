#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
WATCHER="$REPO_ROOT/tools/linux_scrolllock_watcher.py"
BOARD_LAUNCHER="$REPO_ROOT/launchers/linux/start_hotkey_board.sh"
PID_DIR="${XDG_RUNTIME_DIR:-/tmp}"
PID_FILE="$PID_DIR/emachination_prompt_rig_scrolllock_watcher.pid"
LOG_FILE="$PID_DIR/emachination_prompt_rig_scrolllock_watcher.log"
YDOTOOL_DAEMON="$REPO_ROOT/launchers/linux/start_ydotool_user_daemon.sh"

if [[ -f "$PID_FILE" ]]; then
  OLD_PID="$(cat "$PID_FILE" 2>/dev/null || true)"
  if [[ -n "$OLD_PID" ]] && kill -0 "$OLD_PID" 2>/dev/null; then
    echo "eMachination CAD Patent Prompt-Rig ScrollLock watcher is already running: PID $OLD_PID"
    echo "PID file: $PID_FILE"
    echo "Log file: $LOG_FILE"
    exit 0
  fi
  rm -f "$PID_FILE"
fi

: >"$LOG_FILE"

# Insert/PageUp require ydotoold. Start it before the watcher so hotkey
# actions never trigger an interactive sudo password prompt.
if ! bash "$YDOTOOL_DAEMON" >>"$LOG_FILE" 2>&1; then
  echo "ERROR: eMachination CAD Patent Prompt-Rig ydotool daemon is not ready; Insert/PageUp helpers would fail."
  echo "Log file: $LOG_FILE"
  sed -n '1,180p' "$LOG_FILE" 2>/dev/null || true
  exit 1
fi

nohup python3 "$WATCHER" \
  --launcher "$BOARD_LAUNCHER" \
  >"$LOG_FILE" 2>&1 &

NEW_PID="$!"
echo "$NEW_PID" > "$PID_FILE"

sleep 1

if ! kill -0 "$NEW_PID" 2>/dev/null; then
  echo "ERROR: eMachination CAD Patent Prompt-Rig ScrollLock watcher exited immediately."
  echo "PID: $NEW_PID"
  echo "PID file: $PID_FILE"
  echo "Log file: $LOG_FILE"
  sed -n '1,240p' "$LOG_FILE" 2>/dev/null || true
  rm -f "$PID_FILE"
  exit 1
fi

echo "Started eMachination CAD Patent Prompt-Rig ScrollLock watcher."
echo "PID: $NEW_PID"
echo "PID file: $PID_FILE"
echo "Log file: $LOG_FILE"
echo "Launcher: $BOARD_LAUNCHER"
