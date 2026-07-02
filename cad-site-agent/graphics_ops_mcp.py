"""
Graphics Ops — MCP Server (headless Inkscape + GIMP + PIL)

Drives the open-source graphics stack programmatically so an agent can do vector
and raster work without a GUI — the automatable, open-source answer to Affinity
Designer/Photo (which is closed and GUI-only, so it can't be MCP-driven).

Backends (installed as extracted AppImages under ~/.local/appimages, launchers in
~/.local/bin): Inkscape 1.4 (vector), GIMP 3 (raster batch/Script-Fu), plus Pillow
for fast raster ops.

Tools:
    - tools_info()                          — backend versions / availability
    - inkscape_export(input, output, ...)   — SVG/PDF/EPS/PS/PNG conversion via Inkscape
    - svg_dimensions(svg)                    — width/height/viewBox of an SVG
    - image_convert(input, output, ...)      — raster format convert (Pillow)
    - image_resize(input, output, ...)       — resize/scale a raster (Pillow)
    - images_to_pdf(inputs, output)          — combine images into one PDF (Pillow)
    - gimp_script(script_fu, ...)            — run an arbitrary GIMP Script-Fu batch

Usage (stdio): python3 graphics_ops_mcp.py
"""
from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path

from PIL import Image
from mcp.server.fastmcp import FastMCP

REPO_ROOT = Path(__file__).parent.resolve()
BIN = Path.home() / ".local" / "bin"

mcp = FastMCP("graphics-ops")


# ── helpers ──────────────────────────────────────────────────────────────────
def _tool(name: str) -> str | None:
    p = BIN / name
    if p.exists():
        return str(p)
    return shutil.which(name)


def _abs(path: str) -> Path:
    p = Path(path).expanduser()
    return p if p.is_absolute() else (REPO_ROOT / p)


def _run(cmd: list[str], timeout: int = 180) -> tuple[int, str]:
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        out = (r.stdout or "") + (("\n[stderr] " + r.stderr) if r.stderr.strip() else "")
        return r.returncode, out.strip()
    except subprocess.TimeoutExpired:
        return 124, f"timed out after {timeout}s"
    except Exception as e:
        return 1, f"{type(e).__name__}: {e}"


# ── tools ────────────────────────────────────────────────────────────────────
@mcp.tool()
def tools_info() -> str:
    """Report which graphics backends are available and their versions."""
    lines = []
    for name in ("inkscape", "gimp", "krita"):
        exe = _tool(name)
        if not exe:
            lines.append(f"{name}: NOT FOUND")
            continue
        flag = "--version"
        rc, out = _run([exe, flag], timeout=120)
        lines.append(f"{name}: {out.splitlines()[0] if out else '(no version output)'}")
    lines.append(f"Pillow: {Image.__version__ if hasattr(Image,'__version__') else 'ok'}")
    return "\n".join(lines)


@mcp.tool()
def inkscape_export(input: str, output: str, dpi: int = 96,
                    width: int = 0, height: int = 0, area: str = "drawing") -> str:
    """Convert/export a vector (or SVG) file via Inkscape.

    Output format is inferred from the output extension: .pdf .png .eps .ps .svg .emf .wmf.
    Great for SVG->PDF (print), SVG->PNG (raster at a chosen DPI/size), PDF->SVG, etc.

    Args:
        input:  Source file (svg, pdf, eps, ...).
        output: Destination file; extension picks the format.
        dpi:    Raster DPI for PNG output (default 96).
        width:  Force output pixel width (PNG); 0 = auto.
        height: Force output pixel height (PNG); 0 = auto.
        area:   "drawing" (tight bbox) or "page" (whole canvas). Default "drawing".
    """
    exe = _tool("inkscape")
    if not exe:
        return "Inkscape not installed."
    src, dst = _abs(input), _abs(output)
    if not src.exists():
        return f"Input not found: {src}"
    dst.parent.mkdir(parents=True, exist_ok=True)
    ext = dst.suffix.lower().lstrip(".")
    fmt = {"ps": "ps", "eps": "eps", "pdf": "pdf", "png": "png",
           "svg": "svg", "emf": "emf", "wmf": "wmf"}.get(ext)
    if not fmt:
        return f"Unsupported output extension .{ext} (use pdf/png/eps/ps/svg/emf/wmf)."
    cmd = [exe, str(src), f"--export-type={fmt}", f"--export-filename={dst}"]
    if area == "page":
        cmd.append("--export-area-page")
    else:
        cmd.append("--export-area-drawing")
    if fmt == "png":
        cmd.append(f"--export-dpi={dpi}")
        if width:
            cmd.append(f"--export-width={width}")
        if height:
            cmd.append(f"--export-height={height}")
    rc, out = _run(cmd, timeout=180)
    if dst.exists():
        return f"OK -> {dst} ({dst.stat().st_size//1024} KB)\n{out}".strip()
    return f"FAILED (rc={rc})\n{out}"


