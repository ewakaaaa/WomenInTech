# %% [markdown]
# # Setup — uruchom agenta u siebie
#
# Są **dwa sposoby** na podłączenie modelu (wybierz JEDEN):
#
# - **A. Własny klucz API** do LLM-a — OpenAI albo dowolny dostawca zgodny z interfejsem OpenAI.
# - **B. Lokalnie przez Ollamę** — bez klucza, model chodzi na Twoim komputerze.
#
# Ustaw zmienne w komórce poniżej, a potem uruchom test. Szczegóły (w tym instalacja
# Ollamy) są w głównym `README.md`.
#
# > Wersja `.py` notebooka `setup.ipynb` — komórki oddzielone `# %%`.
# > W Zedzie: kursor w komórce → **Ctrl+Shift+Enter** (`repl: run`).

# %% [markdown]
# ## 1. Wybierz sposób i ustaw zmienne
#
# Ustaw zmienne **zanim** zaimportujesz `call_llm` (uruchamiaj komórki po kolei).
# Jeśli później zmieniasz sposób — **zrestartuj kernel** i zacznij od tej komórki.

# %%
import os

# ── A. Własny klucz API (OpenAI lub zgodny z OpenAI) ──
os.environ["LLM_BASE_URL"] = "https://api.openai.com/v1"
os.environ["LLM_API_KEY"] = "sk-...wpisz-swój-klucz..."
os.environ["LLM_MODEL"] = "gpt-4o-mini"

# ── B. Lokalnie przez Ollamę (odkomentuj te 3 linie, zakomentuj sekcję A) ──
# os.environ["LLM_BASE_URL"] = "http://localhost:11434/v1"
# os.environ["LLM_API_KEY"]  = "ollama"      # dowolny placeholder — Ollama nie wymaga klucza
# os.environ["LLM_MODEL"]    = "mistral"     # najpierw: ollama pull mistral

print("base_url:", os.environ["LLM_BASE_URL"])
print("model:   ", os.environ["LLM_MODEL"])

# %% [markdown]
# ## 2. Test — czy działa?
#
# Proste wywołanie ze **structured output** (Pydantic). Jeśli wróci obiekt z polami
# `country` i `capital` — konfiguracja działa.

# %%
from pydantic import BaseModel
from src.llm import call_llm


class Capital(BaseModel):
    country: str
    capital: str


result = call_llm(
    messages=[{"role": "user", "content": "Jaka jest stolica Polski?"}],
    response_model=Capital,
)
print(result)

# %% [markdown]
# ## 3. Gotowe 🎉
#
# Jeśli powyżej zobaczyłeś coś w stylu `country='Polska' capital='Warszawa'` — działa.
# Możesz teraz odpalić:
#
# - `baseline_walkthrough.ipynb` — umiejętności krok po kroku,
# - `planner_walkthrough.ipynb` — agent nieliniowy z human-in-the-loop.
#
# **Nie działa?**
# - Klucz API: sprawdź `LLM_API_KEY`, `LLM_BASE_URL` i czy masz środki na koncie.
# - Ollama: czy działa `ollama serve` i czy pobrałeś model (`ollama pull mistral`)?
#   Zob. sekcję *Konfiguracja LLM* w głównym `README.md`.
