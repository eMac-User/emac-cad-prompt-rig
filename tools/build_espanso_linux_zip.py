#!/usr/bin/env python3
"""
Build a repo-local Espanso Linux ZIP package for the VeydraNet prompt board.

This script packages generated Espanso YAML and documentation only.
It does not install Espanso, modify user config, restart Espanso, or verify GUI expansion.
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path


PACKAGE_NAME = "veydranet_prompt_board_espanso_linux"
ZIP_NAME = f"{PACKAGE_NAME}.zip"

YAML_NAME = "veydranet_prompt_board.yml"
REPORT_NAME = "veydranet_prompt_board_report.md"
README_NAME = "README_INSTALL.md"
MANIFEST_NAME = "MANIFEST.txt"

TRIGGER_PREFIX = "vhb"
TEST_TRIGGER = ":vhb-ci-p01"

TRIGGER_RE = re.compile(
    r"""^\s*(?:-\s*)?trigger:\s*["']?([^"'\s]+)["']?\s*$""",
    re.MULTILINE,
)


def find_repo_root() -> Path:
    script_path = Path(__file__).resolve()
    repo_root = script_path.parents[1]

    required_paths = [
        repo_root / "tools" / "export_prompts_to_espanso.py",
        repo_root / "prompts" / "index.ini",
    ]

    missing = [path for path in required_paths if not path.exists()]
    if missing:
        missing_text = "\n".join(f"- {path}" for path in missing)
        raise SystemExit(
            "Could not confirm repo root from script location.\n"
            f"Resolved repo root: {repo_root}\n"
            f"Missing required path(s):\n{missing_text}"
        )

    return repo_root


def require_file_nonempty(path: Path, label: str) -> None:
    if not path.exists():
        raise SystemExit(f"{label} was not created: {path}")
    if not path.is_file():
        raise SystemExit(f"{label} is not a file: {path}")
    if path.stat().st_size <= 0:
        raise SystemExit(f"{label} is empty: {path}")


def inspect_exporter_cli(python_exe: str, exporter_path: Path) -> None:
    completed = subprocess.run(
        [python_exe, str(exporter_path), "--help"],
        cwd=str(exporter_path.parent.parent),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )

    help_text = completed.stdout or ""
    required_flags = ["--repo-root", "--output", "--report", "--trigger-prefix"]
    missing_flags = [flag for flag in required_flags if flag not in help_text]

    if completed.returncode != 0:
        raise SystemExit(
            "Exporter CLI inspection failed.\n"
            f"Command: {python_exe} {exporter_path} --help\n"
            f"Exit code: {completed.returncode}\n\n"
            f"{help_text}"
        )

    if missing_flags:
        missing_text = ", ".join(missing_flags)
        raise SystemExit(
            "Exporter CLI does not expose the expected options.\n"
            f"Missing flag(s): {missing_text}\n"
            f"Exporter path: {exporter_path}\n\n"
            f"Exporter help output:\n{help_text}"
        )


def run_exporter(
    *,
    python_exe: str,
    repo_root: Path,
    exporter_path: Path,
    yaml_path: Path,
    report_path: Path,
) -> None:
    command = [
        python_exe,
        str(exporter_path),
        "--repo-root",
        str(repo_root),
        "--output",
        str(yaml_path),
        "--report",
        str(report_path),
        "--trigger-prefix",
        TRIGGER_PREFIX,
    ]

    completed = subprocess.run(
        command,
        cwd=str(repo_root),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )

    if completed.returncode != 0:
        command_text = " ".join(command)
        raise SystemExit(
            "Exporter command failed.\n"
            f"Command: {command_text}\n"
            f"Exit code: {completed.returncode}\n\n"
            f"{completed.stdout}"
        )

    if completed.stdout.strip():
        print("\n## Exporter output")
        print(completed.stdout.rstrip())


def read_triggers(yaml_path: Path) -> list[str]:
    yaml_text = yaml_path.read_text(encoding="utf-8")
    return TRIGGER_RE.findall(yaml_text)


def write_readme(readme_path: Path) -> None:
    readme_path.write_text(
        f"""# VeydraNet Prompt Board for Espanso on Linux

