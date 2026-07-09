UŽDUOTIS — HERA MODELIŲ TARYBA (council_decision, Fazė 7). Autonomiškai, atsargiai.
Statyk PILNĄ automatinę tarybą kad veiktų per API be rankinio klijavimo. Atsiskaityk į Telegram TRUMPAI.

KONTEKSTAS (valdymo hierarchija — LAIKYK):
- HERA Gemini selektorius = greitas PIRMAS filtras (klysta: NVIDIA straipsniui davė 8.0, realiai off-domain).
- TARYBA = tvirtas "antras vartas": keli modeliai kartu IŠGRYNINA + PATVIRTINA ar verta sistemai.
- Rezultatas VISADA lieka draft/staged (proposals/), NIEKADA auto-promote į gamybą. Žmogus tvirtina.
- Įvairovė > vienas modelis. Nesutarimas tarp modelių = signalas žmogui peržiūrėti.

SAUGUMAS (privaloma):
- Raktus SKAITYK TIK iš /root/hera.env per os.environ. NIEKADA nespausdink, necommit'ink, nerodyk chate/Telegram.
- Pirma sutvarkyk /root/hera.env: pašalink pasenusią placeholder eilutę `OPENAI_API_KEY=sk-TAVO_RAKTAS`
  (palik TIK tikrą raktą; jei dubliuota — dedup, chmod 600). Neišvesk rakto reikšmės niekur.

1) TARYBOS BRANDUOLYS — naujas modulis hera_council.py (/opt/hera-processor/):
   Funkcija council_decision(candidate) -> verdiktas. Kandidatas = HERA selektoriaus output
   (ištrauktas turinys + selektoriaus balas/priežastis). Nariai (juror'iai) — kas NEMOKAMA/pasiekiama DABAR:
   a) GEMINI free — panaudok fallback SĄRAŠĄ kaip ATSKIRUS juror'ius įvairovei
      (pvz. gemini-flash-latest, gemini-2.5-flash, gemini-2.0-flash) — kiekvienas balsuoja atskirai.
   b) OPENROUTER free — jei /root/hera.env yra OPENROUTER_API_KEY, pridėk 1-2 nemokamus modelius
      (pvz. tuos su ":free" sufiksu). Jei rakto NĖRA — praleisk tyliai (be klaidos), pažymėk "openrouter: skipped".
   c) OPENAI/ChatGPT = MOKAMAS TIE-BREAKER, NE kiekvienam kandidatui:
      kviesk TIK kai (i) free juror'iai nesutaria (verdiktų dispersija didelė) ARBA
      (ii) balas aukštas (arti promote ribos) — t.y. brangus balsas tik kai realiai lemia sprendimą.
      Skaityk OPENAI_API_KEY iš env; jei nėra — praleisk tyliai.
   Kiekvienas juror gauna TĄ PATĮ struktūrizuotą prompt'ą: grąžink JSON {verdict: keep/drop/revise,
   score: 0-10, domain_fit: 0-10, reason: "..."}. Parse tvirtai (fallback jei modelis grąžina ne JSON).

2) AGREGACIJA: surink visų juror'ių balsus -> council verdiktas:
   - median score + verdict balsų dauguma; pažymėk disagreement (std/skirtumą).
   - final_action: promote_candidate / stage_for_review / drop — bet VISADA tik SIŪLYMAS.
   - Įrašyk pilną tarybos protokolą (kas ką balsavo + priežastys) į vault: proposals/council/<job_id>.json.
   - Integruok su selektoriumi: council verdiktas AUGINA/PERRAŠO vieno-Gemini balą (bet žmogaus gate lieka).
     NEliesk esamos selektoriaus logikos destruktyviai — pridėk sluoksnį virš jo (jei council pasiekiamas).

3) ATSPARUMAS: naudok esamą Gemini fallback (jei model-fallback task jau atliktas — remkis juo;
   jei ne — bent retry/backoff + rollink per modelius). Bet kuris juror gali kristi (503/timeout) —
   taryba turi veikti su likusiais (min 2 balsai = galioja; <2 = "nepakanka balsų, į review").

4) TESTAS:
   (a) unit — sufabrikuoti juror balsai (sutarimas / nesutarimas / vienas krito) -> teisingas agregatas + tie-breaker trigeris.
   (b) realus — paleisk council_decision ant EGZISTUOJANČIO vault kandidato (pvz. NVIDIA straipsnis, kurį Gemini pervertino).
      Parodyk: ar taryba pagavo off-domain klaidą (žemesnis domain_fit nei vieno Gemini 8.0)? Kiek juror'ių balsavo, kuris tie-breaker'is (jei buvo).

5) DURABILUMAS: kodą kopijuok į /opt/cad-site-agent/n8n/hera/. Push NEDARYK.

ATSISKAITYMAS į Telegram (TRUMPAI, be raktų): tarybos nariai kurie balsavo, testo rezultatas
(ar pagavo NVIDIA off-domain), kur protokolas saugomas, ir aiškiai „TARYBA BAIGTA". NErodyk jokių rakto reikšmių.
