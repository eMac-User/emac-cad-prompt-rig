#!/usr/bin/env python3
"""
Raw Linux key-event probe for VeydraNet Hotkey Board.

Use this to discover what Fedora receives when a physical key is pressed.
It prints EV_KEY events from readable keyboard event devices.
"""

from __future__ import annotations

import argparse
import glob
import os
import select
import struct
import time
from pathlib import Path

EV_KEY = 0x01
EVENT_STRUCT = "llHHI"
EVENT_SIZE = struct.calcsize(EVENT_STRUCT)

KEY_NAMES = {
    1: "KEY_ESC",
    28: "KEY_ENTER",
    29: "KEY_LEFTCTRL",
    42: "KEY_LEFTSHIFT",
    54: "KEY_RIGHTSHIFT",
    56: "KEY_LEFTALT",
    58: "KEY_CAPSLOCK",
    69: "KEY_NUMLOCK",
    70: "KEY_SCROLLLOCK",
    97: "KEY_RIGHTCTRL",
    100: "KEY_RIGHTALT",
    102: "KEY_HOME",
    104: "KEY_PAGEUP",
    107: "KEY_END",
    109: "KEY_PAGEDOWN",
    110: "KEY_INSERT",
    111: "KEY_DELETE",
    119: "KEY_PAUSE",
    125: "KEY_LEFTMETA",
    126: "KEY_RIGHTMETA",
}

VALUE_NAMES = {
    0: "release",
    1: "press",
    2: "repeat",
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


def probe(device_paths: list[str], seconds: float) -> int:
    opened = open_devices(device_paths)
    if not opened:
        print("ERROR: no readable event devices found.", flush=True)
        return 2

    print("", flush=True)
    print("Press ScrollLock now. Also try Pause/Break if ScrollLock prints nothing.", flush=True)
    print(f"Probe window: {seconds:.1f} seconds", flush=True)
    print("", flush=True)

    stop_at = time.monotonic() + seconds
    while time.monotonic() < stop_at:
        timeout = max(0.1, min(1.0, stop_at - time.monotonic()))
        readable, _, _ = select.select(list(opened.keys()), [], [], timeout)
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
                if event_type != EV_KEY:
                    continue
                name = KEY_NAMES.get(code, f"KEY_CODE_{code}")
                value_name = VALUE_NAMES.get(value, str(value))
                print(
                    f"device={opened[fd]} type=EV_KEY code={code} name={name} value={value} action={value_name}",
                    flush=True,
                )

    for fd in list(opened):
        try:
            os.close(fd)
        except OSError:
            pass
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Print raw Linux EV_KEY events.")
    parser.add_argument("--seconds", type=float, default=20.0)
    parser.add_argument("--device", action="append", default=[])
    args = parser.parse_args()

    devices = args.device or keyboard_device_candidates()
    return probe(devices, args.seconds)


if __name__ == "__main__":
    raise SystemExit(main())
