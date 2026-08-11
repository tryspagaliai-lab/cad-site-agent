# Fazė 56 — nuimti struktūrinimo dienos lubas: pinas į `gemini-2.5-flash` + Groq atsarginis. <13 min.

## Kontekstas — jau padaryta, netikrink iš naujo

Fazė 55 uždarė **titrų** gavimą: tiltas iš laptopo per Tailscale veikia, `[tiltas] OK lang=en 15676 sim.`,
Gemini titrams nebekviečiamas. **Liko VIENINTELĖS lubos: `structure_text()` vis dar kviečia Gemini.**

Fazė 54 turėjo tą piną padaryti, bet **krito `rc=124` (timeout)** — jai buvo užduota per daug darbų viename
cikle. Ši užduotis sąmoningai maža, kad tilptų.

**Kvotų faktas (išmatuotas 2026-08-11, ne prielaida):** `gemini-flash-latest` pseudonimas tiekėjo pusėje
persuktas į `gemini-3.6-flash`, kurio nemokama riba = **20 užklausų PER PARĄ**
(`GenerateRequestsPerDayPerProjectPerModel-FreeTier`). `gemini-2.5-flash` riba = **250 per parą**.
Tas pats raktas, tas pats €0 lygis, **12,5× daugiau**.

⚠️ **Vartotojas turi Gemini Pro prenumeratą (iki lapkričio), bet NEDARYK prielaidos, kad ji kelia API kvotą** —
vartotojiška prenumerata ir API apmokestinimas Google'e atskiri. Nieko dėl jos nekeisk.

## Tikslas

**1. Pinas.** Struktūrinimo kelyje (`structure_text()` ir kur dar naudojamas tas pats pseudonimas)
`gemini-flash-latest` → **`gemini-2.5-flash`**.
⚠️ Žinomas šio modelio elgesys, jau užfiksuotas: jis nukerta JSON dėl vidinio „thinking" — todėl
**kartu privalo eiti `maxOutputTokens=2048`** (be jo pinas pablogins, ne pagerins). `thinkingBudget=0`
**deprecated — NENAUDOTI**, jis laužė enrichment.

**2. Groq kaip atsarginis struktūrintojas.** Raktas `GROQ_API_KEY` jau yra `/root/hera.env`.
Groq → **tik kai Gemini grąžina kvotos klaidą (429 / RESOURCE_EXHAUSTED)**, ne visada.
Tvarka: Gemini → (kvotos klaida) → Groq → (ir Groq krito) → esamas elgesys, kaip dabar.
Naujas jungiklis **`HERA_STRUCT_GROQ_FALLBACK` — default 1**. Pagrindimas nukrypimui nuo „default 0":
tai nėra naujas elgesys sistemoje, o atsarginis kelias, kuris įsijungia TIK ten, kur dabar yra
garantuotas gedimas (kvota išsemta). Išjungus jungiklį elgesys grįžta bit-į-bitą į dabartinį.

**3. Tilto patikra ataskaitoje.** `curl -s --max-time 10 http://100.68.100.14:8790/health` iš VPS.
Rezultatą (OK / negyvas) įrašyk į ataskaitą. **Jei negyvas — NIEKO netaisyk ir nedispatch'ink**,
tai laptopo pusė, tik pranešk. Fazės sėkmė nuo to nepriklauso.

## Apribojimai

- **€0.** Jokio mokamo modelio, jokio naujo tiekėjo, jokio naujo rakto.
- **BACKUP prieš keitimą** (`.bak` toje pačioje vietoje). **Backup'ų NETRINTI niekada** — nei valymo
  komandoje, nei „nebereikalingas" pagrindu.
- **Fail-safe:** bet kuri klaida naujame kelyje → grįžtam į dabartinį elgesį, ne crash.
- Viešas `cad-site-agent` git-tvarkiškai **neliečiamas**. **Jokių raktų reikšmių** log'uose, ataskaitoje
  ar commit'uose — tik vardai ir ilgiai.
- Ataskaita ir kodo komentarai **lietuviškai; kiekvienas angliškas terminas su vertimu skliaustuose.**

## Įrodymai (be jų fazė nelaikoma atlikta)

1. `--selftest` naujam/pakeistam keliui **PASS** (be pytest). Privalo apimti:
   · Gemini grąžina 429 → **iškviečiamas Groq** · Groq grąžina rezultatą → jis grąžinamas toliau
   · `HERA_STRUCT_GROQ_FALLBACK=0` → Groq **NEkviečiamas**, elgesys kaip dabar
   · Groq irgi krito → **no-op, ne exception**
2. `grep -rn "gemini-flash-latest"` struktūrinimo kelyje → **0 atitikmenų** (arba paaiškink kiekvieną likusį).
3. Vienas **realus** struktūrinimo darbas su tikrais titrais — parodyk, kuris modelis atsakė ir kiek simbolių.
4. `systemctl is-active hera-processor` po pakeitimo.
5. Tilto `/health` rezultatas.
6. Backup'as padarytas ir **push'intas į privatų `hera-core-backup`** (nurodyk commit).

## Ataskaita

Per HERA botą. Formatas: kas pakeista (failai) · 6 įrodymai aukščiau · kas NEPADARYTA ir kodėl.
Jei nespėji — **geriau padaryk tik dalį 1 (piną) pilnai su įrodymais**, negu abi dalis pusiau.
Dalis 2 tada lieka kitai fazei. **Anti-rc124: nespėjus — stok ir pranešk, NEKARTOK.**
