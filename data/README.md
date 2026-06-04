# Dane — sprawa Daniela Dzika

Akta pochodzą z oficjalnego zadania na **egzamin radcowski 2025** (prawo karne),
opublikowanego przez Ministerstwo Sprawiedliwości:

> https://www.gov.pl/web/sprawiedliwosc/zadania-wraz-z-opisem-istotnych-zagadnien-na-egzamin-radcowski-w-2025-r2

Pliki pobrano ręcznie i podzielono na pojedyncze dokumenty (po jednym piśmie na plik).

## Zawartość

- `input/` — 16 pism z akt sprawy w PDF (po jednym piśmie na plik). Nagłówek arkusza
  „EGZAMIN RADCOWSKI – PRAWO KARNE" jest usuwany przy wczytywaniu (`clean_text`
  w `src/loader.py`). Co zawierają poszczególne pliki:

  | Plik | Co to jest |
  |------|------------|
  | `02_Notatka_urzędowa...` | Ustalenia policji z interwencji wobec nietrzeźwego kierowcy |
  | `03_Protokół_z_badania_stanu_trzeźwości...` | Wynik badania alkomatem (analizator wydechu) |
  | `04_Postanowienie_o_wszczęciu_dochodzenia` | Formalne wszczęcie dochodzenia |
  | `05_`, `06_`, `07_Protokół_przesłuchania_świadka` | Zeznania świadków (trzy osoby) |
  | `08_Postanowienie_o_przedstawieniu_zarzutów` | Przedstawienie zarzutów oskarżonemu |
  | `09_`, `10_Protokół_przesłuchania_podejrzanego` | Wyjaśnienia podejrzanego (dwa przesłuchania) |
  | `11_Akt_oskarżenia` | Akt oskarżenia sporządzony przez prokuraturę |
  | `12_`, `15_Protokół_rozprawy_głównej` | Przebieg rozpraw przed sądem I instancji |
  | `13_Odpowiedź...zarządzania_cmentarzem` | Pismo o statusie/zarządcy alejki cmentarnej |
  | `14_Opinia_biegłego...toksykologii_sądowej` | Opinia biegłego o stężeniu alkoholu w czasie |
  | `16_Wyrok` | Wyrok sądu I instancji |
  | `17_Wniosek_o_sporządzenie_uzasadnienia` | Wniosek o pisemne uzasadnienie wyroku |

- `eval.json` — **lista zagadnień, które apelacja powinna poruszyć** (klucz oceny).

> Dane są zanonimizowane/syntetyczne (fikcyjne osoby), więc nadają się do publicznego
> repo i dema na żywo.

## O co chodzi w sprawie

- **Oskarżony:** Daniel Dzik (ur. 1968, informatyk, niekarany), obrońca: Gabriela Gil.
- **Sąd:** Sąd Rejonowy dla Krakowa – Krowodrzy, II Wydział Karny, sygn. **II K 25/25**,
  wyrok z 14 marca 2025 r.
- **Zdarzenie:** 31 grudnia 2024 r. w Szczyglicach — oskarżony wjechał samochodem
  (Jeep Wrangler) w **alejkę cmentarną**, gdzie spożywał alkohol; zniszczył też ławkę.

### Zarzuty i wyrok I instancji

| | Czyn | Kwalifikacja | Rozstrzygnięcie |
|---|------|--------------|-----------------|
| I | Prowadzenie pojazdu w stanie nietrzeźwości (1,63→1,22 mg/l) | art. 178a § 1 k.k. | wina; grzywna, **5-letni zakaz prowadzenia**, świadczenie 6 000 zł, **przepadek auta** |
| II | Umyślne zniszczenie drewnianej ławki (7 000 zł) na szkodę Ryszarda Rysia | art. 288 § 1 k.k. | wina; grzywna + **obowiązek naprawienia szkody 7 000 zł** |

Kara łączna: 350 stawek dziennych grzywny po 20 zł.
