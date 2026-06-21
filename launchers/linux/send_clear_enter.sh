#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SOCKET_PATH="${XDG_RUNTIME_DIR:-/run/user/$(id -u)}/emachination_prompt_rig_ydotool.sock"
export YDOTOOL_SOCKET="$SOCKET_PATH"

"$SCRIPT_DIR/start_ydotool_user_daemon.sh" >/dev/null

# eMachination Prompt-Rig Insert baseline:
# - Keep the working focus-based ydotool path.
# - Do not replace this with Konsole DBus without an explicit rollback-safe slice.
# - Do not send Ctrl+C here; it can cancel the shell running the proof/action and
#   turn a clear action into broken text such as "uclear".
# - Raw Insert may still reach Konsole first. Ctrl+U clears the active shell line.
SETTLE_SECONDS="${VEYDRANET_CLEAR_ENTER_SETTLE_SECONDS:-0.08}"
STEP_SECONDS="${VEYDRANET_CLEAR_ENTER_STEP_SECONDS:-0.03}"

sleep "$SETTLE_SECONDS"

# Ctrl+U clears any raw Insert escape text or prompt input before running clear.
# Evdev: LeftCtrl=29, U=22.
ydotool key 29:1 22:1 22:0 29:0
sleep "$STEP_SECONDS"

# Run the intended shell action.
ydotool type -- "clear"
sleep "$STEP_SECONDS"
ydotool key 28:1 28:0
