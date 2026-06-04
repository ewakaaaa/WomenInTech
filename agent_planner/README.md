# Agent z planerem (nieliniowy)

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

## Umiejętności

Reużywa `src/skills/*`: `file_description`, `make_task`, `generate_document` oraz nową
`planner` (decyzja: `analyze` / `ask_human` / `write` / `no_grounds`). Nie korzysta z
`tasks` ani `strategy` — zadania tworzy planer, a „strategię" stanowi jego rozumowanie
przed napisaniem pisma.

## Uruchomienie

```bash
uv run python -m agent_planner.main   # → agent_planner/apelacja.txt
```

Wymaga klucza LLM w `.env`. Przy `ask_human` graf zatrzyma się i poprosi o decyzję.

Interaktywnie (z diagramem i podglądem przebiegu): notebook
[`notebooks/planner_walkthrough.ipynb`](../notebooks/planner_walkthrough.ipynb)
(`uv run jupyter lab`).
