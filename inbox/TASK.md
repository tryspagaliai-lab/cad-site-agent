UŽDUOTIS — HERA MODELIŲ TARYBA (council_decision, Fazė 7). Autonomiškai, atsargiai.
Statyk PILNĄ automatinę tarybą kad veiktų per API be rankinio klijavimo. Atsiskaityk į Telegram TRUMPAI.

*** ATNAUJINTA: OPENROUTER_API_KEY JAU ĮDĖTAS į /root/hera.env. ***
PIRMA PATIKRINK ar raktas veikia (GET https://openrouter.ai/api/v1/models su Authorization: Bearer <key>
iš env — grąžink tik HTTP statusą + kiek NEMOKAMŲ modelių rasta, NErodyk rakto). Jei 200 — tęsk su pilna
open-source taryba. Jei modulis hera_council.py jau pastatytas praeitą kartą — NEstatyk iš naujo, tik
PALEISK realų testą (4b) su pilna open-source sudėtimi ir raportuok kurie juror'iai realiai balsavo.
Jei rakto patikra nepavyko (401/403) — parašyk Telegram kad raktas negalioja, ir sustok.

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
   (ištrauktas turinys + selektoriaus balas/priežastis).
   PAGRINDINĖ TARYBA = OPEN-SOURCE MODELIAI (jų daug, nemokami, įvairūs). ChatGPT tik kraštutiniu atveju.
   Nariai (juror'iai):
   a) OPEN-SOURCE per OPENROUTER free (PAGRINDINIAI juror'iai) — jei /root/hera.env yra OPENROUTER_API_KEY:
      gauk modelių sąrašą (GET /models), filtruok NEMOKAMUS (`:free` / pricing=0), ir atrink ĮVAIRIŲ
      ŠEIMŲ 4-6 juror'ius (po vieną iš: Llama, Qwen, DeepSeek, GLM/z-ai, Kimi/Moonshot, Mistral —
      tai atitinka originalią tarybą GLM/Qwen/Kimi/MiMo). Kiekvienas balsuoja atskirai.
      Sąrašą laikyk konfigūruojamą env `HERA_COUNCIL_MODELS` (kableliais) su protingu default;
      jei kuris modelis nepasiekiamas — praleisk, imk kitą tos pačios/kitos šeimos.
   b) GEMINI free — pridėk 1-2 Gemini modelius kaip papildomus juror'ius (per esamą fallback sąrašą).
   c) OPENROUTER rakto NĖRA — praleisk open-source tyliai (be klaidos, "openrouter: skipped"),
      tada taryba veikia bent iš Gemini juror'ių + prašyk žmogaus pridėti raktą (raportuok Telegram).
   d) OPENAI/ChatGPT = MOKAMAS KRAŠTUTINIS TIE-BREAKER, NE kiekvienam kandidatui:
      kviesk TIK kai open-source juror'iai stipriai nesutaria IR balas arti promote ribos.
      Skaityk OPENAI_API_KEY iš env; jei nėra — praleisk tyliai. Default: taupyk, retai kviesk.
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
