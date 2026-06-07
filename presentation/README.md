# Prezentacja — plan warsztatu

> **Czy AI może napisać dobrą apelację? Case study systemu, który zdałby egzamin radcowski.**
> Format: 70 min, case study + live demo. Women in Tech Summit.

## Teza

AI potrafi napisać apelację na poziomie egzaminu radcowskiego — **ale tylko przy
odpowiedniej architekturze**. Sam prompt „napisz apelację" nie wystarczy; potrzebny
jest wieloetapowy agent **i** człowiek weryfikujący każdy etap.

## Jak czytać ten plan

Każdy slajd ma dwie warstwy:
- **Na slajdzie** — hasła, które widzi sala (minimalistycznie, ≤6 słów/bullet).
- **Mówię** — notatki prowadzącego (to, co opowiadasz).

`[demo]` = pokaz na żywo · `[img]` = obraz/diagram zamiast tekstu. **Czasy: do
rozplanowania od nowa** (slot 70 min). Liczby do wstawienia są w README podejść.

---

## Wstęp i kontekst

### 1 · Czy AI napisze dobrą apelację?
**Na slajdzie:**
- case study: system zdający egzamin radcowski
- Women in Tech
**Mówię:** przywitanie, tytuł, hook.

### 2 · Agenda
**Na slajdzie:**
- baseline i jego granice
- jak zrobiłby to człowiek → agent
- ewaluacja i wyniki
- LangGraph: co daje, co kosztuje
- pytania na końcu
**Mówię:** uzupełnić na końcu pracy nad slajdami; zapowiedzieć, że **pytania zbieramy na finał**.

### 3 · Kim jestem
**Na slajdzie:**
- matematyczka → data scientist (COI)
- mObywatel, działka prawna
- „nigdy nie mów nigdy" — pokazuję swój kod
**Mówię:** na studiach nie wyobrażałam sobie siebie jako programistki — a teraz publicznie pokazuję repo.

### 4 · Repo na żywo
**Na slajdzie:**
- `[img]` QR → repo (`qr-repo.svg`)
- `github.com/ewakaaaa/WomenInTech`
- pobierzcie, patrzcie ze mną
**Mówię:** „jestem na konferencji i pokazuję wam swój kod" — zaproszenie do odpalania razem.

### 5 · Cel
**Na slajdzie:**
- generator pism prawniczych
- zerowy margines błędu
**Mówię:** chcemy generator dokumentów; halucynacja = przegrana sprawa.

### 6 · Dane — sprawa Daniela Dzika
**Na slajdzie:**
- akta egzaminu radcowskiego 2025
- zanonimizowane + **klucz odpowiedzi** → mierzymy
- bez wektorów / RAG-a (sprawę prowadzi się raz)
- `[img]` biurko z aktami
**Mówię:** świetne dane, bo zanonimizowane i z kluczem odpowiedzi → *mierzymy* jakość, nie „patrzymy, że ładne".
Przybliżenie sprawy (zob. [`data/README.md`](../data/README.md)). Bez wektorów/RAG-a — sprawę prowadzi się
raz, liczy się dobre przygotowanie danych i metadane.

## Baseline i jego problemy

### 7 · Baseline: kod, ocena, wynik
**Na slajdzie:**
- całe akta → **1 prompt** `[demo]`
- ocena: **pokrycie X/12** + **jakość 2–6**
- wynik: **4/12 (33%)** *(3 przebiegi: 33–42%)*
- „działa — ale czy *dobrze*?"
**Mówię:** trzy rzeczy:
1. **Kod na żywo** (`notebooks/baseline_walkthrough.ipynb`) — jak banalny jest baseline: `build_context`
   skleja całe akta + jeden `call_llm` „napisz apelację".
2. **Jak będziemy ewaluować** (`notebooks/eval_walkthrough.ipynb`) — umawiamy się na starcie, raz dla
   wszystkich podejść: **pokrycie** (sędzia-LLM sprawdza każde zagadnienie z `data/eval.json`, `X/12`) +
   **jakość** (3 kryteria egzaminu, 2–6).
3. **Wynik baseline** + niepokryte zagadnienia. Pointa: „technicznie działa, ale czy *dobrze*?".

### 8 · ❓ Co z tym jest nie tak?
**Na slajdzie:**
- *(pytanie do sali)*
- → kontekst, wszystko naraz, audyt, halucynacje
**Mówię:** zbieramy od sali listę ograniczeń (zapchany kontekst, wszystko naraz, brak audytu, halucynacje…).
To wrócimy na slajdzie 17 jako „rozwiązane".

### 9 · A jak zrobiłby to człowiek?
**Na slajdzie:**
- ekspert domenowy = radca
- intuicja zamiast jednego strzału
**Mówię:** jak ważni są eksperci domenowi i jak człowiek podszedłby do zadania — zawias do architektury.

## Jak zrobiłby to człowiek (intuicja, bez kodu)

