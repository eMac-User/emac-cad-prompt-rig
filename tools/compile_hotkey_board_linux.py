#!/usr/bin/env python3
"""
Compile a Windows AutoHotkey-style prompt board into a declarative Linux board spec.

This compiler is intentionally generic. It reads the board package config, the
Windows AHK runtime when available, prompts/index.ini, prompt Markdown bodies,
and config/settings.ini when present. The Linux runtime consumes the JSON spec;
it should not contain board-specific VeydraNet assumptions.
"""

from __future__ import annotations

import argparse
import configparser
import hashlib
import json
import os
import re
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

DEFAULT_PACKAGE_CONFIG = "package/board_package.ini"
DEFAULT_OUTPUT_SPEC = "build/linux_hotkey_board/board_spec.json"
DEFAULT_SETTINGS = {
    "enable_global_chat_hotkeys": "1",
    "enable_numpad_mode": "0",
    "remember_numpad_mode": "0",
}


@dataclass(frozen=True)
class PromptEntry:
    section: str
    profile_id: str
    board_id: str
    slot: int
    label: str
    path: str
    body_sha256: str
    size_bytes: int


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def load_config(path: Path) -> configparser.ConfigParser:
    cp = configparser.ConfigParser()
    cp.optionxform = str
    if path.exists():
        cp.read(path, encoding="utf-8")
    return cp


def parse_bool_string(value: str, default: str = "0") -> str:
    normalized = str(value if value is not None else default).strip().lower()
    if normalized in {"1", "true", "yes", "on"}:
        return "1"
    if normalized in {"0", "false", "no", "off"}:
        return "0"
    return default


def parse_multiline(value: str) -> list[str]:
    items: list[str] = []
    for line in value.splitlines():
        line = line.strip()
        if not line or line.startswith("#") or line.startswith(";"):
            continue
        items.append(line)
    return items


def safe_rel_path(value: str, *, label: str) -> str:
    value = value.strip().replace("\\", "/")
    if not value:
        raise ValueError(f"Empty path for {label}")
    path = Path(value)
    if path.is_absolute():
        raise ValueError(f"Absolute paths are not allowed in {label}: {value}")
    if any(part == ".." for part in path.parts):
        raise ValueError(f"Parent traversal is not allowed in {label}: {value}")
    return path.as_posix()


def extract_ahk_array_maps(ahk_text: str, variable_name: str) -> list[dict[str, str]]:
    """Extract arrays like: profiles := [ Map("id", "x", "name", "X") ]."""
    pattern = re.compile(rf"{re.escape(variable_name)}\s*:=\s*\[(.*?)\]\s*\r?\n", re.S)
    match = pattern.search(ahk_text)
    if not match:
        return []

    block = match.group(1)
    rows: list[dict[str, str]] = []
    for row in re.finditer(r'Map\("id",\s*"([^"]+)",\s*"name",\s*"([^"]+)"\)', block):
        rows.append({"id": row.group(1), "name": row.group(2)})
    return rows


def title_from_id(value: str) -> str:
    return value.replace("_", " ").replace("-", " ").title()


def infer_profiles_and_boards(entries: list[PromptEntry]) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    profile_ids: list[str] = []
    board_ids: list[str] = []
    for entry in entries:
        if entry.profile_id not in profile_ids:
            profile_ids.append(entry.profile_id)
        if entry.board_id not in board_ids:
            board_ids.append(entry.board_id)
    return (
        [{"id": profile_id, "name": title_from_id(profile_id)} for profile_id in profile_ids],
        [{"id": board_id, "name": title_from_id(board_id)} for board_id in board_ids],
    )


def ahk_key_to_text(value: str) -> str:
    prefixes = []
    raw = value.strip()
    while raw and raw[0] in "^!+#":
        char = raw[0]
        raw = raw[1:]
        prefixes.append({"^": "Ctrl", "!": "Alt", "+": "Shift", "#": "Super"}[char])
    key_map = {
        "SC046": "ScrollLock",
        "Pause": "Pause",
        "CtrlBreak": "CtrlBreak",
        "NumpadIns": "Numpad0",
        "NumpadEnd": "Numpad1",
        "NumpadDown": "Numpad2",
        "NumpadPgDn": "Numpad3",
        "NumpadLeft": "Numpad4",
        "NumpadClear": "Numpad5",
        "NumpadRight": "Numpad6",
        "NumpadHome": "Numpad7",
        "NumpadUp": "Numpad8",
        "NumpadPgUp": "Numpad9",
    }
    key = key_map.get(raw, raw)
    return "+".join([*prefixes, key]) if prefixes else key


