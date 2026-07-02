# Imagery MCP — `sasplanet-imagery` (headless GeoTIFF eksportas)

SASPlanet yra Windows GUI programa be API/headless režimo, tad jos „iš vidaus"
patikimai valdyti negalima. Bet SASPlanet iš esmės tik atsisiunčia standartines
Web-Mercator (XYZ) plyteles (ESRI/Google/OSM) ir jas sujungia. Šis MCP daro tą patį
**headless**, kad agentas galėtų paimti georeferencuotą GeoTIFF be jokio GUI.

Failas: `cad-site-agent/sasplanet_mcp.py` · registracija: `.mcp.json` (repo šaknis).

## Priklausomybės
```bash
pip install --user rasterio pyproj pillow requests numpy   # mcp jau įdiegtas
```

## Įrankiai
- **`list_providers()`** — galimi šaltiniai (`esri` numatytas, `esri_clarity`,
  `google_sat`, `google_hybrid`, `osm`) ir max zoom.
- **`geocode(place, limit=5)`** — vietovės pavadinimas → koordinatės + bbox
  (OSM Nominatim). Grąžintą bbox gali paduoti tiesiai į `export_geotiff`.
- **`export_geotiff(...)`** — atsisiunčia plyteles, sujungia, apkarpo iki bbox ir
  įrašo GeoTIFF. Plotą nurodyk **arba** bbox (`min_lon/min_lat/max_lon/max_lat`),
  **arba** `place` + `buffer_m`. Parametrai: `zoom` (18≈pastatas, 19≈max),
  `provider`, `crs` ("3857" native / "4326" reprojektuota), `out_path`,
  `max_tiles` (apsauga, def. 800).

## Pavyzdys (ką agentas darys)
```
geocode("Osprey Heights, Flamborough")     -> bbox
export_geotiff(min_lon=..., min_lat=..., max_lon=..., max_lat=..., zoom=19,
               provider="esri", crs="3857")
-> data/imagery/esri_z19_<ts>.tif  (EPSG:3857, ~0.3 m/px)
```

## Aktyvavimas Claude Code'e
`.mcp.json` yra repo šaknyje — paleidus Claude Code šiame kataloge, jis pasiūlys
patvirtinti (trust) projekto MCP serverius. Patvirtinus, `sasplanet-imagery`
įrankiai tampa prieinami. (Patikra be Claude: `python3 cad-site-agent/sasplanet_mcp.py`
— lauks stdio.)

## Naudojimo teisės
Numatytasis `esri` (ESRI World Imagery) leidžia peržiūrą/analizę. Google/Bing ToS
riboja masinį plytelių ėmimą — naudok tik turėdamas teisę. Skirta objekto masto
iškarpoms, ne masiniam scrape'inimui. Išvestis (`*.tif`, `data/imagery/`) — gitignore.
