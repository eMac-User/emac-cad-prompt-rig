#!/usr/bin/env bash
set -euo pipefail

SOCKET_PATH="${XDG_RUNTIME_DIR:-/run/user/$(id -u)}/emachination_prompt_rig_ydotool.sock"
LOG_FILE="${XDG_RUNTIME_DIR:-/tmp}/emachination_prompt_rig_ydotoold.log"
USER_ID="$(id -u)"
USER_GID="$(id -g)"
YDOTOOLD_BIN="$(command -v ydotoold || true)"

if [[ -z "$YDOTOOLD_BIN" ]]; then
  echo "ERROR: ydotoold not found; install ydotool before using Insert/PageUp helpers." >&2
  exit 1
fi

if pgrep -af "ydotoold.*emachination_prompt_rig_ydotool.sock" >/dev/null 2>&1 && [[ -S "$SOCKET_PATH" ]]; then
  echo "eMachination CAD Patent Prompt-Rig ydotool daemon is already running."
  echo "Socket: $SOCKET_PATH"
  exit 0
fi

rm -f "$SOCKET_PATH"
: >"$LOG_FILE"

# Noninteractive only. Hotkey actions must never trigger a sudo password prompt.
# Install /etc/sudoers.d/emachination-prompt-rig-ydotoold with the setup command before relying
# on Insert/PageUp after login/reboot.
if ! sudo -n -b "$YDOTOOLD_BIN" \
  --socket-path="$SOCKET_PATH" \
  --socket-own="$USER_ID:$USER_GID" \
  >>"$LOG_FILE" 2>&1; then
  cat >&2 <<ERR
ERROR: could not start eMachination CAD Patent Prompt-Rig ydotool daemon noninteractively.
This hotkey path must not prompt for sudo during Insert/PageUp.
Install the narrow sudoers rule for ydotoold, then start the watcher again.
Socket: $SOCKET_PATH
Log file: $LOG_FILE
ERR
  exit 1
fi

for _ in 1 2 3 4 5 6 7 8 9 10; do
  if [[ -S "$SOCKET_PATH" ]]; then
    echo "Started eMachination CAD Patent Prompt-Rig ydotool daemon."
    echo "Socket: $SOCKET_PATH"
    echo "Log file: $LOG_FILE"
    exit 0
  fi
  sleep 0.2
done

echo "ERROR: ydotool daemon socket was not created." >&2
echo "Socket: $SOCKET_PATH" >&2
echo "Log file: $LOG_FILE" >&2
sed -n '1,160p' "$LOG_FILE" >&2 || true
exit 1
