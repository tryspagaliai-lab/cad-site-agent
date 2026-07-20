UŽDUOTIS — ai_digest: pridėti AGRO temą → @ARTOJAS_BOT (AGRO_BOT_TOKEN). „ai"+„design" temos NEPALIESTOS. <18 min.
NEleisk pytest-all. Fail-safe. €0. Raktų nespausdink. Ataskaita TIK į HERA botą.
ANTI-RC124: KIEKVIENAS fetch HARD ≤20s, JOKIO retry; per-feed klaida → skip. Semantic Scholar: HARD 20s, max 3 užklausos/run.

KONTEKSTAS: vartotojas patvirtino agro šaltinių sąrašą (deep-research, dalinis tikrinimas — kandidatai su fallback).
TOPICS šablonas jau yra (ai/design) — pridėk temą „agro": token_env=AGRO_BOT_TOKEN, seen=/var/lib/ai_digest/seen_agro.jsonl,
antraštė „🌾 AI Žemės ūkyje — Digest". Tema = AI EKSPLOATAVIMAS žemės ūkyje (ne bendros ūkio naujienos!).

ŠALTINIAI:

1) MOKSLINIS STUBURAS:
   - Semantic Scholar bulk API (BE rakto): GET https://api.semanticscholar.org/graph/v1/paper/search/bulk su
     query (pvz. "precision agriculture AI" / "plant disease detection deep learning" / "agricultural robotics"),
     fields=title,abstract,publicationDate,externalIds,url; filtruok pagal publicationDate (nauji nuo praeito run).
     Max 3 užklausos/run, HARD 20s, klaida→skip (shared pool gali droselinti — fail-safe).
   - OpenAlex PARUOŠTA VIETA: jei env yra OPENALEX_KEY → įjunk šaltinį (works?filter=topic+data, pipe-OR, mailto
     param); jei rakto NĖRA → tyliai skip (vartotojas pridės vėliau, įsijungs automatiškai). NEreikalauk rakto.
   - arXiv API užklausa (kaip aptarta): http://export.arxiv.org/api/query su
     search_query=(cat:cs.CV+OR+cat:cs.RO+OR+cat:eess.IV)+AND+(all:agriculture+OR+all:crop+OR+all:"plant disease"+OR+all:farming),
     sortBy=submittedDate&sortOrder=descending&max_results=25. Atom → feedparser. 1 kvietimas/run.

2) INSTITUCIJOS (patvirtinti; browser User-Agent visiems, kaip design temoje):
   - WUR: atrask feed URL iš https://www.wur.nl/nl/Resources/RSS.htm (news-EN feed'ą; jei 403/nerandi → skip, pažymėk)
   - CORDIS agri RSS (iš cordis.europa.eu; jei tiksli nuoroda nepasiekiama → skip, pažymėk)
   - UPM: https://oa.upm.es/view/institution/Agronomos/ (EPrints — Atom/RSS; atrask tikslų feed URL puslapy)
   - SFA Singapūras: feed iš https://www.sfa.gov.sg/news-publications/newsroom/subscribe-to-sfa-rss-feeds
   - IWMI/CGIAR: feed iš https://www.iwmi.cgiar.org/news/rss-feeds/ (news+publications)

3) KANDIDATAI (fallback-skip — jei feed 404/403/nėra, tyliai praleisk, pažymėk ataskaitoje):
   - ICRISAT: https://pressroom.icrisat.org/feed ; Rothamsted (ieškok /rss ar /feed iš rothamsted.ac.uk/news);
     IRTA (irta.cat/en — /feed); CREA (crea.gov.it/en — /feed); SLU (slu.se/en/news — rss); NARO EN (naro.go.jp/english);
     Global Ag Tech Initiative: https://www.globalagtechinitiative.com/feed/
   - P.Korėjos padengimui (RDA be feed'o): Google News RSS užklausa
     https://news.google.com/rss/search?q=AI+agriculture+Korea+OR+smart+farm+Korea&hl=en (1 vnt., fallback-skip)

4) GitHub .atom: FarmBot/Farmbot-Web-App/releases.atom · Project-AgML/AgML/releases.atom ·
   microsoft/farmvibes-ai/releases.atom · danforthcenter/plantcv/releases.atom

FILTRAI: (a) privalomas AI-relevancijos filtras (title/abstract/tags): ai, machine learning, deep learning, neural,
computer vision, drone, uav, robot, autonomous, precision, smart farm, yield prediction, disease detection, llm,
segmentation, satellite (jei nė vieno → praleisk — NE bendros ūkio naujienos); (b) esamas is_noise filtras.

SANTRAUKOS: v3 šablonas (kas_tai 2-3 sak. + kur_panaudoti), BET kur_panaudoti tilt = KAIP AI PRITAIKOMAS ŽEMĖS ŪKYJE
(ką technologija įgalina ūkyje/agroversle — praktinis pritaikymas srityje; NE vartotojo 3D kontekstas). Batch Gemini
kaip design temoje, fallback bare.

VERIFIKACIJA: (a) „ai"+„design" temos nepakeistos (assertai); (b) agro dry-run: surinkta/po filtro/nauji per šaltinį
(pažymėk kurie feed'ai gyvi, kurie skip); (c) TEST-SEND į @ARTOJAS_BOT (AGRO_BOT_TOKEN): žyma „🧪 TESTAS — ARTOJAS",
seen_agro NEkurk dėl testo.

BACKUP: hera-core-backup push. Nepavyko → NEkartok begalos, pranešk.

ATASKAITA (HERA botas, trumpai): (a) agro tema pridėta (ai/design nepaliestos)? (b) šaltinių būklė: gyvi N / skip M
(kurie); (c) Semantic Scholar + arXiv veikia? OpenAlex placeholder paruoštas? (d) dry-run skaičiai; (e) test-send į
ARTOJAS OK (kiek įrašų)? (f) backup push; (g) 1 eil. toliau (ai-tech tema).
