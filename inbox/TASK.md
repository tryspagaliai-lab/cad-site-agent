UŽDUOTIS — Fazė 23: hera_skillcapture.py — dvigubo naudojimo skill/trace kaupimas (RAG dabar + SFT-ready vėliau). <14 min.
NEleisk pytest (tik savo selftest). Fail-safe. €0. Deterministiška (BE LLM, BE tinklo). Ataskaita TIK į HERA botą. Viešo cad-site-agent NELIESK git prasme. Secret'us NEliesk.

KONTEKSTAS: web tyrimas + €0 taryba (4/5 TAIP) konvergavo — kaupti DVIGUBO NAUDOJIMO trace duomenis DABAR verta (RAG uplift + optionality, ~€0).
Local LoRA = optional/eksperimentas, NE smegenys — TODĖL šis modulis TIK kaupia duomenis dvigubu formatu, JOKIO treniravimo, jokio lokalaus modelio.
Kanoninis formatas (iš tyrimo): vienas rich JSON record → flat projekcija RAG'ui DABAR + ShareGPT/ChatML konversija SFT'ui VĖLIAU.

1) Sukurk /root/hera_skillcapture.py (kaip kiti hera_* moduliai; determ., fail-safe):
   - Jungiklis: HERA_SKILLCAPTURE def 0 = DRY-RUN (apskaičiuoja + grąžina record'ą, BET NIEKO NERAŠO į diską/korpusą — saugus default). =1 → taip pat persistina failus.
   - API: `capture(task, steps, context="", final_response="", outcome="unverified", tags=None, skill_id=None, save_dir="/root/hera_skills") -> dict`
     * steps = list; kiekvienas elementas dict {thought, tool, args, observation} ARBA string (normalizuok string→{thought:string, tool:"", args:"", observation:""}).
     * skill_id: jei None → determ. iš task (slug + sha8(task)) — TAS PATS task → TAS PATS id (idempotent).
     * KANONINIS RECORD (source of truth): {skill_id, task, context, steps:[{thought,tool,args,observation}], final_response, outcome, tags, timestamp}. timestamp = ISO iš sistemos laiko.
   - VEIKSMAI (jei HERA_SKILLCAPTURE=1; jei 0 → tik grąžink, nerašyk):
     a) įrašyk kanoninį JSON į save_dir/skill_<skill_id>.json.
     b) sukurk skill.md SCAFFOLD į save_dir/skill_<skill_id>.md (STAGING — NE į vault skills/; human-gate promovuos vėliau). Sekcijos: # <task>, ## Trigger, ## Žingsniai (iš steps), ## Taisyklės/išimtys (iš konteksto+tagų, palik placeholder jei nėra), ## Įvestys/Išvestys, ## Outcome.
     c) rag_text = flat projekcija (task + " :: " + final_response + kompaktiška steps santrauka) — grąžink lauke IR appendink į save_dir/rag_corpus.jsonl kaip {skill_id, text, tags} (semsearch indeksuos VĖLIAU — čia NEindeksuok).
   - GAP-CHECK (determ. heuristika, VISADA skaičiuok, grąžink `gaps: [klausimai]`): step su tool bet be args; ne-paskutinis step be observation; nėra final_response; outcome=="unverified"/tuščias; steps su sąlyga ("if"/"jei"/"jeigu") be aiškios šakos; nėra sėkmės kriterijaus. Kiekviena spraga → patikslinamasis klausimas LT (idėja iš „Record a skill": AI gaudo spragas).
   - SCHEDULE-KANDIDATAS (determ.): jei task/tags turi kartotinumo signalą ("kasdien","daily","kiekvien","naujausi","check for new","periodiš") → `schedule_candidate: True`, kitaip False.
   - DVIGUBO NAUDOJIMO konversija: funkcija `to_sft(record) -> dict` → ShareGPT formatas {conversations:[{from:"human",value:task+context}, {from:"gpt",value:thought}, {from:"function",value:tool+args}, {from:"observation",value:observation}, ..., {from:"gpt",value:final_response}]}. Steps→human/gpt/function/observation turns. (Įrodo kad formatas konvertuojamas nuo 1 dienos, net jei niekada netreniruosim.)
   - FAIL-SAFE: bet kokia klaida (pvz. nerašomas save_dir) → grąžink record'ą ATMINTYJE (jokio duomenų praradimo!) su {persisted:False, error:...} + log /root/hera_skillcapture.log. NIEKAD necrashink.
   - €0, be tinklo, be LLM. (Natūrali kalba→struktūra per LLM = v2 vėliau, NE dabar.)

2) SELFTEST (`--selftest`, be pytest, be tinklo), spausdink PASS/FAIL kiekvienam:
   (a) pilnas capture (HERA_SKILLCAPTURE=1): task+steps(thought/tool/args/observation)+final_response+outcome="success" → JSON įrašytas, skill.md įrašytas, rag_text yra, rag_corpus.jsonl papildytas, gaps=[] (gerai apibrėžta).
   (b) gap detekcija: nepilni steps (tool be args) + nėra final_response + outcome tuščias → gaps NEtuščias (išvardija trūkstamus kaip klausimus).
   (c) schedule: task="kiekvieną dieną tikrink naujus YouTube video" → schedule_candidate True.
   (d) to_sft: pilnas record → grąžina validų ShareGPT {conversations:[...]} su human/gpt/function/observation turns; laukai išsaugoti.
   (e) def 0 dry-run: HERA_SKILLCAPTURE=0 → grąžina record BET save_dir NEpakito (jokių naujų failų).
   (f) fail-safe: save_dir="/nonexistent/xyz" su =1 → grąžina record atmintyje persisted=False, NE crash.
   (g) idempotent id: tas pats task 2x → tas pats skill_id.

3) JOKIOS runner/cron integracijos (tai sąmoningai iškviečiamas įrankis, ne hook). Vault skills/ NELIESK — skill.md lieka STAGING (/root/hera_skills). Promovavimas į vault = atskiras human-gate vėliau.

4) BACKUP: cp /root/hera_skillcapture.py /opt/hera-processor/ (ar /root/hera-core-backup/) + commit/push į PRIVATŲ hera-core-backup (TIK šitas failas; nesusijusių NELIESK). Vault ROADMAP.md 1 eilutė:
   „Fazė 23 hera_skillcapture — ĮDIEGTA <data>, HERA_SKILLCAPTURE def 0 dry-run, determ. dvigubo naudojimo kaupimas (kanoninis JSON→RAG flat + ShareGPT SFT), gap-check, schedule-kandidatas; iš Record-a-skill pattern + tyrimo/tarybos konvergencijos; LLM-struktūrizavimas + semsearch indeksavimas=vėliau."

ATASKAITA (HERA botas, trumpai): modulis OK/ne; selftest a/b/c/d/e/f/g PASS/FAIL (ypač a: dvigubo naudojimo failai sukurti; d: ShareGPT konversija validi; e: def 0 nieko nerašo; f: fail-safe jokio duomenų praradimo); backup+push; ROADMAP. Jei STOP — kodėl.
