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

## 📂 Struktura projektu (propozycja)

#TODO

## 🛠️ Wymagania

- Python 3.x
- Pydantic
- dostęp do modelu LLM przez API / Ollama
