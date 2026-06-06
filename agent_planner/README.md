# Agent z planerem (nieliniowy)

> ⚠️ **To sam pomysł — bez kodu.** W repo są tylko ten README + diagram; planera
> świadomie **nie budujemy** (dlaczego — [niżej](#dlaczego-tylko-idea-bez-kodu)).
> Opisy poniżej są w trybie „jak by to działało".

> Krok dalej niż `agent_langgraph`: zamiast sztywnego, liniowego przepływu mamy
> **planer („mózg operacji")** w centrum grafu. To on dynamicznie decyduje, co robić
> dalej — graf **zawraca**, dopóki planer nie uzna, że ma dość.

📊 Diagram: [`graph.md`](graph.md).

## Jak to działa

Planer dostaje **ogólne zadanie** (jak na egzaminie: *oceń, czy apelacja jest zasadna,
i napisz ją, jeśli tak*), zna **opisy dostępnych dokumentów** oraz **dotychczasowe
wyniki analiz**. W każdej rundzie wybiera jedną akcję:

| akcja | co się dzieje |
|-------|---------------|
| `analyze` | tworzy nowe zadania → `make_task` realizuje je na wybranych dokumentach → wyniki **wracają do planera** |
| `ask_human` | **pauza** (`interrupt`): planer pokazuje podsumowanie i pyta radcę, czy pisać, czy analizować dalej |
| `write` | mamy dość — `generate_document` pisze apelację |
| `no_grounds` | z analizy wynika, że brak podstaw do apelacji — kończymy z uzasadnieniem |

Bezpiecznik: po `MAX_ROUNDS` rundach planer jest zmuszany do napisania pisma (żeby się
nie zapętlił).

## Czym różni się od pozostałych podejść

- `baseline` / `agent_linear` / `agent_langgraph` — przepływ **liniowy** (z góry ustalona
  kolejność kroków).
- **`agent_planner`** — przepływ **nieliniowy/cykliczny**: planer może zawracać do analizy
  i włącza **człowieka w pętlę** (human-in-the-loop). To pokazuje, co LangGraph naprawdę
  dokłada ponad zwykły pipeline: cykle, warunkowe sterowanie i pauzy na decyzję człowieka.

## Human-in-the-loop

Pauza działa przez `interrupt()` + **checkpointer** (`MemorySaver`) i `thread_id`.
Po zatrzymaniu podajesz decyzję w terminalu — wcielasz się w radcę:

```
=== PLANER PYTA ===
Przeanalizowałem ... Proponuję strategię ... Pisać apelację czy analizować dalej?

Twoja decyzja (radca): pisz
```

## Umiejętności (gdyby to zbudować)

Reużywałby `src/skills/*`: `file_description`, `make_task`, `generate_document` oraz
osobną decyzję planera (`analyze` / `ask_human` / `write` / `no_grounds`). Nie potrzebuje
`tasks` ani `strategy` — zadania tworzy planer, a „strategię" stanowi jego rozumowanie
przed napisaniem pisma.

## Dlaczego TYLKO idea (bez kodu)

Ten katalog to **świadomie sam pomysł** — README + diagram, **bez implementacji**.
Powody:

- **Warsztat ma być „mniej, a dokładniej"** — pełny agent nieliniowy z human-in-the-loop
  to kolejny duży kawałek do napisania, przetestowania i opłacenia (API), a narracyjnie
  domykają go już baseline → liniowy → LangGraph.
- **Koszt złożoności.** W LangGraph cykle i warunki to natywne krawędzie grafu, więc
  pętlę planera *dałoby się* zrobić bez własnej orkiestracji. Ale żeby zrobić to
  **dobrze (dynamicznie + równolegle)**, schodzi się na **logikę async**
  (`ainvoke`/async-węzły) zamiast wygodnej ścieżki sync z wątkami — czyli więcej mocy
  za cenę realnej złożoności.

Dlatego na prezentacji planer pojawia się jako **kierunek „co dalej?"** (slajd z pytaniem
do sali) — pokazujemy diagram i ideę, a nie uruchamiany kod.
