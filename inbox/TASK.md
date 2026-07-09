UŽDUOTIS — GROWTH UŽRAŠAS + DISTILL PAPILDYMAS (LENGVA, TIK VAULT TURINYS, BE KODO KEITIMO). <10 min.
NEperstatyk servisų, NEleisk pytest, NEkeisk hera_*.py kodo. Atsiskaityk Telegram TRUMPAI.

SAUGUMAS: raktų nespausdink/necommit'ink/nerodyk.

KONTEKSTAS: šiandien (2026-07-09 ~19:41) per pipeline praėjo Schmidhuberio interviu ištraukimas („Unsupervised
Learning" podcast, Jacob Effron / Redpoint). Claude (kuratorius, antras vartas) peržiūrėjo ir verdiktas: domain fit
mišrus (~6/10), verta GROWTH užrašo (ne SKILL — nėra atkartojamos metodikos), plius 3 principai papildo HERA dizainą.

1) GROWTH UŽRAŠAS: sukurk /opt/hera-vault/growth/2026-07-09-schmidhuber-godel-smalsumas.md su šiuo turiniu
   (gali performuluoti, esmę išlaikyk):

   Šaltinis: interviu su Jürgen Schmidhuber, „Unsupervised Learning" (Jacob Effron, Redpoint), ištraukta per
   HERA pipeline 2026-07-09. Kuratoriaus (Claude) verdiktas: growth, ne skill. On-domain dalys HERA'i:

   a) GÖDELIO MAŠINOS PRINCIPAS (2003): sistema keičia savo kodą TIK pateikusi įrodymą, kad pakeitimas padidins
      naudingumą. HERA atitikmuo (jau įgyvendinta): outer-loop -> kontrafaktinis replay (PAGERĖJO/PABLOGĖJO) ->
      staged į proposals/ -> žmogaus gate. Replay = praktinė Gödelio „įrodymo" aproksimacija. Išvada-principas:
      pakeitimas be replay įrodymo = automatiškai atmetamas, nepriklausomai nuo LLM verdikto (formuluotė būsimam
      reward-hacking sargui). NIEKADA auto-promote — dabar tai turi teorinį pagrindą.

   b) DIRBTINIS SMALSUMAS / SUSPAUDIMO PROGRESAS (1990): vidinis reward = skirtumas tarp bitų, reikalingų duomenims
      aprašyti prieš ir po mokymosi. HERA pritaikymas: stagnaciją matuoti ne tik balų kreive, bet „ar naujas
      ingest'as prideda išmokstamo naujumo" — jei selektoriaus balai aukšti, bet vault'e konceptai dubliuojasi
      (naujumo nėra), STAGNATION-REDIRECTION heartbeat turi nukreipti kitur. (DISTILL kandidatas #4.)

   c) TINGUMO PRINCIPAS: intelektas = tikslo siekimas su kuo mažiau resursų; kaštai įtraukti į tikslo funkciją.
      HERA pritaikymas: į trajektorijų reward įtraukti kaštų dedamąją (LLM kvietimų sk., retry'ai, digest dydis) —
      pigesnis kelias iki to paties rezultato = aukštesnis reward. Dera su €0 stack'u. (DISTILL kandidatas #5.)

   Off-domain (neplėtoti): investicijų burbulas/CapEx, robotikos hardware, MOF chemija, saugumo nuomonės,
   tiesiniai transformatoriai (HERA netreniruoja modelių).

2) DISTILL SĄRAŠO PAPILDYMAS: jei /opt/hera-vault/skills/ yra skill'as swarm-research-git-atmintis (ar panašiu
   vardu iš SwarmResearch ingest'o) — pridėk jame sekciją „DISTILL kandidatai HERA'i (draft, human_gate)" su
   kandidatais #4 (compression-progress stagnacijos metrika) ir #5 (kaštų dedamoji reward'e) iš aukščiau, ir
   nuoroda į growth užrašą. Jei tokio skill'o NĖRA — vietoj to sukurk
   /opt/hera-vault/proposals/distill-kandidatai-2026-07-09.md (draft, human_gate=True) su abiem kandidatais.
   NIEKO nepromote'ink, NIEKO nekeisk kode — tik staged tekstas.

3) TRAJEKTORIJA: jei paprasta — įrašyk šį veiksmą į trajectories (tipas: curation/growth). Jei nepatogu — praleisk.

TELEGRAM (trumpai, be raktų): (1) growth užrašo kelias, (2) kur padėti DISTILL kandidatai (skill'e ar proposals/),
(3) „GROWTH+DISTILL BAIGTA".
