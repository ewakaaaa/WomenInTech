# Prezentacja — plan warsztatu

> **Czy AI może napisać dobrą apelację? Case study systemu, który zdałby egzamin radcowski.**
> Format: 70 min, case study + live demo. Konferencja Women in Tech.

Tu trzymamy materiały do prezentacji (slajdy, notatki) i poniższy plan.

## Teza

AI potrafi napisać apelację na poziomie egzaminu radcowskiego — **ale tylko przy
odpowiedniej architekturze**. Sam prompt „napisz apelację" nie wystarczy; potrzebny
jest wieloetapowy agent **i** człowiek weryfikujący każdy etap.

## Plan (≈70 min)

| # | Blok | Czas | Co pokazujemy |
|---|------|------|---------------|
| 1 | **Problem** | 8 min | Czym jest apelacja i akta sprawy (setki stron żargonu). Dlaczego margines błędu = 0 (halucynacja = przegrana). Sprawa Daniela Dzika jako przykład. |
| 2 | **Baseline: wszystko → jeden prompt** | 10 min | `baseline/` — demo generacji + `src.eval.compare`. Pokazać, że „działa", ale: zapchany kontekst, „lost in the middle", wszystko naraz, błąd w połowie, brak audytu, halucynacje. |
| 3 | **Pomysł na agenta** | 7 min | Dziel i rządź + **selektywny kontekst**. Klocek = jedna umiejętność. Dlaczego NIE chunkowanie / wektorowa baza / Graph RAG. |
| 4 | **Umiejętności na żywo (notebook)** | 18 min | `notebooks/walkthrough.ipynb` — przejść etap po etapie: opis plików → plan zadań → wykonanie na wybranych dokumentach → strategia → dokument. Pokazać outputy pośrednie. |
| 5 | **Spięcie liniowe** | 5 min | `linear_agent/pipeline.py` — te same funkcje, czysty Python. Tabela „klocek → rozwiązany problem". |
| 6 | **LangGraph + Studio** | 12 min | `langgraph_agent/` — ten sam graf, fan-out `Send`, równoległość. Live: `uv run langgraph dev`. Po co LangGraph (i jego koszt: dług zależności — POC vs produkcja). |
| 7 | **Rola człowieka** | 4 min | Dlaczego radca prawny musi weryfikować każdy etap — pipeline to za mało. |
| 8 | **Wyniki i wnioski** | 6 min | Tabela porównawcza (baseline vs agent) z `src.eval.compare`. Co działa, czego nie robić, take-aways. |

## Demo — checklista

- [ ] `.env` z działającym kluczem LLM (zapasowy backend: Ollama / proxy)
- [ ] Wygenerowane apelacje w `baseline/`, `linear_agent/`, `langgraph_agent/` (na wypadek braku sieci)
- [ ] Wyniki `uv run python -m src.eval.compare` zrzucone do slajdu (plan B bez live)
- [ ] `uv run jupyter lab` — sprawdzony `notebooks/walkthrough.ipynb`
- [ ] `uv run langgraph dev` — sprawdzone Studio
- [ ] Diagram grafu (mermaid z `langgraph_agent`)

## Kluczowe przekazy (take-aways)

1. Architektura > pojedynczy prompt — margines błędu zero wymusza etapowość.
2. **Selektywny kontekst** zamiast wrzucania wszystkiego (bez chunkowania/wektorów).
3. Logika umiejętności **niezależna od frameworka** — to samo działa liniowo i w grafie.
4. LangGraph daje równoległość/obserwowalność/Studio, ale to dług zależności.
5. **Człowiek w pętli** jest częścią systemu, nie dodatkiem.

## Do uzupełnienia

- [ ] Realne liczby do tabeli wyników (po uruchomieniu na żywo)
- [ ] Slajdy
