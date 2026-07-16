UŽDUOTIS — 2D→3D ingesto atsakinga ekstrakcija (faithfulness-filtruota, cad/3D domenui). <12 min.
NEleisk pytest. Telegram TRUMPAI į HERA botą. Fail-safe. €0. Raktų nespausdink. Privatus hera-vault.
Viešo cad-site-agent NELIESK (tik nuoroda tekste — jokio kodo keitimo).

KONTEKSTAS (kodėl): vartotojui labai aktualu — ingestas „A better way to turn 2D designs into 3D models for rapid
prototyping" (sel 8.0), TIESIOGIAI liečia jo cad-site-agent (2D DXF sklypų apdorojimas → natūrali 2D→3D plėtra) ir
jo 3D/ArchViz foną. BET faithfulness pažymėjo `suspect 0.7045` → ~30% atomų neatremti į transkriptą. Todėl „paimti
viską" ATSAKINGAI = imti TIK patvirtintą, įtartinus atskirti, kad į cad-domeną nepakliūtų haliucinacijos.

ŽINGSNIAI:

1) RASK šitą ingestą (growth kandidatą „2D...3D...rapid prototyping"; per grep title/slug). Jei dar neįrašytas kaip
   growth — paimk iš paskutinio ingest rezultato (full_md). Nurodyk failą/slug ataskaitoje.

2) FAITHFULNESS ATOM-LYGIU (deterministiška, be LLM/tinklo): paleisk hera_faithfulness ant jo parse↔verbatim ir
   parodyk KONKREČIAI:
   - score + verdict (turėtų būti ~0.7045 suspect),
   - SĄRAŠĄ ungrounded atomų (kurie teiginiai/vardai/skaičiai NEatremti į transkriptą) — kad matytume kas įtartina.
   - Atskirk: realūs angl. terminai/linksniai (triukšmas) vs tikri neatremti faktai (galima haliucinacija).

3) EKSTRAKCIJA (tik PATVIRTINTA): iš „Struktūrizuota ištrauka" bloko paimk kandidatus (idėjos/įrankiai/technikos/
   faktai), kurie ATREMTI į transkriptą. Ungrounded/įtartinus — NEIŠMESK, bet pažymėk „⚠️ nepatvirtinta parse'e —
   netraukti kaip fakto". Jokių naujų tinklo kvietimų (necituok, netikrink išorėje).

3) VAULT (staged, human-gate): įrašyk/atnaujink growth natą su:
   - frontmatter: status: staged, gate: human, domain: cad-3d, faithfulness: „suspect 0.7045 (atom-filtruota)".
   - PATVIRTINTI kandidatai (2D→3D metodas, įrankiai, rapid-prototyping technikos) — su „Kodėl sistemai".
   - Aiškus skyrius „⚠️ Nepatvirtinta parse'e" su ungrounded atomais (kad ateity žinotume necituoti).
   - Skyrius „Sąsaja su cad-site-agent": 1-2 sakiniai kaip 2D→3D plečia esamą 2D-DXF→semantika pipeline (idėjos
     lygiu; JOKIO viešo kodo keitimo — tik žinia vault'e). Wiki-link auto.

4) BACKUP: commit hera-vault. Persistent askpass yra. Push nepavyko → NEkartok begalos, pranešk.

RIBOS: €0. Jokių lokalių/GPU modelių. Jokio pytest-all. Viešo cad-site-agent NELIESK. Anti-rc124: viskas
deterministiška, faithfulness be LLM/tinklo. Ekstrakcijai NEnaudok naujų model-call (imk jau turimą parse'ą).

ATASKAITA (HERA botas, trumpai): (a) failas/slug; (b) faithfulness score + 3-6 ungrounded atomų pavyzdžiai
(realu vs įtartina); (c) kiek PATVIRTINTŲ kandidatų ištraukta (idėjos/įrankiai); (d) cad-site-agent sąsaja 1 eil.;
(e) vault push OK/ne; (f) 1 eil. kas toliau.
