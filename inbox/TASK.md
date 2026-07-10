UŽDUOTIS — NAPMEM-A ATSTATYMAS PO TIMEOUT (SIAURA: TIK NARŠYMO KILPA, BE VAULT SYNC). <12 min, griežtai.
Ankstesnė užduotis (NapMem-A + vault sync) NUTRAUKTA po 15 min (rc=124) — kodas gali būti PUSIAU pakeistas.
NEleisk pytest. Vault sync NEDARYK (GITHUB_TOKEN dar keičiamas — bus atskira užduotis). Atsiskaityk Telegram TRUMPAI.

SAUGUMAS: raktų nespausdink/necommit'ink/nerodyk.

0) PIRMIAUSIA BŪKLĖ (2 min): systemctl is-active hera-processor hera-ingest; python3 -c "import" pagrindinių
   modulių sintaksei (hera_query.py ir kas liesta). Jei servisas krito ar failas pusiau redaguotas — PIRMA
   grąžink į veikiančią būseną (git diff /opt/cad-site-agent/n8n/hera/ kopijos atžvilgiu padės pamatyti kas keista).

1) UŽBAIK NARŠYMO KILPĄ (tik tiek, minimaliai):
   - Įrankiai: search_records, get_record, search_extracted, get_extracted, stop_and_answer.
   - Biudžetas: max 5 kvietimai (HERA_NAV_BUDGET, default 5); pasiekus — atsakyti iš surinkto.
   - Jungiklis: HERA_NAV=1 įjungia, HERA_NAV=0 = senas vienkartinis RAG (rollback be kodo). Įjunk =1 /root/hera.env.
   - Kiekvienam LLM/įrankio kvietimui — GRIEŽTAS timeout (pvz. 60s) + 1 retry, kad kilpa niekada nekabėtų
     (greičiausiai timeout'ą sukėlė kabantis kvietimas — būtinai apsisaugok).
   - document_bounded grounding taisyklė lieka galioti kilpoje.
   - Trajektorija: naršymo veiksmų seka loginama (kaip buvo prašyta).

2) TESTAS (greitas): 1 klausimas per kilpą („kas yra ATDP?") — parodyk veiksmų seką ir atsakymą;
   1 regresija su HERA_NAV=0 (senas kelias veikia). Jei kilpa stringa >2 min — HERA_NAV=0, pažymėk FAILED
   ir ataskaitoje aprašyk kur stringa (nekartok iki timeout!).

3) DURABILUMAS: pakeistų failų kopija į /opt/cad-site-agent/n8n/hera/ (lokaliai; push niekur NEDARYK).

TELEGRAM (trumpai, be raktų): (1) ar rasta pusiau padarytos būklės ir kas sutvarkyta, (2) kilpa veikia? testo
veiksmų seka trumpai, (3) HERA_NAV=1 prod'e (ar 0 jei FAILED + priežastis), (4) „NAPMEM-A ATSTATYTA" arba „FAILED".
