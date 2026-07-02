"""Tests for semantic/normalizer.py — layer normalisation."""
from pathlib import Path

import ezdxf
import pytest

from cad_site_agent.semantic.normalizer import run_normalization

CONFIG = Path(__file__).resolve().parents[1] / "config" / "layer_aliases.yaml"


def _make_dxf(tmp_path: Path, layers: list[str]) -> Path:
    doc = ezdxf.new("R2018")
    msp = doc.modelspace()
    for name in layers:
        doc.layers.add(name)
        msp.add_lwpolyline(
            [(0, 0), (100, 0), (100, 100), (0, 100)],
            close=True,
            dxfattribs={"layer": name},
        )
    p = tmp_path / "in.dxf"
    doc.saveas(str(p))
    return p


class TestCaseInsensitiveLayerTable:
    def test_canonical_differs_only_by_case_does_not_raise(self, tmp_path):
        # Regression: DXF layer table is case-insensitive; when the drawing
        # already has "PARKING" and the alias maps to canonical "parking",
        # doc.layers.new() used to raise DXFTableEntryError.
        src = _make_dxf(tmp_path, ["PARKING"])
        out = tmp_path / "out.dxf"
        result = run_normalization(src, config_path=CONFIG, output_path=out)
        assert out.exists()
        assert result["output_path"] == str(out)

    def test_entities_moved_to_canonical_layer(self, tmp_path):
        src = _make_dxf(tmp_path, ["PARKING"])
        out = tmp_path / "out.dxf"
        result = run_normalization(src, config_path=CONFIG, output_path=out)
        if "PARKING" in result["mapping"]:
            canonical = result["mapping"]["PARKING"]
            doc = ezdxf.readfile(str(out))
            layers_used = {e.dxf.layer for e in doc.modelspace()}
            assert canonical in layers_used


class TestBasicNormalisation:
    def test_unmapped_layer_reported(self, tmp_path):
        src = _make_dxf(tmp_path, ["TOTALLY_UNKNOWN_LAYER_XYZ"])
        out = tmp_path / "out.dxf"
        result = run_normalization(src, config_path=CONFIG, output_path=out)
        assert "TOTALLY_UNKNOWN_LAYER_XYZ" in result["unmapped_layers"]

    def test_returns_expected_keys(self, tmp_path):
        src = _make_dxf(tmp_path, ["FENCE"])
        out = tmp_path / "out.dxf"
        result = run_normalization(src, config_path=CONFIG, output_path=out)
        for key in ("source", "layers_found", "layers_renamed", "unmapped",
                    "mapping", "unmapped_layers", "output_path"):
            assert key in result
