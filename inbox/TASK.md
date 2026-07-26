UŽDUOTIS — hera_goalanchor: pašalinti tarpkalbinį drift false-positive. <12 min.

## Tikslas
2026-07-26 GoalAnchor pirmą kartą suveikė produkcijoje ir tai buvo **klaidingas įspėjimas**:
`🧭 GOALANCHOR status=warn overlap=0.1368 signals=drift` ant VPS-grafo užduoties, kuri buvo atlikta TIKSLIAI pagal TASK.md.
Priežastis: TASK.md **lietuviškas**, agento galutinė išvestis **angliška** → drift matuojamas žodžių aibių sankirta,
o tarp LT ir EN teksto ji natūraliai ~0. HERA veikia dvikalbiu režimu, tad tai kartosis.
Rizika: jei 🧭 vėliava kartos klaidingus įspėjimus, ji taps triukšmu ir bus ignoruojama — guardas praras VISĄ vertę.
Sutvarkyk taip, kad tarpkalbinis atvejis NEbūtų raportuojamas kaip drift, bet tikras drift būtų gaudomas toliau.

## Realybė (ko pats neišvestum)
- Modulis `/root/hera_goalanchor.py` (Fazė 21), integruotas į runner'į (Fazė 22) kaip ADVISORY `GA_NOTE` prieš `send_tg`.
- HERA turinys mišrus: TASK.md rašomas lietuviškai, agentų ataskaitos dažnai angliškos, kartais mišrios.
- Ta pati problemos klasė jau žinoma projekte: faithfulness vartas duoda „suspect", kai LT santrauka lyginama su EN
  transkriptu — irgi tarpkalbinis triukšmas, ne haliucinacija. Nesukurk trečio nesuderinto sprendimo; jei logika
  perpanaudojama, tuo geriau.
- PF-1..PF-4 injection detekcija nuo kalbos NEPRIKLAUSO ir veikia teisingai — jos NELIESK.
- HERA turi daugiakalbį embedding modelį (fastembed `paraphrase-multilingual-MiniLM`, naudojamas semsearch).
  **NEnaudok jo šitam guardui** — guardas turi likti greitas, deterministinis ir be priklausomybių (jis vykdomas
  kiekviename runner cikle su `timeout 10`). Sprendimas turi būti grynai string/heuristinis.

## Apribojimai
€0, be tinklo, be LLM, deterministiška. Fail-safe (klaida → grąžinti „ok", niekada necrashinti, niekada neblokuoti).
`HERA_GOALANCHOR` def 0 semantika NEKEIČIAMA (išjungta → status „ok", bet signalai vis tiek skaičiuojami).
Ataskaita TIK į HERA botą. Viešo `cad-site-agent` NELIESK. BACKUP prieš keitimą. Runner'io NELIESK — tik modulį.

## Įrodymai (selftest, be pytest, be tinklo)
1. **Realus produkcijos atvejis:** LT tikslas + EN kandidatas, turinys ATITINKANTIS → **NE drift** (status ok).
   Naudok tikrą porą: tikslas = VPS-grafo TASK.md esmė lietuviškai; kandidatas = tos užduoties angliška ataskaita.
2. **Regresija — tikras drift privalo išlikti:** ta pati kalba, nesusijęs turinys (pvz. tikslas apie DXF parsinimą,
   kandidatas apie kriptovaliutų pirkimą) → **VIS TIEK warn**. Tai svarbiausias testas: nesuvelk guardo į tylėjimą.
3. **Tikras drift KITA kalba:** LT tikslas + EN kandidatas, turinys VISIŠKAI nesusijęs → ką grąžina? Aprašyk elgesį
   sąžiningai. Jei šitas atvejis nebegaudomas — tai priimtina kaina, bet PASAKYK aiškiai ataskaitoje, netylėk.
4. **Injection nepaliesta:** PF-1 ir PF-4 atvejai (bet kuria kalba) → vis tiek `alert`.
5. Ankstesni Fazės 21 selftest atvejai (6/6) toliau PASS.
6. BACKUP + push į privatų `hera-core-backup`; ROADMAP.md eilutė.

Ataskaitoje aiškiai pasakyk, KOKĮ metodą pasirinkai kalbų nesutapimui aptikti ir kokia jo klaidos riba.
Jei STOP — kodėl.
