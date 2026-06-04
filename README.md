# Czy AI może napisać dobrą apelację?

> **Case study systemu, który zdałby egzamin radcowski.**
> Projekt warsztatowy przygotowany na konferencję **Women in Tech**.

## 📋 O projekcie

Czy AI potrafi napisać apelację na poziomie egzaminu radcowskiego? **Tak — ale tylko
przy odpowiedniej architekturze.**

Akta sprawy to setki stron żargonu, w których model musi znaleźć konkretne fakty.
Halucynacja w piśmie procesowym = przegrana sprawa, więc margines błędu jest zerowy.
Klasyczne RAG-i i chunkowanie tu nie wystarczą.

To 70-minutowe case study pokazuje, jak zbudować system, który radzi sobie z tym
zadaniem — oraz dlaczego bez radców prawnych weryfikujących każdy etap by się nie
udało. Sam pipeline to za mało.

### Co omawiamy

- **Wieloetapowe wnioskowanie** z walidacją **Pydantic** — jak utrzymać
  model na właściwym torze.
- Co robić, gdy model **gubi wątek w długim kontekście**, mimo że „powinien" go pamiętać.
- **Pełen przepływ na żywych aktach**: od plików wejściowych do gotowej apelacji.

### Czego nie będzie

Chunkowania, wektorowej bazy danych ani Graph RAG-a. Zamiast tego — podejście
wypracowane podczas pracy z prawdziwymi sprawami.

### Dla kogo

Dla osób, które znają podstawy LLM-ów i chcą zbudować coś, co działa **na produkcji**,
a nie tylko na demo.

## 📁 Dane

Akta pochodzą z oficjalnego zadania na **egzamin radcowski 2025**, opublikowanego przez
Ministerstwo Sprawiedliwości:

> https://www.gov.pl/web/sprawiedliwosc/zadania-wraz-z-opisem-istotnych-zagadnien-na-egzamin-radcowski-w-2025-r2

Pliki zostały **pobrane** i **podzielone na pojedyncze dokumenty** (po jednym
piśmie na plik), umieszczone w `data/input/`. 

Plik `data/eval.json` to **lista zagadnień, które apelacja powinna poruszyć**.

## 🚀 Uruchomienie

### 1. Środowisko wirtualne (`.venv`)

```bash
# Utworzenie środowiska
python3 -m venv .venv

# Aktywacja
source .venv/bin/activate        # macOS / Linux
# .venv\Scripts\activate         # Windows (PowerShell / cmd)
```

### 2. Instalacja zależności

```bash
pip install --upgrade pip
pip install pdfplumber pydantic
```

## 📂 Struktura projektu

```
WomenInTech/
├── data/
│   ├── input/         # akta sprawy (pojedyncze PDF-y)
│   └── eval.json      # lista zagadnień, które apelacja powinna poruszyć
├── src/               # wspólne moduły
│   ├── loader.py      # wczytywanie PDF do tekstu (Document, load_pdf, load_all)
│   ├── llm.py         # call_llm — jeden punkt wywołania LLM (instructor + OpenAI-compatible)
│   ├── tokens.py      # liczenie tokenów (count_tokens, count_messages_tokens)
│   ├── sources.py     # prepare_input_texts — selektywny kontekst (wybór dok. po nazwie)
│   ├── eval/          # ewaluacja: coverage.py (LLM-as-judge) + compare.py (tabela podejść)
│   └── skills/        # umiejętności agenta — jeden folder per umiejętność
│       ├── file_description/  # generate_file_description (main.py, prompts.py, schemas.py)
│       ├── tasks/             # generate_tasks
│       ├── make_task/         # make_task
│       ├── strategy/          # generate_strategy
│       └── document/          # generate_document
├── baseline/          # wersja 0 — naiwne podejście (wszystko → jeden prompt)
│   ├── prompts.py             # system prompt
│   ├── main.py                # generuje apelację → baseline/apelacja_baseline.txt
│   ├── apelacja_baseline.txt  # wygenerowana apelacja (artefakt)
│   └── README.md              # podsumowanie i wyniki baseline
├── linear_agent/      # agent liniowy — te same umiejętności spięte po kolei (bez LangGraph)
│   ├── pipeline.py    # run() spina umiejętności → linear_agent/apelacja.txt
│   └── README.md      # opis procesu krok po kroku
├── langgraph_agent/   # ten sam agent jako graf LangGraph (fan-out przez Send)
│   ├── state.py       # OverallState (z reducerami) + payloady Send
│   ├── graph.py       # węzły opakowujące umiejętności + routing + skompilowany graph
│   ├── main.py        # uruchomienie → langgraph_agent/apelacja.txt
│   └── README.md      # po co LangGraph, skoro wynik ten sam co liniowo
├── notebooks/         # walkthrough.ipynb — interaktywny przebieg umiejętności krok po kroku
├── presentation/      # materiały i plan prezentacji warsztatowej
├── langgraph.json     # konfiguracja LangGraph Studio (uv run langgraph dev)
├── .env.example       # szablon konfiguracji LLM (skopiuj do .env)
├── pyproject.toml     # zależności (uv)
├── uv.lock            # zablokowane wersje
└── requirements.txt   # fallback dla pip
```

