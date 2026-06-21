from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
COMPILER_PATH = REPO_ROOT / "tools" / "compile_hotkey_board_linux.py"
RUNTIME_PATH = REPO_ROOT / "src" / "linux" / "hotkey_board_runtime.py"
SPEC_PATH = REPO_ROOT / "build" / "linux_hotkey_board" / "board_spec.json"
EXPECTED_PROFILES = ['rough_in_part_development', 'mechanical_drawing_cleanup', 'cad_application_assist']
EXPECTED_BOARDS = ['primary', 'secondary', 'tertiary']
EXPECTED_PROMPT_COUNT = 72


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def test_compile_current_board_spec_matches_cad_patent_model() -> None:
    compiler = load_module("compile_prompt_rig_linux_test", COMPILER_PATH)
    spec = compiler.compile_board_spec(REPO_ROOT)

    assert spec["schema_version"] == "linux-hotkey-board-spec-v1"
    assert spec["product"]["name"] == "eMachination CAD Patent Prompt-Rig"
    assert spec["product"]["folder_name"] == "eMachinationCADPatentPromptRig"

    assert spec["model"]["profile_count"] == len(EXPECTED_PROFILES)
    assert spec["model"]["board_count"] == len(EXPECTED_BOARDS)
    assert spec["model"]["prompts_per_board"] == 8
    assert spec["model"]["prompt_count"] == EXPECTED_PROMPT_COUNT
    assert spec["model"]["expected_prompt_count"] == EXPECTED_PROMPT_COUNT

    assert [profile["id"] for profile in spec["model"]["profiles"]] == EXPECTED_PROFILES
    assert [board["id"] for board in spec["model"]["boards"]] == EXPECTED_BOARDS

    assert spec["linux_runtime"]["typed_expansion_triggers_required"] is False
    assert spec["linux_runtime"]["espanso_is_main_workflow"] is False
    assert "linux_fallbacks" in spec["hotkeys"]


def test_compiler_writes_board_spec_json() -> None:
    compiler = load_module("compile_prompt_rig_linux_write_test", COMPILER_PATH)
    spec = compiler.compile_board_spec(REPO_ROOT)
    output = compiler.write_spec(spec, REPO_ROOT)
    data = json.loads(output.read_text(encoding="utf-8"))

    assert output == SPEC_PATH
    assert data["source"]["ahk_path"] == "src/eMachination_Coding_Prompt_Rig.ahk"
    assert data["source"]["prompts_index_path"] == "prompts/index.ini"
    assert data["model"]["prompt_count"] == EXPECTED_PROMPT_COUNT
    assert data["prompts"][0]["label"]
    assert data["prompts"][0]["path"].endswith(".md")


def test_linux_runtime_module_imports_and_contains_prompt_forge_support() -> None:
    runtime = load_module("prompt_rig_linux_runtime_import_test", RUNTIME_PATH)

    assert runtime.DEFAULT_SPEC == "build/linux_hotkey_board/board_spec.json"
    assert "reusable AI prompt" in runtime.PROMPT_COACH_TEXT
    assert "Merge / Combine" in runtime.FORGE_TRANSFORMATIONS
    assert "Repair" in runtime.FORGE_TRANSFORMATIONS


def test_linux_launchers_are_present_and_reference_runtime_baseline() -> None:
    start = REPO_ROOT / "launchers" / "linux" / "start_hotkey_board.sh"
    stop = REPO_ROOT / "launchers" / "linux" / "stop_hotkey_board.sh"
    transcript = REPO_ROOT / "launchers" / "linux" / "start_transcript_terminal.sh"

    for path in [start, stop, transcript]:
        assert path.is_file(), path
        assert path.read_text(encoding="utf-8").startswith("#!/usr/bin/env bash")

    start_text = start.read_text(encoding="utf-8")
    assert "compile_hotkey_board_linux.py" in start_text
    assert "hotkey_board_runtime.py" in start_text
    assert "board_spec.json" in start_text


def test_terminal_copy_provider_imports() -> None:
    provider = load_module(
        "prompt_rig_terminal_copy_provider_import_test",
        REPO_ROOT / "src" / "linux" / "terminal_copy_providers.py",
    )

    assert hasattr(provider, "copy_terminal_buffer_with_provider")


def test_linux_basic_test_script_and_doc_are_present() -> None:
    script = REPO_ROOT / "linux_basic_test.sh"
    doc = REPO_ROOT / "docs" / "LINUX_BASIC_FUNCTIONALITY_TEST.md"

    assert script.is_file(), script
    assert doc.is_file(), doc

    script_text = script.read_text(encoding="utf-8")
    assert "No-pytest Linux smoke test" in script_text
    assert "compile_hotkey_board_linux.py" in script_text
    assert "prompt_count == 72" in script_text

    doc_text = doc.read_text(encoding="utf-8")
    assert "Linux Basic Functionality Test" in doc_text
    assert "start_hotkey_board.sh" in doc_text
