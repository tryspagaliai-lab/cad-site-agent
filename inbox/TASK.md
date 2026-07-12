UŽDUOTIS — AUTO-ATMINTIS + PREP: įrašyk „Apex" produkto viziją į PRIVATŲ vault + sukurk roadmap. <8 min.
NEleisk pytest. Telegram TRUMPAI. Fail-safe. TIK privatus hera-vault. Viešo repo NELIESK. Kodo NELIESK.

KONTEKSTAS: Vartotojas pateikė strateginę produkto viziją „Apex" (autonominis partneris kuris atperka jo
dėmesį/focus). Tai reikšmingas faktas → auto-atmintis į privatų profilį + roadmap kad etapas išliktų tarp sesijų.
NIEKO nediegti, nekurti kodo — tik dokumentacija privačiame vault.

1) PROFILIS (auto-atmintis): į /opt/hera-vault/profile/USER_STRATEGIC_PROFILE.md pridėk sekciją
   „## Apex — produkto vizija (2026-07-11)" su:
   - Pozicionavimas: standartinis AI = genialus praktikantas su amnezija (be verslo konteksto). Apex = iš pagrindų
     kitaip — autonominis partneris, kuris atperka vertingiausią resursą: dėmesio sutelkimą (focus). NE fancy
     wrapper aplink API — sistema veiksmui ir kontekstui.
   - 3 principai:
     1. Nuolatinė atmintis (Persistent Memory) + gyvas, redaguojamas projektų žurnalas (Projects Log): žino prie
        ko dirbama, kas sustabdyta, kas toliau. Nereikia aiškinti iš naujo.
     2. Specializuoti agentai (Specialist Agents): komanda vietoj vieno bendro modelio — Socialiniai tinklai,
        Operacijos (Ops), Dizainas. Kiekvienas: savo tikslas + savo įrankiai + planning loop
        (subgoals → draft → self-critique). Sudėtingi daugiažingsniai darbai, ne tik atsakymai.
     3. Tikri įrankiai, tikri veiksmai (Real Tools, Real Action): Ops = skaito kalendorių + kuria įvykius, ruošia
        juodraščius + siunčia laiškus iš vartotojo domeno. Social = publikuoja tiesiai į Instagram. Sujungta su
        tais pačiais įrankiais kuriuos naudoja vartotojas.
   Necommit'ink jokių raktų/asmens duomenų virš to kas jau vizijoje.

2) ROADMAP (prep durabilumas): sukurk /opt/hera-vault/docs/APEX_ROADMAP.md (status: PROPOSED, laukia vartotojo
   patvirtinimo) su fazėmis (perpanaudoja esamą HERA infrastruktūrą, €0, fail-safe, human-gate):
   - Fazė 6 — Gyvas projektų žurnalas (context retention): projects/<slug>/STATE.md, auto-skaitomas užduoties
     pradžioje, auto-atnaujinamas pabaigoje; jungiasi prie NapMem L1-L4 + auto-atminties taisyklės. Rizika: žema.
   - Fazė 7 — Specialist agents + Planning Loop: Ops/Social/Design agentai; kiekvienas subgoals→draft→self-critique
     (Reflexion-tipo, HARD budget/timeout anti-rc124); perpanaudoja council+CoVe. Išvestis=draft, nulis išorinės
     rizikos. Rizika: žema-vidutinė.
   - Fazė 8 — Tool Use (Ops: kalendorius+laiškai iš domeno; Social: Instagram publish): PASKUTINĖ, labiausiai
     apsaugota. RĖMAI: default DRAFT/READ-ONLY (nieko nesiunčia/nepublikuoja be human „tvirtinu"), recipient/domain
     allowlist, jokio masinio siuntimo, audit log, kredencialai TIK .env (niekada necommit), reversibilumas kur
     įmanoma. Rizika: AUKŠTA (veiksmai vartotojo vardu, negrįžtama).
   - ATVIRI SPRENDIMAI (laukia vartotojo): laiškų provideris (SMTP/Zoho/Google Workspace?), kalendorius
     (Google/CalDAV?), Instagram publikavimas (reikia IG Business/Creator + Meta Graph API + app review — NE
     trivialiai €0, pažymėk sąžiningai), autonomijos lygis (draft-only startas rekomenduojamas).

3) DURABILUMAS: vault commit+push (privatus hera-vault). Viešo cad-site-agent NELIESK. Kodo NELIESK.

TELEGRAM (per HERA botą, trumpai): (1) Apex vizija įrašyta į privatų profilį (auto-atmintis), (2) APEX_ROADMAP.md
sukurtas (fazės 6/7/8, PROPOSED, laukia patvirtinimo), (3) „ETAPAS PARUOŠTAS — laukia platformų sprendimų (Fazė 8)".
