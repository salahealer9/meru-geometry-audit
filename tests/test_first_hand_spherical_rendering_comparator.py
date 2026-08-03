"""Synthetic tests for the First Hand spherical-rendering comparator."""

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
    / "audit_first_hand_spherical_rendering_comparator.py"
)


def load_module():
    spec = importlib.util.spec_from_file_location(
        "first_hand_spherical_rendering_comparator_test",
        SCRIPT,
    )

    if (
        spec is None
        or spec.loader is None
    ):
        raise RuntimeError(
            "Could not load rendering comparator."
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
        "center_x_px": 10.0,
        "center_y_px": -20.0,
        "radius_px": 100.0,
    }


def circle_dict(
    *,
    cx: float,
    cy: float,
    radius: float,
):
    return {
        "center_x_px": cx,
        "center_y_px": cy,
        "radius_px": radius,
        "residuals": {
            "absolute_px": {
                "median": 0.1,
                "rms": 0.2,
                "p95": 0.3,
                "maximum": 0.4,
            },
        },
    }


def line_dict(
    *,
    px: float,
    py: float,
    dx: float,
    dy: float,
):
    return {
        "center_x_px": px,
        "center_y_px": py,
        "direction_x": dx,
        "direction_y": dy,
        "unoriented_bearing_deg": 0.0,
        "residuals": {
            "absolute_px": {
                "median": 0.1,
                "rms": 0.2,
                "p95": 0.3,
                "maximum": 0.4,
            },
        },
    }


def test_exact_stereographic_circle_has_zero_power_closure() -> None:
    module = load_module()

    # R=100, d=75, r=125:
    # 125^2 - 75^2 = 100^2 exactly.
    result = (
        module.evaluate_circle_branch(
            circle_dict(
                cx=85.0,
                cy=-20.0,
                radius=125.0,
            ),
            limb(),
        )
    )

    assert math.isclose(
        result[
            "epsilon_power"
        ],
        0.0,
        rel_tol=0.0,
        abs_tol=1.0e-12,
    )

    assert math.isclose(
        result[
            "R_implied_px"
        ],
        100.0,
        rel_tol=0.0,
        abs_tol=1.0e-12,
    )

    assert math.isclose(
        result[
            "delta_R_px"
        ],
        0.0,
        rel_tol=0.0,
        abs_tol=1.0e-12,
    )


def test_exact_stereographic_circle_intersections_are_antipodal() -> None:
    module = load_module()

    result = (
        module.evaluate_circle_branch(
            circle_dict(
                cx=85.0,
                cy=-20.0,
                radius=125.0,
            ),
            limb(),
        )
    )

    assert (
        result[
            "equator_intersections"
        ][
            "intersection_count"
        ]
        == 2
    )

    assert math.isclose(
        result[
            "antipodal_separation_deg"
        ],
        180.0,
        rel_tol=0.0,
        abs_tol=1.0e-10,
    )

    assert math.isclose(
        result[
            "delta_antipodal_deg"
        ],
        0.0,
        rel_tol=0.0,
        abs_tol=1.0e-10,
    )


def test_centre_passing_line_has_zero_stereographic_line_residual() -> None:
    module = load_module()

    result = (
        module.evaluate_line_branch(
            line_dict(
                px=10.0,
                py=-20.0,
                dx=2.0,
                dy=3.0,
            ),
            limb(),
        )
    )

    assert math.isclose(
        result[
            "line_to_frozen_sphere_center_px"
        ],
        0.0,
        rel_tol=0.0,
        abs_tol=1.0e-12,
    )


def test_offset_line_reports_exact_perpendicular_distance() -> None:
    module = load_module()

    # Horizontal line y=-15; frozen centre y=-20.
    result = (
        module.evaluate_line_branch(
            line_dict(
                px=0.0,
                py=-15.0,
                dx=1.0,
                dy=0.0,
            ),
            limb(),
        )
    )

    assert math.isclose(
        result[
            "line_to_frozen_sphere_center_px"
        ],
        5.0,
        rel_tol=0.0,
        abs_tol=1.0e-12,
    )

    assert math.isclose(
        result[
            "line_to_frozen_sphere_center_over_R"
        ],
        0.05,
        rel_tol=0.0,
        abs_tol=1.0e-12,
    )


def test_perturbed_circle_has_nonzero_power_closure() -> None:
    module = load_module()

    result = (
        module.evaluate_circle_branch(
            circle_dict(
                cx=85.0,
                cy=-20.0,
                radius=120.0,
            ),
            limb(),
        )
    )

    assert not math.isclose(
        result[
            "epsilon_power"
        ],
        0.0,
        rel_tol=0.0,
        abs_tol=1.0e-6,
    )


def test_disjoint_circles_report_no_fake_intersections() -> None:
    module = load_module()

    result = (
        module.circle_circle_intersections(
            np.asarray(
                [0.0, 0.0]
            ),
            1.0,
            np.asarray(
                [10.0, 0.0]
            ),
            1.0,
        )
    )

    assert (
        result[
            "intersection_count"
        ]
        == 0
    )

    assert (
        result[
            "points_px"
        ]
        == []
    )


def test_branch_allocation_is_frozen_and_holdout_is_separate() -> None:
    module = load_module()

    assert module.LINE_IDS == (
        module.Y0_ID,
        module.YAXIS_ID,
    )

    assert module.CURVED_LABELLED_IDS == (
        module.Y1_ID,
        module.X1_ID,
    )

    assert (
        module.HOLDOUT_ID
        not in module.LABELLED_IDS
    )


def test_implementation_contains_no_scipy_optimizer_dependency() -> None:
    source = SCRIPT.read_text(
        encoding="utf-8",
    )

    assert "scipy.optimize" not in source
    assert "least_squares(" not in source
    assert "minimize(" not in source


def test_output_does_not_overwrite_parent_results() -> None:
    module = load_module()

    assert (
        module.OUTPUT_JSON
        != module.MORPHOLOGY_JSON
    )

    assert (
        module.OUTPUT_JSON
        != module.ORTHOGRAPHIC_JSON
    )

    assert (
        module.OUTPUT_REPORT.name
        == "first_hand_spherical_rendering_comparator.md"
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
        "--check-inputs"
        in result.stdout
    )
