#!/usr/bin/env bash
set -Eeuo pipefail

APP_NAME="VeydraNet AI Hotkey Board Espanso Linux Installer"

YAML_NAME="veydranet_prompt_board.yml"
REPORT_NAME="veydranet_prompt_board_report.md"
TRIGGER_PREFIX="vhb"
PRIMARY_TEST_TRIGGER=":vhb-ci-p01"

print_step() {
  printf '\n## %s\n' "$1"
}

print_warn() {
  printf '\nWARNING: %s\n' "$1" >&2
}

print_error() {
  printf '\nERROR: %s\n' "$1" >&2
}

find_repo_root() {
  local script_dir
  local dir

  script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
  dir="$script_dir"

  while [[ "$dir" != "/" ]]; do
    if [[ -f "$dir/prompts/index.ini" && -f "$dir/tools/export_prompts_to_espanso.py" ]]; then
      printf '%s\n' "$dir"
      return 0
    fi

    dir="$(dirname -- "$dir")"
  done

  return 1
}

parse_espanso_config_dir() {
  local path_output="$1"

  printf '%s\n' "$path_output" |
    awk -F ':' '
      BEGIN { IGNORECASE = 1 }
      /^[[:space:]]*Config[[:space:]]*:/ {
        $1 = ""
        sub(/^:/, "")
        sub(/^[[:space:]]+/, "")
        sub(/[[:space:]]+$/, "")
        print
        exit
      }
    '
}

print_trigger_list() {
  local yaml_path="$1"

  awk -F '"' '
    /^[[:space:]]*-[[:space:]]*trigger:[[:space:]]*"/ {
      print "  " $2
      count++
      if (count >= 8) {
        exit
      }
    }
  ' "$yaml_path"
}

