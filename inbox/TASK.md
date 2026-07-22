UŽDUOTIS — Fazė 14: „Validator-first" vartai (hera_validator.py). <15 min.
NEleisk pytest (tik savo selftest). Fail-safe. €0. Deterministiška (BE LLM v1). Ataskaita TIK į HERA botą.
Privatus hera-vault (/opt/hera-vault). Viešo cad-site-agent NELIESK. Secret'us redaguok.

KONTEKSTAS (kodėl): „Model Synthesis" video (vault nata 1wuqk8) — /auto-validate idėja: PRIEŠ darbą parašomas
„proof" scriptas su aiškiais pass/fail teiginiais; failure-teiginiai = tikslus feedback. Mes imam TIK deterministinį
branduolį (v1 be LLM). Architektūros validacija #4. Human-gate: vartotojas patvirtino („VAROM").

1) Sukurk /root/hera_validator.py (kaip kiti hera_* moduliai; HERA_VALIDATOR jungiklis, default 0 = no-op):
   - IDĖJA: užduotis/darbo vienetas deklaruoja SĖKMĖS TEIGINIUS iš anksto (validator-first). Modulis juos vykdo
     PRIEŠ darbą (baseline — tikimasi FAIL, nes dar nieko nepadaryta) ir PO darbo (tikimasi PASS). Kiekvienam teiginiui —
     aiškus failure-message = feedback.
   - ĮVESTIS (v1, deterministinė, be LLM, be tinklo): success-criteria kaip mažas deklaratyvus sąrašas. Palaikyk bent šiuos
     teiginių tipus (JSON/dict arba paprastas DSL — pasirink švariausią):
       * file_exists: <kelias>
       * file_contains: {path, pattern}  (regex/substr)
       * cmd_exit0: <shell komanda>  (rc==0 = pass; SAUGU: leisk TIK read-only komandas — whitelist: test, grep, ls,
         cat, python3 -c, git status/rev-parse; blacklist rm/mv/dd/curl/wget/>—jei komandoj yra blacklist token → SKIP+flag)
       * count_at_least: {cmd, n}  (komandos stdout eilučių >= n)
   - API: `run_assertions(assertions, phase) -> {passed, failed, results:[{assertion, ok, message}]}`.
     `validate_task(spec_path_or_dict) -> before/after ataskaita`.
   - Fail-safe: viskas try/except; bet kokia klaida vieno teiginio → tas teiginys „error" (ne crash); log į /root/hera_validator.log.
   - IŠVESTIS: struktūrizuota ataskaita (dict/JSON) — pass/fail suvestinė + per-assertion message. Neprivalo rašyti į vault v1.
2) SELFTEST (`--selftest`, be pytest): sintetinis spec (file_exists tmp failui + file_contains) →
   (a) prieš sukuriant failą: FAIL (baseline); (b) sukūrus: PASS. + blacklist komandos SKIP patvirtinimas. Spausdink PASS/FAIL.
3) Realaus integravimo v1 NEDIEGIAM į runner'į (tai v2 su atskiru human-gate) — TIK modulis + selftest paruošti naudojimui.
4) Cron NEDĖK. BACKUP: cp /root/hera_validator.py /opt/hera-processor/ (tikras git repo, kaip diffrules) + push.
5) Vault ROADMAP.md: pridėk „Fazė 14 Validator-first (hera_validator) — ĮDIEGTA <data>, HERA_VALIDATOR def 0, v1 determ. be LLM,
   integravimas į runner = v2". Vault commit/push per esamą sync (pull --rebase pirma).

ATASKAITA (HERA botas, trumpai): (1) modulis OK/ne; (2) selftest PASS/FAIL (baseline-fail→post-pass→blacklist-skip);
(4) backup+push OK; (5) ROADMAP OK.
