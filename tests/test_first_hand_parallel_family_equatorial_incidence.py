"""Synthetic tests for First Hand equatorial-incidence diagnostic."""

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
    / "audit_first_hand_parallel_family_equatorial_incidence.py"
)


def load_module():
    spec = importlib.util.spec_from_file_location(
        "first_hand_equatorial_incidence_test",
        SCRIPT,
    )

    if (
        spec is None
        or spec.loader is None
    ):
        raise RuntimeError(
            "Could not load equatorial-incidence module."
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


def test_exact_parallel_family_intersects_equator() -> None:
    module = load_module()

    # n0=(gx,gy,0), n1=(gx,gy,-1)
    n0 = np.asarray(
        [
            2.0,
            -3.0,
            0.0,
        ]
    )

    n1 = np.asarray(
        [
            2.0,
            -3.0,
            -1.0,
        ]
    )

    result = (
        module.intersection_diagnostic(
            n0,
            n1,
        )
    )

    assert math.isclose(
        result[
            "absolute_z"
        ],
        0.0,
        rel_tol=0.0,
        abs_tol=1.0e-15,
    )

    assert math.isclose(
        result[
            "epsilon_equator_deg"
        ],
        0.0,
        rel_tol=0.0,
        abs_tol=1.0e-15,
    )


def test_known_non_equatorial_intersection() -> None:
    module = load_module()

    n0 = np.asarray(
        [
            1.0,
            0.0,
            0.0,
        ]
    )

    n1 = np.asarray(
        [
            0.0,
            1.0,
            1.0,
        ]
    )

    result = (
        module.intersection_diagnostic(
            n0,
            n1,
        )
    )

    assert math.isclose(
        result[
            "absolute_z"
        ],
        1.0
        / math.sqrt(
            2.0
        ),
        rel_tol=0.0,
        abs_tol=1.0e-12,
    )

    assert math.isclose(
        result[
            "epsilon_equator_deg"
        ],
        45.0,
        rel_tol=0.0,
        abs_tol=1.0e-12,
    )


def test_plane_normal_sign_change_preserves_diagnostic() -> None:
    module = load_module()

    a = np.asarray(
        [
            0.7,
            -0.2,
            0.1,
        ]
    )

    b = np.asarray(
        [
            0.3,
            0.8,
            -0.5,
        ]
    )

    first = (
        module.intersection_diagnostic(
            a,
            b,
        )
    )

    second = (
        module.intersection_diagnostic(
            -a,
            b,
        )
    )

    assert math.isclose(
        first[
            "absolute_z"
        ],
        second[
            "absolute_z"
        ],
        rel_tol=0.0,
        abs_tol=1.0e-12,
    )

    assert math.isclose(
        first[
            "epsilon_equator_deg"
        ],
        second[
            "epsilon_equator_deg"
        ],
        rel_tol=0.0,
        abs_tol=1.0e-12,
    )

    assert math.isclose(
        first[
            "horizontal_azimuth_canonical_deg"
        ],
        second[
            "horizontal_azimuth_canonical_deg"
        ],
        rel_tol=0.0,
        abs_tol=1.0e-12,
    )


def test_swapping_plane_order_preserves_unoriented_result() -> None:
    module = load_module()

    a = np.asarray(
        [
            0.4,
            0.9,
            0.0,
        ]
    )

    b = np.asarray(
        [
            0.4,
            0.9,
            -1.0,
        ]
    )

    first = (
        module.intersection_diagnostic(
            a,
            b,
        )
    )

    second = (
        module.intersection_diagnostic(
            b,
            a,
        )
    )

    assert math.isclose(
        first[
            "absolute_z"
        ],
        second[
            "absolute_z"
        ],
        rel_tol=0.0,
        abs_tol=1.0e-12,
    )

    assert math.isclose(
        first[
            "horizontal_azimuth_canonical_deg"
        ],
        second[
            "horizontal_azimuth_canonical_deg"
        ],
        rel_tol=0.0,
        abs_tol=1.0e-12,
    )


def test_circular_distance_wraps_correctly() -> None:
    module = load_module()

    assert math.isclose(
        module.circular_distance_deg(
            359.0,
            1.0,
        ),
        2.0,
        rel_tol=0.0,
        abs_tol=1.0e-12,
    )


def test_nearest_antipodal_branch_selects_correct_direction() -> None:
    module = load_module()

    result = (
        module.nearest_antipodal_branch(
            299.0,
            120.0,
            300.0,
        )
    )

    assert math.isclose(
        result[
            "selected_azimuth_deg"
        ],
        300.0,
        rel_tol=0.0,
        abs_tol=1.0e-12,
    )

    assert math.isclose(
        result[
            "angular_separation_deg"
        ],
        1.0,
        rel_tol=0.0,
        abs_tol=1.0e-12,
    )


def test_page_limb_projection_uses_mathematical_y_up() -> None:
    module = load_module()

    diagnostic = {
        "horizontal_azimuth_canonical_deg": 90.0,
        "horizontal_azimuth_antipode_deg": 270.0,
    }

    node = {
        "landmark_id": module.LR_NODE_ID,
        "bearing_deg": 90.0,
        "consensus_x_px": 100.0,
        "consensus_y_px": 100.0,
        "radial_distance_px": 10.0,
        "radial_residual_from_limb_circle_px": 0.0,
    }

    limb = {
        "center_x_px": 100.0,
        "center_y_px": 110.0,
        "radius_px": 10.0,
    }

    result = (
        module.y_family_node_comparison(
            diagnostic,
            node,
            limb,
        )
    )

    assert math.isclose(
        result[
            "predicted_limb_x_px"
        ],
        100.0,
        rel_tol=0.0,
        abs_tol=1.0e-12,
    )

    assert math.isclose(
        result[
            "predicted_limb_y_px"
        ],
        100.0,
        rel_tol=0.0,
        abs_tol=1.0e-12,
    )


def test_exact_node_bearing_gives_zero_angular_residual() -> None:
    module = load_module()

    diagnostic = {
        "horizontal_azimuth_canonical_deg": 119.75,
        "horizontal_azimuth_antipode_deg": 299.75,
    }

    node = {
        "landmark_id": module.LR_NODE_ID,
        "bearing_deg": 299.75,
        "consensus_x_px": 0.0,
        "consensus_y_px": 0.0,
        "radial_distance_px": 1.0,
        "radial_residual_from_limb_circle_px": 0.0,
    }

    limb = {
        "center_x_px": 0.0,
        "center_y_px": 0.0,
        "radius_px": 1.0,
    }

    result = (
        module.y_family_node_comparison(
            diagnostic,
            node,
            limb,
        )
    )

    assert math.isclose(
        result[
            "delta_node_deg"
        ],
        0.0,
        rel_tol=0.0,
        abs_tol=1.0e-12,
    )


def test_x_family_has_no_rim_node_assignment_in_source() -> None:
    source = SCRIPT.read_text(
        encoding="utf-8",
    )

    # LR landmark appears only as the y-family source landmark.
    assert "x_family_rim_node_selected" in source
    assert '"x_family_rim_node_selected": False' in source


def test_implementation_contains_no_optimizer_or_refit() -> None:
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
