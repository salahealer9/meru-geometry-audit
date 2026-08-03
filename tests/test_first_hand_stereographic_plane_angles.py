"""Synthetic tests for stereographic First Hand spherical-plane reconstruction."""

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
    / "audit_first_hand_stereographic_plane_angles.py"
)


def load_module():
    spec = importlib.util.spec_from_file_location(
        "first_hand_stereographic_plane_angles_test",
        SCRIPT,
    )

    if (
        spec is None
        or spec.loader is None
    ):
        raise RuntimeError(
            "Could not load plane-angle module."
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


def limb():
    return {
        "center_x_px": 100.0,
        "center_y_px": 200.0,
        "radius_px": 100.0,
    }


def line(
    dx: float,
    dy: float,
):
    return {
        "direction_x": dx,
        "direction_y": dy,
    }


def circle_from_normalized_center(
    u: float,
    v: float,
    radius_px: float = 150.0,
):
    # v is mathematical y-up.
    return {
        "center_x_px": (
            100.0
            + 100.0
            * u
        ),
        "center_y_px": (
            200.0
            - 100.0
            * v
        ),
        "radius_px": (
            radius_px
        ),
    }


def test_circle_plane_normal_uses_y_up_center_displacement() -> None:
    module = load_module()

    result = (
        module.finite_circle_plane_normal(
            circle_from_normalized_center(
                2.0,
                -3.0,
            ),
            limb(),
        )
    )

    raw = np.asarray(
        result[
            "raw_plane_normal"
        ]
    )

    assert np.allclose(
        raw,
        np.asarray(
            [
                -2.0,
                3.0,
                1.0,
            ]
        ),
        atol=1.0e-12,
        rtol=0.0,
    )


def test_circle_radius_does_not_change_reconstructed_plane() -> None:
    module = load_module()

    a = (
        module.finite_circle_plane_normal(
            circle_from_normalized_center(
                1.25,
                -0.75,
                radius_px=110.0,
            ),
            limb(),
        )
    )

    b = (
        module.finite_circle_plane_normal(
            circle_from_normalized_center(
                1.25,
                -0.75,
                radius_px=900.0,
            ),
            limb(),
        )
    )

    assert np.allclose(
        a[
            "unit_plane_normal"
        ],
        b[
            "unit_plane_normal"
        ],
        atol=1.0e-12,
        rtol=0.0,
    )

    assert (
        a[
            "circle_radius_used_for_plane_normal"
        ]
        is False
    )


def test_vertical_page_line_reconstructs_x_normal_plane() -> None:
    module = load_module()

    # Image direction downward/upward is the mathematical y direction.
    result = (
        module.line_plane_normal(
            line(
                0.0,
                -1.0,
            )
        )
    )

    normal = np.asarray(
        result[
            "unit_plane_normal"
        ]
    )

    assert math.isclose(
        abs(
            normal[0]
        ),
        1.0,
        rel_tol=0.0,
        abs_tol=1.0e-12,
    )

    assert math.isclose(
        normal[1],
        0.0,
        rel_tol=0.0,
        abs_tol=1.0e-12,
    )

    assert math.isclose(
        normal[2],
        0.0,
        rel_tol=0.0,
        abs_tol=1.0e-12,
    )


def test_horizontal_page_line_reconstructs_y_normal_plane() -> None:
    module = load_module()

    result = (
        module.line_plane_normal(
            line(
                1.0,
                0.0,
            )
        )
    )

    normal = np.asarray(
        result[
            "unit_plane_normal"
        ]
    )

    assert math.isclose(
        normal[0],
        0.0,
        rel_tol=0.0,
        abs_tol=1.0e-12,
    )

    assert math.isclose(
        abs(
            normal[1]
        ),
        1.0,
        rel_tol=0.0,
        abs_tol=1.0e-12,
    )

    assert math.isclose(
        normal[2],
        0.0,
        rel_tol=0.0,
        abs_tol=1.0e-12,
    )


def test_unoriented_plane_angle_is_sign_invariant() -> None:
    module = load_module()

    a = np.asarray(
        [
            1.0,
            0.0,
            0.0,
        ]
    )

    b = np.asarray(
        [
            0.5,
            0.0,
            math.sqrt(
                3.0
            )
            / 2.0,
        ]
    )

    angle1 = (
        module.unoriented_plane_angle_deg(
            a,
            b,
        )
    )

    angle2 = (
        module.unoriented_plane_angle_deg(
            -a,
            b,
        )
    )

    assert math.isclose(
        angle1,
        angle2,
        rel_tol=0.0,
        abs_tol=1.0e-12,
    )


def test_synthetic_G30_x_pair_recovers_30_degrees() -> None:
    module = load_module()

    # For delta=30 degrees, k=tan30 and the stereographic
    # circle-centre magnitude is 1/k = cot30 = sqrt(3).
    k = math.tan(
        math.radians(
            30.0
        )
    )

    yaxis = (
        module.line_plane_normal(
            line(
                0.0,
                -1.0,
            )
        )
    )

    x1 = (
        module.finite_circle_plane_normal(
            circle_from_normalized_center(
                1.0
                / k,
                0.0,
            ),
            limb(),
        )
    )

    angle = (
        module.unoriented_plane_angle_deg(
            np.asarray(
                yaxis[
                    "unit_plane_normal"
                ]
            ),
            np.asarray(
                x1[
                    "unit_plane_normal"
                ]
            ),
        )
    )

    assert math.isclose(
        angle,
        30.0,
        rel_tol=0.0,
        abs_tol=1.0e-10,
    )


def test_synthetic_G30_y_pair_recovers_30_degrees() -> None:
    module = load_module()

    k = math.tan(
        math.radians(
            30.0
        )
    )

    y0 = (
        module.line_plane_normal(
            line(
                1.0,
                0.0,
            )
        )
    )

    y1 = (
        module.finite_circle_plane_normal(
            circle_from_normalized_center(
                0.0,
                1.0
                / k,
            ),
            limb(),
        )
    )

    angle = (
        module.unoriented_plane_angle_deg(
            np.asarray(
                y0[
                    "unit_plane_normal"
                ]
            ),
            np.asarray(
                y1[
                    "unit_plane_normal"
                ]
            ),
        )
    )

    assert math.isclose(
        angle,
        30.0,
        rel_tol=0.0,
        abs_tol=1.0e-10,
    )


def test_scale_comparator_prefers_exact_G30_synthetic_pair() -> None:
    module = load_module()

    scales = {
        "G30": {
            "scale_k": math.tan(
                math.radians(
                    30.0
                )
            ),
            "predicted_delta_radians": (
                math.radians(
                    30.0
                )
            ),
            "predicted_delta_degrees": 30.0,
            "source_role": "synthetic",
        },
        "GHALF": {
            "scale_k": math.tan(
                0.5
            ),
            "predicted_delta_radians": 0.5,
            "predicted_delta_degrees": math.degrees(
                0.5
            ),
            "source_role": "synthetic",
        },
        "GUNIT": {
            "scale_k": 1.0,
            "predicted_delta_radians": math.pi / 4.0,
            "predicted_delta_degrees": 45.0,
            "source_role": "synthetic",
        },
        "GONE": {
            "scale_k": math.tan(
                1.0
            ),
            "predicted_delta_radians": 1.0,
            "predicted_delta_degrees": math.degrees(
                1.0
            ),
            "source_role": "synthetic",
        },
    }

    result = (
        module.scale_candidate_comparison(
            30.0,
            30.0,
            scales,
        )
    )

    assert math.isclose(
        result[
            "G30"
        ][
            "two_axis_angular_rms_deg"
        ],
        0.0,
        rel_tol=0.0,
        abs_tol=1.0e-12,
    )

    assert (
        result[
            "G30"
        ][
            "two_axis_angular_rms_deg"
        ]
        <
        result[
            "GHALF"
        ][
            "two_axis_angular_rms_deg"
        ]
    )


def test_holdout_is_not_in_plane_reconstruction_set() -> None:
    module = load_module()

    assert (
        module.HOLDOUT_ID
        not in module.LABELLED_IDS
    )

    assert set(
        module.LABELLED_IDS
    ) == {
        module.Y0_ID,
        module.Y1_ID,
        module.YAXIS_ID,
        module.X1_ID,
    }


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
