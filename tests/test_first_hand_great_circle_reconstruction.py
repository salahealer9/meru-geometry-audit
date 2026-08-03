"""Synthetic tests for the First Hand great-circle reconstruction."""

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
    / "audit_first_hand_great_circle_reconstruction.py"
)


def load_module():
    spec = importlib.util.spec_from_file_location(
        "first_hand_great_circle_reconstruction_test",
        SCRIPT,
    )

    if (
        spec is None
        or spec.loader is None
    ):
        raise RuntimeError(
            "Could not load great-circle reconstruction module."
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
        "center_x_px": 700.0,
        "center_y_px": 500.0,
        "radius_px": 300.0,
    }


def sample_from_uv(
    module,
    uv: np.ndarray,
):
    pixels = (
        module.normalized_to_pixel(
            uv,
            limb(),
        )
    )

    count = len(
        pixels
    )

    return module.base.ResampledCurve(
        points=pixels,
        sigma_px=np.full(
            count,
            2.0,
            dtype=np.float64,
        ),
        weights=np.full(
            count,
            1.0
            / count,
            dtype=np.float64,
        ),
        total_arc_length_px=1.0,
        segment_count=1,
    )


def angular_difference_deg(
    a: float,
    b: float,
) -> float:
    delta = abs(
        (
            a
            - b
        )
        % 180.0
    )

    return min(
        delta,
        180.0
        - delta,
    )


def test_exact_ellipse_points_have_zero_nearest_distance() -> None:
    module = load_module()

    phi = math.radians(
        31.0
    )

    q = 0.43

    t = np.linspace(
        0.0,
        2.0
        * math.pi,
        401,
        endpoint=False,
    )

    points = (
        module.projected_great_circle_points(
            phi,
            q,
            t,
        )
    )

    distance = (
        module.projected_great_circle_distance_normalized(
            points,
            phi,
            q,
        )
    )

    assert float(
        np.max(
            distance
        )
    ) < 1.0e-10


def test_q_zero_is_exact_closed_diameter_segment() -> None:
    module = load_module()

    phi = math.radians(
        40.0
    )

    major, minor = (
        module.ellipse_axes(
            phi
        )
    )

    on_segment = np.asarray(
        [
            -0.8,
            -0.2,
            0.0,
            0.3,
            0.9,
        ]
    )[:, None] * major[
        None,
        :
    ]

    distance = (
        module.projected_great_circle_distance_normalized(
            on_segment,
            phi,
            0.0,
        )
    )

    assert float(
        np.max(
            distance
        )
    ) < 1.0e-12

    outside = (
        1.2
        * major
        + 0.1
        * minor
    )[
        None,
        :
    ]

    distance_out = (
        module.projected_great_circle_distance_normalized(
            outside,
            phi,
            0.0,
        )[0]
    )

    assert math.isclose(
        distance_out,
        math.hypot(
            0.2,
            0.1,
        ),
        rel_tol=0.0,
        abs_tol=1.0e-12,
    )


def test_curved_synthetic_great_circle_is_recovered() -> None:
    module = load_module()

    phi_deg = 34.0
    q = 0.52

    t = np.linspace(
        -1.3,
        1.5,
        240,
    )

    uv = (
        module.projected_great_circle_points(
            math.radians(
                phi_deg
            ),
            q,
            t,
        )
    )

    sample = (
        sample_from_uv(
            module,
            uv,
        )
    )

    result = (
        module.fit_projected_great_circle(
            [
                sample
            ],
            limb(),
            phi_seeds_deg=(
                0.0,
                30.0,
                60.0,
                90.0,
            ),
            q_seeds=(
                0.10,
                0.50,
                0.90,
            ),
        )
    )

    assert (
        angular_difference_deg(
            result[
                "phi_degrees"
            ],
            phi_deg,
        )
        < 1.0e-4
    )

    assert math.isclose(
        result[
            "q"
        ],
        q,
        rel_tol=0.0,
        abs_tol=1.0e-5,
    )

    assert (
        result[
            "residuals"
        ][
            "absolute_px"
        ][
            "rms"
        ]
        < 1.0e-4
    )


