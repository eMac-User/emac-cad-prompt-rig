# Linux Install

## Repository Navigation

| Page | Link |
| --- | --- |
| Start here | [START_HERE.md](../START_HERE.md) |
| Windows install | [docs/windows-install.md](windows-install.md) |
| Linux install | [docs/linux-install.md](linux-install.md) |
| Visual guide | [docs/visual-guide.md](visual-guide.md) |
| User guide | [docs/USER_GUIDE.md](USER_GUIDE.md) |
| Prompt catalog | [docs/PROMPT_CATALOG.md](PROMPT_CATALOG.md) |
| Roadmap | [docs/ROADMAP.md](ROADMAP.md) |
| License | [LICENSE](../LICENSE) |

The Linux installer is currently proven on Fedora KDE Wayland.

The Linux path uses `bash`, `systemd --user`, and `ydotool` for hotkeys. PowerShell on Linux may be useful for users who like PowerShell-style repo workflows, but it is optional and not required by the installer.

Install from the final folder where you want to keep the repo. Do not move or delete the folder after installation because the systemd user hotkey service points back to that folder.

## Download ZIP Flow

1. Download the repo ZIP from GitHub.
2. Extract it into the folder where you want to keep the project.
3. Open a terminal in the extracted folder.
4. Run:

   ```bash
   bash install_linux.sh
   ```

## Git Clone Flow

Clone into the final folder location:

```bash
git clone https://github.com/eMachination/emac-coding-prompt-rig.git
cd emac-coding-prompt-rig
bash install_linux.sh
```

## Final-Folder Warning

The installer writes a systemd user service with absolute paths back to this repo folder. If you move or delete the folder after installation, the hotkey service will point at the old location.

## Fedora Notes

On Fedora, the installer can use `dnf` to install missing packages such as `ydotool`, `acl`, and Python UI dependencies. It also configures uinput, input device access, a narrow sudoers rule for `ydotoold`, and the systemd user hotkey service.

The clean-tested Linux path was Fedora KDE Wayland.

## Non-Fedora Notes

On non-Fedora systems, install required packages with your distribution package manager before running the installer. If `dnf` is not available and required packages are missing, the installer reports the missing package list and exits.

Desktop-session behavior can vary. You may need to adapt package names, keyboard device permissions, ydotool availability, or terminal helper behavior for your environment.

## Expected Success Block

A successful tested install ends with:

```text
BOARD_OK=1
WATCHER_OK=1
YDO_OK=1
SERVICE_OK=1

PASS: Linux hotkey stack installed, enabled for login, started, and ScrollLock-open path was proven.
```

## Service Status Commands

Check whether the user service is active:

```bash
systemctl --user status emachination-prompt-rig-hotkeys.service --no-pager
```

Check only active/inactive state:

```bash
systemctl --user is-active emachination-prompt-rig-hotkeys.service
```

## Journal Troubleshooting Commands

Show recent logs:

```bash
journalctl --user -u emachination-prompt-rig-hotkeys.service -n 160 --no-pager
```

Follow logs while testing the hotkey:

```bash
journalctl --user -u emachination-prompt-rig-hotkeys.service -f
```

Look for `watching:` lines to confirm the watcher opened keyboard devices.

## Manual Board Start Command

Start the board directly from the repo folder:

```bash
bash launchers/linux/start_hotkey_board.sh
```

## Terminal Copy

Linux terminal-buffer copy helpers are experimental and can be intermittent. Terminal applications, Wayland/X11 session behavior, clipboard permissions, and compositor rules vary widely. The Fedora-proven installer focuses on the ScrollLock board-open path and the hotkey watcher service. For reliable terminal capture, prefer explicit transcript/provider workflows or manual copy/paste until the Linux terminal-copy layer is hardened.

---

Back to: [Start here](../START_HERE.md) | [Windows install](windows-install.md) | [Linux install](linux-install.md) | [Visual guide](visual-guide.md) | [README](../README.md)
