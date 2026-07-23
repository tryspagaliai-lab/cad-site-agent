UŽDUOTIS — Fazė 18: „perceived-error" (numanoma klaida) detektorius (hera_perceived_error.py). <14 min.
NEleisk pytest (tik savo selftest). Fail-safe. €0. Deterministiška (BE LLM, be tinklo). Ataskaita TIK į HERA botą.
Viešo cad-site-agent NELIESK git prasme (untracked + /opt/hera-processor). Secret'us NEliesk.

KONTEKSTAS: iš LangChain lifecycle (validacija #6) — „online eval" be etalono: aptikti kada agentas suklydo iš POKALBIO signalų
(vartotojo pataisymai „padarei blogai", įklijuota klaida/traceback), ir pažymėti blogus paleidimus peržiūrai. Monitor fazės dalis,
šalia loop-guard/diffrules. v1 deterministinis, be LLM.

1) Sukurk /root/hera_perceived_error.py (kaip kiti hera_* moduliai; HERA_PERCEIVED_ERROR jungiklis def 0 = no-op importui; CLI/funkc. veikia):
   - API: `detect(run_output: str, followup: str = "") -> dict` grąžina {status: ok|suspect, signals:[{type,match}], recommend}.
   - SIGNALŲ TIPAI (deterministiniai, LT+EN, case-insensitive; naudok žodžių ribas kur įmanoma, venk substring false-positive):
     a) user_correction: „padarei blogai|neteisinga|ne to prašiau|atsuk|sugadin|blogai padary|you messed up|that'?s wrong|not what i asked|no,? you should|undo|revert".
     b) pasted_error: „traceback|exception|\berror:|\bfailed\b|assert|rc=124|rc=137|rc=1\b|http (4|5)\d\d|stack trace|klaida:".
     c) run_abort: „NUTRAUKTA|timeout|pakib|124|137" (tik jei kontekste su rc/nutraukimu).
   - LOGIKA: jei bent 1 signalas → status=suspect + recommend „peržiūrėti"; kitaip ok. Grąžink įrodymus (match ištraukas).
   - Fail-safe: viskas try/except; klaida → status=ok + flag log /root/hera_perceived_error.log; NIEKAD necrashink. €0, be tinklo.
2) SELFTEST (`--selftest`, be pytest): (a) output + followup „padarei blogai, atsuk" → suspect(user_correction);
   (b) švarus output → ok; (c) output su „Traceback ... Error:" → suspect(pasted_error); (d) HERA_PERCEIVED_ERROR=0 → no-op importas.
   Spausdink PASS/FAIL kiekvienam.
3) Runner integracija = v2 (atskiras human-gate) — TIK modulis + selftest. Cron NEDĖK.
4) BACKUP: cp /root/hera_perceived_error.py /opt/hera-processor/ + commit/push. Vault ROADMAP.md: „Fazė 18 perceived-error (hera_perceived_error) —
   ĮDIEGTA <data>, HERA_PERCEIVED_ERROR def 0, v1 determ., Monitor fazė, runner integr.=vėliau".

ATASKAITA (HERA botas, trumpai): modulis OK/ne; selftest PASS/FAIL (a/b/c/d); backup+push; ROADMAP. Jei STOP — kodėl.
