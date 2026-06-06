"""Opisy dokumentów (file_description) wraz z cache na dysku.

Opisanie akt to po jednym wywołaniu LLM na dokument — kosztowne, a wynik jest
wielokrotnie używany (agent liniowy, langgraph, planer, grounding). Liczymy więc
raz, zapisujemy do JSON, a kolejne przebiegi/agenci wczytują gotowe opisy.

Cache leży w `data/output/described.json` (poza gitem). `refresh=True` przelicza
od nowa (np. po zmianie modelu — opisy zależą od modelu).
"""

from __future__ import annotations

import json
from pathlib import Path

from src.loader import Document, load_all
from src.skills.file_description.main import generate_file_description
from src.skills.file_description.schemas import DescribedFile

CACHE_PATH = Path(__file__).resolve().parents[1] / "data" / "output" / "described.json"
DEFAULT_GOAL = "Zrozumieć akta sprawy i wskazać, co zawiera każdy dokument"


def describe_documents(
    documents: list[Document], goal: str = DEFAULT_GOAL, model: str | None = None
) -> list[DescribedFile]:
    """Opisz każdy dokument (jedno wywołanie LLM na plik)."""
    return [generate_file_description(doc, goal, model=model) for doc in documents]


def descriptions_cached(path: str | Path = CACHE_PATH) -> bool:
    """Czy istnieje zapisany cache opisów."""
    return Path(path).exists()


def save_descriptions(
    described: list[DescribedFile], path: str | Path = CACHE_PATH
) -> Path:
    """Zapisz opisy do JSON (czytelny UTF-8)."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = [d.model_dump() for d in described]
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


def load_descriptions(path: str | Path = CACHE_PATH) -> list[DescribedFile]:
    """Wczytaj opisy z cache."""
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    return [DescribedFile(**d) for d in data]


def get_descriptions(
    documents: list[Document] | None = None,
    goal: str = DEFAULT_GOAL,
    model: str | None = None,
    refresh: bool = False,
    path: str | Path = CACHE_PATH,
) -> list[DescribedFile]:
    """Zwróć opisy z cache; jeśli go nie ma (lub refresh=True) — policz i zapisz.

    Liczy raz, kolejne wywołania (też z innych agentów) wczytują z pliku.
    """
    if not refresh and descriptions_cached(path):
        return load_descriptions(path)
    docs = documents if documents is not None else load_all()
    described = describe_documents(docs, goal, model=model)
    save_descriptions(described, path)
    return described
