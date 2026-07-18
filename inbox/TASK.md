UŽDUOTIS — PERSIST 2 KURUOTUS GROWTH ĮRAŠUS (strateginio sluoksnio kuravimas, be PARSER). <10 min.
NEleisk pytest. Telegram TRUMPAI į HERA botą. Fail-safe. €0. Raktų nespausdink. Deterministiška
(JOKIŲ LLM/tinklo — visas turinys duotas žemiau verbatim, tik įrašyk failus). Ataskaita TIK į HERA botą.
Privatus hera-vault. Viešo cad-site-agent NELIESK.

KONTEKSTAS: web sesija (Claude Code) kuravo ManuAGI Weekly #275 ingestą (`h7pxnt`, stage_for_review):
iš 20 projektų ištraukti 2 stiprūs kandidatai, verifikuoti tiesiogiai iš GitHub (ne iš transkripto).
Vartotojas patvirtino kelią „kuruotas įrašas vietoj auto-parse". Digest'o likusius 16 — NIEKO nedaryti
(prune sprendimas atskirai per dashboard). h7pxnt natą papildyk eilute: „Kuruota 2026-07-18: išskirti 2
kandidatai → headroom + herdr (atskiros natos); likusi apžvalga referencinė, ne-promote."

A) SUKURK growth natą (standartinis vardinimas, slug `headroom`, data 2026-07-18, source: kuruota-web-sesija,
   STATUS: PRIIMTA kaip žinojimas 2026-07-18 (human-gate: vartotojas per web sesiją)) su turiniu:
---
# Headroom — konteksto suspaudimo sluoksnis agentams
- **Repo:** https://github.com/headroomlabs-ai/headroom (Apache 2.0, ~59.8k žv., v0.32.0 2026-07-17, aktyvus)
- **Kas:** suspaudžia tool-output/logus/failus/RAG prieš LLM. Trys kompresoriai: SmartCrusher (JSON,
  DETERMINISTINIS), CodeCompressor (AST: Py/JS/Go/Rust/Java/C, DETERMINISTINIS), Kompress-v2-base
  (proza, ML per ONNX Runtime — x86 reikia AVX2, yra fallback). Grįžtamasis: originalai cache'inami
  lokaliai, modelis gali pasiimti per headroom_retrieve. Režimai: Python lib / proxy / MCP / `headroom wrap claude`.
- **README skaičiai (ne blogų):** ~20% coding-agentams, 60–95% JSON; GSM8K tikslumas nepakitęs (0.870).
  ⚠️ Blogosferos „60–95% visur" = marketingas, necituoti.
- **HERA pritaikymas (kandidatas, NE sprendimas):** token'ų mažinimas ingest/research grandinėse ant
  nemokamų limitų (Gemini free/Groq). Siūlomas kelias: TIK deterministiniai kompresoriai (JSON+AST),
  BE ML prozos kelio (4GB VPS + deterministinis-core). Įjungimas tik atskiru spec'u su human-gate,
  HERA_HEADROOM=1 (def 0), advisory; anti-rc124 nepažeidžiamas (mažiau token'ų → greičiau).
---

B) SUKURK growth natą (slug `herdr`, kitkas kaip A) su turiniu:
---
# herdr — agentų multiplekseris terminale
- **Repo:** https://github.com/ogulcancelik/herdr (AGPL-3.0+ / dual komercinė; ~17.9k žv., v0.7.4 2026-07,
  vienas Rust binary ~10MB, Linux/macOS, be telemetrijos/tinklo)
- **Kas:** tmux agentams: kiekvienas agentas savo tikrame terminale, sidebar su būsenom
  (blocked/working/done/idle); detach → agentai gyvi fone → reattach iš bet kur per SSH (telefonas per
  SSH klientą veikia). Aptinka Claude Code, Codex, Copilot CLI ir kt.
- **Svarbiausia (video neminėjo, verifikuota):** SOCKET API — agentai patys gali kurti panes, skaityti
  vienas kito išvestį, laukti būsenų. Tai orkestravimo primityvas, ne tik UI.
- **Pritaikymas:** DABAR — vartotojo laptopo darbo eigai (multi-agent valdymas, SSH iš telefono).
  VPS flock/cron runner'io NEKEIČIA (jis stabilus); socket API — tik ateities kandidatas, jei prireiks
  interaktyvios multi-agent koordinacijos. Saugumo higiena: diegti iš release binary su checksum,
  ne `curl | sh`.
---

C) hera_wikilink + hera_lint deterministinis pass. Commit + push hera-vault. Push nepavyko → NEkartok
   begalos, pranešk.

RIBOS: €0. Jokių LLM/tinklo skambučių. Jokio pytest. Viešo NELIESK. Nieko netrink. Tik 2 naujos natos
+ 1 eilutė h7pxnt natoje + wiki pass.

ATASKAITA (HERA botas, trumpai): (a) 2 natos sukurtos (pavadinimai)? (b) h7pxnt pažymėta? (c) wiki
orphan/dangling PO; (d) vault push OK/ne.
