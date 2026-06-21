#!/usr/bin/env python3
"""
Linux keyboard action watcher for VeydraNet Hotkey Board.

Current Linux KDE/Konsole behavior:
- ScrollLock opens the Linux hotkey board.
- Insert sends "clear" plus Enter to the active Konsole session path.
- PageUp sends "Ok, continue" plus Enter to the active Konsole session path.

This uses raw Linux input events for key detection and Konsole DBus for
terminal text sending. It uses only the Python standard library plus the
already-installed qdbus command.
"""

from __future__ import annotations

import argparse
import glob
import os
import select
import shutil
import struct
import subprocess
import time
from pathlib import Path

EV_KEY = 0x01

KEY_PAGEUP = 104
KEY_INSERT = 110
KEY_SCROLLLOCK = 70

KEY_PRESS = 1
EVENT_STRUCT = "llHHI"
EVENT_SIZE = struct.calcsize(EVENT_STRUCT)

KEY_NAMES = {
    KEY_SCROLLLOCK: "ScrollLock",
    KEY_INSERT: "Insert",
    KEY_PAGEUP: "PageUp",
    28: "Enter",
    69: "NumLock",
    70: "ScrollLock",
    97: "RightCtrl",
    102: "Home",
    104: "PageUp",
    107: "End",
    109: "PageDown",
    110: "Insert",
    111: "Delete",
    119: "Pause",
    272: "MouseLeft",
}


