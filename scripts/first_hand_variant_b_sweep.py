#!/usr/bin/env python3
"""
Preregistered First Hand Variant-B swept-family evaluator.

IMPORTANT EXECUTION BOUNDARY
----------------------------
This module encodes the mathematics frozen in:

    first_hand_variant_b_swept_family_preregistration_v0.8

Importing this module evaluates zero registered endpoint cells.
Running this file without --execute-registered-variant-b also evaluates zero
registered endpoint cells.

Registered confirmatory matrix:
    25 carriers
    x 8 spiral branches
    x 2 mapping scales
    = 400 geometric endpoint cells

Each cell reports:
    1. directed ambient endpoint angle
    2. unoriented ambient tangent-line angle

No parallel transport, image fitting, parameter optimization, interpolation,
root finding, adaptive grid refinement, AOG-PROSE, S1.5, S2, or arbitrary
carrier/spiral CLI parameter is implemented.
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


CHECKPOINT = "first_hand_variant_b_swept_family_preregistration_v0.8"
VARIANT = "B"
ZERO_TOL_RAD = 1.0e-10

THETA_OUTER = 1.0
SPAN_RAD = 3.0 * math.pi
THETA_INNER = THETA_OUTER + SPAN_RAD

K_G30 = math.tan(math.pi / 6.0)
K_GHALF = math.tan(0.5)
SCALES = (
    ("G30", K_G30),
    ("GHALF", K_GHALF),
)

W_VALUES = (0.02, 0.05, 0.10, 0.20, 0.30)
E_VALUES = (1.4, 1.6, 1.8, 2.0, 2.2)

PHI = (1.0 + math.sqrt(5.0)) / 2.0
B_STAR = math.log(1.0 + 3.0 * math.pi) / (3.0 * math.pi)
LOG_MULTIPLIERS = (0.50, 0.75, 1.00, 1.25, 1.50, 2.00)
B_GOLDEN = 2.0 * math.log(PHI) / math.pi

# Fixed deterministic quadrature used only for the preregistered descriptive
# carrier sphere-likeness diagnostic E_sph. It does not enter endpoint states.
SPHERE_LIKENESS_QUADRATURE_ORDER = 128


@dataclass(frozen=True)
class CarrierSpec:
    carrier_id: str
    w: float
    throat_class: str
    e: float
    R: float
    a: float


@dataclass(frozen=True)
class SpiralSpec:
    spiral_id: str
    family: str
    log_multiplier: Optional[float]
    b: Optional[float]
    radius: Callable[[float], float]
    radius_prime: Callable[[float], float]


@dataclass(frozen=True)
class CellSpec:
    cell_id: str
    carrier_id: str
    spiral_id: str
    scale: str
    k: float


@dataclass(frozen=True)
class AmbientRecord:
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
class SweepResult:
    cell_id: str
    carrier_id: str
    w: float
    throat_class: str
    e: float
    R: float
    a: float
    sphere_likeness_rms: float
    spiral_family: str
    spiral_id: str
    log_multiplier: Optional[float]
    b: Optional[float]
    scale: str
    k: float
    theta_outer: float
    theta_inner: float
    r_outer: Optional[float]
    r_inner: Optional[float]
    u_outer: Optional[float]
    v_outer: Optional[float]
    u_inner: Optional[float]
    v_inner: Optional[float]
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
    parallel_transport_used: bool
    image_pixel_data_used: bool
    technical_error: Optional[str] = None


def throat_class(w: float) -> str:
    if w in (0.02, 0.05):
        return "NARROW"
    if w in (0.10, 0.20):
        return "MODERATE"
    if w == 0.30:
        return "WIDE"
    raise ValueError(f"Unregistered throat value: {w}")


def carrier_R_a(w: float) -> tuple[float, float]:
    w = float(w)
    if not (0.0 < w < 1.0):
        raise ValueError("w must satisfy 0 < w < 1")
    return (1.0 + w) / 2.0, (1.0 - w) / 2.0


def _build_carriers() -> tuple[CarrierSpec, ...]:
    carriers: list[CarrierSpec] = []
    for w in W_VALUES:
        R, a = carrier_R_a(w)
        for e in E_VALUES:
            carriers.append(
                CarrierSpec(
                    carrier_id=f"VB-W{int(round(100*w)):02d}-E{int(round(10*e)):02d}",
                    w=w,
                    throat_class=throat_class(w),
                    e=e,
                    R=R,
                    a=a,
                )
            )
    return tuple(carriers)


REGISTERED_CARRIERS = _build_carriers()
_CARRIER_BY_ID = {carrier.carrier_id: carrier for carrier in REGISTERED_CARRIERS}


def reciprocal_radius(theta: float) -> float:
    theta = float(theta)
    if theta <= 0.0:
        raise ValueError("theta must be positive")
    return 1.0 / theta


def reciprocal_radius_prime(theta: float) -> float:
    theta = float(theta)
    if theta <= 0.0:
        raise ValueError("theta must be positive")
    return -1.0 / (theta * theta)


def logarithmic_radius(theta: float, b: float) -> float:
    return math.exp(-float(b) * (float(theta) - 1.0))


def logarithmic_radius_prime(theta: float, b: float) -> float:
    return -float(b) * logarithmic_radius(theta, b)


def _make_log_spiral(multiplier: float) -> SpiralSpec:
    b = multiplier * B_STAR
    return SpiralSpec(
        spiral_id=f"LOG-M{int(round(100*multiplier)):03d}",
        family="Logarithmic",
        log_multiplier=multiplier,
        b=b,
        radius=lambda theta, _b=b: logarithmic_radius(theta, _b),
        radius_prime=lambda theta, _b=b: logarithmic_radius_prime(theta, _b),
    )


RECIPROCAL_SPIRAL = SpiralSpec(
    spiral_id="RECIPROCAL",
    family="Reciprocal",
    log_multiplier=None,
    b=None,
    radius=reciprocal_radius,
    radius_prime=reciprocal_radius_prime,
)

GENERIC_LOG_SPIRALS = tuple(_make_log_spiral(m) for m in LOG_MULTIPLIERS)

GOLDEN_SPIRAL = SpiralSpec(
    spiral_id="GOLDEN-MEAN",
    family="Golden Mean logarithmic",
    log_multiplier=None,
    b=B_GOLDEN,
    radius=lambda theta: logarithmic_radius(theta, B_GOLDEN),
    radius_prime=lambda theta: logarithmic_radius_prime(theta, B_GOLDEN),
)

REGISTERED_SPIRALS = (
    RECIPROCAL_SPIRAL,
    *GENERIC_LOG_SPIRALS,
    GOLDEN_SPIRAL,
)
_SPIRAL_BY_ID = {spiral.spiral_id: spiral for spiral in REGISTERED_SPIRALS}


def _build_cells() -> tuple[CellSpec, ...]:
    cells: list[CellSpec] = []
    for carrier in REGISTERED_CARRIERS:
        for spiral in REGISTERED_SPIRALS:
            for scale, k in SCALES:
                cells.append(
                    CellSpec(
                        cell_id=f"{carrier.carrier_id}-{spiral.spiral_id}-{scale}",
                        carrier_id=carrier.carrier_id,
                        spiral_id=spiral.spiral_id,
                        scale=scale,
                        k=k,
                    )
                )
    return tuple(cells)


REGISTERED_CELLS = _build_cells()


def carrier_point(carrier: CarrierSpec, u: float, v: float) -> np.ndarray:
    u = float(u)
    v = float(v)
    rho = carrier.R + carrier.a * math.cos(u)
    return np.array(
        [
            rho * math.cos(v),
            rho * math.sin(v),
            carrier.e * carrier.a * math.sin(u),
        ],
        dtype=float,
    )


def carrier_partials(
    carrier: CarrierSpec,
    u: float,
    v: float,
) -> tuple[np.ndarray, np.ndarray]:
    u = float(u)
    v = float(v)

    Xu = np.array(
        [
            -carrier.a * math.sin(u) * math.cos(v),
            -carrier.a * math.sin(u) * math.sin(v),
            carrier.e * carrier.a * math.cos(u),
        ],
        dtype=float,
    )

    rho = carrier.R + carrier.a * math.cos(u)
    Xv = np.array(
        [
            -rho * math.sin(v),
            rho * math.cos(v),
            0.0,
        ],
        dtype=float,
    )

    return Xu, Xv


def carrier_regular_cross_norm_analytic(carrier: CarrierSpec, u: float) -> float:
    u = float(u)
    rho = carrier.R + carrier.a * math.cos(u)
    return (
        carrier.a
        * rho
        * math.sqrt(
            math.sin(u) ** 2
            + carrier.e ** 2 * math.cos(u) ** 2
        )
    )


def carrier_is_analytically_admissible(carrier: CarrierSpec) -> bool:
    return (
        0.0 < carrier.w < 1.0
        and carrier.R - carrier.a > 0.0
        and carrier.a > 0.0
        and carrier.e > 0.0
        and math.isclose(
            carrier.R + carrier.a,
            1.0,
            rel_tol=0.0,
            abs_tol=1.0e-15,
        )
        and math.isclose(
            carrier.R - carrier.a,
            carrier.w,
            rel_tol=0.0,
            abs_tol=1.0e-15,
        )
    )


def carrier_radial_distance(carrier: CarrierSpec, u: float) -> float:
    rho = carrier.R + carrier.a * math.cos(float(u))
    z = carrier.e * carrier.a * math.sin(float(u))
    return math.hypot(rho, z)


def sphere_likeness_rms(carrier: CarrierSpec) -> float:
    nodes, weights = np.polynomial.legendre.leggauss(
        SPHERE_LIKENESS_QUADRATURE_ORDER
    )
    half_span = math.pi / 2.0
    u_values = half_span * nodes
    integrand = np.array(
        [
            (carrier_radial_distance(carrier, u) - 1.0) ** 2
            for u in u_values
        ],
        dtype=float,
    )
    # Integral from -pi/2 to +pi/2 divided by pi.
    integral = half_span * float(np.dot(weights, integrand))
    return math.sqrt(integral / math.pi)


def inverse_gnomonic_fraction(r: float, k: float) -> float:
    r = float(r)
    k = float(k)
    if not (0.0 < r <= 1.0):
        raise ValueError("registered radial fraction must satisfy 0 < r <= 1")
    if k <= 0.0:
        raise ValueError("k must be positive")
    return math.atan(k * r) / math.atan(k)


def meridional_coordinate(r: float, k: float) -> float:
    return math.pi * (1.0 - inverse_gnomonic_fraction(r, k))


def meridional_derivative(r: float, r_prime: float, k: float) -> float:
    r = float(r)
    r_prime = float(r_prime)
    k = float(k)
    return (
        -math.pi
        * k
        * r_prime
        / ((1.0 + (k * r) ** 2) * math.atan(k))
    )


def mapped_coordinates(
    theta: float,
    spiral: SpiralSpec,
    k: float,
) -> tuple[float, float]:
    theta = float(theta)
    r = float(spiral.radius(theta))
    u = meridional_coordinate(r, k)
    v = theta - 1.0
    return u, v


def mapped_curve_point(
    theta: float,
    carrier: CarrierSpec,
    spiral: SpiralSpec,
    k: float,
) -> np.ndarray:
    u, v = mapped_coordinates(theta, spiral, k)
    return carrier_point(carrier, u, v)


def mapped_curve_prime(
    theta: float,
    carrier: CarrierSpec,
    spiral: SpiralSpec,
    k: float,
) -> np.ndarray:
    theta = float(theta)
    r = float(spiral.radius(theta))
    r_prime = float(spiral.radius_prime(theta))
    u, v = mapped_coordinates(theta, spiral, k)
    u_prime = meridional_derivative(r, r_prime, k)
    Xu, Xv = carrier_partials(carrier, u, v)
    return Xu * u_prime + Xv


def mapped_directed_tangent(
    theta: float,
    carrier: CarrierSpec,
    spiral: SpiralSpec,
    k: float,
) -> np.ndarray:
    derivative = mapped_curve_prime(theta, carrier, spiral, k)
    norm = float(np.linalg.norm(derivative))
    if norm == 0.0:
        raise ValueError("mapped curve derivative is zero")
    # inner -> outer means decreasing theta.
    return -derivative / norm


def _as_unit_vector3(value) -> np.ndarray:
    arr = np.asarray(value, dtype=float)
    if arr.shape != (3,):
        raise ValueError(f"Expected a 3-vector, got {arr.shape}")
    if not np.all(np.isfinite(arr)):
        raise ValueError("Vector contains non-finite values")
    norm = float(np.linalg.norm(arr))
    if norm == 0.0:
        raise ValueError("Cannot compare zero vector")
    return arr / norm


def ambient_angle_record(
    tau_outer,
    tau_inner,
    *,
    zero_tolerance_rad: float = ZERO_TOL_RAD,
) -> AmbientRecord:
    a = _as_unit_vector3(tau_outer)
    b = _as_unit_vector3(tau_inner)

    dot_d = float(np.clip(np.dot(a, b), -1.0, 1.0))
    cross_norm_c = float(np.linalg.norm(np.cross(a, b)))

    delta_directed = math.atan2(cross_norm_c, dot_d)
    delta_line = math.atan2(cross_norm_c, abs(dot_d))
    residual = float(np.linalg.norm(a - b))

    return AmbientRecord(
        dot_d=dot_d,
        cross_norm_c=cross_norm_c,
        delta_directed_rad=delta_directed,
        delta_directed_deg=math.degrees(delta_directed),
        residual_directed=residual,
        directed_state=(
            "AMBIENT_DIRECTED_PARALLEL"
            if delta_directed <= zero_tolerance_rad
            else "AMBIENT_DIRECTED_NOT_PARALLEL"
        ),
        delta_line_rad=delta_line,
        delta_line_deg=math.degrees(delta_line),
        line_state=(
            "AMBIENT_LINE_PARALLEL"
            if delta_line <= zero_tolerance_rad
            else "AMBIENT_LINE_NOT_PARALLEL"
        ),
    )


def evaluate_registered_cell(spec: CellSpec) -> SweepResult:
    carrier = _CARRIER_BY_ID[spec.carrier_id]
    spiral = _SPIRAL_BY_ID[spec.spiral_id]
    e_sph = sphere_likeness_rms(carrier)

    try:
        if not carrier_is_analytically_admissible(carrier):
            raise ValueError("registered carrier failed analytic admissibility")

        r_outer = float(spiral.radius(THETA_OUTER))
        r_inner = float(spiral.radius(THETA_INNER))

        u_outer, v_outer = mapped_coordinates(
            THETA_OUTER,
            spiral,
            spec.k,
        )
        u_inner, v_inner = mapped_coordinates(
            THETA_INNER,
            spiral,
            spec.k,
        )

        p_outer = mapped_curve_point(
            THETA_OUTER,
            carrier,
            spiral,
            spec.k,
        )
        p_inner = mapped_curve_point(
            THETA_INNER,
            carrier,
            spiral,
            spec.k,
        )

        tau_outer = mapped_directed_tangent(
            THETA_OUTER,
            carrier,
            spiral,
            spec.k,
        )
        tau_inner = mapped_directed_tangent(
            THETA_INNER,
            carrier,
            spiral,
            spec.k,
        )

        angles = ambient_angle_record(tau_outer, tau_inner)

        return SweepResult(
            cell_id=spec.cell_id,
            carrier_id=carrier.carrier_id,
            w=carrier.w,
            throat_class=carrier.throat_class,
            e=carrier.e,
            R=carrier.R,
            a=carrier.a,
            sphere_likeness_rms=e_sph,
            spiral_family=spiral.family,
            spiral_id=spiral.spiral_id,
            log_multiplier=spiral.log_multiplier,
            b=spiral.b,
            scale=spec.scale,
            k=spec.k,
            theta_outer=THETA_OUTER,
            theta_inner=THETA_INNER,
            r_outer=r_outer,
            r_inner=r_inner,
            u_outer=u_outer,
            v_outer=v_outer,
            u_inner=u_inner,
            v_inner=v_inner,
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
            parallel_transport_used=False,
            image_pixel_data_used=False,
        )

    except Exception as exc:
        return SweepResult(
            cell_id=spec.cell_id,
            carrier_id=carrier.carrier_id,
            w=carrier.w,
            throat_class=carrier.throat_class,
            e=carrier.e,
            R=carrier.R,
            a=carrier.a,
            sphere_likeness_rms=e_sph,
            spiral_family=spiral.family,
            spiral_id=spiral.spiral_id,
            log_multiplier=spiral.log_multiplier,
            b=spiral.b,
            scale=spec.scale,
            k=spec.k,
            theta_outer=THETA_OUTER,
            theta_inner=THETA_INNER,
            r_outer=None,
            r_inner=None,
            u_outer=None,
            v_outer=None,
            u_inner=None,
            v_inner=None,
            p_outer=None,
            p_inner=None,
            tau_outer=None,
            tau_inner=None,
            dot_d=None,
            cross_norm_c=None,
            delta_ambient_directed_rad=None,
            delta_ambient_directed_deg=None,
            residual_ambient_directed=None,
            directed_state="VARIANT_B_TECHNICAL_FAILURE",
            delta_ambient_line_rad=None,
            delta_ambient_line_deg=None,
            line_state="VARIANT_B_TECHNICAL_FAILURE",
            parallel_transport_used=False,
            image_pixel_data_used=False,
            technical_error=f"{type(exc).__name__}: {exc}",
        )


def evaluate_registered_cells() -> list[SweepResult]:
    """Evaluate exactly the 400 preregistered Variant-B cells."""
    return [evaluate_registered_cell(spec) for spec in REGISTERED_CELLS]


def _successful_results(results: list[SweepResult]) -> list[SweepResult]:
    return [r for r in results if r.technical_error is None]


def _technical_failure_count(results: list[SweepResult]) -> int:
    return sum(r.technical_error is not None for r in results)


def reciprocal_directed_summary(results: list[SweepResult]) -> str:
    recips = [r for r in results if r.spiral_id == "RECIPROCAL"]
    if any(r.technical_error is not None for r in recips):
        return "RECIPROCAL_DIRECTED_INCOMPLETE"
    if any(r.directed_state == "AMBIENT_DIRECTED_PARALLEL" for r in recips):
        return "RECIPROCAL_DIRECTED_PARALLEL_CELL_FOUND"
    return "NO_REGISTERED_RECIPROCAL_DIRECTED_PARALLEL_CELL"


def reciprocal_line_summary(results: list[SweepResult]) -> str:
    recips = [r for r in results if r.spiral_id == "RECIPROCAL"]
    if any(r.technical_error is not None for r in recips):
        return "RECIPROCAL_LINE_INCOMPLETE"
    if any(r.line_state == "AMBIENT_LINE_PARALLEL" for r in recips):
        return "RECIPROCAL_LINE_PARALLEL_CELL_FOUND"
    return "NO_REGISTERED_RECIPROCAL_LINE_PARALLEL_CELL"


def _is_log_family(result: SweepResult) -> bool:
    return (
        result.spiral_family == "Logarithmic"
        or result.spiral_family == "Golden Mean logarithmic"
    )


def log_directed_summary(results: list[SweepResult]) -> str:
    logs = [r for r in results if _is_log_family(r)]
    if any(r.technical_error is not None for r in logs):
        return "LOG_DIRECTED_INCOMPLETE"
    if any(r.directed_state == "AMBIENT_DIRECTED_PARALLEL" for r in logs):
        return "LOG_DIRECTED_COUNTEREXAMPLE_FOUND"
    return "NO_REGISTERED_LOG_DIRECTED_COUNTEREXAMPLE"


def log_line_summary(results: list[SweepResult]) -> str:
    logs = [r for r in results if _is_log_family(r)]
    if any(r.technical_error is not None for r in logs):
        return "LOG_LINE_INCOMPLETE"
    if any(r.line_state == "AMBIENT_LINE_PARALLEL" for r in logs):
        return "LOG_LINE_COUNTEREXAMPLE_FOUND"
    return "NO_REGISTERED_LOG_LINE_COUNTEREXAMPLE"


def _minimum_record(
    results: list[SweepResult],
    *,
    angle_field: str,
) -> Optional[dict]:
    valid = [
        r
        for r in results
        if r.technical_error is None
        and getattr(r, angle_field) is not None
    ]
    if not valid:
        return None
    best = min(valid, key=lambda r: getattr(r, angle_field))
    return {
        "cell_id": best.cell_id,
        "carrier_id": best.carrier_id,
        "w": best.w,
        "e": best.e,
        "throat_class": best.throat_class,
        "spiral_id": best.spiral_id,
        "spiral_family": best.spiral_family,
        "scale": best.scale,
        "k": best.k,
        "sphere_likeness_rms": best.sphere_likeness_rms,
        "angle_deg": getattr(best, angle_field),
    }


def descriptive_minima(results: list[SweepResult]) -> dict:
    reciprocal = [r for r in results if r.spiral_id == "RECIPROCAL"]
    all_logs = [r for r in results if _is_log_family(r)]

    per_log: dict[str, dict] = {}
    for spiral in (*GENERIC_LOG_SPIRALS, GOLDEN_SPIRAL):
        subset = [r for r in results if r.spiral_id == spiral.spiral_id]
        per_log[spiral.spiral_id] = {
            "directed": _minimum_record(
                subset,
                angle_field="delta_ambient_directed_deg",
            ),
            "line": _minimum_record(
                subset,
                angle_field="delta_ambient_line_deg",
            ),
        }

    return {
        "reciprocal": {
            "directed": _minimum_record(
                reciprocal,
                angle_field="delta_ambient_directed_deg",
            ),
            "line": _minimum_record(
                reciprocal,
                angle_field="delta_ambient_line_deg",
            ),
        },
        "per_log_family": per_log,
        "global_logarithmic": {
            "directed": _minimum_record(
                all_logs,
                angle_field="delta_ambient_directed_deg",
            ),
            "line": _minimum_record(
                all_logs,
                angle_field="delta_ambient_line_deg",
            ),
        },
    }


def carrier_metric_rows() -> list[dict]:
    return [
        {
            "carrier_id": carrier.carrier_id,
            "w": carrier.w,
            "throat_class": carrier.throat_class,
            "e": carrier.e,
            "R": carrier.R,
            "a": carrier.a,
            "outer_equatorial_radius": carrier.R + carrier.a,
            "throat_radius": carrier.R - carrier.a,
            "sphere_likeness_rms": sphere_likeness_rms(carrier),
            "analytic_admissible": carrier_is_analytically_admissible(carrier),
            "genus": 1,
        }
        for carrier in REGISTERED_CARRIERS
    ]


def _write_results_csv(results: list[SweepResult], path: Path) -> None:
    rows = [asdict(result) for result in results]
    if not rows:
        raise ValueError("No Variant-B results to write")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def _write_carrier_csv(path: Path) -> None:
    rows = carrier_metric_rows()
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def _write_json(results: list[SweepResult], path: Path) -> None:
    metrics = carrier_metric_rows()
    payload = {
        "checkpoint": CHECKPOINT,
        "variant": VARIANT,
        "registered_carrier_count": len(REGISTERED_CARRIERS),
        "registered_spiral_count": len(REGISTERED_SPIRALS),
        "registered_scale_count": len(SCALES),
        "registered_cell_count": len(REGISTERED_CELLS),
        "parallel_transport_used": False,
        "image_pixel_data_used": False,
        "adaptive_refinement_used": False,
        "technical_failure_count": _technical_failure_count(results),
        "reciprocal_directed_summary": reciprocal_directed_summary(results),
        "reciprocal_line_summary": reciprocal_line_summary(results),
        "log_directed_summary": log_directed_summary(results),
        "log_line_summary": log_line_summary(results),
        "carrier_sphere_likeness_range": {
            "min": min(row["sphere_likeness_rms"] for row in metrics),
            "max": max(row["sphere_likeness_rms"] for row in metrics),
        },
        "descriptive_minima": descriptive_minima(results),
        "results": [asdict(result) for result in results],
    }
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _fmt(value: Optional[float], digits: int = 12) -> str:
    if value is None:
        return "NA"
    return f"{value:.{digits}g}"


def _write_report(results: list[SweepResult], path: Path) -> None:
    metrics = carrier_metric_rows()
    minima = descriptive_minima(results)

    lines = [
        "# First Hand Variant-B Swept-Family Results",
        "",
        f"**Checkpoint:** `{CHECKPOINT}`  ",
        "**Carrier:** normalized elliptic fat torus  ",
        "**Historical span:** 1.5 turns  ",
        f"**Registered cells:** {len(REGISTERED_CELLS)}  ",
        "**Parallel transport used:** no  ",
        "**Image pixel data used:** no  ",
        "**Adaptive refinement used:** no",
        "",
        "## Carrier family",
        "",
        r"\[",
        r"X_{w,e}(u,v)=((R+a\cos u)\cos v,\,(R+a\cos u)\sin v,\,ea\sin u),",
        r"\]",
        "",
        r"\[",
        r"R=(1+w)/2,\qquad a=(1-w)/2.",
        r"\]",
        "",
        "All 25 registered carriers satisfy `analytic_admissible=true` and "
        "are embedded genus-1 tori because `R-a=w>0`.",
        "",
        "Sphere-likeness diagnostic range:",
        "",
        f"- minimum: {_fmt(min(row['sphere_likeness_rms'] for row in metrics))}",
        f"- maximum: {_fmt(max(row['sphere_likeness_rms'] for row in metrics))}",
        "",
        "## Primary summaries",
        "",
        f"Reciprocal directed: `{reciprocal_directed_summary(results)}`",
        "",
        f"Reciprocal line: `{reciprocal_line_summary(results)}`",
        "",
        f"Logarithmic directed: `{log_directed_summary(results)}`",
        "",
        f"Logarithmic line: `{log_line_summary(results)}`",
        "",
        f"Technical failures: `{_technical_failure_count(results)}`",
        "",
        "## Reciprocal fixed-grid minima",
        "",
        "| Semantics | Angle (deg) | Cell |",
        "|---|---:|---|",
    ]

    for semantic in ("directed", "line"):
        item = minima["reciprocal"][semantic]
        lines.append(
            f"| {semantic} | {_fmt(None if item is None else item['angle_deg'])} | "
            f"`{'NA' if item is None else item['cell_id']}` |"
        )

    lines.extend(
        [
            "",
            "## Per-log-family fixed-grid minima",
            "",
            "| Spiral | Directed min (deg) | Directed cell | "
            "Line min (deg) | Line cell |",
            "|---|---:|---|---:|---|",
        ]
    )

    for spiral_id, record in minima["per_log_family"].items():
        d = record["directed"]
        l = record["line"]
        lines.append(
            f"| `{spiral_id}` | "
            f"{_fmt(None if d is None else d['angle_deg'])} | "
            f"`{'NA' if d is None else d['cell_id']}` | "
            f"{_fmt(None if l is None else l['angle_deg'])} | "
            f"`{'NA' if l is None else l['cell_id']}` |"
        )

    lines.extend(
        [
            "",
            "## Global logarithmic fixed-grid minima",
            "",
        ]
    )

    for semantic in ("directed", "line"):
        item = minima["global_logarithmic"][semantic]
        lines.append(
            f"- {semantic}: "
            f"{_fmt(None if item is None else item['angle_deg'])} deg "
            f"at `{'NA' if item is None else item['cell_id']}`"
        )

    lines.extend(
        [
            "",
            "## Interpretation boundary",
            "",
            "These are fixed-grid results for one preregistered, source-constrained "
            "analytic Variant-B carrier family. They do not establish the "
            "continuous optimum over carrier parameters and do not identify a "
            "unique historical Dimpled-Sphere.",
            "",
            "No interpolation, optimization, root finding, or adaptive "
            "refinement was used.",
            "",
        ]
    )

    path.write_text("\n".join(lines), encoding="utf-8")


def write_registered_outputs(
    results: list[SweepResult],
    output_dir: Path,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    _write_json(results, output_dir / "variant_b_sweep_results.json")
    _write_results_csv(results, output_dir / "variant_b_sweep_results.csv")
    _write_report(results, output_dir / "variant_b_sweep_report.md")
    _write_carrier_csv(output_dir / "variant_b_carrier_metrics.csv")


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Preregistered First Hand Variant-B swept-family evaluator"
    )
    parser.add_argument(
        "--execute-registered-variant-b",
        action="store_true",
        help="explicitly execute exactly the 400 preregistered Variant-B cells",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("results/first_hand_variant_b_sweep_v0_8"),
        help="result directory used only during explicit registered execution",
    )
    return parser.parse_args()


def main() -> int:
    args = _parse_args()

    if not args.execute_registered_variant_b:
        print(
            "No registered Variant-B endpoint cell evaluated. "
            "Use --execute-registered-variant-b only after the "
            "implementation-only commit has been frozen."
        )
        return 0

    results = evaluate_registered_cells()
    write_registered_outputs(results, args.output_dir)

    print(f"Wrote registered Variant-B outputs to: {args.output_dir}")
    print(f"Registered cells executed: {len(results)}")
    print(f"Technical failures: {_technical_failure_count(results)}")
    print(f"Reciprocal directed: {reciprocal_directed_summary(results)}")
    print(f"Reciprocal line: {reciprocal_line_summary(results)}")
    print(f"Log directed: {log_directed_summary(results)}")
    print(f"Log line: {log_line_summary(results)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
