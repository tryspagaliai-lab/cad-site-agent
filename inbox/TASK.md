UŽDUOTIS — FIX routing: rc=0 ataskaitos → HERA botas (ne @tryspagaliabot). <10 min. NEleisk pytest. Telegram TRUMPAI.
SAUGUMAS KRITINIS: token reikšmių NIEKADA nespausdink/necommit'ink. Kodas -> PRIVATUS hera-core-backup. Viešo NELIESK.

KONTEKSTAS (iš audit'o): „✅/⚠️ VPS agentas baigė (rc=$RC)" ataskaitos siunčiamos per TELEGRAM_TOKEN →
@tryspagaliabot (tas pats botas kaip AI news digest). Vartotojas nori: @tryspagaliabot = TIK naujienos/nauji
išleidimai; VISOS operacinės ataskaitos (rc=0) → TIK HERA botas @tryspagaliai_hera_bot (HERA_BOT_TOKEN).
Live processor routing (dispatcher/Loop B) JAU teisingas — NELIESK. PARSER (@tryspagliai_bot) NELIESK.

1) RASK GYVĄ runner'į: audit'e repo turėjo tik `vps_agent_runner.sh.indexed`; faktinis deploy nerastas. Surask
   VEIKIANTĮ skriptą kuris siunčia „VPS agentas baigė (rc=$RC)" (ieškok: cron, systemd, n8n /files, /root, /opt,
   /home; grep „VPS agentas baigė" arba „rc=" siuntimo). Nustatyk TIKSLŲ failą kuris realiai vykdomas.

2) PAKEISK: to runner'io `send_tg` (ar analogiška siuntimo vieta) rc-ataskaitai naudok `HERA_BOT_TOKEN` (iš
   /root/hera.env) vietoj `TELEGRAM_TOKEN`. TIK rc/ops ataskaitos — news digest (ai_digest.py) LIEKA ant
   TELEGRAM_TOKEN/@tryspagaliabot, jo NELIESK. Necommit'ink token reikšmių.

3) TESTAS (privalomas — įrodyk): paleisk bandomąjį rc-pranešimą (arba runner'į dry/echo režimu) -> patvirtink kad
   testinė žinutė atkeliauja į @tryspagaliai_hera_bot (HERA), o @tryspagaliabot rc NEBEGAUNA. Patvirtink per getMe/
   chat_id kad taikinys teisingas (be token reikšmių). Jei runner'io vietos nerandi -> NEspėk/NEkeisk, pranešk
   „gyvas runner nerastas — reikia vartotojo/kelio" ir sustok (fail-safe).

4) DURABILUMAS: pakeistas skriptas -> hera-core-backup (BE tokenų). Jei skriptas gyvena n8n/vietoj kur necommit'inama
   — bent dokumentuok pakeitimą backup'e. ROADMAP/atmintis: „routing fix — rc=0 → HERA botas 2026-07-13".

TELEGRAM (per HERA botą, trumpai, BE token reikšmių): (1) gyvas runner rastas: <failas>, (2) rc=0 perjungtas
TELEGRAM_TOKEN→HERA_BOT_TOKEN, (3) TESTAS: testinė rc atėjo į @tryspagaliai_hera_bot, @tryspagaliabot rc nebegauna,
(4) news digest nepaliestas (@tryspagaliabot=tik naujienos), (5) „ROUTING SUTVARKYTA — ataskaitos tik į HERA botą".
