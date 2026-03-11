"""test_cli.py — verify CLI entry-point is importable by pyproject.toml scripts."""


def test_hatch_candidates_is_importable():
    """pyproject.toml entry point cad_site_agent.cli:hatch_candidates must exist."""
    from cad_site_agent.cli import hatch_candidates  # noqa: F401 — import is the test
