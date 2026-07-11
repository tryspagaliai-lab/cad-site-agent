UŽDUOTIS — HERA NARŠYKLĖS PAMATAS: headless Chromium+Playwright VPS'e (TIK diegimas+testas, be įpynimo). <13 min.
NEleisk pytest. Telegram TRUMPAI. SVARBU: griežtas laikas — jei diegimas užtrunka, atsiskaityk KĄ spėjai, neužstrik.

SAUGUMAS: raktų nespausdink/necommit'ink.

KONTEKSTAS: HERA gaus savo naršyklę — kad galėtų atsidaryti/naršyti/ištraukti JS-sunkius puslapius + žingsnis
link „sistema daro darbus". ŠITA užduotis TIK pamatas (diegimas+smoke test). Įpynimą į HERA darysim atskirai.

1) IZOLIUOTAS venv /root/brvenv (python3 -m venv); pip install playwright. Tada:
   - `playwright install-deps chromium` (apt sistemos priklausomybės; root — OK) IR `playwright install chromium`
     (parsisiunčia Chromium). Jei parsisiuntimas per lėtas/timeout rizika — bandyk system chromium
     (apt-get install -y chromium-browser ARBA chromium) ir Playwright su executablePath. Pasirink kas greičiau
     suveikia; aprašyk ką panaudojai.
2) SMOKE TEST skriptas /root/br_smoke.py: headless paleisk Chromium, atidaryk https://example.com,
   paimk page.title() ir pirmus ~200 simb. teksto, atspausdink. Paleisk jį — turi parodyti „Example Domain".
   (Aplinka: PLAYWRIGHT_BROWSERS_PATH jei reikia; headless=True; be sandbox jei root: args=['--no-sandbox'].)
3) FAIL-SAFE laikui: jei per limitą nespėji visko — įdiek kiek spėji, paleisk ką turi, ir ataskaitoje AIŠKIAI
   parašyk kas veikia / kas liko (pvz. „venv+playwright OK, chromium parsisiuntimas nespėjo"). NEUŽSTRIK iki 15min.
4) DURABILUMAS: br_smoke.py kopija į /opt/cad-site-agent/n8n/ lokaliai (be push į viešą). HERA kodo neliesk
   (tik naujas venv+skriptas), tad hera-core-backup push nereikia.

TELEGRAM (trumpai, be raktų): (1) chromium įdiegtas (parsisiųstas ar system), (2) smoke test rezultatas
(page.title veikia? „Example Domain"?), (3) kas liko jei nespėta, (4) „NARŠYKLĖS PAMATAS PARUOŠTAS" arba
„DALINAI — <kas liko>".
