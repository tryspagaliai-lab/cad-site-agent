UŽDUOTIS — Fazė 37: Anthropic rakto liekanos VALYMAS + 2 kuravimo verdiktų pritaikymas. HUMAN-GATE GAUTAS („Varom"). <13 min.

Dvi nepriklausomos dalys. Jei laikas baigiasi — A dalis svarbesnė; B gali likti kitam kartui, bet pasakyk tai ataskaitoje.

## A) Anthropic rakto liekanų valymas (Fazės 36 plano vykdymas)

Fazė 36 nustatė: sistemoje vienas fizinis Anthropic API raktas (fingerprint sha256[:8]=2f8208e5), jo NIEKAS
nenaudoja (patikrinti visi 7 workflow nodes + workflow_history), gyvena tik 2 vietose:
n8n kredencialas `zzAnthropicCr001` (šifruota DB) ir **plaintext `/root/.bash_history`** (~eil. 14 ir 23).
Vartotojas patvirtino: kredencialą TRINAM (ne rotuojam — naujo nereikia), bash_history liekanas VALOM.
Rakto atšaukimą (revoke) Anthropic konsolėje daro pats vartotojas — tai NE tavo darbas.

Veiksmai:
1. **n8n kredencialo `zzAnthropicCr001` trynimas.** Prieš trinant užsirašyk metaduomenis ataskaitai
   (id, vardas, tipas, createdAt/updatedAt — BE reikšmės). Trink per n8n CLI arba API konteineryje.
   n8n perkrauti NEREIKIA (Fazė 36 patvirtino — niekas neskaito paleidimo metu).
2. **`/root/.bash_history` valymas.** Eilutes rask NE pagal numerį (istorija galėjo pasislinkti), o pagal turinį:
   eilutės, kuriose yra rakto reikšmė (atpažinsi pagal sha256[:8]=2f8208e5 substringo patikrą; raktas prasideda
   `sk-ant-`). Pašalink TIK tas eilutes, likusią istoriją palik nepaliestą.
3. **Patikra po valymo:** perskenuok `/root/.bash_history` ir gretimas vietas (`/root/.bash_history*`,
   `/root/.*history`) — jokioje neturi likti eilutės su fp=2f8208e5. Patikrink ir ar n8n kredencialų sąraše
   `zzAnthropicCr001` nebėra.

⚠️ **BACKUP IŠIMTIS (sąmoninga, užfiksuota):** įprastai prieš keitimą darom backup, bet ČIA backup'as būtų
nauja plaintext rakto kopija — tai paneigtų valymo tikslą. Todėl rakto turinčių eilučių NEkopijuojam niekur.
Vietoj backup'o — ataskaitoje užfiksuok, KIEK eilučių pašalinta ir jų komandų tipą (pvz. „curl į n8n API",
„curl į api.anthropic.com") be pačio rakto. n8n kredencialo trynimas atstatomas tik sukuriant naują — tai OK,
nes vartotojas raktą vis tiek atšaukia konsolėje.

🔴 Rakto reikšmės (ar jos dalies) NIEKUR nespausdink — nei ataskaitoje, nei tarpiniuose failuose, nei git'e.

## B) Dviejų staged ingest'ų kuravimo verdiktai (vartotojo patvirtinti — pritaikyk anotacijas)

Abu note'ai vault'e (kur growth note'ai gyvena; rasi pagal vardą):
- `2026-07-29-20260729T050130Z-qcku88.md` (Import AI 466)
- `2026-07-29-20260729T190400Z-z9ww92.md` (Beyond Memory, arXiv 2607.24759)

Kiekvienam pridėk verdikto bloką viršuje (po front-matter, jei yra) su `## KURAVIMO VERDIKTAS (žmogus, 2026-07-29)`:

**Import AI 466 — IMAM 3 blokus, 1 praleidžiam:**
· Sunday ACT-2 / bitter lesson: „stiprus bazinis modelis + maži kokybiški vidiniai duomenys; perkeliamumas auga
  su baziniu" = TIESIOGINIS mūsų skillcapture→LoRA-vėliau strategijos patvirtinimas; GPU laukimas = privalumas.
  ⚠️ 99.1% — startuolio savideklaracija (self-reported), imam idėją, ne skaičių.
· OpenAI incidentai (sandbox pabėgimai, žetono maskavimas prieš skenerį): ĮSPĖJIMAS eilės klausimui
  „hera_verify retry įjungimas" — grader balas valdantis pakartojimą = reward-hacking paviršius. Mūsų
  advisory-first / def 0 / human-gate = būtent tos klasės mitigacijos. Ilgesnė autonomija = sunkesnė priežiūra
  → palaiko 15-min limitą ir užduočių skaidymą.
· MirrorCode: „black-box self-orientation" — žinia ateičiai, praktinio veiksmo VPS'e nėra; faktai cituojami
  kaip šaltinio teiginiai.
· Tech Tales (fikcija) — PRALEISTA, nestiprina.

**Beyond Memory — IMAM kaip stipriausią architektūros patvirtinimą + 1 naują idėją:**
· llm-wiki pattern (LLM prižiūrima susieta wiki tarp šaltinių ir agento, append-only, nesėkmių kelio
  išsaugojimas, agent honesty) = HERA architektūra beveik 1:1 (hera-vault + wikilink + ARCHYVUOJAM-NETRINAM +
  sąžiningas „ko nepatikrinau" sąrašas). Konvergencija užfiksuota profilyje.
· NAUJA idėja: **retroaktyvus teiginių auditas** (jų atvejis: „20 iš 20" → auditas su įrodymais → 14/12 → po
  pataisos 18/18, nesėkmės kelias išsaugotas) = mūsų pamokos „tikrinti, ne tikėti" pavertimas reguliaria
  praktika. KANDIDATAS į human-gate eilę: advisory ciklas, tikrinantis vault teiginius prieš įrodymus.
· Niuansas: mes append-only laikom GIT sluoksnyje, darbinę kopiją kuruojam — gaunam abu.
· ⚠️ Įrodymai ploni: 3 case studies + 1 design report (multi-agent dalis NEĮDIEGTA, tik aprašyta), be bazinių
  palyginimų — imam koncepcijas, ne skaičius.
· ⚠️ Parserio data „May 29" KLAIDINGA (ID 2607.* = liepa) — arXiv datos defekto atvejis 3/3.

Jei note'uose yra staging žymė (pvz. `stage_for_review`) — pakeisk į patvirtintą būseną pagal esamą konvenciją.
Po redagavimo vault sync (cron kas 30 min) juos paims pats — nieko papildomo nereikia, tik NElaužyk vault git būsenos.

## Apribojimai
€0 · viešo `cad-site-agent` git NELIESK · jokių secret reikšmių · HARD timeout, be retry ·
ataskaita į HERA botą su: (A) pašalintų eilučių skaičius + patikros rezultatas + kredencialo metaduomenys,
(B) abiejų note'ų anotacijos statusas, ir sąžiningas „ko nepadariau" sąrašas.

Jei STOP — kodėl.
