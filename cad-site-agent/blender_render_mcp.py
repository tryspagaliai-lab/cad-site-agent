"""
Blender Render — MCP Server (headless Blender automation)

Drives Blender fully headless (`blender -b`) so an agent can render scenes, run
Python against the bpy API, and turn 3D models into images without any GUI.

Backend: Blender 5.1 (native Linux, ~/.local/bin/blender).

Tools:
    - blender_info()                         — Blender version / path
    - render_blend(blend, output, ...)       — render frame(s) of a .blend file
    - quick_render(model, output, ...)       — import a 3D model + auto camera/light + render
    - run_python(script, blend="")           — run arbitrary bpy Python headless (power tool)

Usage (stdio): python3 blender_render_mcp.py
"""
from __future__ import annotations

import shutil
import subprocess
import tempfile
from pathlib import Path

from mcp.server.fastmcp import FastMCP

REPO_ROOT = Path(__file__).parent.resolve()
BIN = Path.home() / ".local" / "bin"

mcp = FastMCP("blender-render")


def _blender() -> str | None:
    p = BIN / "blender"
    return str(p) if p.exists() else shutil.which("blender")


def _abs(path: str) -> Path:
    p = Path(path).expanduser()
    return p if p.is_absolute() else (REPO_ROOT / p)


def _run(cmd: list[str], timeout: int) -> tuple[int, str]:
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        out = (r.stdout or "") + (("\n[stderr] " + r.stderr) if r.stderr.strip() else "")
        return r.returncode, out.strip()
    except subprocess.TimeoutExpired:
        return 124, f"timed out after {timeout}s"
    except Exception as e:
        return 1, f"{type(e).__name__}: {e}"


@mcp.tool()
def blender_info() -> str:
    """Report the Blender version and executable path."""
    exe = _blender()
    if not exe:
        return "Blender not installed."
    rc, out = _run([exe, "--version"], 60)
    return f"{exe}\n{out}"


@mcp.tool()
def render_blend(blend: str, output: str, frame: int = 1,
                 engine: str = "", samples: int = 0, timeout: int = 600) -> str:
    """Render a frame of an existing .blend file headless.

    Args:
        blend:   Path to the .blend file.
        output:  Output image path (extension sets format, e.g. .png). Blender appends
                 the frame number unless you use a '#' pattern; the final file is reported.
        frame:   Frame number to render (default 1).
        engine:  "" (keep file's), "BLENDER_EEVEE", "CYCLES", or "BLENDER_WORKBENCH".
        samples: Override render samples (0 = keep scene setting).
        timeout: Seconds (default 600).
    """
    exe = _blender()
    if not exe:
        return "Blender not installed."
    src = _abs(blend)
    if not src.exists():
        return f"Blend not found: {src}"
    dst = _abs(output)
    dst.parent.mkdir(parents=True, exist_ok=True)
    # Blender -o uses a prefix; strip extension and let it append frame + ext
    out_prefix = str(dst.with_suffix("")) + "_"
    ext = dst.suffix.lower().lstrip(".") or "png"
    fmt = {"png": "PNG", "jpg": "JPEG", "jpeg": "JPEG", "tif": "TIFF",
           "tiff": "TIFF", "exr": "OPEN_EXR", "bmp": "BMP"}.get(ext, "PNG")
    cmd = [exe, "-b", str(src)]
    if engine:
        cmd += ["-E", engine]
    if samples:
        expr = f"import bpy; bpy.context.scene.cycles.samples={samples}; " \
               f"bpy.context.scene.eevee.taa_render_samples={samples}"
        cmd += ["--python-expr", expr]
    cmd += ["-o", out_prefix, "-F", fmt, "-f", str(frame)]
    rc, out = _run(cmd, timeout)
    produced = sorted(dst.parent.glob(dst.with_suffix("").name + "_*"))
    tail = "\n".join(out.splitlines()[-6:])
    if produced:
        p = produced[-1]
        return f"OK -> {p} ({p.stat().st_size//1024} KB)\n{tail}"
    return f"No output produced (rc={rc}).\n{tail}"


