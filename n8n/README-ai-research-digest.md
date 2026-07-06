# AI Research Digest → Telegram (n8n workflow)

Kasdienė automatinė AI naujienų žvalgyba: workflow surenka, kas naujo buvo
išleista per pastarąsias 24 val. (modeliai, agentų įrankiai / harness / skills,
tyrimai, laboratorijų ir universitetų naujienos), Claude sudaro lietuvišką
santrauką ir ataskaita išsiunčiama į Telegram.

Failas importui: **`ai-research-digest.workflow.json`**

## Architektūra

```
Kasdien 08:00 (Europe/Vilnius)
  └─ Nustatymai (chatId, limitai, Claude modelis)
       ├─ RSS saltiniai (19 feed'ų) ─ Parsisiusti RSS ─ XML i JSON ─ Normalizuoti RSS ─┐
       └─ HF nauji modeliai (Hugging Face API) ─ Normalizuoti HF ─────────────────────┤
                                                                                       └─ Sujungti
                                                                                            └─ Sudaryti uzklausa
                                                                                                 └─ Ar yra naujienu?
                                                                                                      ├─ taip → Claude santrauka
                                                                                                      └─ ne ──────────────┐
                                                                                                             Padalinti zinutes (≤3800 simb.)
                                                                                                                  └─ Siusti i Telegram
```

## Stebimi šaltiniai

| Kategorija | Šaltiniai |
|---|---|
| Tyrimai (preprint) | arXiv cs.AI, cs.LG, cs.CL |
| Modeliai | Hugging Face API (naujausi modeliai) + HF Blog |
| Laboratorijos | OpenAI, Google DeepMind, Google AI, Meta AI, Microsoft Research, NVIDIA, Allen AI (AI2), EleutherAI |
| Universitetai | MIT News (AI), Stanford HAI, Berkeley BAIR, CMU ML Blog |
| Bendruomenė / įrankiai | Simon Willison (agentų įrankiai, harness, skills), The Gradient, Import AI |

Šaltinį pridėti / išimti — redaguok masyvą node „RSS saltiniai“ (Code node,
paprastas `{source, url}` sąrašas). Neveikiantis feed'as darbo nesustabdo
(`onError: continue`), jis tiesiog praleidžiamas.

Pastaba: Anthropic naujienoms oficialaus RSS nėra — jas padengia HF/bendruomenės
šaltiniai; galima pridėti per RSSHub, jei prireiks.

## Diegimas (VPS n8n)

1. **Importuok**: n8n → Workflows → Import from File → `ai-research-digest.workflow.json`.

2. **Telegram credential**: Credentials → New → *Telegram API* → įklijuok boto
   token (iš @BotFather). Priskirk jį node „Siusti i Telegram“.
   ⚠️ Token laikyk TIK n8n credentials — niekada necommit'ink į repo.

3. **Sužinok savo `chat_id`**:
   - Telegram'e parašyk botui bet ką (pvz., `/start`);
   - VPS'e paleisk:
     ```bash
     curl -s "https://api.telegram.org/bot<TOKEN>/getUpdates" | python3 -m json.tool
     ```
   - atsakyme rasi `"chat": {"id": 123456789, ...}` — tai tavo `chat_id`.

4. **Nustatymai**: node „Nustatymai“ įrašyk `chatId` (iš 3 žingsnio).
   Ten pat gali keisti: `maxAgeHours` (kiek valandų atgal žiūrėti),
   `maxPerSource`, `maxItemsTotal`, `claudeModel`.

5. **Anthropic credential**: Credentials → New → *Header Auth*:
   - Name: `x-api-key`
   - Value: tavo Anthropic API raktas (console.anthropic.com)
   Priskirk node „Claude santrauka“. (Norint kito LLM — pakeisk šio HTTP node
   URL/body į savo tiekėjo API.)

6. **Testas**: paspausk „Execute workflow“ — ataskaita turi ateiti į Telegram.

7. **Aktyvuok** workflow. Pagal nutylėjimą leidžiasi kasdien 08:00
   Europe/Vilnius (cron `0 8 * * *` node „Kasdien 08:00“ — keisk pagal poreikį;
   savaitinei apžvalgai: cron `0 9 * * 1` ir `maxAgeHours` = 170).

## Kaip veikia ataskaita

- Claude gauna visą surinktą sąrašą ir grupuoja į sekcijas:
  🧠 nauji modeliai · 🛠️ agentai/įrankiai/harness/skills · 📄 tyrimai (arXiv) ·
  🏛️ laboratorijos ir universitetai · ⭐ TOP 3 dienos įvykiai.
- Ataskaita rašoma lietuviškai, su nuorodomis.
- Ilgesnė nei 3800 simbolių žinutė automatiškai dalinama į kelias Telegram žinutes.
- Jei per parą naujienų nėra — atsiunčiamas trumpas pranešimas apie tai.

## Saugumas

- Boto token ir API raktai gyvena tik n8n Credentials — ne workflow JSON'e ir ne git'e.
- Jei token kada nors buvo persiųstas nesaugiu kanalu, pergeneruok jį per
  @BotFather (`/revoke`) ir atnaujink n8n credential.
