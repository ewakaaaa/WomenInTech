"""Schemas for the strategy skill."""

from __future__ import annotations

from pydantic import BaseModel, Field


class Strategy(BaseModel):
    """Skonsolidowane i spriorytetyzowane wnioski z analizy (reasoning najpierw)."""

    reasoning: str = Field(
        ...,
        description=(
            "Podsumowanie i konsolidacja analiz: co istotne, co się powtarza "
            "(bez dublowania), oraz uzasadnienie priorytetyzacji — wg WAGI dla "
            "sprawy, a NIE częstości występowania (kilkukrotne pojawienie się "
            "wątku nie znaczy, że jest najważniejszy)."
        ),
    )
    prioritized_grounds: list[str] = Field(
        ...,
        description=(
            "Uporządkowana wg istotności lista zarzutów/wątków do ujęcia w "
            "dokumencie — od najważniejszego. Bez powtórzeń."
        ),
    )
