# Fazė 61 — nustoti daryti Groq kvietimus, kurie NEĮSISKAITO. <11 min.

## ⚠️ VIENAS tikslas. Pamatęs kitą defektą — UŽRAŠYK, NETAISYK. Nespėji — stok ir pranešk.

## Pirma patikrink: ar Fazė 60 paliko necommit'intą darbą

`git -C /opt/hera-processor log --oneline -2` prieš pradedant. Jei viršuje **NĖRA** Fazės 60 —
ji krito nespėjusi commit'inti (taip jau buvo su Faze 56). Darbiniame medyje gali gulėti geras kodas
(`extractors/base.py.bak-1786458996` rodo, kad failas buvo keistas).
⇒ **NEIŠMESK jo. Peržiūrėk, ir jei sveikas — commit'ink KARTU su savo darbu.** Jei sugadintas —
pasakyk tai atvirai ataskaitoje ir grąžink į paskutinę gerą būseną.

## Realybė (išmatuota šįvakar, netikrink iš naujo)

Naujas Gemini raktas (`AQ.` priešdėlis — Google tyliai pakeitė formatą) veikia: `gemini_http=200`.
**Taryba atgijo:** `6 balsai / 4 šeimos ['gemini','glm','groq','nvidia']`, darbas
`20260811T162830Z-unsltd` praėjo `decision=pass conf=0.7`.

**Bet Groq muša 429 ties žetonų-per-minutę (TPM) riba.** Tiesioginis testas grąžino švarų atsakymą
(`total_tokens: 41`) tuo pačiu metu, kai realūs darbai krito ⇒ **tai NE paros riba ir NE gedimas Groq
pusėje. Tai mūsų pačių apkrova.**

🔥 **Ir esminis dalykas — didelė tos apkrovos dalis yra GRYNAS ŠVAISTYMAS.**
Fazė 33 įvedė tiekėjo ribą (cap) = 2 balsai, bet įgyvendino kaip **post-hoc apkarpymą**: taryba
**vis tiek iškviečia 5 Groq juror'ius, o įsiskaito tik 2.** Tai užfiksuota tos fazės pastabose
(„groq vis tiek daro 5 kvietimus, įsiskaito 2 … latency nesutaupo").
Log patvirtina: `taryba: Groq sėkmingų balsų 5/5 bandymų` → `tiekėjo riba=2 … 3 apkarpyta`.
⇒ **Trys iš penkių Groq kvietimų kiekvienoje taryboje neturi JOKIOS įtakos verdiktui**, bet degina
TPM biudžetą, kurio tuo pačiu metu reikia struktūrinimui ir atrankai.

## Tikslas — VIENAS

**Perkelk tiekėjo ribą iš post-hoc apkarpymo į PIRMINĘ ATRANKĄ:** taryba tekviečia tiek to paties
tiekėjo juror'ių, kiek realiai įsiskaitys.

Kodėl būtent taip, o ne kitaip:
· **Verdiktas NESIKEIČIA** — įsiskaito lygiai tie patys 2 balsai kaip dabar.
· **Šeimų įvairovė NENUKENČIA** — Groq lieka taryboje, tik nustoja siųsti balsus į šiukšlinę.
· Groq kvietimų taryboje sumažėja ~60 % ⇒ TPM spaudimas atslūgsta be jokio backoff'o derinimo.
· Užsidaro Fazės 33 skola, užrašyta prieš dvi savaites.

Jungiklis **`HERA_COUNCIL_PRESELECT_CAP`** — default **1** (nauja elgsena). Reikšmė 0 grąžina
dabartinį post-hoc apkarpymą bit-į-bitą.

⚠️ **Nepakeisk šeimų-atrankos logikos** — ji jautri ir turi žinomą defektą kitoje kopijoje
(`test_live_check_nvidia_fabricated`). Keisk TIK kiek kvietimų daroma, ne kaip parenkamos šeimos.

## Ko NEDARYTI (pastebėta, bet atidėta)

❌ **NVIDIA negyvi juror'iai** — 5 iš 7 grąžina HTTP 404 (`deepseek-coder-6.7b`, `kimi-k2.6`,
`mistral-7b-v0.3`, `nemotron-4-340b`, `gemma-2b`). Realus defektas, bet **NE ši fazė.**
❌ Backoff'o nederink. ❌ `gemini-flash-latest` iš `DEFAULT_MODELS` neišiminėk.
❌ Neliesk tilto, struktūrinimo, atrankos, dispatcher'io, ASR, digest'o.

## Apribojimai

€0 · **BACKUP prieš keitimą**, backup'ų NIEKADA netrinti · viešas `cad-site-agent` neliečiamas ·
jokių raktų reikšmių log'uose/ataskaitoje/commit'uose · ataskaita ir komentarai **lietuviškai,
angliški terminai su vertimu skliaustuose.**

## Įrodymai

1. `--selftest` PASS: su ribą=2 daromi **2, ne 5** to paties tiekėjo kvietimai ·
   `HERA_COUNCIL_PRESELECT_CAP=0` grąžina seną elgesį · **verdiktas abiem atvejais tas pats** ·
   tiekėjo gedimas → fail-safe kaip anksčiau (ne crash).
2. **Reali taryba** su tikru darbu: log privalo rodyti `Groq sėkmingų balsų 2/2` (ne `5/5`)
   ir `0 apkarpyta`. Parodyk abi eilutes pažodžiui.
3. Šeimų skaičius tame pačiame darbe **nesumažėjo** (buvo 4 — palygink).
4. `systemctl is-active hera-processor`.
5. `git -C /opt/hera-processor log --oneline -3` — Fazė 61 (+ Fazės 60 darbas, jei buvo necommit'intas)
   push'inta į privatų `hera-core-backup`.

## Ataskaita

Per HERA botą: kas pakeista · **Fazės 60 likimas atskirai** (rasta / necommit'inta / sugadinta) ·
5 įrodymai · ką pastebėjai, bet sąmoningai nelietei.
