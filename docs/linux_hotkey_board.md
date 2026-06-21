# Linux Runtime Notes — eMachination CAD Patent Prompt-Rig

Linux runtime/source support remains included for this CAD / patent prompt-board package. Windows remains the primary release target.

## Compile Board Spec

```bash
python3 tools/compile_hotkey_board_linux.py --repo-root .
```

## Start Runtime

```bash
bash launchers/linux/start_hotkey_board.sh
```

## Limits

Linux hotkey behavior can vary by distribution, desktop session, compositor, and keyboard permissions. Terminal-buffer capture is not a blocker for this CAD / patent prompt library slice.
