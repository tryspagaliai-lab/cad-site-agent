UŽDUOTIS — Fazė 16 (v2): įpinti loop-guard + diffrules į vps_agent_runner.sh — ADVISORY, flag-gated, fail-safe. <15 min.
KRITIŠKA: čia backbone (runner). NEleisk pytest. Fail-safe MAX. €0. Ataskaita TIK į HERA botą. Viešo cad-site-agent NELIESK.
PAGRINDINĖ TAISYKLĖ: su HERA_* flag'ais = 0 runner elgesys turi likti 100% IDENTIŠKAS. Jei ABEJOJI — atstatyk iš backup, STOP, pranešk.

KONTEKSTAS: turim 3 gyvus modulius (hera_diffrules.py Fazė13, hera_validator.py Fazė14, hera_loopguard.py Fazė15), visi
v1 selftest PASS. v2 = įpinti į runner. ŠIOJE užduotyje darom TIK 2 SAUGIAUSIUS (loop-guard advisory + diffrules post-hook).
Validator-first (reikia TASK.md assertions konvencijos) = v2.1 vėliau, NE dabar.

ŽINGSNIAI:
1) BACKUP BŪTINAS: `mkdir -p /root/hera-core-backup && cp /usr/local/bin/vps_agent_runner.sh /root/hera-core-backup/vps_agent_runner.sh.$(date +%s)`.
   Taip pat commit'ink dabartinį į /opt/hera-processor jei ten laikai (kaip modulius).
2) Perskaityk /usr/local/bin/vps_agent_runner.sh. Rask kur apskaičiuojamas OUT ir RC (po `claude ... -p`), ir kur send_tg siunčia rezultatą.
3) ĮTERPK 2 dalykus, VISKAS fail-safe (subshell + `|| true`, kaip jau daro esamas indekso blokas skripto gale):
   (A) LOOP-GUARD (advisory): PO to kai OUT ir RC žinomi, PRIEŠ galutinį send_tg — jei `[ "${HERA_LOOPGUARD:-0}" = "1" ]`,
       paleisk determ. patikrą ant OUT: `LG=$( printf '%s' "$OUT" | HERA_LOOPGUARD=1 python3 /root/hera_loopguard.py --stdin 2>/dev/null || true )`.
       (Jei hera_loopguard.py neturi --stdin rėžimo — PRIDĖK jį: skaito stdin, spausdina 1 eilutę „status=... recommend=..."; be crash.)
       Sudaryk trumpą LG_NOTE (pvz. „\n⚠️ loop-guard: <status>/<recommend>" jei status!=ok, kitaip tuščią). Įterp LG_NOTE į send_tg tekstą.
       Su flag=0 → LG_NOTE tuščias, žinutė nepakitusi.
   (B) DIFFRULES (post-hook): skripto GALE (šalia esamo indekso subshell'io) — jei `[ "${HERA_DIFFRULES:-0}" = "1" ]`,
       `( HERA_DIFFRULES=1 /usr/bin/python3 /root/hera_diffrules.py ) >>"$LOG" 2>&1 || true`. Su flag=0 → nieko.
   NELIESK: fetch, blob-dedup, claude -p eilutės, timeout, STATE rašymo, esamo indekso bloko.
4) FLAG'Ų NEĮJUNK — palik HERA_LOOPGUARD ir HERA_DIFFRULES neapibrėžtus/0 (dormant plumbing). Vartotojas įjungs vėliau po verifikacijos.
5) PATIKRA: `bash -n /usr/local/bin/vps_agent_runner.sh` → turi būti OK. Jei blogai → atstatyk iš backup, STOP, pranešk.
   Papildomai: mock-testas su flag=0 kad post-process blokai no-op (pvz. paleisk tik tuos naujus fragmentus atskirai su HERA_*=0).
6) Į ataskaitą įrašyk PRIEŠ/PO svarbias eilutes (diff santrauką), backup kelią, bash -n rezultatą.

ATASKAITA (HERA botas): backup OK+kelias; (A) loop-guard advisory įterptas (ir ar reikėjo --stdin priedo); (B) diffrules post-hook įterptas;
bash -n OK/ne; flag'ai palikti 0 (patvirtink); mock no-op patikra. Jei kur STOP — kodėl + kad backup atstatytas.
