# SPEC — cad-3d P0: PDF brėžinys → vektorinis sluoksnis → SQLite + Wiki

> Statusas: **PROPOSED — laukia human-gate patvirtinimo. Jokio kodo, kol nepatvirtinta.**
> Metodo šaltinis: kuruotas žinių mazgas `kq6reu` (PDF → vektorius → SQLite + LLM-wiki,
> Karpathy-tipo „LLM skaitomas žinių sluoksnis"). Čia — jo adaptacija cad-site-agent'ui.
> Data: 2026-07-18

## 1. Tikslas

Praplėsti cad-site-agent įvestį nuo „tik DXF" iki „PDF brėžinys", o išvestį — nuo
JSON/MD ataskaitų iki užklausiamo SQLite sluoksnio su wiki mazgais. Tai pirmas
žingsnis cad-3d kryptimi (2D semantika → struktūrizuotos žinios → vėliau 3D), be GPU
ir be mokamų paslaugų.

```
PDF (vektorinis brėžinys)
   │  A. pdf_ingest (pdfplumber, MIT) — primityvai: lines/curves/rects/text + bbox
   ▼
Pseudo-DXF (ezdxf, jau dependency) — pseudo-sluoksniai iš stroke spalvos/storio
   │  B. ESAMAS pipeline NEPAKEISTAS: analyzer → classify → hatch → routing
   ▼
reports/analysis/<stem>.*.json
   │  C. sqlite_writer — deterministinis faktų įrašymas
   ▼
data/wiki/cad3d.sqlite  ──►  D. wiki_writer — MD mazgas per brėžinį (šablonas, be LLM)
                                  └─ (v1, atskiras vartas) LLM anotacija, def OFF
```

**Kertinis architektūrinis sprendimas:** PDF→DXF adapteris, o NE lygiagretus PDF
pipeline'as. Visas deterministinis branduolys (analyzer, classifier, hatch, routing,
taxonomy) perpanaudojamas be pakeitimų; PDF tampa tik dar vienu įėjimo formatu.

## 2. Apimtis (P0)

| # | Komponentas | Kas daroma |
|---|-------------|------------|
| A | `ingest/pdf_vector.py` | pdfplumber ištraukia vektorinius primityvus (lines, curves→flatten į polylines, rects, text su bbox). Kreivės flatten'inamos su tolerancija iš `config/tolerances.yaml` (naujas raktas `pdf.flatten_tolerance`). |
| B | `ingest/pdf_to_dxf.py` | Primityvai → laikinas DXF per ezdxf. Pseudo-sluoksniai deterministiškai iš (stroke spalva, linijos storis): `PDF_C<rgbhex>_W<width_class>`; tekstas → `PDF_TEXT`. Naujas `layer_aliases.yaml` skyrius leidžia rankiniu būdu map'inti pseudo-sluoksnius į semantines klases (human-in-the-loop, ne auto). |
| C | `wiki/sqlite_writer.py` | Esamų ataskaitų (`analysis.json`, `hatch_candidates.json`, `routing.json`, `process report`) faktai → SQLite. Append/replace per `drawing_id`; deterministinis (be LLM). |
| D | `wiki/wiki_writer.py` | Iš SQLite faktų sugeneruojamas MD wiki mazgas per brėžinį (`data/wiki/<stem>.md`): tipas, sluoksniai, klasės, regionai, review sąrašas, kryžminės nuorodos į kitus brėžinius pagal bendrą semantinę klasę. Grynas šablonas — be LLM. |
| — | CLI | Naujos komandos: `cad-agent pdf-ingest <pdf>` ir `cad-agent wiki-build <reports...>`. Esamos komandos nesikeičia. |

### SQLite schema (v0)

```sql
drawings(id, stem, source_path, source_format, drawing_type, confidence,
         units, scale_status, ingested_at)
layers(drawing_id, name, entity_count, semantic_class, feature_type, export_role)
regions(drawing_id, region_id, source_layer, class_guess, hatch_class,
        confidence, status, area, perimeter, bbox)
texts(drawing_id, layer, content, bbox)
routing(drawing_id, feature_type, semantic_class, dest_layer, count)
wiki_nodes(drawing_id, path, generated_at)
wiki_links(from_drawing_id, to_drawing_id, shared_class)
```

## 3. Ne-apimtis (P0 sąmoningai NEdaro)

- **Jokio 3D** — GIFT-tipo 2D→CAD-kodas→3D reikalauja GPU; lieka `future-gpu`.
- **Jokio OCR / raster PDF** — jei puslapyje nėra vektorinių primityvų, adapteris
  grąžina tuščią rezultatą su aiškia priežastimi ataskaitoje (fail-safe, ne crash).
- **Jokio LLM P0 kelyje** — wiki mazgai deterministiniai. LLM anotacija yra v1
  (atskiras flag'as, HARD 45–60s timeout, NO retry, klaida → mazgas lieka be
  anotacijos; €0 tiekėjai).
- **Jokio mastelio spėjimo** — PDF koordinatės saugomos pt vienetais,
  `scale_status='unknown'`. Mastelio išvedimas iš titleblock'o — v1+.
- **Jokių pakeitimų esamiems moduliams** — tik nauji failai + du nauji config raktai.

## 4. Principai (paveldimi, nekintantys)

- **€0**: pdfplumber (MIT), ezdxf ir sqlite3 — jau turimi/stdlib. Jokių naujų mokamų
  ar GPU priklausomybių.
- **Deterministinis branduolys**: tas pats PDF → bit-identiškas SQLite turinys
  (išskyrus timestamp stulpelius) ir identiškas wiki MD.
- **Fail-safe**: bloga/rasterinė/tuščia PDF → no-op su ataskaita, niekada ne crash;
  SQLite rašymas transakcinis.
- **Human-gate**: pseudo-sluoksnių → semantinių klasių mapping'as tik rankinis per
  `layer_aliases.yaml`; jokio auto-merge; šis spec'as tvirtinamas prieš kodą.
- **Regresija draudžiama**: visi esami testai (baseline 208 passed) lieka žali.

## 5. Etapai ir priėmimo kriterijai

| Etapas | Turinys | Priėmimo kriterijus |
|--------|---------|---------------------|
| M0 | Šis spec'as | Human-gate patvirtinimas |
| M1 | A+B: pdf_ingest + pdf_to_dxf | Sintetinis vektorinis PDF fixture → DXF, kurį esamas `run_process` suvirškina be klaidų; unit testai primityvų ekstrakcijai ir pseudo-sluoksnių determinizmui |
| M2 | C: sqlite_writer | Esamų JSON ataskaitų → SQLite; determinizmo testas (dvigubas paleidimas → identiškas turinys) |
| M3 | D: wiki_writer + CLI | Wiki mazgas iš SQLite; kryžminės nuorodos tarp ≥2 fixture brėžinių; pilnas testų rinkinys žalias |
| v1 (atskiras spec'as) | LLM anotacija, mastelio išvedimas, raster/OCR kelias | — |

## 6. Rizikos

| Rizika | Mažinimas |
|--------|-----------|
| PDF be tikrų vektorių (rasteris) | Fail-safe skip su priežastimi; v1 OCR kelias |
| Kreivių flatten iškraipo plotus | Tolerancija konfigūruojama; testas lygina plotą prieš/po |
| Pseudo-sluoksniai per grubūs semantikai | Tikslas P0 — struktūra, ne klasifikacijos tikslumas; mapping'as human-in-the-loop |
| pdfplumber koordinačių sistema (y žemyn) | Adapteryje vienkartinė y-inversija su testu |
