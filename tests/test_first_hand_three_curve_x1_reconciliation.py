"""Synthetic tests for three-curve X1 reconciliation."""

from __future__ import annotations

import importlib.util
import math
import sys
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]

SCRIPT = (
    ROOT
    / "scripts"
    / "audit_first_hand_three_curve_x1_reconciliation.py"
)


def load_module():
    spec = importlib.util.spec_from_file_location(
        "first_hand_three_curve_x1_reconciliation_test",
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


def test_unoriented_plane_angle_ignores_normal_sign():
    module = load_module()

    a = np.asarray(
        [1.0, 2.0, 3.0]
    )

    assert math.isclose(
        module.stable_unoriented_plane_angle_deg(
            a,
            -a,
        ),
        0.0,
        abs_tol=1.0e-12,
    )


def test_isotropic_candidate_has_two_opposite_centres():
    module = load_module()

    result = module.isotropic_candidates(
        np.asarray(
            [3.0, 4.0]
        ),
        np.asarray(
            [1.0, 0.0, 0.0]
        ),
    )

    plus = np.asarray(
        result[
            "branches"
        ][
            "plus_frozen_yaxis_normal"
        ][
            "g_x"
        ]
    )

    minus = np.asarray(
        result[
            "branches"
        ][
            "minus_frozen_yaxis_normal"
        ][
            "g_x"
        ]
    )

    assert np.allclose(
        plus,
        -minus,
        atol=1.0e-12,
    )

    assert math.isclose(
        result["r_y"],
        5.0,
        abs_tol=1.0e-12,
    )

    assert math.isclose(
        result["k_y"],
        0.2,
        abs_tol=1.0e-12,
    )


def test_isotropic_constructor_does_not_take_x1_input():
    module = load_module()

    names = (
        module.isotropic_candidates
        .__code__
        .co_varnames[
            :
            module.isotropic_candidates
            .__code__
            .co_argcount
        ]
    )

    assert names == (
        "y1_center",
        "yaxis_plane_normal",
    )


def test_analytic_interior_optimum_matches_dense_search():
    module = load_module()

    u = np.asarray(
        [1.0, 0.0]
    )

    observed = module.unit_vector(
        np.asarray(
            [-0.6, 0.3, 0.7]
        )
    )

    analytic = (
        module.analytic_anisotropic_branch(
            observed,
            u,
            +1,
        )
    )

    assert (
        analytic[
            "optimum_class"
        ]
        == "FINITE_INTERIOR"
    )

    log_r = np.linspace(
        -6.0,
        6.0,
        20001,
    )

    brute = []

    for value in log_r:
        r = 10.0 ** float(value)

        predicted = (
            module.predicted_plane_normal_from_g(
                r * u
            )
        )

        brute.append(
            module.stable_unoriented_plane_angle_deg(
                predicted,
                observed,
            )
        )

    assert math.isclose(
        analytic[
            "minimum_x1_plane_angle_residual_deg"
        ],
        min(brute),
        abs_tol=2.0e-3,
    )


def test_boundary_zero_optimum():
    module = load_module()

    # A and B have opposite signs and |B| > |A|.
    observed = module.unit_vector(
        np.asarray(
            [0.1, 0.0, 0.99]
        )
    )

    result = (
        module.analytic_anisotropic_branch(
            observed,
            np.asarray(
                [1.0, 0.0]
            ),
            +1,
        )
    )

    assert (
        result[
            "optimum_class"
        ]
        == "LIMIT_R_TO_ZERO"
    )

    assert (
        result[
            "optimal_r_x"
        ]
        is None
    )


def test_boundary_infinity_optimum():
    module = load_module()

    # Opposite-sign A/B with stronger horizontal correlation.
    observed = module.unit_vector(
        np.asarray(
            [0.99, 0.0, 0.1]
        )
    )

    result = (
        module.analytic_anisotropic_branch(
            observed,
            np.asarray(
                [1.0, 0.0]
            ),
            +1,
        )
    )

    assert (
        result[
            "optimum_class"
        ]
        == "LIMIT_R_TO_INFINITY"
    )


def test_observed_plane_sign_flip_preserves_analytic_result():
    module = load_module()

    observed = module.unit_vector(
        np.asarray(
            [-0.4, 0.2, 0.8]
        )
    )

    first = (
        module.analytic_anisotropic_branch(
            observed,
            np.asarray(
                [1.0, 0.0]
            ),
            +1,
        )
    )

    second = (
        module.analytic_anisotropic_branch(
            -observed,
            np.asarray(
                [1.0, 0.0]
            ),
            +1,
        )
    )

    assert (
        first[
            "optimum_class"
        ]
        == second[
            "optimum_class"
        ]
    )

    assert math.isclose(
        first[
            "minimum_x1_plane_angle_residual_deg"
        ],
        second[
            "minimum_x1_plane_angle_residual_deg"
        ],
        abs_tol=1.0e-12,
    )


def test_reversing_yaxis_normal_swaps_sign_branches():
    module = load_module()

    y1 = np.asarray(
        [2.0, 0.0]
    )

    first = module.isotropic_candidates(
        y1,
        np.asarray(
            [1.0, 0.0, 0.0]
        ),
    )

    second = module.isotropic_candidates(
        y1,
        np.asarray(
            [-1.0, 0.0, 0.0]
        ),
    )

    first_plus = np.asarray(
        first[
            "branches"
        ][
            "plus_frozen_yaxis_normal"
        ][
            "g_x"
        ]
    )

    second_minus = np.asarray(
        second[
            "branches"
        ][
            "minus_frozen_yaxis_normal"
        ][
            "g_x"
        ]
    )

    assert np.allclose(
        first_plus,
        second_minus,
        atol=1.0e-12,
    )


def test_sweep_has_fixed_preregistered_size():
    module = load_module()

    q = np.linspace(
        module.SWEEP_LOG10_K_MIN,
        module.SWEEP_LOG10_K_MAX,
        module.SWEEP_POINTS,
    )

    assert len(q) == 1201

    assert math.isclose(
        q[0],
        -3.0,
        abs_tol=1.0e-12,
    )

    assert math.isclose(
        q[-1],
        3.0,
        abs_tol=1.0e-12,
    )


def test_sweep_agrees_with_direct_isotropic_point():
    module = load_module()

    observed = module.unit_vector(
        np.asarray(
            [-0.2, 0.5, 0.8]
        )
    )

    u = np.asarray(
        [0.6, 0.8]
    )

    k = 0.75

    sweep = (
        module.sweep_branch_angles(
            observed,
            u,
            +1,
            np.asarray(
                [math.log10(k)]
            ),
        )
    )

    g = (
        (1.0 / k)
        * module.unit_vector(u)
    )

    direct = (
        module.stable_unoriented_plane_angle_deg(
            module.predicted_plane_normal_from_g(
                g
            ),
            observed,
        )
    )

    assert math.isclose(
        float(sweep[0]),
        direct,
        abs_tol=1.0e-12,
    )


def test_implementation_contains_no_optimizer():
    source = SCRIPT.read_text(
        encoding="utf-8",
    )

    assert "scipy.optimize" not in source
    assert "least_squares(" not in source
    assert "minimize(" not in source


def test_protocol_scope_does_not_use_scaffold_for_fit():
    source = SCRIPT.read_text(
        encoding="utf-8",
    )

    assert '"scaffold_used": False' in source
    assert '"x1_reclassified_as_scaffold": False' in source
