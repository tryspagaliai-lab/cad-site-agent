UŽDUOTIS — FAZĖ 12b: prijungti source_text prie faithfulness-vartų (YouTube/url), TADA įjungti HERA_FAITHFULNESS=1 live. <14 min.
NEleisk pytest pilnai (tik hera_faithfulness --bench + 1 live dry-run). Telegram TRUMPAI į HERA botą. Fail-safe. €0.
Raktų nespausdink. Ataskaita TIK į HERA botą. Privatūs repo. Viešo cad-site-agent NELIESK.

KONTEKSTAS (kodėl): Fazė 12 sukūrė hera_faithfulness.py (benchmark 14/14), bet HERA_FAITHFULNESS=0 ir YouTube/url →
`inconclusive`, nes extraktoriai neteikia source_text. Vartotojo ingests dažniausiai YouTube. Vien flag'o įjungimas
beveik nieko neduotų. Todėl: prijungti šaltinį, kad yt/url irgi būtų tikrinami, TADA įjungti. YouTube atveju šaltinis
JAU egzistuoja — verbatim transkripcija, kurią PARSER'is gamina. faithfulness = ar Gemini struktūrizuota santrauka
atitinka verbatim transkriptą (haliucinacijų gaudymas). Tai grynai deterministiška (be LLM/tinklo) → negali pakibti.

ŽINGSNIAI:

1) SOURCE_TEXT PRIJUNGIMAS (minimalus, tikslinis — NEperrašinėk extraktorių logikos):
   - Dispatcher `_maybe_faithfulness` pakopoje: kur imamas `parsed`, PRIDĖK `source_text` iš jau turimų duomenų:
     • YouTube (gemini-titrai): source_text = VERBATIM transkriptas (pilnas „Pilna transkripcija (verbatim)" blokas),
       kurį jau turi ingest rezultate. Jei yra ir titrai, ir verbatim — sujunk.
     • url (trafilatura/playwright): source_text = ištrauktas puslapio tekstas (jau turimas prieš struktūrizavimą).
     • tekstas/failai: kaip dabar (verbatim-block fallback).
   - Jei source_text tuščias/nerastas KONKREČIAM ingestui → verdict `inconclusive` (kaip dabar), NIEKADA neblokuok.
   - NEkeisk pačių extraktorių — TIK paduok jų jau turimą tekstą į check(). Jei kur source_text nepasiekiamas be
     papildomo darbo — praleisk tą kelią, pažymėk ataskaitoje (NEdaryk naujų tinklo kvietimų — anti-rc124).

2) ĮJUNGTI HERA_FAITHFULNESS=1 LIVE:
   - Nustatyk flag'ą į 1 nuolatinėje konfigūracijoje (ten kur kiti HERA_* flag'ai). Pakopa lieka ADVISORY —
     NIEKADA neblokuoja ingest'o; `suspect` → ⚠️ tik į HERA botą; klaida/timeout → `inconclusive`, rc=0.
   - Patvirtink, kad kai flag=1, esamas pipeline elgesys nesikeičia IŠSKYRUS naują advisory pastabą.

3) VERIFIKACIJA (privaloma, be pakibimo, deterministiška):
   - `hera_faithfulness --bench` turi likti 100% (buvo 14/14). Jei nukrito — NEjunk, grąžink flag=0, pranešk.
   - LIVE DRY-RUN (be LLM, be tinklo): paleisk faithfulness ant ≥1 JAU ingestinto YouTube įrašo parse↔verbatim
     (pvz. Artifacts/yarabu arba GeoWorld/H-JEPA). Parodyk REALŲ score + kiek ungrounded atomų + verdict. Tikslas —
     ĮRODYTI, kad yt dabar gauna `ok/suspect` su tikru balu, NE `inconclusive`. Jei vis tiek inconclusive — pranešk
     kodėl (kur source_text nepasiekiamas), palik flag=1 tik jei bench 100% ir tekstui veikia.

4) BACKUP: commit į hera-core-backup. Persistent askpass jau yra. Push nepavyko → NEkartok begalos, pranešk.

RIBOS: €0. Jokių lokalių/GPU modelių. Jokių NAUJŲ tinklo kvietimų (naudok jau turimą tekstą). Jokio pytest-all.
NEperrašinėk hera_council/hera_selfedit/extraktorių — tik paduok source_text. Anti-rc124: viskas deterministiška.

ATASKAITA (HERA botas, trumpai): (a) source_text prijungtas yt/url? (kuriems keliams veikia); (b) HERA_FAITHFULNESS
įjungtas=1? (c) bench X/Y; (d) LIVE dry-run: kuris įrašas, score, ungrounded N, verdict (ok/suspect, NE inconclusive?);
(e) backup push OK/ne; (f) 1 eil. kas toliau.