### Moduły

- **`src/loader.py`** — `load_pdf(path)` wczytuje pojedynczy plik PDF i zwraca
  `Document` (Pydantic) z nazwą pliku i wyekstrahowanym tekstem; `load_all(dir)`
  wczytuje wszystkie PDF-y z katalogu.
- **`src/llm.py`** — `call_llm(messages, response_model, ...)` zwraca odpowiedź
  zwalidowaną względem modelu Pydantic. Klient jest zgodny z interfejsem OpenAI,
  więc przez zmianę `base_url`/`api_key` w `.env` można podpiąć dowolny backend
  (OpenAI, lokalny model przez Ollama, proxy itp.).
- **`src/tokens.py`** — pomocnicze liczenie tokenów (tiktoken) dla tekstu i listy
  wiadomości.
- **`src/eval/`** — ewaluacja: `coverage.py` (`evaluate(appeal_text)` ocenia apelację
  względem zagadnień z `data/eval.json`, LLM-as-judge) oraz `compare.py` — runner,
  który ocenia wszystkie podejścia i drukuje tabelę porównawczą
  (`uv run python -m src.eval.compare`).
- **`src/sources.py`** — `prepare_input_texts(documents, names)` zwraca tekst tylko
  wybranych dokumentów (selektywny kontekst); współdzielone przez agenta liniowego
  i wersję LangGraph.
- **`src/skills/`** — umiejętności agenta, każda w osobnym folderze (`main.py` =
  czysta funkcja, `prompts.py`, `schemas.py`): `file_description`, `tasks`,
  `make_task`, `strategy`, `document`.
- **`baseline/`** — naiwna „wersja 0": całe akta + jeden prompt „napisz apelację".
  Punkt wyjścia warsztatu (szczegóły w `baseline/README.md`).
- **`linear_agent/`** — agent liniowy: te same umiejętności (`src/skills/*`) spięte
  po kolei, bez LangGraph. Pętle `for` to miejsca, które później zastąpi fan-out
  grafu.
- **`langgraph_agent/`** — ten sam agent jako graf LangGraph: węzły to cienkie
  opakowania umiejętności, a pętle z agenta liniowego zastępuje fan-out przez `Send`
  (jeden plik / jedno zadanie na gałąź), z reducerami zbierającymi wyniki. Można go
  uruchomić w **LangGraph Studio** (`uv run langgraph dev`) — szczegóły i odpowiedź
  „po co LangGraph" w `langgraph_agent/README.md`.
- **`notebooks/walkthrough.ipynb`** — interaktywny przebieg: uruchamia umiejętności
  po kolei i pokazuje wynik każdego etapu (`uv run jupyter lab`).
- **`presentation/`** — plan i materiały do warsztatu (`presentation/README.md`).

## 🛠️ Wymagania

- Python 3.x
- Pydantic
- dostęp do modelu LLM przez API / Ollama
