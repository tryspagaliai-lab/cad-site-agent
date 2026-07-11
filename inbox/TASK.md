UŽDUOTIS — BOTŲ MARŠRUTAS: SANTRAUKA PER PARSER_BOT_TOKEN Į @tryspagliai_bot. <12 min.
NEleisk pytest. Telegram TRUMPAI. Fail-safe. PRIORITETAS — vartotojas pyksta, dar neveikia.

SAUGUMAS: raktų/tokenų NIEKUR nespausdink.

FAKTAS: vartotojas ką tik įrašė PARSER boto tokeną į /root/hera.env kaip **PARSER_BOT_TOKEN** (patvirtinta, ilgis 46).
`getMe` su juo → @tryspagliai_bot (PARSER). Naudok TIESIAI šitą kintamąjį, nebespėliok.

BOTAI:
- PARSER = @tryspagliai_bot, tokenas = **PARSER_BOT_TOKEN** (/root/hera.env). ČIA vartotojas meta linkus; ČIA
  turi grįžti pilna santrauka + isparsinta info + eilės ACK „🔎 Priimta".
- HERA = @tryspagaliai_hera_bot (jo tokenas hera.env, HERA/HERA_BOT). TIK sistemos ataskaitos (Loop B, lint,
  VPS agento ataskaitos). JOKIOS santraukos.
- Digest = @tryspagaliabot — nekeisti.

1) PATIKRA: getMe su PARSER_BOT_TOKEN → turi grąžinti username @tryspagliai_bot (nespausdink tokeno). Patvirtink.

2) TAISYMAS: hera_fullsend/dispatcher — pilnos santraukos (extracted full.md) siuntimas turi eiti per
   **PARSER_BOT_TOKEN** į chat 725037198 (NE per HERA botą). Santrauka VISADA dalimis (≤3800 simb.), NE dokumentu.
   Eilės ACK „🔎 Priimta" taip pat per PARSER_BOT_TOKEN (kur metė linką).
   Jei ingest ateina per n8n ir n8n pats siunčia ACK — suderink, kad santrauka (iš processor) eitų per PARSER,
   o ne dubliuotųsi ir ne per HERA botą.

3) HERA botas: įsitikink, kad į @tryspagaliai_hera_bot NEBEeina santrauka/„📖 analizė" — tik sistemos ataskaitos.

4) HERA vidinis apdorojimas (ingest/taryba/vault/tyrimas) NEKEISK.

5) TESTAS: perleisk 1 kandidatą (turintį full.md) per siuntimo funkciją -> santrauka realiai nueina į PARSER
   @tryspagliai_bot dalimis; HERA bote santraukos NĖRA. Fail-safe: klaida nelaužo ingest.

6) DURABILUMAS: kopija į /opt/cad-site-agent/n8n/hera/ + push į PRIVATŲ hera-core-backup. Viešo NELIESK.

TELEGRAM ataskaita per HERA botą, trumpai, be raktų: (1) getMe PARSER_BOT_TOKEN → @tryspagliai_bot patvirtinta?,
(2) santrauka+ACK dabar per PARSER (dalimis), (3) HERA bote santraukos nebėra, (4) testas: santrauka nuėjo į
PARSER (taip/ne), (5) „PARSER MARŠRUTAS SUTVARKYTAS".
