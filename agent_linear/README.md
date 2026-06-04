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
2. generate_tasks              ── plan analizy: lista kroków, każdy ze wskazaniem,
        │                          KTÓRE dokumenty są do niego potrzebne (task.input)
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
   agent_linear/apelacja.txt
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

## Skąd biorą się umiejętności

Każdy krok to czysta funkcja z `src/skills/<umiejętność>/main.py` (wejście → wyjście
Pydantic). `pipeline.py` tylko je wywołuje i przekazuje wyniki dalej. Pętle `for`
(opis plików, wykonywanie zadań) to dokładnie te miejsca, które w `agent_langgraph/`
zastępuje równoległy fan-out przez `Send`.

## Uruchomienie

```bash
# wygenerowanie apelacji → agent_linear/apelacja.txt
uv run python -m agent_linear.pipeline

# ewaluacja (wspólny runner porównuje wszystkie podejścia)
uv run python -m src.eval.compare
```
