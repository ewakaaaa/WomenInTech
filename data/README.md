# Dane — sprawa Daniela Dzika

Akta pochodzą z oficjalnego zadania na **egzamin radcowski 2025** (prawo karne),
opublikowanego przez Ministerstwo Sprawiedliwości:

> https://www.gov.pl/web/sprawiedliwosc/zadania-wraz-z-opisem-istotnych-zagadnien-na-egzamin-radcowski-w-2025-r2

Pliki pobrano ręcznie i podzielono na pojedyncze dokumenty (po jednym piśmie na plik).
Dane są zanonimizowane/syntetyczne (fikcyjne osoby), więc nadają się do publicznego repo.

Klucz oceny to `eval.json` — lista zagadnień, które dobra apelacja powinna poruszyć.

## Akta okiem agenta — `data/output/described.json`

Pierwszy krok pipeline'u (`generate_file_description`) zamienia każdy z 16 PDF-ów w
zwięzły wpis `{title, description, name}` i zapisuje całość do
`data/output/described.json` (cache, poza gitem — powstaje przy pierwszym przebiegu).
To z tej **mapy** agent rozumie, *o co chodzi w sprawie*, nie czytając 16 pełnych
dokumentów naraz. Przykładowy wpis:

```json
{
  "title": "NOTATKA URZĘDOWA",
  "description": "Dokument sporządzony przez sierż. Wiesława Wilka z KP w Balicach 31 grudnia 2024 r. Opisuje interwencję w Szczyglicach w rejonie cmentarza wobec kierującego pojazdem marki Jeep Wrangler, u którego wyczuwalna była silna woń alkoholu…",
  "name": "02_Notatka_urzędowa_z_interwencji_dotyczącej_nietrzeźwego_kierowcy.pdf"
}
```

## O co chodzi w sprawie (odtworzone z `described.json`)

- **Oskarżony:** Daniel Dzik; sprawa przed **Sądem Rejonowym dla Krakowa – Krowodrzy**,
  II Wydział Karny, sygn. **II K 25/25**, wyrok z **14 marca 2025 r.**
- **Zdarzenie:** 31 grudnia 2024 r. w Szczyglicach oskarżony wjechał Jeepem Wranglerem
  w **alejkę cmentarną**; policja stwierdziła woń alkoholu, przeprowadzono **badanie
  alkomatem**. Uszkodzona została też drewniana ławka.
- **Dwa zarzuty:** prowadzenie pojazdu w stanie nietrzeźwości (**art. 178a § 1 k.k.**)
  oraz zniszczenie mienia — ławki (**art. 288 § 1 k.k.**).

Chronologia widoczna w opisach (od notatki policji do wyroku):

| etap | dokumenty |
|------|-----------|
| interwencja i badanie trzeźwości | `02` notatka, `03` protokół alkomatu |
| wszczęcie dochodzenia | `04` postanowienie |
| świadkowie (Sikora, Kot, Ryś) | `05`–`07` protokoły przesłuchań |
| zarzuty i wyjaśnienia podejrzanego | `08` postanowienie, `09`–`10` przesłuchania |
| oskarżenie i proces | `11` akt oskarżenia, `12`/`15` rozprawy główne |
| dowody uzupełniające | `13` pismo o cmentarzu, `14` opinia biegłego toksykologa |
| rozstrzygnięcie | `16` wyrok, `17` wniosek o uzasadnienie |

Te wątki (m.in. czy oskarżony był nietrzeźwy **w chwili jazdy**, czy alejka cmentarna
to „ruch lądowy", brak wniosku o ściganie przy art. 288) to materiał, który apelacja
powinna podnieść — i które sprawdza `eval.json`.
