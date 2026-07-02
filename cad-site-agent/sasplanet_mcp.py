"""
SASPlanet-style Imagery — MCP Server (headless GeoTIFF exporter)

SASPlanet itself is a Windows GUI app with no API/headless mode, so it cannot be
driven programmatically in a reliable way. What it actually does under the hood is
fetch standard Web-Mercator (XYZ) map tiles from providers (ESRI / Google / OSM …)
and stitch them. This MCP server does the same thing **headless**, so an agent can
request a georeferenced GeoTIFF of any location without touching a GUI:

  tools:
    - list_providers()                       — available tile sources
    - geocode(place)                         — place name -> bbox (Nominatim)
    - export_geotiff(...)                    — download + stitch + georeference -> .tif

Output is a proper GeoTIFF (EPSG:3857 by default, optional EPSG:4326) that opens in
QGIS / AutoCAD Map / gdal etc. Deps: rasterio, pyproj, pillow, requests, numpy.

Usage (stdio transport, for Claude Code / Claude Desktop):
    python sasplanet_mcp.py

.mcp.json entry:
{
  "mcpServers": {
    "sasplanet-imagery": { "command": "python3", "args": ["/abs/path/sasplanet_mcp.py"] }
  }
}

NOTE on usage rights: default provider is ESRI World Imagery, which permits tile
access for viewing/analysis. Some providers (Google, Bing) restrict bulk tile
fetching in their ToS — use those only where you have the right to. Keep areas /
zoom modest; this is meant for site-scale extracts, not mass scraping.
"""
from __future__ import annotations

import concurrent.futures
import io
import math
import time
from datetime import datetime
from pathlib import Path

import numpy as np
import requests
from PIL import Image

import rasterio
from rasterio.transform import from_origin
from rasterio.crs import CRS
from rasterio.warp import calculate_default_transform, reproject, Resampling

from mcp.server.fastmcp import FastMCP

# ── config ─────────────────────────────────────────────────────────────────────
REPO_ROOT = Path(__file__).parent.resolve()
DEFAULT_OUT_DIR = REPO_ROOT / "data" / "imagery"
TILE = 256
R = 6378137.0                      # Web Mercator sphere radius
ORIGIN = math.pi * R               # 20037508.342789244
UA = "cad-site-agent-imagery/1.0 (+https://github.com/tryspagaliai-lab/cad-site-agent)"
MAX_TILES = 800                    # hard guard against runaway downloads

PROVIDERS = {
    "esri": {
        "url": "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
        "ext": "jpg", "max_zoom": 19,
        "label": "ESRI World Imagery (satellite) — default, viewing/analysis OK",
    },
    "esri_clarity": {
        "url": "https://clarity.maptiles.arcgis.com/arcgis/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
        "ext": "jpg", "max_zoom": 19,
        "label": "ESRI World Imagery Clarity (often higher-res)",
    },
    "google_sat": {
        "url": "https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}",
        "ext": "jpg", "max_zoom": 21,
        "label": "Google Satellite (check ToS before bulk use)",
    },
    "google_hybrid": {
        "url": "https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}",
        "ext": "jpg", "max_zoom": 21,
        "label": "Google Hybrid sat+labels (check ToS)",
    },
    "osm": {
        "url": "https://tile.openstreetmap.org/{z}/{x}/{y}.png",
        "ext": "png", "max_zoom": 19,
        "label": "OpenStreetMap street map (not satellite)",
    },
}

mcp = FastMCP("sasplanet-imagery")


# ── web mercator math ──────────────────────────────────────────────────────────
def _lonlat_to_merc(lon: float, lat: float) -> tuple[float, float]:
    lat = max(min(lat, 85.05112878), -85.05112878)
    x = math.radians(lon) * R
    y = R * math.log(math.tan(math.pi / 4 + math.radians(lat) / 2))
    return x, y


