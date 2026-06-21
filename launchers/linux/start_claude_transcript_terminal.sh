#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
TRANSCRIPT_PATH="${VEYDRANET_TERMINAL_TRANSCRIPT:-${XDG_RUNTIME_DIR:-/tmp}/veydranet_terminal_transcript.log}"
TRANSCRIPT_PID_PATH="${TRANSCRIPT_PATH}.pid"
REGISTRY_PATH="${XDG_RUNTIME_DIR:-/tmp}/veydranet_terminal_transcripts.registry"
REQUESTED_PROFILE="${VEYDRANET_TRANSCRIPT_TERMINAL_PROFILE:-auto}"
SUPPORTED_PROFILES="auto konsole alacritty gnome-terminal blackbox cosmic kitty wezterm terminator"

mkdir -p "$(dirname "$TRANSCRIPT_PATH")"
export VEYDRANET_TERMINAL_TRANSCRIPT="$TRANSCRIPT_PATH"

if ! command -v script >/dev/null 2>&1; then
  echo "ERROR: script command not found. On Fedora, install: sudo dnf install -y util-linux-script" >&2
  exit 1
fi

_select_profile() {
  case "$REQUESTED_PROFILE" in
    auto) ;;
    konsole|alacritty|gnome-terminal|blackbox|cosmic|kitty|wezterm|terminator)
      printf '%s\n' "$REQUESTED_PROFILE"
      return 0
      ;;
    *)
      echo "ERROR: unknown VEYDRANET_TRANSCRIPT_TERMINAL_PROFILE='$REQUESTED_PROFILE'." >&2
      echo "Supported profiles: $SUPPORTED_PROFILES" >&2
      exit 1
      ;;
  esac

  if command -v konsole >/dev/null 2>&1; then
    printf '%s\n' "konsole"
  elif command -v alacritty >/dev/null 2>&1; then
    printf '%s\n' "alacritty"
  elif command -v cosmic-term >/dev/null 2>&1 || command -v cosmic-terminal >/dev/null 2>&1; then
    printf '%s\n' "cosmic"
  elif command -v blackbox-terminal >/dev/null 2>&1; then
    printf '%s\n' "blackbox"
  elif command -v gnome-terminal >/dev/null 2>&1; then
    printf '%s\n' "gnome-terminal"
  elif command -v kitty >/dev/null 2>&1; then
    printf '%s\n' "kitty"
  elif command -v wezterm >/dev/null 2>&1; then
    printf '%s\n' "wezterm"
  elif command -v terminator >/dev/null 2>&1; then
    printf '%s\n' "terminator"
  else
    echo "ERROR: auto mode found no supported terminal launcher." >&2
    echo "Supported profiles: $SUPPORTED_PROFILES" >&2
    exit 1
  fi
}

_require_profile_command() {
  case "$1" in
    konsole)
      command -v konsole >/dev/null 2>&1 || { echo "ERROR: profile 'konsole' requested but konsole is not installed." >&2; exit 1; }
      ;;
    alacritty)
      command -v alacritty >/dev/null 2>&1 || { echo "ERROR: profile 'alacritty' requested but alacritty is not installed." >&2; exit 1; }
      ;;
    cosmic)
      command -v cosmic-term >/dev/null 2>&1 || command -v cosmic-terminal >/dev/null 2>&1 || { echo "ERROR: profile 'cosmic' requested but neither cosmic-term nor cosmic-terminal is installed." >&2; exit 1; }
      ;;
    blackbox)
      command -v blackbox-terminal >/dev/null 2>&1 || { echo "ERROR: profile 'blackbox' requested but blackbox-terminal is not installed." >&2; exit 1; }
      ;;
    gnome-terminal)
      command -v gnome-terminal >/dev/null 2>&1 || { echo "ERROR: profile 'gnome-terminal' requested but gnome-terminal is not installed." >&2; exit 1; }
      ;;
    kitty)
      command -v kitty >/dev/null 2>&1 || { echo "ERROR: profile 'kitty' requested but kitty is not installed." >&2; exit 1; }
      ;;
    wezterm)
      command -v wezterm >/dev/null 2>&1 || { echo "ERROR: profile 'wezterm' requested but wezterm is not installed." >&2; exit 1; }
      ;;
    terminator)
      command -v terminator >/dev/null 2>&1 || { echo "ERROR: profile 'terminator' requested but terminator is not installed." >&2; exit 1; }
      ;;
  esac
}

