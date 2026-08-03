"""Synthetic tests for First Hand linear central-projective reconstruction."""

from __future__ import annotations

import importlib.util
import math
import subprocess
import sys
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]

SCRIPT = (
    ROOT
    / "scripts"
    / "audit_first_hand_linear_central_projective_reconstruction.py"
)


def load_module():
    spec = importlib.util.spec_from_file_location(
        "first_hand_linear_central_projective_test",
        SCRIPT,
    )

    if (
        spec is None
        or spec.loader is None
    ):
        raise RuntimeError(
            "Could not load linear reconstruction module."
        )

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


def test_general_sheared_L_is_recovered_exactly() -> None:
    module = load_module()

    L_true = np.asarray(
        [
            [1.20, 0.25],
            [-0.15, 0.85],
        ],
        dtype=float,
    )

    G_true = (
        np.linalg.inv(
            L_true
        ).T
    )

    result = (
        module.reconstruct_linear_map(
            G_true[:, 0],
            G_true[:, 1],
        )
    )

    assert (
        result[
            "inverse_available"
        ]
        is True
    )

    assert np.allclose(
        np.asarray(
            result[
                "G"
            ]
        ),
        G_true,
        atol=1.0e-12,
        rtol=0.0,
    )

    assert np.allclose(
        np.asarray(
            result[
                "L"
            ]
        ),
        L_true,
        atol=1.0e-12,
        rtol=0.0,
    )


def test_parallel_family_validation_is_zero_when_normals_match() -> None:
    module = load_module()

    gx = np.asarray(
        [2.0, 1.0]
    )

    gy = np.asarray(
        [-0.5, 1.5]
    )

    result = (
        module.validation_diagnostics(
            gx,
            gy,
            gx,
            gy,
        )
    )

    assert math.isclose(
        result[
            "eta_x_deg"
        ],
        0.0,
        rel_tol=0.0,
        abs_tol=1.0e-10,
    )

    assert math.isclose(
        result[
            "eta_y_deg"
        ],
        0.0,
        rel_tol=0.0,
        abs_tol=1.0e-10,
    )


def test_validation_is_unoriented_sign_invariant() -> None:
    module = load_module()

    gx = np.asarray(
        [1.0, 2.0]
    )

    gy = np.asarray(
        [3.0, -1.0]
    )

    result = (
        module.validation_diagnostics(
            gx,
            gy,
            -gx,
            -gy,
        )
    )

    assert math.isclose(
        result[
            "eta_x_deg"
        ],
        0.0,
        abs_tol=1.0e-10,
    )

    assert math.isclose(
        result[
            "eta_y_deg"
        ],
        0.0,
        abs_tol=1.0e-10,
    )


def test_orthogonal_dual_vectors_have_90_degree_gamma() -> None:
    module = load_module()

    result = (
        module.validation_diagnostics(
            np.asarray(
                [2.0, 0.0]
            ),
            np.asarray(
                [0.0, 3.0]
            ),
            np.asarray(
                [1.0, 0.0]
            ),
            np.asarray(
                [0.0, 1.0]
            ),
        )
    )

    assert math.isclose(
        result[
            "gamma_G_deg"
        ],
        90.0,
        rel_tol=0.0,
        abs_tol=1.0e-12,
    )

    assert math.isclose(
        result[
            "gamma_G_deviation_from_90_deg"
        ],
        0.0,
        rel_tol=0.0,
        abs_tol=1.0e-12,
    )


def test_isotropic_L_has_unit_singular_value_ratio() -> None:
    module = load_module()

    theta = math.radians(
        23.0
    )

    rotation = np.asarray(
        [
            [
                math.cos(theta),
                -math.sin(theta),
            ],
            [
                math.sin(theta),
                math.cos(theta),
            ],
        ]
    )

    k = 0.75

    L_true = (
        k
        * rotation
    )

    G_true = (
        np.linalg.inv(
            L_true
        ).T
    )

    result = (
        module.reconstruct_linear_map(
            G_true[:, 0],
            G_true[:, 1],
        )
    )

    assert math.isclose(
        result[
            "singular_value_ratio"
        ],
        1.0,
        rel_tol=0.0,
        abs_tol=1.0e-12,
    )


def test_axis_anisotropic_rotated_L_recovers_singular_values() -> None:
    module = load_module()

    theta = math.radians(
        31.0
    )

    rotation = np.asarray(
        [
            [
                math.cos(theta),
                -math.sin(theta),
            ],
            [
                math.sin(theta),
                math.cos(theta),
            ],
        ]
    )

    L_true = (
        rotation
        @ np.diag(
            [
                1.4,
                0.7,
            ]
        )
    )

    G_true = (
        np.linalg.inv(
            L_true
        ).T
    )

    result = (
        module.reconstruct_linear_map(
            G_true[:, 0],
            G_true[:, 1],
        )
    )

    singular = np.asarray(
        result[
            "singular_values_L"
        ]
    )

    assert np.allclose(
        singular,
        np.asarray(
            [
                1.4,
                0.7,
            ]
        ),
        atol=1.0e-12,
        rtol=0.0,
    )

    assert math.isclose(
        result[
            "singular_value_ratio"
        ],
        2.0,
        rel_tol=0.0,
        abs_tol=1.0e-12,
    )


def test_singular_G_is_reported_without_inventing_L() -> None:
    module = load_module()

    result = (
        module.reconstruct_linear_map(
            np.asarray(
                [1.0, 2.0]
            ),
            np.asarray(
                [2.0, 4.0]
            ),
        )
    )

    assert (
        result[
            "inverse_available"
        ]
        is False
    )

    assert (
        result[
            "L"
        ]
        is None
    )


def test_unoriented_angle_known_value() -> None:
    module = load_module()

    angle = (
        module.unoriented_angle_deg(
            np.asarray(
                [1.0, 0.0]
            ),
            np.asarray(
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
            ),
        )
    )

    assert math.isclose(
        angle,
        30.0,
        rel_tol=0.0,
        abs_tol=1.0e-12,
    )


def test_calibration_and_validation_partitions_are_disjoint() -> None:
    module = load_module()

    assert set(
        module.CALIBRATION_CIRCLE_IDS
    ).isdisjoint(
        module.VALIDATION_LINE_IDS
    )

    assert (
        module.HOLDOUT_ID
        not in module.CALIBRATION_CIRCLE_IDS
    )

    assert (
        module.HOLDOUT_ID
        not in module.VALIDATION_LINE_IDS
    )


def test_implementation_contains_no_optimizer() -> None:
    source = SCRIPT.read_text(
        encoding="utf-8",
    )

    assert "scipy.optimize" not in source
    assert "least_squares(" not in source
    assert "minimize(" not in source


def test_direct_cli_import_path() -> None:
    result = subprocess.run(
        [
            sys.executable,
            str(
                SCRIPT
            ),
            "--help",
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, (
        result.stdout
        + "\n"
        + result.stderr
    )

    assert (
        "--check-inputs"
        in result.stdout
    )
