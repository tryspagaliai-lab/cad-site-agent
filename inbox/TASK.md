UŽDUOTIS — Council v1 statyba (user-facing €0 taryba). <30 min.
Fail-safe: jei ABEJOJI — STOP+reportuok, nekeisk (ypač runner). €0. NELIESK core hera_council.py. Ataskaita TIK į HERA botą.
TIKSLAS: plonas sluoksnis ant esamo hera_council.py — kviest tarybą per git-inbox „council: <klausimas>", €0 juror-set
(gemini+groq+glm), async, synthesis → proposals/council/<id>.json + Telegram.

PAKEITIMAI vs pradinis spec (SAUGUMAS): (i) env → /root/council_ask.env (NE į viešą /opt/cad-site-agent tree — ten net
gitignore'intų secret'ų negulti); (ii) runner edit: BŪTINAS backup + bash -n + STOP/restore; (iii) council-šaka PRIVALO
įrašyti BLOB→STATE ir exit (kitaip runner kas 2 min perpaleistų tą patį klausimą — degintų quota).

1) €0 ENV — sukurk /root/council_ask.env (NE public repo!):
   GROQ_API_KEY=<kopijuok iš esamo šaltinio, pvz. /root/ai_digest.env ar /root/hera.env>
   ZHIPU_API_KEY=<kopijuok>
   GEMINI_KEY=<kopijuok>
   NVIDIA_API_KEY=
   DEEPSEEK_API_KEY=
   MIMO_API_KEY=
   OPENAI_API_KEY=
   OPENROUTER_API_KEY=
   HERA_COUNCIL_FORCE_OR=0
   (Tušti raktai = fail-safe skip → tik gemini+groq+glm balsuos. chmod 600. NE į git.)

2) WRAPPER — sukurk hera_council_ask.py ŠALIA hera_council.py (/opt/cad-site-agent/n8n/hera/), NELIESK hera_council.py:
   - CLI: python3 hera_council_ask.py "<klausimas>"
   - Užkrauk TIK /root/council_ask.env į IZOLIUOTĄ env (os.environ kopija subprocesui/kvietimui; NE globalus), kad council
     matytų tik €0 raktus (mokami tušti → skip).
   - candidate = {"content": <klausimas>, "selector": {}, "job_id": "ask-"+ts, "date": today, "meta": {"source":"user-ask"}}
   - ADAPTYVUS ask-prompt (override domain-fit framing): „Esi tarybos narys. Įvertink šį klausimą/sprendimą. JEI taip/ne →
     verdict: taip|ne, score 0-100. JEI variantai (X ar Y) → verdict: pasirinktas variantas, score 0-100, reason. Visada trumpai pagrįsk."
   - Kviesk esamą variklį (council_decision/council_run — koks yra; write=True kad išsaugotų proposals/council/).
   - SYNTHESIS formatter iš jurors+aggregate → tekstas:
     🏛 COUNCIL: <klausimas trumpai>
     VERDIKTAS: <majority> · sutarimas <100-disagreement>%
     Balsai: <valid>/<total> · median <median_score>
     ✅ SUTARIMAS: <ką dauguma> | ⚡ DIVERGENCIJA (spread=<x>): <kur nesutaria> | ❌ ATMESTA: <silpniausi>
     Per-juror: <juror:score sąrašas>
   - Siųsk synthesis → HERA botas (naudok tą patį TG mechanizmą kaip runner/hera). Fail-safe: viskas try/except.

3) RUNNER DISPATCH — /usr/local/bin/vps_agent_runner.sh, ADITYVI šaka:
   - BACKUP PIRMA: cp /usr/local/bin/vps_agent_runner.sh /root/hera-core-backup/vps_agent_runner.sh.$(date +%s)
   - PO to kai TASK užkrautas ir po tuščias/IDLE patikros, PRIEŠ claude -p: jei TASK pirma netuščia eilutė prasideda „council:"
     → q="${eilutė be 'council:' prefikso}"; `( python3 /opt/cad-site-agent/n8n/hera/hera_council_ask.py "$q" ) >>"$LOG" 2>&1`;
     tada `echo "$BLOB" >"$STATE"`; exit 0. (council-šaka SIUNČIA savo TG pati; nekvieskiam claude -p.)
   - KITU atveju → esama logika NEPAKEISTA (fetch/blob/claude -p/timeout/STATE/indeksas).
   - `bash -n /usr/local/bin/vps_agent_runner.sh` → jei blogai, atstatyk iš backup, STOP, pranešk.
   - git-commit runner pakeitimą į /opt/hera-processor (reversible).

4) TEST (visi):
   a. python3 hera_council_ask.py "Ar geriau async ar sync council?" lokaliai
   b. Patvirtink: balsavo TIK groq+glm+gemini (grep log/output — NE deepseek/mimo/openai, jokio 402)
   c. proposals/council/ask-<id>.json sukurtas
   d. hera_vault_sync.sh nunešė į hera-vault (arba paleisk jį; PUSH OK)
   e. Telegram synthesis atėjo
   f. REGRESIJA: sukurk laikiną normalų (ne council:) mock TASK ir paleisk TIK runner šakos logiką (arba mintyse patvirtink kad
      ne-council kelias nepaliestas) — runner turi veikt kaip anksčiau
   g. EDGE: tuščias klausimas → graceful (ne crash)

5) SESSION-LOG — hera-vault:sessions/n8n-session-log.md: kas sukurta, runner šaka, test a-g, kaip kviesti („council: <klausimas>").

ATASKAITA (HERA botas, trumpai): failai (council_ask.env /root + hera_council_ask.py + runner-branch backup kelias); €0 juror-set
patvirtintas (kurie balsavo); test a-g pass/fail; pvz synthesis output; bash -n OK; session-log commit. Jei STOP — kodėl + backup atstatytas.
