#!/usr/bin/env python3
"""
Generic portable board ZIP builder.

Reads package/board_package.ini and creates a portable source ZIP from the
current repo shape. This script is intentionally config-driven so a different
board can reuse it by providing its own package config.
"""

from __future__ import annotations

import argparse
import configparser
import sys
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile


DEFAULT_CONFIG = "package/board_package.ini"


def parse_multiline(value: str) -> list[str]:
    items: list[str] = []
    for line in value.splitlines():
        line = line.strip()
        if not line or line.startswith("#") or line.startswith(";"):
            continue
        items.append(line)
    return items


def load_config(config_path: Path) -> configparser.ConfigParser:
    if not config_path.exists():
        raise SystemExit(f"Missing package config: {config_path}")

    cp = configparser.ConfigParser()
    read_files = cp.read(config_path, encoding="utf-8")
    if not read_files:
        raise SystemExit(f"Could not read package config: {config_path}")

    required_sections = ["package", "required_files", "include", "skip"]
    for section in required_sections:
        if not cp.has_section(section):
            raise SystemExit(f"Missing required config section: [{section}]")

    return cp


def required_package_value(cp: configparser.ConfigParser, key: str) -> str:
    value = cp["package"].get(key, "").strip()
    if not value:
        raise SystemExit(f"Missing [package] value: {key}")
    return value


def should_skip(
    path: Path,
    repo_root: Path,
    skip_dirs: set[str],
    skip_suffixes: set[str],
    explicit_include_parts: tuple[str, ...] = (),
) -> bool:
    rel_parts = path.relative_to(repo_root).parts
    check_parts = rel_parts
    if explicit_include_parts and rel_parts[: len(explicit_include_parts)] == explicit_include_parts:
        # Allow an explicit include such as build/linux_hotkey_board even when
        # the top-level build directory is skipped by default. Nested cache
        # folders under that explicit include are still skipped.
        check_parts = rel_parts[len(explicit_include_parts) :]
    if any(part in skip_dirs for part in check_parts):
        return True
    if path.suffix.lower() in skip_suffixes:
        return True
    return False


def collect_files(repo_root: Path, include_paths: list[str], skip_dirs: set[str], skip_suffixes: set[str]) -> list[Path]:
    files: list[Path] = []

    for rel in include_paths:
        item = repo_root / rel
        if not item.exists():
            raise SystemExit(f"Missing include path: {rel}")

        explicit_include_parts = Path(rel).parts

        if item.is_file():
            if not should_skip(item, repo_root, skip_dirs, skip_suffixes, explicit_include_parts):
                files.append(item)
            continue

        if item.is_dir():
            for child in item.rglob("*"):
                if child.is_file() and not should_skip(child, repo_root, skip_dirs, skip_suffixes, explicit_include_parts):
                    files.append(child)
            continue

        raise SystemExit(f"Unsupported include path type: {rel}")

    deduped = sorted(set(files), key=lambda p: p.relative_to(repo_root).as_posix())
    return deduped


def validate_required_files(repo_root: Path, required_files: list[str]) -> None:
    missing: list[str] = []
    for rel in required_files:
        if not (repo_root / rel).is_file():
            missing.append(rel)

    if missing:
        print("Missing required package files:", file=sys.stderr)
        for rel in missing:
            print(f"- {rel}", file=sys.stderr)
        raise SystemExit(1)


def build_zip(repo_root: Path, output_path: Path, folder_name: str, files: list[Path]) -> None:
    if output_path.exists():
        output_path.unlink()

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with ZipFile(output_path, "w", ZIP_DEFLATED) as zf:
        for file in files:
            arcname = f"{folder_name}/{file.relative_to(repo_root).as_posix()}"
            zf.write(file, arcname)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build a portable source ZIP for a prompt/hotkey board using package/board_package.ini."
    )
    parser.add_argument(
        "--repo-root",
        default=".",
        help="Repo root containing the package config. Default: current directory.",
    )
    parser.add_argument(
        "--config",
        default=DEFAULT_CONFIG,
        help=f"Package config path relative to repo root. Default: {DEFAULT_CONFIG}",
    )
    parser.add_argument(
        "--output-dir",
        default="dist",
        help="Output directory relative to repo root. Default: dist",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate config and print the files that would be packaged without writing the ZIP.",
    )
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    config_path = (repo_root / args.config).resolve()
    output_dir = (repo_root / args.output_dir).resolve()

    cp = load_config(config_path)

    product_name = required_package_value(cp, "product_name")
    folder_name = required_package_value(cp, "folder_name")
    portable_zip_name = required_package_value(cp, "portable_zip_name")

    required_files = parse_multiline(cp["required_files"].get("files", ""))
    include_paths = parse_multiline(cp["include"].get("paths", ""))
    skip_dirs = set(parse_multiline(cp["skip"].get("dirs", "")))
    skip_suffixes = {item.lower() for item in parse_multiline(cp["skip"].get("suffixes", ""))}

    if not required_files:
        raise SystemExit("No [required_files] files configured.")
    if not include_paths:
        raise SystemExit("No [include] paths configured.")

    print("## Generic Portable Board ZIP Builder")
    print()
    print("## Resolved paths")
    print(f"Repo root:    {repo_root}")
    print(f"Config:       {config_path}")
    print(f"Product:      {product_name}")
    print(f"Folder name:  {folder_name}")
    print(f"Output dir:   {output_dir}")
    print(f"ZIP name:     {portable_zip_name}")

    print()
    print("## Validate required files")
    validate_required_files(repo_root, required_files)
    print(f"Required files: {len(required_files)} present")

    print()
    print("## Collect package files")
    files = collect_files(repo_root, include_paths, skip_dirs, skip_suffixes)
    print(f"Files selected: {len(files)}")

    if args.dry_run:
        print()
        print("## Dry run file list")
        for file in files:
            print(file.relative_to(repo_root).as_posix())
        print()
        print("Dry run complete. No ZIP was written.")
        return 0

    output_path = output_dir / portable_zip_name

    print()
    print("## Build ZIP")
    build_zip(repo_root, output_path, folder_name, files)
    print(f"Created ZIP: {output_path}")
    print(f"Packaged files: {len(files)}")
    print()
    print("## Install behavior")
    print("Nothing was installed.")
    print("No runtime config directory was modified.")
    print("No Espanso command was called.")
    print("No AutoHotkey command was called.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
