UŽDUOTIS — Fazė 47: ar `hera_pii` SECRET šablonas dengia TIKRUS mūsų kredencialų formatus? Auditas + pataisa. HUMAN-GATE GAUTAS („Varom #1"). <14 min.

## Kodėl (konkretus radinys, ne teorija)
Fazė 46: apsauginis šablonas `gh[pousr]_` **nepataikė** į `github_pat_...` (GitHub fine-grained PAT) — todėl
raktas atsispausdino į transkriptą. **Įtarimas: ta pati spraga yra `hera_pii.py` SECRET kategorijoje**, pridėtoje
Fazėje 38. Jei taip, **GitHub token'as pėdsake pereitų į `projection/` NESUREDAGUOTAS** — spraga saugumo
kontrolėje, kurią patys ką tik pastatėm ir kuri praėjo 30/30 testų.
Klasė: tai **PRALEIDIMAS** (miss), priešingas Fazės 39 PHONE klaidingam pozityvui. Ta pati šeima — regex,
kurio niekas nepatikrino prieš **tikrą formatą**.

## 🔴 SINTETINIAI DUOMENYS — griežtai
Visiems testams naudok **išgalvotas, akivaizdžiai netikras** reikšmes (pvz. `github_pat_EXAMPLE...`).
**NIEKADA nenaudok ir nespausdink tikrų kredencialų** — nei galiojančių, nei negaliojančių, nei iš `hera.env`,
nei iš `.credentials.json`, nei iš logų. Testų failuose taip pat neturi likti nieko, kas atrodytų kaip tikras raktas.

## Dalis A — AUDITAS (pirma, prieš bet kokį keitimą)

1. **Kokius formatus SECRET dengia dabar?** Perskaityk esamą šabloną ir surašyk faktą, ne įspūdį.
2. **Patikrink prieš MŪSŲ realiai naudojamų kredencialų formatus** (sintetiniais pavyzdžiais). Bent:
   · GitHub **fine-grained** `github_pat_...` ⚠️ (žinomas įtariamas praleidimas)
   · GitHub classic `ghp_` ir kiti `gho_`/`ghu_`/`ghs_`/`ghr_`
   · **Anthropic** `sk-ant-...` (turėjom tokį) ir **`sk-ant-oat01-...`** (OAuth/environment tipo)
   · **Telegram** boto token'as (formatas `<skaitmenys>:<~35 simbolių>`) — mūsų vienintelis grįžtamojo ryšio kanalas
   · **Gemini/Google** `AIza...` · **Groq** `gsk_...` · GLM/zhipu raktas
   · Bendri: `-----BEGIN ... PRIVATE KEY-----`
   Pateik **lentelę: formatas → pagaunamas TAIP/NE.**

3. **⭐ REALAUS POVEIKIO PATIKRA (svarbiausia dalis).** Fazės 43–46 vyko kaip tik apie GitHub raktą, tad
   pėdsakuose jis greičiausiai YRA. Patikrink:
   · **`/root/hera_skills/projection/`** (`rag_corpus.jsonl`, `sft_corpus.jsonl`) — ar ten pateko
     kredencialas NESUREDAGUOTAS? **Tai kritinis klausimas.** Ieškok pagal fingerprint palyginimą
     (senas = `90fcb4b8`, naujas = `92203a0c`) — **reikšmių nespausdink.**
   · `raw/` — ten neredaguota PAGAL DIZAINĄ, tai NE problema; tik pasakyk, ar yra (kad žinotume mastą).
   **Jei projekcijoje kredencialas rastas — tai avarija: pranešk NEDELSIANT ir NEtęsk į B dalį,
   kol negausi atskiro leidimo.** Nurodyk failą ir eilučių skaičių, be reikšmių.

## Dalis B — PATAISA (tik jei A rado praleidimų IR projekcija švari)

Susiaurink/išplėsk SECRET šabloną taip, kad pagautų aukščiau esančius formatus.

**Privalomi testai `test_pii.py` (abiem kryptimis — tai ne pasirinkimas):**
- Kiekvienam naujai dengiamam formatui: **pagaunamas** (sintetinis pavyzdys).
- **Regresijos testai: visi seniau pagaunami formatai VIS DAR pagaunami.**
- **Klaidingų pozityvų testai:** įprastas techninis tekstas NEredaguojamas. Būtinai patikrink bent
  `/opt/hera-venv`, `/opt/cad-venv`, git SHA (`6828794`), UUID, `github.com` URL be token'o.
  *(Fazės 39 pamoka: šablonas gali pagauti per daug, ir tai sunaikina mokymo vertę.)*
- `test_pii.py` turi likti **visas PASS** (buvo 30/30).

**Po pataisos — išmatuok poveikį:** paleisk scrub'ą ant esamų pėdsakų ir pranešk **naują redagavimo tankį**
(prieš buvo 0,0515%). Jei jis staiga šoktelėjo — tai perspaudimo požymis, pranešk.

## Apribojimai
€0 · **BACKUP `hera_pii.py` prieš keitimą** · push į privatų `hera-core-backup` · viešo `cad-site-agent` git NELIESK ·
`hera.env` NELIESK · HARD timeout, be retry · jokių tikrų kredencialų reikšmių niekur.
**Jei saugesnį kelią blokuoja hook'as — SUSTOK ir pranešk, o ne apeik** (Fazės 44 elgesys teisingas, Fazės 46 `git remote -v` — ne).

## Ataskaitoje
A: formatų lentelė TAIP/NE · projekcijos patikros rezultatas (kritinis) · B: kas pakeista, `test_pii` rezultatas,
naujas redagavimo tankis · sąžiningas „ko nepavyko".

**ATASKAITOS TAISYKLĖ:** „neįmanoma / nepavyko" galioja tik su sąrašu, KĄ BANDEI.

Jei STOP — kodėl.
