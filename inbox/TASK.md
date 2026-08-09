# Fazė 52 — matavimo sąžiningumo vartas Loop B/C ataskaitose. HUMAN-GATE GAUTAS („Varom"). <14 min.

## Tikslas

1. **Kiekviena Loop B/C ataskaitos metrika privalo nešti savo duomenų langą.** Šiandien ataskaita spausdina
   skaičių be jokios nuorodos, iš kokių ir kada surinktų duomenų jis gautas — todėl mirusi metrika atrodo
   lygiai taip pat kaip gyva. Prie kiekvienos skaičiuojamos metrikos pridėk **įrašų skaičių + naujausio
   įrašo datą**, pvz.:
   `- **cache-hit %:** 45.5  ⟨n=11, naujausias 2026-07-11, 29 d. senumo⟩`

2. **Raudona žyma pasenusiai metrikai.** Jei metrikos naujausias įrašas senesnis už ataskaitos periodą
   (Loop B — paros; Loop C — savaitės), metrika pažymima aiškiai, pvz. `⚠️ PASENĘ` / `STALE`.
   Kriterijus turi būti bendras (viena funkcija/pagalbinė), o ne įrašytas ranka prie vienos metrikos —
   kitaip kita mirusi metrika vėl praslys.

3. **Trumpa read-only diagnozė: kodėl `nav` nustojo rašytis?** (Antraeilis prioritetas — jei laiko
   mažai, daryk 1+2 pilnai ir šitą palik kitai fazei.) Nustatyk, KAS turėtų rašyti `action=nav` įrašus
   ir kodėl nustojo: ar navigacijos instrumentacija pašalinta/sugedusi, ar pati navigacija nebevyksta?
   Išvada su įrodymais (kodo vieta / log'as), ne spėjimu. **Netaisyk** — tik diagnozė.

## Realybė (jau patikrinta iš šalies 2026-08-09 — nekartok, naudok)

- `trajectories/*.jsonl`: **29 failai, 570 įrašų, naujausias įrašas 2026-08-08** ⇒ pėdsakų rašymas GYVAS ir auga.
- **BET `action=nav` įrašų — lygiai 20, ir naujausias iš jų 2026-07-11T17:58:47.** Nė vieno per 29 dienas.
- 11 iš tų 20 turi `cache_hit` lauką, 5 = True ⇒ **5/11 = 45,45% ≈ 45,5%.** Aritmetika teisinga —
  miręs yra duomenų šaltinis, ne skaičiuoklė. `vid. įrankių kvietimų / query: 1.55` — iš to paties šaltinio.
- Loop B tą patį 45,5% atspausdino kiekvienoje ataskaitoje nuo 08-02 iki 08-09 imtinai (patikrinta failuose).
- **Svarbu:** šis „cache-hit" yra **HERA vidinis vault navigacijos kešas** (L2 santraukos vs žalias
  `extracted/`), NE Anthropic prompt caching. Nesumaišyk.
- Kitos Loop B metrikos (skills, growth, wiki-lint orphan/dangling/prov) juda normaliai — jos gyvos.
  Šio darbo tikslas ne jas taisyti, o padaryti, kad SKIRTUMAS tarp gyvos ir mirusios būtų matomas iš ataskaitos.

## Apribojimai (nekintami)

- €0 · fail-safe (klaida skaičiuojant langą → metrika rodoma be lango, ataskaita NELŪŽTA) · **BACKUP prieš
  keitimą** (push į privatų `hera-core-backup`) · HARD laiko biudžetas, **NO retry**.
- Tai **ataskaitos matomumo pataisa** — pačių metrikų skaičiavimo NEKEISK ir mirusio šaltinio netaisyk
  (3 punktas — tik diagnozė). Jokio naujo modulio, jokių naujų priklausomybių.
- Viešo `cad-site-agent` git'o neliesti.
- Savas `--selftest` (be pytest): sintetinis duomenų rinkinys su šviežiu ir su pasenusiu įrašu →
  pirmas be žymės, antras su `PASENĘ`; plius atvejis „0 įrašų" (neturi dalybos iš nulio ar crash'o).

## Sėkmės kriterijai (selftest)

1. Kita Loop B ataskaita prie cache-hit rodo `n=11, naujausias 2026-07-11` ir **PASENĘ** žymę.
2. Gyvos metrikos (skills / growth / wiki-lint) rodo savo langą BE žymės — t.y. vartas neduoda
   klaidingų pozityvų.
3. Selftest 3/3 (šviežias · pasenęs · tuščias).
4. Backup commit'as `hera-core-backup`.

**ATASKAITOS TAISYKLĖ:** teiginys „neįmanoma / nepavyko patikrinti" galioja **tik kartu su sąrašu, KĄ BANDEI.**
Negalimybė turi būti pagrįsta veiksmais, ne intuicija. Neapsimesk, kad patikrinai, jei tik pažiūrėjai.

**BACKUP TAISYKLĖ (nauja, nuo Fazės 52):** backup failų **NIEKADA netrinti** — nei valymo komandoje, nei
„jau nebereikalingas" pagrindu. Palikimas kainuoja 0; trynimui reikia atskiro human-gate. Galioja ir tavo
paties tą pačią sesiją sukurtiems `.bak` failams.
