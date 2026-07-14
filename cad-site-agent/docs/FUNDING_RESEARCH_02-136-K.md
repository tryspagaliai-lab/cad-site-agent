# Tyrimo ataskaita: kvietimas Nr. 02-136-K ir jo dermė su `cad-site-agent` sistema

- **Data:** 2026-07-14
- **Kvietimas:** „Finansinės paskatos startuoliams ir atžalinėms įmonėms kurti DI, blokų grandinės technologijų, robotikos procesų automatizavimo produktus ir sprendimus" (kvietimo puslapis su galūne `-1` esinvesticijos.lt — naujausias, 2026 m. kvietimas)
- **Pastaba dėl šaltinių:** esinvesticijos.lt iš šios darbo aplinkos tiesiogiai nepasiekiamas (tinklo politika), todėl faktai surinkti iš viešų antrinių šaltinių (CPVA, EIMIN, konsultantų apžvalgos). Prieš teikiant paraišką sąlygas BŪTINA pasitikrinti pačiame kvietime ir PFSA (projektų finansavimo sąlygų apraše).

---

## 1. Kvietimo santrauka

| Parametras | Reikšmė |
|---|---|
| Kvietimo Nr. | **02-136-K** |
| Administratorius | **CPVA** (Centrinė projektų valdymo agentūra) |
| Paraiškų priėmimas | **2026-06-09 → 2026-07-31 15:45** |
| Bendra kvietimo suma | **3 000 000 €** |
| Maks. suma projektui | **100 000 €** |
| Finansavimo intensyvumas | **iki 90 %** tinkamų išlaidų (likusius ~10 % — nuosavos lėšos) |
| Pagalbos schema | de minimis |
| Regionas | **Sostinės regionas (Vilniaus apskritis)** — pareiškėjas paraiškos pateikimo metu turi būti registruotas Sostinės regione ir nebūti persiregistravęs iš Vidurio ir vakarų Lietuvos regiono po 2026-05-01 |

### Kas gali teikti paraišką

- **Startuoliai ir atžalinės (spin-off) įmonės**, registruotos **ne anksčiau kaip prieš 5 metus** iki paraiškos pateikimo.
- Statusas: **labai maža, maža arba vidutinė įmonė (MVĮ)** pagal SVV įstatymą.
- Įmonė kuria arba ketina kurti **DI, blokų grandinės technologijų (BGT) arba robotikos procesų automatizavimo (RPA)** produktus/sprendimus.
- ⚠️ Vienoje EIMIN naujienos versijoje minimas ir veiklos trukmės kriterijus (skirtingi šaltiniai nesutampa) — **patikrinti PFSA**, ar reikalaujama minimali veiklos trukmė / pajamos.

### Finansuojamos veiklos (stadijos)

- **1 stadija** — preliminariai minimaliai gyvybingo produkto (prototipo) sukūrimas: DI / BGT / RPA produkto ar sprendimo **prototipas** (~TPL 2–4).
- **2 stadija** — **rinkai pateikti tinkamos produkto versijos** sukūrimas (MVP → market-ready).

### Tinkamos išlaidos (pagal viešas apžvalgas)

- **Darbo užmokestis** darbuotojams, kuriantiems DI/BGT/RPA produktą (programuotojai ir kt.) + susiję mokesčiai;
- **Debesijos infrastruktūros nuoma** ir **programinės įrangos licencijos**, tiesiogiai susijusios su produkto kūrimu;
- **Konsultacinės ir joms prilygintos paslaugos** produkto kūrimui — **iki 25 %** visų tinkamų išlaidų.

### Prioritetiniai atrankos kriterijai

1. **Nuosavas indėlis** — kuo didesnė privačių lėšų dalis, tuo daugiau balų.
2. **Patirtis** — ar įmonė jau yra įgyvendinusi DI / RPA / BGT sprendimą(-us).

### Remiamos DI sritys

