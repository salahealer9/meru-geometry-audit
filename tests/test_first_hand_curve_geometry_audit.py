"""Synthetic-only tests for the First Hand curve-geometry engine."""

from __future__ import annotations

import importlib.util
import math
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "audit_first_hand_curve_geometry.py"


def load_module():
    spec = importlib.util.spec_from_file_location(
        "first_hand_curve_geometry_audit",
        SCRIPT,
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("Could not load audit module")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_partition_is_four_plus_one_holdout() -> None:
    module = load_module()
    assert len(module.CALIBRATION_IDS) == 4
    assert module.HOLDOUT_ID not in module.CALIBRATION_IDS
    assert set(module.CURVE_IDS) == (
        set(module.CALIBRATION_IDS) | {module.HOLDOUT_ID}
    )


def test_uniform_resampling_removes_raw_click_density() -> None:
    module = load_module()

    sparse = np.asarray([[0.0, 0.0], [10.0, 0.0]])
    dense = np.asarray(
        [
            [0.0, 0.0],
            [0.5, 0.0],
            [1.0, 0.0],
            [3.0, 0.0],
            [7.5, 0.0],
            [9.5, 0.0],
            [10.0, 0.0],
        ]
    )

    a, _, wa, la = module.resample_segment(
        sparse,
        np.full(len(sparse), 2.0),
        2.0,
    )
    b, _, wb, lb = module.resample_segment(
        dense,
        np.full(len(dense), 2.0),
        2.0,
    )

    assert np.allclose(a, b, atol=1e-12)
    assert math.isclose(la, 10.0, abs_tol=1e-12)
    assert math.isclose(lb, 10.0, abs_tol=1e-12)
    assert math.isclose(float(np.sum(wa)), 10.0, abs_tol=1e-12)
    assert math.isclose(float(np.sum(wb)), 10.0, abs_tol=1e-12)


def test_point_to_polyline_distance_uses_segments_not_clicks() -> None:
    module = load_module()

    target = module.Segment(
        landmark_id="synthetic",
        pass_number=1,
        segment_id="S01",
        points=np.asarray([[0.0, 0.0], [10.0, 0.0]]),
        sigma_px=np.asarray([2.0, 2.0]),
    )

    query = np.asarray([[5.0, 3.0], [12.0, 0.0]])
    distances = module.point_to_curve_distance(query, [target])
    assert np.allclose(distances, [3.0, 2.0], atol=1e-12)


def test_segment_ids_are_not_forced_to_correspond() -> None:
    module = load_module()

    p1_segment = module.Segment(
        landmark_id="synthetic",
        pass_number=1,
        segment_id="S01",
        points=np.asarray([[0.0, 0.0], [10.0, 0.0]]),
        sigma_px=np.asarray([2.0, 2.0]),
    )
    p2_segment = module.Segment(
        landmark_id="synthetic",
        pass_number=2,
        segment_id="S99",
        points=np.asarray([[0.0, 1.0], [10.0, 1.0]]),
        sigma_px=np.asarray([2.0, 2.0]),
    )

    pass1 = module.resample_curve([p1_segment], 2.0)
    pass2 = module.resample_curve([p2_segment], 2.0)
    result = module.symmetric_pass_agreement(
        pass1,
        [p1_segment],
        pass2,
        [p2_segment],
    )

    assert math.isclose(
        result["symmetric_px"]["median"],
        1.0,
        abs_tol=1e-12,
    )
    assert result["manual_review_required"] is False


def circle_sample(module, radius: float, count: int):
    theta = np.linspace(0.0, 2.0 * math.pi, count, endpoint=False)
    points = np.column_stack(
        (3.0 + radius * np.cos(theta), -4.0 + radius * np.sin(theta))
    )
    return module.ResampledCurve(
        points=points,
        sigma_px=np.full(count, 2.0),
        weights=np.full(count, 1.0 / count),
        total_arc_length_px=2.0 * math.pi * radius,
        segment_count=1,
    )


def test_equal_pass_weighting_survives_tenfold_point_count_difference() -> None:
    module = load_module()

    pass1 = circle_sample(module, 10.0, 40)
    pass2 = circle_sample(module, 12.0, 400)
    fit = module.fit_circle([pass1, pass2], limb_radius_px=100.0)

    assert math.isclose(fit["center_x_px"], 3.0, abs_tol=1e-7)
    assert math.isclose(fit["center_y_px"], -4.0, abs_tol=1e-7)
    assert math.isclose(fit["radius_px"], 11.0, abs_tol=1e-6)


def test_circle_fit_recovers_clean_synthetic_circle() -> None:
    module = load_module()

    sample = circle_sample(module, 17.0, 180)
    fit = module.fit_circle([sample], limb_radius_px=100.0)

    assert math.isclose(fit["center_x_px"], 3.0, abs_tol=1e-7)
    assert math.isclose(fit["center_y_px"], -4.0, abs_tol=1e-7)
    assert math.isclose(fit["radius_px"], 17.0, abs_tol=1e-7)
    assert fit["residuals"]["absolute_px"]["rms"] < 1e-8


def test_ellipse_fit_recovers_clean_synthetic_ellipse() -> None:
    module = load_module()

    cx, cy = 8.0, -3.0
    a, b = 20.0, 12.0
    angle = 0.37

    theta = np.linspace(0.0, 2.0 * math.pi, 300, endpoint=False)
    local = np.column_stack((a * np.cos(theta), b * np.sin(theta)))
    rotation = np.asarray(
        [
            [math.cos(angle), -math.sin(angle)],
            [math.sin(angle), math.cos(angle)],
        ]
    )
    points = local @ rotation.T + np.asarray([cx, cy])

    sample = module.ResampledCurve(
        points=points,
        sigma_px=np.full(len(points), 2.0),
        weights=np.full(len(points), 1.0 / len(points)),
        total_arc_length_px=100.0,
        segment_count=1,
    )

    fit = module.fit_ellipse([sample], limb_radius_px=100.0)

    assert math.isclose(fit["center_x_px"], cx, abs_tol=1e-5)
    assert math.isclose(fit["center_y_px"], cy, abs_tol=1e-5)
    assert math.isclose(fit["semi_major_px"], a, rel_tol=1e-5)
    assert math.isclose(fit["semi_minor_px"], b, rel_tol=1e-5)
    assert fit["residuals"]["absolute_px"]["rms"] < 1e-5


def test_review_threshold_is_above_twelve_pixels() -> None:
    module = load_module()

    def segment(y: float, pass_number: int, segment_id: str):
        return module.Segment(
            landmark_id="synthetic",
            pass_number=pass_number,
            segment_id=segment_id,
            points=np.asarray([[0.0, y], [20.0, y]]),
            sigma_px=np.asarray([2.0, 2.0]),
        )

    p1_seg = segment(0.0, 1, "S01")
    p2_seg = segment(13.0, 2, "S88")
    p1 = module.resample_curve([p1_seg], 2.0)
    p2 = module.resample_curve([p2_seg], 2.0)

    result = module.symmetric_pass_agreement(
        p1,
        [p1_seg],
        p2,
        [p2_seg],
    )

    assert math.isclose(result["symmetric_px"]["median"], 13.0)
    assert result["manual_review_required"] is True


def test_source_code_keeps_model_verdicts_disabled() -> None:
    text = " ".join(SCRIPT.read_text(encoding="utf-8").lower().split())

    assert '"projective_map_fitted": false' in text
    assert '"projective_gauge_selected": false' in text
    assert '"spherical_scale_selected": false' in text
    assert '"great_circle_certification_issued": false' in text
    assert '"s1_computed": false' in text
    assert '"s1_5_computed": false' in text
    assert '"s2_computed": false' in text


def test_limb_reference_comes_from_original_neutral_census() -> None:
    """The limb belongs to the frozen neutral census, not its addendum."""
    module = load_module()

    assert (
        module.NEUTRAL_GEOMETRY_SCRIPT.name
        == "audit_first_hand_neutral_geometry.py"
    )

    assert (
        "expanded_neutral"
        not in str(
            module.NEUTRAL_GEOMETRY_SCRIPT
        )
    )


def test_frozen_limb_reference_interface() -> None:
    """The existing neutral census exposes the required frozen limb."""
    module = load_module()

    limb = (
        module.load_frozen_limb_reference()
    )

    assert set(
        limb
    ) == {
        "center_x_px",
        "center_y_px",
        "radius_px",
    }

    assert math.isfinite(
        limb[
            "center_x_px"
        ]
    )
    assert math.isfinite(
        limb[
            "center_y_px"
        ]
    )
    assert (
        math.isfinite(
            limb[
                "radius_px"
            ]
        )
        and limb[
            "radius_px"
        ] > 0.0
    )
