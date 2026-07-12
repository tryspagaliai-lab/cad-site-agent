UŽDUOTIS — APR į future-gpu track + planning-loop v2 cross-note. <8 min. NEleisk pytest. Telegram TRUMPAI.
Fail-safe €0. TIK privatus hera-vault. Viešo repo NELIESK. Kodo NELIESK. Necommit'ink raktų.

KONTEKSTAS: Vartotojas patvirtino. „Adaptive Parallel Reasoning" (APR, Berkeley BAIR) — ~90% GPU/model-training
(SFT+RL kad modelis emituotų <Parallel> žetonus + inference-engine KV-cache valdymas) → future-gpu track (pagal
standing rule). BET vienas engine-agnostic grūdas (ThreadWeaver client-side fork-join) — galima ateities planning-
loop refinement, ribota mūsų budget/rc124 disciplinos.

1) FUTURE-GPU: rask growth „Adaptive Parallel Reasoning" (growth/2026-07-12-*7u90ag*). Pažymėk
   „hardware: future-gpu · STATUS: priimta į future-gpu track (human-gate 2026-07-12)". Įrašyk į FUTURE_GPU.md
   (kodėl-GPU: APR reikalauja modelio treniravimo SFT+RL + inference-engine KV-cache; nauda su GPU: adaptyvus
   lygiagretus mąstymas — mažesnė latencija/critical-path be tikslumo praradimo).

2) CROSS-NOTE (aktyvus track, planning-loop v2 kandidatas): docs/ROADMAP.md prie Fazės 7 pridėk:
   „Fazė 7 v2 kandidatas (iš APR/ThreadWeaver): client-side fork-join (map-reduce ant LLM kvietimų, engine-agnostic,
    BE GPU/treniravimo) — planuotojas adaptyviai nusprendžia kada skaidyti į lygiagrečias subgoal-gijas.
    ⚠️ RIBOTA: lygiagretūs API kvietimai = lygiagretus budget = rc124 rizika → reikia HARD cap. NE DABAR.
    Principas patvirtintas: 'structure-only rewards apgaunami' = ta pati reward-hacking pamoka (tripwire/SkillOpt)."
   Ir APR growth faile pridėk vieną eilutę: „SĖKLA aktyviam track'ui: ThreadWeaver client-side fork-join → žr.
   ROADMAP Fazė 7 v2 (budget-gated, ne dabar)."

3) WIKI: hera_wikilink.py (arba lint) — parodyk orphan/dangling.
4) TRAJEKTORIJA: įrašyk (curation/future-gpu + planning-v2-seed).
5) DURABILUMAS: vault commit („APR -> future-gpu + planning-loop v2 seed note") + push privatus hera-vault.
   Viešo NELIESK.

TELEGRAM (per HERA botą, trumpai): (1) APR įdėta į future-gpu track (GPU/training), (2) ištraukta sėkla:
ThreadWeaver client-side fork-join → planning-loop v2 kandidatas (budget-gated, ne dabar), (3) wiki OK,
(4) „APR SUTVARKYTA — GPU dalis kaupiama, taikoma sėkla pažymėta ateičiai".
