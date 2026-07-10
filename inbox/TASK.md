UŽDUOTIS — VAULT HIGIENA: EVICTION ŽYMĖJIMAS + DIENOS CHANGELOG + OPEN_QUESTIONS (VIENA UŽDUOTIS, VISKAS
DETERMINISTINIS — BE LLM KVIETIMŲ). <12 min. NEleisk pytest. Telegram TRUMPAI.

SAUGUMAS: raktų nespausdink/necommit'ink/nerodyk. NIEKO netrink — tik žymėk (human gate!).

KONTEKSTAS: LLM-Wiki webinaro (o3srk6, council promote_candidate) DISTILL #6-#8, vartotojas diegimą patvirtino.

1) #6 EVICTION ŽYMĖJIMAS (Loop C): savaitinės konsolidacijos metu pažymėk kandidatus archyvavimui —
   įrašai (growth/skills), kurių: (a) nė karto neskaitė naršymo kilpa / RAG (pagal trajektorijas),
   (b) žemas importance (<0.3 ar pan.), (c) superseded dublikatai. Žymė frontmatter'yje:
   eviction_candidate: true + priežastis. NETRINK ir NEarchyvuok pats — tik žymė + sąrašas changelog'e,
   sprendžia žmogus/kuratorius. Deterministinis (statistika iš trajektorijų + frontmatter), be LLM.
2) #7 DIENOS CHANGELOG (Loop B): į Loop B Telegram raportą pridėk „kas naujo vault'e per parą" bloką —
   pigiausias kelias: /opt/hera-vault yra git repo (sync cron commit'ina) -> git log --since=1day --stat
   santrauka: +N skills, +M growth, pakeisti X, eviction kandidatų Y. 3-5 eilutės max.
3) #8 OPEN_QUESTIONS.md: sukurk /opt/hera-vault/OPEN_QUESTIONS.md (jei nėra). Du pigūs rašymo hook'ai:
   (a) hera_council: kai balsai stipriai išsiskiria (pvz. score spread >4 tarp juror'ių) — append klausimas
   „ar <kandidatas> vertas? taryba pasidalino X vs Y"; (b) naršymo kilpa: kai atsakymas nerastas
   (found=false) — append „vault'e nėra atsakymo į: <klausimas>". Su data, be dublikatų (jei toks pat
   klausimas jau yra — praleisk). Loop B raporte — atvirų klausimų skaičius.
4) TESTAS (greitas, deterministinis): (a) Loop C dry-run ar tiesiog funkcijos kvietimas — eviction kandidatų
   sąrašas sugeneruotas (kiek, kokie); (b) Loop B raporto generavimas — changelog blokas matosi;
   (c) dirbtinai įrašyk 1 testinį open question per hook'ą — failas atsirado/papildytas.
5) DURABILUMAS: kodo kopija į /opt/cad-site-agent/n8n/hera/ (be push į viešą) + push į PRIVATŲ hera-core-backup.

TELEGRAM (trumpai, be raktų): (1) eviction kandidatų kiek pažymėta (ir 2-3 pavyzdžiai), (2) changelog blokas
Loop B raporte — pavyzdys, (3) OPEN_QUESTIONS.md sukurtas + hook'ai veikia, (4) backup OK, (5) „VAULT HIGIENA BAIGTA".
