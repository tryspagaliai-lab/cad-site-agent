# Fazė 58 — selektorius ant Groq. `sel 0` turi virsti realiu skaičiumi. <10 min.

## ⚠️ Apimtis griežta. Fazės 54 ir 56 krito `rc=124`, nes turėjo po kelis darbus. Ši turi VIENĄ.

**Daryk TIK selektorių. Pamatęs kitą defektą — UŽRAŠYK ataskaitoje, NETAISYK.**
Nespėji — **stok ir pranešk, NEKARTOK.**

## Realybė (išmatuota šiandien, netikrink iš naujo)

Šio projekto Gemini raktui **abu modeliai = 20 užklausų per parą** (tikras 429, ne dokumentacija).
Fazė 57 (`d87fe65`) tai jau apėjo **struktūrinimo** kelyje: Groq pagrindinis, Gemini atsarginis,
jungiklis `HERA_STRUCT_PRIMARY`, `dispatcher._has_struct_fallback()` atrakina `quota_skip` vartą.
Selftest 9/9, trys darbai baigti, Groq struktūrino.

**Bet problema tik persikėlė.** Tavo pirmtakas pats užfiksavo: taryba / **selektorius** / research
**nenaudoja `structure_text` kelio**, todėl liko Gemini kalėjime — log'e `selektoriaus klaida`,
`research: kvietimas krito`, o ingest ataskaitose **`sel 0`**.
⇒ Pasekmė matoma Loop B: **`+0 skills · +0 growth` per parą.** Tekstą gaunam ir struktūrizuojam,
bet **žinių iš jo neišsitraukiam** — medžiaga sustoja ties `stage_for_review`.

✅ Groq raktas gyvas (`GROQ_API_KEY` iš `/root/hera.env`, patikrinta `groq_http=200`).
✅ Titrų tiltas gyvas.

## Tikslas — VIENAS

**Perkelk SELEKTORIŲ ant Groq tuo pačiu šablonu, kurį Fazė 57 jau įrodė veikiantį.**
Nesugalvok naujo dizaino — **pakartok `extractors/base.py` sprendimą**: Groq pirmas, Gemini atsarginis,
jungiklis (siūlomas vardas `HERA_SEL_PRIMARY`, default **`groq`**, reikšmė `gemini` = sena tvarka),
fail-safe (abu krito → dabartinis elgesys, **ne crash**).

⚠️ **Panaudok jau egzistuojantį kodą, neperrašinėk:** `extractors/base.py` turi
`_groq_structure_fallback()`, `_is_quota_error()` ir **Cloudflare WAF apėjimą per `User-Agent`**
(`GROQ_STRUCT_HEADERS`) — be to apėjimo Groq grąžina `403 error code: 1010`. Jei prasminga —
iškelk bendrą pagalbinį, bet **tik jei tai NEPAREIKALAUS liesti kitų failų daugiau nei būtina.**
Abejoji — geriau pakartok lokaliai, negu daryk platų refaktoringą.

## Ko NEDARYTI (sąmoningai atidėta kitoms fazėms)

❌ **Tarybos (council) NELIESK.** ❌ **Research kelio NELIESK.**
❌ Neišiminėk `gemini-flash-latest` iš `DEFAULT_MODELS`.
❌ Nedaryk bendro „€0 tiekėjo maršrutizatoriaus" — tai suplanuota, bet NE dabar.
❌ Neliesk titrų tilto, ASR, digest'o, `hera_hygiene`, dispatcher'io kvotos varto (jau sutvarkytas).

## Apribojimai

€0 · **BACKUP prieš keitimą**, backup'ų **NIEKADA netrinti** · viešas `cad-site-agent` git-tvarkiškai
neliečiamas · **jokių raktų reikšmių** log'uose / ataskaitoje / commit'uose — tik vardai, ilgiai, http kodai ·
ataskaita ir kodo komentarai **lietuviškai, kiekvienas angliškas terminas su vertimu skliaustuose.**

## Įrodymai (be jų fazė nelaikoma atlikta)

1. `--selftest` PASS: Groq kviečiamas pirmas · `HERA_SEL_PRIMARY=gemini` grąžina seną tvarką ·
   Groq krito → Gemini bandomas · **abu krito → no-op, ne exception**.
2. **Realus ingest darbas, kuriame `sel` NEBE 0** — parodyk ataskaitos eilutę ir kiek atrinkta.
   Jei po perkėlimo `sel` vis tiek 0, bet **be klaidos** — tai irgi galiojantis rezultatas,
   tik aiškiai pasakyk: „selektorius veikė, tiesiog nieko neatrinko", ir parodyk log'ą.
3. Log'o eilutė, rodanti **kuris tiekėjas atrinko**.
4. `systemctl is-active hera-processor`.
5. `git -C /opt/hera-processor log --oneline -2` — commit'inta ir **push'inta į privatų
   `hera-core-backup`** (nurodyk commit).

## Ataskaita

Per HERA botą: kas pakeista (failai) · 5 įrodymai · **ką pastebėjai, bet SĄMONINGAI nelietei.**
