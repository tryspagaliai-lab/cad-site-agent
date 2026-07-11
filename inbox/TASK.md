UŽDUOTIS — LOOP B RAPORTAI Į TELEGRAM KAS 6H (ne kas valandą). <6 min. NEleisk pytest. Telegram TRUMPAI.

SAUGUMAS: raktų nespausdink/necommit'ink.

KONTEKSTAS: vartotojui per dažni Loop B raportai (kas valandą). Nori KAS 6H.

1) Loop B skaičiavimus (concepts.md šviežinimas, cache-hit, klasteriai) palik kaip yra (valandinis — vidinis
   šviežumas svarbus). PAKEISK TIK Telegram raporto SIUNTIMĄ: siųsk tik kas 6 val (pvz. valandos 0/6/12/18,
   arba žymė paskutinio siuntimo). Tarp jų Loop B tyliai skaičiuoja, bet žinutės nesiunčia.
2) Fail-safe: jei throttle logika krenta — Loop B TĘSIA (geriau nusiųsti nei sulaužyti).
3) TESTAS: parodyk, kad throttle veikia (dabartinė valanda ne 0/6/12/18 -> raportas praleistas su log eilute).
4) DURABILUMAS: jei liesta hera kodą — kopija į /opt/cad-site-agent/n8n/hera/ + push į PRIVATŲ hera-core-backup.
   Viešo repo NELIESK.

TELEGRAM (trumpai, be raktų): (1) Loop B raportas dabar kas 6h, (2) skaičiavimai liko valandiniai,
(3) „LOOP B RAPORTAI KAS 6H".
