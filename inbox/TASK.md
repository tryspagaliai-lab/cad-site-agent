# Fazė 57 — Groq tampa PAGRINDINIU struktūrintoju. Trys eilėje kabantys darbai turi baigtis ŠIANDIEN. <10 min.

## ⚠️ SKAITYK PIRMA: dvi fazės iš eilės krito `rc=124`. Ši sąmoningai maža.

**Griežta apimtis: TIK tai, kas žemiau. Jokių papildomų patobulinimų, jokio refaktoringo,
jokio „pakeliui pataisiau". Pamatęs kitą defektą — UŽRAŠYK ataskaitoje, NETAISYK.**
Nespėji — **stok ir pranešk, NEKARTOK** (anti rc=124).

## Realybė (išmatuota, netikrink iš naujo)

Tavo pirmtakas Fazėje 56 gavo tikrą 429 ir teisingai užfiksavo kode:
**šio projekto raktui `gemini-2.5-flash` riba irgi = 20 užklausų per parą, ne 250.**
⇒ Planavimo prielaida buvo klaidinga. **Gemini negali būti struktūrintojas** — 20/parą tai 3–4 video.

**Fazė 56 paliko darbą NEUŽBAIGTĄ ir NEĮRAŠYTĄ:**
· `extractors/base.py` — `_groq_structure_fallback()` ir `_is_quota_error()` **parašyti ir geri**
  (fail-safe, Cloudflare WAF apėjimas per `User-Agent`). **NEPERRAŠINĖK jų — panaudok.**
· ❌ Neaišku, ar jie apskritai kviečiami iš `structure_text()`.
· ❌ `git -C /opt/hera-processor log` rodo tik Fazę 55 — **Fazės 56 pakeitimai NECOMMIT'INTI.**
  Jie guli darbiniame medyje. **NEIŠMESK jų** — commit'ink kartu su savo darbu.
· ✅ Groq raktas gyvas (`groq_http=200`). ✅ Titrų tiltas iš VPS `{"ok": true}`.

**Blokatorius, dėl kurio vartotojo darbai kabo ~4 val.:** `dispatcher.py:486` praleidžia darbus su
žinute „Gemini dienos kvota išsemta (bandysiu kitą parą)". Servisas perkrautas 12:12:01, o darbai
praleisti po **8 ms** ⇒ žymė išlieka tarp perkrovimų (ne tik `gemini.LAST_QUOTA_EXHAUSTED` globalas).
**Kol ji galioja, Groq nebus iškviestas net prijungtas — darbai neprieina iki struktūrinimo.**

## Tikslas — TIK ŠIE TRYS DALYKAI

**1. Apversk pirmumą `structure_text()`: Groq PIRMAS, Gemini ATSARGINIS.**
Jungiklis `HERA_STRUCT_PRIMARY` — default **`groq`**; reikšmė `gemini` grąžina seną tvarką.
Fail-safe nesikeičia: Groq krito → Gemini → abu krito → dabartinis elgesys (ne crash).

**2. Sutvarkyk kvotos vartus `dispatcher.py`:** darbas **NEBEPRALEIDŽIAMAS**, kai struktūrinimas
turi neišsemtą kelią. Gemini kvota nebėra pakankama priežastis atidėti darbą iki kitos paros,
nes Gemini nebėra pagrindinis kelias. Kaip tiksliai — spręsk pats, bet elgesys privalo būti:
**yra Groq → darbas vykdomas dabar.**

**3. Paleisk tris kabančius darbus ir įsitikink, kad jie BAIGIASI:**
`20260811T080700Z-h32yf2` · `20260811T090630Z-z618ro` · `20260811T110030Z-olvxdw`

## Ko NEDARYTI šioje fazėje (sąmoningai atidėta)

❌ Neišiminėk `gemini-flash-latest` iš `DEFAULT_MODELS` — atskira fazė.
❌ Nekeisk titrų tilto, ASR, tarybos, digest'o, `hera_hygiene`, nieko kito.
❌ Nerašyk naujų testų failų daugiau nei reikia 1 punktui. `test_struct_groq_fallback.py` jau yra — panaudok.

## Apribojimai

€0 · **BACKUP prieš keitimą**, backup'ų **NIEKADA netrinti** · viešas `cad-site-agent` git-tvarkiškai
neliečiamas · **jokių raktų reikšmių** log'uose/ataskaitoje/commit'uose — tik vardai, ilgiai, http kodai ·
ataskaita ir komentarai **lietuviškai, kiekvienas angliškas terminas su vertimu skliaustuose.**

## Įrodymai (be jų fazė nelaikoma atlikta)

1. `--selftest` PASS: Groq kviečiamas pirmas · `HERA_STRUCT_PRIMARY=gemini` grąžina seną tvarką ·
   Groq krito → Gemini bandomas · abu krito → **no-op, ne exception**.
2. **Trijų darbų ID būsena** — parodyk, kad jie nebe „praleidžiu", o baigti (arba nurodyk tikslią kliūtį).
3. Log'o eilutė iš realaus darbo, rodanti **kuris tiekėjas struktūrino** ir kiek simbolių išėjo.
4. `systemctl is-active hera-processor`.
5. **`git -C /opt/hera-processor log --oneline -2`** — Fazės 56+57 pakeitimai commit'inti ir
   **push'inti į privatų `hera-core-backup`** (nurodyk commit).

## Ataskaita

Per HERA botą: kas pakeista (failai) · 5 įrodymai · **ką pastebėjai, bet SĄMONINGAI nelietei.**
Jei spėji tik 1+3 punktus — daryk juos pilnai su įrodymais, o 2 palik kitai fazei ir pasakyk tai aiškiai.
