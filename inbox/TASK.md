UŽDUOTIS — FAZĖ 12c: pravalyti faithfulness balą (išmesti md-karkaso false-ungrounded triukšmą). <10 min.
NEleisk pytest pilnai (tik hera_faithfulness --bench + 1 live dry-run). Telegram TRUMPAI į HERA botą. Fail-safe. €0.
Raktų nespausdink. Ataskaita TIK į HERA botą. Privatūs repo. Viešo cad-site-agent NELIESK.

KONTEKSTAS (kodėl): Fazė 12b įjungė faithfulness gyvai, veikia (yt score 0.847 ir kt., realūs balai). BET pats VPS
pažymėjo: `parsed=full_md` įtraukia md-karkasą (URL, „Metodas:", „Skambučių:", „Transkripto sim.", skyrių antraštes
tipo „# YouTube ištrauka", „## Pilna transkripcija") — tie atomai kelia MELAGINGĄ ungrounded triukšmą (dalis 24/157
buvo ne haliucinacijos, o URL/antraštės). Triukšmingas balas → `suspect` vėliavėlės nepatikimos → įrankis praranda
vertę. Reikia: tikrinti TIK semantinius teiginius, ne md-karkasą.

ŽINGSNIAI (minimalūs, tiksliniai):

1) SIAURINTI `parsed` faithfulness pakopoje:
   - Vietoj viso `full_md`, paduok į check() TIK „## Struktūrizuota ištrauka (Gemini)" bloką (PAVADINIMAS/ESMĖ/
     PAGRINDINIAI TAŠKAI/FAKTAI IR DUOMENYS/ĮRANKIAI/CITATOS) — tikrus semantinius teiginius.
   - IŠMESK md-karkasą: „# ... ištrauka" antraštes, metaduomenų eilutes (URL:/Metodas:/Skambučių:/Transkripto sim.),
     „## Pilna transkripcija (verbatim)" antraštę ir patį verbatim bloką (verbatim = ŠALTINIS, ne parse — jo netikrink
     kaip parsed atomų).
   - source_text lieka = verbatim transkriptas (+titrai/ASR/url tekstas) — kaip 12b.
   - Jei „Struktūrizuota ištrauka" bloko nerandi konkrečiam ingestui → fallback į dabartinį elgesį (nesugadink), pažymėk.
   - Papildomai (jei lengva, deterministiška): atomų ekstrakcijoje ignoruok URL/domenus ir grynus metaduomenų raktažodžius.

2) VERIFIKACIJA (be pakibimo, deterministiška):
   - `hera_faithfulness --bench` turi likti 100% (14/14). Jei nukrito — grąžink, NEjunk pakeitimo, pranešk.
   - LIVE dry-run (be LLM/tinklo) ant TO PATIES YouTube v=6V3RiljfY7A: parodyk NAUJĄ score + ungrounded N.
     Tikslas — ungrounded turi SUMAŽĖTI (buvo 24/157), balas švaresnis. Palygink prieš/po.
   - Paleisk ant dar 1-2 jau ingestintų yt, kad įsitikintum, jog `suspect` dabar reiškia tikrą neatitikimą, ne triukšmą.

3) BACKUP: commit į hera-core-backup. Persistent askpass jau yra. Push nepavyko → NEkartok begalos, pranešk.

RIBOS: €0. Jokių lokalių/GPU modelių. Jokių naujų tinklo kvietimų. Jokio pytest-all. HERA_FAITHFULNESS lieka=1 (gyvai).
NEperrašinėk extraktorių/council — TIK siaurink kas paduodama į check(). Anti-rc124: viskas deterministiška, be model-call.

ATASKAITA (HERA botas, trumpai): (a) parsed susiaurintas iki Struktūrizuota-ištrauka bloko? (b) bench X/Y;
(c) v=6V3RiljfY7A: prieš 24/157 (0.847) → PO: ungrounded N / score; (d) 1-2 kitų yt verdict po pravalymo;
(e) backup push OK/ne; (f) 1 eil. kas toliau.
