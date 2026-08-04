#!/usr/bin/env python3
"""
Preregistered First Hand S1 comparator evaluator for the Meru Geometry Audit.

IMPORTANT EXECUTION BOUNDARY
----------------------------
This module encodes the mathematics frozen in:

    first_hand_s1_comparator_preregistration_v0.8

Importing this module does not evaluate any comparator branch.
Running this file without the explicit --execute-registered-comparators flag
also does not evaluate any comparator branch.

Primary named-comparator cells:
    ARCHIMEDES x {G30, GHALF}
    LOG_ENDPOINT_MATCHED x {G30, GHALF}
    GOLDEN_MEAN x {G30, GHALF}

Secondary logarithmic sensitivity cells:
    multipliers {0.50, 0.75, 1.00, 1.25, 1.50, 2.00}
    x {G30, GHALF}

The reciprocal AOG-DIAGRAM values are immutable reference inputs from the
completed S1 checkpoint and are not recomputed here.

No AOG-PROSE comparator, parameter optimisation, GUNIT/GONE scale, alternative
projection, S1.5, S2, toroidal, dimpled-sphere, or image-derived fitting is
implemented here.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Callable, Optional

import numpy as np

# Reuse only the frozen Variant-A transport and scale definitions.
from first_hand_s1 import (
    AntipodalTransportError,
    K_G30,
    K_GHALF,
    S1_ZERO_TOL_RAD,
    minimal_sphere_transport,
)


L = 3.0 * math.pi
THETA0 = 1.0
PHI = (1.0 + math.sqrt(5.0)) / 2.0

Q_RECIPROCAL = 1.0 / (1.0 + L)

B_ENDPOINT_MATCHED = math.log(1.0 / Q_RECIPROCAL) / L
B_GOLDEN = 2.0 * math.log(PHI) / math.pi

LOG_MULTIPLIERS = (0.50, 0.75, 1.00, 1.25, 1.50, 2.00)

# Frozen reciprocal references from the completed S1 execution.
RECIPROCAL_DELTA_RAD = {
    "G30": 2.5233555305045834,
    "GHALF": 2.5168042811835494,
}

RECIPROCAL_DELTA_DEG = {
    "G30": 144.5776221089075,
    "GHALF": 144.2022631722743,
}


@dataclass(frozen=True)
class CurveSpec:
    comparator_id: str
    family: str
    equation_label: str
    normalization: str
    radius: Callable[[float], float]
    radius_prime: Callable[[float], float]
    growth_parameter: Optional[float] = None
    log_multiplier: Optional[float] = None
    primary_named: bool = True


@dataclass(frozen=True)
class ComparatorCell:
    cell_id: str
    comparator_id: str
    scale: str
    k: float
    primary_named: bool


@dataclass
class ComparatorResult:
    cell_id: str
    comparator_id: str
    family: str
    primary_named: bool
    equation_label: str
    normalization: str
    growth_parameter: Optional[float]
    log_multiplier: Optional[float]
    u_outer: float
    u_inner: float
    theta0: float
    scale: str
    k: float
    r_outer: Optional[float]
    r_inner: Optional[float]
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
    reciprocal_reference_rad: float
    reciprocal_reference_deg: float
    difference_d_rad: Optional[float]
    difference_d_deg: Optional[float]
    state: str
    image_pixel_data_used: bool
    technical_error: Optional[str] = None


def archimedean_radius(u: float) -> float:
    u = float(u)
    return 1.0 - ((1.0 - Q_RECIPROCAL) / L) * u


def archimedean_radius_prime(u: float) -> float:
    _ = float(u)
    return -(1.0 - Q_RECIPROCAL) / L


def logarithmic_radius(u: float, b: float) -> float:
    return math.exp(-float(b) * float(u))


def logarithmic_radius_prime(u: float, b: float) -> float:
    return -float(b) * logarithmic_radius(u, b)


def _log_curve(
    *,
    comparator_id: str,
    family: str,
    b: float,
    normalization: str,
    log_multiplier: Optional[float],
    primary_named: bool,
) -> CurveSpec:
    b = float(b)
    return CurveSpec(
        comparator_id=comparator_id,
        family=family,
        equation_label=f"r(u)=exp(-{b:.17g} u)",
        normalization=normalization,
        radius=lambda u, _b=b: logarithmic_radius(u, _b),
        radius_prime=lambda u, _b=b: logarithmic_radius_prime(u, _b),
        growth_parameter=b,
        log_multiplier=log_multiplier,
        primary_named=primary_named,
    )


ARCHIMEDES = CurveSpec(
    comparator_id="ARCHIMEDES-ENDPOINT-MATCHED",
    family="Archimedean",
    equation_label="r(u)=1-((1-q_R)/L)u",
    normalization="r(0)=1 and r(L)=q_R",
    radius=archimedean_radius,
    radius_prime=archimedean_radius_prime,
    primary_named=True,
)

LOG_ENDPOINT_MATCHED = _log_curve(
    comparator_id="LOG-ENDPOINT-MATCHED",
    family="Logarithmic",
    b=B_ENDPOINT_MATCHED,
    normalization="r(0)=1 and r(L)=q_R",
    log_multiplier=1.0,
    primary_named=True,
)

GOLDEN_MEAN = _log_curve(
    comparator_id="GOLDEN-MEAN",
    family="Golden Mean logarithmic",
    b=B_GOLDEN,
    normalization="quarter-turn radius ratio phi; r(0)=1",
    log_multiplier=None,
    primary_named=True,
)

PRIMARY_COMPARATORS = (
    ARCHIMEDES,
    LOG_ENDPOINT_MATCHED,
    GOLDEN_MEAN,
)

LOG_GRID_COMPARATORS = tuple(
    _log_curve(
        comparator_id=f"LOG-GRID-M{int(round(multiplier * 100)):03d}",
        family="Logarithmic sensitivity grid",
        b=multiplier * B_ENDPOINT_MATCHED,
        normalization="r(0)=1; b fixed by preregistered multiplier of b_*",
        log_multiplier=multiplier,
        primary_named=False,
    )
    for multiplier in LOG_MULTIPLIERS
)

ALL_COMPARATORS = PRIMARY_COMPARATORS + LOG_GRID_COMPARATORS

SCALES = (
    ("G30", K_G30),
    ("GHALF", K_GHALF),
)

PRIMARY_CELLS = tuple(
    ComparatorCell(
        cell_id=f"{curve.comparator_id}-{scale}",
        comparator_id=curve.comparator_id,
        scale=scale,
        k=k,
        primary_named=True,
    )
    for curve in PRIMARY_COMPARATORS
    for scale, k in SCALES
)

LOG_GRID_CELLS = tuple(
    ComparatorCell(
        cell_id=f"{curve.comparator_id}-{scale}",
        comparator_id=curve.comparator_id,
        scale=scale,
        k=k,
        primary_named=False,
    )
    for curve in LOG_GRID_COMPARATORS
    for scale, k in SCALES
)

REGISTERED_COMPARATOR_CELLS = PRIMARY_CELLS + LOG_GRID_CELLS

_CURVE_BY_ID = {curve.comparator_id: curve for curve in ALL_COMPARATORS}


def spherical_curve(
    u: float,
    k: float,
    radius: Callable[[float], float],
) -> np.ndarray:
    """
    Variant-A inverse-gnomonic image of a finite AOG-DIAGRAM comparator:

        theta(u) = 1 + u
        Gamma(u) =
            (k r cos(theta), k r sin(theta), 1)
            / sqrt(1 + k^2 r^2)
    """
    u = float(u)
    k = float(k)
    if not (0.0 <= u <= L):
        raise ValueError("u must satisfy 0 <= u <= 3*pi")
    if k <= 0.0:
        raise ValueError("k must satisfy k > 0")

    r = float(radius(u))
    if not math.isfinite(r) or r <= 0.0:
        raise ValueError("registered comparator radius must be finite and positive")

    theta = THETA0 + u
    n = np.array(
        [k * r * math.cos(theta), k * r * math.sin(theta), 1.0],
        dtype=float,
    )
    return n / math.sqrt(1.0 + (k * r) ** 2)


def spherical_curve_prime(
    u: float,
    k: float,
    radius: Callable[[float], float],
    radius_prime: Callable[[float], float],
) -> np.ndarray:
    """Exact derivative of the registered generic polar-to-sphere curve."""
    u = float(u)
    k = float(k)
    if not (0.0 <= u <= L):
        raise ValueError("u must satisfy 0 <= u <= 3*pi")
    if k <= 0.0:
        raise ValueError("k must satisfy k > 0")

    r = float(radius(u))
    rp = float(radius_prime(u))
    if not (math.isfinite(r) and math.isfinite(rp)):
        raise ValueError("registered radius and derivative must be finite")
    if r <= 0.0:
        raise ValueError("registered comparator radius must be positive")

    theta = THETA0 + u
    cos_t = math.cos(theta)
    sin_t = math.sin(theta)

    n = np.array(
        [k * r * cos_t, k * r * sin_t, 1.0],
        dtype=float,
    )
    n_prime = np.array(
        [
            k * (rp * cos_t - r * sin_t),
            k * (rp * sin_t + r * cos_t),
            0.0,
        ],
        dtype=float,
    )

    s = math.sqrt(1.0 + (k * r) ** 2)
    # s' = k^2 r r' / s
    return n_prime / s - n * (k * k * r * rp) / (s ** 3)


def directed_tangent_for_curve(
    u: float,
    k: float,
    curve: CurveSpec,
) -> np.ndarray:
    """
    Directed inner -> outer unit tangent.

    Since inner -> outer corresponds to decreasing u, use -Gamma'/||Gamma'||.
    """
    derivative = spherical_curve_prime(
        u,
        k,
        curve.radius,
        curve.radius_prime,
    )
    norm = float(np.linalg.norm(derivative))
    if norm == 0.0:
        raise ValueError("comparator spherical derivative is zero")
    return -derivative / norm


def evaluate_comparator_cell(cell: ComparatorCell) -> ComparatorResult:
    """
    Evaluate one frozen comparator cell.

    This function is intentionally not called on import or by primitive tests.
    """
    curve = _CURVE_BY_ID[cell.comparator_id]
    reciprocal_rad = RECIPROCAL_DELTA_RAD[cell.scale]
    reciprocal_deg = RECIPROCAL_DELTA_DEG[cell.scale]

    try:
        r_outer = float(curve.radius(0.0))
        r_inner = float(curve.radius(L))

        p_outer = spherical_curve(0.0, cell.k, curve.radius)
        p_inner = spherical_curve(L, cell.k, curve.radius)

        tau_outer = directed_tangent_for_curve(0.0, cell.k, curve)
        tau_inner = directed_tangent_for_curve(L, cell.k, curve)

        try:
            transport = minimal_sphere_transport(
                p_outer,
                p_inner,
                tau_outer,
            )
        except AntipodalTransportError:
            return ComparatorResult(
                cell_id=cell.cell_id,
                comparator_id=curve.comparator_id,
                family=curve.family,
                primary_named=cell.primary_named,
                equation_label=curve.equation_label,
                normalization=curve.normalization,
                growth_parameter=curve.growth_parameter,
                log_multiplier=curve.log_multiplier,
                u_outer=0.0,
                u_inner=L,
                theta0=THETA0,
                scale=cell.scale,
                k=cell.k,
                r_outer=r_outer,
                r_inner=r_inner,
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
                reciprocal_reference_rad=reciprocal_rad,
                reciprocal_reference_deg=reciprocal_deg,
                difference_d_rad=None,
                difference_d_deg=None,
                state="COMPARATOR_TRANSPORT_UNDEFINED_ANTIPODAL",
                image_pixel_data_used=False,
            )

        transported = transport.vector
        d = float(np.clip(np.dot(transported, tau_inner), -1.0, 1.0))
        c = float(np.linalg.norm(np.cross(transported, tau_inner)))
        delta = math.atan2(c, d)
        residual = float(np.linalg.norm(transported - tau_inner))

        difference_rad = delta - reciprocal_rad
        difference_deg = math.degrees(difference_rad)

        numerical_tie_tol = 1.0e-12
        if abs(difference_rad) <= numerical_tie_tol:
            state = "EQUAL_WITHIN_NUMERICAL_PRECISION"
        elif difference_rad > 0.0:
            state = "RECIPROCAL_SMALLER_MISMATCH"
        else:
            state = "COMPARATOR_SMALLER_MISMATCH"

        return ComparatorResult(
            cell_id=cell.cell_id,
            comparator_id=curve.comparator_id,
            family=curve.family,
            primary_named=cell.primary_named,
            equation_label=curve.equation_label,
            normalization=curve.normalization,
            growth_parameter=curve.growth_parameter,
            log_multiplier=curve.log_multiplier,
            u_outer=0.0,
            u_inner=L,
            theta0=THETA0,
            scale=cell.scale,
            k=cell.k,
            r_outer=r_outer,
            r_inner=r_inner,
            p_outer=p_outer.tolist(),
            p_inner=p_inner.tolist(),
            tau_outer=tau_outer.tolist(),
            tau_inner=tau_inner.tolist(),
            transport_axis=None if transport.axis is None else transport.axis.tolist(),
            transport_angle_rad=transport.angle_rad,
            transported_tau_outer=transported.tolist(),
            dot_d=d,
            cross_norm_c=c,
            delta_s1_rad=delta,
            delta_s1_deg=math.degrees(delta),
            residual_r_s1=residual,
            reciprocal_reference_rad=reciprocal_rad,
            reciprocal_reference_deg=reciprocal_deg,
            difference_d_rad=difference_rad,
            difference_d_deg=difference_deg,
            state=state,
            image_pixel_data_used=False,
        )

    except Exception as exc:
        return ComparatorResult(
            cell_id=cell.cell_id,
            comparator_id=curve.comparator_id,
            family=curve.family,
            primary_named=cell.primary_named,
            equation_label=curve.equation_label,
            normalization=curve.normalization,
            growth_parameter=curve.growth_parameter,
            log_multiplier=curve.log_multiplier,
            u_outer=0.0,
            u_inner=L,
            theta0=THETA0,
            scale=cell.scale,
            k=cell.k,
            r_outer=None,
            r_inner=None,
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
            reciprocal_reference_rad=reciprocal_rad,
            reciprocal_reference_deg=reciprocal_deg,
            difference_d_rad=None,
            difference_d_deg=None,
            state="COMPARATOR_TECHNICAL_FAILURE",
            image_pixel_data_used=False,
            technical_error=f"{type(exc).__name__}: {exc}",
        )


def evaluate_registered_comparators() -> list[ComparatorResult]:
    """Evaluate exactly the frozen six primary plus twelve grid cells."""
    return [
        evaluate_comparator_cell(cell)
        for cell in REGISTERED_COMPARATOR_CELLS
    ]


def _primary_scale_summary(
    results: list[ComparatorResult],
    scale: str,
) -> str:
    subset = [r for r in results if r.primary_named and r.scale == scale]

    if len(subset) != 3 or any(
        r.state in {
            "COMPARATOR_TECHNICAL_FAILURE",
            "COMPARATOR_TRANSPORT_UNDEFINED_ANTIPODAL",
        }
        for r in subset
    ):
        return "NAMED_COMPARATOR_COMPARISON_INCOMPLETE"

    if all(r.state == "RECIPROCAL_SMALLER_MISMATCH" for r in subset):
        return "RECIPROCAL_STRICTLY_BEST_NAMED_COMPARATORS"

    return "RECIPROCAL_NOT_STRICTLY_BEST_NAMED_COMPARATORS"


def _primary_checkpoint_summary(results: list[ComparatorResult]) -> str:
    primary = [r for r in results if r.primary_named]

    if len(primary) != 6 or any(
        r.state in {
            "COMPARATOR_TECHNICAL_FAILURE",
            "COMPARATOR_TRANSPORT_UNDEFINED_ANTIPODAL",
        }
        for r in primary
    ):
        return "PRIMARY_COMPARISON_INCOMPLETE"

    if all(r.state == "RECIPROCAL_SMALLER_MISMATCH" for r in primary):
        return "RECIPROCAL_STRICTLY_BEST_ALL_PRIMARY_CELLS"

    return "RECIPROCAL_NOT_STRICTLY_BEST_ALL_PRIMARY_CELLS"


def _log_grid_summary(
    results: list[ComparatorResult],
    scale: str,
) -> str:
    subset = [r for r in results if (not r.primary_named) and r.scale == scale]

    if len(subset) != 6 or any(
        r.state in {
            "COMPARATOR_TECHNICAL_FAILURE",
            "COMPARATOR_TRANSPORT_UNDEFINED_ANTIPODAL",
        }
        for r in subset
    ):
        return "LOG_GRID_COMPARISON_INCOMPLETE"

    if all(r.state == "RECIPROCAL_SMALLER_MISMATCH" for r in subset):
        return "RECIPROCAL_BEATS_ALL_REGISTERED_LOG_GRID_POINTS"

    return "REGISTERED_LOG_GRID_CONTAINS_EQUAL_OR_BETTER_POINT"


def _write_json(results: list[ComparatorResult], output_path: Path) -> None:
    payload = {
        "checkpoint": "first_hand_s1_comparator_preregistration_v0.8",
        "variant": "A",
        "image_pixel_data_used": False,
        "reciprocal_recomputed": False,
        "primary_checkpoint_summary": _primary_checkpoint_summary(results),
        "primary_scale_summary": {
            scale: _primary_scale_summary(results, scale)
            for scale, _ in SCALES
        },
        "log_grid_summary": {
            scale: _log_grid_summary(results, scale)
            for scale, _ in SCALES
        },
        "results": [asdict(r) for r in results],
    }
    output_path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _write_csv(results: list[ComparatorResult], output_path: Path) -> None:
    rows = [asdict(r) for r in results]
    if not rows:
        raise ValueError("No comparator results to write")

    with output_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def _fmt(value: Optional[float], digits: int = 15) -> str:
    if value is None:
        return "NA"
    return f"{value:.{digits}g}"


def _write_report(results: list[ComparatorResult], output_path: Path) -> None:
    lines = [
        "# First Hand S1 Comparator Results",
        "",
        "**Checkpoint:** `first_hand_s1_comparator_preregistration_v0.8`  ",
        "**Variant:** A only  ",
        "**Reciprocal reference recomputed:** no  ",
        "**Image pixel data used:** no",
        "",
        "## Primary checkpoint summary",
        "",
        f"`{_primary_checkpoint_summary(results)}`",
        "",
        "## Primary named comparators",
        "",
        "| Comparator | Scale | State | Delta S1 (deg) | Reciprocal (deg) | D (deg) |",
        "|---|---|---|---:|---:|---:|",
    ]

    for result in [r for r in results if r.primary_named]:
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{result.comparator_id}`",
                    result.scale,
                    f"`{result.state}`",
                    _fmt(result.delta_s1_deg),
                    _fmt(result.reciprocal_reference_deg),
                    _fmt(result.difference_d_deg),
                ]
            )
            + " |"
        )

    lines.extend(
        [
            "",
            "## Fixed logarithmic sensitivity grid",
            "",
            "| Comparator | Scale | Multiplier | b | State | Delta S1 (deg) | D (deg) |",
            "|---|---|---:|---:|---|---:|---:|",
        ]
    )

    for result in [r for r in results if not r.primary_named]:
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{result.comparator_id}`",
                    result.scale,
                    _fmt(result.log_multiplier),
                    _fmt(result.growth_parameter),
                    f"`{result.state}`",
                    _fmt(result.delta_s1_deg),
                    _fmt(result.difference_d_deg),
                ]
            )
            + " |"
        )

    lines.extend(
        [
            "",
            "## Interpretation boundary",
            "",
            "This checkpoint compares only the Variant-A directed endpoint-tangent "
            "S1 proxy on the finite AOG-DIAGRAM construction.",
            "",
            "It does not establish literal recursive self-embedment, global "
            "spiral superiority, or the corresponding ordering on the "
            "dimpled-sphere torus.",
            "",
        ]
    )

    output_path.write_text("\n".join(lines), encoding="utf-8")


def write_registered_outputs(
    results: list[ComparatorResult],
    output_dir: Path,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    _write_json(results, output_dir / "s1_comparator_results.json")
    _write_csv(results, output_dir / "s1_comparator_results.csv")
    _write_report(results, output_dir / "s1_comparator_report.md")


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Preregistered First Hand S1 comparator evaluator"
    )
    parser.add_argument(
        "--execute-registered-comparators",
        action="store_true",
        help="explicitly execute the frozen comparator matrix",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("results/first_hand_s1_comparators_v0_8"),
        help="result directory used only with explicit comparator execution",
    )
    return parser.parse_args()


def main() -> int:
    args = _parse_args()

    if not args.execute_registered_comparators:
        print(
            "No comparator branch evaluated. "
            "Use --execute-registered-comparators only after the "
            "implementation-only commit has been frozen."
        )
        return 0

    results = evaluate_registered_comparators()
    write_registered_outputs(results, args.output_dir)

    print(f"Wrote registered comparator outputs to: {args.output_dir}")
    print(f"Primary summary: {_primary_checkpoint_summary(results)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
