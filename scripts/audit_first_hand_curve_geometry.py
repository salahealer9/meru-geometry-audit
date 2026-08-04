#!/usr/bin/env python3
"""Model-neutral two-pass geometry audit for First Hand source curves."""

from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import json
import math
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Sequence

import numpy as np
from scipy.optimize import least_squares

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data" / "derived" / "first_hand_arm_of_god"
PASS_PATHS = {
    1: DATA_DIR / "great_circle_segments_pass1.csv",
    2: DATA_DIR / "great_circle_segments_pass2.csv",
}
SEAL_PATH = DATA_DIR / "great_circle_segment_passes.sha256"
OUTPUT_JSON = DATA_DIR / "first_hand_curve_geometry_audit.json"
OUTPUT_REPORT = ROOT / "reports" / "first_hand_curve_geometry_audit.md"
NEUTRAL_GEOMETRY_SCRIPT = (
    ROOT / "scripts" / "audit_first_hand_neutral_geometry.py"
)

CALIBRATION_IDS = (
    "AOG-LM-P07-GC-Y0",
    "AOG-LM-P07-GC-Y1",
    "AOG-LM-P07-GC-YAXIS",
    "AOG-LM-P07-GC-X1",
)
HOLDOUT_ID = "AOG-LM-P07-GC-SCAFFOLD-UR-UC-X1LL-LL"
CURVE_IDS = (*CALIBRATION_IDS, HOLDOUT_ID)

PRIMARY_SPACING_PX = 2.0
SENSITIVITY_SPACINGS_PX = (1.0, 4.0)
CURVE_SIGMA_FLOOR_PX = 2.0
MANUAL_REVIEW_MEDIAN_PX = 12.0

REQUIRED_FIELDS = {
    "crop_id",
    "crop_file_sha256",
    "crop_pixel_sha256",
    "landmark_id",
    "pass_number",
    "operator",
    "segment_id",
    "sequence_index",
    "x_px",
    "y_px",
    "local_stroke_width_px",
    "source_feature",
    "operator_note",
    "timestamp_utc",
}


@dataclass(frozen=True)
class Segment:
    landmark_id: str
    pass_number: int
    segment_id: str
    points: np.ndarray
    sigma_px: np.ndarray


@dataclass(frozen=True)
class ResampledCurve:
    points: np.ndarray
    sigma_px: np.ndarray
    weights: np.ndarray
    total_arc_length_px: float
    segment_count: int


