UŽDUOTIS — Fazė 24 (ETAPAS 1): hera_dxf2png.py — DXF → švarus 2D planas PNG/SVG (ezdxf headless, determ., BE AI). <14 min.
NEleisk pytest (tik savo selftest). Fail-safe. €0. Deterministiška (BE LLM, BE tinklo). Ataskaita TIK į HERA botą. Viešo cad-site-agent NELIESK git prasme (modulis gyvena /root/, backup į privatų hera-core-backup). Secret'us NEliesk.

KONTEKSTAS: taryba pritarė (7/9, median 8.0) DXF→PNG→AI-renderis krypčiai, BET komercinė vertė kvalifikuota (tik koncepcinei stadijai).
Todėl SKALDOM: šis ETAPAS 1 = grynai deterministinis DXF→švarus PNG, BE jokio AI, BE API. Vertingas SAVAIME
(peržiūros/miniatiūros, dokumentacija, ir svarbiausia — PARSINIMO QA: vizualiai patikrinti ar ezdxf teisingai perskaitė brėžinį).
ETAPAS 2 (PNG→Gemini→3D renderis) = ATSKIRA fazė vėliau, NEDARYK jos čia.

⚠️ SVARBU dėl priklausomybių — NIEKO SUNKAUS NEDIEK aklai:
- ezdxf JAU yra (cad-site-agent juo naudojasi). Patikrink versiją.
- Renderinimui ezdxf turi `ezdxf.addons.drawing`. PIRMENYBĖ: NATYVUS SVG backend (be matplotlib) — `ezdxf.addons.drawing.svg`
  (naujesnės versijos) → SVG be jokių papildomų priklausomybių. Jei SVG→PNG konversijai reikia bibliotekos (cairosvg/Pillow) ir jos NĖRA — 
  GRĄŽINK SVG kaip pagrindinį formatą (jis puikiai tinka peržiūrai IR Gemini priima vaizdus; PNG tada = optional).
- matplotlib backend naudok TIK jei matplotlib JAU įdiegtas (patikrink). Jei nėra — NEDIEK (jis ~50-60MB; tai human-gate).
- Ataskaitoj aiškiai pasakyk: kokį backend'ą naudojai, ko trūko, ir ar kas nors būtų verta įdiegti (bet NEDIEK).

