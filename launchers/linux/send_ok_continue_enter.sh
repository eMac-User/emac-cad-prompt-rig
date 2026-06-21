#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SOCKET_PATH="${XDG_RUNTIME_DIR:-/run/user/$(id -u)}/emachination_prompt_rig_ydotool.sock"
export YDOTOOL_SOCKET="$SOCKET_PATH"

"$SCRIPT_DIR/start_ydotool_user_daemon.sh" >/dev/null

# Raw PageUp may still reach Konsole first. Ctrl+U clears recalled/raw line text.
ydotool key 29:1 22:1 22:0 29:0
ydotool type -- "Ok, continue"
ydotool key 28:1 28:0
