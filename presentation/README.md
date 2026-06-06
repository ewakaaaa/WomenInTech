# Prezentacja — plan warsztatu

> **Czy AI może napisać dobrą apelację? Case study systemu, który zdałby egzamin radcowski.**
> Format: 70 min, case study + live demo. Perspektywy Women in Tech Summit.

Tu trzymamy materiały do prezentacji (slajdy, notatki) i poniższy plan.

## Teza

AI potrafi napisać apelację na poziomie egzaminu radcowskiego — **ale tylko przy
odpowiedniej architekturze**. Sam prompt „napisz apelację" nie wystarczy; potrzebny
jest wieloetapowy agent **i** człowiek weryfikujący każdy etap.

## Plan slajd po slajdzie

> ⏱️ Czasy orientacyjne, **70 min**. 

### Wstęp i kontekst — *~10 min*

1. **Przywitanie.** — *1 min*
2. **Agenda.** *(uzupełnimy na końcu)* — *1 min*
3. **Kim jestem.** Matematyczka → data scientist w COI. Najbardziej kojarzalna z
   chatbotem w mObywatelu, ale głównie pracuję w mniej widocznej działce prawnej.
   Na studiach nie wyobrażałam sobie siebie jako programistki — a teraz pokazuję
   publicznie swoje repo. *(„nigdy nie mów nigdy")* — *2 min*
4. **Repo na żywo.** Link do repozytorium — „jestem na konferencji i pokazuję wam
   swój kod". Zaproszenie: pobierzcie projekt i odpalajcie / patrzcie razem ze mną. — *2 min*
5. **Cel i motywacja.** Chcemy mieć **generator dokumentów** (pism prawniczych). — *1 min*
6. **Dane.** Udało się znaleźć świetne dane, bo: 
    a) są **zanonimizowane**,
    b) mają **klucz odpowiedzi** → możemy *mierzyć* jakość, nie tylko „patrzeć, że ładne".
   Przybliżenie sprawy: **sprawa Daniela Dzika** — o co w niej chodzi (zob.
   [`data/README.md`](../data/README.md)).
   Przygotowanie danych: **bez wektorowej bazy i bez RAG-a** — możemy sobie na to
   pozwolić, bo taką sprawę prowadzi się zwykle **raz** (nie budujemy wyszukiwarki po
   tysiącach spraw). Liczy się dobre **przygotowanie danych** — i można z nich wyciągać
   jeszcze więcej **metadanych**. — *3 min*

### Baseline i jego problemy — *~11 min*

7. **Baseline — kod, ewaluacja, wyniki.** Warto zacząć od czegoś prostego — mamy punkt
   startowy. Trzy rzeczy: — *6 min*
   - **Kod na żywo** (`notebooks/baseline_walkthrough.ipynb`): jak banalny jest baseline —
     `build_context` skleja **całe akta** i jeden `call_llm` z promptem „napisz apelację".
   - **Jak będziemy ewaluować** (`notebooks/eval_walkthrough.ipynb`) — *to umawiamy się
     na samym początku, raz dla wszystkich podejść:*
       - **pokrycie** — sędzia-LLM sprawdza dla **każdego** zagadnienia z `data/eval.json`,
         czy apelacja je porusza (wynik `X/12`),
       - **jakość** — ocena formy wg 3 kryteriów egzaminu (skala 2–6).
   - **Wynik baseline:** pokrycie **4/12 (33%)** *(w 3 przebiegach 33–42%)* + niepokryte
     zagadnienia. Pointa: **„technicznie działa, ale czy *dobrze*?"**
8. **Pytanie do sali:** jakie widzicie z tym problemy? *(odpowiedzi złożą się w listę
   ograniczeń: zapchany kontekst, wszystko naraz, brak audytu, halucynacje…)* — *3 min*
9. **Eksperci domenowi.** Jak ważni są eksperci domenowi — i **jak człowiek
   podszedłby do tego zadania?** *(zawias do architektury)* — *2 min*

