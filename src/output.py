"""Zapis wygenerowanych apelacji do data/output/.

Nazwa pliku zawiera podejście i znacznik czasu, więc widać, z jakiego przebiegu
pochodzi dana apelacja. Katalog `data/output/` jest poza gitem (artefakty).
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

# Katalog na artefakty liczony od korzenia repo (niezależnie od bieżącego katalogu).
OUTPUT_DIR = Path(__file__).resolve().parents[1] / "data" / "output"


def save_appeal(text: str, approach: str) -> Path:
    """Zapisz apelację do `data/output/apelacja_<approach>_<RRRR-MM-DD_GGMMSS>.txt`.

    Args:
        text: treść apelacji.
        approach: nazwa podejścia (np. "baseline", "agent_linear", "agent_planner").

    Returns:
        Ścieżka zapisanego pliku.
    """
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    path = OUTPUT_DIR / f"apelacja_{approach}_{timestamp}.txt"
    path.write_text(text, encoding="utf-8")
    return path