1) FEASIBILITY (greitai, prieš rašant):
   a) `/opt/hera-venv/bin/python3 -c "import ezdxf; print(ezdxf.__version__)"` (ir sistemos python3 jei venv neturi).
      PASTABA: cad-site-agent gali naudoti KITĄ venv — patikrink kur ezdxf realiai gyvena (pvz. /opt/cad-site-agent/.venv). Naudok TĄ interpretatorių.
   b) ar importuojasi `ezdxf.addons.drawing` + kokie backend'ai (svg natyvus? matplotlib? Pillow?).
   c) ar yra realių DXF failų testui (pvz. /opt/cad-site-agent/data/**.dxf) — jei yra, PAIMK VIENĄ MAŽĄ kaip realų testą (tik SKAITYMAS, nieko nekeisk).

2) Sukurk /root/hera_dxf2png.py (kaip kiti hera_* moduliai):
   - Jungiklis: HERA_DXF2PNG def 0 = DRY-RUN (viską apskaičiuoja, grąžina planuojamą rezultatą, BET failo NERAŠO). =1 → rašo.
   - API: `render_clean(dxf_path, out_path=None, drop_text=True, layer_exclude=None, fmt="auto") -> dict`
     grąžina {ok, out_path, fmt, entities_total, entities_kept, entities_dropped, dropped_by_type:{...}, layers_excluded:[...], msg}.
   - ŠVARINIMO LOGIKA (determ., tai atitikmuo AutoCAD `select similar`+`hide`):
     * jei drop_text=True → praleisk entity tipus: TEXT, MTEXT, DIMENSION, LEADER, MULTILEADER, ATTDEF, ATTRIB, TOLERANCE.
     * layer_exclude: list pattern'ų (case-insensitive substring), def None → naudok saugų numatytą sąrašą:
       ["text","dim","anno","annot","hatch-text","notes","tekst","matmen"] (EN+LT). Sluoksnis atitinka bet kurį → jo entity praleidžiami.
     * VISKAS kita (sienos, linijos, lankai, polilinijos, blokai/INSERT) — IŠLAIKOMA.
     * Skaičiuok kiek numesta pagal tipą (skaidrumas — vartotojas turi matyti KĄ pašalino).
   - RENDERINIMAS: naudok ezdxf.addons.drawing su pasirinktu backend'u (svg natyvus PIRMENYBĖ). fmt="auto" → rink geriausią GALIMĄ
     (png jei gali, kitaip svg). Baltas/šviesus fonas, be tinklelio, be ašių — švarus planas kaip AutoCAD ekrano nuotraukoj.
   - FAIL-SAFE: bet kokia klaida (blogas DXF, trūkstamas backend, neįrašomas kelias) → grąžink {ok:False, msg:<aiški priežastis>},
     log /root/hera_dxf2png.log. NIEKAD necrashink. NIEKAD nemodifikuok įvesties DXF (tik skaitymas).
   - ATMINTIES SAUGIKLIS (taryba įspėjo dėl 4GB): jei entity kiekis > 200000 → grąžink {ok:False, msg:"per didelis brėžinys (N entities) — praleista dėl RAM"}
     NEBANDYK renderinti. (Determ. riba, apsaugo VPS.)
   - €0, be tinklo, be LLM, be AI.

3) SELFTEST (`--selftest`, be pytest, be tinklo), spausdink PASS/FAIL:
   (a) sintetinis DXF (sukurk PATS su ezdxf: stačiakampis „sienos" + kelios linijos + 1 TEXT + 1 DIMENSION, sluoksniai „WALLS" ir „TEXT")
       → render_clean su HERA_DXF2PNG=1: ok=True, failas sukurtas (dydis>0), entities_dropped>=2, dropped_by_type turi TEXT ir/ar DIMENSION,
       geometrija (sienos) IŠLIKO (entities_kept>0).
   (b) drop_text=False → TEXT nebenumetamas (entities_kept didesnis nei (a)).
   (c) def 0 dry-run: HERA_DXF2PNG=0 → grąžina skaičiavimus BET failas NESUKURTAS.
   (d) fail-safe: neegzistuojantis DXF kelias → ok=False, aiški msg, NE crash.
   (e) sluoksnių filtras: entity sluoksnyje „A-ANNO-TEXT" numetamas net jei jo tipas LINE (patikrina layer_exclude veikimą).
   (f) JEI radai realų DXF (1c) — paleisk ant jo, pažymėk ar pavyko + entity skaičius + gautas failas. Jei nerado — pažymėk „praleista".
   Spausdink PASS/FAIL kiekvienam.

4) BACKUP: cp /root/hera_dxf2png.py į /opt/hera-processor/ (ar /root/hera-core-backup/) + commit/push į PRIVATŲ hera-core-backup (TIK šis failas).
   Vault ROADMAP.md 1 eilutė: „Fazė 24 hera_dxf2png (ETAPAS 1) — ĮDIEGTA <data>, HERA_DXF2PNG def 0, determ. DXF→švarus planas (ezdxf headless,
   text/dim filtras, RAM saugiklis), BE AI; vertingas savaime (peržiūra/QA); ETAPAS 2 (→Gemini 3D) = atskira fazė."

ATASKAITA (HERA botas, trumpai): kokį ezdxf/interpretatorių radai; koks RENDER BACKEND panaudotas (svg natyvus / matplotlib / kt.) ir ko trūko;
selftest a/b/c/d/e/f PASS/FAIL; ar testavai ant realaus DXF (jei taip — rezultatas); ką VERTĖTŲ įdiegti ateity (bet NEDIEGTA); backup+push; ROADMAP.
Jei STOP — kodėl + ką radai feasibility etape.