@mcp.tool()
def svg_dimensions(svg: str) -> str:
    """Return the width, height and viewBox of an SVG (via Inkscape --query)."""
    exe = _tool("inkscape")
    if not exe:
        return "Inkscape not installed."
    src = _abs(svg)
    if not src.exists():
        return f"Not found: {src}"
    rc, w = _run([exe, str(src), "--query-width"], 60)
    rc, h = _run([exe, str(src), "--query-height"], 60)
    return f"width={w.splitlines()[-1] if w else '?'} height={h.splitlines()[-1] if h else '?'} (user units)"


@mcp.tool()
def image_convert(input: str, output: str, quality: int = 90) -> str:
    """Convert a raster image between formats (PNG/JPEG/WEBP/TIFF/BMP) with Pillow.

    Args:
        input:   Source raster.
        output:  Destination; extension picks the format.
        quality: JPEG/WEBP quality 1-95 (default 90).
    """
    src, dst = _abs(input), _abs(output)
    if not src.exists():
        return f"Input not found: {src}"
    dst.parent.mkdir(parents=True, exist_ok=True)
    try:
        im = Image.open(src)
        if dst.suffix.lower() in (".jpg", ".jpeg") and im.mode in ("RGBA", "P"):
            im = im.convert("RGB")
        params = {}
        if dst.suffix.lower() in (".jpg", ".jpeg", ".webp"):
            params["quality"] = int(quality)
        im.save(dst, **params)
        return f"OK -> {dst} ({dst.stat().st_size//1024} KB, {im.size[0]}x{im.size[1]})"
    except Exception as e:
        return f"FAILED: {type(e).__name__}: {e}"


@mcp.tool()
def image_resize(input: str, output: str, width: int = 0, height: int = 0,
                 keep_aspect: bool = True) -> str:
    """Resize a raster image with Pillow.

    Provide width and/or height (px). With keep_aspect, the missing dimension is
    computed; if both given and keep_aspect, the image is fit inside the box.
    """
    src, dst = _abs(input), _abs(output)
    if not src.exists():
        return f"Input not found: {src}"
    if not width and not height:
        return "Provide width and/or height."
    dst.parent.mkdir(parents=True, exist_ok=True)
    try:
        im = Image.open(src)
        w0, h0 = im.size
        if keep_aspect:
            if width and height:
                im.thumbnail((width, height), Image.LANCZOS)
            elif width:
                im = im.resize((width, round(h0 * width / w0)), Image.LANCZOS)
            else:
                im = im.resize((round(w0 * height / h0), height), Image.LANCZOS)
        else:
            im = im.resize((width or w0, height or h0), Image.LANCZOS)
        if dst.suffix.lower() in (".jpg", ".jpeg") and im.mode in ("RGBA", "P"):
            im = im.convert("RGB")
        im.save(dst)
        return f"OK -> {dst} ({im.size[0]}x{im.size[1]}, {dst.stat().st_size//1024} KB)"
    except Exception as e:
        return f"FAILED: {type(e).__name__}: {e}"


@mcp.tool()
def images_to_pdf(inputs: list[str], output: str) -> str:
    """Combine one or more raster images into a single multi-page PDF (Pillow)."""
    if not inputs:
        return "No input images."
    dst = _abs(output)
    dst.parent.mkdir(parents=True, exist_ok=True)
    try:
        imgs = [Image.open(_abs(p)).convert("RGB") for p in inputs]
        imgs[0].save(dst, save_all=True, append_images=imgs[1:])
        return f"OK -> {dst} ({len(imgs)} pages, {dst.stat().st_size//1024} KB)"
    except Exception as e:
        return f"FAILED: {type(e).__name__}: {e}"


@mcp.tool()
def gimp_script(script_fu: str, timeout: int = 180) -> str:
    """Run an arbitrary GIMP Script-Fu batch expression headless (power tool).

    The expression runs in `gimp -i` (no GUI). You are responsible for loading/saving
    files inside the script. A (gimp-quit 0) is appended automatically.
    Example: '(let* ((img (car (gimp-file-load RUN-NONINTERACTIVE "/a.png" "a.png"))))
              (gimp-image-flatten img)
              (file-png-save RUN-NONINTERACTIVE img (car (gimp-image-get-active-drawable img))
                             "/b.png" "b" 0 9 1 1 1 1 1))'
    """
    exe = _tool("gimp")
    if not exe:
        return "GIMP not installed."
    cmd = [exe, "-i", "-d", "-f", "--batch-interpreter=plug-in-script-fu-eval",
           "-b", script_fu, "-b", "(gimp-quit 0)"]
    rc, out = _run(cmd, timeout=timeout)
    return f"rc={rc}\n{out}"


if __name__ == "__main__":
    mcp.run(transport="stdio")
