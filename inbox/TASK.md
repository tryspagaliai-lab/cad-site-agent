UŽDUOTIS — SKUBU: pataisyk ai_digest.py kad pristatytų VISUS naujus įrašus (ne 3 iš 11). <12 min.
NEleisk pytest. Fail-safe. €0. Raktų nespausdink. Ataskaita TIK į HERA botą. Maršruto NEKEISK (@tryspagaliabot).
ANTI-RC124: Telegram send su HARD timeout (≤15s/žinutė), JOKIO begalinio retry.

PROBLEMA: log rodo „11 naujų išsiųsta", bet vartotojas gauna TIK 3. Reikia: kad ATEITŲ VISI nauji, nepriekaištingai.

1) DIAGNOZĖ (be keitimo pirma): perskaityk ai_digest.py siuntimo+formatavimo funkciją. Nustatyk KODĖL 11→3:
   - (a) Telegram 4096 simbolių riba — viena ilga žinutė nukertama? (log skaičiuoja PRIEŠ nukirpimą), ARBA
   - (b) Gemini santrauka kondensuoja 11 į kelis „highlight'us"?
   Parašyk ataskaitoje TIKSLIĄ priežastį + eilutę.

2) FIX (pagal priežastį — tikslas: VISI nauji įrašai pasiekia vartotoją):
   - Jei (a) TRUNCATION: skaidyk digestą į KELIAS žinutes, kiekviena ≤ ~3800 simbolių (saugi riba < 4096); siųsk
     nuosekliai su mažu delay (pvz. 0.5s) tarp žinučių. Kiekvienas naujas įrašas TURI patekti (nė vienas neprarastas).
     Naudok Telegram parse saugiai (jei HTML/Markdown — escape'ink, kad nelūžtų). Fallback: jei žinutė vis tiek per
     ilga — skaidyk toliau, niekada nemesk įrašų.
   - Jei (b) GEMINI KONDENSUOJA: pakeisk kad siųstų PILNĄ naujų įrašų sąrašą (kiekvienas: antraštė + šaltinis + URL),
     Gemini santrauka LIEKA tik kaip trumpa antraštė VIRŠUJE (neprivaloma), bet po jos — visi įrašai.
   - Bendra: „0 naujų → nieko naujo" elgesys lieka. seen.jsonl logika NEKEISK.

3) VERIFIKACIJA (be spam'o):
   - DETERMINISTINIS dry-run: paimk paskutinio run 11 naujų (arba iš seen/istorijos), suformuok žinutes NAUJU būdu,
     parodyk: kiek žinučių, ir kad VISI 11 įrašų telpa (nė vienas neprarastas). Įrašyk skaičius.
   - VIENAS TEST-SEND į @tryspagaliabot: nusiųsk tuos paskutinius įrašus nauju formatu, PIRMOJE žinutėje pažymėk
     „🧪 TESTAS — pilno pristatymo patikra (senų run įrašai)". Kad vartotojas IŠKART pamatytų, jog dabar ateina VISI.
     (Tai vienkartinis testas, ne dubliuoja gyvo seen — nekeisk seen dėl testo.)

4) BACKUP: commit ai_digest.py į hera-core-backup. Persistent askpass yra. Push nepavyko → NEkartok begalos, pranešk.

RIBOS: €0. Maršrutas nekeičiamas (@tryspagaliabot, TELEGRAM_TOKEN). Jokio pytest-all. Anti-rc124 (HARD timeout siuntimui).
NElisk kitų šaltinių/feed'ų šioje užduotyje — TIK pristatymo fix. Praplėtimas bus atskirai po deep-research.

ATASKAITA (HERA botas, trumpai): (a) TIKSLI priežastis (truncation/Gemini + eilutė); (b) kas pataisyta (skaidymas/
pilnas sąrašas); (c) dry-run: kiek žinučių, visi 11 telpa? (d) test-send į @tryspagaliabot OK (kiek žinučių atėjo)?
(e) backup push OK/ne; (f) 1 eil. kas toliau.
