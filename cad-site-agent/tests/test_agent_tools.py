"""Tests for agent_tools: path allowlist, measure_dxf, render_dxf_png."""
from __future__ import annotations

import math
from pathlib import Path

import ezdxf
import pytest

from cad_site_agent.agent_tools import (
    ALLOW_ENV,
    PathNotAllowed,
    measure_dxf,
    render_dxf_png,
    resolve_allowed,
)


# ─── fixtures ────────────────────────────────────────────────────────────────


@pytest.fixture
def sample_dxf(tmp_path: Path) -> Path:
    """Known geometry: 10×20 closed rect, r=5 circle, 30-long line, open polyline."""
    doc = ezdxf.new("R2010")
    doc.header["$INSUNITS"] = 4  # mm
    msp = doc.modelspace()
    msp.add_lwpolyline([(0, 0), (10, 0), (10, 20), (0, 20)], close=True,
                       dxfattribs={"layer": "BUILDING"})
    msp.add_circle((50, 50), 5, dxfattribs={"layer": "TREES"})
    msp.add_line((0, -10), (30, -10), dxfattribs={"layer": "ROAD"})
    msp.add_lwpolyline([(0, 30), (5, 30), (5, 35)], dxfattribs={"layer": "ROAD"})
    msp.add_text("A", dxfattribs={"layer": "TEXT"})
    path = tmp_path / "sample.dxf"
    doc.saveas(str(path))
    return path


# ─── resolve_allowed ─────────────────────────────────────────────────────────


class TestResolveAllowed:
    def test_relative_inside_repo(self, tmp_path, monkeypatch):
        monkeypatch.delenv(ALLOW_ENV, raising=False)
        assert resolve_allowed("a/b.dxf", tmp_path) == (tmp_path / "a/b.dxf").resolve()

    def test_absolute_outside_rejected(self, tmp_path, monkeypatch):
        monkeypatch.delenv(ALLOW_ENV, raising=False)
        with pytest.raises(PathNotAllowed):
            resolve_allowed("/etc/passwd", tmp_path)

    def test_dotdot_escape_rejected(self, tmp_path, monkeypatch):
        monkeypatch.delenv(ALLOW_ENV, raising=False)
        repo = tmp_path / "repo"
        repo.mkdir()
        with pytest.raises(PathNotAllowed):
            resolve_allowed("../secret.dxf", repo)

    def test_symlink_escape_rejected(self, tmp_path, monkeypatch):
        monkeypatch.delenv(ALLOW_ENV, raising=False)
        repo = tmp_path / "repo"
        outside = tmp_path / "outside"
        repo.mkdir()
        outside.mkdir()
        (repo / "link").symlink_to(outside)
        with pytest.raises(PathNotAllowed):
            resolve_allowed("link/x.dxf", repo)

    def test_env_allow_path(self, tmp_path, monkeypatch):
        repo = tmp_path / "repo"
        data = tmp_path / "data"
        repo.mkdir()
        data.mkdir()
        monkeypatch.setenv(ALLOW_ENV, str(data))
        assert resolve_allowed(str(data / "h.dxf"), repo) == (data / "h.dxf").resolve()

    def test_sibling_prefix_not_allowed(self, tmp_path, monkeypatch):
        """/x/repo2 must not pass because it shares a string prefix with /x/repo."""
        monkeypatch.delenv(ALLOW_ENV, raising=False)
        repo = tmp_path / "repo"
        repo.mkdir()
        with pytest.raises(PathNotAllowed):
            resolve_allowed(str(tmp_path / "repo2" / "a.dxf"), repo)


# ─── measure_dxf ─────────────────────────────────────────────────────────────


class TestMeasureDxf:
    def test_units_and_totals(self, sample_dxf):
        m = measure_dxf(sample_dxf)
        assert m["units"] == "mm"
        assert m["totals"]["entities"] == 5
        assert m["totals"]["closed_count"] == 2

    def test_rect_area_and_perimeter(self, sample_dxf):
        b = measure_dxf(sample_dxf)["layers"]["BUILDING"]
        assert b["closed_area"] == pytest.approx(200.0)
        assert b["length"] == pytest.approx(60.0)
        assert b["open_polylines"] == 0

    def test_circle_area_and_length(self, sample_dxf):
        t = measure_dxf(sample_dxf)["layers"]["TREES"]
        assert t["closed_area"] == pytest.approx(math.pi * 25, abs=1e-3)
        assert t["length"] == pytest.approx(2 * math.pi * 5, abs=1e-3)

    def test_arc_length_exact(self, tmp_path):
        doc = ezdxf.new("R2010")
        doc.modelspace().add_arc((0, 0), 10, 350, 80)  # 90° sweep across 0°
        p = tmp_path / "arc.dxf"
        doc.saveas(str(p))
        a = measure_dxf(p)["layers"]["0"]
        assert a["length"] == pytest.approx(math.pi * 10 / 2, abs=1e-3)
        assert a["closed_count"] == 0

    def test_open_polyline_counted(self, sample_dxf):
        r = measure_dxf(sample_dxf)["layers"]["ROAD"]
        assert r["length"] == pytest.approx(40.0)
        assert r["open_polylines"] == 1
        assert r["closed_count"] == 0

    def test_non_curve_counted_not_measured(self, sample_dxf):
        t = measure_dxf(sample_dxf)["layers"]["TEXT"]
        assert t["counts"] == {"TEXT": 1}
        assert t["length"] == 0

    def test_layer_filter(self, sample_dxf):
        m = measure_dxf(sample_dxf, layer="ROAD")
        assert list(m["layers"]) == ["ROAD"]
        assert m["layer_filter"] == "ROAD"

    def test_extents(self, sample_dxf):
        e = measure_dxf(sample_dxf)["extents"]
        assert e["min"] == [0.0, -10.0]
        assert e["max"] == pytest.approx([55.0, 55.0])


# ─── render_dxf_png ──────────────────────────────────────────────────────────


def test_render_png(sample_dxf, tmp_path):
    png = render_dxf_png(sample_dxf, tmp_path / "out" / "s.png", size_in=3)
    assert png.exists()
    assert png.read_bytes()[:8] == b"\x89PNG\r\n\x1a\n"


def test_render_bad_file_raises(tmp_path):
    bad = tmp_path / "bad.dxf"
    bad.write_text("not a dxf")
    with pytest.raises(RuntimeError):
        render_dxf_png(bad, tmp_path / "bad.png")
