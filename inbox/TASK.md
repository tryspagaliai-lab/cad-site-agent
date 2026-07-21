UŽDUOTIS — VPS pakeitimai (3 dalys): (A) prisegti runner prie Sonnet 5; (B) pastatyti @AI_HOWTO_BOT digest temą; (C) pridėti 2 feed'us. <14 min.
NEleisk pytest. Fail-safe. €0. Ataskaita TIK į HERA botą. Privatus hera-vault; viešo cad-site-agent NELIESK.
PASTABA: 3ds Max IR AutoCAD MCP vault natos JAU sukurtos tiesiogiai (vault commit c325abd) — jų NEBEDARYK.

============================================================
(A) SONNET 5 PIN — runner modelis (svarbiausia, daryk PIRMA)
============================================================
Priežastis: bendra Claude prenumeratos sesijos riba stabdo runner'į. Prisegam prie Sonnet 5, kad nebedegintų quota.
1) Backup: `mkdir -p /root/hera-core-backup && cp /usr/local/bin/vps_agent_runner.sh /root/hera-core-backup/vps_agent_runner.sh.$(date +%s)`.
2) Rask eilutę su `claude -p` (arba `claude --print`). Jei JOJE dar NĖRA `--model`, pridėk `--model claude-sonnet-5`.
   Pvz.: `claude -p ...` → `claude --model claude-sonnet-5 -p ...`. Jei jau yra kitas --model, pakeisk į claude-sonnet-5.
3) `bash -n /usr/local/bin/vps_agent_runner.sh` (sintaksės patikra). Jei blogai — atstatyk iš backup, pranešk, STOP.
4) Į ataskaitą įrašyk PRIEŠ/PO `claude ...` eilutę.

============================================================
(B) @AI_HOWTO_BOT — nauja digest tema `aitech` faile /root/ai_digest.py
============================================================
Kontekstas: 4-as botas. Tema = AI EKSPLOATAVIMO METODAI / how-to (kaip praktiškai naudoti AI įrankius, agentus,
workflow'us), NE bendros naujienos. Token env: AITECH_BOT_TOKEN (jau /root/ai_digest.env). seen: /root/seen_howto.jsonl.
1) Į TOPICS dict pridėk raktą `aitech` tokio pat pavidalo kaip esami (ai/design/agro): laukai token_env,
   feeds, hf_orgs, github_atom, arxiv_cats, filter_kw, seen_path, label. Reik minimaliai:
   - token_env: "AITECH_BOT_TOKEN"
   - seen_path: "/root/seen_howto.jsonl"
   - label: "🤖 AI how-to / eksploatavimo metodai"
   - feeds (patvirtinti šaltiniai iš deep-research; naudok User-Agent kaip kituose):
       https://www.anthropic.com/rss.xml,
       https://openai.com/blog/rss.xml,
       https://huggingface.co/blog/feed.xml,
       https://simonwillison.net/atom/everything/,
       https://www.latent.space/feed,
       https://blog.langchain.dev/rss/,
       https://www.llamaindex.ai/blog/feed.xml,
       https://newsletter.maartengrootendorst.com/feed,
       https://eugeneyan.com/rss/
   - github_atom (kaip kitur, .atom):
       https://github.com/langchain-ai/langchain/releases.atom,
       https://github.com/run-llama/llama_index/releases.atom,
       https://github.com/microsoft/autogen/releases.atom,
       https://github.com/crewAIInc/crewAI/releases.atom,
       https://github.com/openai/openai-cookbook/commits/main.atom
   - hf_orgs: [] (nebūtina šiai temai; palik tuščią sąrašą)
   - arxiv_cats: ["cs.AI","cs.CL"]  (per filter_kw susiaurinsim į agent/RAG/tooling)
   - filter_kw: agent, agentic, RAG, retrieval, tool use, function calling, MCP, prompt, fine-tun, workflow,
     orchestrat, LLM app, evaluation, eval, guardrail
2) Kaip ir kitos temos — per-topic try/except, per-topic seen, per-topic token, per-topic send. NELIESK ai/design/agro logikos.
3) Panaudojimo aprašas kaip visose temose: kiekvienam įrašui 2–3 sakiniai „Kas tai" + „Kur panaudoti"
   (usage pakreiptas į vartotojo kontekstą: AI orkestracija, agentai, ArchViz/CAD automatizacija).

============================================================
(C) FEED papildymai (tame pačiame /root/ai_digest.py)
============================================================
- Į `ai` temos feeds pridėk: https://aimodels.substack.com/feed
- Į `design` temos feeds pridėk: https://tldr.tech/api/rss/design

============================================================
PATIKRA + BACKUP
============================================================
5) `python3 -c "import ast; ast.parse(open('/root/ai_digest.py').read()); print('OK')"` — sintaksė.
6) Testinis paleidimas TIK aitech temai jei skriptas turi tokį rėžimą; jei ne — nepaleisk viso (kad 08:00 cron atliktų).
7) BACKUP: `cp /root/ai_digest.py /root/hera-core-backup/ai_digest.py.$(date +%s)`. Nepavyko patikra → atstatyk iš backup, pranešk, STOP.

ATASKAITA (HERA botas, trumpai): (A) claude eilutė prieš/po; (B) aitech tema pridėta OK/ne, feeds skaičius;
(C) 2 feed'ai pridėti; (5) ast OK/ne; (7) backup OK.
