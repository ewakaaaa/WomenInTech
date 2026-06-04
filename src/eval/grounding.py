"""Ewaluacja halucynacji — czy apelacja opiera się na faktach z akt sprawy.

Pokrycie (`coverage.py`) mówi, *czy* apelacja porusza wymagane zagadnienia.
Ta ewaluacja sprawdza coś innego: czy apelacja nie **zmyśla** — nie powołuje
faktów (dat, kwot, nazwisk, zdarzeń, cytatów), których w aktach nie ma.

Budujemy to etapowo:

  Etap 1: ekstrakcja atomowych twierdzeń faktycznych z apelacji.
  Etap 2: weryfikacja każdego twierdzenia względem akt — BEZ wczytywania
          wszystkich akt. Dwustopniowo:
            2a. dla twierdzenia LLM wybiera, w których plikach je sprawdzić
                (na podstawie krótkich OPISÓW dokumentów z file_description),
            2b. wczytujemy tylko tekst wybranych plików i dopiero w nich
                weryfikujemy fakt (supported / unsupported / contradicted).
  Etap 3: agregacja — wskaźnik halucynacji + lista podejrzanych twierdzeń.

    uv run python -m src.eval.grounding        # demo Etapów 1–2 na przykładzie

Pełna ewaluacja end-to-end (Etap 1→2→3): `evaluate_grounding(appeal_text, documents)`.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

from src.llm import call_llm
from src.loader import Document
from src.skills.file_description.main import generate_file_description
from src.skills.file_description.schemas import DescribedFile
from src.sources import prepare_input_texts

# ──────────────────────────────────────────────────────────────────────────
# Etap 1 — ekstrakcja twierdzeń faktycznych
# ──────────────────────────────────────────────────────────────────────────

EXTRACT_SYSTEM_PROMPT = (
    "Jesteś analitykiem, który rozkłada pismo procesowe na pojedyncze "
    "twierdzenia faktyczne (fakty), żeby można je było później zweryfikować "
    "względem akt sprawy.\n\n"
    "Wyciągnij WYŁĄCZNIE twierdzenia o faktach — coś, co da się sprawdzić w "
    "dokumentach: daty, godziny, kwoty, nazwiska, miejsca, przebieg zdarzeń, "
    "treść dowodów, co kto zeznał lub wyjaśnił, sygnatury, parametry (np. "
    "stężenie alkoholu, szerokość alejki).\n\n"
    "POMIŃ: oceny prawne, kwalifikacje czynów, wnioski apelacji, argumentację "
    "i interpretacje przepisów — to nie są fakty do weryfikacji.\n\n"
    "Każde twierdzenie sformułuj jako jedno samodzielne, konkretne zdanie "
    "(rozwiń zaimki, żeby było zrozumiałe bez kontekstu)."
)


class Claim(BaseModel):
    """Pojedyncze twierdzenie faktyczne wyciągnięte z apelacji."""

    claim: str = Field(..., description="Jedno samodzielne twierdzenie o faktach")
    quote: str = Field(
        ..., description="Krótki fragment apelacji, z którego pochodzi twierdzenie"
    )


class ClaimList(BaseModel):
    """Lista twierdzeń faktycznych z jednej apelacji."""

    claims: list[Claim] = Field(..., description="Wszystkie twierdzenia faktyczne")


def extract_claims(appeal_text: str, model: str | None = None) -> list[Claim]:
    """Etap 1: wyciągnij z apelacji listę atomowych twierdzeń faktycznych."""
    messages = [
        {"role": "system", "content": EXTRACT_SYSTEM_PROMPT},
        {"role": "user", "content": f"APELACJA:\n{appeal_text}"},
    ]
    return call_llm(messages, response_model=ClaimList, model=model).claims


# ──────────────────────────────────────────────────────────────────────────
# Etap 2 — weryfikacja twierdzenia względem akt (bez wczytywania wszystkich)
# ──────────────────────────────────────────────────────────────────────────

# Etap 2a: wybór plików do sprawdzenia na podstawie samych OPISÓW dokumentów.

SELECT_SYSTEM_PROMPT = (
    "Masz zweryfikować pojedyncze twierdzenie faktyczne z apelacji. Dostajesz "
    "listę dokumentów w aktach sprawy — każdy z krótkim opisem. Wskaż, w "
    "których dokumentach najprawdopodobniej znajduje się informacja "
    "potwierdzająca lub zaprzeczająca temu twierdzeniu.\n\n"
    "Wybierz tylko naprawdę istotne pliki (zwykle 1–3). Podaj DOKŁADNE nazwy "
    "plików z listy. Jeśli żaden dokument nie wydaje się właściwy, zwróć pustą "
    "listę."
)


class SourceSelection(BaseModel):
    """Wybór dokumentów, w których należy sprawdzić twierdzenie."""

    files: list[str] = Field(..., description="Nazwy plików do sprawdzenia")
    reasoning: str = Field(..., description="Krótkie uzasadnienie wyboru")


def _format_descriptions(described: list[DescribedFile]) -> str:
    """Złóż listę opisów dokumentów do promptu wyboru."""
    return "\n".join(
        f"- {d.name}: {d.title} — {d.description}" for d in described
    )


def select_sources(
    claim: str, described: list[DescribedFile], model: str | None = None
) -> SourceSelection:
    """Etap 2a: na podstawie opisów wybierz pliki, w których sprawdzić fakt."""
    messages = [
        {"role": "system", "content": SELECT_SYSTEM_PROMPT},
        {
            "role": "user",
            "content": (
                f"TWIERDZENIE:\n{claim}\n\n"
                f"DOSTĘPNE DOKUMENTY:\n{_format_descriptions(described)}"
            ),
        },
    ]
    selection = call_llm(messages, response_model=SourceSelection, model=model)
    # Zatrzymaj tylko nazwy faktycznie istniejące na liście (LLM bywa kreatywny).
    valid = {d.name for d in described}
    selection.files = [f for f in selection.files if f in valid]
    return selection


# Etap 2b: weryfikacja twierdzenia w treści wybranych plików.

VERIFY_SYSTEM_PROMPT = (
    "Jesteś weryfikatorem faktów. Oceniasz, czy podane twierdzenie z apelacji "
    "znajduje oparcie w załączonych fragmentach akt sprawy. Odpowiadaj WYŁĄCZNIE "
    "na podstawie tych fragmentów — nie korzystaj z wiedzy zewnętrznej.\n\n"
    "Zwróć status:\n"
    "- supported: akta wprost potwierdzają twierdzenie,\n"
    "- contradicted: akta mówią coś przeciwnego,\n"
    "- unsupported: w aktach brak informacji, by to potwierdzić (możliwa "
    "halucynacja).\n\n"
    "W polu evidence podaj krótki cytat z akt, na którym opierasz ocenę (lub "
    "pusty string, gdy brak)."
)


class ClaimVerdict(BaseModel):
    """Werdykt weryfikacji jednego twierdzenia względem akt."""

    status: Literal["supported", "unsupported", "contradicted"] = Field(
        ..., description="supported / unsupported / contradicted"
    )
    reasoning: str = Field(..., description="Krótkie uzasadnienie")
    evidence: str = Field(..., description="Cytat z akt lub pusty string")


def verify_claim(
    claim: str, sources_text: str, model: str | None = None
) -> ClaimVerdict:
    """Etap 2b: sprawdź twierdzenie w treści wybranych dokumentów."""
    if not sources_text.strip():
        return ClaimVerdict(
            status="unsupported",
            reasoning="Nie wybrano żadnego dokumentu do sprawdzenia.",
            evidence="",
        )
    messages = [
        {"role": "system", "content": VERIFY_SYSTEM_PROMPT},
        {
            "role": "user",
            "content": (
                f"TWIERDZENIE:\n{claim}\n\n"
                f"FRAGMENTY AKT:\n{sources_text}"
            ),
        },
    ]
    return call_llm(messages, response_model=ClaimVerdict, model=model)


class ClaimResult(ClaimVerdict):
    """Pełny wynik weryfikacji twierdzenia: wybór plików + werdykt."""

    claim: str = Field(..., description="Sprawdzane twierdzenie")
    checked_files: list[str] = Field(..., description="Pliki, w których sprawdzano")


def check_claim(
    claim: str,
    documents: list[Document],
    described: list[DescribedFile],
    model: str | None = None,
) -> ClaimResult:
    """Etap 2 (2a + 2b): wybierz pliki po opisach, wczytaj je i zweryfikuj fakt."""
    selection = select_sources(claim, described, model=model)
    sources_text = prepare_input_texts(documents, selection.files)
    verdict = verify_claim(claim, sources_text, model=model)
    return ClaimResult(
        claim=claim, checked_files=selection.files, **verdict.model_dump()
    )


def describe_documents(
    documents: list[Document],
    goal: str = "Zweryfikować fakty powołane w apelacji",
    model: str | None = None,
) -> list[DescribedFile]:
    """Opisz każdy dokument raz (file_description) — opisy zasilają Etap 2a."""
    return [generate_file_description(doc, goal, model=model) for doc in documents]


# ──────────────────────────────────────────────────────────────────────────
# Etap 3 — agregacja (wskaźnik halucynacji + lista podejrzanych)
# ──────────────────────────────────────────────────────────────────────────


class GroundingResult(BaseModel):
    """Zbiorczy wynik ewaluacji halucynacji dla jednej apelacji."""

    total: int = Field(..., description="Liczba sprawdzonych twierdzeń")
    supported: int = Field(..., description="Potwierdzone w aktach")
    unsupported: int = Field(..., description="Brak oparcia w aktach")
    contradicted: int = Field(..., description="Sprzeczne z aktami")
    hallucination_rate: float = Field(
        ..., description="(unsupported + contradicted) / total (0.0–1.0)"
    )
    results: list[ClaimResult] = Field(..., description="Werdykt per twierdzenie")


def evaluate_grounding(
    appeal_text: str,
    documents: list[Document],
    goal: str = "Zweryfikować fakty powołane w apelacji",
    model: str | None = None,
) -> GroundingResult:
    """Pełna ewaluacja halucynacji: Etap 1 → 2 → 3.

    1. wyciągnij twierdzenia faktyczne z apelacji,
    2. opisz akta raz i dla każdego twierdzenia wybierz pliki + zweryfikuj,
    3. policz wskaźnik halucynacji i zbierz raport.
    """
    claims = extract_claims(appeal_text, model=model)
    described = describe_documents(documents, goal, model=model)
    results = [check_claim(c.claim, documents, described, model=model) for c in claims]

    supported = sum(r.status == "supported" for r in results)
    unsupported = sum(r.status == "unsupported" for r in results)
    contradicted = sum(r.status == "contradicted" for r in results)
    total = len(results)
    return GroundingResult(
        total=total,
        supported=supported,
        unsupported=unsupported,
        contradicted=contradicted,
        hallucination_rate=(unsupported + contradicted) / total if total else 0.0,
        results=results,
    )


if __name__ == "__main__":
    # Demo Etapów 1–2 na mini-przykładzie (bez wczytywania prawdziwych PDF-ów).
    sample = (
        "Badanie alkomatem wykazało u oskarżonego 1,63 mg/l. Świadek Karol Kot "
        "zeznał, że widział oskarżonego dopiero po wjechaniu w alejkę cmentarną."
    )
    claims = extract_claims(sample)
    print(f"ETAP 1 — wyciągnięto {len(claims)} twierdzeń:\n")
    for i, c in enumerate(claims, 1):
        print(f"{i}. {c.claim}")

    # Sztuczne opisy dokumentów (w realu z describe_documents na aktach).
    described = [
        DescribedFile(
            name="03_Protokół_z_badania_stanu_trzeźwości.pdf",
            title="Protokół badania trzeźwości",
            description="Wynik badania alkomatem — stężenie alkoholu w wydechu.",
        ),
        DescribedFile(
            name="06_Protokół_przesłuchania_świadka.pdf",
            title="Przesłuchanie świadka",
            description="Zeznania świadka o przebiegu zdarzenia na cmentarzu.",
        ),
    ]
    print("\nETAP 2a — wybór plików dla pierwszego twierdzenia:")
    sel = select_sources(claims[0].claim, described)
    print(f"  wybrane: {sel.files}\n  bo: {sel.reasoning}")
