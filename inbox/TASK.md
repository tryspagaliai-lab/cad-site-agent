UŽDUOTIS — PATAISYTI tg_pull.py: JUNGTIS KAIP VARTOTOJAS, NE BOTAS (VIENA SIAURA UŽDUOTIS). <10 min.
NEleisk pytest. Telegram TRUMPAI. Interaktyvaus login NEpaleidinėk (užkibtų) — tik pataisyk + duok komandą.

SAUGUMAS: raktų/sesijos/2FA nespausdink/necommit'ink. Privatu, tik VPS.

PROBLEMA: vartotojui paleidus tg_pull.py gauta „BotMethodInvalidError: API access for bot users is restricted
(GetHistoryRequest)". Reiškia klientas prisijungė KAIP BOTAS, ne kaip vartotojo paskyra — botai istorijos
neskaito. Reikia GRYNO user-login (telefonas+kodas+2FA), JOKIO bot_token.

1) IŠTRINK sena/sugadintą sesiją: rm -f /root/.tg_session* (kad autentikacija būtų švari, nauja).

2) PATIKRINK /root/tg_pull.py ir pataisyk, kad:
   - klientas kuriamas TIK su api_id, api_hash + sesijos failu: TelegramClient('/root/.tg_session', api_id, api_hash).
   - prisijungimas TIK per client.start(phone=...) VARTOTOJO srautu — interaktyvus phone -> code -> 2FA password.
     JOKIO bot_token niekur (patikrink, ar kode/aplinkoje neįsivėlė HERA_BOT_TOKEN/BOT_TOKEN — jei script'as
     kur nors ima tokeną, PAŠALINK tą kelią).
   - jei client.is_bot() True po prisijungimo — nutrauk su aiškia klaida „prisijungta kaip botas, reikia user".
   - po user-login: resolve @FlashCodeMon_bot -> iter_messages (visa istorija) -> /root/flashcode_history.json (600).
   - jei paskyra turi 2FA — Telethon pats paprašys password (SessionPasswordNeeded) — tai OK, vartotojas įves.

3) NEpaleisk pats. Ataskaitoje duok TIKSLIĄ vieną komandą vartotojui:
   set -a; . /root/hera.env; set +a; /root/tgvenv/bin/python /root/tg_pull.py
   ir aiškiai parašyk seką: telefonas +447516580893 -> kodas iš Telegram -> Telegram 2FA slaptažodis
   (NE VPS, NE api_hash). Jei 2FA neatsimena — Telegram app Settings > Privacy & Security > Two-Step Verification.

4) Kopija į /opt/cad-site-agent/n8n/ lokaliai (be push į viešą). Sesijos/istorijos necommit'ink.

TELEGRAM (trumpai, be raktų): (1) sena sesija ištrinta, (2) tg_pull.py dabar TIK user-login (bot kelio nėra),
(3) tiksli komanda+seka vartotojui, (4) „TG PULL PATAISYTA — USER LOGIN".
