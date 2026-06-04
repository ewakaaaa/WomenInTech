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

- **Wieloetapowe wnioskowanie z LangGraph** z walidacją **Pydantic** — jak utrzymać
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

Pliki zostały **pobrane ręcznie** i **podzielone na pojedyncze dokumenty** (po jednym
piśmie na plik), umieszczone w `data/input/`.

Plik `data/eval.json` to **lista zagadnień, które apelacja powinna poruszyć**.

## 🚀 Uruchomienie

Projekt korzysta z [**uv**](https://docs.astral.sh/uv/). Instalacja uv:

```bash
brew install uv                              # macOS
# curl -LsSf https://astral.sh/uv/install.sh | sh   # macOS / Linux
```

### 1. Instalacja zależności

```bash
uv sync        # tworzy .venv i instaluje zależności z pyproject.toml / uv.lock
```

### 2. Test wczytywania akt

```bash
uv run python -m src.loader
```

Powinno wypisać listę wczytanych dokumentów z `data/input/` wraz z liczbą stron
i znaków.

> Polecenia uruchamiasz przez `uv run ...` (uv samo aktywuje środowisko).
> Bez uv: `pip install -r requirements.txt` również zadziała.

## 📂 Struktura projektu (propozycja)

```
WomenInTech/
├── data/                  # akta sprawy (wejście) — ignorowane w gitignore
│   └── przyklad/          # zanonimizowany przykład do dema
├── src/
│   ├── graph/             # definicja grafu LangGraph (węzły, krawędzie, stan)
│   ├── models/            # modele Pydantic (stan, fakty, sekcje apelacji)
│   ├── nodes/             # poszczególne kroki wnioskowania
│   ├── prompts/           # szablony promptów
│   └── pipeline.py        # punkt wejścia uruchamiający przepływ
├── tests/
├── requirements.txt
├── .env.example
└── README.md
```

## 🛠️ Wymagania

- Python 3.x
- LangGraph
- Pydantic
- (opcjonalnie) dostęp do modelu LLM przez API

## ⚠️ Uwaga

Akta sądowe zawierają dane wrażliwe. Do prezentacji używaj wyłącznie
**zanonimizowanych** przykładów. Katalog `data/` jest celowo ignorowany przez git.

## 📝 Licencja

_(do uzupełnienia)_
