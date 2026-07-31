#!/usr/bin/env python3
"""Neutral two-pass geometry census for the First Hand source diagram.

Uses only the frozen source crop and the two blind neutral passes. It does
not fit a projective map, assign great-circle endpoints, select a scale,
or compute S1, S1.5, S2, or any self-embedment verdict.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from collections import defaultdict
from pathlib import Path
from typing import Any, Iterable, Sequence

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from scipy.optimize import least_squares
from scipy.spatial import cKDTree

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/derived/first_hand_arm_of_god"
PASS_PATHS = {
    1: DATA / "diagram_landmarks_pass1.csv",
    2: DATA / "diagram_landmarks_pass2.csv",
}
CHECKSUM_PATH = DATA / "diagram_landmark_passes.sha256"
CROP_MANIFEST = ROOT / "data/source_manifests/first_hand_arm_of_god/diagram_crop_manifest.csv"
CONSENSUS_PATH = DATA / "neutral_landmark_consensus.csv"
RESULT_PATH = DATA / "neutral_geometry_census.json"
REPORT_PATH = ROOT / "reports/first_hand_neutral_geometry_census.md"
FIGURE_PATH = ROOT / "figures/first_hand_neutral_geometry_overlay.png"

LIMB_ID = "AOG-LM-P07-EQUATOR-HORIZON-LIMB"
RIM_IDS = (
    "AOG-LM-P07-RIM-NODE-UR",
    "AOG-LM-P07-RIM-NODE-R",
    "AOG-LM-P07-RIM-NODE-LR-SHARED",
    "AOG-LM-P07-RIM-NODE-LL",
    "AOG-LM-P07-RIM-NODE-L",
    "AOG-LM-P07-RIM-NODE-UL",
)
CENTRAL_ID = "AOG-LM-P07-CENTRAL-REFERENCE-NODE"
CROSSING_ID = "AOG-LM-P07-UPPER-INTERIOR-CROSSING"
PANEL_IDS = (
    "AOG-LM-P07-FLAT-UNIT-R1-THETA1RAD",
    "AOG-LM-P07-SPHERE-UNIT-R1-ONEMONTH",
    "AOG-LM-P07-FLAT-INNER-END",
    "AOG-LM-P07-SPHERE-INNER-END",
)
EXPECTED_IDS = {LIMB_ID, *RIM_IDS, CENTRAL_ID, CROSSING_ID, *PANEL_IDS}
POINT_FLOOR = {landmark_id: 2.0 for landmark_id in (*RIM_IDS, CENTRAL_ID, CROSSING_ID)}
POINT_FLOOR.update({landmark_id: 3.0 for landmark_id in PANEL_IDS})

CONSENSUS_FIELDS = [
    "landmark_id", "source_feature", "fit_partition",
    "pass1_x_px", "pass1_y_px", "pass2_x_px", "pass2_y_px",
    "consensus_x_px", "consensus_y_px", "pass_separation_px",
    "pass1_stroke_width_px", "pass2_stroke_width_px",
    "uncertainty_floor_px", "consensus_uncertainty_px",
    "crop_file_sha256", "crop_pixel_sha256",
]


def sha256_path(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def group_rows(rows: Iterable[dict[str, str]]) -> dict[str, list[dict[str, str]]]:
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        grouped[row["landmark_id"]].append(row)
    for values in grouped.values():
        values.sort(key=lambda row: int(row["sequence_index"]))
    return dict(grouped)


def rows_to_points(rows: Sequence[dict[str, str]]) -> np.ndarray:
    return np.asarray([(float(row["x_px"]), float(row["y_px"])) for row in rows], dtype=float)


def verify_checksum_manifest(path: Path = CHECKSUM_PATH) -> dict[str, str]:
    expected: dict[str, str] = {}
    for raw in path.read_text(encoding="utf-8").splitlines():
        if not raw.strip():
            continue
        parts = raw.split()
        if len(parts) != 2:
            raise RuntimeError(f"Malformed checksum line: {raw!r}")
        digest, filename = parts
        target = path.parent / filename
        if not target.exists() or sha256_path(target) != digest:
            raise RuntimeError(f"Checksum verification failed for {target}")
        expected[filename] = digest
    required = {PASS_PATHS[1].name, PASS_PATHS[2].name}
    if set(expected) != required:
        raise RuntimeError("Checksum manifest must contain exactly the two pass CSV files.")
    return expected


def validate_pass(pass_number: int, path: Path) -> list[dict[str, str]]:
    rows = read_csv(path)
    if not rows:
        raise RuntimeError(f"Empty pass file: {path}")
    if {int(row["pass_number"]) for row in rows} != {pass_number}:
        raise RuntimeError(f"Wrong pass number in {path}")
    if len({row["crop_file_sha256"] for row in rows}) != 1:
        raise RuntimeError(f"Multiple crop hashes in {path}")
    if len({row["crop_pixel_sha256"] for row in rows}) != 1:
        raise RuntimeError(f"Multiple pixel hashes in {path}")
    grouped = group_rows(rows)
    if set(grouped) != EXPECTED_IDS:
        raise RuntimeError(
            f"Unexpected landmark vocabulary in {path}: "
            f"missing={sorted(EXPECTED_IDS-set(grouped))}, extra={sorted(set(grouped)-EXPECTED_IDS)}"
        )
    if len(grouped[LIMB_ID]) < 30:
        raise RuntimeError(f"Too few limb samples in {path}")
    for landmark_id in EXPECTED_IDS - {LIMB_ID}:
        if len(grouped[landmark_id]) != 1:
            raise RuntimeError(f"{landmark_id} must occur exactly once in pass {pass_number}")
    for landmark_id, values in grouped.items():
        indices = sorted(int(row["sequence_index"]) for row in values)
        if indices != list(range(len(indices))):
            raise RuntimeError(f"Non-contiguous indices for {landmark_id} in pass {pass_number}")
    return rows


def equal_pass_weights(n1: int, n2: int) -> np.ndarray:
    if n1 <= 0 or n2 <= 0:
        raise ValueError("Pass counts must be positive")
    return np.r_[np.full(n1, 0.5 / n1), np.full(n2, 0.5 / n2)]


def fit_circle(points: np.ndarray, weights: np.ndarray | None = None) -> dict[str, float]:
    points = np.asarray(points, dtype=float)
    if points.ndim != 2 or points.shape[1] != 2 or len(points) < 3:
        raise ValueError("points must have shape (N,2), N>=3")
    weights = np.ones(len(points)) if weights is None else np.asarray(weights, dtype=float)
    if weights.shape != (len(points),) or np.any(weights <= 0):
        raise ValueError("weights must be positive with shape (N,)")
    x, y = points[:, 0], points[:, 1]
    sw = np.sqrt(weights)
    matrix = np.c_[2*x, 2*y, np.ones(len(points))]
    target = x*x + y*y
    solution, *_ = np.linalg.lstsq(matrix * sw[:, None], target * sw, rcond=None)
    cx0, cy0 = float(solution[0]), float(solution[1])
    r20 = float(solution[2] + cx0*cx0 + cy0*cy0)
    if r20 <= 0:
        raise RuntimeError("Non-positive initial circle radius")
    r0 = math.sqrt(r20)

    def residual(parameters: np.ndarray) -> np.ndarray:
        cx, cy, radius = parameters
        return (np.hypot(x-cx, y-cy) - radius) * sw

    fitted = least_squares(
        residual,
        np.asarray([cx0, cy0, r0]),
        bounds=([-np.inf, -np.inf, 1e-12], [np.inf, np.inf, np.inf]),
    )
    cx, cy, radius = map(float, fitted.x)
    raw = np.hypot(x-cx, y-cy) - radius
    return {
        "center_x_px": cx,
        "center_y_px": cy,
        "radius_px": radius,
        "rms_radial_residual_px": float(np.sqrt(np.mean(raw**2))),
        "weighted_rms_radial_residual_px": float(np.sqrt(np.sum(weights*raw**2)/np.sum(weights))),
        "max_abs_radial_residual_px": float(np.max(np.abs(raw))),
        "sample_count": int(len(points)),
    }


def fit_ellipse_radial(points: np.ndarray, weights: np.ndarray | None = None) -> dict[str, float]:
    """Descriptive ellipse fit; residual is approximate radial pixels."""
    points = np.asarray(points, dtype=float)
    if len(points) < 5:
        raise ValueError("At least five points required")
    weights = np.ones(len(points)) if weights is None else np.asarray(weights, dtype=float)
    weights = weights / np.sum(weights)
    center0 = np.sum(points * weights[:, None], axis=0)
    centered = points - center0
    covariance = centered.T @ (centered * weights[:, None])
    eigenvalues, eigenvectors = np.linalg.eigh(covariance)
    order = np.argsort(eigenvalues)[::-1]
    eigenvalues, eigenvectors = eigenvalues[order], eigenvectors[:, order]
    a0 = math.sqrt(max(2*float(eigenvalues[0]), 1.0))
    b0 = math.sqrt(max(2*float(eigenvalues[1]), 1.0))
    v = eigenvectors[:, 0]
    angle0 = math.atan2(float(v[1]), float(v[0]))
    sw = np.sqrt(weights)

    def raw(parameters: np.ndarray) -> tuple[np.ndarray, float, float]:
        cx, cy, log_a, log_b, angle = parameters
        a, b = math.exp(float(log_a)), math.exp(float(log_b))
        c, s = math.cos(float(angle)), math.sin(float(angle))
        dx, dy = points[:, 0]-cx, points[:, 1]-cy
        xr, yr = c*dx+s*dy, -s*dx+c*dy
        rho = np.sqrt((xr/a)**2 + (yr/b)**2)
        return (rho-1.0)*math.sqrt(a*b), a, b

    initial = np.asarray([center0[0], center0[1], math.log(a0), math.log(b0), angle0])
    fitted = least_squares(lambda p: raw(p)[0] * sw, initial)
    cx, cy, log_a, log_b, angle = map(float, fitted.x)
    a, b = math.exp(log_a), math.exp(log_b)
    if b > a:
        a, b = b, a
        angle += math.pi/2
    angle %= math.pi
    residual, _, _ = raw(np.asarray([cx, cy, math.log(a), math.log(b), angle]))
    return {
        "center_x_px": cx,
        "center_y_px": cy,
        "semi_major_px": a,
        "semi_minor_px": b,
        "axis_ratio_minor_major": b/a,
        "major_axis_angle_deg_image": math.degrees(angle),
        "rms_approx_radial_residual_px": float(np.sqrt(np.mean(residual**2))),
        "weighted_rms_approx_radial_residual_px": float(np.sqrt(np.sum(weights*residual**2))),
        "max_abs_approx_radial_residual_px": float(np.max(np.abs(residual))),
        "sample_count": int(len(points)),
    }


def symmetric_chamfer(points1: np.ndarray, points2: np.ndarray) -> dict[str, Any]:
    d12 = cKDTree(points2).query(points1, k=1)[0]
    d21 = cKDTree(points1).query(points2, k=1)[0]

    def summary(values: np.ndarray) -> dict[str, float]:
        return {
            "rms_px": float(np.sqrt(np.mean(values**2))),
            "median_px": float(np.median(values)),
            "p95_px": float(np.percentile(values, 95)),
            "max_px": float(np.max(values)),
        }

    return {
        "pass1_to_pass2": summary(d12),
        "pass2_to_pass1": summary(d21),
        "equal_direction_symmetric_rms_px": float(math.sqrt(0.5*(np.mean(d12**2)+np.mean(d21**2)))),
    }


def point_consensus(pass1: Sequence[dict[str, str]], pass2: Sequence[dict[str, str]]) -> list[dict[str, str]]:
    grouped1, grouped2 = group_rows(pass1), group_rows(pass2)
    output: list[dict[str, str]] = []
    for landmark_id in sorted(EXPECTED_IDS - {LIMB_ID}):
        row1, row2 = grouped1[landmark_id][0], grouped2[landmark_id][0]
        if row1["crop_file_sha256"] != row2["crop_file_sha256"]:
            raise RuntimeError(f"Crop hash mismatch for {landmark_id}")
        if row1["crop_pixel_sha256"] != row2["crop_pixel_sha256"]:
            raise RuntimeError(f"Pixel hash mismatch for {landmark_id}")
        p1 = np.asarray([float(row1["x_px"]), float(row1["y_px"])])
        p2 = np.asarray([float(row2["x_px"]), float(row2["y_px"])])
        mean = (p1+p2)/2
        separation = float(np.linalg.norm(p1-p2))
        width1, width2 = float(row1["local_stroke_width_px"]), float(row2["local_stroke_width_px"])
        floor = POINT_FLOOR[landmark_id]
        uncertainty = max(floor, 0.5*max(width1, width2), 0.5*separation)
        output.append({
            "landmark_id": landmark_id,
            "source_feature": row1["source_feature"],
            "fit_partition": row1["fit_partition"],
            "pass1_x_px": f"{p1[0]:.12g}", "pass1_y_px": f"{p1[1]:.12g}",
            "pass2_x_px": f"{p2[0]:.12g}", "pass2_y_px": f"{p2[1]:.12g}",
            "consensus_x_px": f"{mean[0]:.12g}", "consensus_y_px": f"{mean[1]:.12g}",
            "pass_separation_px": f"{separation:.12g}",
            "pass1_stroke_width_px": f"{width1:.12g}",
            "pass2_stroke_width_px": f"{width2:.12g}",
            "uncertainty_floor_px": f"{floor:.12g}",
            "consensus_uncertainty_px": f"{uncertainty:.12g}",
            "crop_file_sha256": row1["crop_file_sha256"],
            "crop_pixel_sha256": row1["crop_pixel_sha256"],
        })
    return output


def consensus_lookup(rows: Sequence[dict[str, str]]) -> dict[str, np.ndarray]:
    return {
        row["landmark_id"]: np.asarray([float(row["consensus_x_px"]), float(row["consensus_y_px"])])
        for row in rows
    }


def bearing_deg(point: np.ndarray, center: np.ndarray) -> float:
    return math.degrees(math.atan2(float(center[1]-point[1]), float(point[0]-center[0]))) % 360.0


def wrap_period(value: float, period: float) -> float:
    return (value + 0.5*period) % period - 0.5*period


def fit_regular_sixfold(bearings_deg: Sequence[float]) -> dict[str, Any]:
    bearings = np.asarray(bearings_deg, dtype=float)
    if bearings.shape != (6,):
        raise ValueError("Exactly six bearings required")
    resultant = np.mean(np.exp(1j*6*np.radians(bearings)))
    phase = math.degrees(np.angle(resultant)/6) % 60.0
    residuals = np.asarray([wrap_period(value-phase, 60.0) for value in bearings])
    ordered = np.sort(bearings)
    gaps = np.diff(np.r_[ordered, ordered[0]+360.0])
    return {
        "phase_deg_mod_60": phase,
        "sixfold_resultant_strength": float(abs(resultant)),
        "bearing_residuals_deg": [float(v) for v in residuals],
        "bearing_rms_residual_deg": float(np.sqrt(np.mean(residuals**2))),
        "bearing_max_abs_residual_deg": float(np.max(np.abs(residuals))),
        "sorted_bearings_deg": [float(v) for v in ordered],
        "successive_gaps_deg": [float(v) for v in gaps],
        "gap_rms_residual_from_60_deg": float(np.sqrt(np.mean((gaps-60)**2))),
        "gap_max_abs_residual_from_60_deg": float(np.max(np.abs(gaps-60))),
    }


def build_analysis() -> tuple[dict[str, Any], list[dict[str, str]], dict[int, list[dict[str, str]]]]:
    checksums = verify_checksum_manifest()
    passes = {number: validate_pass(number, path) for number, path in PASS_PATHS.items()}
    hashes1 = {row["crop_file_sha256"] for row in passes[1]}
    hashes2 = {row["crop_file_sha256"] for row in passes[2]}
    pixels1 = {row["crop_pixel_sha256"] for row in passes[1]}
    pixels2 = {row["crop_pixel_sha256"] for row in passes[2]}
    if hashes1 != hashes2 or pixels1 != pixels2:
        raise RuntimeError("The two passes do not reference the same crop")

    grouped1, grouped2 = group_rows(passes[1]), group_rows(passes[2])
    limb1, limb2 = rows_to_points(grouped1[LIMB_ID]), rows_to_points(grouped2[LIMB_ID])
    circle1, circle2 = fit_circle(limb1), fit_circle(limb2)
    pooled = np.vstack([limb1, limb2])
    weights = equal_pass_weights(len(limb1), len(limb2))
    circle = fit_circle(pooled, weights)
    ellipse = fit_ellipse_radial(pooled, weights)
    consensus_rows = point_consensus(passes[1], passes[2])
    points = consensus_lookup(consensus_rows)
    center = np.asarray([circle["center_x_px"], circle["center_y_px"]])
    radius = float(circle["radius_px"])

    rim_nodes, bearings = [], []
    for landmark_id in RIM_IDS:
        point = points[landmark_id]
        bearing = bearing_deg(point, center)
        radial = float(np.linalg.norm(point-center))
        bearings.append(bearing)
        rim_nodes.append({
            "landmark_id": landmark_id,
            "consensus_x_px": float(point[0]),
            "consensus_y_px": float(point[1]),
            "bearing_deg": bearing,
            "radial_distance_px": radial,
            "radial_residual_from_limb_circle_px": radial-radius,
        })
    sixfold = fit_regular_sixfold(bearings)
    for node, residual in zip(rim_nodes, sixfold["bearing_residuals_deg"], strict=True):
        node["sixfold_bearing_residual_deg"] = residual
    radial_residuals = np.asarray([node["radial_residual_from_limb_circle_px"] for node in rim_nodes])

    central = points[CENTRAL_ID]
    crossing = points[CROSSING_ID]
    central_offset = float(np.linalg.norm(central-center))
    crossing_offset = float(np.linalg.norm(crossing-center))
    point_agreement = sorted(
        [{
            "landmark_id": row["landmark_id"],
            "pass_separation_px": float(row["pass_separation_px"]),
            "consensus_uncertainty_px": float(row["consensus_uncertainty_px"]),
        } for row in consensus_rows],
        key=lambda item: (item["pass_separation_px"], item["landmark_id"]),
        reverse=True,
    )

    analysis = {
        "analysis_id": "first_hand_neutral_geometry_census_v0_8",
        "scope": {
            "uses_only": ["frozen prepared source crop", "blind neutral pass 1", "blind neutral pass 2"],
            "does_not_compute": [
                "projective map fit", "great-circle identity or endpoint assignment",
                "unit-angle scale selection", "truncation reconciliation",
                "S1 tangent alignment", "S1.5 Darboux-frame alignment", "S2 recursive nesting",
            ],
        },
        "provenance": {
            "checksum_manifest": str(CHECKSUM_PATH.relative_to(ROOT)),
            "checksum_manifest_sha256": sha256_path(CHECKSUM_PATH),
            "pass_file_sha256": checksums,
            "crop_id": passes[1][0]["crop_id"],
            "crop_file_sha256": next(iter(hashes1)),
            "crop_pixel_sha256": next(iter(pixels1)),
            "pass_row_counts": {"pass1": len(passes[1]), "pass2": len(passes[2])},
            "limb_sample_counts": {"pass1": len(limb1), "pass2": len(limb2)},
            "point_landmark_count": len(consensus_rows),
        },
        "pass_agreement": {
            "limb_symmetric_chamfer": symmetric_chamfer(limb1, limb2),
            "point_landmarks_by_separation_descending": point_agreement,
        },
        "limb_geometry": {
            "pass1_circle": circle1,
            "pass2_circle": circle2,
            "equal_pass_weight_circle": circle,
            "equal_pass_weight_ellipse": ellipse,
            "circle_parameter_pass_difference": {
                "center_separation_px": math.hypot(circle1["center_x_px"]-circle2["center_x_px"], circle1["center_y_px"]-circle2["center_y_px"]),
                "radius_difference_px": circle1["radius_px"]-circle2["radius_px"],
            },
            "weighting": "Each blind pass contributes total weight 0.5, independent of sample count.",
            "ellipse_residual_note": "Approximate pixel-scale normalized-radial residual, not exact orthogonal distance.",
        },
        "rim_node_census": {
            "nodes": rim_nodes,
            "radial_rms_residual_from_limb_circle_px": float(np.sqrt(np.mean(radial_residuals**2))),
            "radial_max_abs_residual_from_limb_circle_px": float(np.max(np.abs(radial_residuals))),
            "sixfold_fit": sixfold,
            "interpretation_boundary": "Sixfold regularity is an empirical image-space diagnostic, not a unique cuboctahedral or coordinate identification.",
        },
        "central_reference": {
            "landmark_id": CENTRAL_ID,
            "consensus_x_px": float(central[0]), "consensus_y_px": float(central[1]),
            "offset_from_limb_center_px": central_offset,
            "offset_fraction_of_limb_radius": central_offset/radius,
            "role": "Neutral central reference; origin or pole status is not assumed.",
        },
        "upper_interior_crossing": {
            "landmark_id": CROSSING_ID,
            "consensus_x_px": float(crossing[0]), "consensus_y_px": float(crossing[1]),
            "bearing_from_limb_center_deg": bearing_deg(crossing, center),
            "radial_distance_from_limb_center_px": crossing_offset,
            "radial_fraction_of_limb_radius": crossing_offset/radius,
            "role": "Neutral incidence landmark; curve identities remain unassigned.",
        },
        "panel_specific_landmarks": {
            landmark_id: {
                "consensus_x_px": float(points[landmark_id][0]),
                "consensus_y_px": float(points[landmark_id][1]),
                "pass_separation_px": float(next(row["pass_separation_px"] for row in consensus_rows if row["landmark_id"] == landmark_id)),
                "consensus_uncertainty_px": float(next(row["consensus_uncertainty_px"] for row in consensus_rows if row["landmark_id"] == landmark_id)),
            } for landmark_id in PANEL_IDS
        },
        "panel_comparison_boundary": "Flat and spherical panel coordinates are preserved separately; raw crop-pixel separation is not interpreted physically because the panels have different image frames.",
        "verdict": "No projection, scale, truncation, or self-embedment verdict is issued at this stage.",
    }
    return analysis, consensus_rows, passes


def write_consensus(path: Path, rows: Sequence[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=CONSENSUS_FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def build_report(analysis: dict[str, Any]) -> str:
    p = analysis["provenance"]
    limb = analysis["limb_geometry"]
    c1, c2 = limb["pass1_circle"], limb["pass2_circle"]
    circle, ellipse = limb["equal_pass_weight_circle"], limb["equal_pass_weight_ellipse"]
    rim, six = analysis["rim_node_census"], analysis["rim_node_census"]["sixfold_fit"]
    central, crossing = analysis["central_reference"], analysis["upper_interior_crossing"]
    chamfer = analysis["pass_agreement"]["limb_symmetric_chamfer"]
    f = lambda value, digits=6: f"{value:.{digits}f}"
    lines = [
        "# First Hand neutral geometry census", "",
        "**Stage:** v0.8 neutral two-pass source geometry", "",
        "## Scope", "",
        "This report uses only the frozen prepared crop and two blind neutral passes. It does not fit a projective map, assign coordinate identities, select a unit convention, reconcile truncations, or compute S1, S1.5, or S2.", "",
        "## Provenance", "",
        f"- Pass rows: `{p['pass_row_counts']['pass1']}` and `{p['pass_row_counts']['pass2']}`",
        f"- Limb samples: `{p['limb_sample_counts']['pass1']}` and `{p['limb_sample_counts']['pass2']}`",
        f"- Paired point landmarks: `{p['point_landmark_count']}`",
        f"- Crop pixel SHA-256: `{p['crop_pixel_sha256']}`", "",
        "Each pass contributes total pooled weight 0.5, so unequal click counts do not make either pass dominate.", "",
        "## Blind-pass agreement", "",
        f"- Equal-direction symmetric limb Chamfer RMS: `{f(chamfer['equal_direction_symmetric_rms_px'])} px`",
        f"- Pass-1 circle centre: `({f(c1['center_x_px'])}, {f(c1['center_y_px'])}) px`",
        f"- Pass-2 circle centre: `({f(c2['center_x_px'])}, {f(c2['center_y_px'])}) px`",
        f"- Circle-centre separation: `{f(limb['circle_parameter_pass_difference']['center_separation_px'])} px`",
        f"- Circle-radius difference: `{f(limb['circle_parameter_pass_difference']['radius_difference_px'])} px`", "",
        "## Outer limb", "",
        f"- Equal-pass circle centre: `({f(circle['center_x_px'])}, {f(circle['center_y_px'])}) px`",
        f"- Equal-pass circle radius: `{f(circle['radius_px'])} px`",
        f"- Circle weighted RMS radial residual: `{f(circle['weighted_rms_radial_residual_px'])} px`",
        f"- Circle maximum absolute radial residual: `{f(circle['max_abs_radial_residual_px'])} px`",
        f"- Ellipse semi-axes: `{f(ellipse['semi_major_px'])} px × {f(ellipse['semi_minor_px'])} px`",
        f"- Ellipse minor/major ratio: `{f(ellipse['axis_ratio_minor_major'])}`",
        f"- Ellipse weighted approximate radial RMS: `{f(ellipse['weighted_rms_approx_radial_residual_px'])} px`", "",
        "The ellipse residual is normalized-radial, not exact orthogonal distance. Circle and ellipse are descriptive rather than a model-selection verdict.", "",
        "## Rim-node census", "",
        "| Landmark | Bearing (deg) | Radial residual (px) | Sixfold residual (deg) |",
        "|---|---:|---:|---:|",
    ]
    for node in rim["nodes"]:
        lines.append(f"| `{node['landmark_id']}` | {f(node['bearing_deg'],3)} | {f(node['radial_residual_from_limb_circle_px'],3)} | {f(node['sixfold_bearing_residual_deg'],3)} |")
    lines += [
        "",
        f"- Sixfold phase modulo 60°: `{f(six['phase_deg_mod_60'])}°`",
        f"- Sixfold bearing RMS residual: `{f(six['bearing_rms_residual_deg'])}°`",
        f"- Maximum absolute bearing residual: `{f(six['bearing_max_abs_residual_deg'])}°`",
        f"- Successive-gap RMS residual from 60°: `{f(six['gap_rms_residual_from_60_deg'])}°`",
        f"- Rim radial RMS from fitted circle: `{f(rim['radial_rms_residual_from_limb_circle_px'])} px`", "",
        "These values measure image-space sixfold regularity only; they do not uniquely establish a cuboctahedral interpretation.", "",
        "## Central reference", "",
        f"- Consensus: `({f(central['consensus_x_px'])}, {f(central['consensus_y_px'])}) px`",
        f"- Offset from limb centre: `{f(central['offset_from_limb_center_px'])} px`",
        f"- Offset/radius: `{f(central['offset_fraction_of_limb_radius'],8)}`", "",
        "The point remains neutral; origin or pole status is not assumed.", "",
        "## Upper interior crossing", "",
        f"- Consensus: `({f(crossing['consensus_x_px'])}, {f(crossing['consensus_y_px'])}) px`",
        f"- Bearing from limb centre: `{f(crossing['bearing_from_limb_center_deg'])}°`",
        f"- Radial fraction: `{f(crossing['radial_fraction_of_limb_radius'])}`", "",
        "It remains an incidence landmark without assigned great-circle identities.", "",
        "## Panel-specific landmarks", "",
        "| Landmark | x (px) | y (px) | Pass separation (px) | Uncertainty (px) |",
        "|---|---:|---:|---:|---:|",
    ]
    for landmark_id in PANEL_IDS:
        item = analysis["panel_specific_landmarks"][landmark_id]
        lines.append(f"| `{landmark_id}` | {f(item['consensus_x_px'],3)} | {f(item['consensus_y_px'],3)} | {f(item['pass_separation_px'],3)} | {f(item['consensus_uncertainty_px'],3)} |")
    lines += [
        "", "Flat and spherical panel coordinates remain separate; their raw crop-pixel separation is not interpreted as an angular discrepancy.", "",
        "## Interpretation boundary", "",
        "No projective-map, great-circle, scale, truncation, or self-embedment verdict is issued.", "",
    ]
    return "\n".join(lines)


def resolve_crop(crop_id: str) -> tuple[Path, dict[str, str]]:
    matches = [row for row in read_csv(CROP_MANIFEST) if row["crop_id"] == crop_id]
    if len(matches) != 1:
        raise RuntimeError(f"Expected one crop manifest row for {crop_id}")
    return ROOT / matches[0]["output_path"], matches[0]


def write_overlay(path: Path, analysis: dict[str, Any], consensus_rows: Sequence[dict[str, str]], passes: dict[int, list[dict[str, str]]]) -> None:
    crop_path, manifest = resolve_crop(analysis["provenance"]["crop_id"])
    if sha256_path(crop_path) != manifest["file_sha256"]:
        raise RuntimeError("Prepared crop file hash mismatch")
    with Image.open(crop_path) as opened:
        image = opened.convert("RGB")
    grouped1, grouped2 = group_rows(passes[1]), group_rows(passes[2])
    limb1, limb2 = rows_to_points(grouped1[LIMB_ID]), rows_to_points(grouped2[LIMB_ID])
    circle = analysis["limb_geometry"]["equal_pass_weight_circle"]
    theta = np.linspace(0, 2*math.pi, 1000)
    cx, cy, radius = circle["center_x_px"], circle["center_y_px"], circle["radius_px"]
    figure, axis = plt.subplots(figsize=(14, 10))
    axis.imshow(image)
    axis.plot(limb1[:,0], limb1[:,1], ".-", linewidth=0.8, markersize=3, label="Blind pass 1 limb")
    axis.plot(limb2[:,0], limb2[:,1], ".-", linewidth=0.8, markersize=3, label="Blind pass 2 limb")
    axis.plot(cx+radius*np.cos(theta), cy+radius*np.sin(theta), linewidth=1.2, label="Equal-pass circle fit")
    short = {
        "AOG-LM-P07-RIM-NODE-UL":"UL", "AOG-LM-P07-RIM-NODE-UR":"UR",
        "AOG-LM-P07-RIM-NODE-R":"R", "AOG-LM-P07-RIM-NODE-LR-SHARED":"LR shared",
        "AOG-LM-P07-RIM-NODE-LL":"LL", "AOG-LM-P07-RIM-NODE-L":"L",
        CENTRAL_ID:"central", CROSSING_ID:"upper crossing",
        "AOG-LM-P07-FLAT-UNIT-R1-THETA1RAD":"flat r=1",
        "AOG-LM-P07-SPHERE-UNIT-R1-ONEMONTH":"sphere r=1",
        "AOG-LM-P07-FLAT-INNER-END":"flat inner",
        "AOG-LM-P07-SPHERE-INNER-END":"sphere inner",
    }
    for row in consensus_rows:
        x, y = float(row["consensus_x_px"]), float(row["consensus_y_px"])
        sigma = float(row["consensus_uncertainty_px"])
        axis.errorbar([x], [y], xerr=[sigma], yerr=[sigma], fmt="o", markersize=4, capsize=2)
        axis.annotate(short[row["landmark_id"]], (x,y), xytext=(5,5), textcoords="offset points", fontsize=7)
    axis.set_title("First Hand neutral two-pass geometry census")
    axis.set_xlabel("Prepared-crop x coordinate (px)")
    axis.set_ylabel("Prepared-crop y coordinate (px)")
    axis.set_xlim(0, image.width)
    axis.set_ylim(image.height, 0)
    axis.set_aspect("equal")
    axis.legend(loc="best")
    figure.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(path, dpi=180, bbox_inches="tight", metadata={"Title":"First Hand neutral geometry census"})
    plt.close(figure)


def main() -> int:
    parser = argparse.ArgumentParser(description="Compute the First Hand neutral two-pass geometry census.")
    parser.add_argument("--consensus-csv", type=Path, default=CONSENSUS_PATH)
    parser.add_argument("--result-json", type=Path, default=RESULT_PATH)
    parser.add_argument("--report", type=Path, default=REPORT_PATH)
    parser.add_argument("--figure", type=Path, default=FIGURE_PATH)
    parser.add_argument("--no-figure", action="store_true")
    args = parser.parse_args()

    analysis, consensus_rows, passes = build_analysis()
    args.consensus_csv.parent.mkdir(parents=True, exist_ok=True)
    write_consensus(args.consensus_csv, consensus_rows)
    args.result_json.parent.mkdir(parents=True, exist_ok=True)
    args.result_json.write_text(json.dumps(analysis, indent=2, sort_keys=True)+"\n", encoding="utf-8")
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(build_report(analysis), encoding="utf-8")
    if not args.no_figure:
        write_overlay(args.figure, analysis, consensus_rows, passes)

    circle = analysis["limb_geometry"]["equal_pass_weight_circle"]
    six = analysis["rim_node_census"]["sixfold_fit"]
    central = analysis["central_reference"]
    print("First Hand neutral geometry census: COMPLETE")
    print(f"Equal-pass circle centre: ({circle['center_x_px']:.6f}, {circle['center_y_px']:.6f}) px")
    print(f"Equal-pass circle radius: {circle['radius_px']:.6f} px")
    print(f"Sixfold bearing RMS residual: {six['bearing_rms_residual_deg']:.6f} deg")
    print(f"Central-reference offset/radius: {central['offset_fraction_of_limb_radius']:.8f}")
    print("No projective, scale, truncation, or self-embedment verdict was computed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
