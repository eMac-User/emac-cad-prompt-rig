#!/usr/bin/env python3
"""
Provider-based Linux terminal copy helpers.

This module exists so Copy Terminal Buffer does not become a Konsole-only hack.

Provider result quality values:

- full
  The provider has proven that it copied full terminal scrollback.

- partial_visible_only
  The provider copied only the visible/current terminal text.

- unsupported
  The terminal/provider is detected but no safe full-copy strategy is implemented.

- failed
  A provider was attempted and failed.
"""

from __future__ import annotations

from dataclasses import dataclass
import json
import os
import re
from pathlib import Path
import shutil
import subprocess
import time


@dataclass(frozen=True)
class TerminalCopyResult:
    ok: bool
    text: str
    message: str
    provider: str = "none"
    quality: str = "failed"


TRANSCRIPT_ENV_VAR = "VEYDRANET_TERMINAL_TRANSCRIPT"
TRANSCRIPT_MAX_AGE_ENV_VAR = "VEYDRANET_TERMINAL_TRANSCRIPT_MAX_AGE_SECONDS"
COPY_MODE_ENV_VAR = "VEYDRANET_TERMINAL_COPY_MODE"
DEFAULT_TRANSCRIPT_NAME = "veydranet_terminal_transcript.log"
DEFAULT_TRANSCRIPT_MAX_AGE_SECONDS = 30 * 60
TRANSCRIPT_REGISTRY_FILE_NAME = "veydranet_terminal_transcripts.registry"


def configured_terminal_copy_mode() -> str:
    """Return terminal copy mode: auto, transcript, live, or konsole."""
    configured = os.environ.get(COPY_MODE_ENV_VAR, "auto").strip().lower()
    if configured not in {"auto", "transcript", "live", "konsole"}:
        return "auto"
    return configured


def default_terminal_transcript_path() -> Path:
    """Return the default VeydraNet terminal transcript path."""
    runtime_dir = os.environ.get("XDG_RUNTIME_DIR") or "/tmp"
    return Path(runtime_dir) / DEFAULT_TRANSCRIPT_NAME


def configured_terminal_transcript_path() -> Path:
    """Return the configured transcript path, or the default runtime path."""
    configured = os.environ.get(TRANSCRIPT_ENV_VAR, "").strip()
    if configured:
        return Path(configured).expanduser()
    return default_terminal_transcript_path()

def configured_terminal_transcript_max_age_seconds() -> float:
    """Return max allowed transcript age in seconds."""
    configured = os.environ.get(TRANSCRIPT_MAX_AGE_ENV_VAR, "").strip()
    if not configured:
        return float(DEFAULT_TRANSCRIPT_MAX_AGE_SECONDS)

    try:
        seconds = float(configured)
    except ValueError:
        return float(DEFAULT_TRANSCRIPT_MAX_AGE_SECONDS)

    return max(0.0, seconds)


def sanitize_terminal_transcript_text(text: str) -> str:
    """Strip terminal control sequences from script/PTY transcript text."""
    # OSC sequences, including OSC 52 clipboard writes: ESC ] ... BEL or ESC ] ... ESC \
    text = re.sub(r"\x1b\][^\x07\x1b]*(?:\x07|\x1b\\)", "", text)

    # CSI sequences: colors, cursor movement, alternate screen, mouse tracking, etc.
    text = re.sub(r"\x1b\[[0-?]*[ -/]*[@-~]", "", text)

    # Charset selection and simple ESC sequences, for example ESC(B.
    text = re.sub(r"\x1b[()][A-Za-z0-9]", "", text)
    text = re.sub(r"\x1b[@-Z\\-_]", "", text)

    # Drop any remaining ESC characters.
    text = text.replace("\x1b", "")

    # Normalize carriage returns from terminal redraws.
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    # Remove non-printing controls except tab/newline.
    text = "".join(ch for ch in text if ch == "\n" or ch == "\t" or ord(ch) >= 32)

    # Trim excessive blank vertical space from full-screen TUIs.
    lines = text.splitlines()
    cleaned: list[str] = []
    blank_count = 0
    for line in lines:
        if line.strip():
            blank_count = 0
            cleaned.append(line.rstrip())
        else:
            blank_count += 1
            if blank_count <= 2:
                cleaned.append("")

    return "\n".join(cleaned).strip() + "\n"


def transcript_path_is_explicitly_configured() -> bool:
    """Return whether the transcript path came from an explicit environment setting."""
    return bool(os.environ.get(TRANSCRIPT_ENV_VAR, "").strip())


