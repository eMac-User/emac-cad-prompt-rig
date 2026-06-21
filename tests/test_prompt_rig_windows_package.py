from pathlib import Path
import configparser

ROOT = Path(__file__).resolve().parents[1]
EXPECTED_PROFILES = ['rough_in_part_development', 'mechanical_drawing_cleanup', 'cad_application_assist']
EXPECTED_BOARDS = ['primary', 'secondary', 'tertiary']
EXPECTED_PROMPT_COUNT = 72


def test_windows_runtime_preserves_requested_feature_set():
    runtime = (ROOT / "src/eMachination_Coding_Prompt_Rig.ahk").read_text(encoding="utf-8")

    assert 'APP_NAME := "eMachination CAD Patent Prompt-Rig"' in runtime
    assert 'APP_TITLE_LINE_1 := "eMachination CAD Patent"' in runtime
    assert 'APP_TITLE_LINE_2 := "Prompt-Rig"' in runtime

    assert 'Map("id", "rough_in_part_development", "name", "Rough-In Parts")' in runtime
    assert 'Map("id", "mechanical_drawing_cleanup", "name", "Mechanical Drawing Cleanup")' in runtime
    assert 'Map("id", "cad_application_assist", "name", "CAD Application Assist")' in runtime

    assert 'academic_creative_writing' not in runtime

    assert "CycleBoard" in runtime
    assert "Pause::" in runtime
    assert "NumLock::CycleProfile()" in runtime

    assert "CopyTerminalBuffer" in runtime
    assert "OpenPromptForge" in runtime
    assert "CopyPromptCoach" in runtime
    assert "Enable Numpad Mode" in runtime

    assert 'boardGui.SetFont("s9 Bold", "Segoe UI")' in runtime
    assert 'boardGui.Add("Text", "xm w360 Center", profileName " - " boardName)' in runtime
    assert 'return numpadModeEnabled' in runtime
    assert 'activeHwnd := WinGetID("A")' in runtime
    assert 'forgeGui.SetFont("s9 Bold", "Segoe UI")' in runtime


def test_prompt_index_is_six_profiles_three_boards_eight_slots():
    cp = configparser.ConfigParser()
    cp.optionxform = str
    cp.read(ROOT / "prompts" / "index.ini", encoding="utf-8")

    sections = cp.sections()
    assert len(sections) == EXPECTED_PROMPT_COUNT

    profiles = {section.rsplit(".", 2)[0] for section in sections}
    boards = {section.rsplit(".", 2)[1] for section in sections}
    slots = {section.rsplit(".", 2)[2] for section in sections}

    assert profiles == set(EXPECTED_PROFILES)
    assert boards == set(EXPECTED_BOARDS)
    assert slots == {f"{i:02d}" for i in range(1, 9)}

    for profile in EXPECTED_PROFILES:
        for board in EXPECTED_BOARDS:
            pair_slots = {section.rsplit(".", 2)[2] for section in sections if section.startswith(f"{profile}.{board}.")}
            assert pair_slots == {f"{i:02d}" for i in range(1, 9)}

    for section in sections:
        rel_path = cp[section]["path"]
        prompt_path = ROOT / rel_path
        assert prompt_path.is_file(), rel_path
        text = prompt_path.read_text(encoding="utf-8")
        assert text.strip()
        assert "**Runtime key:**" in text
        assert "### Goal" in text
        assert "### Use when" in text
        assert "### Source material" in text
        assert "### Rules" in text
        assert "### Output format" in text
        assert "### Final instruction" in text or section == "mechanical_drawing_cleanup.primary.01"


def test_clean_drawing_prompt_contains_design_intent_rule():
    path = ROOT / "prompts" / "mechanical_drawing_cleanup" / "primary" / "01_clean_drawing.md"
    text = path.read_text(encoding="utf-8")
    assert "Preserve design intent, not ugly geometry." in text
    assert "Straighten lines that should be horizontal or vertical." in text
    assert "black-and-white mechanical drawing" in text
    assert "no photorealistic rendering" in text


def test_windows_launchers_exist_and_target_runtime():
    start_ahk = ROOT / "launchers" / "Start eMachination CAD Patent Prompt-Rig.ahk"
    start_bat = ROOT / "launchers" / "Start eMachination CAD Patent Prompt-Rig.bat"
    start_ps1 = ROOT / "launchers" / "Start eMachination CAD Patent Prompt-Rig.ps1"
    stop_ahk = ROOT / "launchers" / "Stop eMachination CAD Patent Prompt-Rig.ahk"
    stop_bat = ROOT / "launchers" / "Stop eMachination CAD Patent Prompt-Rig.bat"
    stop_ps1 = ROOT / "launchers" / "Stop eMachination CAD Patent Prompt-Rig.ps1"

    for path in [start_ahk, start_bat, start_ps1, stop_ahk, stop_bat, stop_ps1]:
        assert path.is_file(), path

    assert "eMachination_Coding_Prompt_Rig.ahk" in start_ahk.read_text(encoding="utf-8")
    assert "stop_emachination_cad_patent_prompt_rig.ahk" in stop_ahk.read_text(encoding="utf-8")
    assert "Start eMachination CAD Patent Prompt-Rig.ps1" in start_bat.read_text(encoding="utf-8")
    assert "Stop eMachination CAD Patent Prompt-Rig.ps1" in stop_bat.read_text(encoding="utf-8")
    assert "AutoHotkey64.exe" in start_ps1.read_text(encoding="utf-8")
    assert "Stop-Process -Force" in stop_ps1.read_text(encoding="utf-8")


def test_package_config_matches_cad_patent_release():
    cp = configparser.ConfigParser()
    cp.read(ROOT / "package" / "board_package.ini", encoding="utf-8")

    assert cp["package"]["product_name"] == "eMachination CAD Patent Prompt-Rig"
    assert cp["package"]["folder_name"] == "eMachinationCADPatentPromptRig"
    assert cp["package"]["portable_zip_name"] == "emachination_cad_patent_prompt_rig_roughin_slim_portable.zip"
    assert cp["linux_board"]["source_ahk_path"] == "src/eMachination_Coding_Prompt_Rig.ahk"
    assert cp["linux_board"]["expected_prompt_count"] == str(EXPECTED_PROMPT_COUNT)
