#!/usr/bin/env python3
"""
Preregistered Variant-A ambient endpoint-parallelism evaluator.

IMPORTANT EXECUTION BOUNDARY
----------------------------
This module encodes the mathematics frozen in:

    first_hand_variant_a_ambient_parallelism_preregistration_v0.8

Importing this module does not evaluate either registered ambient endpoint
branch. Running this file without --execute-registered-ambient also evaluates
nothing.

Registered geometric branches:
    AMB-DIAGRAM-G30
    AMB-DIAGRAM-GHALF

Each branch reports both preregistered semantic interpretations:
    1. directed ambient vector angle
    2. unoriented ambient tangent-line angle

No spherical parallel transport is imported or used.
No fitting, optimization, comparator, truncation sensitivity, AOG-PROSE,
Variant-B, dimpled-sphere, image-derived, S1.5, or S2 operation is implemented.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Optional

import numpy as np

from first_hand_s1 import (
    K_G30,
    K_GHALF,
    S1_ZERO_TOL_RAD,
    directed_tangent,
    gamma_k,
)


CHECKPOINT = "first_hand_variant_a_ambient_parallelism_preregistration_v0.8"
VARIANT = "A"
TRUNCATION = "AOG-DIAGRAM"
THETA_OUTER = 1.0
THETA_INNER = 1.0 + 3.0 * math.pi

# Immutable intrinsic S1 references from the sealed S1 checkpoint.
# They are descriptive comparison inputs only and are never recomputed here.
INTRINSIC_S1_REFERENCE_DEG = {
    "G30": 144.5776221089075,
    "GHALF": 144.2022631722743,
}


@dataclass(frozen=True)
class AmbientBranchSpec:
    branch_id: str
    truncation: str
    scale: str
    k: float
    theta_outer: float
    theta_inner: float


REGISTERED_BRANCHES = (
    AmbientBranchSpec(
        branch_id="AMB-DIAGRAM-G30",
        truncation=TRUNCATION,
        scale="G30",
        k=K_G30,
        theta_outer=THETA_OUTER,
        theta_inner=THETA_INNER,
    ),
    AmbientBranchSpec(
        branch_id="AMB-DIAGRAM-GHALF",
        truncation=TRUNCATION,
        scale="GHALF",
        k=K_GHALF,
        theta_outer=THETA_OUTER,
        theta_inner=THETA_INNER,
    ),
)


@dataclass(frozen=True)
class AmbientAngleRecord:
    dot_d: float
    cross_norm_c: float
    delta_directed_rad: float
    delta_directed_deg: float
    residual_directed: float
    directed_state: str
    delta_line_rad: float
    delta_line_deg: float
    line_state: str


@dataclass
class AmbientResult:
    branch_id: str
    truncation: str
    scale: str
    k: float
    theta_outer: float
    theta_inner: float
    p_outer: Optional[list[float]]
    p_inner: Optional[list[float]]
    tau_outer: Optional[list[float]]
    tau_inner: Optional[list[float]]
    dot_d: Optional[float]
    cross_norm_c: Optional[float]
    delta_ambient_directed_rad: Optional[float]
    delta_ambient_directed_deg: Optional[float]
    residual_ambient_directed: Optional[float]
    directed_state: str
    delta_ambient_line_rad: Optional[float]
    delta_ambient_line_deg: Optional[float]
    line_state: str
    intrinsic_s1_reference_deg: float
    ambient_minus_intrinsic_deg: Optional[float]
    zero_tolerance_rad: float
    parallel_transport_used: bool
    image_pixel_data_used: bool
    technical_error: Optional[str] = None


def _as_unit_vector3(value) -> np.ndarray:
    arr = np.asarray(value, dtype=float)
    if arr.shape != (3,):
        raise ValueError(f"Expected a 3-vector, got shape {arr.shape}")
    if not np.all(np.isfinite(arr)):
        raise ValueError("Vector contains non-finite values")
    norm = float(np.linalg.norm(arr))
    if norm == 0.0:
        raise ValueError("Cannot compare the zero vector")
    return arr / norm


def ambient_angle_record(
    tau_outer,
    tau_inner,
    *,
    zero_tolerance_rad: float = S1_ZERO_TOL_RAD,
) -> AmbientAngleRecord:
    """
    Compute both preregistered ambient meanings of endpoint parallelism.

    This primitive is path-free and transport-free because both vectors are
    compared directly in the common embedding space R^3.
    """
    a = _as_unit_vector3(tau_outer)
    b = _as_unit_vector3(tau_inner)

    dot_d = float(np.clip(np.dot(a, b), -1.0, 1.0))
    cross_norm_c = float(np.linalg.norm(np.cross(a, b)))

    delta_directed = math.atan2(cross_norm_c, dot_d)
    delta_line = math.atan2(cross_norm_c, abs(dot_d))
    residual_directed = float(np.linalg.norm(a - b))

    directed_state = (
        "AMBIENT_DIRECTED_PARALLEL"
        if delta_directed <= zero_tolerance_rad
        else "AMBIENT_DIRECTED_NOT_PARALLEL"
    )
    line_state = (
        "AMBIENT_LINE_PARALLEL"
        if delta_line <= zero_tolerance_rad
        else "AMBIENT_LINE_NOT_PARALLEL"
    )

    return AmbientAngleRecord(
        dot_d=dot_d,
        cross_norm_c=cross_norm_c,
        delta_directed_rad=delta_directed,
        delta_directed_deg=math.degrees(delta_directed),
        residual_directed=residual_directed,
        directed_state=directed_state,
        delta_line_rad=delta_line,
        delta_line_deg=math.degrees(delta_line),
        line_state=line_state,
    )


def evaluate_registered_branch(spec: AmbientBranchSpec) -> AmbientResult:
    """
    Evaluate one registered AOG-DIAGRAM branch.

    IMPORTANT: this function is never called at import time, by the default
    CLI path, or by the primitive test suite.
    """
    try:
        p_outer = gamma_k(spec.theta_outer, spec.k)
        p_inner = gamma_k(spec.theta_inner, spec.k)
        tau_outer = directed_tangent(spec.theta_outer, spec.k)
        tau_inner = directed_tangent(spec.theta_inner, spec.k)

        angles = ambient_angle_record(tau_outer, tau_inner)
        intrinsic_reference = INTRINSIC_S1_REFERENCE_DEG[spec.scale]

        return AmbientResult(
            branch_id=spec.branch_id,
            truncation=spec.truncation,
            scale=spec.scale,
            k=spec.k,
            theta_outer=spec.theta_outer,
            theta_inner=spec.theta_inner,
            p_outer=p_outer.tolist(),
            p_inner=p_inner.tolist(),
            tau_outer=tau_outer.tolist(),
            tau_inner=tau_inner.tolist(),
            dot_d=angles.dot_d,
            cross_norm_c=angles.cross_norm_c,
            delta_ambient_directed_rad=angles.delta_directed_rad,
            delta_ambient_directed_deg=angles.delta_directed_deg,
            residual_ambient_directed=angles.residual_directed,
            directed_state=angles.directed_state,
            delta_ambient_line_rad=angles.delta_line_rad,
            delta_ambient_line_deg=angles.delta_line_deg,
            line_state=angles.line_state,
            intrinsic_s1_reference_deg=intrinsic_reference,
            ambient_minus_intrinsic_deg=(
                angles.delta_directed_deg - intrinsic_reference
            ),
            zero_tolerance_rad=S1_ZERO_TOL_RAD,
            parallel_transport_used=False,
            image_pixel_data_used=False,
        )

    except Exception as exc:
        return AmbientResult(
            branch_id=spec.branch_id,
            truncation=spec.truncation,
            scale=spec.scale,
            k=spec.k,
            theta_outer=spec.theta_outer,
            theta_inner=spec.theta_inner,
            p_outer=None,
            p_inner=None,
            tau_outer=None,
            tau_inner=None,
            dot_d=None,
            cross_norm_c=None,
            delta_ambient_directed_rad=None,
            delta_ambient_directed_deg=None,
            residual_ambient_directed=None,
            directed_state="AMBIENT_DIRECTED_TECHNICAL_FAILURE",
            delta_ambient_line_rad=None,
            delta_ambient_line_deg=None,
            line_state="AMBIENT_LINE_TECHNICAL_FAILURE",
            intrinsic_s1_reference_deg=INTRINSIC_S1_REFERENCE_DEG[spec.scale],
            ambient_minus_intrinsic_deg=None,
            zero_tolerance_rad=S1_ZERO_TOL_RAD,
            parallel_transport_used=False,
            image_pixel_data_used=False,
            technical_error=f"{type(exc).__name__}: {exc}",
        )


def evaluate_registered_branches() -> list[AmbientResult]:
    """Evaluate exactly the two preregistered ambient branches."""
    return [evaluate_registered_branch(spec) for spec in REGISTERED_BRANCHES]


def directed_cross_scale_summary(results: list[AmbientResult]) -> str:
    states = [result.directed_state for result in results]

    if any(state == "AMBIENT_DIRECTED_TECHNICAL_FAILURE" for state in states):
        return "AMBIENT_DIRECTED_INCOMPLETE"

    parallel_count = sum(
        state == "AMBIENT_DIRECTED_PARALLEL"
        for state in states
    )

    if parallel_count == len(states):
        return "AMBIENT_DIRECTED_PARALLEL_ALL_SCALES"
    if parallel_count == 0:
        return "AMBIENT_DIRECTED_NOT_PARALLEL_ALL_SCALES"
    return "AMBIENT_DIRECTED_MIXED_SCALE_RESULT"


def line_cross_scale_summary(results: list[AmbientResult]) -> str:
    states = [result.line_state for result in results]

    if any(state == "AMBIENT_LINE_TECHNICAL_FAILURE" for state in states):
        return "AMBIENT_LINE_INCOMPLETE"

    parallel_count = sum(
        state == "AMBIENT_LINE_PARALLEL"
        for state in states
    )

    if parallel_count == len(states):
        return "AMBIENT_LINE_PARALLEL_ALL_SCALES"
    if parallel_count == 0:
        return "AMBIENT_LINE_NOT_PARALLEL_ALL_SCALES"
    return "AMBIENT_LINE_MIXED_SCALE_RESULT"


def _write_json(results: list[AmbientResult], output_path: Path) -> None:
    payload = {
        "checkpoint": CHECKPOINT,
        "variant": VARIANT,
        "registered_branch_count": len(REGISTERED_BRANCHES),
        "directed_cross_scale_summary": directed_cross_scale_summary(results),
        "line_cross_scale_summary": line_cross_scale_summary(results),
        "parallel_transport_used": False,
        "image_pixel_data_used": False,
        "intrinsic_s1_recomputed": False,
        "results": [asdict(result) for result in results],
    }
    output_path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _write_csv(results: list[AmbientResult], output_path: Path) -> None:
    rows = [asdict(result) for result in results]
    if not rows:
        raise ValueError("No ambient results to write")

    with output_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def _fmt(value: Optional[float], digits: int = 15) -> str:
    if value is None:
        return "NA"
    return f"{value:.{digits}g}"


def _write_report(results: list[AmbientResult], output_path: Path) -> None:
    lines = [
        "# First Hand Variant-A Ambient Endpoint-Parallelism Results",
        "",
        f"**Checkpoint:** `{CHECKPOINT}`  ",
        "**Variant:** A only  ",
        "**Truncation:** AOG-DIAGRAM, 1.5 turns  ",
        "**Parallel transport used:** no  ",
        "**Intrinsic S1 recomputed:** no  ",
        "**Image pixel data used:** no",
        "",
        "## Cross-scale summaries",
        "",
        f"Directed: `{directed_cross_scale_summary(results)}`",
        "",
        f"Unoriented line: `{line_cross_scale_summary(results)}`",
        "",
        "## Registered branches",
        "",
        "| Branch | Scale | Directed state | Directed angle (deg) | "
        "Line state | Line angle (deg) | Intrinsic S1 ref (deg) | "
        "Ambient - intrinsic (deg) |",
        "|---|---|---|---:|---|---:|---:|---:|",
    ]

    for result in results:
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{result.branch_id}`",
                    result.scale,
                    f"`{result.directed_state}`",
                    _fmt(result.delta_ambient_directed_deg),
                    f"`{result.line_state}`",
                    _fmt(result.delta_ambient_line_deg),
                    _fmt(result.intrinsic_s1_reference_deg),
                    _fmt(result.ambient_minus_intrinsic_deg),
                ]
            )
            + " |"
        )

    lines.extend(
        [
            "",
            "## Interpretation boundary",
            "",
            "This checkpoint compares already-frozen Variant-A endpoint tangents "
            "directly in ambient R^3 under both preregistered meanings of "
            "parallelism.",
            "",
            "It does not choose between directed-vector and unoriented-line "
            "semantics post hoc, and it does not alter the sealed intrinsic "
            "S1 result.",
            "",
        ]
    )

    output_path.write_text("\n".join(lines), encoding="utf-8")


def write_registered_outputs(
    results: list[AmbientResult],
    output_dir: Path,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    _write_json(results, output_dir / "ambient_parallelism_results.json")
    _write_csv(results, output_dir / "ambient_parallelism_results.csv")
    _write_report(results, output_dir / "ambient_parallelism_report.md")


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Preregistered Variant-A ambient endpoint-parallelism evaluator"
    )
    parser.add_argument(
        "--execute-registered-ambient",
        action="store_true",
        help="explicitly evaluate exactly the two registered ambient branches",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("results/first_hand_variant_a_ambient_parallelism_v0_8"),
        help="result directory used only with explicit registered execution",
    )
    return parser.parse_args()


def main() -> int:
    args = _parse_args()

    if not args.execute_registered_ambient:
        print(
            "No registered ambient endpoint branch evaluated. "
            "Use --execute-registered-ambient only after the "
            "implementation-only commit has been frozen."
        )
        return 0

    results = evaluate_registered_branches()
    write_registered_outputs(results, args.output_dir)

    print(f"Wrote registered ambient outputs to: {args.output_dir}")
    print(f"Registered branches executed: {len(results)}")
    print(f"Directed summary: {directed_cross_scale_summary(results)}")
    print(f"Line summary: {line_cross_scale_summary(results)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
