UŽDUOTIS — pataisyti thinkingBudget=0 faile n8n/hera/gemini.py (apsaugoti tarybą + maršrutizatorių). <12 min.
Fail-safe: jei fix neaiškus — STOP+backup restore. NEleisk pytest. €0 (1-2 maži Gemini call'ai). Ataskaita TIK į HERA botą. Secret'us NEliesk.
Viešo cad-site-agent NELIESK git prasme (failas untracked — palik untracked, kopija + push į hera-core-backup, kaip įprasta).

KONTEKSTAS: ai_digest.py jau pataisytas — gemini-flash-latest nebepriima thinkingBudget=0 (grąžina 400 INVALID_ARGUMENT). Auditas rado
tą pačią klaidą /opt/cad-site-agent/n8n/hera/gemini.py: gen()/gen_meta() default thinking=0 → siunčia thinkingConfig.thinkingBudget=0.
Naudoja hera_router.py + hera_council.py (taryba). Fallback rolina tik 503/kvotą, NE 400 — tad taryba gali tyliai gedinti jurorą.

ŽINGSNIAI:
1) BACKUP: cp /opt/cad-site-agent/n8n/hera/gemini.py /root/hera-core-backup/gemini.py.$(date +%s).
2) FIX (mažas, toks pat principas kaip ai_digest): gen()/gen_meta() — kai thinking<=0 (arba budget=0), NEsiųsk thinkingConfig lauko
   iš viso (praleisk jį), o ne siųsk thinkingBudget=0. Jei thinking>0 — palik thinkingConfig su tuo budget. Numatytas elgesys („minimizuoti
   samprotavimą") išlieka, tik be atmetamos 0 reikšmės. NELIESK kitų wrapper dalių (retry/fallback/model sąrašo).
3) PATIKRA: `python3 -c "import ast; ast.parse(open('/opt/cad-site-agent/n8n/hera/gemini.py').read()); print('OK')"`.
   RE-TEST: paleisk realų gen() call'ą su default nustatymais (thinking=0), pvz. trumpas promptas → turi grąžinti 200 + tekstą (NE 400).
   Papildomai (jei greita): mini council/router kelio patikra — pvz. importuok hera_council ir paleisk 1 juror gen() → 200. (NEleisk viso council fan-out.)
4) BACKUP kodą: cp į /opt/hera-processor (jei ten laikai) + commit/push į hera-core-backup.

ATASKAITA (HERA botas, trumpai): fix eilutė (prieš/po); ast OK; re-test gen() 200 (ne 400); ar council/router kelias patikrintas; backup kelias.
Jei STOP — kodėl + restore. NELIESK ai_digest feeds ar TLDR (atskiri žingsniai).
