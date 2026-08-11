# Fazė 59 — backoff ties TRUMPALAIKE Groq riba (ne ties paros kvota). +perleisti `z618ro`. <10 min.

## ⚠️ Apimtis griežta. Fazės 54 ir 56 krito `rc=124`. Ši turi VIENĄ tikslą + vieną trumpą veiksmą.

**Pamatęs kitą defektą — UŽRAŠYK ataskaitoje, NETAISYK.** Nespėji — **stok ir pranešk.**

## ⚠️ SĄMONINGA IŠIMTIS IŠ NEKINTANČIOS TAISYKLĖS — perskaityk atidžiai

HERA nekintanti taisyklė yra **„HARD timeout, NO retry"** (anti `rc=124`). Ši fazė daro **siaurą,
sąmoningą išimtį**, ir ji leidžiama TIK tokiomis sąlygomis:
· retry **TIK** ties trumpalaike (per-minutę) tiekėjo riba — 429 / `rate_limit` / `too many requests`
· **NIEKADA** ties paros kvota (`RESOURCE_EXHAUSTED`, „quota", „limit: N per day") — ten laukimas
  nepadeda, ir retry tik degina laiką iki `rc=124`
· **NIEKADA** ties bet kokia kita klaida (tinklas, 4xx, 5xx, blogas atsakymas) — ten elgesys nesikeičia
· griežtos lubos: **max 3 bandymai**, **bendras laukimas ≤ 20 s** viename kvietime
Jei negali patikimai atskirti trumpalaikės ribos nuo paros kvotos — **geriau NEDARYK retry**, o pranešk.
Klaidingas retry ties paros kvota yra blogiau nei jokio retry.

## Realybė (išmatuota šiandien, netikrink iš naujo)

Fazės 57 (`d87fe65`) ir 58 (`a4ab97b`) perkėlė **struktūrinimą** (`extractors/base.py`) ir
**atranką** (`hera_select.py`) ant Groq. Grandinė veikia: `sel 0` → `sel=9/10`, growth failai rašomi.

**Naujas gedimas, kurį tai sukūrė:** darbas `20260811T090630Z-z618ro` krito, nes **du Groq kvietimai
iš eilės** (struktūrinimas + atranka) pramušė Groq **trumpalaikę** ribą. Fail-safe atlaikė — švarus
no-op, ne crash — bet darbas liko be atrankos.
⇒ Tai **struktūriška, ne atsitiktinumas**: po 57+58 KIEKVIENAS darbas daro ≥2 Groq kvietimus paeiliui.
Kartosis kaskart, kai vartotojas mes kelis video iš eilės.

📌 **Skirtumas, kuris yra visos šios fazės esmė:**
· **Paros kvota** (Gemini 20/parą): laukimas NEPADEDA ⇒ sprendimas = kitas tiekėjas (jau padaryta).
· **Trumpalaikė riba** (Groq): atsistato per sekundes ⇒ sprendimas = **backoff**. Tai vienintelis atvejis,
  kur laukimas yra teisingas vaistas.

✅ Groq raktas gyvas. ✅ Titrų tiltas gyvas. ✅ `hera-processor` active.

## Tikslas

**1. Eksponentinis backoff ties trumpalaike Groq riba** — abiejuose keliuose:
`extractors/base.py` (struktūrinimas) ir `hera_select.py` (atranka).
Siūloma: 2 s → 4 s → 8 s, max 3 bandymai. Jei Groq atsakyme yra `Retry-After` arba nurodytas laukimo
laikas — **naudok jį**, jis tikslesnis už spėjimą (bet vis tiek ribok ≤ 20 s).
Jungiklis `HERA_GROQ_BACKOFF` — default **1**. Reikšmė 0 = elgesys tiksliai kaip dabar.
Išnaudojus bandymus — **dabartinis elgesys nesikeičia**: krentam į Gemini, paskui į no-op. Ne crash.

**2. Perleisk darbą `20260811T090630Z-z618ro`** — jis liko be atrankos. Parodyk rezultatą.

## Ko NEDARYTI (sąmoningai atidėta)

❌ **Tarybos (council) ir research kelio NELIESK** — jie tebėra Gemini kalėjime, tai atskira fazė.
❌ Neišiminėk `gemini-flash-latest` iš `DEFAULT_MODELS`.
❌ Nedaryk bendro „€0 tiekėjo maršrutizatoriaus".
❌ Neperbėginėk senų sustabarėjusių darbų — tik `z618ro`.
❌ Neliesk titrų tilto, ASR, digest'o, dispatcher'io kvotos varto.

## Apribojimai

€0 · **BACKUP prieš keitimą**, backup'ų **NIEKADA netrinti** · viešas `cad-site-agent` neliečiamas ·
**jokių raktų reikšmių** log'uose / ataskaitoje / commit'uose · ataskaita ir komentarai **lietuviškai,
kiekvienas angliškas terminas su vertimu skliaustuose.**

## Įrodymai (be jų fazė nelaikoma atlikta)

1. `--selftest` PASS, privalomai apimantis **abu klaidų tipus atskirai**:
   · trumpalaikė riba → **backoff įvyksta**, bandymų skaičius teisingas
   · **paros kvota → backoff NEĮVYKSTA**, krentam iškart (tai svarbiausias testas šioje fazėje)
   · `HERA_GROQ_BACKOFF=0` → elgesys kaip dabar
   · išnaudoti bandymai → **no-op, ne exception**
2. `z618ro` perleistas — parodyk `sel=N` ir ar parašytas growth failas.
3. Log'o eilutė, rodanti realų backoff (kiek laukta, kelintas bandymas).
4. `systemctl is-active hera-processor`.
5. `git -C /opt/hera-processor log --oneline -2` — commit'inta ir push'inta į privatų `hera-core-backup`.

## Ataskaita

Per HERA botą: kas pakeista (failai) · 5 įrodymai · **ką pastebėjai, bet SĄMONINGAI nelietei.**
Jei spėji tik 1 punktą pilnai su įrodymais — daryk jį, o `z618ro` palik kitai fazei ir pasakyk aiškiai.
