UŽDUOTIS — hera_semsearch KOKYBĖS testas: paleisk realias užklausas, parodyk top-3. READ-ONLY (tik query, jokių pakeitimų). <10 min.
NEleisk pytest. Fail-safe. €0. Ataskaita TIK į HERA botą.

KONTEKSTAS: Fazė 17 hera_semsearch gyvas (fastembed, def 0, index=growth+skills+memory_index). Testuojam ar semantinis recall
tikrai geras + ką praleidžia (index apimtis). Rezultatas nulems ar plėsti index (sessions/proposals/profile) ir ar integruot į runner.

ŽINGSNIAI:
1) Įsitikink index šviežias: `HERA_SEMSEARCH=1 python3 <kelias>/hera_semsearch.py build` (inkrementinis, greitas). 
2) Paleisk ŠIAS 8 užklausas (mišrios LT+EN, testuoja SEMANTIKĄ ne raktažodžius; kiekvienai top-3 su path+score+snippet):
   a) „kaip apsisaugoti nuo begalinių LLM ciklų ir pergalvojimo"        (turėtų rast loop-guard/PUMA/anti-rc124)
   b) „mokytis iš klaidų ir jas taisyti automatiškai"                    (EMG/diffrules)
   c) „patvirtinti kad darbas atliktas prieš pradedant"                  (validator-first/model-synthesis)
   d) „3D modeliavimo ir vizualizacijos AI įrankiai"                     (3ds Max / AutoCAD MCP natos)
   e) „žemės ūkio dirbtinis intelektas ūkininkams"                       (agro)
   f) „sujungti kelis skirtingus AI modelius vienam sprendimui"          (council / model-synthesis)
   g) „semantinė atmintis ir paieška tarp pokalbių"                      (self-ref: semsearch/MemPalace/atmintis)
   h) „vartotojo tikslai ir 3D dizaino patirtis"                         (profile — TIKĖTINA MISS, nes profile ne index'e)
3) Kiekvienai užklausai įvertink: PATAIKĖ (relevantus top-1) / DALINAI / MISS. Ypač pažymėk h) ir f) — ar praleido dėl index apimties
   (profile/sessions/proposals neindeksuoti), ar dėl semantikos.

ATASKAITA (HERA botas): 8 užklausos × top-1 (path+score) + verdiktas PATAIKĖ/DALINAI/MISS; bendra išvada — ar semantika gera;
kurios užklausos praleistos DĖL INDEX APIMTIES (rekomendacija plėst sessions/proposals/profile ar ne). Nieko nekeisk.