Mašininis mokymasis, **kompiuterinė rega**, natūralios kalbos apdorojimas, **skaitmeniniai dvyniai**, išmanioji robotika.

---

## 2. Kas yra `cad-site-agent` (vertinimo kontekstas)

- Python CLI vamzdynas, automatizuojantis **CAD (DXF/DWG) sklypų planų valymą ir semantinį struktūrizavimą** ArchViz / 3D vizualizacijos (3ds Max, Blender) darbų srautui: analizė → brėžinio tipo klasifikacija → geometrijos valymas/tarpelių uždarymas → sluoksnių normalizavimas pagal taksonomiją (~43 klasės, ~55 stabilūs sluoksniai) → uždarų regionų radimas + pasikliautinumo balai → HATCH generavimas → ne-regioninių elementų maršrutizavimas.
- Aplink branduolį — **4 MCP serveriai** (pipeline, palydovinės nuotraukos, Inkscape/GIMP grafikos automatizavimas, headless Blender render) ir **n8n LLM agento** darbo srautas.
- Branda: **veikiantis v1 prototipas** — ~218 unit testų, pyproject pakuotė, Docker, realūs klientų tipo brėžiniai (Roman Gardens, ST-23-01S, H7149); be CI, be klientų, be įregistruotos įmonės (individualus/lab lygmuo).
- Svarbu: **dabartinis branduolys — deterministinės taisyklės ir geometrija (be ML/LLM)**. DI dalis šiuo metu yra: (a) suplanuotas Ollama+ChromaDB semantinis sluoksnių klasifikatorius (Phase 4 AI enhancement, dar neįgyvendintas), (b) LLM agentų orkestravimo sluoksnis aplink kūrimą/valdymą (Claude/Gemini/Kimi/MiMo, HERA vizija).

---

## 3. Dermės vertinimas

### 3.1 Teminis atitikimas

| Kvietimo sritis | Atitikimas | Komentaras |
|---|---|---|
| **Procesų automatizavimas (RPA)** | ✅ **Stiprus** | Sistemos esmė — rankinį CAD valymo darbą pakeičiantis automatizuotas, konfigūruojamas, testuotas vamzdynas + MCP/n8n automatizacijos. Tai tikras, veikiantis „procesų automatizavimo produktas". |
| **Dirbtinis intelektas (DI)** | 🟡 **Dalinis, bet plėtojamas** | Šiandien branduolys — taisyklės, ne ML. Tačiau projekto planas tiesiogiai atitinka remiamas DI sritis: ML sluoksnių klasifikacija (embeddings), kompiuterinė rega brėžiniams, LLM agentai. CAD planas → 3D scena konceptualiai artimas ir „skaitmeninių dvynių" sričiai. **DI paraiškai reikėtų DI komponentus paversti projekto šerdimi, ne priedu.** |
| **Blokų grandinės (BGT)** | ❌ Nėra | Jokių komponentų; nesiūlytina dirbtinai pritempti. |
| **Robotika (fizinė)** | ❌ Nėra | Tik programinė automatizacija. |

Kvietimui pakanka atitikti **vieną** iš sričių — realiausia pozicija: **„DI + procesų automatizavimo produktas CAD/ArchViz rinkai"** (pvz., „AI įrankis, automatiškai paverčiantis netvarkingus sklypo planus struktūruota, vizualizacijai paruošta 3D scena").

### 3.2 Projekto stadijų atitikimas

- Faktinė būsena gerai atitinka kvietimo logiką: **v1 prototipas jau yra** (1 stadijos rezultatas), o finansavimas leistų įgyvendinti **2 stadiją** — rinkai tinkamą versiją (SaaS/produkto pakuotė, ML klasifikatorius, SVG/PNG/GeoJSON ir MAX-prep eksportai, UI, CI/CD, dokumentacija, pilotiniai klientai ArchViz studijose).
- Prioritetinis kriterijus „jau įgyvendinęs DI/RPA/BGT sprendimą" — veikiantis pipeline su realiais brėžiniais yra argumentas balams.

