"""Tests for the First Hand spherical-spiral endpoint-consistency audit."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import numpy as np
import pytest


ROOT = Path(__file__).resolve().parents[1]

SCRIPT = (
    ROOT
    / "scripts"
    / "audit_first_hand_spherical_spiral_endpoint_consistency.py"
)


def load_module():
    spec = importlib.util.spec_from_file_location(
        "first_hand_spiral_endpoint_test",
        SCRIPT,
    )

    assert spec is not None
    assert spec.loader is not None

    module = (
        importlib.util.module_from_spec(
            spec
        )
    )

    sys.modules[
        spec.name
    ] = module

    spec.loader.exec_module(
        module
    )

    return module


def synthetic_rows():
    return [
        {
            "segment_id": "S10",
            "sequence_index": "2",
            "x_px": "20",
            "y_px": "30",
            "local_stroke_width_px": "14",
        },
        {
            "segment_id": "S01",
            "sequence_index": "1",
            "x_px": "2",
            "y_px": "3",
            "local_stroke_width_px": "14",
        },
        {
            "segment_id": "S10",
            "sequence_index": "0",
            "x_px": "18",
            "y_px": "28",
            "local_stroke_width_px": "14",
        },
        {
            "segment_id": "S01",
            "sequence_index": "0",
            "x_px": "1",
            "y_px": "2",
            "local_stroke_width_px": "14",
        },
        {
            "segment_id": "S10",
            "sequence_index": "1",
            "x_px": "19",
            "y_px": "29",
            "local_stroke_width_px": "14",
        },
    ]


def test_euclidean_distance_three_four_five():
    module = load_module()

    assert module.euclidean_distance(
        np.array(
            [0.0, 0.0]
        ),
        np.array(
            [3.0, 4.0]
        ),
    ) == pytest.approx(
        5.0
    )


def test_mean_point():
    module = load_module()

    result = module.mean_point(
        np.array(
            [2.0, 4.0]
        ),
        np.array(
            [6.0, 10.0]
        ),
    )

    assert np.allclose(
        result,
        np.array(
            [4.0, 7.0]
        ),
    )


def test_endpoint_selection_uses_first_s01_and_last_s10():
    module = load_module()

    selected = (
        module.selected_endpoint_rows(
            synthetic_rows()
        )
    )

    assert selected[
        "inner"
    ][
        "segment_id"
    ] == "S01"

    assert selected[
        "inner"
    ][
        "sequence_index"
    ] == "0"

    assert selected[
        "outer"
    ][
        "segment_id"
    ] == "S10"

    assert selected[
        "outer"
    ][
        "sequence_index"
    ] == "2"


def test_spiral_source_scale_for_14px_stroke_is_7px():
    module = load_module()

    row = {
        "local_stroke_width_px": "14"
    }

    assert module.spiral_source_scale(
        row
    ) == pytest.approx(
        7.0
    )


def test_spiral_source_scale_has_2px_floor():
    module = load_module()

    row = {
        "local_stroke_width_px": "1"
    }

    assert module.spiral_source_scale(
        row
    ) == pytest.approx(
        2.0
    )


def test_landmark_ids_are_frozen():
    module = load_module()

    assert module.INNER_ID == (
        "AOG-LM-P07-SPHERE-INNER-END"
    )

    assert module.OUTER_ID == (
        "AOG-LM-P07-RIM-NODE-LR-SHARED"
    )


def test_consensus_schema_is_exact():
    module = load_module()

    assert module.EXPECTED_CONSENSUS_FIELDS == [
        "landmark_id",
        "source_feature",
        "fit_partition",
        "pass1_x_px",
        "pass1_y_px",
        "pass2_x_px",
        "pass2_y_px",
        "consensus_x_px",
        "consensus_y_px",
        "pass_separation_px",
        "pass1_stroke_width_px",
        "pass2_stroke_width_px",
        "uncertainty_floor_px",
        "consensus_uncertainty_px",
        "crop_file_sha256",
        "crop_pixel_sha256",
    ]


def test_no_fit_or_registration_calls():
    source = SCRIPT.read_text(
        encoding="utf-8"
    ).lower()

    forbidden = (
        "least_squares(",
        "curve_fit(",
        "optimize.minimize",
        "procrustes(",
        "iterativeclosestpoint",
    )

    for token in forbidden:
        assert token not in source


def test_no_theoretical_endpoint_parameter_is_used():
    source = SCRIPT.read_text(
        encoding="utf-8"
    ).lower()

    forbidden = (
        "3 * math.pi",
        "3*np.pi",
        "3 * np.pi",
        "1 + 3",
    )

    for token in forbidden:
        assert token not in source


def test_limb_radius_is_frozen():
    module = load_module()

    assert module.LIMB_RADIUS_PX == pytest.approx(
        341.906449919
    )
