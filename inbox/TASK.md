UŽDUOTIS — TARYBA: PRIJUNK VISUS PRIDĖTUS TIEKĖJUS + PATIKRINK KIEKVIENĄ RAKTĄ. Atsargiai, autonomiškai.
Taryba (hera_council.py) veikia (26/26 unit, aktyvi prod'e HERA_COUNCIL=1). NEperstatyk branduolio — PLĖSK.
Vartotojas pridėjo kelis native API raktus į /root/hera.env. Tavo darbas: aptikti kurie yra, prijungti kiekvieną
kaip nepriklausomą juror'į, GYVAI patikrinti ar veikia, ir perleisti tarybos testą su pilna sudėtim.
Atsiskaityk į Telegram TRUMPAI, BE raktų.

SAUGUMAS: raktų reikšmių NIEKADA nespausdink, necommit'ink, nerodyk Telegram/chate. Tik pavadinimai/prefiksai/statusai.

0) ENV APTIKIMAS: iš /root/hera.env (per hera_env self-load) nustatyk kurie raktai YRA. Rodyk TIK vardą + prefiksą +
   taip/ne (pvz "DEEPSEEK_API_KEY: yra (sk-)", "MIMO_API_KEY: yra (tp-/sk-)"). Tikrink visus: GROQ_API_KEY,
   NVIDIA_API_KEY, DEEPSEEK_API_KEY, ZHIPU_API_KEY, MIMO_API_KEY, OPENROUTER_API_KEY, OPENAI_API_KEY.

1) NAUJI NATIVE TIEKĖJAI (visi OpenAI-suderinami /chat/completions; pridėk TIK tuos, kurių raktas yra;
   kiekvienam: tas pats struktūrizuotas prompt'as -> JSON {verdict,score,domain_fit,reason}, tvirtas parse,
   retry/backoff 429/5xx+Retry-After, stagger, timeout). Bazinius URL laikyk konfigūruojamus env:
   a) DEEPSEEK — base https://api.deepseek.com, modelis default `deepseek-chat` (env HERA_DEEPSEEK_MODEL).
   b) ZHIPU/GLM — tarptautinis endpoint PIRMAS: https://api.z.ai/api/paas/v4 ; fallback https://open.bigmodel.cn/api/paas/v4
      (env HERA_ZHIPU_BASE). Modelis default `glm-4.6` arba `glm-4-flash` (env HERA_ZHIPU_MODEL). Jei rakto formatas
      id.secret ir Bearer neveikia — pabandyk JWT (Zhipu v4). Verdiktą raportuok kaip juror "glm".
   c) MIMO/XIAOMI — base https://api.xiaomimimo.com/v1 (env HERA_MIMO_BASE). Modelis: gauk GET /models arba default
      `mimo-v2.5-pro` (env HERA_MIMO_MODEL). Juror "mimo". Šitas — tavo originalios tarybos narys, PRIVALOMAS jei raktas yra.
   d) NVIDIA NIM — base https://integrate.api.nvidia.com/v1 (jei raktas yra): atrink DeepSeek/GLM/Kimi/Qwen iš /models.
      (jei DeepSeek/GLM jau eina per native raktus — per NVIDIA imk daugiau KIMI/Qwen įvairovei, be dublių.)

2) DUBLIŲ VENGIMAS: jei tą pačią šeimą (pvz DeepSeek) turi ir native, ir per NVIDIA/Groq — imk TIK vieną (native pirmenybė),
   kad taryba būtų įvairi, ne tas pats modelis kelis kartus. Tikslas: 6-8 galiojantys balsai iš SKIRTINGŲ šeimų
   (Llama, Qwen, GPT-OSS [Groq]; DeepSeek [native]; GLM [Zhipu]; MiMo [Xiaomi]; + Kimi jei per NVIDIA; + 1-2 Gemini).

3) GYVA PATIKRA kiekvieno tiekėjo: pasiųsk MINIMALŲ testinį verdikto kvietimą (trumpas prompt, ~1 sakinys) ->
   raportuok per tiekėją: OK (HTTP 200, grąžino JSON) / FAIL (statusas ar klaida). NErodyk rakto. Taip pamatysim
   KURIE raktai realiai veikia, o kurie ne (blogas raktas / regionas / kvota).

4) PRIORITETAS: native + Groq + NVIDIA open-source = PAGRINDINIAI; Gemini = papildomi (1-2);
   OpenRouter = tik jei balsų <3; OpenAI = kraštutinis tie-breaker (nesutarime/prie ribos). Bet kuris gali kristi;
   min 2 galioja, <2 -> stage_for_review. Fail-safe: taryba NIEKADA neblokuoja ingest'o.

5) RE-RUN NVIDIA off-domain testas su PILNA sudėtim. Raporte: KURIE nariai realiai balsavo (vardai + score/verdict),
   council_score, domain_fit, final_action, ar tie-breaker kviestas. Ar vėl pagavo off-domain? Protokolas -> proposals/council/.
   Unit: naujų juror'ių parse + atranka + dublių vengimas (fabrikuoti atsakymai). Visi testai turi PRAEITI.

6) Nex-N2 Pro: jei nėra nė vieno pridėto rakto tam — raporte trumpai "Nex-N2 Pro: tik OpenRouter mokamas, praleista".

7) DURABILUMAS: pakeistą kodą kopijuok į /opt/cad-site-agent/n8n/hera/. Push NEDARYK.

TELEGRAM (trumpai, be raktų): (1) kurie raktai YRA (vardai+prefiksai), (2) GYVOS PATIKROS lentelė —
kiekvienas tiekėjas OK/FAIL, (3) testo verdiktas + kurie nariai balsavo su balais (ypač MiMo, GLM, DeepSeek),
(4) aiškiai „PILNA TARYBA VEIKIA: N narių" arba kurie raktai blogi/trūksta.