def _lonlat_to_tile_frac(lon: float, lat: float, z: int) -> tuple[float, float]:
    lat_r = math.radians(max(min(lat, 85.05112878), -85.05112878))
    n = 2 ** z
    x = (lon + 180.0) / 360.0 * n
    y = (1.0 - math.asinh(math.tan(lat_r)) / math.pi) / 2.0 * n
    return x, y


def _tile_merc_bounds(z: int) -> float:
    """Return metres-per-tile edge at zoom z."""
    return (2 * ORIGIN) / (2 ** z)


# ── tile download ──────────────────────────────────────────────────────────────
def _fetch_tile(session: requests.Session, url: str) -> Image.Image | None:
    for attempt in range(3):
        try:
            r = session.get(url, timeout=20, headers={"User-Agent": UA})
            if r.status_code == 200 and r.content:
                return Image.open(io.BytesIO(r.content)).convert("RGB")
            if r.status_code in (403, 404):
                return None
        except Exception:
            time.sleep(0.4 * (attempt + 1))
    return None


# ── tools ──────────────────────────────────────────────────────────────────────
@mcp.tool()
def list_providers() -> str:
    """List available imagery/tile providers and their max zoom."""
    lines = ["Available providers (use the key with export_geotiff):", ""]
    for key, p in PROVIDERS.items():
        lines.append(f"  {key:<14} z≤{p['max_zoom']:<3} — {p['label']}")
    lines += ["", "Default: esri. Zoom guide: 15≈city, 17≈street, 18≈building, 19≈max detail."]
    return "\n".join(lines)


@mcp.tool()
def geocode(place: str, limit: int = 5) -> str:
    """Resolve a place name / address to coordinates and a bounding box (OSM Nominatim).

    Args:
        place: Free-text location, e.g. "Osprey Heights, UK" or a postcode.
        limit: Max candidates to return (default 5).

    Returns a list of candidates with lat/lon and a bbox you can feed straight into
    export_geotiff as min_lon/min_lat/max_lon/max_lat.
    """
    try:
        r = requests.get(
            "https://nominatim.openstreetmap.org/search",
            params={"q": place, "format": "jsonv2", "limit": limit, "polygon_geojson": 0},
            headers={"User-Agent": UA}, timeout=20,
        )
        data = r.json()
    except Exception as e:
        return f"Geocode failed: {type(e).__name__}: {e}"
    if not data:
        return f"No matches for: {place!r}"
    out = [f"Candidates for {place!r}:", ""]
    for d in data:
        # nominatim bbox = [south, north, west, east]
        s, n, w, e = (float(x) for x in d["boundingbox"])
        out.append(f"- {d.get('display_name','?')}")
        out.append(f"    center: lon={float(d['lon']):.6f} lat={float(d['lat']):.6f}")
        out.append(f"    bbox:   min_lon={w:.6f} min_lat={s:.6f} max_lon={e:.6f} max_lat={n:.6f}")
    return "\n".join(out)


