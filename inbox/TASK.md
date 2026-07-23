UŽDUOTIS — GREITA: patikrinti hera_semsearch.py integralumą po v1.2 timeout, restore jei sugadintas. TIK tai. <5 min.
NEleisk pytest. Fail-safe. €0. Ataskaita TIK į HERA botą. Viešo cad-site-agent NELIESK. NEDARYK jokio 16-query testo, jokio index rebuild jei nereikia.

KONTEKSTAS: praeita v1.2 užduotis (boilerplate filtras) NUTRŪKO per timeout (rc=124) — per didelė vienam ciklui. hera_semsearch.py
gali būti pusiau-suredaguotas. Reikia grąžinti į ŽINOMĄ-GERĄ būseną. Semsearch def 0, dormant — jokia gyva sistema nepaveikta.

ŽINGSNIAI (greiti):
1) `HERA_SEMSEARCH=1 python3 <kelias>/hera_semsearch.py --selftest 2>&1 | tail -20` → ar PASS?
   - Jei PASS → failas sveikas (arba v1.1, arba dalinis v1.2 kuris vis tiek veikia). Pažymėk kurioj versijoj (grep ar yra boilerplate-filtro kodas).
   - Jei FAIL / import error / crash → SUGADINTAS: restore iš naujausio backupّо:
     `ls -t /root/hera-core-backup/hera_semsearch.py.* | head -1` → cp į veikiantį kelią → dar kartą --selftest → turi PASS.
2) NEDARYK boilerplate filtro dabar (tai atskiras mažas žingsnis kitą kartą). NErebuild'ink index jei selftest nereikalauja.
3) Patvirtink galutinę būseną: selftest PASS + kuri versija (v1.1 švari / v1.2 dalinis-bet-veikia / restored).

ATASKAITA (HERA botas, trumpai): selftest rezultatas (prieš/po restore jei reikėjo); ar buvo sugadintas; galutinė versija (v1.1/v1.2-partial/restored); ar boilerplate-filtro kodas faile yra ar ne. Nieko daugiau nedaryta.
