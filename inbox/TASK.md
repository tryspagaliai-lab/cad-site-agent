UŽDUOTIS — semsearch v1.1: CHUNKING + profile/ + before/after testas (16 užklausų). <30 min.
Fail-safe: jei abejoji STOP+backup restore. NEleisk pytest. €0 (lokalu). Ataskaita TIK į HERA botą. Viešo cad-site-agent NELIESK (untracked + /opt/hera-processor).

KONTEKSTAS: 2 kokybės testai (16 užklausų) diagnozavo RANKING disbalansą — ilgi/bendri skill dok. užgožia specifinius trumpus
(taikinys nusėda net iki #54/151). Fix = CHUNKING: skaidyti dok. į pastraipas, embeddint kiekvieną → trumpas įrašas konkuruoja
kaip vienas fokusuotas chunk'as. + pridėti profile/ (apimties fix h). NELIESK apimties gedimų agro/faithfulness (atskiras turinio klausimas).

ŽINGSNIAI:
1) BACKUP: hera_council-nesusijęs — cp dabartinį hera_semsearch.py → /root/hera-core-backup/hera_semsearch.py.$(date +%s); ir dabartinį index/state kopija (kad grįžtama).
2) MODIFIKUOK hera_semsearch.py (def 0 no-op išlieka; NELIESK council/kitų modulių):
   - CHUNKING: kiekvieną dok. (growth/skills/profile/*.md + memory_index įrašus) skaidyk į chunk'us pagal markdown struktūrą
     (## antraštės / pastraipos), target ~80-250 žodžių, sulieti per mažus. Kiekvienas chunk embeddinamas ATSKIRAI.
   - INDEX saugo: chunk_id, parent_path, parent_sha, chunk_snippet, vektorius. Inkrementinis pagal parent_sha (re-chunk tik pakeistus).
   - QUERY: embeddina užklausą → cosine per VISUS chunk'us → grupuok pagal parent_path → dok. balas = MAX chunk balas → top-K dok.
     su geriausiu chunk snippet. (Tai passage-retrieval, taiso ilgio dilution.)
   - Pridėk profile/ prie indeksuojamų šaltinių.
   - Fail-safe, €0, jokio tinklo query metu.
3) REBUILD chunked index. Užrašyk: chunk skaičius, RAM peak, build laikas, index dydis.
4) SELFTEST (--selftest, be pytest): semantinis top-1 (paraphrase) + HERA_SEMSEARCH=0 no-op → PASS.
5) BEFORE/AFTER — paleisk VISAS 16 užklausų (top-1 path+score+verdiktas), palygink su ankstesniais:
   TEST#1: a)„begaliniai LLM ciklai/pergalvojimas" b)„mokytis iš klaidų taisyti" c)„patvirtinti darbą prieš pradedant"
     d)„3D modeliavimo AI įrankiai" e)„žemės ūkio AI ūkininkams" f)„sujungti kelis AI modelius sprendimui"
     g)„semantinė atmintis tarp pokalbių" h)„vartotojo tikslai ir 3D dizaino patirtis"
   TEST#2: 1)„agentai izoliuotai saugiai vykdo kodą" 2)„RAG prieštaringi dokumentai" 3)„GPU nuoma hostinimas"
     4)„automatinis brėžinių/CAD apdorojimas" 5)„naujų įgūdžių formavimas iš patirties" 6)„faktų tikrinimas haliucinacijos"
     7)„ilgo konteksto projekto atmintis" 8)„self-improvement per near-misses biudžetą"
   YPAČ pažymėk RANKING taikinius ar PAGERĖJO: a,c,d,h (test#1) + q4,q8 (test#2). Apimties (e,q6 agro/faithfulness) tikėtina lieka MISS — OK.
6) IŠVADA: bendras skaičius PRIEŠ (test1:1/2/5, test2:5/0/3) vs PO chunking; ar ranking taikiniai pakilo į top-1/3. 
7) BACKUP kodą /opt/hera-processor + commit/push; ROADMAP „semsearch v1.1 chunking + profile" pastaba.

ATASKAITA (HERA botas): chunk sk. + resursai; selftest PASS/FAIL; 16 užklausų PO-verdiktai (ypač a/c/d/h/q4/q8 pokytis); bendras before/after skaičius; backup+ROADMAP. Jei STOP — kodėl + restore.