### 10–14 · Plan jak człowiek (5 kroków)
**Na slajdzie:**
- przejrzyj akta → zapisz **cel**
- co sprawdzić → **lista TODO**
- realizuj TODO → **wnioski**
- **strategia** pisma
- **napisz** apelację
- `[img]` 5 ikon kroków
**Mówię:** prowadzimy salę przez intuicję (pięć kroków). *(Wzmianka: na egzaminie zadaniem jest też ocena,
czy apelacja ma podstawy — na warsztacie upraszczamy do jednego celu.)* Pięć kroków celowo buduje napięcie
do reveala na slajdzie 15.

## Reveal, oddech i kod

### 15 · To jest dokładnie nasz agent
**Na slajdzie:**
- `[img]` tabela: człowiek → umiejętność
- przegląd → `file_description`
- TODO → `tasks` · realizacja → `make_task`
- strategia → `strategy` · pismo → `document`
**Mówię:** mapujemy kroki człowieka na umiejętności — to **dokładnie** to, co przed chwilą wymyśliliśmy.

### 16 · 🫁 Oddech — anegdota
**Na slajdzie:**
- `[img]` screen z LinkedIna
- senior = **planuje całe rozwiązanie**
- (to właśnie zrobiliśmy)
**Mówię:** ktoś zapytał o top-3 umiejętności DS; jedna (mid→senior) to planowanie całego rozwiązania —
i to przed chwilą zrobiliśmy. Oddech przed gęstą częścią techniczną.

### 17 · Agent liniowy na żywo
**Na slajdzie:**
- `[demo]` `linear_walkthrough`
- podsumowania zamiast pełnych akt
- selektywny kontekst (tylko trafne dok.)
- małe kroki + cel niesiony przez pipeline
**Mówię:** odpalamy umiejętności po kolei, oglądamy outputy etapów. Pokazujemy, jak agent **rozwiązuje
problemy ze slajdu 8**: podsumowania (mniej tokenów), selektywny kontekst (model widzi tylko trafny
wycinek), rozbicie na małe kroki, cel (`goal`) niesiony przez cały pipeline = pamięć agenta.
⏰ **Ryzyko czasowe:** mieć outputy gotowe/widoczne, nie czekać na zimne wywołania na scenie.

## Jak to się spina i wyniki

### 18 · Structured output = klej
**Na slajdzie:**
- każda umiejętność → **typowany obiekt** (Pydantic)
- wiem, co dostanę → podaję dalej
- bez tego nic się nie spina
**Mówię:** żadnej magii — polegamy na tym, że każdy krok zwraca typowany obiekt, więc wiem, czego się
spodziewać i mogę go podać dalej. Bez structured output kroki by się nie połączyły.

### 19 · Wyniki (3 przebiegi)
**Na slajdzie:**
- agent **50–67%** vs baseline **33–42%**
- jakość 4,33 = 4,33
- zakresy się **nie nakładają** → agent zawsze wyżej
- 1 przebieg kłamie → mierz kilka
**Mówię:** porównanie pokrycia (odczyt z `eval_walkthrough`/`linear_walkthrough` lub logów `*/output/`).
Różnicę robi pokrycie (jakość remis). Pointa: zakresy się nie nakładają — agent **zawsze** wyżej, choć
liczba skacze → dlatego ewaluacja na kilku przebiegach, nie jednym.

### 20 · ❓ Co jeszcze usprawnić?
**Na slajdzie:**
- *(pytanie do sali)*
**Mówię:** symetria do slajdu 8 — zbieramy pomysły; część (równoległość, człowiek w pętli) domknie
zaraz LangGraph. *(Rozważ cięcie — bliźniacze do slajdu 22; jeśli brakuje czasu, zrób retoryczne.)*

## LangGraph, „co dalej?" i puenta

### 21 · LangGraph — co daje, co kosztuje
**Na slajdzie:**
- równoległość (`Send`): **2,6× szybciej**, ten sam koszt
- wspólny State, diagram z kodu
- ⚠️ ciężka **zależność** (dług)
**Mówię:** logika w czystych funkcjach → łatwo opakować w węzły. Zyski: wspólny State, równoległość
(fan-out `Send` — konkret: 169,8 s vs 433,5 s, ~$0,74 ten sam koszt), diagram z kodu (mermaid), łatwe
toole/human-in-the-loop (ale tego nie kodujemy — pokaz idei na 22). ⚠️ Przestroga: ciężka zależność
(dług) — świetne do POC, na produkcji świadomie albo wcale.

