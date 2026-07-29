UŽDUOTIS — Fazė 39: projekcijos vartų atidarymas + ar scrub NEPERSPAUDŽIA (klaidingai pozityvių auditas) + CaRE anotacija. HUMAN-GATE GAUTAS („Varom"). <13 min.

## Tikslas
Fazė 38 pastatė dviejų sluoksnių skillcapture: `raw/` (neredaguotas archyvas) + `projection/` (rašoma tik po
`hera_pii.scrub()`, vartai `HERA_SKILLCAPTURE_PROJECTION` def 0). Kaupiasi 5+ pėdsakai, bet projekcija
NEGENERUOJAMA → duomenys kol kas niekam nepadeda.

**Šios fazės tikslas — atidaryti vartus IR atsakyti į vieną konkretų klausimą, kurio testai atsakyti negali:
ar `hera_pii.scrub()` neperspaudžia (over-redaction) tiek, kad projekcija taptų nenaudinga mokymui?**
20/20 testų patvirtina, kad scrub PAGAUNA ką turi. Jie NEpatvirtina, kad jis nepagauna to, ko neturėtų.
Fazė 38 pridėjo 5 naujas kategorijas, iš kurių **PATH ir HOST yra plačios** — būtent jos gali sušveisti tą
techninį kontekstą, kuris pėdsakuose vertingiausias.

Konkretus pavyzdys, kodėl tai svarbu: `/opt/hera-venv/bin/python3` arba `/opt/cad-venv` NĖRA paslaptis —
tai esminis techninis kontekstas (mūsų pačių atmintyje tai užrašyta kaip kritinis faktas). Jei PATH taisyklė
tokius kelius redaguoja, projekcija mokymui bevertė: modelis išmoks „paleisk `[REDACTED]`".

## Ką padaryti
1. **Atidaryti projekcijos vartus** (`HERA_SKILLCAPTURE_PROJECTION=1` ten, kur gyvena kiti `HERA_*` — cron/env,
   pagal esamą konvenciją). Vartai lieka atidaryti ir po užduoties.
2. **Sugeneruoti projekciją visiems esamiems `raw/` pėdsakams** (5+). Jei modulis neturi „reprojektuoti esamus"
   kelio — nekurk naujo režimo, tiesiog paleisk per esamą CLI kelią tiek kartų, kiek reikia, arba pasakyk, kad
   neįmanoma be kodo pakeitimo (tada tik naujiems).
3. **⭐ KLAIDINGAI POZITYVIŲ AUDITAS — svarbiausia dalis.** Kiekvienai kategorijai (SECRET/IP/PATH/TGCHATID/HOST
   + senosios) suskaičiuok, kiek kartų suveikė, ir **kiekvienam PATH/HOST/IP suveikimui atsakyk: ar redaguotas
   dalykas TIKRAI jautrus, ar tai buvo nekaltas techninis kontekstas?** Pateik konkrečius pavyzdžius, KOKIO TIPO
   dalykai buvo užšveisti (pvz. „6 iš 9 PATH suveikimų = `/opt/*venv*` keliai, t.y. klaidingai pozityvūs").
4. **Redagavimo tankis (redaction density):** kiek % simbolių pakeista, per pėdsaką. Jei >20–25% — tai signalas.
5. **NEINDEKSUOK.** semsearch prijungimas = atskiras human-gate. Šioje fazėje projekcija tik sukuriama ir vertinama.
6. **NETAISYK taisyklių pats.** Jei rasi perspaudimą — **pasiūlyk konkretų susiaurinimą ir jo pagrindimą**,
   bet nekeisk `hera_pii.py` be atskiro leidimo. (Išimtis: jei rastum PRALEIDIMĄ, t.y. tikrą secret'ą
   projekcijoje — tai avarija, tada sustok, NEskelbk reikšmės, ir pranešk nedelsiant.)

## 🔴 Ataskaitos saugumas
Ataskaitoje **necituok neredaguotų fragmentų**. Klaidingai pozityvius aprašyk **TIPU, ne turiniu**
(„venv kelias", „vidinis host'o vardas", „docker konteinerio vardas") arba jau suscrub'inta forma.
Jei kuriam pavyzdžiui reikia rodyti tekstą — rodyk TIK tą, kurį pats patikrinai, kad neturi paslapties.

## Realybė (ko pats neišvestum)
- `hera_pii.py` = Rampart modulis, pakartotinai panaudotas; Fazėje 38 papildytas SECRET/IP/PATH/TGCHATID/HOST.
- Pėdsakai `/root/hera_skills/` (root-only 700, NE git repo). `raw/` neredaguojamas — NELIESK jo turinio.
- Vartas tikrinamas `_write_projection()` viduje — jo NEapeidinėk net testuodamas.
- Fail-CLOSED yra TEISINGA šiam vartui (skirtingai nuo advisory modulių) — nekeisk poliariškumo.
- Kritinis techninis kontekstas mūsų domene: `/opt/cad-venv` (ezdxf 1.4.4), `/opt/hera-venv` (semsearch/fastembed),
  `/opt/hera-processor`. Šie keliai mokymui VERTINGI, ne jautrūs.

## Antra dalis (maža) — CaRE kuravimo anotacija
Vault growth note'ui apie **CaRE (arXiv 2607.24763)** pridėk `## KURAVIMO VERDIKTAS (žmogus, 2026-07-29)`
tokiu pačiu formatu kaip qcku88/z9ww92 (Fazė 37). Turinys — **DVI dalys, abi PASILIEKAM:**
· **Metodika — naudojama DABAR:** compute-matched lyginimas + visų šalutinių parametrų fiksavimas; rezultatus
  teikti PER UŽKLAUSĄ, ne tik agregatą. Pririšta prie `semsearch v1.2 eval` ir tarybos jurorų lyginimo.
  CaRE parodė: suderinus resursus keli publikuoti reitingai APSIVERTĖ, o temperatūra paaiškino didžiąją
  metrikos variacijos dalį.
· **MDLM turinys (difuziniai kalbos modeliai) — PASILIEKA kaip žinia GPU erai:** NFE kaip sąžiningas
  skaičiavimo matas · remasking strategijos · „informed remasking vs stochastic unmasking" įtampa · 12 atvirų
  svorių MDLM lyderių lentelė (150M–8B = tilptų į vieną GPU). GPU **BUS** — tada tai bus paruošta atskaitos
  sistema, ne darbas nuo nulio.
· ⚠️ Metodologinė pastaba: **„nėra GPU dabar" NĖRA „neaktualu"** — domenas HERA'oje niekada nesiaurinamas;
  tokiais atvejais ARCHYVUOJAM IR PAŽYMIM (precedentai: FreeCAD MCP, 20 archyvuotų growth užrašų).
`state/*.json` `council.final_action` **NELIESK** — tarybos verdiktas yra istorinis append-only įrašas
(Fazės 37 precedentas); žmogaus sprendimas rašomas atskirai, ne perrašant.

## Apribojimai
€0 · BACKUP prieš `hera_skillcapture.py`/cron keitimą (čia backup'as saugus — jame nėra secret'ų) ·
viešo `cad-site-agent` git NELIESK · push į privatų `hera-core-backup` · HARD timeout, be retry ·
selftest turi likti PASS po pakeitimų · sąžiningas „ko nepadariau" sąrašas ataskaitoje.

Jei STOP — kodėl.
