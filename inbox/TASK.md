UŽDUOTIS — NAUJO HERA BOTO PRIJUNGIMAS (@tryspagaliai_hera_bot) (VIENA SIAURA UŽDUOTIS). <12 min.
NEleisk pytest. Telegram TRUMPAI. SVARBU: tokenų NIEKUR nespausdink — HERA_BOT_TOKEN jau yra /root/hera.env.

TIKSLAS: naujas botas @tryspagaliai_hera_bot = GRYNAS HERA interfeisas (ingest + klausimai + feedback + ACK +
Loop B raportai). Senas @tryspagaliabot LIEKA: AI digest + VPS agento (runner) ataskaitos. chat_id tas pats 725037198.

0) Patikrink kad HERA_BOT_TOKEN yra /root/hera.env (neprint'ink reikšmės; tik yra/nėra). Jei NĖRA — STOP,
   ataskaitoje „TOKENO NĖRA", nieko nekeisk.
1) OUTBOUND (paprasčiausia dalis): hera-processor tg siuntimas (ACK, atsakymai, Loop B raportai, council
   žinutės) -> naudok HERA_BOT_TOKEN vietoj senojo. Runner'io/digest'o siuntimo NELIESK (jie lieka per seną).
   Testas: išsiųsk per naują botą „🤖 HERA botas prijungtas ✅" į 725037198.
2) INBOUND: n8n pusėje prijunk naujo boto žinučių priėmimą į tą patį kelią (writeIngestJob -> 8799):
   BACKUP pirma (/root/linkparser_pre_herabot.json). Saugiausias kelias — nauja Telegram credential su
   HERA_BOT_TOKEN ir Link Parser poll'as perjungiamas į naują botą (arba dubliuotas workflow naujam botui,
   senojo polling'ą palik kol patvirtinta). Eilės ACK („🔎 Priimta...") turi grįžti per NAUJĄ botą.
3) SUDERINAMUMAS: jei vartotojas per klaidą siųs turinį į SENĄ botą — nieko baisaus neturi nutikti (arba
   toliau veikia kaip anksčiau, arba trumpas atsakymas „siųsk į @tryspagaliai_hera_bot"). Pasirink paprastesnį.
4) TESTAS: (a) outbound per naują botą suveikė (žinutė išsiųsta, HTTP 200); (b) inbound — dry-run arba realus:
   ataskaitoje paprašyk vartotojo nusiųsti į @tryspagaliai_hera_bot žinutę „labas HERA" kaip galutinį E2E testą.
5) ROLLBACK: jei kas lūžta — grąžink backup'ą, senas botas lieka pilnai veikiantis, ataskaitoje FAILED+kodėl.
6) ŠALUTINĖ PATIKRA (1 eilutė): ar vault higienos užduotis (d55c07e — eviction žymės/OPEN_QUESTIONS.md) buvo
   įvykdyta anksčiau — taip/ne. Jei ne, pačios užduoties nedaryk, tik pažymėk.
7) DURABILUMAS: pakeitimai į /opt/cad-site-agent/n8n/hera/ kopiją (be push į viešą) + push į PRIVATŲ
   hera-core-backup; n8n patch skriptas į /opt/cad-site-agent/n8n/ lokaliai.

TELEGRAM ataskaita per SENĄ kanalą kaip visada (trumpai, be raktų): (1) outbound per naują botą OK?,
(2) inbound prijungtas — per ką (credential perjungta/dubliuotas workflow), (3) prašymas vartotojui: siųsk
„labas HERA" į @tryspagaliai_hera_bot, (4) vault higiena anksčiau įvykdyta taip/ne, (5) „HERA BOTAS PRIJUNGTAS".
