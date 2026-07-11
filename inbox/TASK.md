UŽDUOTIS — PATAISYTI BOTŲ MARŠRUTĄ: SANTRAUKA TIK Į PARSER, HERA BOTAS TIK ATASKAITOS. <12 min.
NEleisk pytest. Telegram TRUMPAI. Fail-safe: klaida nelaužo ingest.

SAUGUMAS: raktų nespausdink/necommit'ink. Jei liesta kodą — push į PRIVATŲ hera-core-backup.

PROBLEMA: mano ankstesnė „grąžinti analizę" pataisa (hera_fullsend per dispatcher) siunčia PILNĄ LT santrauką į
HERA botą (@tryspagaliai_hera_bot, matėsi „📖 HERA analizė (dalis 6/6)"). VARTOTOJO TAISYKLĖ:
- PARSER botas = pilna LT santrauka (analizė) — TIK ČIA, vartotojas skaito.
- HERA botas (@tryspagaliai_hera_bot) = TIK sistemos ataskaitos (ingest ACK „📥 Priimta: title | selektorius |
  taryba", Loop B, lint, VPS agento ataskaitos). JOKIOS pilnos santraukos.
- HERA sistema info gauna viduje (ingest/tyrimas/savęs tobulinimas) — nepakeista.

1) ŽEMĖLAPIS (pirma išsiaiškink, be spėjimų): kuris botas/tokenas = PARSER (kur vartotojas gauna LT santrauką),
   kuris = HERA botas (ataskaitos). Kur ATEINA vartotojo turinys (į kurį botą/chat). Kur DABAR hera_fullsend
   siunčia pilną analizę (į HERA botą — tai klaida). Aprašyk topologiją ataskaitoje TRUMPAI.

2) TAISYMAS:
   a) Pilna LT santrauka (extracted/full.md) turi eiti TIK į PARSER botą/chat (kur vartotojas skaito turinį).
      Jei PARSER yra atskiras pipeline, kuris JAU natūraliai siunčia santrauką — tada mano hera_fullsend per
      HERA botą tiesiog IŠJUNK (HERA_FULL_ANALYSIS=0), kad nedubliuotų ir nemaišytų. Jei santrauka pasiekia
      vartotoją TIK per hera_fullsend — perkonfigūruok, kad siųstų per PARSER boto tokeną/chat, NE HERA botą.
      Pasirink pagal tai, kaip realiai sukonfigūruota; NEdubliuok santraukos.
   b) HERA botas siunčia TIK ataskaitas — įsitikink, kad „📖 analizė" iš HERA boto DINGSTA.
   c) PARSER santrauka = VISADA žinutėmis (dalimis, ≤3800 simb.), NE dokumentu — vartotojas nori keliomis
      žinutėmis (panaikink „>8 dalys → dokumentas" logiką PARSER kelyje; visada dalimis).
3) HERA vidinis apdorojimas (ingest, selektorius, taryba, vault, savęs tobulinimas) — NEKEISK. Info sistema
   gauna kaip anksčiau.
4) TESTAS: (a) perleisk 1 kandidatą -> patikrink KUR nueina santrauka (turi PARSER, NE HERA botas) ir kad HERA
   bote lieka tik ACK; (b) santrauka dalimis (ne dokumentu); (c) fail-safe: klaida nelaužo ingest.
5) DURABILUMAS: kopija į /opt/cad-site-agent/n8n/hera/ + push į PRIVATŲ hera-core-backup. Viešo NELIESK.

TELEGRAM (per HERA botą, trumpai, be raktų): (1) topologija (PARSER vs HERA botas), (2) santrauka dabar TIK PARSER
(dalimis), HERA bote tik ataskaitos, (3) kaip išspręsta (fullsend išjungtas ar perkreiptas), (4) „MARŠRUTAS PATAISYTAS".
