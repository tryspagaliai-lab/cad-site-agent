UŽDUOTIS — TARYBA: PRIJUNGTI GROQ kaip PAGRINDINIUS open-source juror'ius. Atsargiai, autonomiškai.
Taryba (hera_council.py) pastatyta ir veikia (19/19 unit, pagavo NVIDIA off-domain). NEstatyk iš naujo.
KONTEKSTAS: OpenRouter free tier grąžino 429 (bendra ~50 užklausų/parą be kredito) → open-source nebalsavo.
Sprendimas: GROQ_API_KEY jau įdėtas į /root/hera.env. Groq turi tikrai naudingą free tier'ą ir hostina stiprius
open-source modelius. Prijunk Groq kaip PAGRINDINĮ open-source tiekėją; OpenRouter palik kaip antrinį/egzotiniam.
Atsiskaityk į Telegram TRUMPAI, BE raktų.

SAUGUMAS: raktų reikšmių NIEKADA nespausdink, necommit'ink, nerodyk Telegram/chate. Tik pavadinimai/prefiksai/statusai.

1) ENV: įsitikink kad /root/hera.env raktai pasiekia os.environ (jei praeita pataisa jau įkelia failą — gerai;
   jei ne — hera_council pats perskaito /root/hera.env trūkstamiems raktams). Patikra: ar yra GROQ_API_KEY,
   OPENROUTER_API_KEY, OPENAI_API_KEY (rodyk TIK taip/ne + prefiksą, pvz "gsk_", ne reikšmę).

2) GROQ TIEKĖJAS hera_council.py — nauja juror grupė per Groq API (OpenAI-suderinamas:
   POST https://api.groq.com/openai/v1/chat/completions, Authorization: Bearer <GROQ_API_KEY>).
   - Gauk modelių sąrašą GET https://api.groq.com/openai/v1/models; atrink ĮVAIRIŲ ŠEIMŲ juror'ius
     (po vieną iš: Llama, Qwen, DeepSeek, Kimi/Moonshot, GPT-OSS, Gemma) — tikslas 4-5 balsai.
     Konfigūruojama env `HERA_GROQ_MODELS` (kableliais) su protingu default; jei modelis dingęs — imk kitą.
   - Tas pats struktūrizuotas prompt'as, tas pats JSON verdiktas {verdict, score, domain_fit, reason}, tvirtas parse.
   - Retry/backoff (429/5xx + Retry-After) ir stagger, kaip OpenRouter kelyje.

3) JUROR PRIORITETAS: Groq open-source = PAGRINDINIAI; Gemini free = papildomi (1-2); OpenRouter = antrinis
   (bandyk TIK jei Groq davė <3 balsus ARBA egzotiniam MiMo/Nex-N2 Pro); OpenAI = kraštutinis tie-breaker
   (tik nesutarime/prie ribos). Bet kuris juror gali kristi; min 2 galiojantys balsai = verdiktas, <2 → review.

4) MiMo / Nex-N2 Pro: pabandyk rasti Groq IR OpenRouter modelių sąrašuose (case-insensitive "mimo"/"xiaomi",
   "nex"/"nex-n2"/"n2 pro"). Jei nėra nė vienoje — NEtylėk, raporte aiškiai: "MiMo: nerastas Groq/OpenRouter",
   "Nex-N2 Pro: nerastas" ir pasiūlyk kelią (atskiras tiekėjas/endpoint). NEblokuok tarybos dėl jų nebuvimo.

5) RE-RUN NVIDIA testas su pilna sudėtim (Groq + Gemini). Raporte: KURIE juror'iai realiai balsavo
   (vardai + score/verdict kiekvieno), council_score, domain_fit, final_action, ar tie-breaker kviestas.
   Ar taryba vėl pagavo off-domain? Protokolas -> proposals/council/<job>.json (human_gate=True).
   Taip pat greitas unit: Groq juror parse + atranka (fabrikuoti atsakymai). Turi PRAEITI.

6) DURABILUMAS: pakeistą kodą kopijuok į /opt/cad-site-agent/n8n/hera/. Push NEDARYK.

TELEGRAM (trumpai, be raktų): (1) ar Groq raktas įsiskaito (taip + prefiksas), (2) kiek Groq modelių atrinkta ir
KURIE (vardai), (3) NVIDIA testo verdiktas + kurie nariai balsavo su balais, (4) MiMo/Nex-N2 Pro — rasti ar ne,
(5) aiškiai „OPEN-SOURCE TARYBA VEIKIA (Groq)" arba kas dar trūksta.
