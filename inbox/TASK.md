UŽDUOTIS — WIKI GRAFO SUJUNGIMAS (deterministinis auto-linkinimas, sumažinti orphan). <12 min.
NEleisk viso pytest — tik taikinius. Telegram TRUMPAI. €0, BE LLM. Fail-safe: klaida nelaužo HERA.

SAUGUMAS: raktų nespausdink/necommit'ink. Vault edit'ai eina per git (curator matys diff). Push į PRIVATŲ.

KONTEKSTAS: lint parodė 40 orphan iš 70 — vault dar nesujungtas. Dabar sujungiam DETERMINISTIŠKAI (be LLM),
kad grafas taptų tikras ir orphan kristų.

1) hera_wikilink.py (deterministinis): kiekvienam skills/growth puslapiui pridėk `[[nuorodas]]` į giminingus
   puslapius pagal AIŠKIUS, ne spėjamus ryšius:
   - skill <-> jo source_job growth (jei yra) — dvipusiai;
   - puslapiai tame pačiame Loop B klasteryje (kind×domenas) — susiek top-artimiausius (pvz. iki 3);
   - puslapiai, dalinantis >=2 concepts.md tokenais/konceptu — susiek;
   - esamas `related_*` frontmatter -> paversk `[[]]` kūne (jei dar ne).
   Ribos: max ~3-5 nuorodos vienam puslapiui (ne perkrauti); dvipusiškumas; dedup; NEliesk jau esamų `[[]]`.
   Įterpk tvarkingai (pvz. sekcija „## Susiję" puslapio gale). Idempotent (antras paleidimas nedubliuoja).

2) NEDIRBK su LLM (šitas turi būti greitas ir pigus). Jei koks ryšys neaiškus — praleisk (geriau mažiau
   nuorodų nei klaidingų).

3) PALEISK + PERLINT: po linkinimo paleisk hera_lint.py -> parodyk orphan/dangling/be-out skaičius PRIEŠ (40/1/40)
   ir PO. Tikslas — orphan reikšmingai mažesnis.

4) TESTAS: (a) 1 skill puslapio pavyzdys su nauja „Susiję" sekcija (be raktų); (b) idempotencija — paleisk 2x,
   nuorodos nedubliuojasi; (c) lint PO < lint PRIEŠ (orphan sumažėjo).

5) DURABILUMAS: vault pakeitimai commit'inami ir sync'inami (privatus hera-vault per cron arba rankinis sync).
   hera_wikilink.py kopija į /opt/cad-site-agent/n8n/hera/ + push į PRIVATŲ hera-core-backup. Viešo NELIESK.

TELEGRAM (trumpai, be raktų): (1) auto-linkinimas atliktas, kiek nuorodų pridėta, (2) lint PRIEŠ vs PO
(orphan skaičius), (3) idempotencija OK, (4) „WIKI GRAFAS SUJUNGTAS".
