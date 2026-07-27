UŽDUOTIS — Fazė 32: `hera_skillcapture` prijungimas prie runner'io (post-hook, ADVISORY — duomenys pradeda kauptis). <14 min.

## Tikslas
`hera_skillcapture` (Fazė 23, 7/7 PASS) pastatytas, bet **niekas jo nekviečia — pėdsakai NESIKAUPIA.**
Vartotojas patvirtino: prijungti kaip **runner post-hook**, advisory-first. Po kiekvienos įvykdytos inbox užduoties
fiksuoti kanoninį pėdsaką (užduotis → žingsniai → rezultatas) į diską. **Šiame žingsnyje TIK kaupiam ir raportuojam
kiekį — jokio semsearch indeksavimo, jokio panaudojimo srauto.** Indeksavimas = atskiras human-gate po duomenų peržiūros.

**Kodėl tai svarbiausia likusi jungtis:** kuruotas FlowEvo (arXiv, 2026-07-27) parodė, kad HERA turi visus tris jo
mechanizmus (workflow→skill kompiliavimas, skill→workflow grįžtamasis ryšys, įgūdžių kuravimas), bet **miega būtent
čia** — be kaupiamų pėdsakų neveikia nei ištraukimas, nei naudingumo sekimas. Taryba (4/5) tą patį patvirtino
2026-07-24: dvigubo naudojimo formatas duoda RAG naudą DABAR ir lieka LoRA-paruoštas jei kada bus GPU.

## Realybė (ko pats neišvestum)
- ⚠️ **Kanoninis kelias = `/opt/hera-processor/`** (ką tik nustatyta Fazėje 31: runner kvietė pasenusią
  `/opt/cad-site-agent/n8n/hera/` kopiją ir Fazės 30 pataisa NEBUVO gyva; `/usr/local/bin/vps_agent_runner.sh`
  dabar symlink į `/opt/hera-processor/vps_agent_runner.sh`). **Naudok kanoninį kelią, nekurk naujos kopijos.**
- Runner turi TASK.md tekstą ir agento išvestį (`/root/agent_result_<blob>.txt`) — abu reikalingi pėdsakui.
- Integracijos precedentas, kurį sek: `GA_NOTE` (Fazė 22) / `VE_NOTE` (Fazė 29) — `timeout N ... || true`,
  jungiklis, anotacija prieš `send_tg`. **NEKEISTI:** `flock`, HARD timeout, STATE dedup, exit code, cron.
- `hera_skillcapture` API: `capture(task, steps, context, final_response, outcome, tags, skill_id, save_dir)`;
  `to_sft(record)`. Def 0 = dry-run (skaičiuoja, nerašo). Šiai integracijai reikės jungiklio, kuris LEIDŽIA rašyti —
  pasirink vardą ir def reikšmę, pagrįsk (žr. Fazės 26 staleguard precedentą: def0=advisory buvo pagrįstas matomumu).
- **`outcome` laukas kritiškas** (tyrimas + FlowEvo vieningi: tik SĖKMINGI pėdsakai verti mokymui/ištraukimui).
  Runner žino `rc` — naudok jį, nespėliok.

## Apribojimai
€0, be tinklo, be LLM (LLM-struktūrizavimas = vėliau). Fail-safe: **capture klaida NEGALI paveikti užduoties rezultato
ar ataskaitos** — `|| true` + tęsti. Ataskaita TIK į HERA botą. Viešo `cad-site-agent` NELIESK (nei git, nei kopijų).
BACKUP prieš keitimą. Cron NELIESK. `hera_verify`/`staleguard`/`goalanchor` integracijų NELIESK.
🔴 **SECRET'AI:** pėdsakai saugo TASK.md ir išvestį — jie gali turėti kelių, token'ų vardų, vidinių URL.
Saugykla turi būti **PRIVATI** (ne viešo repo medyje, ne git-tracked viešai). Jei matai riziką, kad į pėdsakus pateks
kredencialai — pridėk paprastą redakciją arba PASAKYK ataskaitoje, kad to nedarei ir kodėl.

## Įrodymai
1. **Elgesys nepakito:** su jungikliu išjungtu runner elgiasi identiškai; su įjungtu — ataskaita ir exit code tokie patys,
   skiriasi tik tai, kad atsiranda pėdsakas. Parodyk.
2. **Pėdsakai TIKRAI kaupiasi:** paleisk bent vieną realų ciklą (arba tikslią simuliaciją su realiu TASK.md+result) →
   parodyk sukurto įrašo **kelią, dydį ir laukus**. Vienas pilnas pavyzdys (sutrumpintas) ataskaitoje.
3. **`outcome` teisingas:** sėkmingas ciklas → `success`; nesėkmingas (rc≠0) → atitinkamai. Parodyk, iš kur imi signalą.
4. **`to_sft()` veikia ant TIKRO surinkto įrašo** (ne sintetinio) — grąžina validų ShareGPT. Tai įrodo, kad dvigubo
   naudojimo formatas laikosi ant realių duomenų.
5. **Fail-safe:** imituok capture klaidą → užduotis ir ataskaita nepaveiktos.
6. **Saugykla ir privatumas:** kur guli pėdsakai, ar ne viešame repo medyje, ar `git status` viešame repo nepakitęs.
7. **Kiek duomenų tikėtis:** įvertink, kiek pėdsakų susikaups per savaitę esant dabartiniam tempui, ir kiek vietos užims.
8. `bash -n` OK; BACKUP + push į `hera-core-backup`; ROADMAP.md eilutė (**patikrink grep'u, kad tikrai faile**).

Jei STOP — kodėl.