def test_diameter_synthetic_trace_can_reach_q_zero() -> None:
    module = load_module()

    phi_deg = 72.0

    phi = math.radians(
        phi_deg
    )

    major, _ = (
        module.ellipse_axes(
            phi
        )
    )

    values = np.linspace(
        -0.92,
        0.93,
        220,
    )

    uv = (
        values[
            :,
            None,
        ]
        * major[
            None,
            :
        ]
    )

    sample = (
        sample_from_uv(
            module,
            uv,
        )
    )

    result = (
        module.fit_projected_great_circle(
            [
                sample
            ],
            limb(),
            phi_seeds_deg=(
                45.0,
                60.0,
                75.0,
                90.0,
            ),
            q_seeds=(
                0.0,
                0.10,
                0.50,
            ),
        )
    )

    assert (
        angular_difference_deg(
            result[
                "phi_degrees"
            ],
            phi_deg,
        )
        < 1.0e-3
    )

    assert (
        result[
            "q"
        ]
        < 1.0e-5
    )

    assert (
        result[
            "residuals"
        ][
            "absolute_px"
        ][
            "rms"
        ]
        < 1.0e-3
    )


def test_plane_normal_branches_are_unit_and_project_same_conic() -> None:
    module = load_module()

    branches = (
        module.plane_normal_branches(
            math.radians(
                25.0
            ),
            0.6,
        )
    )

    plus = np.asarray(
        branches[
            "plus_z"
        ]
    )

    minus = np.asarray(
        branches[
            "minus_z"
        ]
    )

    assert math.isclose(
        float(
            np.linalg.norm(
                plus
            )
        ),
        1.0,
        abs_tol=1.0e-12,
    )

    assert math.isclose(
        float(
            np.linalg.norm(
                minus
            )
        ),
        1.0,
        abs_tol=1.0e-12,
    )

    assert np.allclose(
        plus[:2],
        minus[:2],
        atol=1.0e-12,
        rtol=0.0,
    )

    assert math.isclose(
        plus[2],
        -minus[2],
        abs_tol=1.0e-12,
    )


def test_unoriented_plane_angle_ignores_normal_sign() -> None:
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
            0.0,
            1.0,
            0.0,
        ]
    )

    assert math.isclose(
        module.unoriented_plane_angle_deg(
            a,
            b,
        ),
        90.0,
        abs_tol=1.0e-12,
    )

    assert math.isclose(
        module.unoriented_plane_angle_deg(
            -a,
            b,
        ),
        90.0,
        abs_tol=1.0e-12,
    )


def test_multistart_grid_matches_frozen_protocol() -> None:
    module = load_module()

    assert module.PHI_SEEDS_DEG == (
        0.0,
        15.0,
        30.0,
        45.0,
        60.0,
        75.0,
        90.0,
        105.0,
        120.0,
        135.0,
        150.0,
        165.0,
    )

    assert module.Q_SEEDS == (
        0.00,
        0.10,
        0.25,
        0.50,
        0.75,
        0.95,
    )

    assert (
        len(
            module.PHI_SEEDS_DEG
        )
        * len(
            module.Q_SEEDS
        )
        == 72
    )


def test_scaffold_is_not_in_fit_partition() -> None:
    module = load_module()

    assert (
        module.HOLDOUT_ID
        not in module.FIT_IDS
    )

    assert set(
        module.FIT_IDS
    ) == set(
        module.base.CALIBRATION_IDS
    )


def test_output_is_separate_from_prior_results() -> None:
    module = load_module()

    assert (
        module.OUTPUT_JSON
        != module.MORPHOLOGY_JSON
    )

    assert (
        module.OUTPUT_JSON.name
        == "first_hand_great_circle_reconstruction.json"
    )


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
        "great-circle reconstruction"
        in result.stdout
    )
