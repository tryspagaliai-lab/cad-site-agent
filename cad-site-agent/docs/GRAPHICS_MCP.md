# Graphics MCP — `graphics-ops` + `blender-render`

Open source, automatable atitikmuo Affinity paketui (kuris uždaras, GUI-only, tad
MCP'inti negalima). Visi backend'ai — extracted AppImage'ai `~/.local/appimages/`,
paleidikliai `~/.local/bin/`. Aktyvuojami per `.mcp.json` (repo šaknis).

## `graphics-ops` (`cad-site-agent/graphics_ops_mcp.py`)
Backend'ai: **Inkscape 1.4** (vektoriai), **GIMP 3** (rastro batch/Script-Fu), **Pillow**.
- `tools_info()` — versijos
- `inkscape_export(input, output, dpi, width, height, area)` — SVG↔PDF↔PNG↔EPS↔PS
- `svg_dimensions(svg)` — matmenys
- `image_convert(input, output, quality)` — PNG/JPEG/WEBP/TIFF/BMP (Pillow)
- `image_resize(input, output, width, height, keep_aspect)` — resize (Pillow)
- `images_to_pdf(inputs, output)` — keli vaizdai → 1 PDF
- `gimp_script(script_fu, timeout)` — bet koks GIMP Script-Fu batch (power tool)

## `blender-render` (`cad-site-agent/blender_render_mcp.py`)
Backend: **Blender 5.1** (native, tikras headless `blender -b`).
- `blender_info()`
- `render_blend(blend, output, frame, engine, samples)` — .blend kadro render
- `quick_render(model, output, resolution, samples, engine)` — import 3D (.obj/.stl/.fbx/.glb/.gltf/.ply/.x3d/.dae) + auto kamera/šviesa + render
- `run_python(script, blend)` — bet koks bpy Python headless (power tool)

Pastaba: engine 5.1 = `BLENDER_EEVEE` / `CYCLES` / `BLENDER_WORKBENCH` (kodas parenka
galiojantį automatiškai). DXF Blender natively neimportuoja (reikia addon).

## Testuota (2026-07-02, end-to-end)
- SVG→PDF ✓, SVG→PNG@300dpi ✓, PNG→JPG ✓
- OBJ eksportas + quick_render → 256×256 PNG ✓

## Krita
Įdiegtas (`~/.local/bin/krita`, Krita 6.0.2) GUI/piešimui; MCP wrapper'io kol kas nėra
(PyKrita headless silpnesnis) — pridėsim jei prireiks piešimo automatikos.

## Scribus — ATIDĖTA
Numatytas AppImage (SourceForge 1.6.6) — SF blokuoja tiesioginį atsisiuntimą (anti-bot,
grąžina HTML). Paimti naršykle iš sourceforge.net/projects/scribus/files/ ir įdėti į
`~/.local/appimages/scribus/` (extract-and-run) — tada `scribus -py` maketų MCP galimas.