def parse_ahk_hotkeys(ahk_text: str) -> dict[str, Any]:
    board_launchers: list[dict[str, Any]] = []
    close_exit: list[dict[str, str]] = []
    global_chat: list[dict[str, str]] = []
    numpad: list[dict[str, Any]] = []

    lines = ahk_text.splitlines()
    for index, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith(";") or "::" not in stripped:
            continue
        key, tail = stripped.split("::", 1)
        key = key.strip()
        if not key or key.startswith("#"):
            continue
        lookahead = "\n".join(lines[index : index + 5])

        open_match = re.search(r"OpenBoard\((\d+)\)", lookahead)
        if open_match:
            board_launchers.append(
                {
                    "windows_key": ahk_key_to_text(key),
                    "ahk_key": key,
                    "action": "open_board",
                    "board_index": int(open_match.group(1)),
                }
            )
            continue

        if re.search(r"(?:CloseBoard|Exit[A-Za-z0-9_]*|ExitApp)\(", lookahead):
            close_exit.append({"windows_key": ahk_key_to_text(key), "ahk_key": key, "action": "close_board"})
            continue

        chat_match = re.search(r'SendChatUtility\("([^"]*)"\)', lookahead)
        if chat_match:
            global_chat.append(
                {
                    "windows_key": ahk_key_to_text(key),
                    "ahk_key": key,
                    "action": "send_text",
                    "text": chat_match.group(1),
                }
            )
            continue

        paste_match = re.search(r"PastePromptSlot\((\d+)\)", lookahead)
        if paste_match:
            numpad.append(
                {
                    "windows_key": ahk_key_to_text(key),
                    "ahk_key": key,
                    "action": "paste_prompt_slot",
                    "slot": int(paste_match.group(1)),
                }
            )
            continue

        if re.search(r"OpenPromptForge\(", lookahead):
            numpad.append({"windows_key": ahk_key_to_text(key), "ahk_key": key, "action": "open_prompt_forge"})
            continue

    if not global_chat:
        global_chat = [
            {"windows_key": "Insert", "action": "send_text", "text": "clear"},
            {"windows_key": "PgUp", "action": "send_text", "text": "Ok, continue"},
            {
                "windows_key": "Home",
                "action": "send_text",
                "text": "Checkpoint this. What is locked, what is open, and what is the next best step?",
            },
            {"windows_key": "End", "action": "send_text", "text": "Finalize this. Produce the clean final version now."},
            {"windows_key": "PgDn", "action": "send_text", "text": "Next step only. Give me the next concrete action and stop."},
        ]

    return {
        "board_launchers_windows_equivalent": board_launchers,
        "board_close_exit_windows_equivalent": close_exit,
        "global_chat_windows_equivalent": global_chat,
        "numpad_windows_equivalent": numpad,
        "linux_fallbacks": [
            {"key": "Ctrl+Alt+Space", "action": "open_board", "board_index": 1},
            {"key": "Ctrl+Alt+Page_Up", "action": "open_board", "board_index": 2},
            {"key": "Ctrl+Alt+Page_Down", "action": "open_board", "board_index": 3},
        ],
        "scroll_lock_warning": (
            "ScrollLock is the Windows-equivalent launcher intent, but it is not reliable as the only Linux launcher hotkey. "
            "The runtime must report session/backend support and use configurable fallbacks where possible."
        ),
    }


def load_settings(repo_root: Path, settings_rel: str) -> dict[str, str]:
    settings = dict(DEFAULT_SETTINGS)
    settings_path = repo_root / settings_rel
    if not settings_path.exists():
        return settings
    cp = configparser.ConfigParser()
    cp.read(settings_path, encoding="utf-8")
    if cp.has_section("settings"):
        for key in DEFAULT_SETTINGS:
            settings[key] = parse_bool_string(cp["settings"].get(key, DEFAULT_SETTINGS[key]), DEFAULT_SETTINGS[key])
    return settings


def load_prompt_entries(repo_root: Path, index_rel: str) -> list[PromptEntry]:
    index_path = repo_root / index_rel
    if not index_path.is_file():
        raise FileNotFoundError(f"Missing prompt index: {index_path}")

    cp = configparser.ConfigParser()
    cp.optionxform = str
    cp.read(index_path, encoding="utf-8")

    entries: list[PromptEntry] = []
    errors: list[str] = []

    for section in cp.sections():
        parts = section.split(".")
        if len(parts) < 3:
            errors.append(f"Invalid prompt section name: {section}")
            continue
        slot_text = parts[-1]
        board_id = parts[-2]
        profile_id = ".".join(parts[:-2])
        if not profile_id or not board_id or not slot_text.isdigit():
            errors.append(f"Invalid prompt section name: {section}")
            continue
        slot = int(slot_text)
        label = cp[section].get("label", "").strip()
        rel_path = cp[section].get("path", "").strip()
        if not label:
            errors.append(f"Missing label in [{section}]")
            continue
        try:
            rel_path = safe_rel_path(rel_path, label=f"[{section}] path")
        except ValueError as exc:
            errors.append(str(exc))
            continue
        if not rel_path.lower().endswith(".md"):
            errors.append(f"Prompt path must point to a Markdown file in [{section}]: {rel_path}")
            continue
        prompt_path = repo_root / rel_path
        if not prompt_path.is_file():
            errors.append(f"Missing prompt Markdown file in [{section}]: {rel_path}")
            continue
        body = prompt_path.read_bytes()
        if not body.strip():
            errors.append(f"Prompt Markdown file is empty in [{section}]: {rel_path}")
            continue
        entries.append(
            PromptEntry(
                section=section,
                profile_id=profile_id,
                board_id=board_id,
                slot=slot,
                label=label,
                path=rel_path,
                body_sha256=hashlib.sha256(body).hexdigest(),
                size_bytes=len(body),
            )
        )

    if errors:
        raise ValueError("Prompt library validation failed:\n" + "\n".join(f"- {item}" for item in errors))

    return sorted(entries, key=lambda item: (item.profile_id, item.board_id, item.slot))


