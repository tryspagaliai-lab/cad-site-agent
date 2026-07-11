UŽDUOTIS — PARUOŠTI TELEGRAM ISTORIJOS IŠTRAUKIMO SCRIPTĄ (@FlashCodeMon_bot) (VIENA SIAURA UŽDUOTIS). <10 min.
NEleisk pytest. Telegram TRUMPAI. Prisijungimas INTERAKTYVUS — jį vykdys VARTOTOJAS Termius'e, NE tu.

SAUGUMAS: raktų/sesijos NIEKUR nespausdink/necommit'ink. TG_API_ID/TG_API_HASH jau /root/hera.env.
Sesijos failas ir istorija — PRIVATU, TIK VPS, jokio push į jokį repo.

0) PATIKRA: ar /root/hera.env turi TG_API_ID ir TG_API_HASH (neprint'ink reikšmių, tik yra/nėra). Jei NĖRA — STOP,
   ataskaitoje „TG API RAKTŲ NĖRA".

1) TELETHON: sukurk izoliuotą venv /root/tgvenv (python3 -m venv), pip install telethon. (Nemaišyk su hera venv.)

2) SCRIPTAS /root/tg_pull.py (Python, Telethon), kuris:
   - skaito TG_API_ID, TG_API_HASH iš /root/hera.env (os.environ arba parse);
   - sesijos failas /root/.tg_session (Telethon StringSession faile arba SQLite sesija) — chmod 600;
   - jungiasi kaip VARTOTOJO paskyra (NE botas); PIRMĄ kartą interaktyviai paprašo telefono nr. ir kodo
     (Telethon pats prompt'ina) — tai vartotojas įves Termius'e;
   - po prisijungimo: resolve @FlashCodeMon_bot, ištraukia VISĄ pokalbio istoriją (iter_messages, be limito,
     su datom/tekstais/nuo ko), rašo į /root/flashcode_history.json (UTF-8, chmod 600). Parodo kiek žinučių ištraukta.
   - Jei sesija JAU yra (antras paleidimas) — neprašo kodo, iškart traukia.
   - Būk atsparus: jei @FlashCodeMon_bot nerandamas — aiški klaida; jei rate-limit (FloodWait) — palauk/pranešk.

3) NEPALEIDINĖK pats interaktyvaus login (tu non-interaktyvus, užkibtų). Tik PARUOŠK scriptą + venv.
   Ataskaitoje duok vartotojui TIKSLIĄ Termius komandą paleidimui, pvz.:
   `set -a; . /root/hera.env; set +a; /root/tgvenv/bin/python /root/tg_pull.py`

4) DURABILUMAS: patch/script į /opt/cad-site-agent/n8n/ lokaliai (be push į viešą). Sesijos/istorijos NEcommit'ink niekur.

TELEGRAM (trumpai, be raktų): (1) TG raktai rasti?, (2) telethon+scriptas paruošti?, (3) TIKSLI Termius komanda
vartotojui login+ištraukimui (viena eilutė), (4) „TG PULL SCRIPTAS PARUOŠTAS".
