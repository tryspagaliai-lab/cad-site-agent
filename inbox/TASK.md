UŽDUOTIS — HERA WIKI/LINT AUDITAS: 3 defektų klasės iš tandem-review (pritaikyti /opt'e). <14 min.
NEleisk pytest-all. Telegram TRUMPAI į HERA botą. Fail-safe. €0. Raktų nespausdink. Anti-rc124
(JOKIŲ LLM skambučių — grynas deterministinis kodo auditas+pataisos). Ataskaita TIK į HERA botą.
HERA kodas: /opt/hera-processor + push į PRIVATŲ hera-core-backup. Viešo cad-site-agent NELIESK.
HERA_FAITHFULNESS lieka GYVAS (=1); jokių jungiklių nekeisk.

KONTEKSTAS: web sesijoje tandeminis code-review (2 nepriklausomi tikrintojai) analogiškame wiki
kode rado 3 defektų klases, kurios labai tikėtinos ir HERA wiki/lint moduliuose (hera_wikilink,
hera_lint, sesijų indeksatorius, hera_journal — kur aktualu). AUDITUOK ir, KUR RANDI, pataisyk
minimaliai:

1. MARKDOWN NUORODŲ KODAVIMAS: jei wiki/grafo generatorius stato `[label](failas.md)` nuorodas —
   stem'ai su tarpais/skliaustais duoda lūžusį CommonMark. Pataisa: URL-encode href
   (urllib.parse.quote), label palikti. Deterministiška.
2. STEM/RAKTŲ KOLIZIJA: jei indeksavimas raktuoja pagal failo vardą be katalogo — du skirtingi
   failai tuo pačiu vardu tyliai perrašo vienas kitą, o ataskaita rodo abu kaip įrašytus. Pataisa:
   batch'e sekti matytus raktus, dublikatą praleisti su aiškia priežastimi ataskaitoje (pirmas
   laimi), NE tyliai perrašyti.
3. TIKRAS COUNT vs SAMPLE: jei kur nors saugomas/rodomas capped sample dydis kaip „viso" skaičius
   (pvz., N pirmų įrašų vietoj tikro text_count/entry_count) — saugoti tikrą count atskirai ir
   rodyti „X (sample: Y)". Jei schema SQLite — stulpelį pridėti per saugų ALTER TABLE ADD COLUMN
   (try/except, be migracijos frameworkų), senų DB neperrašinėti.

TVARKA: (a) grep/apžiūra kur šios klasės taikosi; (b) minimalios pataisos TIK ten, kur defektas
realiai yra — jei klasė netaikoma, pažymėk „netaikoma" ir NIEKO nekeisk; (c) hera_bench
deterministinis baseline PRIEŠ ir PO — turi likti ŽALIAS (jei PO raudonas → revert'ink pataisą,
pranešk); (d) hera_wikilink+hera_lint pass PO pataisų (orphan/dangling neturi blogėti);
(e) commit /opt'e + push į hera-core-backup. Push nepavyko → NEkartok begalos, pranešk.

RIBOS: €0, be LLM, be pytest-all (tik bench + taikiniai unit jei yra), viešo cad-site-agent
NELIESK, jungiklių nekeisk, nieko netrink, jokio auto-merge į nieką — tik tiesioginės minimalios
pataisos su bench-vartais kaip aukščiau.

ATASKAITA (HERA botas, trumpai): (a) kuri iš 3 klasių rasta kur (failai) / netaikoma;
(b) pataisyta kas; (c) bench PRIEŠ/PO žalias?; (d) wiki orphan/dangling PO; (e) backup push OK/ne.
