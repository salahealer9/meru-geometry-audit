"""Tests for the First Hand first-order translation-signature audit."""

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
    / "audit_first_hand_spherical_reciprocal_spiral_translation_signature.py"
)


def load_module():
    spec = importlib.util.spec_from_file_location(
        "translation_signature_test",
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


def test_frozen_dimensions():
    module = load_module()

    assert module.N_RESAMPLE == 401
    assert module.N_SEGMENTS == 10
    assert module.N_PER_PASS == 4010


def test_radial_partition_is_ten_fixed_bins():
    module = load_module()

    assert len(
        module.RADIAL_EDGES
    ) == 11

    assert np.allclose(
        np.diff(
            module.RADIAL_EDGES
        ),
        0.1,
    )


def test_phase_partition_is_36_ten_degree_bins():
    module = load_module()

    assert len(
        module.PHASE_EDGES
    ) == 37

    assert math.degrees(
        module.PHASE_EDGES[1]
        - module.PHASE_EDGES[0]
    ) == pytest.approx(
        10.0
    )


def test_translation_basis_formula():
    module = load_module()

    F = np.array(
        [
            0.5,
            1.0,
        ]
    )

    beta = np.array(
        [
            0.0,
            math.pi / 2.0,
        ]
    )

    weights = np.ones(
        2
    )

    # Direct raw basis expected before orthogonalization:
    raw = np.column_stack(
        (
            -F
            * np.sin(
                beta
            ),
            F
            * np.cos(
                beta
            ),
        )
    )

    assert np.allclose(
        raw,
        [
            [0.0, 0.5],
            [-1.0, 0.0],
        ],
    )


def test_orthogonalized_basis_is_weight_orthogonal_to_parent():
    module = load_module()

    F = np.linspace(
        0.1,
        2.0,
        200,
    )

    beta = np.linspace(
        0.0,
        5.0 * math.pi,
        200,
    )

    weights = np.linspace(
        1.0,
        2.0,
        200,
    )

    G_perp, _ = (
        module.orthogonalize_translation_basis(
            F,
            beta,
            weights,
        )
    )

    X0 = np.column_stack(
        (
            np.ones_like(
                F
            ),
            F,
        )
    )

    cross = (
        X0.T
        @ (
            weights[:, None]
            * G_perp
        )
    )

    assert np.max(
        np.abs(
            cross
        )
    ) < 1e-10


def test_exact_synthetic_signature_recovery():
    module = load_module()

    F = np.linspace(
        0.15,
        2.5,
        1000,
    )

    beta = np.linspace(
        -4.0 * math.pi,
        4.0 * math.pi,
        1000,
    )

    weights = np.linspace(
        0.7,
        1.5,
        1000,
    )

    G_perp, _ = (
        module.orthogonalize_translation_basis(
            F,
            beta,
            weights,
        )
    )

    true_c = np.array(
        [
            0.24,
            -0.17,
        ]
    )

    residual = (
        G_perp
        @ true_c
    )

    rows = []

    for i in range(
        len(F)
    ):
        rows.append(
            {
                "F_rho": float(
                    F[i]
                ),
                "beta_hat": float(
                    beta[i]
                ),
                "residual": float(
                    residual[i]
                ),
                "weight_length": float(
                    weights[i]
                ),
            }
        )

    fit = module.translation_signature_fit(
        rows,
        "weight_length",
    )

    assert fit[
        "c_x"
    ] == pytest.approx(
        true_c[0],
        abs=1e-11,
    )

    assert fit[
        "c_y"
    ] == pytest.approx(
        true_c[1],
        abs=1e-11,
    )

    assert fit[
        "fraction_parent_sse_explained"
    ] == pytest.approx(
        1.0,
        abs=1e-11,
    )


def test_phase_coverage_full_circle():
    module = load_module()

    phases = np.linspace(
        0.0,
        2.0 * math.pi,
        360,
        endpoint=False,
    )

    coverage, largest_gap = (
        module.phase_coverage(
            phases
        )
    )

    assert math.degrees(
        largest_gap
    ) == pytest.approx(
        1.0,
        abs=1e-10,
    )

    assert math.degrees(
        coverage
    ) == pytest.approx(
        359.0,
        abs=1e-10,
    )


def test_phase_coverage_narrow_arc():
    module = load_module()

    phases = np.radians(
        np.linspace(
            10.0,
            70.0,
            100,
        )
    )

    coverage, _ = (
        module.phase_coverage(
            phases
        )
    )

    assert math.degrees(
        coverage
    ) == pytest.approx(
        60.0,
        abs=1e-10,
    )


def test_exact_harmonic_amplitude_and_phase():
    module = load_module()

    phases = np.linspace(
        0.0,
        2.0 * math.pi,
        720,
        endpoint=False,
    )

    amplitude = 0.4
    phase_axis = 1.1
    dc = -0.07

    residual = (
        dc
        + amplitude
        * np.cos(
            phases
            - phase_axis
        )
    )

    rows = []

    for i, phase in enumerate(
        phases
    ):
        rows.append(
            {
                "beta_hat": float(
                    phase
                ),
                "residual": float(
                    residual[i]
                ),
                "weight_length": 1.0,
                "F_rho": 0.8,
            }
        )

    fit = module.harmonic_band_fit(
        rows
    )

    assert fit[
        "eligible"
    ]

    assert fit[
        "amplitude_rad"
    ] == pytest.approx(
        amplitude,
        abs=1e-11,
    )

    assert fit[
        "phase_axis_rad"
    ] == pytest.approx(
        phase_axis,
        abs=1e-11,
    )

    assert fit[
        "c0_rad"
    ] == pytest.approx(
        dc,
        abs=1e-11,
    )


def test_narrow_phase_band_is_ineligible():
    module = load_module()

    phases = np.radians(
        np.linspace(
            20.0,
            80.0,
            100,
        )
    )

    rows = []

    for phase in phases:
        rows.append(
            {
                "beta_hat": float(
                    phase
                ),
                "residual": 0.1,
                "weight_length": 1.0,
                "F_rho": 0.5,
            }
        )

    fit = module.harmonic_band_fit(
        rows
    )

    assert not fit[
        "eligible"
    ]

    assert (
        fit[
            "status"
        ]
        == "INSUFFICIENT_PHASE_COVERAGE"
    )


def test_last_radial_edge_maps_to_last_bin():
    module = load_module()

    assert module.radial_bin_index(
        1.0
    ) == 9


def test_internal_radial_edge_maps_right():
    module = load_module()

    assert module.radial_bin_index(
        0.1
    ) == 1


def test_phase_wrap_maps_to_first_bin():
    module = load_module()

    assert module.phase_bin_index(
        2.0
        * math.pi
    ) == 0


def test_circular_difference_wraps_correctly():
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


def test_no_nonlinear_optimizer():
    source = SCRIPT.read_text(
        encoding="utf-8"
    ).lower()

    forbidden = (
        "differential_evolution",
        "least_squares(",
        "curve_fit(",
        "minimize(",
        "optimize.",
    )

    for token in forbidden:
        assert token not in source


def test_no_raw_digitization_inputs():
    source = SCRIPT.read_text(
        encoding="utf-8"
    )

    assert (
        "spherical_spiral_segments_pass1.csv"
        not in source
    )

    assert (
        "spherical_spiral_segments_pass2.csv"
        not in source
    )


def test_no_coordinate_landmark_inputs():
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
