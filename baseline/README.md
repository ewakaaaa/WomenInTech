# Baseline — wersja 0 (naiwne podejście)

> Po co budować agenta, skoro można wrzucić wszystko do LLM-a z jednym promptem
> „napisz apelację"? Ta sekcja to punkt wyjścia warsztatu — pokazuje najprostsze
> możliwe rozwiązanie, żeby potem było jasne, **czego mu brakuje**.

## Pomysł

1. Wczytaj **wszystkie** akta z `data/input/`.
2. Sklej je w jeden kontekst.
3. Wyślij do modelu jeden prompt: *„jesteś radcą prawnym, napisz apelację na
   podstawie akt"*.

## Pliki

| Plik | Rola |
|------|------|
| `prompts.py` | system prompt |
| `main.py` | `build_context`, `generate_appeal`; uruchomiony generuje apelację i zapisuje do `.txt` |
| `apelacja_baseline.txt` | wygenerowana apelacja (artefakt) |

## Uruchomienie

```bash
# wygenerowanie apelacji → baseline/apelacja_baseline.txt
uv run python -m baseline.main
```

Ewaluacja (pokrycie + halucynacje) krok po kroku — w notebooku
`notebooks/baseline_and_eval.ipynb`.

> ⚠️ **Lokalnie na Ollamie tego podejścia nie uruchomisz.** Prompt baseline to
> ~19–20 tys. tokenów, a Ollama domyślnie obcina kontekst do **4096 tokenów** —
> model dostaje ~⅕ akt, gubi instrukcję o formacie odpowiedzi i zwraca błędny
> JSON (`ValidationError: tekst Field required`). Potrzebny jest model z **dużym
> oknem kontekstu**: użyj dostawcy API (np. OpenAI), albo — kosztem RAM —
> podnieś kontekst Ollamy (`OLLAMA_CONTEXT_LENGTH=32768`, restart serwera).
> Agent liniowy/planer dzielą akta na małe kawałki, więc te działają na Ollamie
> bez problemu — baseline jest tu wyjątkiem właśnie przez jeden wielki prompt.

## Wyniki (zużycie kontekstu)

| metryka | wartość |
|---------|---------|
| dokumenty | 16 |
| znaki kontekstu | 53 100 |
| tokeny wejścia (prompt) | ~19 761 |

Całe akta to ~20 tys. tokenów — mieszczą się w jednym oknie kontekstu, **o ile
model ma dość duże okno** (dostawcy API to mają; Ollama domyślnie nie — patrz
ostrzeżenie wyżej). Przy modelu z dużym kontekstem naiwne podejście **technicznie
zadziała**, więc pytanie warsztatowe brzmi nie „czy zadziała", tylko **„czy zrobi
to dobrze"** — i to zweryfikujemy ewaluacją na podstawie `data/eval.json`.

## Wyniki ewaluacji (przykładowy przebieg, `gpt-5.4-mini`)

Z `notebooks/baseline_and_eval.ipynb` (apelacja ~7,9 tys. znaków z jednego promptu):

| miara | wynik |
|-------|-------|
| **pokrycie** (średnia z 5 przebiegów) | **47%** (42–50%) |
| **halucynacje** (fakty bez oparcia / sprzeczne z aktami) | ~**17%** (5 z 30 twierdzeń) |

> Liczby orientacyjne — zależą od modelu i losowości. Odpal notebook, by odtworzyć.

## Ograniczenia (czyli po co agent)

Naiwne podejście „wszystko → jeden prompt" rodzi konkretne problemy:

- **Zapchany kontekst.** W tej sprawie akta to ~20 tys. tokenów i mieszczą się w
  oknie — ale prawdziwe sprawy mają setki stron. Wtedy albo przekraczamy limit, albo
  model **gubi się w szumie** (zjawisko „lost in the middle" — informacje ze środka
  długiego kontekstu wypadają z uwagi).
- **Wszystko naraz.** Model w jednym kroku ma zrozumieć sprawę, odnaleźć fakty,
  ustalić zarzuty, dobrać podstawy prawne i napisać pismo. Im więcej zadań na raz, tym
  łatwiej któreś **pominąć** albo wykonać pobieżnie.
- **Błąd „w połowie" psuje całość.** To jeden długi przebieg — jeśli model
  zhalucynuje albo pomyli się w środku, **nie ma jak tego wyłapać ani powtórzyć
  fragmentu**; błąd propaguje się do gotowej apelacji.
- **Brak śladu / audytu.** Nie wiadomo, na podstawie którego dokumentu model coś
  stwierdził — a tu radca musi móc **zweryfikować każdy etap**.
- **Halucynacje.** Bez ukierunkowania model chętnie „dopowiada" fakty, których w
  aktach nie ma. W piśmie procesowym to dyskwalifikuje wynik.
- **Trudno iterować.** To monolit — nie da się poprawić ani przetestować pojedynczego
  etapu w oderwaniu od reszty.

Jak te problemy rozwiązuje podejście wieloetapowe (i co robi każdy klocek) —
opisane w [`agent_linear/README.md`](../agent_linear/README.md).