main() {
  print_step "$APP_NAME"

  local repo_root
  if ! repo_root="$(find_repo_root)"; then
    print_error "Could not find repo root. Expected prompts/index.ini and tools/export_prompts_to_espanso.py above this installer."
    exit 1
  fi

  local exporter="$repo_root/tools/export_prompts_to_espanso.py"
  local build_dir="$repo_root/build/espanso_export"
  local generated_yaml="$build_dir/$YAML_NAME"
  local generated_report="$build_dir/$REPORT_NAME"
  local manual_test_file="$build_dir/manual_gui_test.txt"

  print_step "Resolved repo paths"
  printf 'Repo root:        %s\n' "$repo_root"
  printf 'Exporter:         %s\n' "$exporter"
  printf 'Build/export dir: %s\n' "$build_dir"

  if [[ ! -f "$exporter" ]]; then
    print_error "Exporter not found: $exporter"
    exit 1
  fi

  local python_bin
  python_bin="$(command -v python3 || true)"
  if [[ -z "$python_bin" ]]; then
    print_error "python3 was not found on PATH."
    exit 1
  fi

  local espanso_bin
  espanso_bin="$(command -v espanso || true)"
  if [[ -z "$espanso_bin" ]]; then
    print_error "espanso was not found on PATH."
    print_error "Install and verify Espanso for this Linux desktop session first, then rerun this installer."
    exit 1
  fi

  print_step "Resolved required commands"
  printf 'python3: %s\n' "$python_bin"
  printf 'espanso: %s\n' "$espanso_bin"

  local session_type="${XDG_SESSION_TYPE:-unknown}"

  print_step "Desktop session"
  printf 'XDG_SESSION_TYPE: %s\n' "$session_type"

  if [[ "$session_type" == "wayland" ]]; then
    print_warn "Wayland session detected."
    print_warn "This installer can install the prompt board YAML, but it cannot prove GUI text injection."
    print_warn "Espanso Wayland support/session compatibility must already work for this user's desktop session."
  fi

  print_step "Resolving Espanso config path"

  local espanso_path_output
  if ! espanso_path_output="$("$espanso_bin" path 2>&1)"; then
    print_error "espanso path failed. Output:"
    printf '%s\n' "$espanso_path_output" >&2
    exit 1
  fi

  local espanso_config_dir
  espanso_config_dir="$(parse_espanso_config_dir "$espanso_path_output")"

  if [[ -z "$espanso_config_dir" ]]; then
    print_error "Could not parse Espanso config directory from espanso path output:"
    printf '%s\n' "$espanso_path_output" >&2
    exit 1
  fi

  local match_dir="$espanso_config_dir/match"
  local installed_yaml="$match_dir/$YAML_NAME"

  printf 'Espanso config dir: %s\n' "$espanso_config_dir"
  printf 'Espanso match dir:  %s\n' "$match_dir"
  printf 'Install target:     %s\n' "$installed_yaml"

  print_step "Generating Espanso YAML from prompt board"

  mkdir -p "$build_dir"
  rm -f "$generated_yaml" "$generated_report"
  : > "$manual_test_file"

  "$python_bin" "$exporter" \
    --repo-root "$repo_root" \
    --output "$generated_yaml" \
    --report "$generated_report" \
    --trigger-prefix "$TRIGGER_PREFIX"

  if [[ ! -s "$generated_yaml" ]]; then
    print_error "Generated YAML is missing or empty: $generated_yaml"
    exit 1
  fi

  if [[ ! -s "$generated_report" ]]; then
    print_error "Generated report is missing or empty: $generated_report"
    exit 1
  fi

  if ! grep -q 'trigger: ":vhb-ci-p01"' "$generated_yaml"; then
    print_error "Generated YAML does not contain expected test trigger: $PRIMARY_TEST_TRIGGER"
    exit 1
  fi

  print_step "Generated files"
  printf 'Generated YAML:   %s\n' "$generated_yaml"
  printf 'Generated report: %s\n' "$generated_report"
  printf 'Manual test file: %s\n' "$manual_test_file"

  print_step "Installing YAML into Espanso match directory"

  mkdir -p "$match_dir"
  install -m 0644 "$generated_yaml" "$installed_yaml"

  if [[ ! -s "$installed_yaml" ]]; then
    print_error "Installed YAML is missing or empty: $installed_yaml"
    exit 1
  fi

  if ! grep -q 'trigger: ":vhb-ci-p01"' "$installed_yaml"; then
    print_error "Installed YAML does not contain expected test trigger: $PRIMARY_TEST_TRIGGER"
    exit 1
  fi

  printf 'Installed YAML: %s\n' "$installed_yaml"
  printf 'Verified trigger: %s\n' "$PRIMARY_TEST_TRIGGER"

  print_step "Restarting Espanso"

  if "$espanso_bin" restart; then
    printf 'Espanso restart command completed.\n'
  else
    print_warn "espanso restart returned a non-zero status."
    print_warn "The YAML was installed, but Espanso may need manual restart or session repair."
  fi

  print_step "Espanso status"

  if ! "$espanso_bin" status; then
    print_warn "espanso status returned a non-zero status."
  fi

  print_step "Trigger smoke-test list"
  print_trigger_list "$installed_yaml"

  print_step "Manual GUI expansion test"
  cat <<EOF
Manual test app:

  gedit

Manual test file:

  $manual_test_file

Open the manual test file with this exact command:

  gedit "$manual_test_file"

In gedit:

  1. Click at line 1, column 1.
  2. Type this exact trigger:

       $PRIMARY_TEST_TRIGGER

  3. Wait for Espanso to expand it.
  4. Press Ctrl+S to save the file.
  5. Close gedit.

Expected saved file content:

  The file should contain the Repo Inspect prompt text.
  The file should not contain the literal trigger text:

    $PRIMARY_TEST_TRIGGER

After saving, verify the saved file with this exact command:

  sed -n '1,40p' "$manual_test_file"

If the saved file still contains only this literal text:

  $PRIMARY_TEST_TRIGGER

then run:

  echo "\$XDG_SESSION_TYPE"
  espanso status

If XDG_SESSION_TYPE is wayland, the likely problem is Espanso installation/session compatibility, not the prompt board YAML.

This installer verified:
  - python3 exists
  - espanso exists
  - espanso path works
  - YAML generated
  - YAML installed
  - trigger exists in installed YAML
  - Espanso restart was attempted
  - Espanso status was printed when available

This installer cannot fully prove GUI text injection until a human opens the named test file, types the trigger, saves the named file, and checks the saved result.
EOF

  print_step "Done"
}

main "$@"
