"""Tests for the First Hand spherical reciprocal-spiral shape audit."""

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
    / "audit_first_hand_spherical_reciprocal_spiral_shape.py"
)


def load_module():
    spec = importlib.util.spec_from_file_location(
        "first_hand_reciprocal_shape_test",
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


def test_frozen_frame_constants():
    module = load_module()

    assert module.CENTER_X_PX == pytest.approx(
        1255.1268387556074
    )

    assert module.CENTER_Y_PX == pytest.approx(
        694.602781503521
    )

    assert module.LIMB_RADIUS_PX == pytest.approx(
        341.906449919406
    )


def test_resampling_count_is_401():
    module = load_module()

    assert module.N_RESAMPLE == 401


def test_segment_order_is_frozen():
    module = load_module()

    assert module.SEGMENT_IDS == tuple(
        f"S{i:02d}"
        for i in range(
            1,
            11,
        )
    )


def test_page_coordinate_y_is_up():
    module = load_module()

    points = np.array(
        [
            [
                module.CENTER_X_PX
                + module.LIMB_RADIUS_PX,
                module.CENTER_Y_PX,
            ],
            [
                module.CENTER_X_PX,
                module.CENTER_Y_PX
                - module.LIMB_RADIUS_PX,
            ],
        ],
        dtype=float,
    )

    u, v = module.page_coordinates(
        points
    )

    assert np.allclose(
        u,
        [1.0, 0.0],
    )

    assert np.allclose(
        v,
        [0.0, 1.0],
    )


def test_radial_transform_unit_limb_is_zero():
    module = load_module()

    result = module.radial_transform(
        np.array(
            [1.0]
        )
    )

    assert result[
        0
    ] == pytest.approx(
        0.0
    )


def test_radial_transform_matches_inverse_formula():
    module = load_module()

    rho = np.array(
        [
            0.2,
            0.5,
            0.8,
        ]
    )

    result = module.radial_transform(
        rho
    )

    expected = (
        1.0
        - rho
        * rho
    ) / (
        2.0
        * rho
    )

    assert np.allclose(
        result,
        expected,
    )


def test_radial_transform_refuses_center_point():
    module = load_module()

    with pytest.raises(
        RuntimeError
    ):
        module.radial_transform(
            np.array(
                [0.0]
            )
        )


def test_weighted_linear_fit_recovers_exact_line():
    module = load_module()

    x = np.linspace(
        -2.0,
        4.0,
        101,
    )

    intercept = 1.25
    slope = -1.7

    y = (
        intercept
        + slope
        * x
    )

    weights = np.linspace(
        1.0,
        2.0,
        len(
            x
        ),
    )

    fit = module.weighted_linear_fit(
        x,
        y,
        weights,
    )

    assert fit[
        "intercept_rad"
    ] == pytest.approx(
        intercept,
        abs=1e-12,
    )

    assert fit[
        "slope_signed"
    ] == pytest.approx(
        slope,
        abs=1e-12,
    )

    assert fit[
        "scale_k"
    ] == pytest.approx(
        abs(
            slope
        ),
        abs=1e-12,
    )

    assert fit[
        "handedness"
    ] == -1

    assert fit[
        "weighted_r_squared"
    ] == pytest.approx(
        1.0,
        abs=1e-12,
    )


def test_unwrap_standard_nearest_phase_rule():
    principal = np.array(
        [
            3.0,
            -3.0,
            -2.8,
        ]
    )

    result = np.unwrap(
        principal,
        discont=math.pi,
    )

    assert result[
        1
    ] > result[
        0
    ]

    assert (
        abs(
            result[
                1
            ]
            - result[
                0
            ]
        )
        < math.pi
    )


def test_circular_difference_is_modulo_two_pi():
    module = load_module()

    result = module.circular_difference(
        math.radians(
            1.0
        ),
        math.radians(
            359.0
        ),
    )

    assert math.degrees(
        result
    ) == pytest.approx(
        2.0
    )


def test_weighted_quantile_basic_case():
    module = load_module()

    values = np.array(
        [
            1.0,
            2.0,
            3.0,
            4.0,
        ]
    )

    weights = np.ones(
        4
    )

    assert module.weighted_quantile(
        values,
        weights,
        0.5,
    ) == pytest.approx(
        2.0
    )


def test_chord_formula_small_angle_limit():
    radius = 100.0
    rho = 0.5
    delta = 1e-6

    exact = (
        2.0
        * radius
        * rho
        * abs(
            math.sin(
                delta
                / 2.0
            )
        )
    )

    first_order = (
        radius
        * rho
        * abs(
            delta
        )
    )

    assert exact == pytest.approx(
        first_order,
        rel=1e-10,
    )


def test_no_forbidden_coordinate_scale_tokens():
    source = SCRIPT.read_text(
        encoding="utf-8"
    )

    forbidden = (
        "0.5773502691896257",
        "0.5463024898437905",
        "1.5574077246549023",
        "1.2906912375597608",
        "0.842814100705873",
    )

    for token in forbidden:
        assert token not in source


def test_no_endpoint_theta_constants():
    source = SCRIPT.read_text(
        encoding="utf-8"
    ).lower()

    forbidden = (
        "theta_outer",
        "theta_inner",
        "aog_prose",
        "aog_diagram",
    )

    for token in forbidden:
        assert token not in source


def test_no_optimizer_calls():
    source = SCRIPT.read_text(
        encoding="utf-8"
    ).lower()

    forbidden = (
        "least_squares(",
        "curve_fit(",
        "optimize.minimize",
        "differential_evolution",
    )

    for token in forbidden:
        assert token not in source


def test_no_endpoint_landmark_ids():
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
