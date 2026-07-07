UŽDUOTIS — HERA Fazė 5: SONA-įkvėptos laiko kilpos + ReasoningBank + EWC-lite. Autonomiškai
(superpowers OK). NELIESK veikiančių Fazės 2–4 — tik PRAPLĖSK. Feasible tik NEMOKAMAM stack'ui:
Gemini free, JOKIO treniravimo/RL/svorių/GPU. Laikykis RIC gardo, append-only, žmogaus-gate destruktyviems.
Atsiskaityk į Telegram TRUMPAI, aiškiu galutiniu statusu.

Tikslas: PANAUDOTI jau loginamą ATDP `reward` lauką, kad jis realiai VALDYTŲ HERA sprendimus (dabar tik saugomas).

1) LOOP B (planinė, valandinė — pridėk į hera-processor ciklą ar cron). Klasterizuok ATDP-lite trajektorijas
   (paprastas grupavimas pagal kind/domeną arba TF-IDF/lexical; jei nori — Gemini embeddings, bet neprivaloma) →
   kiekvienam klasteriui vidutinis kokybės/reward balas → raportas /opt/hera-vault/analysis/loopB-<data>.md,
   išryškinantis SILPNAS sritis (žemas reward). Nieko nekeičia, tik raportuoja.

2) LOOP C (planinė, savaitinė). Vault konsolidacija: aptik dublikatinius/panašius skills+growth →
   PASIŪLYK merge/prune į /opt/hera-vault/proposals/ (STAGED, NEtrina — RIC + append-only, promote tik žmogus).
   Sukurk sąvokų indeksą /opt/hera-vault/index/concepts.md (kas vault'e yra, sugrupuota).

3) REASONINGBANK (/opt/hera-vault/reasoningbank.jsonl). Įrašai: (užduoties/konteksto parašas, panaudotas
   prompt/skill, reward). Retrieval helper: naujai užduočiai parenka aukščiausio-reward variantą →
   integruok į selektorių/skill-retrieve, kad reward'as KREIPTŲ pasirinkimą. Tai uždaro self-improve kilpą.

4) EWC-LITE. Pridėk `importance` (0..1) lauką skills'ams — kaupiamas iš reward+panaudojimo. hera_optimize/Loop C
   negali perrašyti aukštos importance įgūdžio be STIPRESNIO replay-pagerėjimo slenksčio (apsauga nuo katastrofiško
   „užmiršimo"). Dokumentuok slenksčius.

5) SELF-TEST: (a) Loop B ant esamų trajektorijų → silpnų sričių raportas; (b) ReasoningBank užpildyk iš esamų
   reward event'ų ir parodyk vieną reward-kreipiamą pasirinkimą; (c) EWC-lite importance ant ai-wargaming-metodika;
   (d) Loop C dry-run → bent 1 merge/prune pasiūlymas (necommit'intas į gamybą).

6) DURABILUMAS: kodą kopijuok į /opt/cad-site-agent/n8n/hera/. Push nedaryk (nėra creds).

Į Telegram: kas pridėta (Loop B/C, ReasoningBank, EWC-lite), self-test rezultatai, ir aiškiai
„FAZĖ 5 BAIGTA" arba ko trūksta.
