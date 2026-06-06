"""Saving run artifacts to `<method>/output/`.

Each method writes to its own `output/` subdirectory next to its code
(`baseline/output/`, `agent_linear/output/`, ...), where both the generated
appeal and the run log end up — everything from a single run in one place.
File names carry a timestamp, so successive runs don't overwrite each other.
The `output/` directories are kept out of git (artifacts).
"""

from __future__ import annotations

import sys
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path

# Repo root resolved from this file (independent of the current directory).
REPO_ROOT = Path(__file__).resolve().parents[1]


def approach_dir(approach: str) -> Path:
    """Artifact subdirectory for a method (`<approach>/output/`); creates it if missing."""
    path = REPO_ROOT / approach / "output"
    path.mkdir(parents=True, exist_ok=True)
    return path


@contextmanager
def tee_output(approach: str):
    """Mirror everything sent to ``stdout`` into a log file in the method's folder.

    This way prints from generation and evaluation (including the checks from
    `evaluate`) also end up in `<approach>/output/run_<YYYY-MM-DD_HHMMSS>.log` —
    for pasting/comparing without scrolling the terminal.

        with tee_output("baseline") as log_path:
            ...  # all print() output goes to the screen and to the file

    Returns the path of the log file.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    path = approach_dir(approach) / f"run_{timestamp}.log"
    log_file = path.open("w", encoding="utf-8")
    real_stdout = sys.stdout

    class _Tee:
        def write(self, data: str) -> int:
            real_stdout.write(data)
            log_file.write(data)
            return len(data)

        def flush(self) -> None:
            real_stdout.flush()
            log_file.flush()

    sys.stdout = _Tee()  # type: ignore[assignment]
    try:
        yield path
    finally:
        sys.stdout = real_stdout
        log_file.close()


def save_appeal(text: str, approach: str) -> Path:
    """Save an appeal to `<approach>/output/apelacja_<YYYY-MM-DD_HHMMSS>.txt`.

    Args:
        text: the appeal content.
        approach: approach name (e.g. "baseline", "agent_linear", "agent_planner").

    Returns:
        Path of the saved file.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    path = approach_dir(approach) / f"apelacja_{timestamp}.txt"
    path.write_text(text, encoding="utf-8")
    return path


def latest_appeal_path(approach: str) -> Path | None:
    """Return the path of the latest saved appeal for the given approach (or None).

    The timestamp in the name sorts lexicographically, so the last file after
    sorting is the newest.
    """
    files = sorted((REPO_ROOT / approach / "output").glob("apelacja_*.txt"))
    return files[-1] if files else None


def load_latest_appeal(approach: str) -> str:
    """Load the content of the most recently saved appeal for the given approach.

    Lets you run evaluation alone without generating the appeal anew.
    """
    path = latest_appeal_path(approach)
    if path is None:
        raise FileNotFoundError(
            f"Brak zapisanej apelacji dla podejścia '{approach}' w {REPO_ROOT / approach / 'output'}"
        )
    return path.read_text(encoding="utf-8")
