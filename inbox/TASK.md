UŽDUOTIS — READ-ONLY žvalgyba: ar TIKRAS multi-model council kur nors bandytas + kas paruošta jam. NIEKO NEKEISK. <12 min.
NEleisk pytest. Fail-safe. €0. TIK skaitymas + reportas į HERA botą. Viešo cad-site-agent NELIESK. Secret'us → [REDACTED].
JAU ŽINOMA (nekartok): n8n 2.28.4 agentos-1; 3 MCP endpoint'ai deaktyvuoti; UI 401 saugu; Link Parser = single-model gemini
(nominali „council" nuoroda, NE tikras council). Ieškom ar KAŽKUR bandytas TIKRAS multi-model fan-out.

Grąžink HERA botui užpildytą JSON (šitą struktūrą, trumpai):

1_council_artifacts:
  - `grep -ril 'council\|fan.\?out\|multi.\?model\|ensemble\|debate\|panel\|jury\|taryba' /opt /root /opt/hera-vault 2>/dev/null | grep -vE '/\.git/|node_modules' | head -30`
  - Ar yra scriptas siunčiantis TĄ PATĮ prompt į 2+ modelius ir agreguojantis? (peržiūrėk kandidatus iš grep)
  - n8n DB: `docker exec n8n-n8n-1 n8n export:workflow --all --output=/tmp/wf.json 2>/dev/null` → ar yra workflow su 2+ SKIRTINGŲ LLM
    (gemini+anthropic+kt) viename? (grep node tipus/URL host'us; po to rm /tmp/wf.json). 
  - hera-vault: `grep -rin 'council\|taryba\|multi-model' /opt/hera-vault/docs/ROADMAP.md /opt/hera-vault/OPEN_QUESTIONS.md /opt/hera-vault/proposals 2>/dev/null | head`
  return: council_attempted(taip/ne), artifacts_found[], closest_existing, roadmap_mention

2_available_models:
  - LLM raktų VARDAI (NE reikšmės) iš /root/ai_digest.env /root/hera.env: `grep -oiE '^[A-Z_]*(OPENAI|OPENROUTER|GROQ|GLM|GEMINI|GOOGLE|ANTHROPIC|PERPLEXITY|DEEPSEEK|MISTRAL|HF|HUGGING)[A-Z_]*' <failai> | sort -u`
  - n8n kredencialai (tipai, iš ankstesnio audito: Anthropic zzAnthropicCr001, Gemini zzGeminiCred001 — patvirtink + ar dar yra)
  - Kurie €0 free-tier (Gemini free / Groq / GLM) vs mokami; kurie pasiekiami iš n8n konteinerio tinklo vs tik host
  return: models_with_keys[], free_tier_models[], paid_models[], reachable_from_n8n[]

3_write_back_target:
  - Ar n8n jau rašo į vault/git? (Link Parser output kur eina — peržiūrėk jo node'us)
  - hera-vault kelias council sprendimams: ar sessions/ ar naujas decisions/ (pažiūrėk kokie folder'iai yra: `ls /opt/hera-vault`)
  - Esamas write-back pattern (hera_vault_sync.sh? git commit iš n8n?)
  - Ar hera-vault = vienintelis pasiekiamas rašymui (Obsidian laptop sugadintas)
  return: existing_writeback, vault_target_path, writeback_pattern, obsidian_reachable

4_auth_pattern_for_new:
  - Ar mcpTrigger v2 (2.28.4) palaiko header/bearer auth? (iš deaktyvuoto Shell MCP node param'ų — ar yra 'authentication' opcija su bearer/header)
  - Ar Caddy gali dėti auth prieš /mcp/* (basic_auth / forward_auth direktyvos Caddyfile'e — pažiūrėk n8n-caddy config)
  - Saugaus trigger'io rekomendacija council'ui: MCP+header VS webhook+header VS schedule (be išorinio įėjimo)
  return: mcp_header_auth_supported, caddy_auth_possible, safe_trigger_recommendation, reasoning

5_trigger_intent: PENDING_USER (NEtirk — tai vartotojo sprendimas; tik pažymėk „PENDING_USER").

ATASKAITA (HERA botas): užpildyta JSON struktūra (1–4 sekcijos trumpai), 5 = PENDING_USER. Jei kur nepavyko — pažymėk.
