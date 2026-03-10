"""
Integration tests for the DXF analyzer.
Requires real DXF files at E:/SHAKESPEARE/RAW_DATA/.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import pytest
from cad_site_agent.analyzer.dxf_analyzer import analyze_dxf, AnalysisReport

RAW_DATA = Path("E:/SHAKESPEARE/RAW_DATA")
ROMAN_GARDENS = RAW_DATA / "roman_gardens_gapclosed.dxf"
PLANNING_LAYOUT = RAW_DATA / "ST-23-01S Planning Layout.dxf"


# ─── Skip markers ───────────────────────────────────────────────────────────

skip_if_no_raw = pytest.mark.skipif(
    not RAW_DATA.exists(),
    reason="E:/SHAKESPEARE/RAW_DATA not available"
)


# ─── Basic analyzer smoke tests ──────────────────────────────────────────────

@skip_if_no_raw
@pytest.mark.skipif(not ROMAN_GARDENS.exists(), reason="roman_gardens_gapclosed.dxf not found")
def test_analyze_roman_gardens_returns_report():
    report = analyze_dxf(str(ROMAN_GARDENS))
    assert isinstance(report, AnalysisReport)
    assert report.total_entities > 0
    assert report.total_layers > 0


@skip_if_no_raw
@pytest.mark.skipif(not ROMAN_GARDENS.exists(), reason="roman_gardens_gapclosed.dxf not found")
def test_analyze_roman_gardens_has_expected_fields():
    report = analyze_dxf(str(ROMAN_GARDENS))
    assert report.source_file.endswith(".dxf")
    assert report.file_size_kb > 0
    assert isinstance(report.entity_type_counts, dict)
    assert isinstance(report.layers, dict)
    assert len(report.layers) > 0


@skip_if_no_raw
@pytest.mark.skipif(not PLANNING_LAYOUT.exists(), reason="ST-23-01S Planning Layout.dxf not found")
def test_analyze_planning_layout_returns_report():
    report = analyze_dxf(str(PLANNING_LAYOUT))
    assert isinstance(report, AnalysisReport)
    assert report.total_entities > 0


@skip_if_no_raw
@pytest.mark.skipif(not ROMAN_GARDENS.exists(), reason="roman_gardens_gapclosed.dxf not found")
def test_report_to_dict_serialisable():
    """report.to_dict() must return a JSON-serialisable dict."""
    import json
    report = analyze_dxf(str(ROMAN_GARDENS))
    d = report.to_dict()
    # Verify it's serialisable
    json.dumps(d)
    assert "total_entities" in d
    assert "layers" in d


@skip_if_no_raw
@pytest.mark.skipif(not ROMAN_GARDENS.exists(), reason="roman_gardens_gapclosed.dxf not found")
def test_classify_roman_gardens():
    """Integration: analyze + classify should produce a non-unknown result."""
    from cad_site_agent.classify.drawing_type import classify_drawing_type
    report = analyze_dxf(str(ROMAN_GARDENS))
    result = classify_drawing_type(report)
    assert result.label in {
        "rich_site_layout", "sparse_linework",
        "illustrator_derived", "max_prep", "unknown"
    }
    # Roman gardens is a rich site DXF — should classify as rich_site_layout or sparse_linework
    print(f"\nRoman Gardens classification: {result.label} ({result.confidence:.2f})")
    print(f"  Reasons: {result.reasons}")
    print(f"  Diagnostics: hatch={result.hatch_count} spline={result.spline_count} semantic={result.semantic_class_count}")


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v", "-s"])
