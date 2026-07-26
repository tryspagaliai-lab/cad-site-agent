UŽDUOTIS — Fazė 29: `hera_verify` integracija į runner'į — ADVISORY-FIRST, BE tikro pakartojimo. <14 min.

## Tikslas
Fazė 27 sukūrė `hera_verify.py` (rubrika + vertinimas + suspausta pakartojimo užklausa), bet jis STANDALONE.
Uždaryk Ciklą 2, BET pirmu žingsniu **TIK stebėjimo režimu**: po darbo vieneto įvertink išvestį pagal TASK.md
„Įrodymai" rubriką ir **PARODYK ataskaitoje verdiktą + kokia pakartojimo užklausa BŪTŲ siųsta** —
**tikro pakartojimo NEVYKDYK.**
Priežastis: pirma turim įsitikinti, kad leksinis vertinimas TIKSLUS. Jei įjungtume retry su netiksliu vertintoju,
runner kartotų sėkmingas užduotis arba praleistų nesėkmes. Tai ta pati „pirma išmatuok, tada įjunk" disciplina,
kurią sėkmingai pritaikė Fazė 28 (staleguard advisory).

## 🔴 Runner yra kertinis — tie patys saugikliai kaip Fazėje 22
Fazė 22 (GoalAnchor) integravosi į runner'į saugiai; sek TUO PAT precedentu:
- Kvietimas izoliuotas: `timeout N ... || true` — jei `hera_verify` krenta ar kabo, runner tęsia NORMALIAI.
- **NEKEISTI:** `flock`, HARD timeout, STATE dedup, exit code, cron tvarkaraštis. Diff turi rodyti TIK anotacijos eilutes.
- Anotacija prisegama prie ataskaitos šalia esamų `LG_NOTE` / `GA_NOTE` (loop-guard / goalanchor) — tas pats mechanizmas.
- Tylėti kai `pass`; rodyti tik kai `fail` arba `undecided`.
Jei kyla NORS MENKIAUSIA abejonė dėl runner'io stabilumo — STOP, nekeisk, praneša.

## Realybė (ko pats neišvestum)
- `hera_verify.py`: `parse_rubric(task_text)`, `evaluate(output, criteria)`, `build_retry_prompt(...)`,
  `run_verification_cycle(...)`. Def0: grynosios funkcijos veikia visada, jungiklis tik TG pranešimui.
- Runner turi ir TASK.md tekstą, ir agento išvestį (`/root/agent_result_<blob>.txt`) — abu reikalingi vertinimui.
- **Puiki testavimo medžiaga jau egzistuoja:** kelios paskutinės realiai įvykdytos užduotys (Fazės 26, 27, 28) turi
  ir TASK.md, ir ataskaitas. Naudok jas RETROSPEKTYVIAI vertintojo tikslumui patikrinti — tai vertingiau nei sintetiniai testai.
- Šitas pats failas turi „Įrodymai" skiltį — irgi tinkamas parse testui.

## Apribojimai
€0, be tinklo, be LLM. Fail-safe. **JOKIO tikro pakartojimo šiame žingsnyje** — tik vertinimas + parodyta užklausa.
Ataskaita TIK į HERA botą. Viešo `cad-site-agent` NELIESK. BACKUP runner'io prieš keitimą. Secret'us NEliesk.
Cron NELIESK. `hera_staleguard` integracijos (Fazė 28) NELIESK.

## Įrodymai (ko tikiuosi ataskaitoje)
1. **Vertintojo TIKSLUMAS retrospektyviai:** paleisk vertinimą ant Fazių 26/27/28 TASK.md + jų realių ataskaitų.
   Kiek įvertino `pass`/`fail`/`undecided` ir ar tai ATITINKA tikrovę (visos trys realiai pavyko)?
   **Jei vertintojas duoda daug klaidingų `fail` — tai KRITINĖ išvada, pasakyk ją garsiai.** Būtent dėl to nedarome retry.
2. **Runner'io vientisumas:** `bash -n` OK; diff rodo TIK anotacijos eilutes; `flock`/STATE/timeout/exit code nepaliesti.
3. **Elgesys nepakito:** kai `pass` — ataskaita atrodo kaip anksčiau (jokio triukšmo).
4. **Fail-safe:** imituok `hera_verify` klaidą → runner tęsia normaliai, ataskaita išsiunčiama.
5. **Parodyta pakartojimo užklausa:** vienam `fail` atvejui parodyk, kokia užklausa BŪTŲ siųsta ir jos dydį.
6. BACKUP + push į privatų `hera-core-backup`; ROADMAP.md eilutė.
7. **Rekomendacija:** ar vertintojas pakankamai tikslus, kad kitame žingsnyje įjungtume tikrą retry? Sąžiningai.

Jei STOP — kodėl.