def terminal_transcript_pid_path(transcript_path: Path) -> Path:
    """Return the live transcript owner PID file path."""
    return Path(f"{transcript_path}.pid")


def read_terminal_transcript_pid(pid_path: Path) -> int | None:
    """Read a transcript owner PID from a pid file."""
    try:
        raw_pid = pid_path.read_text(encoding="utf-8").strip()
    except OSError:
        return None

    try:
        pid = int(raw_pid)
    except ValueError:
        return None

    return pid if pid > 0 else None


def process_is_alive(pid: int) -> bool:
    """Return whether a process id appears alive."""
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    except OSError:
        return False
    return True


def default_transcript_requires_live_owner(transcript_path: Path) -> TerminalCopyResult | None:
    """
    Refuse default transcript copy unless the launcher-owned PID is alive.

    Explicit VEYDRANET_TERMINAL_TRANSCRIPT paths are treated as controlled harness/config input.
    The default runtime transcript must prove an active launcher to avoid copying old terminal output.
    """
    if transcript_path_is_explicitly_configured():
        return None

    pid_path = terminal_transcript_pid_path(transcript_path)
    pid = read_terminal_transcript_pid(pid_path)
    if pid is None:
        return TerminalCopyResult(
            ok=False,
            text="",
            message=(
                "UNSUPPORTED: VeydraNet terminal transcript is not active; "
                f"missing live transcript PID file: {pid_path}. "
                "Launch an active transcript terminal with "
                "launchers/linux/start_transcript_terminal.sh or "
                "launchers/linux/start_claude_transcript_terminal.sh."
            ),
            provider="veydranet_transcript_file",
            quality="unsupported",
        )

    if not process_is_alive(pid):
        return TerminalCopyResult(
            ok=False,
            text="",
            message=(
                "UNSUPPORTED: VeydraNet terminal transcript is not active; "
                f"transcript owner PID is not running: {pid}. "
                f"PID file: {pid_path}. "
                "Launch a new active transcript terminal before using Copy Terminal Buffer."
            ),
            provider="veydranet_transcript_file",
            quality="unsupported",
        )

    return None



def transcript_has_live_owner(transcript_path: Path) -> bool:
    """Return whether a transcript path has a live owner PID file."""
    pid_path = terminal_transcript_pid_path(transcript_path)
    pid = read_terminal_transcript_pid(pid_path)
    if pid is None:
        return False
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    return True

def copy_terminal_transcript_file() -> TerminalCopyResult:
    """
    Copy the VeydraNet-managed terminal transcript file.

    This provider is allowed to report quality=full because it reads the full
    transcript file that VeydraNet owns. It does not claim to scrape full
    scrollback from Konsole, Black Box, or any other terminal emulator.
    """
    transcript_path = configured_terminal_transcript_path()

    if not transcript_path.exists():
        return TerminalCopyResult(
            ok=False,
            text="",
            message=(
                "UNSUPPORTED: no VeydraNet terminal transcript file exists yet. "
                f"Expected transcript path: {transcript_path}"
            ),
            provider="veydranet_transcript_file",
            quality="unsupported",
        )

    if not transcript_path.is_file():
        return TerminalCopyResult(
            ok=False,
            text="",
            message=f"ERROR: transcript path is not a file: {transcript_path}",
            provider="veydranet_transcript_file",
            quality="failed",
        )

    try:
        transcript_stat = transcript_path.stat()
    except OSError as exc:
        return TerminalCopyResult(
            ok=False,
            text="",
            message=f"ERROR: could not stat transcript file {transcript_path}: {exc}",
            provider="veydranet_transcript_file",
            quality="failed",
        )

    inactive_result = default_transcript_requires_live_owner(transcript_path)
    if inactive_result is not None:
        return inactive_result

    has_live_owner = transcript_has_live_owner(transcript_path)
    max_age_seconds = configured_terminal_transcript_max_age_seconds()
    transcript_age_seconds = max(0.0, time.time() - transcript_stat.st_mtime)
    if transcript_age_seconds > max_age_seconds and not has_live_owner:
        return TerminalCopyResult(
            ok=False,
            text="",
            message=(
                "UNSUPPORTED: VeydraNet terminal transcript file is stale "
                f"({transcript_age_seconds:.0f}s old; max age {max_age_seconds:.0f}s). "
                f"Expected transcript path: {transcript_path}. "
                "Launch a transcript terminal with launchers/linux/start_transcript_terminal.sh "
                "or launchers/linux/start_claude_transcript_terminal.sh."
            ),
            provider="veydranet_transcript_file",
            quality="unsupported",
        )

    try:
        transcript_text = transcript_path.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        return TerminalCopyResult(
            ok=False,
            text="",
            message=f"ERROR: could not read transcript file {transcript_path}: {exc}",
            provider="veydranet_transcript_file",
            quality="failed",
        )

    if not transcript_text.strip():
        return TerminalCopyResult(
            ok=False,
            text="",
            message=f"UNSUPPORTED: transcript file is empty: {transcript_path}",
            provider="veydranet_transcript_file",
            quality="unsupported",
        )

    sanitized_text = sanitize_terminal_transcript_text(transcript_text)
    if not sanitized_text.strip():
        return TerminalCopyResult(
            ok=False,
            text="",
            message=f"UNSUPPORTED: transcript file has no readable text after sanitizing terminal controls: {transcript_path}",
            provider="veydranet_transcript_file",
            quality="unsupported",
        )

    return TerminalCopyResult(
        ok=True,
        text=sanitized_text,
        message=f"FULL: copied sanitized VeydraNet terminal transcript file: {transcript_path}",
        provider="veydranet_transcript_file",
        quality="full",
    )


