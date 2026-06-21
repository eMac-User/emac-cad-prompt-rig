#!/usr/bin/env bash
set -euo pipefail

PID_DIR="${XDG_RUNTIME_DIR:-/tmp}"
PID_FILE="$PID_DIR/emachination_prompt_rig_scrolllock_watcher.pid"

if [[ ! -f "$PID_FILE" ]]; then
  echo "No eMachination CAD Patent Prompt-Rig ScrollLock watcher PID file found: $PID_FILE"
  exit 0
fi

PID="$(cat "$PID_FILE" 2>/dev/null || true)"

if [[ -z "$PID" ]]; then
  echo "PID file was unreadable; removing stale file: $PID_FILE"
  rm -f "$PID_FILE"
  exit 0
fi

if ! kill -0 "$PID" 2>/dev/null; then
  echo "Watcher PID is not active; removing stale file: $PID_FILE"
  rm -f "$PID_FILE"
  exit 0
fi

CMDLINE="$(tr '\0' ' ' < "/proc/$PID/cmdline" 2>/dev/null || true)"
if [[ "$CMDLINE" != *"linux_scrolllock_watcher.py"* ]]; then
  echo "Refusing to stop PID $PID because it does not look like the eMachination CAD Patent Prompt-Rig ScrollLock watcher."
  echo "Command line: $CMDLINE"
  exit 1
fi

kill "$PID"
sleep 1
if kill -0 "$PID" 2>/dev/null; then
  kill -TERM "$PID" 2>/dev/null || true
fi

rm -f "$PID_FILE"
echo "Stopped eMachination CAD Patent Prompt-Rig ScrollLock watcher PID $PID."
