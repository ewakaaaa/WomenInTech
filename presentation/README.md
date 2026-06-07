# Prezentacja — plan warsztatu

> **Czy AI może napisać dobrą apelację? Case study systemu, który zdałby egzamin radcowski.**
> Format: 70 min, case study + live demo. Women in Tech Summit.

> 📌 **Źródło prawdy = `COI_prezentacja_standard.pptx.pdf`** (plik poza gitem). Ten plan
> **podąża za PDF-em**: numeracja = strony PDF, zakresy (np. 2–7) to buildy jednego slajdu.
> Czasy: do rozplanowania (slot 70 min). 🖥️ = demo na żywo.

## Teza

AI potrafi napisać apelację na poziomie egzaminu radcowskiego — **ale tylko przy
odpowiedniej architekturze**. Sam prompt „napisz apelację" nie wystarczy; potrzebny
jest wieloetapowy agent **i** człowiek weryfikujący każdy etap.

## Plan slajd po slajdzie (wg PDF)

### Wstęp
- **1 · Tytuł** — Czy AI może napisać dobrą apelację?
- **2–7 · Agenda** (build, 6 punktów): cel/dane/sprawa · baseline+ewaluacja · dlaczego to za mało? · architektura „agenta" · wyniki · podsumowanie.
- **8 · Kim jestem** — matematyczka → data scientist w COI (zespół mObywatela), działka prawna. „nigdy nie mów nigdy".
- **9 · Link do githuba** — QR + `github.com/ewakaaaa/WomenInTech`. „Pobierzcie, patrzcie ze mną".
- **10 · Cel i motywacja** — chcemy **generator pism prawniczych**; zerowy margines błędu.
- **11 · Dane** — źródło: zadanie na **egzamin radcowski 2025** (gov.pl).

### Dane i sprawa
- **12–14 · Dlaczego dane są fantastyczne?** (build): anonimowe · czytelne PDF-y · **klucz odpowiedzi** → możemy *mierzyć*.
- **15 · Dokumenty** — chronologia akt (02–17): interwencja, dochodzenie, świadkowie, zarzuty, oskarżenie, rozprawy, opinia biegłego, wyrok.
- **16–18 · O czym jest sprawa Daniela Dzika?** (build): sąd + sygn. **II K 25/25** · zdarzenie (31.12.2024, Jeep w alejce cmentarnej, alkomat, ławka) · zarzuty (art. 178a § 1 i art. 288 § 1 k.k.).

### Baseline + ewaluacja
- **19–21 · Baseline — wrzućmy wszystko do LLM-a** (build): wczytanie/format PDF · 1 `call_llm` „napisz apelację" · output (gotowa apelacja).
- **22 · 🖥️ Demo techniczne — baseline** (`notebooks/baseline_walkthrough.ipynb`): całe akta → jeden prompt.
- **23 · Ewaluacja** — *jak mierzymy (umowa na starcie, raz dla wszystkich):* **pokrycie** (LLM-as-judge per zagadnienie z `data/eval.json`, `X/12`) + **jakość/styl** (3 kryteria, 2–6).
- **24 · 🖥️ Demo techniczne — ewaluacja** (`notebooks/eval_walkthrough.ipynb`).
- **25 · Wyniki (baseline)** — koszt $0,105 · czas 48,3 s · **pokrycie 4–5/12 (33–42%)** · jakość 4,33/6.

### Dlaczego za mało → jak człowiek
- **26 · „Dlaczego?"** — dramatyczna pauza (miejsce na mem „miało wyjść inaczej"). Pointa: „działa, ale czy *dobrze*?".
- **27 · Eksperci domenowi** — jak **człowiek/radca** podszedłby do zadania (zawias do architektury).
- **28–33 · Jak zrobiłby to człowiek** (build, 6 kroków): cel · pobieżne zapoznanie z dokumentami · plan/lista TODO · analiza (realizacja TODO) · podsumowanie/strategia · napisanie apelacji.

