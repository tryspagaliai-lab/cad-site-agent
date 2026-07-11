UŽDUOTIS — ĮPINTI NARŠYKLĘ Į HERA URL IŠTRAUKIMĄ (fallback kai trafilatura silpna). <12 min.
NEleisk viso pytest — tik taikinius. Telegram TRUMPAI. Fail-safe: naršyklės klaida NIEKADA nelaužo ingest.

SAUGUMAS: raktų nespausdink/necommit'ink. Jei liesta HERA kodą — push į PRIVATŲ hera-core-backup.

KONTEKSTAS: naršyklės pamatas paruoštas (/root/brvenv, Playwright+Chromium, /root/br_smoke.py veikia).
Dabar įpinam į HERA url ištraukimą — kai trafilatura grąžina mažai/tuščią (JS-sunkūs puslapiai, SPA), HERA
pabando naršykle.

1) MODULIS /opt/hera-processor/hera_browser.py: funkcija fetch_rendered(url, timeout=45) ->
   {title, text, ok} naudojant Playwright headless Chromium (args --no-sandbox, headless=True,
   PLAYWRIGHT_BROWSERS_PATH kaip pamate). Paima page.title() + matomą tekstą (body innerText, apvalyk tarpus).
   Jei brvenv Python skiriasi nuo hera venv — kviesk kaip subprocess (/root/brvenv/bin/python worker) su
   JSON stdout, NE import (kad priklausomybės nesikirstų). Griežtas per-call timeout, 1 retry.

2) ĮPYNIMAS į url ekstraktavimą (hera_extract ar kur trafilatura kviečiama): jei trafilatura rezultatas
   TRUMPAS/tuščias (pvz. <200 simb. arba tuščia) IR HERA_BROWSER=1 -> pabandyk fetch_rendered(url); jei duoda
   daugiau teksto — naudok jį; kitaip lik prie trafilatura. Kokybiškus trafilatura rezultatus NEKEISK
   (naršyklė tik fallback — brangesnė/lėtesnė).
   GRIEŽTAI fail-safe: naršyklės klaida/timeout -> log + tęsk su tuo ką turi (trafilatura ar tuščia),
   ingest NIEKADA nelūžta.

3) JUNGIKLIS: env HERA_BROWSER=1 įjungia fallback (default 1); =0 rollback be kodo. Įrašyk =1 /root/hera.env.

4) TESTAS: (a) fetch_rendered ant paprasto puslapio -> title+tekstas grįžta; (b) 1 JS-sunkaus/SPA url pavyzdys
   kur trafilatura duoda mažai -> parodyk, kad naršyklės fallback davė daugiau teksto (simbolių skaičius prieš/po);
   (c) fail-safe: blogas url -> ingest nesulūžta, grįžta tvarkingai.

5) DURABILUMAS: kopija į /opt/cad-site-agent/n8n/hera/ + push į PRIVATŲ hera-core-backup (secret-scan).
   Viešo repo NELIESK.

TELEGRAM (trumpai, be raktų): (1) hera_browser.py veikia (subprocess/import), (2) įpinta kaip fallback
(kada kviečiama), fail-safe, HERA_BROWSER=1, (3) testas — trafilatura vs naršyklė simbolių pavyzdys,
(4) backup OK, (5) „NARŠYKLĖ ĮPINTA Į HERA".
