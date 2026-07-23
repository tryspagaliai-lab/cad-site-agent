UŽDUOTIS — Fazė 19: „LangFuzz-lite" parafrazių konsistencijos testas (hera_langfuzz.py). <14 min.
NEleisk pytest (tik savo selftest). Fail-safe. €0. Ataskaita TIK į HERA botą. Viešo cad-site-agent NELIESK git prasme (untracked + /opt/hera-processor). Secret'us NEliesk.

KONTEKSTAS: iš LangChain lifecycle (LangFuzz idėja) — paleist tą pačią užklausą KELIOM formuluotėm per taikinį; jei atsakymai
DRASTIŠKAI skiriasi → vienas klaidingas. €0 savitikros metodas (Test fazė). v1 branduolys DETERMINISTINIS (palyginimas be LLM);
parafrazių generavimas — NEPRIVALOMAS pagalbininkas per JAU pataisytą gemini wrapper'į (fail-safe).

1) Sukurk /root/hera_langfuzz.py (kaip kiti hera_* moduliai; HERA_LANGFUZZ jungiklis def 0 = no-op importui; funkc. veikia):
   - BRANDUOLYS (determ., €0): `check_consistency(fn, variants, compare="token") -> dict`:
     * fn = iškviečiamas objektas (callable), priima str, grąžina str (ar dict → serializuok į str).
     * variants = sąrašas semantiškai vienodų įvesčių formuluočių.
     * Paleidžia fn(v) kiekvienam variantui (fail-safe: fn klaida vienam → tas rezultatas „ERROR", tęsia).
     * Palygina išvestis POROMIS pagal compare:
        - "exact": normalizuotas string lygumas (struktūriniams verdiktams/keliams).
        - "token": Jaccard žodžių persidengimas (determ.).
        - "embed": NEPRIVALOMA — jei fastembed/hera_semsearch prieinamas, cosine; jei ne → fallback į token.
     * divergence = 1 - min poros panašumas. Jei divergence > slenkstis (def 0.5) → inconsistent (pažymėk poras).
     * Grąžina {consistent: bool, divergence: float, per_variant: [...], flagged_pairs: [...]}.
   - NEPRIVALOMAS: `gen_paraphrases(question, n=3) -> list[str]` per hera gemini wrapper (n8n/hera/gemini.py, JAU pataisytas thinkingBudget).
     Fail-safe: jei Gemini nepasiekiamas/klaida → grąžink [question] (1 elementas), NIEKAD necrashink. (Šitas kelias — €0 free tier.)
   - Fail-safe visur; klaida → log /root/hera_langfuzz.log, saugus grąžinimas. HERA_LANGFUZZ=0 → no-op importui.
2) SELFTEST (`--selftest`, be pytest): (a) fn grąžina TĄ PATĮ visiems variantams → consistent=True;
   (b) fn grąžina drastiškai skirtingus → consistent=False + flagged_pairs; (c) fn su viena klaida (išmeta) → graceful, ne crash;
   (d) HERA_LANGFUZZ=0 → no-op importas. Spausdink PASS/FAIL. (gen_paraphrases NEPRIVALOMA testuoti gyvai — jei greita, 1 call, kitaip praleisk.)
3) Runner integracija = v2 (atskiras human-gate). Cron NEDĖK.
4) BACKUP: cp /root/hera_langfuzz.py /opt/hera-processor/ + commit/push. Vault ROADMAP.md: „Fazė 19 LangFuzz-lite (hera_langfuzz) —
   ĮDIEGTA <data>, HERA_LANGFUZZ def 0, v1 determ. konsistencija + neprivalomas Gemini parafrazių gen, Test fazė, runner integr.=vėliau".

ATASKAITA (HERA botas, trumpai): modulis OK/ne; selftest PASS/FAIL (a/b/c/d); ar gen_paraphrases patikrintas; backup+push; ROADMAP. Jei STOP — kodėl.
