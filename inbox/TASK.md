UŽDUOTIS — AUDIT: nustatyk botus + dabartinį ataskaitų routing'ą. TIK PERŽIŪRA, NIEKO NEKEISK. <8 min.
NEleisk pytest. Telegram TRUMPAI. SAUGUMAS KRITINIS: tokenų/raktų reikšmių NIEKADA nespausdink (nei į logą, nei
Telegram, nei failą). Viešo repo NELIESK. Kodo NEKEISK — tik skaityk ir raportuok.

KONTEKSTAS: Botų pavadinimai panašūs (@tryspagaliabot vs @tryspagaliai_hera_bot), painiava. Reikia TIKSLIAI
nustatyti kuris token=kuris botas=ką dabar siunčia, kad galėčiau taisyti routing'ą be spėjimo. Vartotojo skundas:
operacinės ataskaitos (VPS agentas rc=0 ir pan.) nutekа į PARSER botą, o turi eiti TIK į HERA botą; PARSER = tik
tyrimų/naujienų rezultatai.

1) BOTŲ IDENTIFIKACIJA (be token reikšmių): rask hera.env bot-token kintamuosius (pvz. PARSER_BOT_TOKEN,
   HERA_BOT_TOKEN / TELEGRAM_* — kokie bebūtų). Kiekvienam iškviesk Telegram API getMe (curl) ir gauk bot @username
   + display name. Raportuok lentelę: ENV_VAR_PAVADINIMAS → @username → display name. TOKEN REIKŠMĖS NEspausdink
   (nei pilnos, nei dalies). Tik env-var vardą ir gautą @username.

2) ROUTING AUDIT (kodas, tik skaitymas): rask KUR kode siunčiamos žinutės ir su KURIUO token/env-var:
   - Ingest rezultatai (📥 Priimta / 📖 transkriptai) — su kuriuo botu?
   - „VPS agentas baigė (rc=0)" cron-runner completion report — su kuriuo botu? (Įtariu čia problema.)
   - Loop B ataskaita — su kuriuo?
   - Fazių/operacinės (per-ingest 🧠 log, gate 🔎) — su kuriuo?
   Raportuok: kiekvienas pranešimo TIPAS → kuris env-var/botas siunčia (pagal kodą). Nurodyk failą:eilutę.

3) IŠVADA: aiškiai pasakyk kuris @username yra PARSER (tyrimų) ir kuris HERA (ataskaitų), IR kurie pranešimų tipai
   dabar KLAIDINGAI eina į PARSER (turėtų į HERA). Jokių pakeitimų — tik planas ką taisyti.

TELEGRAM (per HERA botą — jei neaišku kuris, tai pats audit'as pasakys; siųsk trumpai, BE token reikšmių):
(1) botų mapping: env-var → @username (be tokenų), (2) routing: kuris pranešimų tipas → kuris botas, (3) kurie tipai
klaidingai PARSER'yje, (4) „AUDIT BAIGTA — routing planas paruoštas, pakeitimų NEdaryta".
