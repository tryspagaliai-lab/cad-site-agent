UŽDUOTIS — Fazė 17: hera_semsearch — €0 LOKALI semantinė paieška per vault (embedding). <30 min.
Fail-safe: jei NETELPA €0/resursuose (4GB RAM, be GPU) — STOP+reportuok, NEbloatink VPS. NEleisk pytest. €0 (jokio API, viskas lokaliai).
Ataskaita TIK į HERA botą. Viešo cad-site-agent NELIESK (kodą dėk untracked + kopija /opt/hera-processor). Secret'us NEliesk.

KONTEKSTAS: HERA turi persistentišką atmintį (memory_index.jsonl, growth/, skills/, reasoningbank), BET paieška =
leksinė/anchor (cue_anchors), NE semantinė. Trūkumas: rasti „ką kalbėjom apie X" kai užrašyta kitais žodžiais. Statom
€0 lokalų embedding-paieškos sluoksnį. NEadoptuojam MemPalace (self-built, HERA-native, be trečios šalies rizikos).

SVARBU (resursai): VPS 4GB RAM, be GPU. VENK torch bloat. PIRMENYBĖ lengviems lokaliams embedder'iams:
  1-as pasirinkimas: fastembed (ONNX, be torch) su mažu MULTILINGUAL modeliu (LT+EN), pvz. intfloat/multilingual-e5-small
     ar BAAI/bge-small (ONNX). Jei fastembed netelpa — 2) llama.cpp/GGUF embedding modelis; 3) jei jau yra sentence-transformers.
  Jei NĖ VIENAS netelpa €0/RAM — STOP, reportuok kas realiai įmanoma (nediek torch 2GB be reikalo).

ŽINGSNIAI:
1) FEASIBILITY (pirma): `df -h /`, `free -m`; pasirink embedder pagal tai kas telpa (€0, lokalus, multilingual). Užrašyk sprendimą.
   Modelio download OK (VPS turi internetą), bet flag'ni dydį (MB) ataskaitoj.
2) hera_semsearch.py (HERA_SEMSEARCH jungiklis def 0 = no-op importui; CLI veikia visada):
   - `build`: skenuoja /opt/hera-vault/{growth,skills}/*.md + memory_index.jsonl → tekstą embeddina LOKALIAI → saugo vektorius +
     manifest (path, sha, snippet) į STATE dir (/opt/hera-processor/semsearch/ ARBA /root/hera_semsearch/ — NE į vault git, kad
     nebūtų binarų churn). INKREMENTINIS: re-embeddina TIK pakeistus (sha palyginimas).
   - `query "<klausimas>"`: embeddina klausimą → cosine top-K (def 5) → spausdina path + score + snippet.
   - Fail-safe: viskas try/except; klaida → log /root/hera_semsearch.log, ne crash. €0, jokio tinklo query metu.
3) SELFTEST (--selftest, be pytest): (a) mažas sintetinis rinkinys, query KITAIS žodžiais ta pačia prasme → teisingas top-hit
   (įrodo semantiką, ne raktažodžius); (b) HERA_SEMSEARCH=0 importas = no-op.
4) REALUS DEMO: `build` ant tikro vault + 2 query pvz: „kaip veikia taryba/council" ir „atminties paieška tarp sesijų" → parodyk top-3
   (path+score). Tai parodo ar semantika realiai veikia mūsų LT+EN turiny.
5) RESURSŲ ATASKAITA (svarbu): modelis+dydis MB, RAM peak build metu, index dydis, build laikas, disk po.
6) Cron NEDĖK. Runner integracija = ATSKIRAS žingsnis (v2 vėliau). BACKUP: hera_semsearch.py → /opt/hera-processor + commit/push.
   Vault ROADMAP.md: „Fazė 17 hera_semsearch (€0 lokali semantinė vault paieška) — ĮDIEGTA <data>, HERA_SEMSEARCH def 0, <embedder>, runner integr.=vėliau".

ATASKAITA (HERA botas, trumpai): pasirinktas embedder+dydis; feasibility (df/free verdiktas); modulis+selftest PASS/FAIL;
demo 2 query top-3 (ar semantika veikia); resursai (RAM peak/index dydis/laikas); backup+ROADMAP. Jei STOP — kodėl + kas įmanoma vietoj.
