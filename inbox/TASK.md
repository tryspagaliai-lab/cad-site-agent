# Fazė 60 — išvesties sąžiningumas: kilmė, pavadinimas, ASR abejonės, formulės verbatim. <12 min.

## ⚠️ Apimtis griežta. Pamatęs kitą defektą — UŽRAŠYK, NETAISYK. Nespėji — stok ir pranešk.

## Kodėl — keturi defektai, rasti skaitant REALIĄ išvestį (ne testuose)

Fazės 57–59 sutvarkė, kad grandinė **veikia**. Ši fazė tvarko, kad jos rezultatas būtų **teisingas**.
Visi keturi defektai rasti dviejose šiandienos ištraukose (Kestra ir HarnessOpt-Bench).

**1. 🔴 KILMĖ MELUOJA.** Kiekviena ištrauka pasirašyta „## Struktūrizuota ištrauka **(Gemini)**",
nors log rodo `structure_text: Groq struktūrino pirmas (llama-3.3-70b-versatile)`, o Gemini tą parą
buvo 429. **Tiekėjo vardas užkoduotas kietai antraštėje.**
⇒ Žinių sistemai tai ne kosmetika — griauna kilmės (provenance) ir pasitikėjimo (`trust_level`) sluoksnį.
⇒ **Taisyklė: kilmė IŠVEDAMA iš realiai įvykusio kvietimo, NIEKADA nerašoma ranka.**
Antraštėje turi būti tikras tiekėjas + modelis.

**2. `PAVADINIMAS` — ne pavadinimas, o sakinys.** Realus pavyzdys:
„Šis tekstas apie tai, kaip optimizuoti dirbtinio intelekto (AI) mašiną, ypač dėmesys skiriamas…"
⇒ Telegram tema nukirsta per vidurį žodžio: **„ypač dėm"**.
⇒ Reikia: trumpas dalykinis pavadinimas su **ilgio riba** (siūloma ≤80 simbolių), be „Šis tekstas apie…".

**3. 🔴 ASR TRIUKŠMAS ĮRAŠOMAS KAIP FAKTAI.** `FAKTAI IR DUOMENYS` skiltyje surašyti sudarkyti tikriniai
vardai kaip patvirtinti duomenys. Realiame transkripte: „Kimmy K3" (=Kimi), „GPT 5.6 **Soul**/**Tara**",
**„entropic system"** (=Anthropic), „chimera system", „deep seek version for flash", „Grok build".
Modelis to **nepažymėjo kaip abejotino — pateikė kaip duomenis.**
⇒ Tai **užterštumas, ne paviršutiniškumas: sistema pasitikinčiai rašo triukšmą į savo atmintį.**
⇒ Reikia: prompt'e aiškiai — tai **automatinė kalbos atpažinimo (ASR) transkripcija**; tikriniai vardai,
modelių pavadinimai ir skaičiai gali būti iškraipyti. **Abejotinus žymėti kaip neaiškius
(pvz. `[?]` arba „neaišku"), NE teigti kaip faktą.** Geriau praleisti nei prasimanyti.

**4. PRALEIDŽIA VERTINGIAUSIA.** HarnessOpt-Bench video esmė buvo **formulė**
`normalized gain = (H⁺ − H₀) / (1 − H₀)`. Ištraukoje jos **NĖRA** iš viso.
Be to `CITATOS` skiltis parašė „čia nėra tiesioginių citatų" — **netiesa**, jų pilna.
⇒ Reikia: formulės, specifikacijos, skaitiniai parametrai ir tikros citatos traukiamos **VERBATIM**.

## Tikslas

Sutvarkyk struktūrinimo išvestį taip, kad visi keturi punktai būtų padengti.
Kur taisyti — spręsk pats (antraštės sudarymas vs `STRUCT_INSTR` prompt'as `extractors/base.py`),
bet **kilmė privalo būti išvesta iš kodo, ne iš prompt'o** — modeliu čia pasitikėti negalima.

## ĮRODYMAS — vienas, griežtas, natūralus

**Perleisk video `32AK4b0eW04`** (HarnessOpt-Bench apžvalga, 20964 sim., dabar turi `sel 0`).
Nauja ištrauka **PRIVALO** tenkinti visus keturis:
1. kilmė sako **Groq + realų modelį** (ne „Gemini")
2. `PAVADINIMAS` ≤80 sim., dalykinis, be „Šis tekstas apie…"
3. bent vienas abejotinas ASR vardas **pažymėtas kaip neaiškus** (arba praleistas), ne teigiamas
4. **formulė `(H⁺ − H₀) / (1 − H₀)` ARBA jos žodinis atitikmuo ištraukoje YRA**

Jei bent vienas netenkinamas — **fazė NEATLIKTA**, sakyk tai atvirai, nerašyk „iš dalies pavyko".

## Ko NEDARYTI

❌ Tarybos ir research kelio NELIESK. ❌ `gemini-flash-latest` iš `DEFAULT_MODELS` neišiminėk.
❌ Dublių gaudyklės pagal `video_id` NEDARYK (kita fazė). ❌ Kitų senų darbų neperleidinėk.
❌ Neliesk tilto, ASR modulio, digest'o, backoff'o, dispatcher'io.

## Apribojimai

€0 · **BACKUP prieš keitimą**, backup'ų NIEKADA netrinti · viešas `cad-site-agent` neliečiamas ·
jokių raktų reikšmių · ataskaita ir komentarai **lietuviškai, angliški terminai su vertimu skliaustuose.**

## Papildomi įrodymai

5. `--selftest` PASS (kilmės išvedimas + pavadinimo ilgio riba tikrinami be tinklo).
6. `systemctl is-active hera-processor`.
7. `git -C /opt/hera-processor log --oneline -2` + push į privatų `hera-core-backup`.

## Ataskaita

Per HERA botą: kas pakeista · **naujos ištraukos antraštė ir `PAVADINIMAS` cituojami pažodžiui** ·
4 kriterijų atitikimas po vieną · ką pastebėjai, bet sąmoningai nelietei.
