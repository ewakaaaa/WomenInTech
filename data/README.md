# Dane — sprawa Daniela Dzika

Akta pochodzą z oficjalnego zadania na **egzamin radcowski 2025** (prawo karne),
opublikowanego przez Ministerstwo Sprawiedliwości:

> https://www.gov.pl/web/sprawiedliwosc/zadania-wraz-z-opisem-istotnych-zagadnien-na-egzamin-radcowski-w-2025-r2

Pliki pobrano ręcznie i podzielono na pojedyncze dokumenty (po jednym piśmie na plik).

## Zawartość

- `input/` — 16 pism z akt sprawy w PDF (notatka, protokoły, akt oskarżenia, opinia
  biegłego, wyrok itd.). Nagłówek arkusza „EGZAMIN RADCOWSKI – PRAWO KARNE" jest
  usuwany przy wczytywaniu (`clean_text` w `src/loader.py`).
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

## Zadanie

Wcielamy się w **obrońcę** i piszemy **apelację** od tego wyroku.

> Uwaga: prawdziwe zadanie egzaminacyjne dopuszcza również wniosek, że apelacja jest
> niezasadna — na potrzeby warsztatu **upraszczamy to do jednego celu**: napisać apelację.

Kluczowe wątki, na których opiera się obrona (zob. `eval.json`), to m.in.: czy jazda
po alejce cmentarnej to „ruch lądowy", błędne ustalenie nietrzeźwości w chwili dojazdu,
zasada *in dubio pro reo* (art. 5 § 2 k.p.k.), dowód z wyjaśnień złożonych w stanie
nietrzeźwości (art. 171 § 7 k.p.k.), brak wniosku o ściganie przy czynie z art. 288 k.k.
oraz orzeczenie naprawienia szkody mimo toczącej się sprawy cywilnej.
