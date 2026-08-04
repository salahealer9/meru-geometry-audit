"""Tests for the First Hand spherical-spiral reproducibility audit."""

from __future__ import annotations

import importlib.util
import math
import sys
from pathlib import Path

import numpy as np
import pytest


ROOT = Path(__file__).resolve().parents[1]

SCRIPT = (
    ROOT
    / "scripts"
    / "audit_first_hand_spherical_spiral_reproducibility.py"
)


def load_module():
    spec = importlib.util.spec_from_file_location(
        "first_hand_spiral_repro_test",
        SCRIPT,
    )

    assert spec is not None
    assert spec.loader is not None

    module = importlib.util.module_from_spec(
        spec
    )

    sys.modules[
        spec.name
    ] = module

    spec.loader.exec_module(
        module
    )

    return module


def test_fixed_resample_count():
    module = load_module()

    points = np.array(
        [
            [0.0, 0.0],
            [10.0, 0.0],
        ]
    )

    result = module.resample_polyline(
        points
    )

    assert result.shape == (
        module.N_RESAMPLE,
        2,
    )

    assert np.allclose(
        result[0],
        points[0],
    )

    assert np.allclose(
        result[-1],
        points[-1],
    )


def test_identical_polyline_has_zero_distance():
    module = load_module()

    points = np.array(
        [
            [0.0, 0.0],
            [5.0, 2.0],
            [10.0, 0.0],
        ]
    )

    distances, _, _ = (
        module.symmetric_distance_sample(
            points,
            points,
        )
    )

    assert np.max(
        distances
    ) == pytest.approx(
        0.0,
        abs=1e-12,
    )


def test_parallel_translation_distance():
    module = load_module()

    a = np.array(
        [
            [0.0, 0.0],
            [10.0, 0.0],
        ]
    )

    b = np.array(
        [
            [0.0, 3.0],
            [10.0, 3.0],
        ]
    )

    distances, _, _ = (
        module.symmetric_distance_sample(
            a,
            b,
        )
    )

    assert np.median(
        distances
    ) == pytest.approx(
        3.0,
        abs=1e-10,
    )

    assert math.sqrt(
        np.mean(
            distances
            * distances
        )
    ) == pytest.approx(
        3.0,
        abs=1e-10,
    )


def test_direction_reversal_invariance():
    module = load_module()

    a = np.array(
        [
            [0.0, 0.0],
            [5.0, 3.0],
            [10.0, 1.0],
        ]
    )

    b = a[
        ::-1
    ].copy()

    distances, _, _ = (
        module.symmetric_distance_sample(
            a,
            b,
        )
    )

    assert np.max(
        distances
    ) == pytest.approx(
        0.0,
        abs=1e-10,
    )


def test_click_density_does_not_change_same_line():
    module = load_module()

    sparse = np.array(
        [
            [0.0, 0.0],
            [10.0, 0.0],
        ]
    )

    dense = np.array(
        [
            [0.0, 0.0],
            [1.0, 0.0],
            [2.0, 0.0],
            [4.0, 0.0],
            [7.0, 0.0],
            [10.0, 0.0],
        ]
    )

    distances, _, _ = (
        module.symmetric_distance_sample(
            sparse,
            dense,
        )
    )

    assert np.max(
        distances
    ) == pytest.approx(
        0.0,
        abs=1e-10,
    )


def test_point_to_segment_uses_orthogonal_projection():
    module = load_module()

    query = np.array(
        [
            [5.0, 4.0],
        ]
    )

    line = np.array(
        [
            [0.0, 0.0],
            [10.0, 0.0],
        ]
    )

    distance = (
        module.point_to_polyline_distances(
            query,
            line,
        )
    )

    assert distance[0] == pytest.approx(
        4.0
    )


def test_equal_segment_aggregate_formula():
    module = load_module()

    results = [
        {
            "mean_polyline_length_px": 10.0,
            "distance": {
                "mse_px2": 4.0,
                "median_px": 2.0,
                "p95_px": 2.0,
            },
        },
        {
            "mean_polyline_length_px": 10.0,
            "distance": {
                "mse_px2": 16.0,
                "median_px": 4.0,
                "p95_px": 4.0,
            },
        },
    ]

    aggregate = (
        module.aggregate_rms(
            results
        )
    )

    assert aggregate[
        "rms_equal_segment_px"
    ] == pytest.approx(
        math.sqrt(
            10.0
        )
    )


def test_length_weighted_aggregate_formula():
    module = load_module()

    results = [
        {
            "mean_polyline_length_px": 1.0,
            "distance": {
                "mse_px2": 1.0,
                "median_px": 1.0,
                "p95_px": 1.0,
            },
        },
        {
            "mean_polyline_length_px": 3.0,
            "distance": {
                "mse_px2": 9.0,
                "median_px": 3.0,
                "p95_px": 3.0,
            },
        },
    ]

    aggregate = (
        module.aggregate_rms(
            results
        )
    )

    expected = math.sqrt(
        (
            1.0 * 1.0
            + 3.0 * 9.0
        )
        / 4.0
    )

    assert aggregate[
        "rms_length_weighted_px"
    ] == pytest.approx(
        expected
    )


def test_frozen_correspondence_has_ten_identity_pairs():
    module = load_module()

    assert len(
        module.PAIRINGS
    ) == 10

    assert module.PAIRINGS == tuple(
        (
            f"S{i:02d}",
            f"S{i:02d}",
        )
        for i in range(
            1,
            11,
        )
    )


def test_endpoint_holdout_ids_are_not_loaded():
    source = SCRIPT.read_text(
        encoding="utf-8"
    )

    assert (
        "AOG-LM-P07-SPHERE-INNER-END"
        not in source
    )

    assert (
        "AOG-LM-P07-RIM-NODE-LR-SHARED"
        not in source
    )


def test_no_registration_or_theoretical_fit_calls():
    source = SCRIPT.read_text(
        encoding="utf-8"
    ).lower()

    forbidden = (
        "procrustes(",
        "iterativeclosestpoint",
        "optimize.minimize",
        "least_squares(",
        "curve_fit(",
    )

    for token in forbidden:
        assert token not in source


def test_resample_constant_is_401():
    module = load_module()

    assert (
        module.N_RESAMPLE
        == 401
    )
