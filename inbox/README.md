# inbox — autonominio VPS agento užduočių dėžutė

VPS'e cron'as (kas 2 min) tikrina šitą failą per `n8n/vps_agent_runner.sh`.

- **TASK.md** — čia įrašoma užduotis (lietuviškai, laisvu tekstu). Kai turinys
  pasikeičia (ir nėra `IDLE`), VPS Claude Code ją įvykdo headless (`claude -p`)
  ir rezultatą atsiunčia į Telegram (@tryspagaliabot).
- Baigus, grąžink į `IDLE`, kad nepasileistų iš naujo.

Nereikia nei terminalo, nei connectorių — tik commit'as į šią šaką.
