UŽDUOTIS — CAVEMAN: GLAUSTI LLM ATSAKYMAI (token'ų taupymas, €0). <10 min.
NEleisk viso pytest — tik taikinius. Telegram TRUMPAI. Fail-safe: nekeisk vertinimo kokybės, tik daugiažodiškumą.

SAUGUMAS: raktų nespausdink/necommit'ink. Jei liesta HERA kodą — push į PRIVATŲ hera-core-backup.

KONTEKSTAS: iš dev-tools video „Caveman" idėja — priversti LLM kalbėti glaustai (išlaikant techninę esmę,
pašalinant vandenį) → iki ~65% mažiau token'ų. Diegiam kaip SISTEMOS dalį.

1) GLAUSTUMO DIREKTYVA: sukurk trumpą sistemos prompt fragmentą (pvz. hera_terse.py: TERSE_DIRECTIVE string):
   „Atsakyk glaustai. Išlaikyk techninę/faktinę esmę, pašalink įžangas, pasikartojimus, mandagumo frazes.
   Trumpi sakiniai/fragmentai. Be „as an AI"/„svarbu pažymėti"." (LT+EN mišru, veikia abiem.)
   Įpink jį į HERA LLM kvietimus, kur išvestis ilga ir vidinė (NE vartotojui skirti atsakymai, jei nori pilnesnių):
   - selektoriaus reason lauką (trumpesnis pagrindimas),
   - council juror reason,
   - hera_optimize/replay verdiktų tekstą.
   VARTOTOJUI skirti RAG atsakymai (vault query) — palik informatyvius, bet taip pat gali turėti „be vandens" toną.

2) NEKEISK struktūros/schema: JSON laukai, score, verdict — tie patys; keičiasi TIK teksto daugiažodiškumas.
   NEsutrumpink taip, kad dingtų priežastis (reason turi likti suprantamas, tik be balasto).

3) JUNGIKLIS: env HERA_TERSE=1 įjungia (default 1); =0 rollback be kodo. Įrašyk =1 /root/hera.env.

4) TESTAS: (a) 1 selektoriaus arba juror kvietimas su HERA_TERSE=1 vs =0 — parodyk reason ilgio skirtumą
   (simboliai/apytiksliai token'ai), esmė išlikus; (b) score/verdict schema nepakito (council units žali).

5) DURABILUMAS: kopija į /opt/cad-site-agent/n8n/hera/ + push į PRIVATŲ hera-core-backup (secret-scan).
   Viešo repo NELIESK.

TELEGRAM (trumpai, be raktų): (1) glaustumo direktyva įpinta (kur), (2) testas — reason token'ų ~% sumažėjimas,
schema nepakito, (3) HERA_TERSE=1, backup OK, (4) „CAVEMAN GLAUSTUMAS ĮDIEGTAS".