### Architektura agenta
- **34 · Architektura** — diagram pipeline'u: `file_description → tasks → make_task → strategy → document`. Sedno: **selektywny kontekst** (każdy krok widzi tylko trafny wycinek akt).
- **35 · Top 3 umiejętności** — 🫁 oddech + **hook z LinkedIna** (pytanie o top-3 DS). Senior nie tylko robi, ale **planuje całe rozwiązanie** — to przed chwilą zrobiliśmy.
- **36 · 🖥️ Demo techniczne — agent liniowy** (`notebooks/linear_walkthrough.ipynb`): umiejętności po kolei; jak agent rozwiązuje problemy baseline (podsumowania, selektywny kontekst, małe kroki, cel niesiony przez pipeline).
- **37 · Structured Output** — **klej** pipeline'u: każdy krok zwraca **typowany obiekt** (Pydantic) → wiem, co podać dalej.
- **38 · Wyniki (agent liniowy)** — koszt ~$0,743 · czas ~7 min · **pokrycie 6–8/12 (50–67%)** · jakość 4,33/6. Agent > baseline; zakresy **się nie nakładają** (przewaga odporna na losowość).

### Co dalej + puenta
- **39 · „Co dalej?"** — pivot do rozszerzeń.
- **40 · LangGraph** — co daje: **zrównoleglenie (≈2,6×, ten sam koszt)**, dostęp do źródeł zewnętrznych, koordynator (powrót do planowania), human-in-the-loop. *(⚠️ rozważ dodanie przestrogi: ciężka **zależność/dług** — buduje puentę 41.)*
- **41 · Structured Output + plan ≫ LangGraph** — puenta techniczna: klej (Pydantic) ważniejszy niż framework.
- **42–44 · Podsumowanie** (build, 3 take-awaye): zaplanowanie rozwiązania · rozmowa z biznesem i ekspertami · **ewaluacja ustalona na starcie**.
- **45 · Q&A** — „Dziękuję za uwagę".

## Demo — checklista

- [x] `.env` z działającym kluczem LLM (`gpt-5.4`) — sprawdzone
- [x] Wygenerowane apelacje w `*/output/` (plan B offline, bez sieci)
- [x] Liczby ewaluacji: baseline **33–42%**, liner **50–67%**, jakość **4,33**
- [x] Liczby do slajdu **40** (langgraph vs liner): 169,8 s, ≈2,6×, ~$0,74
- [x] Notebooki przeklikane: `baseline_walkthrough` (22), `eval_walkthrough` (24), `linear_walkthrough` (36)
- [x] Hook z LinkedIna na slajdzie **35**
- [x] Sygnatura **„II K 25/25"** spójnie na slajdach 16/17/18
- [ ] *(opcjonalnie)* literówki slajd 23 („LLM calle", „-czy"); przestroga „dług" na slajdzie 40

## Kluczowe przekazy (take-aways)

### Callback do anegdoty — 3 top umiejętności DS (przeplatają się przez cały warsztat)

1. **Zaplanowanie całego rozwiązania** (mid → senior). To dziś przećwiczyliśmy: rozbić
   problem na kroki, zanim się zacznie kodować.
2. **Umiejętności miękkie — rozmowa z biznesem i ekspertami.** Dostaliśmy tylko
   „generator dokumentów", ale każdy krok to **wiedza domenowa od radców**. Im szybciej
   dostarczysz **proste** rozwiązanie, tym szybciej masz **feedback** — nie wskakuj od
   razu na framework.
3. **Ewaluacja ustalona na starcie.** Na jaki rezultat się umawiamy i jak go mierzymy —
   zanim zaczniemy. Bez kryteriów zostaje tylko „no, generuje, spoko".

### Techniczne

- Architektura > pojedynczy prompt — margines błędu zero wymusza etapowość.
- **Selektywny kontekst** zamiast wrzucania wszystkiego (bez chunkowania/wektorów/RAG-a).
- **Pydantic / structured output ≫ LangGraph.** Structured output to **klej**, bez którego
  nic by się nie spięło — lekki, zero długu, działa w *każdym* podejściu. LangGraph to
  opcjonalny cukier i **dług zależności**; pójście dalej (planer, cykle) wpycha w **async**.
- Logika umiejętności **niezależna od frameworka** — to samo działa liniowo i w grafie.
- **Najpierw logika + baseline, framework na końcu — jeśli w ogóle.**

## Do uzupełnienia

- [x] Agenda (slajdy 2–7) — gotowa
- [x] Realne liczby — w README podejść (`baseline/`, `agent_linear/`, `agent_langgraph/`)
- [x] Sygnatura sprawy spójna (II K 25/25)
- [ ] Czasy per slajd/sekcja — rozplanować (slot 70 min)