@mcp.tool()
def quick_render(model: str, output: str, resolution: int = 1024,
                 samples: int = 64, engine: str = "BLENDER_EEVEE",
                 timeout: int = 600) -> str:
    """Import a 3D model into an empty scene, add a framing camera + light, and render.

    Supported model formats: .obj .stl .fbx .glb .gltf .ply .x3d .dae (native importers).
    (DXF is NOT natively importable by Blender without an add-on.)

    Args:
        model:      Path to the 3D model.
        output:     Output PNG path.
        resolution: Square render resolution in px (default 1024).
        samples:    Render samples (default 64).
        engine:     Render engine (default EEVEE Next; use CYCLES for quality).
    """
    exe = _blender()
    if not exe:
        return "Blender not installed."
    src = _abs(model)
    if not src.exists():
        return f"Model not found: {src}"
    dst = _abs(output)
    dst.parent.mkdir(parents=True, exist_ok=True)
    ext = src.suffix.lower()
    importers = {
        ".obj": "bpy.ops.wm.obj_import(filepath=M)",
        ".stl": "bpy.ops.wm.stl_import(filepath=M)",
        ".ply": "bpy.ops.wm.ply_import(filepath=M)",
        ".fbx": "bpy.ops.import_scene.fbx(filepath=M)",
        ".glb": "bpy.ops.import_scene.gltf(filepath=M)",
        ".gltf": "bpy.ops.import_scene.gltf(filepath=M)",
        ".x3d": "bpy.ops.import_scene.x3d(filepath=M)",
        ".dae": "bpy.ops.wm.collada_import(filepath=M)",
    }
    if ext not in importers:
        return f"Unsupported model format {ext}. Supported: {', '.join(importers)}"

    script = f'''
import bpy, math, mathutils
M = r"{src}"
bpy.ops.wm.read_factory_settings(use_empty=True)
{importers[ext]}
objs = [o for o in bpy.context.scene.objects if o.type == "MESH"]
if not objs:
    raise SystemExit("no mesh imported")
# bounding box of all imported meshes
import itertools
mins = [1e18]*3; maxs = [-1e18]*3
for o in objs:
    for v in o.bound_box:
        w = o.matrix_world @ mathutils.Vector(v)
        for i in range(3):
            mins[i] = min(mins[i], w[i]); maxs[i] = max(maxs[i], w[i])
center = mathutils.Vector([(mins[i]+maxs[i])/2 for i in range(3)])
size = max(maxs[i]-mins[i] for i in range(3)) or 1.0
# camera
cam_data = bpy.data.cameras.new("Cam"); cam = bpy.data.objects.new("Cam", cam_data)
bpy.context.scene.collection.objects.link(cam)
d = size * 2.2
cam.location = center + mathutils.Vector((d, -d, d*0.8))
direction = center - cam.location
cam.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()
bpy.context.scene.camera = cam
# light
light_data = bpy.data.lights.new("Sun", type='SUN'); light_data.energy = 3.0
light = bpy.data.objects.new("Sun", light_data)
bpy.context.scene.collection.objects.link(light)
light.location = center + mathutils.Vector((d, -d, d*1.5))
# world bg
world = bpy.data.worlds.new("W"); bpy.context.scene.world = world
world.use_nodes = True
world.node_tree.nodes["Background"].inputs[0].default_value = (0.05,0.05,0.05,1)
# render settings — pick a valid engine (enum names differ across Blender versions)
sc = bpy.context.scene
_want = "{engine}"
_avail = list(sc.render.bl_rna.properties['engine'].enum_items.keys())
sc.render.engine = _want if _want in _avail else ("BLENDER_EEVEE" if "BLENDER_EEVEE" in _avail else _avail[0])
sc.render.resolution_x = {resolution}; sc.render.resolution_y = {resolution}
sc.render.image_settings.file_format = 'PNG'
try: sc.eevee.taa_render_samples = {samples}
except Exception: pass
try: sc.cycles.samples = {samples}
except Exception: pass
sc.render.filepath = r"{dst}"
bpy.ops.render.render(write_still=True)
'''
    with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False) as f:
        f.write(script)
        script_path = f.name
    rc, out = _run([exe, "-b", "--python", script_path], timeout)
    Path(script_path).unlink(missing_ok=True)
    tail = "\n".join(out.splitlines()[-6:])
    if dst.exists():
        return f"OK -> {dst} ({dst.stat().st_size//1024} KB)\n{tail}"
    return f"No output produced (rc={rc}).\n{tail}"


@mcp.tool()
def run_python(script: str, blend: str = "", timeout: int = 600) -> str:
    """Run arbitrary Blender Python (bpy) headless (power tool).

    Args:
        script: Python source executed inside Blender's interpreter (bpy available).
        blend:  Optional .blend to open first (default: factory-empty scene).
        timeout: Seconds (default 600).
    """
    exe = _blender()
    if not exe:
        return "Blender not installed."
    with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False) as f:
        f.write(script)
        sp = f.name
    cmd = [exe, "-b"]
    if blend:
        src = _abs(blend)
        if not src.exists():
            Path(sp).unlink(missing_ok=True)
            return f"Blend not found: {src}"
        cmd.append(str(src))
    cmd += ["--python", sp]
    rc, out = _run(cmd, timeout)
    Path(sp).unlink(missing_ok=True)
    return f"rc={rc}\n" + "\n".join(out.splitlines()[-40:])


if __name__ == "__main__":
    mcp.run(transport="stdio")
