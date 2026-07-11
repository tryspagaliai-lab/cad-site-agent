UŽDUOTIS — 3 FAZĖ: PLONAS RESEARCH ORKESTRATORIUS (plan→search→fetch→CoVe→synthesize). <13 min, time-boxed.
NEleisk pytest. Telegram TRUMPAI. €0. Fail-safe.

⚠️ KRITINIS SAUGIKLIS NUO rc=124 (jau 2x kabo): KIEKVIENAS LLM kvietimas timeout 45s, JOKIO retry (retry dvigubina).
KIEKVIENAS fetch timeout 20s. VISO research kvietimo biudžetas HARD: max 3 užklausos × max 2 fetch = ≤6 šaltiniai,
max 6 LLM kvietimai. Jei viršija biudžetą/timeout — grąžink DALINĮ rezultatą, NIEKADA nekabink. Testas — mažas.

SAUGUMAS: raktų nespausdink/necommit'ink. Jei liesta hera kodą — push į PRIVATŲ hera-core-backup.

KONTEKSTAS: turim hera_search.py (SearXNG) + hera_browser.py (fetch) + nemokamus modelius. Dabar plonas ciklas,
kuris juos sujungia į gilų tyrimą teiginio/temos verifikavimui.

1) /opt/hera-processor/hera_research.py — funkcija research(topic_or_claim, max_queries=3, max_sources=6) ->
   {verdict, confidence, evidence:[{quote,url}], sources:[url], synthesis, partial:bool}. Ciklas:
   a) PLAN: 1 LLM kvietimas (Gemini flash, 45s, be retry) -> 2-3 paieškos užklausos. Jei krenta -> naudok patį topic kaip 1 užklausą.
   b) SEARCH: hera_search kiekvienai užklausai -> surink URL'us (dedup, top ~6 viso).
   c) FETCH: top ~4-6 URL per trafilatura->naršyklė (20s each, fail-safe -> praleisk); apkarpyk kiekvieną ~2000 tokenų.
   d) VERIFY (CoVe): 1 LLM kvietimas (45s) -> griežtas JSON {verdict: supported|contradicted|no-evidence,
      confidence 0-1, evidence:[{quote,url}], reasoning}. Modelis mato teiginį + ištraukas.
   e) SYNTHESIZE: 1 LLM kvietimas (45s, gali būti Groq greičiui) -> trumpa sintezė su citatomis.
   LLM paskirstymas: plan/synth Gemini flash; verify Groq arba GLM (rotacija). Centrinis timeout wrapper VISIEMS.
2) JUNGIKLIS: HERA_RESEARCH=1 (default 1); =0 išjungia. Šitas modulis kol kas STANDALONE — dar NEjungiam į
   ingest/gate (tai kita fazė). Tik pastatom ir ištestuojam.
3) TESTAS (MAŽAS, kad neužtruktų): research("Shepherd is a Python framework that records agent actions as a
   git-like reversible trace for sandboxed review") su max_queries=2, max_sources=3 -> grąžina JSON su verdict +
   bent 1 šaltiniu. Parodyk verdict, confidence, kiek šaltinių, ar partial (be viso turinio, be raktų).
   Jei per biudžetą negrįžta — grąžink partial, ataskaitoje pažymėk „biudžetas/timeout suveikė (gerai)".
4) FAIL-SAFE PATIKRA: SearXNG down / tuščia paieška -> research grąžina {verdict:no-evidence, partial:true},
   NEkabo, NEcrash.
5) DURABILUMAS: kopija į /opt/cad-site-agent/n8n/hera/ + push į PRIVATŲ hera-core-backup. Viešo NELIESK.

TELEGRAM (trumpai, be raktų): (1) hera_research.py veikia, biudžeto ribos (queries/sources/LLM), (2) testo
rezultatas (verdict/confidence/šaltinių sk./partial), kiek užtruko, (3) fail-safe OK, (4) „RESEARCH ORKESTRATORIUS PARUOŠTAS (3 FAZĖ)".