### Jak zrobiłby to człowiek (intuicja, bez kodu) — *~8 min*

10. **Plan jak człowiek (1):** najpierw pobieżnie przeglądasz, jakie masz dokumenty
    i zapisujesz **główny cel** — „napisać apelację".
    *(wzmianka: na egzaminie zadaniem jest też ocena, czy apelacja ma podstawy — na
    warsztacie upraszczamy do jednego celu.)* — *1,5 min*
11. **Plan jak człowiek (2):** skoro wiem mniej więcej, co mam w papierach, zastanawiam
    się, **co trzeba sprawdzić** — np. przeczytać wszystkie zeznania i poszukać
    nieścisłości. Powstaje **lista TODO**. — *1,5 min*
12. **Plan jak człowiek (3):** realizuję rzeczy z listy TODO i **spisuję wnioski**. — *1,5 min*
13. **Plan jak człowiek (4):** happy path — przechodzę do **podsumowania i obmyślenia
    strategii** pisania apelacji. — *1,5 min*
14. **Plan jak człowiek (5):** skoro wiem, co chcę napisać — **piszę apelację**. — *1,5 min*

### Reveal, oddech i kod — *~12 min*

15. **Reveal: to jest dokładnie nasz agent.** Mapowanie kroków człowieka na umiejętności: — *2 min*

    | człowiek | umiejętność |
    |----------|-------------|
    | przegląda papiery, notuje co ważne | `generate_file_description` |
    | robi listę TODO, co sprawdzić | `generate_tasks` |
    | realizuje TODO, spisuje wnioski | `make_task` |
    | podsumowuje, obmyśla strategię | `generate_strategy` |
    | pisze apelację | `generate_document` |

16. **🫁 Oddech — anegdota.** Przed gęstą częścią techniczną: ostatnio ktoś zapytał
    mnie o top-3 rzeczy, które powinien umieć data scientist *(skren z LinkedIna)*.
    Jedna z nich — odróżniająca mida od seniora — to to, że senior nie tylko zrobi
    zadanie, ale **zaplanuje całe rozwiązanie**. *(I to właśnie przed chwilą zrobiliśmy.)* — *2 min*
17. **Kod na żywo:** `notebooks/linear_walkthrough.ipynb` — odpalamy umiejętności po kolei i
    oglądamy outputy każdego etapu. Przy okazji pokazujemy, jak agent **rozwiązuje
    problemy ze slajdu 8**: — *8 min*
    - **podsumowania zamiast pełnych akt** → mniej tokenów (opisy plików, nie 16 pełnych dokumentów),
    - **analiza wybranych dokumentów**, a nie wszystkich naraz → selektywny kontekst (model widzi tylko trafny wycinek),
    - **rozbicie dużego zadania na małe kawałki** → łatwiej i dokładniej, każdy krok robi jedno,
    - **przekazywanie głównego celu** (`goal`) przez wszystkie etapy → swego rodzaju **pamięć agenta**, dzięki której nie gubi kierunku.

### Jak to się spina i wyniki — *~8 min*

18. **Structured output — klej całego pipeline'u.** Bez tego nie dałoby się spiąć
    umiejętności w jeden przepływ. Nie ma tu żadnej magii — po prostu **polegamy** na
    tym, że każda umiejętność zwraca **typowany obiekt** (Pydantic), więc dokładnie
    wiem, jakiego outputu się spodziewać i mogę go podać dalej. Bez structured output
    te kroki by się nie połączyły. — *3 min*
19. **Pokazujemy wyniki** — apelacja agenta + porównanie z baseline (odczyt z notebooków
    `eval_walkthrough` / `linear_walkthrough` lub logów `*/output/`). Pokrycie na **3
    przebiegach**: agent **50–67%** (śr. ~58%) vs baseline **33–42%** (śr. ~36%); jakość
    **4,33 = 4,33** (różnicę robi pokrycie). Pointa: zakresy **się nie nakładają** — agent
    **zawsze** wyżej, choć liczba skacze → dlatego ewaluacja na kilku przebiegach, nie jednym. — *3 min*
