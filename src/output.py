"""Zapis artefaktów przebiegu do `data/output/<metoda>/`.

Każda metoda ma swój podfolder (`baseline/`, `agent_linear/`, ...), a w nim
lądują i wygenerowana apelacja, i log przebiegu — wszystko z jednego uruchomienia
w jednym miejscu. Nazwy plików mają znacznik czasu, więc kolejne przebiegi się nie
nadpisują. Katalog `data/output/` jest poza gitem (artefakty).
"""

from __future__ import annotations

import sys
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path

# Katalog na artefakty liczony od korzenia repo (niezależnie od bieżącego katalogu).
OUTPUT_DIR = Path(__file__).resolve().parents[1] / "data" / "output"


def approach_dir(approach: str) -> Path:
    """Podfolder danej metody (`data/output/<approach>/`); tworzy go, jeśli brak."""
    path = OUTPUT_DIR / approach
    path.mkdir(parents=True, exist_ok=True)
    return path


@contextmanager
def tee_output(approach: str):
    """Duplikuj wszystko, co leci na ``stdout``, do pliku logu w folderze metody.

    Dzięki temu printy z generacji i ewaluacji (m.in. checki z `evaluate`) lądują
    też w pliku `data/output/<approach>/run_<RRRR-MM-DD_GGMMSS>.log` — do
    wklejenia/porównania bez przewijania terminala.

        with tee_output("baseline") as log_path:
            ...  # wszystkie print() trafiają na ekran i do pliku

    Zwraca ścieżkę pliku logu.
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
    """Zapisz apelację do `data/output/<approach>/apelacja_<RRRR-MM-DD_GGMMSS>.txt`.

    Args:
        text: treść apelacji.
        approach: nazwa podejścia (np. "baseline", "agent_linear", "agent_planner").

    Returns:
        Ścieżka zapisanego pliku.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    path = approach_dir(approach) / f"apelacja_{timestamp}.txt"
    path.write_text(text, encoding="utf-8")
    return path


def latest_appeal_path(approach: str) -> Path | None:
    """Zwróć ścieżkę najnowszej zapisanej apelacji danego podejścia (lub None).

    Znacznik czasu w nazwie jest sortowalny leksykograficznie, więc ostatni plik
    po posortowaniu jest najnowszy.
    """
    files = sorted((OUTPUT_DIR / approach).glob("apelacja_*.txt"))
    return files[-1] if files else None


def load_latest_appeal(approach: str) -> str:
    """Wczytaj treść ostatnio zapisanej apelacji danego podejścia.

    Pozwala puścić samą ewaluację bez generowania apelacji od nowa.
    """
    path = latest_appeal_path(approach)
    if path is None:
        raise FileNotFoundError(
            f"Brak zapisanej apelacji dla podejścia '{approach}' w {OUTPUT_DIR / approach}"
        )
    return path.read_text(encoding="utf-8")