### 22 · ❓ Co dalej? (agent nieliniowy)
**Na slajdzie:**
- `[img]` diagram planera (zawraca w pętli)
- sam decyduje: analizuj / pytaj / pisz / brak podstaw
- człowiek w pętli, narzędzia
- robić dobrze → **async** = złożoność (nie robimy)
**Mówię:** pytanie do sali + gotowe odpowiedzi = kierunek „agenta nieliniowego" (świadomie nie budujemy
w kodzie — idea + diagram `agent_planner/graph.md`). Planer w pętli sam decyduje, graf zawraca; człowiek
w pętli; narzędzia (np. najnowsze przepisy). ❗ W LangGraph *dałoby się* bez własnej orkiestracji, ale
zrobić to dobrze (dynamicznie + równolegle) = **async** = złożoność. Dlatego nie dokładamy.

### 23 · Pydantic ≫ LangGraph
**Na slajdzie:**
- Pydantic = **niezbędny klej**, zero długu
- LangGraph = opcjonalny cukier
- najpierw logika + baseline; framework na końcu
**Mówię:** co naprawdę zbudowało system? Structured output (Pydantic) — bohater i niezbędny klej,
działa w *każdym* podejściu. LangGraph — opcjonalny cukier i dług zależności (pójście dalej wpycha w
async). Morał: najpierw logika + baseline; framework na końcu, jeśli w ogóle.

### 24 · Take-awaye
**Na slajdzie:**
- planuj całe rozwiązanie
- rozmawiaj z ekspertami, dostarczaj szybko
- **ewaluacja ustalona na starcie**
**Mówię:** domykamy anegdotę o top-3 umiejętnościach DS (szczegóły niżej w „Kluczowe przekazy").

### 25 · Pytania
**Na slajdzie:**
- dzięki! · `github.com/ewakaaaa/WomenInTech`
**Mówię:** Q&A (10–15 min). Agendę ze slajdu 2 dopisać na końcu.

---

## Demo — checklista

- [x] `.env` z działającym kluczem LLM (`gpt-5.4`) — sprawdzone (przebiegi 2026-06-06/07)
- [x] Wygenerowane apelacje w `baseline/`, `agent_linear/`, `agent_langgraph/` (`*/output/`, na wypadek braku sieci)
- [x] Liczby ewaluacji zebrane: baseline **33–42%**, liner **50–67%**, jakość **4,33** (3 przebiegi) — *zostaje wstawić na slajdy*
- [x] Liczby do slajdu 21: wall-clock i koszt langgraph vs liner (169,8 s, ≈2,6×, ~$0,74)
- [x] Diagram grafu (mermaid z `agent_langgraph`) — `agent_langgraph/graph.md`
- [x] Diagram grafu nieliniowego (`agent_planner/graph.md`) — slajd 22 (idea „co dalej?", bez kodu/demo)
- [x] `uv run jupyter lab` — przeklikane na żywo `notebooks/baseline_walkthrough.ipynb` (slajd 7, kod),
      `notebooks/eval_walkthrough.ipynb` (slajd 7, jak ewaluujemy) i `notebooks/linear_walkthrough.ipynb` (slajd 17)
- [ ] Skren z LinkedIna (slajd 16 — oddech/anegdota)

## Kluczowe przekazy (take-aways)

### Callback do anegdoty — 3 top umiejętności DS (przeplatają się przez cały warsztat)

1. **Zaplanowanie całego rozwiązania** (mid → senior). To dziś przećwiczyliśmy: rozbić
   problem na kroki, zanim się zacznie kodować.
2. **Umiejętności miękkie — rozmowa z biznesem i ekspertami.** Dostaliśmy tylko
   „generator dokumentów", ale każdy krok po drodze to **wiedza domenowa od radców** —
   trzeba umieć z nimi rozmawiać i budować relacje. Im szybciej dostarczysz **proste**
   rozwiązanie (jak `agent_linear`, gdzie widać krok po kroku, co się dzieje), tym
   szybciej masz **feedback** — dlatego nie wskakuj od razu na framework.
3. **Ewaluacja ustalona na starcie.** Na jaki rezultat się umawiamy i jak go mierzymy —
   zanim zaczniemy. Bez kryteriów zostaje tylko „no, generuje, spoko".

### Techniczne

- Architektura > pojedynczy prompt — margines błędu zero wymusza etapowość.
- **Selektywny kontekst** zamiast wrzucania wszystkiego (bez chunkowania/wektorów/RAG-a).
- **Pydantic / structured output ≫ LangGraph.** To structured output jest **klejem**, bez
  którego nic by się nie spięło — lekki, zero długu, działa w *każdym* podejściu.
  LangGraph to opcjonalny cukier i **dług zależności**; pójście dalej (planer, cykle) wpycha w **async**.
- Logika umiejętności **niezależna od frameworka** — to samo działa liniowo i w grafie.
- **Najpierw logika + baseline, framework na końcu — jeśli w ogóle.**
- **Człowiek w pętli** jest częścią systemu, nie dodatkiem.

## Do uzupełnienia

- [ ] Slajdy (na podstawie tego planu)
- [ ] Agenda (slajd 2) — uzupełnić na końcu, zapowiedzieć, że pytania zbieramy na finał
- [ ] Czasy per slajd/sekcja — rozplanować na nowo (slot 70 min)
