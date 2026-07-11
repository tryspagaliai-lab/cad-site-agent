UŽDUOTIS — 5b FAZĖ: SKILL-KAUPIMO KILPA (SIŪLO naują skill; sandbox+benchmark+human-gate; NE auto-merge). <13 min.
NEleisk pytest. Telegram TRUMPAI. €0. Fail-safe. LLM kvietimams timeout 60s, NO retry (anti-rc124).

⚠️ GOVERNANCE (nepažeisti): kilpa TIK SIŪLO. NIEKO neauto-merge'ina į gyvą vault. Naujas skill = staged proposal,
draft/human_gate. Bazinės kilpos/RIC guard/governance/sandbox/benchmark kodo NIEKADA neliesti (užtikrina sandbox
ro-bind + rašymas tik į worktree skills/).

SAUGUMAS: raktų nespausdink/necommit'ink. Jei liesta kodą — push į PRIVATŲ hera-core-backup.

KONTEKSTAS: turim sandbox (5a, hera_sandbox.py) + matuoklį (hera_bench). Dabar saugi savęs-tobulinimo forma —
skill-akrecija (Voyager): sistema rašo NAUJUS skill failus, bazinis kodas nepaliestas.

1) hera_accretion.py: funkcija propose_skill(gap_description) ->
   {proposed, benchmark_ok, no_regression, proposal_path, diff_summary, decision}. Žingsniai:
   a) DRAFT: 1 LLM kvietimas (Gemini flash, 60s, no retry) -> naujo skill juodraštis (skills/<slug>/SKILL.md su
      tuple, turiniu, provenance, status:draft, human_gate:true). Fail-safe: klaida -> {proposed:false}.
   b) IZOLIUOTAS RAŠYMAS: git-worktree kopija; įrašyk skill TIK į worktree skills/ (gyvas vault nepaliestas).
   c) BENCHMARK-VARTAI (sandbox'e): paleisk hera_bench.run() worktree'je per hera_sandbox -> pass_rate turi būti
      >= baseline (9/9), be regreso. Jei regresas -> decision=reject (nepriimam).
   d) (jei taikoma) counterfactual replay validacija.
   e) STAGE PROPOSAL: proposals/accretion/<slug>-<data>.md (arba .json) su skill juodraščiu + benchmark rezultatu +
      diff santrauka; įrašyk į OPEN_QUESTIONS.md eilutę „skill-akrecija laukia patvirtinimo: <slug>". decision=propose.
   f) NIEKO nemerge'ink į gyvą /opt/hera-vault/skills/ — tik staged proposal. Žmogus/kuratorius tvirtina vėliau.
2) JUNGIKLIS HERA_ACCRETION=1 (default 1; =0 išjungia). Kilpa STANDALONE / rankinis trigeris — NEauto-paleisk ant
   kiekvieno ingest (kad €0 ir kad žmogus valdytų). Įrašyk =1 /root/hera.env.
3) TESTAS (MAŽAS): propose_skill("Trumpas skill: kaip saugiai izoliuoti agento vykdymą su bubblewrap no-net") ->
   parodyk: sukurtas draft skill (kelias, be viso turinio), benchmark sandbox'e pass_rate (turi likti 9/9),
   proposal staged (kelias), decision=propose, IR patvirtink kad gyvas /opt/hera-vault/skills/ NEPAKITĘS
   (nieko nemerge'inta). Fail-safe: LLM/sandbox klaida -> decision=reject/error, nekabo, nieko nepakeičia.
4) BENCHMARK REGRESIJA (gyvas): hera_bench.run() gyvai -> 9/9 nepakito (kilpa standalone, neturi liesti).
5) DURABILUMAS: kopija į n8n/hera/ + push į PRIVATŲ hera-core-backup. Viešo NELIESK.

TELEGRAM (per HERA botą, trumpai, be raktų): (1) hera_accretion.py veikia (draft->sandbox->benchmark->proposal),
(2) testas: skill pasiūlytas, benchmark 9/9, staged proposal, gyvas vault NEPAKITĘS (nieko auto-merge),
(3) fail-safe OK, (4) benchmark gyvai nepakito, (5) backup OK, (6) „SKILL-KAUPIMO KILPA PARUOŠTA (5b)".