def konsole_dbus_services() -> list[str]:
    """Return active Konsole DBus service names."""
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
    """Return Konsole /Sessions/N DBus object paths for a service."""
    proc = subprocess.run(["qdbus", service], check=False, capture_output=True, text=True)
    if proc.returncode != 0:
        return []

    objects: list[str] = []
    for line in proc.stdout.splitlines():
        obj = line.strip()
        if obj.startswith("/Sessions/"):
            objects.append(obj)

    def session_sort_key(obj: str) -> tuple[int, str]:
        try:
            return (int(obj.rsplit("/", 1)[1]), obj)
        except Exception:
            return (999999, obj)

    return sorted(objects, key=session_sort_key)


def copy_konsole_visible_text() -> TerminalCopyResult:
    """
    Read visible/current terminal text from KDE Konsole through DBus.

    This provider is intentionally marked partial_visible_only. Fedora KDE/Konsole
    testing showed getAllDisplayedText copied only the visible/current terminal
    section, while getDisplayedText ranges and KMainWindow select/copy actions
    did not produce full scrollback.
    """
    if not shutil.which("qdbus"):
        return TerminalCopyResult(
            ok=False,
            text="",
            message="ERROR: qdbus not found; Konsole terminal copy provider unavailable.",
            provider="konsole_dbus_visible",
            quality="failed",
        )

    services = konsole_dbus_services()
    if not services:
        return TerminalCopyResult(
            ok=False,
            text="",
            message="ERROR: Konsole provider unavailable; no active Konsole DBus service found.",
            provider="konsole_dbus_visible",
            quality="unsupported",
        )

    last_error = ""
    for service in services:
        sessions = konsole_session_objects(service)
        if not sessions:
            last_error = f"No Konsole sessions found for DBus service {service}."
            continue

        for session in sessions:
            attempts = [
                ["qdbus", service, session, "org.kde.konsole.Session.getAllDisplayedText", "true"],
                ["qdbus", service, session, "org.kde.konsole.Session.getAllDisplayedText"],
            ]
            for command in attempts:
                proc = subprocess.run(command, check=False, capture_output=True, text=True)
                if proc.returncode != 0:
                    last_error = proc.stderr.strip() or proc.stdout.strip() or f"qdbus failed for {service} {session}"
                    continue

                terminal_text = proc.stdout
                if terminal_text.strip():
                    return TerminalCopyResult(
                        ok=True,
                        text=terminal_text,
                        message="PARTIAL: copied visible Konsole text only; full scrollback copy is not implemented for this provider yet.",
                        provider="konsole_dbus_visible",
                        quality="partial_visible_only",
                    )

                last_error = f"Konsole returned empty visible terminal text for {service} {session}."

    return TerminalCopyResult(
        ok=False,
        text="",
        message=f"ERROR: could not read visible Konsole terminal text. {last_error}".strip(),
        provider="konsole_dbus_visible",
        quality="failed",
    )


def detect_installed_terminal_families() -> list[str]:
    """Return installed terminal families that future providers may support."""
    detected: list[str] = []

    if shutil.which("konsole"):
        detected.append("konsole")

    if shutil.which("blackbox-terminal") or shutil.which("blackbox") or shutil.which("com.raggesilver.BlackBox"):
        detected.append("blackbox_vte")

    if shutil.which("gnome-terminal"):
        detected.append("gnome_terminal_vte")

    if shutil.which("tilix"):
        detected.append("tilix_vte")

    if shutil.which("xfce4-terminal"):
        detected.append("xfce4_terminal_vte")

    if shutil.which("kitty"):
        detected.append("kitty")

    if shutil.which("alacritty"):
        detected.append("alacritty")

    if shutil.which("wezterm"):
        detected.append("wezterm")

    return detected