### 3.3 Formalūs trūkumai (kritiniai)

| # | Trūkumas | Poveikis | Ką daryti |
|---|---|---|---|
| 1 | **Nėra juridinio asmens** — projektas vystomas asmeniškai (gmail, „lab" GitHub org) | Paraiškos be įmonės pateikti neįmanoma | Registruoti MB/UAB. Nauja įmonė formaliai tenkina „ne anksčiau kaip prieš 5 m." kriterijų, BET patikrinti PFSA, ar nėra min. veiklos trukmės/pajamų reikalavimų |
| 2 | **Registracija Sostinės regione** (Vilniaus apskritis) | Jei įmonė būtų registruota kitur — netinkama šiam kvietimui | Registruoti Vilniaus apskrityje (jei tai atitinka realią veiklos vietą) |
| 3 | **Terminas: 2026-07-31 15:45** — liko ~2,5 savaitės | Labai maža laiko rezervo paraiškai + įmonės steigimui | Nedelsiant apsispręsti; jei nespėjama — sekti kitus kvietimus (žr. 5 sk.) |
| 4 | **Nuosavas indėlis ≥10 %** + balai už didesnį | Reikia realaus finansinio pajėgumo (iki ~10 t. € prie 100 t. € projekto, daugiau — dėl balų) | Suplanuoti nuosavų lėšų dalį |
| 5 | **DI turinys paraiškoje turi būti pagrįstas** — dabartinis kodas taisyklinis | Vertintojai gali kvestionuoti „DI produkto" statusą | Projekto plane DI (ML klasifikatorius, CV, agentai) apibrėžti kaip kuriamą produkto funkcionalumą su aiškiais rezultatais |

### 3.4 Ko kvietimas NEfinansuotų / rizikos

- Vien esamos taisyklinės sistemos palaikymas be naujo DI/RPA produkto kūrimo.
- Verslo brandos stoka (nėra pajamų, klientų, komandos) mažina atrankos balus, ypač konkuruojant dėl 3 mln. € voko (30 projektų po 100 t. € maks.).
- De minimis limitas (250 t. € per 3 m.) — naujai įmonei problema nebūtų.

---

## 4. Rekomenduojama projekto koncepcija (jei teikiama)

**Produktas:** „CAD Site Agent" — DI grįstas SaaS/įrankis, automatiškai paverčiantis nestandartizuotus sklypų planus (DWG/DXF) semantiškai struktūruota, 3D vizualizacijai ir skaitmeniniams dvyniams paruošta geometrija.

**Projekto (2 stadijos) darbai, tinkami finansuoti:**
1. **ML sluoksnių/objektų klasifikatorius** (embeddings + vektorinė paieška vietoje raktažodžių taisyklių) — jau suplanuota architektūroje;
2. **Kompiuterinės regos modulis** brėžinių elementams/simboliams atpažinti (remiamos DI sritys: CV);
3. **LLM agentų orkestravimas** peržiūrai reikalingų regionų (`review`) sprendimams;
4. Produktizacija: web UI, API, CI/CD, saugumas, dokumentacija;
5. Pilotai su 2–3 ArchViz/architektūros studijomis.

**Išlaidos:** 1–2 kūrėjų DU (didžioji dalis), debesijos/GPU nuoma, licencijos, iki 25 % konsultacijoms (pvz., ML ekspertizė, produkto dizainas).

---

## 5. Alternatyvos, jei nespėjama iki 2026-07-31

- **„Startuolis" (Inovacijų agentūra / 02-025-K tipo kvietimai)** — startuolių akceleravimas ir vystymas; skelbti 2026 m. mokymai pareiškėjams.
- **Analogiškas kvietimas Vidurio ir vakarų Lietuvos regionui** — EIMIN skelbė 10 mln. € kvietimą DI sprendimus kuriantiems regionų verslams (jei įmonė būtų registruota ne Vilniuje).
- **MVĮ skaitmeninimo čekiai** (priemonė 05-001-01-05-05 „Skatinti įmones skaitmenizuotis") — mažesnės apimties, paprastesnės paraiškos.
- **LMT „Atžalinių įmonių MTEP projektai"** — jei kada būtų sąsaja su mokslo institucija (licencinė sutartis) — iki 100 % intensyvumas MTEP.

---

## 6. Išvada

**Teminė dermė — gera** (procesų automatizavimas ✅, DI 🟡 su aiškia plėtros kryptimi; BGT/robotika — neaktualu, bet ir nebūtina). **Projekto logika — beveik ideali**: yra veikiantis prototipas (1 stadija), o kvietimas finansuoja būtent tai, ko trūksta — 2 stadiją (rinkai tinkama versija su tikru DI funkcionalumu), 90 % intensyvumu iki 100 t. €.

**Pagrindinė kliūtis — ne technologija, o formalumai ir laikas:** nėra juridinio asmens, reikalinga registracija Sostinės regione, o paraiškų terminas — **2026-07-31 15:45 (liko ~17 d.)**. Jei įmonės steigimas + paraiška per tiek laiko nerealu, racionaliau taikytis į kitą šio kvietimo ratą ar alternatyvias priemones ir per tą laiką sustiprinti pozicijas (įmonė, ML komponento PoC, 1–2 pilotiniai vartotojai).

## Šaltiniai

- [Kvietimas esinvesticijos.lt (naujausias, `-1`)](https://esinvesticijos.lt/kvietimai/finansines-paskatos-startuoliams-ir-atzalinems-imonems-kurti-di-bloku-grandines-technologiju-robotikos-procesu-automatizavimo-produktus-ir-sprendimus-1)
- [EIMIN: Finansavimas Vilniaus regiono startuoliams](https://eimin.lrv.lt/lt/ziniasklaidai/naujienos/finansavimas-vilniaus-regiono-startuoliams)
- [15min: Finansavimas Vilniaus regiono startuoliams](https://www.15min.lt/verslas/naujiena/finansai/finansavimas-vilniaus-regiono-startuoliams-662-2103470)
- [Probaltic: Parama startuoliams DI, blokų grandinės ir robotizacijos sprendimams kurti](https://probaltic.lt/lt/parama-startuoliams-di-bloku-grandines-ir-robotizacijos-sprendimams-kurti/)
- [Europosparama.lt: kvietimo apžvalga](https://europosparama.lt/finansines-paskatos-startuoliams-ir-atzalinems-imonems-kurti-di-bloku-grandines-technologiju-robotikos-procesu-automatizavimo-produktus-ir-sprendimus/)
- [Sintesi: Finansinės paskatos startuoliams (Sostinės regionas)](https://www.sintesi.lt/finansines-paskatos-startuoliams/)
- [CPVA: nuotoliniai mokymai pareiškėjams](https://cpva.lt/renginiai/nuotoliniai-mokymai-finansines-paskatos-startuoliams-ir-atzalinems-imonems-kurti-di-bloku-grandines-technologiju-robotikos-procesu-automatizavimo-produktus-ir-sprendimus)
- [eskvietimai.blog: ankstesnio (2023) kvietimo sąlygos](https://www.eskvietimai.blog/2023/06/27/finansines-paskatos-startuoliams-ir-atzalinems-imonems-kurti-di-bloku-grandines-technologiju-robotikos-procesu-automatizavimo-produktus-ir-sprendimus-privatus-sektorius/)
- [EIMIN: DI finansavimo iniciatyvos](https://eimin.lrv.lt/lt/veiklos-sritys/skaitmenine-politika/dirbtinis-intelektas/finansavimas/)
