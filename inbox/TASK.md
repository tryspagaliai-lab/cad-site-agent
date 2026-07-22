UŽDUOTIS — READ-ONLY: hera_council.py €0 setup patikra (juror-set konfigas, NVIDIA kaina, entry point). NIEKO NEKEISK. <12 min.
NEleisk pytest. Fail-safe. €0. TIK skaitymas (+ 1 NVIDIA probe call) + reportas į HERA botą. Viešo cad-site-agent NELIESK. Secret'us → [REDACTED].
TIKSLAS: paruošti user-facing council sluoksnį (git-inbox „council: <klausimas>", async, → proposals/council/<id>.json + Telegram) —
plonas sluoksnis ant ESAMO hera_council.py, €0 juror-set (gemini+groq+glm, gal nvidia). ŠI užduotis TIK žvalgyba prieš statybą.

Failas: /opt/cad-site-agent/n8n/hera/hera_council.py (+ gretimi hera_env.py ir kt.).

1) JUROR-SET KONFIGAS:
   - Parodyk KUR ir KAIP apibrėžtas juror sąrašas (grep juror/JUROR/providers/MODELS/PANEL; parodyk tą kodo gabalą, be secret'ų).
   - Ar juror-subset paduodamas per ENV kintamąjį ar param (pvz. COUNCIL_JURORS=...), ar UŽHARDKODINTA į fan-out?
   - Ar galima apriboti iki TIK {gemini, groq, glm} NEREDAGUOJANT core kodo (env/param)? Jei taip — parodyk tikslų kintamąjį/formatą.
   return: juror_def_location, config_mechanism(env|param|hardcoded), can_subset_without_edit(taip/ne + kaip)

2) NVIDIA JUROR — €0 ar mokamas:
   - Rask NVIDIA juror endpoint/model hera_council.py (koks NIM modelis).
   - VIENAS minimalus probe (jei įmanoma be daug žetonų): pvz. `curl -sS -o /dev/null -w "%{http_code}" -X POST <nim_endpoint>
     -H "Authorization: Bearer $NVIDIA_API_KEY" -H "Content-Type: application/json" -d '{"model":"<modelis>","messages":[{"role":"user","content":"hi"}],"max_tokens":1}'`
     (raktą imk iš env, NErodyk). Kodas: 200=veikia(€0?), 402=mokamas, 401/403=auth, 404=modelis/endpoint.
   return: nvidia_model, nvidia_http_code, verdict(€0-imam | mokamas-metam | neaišku)

3) ENTRY POINT:
   - Ar hera_council.py priima ARBITRARY tekstinį klausimą, ar tik HERA proposal objektą? Parodyk entry point / main() / funkcijos parašą.
   - Ar yra CLI (`python hera_council.py "<klausimas>"`) ar tik importuojamas su proposal dict/objektu?
   - Jei tik proposal objektas → įvertink kaip LENGVA pridėti „ask mode" laisvam klausimui (koks minimalus wrapper).
   return: accepts_arbitrary_question(taip/ne), invocation(cli|import), ask_mode_effort(trivialu|vidutinis|reikia refaktoro + kodėl)

4) BONUS (jei greita): kur council rašo output (proposals/council/<id>.json formatas — laukai verdict/score/spread/std/per-juror?).
   return: output_path, output_schema_summary

ATASKAITA (HERA botas): užpildyk 1–4 return laukus trumpai + tikslūs kodo vietos (failas:eilutė). Jei kur nepavyko — pažymėk.
