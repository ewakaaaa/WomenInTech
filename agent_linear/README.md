# Agent liniowy

## Jak wygląda proces

Cel domyślny: `"Wygeneruj apelację z perspektywy obrony"`.

```
load_all (16 PDF-ów z data/input)
        │
        ▼
1. generate_file_description   ── dla KAŻDEGO pliku → krótki, ukierunkowany na cel opis
        │                          (pętla po dokumentach)
        ▼
2. generate_tasks              ── plan analizy: lista kroków (maks. 10), każdy ze
        │                          wskazaniem, KTÓRE dokumenty są potrzebne (task.input)
        ▼
3. make_task                   ── dla KAŻDEGO kroku:
        │                          • prepare_input_texts → bierze TYLKO wskazane dokumenty
        │                          • LLM wykonuje krok na tym wycinku akt
        │                          (pętla po zadaniach)
        ▼
4. generate_strategy           ── z wyników analiz → definicja sukcesu + najlepsza strategia
        │
        ▼
5. generate_document           ── pełna apelacja na podstawie strategii i analiz
        │
        ▼
   agent_linear/output/apelacja_<znacznik>.txt
```

## Sedno — selektywny kontekst

To jest różnica wobec `baseline/` (gdzie całe akta lecą w jeden prompt). Tutaj
`generate_tasks` decyduje, **które** dokumenty są potrzebne do danego kroku, a
`make_task` (przez `prepare_input_texts` z `src/sources.py`) widzi **tylko ten
wycinek**. Model nigdy nie ogląda wszystkiego naraz — pracuje na małych, trafnych
fragmentach.

## Co robi każda umiejętność

Opis wszystkich umiejętności (co robią i jaki problem baseline rozwiązują) jest
wspólny dla wszystkich podejść i mieszka w [`src/skills/README.md`](../src/skills/README.md).
Tutaj liczy się tylko, że agent liniowy odpala je **po kolei**.

## Uruchomienie

```bash
# generacja apelacji + ocena (pokrycie + jakość); model z .env (gpt-5.4)
uv run python -m agent_linear.main
```

Zapisuje apelację i log przebiegu do `agent_linear/output/`. W logu znajdziesz
**koszt metody** (sama generacja, wszystkie wywołania pipeline'u) i — osobno —
koszt ewaluacji.

Krok po kroku (tanie demo na `gpt-5.4-mini`): `notebooks/linear_walkthrough.ipynb`
(sam przepływ, bez oceny). Ewaluację pokazujemy na przykładzie baseline w
`notebooks/eval_walkthrough.ipynb` — tę samą `evaluate(...)` można puścić na apelacji liniowej.

## Wyniki ewaluacji (`gpt-5.4`)

Przebieg `python -m agent_linear.main` (model z `.env`). **Koszt metody** to sama
generacja (cały pipeline) — koszt ewaluacji liczony osobno.

| miara | wynik |
|-------|-------|
| **liczba kroków planu** | **8** (limit: maks. 10) |
| **koszt metody** (cały pipeline) | ~**$0,743** (11 wywołań, 91 265 wej + 34 331 wyj tok) |
| **czas metody** | **433,5 s** (~7 min, 11 wywołań, ≈39,4 s/wyw.) |
| **pokrycie** (zagadnienia z `data/eval.json`) | **8/12 = 67%** |
| **jakość** (średnia 2–6, sędzia `gpt-5.4`) | **4,33/6** (formalne 5 · zastosowanie 4 · poprawność 4) |

Pokrycie wyraźnie wyższe niż baseline (**67% vs 33%**) — selektywny kontekst i analiza
krok po kroku wyłapują więcej wymaganych zagadnień. Pełny log:
`agent_linear/output/run_<znacznik>.log`.
