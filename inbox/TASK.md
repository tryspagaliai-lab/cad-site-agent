UŽDUOTIS — Fazė 40: PHONE/ISO pataisa → projekcijos perkūrimas → ATSKIRAS pėdsakų semsearch indeksas. HUMAN-GATE GAUTAS („daryk kaip rekomenduoji"). <14 min.

**Eiliškumas privalomas: 1 → 2 → 3.** Indeksuoti korpusą su sudarkytomis datomis būtų beprasmiška, todėl
pataisa eina PIRMA, o indeksas — PASKUTINIS. Jei laikas baigiasi, geriau padaryti 1+2 gerai ir sustoti prie 3,
nei visus tris paskubomis. Dalis 4 (anotacija) — maža, daryk kada patogu.

## 1) PHONE klaidingai pozityvių pataisa (Fazės 39 pasiūlymas, dabar patvirtintas)
Fazė 39 rado: PHONE kategorija 9/9 suveikimų = **9/9 klaidingai pozityvūs**. 7/9 — ISO datos
(`scrub("2026-07-29")` → `[PHONE_1]`), 1 — arXiv ID šablonas (`NNNN.NNNNN`), 1 — skaičius+data.
Tikrų telefono numerių — nė vieno. Pėdsakuose datos yra **vertingas turinys** (chronologija = dalis pėdsako
vertės mokymui), tad jų šveitimas kenkia be jokios saugumo naudos.

Padaryk **minimalų saugų susiaurinimą** — tu sprendi tikslią formą, bet:
- ISO data (tiksliai `\d{4}-\d{2}-\d{2}`) NETURI būti laikoma telefonu.
- arXiv ID formos (`\d{4}\.\d{4,5}`) taip pat — įvertink, ar verta įtraukti; jei nusprendi neįtraukti, pasakyk kodėl.
- **Tikrų telefonų aptikimas privalo IŠLIKTI** — pridėk į `test_pii.py` bent po vieną testą kiekvienai naujai
  išimčiai IR bent vieną, patvirtinantį, kad realus telefono numeris VIS DAR pagaunamas. Regresija čia = saugumo skylė.
- `test_pii.py` turi likti PASS visas (buvo 24/24).

## 2) Projekcijos perkūrimas
Esama projekcija turi `[PHONE_1]` vietoj datų — perkurk ją visiems `raw/` pėdsakams per tą patį `capture()`
kelią (Fazė 39 paliko `/root/hera_reproject_phase39.py` pakartotiniam naudojimui). Po perkūrimo pranešk
naują redagavimo tankį ir PHONE suveikimų skaičių (turėtų kristi ~į 0).

## 3) ⭐ ATSKIRAS pėdsakų semsearch indeksas
**Sprendimas: ATSKIRAS indeksas, NE bendras su vault.** Trys priežastys (kad suprastum ribas, ne kad kartotum):
pėdsakai yra **operaciniai žurnalai, ne žinios** → bendrame indekse jie triukšmintų normalią paiešką ·
eilėje laukia `semsearch v1.2 eval`, o naujo korpuso įmaišymas dabar būtų **nekontroliuojamas kintamasis**
(matuotume korpusą, o manytume, kad matuojam versiją) · atskirą indeksą galima išjungti vienu jungikliu.

- Šaltinis: `projection/rag_corpus.jsonl` (NIEKADA `raw/` — tas neredaguotas ir neindeksuojamas niekada).
- **Pagrindinis vault indeksas turi likti BITAI TAS PATS.** Prieš ir po — užfiksuok įrodymą (dokumentų skaičius
  ir failo dydis/mtime arba hash). Jei pastebėsi, kad jį palietei — tai avarija, sustok ir pranešk.
- **Užklausa veikia iš karto per CLI** (kad būtų realiai naudojama ir patikrinama dabar).
- **Automatinis įpurškimas į runner/agento kontekstą — NE.** Tai atskiras jungiklis, **def 0**, atskiras
  human-gate ateityje. Priežastis: automatinis įpurškimas teršia kontekstą ir kainuoja; rankinė užklausa — ne.
- **Sveikatos patikra (sanity check):** paimk atpažįstamą frazę iš vieno pėdsako, paleisk užklausą, patikrink
  ar TAS pėdsakas grįžta pirmas. Pranešk rezultatą sąžiningai.
- ⚠️ **Lūkesčių kalibravimas:** korpusas dabar **6 įrašai**. Prie tokio dydžio paieškos kokybė beveik nieko
  nereiškia. Netrauk išvadų apie naudingumą — tik patvirtink, kad grandinė VEIKIA. Vertinsim, kai bus ~50+.

## 4) crypto-Claude kuravimo anotacija
Note'ui apie **„Discovering cryptographic weaknesses with Claude"** (Simon Willison, 2026-07-28,
`...-i495fo.md`) pridėk `## KURAVIMO VERDIKTAS (žmogus, 2026-07-30)` tuo pačiu formatu kaip CaRE (prieš `---`):
· **Kriptoanalizė mums neaktuali — vertė kitur: pasidalintos užklausos.** Pagrindinė žmogaus intervencija buvo
  **neleisti modeliui pasiduoti** („models tend to think it is impossible to solve so they don't try";
  „we are not looking for low hanging fruit").
· **NAUJA gedimo klasė: PRIEŠLAIKINĖ KAPITULIACIJA**, kurios `hera_goalanchor` NEMATO. Drift = nuklysta nuo
  tikslo. Kapituliacija = paskelbia „neįmanoma" ir grąžina įtikinamą nesėkmę, atrodančią kaip teisėtas atlikimas.
  **Mūsų pačių instrukcija tai kursto:** „jei neįmanoma — pasakyk, nespėliok" (teisinga dėl faktų) kartu sukuria
  mažiausio pasipriešinimo kelią. Precedentas: Fazė 36 enumeruodama rado 2 rakto vietas, Fazė 37 skenuodama — 3.
  **KONVENCIJA: „neįmanoma" galioja tik su „ką bandžiau" sąrašu.**
· **Kaštų kalibravimas:** 60 val., **~$100k** API kaštų (šaltinio įvertis) vienam publikuoti vertam rezultatui
  BE praktinio poveikio. Atsvara pagundai tikėtis, kad €0 taryba „atras" kažką nauja — **taryba skirta ŽINOMŲ
  dalykų trianguliacijai, ne atradimams.**
· **Trečia nepriklausoma konvergencija dėl autonomijos suvaldymo** (PlanFlip → Import AI 466/OpenAI → šis):
  kuo pajėgesnis modelis ir ilgesnė autonomija, tuo labiau randa ir išnaudoja aplinkos silpnybes, kai vertinamas
  balu. Išvada: **nekeičiam nieko** (advisory-first · def 0 · human-gate · no retry · fail-closed vartams).
· ⚠️ Žymės: „Claude Mythos / Mythos Preview" — nepatikrinamas, mums neprieinamas modelis, imam kaip šaltinio
  teiginį. $100k — įvertis. Tai **antrinis šaltinis** (link blogas apie Anthropic įrašą), citatos antros rankos.
`state/*.json` `council.final_action` **NELIESK** (Fazės 37 precedentas).

## Apribojimai
€0 · BACKUP prieš `hera_pii.py` ir bet kokį konfigo keitimą · `/opt/hera-venv/bin/python3` semsearch daliai ·
viešo `cad-site-agent` git NELIESK · push į privatų `hera-core-backup` · HARD timeout, be retry ·
jokių secret reikšmių ataskaitoje.

**⚠️ NAUJA ATASKAITOS TAISYKLĖ (nuo šiol visoms fazėms):** teiginys „neįmanoma / nepavyko patikrinti" galioja
**tik kartu su sąrašu, KĄ BANDEI.** Negalimybė turi būti pagrįsta veiksmais, ne intuicija. „Nespėliok" lieka
galioti; prisideda „ir neapsimesk, kad patikrinai, jei tik pažiūrėjai". *(Fazė 39 parodė teisingą pavyzdį:
neturėdama duomenų, ji perskaitė regex šaltinį ir davė struktūrinį įrodymą — stipresnį už empirinį mėginį.)*

Jei STOP — kodėl.
