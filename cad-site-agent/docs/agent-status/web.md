# Agent status: web

- updated: 2026-07-06T19:30:00Z
- branch: claude/lithuanian-language-question-7al6mx
- head: (žr. paskutinį commit'ą)
- status: DONE (didžioji dalis) — VPS automatika iš telefono. **AI Research Digest VEIKIA**:
  standalone `/root/ai_digest.py` + cron kasdien 08:00 Europe/Vilnius, LLM Google Gemini
  `gemini-flash-latest` (thinkingBudget=0, NEMOKAMAS), į Telegram chat 725037198 (@tryspagaliabot).
  Testas: surinkta 53 naujienos, issiusta. Anthropic išbandytas bet mokamas → atsisakyta.
  n8n variantas buvo nepatikimas → pereita prie standalone. Pilna dokumentacija: `docs/VPS_AUTOMATION.md`.
  **run_shell VEIKIA** — toolCode su child_process (kaip ping); vykdo komandas n8n konteineryje.
  Naudoti naujame Claude pokalbyje. Host lygio valdymui reiktų atskiro agento.
  Saugumo TODO: atšaukti Anthropic raktą, pergeneruoti Telegram token, apsaugoti MCP shell path (viešame repo).