20. **Pytanie do sali:** co jeszcze można by tu usprawnić? Jakie macie pomysły?
    *(symetria do slajdu 8 — zbieramy pomysły; część z nich, np. równoległość czy
    człowiek w pętli, „domknie" zaraz LangGraph)* — *2 min*

### LangGraph, „co dalej?" i puenta — *~13 min*

21. **LangGraph — co wnosi i ile kosztuje.** Mamy logikę **napisaną czystymi
    funkcjami**, więc łatwo ją opakować w węzły — ta sama logika, tylko jako graf.
    Co dostajemy w zamian: — *~4 min*
    - **wspólny State przenoszony między krokami** — jawny i czysty,
    - **równoległość (fan-out `Send`)** — opisy plików i wykonanie zadań liczą się
      **współbieżnie**, podczas gdy w `agent_linear` były to sekwencyjne pętle `for`.
      Konkret z przebiegu: **wall-clock 169,8 s vs 433,5 s** liniowo (**≈2,6× szybciej**),
      a **koszt ten sam** (~$0,74) — to samo, tylko szybciej,
    - **diagram grafu z kodu** — LangGraph rysuje graf w **mermaid** automatycznie
      (`graph.get_graph().draw_mermaid()`), więc obrazek na slajd robi się sam,
    - **toole / human-in-the-loop** — łatwo dołożyć narzędzia (function calling) albo
      pauzę na **potwierdzenie strategii przez radcę** → ale *u nas tego nie kodujemy*
      (pokazujemy pomysł na slajdzie 22, nie kod).
    - **⚠️ Przestroga (do tego wracamy na końcu):** to kolejna, niemała **zależność**
      (dług) — świetne do POC, na produkcji rozważ świadomie albo wcale.
22. **Pytanie do sali: co jeszcze można by zrobić?** *(symetria do slajdu 8 i 20 —
    domykamy warsztat pytaniem)*. Zbieramy pomysły, a w zanadrzu mamy **gotowe
    odpowiedzi** (to był kierunek „agenta nieliniowego", którego świadomie *nie*
    budujemy w kodzie — pokazujemy jako ideę + diagram `agent_planner/graph.md`): — *~4 min*
    - **agent sam decyduje, co dalej** — zamiast sztywnej kolejności planer w pętli:
      *analizuj / zapytaj człowieka / pisz / brak podstaw* (graf **zawraca**),
    - **człowiek w pętli na żywo** — pauza (`interrupt`) na potwierdzenie strategii
      przez radcę, zanim agent napisze pismo,
    - **narzędzia (function calling)** — np. tool sprawdzający **najnowsze przepisy**,
    - **wczesne wyjście „brak podstaw"** — agent może uznać, że apelacja jest niezasadna.
    - **❗ Ale uwaga (puenta techniczna):** w LangGraph *dałoby się* to zrobić bez
      pisania własnej orkiestracji (cykle i warunki to natywne krawędzie grafu) — tylko
      żeby zrobić to **dobrze (dynamicznie + równolegle)**, schodzi się na **logikę
      async**. Czyli: więcej mocy = więcej złożoności. Dlatego **tego nie dokładamy**.
23. **Podsumowanie technologii: Pydantic ≫ LangGraph.** Co naprawdę zbudowało ten
    system? — *~2 min*
    - **Pydantic / structured output — bohater i niezbędny klej.** Bez niego umiejętności
      by się nie spięły (każda zwraca typowany obiekt → wiem, co podać dalej). Lekki,
      zero długu, działa w *każdym* podejściu (baseline, liniowy, graf).
    - **LangGraph — opcjonalny cukier.** Daje równoległość, diagram, checkpointing,
      human-in-the-loop — ale to **ciężka zależność**, a pójście dalej (planer, cykle)
      wpycha w **async**. Świetny do POC; na produkcji **świadomie albo wcale**.
    - **Morał:** najpierw logika + Pydantic + baseline; framework **na końcu, jeśli w
      ogóle**. Nie zaczynaj od frameworka ani od złożonego agenta „robiącego nie wiadomo co".
24. **Take-awaye.** Domykamy **anegdotę o top-3 umiejętnościach DS** — wszystkie trzy
    przewinęły się przez warsztat: (1) **zaplanowanie rozwiązania**, (2) **rozmowa z
    biznesem i ekspertami** (szybko dostarcz proste → szybko zbierz feedback), (3)
    **ewaluacja ustalona na starcie**. (Szczegóły poniżej.) — *~3 min*

### Pytania (Q&A) — *~10 min*

Zarezerwowane na sam koniec. *(Agendę ze slajdu 2 uzupełniamy na końcu — pamiętać,
żeby zapowiedzieć, że pytania zbieramy na finał.)*

## Demo — checklista

- [x] `.env` z działającym kluczem LLM (`gpt-5.4`) — sprawdzone (przebiegi 2026-06-06/07)
- [x] Wygenerowane apelacje w `baseline/`, `agent_linear/`, `agent_langgraph/` (`*/output/`, na wypadek braku sieci)
- [x] Liczby ewaluacji zebrane: baseline **33–42%**, liner **50–67%**, jakość **4,33** (3 przebiegi) — *zostaje wstawić na slajdy*
- [x] Liczby do slajdu 21: wall-clock i koszt langgraph vs liner (169,8 s, ≈2,6×, ~$0,74)
- [x] Diagram grafu (mermaid z `agent_langgraph`) — `agent_langgraph/graph.md`
- [x] Diagram grafu nieliniowego (`agent_planner/graph.md`) — slajd 22 (idea „co dalej?", bez kodu/demo)
- [ ] `uv run jupyter lab` — przeklikać na żywo `notebooks/baseline_walkthrough.ipynb` (slajd 7, kod),
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
   szybciej masz **feedback** — dlatego nie wskakuj od razu na framework i agenta
   robiącego „nie wiadomo co".
3. **Ewaluacja ustalona na starcie.** Na jaki rezultat się umawiamy i jak go mierzymy —
   zanim zaczniemy. Bez kryteriów zostaje tylko „no, generuje, spoko" albo
   bezterminowe czekanie na feedback ekspertów.

### Techniczne

- Architektura > pojedynczy prompt — margines błędu zero wymusza etapowość.
- **Selektywny kontekst** zamiast wrzucania wszystkiego (bez chunkowania/wektorów/RAG-a).
- **Pydantic / structured output ≫ LangGraph.** To structured output jest **klejem**, bez
  którego nic by się nie spięło — lekki, zero długu, działa w *każdym* podejściu.
  LangGraph to opcjonalny cukier (równoległość/diagram/checkpoint/human-in-the-loop) i
  **dług zależności**; pójście dalej (planer, cykle) wpycha w **async** = złożoność.
- Logika umiejętności **niezależna od frameworka** — to samo działa liniowo i w grafie;
  dzięki temu LangGraph da się w razie czego odpiąć.
- **Najpierw logika + baseline, framework na końcu — jeśli w ogóle.** Nie zaczynaj od
  frameworka ani od złożonego agenta „robiącego nie wiadomo co".
- **Człowiek w pętli** jest częścią systemu, nie dodatkiem.

## Do uzupełnienia

- [x] Realne liczby (przebieg 2026-06-06, `gpt-5.4`): baseline **4/12 (33%)**, liner
  **8/12 (67%)**, jakość **4,33** w obu; langgraph **169,8 s ≈2,6×** szybciej, koszt
  **$0,73 ≈ liner**. Szczegóły w README podejść.
- [ ] Slajdy (na podstawie tego planu)
- [ ] Agenda (slajd 2) — uzupełnić na końcu, zapowiedzieć, że pytania zbieramy na finał
