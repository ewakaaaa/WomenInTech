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
# 1) wygenerowanie apelacji → baseline/apelacja_baseline.txt
uv run python -m baseline.main

# 2) ewaluacja — wspólny runner porównuje wszystkie podejścia
uv run python -m src.eval.compare
```

## Wyniki (zużycie kontekstu)

| metryka | wartość |
|---------|---------|
| dokumenty | 16 |
| znaki kontekstu | 53 100 |
| tokeny wejścia (prompt) | ~19 761 |

Całe akta mieszczą się w jednym oknie kontekstu (~20 tys. tokenów), więc naiwne
podejście **technicznie zadziała**. Pytanie warsztatowe brzmi jednak nie „czy
zadziała", tylko **„czy zrobi to dobrze"** — i to zweryfikujemy ewaluacją na
podstawie `data/eval.json`.

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