def validate_prompt_grid(
    entries: list[PromptEntry],
    profiles: list[dict[str, str]],
    boards: list[dict[str, str]],
    expected_prompt_count: int | None,
) -> tuple[int, list[str]]:
    errors: list[str] = []
    if expected_prompt_count is not None and len(entries) != expected_prompt_count:
        errors.append(f"Expected {expected_prompt_count} prompts but found {len(entries)}")

    profile_ids = [profile["id"] for profile in profiles]
    board_ids = [board["id"] for board in boards]
    slots_by_pair: dict[tuple[str, str], set[int]] = {}
    for entry in entries:
        slots_by_pair.setdefault((entry.profile_id, entry.board_id), set()).add(entry.slot)

    if entries and profiles and boards:
        max_slot = max(entry.slot for entry in entries)
        expected_slots = set(range(1, max_slot + 1))
        for profile_id in profile_ids:
            for board_id in board_ids:
                slots = slots_by_pair.get((profile_id, board_id), set())
                if slots != expected_slots:
                    missing = sorted(expected_slots - slots)
                    extra = sorted(slots - expected_slots)
                    if missing:
                        errors.append(f"Missing slots for {profile_id}.{board_id}: {missing}")
                    if extra:
                        errors.append(f"Unexpected slots for {profile_id}.{board_id}: {extra}")
        return max_slot, errors

    return 0, errors


