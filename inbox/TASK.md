UŽDUOTIS — SKUBU: išvalyk bot-token pėdsakus iš /root/.bash_history. <5 min.
NEleisk pytest. Fail-safe. €0. RAKTŲ/REIKŠMIŲ NESPAUSDINK NIEKADA (nei istorijoje, nei ataskaitoje). Ataskaita TIK į HERA botą.

KONTEKSTAS: setup metu bot-token'ai pateko į root komandų istoriją (echo 'DESIGN_BOT_TOKEN=...' ir kt., + viena
standalone token eilutė). Vartotojas NEregeneruoja — vietoj to valom pėdsaką iš history. Env failo (ai_digest.env)
NELIESK — token'ai TEN turi likti (jie ten ir reikalingi).

ŽINGSNIAI (deterministiška, per python3 — nes VPS hardening blokuoja grep/sed ant kai kurių failų):
1) Python3 vienkartiniu skriptu apdorok TIK `/root/.bash_history`:
   - Perskaityk eilutes.
   - IŠMESK bet kurią eilutę, kuri atitinka BENT VIENĄ:
     • turi `_BOT_TOKEN=` (echo/sed komandos su token'ais)
     • atitinka regex `\b\d{6,}:AA[\w-]{20,}\b` (Telegram token forma — standalone token eilutė)
     • turi `PASTE_TOKEN`
   - Perrašyk failą su likusiomis eilutėmis (atominis: temp→os.replace). Teises palik kaip buvo (chmod 600 jei buvo).
   - Išvesk TIK: kiek eilučių pašalinta ir kiek liko. JOKIŲ eilučių turinio/reikšmių.
2) Jei yra ir /root/.python_history ar kitas akivaizdus history su token'ais — tas pats (bet NEliesk ai_digest.env,
   .env, konfigų, kodo). TIK history failai.
3) Patikrink (be turinio): ar po valymo `\d{6,}:AA` likučių history'je 0? Išvesk TRUE/FALSE.

RIBOS: €0. Liesk TIK history failus. Env/kodo/konfigų NELIESK. Reikšmių/token'ų NIEKADA nespausdink. Anti-rc124
(grynas failo apdorojimas, be tinklo/LLM).

ATASKAITA (HERA botas, TRUMPAI, be reikšmių): (a) /root/.bash_history: pašalinta N eilučių, liko M; (b) token-likučių
history'je: 0/ne; (c) ar kiti history failai tvarkyti? (d) ai_digest.env nepaliestas patvirtinta? (e) 1 eil. done.
