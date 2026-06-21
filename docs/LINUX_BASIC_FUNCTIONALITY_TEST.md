# Linux Basic Functionality Test

This is a pragmatic smoke test for the included Linux runtime. It is not a promise that every desktop/session combination supports perfect text injection.

## From the extracted package root

```bash
cd eMachinationCADPatentPromptRig
python3 -m pytest -q tests/test_linux_hotkey_board.py
python3 tools/compile_hotkey_board_linux.py --repo-root .
python3 -m json.tool build/linux_hotkey_board/board_spec.json >/dev/null
bash launchers/linux/start_hotkey_board.sh
```

## Manual smoke test

- Board opens.
- Product name is `eMachination CAD Patent Prompt-Rig`.
- Profiles include Coding and Design Documentation.
- Three boards are present.
- Eight prompt buttons appear per board.
- Prompt Forge opens.
- Copy Prompt Coach copies a reusable prompt coach prompt.
- Copy Terminal Buffer reports a provider result or a documented fallback/limitation.

## Stop runtime

```bash
bash launchers/linux/stop_hotkey_board.sh
```