This ZIP does not install Espanso.

It only packages the generated VeydraNet prompt board YAML for users who already have Espanso installed and working for their current Linux session.

## Package contents

```text
{PACKAGE_NAME}/
  match/
    {YAML_NAME}
  docs/
    {REPORT_NAME}
    {README_NAME}
  {MANIFEST_NAME}
```

## Install requirement

Install and verify Espanso first.

This package does not install Espanso, configure Linux desktop sessions, switch between Wayland and X11, create desktop icons, modify shell startup files, or change Fedora sleep/login settings.

## Manual install target file

Copy this file from the extracted ZIP:

```text
match/{YAML_NAME}
```

Into the Espanso match directory for the user's working Espanso installation.

## Manual GUI test

Use this exact trigger:

```text
{TEST_TRIGGER}
```

Expected result:

```text
The Repo Inspect prompt expands.
```

The prompt-board ZIP only proves that the Espanso YAML package was generated. It does not prove GUI text expansion in a desktop app.

## If the trigger does not expand

Run these checks in a terminal:

```bash
echo "$XDG_SESSION_TYPE"
espanso status
espanso path
```

If `XDG_SESSION_TYPE` is `wayland`, the likely problem is Espanso installation/session/backend compatibility, not the prompt-board YAML.
""",
        encoding="utf-8",
    )


def write_manifest(
    *,
    manifest_path: Path,
    repo_root: Path,
    yaml_path: Path,
    report_path: Path,
    zip_path: Path,
    trigger_count: int,
    first_triggers: list[str],
) -> None:
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    manifest_path.write_text(
        "\n".join(
            [
                f"Package name: {PACKAGE_NAME}",
                f"Build timestamp UTC: {timestamp}",
                f"Repo root used: {repo_root}",
                f"Generated YAML relative path: {yaml_path.relative_to(repo_root)}",
                f"Generated report relative path: {report_path.relative_to(repo_root)}",
                f"ZIP file path: {zip_path}",
                f"Test trigger: {TEST_TRIGGER}",
                f"Total trigger count: {trigger_count}",
                "First triggers:",
                *[f"- {trigger}" for trigger in first_triggers],
                "",
                "Notes:",
                "- This ZIP does not install Espanso.",
                "- This ZIP does not modify user Espanso config.",
                "- This ZIP does not call espanso restart.",
                "- This ZIP does not prove GUI text expansion.",
                "- GUI text expansion depends on the user's Espanso installation and Linux session backend.",
                "",
            ]
        ),
        encoding="utf-8",
    )


def build_zip(*, staging_dir: Path, package_root: Path, zip_path: Path) -> None:
    zip_path.parent.mkdir(parents=True, exist_ok=True)

    if zip_path.exists():
        zip_path.unlink()

    with zipfile.ZipFile(zip_path, mode="w", compression=zipfile.ZIP_DEFLATED) as zip_file:
        for path in sorted(package_root.rglob("*")):
            if path.is_file():
                arcname = path.relative_to(staging_dir).as_posix()
                zip_file.write(path, arcname)

    require_file_nonempty(zip_path, "ZIP file")


def validate_zip_entries(zip_path: Path) -> None:
    expected_entries = {
        f"{PACKAGE_NAME}/match/{YAML_NAME}",
        f"{PACKAGE_NAME}/docs/{REPORT_NAME}",
        f"{PACKAGE_NAME}/docs/{README_NAME}",
        f"{PACKAGE_NAME}/{MANIFEST_NAME}",
    }

    with zipfile.ZipFile(zip_path, mode="r") as zip_file:
        actual_entries = set(zip_file.namelist())

    missing_entries = sorted(expected_entries - actual_entries)
    if missing_entries:
        missing_text = "\n".join(f"- {entry}" for entry in missing_entries)
        raise SystemExit(
            f"ZIP is missing expected entries:\n{missing_text}\n\n"
            f"ZIP path: {zip_path}"
        )


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Build a repo-local Espanso Linux ZIP package for the VeydraNet prompt board. "
            "Does not install Espanso, modify user config, restart Espanso, or verify GUI expansion."
        ),
    )
    parser.add_argument(
        "--repo-root",
        default="",
        help="Repo root directory. Default: derived from this script's own location.",
    )
    parser.add_argument(
        "--output-dir",
        default="",
        help="Directory to write the output ZIP. Default: <repo-root>/dist.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help=(
            "Validate inputs and report what would be built. "
            "Does not create or modify any files."
        ),
    )
    args = parser.parse_args()

    if args.repo_root:
        repo_root = Path(args.repo_root).resolve()
        required = [
            repo_root / "tools" / "export_prompts_to_espanso.py",
            repo_root / "prompts" / "index.ini",
        ]
        missing = [p for p in required if not p.exists()]
        if missing:
            for p in missing:
                print(f"ERROR: required path missing: {p}", file=sys.stderr)
            return 1
    else:
        repo_root = find_repo_root()

    python_exe = sys.executable
    exporter_path = repo_root / "tools" / "export_prompts_to_espanso.py"

    staging_dir = repo_root / "build" / "espanso_zip"
    package_root = staging_dir / PACKAGE_NAME
    match_dir = package_root / "match"
    docs_dir = package_root / "docs"
    dist_dir = Path(args.output_dir).resolve() if args.output_dir else repo_root / "dist"

    yaml_path = match_dir / YAML_NAME
    report_path = docs_dir / REPORT_NAME
    readme_path = docs_dir / README_NAME
    manifest_path = package_root / MANIFEST_NAME
    zip_path = dist_dir / ZIP_NAME

    print("## VeydraNet Prompt Board Espanso Linux ZIP Builder")
    print()
    print("## Resolved paths")
    print(f"Repo root:         {repo_root}")
    print(f"Python:            {python_exe}")
    print(f"Exporter:          {exporter_path}")
    print(f"Staging directory: {staging_dir}")
    print(f"Generated YAML:    {yaml_path}")
    print(f"Generated report:  {report_path}")
    print(f"ZIP output:        {zip_path}")

    if args.dry_run:
        print()
        print("## Dry run: no files will be created or modified.")
        print(f"Would export via:    {exporter_path}")
        print(f"Would stage at:      {package_root}")
        print(f"Would write ZIP to:  {zip_path}")
        print()
        print("Inputs validated. Dry run complete.")
        return 0

    inspect_exporter_cli(python_exe, exporter_path)

    if package_root.exists():
        shutil.rmtree(package_root)

    match_dir.mkdir(parents=True, exist_ok=True)
    docs_dir.mkdir(parents=True, exist_ok=True)

    run_exporter(
        python_exe=python_exe,
        repo_root=repo_root,
        exporter_path=exporter_path,
        yaml_path=yaml_path,
        report_path=report_path,
    )

    require_file_nonempty(yaml_path, "Generated YAML")
    require_file_nonempty(report_path, "Generated report")

    triggers = read_triggers(yaml_path)
    if not triggers:
        raise SystemExit(f"No Espanso triggers were found in generated YAML: {yaml_path}")

    if TEST_TRIGGER not in triggers:
        raise SystemExit(
            f"Expected test trigger was not found in generated YAML: {TEST_TRIGGER}\n"
            f"Generated YAML: {yaml_path}"
        )

    first_triggers = triggers[:8]

    write_readme(readme_path)
    write_manifest(
        manifest_path=manifest_path,
        repo_root=repo_root,
        yaml_path=yaml_path,
        report_path=report_path,
        zip_path=zip_path,
        trigger_count=len(triggers),
        first_triggers=first_triggers,
    )

    require_file_nonempty(readme_path, "README_INSTALL.md")
    require_file_nonempty(manifest_path, "MANIFEST.txt")

    build_zip(staging_dir=staging_dir, package_root=package_root, zip_path=zip_path)
    validate_zip_entries(zip_path)

    print()
    print("## Build result")
    print(f"Trigger count:     {len(triggers)}")
    print("First triggers:")
    for trigger in first_triggers:
        print(f"- {trigger}")

    print()
    print("## ZIP package created")
    print(zip_path)

    print()
    print("## Install behavior")
    print("Nothing was installed.")
    print("No Espanso config directory was modified.")
    print("No Espanso runtime command was called.")
    print("GUI text expansion is not proven by this ZIP build.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
