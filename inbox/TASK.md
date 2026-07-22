UŽDUOTIS — hera_semsearch KOKYBĖS testas #2: NAUJOS 8 užklausos (ne tos pačios kaip pirmam teste). READ-ONLY. <10 min.
NEleisk pytest. Fail-safe. €0. Ataskaita TIK į HERA botą. Nieko nekeisk.

KONTEKSTAS: nepriklausomas kokybės signalas su KITU užklausų rinkiniu (ne a-h iš praeito testo). Tikslas — patvirtinti ar
diagnozė (ranking disbalansas: ilgi skill aprašai užgožia trumpus growth/memory įrašus) laikosi ir su naujom užklausom.

ŽINGSNIAI:
1) Index šviežias (inkrementinis build jei reikia).
2) Paleisk ŠIAS 8 NAUJAS užklausas (LT+EN, semantika ne raktažodžiai; kiekvienai top-3 su path+score+snippet):
   1) „agentai izoliuotai ir saugiai vykdo kodą smėlio dėžėje"        (sandbox/bwrap izoliacija)
   2) „RAG ir prieštaringi ar konfliktuojantys dokumentai"           (RAG-conflicting-docs)
   3) „GPU nuoma ir modelių hostinimas savo serveriuose"            (FUTURE_GPU / self-hosting)
   4) „automatinis brėžinių ir CAD failų apdorojimas"                (cad drawing processing / DXF)
   5) „naujų įgūdžių formavimas iš patirties"                        (skill accretion)
   6) „faktų tikrinimas ir haliucinacijų aptikimas"                  (faithfulness)
   7) „ilgo konteksto išlaikymas ir projekto atmintis"               (journal / context retention)
   8) „self-improvement per near-misses ir biudžetą"                 (GIFT / self-optimization / overfitting)
3) Kiekvienai: PATAIKĖ (relevantus top-1) / DALINAI (relevantus top-3 bet ne #1) / MISS. Jei MISS — patikrink manifest ar
   taikinys APSKRITAI indeksuotas (yra vault'e ir index'e) → ar tai RANKING (indeksuotas bet nusėdo) ar APIMTIS (nėra vault'e/index'e).

ATASKAITA (HERA botas): 8 užklausos × top-1 (path+score) + verdiktas; suvestinė X PATAIKĖ / Y DALINAI / Z MISS;
palyginimas su pirmu testu — ar ranking-disbalanso diagnozė patvirtinta; kurie MISS = ranking vs apimtis. Nieko nekeisk.