def sha256_path(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def verify_input_seal(
    seal_path: Path = SEAL_PATH,
    root: Path = ROOT,
) -> dict[str, str]:
    """Verify that the manifest seals exactly the two expected pass files."""
    if not seal_path.exists():
        raise RuntimeError(f"Missing seal: {seal_path}")

    expected = {str(path.relative_to(root)) for path in PASS_PATHS.values()}
    found: dict[str, str] = {}

    for raw in seal_path.read_text(encoding="utf-8").splitlines():
        raw = raw.strip()
        if not raw:
            continue
        parts = raw.split()
        if len(parts) < 2:
            raise RuntimeError(f"Malformed checksum line: {raw!r}")
        digest = parts[0]
        rel = parts[-1].lstrip("*")
        path = root / rel
        if not path.exists():
            raise RuntimeError(f"Sealed input missing: {rel}")
        actual = sha256_path(path)
        if actual != digest:
            raise RuntimeError(
                f"Hash mismatch for {rel}: expected {digest}, got {actual}"
            )
        found[rel] = digest

    if set(found) != expected:
        raise RuntimeError(
            "Seal must contain exactly the two curve-pass files; "
            f"expected {sorted(expected)}, found {sorted(found)}"
        )
    return found


def _positive_float(raw: str, label: str) -> float:
    value = float(raw)
    if not (math.isfinite(value) and value > 0.0):
        raise RuntimeError(f"{label} must be finite and >0; got {raw!r}")
    return value


def read_curve_pass(path: Path, expected_pass: int) -> dict[str, list[Segment]]:
    """Parse one complete five-curve pass, preserving segment boundaries."""
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        fields = set(reader.fieldnames or [])
        missing = REQUIRED_FIELDS - fields
        if missing:
            raise RuntimeError(f"{path} missing fields: {sorted(missing)}")
        rows = list(reader)

    grouped: dict[tuple[str, str], list[dict[str, str]]] = {}
    for row in rows:
        pass_number = int(row["pass_number"])
        if pass_number != expected_pass:
            raise RuntimeError(
                f"{path} contains pass {pass_number}; expected {expected_pass}"
            )
        curve_id = row["landmark_id"]
        if curve_id not in CURVE_IDS:
            raise RuntimeError(f"Unexpected curve ID in {path}: {curve_id}")
        grouped.setdefault((curve_id, row["segment_id"]), []).append(row)

    observed_ids = {curve_id for curve_id, _ in grouped}
    if observed_ids != set(CURVE_IDS):
        raise RuntimeError(
            f"{path} must contain exactly the five frozen curves; "
            f"found {sorted(observed_ids)}"
        )

    curves = {curve_id: [] for curve_id in CURVE_IDS}
    for (curve_id, segment_id), segment_rows in grouped.items():
        ordered = sorted(segment_rows, key=lambda row: int(row["sequence_index"]))
        indices = [int(row["sequence_index"]) for row in ordered]
        if len(indices) != len(set(indices)):
            raise RuntimeError(f"Duplicate sequence index: {curve_id} {segment_id}")

        points = np.asarray(
            [[float(row["x_px"]), float(row["y_px"])] for row in ordered],
            dtype=np.float64,
        )
        if (
            points.ndim != 2
            or points.shape[1] != 2
            or len(points) < 2
            or not np.all(np.isfinite(points))
        ):
            raise RuntimeError(f"Invalid coordinates: {curve_id} {segment_id}")

        widths = np.asarray(
            [
                _positive_float(row["local_stroke_width_px"], "stroke width")
                for row in ordered
            ],
            dtype=np.float64,
        )
        sigma = np.maximum(CURVE_SIGMA_FLOOR_PX, 0.5 * widths)
        curves[curve_id].append(
            Segment(curve_id, expected_pass, segment_id, points, sigma)
        )

    for segments in curves.values():
        segments.sort(key=lambda segment: segment.segment_id)
    return curves


def resample_segment(
    points: np.ndarray,
    sigma_px: np.ndarray,
    spacing_px: float,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, float]:
    """Uniformly resample one visible polyline in image-space arc length."""
    if not (math.isfinite(spacing_px) and spacing_px > 0.0):
        raise ValueError("spacing_px must be finite and positive")
    if len(points) != len(sigma_px):
        raise ValueError("points and sigma_px length mismatch")

    edge_lengths = np.linalg.norm(np.diff(points, axis=0), axis=1)
    keep = np.concatenate(([True], edge_lengths > 1.0e-12))
    points = points[keep]
    sigma_px = sigma_px[keep]
    if len(points) < 2:
        raise RuntimeError("Segment has zero usable arc length")

    edge_lengths = np.linalg.norm(np.diff(points, axis=0), axis=1)
    cumulative = np.concatenate(([0.0], np.cumsum(edge_lengths)))
    total = float(cumulative[-1])
    if total <= 0.0:
        raise RuntimeError("Segment has non-positive arc length")

    targets = np.arange(0.0, total, spacing_px, dtype=np.float64)
    if len(targets) == 0 or not math.isclose(
        float(targets[-1]), total, rel_tol=0.0, abs_tol=1.0e-12
    ):
        targets = np.append(targets, total)

    sampled = np.column_stack(
        (
            np.interp(targets, cumulative, points[:, 0]),
            np.interp(targets, cumulative, points[:, 1]),
        )
    )
    sampled_sigma = np.interp(targets, cumulative, sigma_px)

    intervals = np.diff(targets)
    weights = np.zeros(len(targets), dtype=np.float64)
    weights[0] = 0.5 * intervals[0]
    weights[-1] = 0.5 * intervals[-1]
    if len(targets) > 2:
        weights[1:-1] = 0.5 * (intervals[:-1] + intervals[1:])

    if not math.isclose(
        float(np.sum(weights)), total, rel_tol=1.0e-10, abs_tol=1.0e-9
    ):
        raise RuntimeError("Arc-length quadrature does not sum to segment length")

    return sampled, sampled_sigma, weights, total


def resample_curve(
    segments: Sequence[Segment],
    spacing_px: float,
) -> ResampledCurve:
    """Resample all visible segments without bridging any occlusion."""
    point_blocks = []
    sigma_blocks = []
    weight_blocks = []
    total = 0.0

    for segment in segments:
        points, sigma, weights, length = resample_segment(
            segment.points, segment.sigma_px, spacing_px
        )
        point_blocks.append(points)
        sigma_blocks.append(sigma)
        weight_blocks.append(weights)
        total += length

    points = np.vstack(point_blocks)
    sigma = np.concatenate(sigma_blocks)
    raw_weights = np.concatenate(weight_blocks)
    weights = raw_weights / float(np.sum(raw_weights))

    return ResampledCurve(points, sigma, weights, total, len(segments))


def point_to_segment_distance(
    query: np.ndarray,
    a: np.ndarray,
    b: np.ndarray,
) -> np.ndarray:
    """Distances from query points to one finite line segment."""
    edge = b - a
    denom = float(np.dot(edge, edge))
    if denom <= 1.0e-24:
        return np.linalg.norm(query - a, axis=1)
    t = ((query - a) @ edge) / denom
    t = np.clip(t, 0.0, 1.0)
    projected = a + t[:, None] * edge
    return np.linalg.norm(query - projected, axis=1)


def point_to_curve_distance(
    query: np.ndarray,
    target_segments: Sequence[Segment],
) -> np.ndarray:
    """Distances to the union of target visible polylines."""
    best = np.full(len(query), np.inf, dtype=np.float64)
    for segment in target_segments:
        for index in range(len(segment.points) - 1):
            best = np.minimum(
                best,
                point_to_segment_distance(
                    query, segment.points[index], segment.points[index + 1]
                ),
            )
    if not np.all(np.isfinite(best)):
        raise RuntimeError("Could not compute finite point-to-curve distances")
    return best


def weighted_quantile(
    values: np.ndarray,
    weights: np.ndarray,
    probability: float,
) -> float:
    """Deterministic left-continuous weighted quantile."""
    order = np.argsort(values, kind="mergesort")
    values = values[order]
    weights = weights[order]
    cumulative = np.cumsum(weights) / float(np.sum(weights))
    index = int(np.searchsorted(cumulative, probability, side="left"))
    return float(values[min(index, len(values) - 1)])


def weighted_stats(values: np.ndarray, weights: np.ndarray) -> dict[str, float]:
    """Frozen descriptive statistics."""
    values = np.asarray(values, dtype=np.float64)
    weights = np.asarray(weights, dtype=np.float64)
    weights = weights / float(np.sum(weights))
    return {
        "median": weighted_quantile(values, weights, 0.50),
        "rms": float(np.sqrt(np.sum(weights * values * values))),
        "p95": weighted_quantile(values, weights, 0.95),
        "maximum": float(np.max(values)),
    }


def symmetric_pass_agreement(
    pass1: ResampledCurve,
    pass1_segments: Sequence[Segment],
    pass2: ResampledCurve,
    pass2_segments: Sequence[Segment],
) -> dict[str, Any]:
    """Directed and symmetric agreement without forced segment correspondence."""
    d12 = point_to_curve_distance(pass1.points, pass2_segments)
    d21 = point_to_curve_distance(pass2.points, pass1_segments)

    symmetric_values = np.concatenate((d12, d21))
    symmetric_weights = np.concatenate((0.5 * pass1.weights, 0.5 * pass2.weights))
    normalized = np.concatenate((d12 / pass1.sigma_px, d21 / pass2.sigma_px))
    symmetric = weighted_stats(symmetric_values, symmetric_weights)

    return {
        "pass1_to_pass2_px": weighted_stats(d12, pass1.weights),
        "pass2_to_pass1_px": weighted_stats(d21, pass2.weights),
        "symmetric_px": symmetric,
        "symmetric_over_source_sigma": weighted_stats(normalized, symmetric_weights),
        "manual_review_trigger_px": MANUAL_REVIEW_MEDIAN_PX,
        "manual_review_required": bool(
            symmetric["median"] > MANUAL_REVIEW_MEDIAN_PX
        ),
    }


def combined_points(
    sample_sets: Sequence[ResampledCurve],
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Combine one/two passes with equal top-level pass weight."""
    if len(sample_sets) not in {1, 2}:
        raise ValueError("expected one or two passes")
    pass_weight = 1.0 / len(sample_sets)
    points = np.vstack([sample.points for sample in sample_sets])
    sigma = np.concatenate([sample.sigma_px for sample in sample_sets])
    weights = np.concatenate(
        [pass_weight * sample.weights for sample in sample_sets]
    )
    weights /= float(np.sum(weights))
    return points, sigma, weights


def residual_summary(
    signed_residual: np.ndarray,
    sigma_px: np.ndarray,
    weights: np.ndarray,
    limb_radius_px: float,
) -> dict[str, Any]:
    absolute = np.abs(signed_residual)
    return {
        "absolute_px": weighted_stats(absolute, weights),
        "absolute_over_source_sigma": weighted_stats(absolute / sigma_px, weights),
        "absolute_over_limb_radius": weighted_stats(
            absolute / limb_radius_px, weights
        ),
    }


def fit_circle(
    sample_sets: Sequence[ResampledCurve],
    limb_radius_px: float,
) -> dict[str, Any]:
    """Weighted geometric circle fit with normalized numerical coordinates.

    The scientific objective remains the weighted exact radial residual.
    Coordinate normalization and the weighted algebraic circle are used
    only to make the nonlinear optimization numerically well conditioned.
    """
    points, sigma, weights = combined_points(
        sample_sets
    )

    origin = np.sum(
        points
        * weights[:, None],
        axis=0,
    )

    centered = (
        points
        - origin
    )

    normalization_scale = float(
        np.sqrt(
            np.sum(
                weights
                * np.sum(
                    centered
                    * centered,
                    axis=1,
                )
            )
        )
    )

    if not (
        math.isfinite(
            normalization_scale
        )
        and normalization_scale > 1.0e-12
    ):
        raise RuntimeError(
            "Circle fit has insufficient geometric spread."
        )

    normalized = (
        centered
        / normalization_scale
    )

    x = normalized[:, 0]
    y = normalized[:, 1]

    # Weighted algebraic circle seed:
    #
    # x^2 + y^2 =
    #     2*cx*x + 2*cy*y + q
    #
    # with
    #
    # r^2 = q + cx^2 + cy^2.
    design = np.column_stack(
        (
            2.0 * x,
            2.0 * y,
            np.ones_like(x),
        )
    )

    target = (
        x * x
        + y * y
    )

    sqrt_weights = np.sqrt(
        weights
    )

    solution, _, rank, _ = (
        np.linalg.lstsq(
            design
            * sqrt_weights[:, None],
            target
            * sqrt_weights,
            rcond=None,
        )
    )

    seed_kind = (
        "weighted_algebraic_circle"
    )

    center_x0 = float(
        solution[0]
    )
    center_y0 = float(
        solution[1]
    )

    radius_squared0 = float(
        solution[2]
        + center_x0 * center_x0
        + center_y0 * center_y0
    )

    if (
        rank < 3
        or not math.isfinite(
            radius_squared0
        )
        or radius_squared0 <= 0.0
    ):
        # Deterministic numerical fallback only.
        # This does not alter the objective being minimized.
        center_x0 = 0.0
        center_y0 = 0.0

        radius0 = float(
            np.sum(
                weights
                * np.linalg.norm(
                    normalized,
                    axis=1,
                )
            )
        )

        seed_kind = (
            "weighted_centroid_fallback"
        )
    else:
        radius0 = math.sqrt(
            radius_squared0
        )

    if not (
        math.isfinite(
            radius0
        )
        and radius0 > 0.0
    ):
        raise RuntimeError(
            "Circle fit produced an invalid initial radius."
        )

    def objective(
        parameters: np.ndarray,
    ) -> np.ndarray:
        center_x = float(
            parameters[0]
        )
        center_y = float(
            parameters[1]
        )
        radius = float(
            parameters[2]
        )

        radial = np.linalg.norm(
            normalized
            - np.asarray(
                [
                    center_x,
                    center_y,
                ],
                dtype=np.float64,
            ),
            axis=1,
        )

        return (
            radial
            - radius
        ) * sqrt_weights

    result = least_squares(
        objective,
        np.asarray(
            [
                center_x0,
                center_y0,
                radius0,
            ],
            dtype=np.float64,
        ),
        bounds=(
            np.asarray(
                [
                    -np.inf,
                    -np.inf,
                    1.0e-12,
                ],
                dtype=np.float64,
            ),
            np.asarray(
                [
                    np.inf,
                    np.inf,
                    np.inf,
                ],
                dtype=np.float64,
            ),
        ),
        method="trf",
        x_scale="jac",
        max_nfev=20000,
        xtol=1.0e-10,
        ftol=1.0e-10,
        gtol=1.0e-10,
    )

    if not result.success:
        raise RuntimeError(
            "Circle fit failed after normalized geometric "
            "optimization: "
            f"{result.message}; "
            f"nfev={result.nfev}; "
            f"optimality={result.optimality:.6e}"
        )

    center_normalized = np.asarray(
        [
            result.x[0],
            result.x[1],
        ],
        dtype=np.float64,
    )

    center = (
        origin
        + normalization_scale
        * center_normalized
    )

    radius = float(
        normalization_scale
        * result.x[2]
    )

    residual = (
        np.linalg.norm(
            points
            - center,
            axis=1,
        )
        - radius
    )

    return {
        "model": "circle",
        "center_x_px": float(
            center[0]
        ),
        "center_y_px": float(
            center[1]
        ),
        "radius_px": radius,
        "residual_definition": (
            "signed exact radial circle residual"
        ),
        "solver": {
            "objective": (
                "equal-pass arc-length-weighted geometric "
                "radial least squares"
            ),
            "coordinate_normalization": (
                "weighted-centroid translation and weighted "
                "RMS radial scale"
            ),
            "initialization": seed_kind,
            "algebraic_seed_rank": int(
                rank
            ),
            "success": bool(
                result.success
            ),
            "nfev": int(
                result.nfev
            ),
            "optimality": float(
                result.optimality
            ),
        },
        "residuals": residual_summary(
            residual,
            sigma,
            weights,
            limb_radius_px,
        ),
    }


def ellipse_radial_residual(
    points: np.ndarray,
    cx: float,
    cy: float,
    semi_major: float,
    semi_minor: float,
    angle: float,
) -> np.ndarray:
    """Signed center-radial residual from a rotated descriptive ellipse."""
    c = math.cos(angle)
    s = math.sin(angle)
    dx = points[:, 0] - cx
    dy = points[:, 1] - cy
    local_x = c * dx + s * dy
    local_y = -s * dx + c * dy
    observed_r = np.hypot(local_x, local_y)
    phi = np.arctan2(local_y, local_x)
    ellipse_r = 1.0 / np.sqrt(
        (np.cos(phi) / semi_major) ** 2
        + (np.sin(phi) / semi_minor) ** 2
    )
    return observed_r - ellipse_r


def fit_ellipse(
    sample_sets: Sequence[ResampledCurve],
    limb_radius_px: float,
) -> dict[str, Any]:
    """Weighted descriptive rotated-ellipse fit."""
    points, sigma, weights = combined_points(sample_sets)
    circle = fit_circle(sample_sets, limb_radius_px)
    cx0 = float(circle["center_x_px"])
    cy0 = float(circle["center_y_px"])
    r0 = float(circle["radius_px"])

    centered = points - np.sum(points * weights[:, None], axis=0)
    covariance = centered.T @ (centered * weights[:, None])
    _, eigenvectors = np.linalg.eigh(covariance)
    major = eigenvectors[:, -1]
    angle0 = math.atan2(float(major[1]), float(major[0]))

    span = max(float(np.ptp(points[:, 0])), float(np.ptp(points[:, 1])), 10.0)
    min_axis = max(1.0, 0.01 * span)
    max_axis = 30.0 * span

    def objective(parameters: np.ndarray) -> np.ndarray:
        cx, cy, log_a, log_b, angle = parameters
        a = math.exp(float(log_a))
        b = math.exp(float(log_b))
        return (
            ellipse_radial_residual(points, cx, cy, a, b, angle)
            * np.sqrt(weights)
        )

    lower = np.asarray(
        [
            np.min(points[:, 0])
            - 10.0 * span,
            np.min(points[:, 1])
            - 10.0 * span,
            math.log(
                min_axis
            ),
            math.log(
                min_axis
            ),
            -math.pi,
        ],
        dtype=np.float64,
    )

    upper = np.asarray(
        [
            np.max(points[:, 0])
            + 10.0 * span,
            np.max(points[:, 1])
            + 10.0 * span,
            math.log(
                max_axis
            ),
            math.log(
                max_axis
            ),
            math.pi,
        ],
        dtype=np.float64,
    )

    # The circle fit is only an ellipse solver seed.
    # Clip it strictly inside the already-frozen ellipse
    # admissible bounds; this does not change those bounds.
    center_x0 = float(
        np.clip(
            cx0,
            lower[0]
            + 1.0e-9,
            upper[0]
            - 1.0e-9,
        )
    )

    center_y0 = float(
        np.clip(
            cy0,
            lower[1]
            + 1.0e-9,
            upper[1]
            - 1.0e-9,
        )
    )

    semi_major0 = float(
        np.clip(
            1.02 * r0,
            min_axis
            * (
                1.0
                + 1.0e-9
            ),
            max_axis
            * (
                1.0
                - 1.0e-9
            ),
        )
    )

    semi_minor0 = float(
        np.clip(
            0.98 * r0,
            min_axis
            * (
                1.0
                + 1.0e-9
            ),
            max_axis
            * (
                1.0
                - 1.0e-9
            ),
        )
    )

    result = least_squares(
        objective,
        np.asarray(
            [
                center_x0,
                center_y0,
                math.log(
                    semi_major0
                ),
                math.log(
                    semi_minor0
                ),
                angle0,
            ],
            dtype=np.float64,
        ),
        bounds=(
            lower,
            upper,
        ),
        method="trf",
        x_scale="jac",
        max_nfev=20000,
        xtol=1.0e-10,
        ftol=1.0e-10,
        gtol=1.0e-10,
    )
    if not result.success:
        raise RuntimeError("Ellipse fit failed: " + result.message)

    cx = float(result.x[0])
    cy = float(result.x[1])
    a = math.exp(float(result.x[2]))
    b = math.exp(float(result.x[3]))
    angle = float(result.x[4])
    if b > a:
        a, b = b, a
        angle += 0.5 * math.pi
    while angle < -0.5 * math.pi:
        angle += math.pi
    while angle >= 0.5 * math.pi:
        angle -= math.pi

    residual = ellipse_radial_residual(points, cx, cy, a, b, angle)
    return {
        "model": "ellipse",
        "center_x_px": cx,
        "center_y_px": cy,
        "semi_major_px": a,
        "semi_minor_px": b,
        "axis_ratio_minor_over_major": b / a,
        "angle_radians": angle,
        "angle_degrees": math.degrees(angle),
        "residual_definition": (
            "signed center-radial image-space residual; not an "
            "orthogonal-distance or great-circle claim"
        ),
        "residuals": residual_summary(residual, sigma, weights, limb_radius_px),
    }


def load_frozen_limb_reference() -> dict[str, float]:
    """Regenerate and extract the previously frozen neutral limb circle.

    This function deliberately calls the original neutral geometry census,
    because that census owns the equator-at-horizon limb fit. The later
    expanded census adds incidence landmarks but does not redefine the
    frozen limb geometry.
    """
    if not NEUTRAL_GEOMETRY_SCRIPT.exists():
        raise RuntimeError(
            "Missing frozen neutral geometry script: "
            f"{NEUTRAL_GEOMETRY_SCRIPT}"
        )

    root_text = str(ROOT)

    if root_text not in sys.path:
        sys.path.insert(
            0,
            root_text,
        )

    spec = importlib.util.spec_from_file_location(
        "first_hand_neutral_geometry_for_curve_audit",
        NEUTRAL_GEOMETRY_SCRIPT,
    )

    if spec is None or spec.loader is None:
        raise RuntimeError(
            "Could not load frozen neutral geometry module."
        )

    module = importlib.util.module_from_spec(
        spec
    )

    spec.loader.exec_module(
        module
    )

    analysis, _, _ = module.build_analysis()

    if "limb_geometry" not in analysis:
        raise RuntimeError(
            "Frozen neutral analysis does not expose limb_geometry."
        )

    limb_geometry = analysis[
        "limb_geometry"
    ]

    if "equal_pass_weight_circle" not in limb_geometry:
        raise RuntimeError(
            "Frozen neutral limb geometry does not expose "
            "equal_pass_weight_circle."
        )

    circle = limb_geometry[
        "equal_pass_weight_circle"
    ]

    required = {
        "center_x_px",
        "center_y_px",
        "radius_px",
    }

    missing = (
        required
        - set(circle)
    )

    if missing:
        raise RuntimeError(
            "Frozen limb circle is missing fields: "
            + ", ".join(
                sorted(
                    missing
                )
            )
        )

    result = {
        "center_x_px": float(
            circle[
                "center_x_px"
            ]
        ),
        "center_y_px": float(
            circle[
                "center_y_px"
            ]
        ),
        "radius_px": float(
            circle[
                "radius_px"
            ]
        ),
    }

    if not (
        math.isfinite(
            result[
                "center_x_px"
            ]
        )
        and math.isfinite(
            result[
                "center_y_px"
            ]
        )
        and math.isfinite(
            result[
                "radius_px"
            ]
        )
        and result[
            "radius_px"
        ] > 0.0
    ):
        raise RuntimeError(
            "Frozen neutral limb reference is invalid."
        )

    return result


def fit_bundle(
    pass1: ResampledCurve,
    pass2: ResampledCurve,
    limb_radius_px: float,
) -> dict[str, Any]:
    return {
        "pass1": {
            "circle": fit_circle([pass1], limb_radius_px),
            "ellipse": fit_ellipse([pass1], limb_radius_px),
        },
        "pass2": {
            "circle": fit_circle([pass2], limb_radius_px),
            "ellipse": fit_ellipse([pass2], limb_radius_px),
        },
        "equal_pass_combined": {
            "circle": fit_circle([pass1, pass2], limb_radius_px),
            "ellipse": fit_ellipse([pass1, pass2], limb_radius_px),
        },
    }


def analyze_curve_at_spacing(
    curve_id: str,
    pass1_segments: Sequence[Segment],
    pass2_segments: Sequence[Segment],
    spacing_px: float,
    limb_radius_px: float,
) -> dict[str, Any]:
    pass1 = resample_curve(pass1_segments, spacing_px)
    pass2 = resample_curve(pass2_segments, spacing_px)
    return {
        "curve_id": curve_id,
        "resampling_spacing_px": spacing_px,
        "pass1": {
            "segment_count": len(pass1_segments),
            "resampled_point_count": len(pass1.points),
            "observed_arc_length_px": pass1.total_arc_length_px,
        },
        "pass2": {
            "segment_count": len(pass2_segments),
            "resampled_point_count": len(pass2.points),
            "observed_arc_length_px": pass2.total_arc_length_px,
        },
        "pass_agreement": symmetric_pass_agreement(
            pass1, pass1_segments, pass2, pass2_segments
        ),
        "image_space_fits": fit_bundle(pass1, pass2, limb_radius_px),
    }


def build_analysis() -> dict[str, Any]:
    """Build the real-data result only after this implementation is frozen."""
    verified = verify_input_seal()
    passes = {
        pass_number: read_curve_pass(path, pass_number)
        for pass_number, path in PASS_PATHS.items()
    }
    limb = load_frozen_limb_reference()
    limb_radius = float(limb["radius_px"])

    curves: dict[str, Any] = {}
    for curve_id in CURVE_IDS:
        primary = analyze_curve_at_spacing(
            curve_id,
            passes[1][curve_id],
            passes[2][curve_id],
            PRIMARY_SPACING_PX,
            limb_radius,
        )
        primary["analysis_partition"] = (
            "calibration_labelled_curve"
            if curve_id in CALIBRATION_IDS
            else "independent_scaffold_holdout"
        )
        primary["sampling_sensitivity"] = {}
        for spacing in SENSITIVITY_SPACINGS_PX:
            result = analyze_curve_at_spacing(
                curve_id,
                passes[1][curve_id],
                passes[2][curve_id],
                spacing,
                limb_radius,
            )
            primary["sampling_sensitivity"][format(spacing, ".1f")] = {
                "resampling_spacing_px": spacing,
                "pass_agreement_symmetric_px": result["pass_agreement"][
                    "symmetric_px"
                ],
                "combined_circle_absolute_px": result["image_space_fits"][
                    "equal_pass_combined"
                ]["circle"]["residuals"]["absolute_px"],
                "combined_ellipse_absolute_px": result["image_space_fits"][
                    "equal_pass_combined"
                ]["ellipse"]["residuals"]["absolute_px"],
            }
        curves[curve_id] = primary

    review_ids = [
        curve_id
        for curve_id, curve in curves.items()
        if curve["pass_agreement"]["manual_review_required"]
    ]

    return {
        "checkpoint": "first_hand_curve_geometry_v0.8",
        "raw_observation_checkpoint": "85ab104",
        "protocol_checkpoint": "7cd3868",
        "provenance": {
            "input_sha256_manifest": str(SEAL_PATH.relative_to(ROOT)),
            "verified_curve_inputs": verified,
            "frozen_limb_reference": limb,
        },
        "method": {
            "primary_resampling_spacing_px": PRIMARY_SPACING_PX,
            "sensitivity_resampling_spacings_px": list(
                SENSITIVITY_SPACINGS_PX
            ),
            "pass_weights": {"pass1": 0.5, "pass2": 0.5},
            "within_pass_weighting": "visible polyline arc length",
            "segment_correspondence_forced": False,
            "curve_sigma_floor_px": CURVE_SIGMA_FLOOR_PX,
            "manual_review_median_threshold_px": MANUAL_REVIEW_MEDIAN_PX,
        },
        "partitions": {
            "calibration_labelled_curves": list(CALIBRATION_IDS),
            "independent_scaffold_holdout": HOLDOUT_ID,
        },
        "curves": curves,
        "manual_review": {
            "triggered_curve_ids": review_ids,
            "any_triggered": bool(review_ids),
        },
        "scope": {
            "raw_image_space_curve_geometry_computed": True,
            "limb_normalized_residuals_computed": True,
            "projective_map_fitted": False,
            "projective_gauge_selected": False,
            "spherical_scale_selected": False,
            "great_circle_certification_issued": False,
            "reciprocal_spiral_verdict_issued": False,
            "s1_computed": False,
            "s1_5_computed": False,
            "s2_computed": False,
        },
        "interpretation_boundary": (
            "The page-7 source is a hand drawing. These are model-neutral "
            "image-space diagnostics. Residuals comparable with stroke width, "
            "pass variation, or digitization sensitivity may support "
            "compatibility with an intended construction but cannot certify "
            "exact mathematical incidence."
        ),
    }


def render_report(analysis: dict[str, Any]) -> str:
    lines = [
        "# First Hand two-pass curve geometry audit",
        "",
        "**Status:** model-neutral image-space result",
        "",
        "## Pass agreement",
        "",
        "| Curve | Partition | Median px | RMS px | P95 px | Max px | Review |",
        "|---|---|---:|---:|---:|---:|---|",
    ]
    for curve_id in CURVE_IDS:
        curve = analysis["curves"][curve_id]
        stats = curve["pass_agreement"]["symmetric_px"]
        lines.append(
            "| "
            f"`{curve_id}` | {curve['analysis_partition']} | "
            f"{stats['median']:.6f} | {stats['rms']:.6f} | "
            f"{stats['p95']:.6f} | {stats['maximum']:.6f} | "
            f"{'REVIEW' if curve['pass_agreement']['manual_review_required'] else 'PASS'} |"
        )

    lines += [
        "",
        "## Equal-pass combined descriptive fits",
        "",
        "| Curve | Circle RMS px | Ellipse RMS px | Ellipse b/a |",
        "|---|---:|---:|---:|",
    ]
    for curve_id in CURVE_IDS:
        fits = analysis["curves"][curve_id]["image_space_fits"][
            "equal_pass_combined"
        ]
        lines.append(
            "| "
            f"`{curve_id}` | "
            f"{fits['circle']['residuals']['absolute_px']['rms']:.6f} | "
            f"{fits['ellipse']['residuals']['absolute_px']['rms']:.6f} | "
            f"{fits['ellipse']['axis_ratio_minor_over_major']:.9f} |"
        )

    lines += [
        "",
        "## Scope boundary",
        "",
        f"`{HOLDOUT_ID}` remains an independent holdout.",
        "",
        "No projective map, projective gauge, spherical scale, great-circle "
        "certification, reciprocal-spiral verdict, S1, S1.5, or S2 is produced.",
        "",
        "The source is hand-drawn; image-space residuals do not certify exact "
        "mathematical incidence.",
        "",
    ]
    return "\n".join(lines)


def write_outputs(analysis: dict[str, Any]) -> None:
    OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_JSON.write_text(
        json.dumps(analysis, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    OUTPUT_REPORT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_REPORT.write_text(render_report(analysis), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Model-neutral First Hand two-pass curve geometry audit."
    )
    parser.add_argument(
        "--check-inputs",
        action="store_true",
        help=(
            "Verify frozen hashes and parse both passes only. "
            "No curve geometry is computed."
        ),
    )
    args = parser.parse_args()

    if args.check_inputs:
        verified = verify_input_seal()
        for pass_number, path in PASS_PATHS.items():
            curves = read_curve_pass(path, pass_number)
            print(
                f"Pass {pass_number}: "
                f"{sum(len(v) for v in curves.values())} segments, "
                f"{len(curves)} curves"
            )
        print(f"Verified {len(verified)} sealed input files.")
        print("No curve geometry was computed.")
        return 0

    analysis = build_analysis()
    write_outputs(analysis)
    print("=" * 78)
    print("FIRST HAND TWO-PASS CURVE GEOMETRY AUDIT")
    print("=" * 78)
    for curve_id in CURVE_IDS:
        stats = analysis["curves"][curve_id]["pass_agreement"]["symmetric_px"]
        print(
            f"{curve_id}: median={stats['median']:.6f} px, "
            f"RMS={stats['rms']:.6f} px, P95={stats['p95']:.6f} px"
        )
    print(
        "Manual review triggered: "
        f"{analysis['manual_review']['any_triggered']}"
    )
    print(f"Wrote {OUTPUT_JSON}")
    print(f"Wrote {OUTPUT_REPORT}")
    print(
        "No projective map, scale, great-circle verdict, "
        "or self-embedment score was computed."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
