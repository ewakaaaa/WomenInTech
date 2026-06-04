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
   linear_agent/apelacja.txt
```

## Sedno — selektywny kontekst

To jest różnica wobec `baseline/` (gdzie całe akta lecą w jeden prompt). Tutaj
`generate_tasks` decyduje, **które** dokumenty są potrzebne do danego kroku, a
`make_task` (przez `prepare_input_texts` z `src/sources.py`) widzi **tylko ten
wycinek**. Model nigdy nie ogląda wszystkiego naraz — pracuje na małych, trafnych
fragmentach.

## Co robi każdy klocek (i jaki problem baseline rozwiązuje)

Baseline robił wszystko jednym promptem. Agent rozbija to na klocki — każdy ma jedno
zadanie i rozwiązuje konkretny problem naiwnego podejścia
(lista problemów: [`baseline/README.md`](../baseline/README.md)).

| Klocek | Co robi | Jaki problem baseline rozwiązuje |
|--------|---------|----------------------------------|
| **generate_file_description** | Zamienia surowe akta w zwięzłe, ukierunkowane na cel opisy — „mapę" sprawy. | Mniej szumu: planer nie czyta 16 pełnych dokumentów, tylko wie, gdzie czego szukać. |
| **generate_tasks** | Rozbija wielki cel na małe kroki; każdy wskazuje, **które** dokumenty są mu potrzebne. | „Wszystko naraz" → dziel i rządź. Plan jest też **śladem**, co i czemu robimy. |
| **make_task** | Wykonuje **jeden** krok na **tylko** wskazanych dokumentach. | Zapchany kontekst i „lost in the middle"; **izolacja błędu** (zła analiza w jednym kroku nie psuje reszty, da się go powtórzyć); **audytowalność** (wiadomo, z czego wynika ustalenie). |
| **generate_strategy** | Z zebranych analiz wybiera linię obrony / najlepsze podejście. | Świadomy, spójny kierunek zamiast przypadkowego — zanim zacznie się pisać. |
| **generate_document** | Pisze pismo na **gotowej, ustalonej analizie i strategii**, a nie na surowych aktach. | Mniej halucynacji i pominięć — model opiera się na zweryfikowanych faktach, nie na całym worku akt. |

Krótko: **mały, skupiony kontekst na każdym etapie + jawny plan + możliwość weryfikacji
i powtórzenia kroku** — to jest to, czego baseline nie daje.

## Skąd biorą się umiejętności

Każdy krok to czysta funkcja z `src/skills/<umiejętność>/main.py` (wejście → wyjście
Pydantic). `pipeline.py` tylko je wywołuje i przekazuje wyniki dalej. Pętle `for`
(opis plików, wykonywanie zadań) to dokładnie te miejsca, które w `langgraph_agent/`
zastępuje równoległy fan-out przez `Send`.

## Uruchomienie

```bash
# wygenerowanie apelacji → linear_agent/apelacja.txt
uv run python -m linear_agent.pipeline

# ewaluacja (wspólny runner porównuje wszystkie podejścia)
uv run python -m src.eval.compare
```
