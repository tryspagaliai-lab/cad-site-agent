UŽDUOTIS — HERA Fazė 4: skill-tuple + struktūros-optimizavimo outer-loop + minimalus RIC.
Dirbk autonomiškai (superpowers OK). NELIESK veikiančių Fazės 2/3 (ingest+extract+processor+selector+
trajectories+skill-output+replay lieka) — tik PRAPLĖSK. Feasible tik NEMOKAMAM stack'ui: Gemini free,
JOKIO treniravimo/RL/svorių/GPU. Atsiskaityk į Telegram TRUMPAI, aiškiu galutiniu statusu.

1) SKILL-TUPLE SCHEMA. SKILL.md frontmatter praplėsk tipizuotu rinkiniu:
   name, description, when_to_use, PLUS tuple: intent (ι – esminis principas), method (μ – procedūra),
   difficulty (δ – 1..10), tool_hint (τ – nuoroda į kodą/įrankį jei yra). Perkurk esamą
   skills/ai-wargaming-metodika/SKILL.md į šį formatą (pavyzdys).
   Įdiek 3-LYGIŲ ĮKĖLIMĄ: L1 metaduomenys (visada), L2 pilnos instrukcijos (tik pagal trigerį/atranką),
   L3 resursai (skriptai/nuorodos, dinamiškai). Ir SELEKTYVI ATRANKA + PRUNING: neįkelk visų skills iš karto
   (lock-in/konteksto perkrovos problema) — atrink pagal užduotį; parodyk paprastą retrieval funkciją.

2) STRUKTŪROS-OPTIMIZAVIMO OUTER-LOOP (AutoMem #1). CLI /opt/hera-processor/hera_optimize.py:
   meta-LLM (Gemini free) peržiūri ATDP-lite trajektorijas → diagnozuoja pasikartojančias silpnybes/klaidas →
   SIŪLO konkrečias pataisas HERA prompt'ams / skill bibliotekai / schemai → per hera_replay.py (kontrafaktinį
   pakartojimą) VALIDUOJA, ar pagerėja → tik tada priima. Pasiūlymus rašo į /opt/hera-vault/proposals/.
   SVARBU: NIEKADA automatiškai netrina esamų skills/growth — versijuok/append. Priima tik po replay-validacijos.

3) MINIMALUS RIC (saugos gardas). Įdiek denylist gardą HERA vykdomoms shell/tool operacijoms IR outer-loop
   pasiūlymams: BLOKUOK tik NEATŠAUKIAMAS katastrofas — `rm -rf` sisteminiuose keliuose, disko trynimas,
   DB drop, `git push --force`, core servisų (n8n, hera-*, cron) naikinimas, /opt/hera-vault ar n8n duomenų trynimas.
   VISKAS kita (kodas, failai, diegimai, commit'ai lokaliai) — auto, be klausimų. Panaudok esamą
   guard_layer_delete.py šabloną kaip pavyzdį. Užblokuota operacija → log + Telegram įspėjimas, ne tylus fail.

4) SELF-TEST: (a) parodyk perkurtą SKILL.md su tuple, (b) paleisk hera_optimize.py ant esamų trajektorijų ir
   parodyk bent 1 pasiūlymą + replay verdiktą, (c) pademonstruok, kad RIC blokuoja pavyzdinę `rm -rf` komandą
   bet praleidžia normalų failo rašymą.

5) DURABILUMAS: kodą kopijuok į /opt/cad-site-agent/n8n/hera/. Push nedaryk (nėra creds).

Į Telegram: kas pridėta (skill-tuple/3-lygiai/outer-loop/RIC), self-test rezultatai, ir aiškiai
„FAZĖ 4 BAIGTA" arba ko trūksta.
