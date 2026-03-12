# tests/test_process.py
"""Tests for pipeline.py — ProcessReport and run_process()."""
from __future__ import annotations

import json
import shutil
import tempfile
from pathlib import Path

import pytest

from cad_site_agent.pipeline import ProcessReport, run_process


# ── Fixtures ──────────────────────────────────────────────────────────────────

SAMPLE_DXF = Path(__file__).parent / "fixtures" / "sample.dxf"


@pytest.fixture()
def tmp_out(tmp_path):
    return tmp_path / "out.dxf"


# ── ProcessReport ──────────────────────────────────────────────────────────────

class TestProcessReport:
    def test_fields_exist(self):
        r = ProcessReport(
            source_dxf="a.dxf",
            output_dxf="b.dxf",
            generated_at="2026-01-01T00:00:00",
            candidates_total=10,
            candidates_auto=8,
            candidates_review=2,
            hatches_written=7,
            features_written=100,
            features_removed=5,
            features_skipped=50,
            drawing_type="site_layout",
            drawing_confidence=0.9,
        )
        assert r.source_dxf == "a.dxf"
        assert r.hatches_written == 7

    def test_to_dict(self):
        r = ProcessReport(
            source_dxf="a.dxf",
            output_dxf="b.dxf",
            generated_at="2026-01-01T00:00:00",
            candidates_total=10,
            candidates_auto=8,
            candidates_review=2,
            hatches_written=7,
            features_written=100,
            features_removed=5,
            features_skipped=50,
            drawing_type="site_layout",
            drawing_confidence=0.9,
        )
        d = r.to_dict()
        assert d["hatches_written"] == 7
        assert "generated_at" in d


# ── run_process ────────────────────────────────────────────────────────────────

class TestRunProcess:
    def test_raises_if_source_missing(self, tmp_out):
        with pytest.raises(FileNotFoundError, match="Source DXF"):
            run_process("nonexistent.dxf", str(tmp_out))

    def test_raises_if_output_exists(self, tmp_path):
        out = tmp_path / "out.dxf"
        out.touch()
        with pytest.raises(FileExistsError):
            run_process(str(SAMPLE_DXF), str(out))

    @pytest.mark.skipif(not SAMPLE_DXF.exists(), reason="no fixture DXF")
    def test_produces_output_files(self, tmp_path):
        out = tmp_path / "result.dxf"
        run_process(str(SAMPLE_DXF), str(out))
        assert out.exists(), "output DXF must be created"
        stem = out.stem
        assert (tmp_path / f"{stem}.hatches.dxf").exists(), "hatches DXF"
        assert (tmp_path / f"{stem}.hatch_candidates.json").exists(), "candidates JSON"
        assert (tmp_path / f"{stem}.process.json").exists(), "process summary JSON"

    @pytest.mark.skipif(not SAMPLE_DXF.exists(), reason="no fixture DXF")
    def test_returns_process_report(self, tmp_path):
        out = tmp_path / "result.dxf"
        report = run_process(str(SAMPLE_DXF), str(out))
        assert isinstance(report, ProcessReport)
        assert report.source_dxf == str(SAMPLE_DXF)
        assert report.output_dxf == str(out)

    @pytest.mark.skipif(not SAMPLE_DXF.exists(), reason="no fixture DXF")
    def test_process_json_is_valid(self, tmp_path):
        out = tmp_path / "result.dxf"
        run_process(str(SAMPLE_DXF), str(out))
        json_file = tmp_path / f"{out.stem}.process.json"
        data = json.loads(json_file.read_text())
        assert "meta" in data
        assert "totals" in data
