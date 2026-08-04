"""Tests for the full translated-isotropic reciprocal-spiral audit."""

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
    / "audit_first_hand_spherical_reciprocal_spiral_translated_isotropic.py"
)


def load_module():
    spec = importlib.util.spec_from_file_location(
        "translated_isotropic_test",
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


def test_frozen_search_bounds():
    module = load_module()

    assert module.PRIMARY_R_TAU_MAX == pytest.approx(
        0.98
    )

    assert module.EXPANDED_R_TAU_MAX == pytest.approx(
        0.995
    )


def test_frozen_optimizer_specification():
    module = load_module()

    assert module.DE_STRATEGY == "best1bin"
    assert module.DE_MAXITER == 300
    assert module.DE_POPSIZE == 15
    assert module.DE_TOL == pytest.approx(1e-10)
    assert module.DE_ATOL == pytest.approx(1e-12)
    assert module.DE_MUTATION == (0.5, 1.0)
    assert module.DE_RECOMBINATION == pytest.approx(0.7)
    assert module.DE_SEED == 20260804
    assert module.DE_UPDATING == "immediate"
    assert module.DE_WORKERS == 1
    assert module.DE_POLISH is True


def test_primary_bound_translation_magnitude():
    module = load_module()

    result = module.tau_polar_to_translation(
        0.98,
        0.0,
    )

    assert result[
        "t_magnitude"
    ] == pytest.approx(
        49.4949494949494,
        rel=1e-12,
    )


def test_expanded_bound_translation_magnitude():
    module = load_module()

    result = module.tau_polar_to_translation(
        0.995,
        0.0,
    )

    assert result[
        "t_magnitude"
    ] == pytest.approx(
        199.498746867168,
        rel=1e-12,
    )


def test_tau_translation_direction():
    module = load_module()

    result = module.tau_polar_to_translation(
        0.4,
        math.pi / 2.0,
    )

    assert result[
        "t_x"
    ] == pytest.approx(
        0.0,
        abs=1e-14,
    )

    assert result[
        "t_y"
    ] > 0.0


def test_stereographic_inverse_roundtrip():
    module = load_module()

    p = np.array(
        [
            [0.1, 0.2],
            [-0.3, 0.15],
            [0.7, -0.1],
        ],
        dtype=float,
    )

    rho2 = np.sum(
        p
        * p,
        axis=1,
    )

    Q = (
        2.0
        * p
        / (
            1.0
            - rho2
        )[
            :,
            None
        ]
    )

    recovered = module.render_construction_plane(
        Q
    )

    assert np.allclose(
        recovered,
        p,
        atol=1e-12,
        rtol=0.0,
    )


def test_profile_exact_linear_relation():
    module = load_module()

    x = np.linspace(
        0.1,
        4.0,
        1000,
    )

    a = 0.7
    m = -1.3

    beta = (
        a
        + m
        * x
    )

    weights = np.linspace(
        0.8,
        1.4,
        len(x),
    )

    result = module.profile_linear_relation(
        x,
        beta,
        weights,
    )

    assert result is not None

    assert result[
        "a"
    ] == pytest.approx(
        a,
        abs=1e-12,
    )

    assert result[
        "m"
    ] == pytest.approx(
        m,
        abs=1e-12,
    )

    assert result[
        "objective"
    ] == pytest.approx(
        0.0,
        abs=1e-20,
    )

    assert result[
        "weighted_r_squared"
    ] == pytest.approx(
        1.0,
        abs=1e-12,
    )


def test_exact_synthetic_translated_reciprocal_spiral():
    module = load_module()

    theta = np.linspace(
        10.0,
        1.0,
        1200,
    )

    k = 0.82
    alpha0 = 0.43

    t = np.array(
        [
            0.31,
            -0.19,
        ]
    )

    W = (
        k
        / theta
    )[
        :,
        None
    ] * np.column_stack(
        (
            np.cos(
                alpha0
                + theta
            ),
            np.sin(
                alpha0
                + theta
            ),
        )
    )

    Q = (
        t[
            None,
            :
        ]
        + W
    )

    p = module.render_construction_plane(
        Q
    )

    weights = np.ones(
        len(theta)
    )

    result = module.evaluate_translation_plane(
        Q,
        p,
        weights,
        t,
        341.906449919406,
    )

    assert result is not None

    assert result[
        "objective"
    ] == pytest.approx(
        0.0,
        abs=1e-18,
    )

    assert result[
        "m"
    ] == pytest.approx(
        k,
        abs=1e-10,
    )

    assert result[
        "page_distance_px"
    ].max() == pytest.approx(
        0.0,
        abs=1e-9,
    )


def test_true_translation_beats_centered_on_synthetic_spiral():
    module = load_module()

    theta = np.linspace(
        9.0,
        1.2,
        900,
    )

    k = 0.7
    alpha0 = -0.2

    t = np.array(
        [
            0.4,
            0.25,
        ]
    )

    Q = (
        t[
            None,
            :
        ]
        + (
            k
            / theta
        )[
            :,
            None
        ]
        * np.column_stack(
            (
                np.cos(
                    alpha0
                    + theta
                ),
                np.sin(
                    alpha0
                    + theta
                ),
            )
        )
    )

    p = module.render_construction_plane(
        Q
    )

    weights = np.ones(
        len(theta)
    )

    correct = module.evaluate_translation_plane(
        Q,
        p,
        weights,
        t,
        341.906449919406,
    )

    centered = module.evaluate_translation_plane(
        Q,
        p,
        weights,
        np.zeros(
            2
        ),
        341.906449919406,
    )

    assert correct is not None
    assert centered is not None

    assert (
        correct[
            "objective"
        ]
        < centered[
            "objective"
        ]
    )


def test_page_distance_zero_for_identical_points():
    module = load_module()

    Q = np.array(
        [
            [0.2, -0.1],
            [1.0, 0.5],
        ]
    )

    p = module.render_construction_plane(
        Q
    )

    assert np.max(
        np.linalg.norm(
            module.render_construction_plane(
                Q
            )
            - p,
            axis=1,
        )
    ) == pytest.approx(
        0.0
    )


def test_relative_difference_identical_is_zero():
    module = load_module()

    assert module.relative_difference(
        2.0,
        2.0,
    ) == pytest.approx(
        0.0
    )


def test_circular_difference_wraps():
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


def test_boundary_tolerance_is_frozen():
    module = load_module()

    assert module.BOUNDARY_TOL == pytest.approx(
        1e-8
    )


def test_three_pi_holdout_constant():
    module = load_module()

    assert math.degrees(
        module.THREE_PI
    ) == pytest.approx(
        540.0
    )


def test_no_first_order_signature_result_dependency():
    source = SCRIPT.read_text(
        encoding="utf-8"
    ).lower()

    forbidden = (
        "translation_signature.json",
        "translation_signature_radial.csv",
        "c_x:",
        "306.727",
        "308.203",
        "0.255314",
        "0.281697",
    )

    for token in forbidden:
        assert token not in source


def test_no_coordinate_landmark_dependencies():
    source = SCRIPT.read_text(
        encoding="utf-8"
    )

    forbidden = (
        "AOG-LM-P07-GC-Y0",
        "AOG-LM-P07-GC-Y1",
        "AOG-LM-P07-GC-X1",
        "AOG-LM-P07-GC-YAXIS",
    )

    for token in forbidden:
        assert token not in source


def test_no_endpoint_landmark_dependencies():
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


def test_no_source_endpoint_branch_constants():
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
