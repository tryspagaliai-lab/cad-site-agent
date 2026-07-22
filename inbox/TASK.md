UŽDUOTIS — Fazė 15: „Output loop/stagnation guard" (hera_loopguard.py) — anti-rc124 priedas. <14 min.
NEleisk pytest (tik savo selftest). Fail-safe. €0. Deterministiška (BE LLM, be tinklo, be hidden-states). Ataskaita TIK į HERA botą.
Privatus hera-vault (/opt/hera-vault). Viešo cad-site-agent NELIESK. Secret'us redaguok.

KONTEKSTAS (kodėl): PUMA preprint (vault nata je8nfw) — aptikti kada modelis nustoja realiai samprotauti (overthinking/
kilpos/stagnacija) ir nutraukti anksčiau nei suveikia HARD timeout. IMAM TIK HERA-įmanomą dalį: OUTPUT teksto analizę
(NE latentinę geometriją/„momentum" — reikia hidden-states, uždariems API modeliams neįmanoma). Validacija #5 anti-rc124.
Human-gate: vartotojas patvirtino („Varom").

1) Sukurk /root/hera_loopguard.py (kaip kiti hera_* moduliai; HERA_LOOPGUARD jungiklis, default 0 = no-op):
   - ĮVESTIS: output tekstas kaip eilučių/blokų sąrašas (arba viena styga → skaidyk į eilutes). Determ., be LLM.
   - APTINKA (3 signalai, kiekvienas su slenksčiu ir įrodymu):
     a) LOOP (post-convergence recurrence): normalizuota eilutė/blokas (lower, trim, collapse whitespace) kartojasi >= K kartų
        (def K=4) → loop. Grąžink kartojamą fragmentą + kiekį.
     b) RE-VALIDATION kilpa: validacijos-markerių frazių pasikartojimas virš slenksčio (pvz. „verify|re-check|validate|
        confirm again|patikrinu|dar kartą" >= M kartų, def M=5) → recurrence.
     c) STAGNACIJA (no new content): slankiu langu (def N=6 paskutinių blokų) naujų unikalių tokenų/žodžių prieaugis ~0
        (pvz. Jaccard su ankstesniu langu > 0.9 ARBA naujų-žodžių dalis < 0.05) → stagnation.
   - IŠVESTIS: dict {status: ok|loop|revalidation|stagnation, evidence, recommend: continue|truncate|restart}.
     (loop/revalidation → recommend restart arba truncate; stagnation → truncate.) ADVISORY — nieko pats nenutraukia v1.
   - Fail-safe: viskas try/except; klaida → status="ok"+flag log (/root/hera_loopguard.log); NIEKADA necrashink.
2) SELFTEST (`--selftest`, be pytest): 4 sintetiniai output'ai → teisinga klasifikacija:
   (a) sveikas progresuojantis → ok; (b) tas pats blokas ×5 → loop; (c) „let me verify..." ×6 → revalidation;
   (d) 6 blokai be naujo turinio → stagnation. + HERA_LOOPGUARD=0 → no-op. Spausdink PASS/FAIL kiekvienam.
3) Integravimas į runner = v2 (atskiras human-gate) — v1 tik modulis + selftest paruošti. Ryšys su anti-rc124: papildo
   HARD timeout (aptinka anksčiau); ateity gali maitinti hera_diffrules (loop→failure signalas).
4) Cron NEDĖK. BACKUP: cp /root/hera_loopguard.py /opt/hera-processor/ + push. 
5) Vault ROADMAP.md: „Fazė 15 Output loop/stagnation guard (hera_loopguard) — ĮDIEGTA <data>, HERA_LOOPGUARD def 0, v1 determ.
   OUTPUT-only (PUMA HERA-įmanoma dalis), anti-rc124 priedas; runner integr.=v2". Vault commit/push per sync (pull --rebase pirma).

ATASKAITA (HERA botas, trumpai): (1) modulis OK/ne; (2) selftest PASS/FAIL (ok/loop/revalidation/stagnation/no-op);
(4) backup+push OK; (5) ROADMAP OK.
