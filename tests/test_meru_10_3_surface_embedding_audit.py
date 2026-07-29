"""Regression tests for the native Meru 10_3 surface embedding audit."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

DERIVED_DIR = (
    ROOT
    / "data"
    / "derived"
    / "meru_3_10_digital"
)

CERTIFICATE_PATH = (
    DERIVED_DIR
    / "meru_10_3_surface_embedding_audit.json"
)

REPORT_PATH = (
    ROOT
    / "reports"
    / "meru_10_3_surface_embedding_audit.md"
)

EXPECTED_SHA256 = (
    "855c46cfeeb31e4394b7a4a294b397aa"
    "c4cbc14154e172a326e33243dd9e384b"
)


def read_certificate() -> dict[str, Any]:
    """Read the frozen surface certificate."""
    return json.loads(
        CERTIFICATE_PATH.read_text(
            encoding="utf-8",
        )
    )


def test_surface_certificate_uses_frozen_source() -> None:
    """The audit must retain the verified native VRML identity."""
    certificate = read_certificate()

    assert certificate["source"]["sha256"] == EXPECTED_SHA256
    assert certificate["source"]["filename"] == (
        "f24de4a08a_10_3.wrl"
    )

    assert certificate["mesh"]["vertices"] == 6000
    assert certificate["mesh"]["faces"] == 12000
    assert certificate["mesh"]["edges"] == 18000


def test_complete_face_pair_partition() -> None:
    """Every distinct triangle pair must belong to one audited class."""
    partition = read_certificate()[
        "complete_face_pair_partition"
    ]

    assert partition[
        "total_distinct_face_pairs"
    ] == 71_994_000

    assert partition[
        "shared_edge_pairs"
    ] == 18_000

    assert partition[
        "shared_vertex_only_pairs"
    ] == 54_000

    assert partition[
        "vertex_disjoint_aabb_candidates"
    ] == 21_622

    assert partition[
        "vertex_disjoint_aabb_rejected"
    ] == 71_900_378

    assert partition[
        "vertex_disjoint_pairs"
    ] == 71_922_000

    assert partition[
        "partition_complete"
    ] is True


def test_vertex_disjoint_faces_are_separated() -> None:
    """The remote narrow phase must find no face overlap."""
    certificate = read_certificate()
    audit = certificate[
        "vertex_disjoint_audit"
    ]

    assert audit[
        "narrow_phase_pairs"
    ] == 21_622

    assert audit["overlaps"] == 0

    assert audit[
        "minimum_sat_separation_margin"
    ] > 0.04

    assert certificate[
        "margin_ratios"
    ][
        "vertex_disjoint_sat_margin_to_tolerance"
    ] > 1_000_000


def test_incident_faces_meet_only_in_shared_simplices() -> None:
    """Incident pairs must have no excess intersections."""
    certificate = read_certificate()
    audit = certificate[
        "incident_face_audit"
    ]

    assert audit["incident_pairs"] == 72_000
    assert audit["shared_edge_pairs"] == 18_000
    assert audit["shared_edge_coplanar"] == 82

    assert audit[
        "shared_edge_excess_intersections"
    ] == 0

    assert audit[
        "shared_vertex_only_pairs"
    ] == 54_000

    assert audit[
        "shared_vertex_excess_intersections"
    ] == 0

    ratios = certificate[
        "margin_ratios"
    ]

    assert ratios[
        "noncoplanar_shared_edge_sine_to_tolerance"
    ] > 10_000

    assert ratios[
        "coplanar_shared_edge_margin_to_tolerance"
    ] > 100_000

    assert ratios[
        "shared_vertex_margin_to_tolerance"
    ] > 10_000


def test_surface_embedding_result_and_scope() -> None:
    """The final result must pass without claiming exact arithmetic."""
    certificate = read_certificate()
    result = certificate["certificate"]

    assert result["mesh_topology_pass"] is True
    assert result["structured_tube_pass"] is True
    assert result["complete_pair_partition_pass"] is True
    assert result["vertex_disjoint_face_pass"] is True
    assert result["incident_face_pass"] is True
    assert result["surface_embedding_pass"] is True

    assert certificate[
        "scope"
    ][
        "all_distinct_face_pairs_accounted_for"
    ] is True

    assert certificate[
        "scope"
    ][
        "formal_exact_arithmetic"
    ] is False

    normalized = " ".join(
        REPORT_PATH.read_text(
            encoding="utf-8",
        ).lower().split()
    )

    assert (
        "the complete native `10_3.wrl` triangle mesh "
        "is a simplicial embedding"
        in normalized
    )

    assert (
        "not a formal exact-arithmetic proof"
        in normalized
    )

    assert (
        "does not independently establish every broader "
        "interpretive claim"
        in normalized
    )
