UŽDUOTIS — Fazė 13: „EMG-lite failure-diff rules" (hera_diffrules.py). <14 min.
NEleisk pytest (tik savo mini-testą). Fail-safe. €0. Deterministiška (BE LLM). Ataskaita TIK į HERA botą.
Privatus hera-vault (/opt/hera-vault). Viešo cad-site-agent NELIESK.

KONTEKSTAS (kodėl): EMG preprint (UESTC 2026-07-15, vault nata 6s36r7) — klaidų taisymas ne per brangų LLM
samprotavimą, o per deterministinį nepavykusios↔pavykusios trajektorijos palyginimą offline; test-time tik paieška.
Tai HERA architektūros validacija #3. Mes imam TIK idėjos branduolį (seq-diff, NE pilną Fused Gromov-Wasserstein —
overkill mūsų masteliui). Human-gate: vartotojas patvirtino („Varom").

1) Sukurk /root/hera_diffrules.py (kaip kiti hera_* moduliai; HERA_DIFFRULES jungiklis, default 0 = no-op):
   - ĮVESTIS (v1, kas jau yra diske — prisitaikyk prie realios struktūros, NEgriauk):
     a) Sesijų indeksas (hera_index_append.py rašomas JSONL; runner_session įrašai su ts/rc/task_title).
     b) /root/agent_result_<blob>.txt failai (runner išvestys).
     c) Jei yra rejected-edit buferis (5d) — rejected↔accepted poros.
   - LOGIKA (deterministinė, be tinklo, be LLM):
     * Rask FAILURE→SUCCESS poras: ankstesnis įrašas rc!=0 (arba timeout 124) + vėlesnis rc==0, kurių
       task_title panašus (normalizuok: lowercase, be skyrybos; sutampa >=60% žodžių arba pirmi 5 žodžiai).
     * Kiekvienai porai ištrauk skirtumą: iš failed rezultato failo — klaidos eilutės (grep -iE
       'error|timeout|fail|traceback|exit|rc=' pirmi ~5 hit'ai); iš succeeded — kas suveikė (pirmos ~5
       prasmingos eilutės). Suformuok TAISYKLĘ: „KONTEKSTAS (task raktažodžiai) / KLAIDA (kas nepavyko) /
       KOREKCIJA (kas suveikė) / šaltinis: <blob_fail>→<blob_ok>, datos".
   - IŠVESTIS: /opt/hera-vault/rules/failure-diff/<data>-<trumpas-slug>.md (po vieną taisyklę; YAML-ish
     antraštė: date, kind: failure-diff-rule, source_pair, keywords). Dedup: jei taisyklė su ta pačia
     source_pair jau egzistuoja — praleisk. Vault sync cron patems pats; Memora indeksuos natūraliai
     (JOKIO runner-prompt injection v1 — tai v2 su atskiru human-gate).
   - Fail-safe: viskas try/except, bet kokia klaida → no-op + viena eilutė į /root/hera_diffrules.log.
2) Mini-testas (be pytest): python3 su 2 sintetiniais index įrašais (rc=124 → rc=0, panašus title) +
   2 fake result failais tmp'e → patikrina kad sugeneruojama >=1 taisyklė ir kad dedup veikia (2-as
   paleidimas nekuria dublio). Įdėk testą kaip `if __name__ == "__main__" and "--selftest" in sys.argv`.
3) Paleisk REALIAI vieną kartą: `HERA_DIFFRULES=1 python3 /root/hera_diffrules.py` — kiek porų rado ir
   kiek taisyklių sukūrė istoriniuose duomenyse (gali būti 0 — tai OK, praneša skaičių).
4) Cron NEDĖK (v1 rankinis/užduotinis paleidimas; cron — po human-gate v2).
5) Vault: į /opt/hera-vault/docs/ROADMAP.md pridėk eilutę „Fazė 13 EMG-lite failure-diff rules — ĮDIEGTA
   <data>, HERA_DIFFRULES def 0, v1 be prompt-injection". BACKUP: cp /root/hera_diffrules.py
   /root/hera-core-backup/. Vault commit+push per esamą sync mechanizmą arba tiesiogiai (pull --rebase pirma).

ATASKAITA (HERA botas, trumpai): (1) modulis sukurtas OK/ne; (2) selftest PASS/FAIL; (3) realus bėgimas:
N porų / M taisyklių; (5) ROADMAP + backup OK.
