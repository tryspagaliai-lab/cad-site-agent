UŽDUOTIS — Produkto vizija (BE pavadinimo) + PURGE „Apex". <8 min. NEleisk pytest. Telegram TRUMPAI. Fail-safe.
TIK privatus hera-vault. Viešo repo NELIESK. Kodo NELIESK. Idempotentiška — vienoda galutinė būsena nesvarbu ar
ankstesnė užduotis spėjo įvykti.

KONTEKSTAS: Vartotojas nusprendė — pavadinimas „Apex" NETURI egzistuoti niekur. Turinį (produkto viziją, roadmap
fazes 6/7/8) IŠLAIKYK, tik BE jokio prekės ženklo. Neutralūs žodžiai: „sistema" / „produktas".

1) PURGE (jei ankstesnė užduotis spėjo įrašyti „Apex"):
   - jei yra /opt/hera-vault/docs/APEX_ROADMAP.md -> pervadink (git mv) į /opt/hera-vault/docs/ROADMAP.md.
   - visuose privataus vault failuose pakeisk bet kokį „Apex" (visos variacijos) -> „sistema"/„produktas"/pašalink
     pagal kontekstą; „APEX_ROADMAP" -> „ROADMAP".

2) PROFILIS (auto-atmintis, BE pavadinimo): į /opt/hera-vault/profile/USER_STRATEGIC_PROFILE.md užtikrink sekciją
   „## Produkto vizija (2026-07-11)" su (jei jos dar nėra — sukurk; jei yra su „Apex" — pataisyk):
   - Pozicionavimas: standartinis AI = genialus praktikantas su amnezija (be verslo konteksto). Šis produktas = iš
     pagrindų kitaip — autonominis partneris, kuris atperka vertingiausią resursą: dėmesio sutelkimą (focus).
     NE fancy wrapper aplink API — sistema veiksmui ir kontekstui.
   - 3 principai: (1) Nuolatinė atmintis + gyvas redaguojamas projektų žurnalas (žino prie ko dirbama, kas
     sustabdyta, kas toliau). (2) Specializuoti agentai — komanda vietoj vieno modelio: Socialiniai tinklai,
     Operacijos (Ops), Dizainas; kiekvienas savo tikslas+įrankiai+planning loop (subgoals→draft→self-critique).
     (3) Tikri įrankiai, tikri veiksmai — Ops: kalendorius+laiškai iš domeno; Social: Instagram publish.

3) ROADMAP (BE pavadinimo): užtikrink /opt/hera-vault/docs/ROADMAP.md (status: PROPOSED, laukia patvirtinimo):
   - Fazė 6 — Gyvas projektų žurnalas (context retention): projects/<slug>/STATE.md, auto-skaitomas/atnaujinamas;
     jungiasi prie NapMem L1-L4. Rizika: žema.
   - Fazė 7 — Specialist agents + Planning Loop (Ops/Social/Design, subgoals→draft→self-critique, Reflexion-tipo,
     HARD budget/timeout, perpanaudoja council+CoVe; išvestis=draft). Rizika: žema-vidutinė.
   - Fazė 8 — Tool Use (Ops: kalendorius+laiškai; Social: Instagram): default DRAFT/READ-ONLY, human „tvirtinu"
     prieš siuntimą/publikavimą, recipient/domain allowlist, jokio masinio siuntimo, audit log, kredencialai TIK
     .env (niekada necommit), reversibilumas. Rizika: AUKŠTA. Instagram = reikia IG Business + Meta Graph API +
     app review (NE trivialiai €0). Atviri sprendimai: email provideris, kalendorius, autonomijos lygis.

4) PATIKRA: `grep -ri "apex" /opt/hera-vault/` (darbinė būsena, ne git istorija) -> turi būti 0. Parodyk tuščią.

5) DURABILUMAS: vault commit („product vision without brand name, roadmap phases 6/7/8, purge Apex") + push
   privatus hera-vault. Viešo cad-site-agent NELIESK. Kodo NELIESK.

TELEGRAM (per HERA botą, trumpai): (1) „Apex" pavadinimas pašalintas visur (grep 0), (2) vizija+roadmap išlaikyti
BE prekės ženklo (ROADMAP.md, fazės 6/7/8 PROPOSED), (3) „PAVADINIMAS IŠVALYTAS, VIZIJA IŠLAIKYTA".
