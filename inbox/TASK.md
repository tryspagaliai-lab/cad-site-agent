# Fazė 54 — ingest'as atgal į gyvenimą: yt-dlp titrų kelias + modelio pinas + pakartojimų stabdis. <14 min.

## Diagnozė JAU ATLIKTA (2026-08-11) — nekartok tikrinimo, naudok

Parser'is nemiręs — jis dirba ir nuolat krenta. Trys sluoksniai vienu metu:

1. **Visi YouTube titrų veidrodžiai negyvi.** `hera-processor` žurnalas: Piped (`pipedapi.reallyaweso.me` HTTP 502,
   `api.piped.yt` ConnectionError), Invidious (`inv.nadeko.net` → „titrų turinys tuščias (IP blokas)",
   `iv.melmac.space` SSLError, `invidious.nerdvpn.de` + `yewtu.be` JSONDecodeError, `invidious.jing.rocks`
   ConnectionError). Tai visos ekosistemos problema, ne mūsų.
2. **Gemini kvota išdegusi.** Tikslus atsakas: `RESOURCE_EXHAUSTED`,
   `GenerateRequestsPerDayPerProjectPerModel-FreeTier`, **limit: 20 per parą**, `model: gemini-3.6-flash`.
   🔴 **Priežastis gili: `gemini-flash-latest` dabar rodo į `gemini-3.6-flash`.** Kodo niekas nekeitė —
   Google perkėlė pseudonimą į modelį su daug griežtesne nemokama riba. Raktas GALIOJA (patikrinta: modelių
   sąrašas HTTP 200, atspaudas `341f87b9`).
3. **Pakartojimų audra.** `journalctl -u hera-processor --since "1 hour ago" | grep -c "try 1/6"` = **65**.
   65 bandymai per valandą × iki 6 kvietimų = paros kvota išdega per minutes po atsistatymo. **Kasdien.**
4. **`yt-dlp` VPS'e NEĮDIEGTAS** (`command -v yt-dlp` tuščias). Rugpjūčio 9 d. klaidos pranešime jo nėra
   šaltinių sąraše — **šio kelio pipeline niekada neturėjo.**

## Tikslas — trys taisymai, prioriteto tvarka

**1. `yt-dlp` kaip PIRMINIS titrų šaltinis (svarbiausia).**
`yt-dlp` ima titrus tiesiai iš YouTube, be jokių veidrodžių ir be Gemini
(`--write-auto-sub --write-sub --sub-langs` + `--skip-download`). Įdiegti (pip --user arba statinis binaras į
`/usr/local/bin`) ir įstatyti **prieš** Piped/Invidious grandinę. Veidrodžių NEŠALINK — palik kaip atsarginius.

**2. Modelio pinas — atsisakyti `-latest` pseudonimų kvotai jautriuose keliuose.**
Pakeisti `gemini-flash-latest` → **`gemini-2.5-flash`** (jo nemokama paros riba gerokai didesnė nei 20).
🔴 **Principas, kurį įtvirtinam: „latest" pseudonimas reiškia, kad tiekėjas gali bet kada pakeisti modelį
IR jo kvotą po mūsų kojomis.** Kvotai jautriuose keliuose pinam konkrečią versiją.
⚠️ Žinomas senas apribojimas: `gemini-2.5-flash` JSON buvo nukertamas dėl vidinio „thinking" —
todėl kartu **pakelti `maxOutputTokens` iki 2048** (tai jau buvo išbandyta ephemeral, bet niekada neįtvirtinta kode).

**3. Pakartojimų stabdis.** Užduotis, kuri krito dėl kvotos (`429`/`RESOURCE_EXHAUSTED`), **NETURI būti
kartojama tą pačią parą** — tai ne laikina klaida, o dienos limitas. Įgyvendinti atskyrimą:
laikina klaida (tinklas, 502, timeout) → normalus pakartojimas · **kvotos klaida → atidėti iki kitos paros.**
Naudok esamą `.attempts` / `PermanentSkip` mechanizmą, nekurk naujo.

## Apribojimai (nekintami)

- €0 · fail-safe (klaida → dabartinis elgesys, ne lūžis) · **BACKUP prieš kiekvieną keitimą** (į privatų
  `hera-core-backup`) · HARD laiko biudžetas · **NO retry** anti-rc124 prasme.
- `yt-dlp` diegimas be `sudo apt` jei įmanoma (pip --user arba binaras) — VPS'e root yra, bet mažiau paketų = geriau.
- Jei laiko trūksta: **1 ir 3 punktai svarbiausi.** 2 punktas be jų neišgelbės — kvotą vis tiek suės ciklas.
- `hera-processor` šiuo metu **sustabdytas ranka** (kad nedegintų kvotos). Baigęs darbą — paleisk jį atgal
  ir patikrink, kad startuoja švariai.

## Sėkmės kriterijai (selftest, be pytest)

1. `yt-dlp` prieinamas ir grąžina titrus bent vienam realiam YouTube video — parodyk simbolių skaičių.
2. Pipeline'as tą patį video apdoroja **nekviesdamas Gemini titrams** — įrodyk žurnalo eilutėmis.
3. Kode nebėra `gemini-flash-latest`; yra `gemini-2.5-flash` su `maxOutputTokens=2048`.
4. Kvotos klaida (`429`) nebeveda į tuoj pat kartojamą bandymą — parodyk logikos vietą arba sausą testą.
5. `hera-processor` paleistas atgal, `systemctl is-active` = active, žurnale nėra klaidų audros.
6. Backup commit'as `hera-core-backup`.

**ATASKAITOS TAISYKLĖ:** teiginys „neįmanoma / nepavyko patikrinti" galioja **tik kartu su sąrašu, KĄ BANDEI.**
Negalimybė turi būti pagrįsta veiksmais, ne intuicija. Neapsimesk, kad patikrinai, jei tik pažiūrėjai.

**BACKUP TAISYKLĖ:** backup failų **NIEKADA netrinti** — nei valymo komandoje, nei „jau nebereikalingas" pagrindu.

**KALBOS TAISYKLĖ:** ataskaitoje kiekvienas angliškas terminas privalo turėti lietuvišką vertimą skliaustuose.
