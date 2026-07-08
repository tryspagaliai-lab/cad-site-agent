UŽDUOTIS — VPS Claude Code sutvirtinimas (saugumas + privatumas + kaštai). Autonomiškai, ATSARGIAI.
KRITIŠKA: blogas ~/.claude/settings.json gali nulaužti runner'į (visą automatiką). Todėl:
BACKUP -> keitimas -> JSON validacija -> testas `claude -p` -> jei lūžta, ROLLBACK. Atsiskaityk į Telegram TRUMPAI.

Kontekstas: VPS Claude Code (kuris vykdo HERA per runner) veikia --dangerously-skip-permissions (bypass).
Deny taisyklės tikrinamos PIRMA ir galioja NET bypass režime — tai kietas saugumo gardas.

1) BACKUP: `cp ~/.claude/settings.json ~/.claude/settings.json.bak-$(date +%s)` (jei failo nėra — pažymėk).

2) PRIDĖK į ~/.claude/settings.json (išlaikyk esamą turinį, tik papildyk):
   - permissions.deny (SAUGUMAS — apsaugo raktus nuo autonominio agento):
     "Read(/root/ai_digest.env)", "Read(/root/hera.env)", "Read(**/.env)", "Read(**/*.env)"
     PASTABA: tai blokuoja Read ĮRANKĮ; bash sourcing (`. /root/ai_digest.env`) NEpaliestas, digest/HERA veiks.
     NEDĖK `Bash(git push *)` deny — push mums reikės kodo backup'ui.
   - env (privatumas + kontekstas): "DISABLE_TELEMETRY":"1", "DISABLE_ERROR_REPORTING":"1",
     "DISABLE_NON_ESSENTIAL_MODEL_CALLS":"1", "CLAUDE_CODE_DISABLE_FEEDBACK_SURVEY":"1",
     "CLAUDE_AUTOCOMPACT_PCT_OVERRIDE":"75"
   - top-level: "cleanupPeriodDays": 365
   - effort/model routing: TIK jei patvirtini teisingą settings raktą Claude Code v2.1.201 (patikrink `claude --help`/docs);
     jei neaišku — PRALEISK (negadink spėdamas).

3) VALIDACIJA: `python3 -c "import json;json.load(open('/root/.claude/settings.json'));print('JSON OK')"`.
   Jei nevalidus — grąžink backup ir STOP.

4) TESTAS: `IS_SANDBOX=1 claude -p "atsakyk vienu žodžiu: OK" --dangerously-skip-permissions` — turi grąžinti atsakymą.
   Papildomai patikrink, kad deny veikia: agentas turi NEGALĖTI Read'inti /root/hera.env.
   Jei testas lūžta ar runner rizikuoja — ROLLBACK į backup.

5) Nekeisk repo .claude/ (tik globalų ~/.claude/settings.json). Kitos fazės/HERA nepaliestos.

Į Telegram: kokie nustatymai pridėti, JSON validus?, `claude -p` testas praėjo?, deny veikia?, ir aiškiai
„VPS SUTVIRTINIMAS BAIGTAS" arba (jei rollback) kas nepavyko.
