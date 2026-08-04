#!/usr/bin/env python3
"""
Preregistered First Hand S1 evaluator for the Meru Geometry Audit.

IMPORTANT EXECUTION BOUNDARY
----------------------------
This module encodes the mathematics frozen in:

    first_hand_analytic_s1_preregistration_v0.8

Importing this module does not evaluate any registered S1 branch.
Running this file without the explicit --execute-registered flag also does
not evaluate any registered S1 branch.

Registered execution surface:
    S1-PROSE-G30
    S1-PROSE-GHALF
    S1-DIAGRAM-G30
    S1-DIAGRAM-GHALF

No optimisation, alternate k values, comparator spirals, S1.5, S2, toroidal,
dimpled-sphere, or image-derived fitting are implemented here.
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


S1_ZERO_TOL_RAD = 1.0e-10
POSITION_TOL = 1.0e-12
TANGENCY_TOL = 1.0e-10

K_G30 = math.tan(math.pi / 6.0)
K_GHALF = math.tan(0.5)


@dataclass(frozen=True)
class BranchSpec:
    branch_id: str
    truncation: str
    scale: str
    k: float
    theta_outer: Optional[float]
    theta_inner: float
    outer_is_limit: bool


REGISTERED_BRANCHES = (
    BranchSpec(
        branch_id="S1-PROSE-G30",
        truncation="AOG-PROSE",
        scale="G30",
        k=K_G30,
        theta_outer=None,
        theta_inner=3.0 * math.pi,
        outer_is_limit=True,
    ),
    BranchSpec(
        branch_id="S1-PROSE-GHALF",
        truncation="AOG-PROSE",
        scale="GHALF",
        k=K_GHALF,
        theta_outer=None,
        theta_inner=3.0 * math.pi,
        outer_is_limit=True,
    ),
    BranchSpec(
        branch_id="S1-DIAGRAM-G30",
        truncation="AOG-DIAGRAM",
        scale="G30",
        k=K_G30,
        theta_outer=1.0,
        theta_inner=1.0 + 3.0 * math.pi,
        outer_is_limit=False,
    ),
    BranchSpec(
        branch_id="S1-DIAGRAM-GHALF",
        truncation="AOG-DIAGRAM",
        scale="GHALF",
        k=K_GHALF,
        theta_outer=1.0,
        theta_inner=1.0 + 3.0 * math.pi,
        outer_is_limit=False,
    ),
)


@dataclass
class TransportRecord:
    vector: np.ndarray
    axis: Optional[np.ndarray]
    angle_rad: float


@dataclass
class S1Result:
    branch_id: str
    truncation: str
    scale: str
    k: float
    theta_outer: Optional[float]
    theta_outer_spec: str
    theta_inner: float
    p_outer: Optional[list[float]]
    p_inner: Optional[list[float]]
    tau_outer: Optional[list[float]]
    tau_inner: Optional[list[float]]
    transport_axis: Optional[list[float]]
    transport_angle_rad: Optional[float]
    transported_tau_outer: Optional[list[float]]
    dot_d: Optional[float]
    cross_norm_c: Optional[float]
    delta_s1_rad: Optional[float]
    delta_s1_deg: Optional[float]
    residual_r_s1: Optional[float]
    zero_tolerance_rad: float
    state: str
    image_pixel_data_used: bool
    technical_error: Optional[str] = None


class AntipodalTransportError(RuntimeError):
    """Raised when minimal-geodesic transport is undefined at antipodal points."""


def _as_vector3(value) -> np.ndarray:
    arr = np.asarray(value, dtype=float)
    if arr.shape != (3,):
        raise ValueError(f"Expected a 3-vector, got shape {arr.shape}")
    if not np.all(np.isfinite(arr)):
        raise ValueError("Vector contains non-finite values")
    return arr


def _unit(value) -> np.ndarray:
    arr = _as_vector3(value)
    norm = float(np.linalg.norm(arr))
    if norm == 0.0:
        raise ValueError("Cannot normalise the zero vector")
    return arr / norm


def gamma_k(theta: float, k: float) -> np.ndarray:
    """Exact spherical image Gamma_k(theta), for theta > 0 and k > 0."""
    theta = float(theta)
    k = float(k)
    if theta <= 0.0:
        raise ValueError("theta must satisfy theta > 0")
    if k <= 0.0:
        raise ValueError("k must satisfy k > 0")

    denom = math.sqrt(k * k + theta * theta)
    return np.array(
        [k * math.cos(theta), k * math.sin(theta), theta],
        dtype=float,
    ) / denom


def gamma_prime_k(theta: float, k: float) -> np.ndarray:
    """Exact derivative of Gamma_k(theta), for theta > 0 and k > 0."""
    theta = float(theta)
    k = float(k)
    if theta <= 0.0:
        raise ValueError("theta must satisfy theta > 0")
    if k <= 0.0:
        raise ValueError("k must satisfy k > 0")

    n = np.array(
        [k * math.cos(theta), k * math.sin(theta), theta],
        dtype=float,
    )
    n_prime = np.array(
        [-k * math.sin(theta), k * math.cos(theta), 1.0],
        dtype=float,
    )
    s = math.sqrt(k * k + theta * theta)

    return n_prime / s - (theta * n) / (s ** 3)


def directed_tangent(theta: float, k: float) -> np.ndarray:
    """Preregistered inner->outer unit tangent: -Gamma'_k / ||Gamma'_k||."""
    derivative = gamma_prime_k(theta, k)
    return -_unit(derivative)


def prose_outer_position(k: float) -> np.ndarray:
    """Exact AOG-PROSE limit lim(theta->0+) Gamma_k(theta) = (1,0,0)."""
    k = float(k)
    if k <= 0.0:
        raise ValueError("k must satisfy k > 0")
    return np.array([1.0, 0.0, 0.0], dtype=float)


def prose_outer_tangent(k: float) -> np.ndarray:
    """Exact directed AOG-PROSE outer tangent; no epsilon is used."""
    k = float(k)
    if k <= 0.0:
        raise ValueError("k must satisfy k > 0")

    return np.array([0.0, -k, -1.0], dtype=float) / math.sqrt(k * k + 1.0)


def minimal_sphere_transport(
    p_from,
    p_to,
    tangent,
    *,
    position_tol: float = POSITION_TOL,
    tangency_tol: float = TANGENCY_TOL,
) -> TransportRecord:
    """Parallel transport along the unique shorter great-circle arc."""
    p = _unit(p_from)
    q = _unit(p_to)
    v = _as_vector3(tangent)

    if abs(float(np.dot(p, v))) > tangency_tol:
        raise ValueError("Input vector is not tangent at p_from within tolerance")

    dot_pq = float(np.clip(np.dot(p, q), -1.0, 1.0))
    cross_pq = np.cross(p, q)
    sin_angle = float(np.linalg.norm(cross_pq))

    if dot_pq >= 1.0 - position_tol:
        return TransportRecord(vector=v.copy(), axis=None, angle_rad=0.0)

    if dot_pq <= -1.0 + position_tol:
        raise AntipodalTransportError(
            "Minimal-geodesic transport is non-unique for antipodal endpoints"
        )

    axis = cross_pq / sin_angle
    angle = math.atan2(sin_angle, dot_pq)

    transported = (
        v * math.cos(angle)
        + np.cross(axis, v) * math.sin(angle)
        + axis * float(np.dot(axis, v)) * (1.0 - math.cos(angle))
    )

    # Validation only: never repair the transported vector.
    if abs(float(np.dot(q, transported))) > tangency_tol:
        raise RuntimeError("Transported vector is not tangent at p_to")
    if not math.isclose(
        float(np.linalg.norm(transported)),
        float(np.linalg.norm(v)),
        rel_tol=0.0,
        abs_tol=1.0e-12,
    ):
        raise RuntimeError("Transport failed to preserve tangent-vector norm")

    return TransportRecord(vector=transported, axis=axis, angle_rad=angle)


def evaluate_branch(spec: BranchSpec) -> S1Result:
    """Evaluate one preregistered S1 branch exactly as frozen."""
    try:
        p_inner = gamma_k(spec.theta_inner, spec.k)
        tau_inner = directed_tangent(spec.theta_inner, spec.k)

        if spec.outer_is_limit:
            p_outer = prose_outer_position(spec.k)
            tau_outer = prose_outer_tangent(spec.k)
            theta_outer_spec = "theta_outer -> 0+ (exact analytic limit)"
        else:
            if spec.theta_outer is None:
                raise RuntimeError("Finite outer branch is missing theta_outer")
            p_outer = gamma_k(spec.theta_outer, spec.k)
            tau_outer = directed_tangent(spec.theta_outer, spec.k)
            theta_outer_spec = repr(spec.theta_outer)

        try:
            transport = minimal_sphere_transport(p_outer, p_inner, tau_outer)
        except AntipodalTransportError:
            return S1Result(
                branch_id=spec.branch_id,
                truncation=spec.truncation,
                scale=spec.scale,
                k=spec.k,
                theta_outer=spec.theta_outer,
                theta_outer_spec=theta_outer_spec,
                theta_inner=spec.theta_inner,
                p_outer=p_outer.tolist(),
                p_inner=p_inner.tolist(),
                tau_outer=tau_outer.tolist(),
                tau_inner=tau_inner.tolist(),
                transport_axis=None,
                transport_angle_rad=None,
                transported_tau_outer=None,
                dot_d=None,
                cross_norm_c=None,
                delta_s1_rad=None,
                delta_s1_deg=None,
                residual_r_s1=None,
                zero_tolerance_rad=S1_ZERO_TOL_RAD,
                state="S1_TRANSPORT_UNDEFINED_ANTIPODAL",
                image_pixel_data_used=False,
            )

        tau_outer_t = transport.vector
        d = float(np.clip(np.dot(tau_outer_t, tau_inner), -1.0, 1.0))
        c = float(np.linalg.norm(np.cross(tau_outer_t, tau_inner)))
        delta = math.atan2(c, d)
        residual = float(np.linalg.norm(tau_outer_t - tau_inner))

        state = (
            "S1_DIRECTED_COMPATIBLE"
            if delta <= S1_ZERO_TOL_RAD
            else "S1_DIRECTED_NOT_COMPATIBLE"
        )

        return S1Result(
            branch_id=spec.branch_id,
            truncation=spec.truncation,
            scale=spec.scale,
            k=spec.k,
            theta_outer=spec.theta_outer,
            theta_outer_spec=theta_outer_spec,
            theta_inner=spec.theta_inner,
            p_outer=p_outer.tolist(),
            p_inner=p_inner.tolist(),
            tau_outer=tau_outer.tolist(),
            tau_inner=tau_inner.tolist(),
            transport_axis=None if transport.axis is None else transport.axis.tolist(),
            transport_angle_rad=transport.angle_rad,
            transported_tau_outer=tau_outer_t.tolist(),
            dot_d=d,
            cross_norm_c=c,
            delta_s1_rad=delta,
            delta_s1_deg=math.degrees(delta),
            residual_r_s1=residual,
            zero_tolerance_rad=S1_ZERO_TOL_RAD,
            state=state,
            image_pixel_data_used=False,
        )

    except Exception as exc:
        # Record failure; never repair source/model inputs silently.
        return S1Result(
            branch_id=spec.branch_id,
            truncation=spec.truncation,
            scale=spec.scale,
            k=spec.k,
            theta_outer=spec.theta_outer,
            theta_outer_spec=(
                "theta_outer -> 0+ (exact analytic limit)"
                if spec.outer_is_limit
                else repr(spec.theta_outer)
            ),
            theta_inner=spec.theta_inner,
            p_outer=None,
            p_inner=None,
            tau_outer=None,
            tau_inner=None,
            transport_axis=None,
            transport_angle_rad=None,
            transported_tau_outer=None,
            dot_d=None,
            cross_norm_c=None,
            delta_s1_rad=None,
            delta_s1_deg=None,
            residual_r_s1=None,
            zero_tolerance_rad=S1_ZERO_TOL_RAD,
            state="S1_TECHNICAL_FAILURE",
            image_pixel_data_used=False,
            technical_error=f"{type(exc).__name__}: {exc}",
        )


def evaluate_registered_branches() -> list[S1Result]:
    """Evaluate exactly the four preregistered S1 branches."""
    return [evaluate_branch(spec) for spec in REGISTERED_BRANCHES]


def cross_branch_state(results: list[S1Result]) -> str:
    states = [r.state for r in results]
    if any(
        s in {"S1_TECHNICAL_FAILURE", "S1_TRANSPORT_UNDEFINED_ANTIPODAL"}
        for s in states
    ):
        return "S1_INCOMPLETE"

    compatible = [s == "S1_DIRECTED_COMPATIBLE" for s in states]
    if all(compatible):
        return "S1_ALL_REGISTERED_BRANCHES_COMPATIBLE"
    if not any(compatible):
        return "S1_NO_REGISTERED_BRANCH_COMPATIBLE"
    return "S1_BRANCH_DEPENDENT"


def _write_json(results: list[S1Result], output_path: Path) -> None:
    payload = {
        "checkpoint": "first_hand_analytic_s1_preregistration_v0.8",
        "cross_branch_state": cross_branch_state(results),
        "image_pixel_data_used": False,
        "branches": [asdict(r) for r in results],
    }
    output_path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _write_csv(results: list[S1Result], output_path: Path) -> None:
    rows = [asdict(r) for r in results]
    if not rows:
        raise ValueError("No S1 results to write")

    fieldnames = list(rows[0].keys())
    with output_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def _fmt(value: Optional[float], digits: int = 15) -> str:
    if value is None:
        return "NA"
    return f"{value:.{digits}g}"


def _write_report(results: list[S1Result], output_path: Path) -> None:
    lines = [
        "# First Hand S1 Results",
        "",
        "**Checkpoint:** `first_hand_analytic_s1_preregistration_v0.8`  ",
        "**Execution:** registered four-cell S1 matrix only  ",
        "**Image pixel data used:** no",
        "",
        "## Cross-branch state",
        "",
        f"`{cross_branch_state(results)}`",
        "",
        "## Registered branch results",
        "",
        "| Branch | State | Delta S1 (rad) | Delta S1 (deg) | R S1 |",
        "|---|---|---:|---:|---:|",
    ]

    for result in results:
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{result.branch_id}`",
                    f"`{result.state}`",
                    _fmt(result.delta_s1_rad),
                    _fmt(result.delta_s1_deg),
                    _fmt(result.residual_r_s1),
                ]
            )
            + " |"
        )

    lines.extend(
        [
            "",
            "## Interpretation boundary",
            "",
            "These values report the preregistered S1 endpoint tangent-compatibility diagnostic only.",
            "",
            "No S1-only result supports or refutes the source's comparative reciprocal-versus-comparator claim.",
            "",
            "No S1-only result establishes recursive self-embedment, historical uniqueness of the spherical map, Hebrew-letter generation, or the toroidal/dimpled-sphere construction.",
            "",
        ]
    )

    output_path.write_text("\n".join(lines), encoding="utf-8")


def write_registered_outputs(results: list[S1Result], output_dir: Path) -> None:
    """Write preregistered JSON, CSV, and Markdown result records."""
    output_dir.mkdir(parents=True, exist_ok=True)
    _write_json(results, output_dir / "s1_results.json")
    _write_csv(results, output_dir / "s1_results.csv")
    _write_report(results, output_dir / "s1_report.md")


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Preregistered First Hand S1 evaluator"
    )
    parser.add_argument(
        "--execute-registered",
        action="store_true",
        help="explicitly execute exactly the four frozen S1 branches",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("results/first_hand_s1_v0_8"),
        help="result directory used only with --execute-registered",
    )
    return parser.parse_args()


def main() -> int:
    args = _parse_args()

    if not args.execute_registered:
        print(
            "No S1 branch evaluated. "
            "Use --execute-registered only after the implementation-only "
            "commit has been frozen."
        )
        return 0

    results = evaluate_registered_branches()
    write_registered_outputs(results, args.output_dir)

    print(f"Wrote registered S1 outputs to: {args.output_dir}")
    print(f"Cross-branch state: {cross_branch_state(results)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