_write_ready_record() {
  cat >> "$TRANSCRIPT_PATH" <<EOT

===== eMachination Prompt-Rig Claude transcript session started: $(date -Is) =====
VEYDRANET_TRANSCRIPT_LAUNCHER_READY
VEYDRANET_CLAUDE_TRANSCRIPT_LAUNCHER_READY
VEYDRANET_TRANSCRIPT_TERMINAL_PROFILE=$SELECTED_PROFILE
VEYDRANET_TRANSCRIPT_PATH=$TRANSCRIPT_PATH
VEYDRANET_TRANSCRIPT_PID_PATH=$TRANSCRIPT_PID_PATH
EOT

  printf 'VEYDRANET_TRANSCRIPT_LAUNCHER_READY\n'
  printf 'VEYDRANET_CLAUDE_TRANSCRIPT_LAUNCHER_READY\n'
  printf 'VEYDRANET_TRANSCRIPT_TERMINAL_PROFILE=%s\n' "$SELECTED_PROFILE"
  printf 'VEYDRANET_TRANSCRIPT_PATH=%s\n' "$TRANSCRIPT_PATH"
  printf 'VEYDRANET_TRANSCRIPT_PID_PATH=%s\n' "$TRANSCRIPT_PID_PATH"
}
_write_registry_record() {
  printf '{"transcript_path":"%s","pid_path":"%s","terminal_profile":"%s","launcher":"start_claude_transcript_terminal.sh"}\n' \
    "$TRANSCRIPT_PATH" "$TRANSCRIPT_PID_PATH" \
    "${SELECTED_PROFILE:-$REQUESTED_PROFILE}" \
    >> "$REGISTRY_PATH"
}

CLAUDE_COMMAND="cd '$REPO_ROOT' && exec script -a -f -c 'VEYDRANET_INNER_PID_PATH='$TRANSCRIPT_PID_PATH'; printf \"%s\n\" \"\$\$\" > \"\$VEYDRANET_INNER_PID_PATH\"; exec claude' '$TRANSCRIPT_PATH'"

INNER_COMMAND="$CLAUDE_COMMAND"

_launch_konsole() {
  exec konsole --workdir "$REPO_ROOT" -e bash -lc "$INNER_COMMAND"
}

_launch_alacritty() {
  exec alacritty -e bash -lc "$INNER_COMMAND"
}

_launch_cosmic() {
  if command -v cosmic-term >/dev/null 2>&1; then
    exec cosmic-term -e bash -lc "$INNER_COMMAND"
  fi
  exec cosmic-terminal -e bash -lc "$INNER_COMMAND"
}

_launch_blackbox() {
  exec blackbox-terminal -- bash -lc "$INNER_COMMAND"
}

_launch_gnome_terminal() {
  exec gnome-terminal --working-directory="$REPO_ROOT" -- bash -lc "$INNER_COMMAND"
}

_launch_kitty() {
  exec kitty --directory "$REPO_ROOT" bash -lc "$INNER_COMMAND"
}

_launch_wezterm() {
  exec wezterm start --cwd "$REPO_ROOT" -- bash -lc "$INNER_COMMAND"
}

_launch_terminator() {
  exec terminator --working-directory="$REPO_ROOT" -x bash -lc "$INNER_COMMAND"
}

SELECTED_PROFILE="$(_select_profile)"
_require_profile_command "$SELECTED_PROFILE"
_write_ready_record
_write_registry_record

case "$SELECTED_PROFILE" in
  konsole) _launch_konsole ;;
  alacritty) _launch_alacritty ;;
  cosmic) _launch_cosmic ;;
  blackbox) _launch_blackbox ;;
  gnome-terminal) _launch_gnome_terminal ;;
  kitty) _launch_kitty ;;
  wezterm) _launch_wezterm ;;
  terminator) _launch_terminator ;;
  *)
    echo "ERROR: selected unsupported terminal profile '$SELECTED_PROFILE'." >&2
    exit 1
    ;;
esac
