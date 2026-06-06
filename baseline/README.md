# Baseline — (naiwne podejście)

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
| `main.py` | `build_context`, `generate_appeal`; uruchomiony: generacja → zapis → ocena (pokrycie + jakość) + log |

Artefakty przebiegu lądują w `baseline/output/` (apelacja + log; poza gitem).

## Uruchomienie

```bash
# generacja apelacji + ocena (pokrycie + jakość); model z .env (gpt-5.4)
uv run python -m baseline.main
```

Krok po kroku w notebookach (tanie demo na `gpt-5.4-mini`):
`notebooks/baseline_walkthrough.ipynb` (generacja) +
`notebooks/eval_walkthrough.ipynb` (pokrycie + jakość).

> ⚠️ Baseline wrzuca **całe akta w jeden prompt** (~19–20 tys. tokenów), więc
> wymaga modelu z **dużym oknem kontekstu** — używamy `gpt-5.4`.

## Wyniki (zużycie kontekstu)

| metryka | wartość |
|---------|---------|
| dokumenty | 16 |
| znaki kontekstu | 53 100 |
| tokeny wejścia (prompt) | ~19 761 |

Całe akta to ~20 tys. tokenów — mieszczą się w jednym oknie kontekstu `gpt-5.4`,
więc naiwne podejście **technicznie zadziała**. Pytanie brzmi jednak
nie „czy zadziała", tylko **„czy zrobi to dobrze"** — i to zweryfikujemy ewaluacją
na podstawie `data/eval.json`.

## Wyniki ewaluacji (`gpt-5.4`)

Przebieg `python -m baseline.main` (model z `.env`).

| miara | wynik |
|-------|-------|
| **koszt** | ~**$0,105** (1 wywołanie, 19 473 wej + 3 757 wyj tok) |
| **czas metody** | **48,3 s** (1 wywołanie) |
| **pokrycie** (zagadnienia z `data/eval.json`) | **4–5/12 = 33–42%** (3 przebiegi, śr. ~36%) |
| **jakość** (średnia 2–6, sędzia `gpt-5.4`) | **4,33/6** (formalne 5 · zastosowanie 4 · poprawność 4) |

> Pokrycie liczone na 3 przebiegach (losowość modelu → różne apelacje); jakość i koszt
> stabilne. Agent liniowy w tym samym teście dał 50–67% — **zawsze wyżej** niż baseline.
> Pełne logi: `baseline/output/run_<znacznik>.log`, `data/output/wariancja_2026-06-06.log`.

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
