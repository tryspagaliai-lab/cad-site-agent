UŽDUOTIS — ai_digest TOPIC-AWARE: pridėti DIZAINO temą/botą (esamas AI-news NEPALIESTAS). <18 min.
NEleisk pytest-all. Fail-safe. €0. Raktų nespausdink. Ataskaita TIK į HERA botą.
ANTI-RC124: KIEKVIENAS feed/HF/GitHub fetch HARD timeout (≤20s), JOKIO retry; per-feed klaida → skip, ne crash.

KONTEKSTAS: 3 nauji token'ai env'e (DESIGN_BOT_TOKEN etc.). Darom ai_digest.py DAUGIA-TEMĮ. DABAR TIK dizainas.
Esamas AI-news topic (TELEGRAM_TOKEN → @tryspagaliabot, dabartiniai 16 feeds + 24 HF org, seen.jsonl) turi likti
100% NEPAKEISTAS (elgesys identiškas). Nauja tema pridedama ŠALIA. Filtras/pristatymas/v3-santraukos pernaudojami.

1) REFAKTORINK į TOPICS struktūrą (be esamo elgesio pakeitimo):
   - `TOPICS = {}` kur kiekviena tema = {token_env, feeds[], hf_orgs[], github_atom[], arxiv_cats[], filter_kw[],
     seen_path, label}. Esamą elgesį įdėk kaip temą „ai" (token_env=TELEGRAM_TOKEN, esami feeds/org/seen.jsonl —
     BE pakeitimų). Cron run'as pereina per visas temas; kiekviena NEPRIKLAUSOMA (sava seen, savas token, savas send).
     Vienos temos klaida NEsugriauna kitų (per-topic try/except, fail-safe).

2) DIZAINO tema „design" (token_env=DESIGN_BOT_TOKEN, seen_path=/var/lib/ai_digest/seen_design.jsonl):
   - HF orgai (per-org createdAt, kaip esama mechanika): black-forest-labs, tencent (FILTRUOK pagal „Hunyuan3D"),
     stabilityai, stepfun-ai. (Filtras 3-4 punkte.)
   - GitHub .atom (NAUJAS feed tipas — pridėk fetch: append .atom, feedparser): 
     https://github.com/comfyanonymous/ComfyUI/releases.atom , https://github.com/Tencent-Hunyuan/Hunyuan3D-2/releases.atom
   - RSS: https://radiancefields.substack.com/feed (Gaussian Splatting/NeRF) ; https://www.blendernation.com/feed/
     (⚠️ siųsk BROWSER User-Agent header, pvz. "Mozilla/5.0 ..."; jei 403 → fallback Feedburner
     https://feeds.feedburner.com/Blendernation ; jei ir tas nepavyksta → skip, ne crash).
   - arXiv cs.CV + cs.GR (kaip esama arXiv RSS mechanika): https://rss.arxiv.org/rss/cs.CV , https://rss.arxiv.org/rss/cs.GR
   - (HN Algolia — ATIDĖTA kitai bangai, nepridedam dabar.)

3) DIZAINO RELEVANCIJOS FILTRAS (deterministinis, be LLM; nes tencent/arXiv platūs):
   - Palik įrašą TIK jei title/tags atitinka design/image/3D raktažodžius: text-to-image, image, diffusion, controlnet,
     flux, hunyuan3d, 3d, gaussian splat, nerf, blender, render, archviz, design, sdxl, comfyui, inpaint, lora (image).
   - Tas pats esamas triukšmo filtras (is_noise: gguf/quant/probe) TAIP PAT taikomas.

4) SANTRAUKOS: pernaudok v3 batch Gemini, BET „kur_panaudoti" tilt į DIZAINO/3D/ArchViz kontekstą
   (kaip vartotojas galėtų panaudoti savo dizaino/3D/vizualizacijos darbe — Blender, ComfyUI, ArchViz pipeline).
   Fallback bare įrašas jei Gemini lūžta. €0, HARD 48s, no retry.

5) SIUNTIMAS: dizaino tema → DESIGN_BOT_TOKEN botas, per esamą skaidymo mechaniką (≤3800 sim.). „0 naujų → nieko naujo".

6) VERIFIKACIJA (privaloma): 
   - Patvirtink kad tema „ai" (senas botas) NEPAKEISTA (kodo diff nekliudo jos feeds/org/seen/token).
   - DRY-RUN dizaino temos: parodyk kiek surinko/po filtro/naujų.
   - TEST-SEND į DIZAINO botą (DESIGN_BOT_TOKEN): žyma „🧪 TESTAS — DIZAINO botas". seen_design NEkeisk dėl testo.

7) BACKUP: commit ai_digest.py → hera-core-backup. Push nepavyko → NEkartok begalos, pranešk.

RIBOS: €0. AI-news tema (TELEGRAM_TOKEN/@tryspagaliabot/seen.jsonl) NEPALIESTA. Jokio pytest-all. Anti-rc124 (HARD
timeout kiekvienam fetch, no retry, per-topic+per-feed fail-safe). Raktų nespausdink. Agro/ai-tech temos — VĖLIAU.

ATASKAITA (HERA botas, trumpai): (a) topic-aware struktūra + „ai" tema nepakeista (patvirtink)? (b) dizaino tema:
šaltiniai prijungti (HF/GitHub-atom/RSS/arXiv)? (c) GitHub .atom + browser-UA veikia? (d) dizaino dry-run: surinkta/
filtruota/nauji; (e) test-send į DIZAINO botą OK (kiek įrašų)? (f) backup push OK/ne; (g) 1 eil. kas toliau (agro).
