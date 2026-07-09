UŽDUOTIS — SKILL DRAFT: VERSLO IDENTITETAS + SVETAINĖ AI ĮRANKIAIS (LENGVA, TIK VAULT TURINYS, BE KODO KEITIMO). <10 min.
NEperstatyk servisų, NEleisk pytest, NEkeisk hera_*.py kodo. Atsiskaityk Telegram TRUMPAI.

SAUGUMAS: raktų nespausdink/necommit'ink/nerodyk.

KONTEKSTAS: šiandien ~20:22 per pipeline praėjo YouTube gido ištraukimas („Claude Design 2026 gidas", fiktyvi
„Apex Roofing" įmonė). Claude (kuratorius, antras vartas) verdiktas: čia YRA atkartojama metodika -> SKILL draft
(ne growth). Domain fit HERA'i vidutinis (~5-6/10), bet praktinė vertė vartotojo verslui aukšta.

1) SKILL DRAFT: sukurk /opt/hera-vault/skills/verslo-identitetas-ir-svetaine-ai-irankiais/SKILL.md
   (status: draft, human_gate — kaip visi skills; NIEKO nepromote'ink). Tuple:
   intent: nuo nulio sukurti verslo identitetą, svetainę, reklamas, skaidres ir sutartį AI įrankiais per 1 dieną
   method: workflow žemiau
   difficulty: vidutinis
   tool_hint: Claude Design, Higgsfield, Claude Code, Netlify CLI

   TURINYS — atskirk DVI dalis:

   A) NESENSTANTIS KARKASAS (pagrindinė vertė):
      1. Dizaino sistema PIRMA — įmonės pavadinimas + pitch, logotipas SVG (vektorinis, redaguojamas tekstas/spalvos),
         šriftų pora + spalvų paletė parenkamos atskiru LLM pokalbiu (pigesniu modeliu), viskas į brand guide
         su komponentais (kortelės, mygtukai, semantinės būsenos) PRIEŠ kuriant bet kokį asset'ą.
      2. Asset'ai generuojami PAGAL dizaino sistemą — svetainė, skaidrės, dokumentai, video reklamos naudoja tą pačią sistemą.
      3. Placeholder pattern'as: svetainė kuriama su vaizdų vietos užpildais + AI pati pateikia prompt'ą ir aspect
         ratio kiekvienam vaizdui -> vaizdai generuojami atskirai pagal tuos prompt'us -> įterpiami pagal numerį.
      4. Video reklama = 3 dalių struktūra (problema -> reakcija -> sprendimas), kiekviena scena generuojama atskirai,
         montažas + tekstas + CTA atskiru žingsniu.
      5. Viskas eksportuojama į VIENĄ repo (Claude Code), deploy su env kintamaisiais secrets'ams
         (ADMIN_USERNAME/ADMIN_PASSWORD), admin skydelis leads peržiūrai.
   B) ĮRANKIŲ SNAPSHOT 2026-07 (sensta, keisis): Claude Design (dizaino sistemos, slides, documents, animacijos);
      Higgsfield: Recraft V4.1 vector mode (SVG logo), Seedream 4.5 (foto), Kling 3.0 (video); Netlify CLI deploy.

   PROVENANCE + EPISTEMINĖ ŽYMA (privaloma skill'e): šaltinis — YouTube marketingo turinys (aifoundations.io promo),
   metodika atrodo reali, bet teiginiai NEPATIKRINTI nepriklausomai; žingsniai gali neveikti pažodžiui. Promo dalių
   (kursai, prenumeratos, mentorystė) į skill'ą NEDĖK.

2) Jei selektorius/taryba šiam ingest'ui jau sukūrė savo skill/growth failą iš to paties turinio — NEdubliuok:
   palik jų failą, o šitą draft'ą sukurk kaip kuratoriaus versiją su nuoroda į aną (arba papildyk aną, jei paprasčiau).

3) TRAJEKTORIJA: jei paprasta — įrašyk veiksmą į trajectories (tipas: curation/skill-draft). Jei nepatogu — praleisk.

TELEGRAM (trumpai, be raktų): (1) skill kelias + status draft, (2) ar buvo selektoriaus dublis ir kaip išspręsta,
(3) šio ingest'o selektoriaus balas ir tarybos verdiktas jei randami loguose/proposals, (4) „SKILL DRAFT BAIGTA".