def unique_paths(paths: list[str]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for raw in paths:
        try:
            resolved = str(Path(raw).resolve())
        except Exception:
            resolved = raw
        if resolved in seen:
            continue
        seen.add(resolved)
        out.append(raw)
    return out


def keyboard_device_candidates() -> list[str]:
    """
    Return all likely keyboard event devices.

    Do not stop at /dev/input/by-path/*-event-kbd. On KDE/VMware, some keys
    can arrive through another /dev/input/event* device even when ScrollLock
    appears on the by-path keyboard device.
    """
    by_path = sorted(glob.glob("/dev/input/by-path/*-event-kbd"))
    event_paths = sorted(glob.glob("/dev/input/event*"))
    return unique_paths(by_path + event_paths)


def open_devices(device_paths: list[str]) -> dict[int, str]:
    opened: dict[int, str] = {}
    for path in device_paths:
        try:
            fd = os.open(path, os.O_RDONLY | os.O_NONBLOCK)
            opened[fd] = path
            print(f"watching: {path}", flush=True)
        except PermissionError:
            print(f"permission denied: {path}", flush=True)
        except OSError as exc:
            print(f"cannot open: {path}: {exc}", flush=True)
    return opened


def konsole_dbus_services() -> list[str]:
    if not shutil.which("qdbus"):
        return []

    proc = subprocess.run(["qdbus"], check=False, capture_output=True, text=True)
    if proc.returncode != 0:
        return []

    services: list[str] = []
    for line in proc.stdout.splitlines():
        service = line.strip()
        if service.startswith("org.kde.konsole-"):
            services.append(service)
    return services


def konsole_session_objects(service: str) -> list[str]:
    proc = subprocess.run(["qdbus", service], check=False, capture_output=True, text=True)
    if proc.returncode != 0:
        return []

    sessions: list[str] = []
    for line in proc.stdout.splitlines():
        obj = line.strip()
        if obj.startswith("/Sessions/"):
            sessions.append(obj)

    def session_sort_key(obj: str) -> tuple[int, str]:
        try:
            return (int(obj.rsplit("/", 1)[1]), obj)
        except Exception:
            return (999999, obj)

    return sorted(sessions, key=session_sort_key)


def send_text_to_konsole(text: str) -> tuple[bool, str]:
    """
    Send text to the first available Konsole session through DBus.

    The text may include a trailing newline. For the current eMachination CAD Patent Prompt-Rig Linux
    parity behavior, Insert and PageUp both send text plus Enter.
    """
    if not shutil.which("qdbus"):
        return False, "ERROR: qdbus not found; cannot send text to Konsole."

    services = konsole_dbus_services()
    if not services:
        return False, "ERROR: no active Konsole DBus service found."

    last_error = ""
    for service in services:
        sessions = konsole_session_objects(service)
        if not sessions:
            last_error = f"No Konsole sessions found for {service}."
            continue

        for session in sessions:
            proc = subprocess.run(
                ["qdbus", service, session, "org.kde.konsole.Session.sendText", text],
                check=False,
                capture_output=True,
                text=True,
            )
            if proc.returncode == 0:
                printable = text.replace("\n", "\\n")
                return True, f"Sent to Konsole {service} {session}: {printable}"

            last_error = proc.stderr.strip() or proc.stdout.strip() or f"qdbus sendText failed for {service} {session}"

    return False, f"ERROR: could not send text to Konsole. {last_error}".strip()


def run_launcher(launcher: Path) -> None:
    print(f"ScrollLock pressed; launching board: {launcher}", flush=True)
    subprocess.Popen(
        ["bash", str(launcher)],
        cwd=str(launcher.parents[2]),
        start_new_session=True,
    )


def run_repo_script(script_name: str) -> tuple[bool, str]:
    repo_root = Path(__file__).resolve().parents[1]
    script = repo_root / "launchers" / "linux" / script_name

    if not script.is_file():
        return False, f"ERROR: script not found: {script}"

    proc = subprocess.run(
        ["bash", str(script)],
        check=False,
        capture_output=True,
        text=True,
    )

    if proc.returncode == 0:
        return True, f"Ran {script}"

    message = proc.stderr.strip() or proc.stdout.strip() or f"script failed: {script}"
    return False, f"ERROR: {message}"


def handle_keypress(code: int, launcher: Path) -> None:
    if code == KEY_SCROLLLOCK:
        run_launcher(launcher)
        return

    if code == KEY_INSERT:
        ok, message = run_repo_script("send_clear_enter.sh")
        print(f"Insert pressed; {message}", flush=True)
        return

    if code == KEY_PAGEUP:
        ok, message = run_repo_script("send_ok_continue_enter.sh")
        print(f"PageUp pressed; {message}", flush=True)
        return

    print(f"Unhandled key code: {code}", flush=True)


def watch_keyboard_actions(device_paths: list[str], launcher: Path, debounce_seconds: float) -> int:
    opened = open_devices(device_paths)
    if not opened:
        print("ERROR: no readable keyboard event devices found.", flush=True)
        print("Grant this user read access to /dev/input/by-path/*-event-kbd, then start watcher again.", flush=True)
        return 2

    last_action_by_code: dict[int, float] = {}
    watched_codes = {KEY_SCROLLLOCK, KEY_INSERT, KEY_PAGEUP}

    print("eMachination CAD Patent Prompt-Rig keyboard action watcher is running.", flush=True)
    print("ScrollLock -> open board", flush=True)
    print("Insert -> send clear + Enter to Konsole", flush=True)
    print("PageUp -> send Ok, continue + Enter to Konsole", flush=True)

    try:
        while True:
            readable, _, _ = select.select(list(opened.keys()), [], [], 1.0)
            for fd in readable:
                try:
                    data = os.read(fd, EVENT_SIZE * 64)
                except BlockingIOError:
                    continue
                except OSError as exc:
                    print(f"device read failed: {opened.get(fd, fd)}: {exc}", flush=True)
                    continue

                for offset in range(0, len(data) - EVENT_SIZE + 1, EVENT_SIZE):
                    sec, usec, event_type, code, value = struct.unpack(
                        EVENT_STRUCT,
                        data[offset : offset + EVENT_SIZE],
                    )
                    if event_type != EV_KEY or value != KEY_PRESS:
                        continue

                    key_name = KEY_NAMES.get(code, f"KEY_CODE_{code}")
                    print(f"key press seen: device={opened.get(fd, fd)} code={code} name={key_name}", flush=True)

                    if code not in watched_codes:
                        continue

                    now = time.monotonic()
                    last_action = last_action_by_code.get(code, 0.0)
                    if now - last_action < debounce_seconds:
                        print(f"{KEY_NAMES.get(code, code)} press ignored by debounce.", flush=True)
                        continue

                    last_action_by_code[code] = now
                    handle_keypress(code, launcher)
    finally:
        for fd in list(opened):
            try:
                os.close(fd)
            except OSError:
                pass


def main() -> int:
    parser = argparse.ArgumentParser(description="Watch Linux input devices for VeydraNet keyboard actions.")
    parser.add_argument(
        "--launcher",
        default=str(
            Path(__file__).resolve().parent.parent
            / "launchers"
            / "linux"
            / "start_hotkey_board.sh"
        ),
        help="Exact launcher script to run when ScrollLock is pressed.",
    )
    parser.add_argument(
        "--device",
        action="append",
        default=[],
        help="Exact /dev/input event device to watch. May be repeated. Default: /dev/input/by-path/*-event-kbd.",
    )
    parser.add_argument(
        "--list-devices",
        action="store_true",
        help="Print candidate keyboard event devices and exit.",
    )
    parser.add_argument(
        "--debounce-seconds",
        type=float,
        default=1.0,
        help="Minimum seconds between repeated actions for the same key.",
    )
    args = parser.parse_args()

    launcher = Path(args.launcher)
    if not launcher.is_file():
        print(f"ERROR: launcher not found: {launcher}", flush=True)
        return 1

    devices = args.device or keyboard_device_candidates()
    if args.list_devices:
        print("Keyboard event device candidates:")
        for device in devices:
            print(device)
        return 0

    return watch_keyboard_actions(devices, launcher, args.debounce_seconds)


if __name__ == "__main__":
    raise SystemExit(main())
