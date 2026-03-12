"""
linework_writer.py — Phase 7

Thin convenience wrapper: route linear entities only.

Public API
----------
    run_linework_write(source_dxf, candidates_json, output_dxf, **kwargs)
        -> RoutingReport
"""
from __future__ import annotations

from typing import Optional

from .routing import RoutingReport, run_route_features, write_routing_reports
from pathlib import Path


def run_linework_write(
    source_dxf: str,
    candidates_json: str,
    output_dxf: str,
    *,
    exclude_noise: bool = True,
    taxonomy_path: Optional[str] = None,
    roles_path: Optional[str] = None,
    routing_hints: Optional[dict] = None,
) -> RoutingReport:
    """Route only linear (linework) entities to the output DXF.

    Calls run_route_features with markings, symbols and text disabled.

    Safety rules mirror run_route_features:
    - Raises FileNotFoundError if source DXF or candidates JSON is absent.
    - Raises FileExistsError if output DXF already exists.
    - Never modifies the source DXF.
    """
    return run_route_features(
        source_dxf,
        candidates_json,
        output_dxf,
        include_linework=True,
        include_markings=False,
        include_symbols=False,
        include_text=False,
        exclude_noise=exclude_noise,
        taxonomy_path=taxonomy_path,
        roles_path=roles_path,
        routing_hints=routing_hints,
    )
