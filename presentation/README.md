# Prezentacja — plan warsztatu

> **Czy AI może napisać dobrą apelację? Case study systemu, który zdałby egzamin radcowski.**
> Format: 70 min, case study + live demo. Perspektywy Women in Tech Summit.

Tu trzymamy materiały do prezentacji (slajdy, notatki) i poniższy plan.

## Teza

AI potrafi napisać apelację na poziomie egzaminu radcowskiego — **ale tylko przy
odpowiedniej architekturze**. Sam prompt „napisz apelację" nie wystarczy; potrzebny
jest wieloetapowy agent **i** człowiek weryfikujący każdy etap.

## Plan slajd po slajdzie

### Wstęp i kontekst

1. **Przywitanie.**
2. **Agenda.** *(uzupełnimy na końcu)*
3. **Kim jestem.** Matematyczka → data scientist w COI. Najbardziej kojarzalna z
   chatbotem w mObywatelu, ale głównie pracuję w mniej widocznej działce prawnej.
   Na studiach nie wyobrażałam sobie siebie jako programistki — a teraz pokazuję
   publicznie swoje repo. *(„nigdy nie mów nigdy")*
4. **Repo na żywo.** Link do repozytorium — „jestem na konferencji i pokazuję wam
   swój kod". Zaproszenie: pobierzcie projekt i odpalajcie / patrzcie razem ze mną.
5. **Cel i motywacja.** Chcemy mieć **generator dokumentów** (pism prawniczych).
6. **Dane.** Udało się znaleźć świetne dane, bo: a) są **zanonimizowane**,
   b) mają **klucz odpowiedzi** → możemy *mierzyć* jakość, nie tylko „patrzeć, że ładne".
   Przybliżenie sprawy: **sprawa Daniela Dzika** — o co w niej chodzi (zob.
   [`data/README.md`](../data/README.md)).

### Baseline i jego problemy

7. **Baseline + wyniki.** Warto zacząć od czegoś prostego — mamy punkt startowy.
   Pokaż wygenerowaną apelację + wynik ewaluacji `X/12` + niepokryte zagadnienia.
   Pointa: **„technicznie działa, ale czy *dobrze*?"**
8. **Pytanie do sali:** jakie widzicie z tym problemy? *(odpowiedzi złożą się w listę
   ograniczeń: zapchany kontekst, wszystko naraz, brak audytu, halucynacje…)*
9. **Eksperci domenowi.** Jak ważni są eksperci domenowi — i **jak człowiek
   podszedłby do tego zadania?** *(zawias do architektury)*

### Jak zrobiłby to człowiek (intuicja, bez kodu)

10. **Anegdota:** ostatnio ktoś zapytał mnie o top-3 rzeczy, które powinien umieć
    data scientist *(skren z LinkedIna)*. Jedna z nich — odróżniająca mida od seniora —
    to to, że senior nie tylko zrobi zadanie, ale **zaplanuje całe rozwiązanie**.
11. **Plan jak człowiek (1):** najpierw pobieżnie przeglądasz, jakie masz dokumenty
    *(slajd: biurko z papierami)* i zapisujesz **główny cel** — „napisać apelację".
    *(wzmianka: na egzaminie zadaniem jest też ocena, czy apelacja ma podstawy — na
    warsztacie upraszczamy do jednego celu.)*
12. **Plan jak człowiek (2):** skoro wiem mniej więcej, co mam w papierach, zastanawiam
    się, **co trzeba sprawdzić** — np. przeczytać wszystkie zeznania i poszukać
    nieścisłości. Powstaje **lista TODO**.
13. **Plan jak człowiek (3):** realizuję rzeczy z listy TODO i **spisuję wnioski**.
14. **Plan jak człowiek (4):** happy path — przechodzę do **podsumowania i obmyślenia
    strategii** pisania apelacji.
15. **Plan jak człowiek (5):** skoro wiem, co chcę napisać — **piszę apelację**.

### Reveal: człowiek = agent

16. **To jest dokładnie nasz agent.** Mapowanie kroków człowieka na umiejętności:

    | człowiek | umiejętność |
    |----------|-------------|
    | przegląda papiery, notuje co ważne | `generate_file_description` |
    | robi listę TODO, co sprawdzić | `generate_tasks` |
    | realizuje TODO, spisuje wnioski | `make_task` |
    | podsumowuje, obmyśla strategię | `generate_strategy` |
    | pisze apelację | `generate_document` |

17. **Kod na żywo:** `notebooks/walkthrough.ipynb` — odpalamy umiejętności po kolei i
    oglądamy outputy każdego etapu. Tu pokazujemy **selektywny kontekst** (każdy krok
    widzi tylko wybrane dokumenty, nie całe akta).

### Dalej — do rozpisania

- [ ] Spięcie liniowe (`linear_agent/`) — te same funkcje, czysty Python
- [ ] LangGraph + Studio (`uv run langgraph dev`) — fan-out `Send`, po co i jaki koszt
- [ ] Rola człowieka w pętli — weryfikacja każdego etapu
- [ ] Wyniki i porównanie (`src.eval.compare`) — baseline vs agent
- [ ] Take-awaye
- [ ] Agenda (slajd 2)

## Demo — checklista

- [ ] `.env` z działającym kluczem LLM (zapasowy backend: Ollama / proxy)
- [ ] Wygenerowane apelacje w `baseline/`, `linear_agent/`, `langgraph_agent/` (na wypadek braku sieci)
- [ ] Wyniki `uv run python -m src.eval.compare` zrzucone do slajdu (plan B bez live)
- [ ] `uv run jupyter lab` — sprawdzony `notebooks/walkthrough.ipynb`
- [ ] `uv run langgraph dev` — sprawdzone Studio
- [ ] Diagram grafu (mermaid z `langgraph_agent`)
- [ ] Skren z LinkedIna (slajd 10)

## Kluczowe przekazy (take-aways)

1. Architektura > pojedynczy prompt — margines błędu zero wymusza etapowość.
2. **Selektywny kontekst** zamiast wrzucania wszystkiego (bez chunkowania/wektorów).
3. Logika umiejętności **niezależna od frameworka** — to samo działa liniowo i w grafie.
4. LangGraph daje równoległość/obserwowalność/Studio, ale to dług zależności.
5. **Człowiek w pętli** jest częścią systemu, nie dodatkiem.

## Do uzupełnienia

- [ ] Realne liczby do tabeli wyników (po uruchomieniu na żywo)
- [ ] Slajdy
