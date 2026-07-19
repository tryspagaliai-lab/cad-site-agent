UŽDUOTIS — SKUBU: patikrink ar 3 nauji bot-token kintamieji YRA /root/ai_digest.env (BE reikšmių). <5 min.
NEleisk pytest. Fail-safe. €0. RAKTŲ/REIKŠMIŲ NESPAUSDINK NIEKADA. Ataskaita TIK į HERA botą. Nieko NEKEISK — tik SKAITYK.

KONTEKSTAS: vartotojas per SSH pridėjo 3 naujų botų token'us į /root/ai_digest.env. Reikia patvirtinti kad įrašyti
teisingai, be reikšmių spausdinimo (saugumas). Dizaino eilutė anksčiau turėjo klaidą (PASTE_TOKEN) — patikrink kad
dabar švaru (tik viena teisinga eilutė kiekvienam).

ŽINGSNIAI (READ-ONLY, be reikšmių):
1) Kiekvienam kintamajam patikrink AR YRA eilutė ir KIEK jų (turi būti PO 1):
   - DESIGN_BOT_TOKEN
   - AGRO_BOT_TOKEN
   - AITECH_BOT_TOKEN
   Naudok: `grep -c '^DESIGN_BOT_TOKEN=' /root/ai_digest.env` ir t.t. (grąžina SKAIČIŲ, ne reikšmę).
2) Patikrink kad NĖRA likusios blogos eilutės `DESIGN_BOT_TOKEN=PASTE_TOKEN`:
   `grep -c 'PASTE_TOKEN' /root/ai_digest.env` (turi būti 0).
3) Patikrink token FORMATĄ be jo spausdinimo: ar reikšmė atitinka `^[0-9]+:` (skaičiai + dvitaškis)? Naudok tik
   TRUE/FALSE išvedimą, pvz.: `grep -qE '^DESIGN_BOT_TOKEN=[0-9]+:' /root/ai_digest.env && echo "DESIGN: formatas OK" || echo "DESIGN: BLOGAS"`.
   Tą patį AGRO ir AITECH. NIEKADA neišvesk pačios reikšmės.
4) Patvirtink kad TELEGRAM_TOKEN (senasis, @tryspagaliabot) NEpaliestas (grep -c, turi būti ≥1).

RIBOS: €0. READ-ONLY (jokio rašymo/keitimo). Raktų/reikšmių NIEKADA nespausdink — tik skaičiai/OK/BLOGAS. Anti-rc124.

ATASKAITA (HERA botas, TRUMPAI, be reikšmių): (a) DESIGN_BOT_TOKEN: kiek eilučių + formatas OK/blogas;
(b) AGRO_BOT_TOKEN: kiek + formatas; (c) AITECH_BOT_TOKEN: kiek + formatas; (d) PASTE_TOKEN likučių: 0/ne;
(e) TELEGRAM_TOKEN nepaliestas? (f) 1 eil. ar viskas paruošta topic-aware žingsniui.
