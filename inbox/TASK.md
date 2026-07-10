UŽDUOTIS — PROPOSALS SPRENDIMAI + VAULT TVARKYMAS (KURATORIAUS/VARTOTOJO VERDIKTAI, MAŽI FAILŲ KEITIMAI). <10 min.
NEleisk pytest. Vienintelis kodo keitimas — selektoriaus prompt'as (2 sakiniai). Telegram TRUMPAI.

SAUGUMAS: raktų nespausdink/necommit'ink/nerodyk.

KONTEKSTAS: vartotojas (galutinis vartas) su kuratoriumi (Claude) peržiūrėjo 3 proposals iš 20260707T200433Z.
Verdiktai: #01 PROMOTE, #02 REJECT, #03 PROMOTE. Plius vault tvarkymas ir backup klaidos ištaisymas.

1) DIEGTI #01 ir #03 į hera_select.py (PIRMA — failo backup kopija šalia, pvz. hera_select.py.bak-<data>):
   append prie selektoriaus prompt'o abu sakinius iš proposals/approved/...-01/prompt_clause.txt ir ...-03/
   prompt_clause.txt (jie validuoti per replay). Greitas testas: replay ant test-file-001 -> score turi būti 0.0.
   Proposal'ų failuose pažymėk status: PROMOTED (data, kas).

2) #02 ATMESTI: proposals/approved/...-02/proposal.md pažymėk status: REJECTED su motyvacija:
   „Vartotojo sprendimas 2026-07-10: HERA domenas NESIAURINAMAS — sistema mokosi plačiai (hardware, robotika,
   fizinis pasaulis įskaitytinai); vertę sprendžia balai ir taryba, ne tematiniai atmetimo filtrai. Papildomai:
   klauzulė keltų riziką vartotojo verslo (CAD/statyba) turiniui; n=2 imtis; selektorius tuos atvejus ir taip
   įvertino teisingai." Klauzulės į kodą NEDĖK.

3) TAISYKLĖ Į PROFILE.md: pridėk prie preferencijų: „HERA domenas NIEKADA nesiaurinamas — jokių tematinių
   atmetimo taisyklių selektoriuje/prompt'uose; bet koks outer-loop pasiūlymas, siaurinantis priimamų temų ratą,
   atmetamas automatiškai (vartotojo direktyva 2026-07-10, žr. proposals ...-02 REJECTED)."

4) SKILL DUBLIO MERGE: github-repo-import-optimization ir github-projekto-importavimas-i-ai-studio — iš to paties
   video (2ls50k/ne08n5 dublis). Palik turiningesnį, antrą pažymėk superseded (kaip C01 pattern'as), su nuoroda
   į paliktąjį. Importance/nuorodas perkelk jei yra.

5) BACKUP KLAIDOS TAISYMAS (svarbu): NapMem-B push nuėjo į VIEŠĄ cad-site-agent repo (šaka
   claude/napmem-phase-b-l4-profile) — POLITIKA: HERA kodas viešame repo NIEKADA; tik lokali kopija
   /opt/cad-site-agent/n8n/hera/ (be push) + privatus hera-core-backup. Padaryk: (a) push'ink dabartinį
   /opt/hera-processor/ į hera-core-backup (askpass, secret-scan), (b) kai push patvirtintas — IŠTRINK viešą šaką:
   git push origin --delete claude/napmem-phase-b-l4-profile (arba per API). Ateičiai įsimink šią politiką.

TELEGRAM (trumpai, be raktų): (1) #01+#03 įdiegti, test-file-001 replay score, (2) #02 REJECTED, (3) taisyklė
PROFILE.md, (4) merge atliktas — kuris paliktas, (5) hera-core-backup push OK + vieša šaka ištrinta,
(6) „PROPOSALS+TVARKYMAS BAIGTA".
