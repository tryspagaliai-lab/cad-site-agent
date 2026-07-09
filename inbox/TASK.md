UŽDUOTIS — TARYBA: ĮJUNGTI OPEN-SOURCE JUROR'IUS (OpenRouter raktas neįsiskaitė). Atsargiai, autonomiškai.
Taryba (hera_council.py) jau pastatyta ir veikia (14/14 unit, pagavo NVIDIA off-domain). NEstatyk iš naujo.
PROBLEMA: praeitas paleidimas rašė "OpenRouter nėra rakto → skip", NORS OPENROUTER_API_KEY jau įdėtas į
/root/hera.env. Vadinasi raktas nepasiekia os.environ. Tavo darbas — kad įsiskaitytų ir open-source nariai
(MiMo, Nex-N2 Pro, GLM, Qwen, Kimi ir kt.) REALIAI balsuotų. Atsiskaityk į Telegram TRUMPAI, BE raktų.

SAUGUMAS: raktų reikšmių NIEKADA nespausdink, necommit'ink, nerodyk Telegram/chate. Tik pavadinimai/statusai.

1) DIAGNOZĖ — kodėl OPENROUTER_API_KEY nepasiekia kodo:
   - Patikrink ar /root/hera.env REALIAI turi eilutę `OPENROUTER_API_KEY=...` (tikslus pavadinimas, be tarpų,
     be BOM). Parodyk TIK: ar eilutė yra (taip/ne) ir rakto ILGIS bei prefiksas (pvz "sk-or-...", pirmi 6 simb.),
     NErodyk viso rakto.
   - Nustatyk kaip hera-processor gauna aplinką: ar systemd servisas turi `EnvironmentFile=/root/hera.env`?
     (`systemctl cat hera-processor.service`). Ar `hera_env.py` / loader'is įkelia /root/hera.env, ar tik
     /root/ai_digest.env? Testas praeitą kartą irgi neturėjo rakto — vadinasi loaderis jo neįkelia.

2) PATAISA (padaryk ABU, kad būtų tvirta):
   a) KODE: hera_council.py (ir bendras loaderis, jei yra hera_env.py) — jei env kintamojo NĖRA os.environ,
      pats perskaityk /root/hera.env (paprastas KEY=VALUE parse, ignoruok #komentarus/tuščias) ir įkelk
      trūkstamus raktus į os.environ. Taip council veikia nepriklausomai nuo systemd aplinkos.
   b) SYSTEMD: jei hera-processor.service neturi `EnvironmentFile=/root/hera.env` — pridėk (drop-in
      /etc/systemd/system/hera-processor.service.d/env.conf su [Service] EnvironmentFile=-/root/hera.env),
      `systemctl daemon-reload` + `systemctl restart hera-processor`. Jei jau turi — palik.

3) PATIKRA OpenRouter: su įkeltu raktu GET https://openrouter.ai/api/v1/models
   -> grąžink HTTP statusą + kiek NEMOKAMŲ (`:free`/pricing=0) modelių. Modelių sąraše paieškok ir raporte
   pažymėk ar RANDA (case-insensitive): MiMo ("mimo"/"xiaomi"), Nex-N2 Pro ("nex"/"n2 pro"/"nex-n2"),
   GLM ("glm"/"z-ai"), Qwen, Kimi ("kimi"/"moonshot"), DeepSeek. Kurių nėra — įvardink aiškiai.

4) RE-RUN TARYBOS TESTAS (4b) ant TO PATIES NVIDIA kandidato, dabar su PILNA sudėtim:
   Gemini juror'iai + OpenRouter open-source juror'iai (privalomai bandyk MiMo ir Nex-N2 Pro).
   Raporte: KURIE juror'iai realiai balsavo (vardai + jų score/verdict), council_score, final_action,
   ar tie-breaker (OpenAI) buvo kviestas. Protokolas -> proposals/council/<job>.json.
   Jei koks privalomas narys (MiMo/Nex-N2 Pro) OpenRouter'yje neegzistuoja — aiškiai parašyk ir pasiūlyk kelią.

5) DURABILUMAS: pakeistą kodą kopijuok į /opt/cad-site-agent/n8n/hera/. Push NEDARYK.

TELEGRAM (trumpai, be raktų): (1) ar raktas dabar įsiskaito (taip/ne + prefiksas), (2) kiek free modelių OpenRouter,
(3) kurie tarybos nariai REALIAI balsavo (ypač MiMo, Nex-N2 Pro, Kimi — yra/nėra), (4) NVIDIA testo verdiktas,
(5) aiškiai „OPEN-SOURCE TARYBA VEIKIA" arba kas dar trūksta.