def default_registry_path() -> Path:
    """Return the default VeydraNet terminal transcript registry path."""
    runtime_dir = os.environ.get("XDG_RUNTIME_DIR") or "/tmp"
    return Path(runtime_dir) / TRANSCRIPT_REGISTRY_FILE_NAME


def read_registry_sessions(
    registry_path: Path | None = None,
) -> list[dict]:
    """Read transcript registry JSONL sessions."""
    if registry_path is None:
        registry_path = default_registry_path()
    if not registry_path.is_file():
        return []

    sessions: list[dict] = []
    try:
        raw = registry_path.read_text(
            encoding="utf-8",
            errors="replace",
        )
    except OSError:
        return []

    for line in raw.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except (ValueError, TypeError):
            continue
        if not isinstance(obj, dict):
            continue
        if "transcript_path" not in obj:
            continue
        if "pid_path" not in obj:
            continue
        sessions.append(obj)

    return sessions


def find_best_live_registry_session(
    registry_path: Path | None = None,
) -> dict | None:
    """Return newest live transcript registry session."""
    live: list[tuple[float, dict]] = []

    for session in read_registry_sessions(registry_path):
        transcript_path = Path(session["transcript_path"])
        pid_path = Path(session["pid_path"])

        if not transcript_path.is_file():
            continue

        pid = read_terminal_transcript_pid(pid_path)
        if pid is None:
            continue
        if not process_is_alive(pid):
            continue

        try:
            mtime = transcript_path.stat().st_mtime
        except OSError:
            continue

        live.append((mtime, session))

    if not live:
        return None

    live.sort(key=lambda item: item[0], reverse=True)
    return live[0][1]


def copy_terminal_buffer_with_provider() -> TerminalCopyResult:
    """
    Try terminal copy providers in current-safe order.

    auto/transcript:
        explicit transcript env -> registry -> default transcript path.
        Never falls back to partial visible terminal text.

    live:
        visible/current Konsole provider is allowed and may be partial.
    """
    copy_mode = configured_terminal_copy_mode()

    if copy_mode == "live":
        live_result = copy_konsole_visible_text()
        if live_result.ok and live_result.text.strip():
            return live_result

        detected = detect_installed_terminal_families()
        if detected:
            message = (
                live_result.message
                + " Detected terminal families: "
                + ", ".join(detected)
                + ". Live mode attempted the visible/current "
                + "Konsole provider."
            )
            return TerminalCopyResult(
                ok=False,
                text="",
                message=message,
                provider=live_result.provider,
                quality=live_result.quality,
            )

        return live_result

    if not transcript_path_is_explicitly_configured():
        best = find_best_live_registry_session()
        if best is not None:
            session_path = best["transcript_path"]
            old_value = os.environ.get(TRANSCRIPT_ENV_VAR)
            os.environ[TRANSCRIPT_ENV_VAR] = session_path
            try:
                registry_result = copy_terminal_transcript_file()
            finally:
                if old_value is None:
                    os.environ.pop(TRANSCRIPT_ENV_VAR, None)
                else:
                    os.environ[TRANSCRIPT_ENV_VAR] = old_value

            if registry_result.ok:
                if registry_result.quality == "full":
                    return TerminalCopyResult(
                        ok=True,
                        text=registry_result.text,
                        message=(
                            "FULL: registry session selected: "
                            + session_path
                        ),
                        provider="veydranet_transcript_file",
                        quality="full",
                    )

    copy_mode = configured_terminal_copy_mode()

    if copy_mode in {"konsole", "live"}:
        live_result = copy_konsole_visible_text()
        if live_result.ok and live_result.text.strip():
            return live_result
        return live_result

    if copy_mode == "transcript":
        return copy_terminal_transcript_file()

    transcript_result = copy_terminal_transcript_file()
    if transcript_result.ok:
        if transcript_result.quality == "full":
            return transcript_result

    detected = detect_installed_terminal_families()
    if detected:
        message = (
            transcript_result.message
            + " UNSUPPORTED: full terminal-emulator scrollback "
            + "copy is not implemented yet. Detected terminal "
            + "families: "
            + ", ".join(detected)
            + ". Set VEYDRANET_TERMINAL_COPY_MODE=live to "
            + "explicitly copy visible/current Konsole text."
        )
        return TerminalCopyResult(
            ok=False,
            text="",
            message=message,
            provider="provider_matrix",
            quality="unsupported",
        )

    return transcript_result
