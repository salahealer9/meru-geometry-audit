"""Synthetic tests for the First Hand neutral morphology census."""

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
    / "audit_first_hand_curve_morphology.py"
)


def load_module():
    spec = importlib.util.spec_from_file_location(
        "first_hand_curve_morphology_test",
        SCRIPT,
    )

    if (
        spec is None
        or spec.loader is None
    ):
        raise RuntimeError(
            "Could not load morphology module."
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


def sample(
    points: np.ndarray,
):
    module = load_module()

    count = len(points)

    return module.base.ResampledCurve(
        points=np.asarray(
            points,
            dtype=np.float64,
        ),
        sigma_px=np.full(
            count,
            2.0,
        ),
        weights=np.full(
            count,
            1.0 / count,
        ),
        total_arc_length_px=1.0,
        segment_count=1,
    )


def test_horizontal_line_has_zero_residual() -> None:
    module = load_module()

    points = np.column_stack(
        (
            np.linspace(
                -10.0,
                10.0,
                101,
            ),
            np.full(
                101,
                7.0,
            ),
        )
    )

    fitted = module.fit_line(
        [
            sample(points)
        ],
        limb_radius_px=500.0,
    )

    assert (
        fitted[
            "residuals"
        ][
            "absolute_px"
        ][
            "rms"
        ]
        < 1.0e-12
    )

    assert math.isclose(
        fitted[
            "unoriented_bearing_deg"
        ],
        0.0,
        abs_tol=1.0e-10,
    )


def test_rotated_line_recovers_orientation() -> None:
    module = load_module()

    angle_deg = 37.0
    angle = math.radians(
        angle_deg
    )

    direction = np.asarray(
        [
            math.cos(angle),
            math.sin(angle),
        ]
    )

    t = np.linspace(
        -50.0,
        50.0,
        151,
    )

    points = (
        np.asarray(
            [
                1234.0,
                -567.0,
            ]
        )
        + t[:, None]
        * direction[None, :]
    )

    fitted = module.fit_line(
        [
            sample(points)
        ],
        limb_radius_px=500.0,
    )

    assert (
        fitted[
            "residuals"
        ][
            "absolute_px"
        ][
            "rms"
        ]
        < 1.0e-10
    )

    assert math.isclose(
        fitted[
            "unoriented_bearing_deg"
        ],
        angle_deg,
        abs_tol=1.0e-9,
    )


def test_equal_pass_weighting_is_not_click_count_weighting() -> None:
    module = load_module()

    x1 = np.linspace(
        -20.0,
        20.0,
        401,
    )

    x2 = np.linspace(
        -20.0,
        20.0,
        21,
    )

    pass1 = np.column_stack(
        (
            x1,
            np.zeros_like(
                x1
            ),
        )
    )

    pass2 = np.column_stack(
        (
            x2,
            np.full_like(
                x2,
                2.0,
            ),
        )
    )

    fitted = module.fit_line(
        [
            sample(pass1),
            sample(pass2),
        ],
        limb_radius_px=500.0,
    )

    assert math.isclose(
        fitted[
            "center_y_px"
        ],
        1.0,
        abs_tol=1.0e-12,
    )

    assert math.isclose(
        fitted[
            "residuals"
        ][
            "absolute_px"
        ][
            "rms"
        ],
        1.0,
        abs_tol=1.0e-12,
    )


def test_curved_arc_is_not_zero_residual_line() -> None:
    module = load_module()

    theta = np.linspace(
        -0.8,
        0.8,
        201,
    )

    points = np.column_stack(
        (
            100.0
            * np.cos(theta),
            100.0
            * np.sin(theta),
        )
    )

    fitted = module.fit_line(
        [
            sample(points)
        ],
        limb_radius_px=500.0,
    )

    assert (
        fitted[
            "residuals"
        ][
            "absolute_px"
        ][
            "rms"
        ]
        > 1.0
    )


def test_outputs_are_separate_from_qc_result() -> None:
    module = load_module()

    assert (
        module.OUTPUT_JSON
        != module.QC_RESULT
    )

    assert (
        module.OUTPUT_REPORT.name
        == "first_hand_curve_morphology_census.md"
    )


def test_direct_cli_import_path() -> None:
    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
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
