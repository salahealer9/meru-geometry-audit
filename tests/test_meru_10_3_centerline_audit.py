"""Regression tests for the frozen Meru 10_3 native-geometry audit."""

from __future__ import annotations

import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

AUDIT_PATH = (
    ROOT
    / "data"
    / "derived"
    / "meru_3_10_digital"
    / "meru_10_3_centerline_audit.json"
)

REPORT_PATH = (
    ROOT
    / "reports"
    / "meru_10_3_native_geometry_audit.md"
)

EXPECTED_SHA256 = (
    "855c46cfeeb31e4394b7a4a294b397aa"
    "c4cbc14154e172a326e33243dd9e384b"
)


def load_audit() -> dict:
    """Load the frozen derived audit."""
    return json.loads(
        AUDIT_PATH.read_text(
            encoding="utf-8",
        )
    )


def test_source_identity_is_frozen() -> None:
    """The audit must remain tied to the recovered native asset."""
    audit = load_audit()
    source = audit["source"]

    assert source["canonical_url"].endswith(
        "/10_3.wrl"
    )

    assert source["byte_count"] == 429_161
    assert source["sha256"] == EXPECTED_SHA256
    assert source["vrml_header"] == "#VRML V2.0 utf8"


def test_native_mesh_is_one_closed_genus_one_surface() -> None:
    """The mesh must retain its certified combinatorial topology."""
    mesh = load_audit()["mesh_topology"]

    assert mesh["used_vertex_count"] == 6000
    assert mesh["unique_edge_count"] == 18000
    assert mesh["face_count"] == 12000
    assert mesh["euler_characteristic"] == 0

    assert mesh["connected_component_count"] == 1
    assert mesh["component_vertex_counts"] == [6000]

    assert mesh["boundary_edge_count"] == 0
    assert mesh["nonmanifold_edge_count"] == 0
    assert mesh["orientation_conflict_count"] == 0
    assert mesh["zero_area_triangle_count"] == 0

    assert mesh["closed_orientable_manifold"] is True
    assert mesh["candidate_genus"] == 1
    assert mesh["vertex_valence_histogram"] == {
        "6": 6000,
    }


def test_source_defined_tube_parameterization_is_frozen() -> None:
    """The mesh must retain its 300 by 20 tube structure."""
    tube = load_audit()[
        "tube_parameterization"
    ]

    assert tube["section_count"] == 300
    assert tube["vertices_per_section"] == 20
    assert tube["centreline_station_count"] == 300

    assert math.isclose(
        tube["median_section_radius"],
        5.00128317,
        rel_tol=0.0,
        abs_tol=1.0e-6,
    )

    assert tube["section_radius_cv"] < 0.002
    assert tube["median_planarity_ratio"] < 0.01

    assert math.isclose(
        tube["median_circularity_ratio"],
        1.0026,
        rel_tol=0.0,
        abs_tol=0.002,
    )

    assert math.isclose(
        tube[
            "closure_to_ordinary_median_ratio"
        ],
        0.982391507,
        rel_tol=0.0,
        abs_tol=1.0e-6,
    )


def test_polygonal_centerline_is_embedded() -> None:
    """No nonadjacent polygonal segment intersections may appear."""
    embedding = load_audit()[
        "centerline_embedding"
    ]

    assert (
        embedding[
            "exact_nonadjacent_intersection_count"
        ]
        == 0
    )

    assert (
        embedding[
            "embedded_polygonal_centerline"
        ]
        is True
    )

    assert (
        embedding[
            "minimum_remote_segment_distance"
        ]
        > embedding[
            "median_tube_diameter"
        ]
    )

    assert (
        embedding[
            "remote_clearance_to_diameter_ratio"
        ]
        > 1.4
    )


def test_toroidal_winding_pair_is_three_ten() -> None:
    """The source-defined centreline must retain its 3/-10 winding."""
    toroidal = load_audit()[
        "toroidal_winding"
    ]

    assert toroidal["best_axis"] == "y"
    assert toroidal["signed_winding_pair"] == [
        3,
        -10,
    ]

    assert toroidal["unsigned_winding_pair"] == [
        3,
        10,
    ]

    assert toroidal[
        "matches_unsigned_3_10"
    ] is True

    assert toroidal[
        "major_phase_monotonic"
    ] is True

    assert toroidal[
        "minor_phase_monotonic"
    ] is True

    best_axis = next(
        row
        for row in toroidal[
            "candidate_axes"
        ]
        if row["axis"] == "y"
    )

    assert math.isclose(
        best_axis[
            "major_phase"
        ][
            "total_winding"
        ],
        3.0,
        rel_tol=0.0,
        abs_tol=1.0e-10,
    )

    assert math.isclose(
        best_axis[
            "minor_phase"
        ][
            "total_winding"
        ],
        -10.0,
        rel_tol=0.0,
        abs_tol=1.0e-10,
    )

    assert (
        best_axis[
            "major_phase"
        ][
            "direction_reversal_count"
        ]
        == 0
    )

    assert (
        best_axis[
            "minor_phase"
        ][
            "direction_reversal_count"
        ]
        == 0
    )


def test_fourier_modes_support_three_ten_structure() -> None:
    """The dominant spectra must retain the source winding signature."""
    toroidal = load_audit()[
        "toroidal_winding"
    ]

    transverse = toroidal[
        "dominant_transverse_fourier_modes"
    ]

    axial = toroidal[
        "dominant_axial_fourier_modes"
    ]

    assert transverse[0]["frequency"] == 3

    transverse_frequencies = {
        row["frequency"]
        for row in transverse[:5]
    }

    assert -7 in transverse_frequencies
    assert 13 in transverse_frequencies

    assert abs(
        axial[0]["frequency"]
    ) == 10

    assert {
        row["frequency"]
        for row in axial[:2]
    } == {
        -10,
        10,
    }


def test_report_preserves_the_interpretive_boundary() -> None:
    """The report must not overclaim the unfinished panel comparison."""
    normalized = " ".join(
        REPORT_PATH.read_text(
            encoding="utf-8",
        ).split()
    )

    assert (
        "The published “3,10” designation is therefore "
        "encoded directly in the native geometry"
        in normalized
    )

    assert (
        "This result does not yet identify which complete "
        "model crossings are suppressed in A10_P03."
        in normalized
    )

    assert (
        "Direct model-to-panel comparison is the next stage."
        in normalized
    )
