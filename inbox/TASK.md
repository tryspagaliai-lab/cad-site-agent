# Fazė 55 — titrus imam iš laptopo per Tailscale (VPS IP blokuotas YouTube pusėje). <14 min.

## Kodėl — įrodyta eksperimentu 2026-08-11, netikrink iš naujo

**VPS IP YouTube pusėje blokuotas.** `yt-dlp` (2026.07.04, įdiegtas `/usr/local/bin/yt-dlp`) iš VPS grąžina:
`ERROR: [youtube] Sign in to confirm you're not a bot.`
Tas pats blokas paaiškina VISUS ankstesnius gedimus vienu ypu: Piped 502/ConnectionError, Invidious
„titrų turinys tuščias (IP blokas)", transcript-api, ir kritimą į Gemini.

**Tas pats `yt-dlp` iš laptopo namų IP tą patį video paima be jokių kliūčių:**
`{"ok": true, "lang": "en", "chars": 11584}` per sekundės dalį, 0 Gemini kvietimų.

**Tiltas jau pastatytas ir pasiekiamas iš VPS** (patikrinta `curl` iš `agentos-1`):
```
GET http://100.68.100.14:8790/health      -> {"ok": true, "service": "hera-transcript-bridge"}
GET http://100.68.100.14:8790/transcript?url=<YouTube nuoroda>
    -> {"ok": true, "lang": "en", "chars": 11584, "text": "..."}   (sėkmė)
    -> {"ok": false, "error": "titru nerasta"}                      (nepavyko)
```
Tailscale gyvas abiejose mašinose: VPS `100.103.24.122`, laptopas `100.68.100.14`.

## Tikslas

**1. Įstatyti tiltą kaip PIRMĄJĮ titrų šaltinį** — prieš yt-dlp-iš-VPS, prieš Piped/Invidious, prieš Gemini.
Sėkmės atveju grandinė nutrūksta iškart ir Gemini titrams **nekviečiamas iš viso**.

**2. Fail-safe (privaloma):** jei tiltas nepasiekiamas (laptopas išjungtas, tinklo nėra, timeout) —
**tyliai kristi į esamą grandinę**, lygiai kaip dabar. Laptopo nebuvimas negali lūžinti pipeline'o.
Timeout tiltui: **180 s** (yt-dlp gali užtrukti), po jo — tolesni šaltiniai.

**3. Jungiklis `HERA_TRANSCRIPT_BRIDGE` — čia SĄMONINGA IŠIMTIS iš „default 0" konvencijos: default **1**.**
Priežastis: dabartinis kelias veikia **0%**, tad def 0 reikštų palikti sistemą sugedusią. Rizika nulinė,
nes gedimo atveju elgesys grįžta į dabartinį. Adresą imti iš aplinkos `HERA_BRIDGE_URL`
(numatytoji `http://100.68.100.14:8790`), kad nebūtų įrašytas kietai.

**4. Jei dar nepadaryta Fazėje 54 — kvotos klaidų atskyrimas.** `429`/`RESOURCE_EXHAUSTED` yra **paros**
limitas (`limit: 20, model: gemini-3.6-flash`), tad kartoti tą pačią parą beprasmiška. Vienas nepavykęs video
sugeneruoja ~54 Gemini kvietimus (3 keliai × 6 bandymai × 3 kartojimai) — **trigubai daugiau nei paros riba.**

## Apribojimai (nekintami)

- €0 · fail-safe · **BACKUP prieš keitimą** (į privatų `hera-core-backup`) · HARD laiko biudžetas · NO retry.
- Tiltas pasiekiamas **tik per Tailscale** — jokių viešų adresų, jokių naujų atvirų portų VPS'e.
- `hera-processor` dabar **sustabdytas ranka**. Baigęs — paleisk atgal ir patikrink, kad startuoja švariai.
- Nekurk naujo HTTP kliento, jei kode jau yra — naudok esamą.

## Sėkmės kriterijai (selftest)

1. Realus YouTube video apdorotas nuo galo iki galo, titrai gauti **iš tilto** — parodyk žurnalo eilutę
   su simbolių skaičiumi ir įrodyk, kad **Gemini titrams nekviestas nė karto**.
2. Tiltas išjungtas (arba `HERA_BRIDGE_URL` nurodo į negyvą adresą) → pipeline **nelūžta**, tyliai pereina
   prie senos grandinės. Parodyk žurnalu.
3. `hera-processor` veikia (`systemctl is-active` = active), žurnale nėra klaidų audros.
4. Backup commit'as `hera-core-backup`.

**ATASKAITOS TAISYKLĖ:** teiginys „neįmanoma / nepavyko patikrinti" galioja **tik kartu su sąrašu, KĄ BANDEI.**
Negalimybė turi būti pagrįsta veiksmais, ne intuicija. Neapsimesk, kad patikrinai, jei tik pažiūrėjai.

**BACKUP TAISYKLĖ:** backup failų NIEKADA netrinti.

**KALBOS TAISYKLĖ:** ataskaitoje kiekvienas angliškas terminas privalo turėti lietuvišką vertimą skliaustuose.
