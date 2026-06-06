"""Ocena „miękka" apelacji — jakość/forma jak u egzaminatora.

Pokrycie (`coverage.py`) sprawdza, **czy** poruszono wymagane zagadnienia (twardy
klucz). Ta ocena patrzy inaczej — tak, jak egzaminator na egzaminie radcowskim,
wg ustawowych kryteriów (art. 36(4) ustawy o radcach prawnych):

  1. zachowanie wymogów formalnych,
  2. właściwość zastosowania przepisów prawa i umiejętność ich interpretacji,
  3. poprawność zaproponowanego rozwiązania.

Każde kryterium w skali ocen egzaminu: 6 (celujący) … 2 (niedostateczny).
"""

from __future__ import annotations

from pydantic import BaseModel, Field

from src.llm import call_llm

QUALITY_SYSTEM_PROMPT = (
    "Jesteś doświadczonym egzaminatorem na egzaminie radcowskim z prawa karnego. "
    "Oceniasz sporządzoną przez zdającego apelację — nie tylko to, czy odhacza "
    "punkty, ale JAK jest napisana.\n\n"
    "Oceń pismo wg trzech ustawowych kryteriów (art. 36(4) ustawy o radcach "
    "prawnych), każde w skali: 6 = celujący, 5 = bardzo dobry, 4 = dobry, "
    "3 = dostateczny, 2 = niedostateczny:\n"
    "1. WYMOGI FORMALNE — właściwy sąd odwoławczy (od wyroku sądu rejonowego "
    "apelację rozpoznaje sąd okręgowy), wniesienie za pośrednictwem sądu I "
    "instancji, oznaczenie stron, zakres zaskarżenia, zarzuty z podstawą prawną, "
    "wnioski, uzasadnienie, podpis.\n"
    "2. ZASTOSOWANIE I INTERPRETACJA PRZEPISÓW — trafność powołanych podstaw "
    "(art. 438 k.p.k. itd.), poprawność i precyzja argumentacji prawnej.\n"
    "3. POPRAWNOŚĆ ROZWIĄZANIA — czy przyjęta linia obrony i wnioski są spójne, "
    "zasadne i adekwatne do sprawy.\n\n"
    "Bądź rzetelny i konkretny: najpierw uzasadnij (mocne i słabe strony), potem "
    "wystaw oceny."
)

# Ocenę jakości robimy MOCNYM modelem. gpt-5.4-mini jako sędzia nie wyłapuje
# błędów formalnych (np. zła właściwość sądu odwoławczego) i nie różnicuje pism —
# sprawdzone empirycznie. Sędzia nie musi być tym samym modelem co autor.
QUALITY_JUDGE_MODEL = "gpt-5.4"


class QualityVerdict(BaseModel):
    """Ocena jakości/formy apelacji (reasoning najpierw, potem oceny 2–6)."""

    reasoning: str = Field(
        ..., description="Uzasadnienie: mocne i słabe strony pisma (forma + argumentacja)."
    )
    wymogi_formalne: int = Field(
        ..., ge=2, le=6, description="Zachowanie wymogów formalnych (2–6)"
    )
    zastosowanie_i_interpretacja: int = Field(
        ..., ge=2, le=6, description="Właściwość zastosowania i interpretacji przepisów (2–6)"
    )
    poprawnosc_rozwiazania: int = Field(
        ..., ge=2, le=6, description="Poprawność zaproponowanego rozwiązania (2–6)"
    )

    @property
    def srednia(self) -> float:
        """Średnia z trzech kryteriów (orientacyjna ocena łączna)."""
        return (
            self.wymogi_formalne
            + self.zastosowanie_i_interpretacja
            + self.poprawnosc_rozwiazania
        ) / 3


def evaluate_quality(
    appeal_text: str, model: str | None = QUALITY_JUDGE_MODEL
) -> QualityVerdict:
    """Oceń jakość/formę apelacji wg kryteriów egzaminu radcowskiego (skala 2–6).

    Domyślnie sędzią jest mocny model (``gpt-5.4``) — patrz `QUALITY_JUDGE_MODEL`.
    """
    messages = [
        {"role": "system", "content": QUALITY_SYSTEM_PROMPT},
        {"role": "user", "content": f"APELACJA DO OCENY:\n{appeal_text}"},
    ]
    return call_llm(messages, response_model=QualityVerdict, model=model)


if __name__ == "__main__":
    # Ocena najnowszej zapisanej apelacji danego podejścia.
    import sys

    from src.output import load_latest_appeal

    approach = sys.argv[1] if len(sys.argv) > 1 else "agent_linear"
    q = evaluate_quality(load_latest_appeal(approach))
    print(f"Ocena jakości apelacji ({approach}):\n")
    print(q.reasoning, "\n")
    print(f"  wymogi formalne:               {q.wymogi_formalne}/6")
    print(f"  zastosowanie/interpretacja:    {q.zastosowanie_i_interpretacja}/6")
    print(f"  poprawność rozwiązania:        {q.poprawnosc_rozwiazania}/6")
    print(f"  ── średnia:                    {q.srednia:.2f}/6")
