UŽDUOTIS — TARYBA: NVIDIA NIM raktas įdėtas → PRIJUNK NVIDIA juror'ius + perleisk pilną testą. Atsargiai.
Taryba (hera_council.py) veikia (38/38 unit, aktyvi prod'e HERA_COUNCIL=1, 7 balsuotojai: GLM native + Groq×5 + Gemini).
NEperstatyk branduolio. NVIDIA tiekėjo kodas praeitą kartą jau paruoštas — dabar tik ĮJUNK su raktu ir patikrink.
Atsiskaityk į Telegram TRUMPAI, BE raktų.

SAUGUMAS: raktų reikšmių NIEKADA nespausdink, necommit'ink, nerodyk Telegram/chate. Tik pavadinimai/prefiksai/statusai.

1) ENV: patvirtink NVIDIA_API_KEY yra (rodyk TIK "yra (nvapi-)"). Taip pat priminimui: GROQ, ZHIPU, DEEPSEEK, MIMO,
   OPENROUTER, OPENAI (taip/ne + prefiksas).

2) NVIDIA NIM juror'iai (base https://integrate.api.nvidia.com/v1, Bearer <NVIDIA_API_KEY>):
   - GET /models -> atrink modelius, prioritetas tiems kurių taryboje DAR NĖRA gyvo balso: KIMI (moonshot),
     QWEN, o jei DeepSeek/GLM native dabar 402/neveikia — imk DeepSeek/GLM per NVIDIA (nemokamai) kaip pakaitalą.
   - Konfigūruojama env HERA_NVIDIA_MODELS su protingu default; jei modelis dingęs — imk kitą tos/kitos šeimos.
   - Tas pats prompt'as/JSON verdiktas, tvirtas parse, retry/backoff (429/5xx), stagger. NVIDIA ~40 RPM global —
     nedaryk per daug lygiagrečiai.

3) DUBLIŲ VENGIMAS (kaip anksčiau): native pirmenybė; NVIDIA papildo tik trūkstamas šeimas (ypač KIMI).
   Tikslas: 7-9 galiojantys balsai iš SKIRTINGŲ šeimų (Llama/Qwen/GPT-OSS [Groq] + GLM [Zhipu] + Kimi/Qwen [NVIDIA]
   + Gemini; DeepSeek/MiMo jei balansas leis).

4) GYVA PATIKRA: NVIDIA — minimalus testinis verdikto kvietimas -> OK 200 / FAIL. Raporte lentelė su visais tiekėjais.

5) RE-RUN NVIDIA off-domain testas su PILNA sudėtim. Raporte: KURIE nariai realiai balsavo (vardai + score/verdict),
   ypač ar KIMI dabar balsuoja. council_score, domain_fit, final_action, ar tie-breaker kviestas. Ar pagavo off-domain?
   Protokolas -> proposals/council/. Unit: NVIDIA juror parse + atranka + dedup (fabrikuoti). Visi testai PRAEITI.

6) DURABILUMAS: pakeistą kodą kopijuok į /opt/cad-site-agent/n8n/hera/. Push NEDARYK.

TELEGRAM (trumpai, be raktų): (1) NVIDIA OK/FAIL + kiek modelių atrinkta ir KURIE (vardai), (2) ar KIMI pagaliau
balsuoja, (3) testo verdiktas + visi balsavę nariai su balais, (4) aiškiai „PILNA TARYBA: N narių".
