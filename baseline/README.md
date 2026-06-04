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
| `llm_call.py` | `load_all`, `build_context`, `generate_appeal`; uruchomiony generuje apelację i zapisuje do `.txt` |
| `eval.py` | czyta wygenerowaną apelację i odpala `evaluate()` z `src/eval.py` |

## Uruchomienie

```bash
# 1) wygenerowanie apelacji → data/output/apelacja_baseline.txt
uv run python -m baseline.llm_call

# 2) ewaluacja apelacji względem data/eval.json
uv run python -m baseline.eval
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

_TODO: uzupełnić po ewaluacji baseline — które zagadnienia z `eval.json` model
pominął, gdzie halucynował, jak wypadł na tle podejścia wieloetapowego._