@mcp.tool()
def export_geotiff(
    min_lon: float | None = None,
    min_lat: float | None = None,
    max_lon: float | None = None,
    max_lat: float | None = None,
    place: str = "",
    buffer_m: float = 500.0,
    zoom: int = 18,
    provider: str = "esri",
    out_path: str = "",
    crs: str = "3857",
    max_tiles: int = MAX_TILES,
) -> str:
    """Download map tiles for an area and write a georeferenced GeoTIFF.

    Specify the area EITHER by an explicit bounding box (min_lon/min_lat/max_lon/max_lat)
    OR by `place` (geocoded via Nominatim) + `buffer_m` (half-size of a square around it).

    Args:
        min_lon, min_lat, max_lon, max_lat: Bounding box in WGS84 degrees.
        place:     Alternative to bbox — a place name to geocode + buffer.
        buffer_m:  Half-width in metres of the square around the geocoded point (default 500).
        zoom:      XYZ zoom level (higher = more detail/tiles). Default 18.
        provider:  One of list_providers() keys. Default "esri".
        out_path:  Output .tif path (default data/imagery/<provider>_z<zoom>_<ts>.tif).
        crs:       "3857" (Web Mercator, native, fast) or "4326" (WGS84, reprojected).
        max_tiles: Safety cap on tile count (default 800). Lower the zoom if exceeded.

    Returns a summary with the output path, pixel size, ground resolution and bounds.
    """
    if provider not in PROVIDERS:
        return f"Unknown provider {provider!r}. Options: {', '.join(PROVIDERS)}"
    prov = PROVIDERS[provider]
    zoom = int(zoom)
    if zoom < 1 or zoom > prov["max_zoom"]:
        return f"zoom must be 1..{prov['max_zoom']} for provider {provider}"

    # ── resolve bbox ────────────────────────────────────────────────────────────
    if place and None in (min_lon, min_lat, max_lon, max_lat):
        try:
            r = requests.get(
                "https://nominatim.openstreetmap.org/search",
                params={"q": place, "format": "jsonv2", "limit": 1},
                headers={"User-Agent": UA}, timeout=20,
            )
            d = r.json()[0]
        except Exception as e:
            return f"Geocode for {place!r} failed: {e}. Provide an explicit bbox instead."
        clon, clat = float(d["lon"]), float(d["lat"])
        cx, cy = _lonlat_to_merc(clon, clat)
        # buffer in metres -> back to lon/lat corners
        from pyproj import Transformer
        t = Transformer.from_crs(3857, 4326, always_xy=True)
        min_lon, min_lat = t.transform(cx - buffer_m, cy - buffer_m)
        max_lon, max_lat = t.transform(cx + buffer_m, cy + buffer_m)

    if None in (min_lon, min_lat, max_lon, max_lat):
        return ("Provide either a bbox (min_lon/min_lat/max_lon/max_lat) or a `place`. "
                "Use geocode() first if unsure.")
    min_lon, max_lon = sorted((float(min_lon), float(max_lon)))
    min_lat, max_lat = sorted((float(min_lat), float(max_lat)))

    # ── tile range ──────────────────────────────────────────────────────────────
    x0f, y0f = _lonlat_to_tile_frac(min_lon, max_lat, zoom)   # top-left
    x1f, y1f = _lonlat_to_tile_frac(max_lon, min_lat, zoom)   # bottom-right
    x0, x1 = int(math.floor(x0f)), int(math.floor(x1f))
    y0, y1 = int(math.floor(y0f)), int(math.floor(y1f))
    nx, ny = (x1 - x0 + 1), (y1 - y0 + 1)
    ntiles = nx * ny
    if ntiles > max_tiles:
        # suggest a zoom that fits
        suggest = zoom
        while suggest > 1:
            suggest -= 1
            sx0, sy0 = _lonlat_to_tile_frac(min_lon, max_lat, suggest)
            sx1, sy1 = _lonlat_to_tile_frac(max_lon, min_lat, suggest)
            if (int(sx1) - int(sx0) + 1) * (int(sy1) - int(sy0) + 1) <= max_tiles:
                break
        return (f"Area needs {ntiles} tiles at zoom {zoom} (cap {max_tiles}). "
                f"Try zoom {suggest} or a smaller area/buffer.")

    # ── download + stitch ───────────────────────────────────────────────────────
    mosaic = Image.new("RGB", (nx * TILE, ny * TILE))
    session = requests.Session()
    failed = 0

    def job(ix_iy):
        ix, iy = ix_iy
        n = 2 ** zoom
        url = prov["url"].format(z=zoom, x=ix % n, y=iy)
        return (ix, iy, _fetch_tile(session, url))

    coords = [(x0 + dx, y0 + dy) for dy in range(ny) for dx in range(nx)]
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:
        for ix, iy, img in ex.map(job, coords):
            if img is None:
                failed += 1
                continue
            mosaic.paste(img, ((ix - x0) * TILE, (iy - y0) * TILE))

    # ── georeference (native EPSG:3857) ─────────────────────────────────────────
    tsize = _tile_merc_bounds(zoom)          # metres per tile edge
    res = tsize / TILE                        # metres per pixel
    mosaic_left = -ORIGIN + x0 * tsize
    mosaic_top = ORIGIN - y0 * tsize

    # crop mosaic to the exact requested bbox
    bminx, bminy = _lonlat_to_merc(min_lon, min_lat)
    bmaxx, bmaxy = _lonlat_to_merc(max_lon, max_lat)
    col_min = max(0, int((bminx - mosaic_left) / res))
    col_max = min(mosaic.width, int(math.ceil((bmaxx - mosaic_left) / res)))
    row_min = max(0, int((mosaic_top - bmaxy) / res))
    row_max = min(mosaic.height, int(math.ceil((mosaic_top - bminy) / res)))
    if col_max <= col_min or row_max <= row_min:
        return "Computed empty crop — check the bbox ordering/values."
    crop = mosaic.crop((col_min, row_min, col_max, row_max))
    arr = np.asarray(crop).transpose(2, 0, 1)   # (bands, H, W)

    left3857 = mosaic_left + col_min * res
    top3857 = mosaic_top - row_min * res
    transform = from_origin(left3857, top3857, res, res)
    src_crs = CRS.from_epsg(3857)

    # ── output path ─────────────────────────────────────────────────────────────
    if out_path:
        out = Path(out_path)
        if not out.is_absolute():
            out = REPO_ROOT / out
    else:
        DEFAULT_OUT_DIR.mkdir(parents=True, exist_ok=True)
        ts = datetime.now().strftime("%Y%m%dT%H%M%S")
        out = DEFAULT_OUT_DIR / f"{provider}_z{zoom}_{ts}.tif"
    out.parent.mkdir(parents=True, exist_ok=True)

    prof = dict(driver="GTiff", height=arr.shape[1], width=arr.shape[2],
                count=3, dtype="uint8", crs=src_crs, transform=transform,
                compress="deflate", tiled=True, blockxsize=256, blockysize=256)

    if crs.replace("EPSG:", "").strip() == "4326":
        dst_crs = CRS.from_epsg(4326)
        dtrans, dw, dh = calculate_default_transform(
            src_crs, dst_crs, arr.shape[2], arr.shape[1],
            left=left3857, bottom=top3857 - arr.shape[1] * res,
            right=left3857 + arr.shape[2] * res, top=top3857)
        prof.update(crs=dst_crs, transform=dtrans, width=dw, height=dh)
        with rasterio.open(out, "w", **prof) as dst:
            for b in range(3):
                reproject(source=arr[b], destination=rasterio.band(dst, b + 1),
                          src_transform=transform, src_crs=src_crs,
                          dst_transform=dtrans, dst_crs=dst_crs,
                          resampling=Resampling.bilinear)
        out_crs = "EPSG:4326"
    else:
        with rasterio.open(out, "w", **prof) as dst:
            dst.write(arr)
        out_crs = "EPSG:3857"

    size_mb = out.stat().st_size / 1e6
    return (
        f"OK — GeoTIFF written: {out}\n"
        f"  provider={provider} zoom={zoom} crs={out_crs}\n"
        f"  pixels={arr.shape[2]}x{arr.shape[1]}  ground_res≈{res:.3f} m/px\n"
        f"  tiles={ntiles} (failed={failed})  file={size_mb:.1f} MB\n"
        f"  bbox(WGS84)= {min_lon:.6f},{min_lat:.6f},{max_lon:.6f},{max_lat:.6f}\n"
        f"  attribution: {prov['label']}"
    )


if __name__ == "__main__":
    mcp.run(transport="stdio")
