UŽDUOTIS — BOTŲ MARŠRUTAS (TIKSLŪS VARDAI): SANTRAUKA GRĮŽTA Į PARSER @tryspagliai_bot. <12 min.
NEleisk pytest. Telegram TRUMPAI. Fail-safe: klaida nelaužo ingest. PRIORITETAS — vartotojas pyksta, dar neveikia.

SAUGUMAS: raktų/tokenų NIEKUR nespausdink (net getMe atsakymuose token nerodyk).

TIKSLŪS BOTAI (patvirtinta iš vartotojo screenshot'o) — nebespėliok:
- **PARSER = @tryspagliai_bot** — ČIA vartotojas meta linkus/turinį. Santrauka + isparsinta info TURI GRĮŽTI ČIA.
- **HERA = @tryspagaliai_hera_bot** — TIK sistemos ataskaitos (ACK, Loop B, lint, VPS agento ataskaitos). JOKIOS santraukos.
- **Digest = @tryspagaliabot** — nekeisti (AI digest).

PROBLEMA: pilna santrauka/isparsinta info dabar siunčiama į HERA botą (@tryspagaliai_hera_bot) — KLAIDA.
Turi grįžti ten, kur vartotojas metė linką = PARSER @tryspagliai_bot.

1) ŽEMĖLAPIS (per getMe, be tokenų spausdinimo): nustatyk, kuris /root/hera.env tokenas atitinka kurį botą
   (username per getMe). Reikia rasti PARSER (@tryspagliai_bot) boto tokeną. Jei jo hera.env NĖRA — STOP,
   ataskaitoje „PARSER @tryspagliai_bot TOKENO NĖRA hera.env — reikia jį pridėti" (tada vartotojas pridės).
2) TAISYMAS: pilnos analizės/santraukos siuntimas (hera_fullsend/dispatcher) — perkreipk, kad siųstų per
   PARSER (@tryspagliai_bot) tokeną į vartotojo chat (725037198), NE per HERA botą. Eilės ACK „🔎 Priimta"
   irgi turi būti PARSER'yje (kur metė linką). Santrauka VISADA dalimis (≤3800 simb.), NE dokumentu.
3) HERA botas (@tryspagaliai_hera_bot): įsitikink, kad į jį NEBEeina jokia santrauka/„📖 analizė" — tik
   ataskaitos (ACK su balu/verdiktu, Loop B, lint, agento ataskaitos). Jei ACK turi eiti į PARSER, o systemos
   raportai į HERA — atskirk: turinio atsakymai -> PARSER; sistemos raportai -> HERA botas.
4) HERA vidinis apdorojimas (ingest/taryba/vault/tyrimas) NEKEISK.
5) TESTAS: perleisk 1 kandidatą -> patvirtink, kad santrauka nueina į PARSER @tryspagliai_bot (dalimis), o
   HERA bote santraukos NĖRA. Fail-safe: klaida nelaužo ingest.
6) DURABILUMAS: kopija į /opt/cad-site-agent/n8n/hera/ + push į PRIVATŲ hera-core-backup. Viešo NELIESK.

TELEGRAM ataskaitą siųsk per HERA botą (@tryspagaliai_hera_bot), trumpai, be raktų: (1) kuris tokenas = PARSER
(username, be token), (2) santrauka dabar grįžta į PARSER @tryspagliai_bot dalimis, (3) HERA bote santraukos
nebėra, (4) „PARSER MARŠRUTAS SUTVARKYTAS" arba „PARSER TOKENO TRŪKSTA".
