"""Tests for the expanded First Hand neutral geometry census."""

from __future__ import annotations

import importlib.util
import math
import sys
from pathlib import Path
from typing import Any

import numpy as np


ROOT = Path(__file__).resolve().parents[1]

SCRIPT_PATH = (
    ROOT
    / "scripts"
    / "audit_first_hand_expanded_neutral_geometry.py"
)


def load_module() -> Any:
    """Load the expanded census without running its CLI."""
    spec = importlib.util.spec_from_file_location(
        "first_hand_expanded_neutral_geometry",
        SCRIPT_PATH,
    )

    assert spec is not None
    assert spec.loader is not None

    module = importlib.util.module_from_spec(
        spec
    )
    sys.modules[
        spec.name
    ] = module

    try:
        spec.loader.exec_module(
            module
        )
    finally:
        sys.modules.pop(
            spec.name,
            None,
        )

    return module


def test_addendum_checksum_manifest_verifies() -> None:
    """Both frozen addendum passes must match their manifest."""
    module = load_module()

    entries = module.verify_checksum_manifest(
        module.ADDENDUM_CHECKSUM_PATH,
        {
            module.ADDENDUM_PASS_PATHS[1].name,
            module.ADDENDUM_PASS_PATHS[2].name,
        },
    )

    assert set(entries) == {
        "diagram_incidence_addendum_pass1.csv",
        "diagram_incidence_addendum_pass2.csv",
    }


def test_addendum_passes_have_exact_three_point_vocabulary() -> None:
    """Each pass must contain the same three unique point IDs."""
    module = load_module()

    for pass_number, path in module.ADDENDUM_PASS_PATHS.items():
        rows = module.validate_addendum_pass(
            pass_number,
            path,
        )

        assert len(rows) == 3
        assert {
            row["landmark_id"]
            for row in rows
        } == set(
            module.ADDENDUM_IDS
        )


def test_angle_function_recovers_thirty_degrees() -> None:
    """The node-angle implementation must recover a known geometry."""
    module = load_module()

    vertex = np.asarray(
        [0.0, 0.0]
    )
    first = np.asarray(
        [1.0, 0.0]
    )
    second = np.asarray(
        [
            math.cos(
                math.radians(
                    30.0
                )
            ),
            math.sin(
                math.radians(
                    30.0
                )
            ),
        ]
    )

    assert abs(
        module.angle_deg(
            first,
            vertex,
            second,
        )
        - 30.0
    ) < 1.0e-12


def test_point_line_distance_recovers_known_offset() -> None:
    """The two-node line diagnostic must use Euclidean distance."""
    module = load_module()

    distance = module.point_line_distance(
        np.asarray(
            [0.0, 5.0]
        ),
        np.asarray(
            [-3.0, 0.0]
        ),
        np.asarray(
            [7.0, 0.0]
        ),
    )

    assert abs(
        distance - 5.0
    ) < 1.0e-12


def test_addendum_consensus_applies_protocol_uncertainty() -> None:
    """Consensus must use floor, node width, and pass separation."""
    module = load_module()

    pass1 = []
    pass2 = []

    for index, landmark_id in enumerate(
        module.ADDENDUM_IDS
    ):
        common = {
            "crop_id": "CROP",
            "crop_file_sha256": "a" * 64,
            "crop_pixel_sha256": "b" * 64,
            "landmark_id": landmark_id,
            "operator": "Test Operator",
            "sequence_index": "0",
            "local_stroke_width_px": "6",
            "object_type": "point",
            "fit_partition": "calibration",
            "source_feature": "feature",
            "operator_note": "",
            "timestamp_utc": "2026-07-31T00:00:00Z",
        }

        pass1.append(
            {
                **common,
                "pass_number": "1",
                "x_px": str(
                    float(index)
                ),
                "y_px": "0",
            }
        )
        pass2.append(
            {
                **common,
                "pass_number": "2",
                "x_px": str(
                    float(index) + 8.0
                ),
                "y_px": "0",
            }
        )

    consensus = module.build_addendum_consensus(
        pass1,
        pass2,
    )

    assert len(consensus) == 3

    for row in consensus:
        assert (
            float(
                row[
                    "pass_separation_px"
                ]
            )
            == 8.0
        )
        assert (
            float(
                row[
                    "consensus_uncertainty_px"
                ]
            )
            == 4.0
        )


def test_expanded_analysis_contains_fifteen_points() -> None:
    """Twelve original points plus three addendum points must survive."""
    module = load_module()

    analysis, rows, coordinates = (
        module.build_expanded_analysis()
    )

    assert len(rows) == 15
    assert len(coordinates) == 15

    assert analysis[
        "provenance"
    ][
        "original_neutral_point_count"
    ] == 12

    assert analysis[
        "provenance"
    ][
        "incidence_addendum_point_count"
    ] == 3

    assert analysis[
        "provenance"
    ][
        "expanded_point_count"
    ] == 15


def test_expanded_analysis_retains_interpretation_boundary() -> None:
    """The new angle must not silently become a map verdict."""
    module = load_module()

    analysis, _, _ = (
        module.build_expanded_analysis()
    )

    diagnostic = analysis[
        "incidence_addendum"
    ][
        "node_defined_thirty_degree_diagnostic"
    ]

    assert math.isfinite(
        diagnostic[
            "angle_deg"
        ]
    )
    assert math.isfinite(
        diagnostic[
            "linearized_coordinate_sensitivity_deg"
        ]
    )

    assert (
        "does not assume an angle-preserving projective map"
        in diagnostic[
            "interpretation_boundary"
        ]
    )

    assert (
        "No great-circle, projective-map, unit-angle, "
        "truncation, or self-embedment verdict"
        in analysis[
            "verdict"
        ]
    )


def test_script_declares_expanded_source_only_scope() -> None:
    """The implementation must state every downstream exclusion."""
    text = " ".join(
        SCRIPT_PATH.read_text(
            encoding="utf-8",
        )
        .lower()
        .split()
    )

    assert "does not fit any great-circle trace" in text
    assert "infer hidden curve segments" in text
    assert "select a projective map" in text
    assert "choose a unit convention" in text
    assert "reconcile truncations" in text
    assert "compute s1, s1.5, or s2" in text


def test_overlay_renders_from_verified_prepared_crop(
    tmp_path: Path,
) -> None:
    """The full overlay path must use the verified crop manifest."""
    module = load_module()

    analysis, rows, _ = (
        module.build_expanded_analysis()
    )

    output_path = (
        tmp_path
        / "expanded_neutral_overlay.png"
    )

    module.write_overlay(
        output_path,
        analysis,
        rows,
    )

    assert output_path.is_file()
    assert output_path.stat().st_size > 1000

