UŽDUOTIS — TARYBA: (A) AKTYVUOK prod'e + (B) PARUOŠK NVIDIA NIM tiekėją. Atsargiai, autonomiškai.
Taryba (hera_council.py) veikia (26/26 unit, Groq 5/5 pagavo NVIDIA off-domain). NEperstatyk branduolio.
Atsiskaityk į Telegram TRUMPAI, BE raktų.

SAUGUMAS: raktų reikšmių NIEKADA nespausdink, necommit'ink, nerodyk Telegram/chate. Tik pavadinimai/prefiksai/statusai.

A) AKTYVAVIMAS PROD'e (vartotojo sprendimas: taryba KIEKVIENAM įrašui):
   - Įrašyk `HERA_COUNCIL=1` į /root/hera.env (jei dar nėra), chmod 600.
   - Įsitikink kad hera-processor mato šį kintamąjį (per EnvironmentFile drop-in, kurį jau pridėjai) ->
     `systemctl daemon-reload` (jei reikia) + `systemctl restart hera-processor`; patikrink `systemctl is-active`.
   - Patvirtink kad dispatcher.augment_verdict dabar REALIAI kviečia tarybą įkeliamam turiniui
     (ne tik teste). Rezultatas VISADA lieka human_gate=True, staged į proposals/council/ — JOKIO auto-promote.
   - APSAUGA nuo limitų: kadangi taryba eina kiekvienam įrašui, įsitikink kad prie 429/klaidų ji fail-safe
     krenta į mažiau balsų (min 2 galioja; <2 -> stage_for_review), NIEKADA neblokuoja ir nemeta ingest'o.

B) NVIDIA NIM TIEKĖJAS (paruošk KODĄ; raktas gali dar nebūti — tada tyliai skip):
   - Naujas juror tiekėjas per NVIDIA NIM (OpenAI-suderinamas): POST https://integrate.api.nvidia.com/v1/chat/completions,
     Authorization: Bearer <NVIDIA_API_KEY> (skaityk iš os.environ / /root/hera.env self-load).
   - GET https://integrate.api.nvidia.com/v1/models -> atrink ĮVAIRIŲ ŠEIMŲ juror'ius, prioritetas tiems,
     kurių Groq NETURI: DeepSeek, GLM/zai, Kimi/Moonshot, Qwen (case-insensitive paieška sąraše).
     Konfigūruojama env `HERA_NVIDIA_MODELS` (kableliais) su protingu default; jei modelis dingęs — imk kitą.
   - Tas pats struktūrizuotas prompt'as / JSON verdiktas {verdict, score, domain_fit, reason}, tvirtas parse,
     retry/backoff (429/5xx + Retry-After), stagger. NVIDIA global limitas ~40 RPM — nedaryk lygiagrečiai per daug.
   - Jei NVIDIA_API_KEY NĖRA — praleisk tyliai ("nvidia: no key"), taryba veikia iš Groq+Gemini.

C) PRIORITETAS (atnaujintas): Groq (Llama/Qwen/GPT-OSS) + NVIDIA NIM (DeepSeek/GLM/Kimi/Qwen) = PAGRINDINIAI
   open-source juror'iai; Gemini free = papildomi (1-2); OpenRouter = tik jei <3 balsai; OpenAI = kraštutinis
   tie-breaker. Tikslas 5-6 galiojantys balsai iš įvairių šeimų.

D) PATIKRA + TESTAS:
   - Env patikra: GROQ/NVIDIA/OPENROUTER/OPENAI (taip/ne + prefiksas, NE reikšmė).
   - Jei NVIDIA raktas YRA: GET /models -> kiek radai, ir ar sąraše yra DeepSeek/GLM/Kimi/Qwen (įvardink).
   - RE-RUN NVIDIA off-domain testas su pilna sudėtim; raporte KURIE nariai balsavo (vardai+score/verdict),
     council_score, domain_fit, final_action, ar tie-breaker kviestas. Protokolas -> proposals/council/.
   - Unit: NVIDIA juror parse + atranka (fabrikuoti atsakymai). Visi testai turi PRAEITI.

E) DURABILUMAS: pakeistą kodą kopijuok į /opt/cad-site-agent/n8n/hera/. Push NEDARYK.

TELEGRAM (trumpai, be raktų): (1) TARYBA prod'e AKTYVI? (HERA_COUNCIL=1, servisas active), (2) NVIDIA raktas
yra/nėra; jei yra — kiek modelių + ar DeepSeek/GLM/Kimi rasti, (3) testo verdiktas + kurie nariai balsavo su balais,
(4) aiškiai „TARYBA AKTYVI (Groq+Gemini)" ir „NVIDIA PARUOŠTA/LAUKIA RAKTO".
