UŽDUOTIS — Fazė 42: ar `claude-agent-sdk` veikia su MŪSŲ esama OAuth prenumerata (be API rakto)? MATAVIMAS. HUMAN-GATE GAUTAS („Varom"). <14 min.

## Kodėl (kontekstas, kurio pats neišvestum)
`vps_agent_runner.sh` dabar kviečia `claude -p` ir **skaito tekstinę išvestį**. Tai trapiausia grandinės vieta —
iš jos kyla „ataskaita teigia tai, ko nepadarė" klasė klaidų, kurias gaudom rankiniu tikrinimu kiekvieną fazę.
**Claude Agent SDK** (`claude-agent-sdk`, Python) yra Claude Code supakuotas kaip biblioteka: agent loop,
konteksto valdymas, hooks, subagentai, teisės, sesijos — programinė sąsaja vietoj teksto parsinimo.

⚠️ **NEPAINIOTI su `anthropic-sdk-python`** — tai kitas produktas, reikalaujantis API rakto (= pinigai;
mūsų vienintelį raktą ką tik sąmoningai ištrynėm). Šioje užduotyje jo NELIEČIAM.

## Vienintelis klausimas, į kurį reikia atsakyti
**Ar `claude-agent-sdk` autentifikuojasi mūsų ESAMA prenumeratos OAuth sesija, be jokio API rakto?**

Nespręsk to iš dokumentacijos — **išbandyk**. Priežastis, kodėl tai tikrai atviras klausimas:
Anthropic dokumentacija sako, kad Claude Code ir Agent SDK laikosi to paties kredencialų eiliškumo, kuriame yra
**`ant auth login` profilis** (`~/.config/anthropic/`). BET mūsų runner naudoja **`/root/.claude/.credentials.json`** —
tai Claude Code NUOSAVA saugykla, kitas kelias. Ar SDK skaito ir ją, ar tik `ant` profilius — **nežinoma.**
Tai ir yra matavimo esmė.

## 🔴 Tai MATAVIMAS, ne migracija
`vps_agent_runner.sh` NELIESK. Nieko neprijunk. Nekeisk jokio esamo modulio. Tikslas — vienas sąžiningas
taip/ne su įrodymu, ir kaina, jei taip.

## Ką išmatuoti ir pranešti
1. **Ar autentifikacija veikia.** Minimalus testas: SDK užklausa su labai trumpu promptu („atsakyk vienu žodžiu").
   **Neleisk jokių brangių ar ilgų užklausų** — tikrinam autentifikaciją, ne pajėgumus.
2. **KURI kredencialų grandies dalis suveikė.** Konkrečiai: ar SDK rado `/root/.claude/.credentials.json`,
   ar reikėjo `ant auth login` profilio, ar išvis nepavyko be API rakto. **Tai svarbiausia ataskaitos dalis.**
3. ⚠️ **PATIKRINK DOKUMENTUOTĄ SPĄSTĄ:** OAuth profilis veikia TIK kai `ANTHROPIC_API_KEY` **neapibrėžtas** —
   net **tuščias** `ANTHROPIC_API_KEY=""` laimi savo eiliškumo vietą ir bando autentifikuotis tuščiu raktu.
   Patikrink, ar tas kintamasis apskritai egzistuoja runner'io/cron aplinkoje (net tuščias). Jei egzistuoja —
   tai būsimos migracijos blokatorius ir turi būti ataskaitoje.
4. **Kaina:** diegimo dydis (venv/npm), RAM, šalto starto laikas. *(Fazė 41 pamoka: skaičiai sprendžia, ne idėja.)*
5. **Kvotos klausimas:** ar SDK naudojimas semia iš TOS PAČIOS prenumeratos kvotos kaip `claude -p`.
   Mums tai svarbu — 2026-07-20 buvo išdegintas bendras limitas, todėl runner pinnintas prie Sonnet 5.
   Jei nustatyti neįmanoma be didelio naudojimo — **NEBANDYK to išsiaiškinti degindamas kvotą**, pasakyk.

## Ribos
- **€0.** Jokių API raktų, jokių mokamų kelių. Jei SDK reikalauja API rakto — tai NEIGIAMAS atsakymas, ir gerai; pranešk.
- **NEDIEK į sisteminį python3.** Laikinas venv; po matavimo išvalyk ir pranešk, ką palikai/ištrynei.
- **n8n neturi nukentėti.** Jei RAM prie ribos — sustok (Fazės 41 elgsena su cgroup saugikliu buvo teisinga).
- Viešo `cad-site-agent` git NELIESK · BACKUP jei ką nors keistum (neturėtum) · HARD timeout, be retry.

## Ataskaitoje
Vienareikšmis **TAIP / NE / NEĮMANOMA NUSTATYTI** dėl OAuth autentifikacijos · kuri kredencialų grandies dalis
suveikė · `ANTHROPIC_API_KEY` būsena aplinkoje · kaina (diskas/RAM/startas) · kvotos atsakymas arba sąžiningas
„negaliu nustatyti nedegindamas kvotos" · **tavo rekomendacija: verta migruoti ar ne, ir kodėl.**

**ATASKAITOS TAISYKLĖ:** teiginys „neįmanoma / nepavyko patikrinti" galioja **tik kartu su sąrašu, KĄ BANDEI.**
Negalimybė turi būti pagrįsta veiksmais, ne intuicija. Neapsimesk, kad patikrinai, jei tik pažiūrėjai.

Jei STOP — kodėl.
