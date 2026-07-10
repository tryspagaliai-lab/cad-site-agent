UŽDUOTIS — NAPMEM FAZĖ C: ŠVIEŽIAS INDEKSAS + CACHE-HIT METRIKA (VIENA SIAURA UŽDUOTIS). <10 min.
NEleisk pytest — tik taikinius testus. LLM kvietimams — griežti timeout'ai (60s + 1 retry). Telegram TRUMPAI.

SAUGUMAS: raktų nespausdink/necommit'ink/nerodyk.

KONTEKSTAS: kuratorius rado, kad index/concepts.md pasenęs (2026-07-07: rodo 1 skill / 8 RB įrašus, realybė —
~20 skills / 34 RB). Savaitinis Loop C nespėja su kasdieniu augimu — naršymo kilpai indeksas beveik nenaudingas.
Plius LLM-Wiki webinaro (o3srk6, council promote_candidate) DISTILL #9: cache-hit ROI metrika.

1) INDEKSO ŠVIEŽINIMAS:
   a) Pergeneruok index/concepts.md DABAR (su timeout'ais; jei generavimas naudoja LLM ant kiekvieno skill —
      apsvarstyk deterministinę versiją iš frontmatter'ių, LLM tik santraukoms kur būtina).
   b) Prijunk prie Loop B (kasdienis) — indeksas atsinaujina kasdien, ne kas savaitę. Loop C lieka gilesnei
      konsolidacijai (merge/prune), bet indekso šviežinimą perima Loop B.
2) CACHE-HIT METRIKA naršymo kilpoje: į trajektorijos įrašą pridėk cache_hit lauką — true, kai atsakymas gautas
   iš L2+ santraukų (records/skills/profile) NEnusileidžiant į žalią extracted; false kai reikėjo žalio teksto
   arba nerasta. Loop B raporte — cache-hit % ir vidutinis įrankių kvietimų sk. per query. Tai matuoja, ar
   vault'as realiai apsimoka (Dosu pattern: cache-hit = ~2x pigesnė užklausa).
3) TESTAS: (a) concepts.md rodo realų skill skaičių (~20) ir šviežią datą; (b) 1 query per kilpą -> trajektorijoje
   matosi cache_hit reikšmė; (c) regresija: „kas yra ATDP?" veikia.
4) DURABILUMAS: kodo kopija į /opt/cad-site-agent/n8n/hera/ (be push į viešą!) + push į PRIVATŲ hera-core-backup
   (askpass, secret-scan). Viešo repo NELIESK.

TELEGRAM (trumpai, be raktų): (1) indeksas šviežias — kiek skills/growth/RB rodo, Loop B hook įjungtas,
(2) cache_hit loginamas — testo query reikšmė, (3) regresija OK, (4) privatus backup push OK, (5) „NAPMEM-C BAIGTA".