def compile_board_spec(repo_root: Path, package_config_rel: str = DEFAULT_PACKAGE_CONFIG) -> dict[str, Any]:
    package_config_path = repo_root / package_config_rel
    package_config = load_config(package_config_path)

    product_name = package_config.get("package", "product_name", fallback="Hotkey Board").strip() or "Hotkey Board"
    folder_name = package_config.get("package", "folder_name", fallback=repo_root.name).strip() or repo_root.name

    source_ahk_rel = package_config.get("linux_board", "source_ahk_path", fallback="").strip()
    prompt_index_rel = package_config.get("linux_board", "prompts_index_path", fallback="prompts/index.ini")
    settings_rel = package_config.get("linux_board", "settings_path", fallback="config/settings.ini")
    output_spec_rel = package_config.get("linux_board", "output_spec_path", fallback=DEFAULT_OUTPUT_SPEC)
    expected_prompt_count_text = package_config.get("linux_board", "expected_prompt_count", fallback="").strip()
    expected_prompt_count = int(expected_prompt_count_text) if expected_prompt_count_text.isdigit() else None

    if source_ahk_rel:
        source_ahk_rel = safe_rel_path(source_ahk_rel, label="source_ahk_path")
    prompt_index_rel = safe_rel_path(prompt_index_rel, label="prompts_index_path")
    settings_rel = safe_rel_path(settings_rel, label="settings_path")
    output_spec_rel = safe_rel_path(output_spec_rel, label="output_spec_path")

    ahk_path = (repo_root / source_ahk_rel) if source_ahk_rel else None
    ahk_text = read_text(ahk_path) if ahk_path is not None and ahk_path.is_file() else ""

    entries = load_prompt_entries(repo_root, prompt_index_rel)
    ahk_profiles = extract_ahk_array_maps(ahk_text, "profiles") if ahk_text else []
    ahk_boards = extract_ahk_array_maps(ahk_text, "boards") if ahk_text else []
    inferred_profiles, inferred_boards = infer_profiles_and_boards(entries)
    profiles = ahk_profiles or inferred_profiles
    boards = ahk_boards or inferred_boards

    prompt_profile_ids = {entry.profile_id for entry in entries}
    prompt_board_ids = {entry.board_id for entry in entries}
    profiles = [profile for profile in profiles if profile["id"] in prompt_profile_ids]
    boards = [board for board in boards if board["id"] in prompt_board_ids]
    if not profiles or not boards:
        profiles, boards = inferred_profiles, inferred_boards

    prompts_per_board, grid_errors = validate_prompt_grid(entries, profiles, boards, expected_prompt_count)
    if grid_errors:
        raise ValueError("Prompt grid validation failed:\n" + "\n".join(f"- {item}" for item in grid_errors))

    prompt_records = [
        {
            "section": entry.section,
            "profile_id": entry.profile_id,
            "board_id": entry.board_id,
            "slot": entry.slot,
            "label": entry.label,
            "path": entry.path,
            "body_sha256": entry.body_sha256,
            "size_bytes": entry.size_bytes,
        }
        for entry in sorted(entries, key=lambda item: (
            next((idx for idx, profile in enumerate(profiles) if profile["id"] == item.profile_id), 999),
            next((idx for idx, board in enumerate(boards) if board["id"] == item.board_id), 999),
            item.slot,
        ))
    ]

    spec: dict[str, Any] = {
        "schema_version": "linux-hotkey-board-spec-v1",
        "compiled_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "product": {"name": product_name, "folder_name": folder_name},
        "source": {
            "package_config_path": package_config_rel,
            "ahk_path": source_ahk_rel,
            "prompts_index_path": prompt_index_rel,
            "settings_path": settings_rel,
        },
        "paths": {"prompt_root": "prompts", "output_spec_path": output_spec_rel},
        "model": {
            "profiles": profiles,
            "boards": boards,
            "profile_count": len(profiles),
            "board_count": len(boards),
            "prompts_per_board": prompts_per_board,
            "prompt_count": len(prompt_records),
            "expected_prompt_count": expected_prompt_count or len(prompt_records),
        },
        "prompts": prompt_records,
        "settings": load_settings(repo_root, settings_rel),
        "hotkeys": parse_ahk_hotkeys(ahk_text),
        "prompt_forge": {
            "local_only": True,
            "ai_model_calls": False,
            "copy_prompt_coach": True,
            "prompt_a_visible_by_default": True,
            "prompt_b_visible_by_default": False,
            "add_prompt_b_reveals_prompt_b": True,
            "merge_combine_auto_shows_prompt_b": True,
            "close_resets_state": True,
            "transformations": [
                "Merge / Combine",
                "Repair",
                "Compress",
                "Expand",
                "Specialize",
                "Convert to Implementation Prompt",
                "Convert to Design-Doc Prompt",
                "Convert to AI-CAD Prompt",
                "Convert to Academic/Writing Prompt",
                "Convert to Current-Session Instruction",
                "Convert to New-Session Prompt",
            ],
        },
        "linux_runtime": {
            "global_hotkeys_experimental": True,
            "typed_expansion_triggers_required": False,
            "espanso_is_main_workflow": False,
        },
    }
    return spec


def write_spec(spec: dict[str, Any], repo_root: Path, output_rel: str | None = None) -> Path:
    rel = output_rel or spec["paths"]["output_spec_path"]
    rel = safe_rel_path(rel, label="output spec")
    output_path = repo_root / rel
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(spec, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return output_path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Compile a prompt-board repo into a generic Linux board spec JSON.")
    parser.add_argument("--repo-root", default=".", help="Repo root. Default: current directory.")
    parser.add_argument("--package-config", default=DEFAULT_PACKAGE_CONFIG, help="Package config relative to repo root.")
    parser.add_argument("--output", default="", help="Output board_spec.json path. Default: config value or build/linux_hotkey_board/board_spec.json.")
    parser.add_argument("--check", action="store_true", help="Compile and validate, but do not write board_spec.json.")
    parser.add_argument("--print-json", action="store_true", help="Print compiled JSON to stdout.")
    args = parser.parse_args(argv)

    repo_root = Path(args.repo_root).resolve()
    try:
        spec = compile_board_spec(repo_root, args.package_config)
        output_path = None
        if not args.check:
            output_path = write_spec(spec, repo_root, args.output or None)
        if args.print_json:
            print(json.dumps(spec, indent=2, ensure_ascii=False))
        else:
            print("## Linux Hotkey Board Compile")
            print(f"Repo root: {repo_root}")
            print(f"Product: {spec['product']['name']}")
            print(f"Profiles: {spec['model']['profile_count']}")
            print(f"Boards: {spec['model']['board_count']}")
            print(f"Prompt buttons per board: {spec['model']['prompts_per_board']}")
            print(f"Prompt entries: {spec['model']['prompt_count']}")
            print("Typed Espanso triggers required: no")
            print("ScrollLock-only Linux launcher: no")
            if output_path is not None:
                print(f"Wrote spec: {output_path}")
            else:
                print("Check only: no file written")
        return 0
    except Exception as exc:  # noqa: BLE001 - CLI must report concise failures.
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
