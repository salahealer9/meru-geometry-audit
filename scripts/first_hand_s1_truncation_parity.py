#!/usr/bin/env python3
"""
Preregistered First Hand S1 truncation-parity evaluator.

IMPORTANT EXECUTION BOUNDARY
----------------------------
This module encodes the mathematics frozen in:

    first_hand_s1_truncation_parity_preregistration_v0.8

Importing this module does not evaluate any newly registered S1 cell.
Running this file without --execute-registered-parity also does not evaluate
any newly registered S1 cell.

The implementation contains exactly 54 new execution cells:
    36 generic logarithmic parity cells
     6 Golden Mean parity cells
     6 reciprocal truncation cells
     6 endpoint-matched Archimedean truncation cells

All L = 3*pi values are immutable references inherited from completed v0.8
checkpoints. They are never recomputed here.

No continuous truncation scan, logarithmic-rate optimization, new scale,
AOG-PROSE proxy, new comparator family, alternate projection, S1.5, S2,
Variant-B/dimpled-sphere construction, or image-derived fitting is implemented.
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

from first_hand_s1 import (
    AntipodalTransportError,
    K_G30,
    K_GHALF,
    S1_ZERO_TOL_RAD,
    minimal_sphere_transport,
)


CHECKPOINT = "first_hand_s1_truncation_parity_preregistration_v0.8"
VARIANT = "A"
THETA0 = 1.0
PHI = (1.0 + math.sqrt(5.0)) / 2.0

TURNS = (1.0, 1.5, 2.0, 2.5)
SPANS = {
    1.0: 2.0 * math.pi,
    1.5: 3.0 * math.pi,
    2.0: 4.0 * math.pi,
    2.5: 5.0 * math.pi,
}
NEW_TURNS = (1.0, 2.0, 2.5)
REFERENCE_TURN = 1.5

INTEGER_TURNS = (1.0, 2.0)
ODD_HALF_TURNS = (1.5, 2.5)

SCALES = (
    ("G30", K_G30),
    ("GHALF", K_GHALF),
)

L_REFERENCE = SPANS[REFERENCE_TURN]
B_STAR = math.log(1.0 + L_REFERENCE) / L_REFERENCE
LOG_MULTIPLIERS = (0.50, 0.75, 1.00, 1.25, 1.50, 2.00)
LOG_RATES = {
    multiplier: multiplier * B_STAR
    for multiplier in LOG_MULTIPLIERS
}
B_GOLDEN = 2.0 * math.log(PHI) / math.pi

# ---------------------------------------------------------------------------
# Immutable L = 3*pi references from completed checkpoints.
# These are scientific inputs. They are not recomputed in this module.
# ---------------------------------------------------------------------------

REFERENCE_RECIPROCAL_DEG = {
    "G30": 144.5776221089075,
    "GHALF": 144.2022631722743,
}

REFERENCE_ARCHIMEDES_DEG = {
    "G30": 139.79273839892204,
    "GHALF": 139.8512318072602,
}

REFERENCE_GOLDEN_DEG = {
    "G30": 177.83451557340433,
    "GHALF": 178.0229980713949,
}

REFERENCE_LOG_GRID_DEG = {
    ("G30", 0.50): 179.16765948673287,
    ("G30", 0.75): 178.6609923590221,
    ("G30", 1.00): 178.20896633780404,
    ("G30", 1.25): 177.80656872081175,
    ("G30", 1.50): 177.44865062838156,
    ("G30", 2.00): 176.85885439634833,
    ("GHALF", 0.50): 179.23782073857865,
    ("GHALF", 0.75): 178.77605472595295,
    ("GHALF", 1.00): 178.36412508643232,
    ("GHALF", 1.25): 177.99754741884183,
    ("GHALF", 1.50): 177.67177619386672,
    ("GHALF", 2.00): 177.13607539488768,
}


@dataclass(frozen=True)
class CurveSpec:
    curve_id: str
    family: str
    equation_label: str
    growth_parameter: Optional[float]
    log_multiplier: Optional[float]
    radius: Callable[[float, float], float]
    radius_prime: Callable[[float, float], float]


@dataclass(frozen=True)
class NewCellSpec:
    cell_id: str
    curve_id: str
    family: str
    turns: float
    span_rad: float
    parity_class: str
    scale: str
    k: float
    growth_parameter: Optional[float]
    log_multiplier: Optional[float]


@dataclass
class NewCellResult:
    cell_id: str
    record_origin: str
    curve_id: str
    family: str
    turns: float
    span_rad: float
    parity_class: str
    theta0: float
    scale: str
    k: float
    growth_parameter: Optional[float]
    log_multiplier: Optional[float]
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
    absolute_s1_state: str
    image_pixel_data_used: bool
    technical_error: Optional[str] = None


def parity_class(turns: float) -> str:
    if turns in INTEGER_TURNS:
        return "INTEGER_TURN"
    if turns in ODD_HALF_TURNS:
        return "ODD_HALF_INTEGER_TURN"
    raise ValueError(f"Unregistered turn count: {turns}")


# ---------------------------------------------------------------------------
# Frozen radial laws.
# ---------------------------------------------------------------------------

def logarithmic_radius(u: float, span: float, b: float) -> float:
    _ = float(span)  # span affects truncation only; b is fixed across spans.
    return math.exp(-float(b) * float(u))


def logarithmic_radius_prime(u: float, span: float, b: float) -> float:
    return -float(b) * logarithmic_radius(u, span, b)


def reciprocal_radius(u: float, span: float) -> float:
    _ = float(span)
    return 1.0 / (1.0 + float(u))


def reciprocal_radius_prime(u: float, span: float) -> float:
    _ = float(span)
    denom = 1.0 + float(u)
    return -1.0 / (denom * denom)


def reciprocal_inner_radius(span: float) -> float:
    return 1.0 / (1.0 + float(span))


def archimedean_radius(u: float, span: float) -> float:
    span = float(span)
    q = reciprocal_inner_radius(span)
    return 1.0 - ((1.0 - q) / span) * float(u)


def archimedean_radius_prime(u: float, span: float) -> float:
    _ = float(u)
    span = float(span)
    q = reciprocal_inner_radius(span)
    return -(1.0 - q) / span


def _make_log_curve(multiplier: float) -> CurveSpec:
    b = LOG_RATES[multiplier]
    return CurveSpec(
        curve_id=f"LOG-M{int(round(multiplier * 100)):03d}",
        family="Logarithmic",
        equation_label=f"r(u)=exp(-{b:.17g} u)",
        growth_parameter=b,
        log_multiplier=multiplier,
        radius=lambda u, span, _b=b: logarithmic_radius(u, span, _b),
        radius_prime=lambda u, span, _b=b: logarithmic_radius_prime(u, span, _b),
    )


LOG_CURVES = tuple(_make_log_curve(m) for m in LOG_MULTIPLIERS)

GOLDEN_CURVE = CurveSpec(
    curve_id="GOLDEN-MEAN",
    family="Golden Mean logarithmic",
    equation_label=f"r(u)=exp(-{B_GOLDEN:.17g} u)",
    growth_parameter=B_GOLDEN,
    log_multiplier=None,
    radius=lambda u, span: logarithmic_radius(u, span, B_GOLDEN),
    radius_prime=lambda u, span: logarithmic_radius_prime(u, span, B_GOLDEN),
)

RECIPROCAL_CURVE = CurveSpec(
    curve_id="RECIPROCAL",
    family="Reciprocal",
    equation_label="r(u)=1/(1+u)",
    growth_parameter=None,
    log_multiplier=None,
    radius=reciprocal_radius,
    radius_prime=reciprocal_radius_prime,
)

ARCHIMEDES_CURVE = CurveSpec(
    curve_id="ARCHIMEDES-ENDPOINT-MATCHED",
    family="Archimedean",
    equation_label="r(u;L)=1-((1-q_R(L))/L)u",
    growth_parameter=None,
    log_multiplier=None,
    radius=archimedean_radius,
    radius_prime=archimedean_radius_prime,
)

ALL_CURVES = LOG_CURVES + (
    GOLDEN_CURVE,
    RECIPROCAL_CURVE,
    ARCHIMEDES_CURVE,
)

_CURVE_BY_ID = {curve.curve_id: curve for curve in ALL_CURVES}


# ---------------------------------------------------------------------------
# Exact registered new-cell matrix: 54 new cells, no L=3*pi cells.
# ---------------------------------------------------------------------------

def _build_new_cells() -> tuple[NewCellSpec, ...]:
    cells: list[NewCellSpec] = []

    for curve in LOG_CURVES:
        for turns in NEW_TURNS:
            span = SPANS[turns]
            for scale, k in SCALES:
                cells.append(
                    NewCellSpec(
                        cell_id=f"{curve.curve_id}-T{turns:g}-{scale}",
                        curve_id=curve.curve_id,
                        family=curve.family,
                        turns=turns,
                        span_rad=span,
                        parity_class=parity_class(turns),
                        scale=scale,
                        k=k,
                        growth_parameter=curve.growth_parameter,
                        log_multiplier=curve.log_multiplier,
                    )
                )

    for curve in (GOLDEN_CURVE, RECIPROCAL_CURVE, ARCHIMEDES_CURVE):
        for turns in NEW_TURNS:
            span = SPANS[turns]
            for scale, k in SCALES:
                cells.append(
                    NewCellSpec(
                        cell_id=f"{curve.curve_id}-T{turns:g}-{scale}",
                        curve_id=curve.curve_id,
                        family=curve.family,
                        turns=turns,
                        span_rad=span,
                        parity_class=parity_class(turns),
                        scale=scale,
                        k=k,
                        growth_parameter=curve.growth_parameter,
                        log_multiplier=curve.log_multiplier,
                    )
                )

    return tuple(cells)


REGISTERED_NEW_CELLS = _build_new_cells()


# ---------------------------------------------------------------------------
# Planar theorem utilities. These do not evaluate spherical S1.
# ---------------------------------------------------------------------------

def planar_log_tangent_vector(u: float, b: float) -> np.ndarray:
    """
    Unnormalised planar tangent for r=e^{-bu}, theta=theta0+u:

        x'(u) = e^{-bu} R(theta0+u) (-b, 1).

    Used only for symbolic/numerical verification of the preregistered planar
    parity theorem, not for spherical S1 execution.
    """
    u = float(u)
    b = float(b)
    theta = THETA0 + u
    base = np.array([-b, 1.0], dtype=float)
    rot = np.array(
        [
            [math.cos(theta), -math.sin(theta)],
            [math.sin(theta), math.cos(theta)],
        ],
        dtype=float,
    )
    return math.exp(-b * u) * (rot @ base)


# ---------------------------------------------------------------------------
# Generic Variant-A spherical curve and derivative for arbitrary registered L.
# ---------------------------------------------------------------------------

def spherical_curve(
    u: float,
    span: float,
    k: float,
    curve: CurveSpec,
) -> np.ndarray:
    u = float(u)
    span = float(span)
    k = float(k)

    if span not in SPANS.values():
        raise ValueError("span is not preregistered")
    if not (0.0 <= u <= span):
        raise ValueError("u must satisfy 0 <= u <= span")
    if k <= 0.0:
        raise ValueError("k must satisfy k > 0")

    r = float(curve.radius(u, span))
    if not math.isfinite(r) or r <= 0.0:
        raise ValueError("registered radius must be finite and positive")

    theta = THETA0 + u
    n = np.array(
        [
            k * r * math.cos(theta),
            k * r * math.sin(theta),
            1.0,
        ],
        dtype=float,
    )
    return n / math.sqrt(1.0 + (k * r) ** 2)


def spherical_curve_prime(
    u: float,
    span: float,
    k: float,
    curve: CurveSpec,
) -> np.ndarray:
    u = float(u)
    span = float(span)
    k = float(k)

    if span not in SPANS.values():
        raise ValueError("span is not preregistered")
    if not (0.0 <= u <= span):
        raise ValueError("u must satisfy 0 <= u <= span")
    if k <= 0.0:
        raise ValueError("k must satisfy k > 0")

    r = float(curve.radius(u, span))
    rp = float(curve.radius_prime(u, span))

    if not (math.isfinite(r) and math.isfinite(rp)):
        raise ValueError("registered radius and derivative must be finite")
    if r <= 0.0:
        raise ValueError("registered radius must be positive")

    theta = THETA0 + u
    ct = math.cos(theta)
    st = math.sin(theta)

    n = np.array(
        [k * r * ct, k * r * st, 1.0],
        dtype=float,
    )
    n_prime = np.array(
        [
            k * (rp * ct - r * st),
            k * (rp * st + r * ct),
            0.0,
        ],
        dtype=float,
    )

    s = math.sqrt(1.0 + (k * r) ** 2)
    return n_prime / s - n * (k * k * r * rp) / (s ** 3)


def directed_tangent(
    u: float,
    span: float,
    k: float,
    curve: CurveSpec,
) -> np.ndarray:
    derivative = spherical_curve_prime(u, span, k, curve)
    norm = float(np.linalg.norm(derivative))
    if norm == 0.0:
        raise ValueError("spherical derivative is zero")
    return -derivative / norm


# ---------------------------------------------------------------------------
# New S1 execution. Intentionally not called by import/default CLI/tests.
# ---------------------------------------------------------------------------

def evaluate_new_cell(spec: NewCellSpec) -> NewCellResult:
    curve = _CURVE_BY_ID[spec.curve_id]

    try:
        span = spec.span_rad
        r_outer = float(curve.radius(0.0, span))
        r_inner = float(curve.radius(span, span))

        p_outer = spherical_curve(0.0, span, spec.k, curve)
        p_inner = spherical_curve(span, span, spec.k, curve)
        tau_outer = directed_tangent(0.0, span, spec.k, curve)
        tau_inner = directed_tangent(span, span, spec.k, curve)

        try:
            transport = minimal_sphere_transport(
                p_outer,
                p_inner,
                tau_outer,
            )
        except AntipodalTransportError:
            return NewCellResult(
                cell_id=spec.cell_id,
                record_origin="new_execution",
                curve_id=spec.curve_id,
                family=spec.family,
                turns=spec.turns,
                span_rad=span,
                parity_class=spec.parity_class,
                theta0=THETA0,
                scale=spec.scale,
                k=spec.k,
                growth_parameter=spec.growth_parameter,
                log_multiplier=spec.log_multiplier,
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
                absolute_s1_state="S1_TRANSPORT_UNDEFINED_ANTIPODAL",
                image_pixel_data_used=False,
            )

        transported = transport.vector
        d = float(np.clip(np.dot(transported, tau_inner), -1.0, 1.0))
        c = float(np.linalg.norm(np.cross(transported, tau_inner)))
        delta = math.atan2(c, d)
        residual = float(np.linalg.norm(transported - tau_inner))

        absolute_state = (
            "S1_DIRECTED_COMPATIBLE"
            if delta <= S1_ZERO_TOL_RAD
            else "S1_DIRECTED_NOT_COMPATIBLE"
        )

        return NewCellResult(
            cell_id=spec.cell_id,
            record_origin="new_execution",
            curve_id=spec.curve_id,
            family=spec.family,
            turns=spec.turns,
            span_rad=span,
            parity_class=spec.parity_class,
            theta0=THETA0,
            scale=spec.scale,
            k=spec.k,
            growth_parameter=spec.growth_parameter,
            log_multiplier=spec.log_multiplier,
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
            absolute_s1_state=absolute_state,
            image_pixel_data_used=False,
        )

    except Exception as exc:
        return NewCellResult(
            cell_id=spec.cell_id,
            record_origin="new_execution",
            curve_id=spec.curve_id,
            family=spec.family,
            turns=spec.turns,
            span_rad=spec.span_rad,
            parity_class=spec.parity_class,
            theta0=THETA0,
            scale=spec.scale,
            k=spec.k,
            growth_parameter=spec.growth_parameter,
            log_multiplier=spec.log_multiplier,
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
            absolute_s1_state="S1_TECHNICAL_FAILURE",
            image_pixel_data_used=False,
            technical_error=f"{type(exc).__name__}: {exc}",
        )


def evaluate_registered_new_cells() -> list[NewCellResult]:
    """Evaluate exactly the 54 newly preregistered cells."""
    return [evaluate_new_cell(spec) for spec in REGISTERED_NEW_CELLS]


# ---------------------------------------------------------------------------
# Immutable reference records and combined-analysis helpers.
# ---------------------------------------------------------------------------

def _reference_delta_deg(
    curve_id: str,
    scale: str,
    multiplier: Optional[float],
) -> float:
    if curve_id == "RECIPROCAL":
        return REFERENCE_RECIPROCAL_DEG[scale]
    if curve_id == "ARCHIMEDES-ENDPOINT-MATCHED":
        return REFERENCE_ARCHIMEDES_DEG[scale]
    if curve_id == "GOLDEN-MEAN":
        return REFERENCE_GOLDEN_DEG[scale]
    if curve_id.startswith("LOG-M"):
        if multiplier is None:
            raise ValueError("log reference requires multiplier")
        return REFERENCE_LOG_GRID_DEG[(scale, multiplier)]
    raise KeyError(curve_id)


def reference_records() -> list[dict]:
    """Return inherited L=3*pi records without evaluating spherical geometry."""
    records: list[dict] = []

    for curve in LOG_CURVES + (
        GOLDEN_CURVE,
        RECIPROCAL_CURVE,
        ARCHIMEDES_CURVE,
    ):
        for scale, k in SCALES:
            delta_deg = _reference_delta_deg(
                curve.curve_id,
                scale,
                curve.log_multiplier,
            )
            records.append(
                {
                    "cell_id": f"{curve.curve_id}-T1.5-{scale}",
                    "record_origin": "inherited_reference",
                    "source_checkpoint": (
                        "first_hand_s1_comparator_preregistration_v0.8"
                        if curve.curve_id != "RECIPROCAL"
                        else "first_hand_analytic_s1_preregistration_v0.8"
                    ),
                    "curve_id": curve.curve_id,
                    "family": curve.family,
                    "turns": 1.5,
                    "span_rad": L_REFERENCE,
                    "parity_class": "ODD_HALF_INTEGER_TURN",
                    "theta0": THETA0,
                    "scale": scale,
                    "k": k,
                    "growth_parameter": curve.growth_parameter,
                    "log_multiplier": curve.log_multiplier,
                    "delta_s1_deg": delta_deg,
                    "delta_s1_rad": math.radians(delta_deg),
                    "image_pixel_data_used": False,
                }
            )

    return records


def _new_result_map(results: list[NewCellResult]) -> dict[tuple[str, float, str], NewCellResult]:
    return {
        (r.curve_id, r.turns, r.scale): r
        for r in results
    }


def _delta_deg(
    results_map: dict[tuple[str, float, str], NewCellResult],
    curve: CurveSpec,
    turns: float,
    scale: str,
) -> Optional[float]:
    if turns == 1.5:
        return _reference_delta_deg(curve.curve_id, scale, curve.log_multiplier)

    result = results_map[(curve.curve_id, turns, scale)]
    return result.delta_s1_deg


def parity_state_for_curve_scale(
    results_map: dict[tuple[str, float, str], NewCellResult],
    curve: CurveSpec,
    scale: str,
) -> str:
    values: dict[float, float] = {}

    for turns in TURNS:
        value = _delta_deg(results_map, curve, turns, scale)
        if value is None:
            return "PARITY_COMPARISON_INCOMPLETE"
        values[turns] = value

    integer_max = max(values[1.0], values[2.0])
    odd_half_min = min(values[1.5], values[2.5])

    if integer_max < odd_half_min:
        return "PARITY_SEPARATION_CONFIRMED"

    return "PARITY_SEPARATION_NOT_CONFIRMED"


def parity_contrast_deg(
    results_map: dict[tuple[str, float, str], NewCellResult],
    curve: CurveSpec,
    scale: str,
) -> Optional[float]:
    values: dict[float, float] = {}

    for turns in TURNS:
        value = _delta_deg(results_map, curve, turns, scale)
        if value is None:
            return None
        values[turns] = value

    mean_integer = 0.5 * (values[1.0] + values[2.0])
    mean_odd_half = 0.5 * (values[1.5] + values[2.5])
    return mean_odd_half - mean_integer


def generic_log_global_summary(results: list[NewCellResult]) -> str:
    results_map = _new_result_map(results)
    states = [
        parity_state_for_curve_scale(results_map, curve, scale)
        for curve in LOG_CURVES
        for scale, _ in SCALES
    ]

    if any(state == "PARITY_COMPARISON_INCOMPLETE" for state in states):
        return "PARITY_LOG_GRID_INCOMPLETE"

    if all(state == "PARITY_SEPARATION_CONFIRMED" for state in states):
        return "PARITY_SEPARATION_CONFIRMED_ALL_LOG_GRID_CELLS"

    return "PARITY_SEPARATION_NOT_CONFIRMED_ALL_LOG_GRID_CELLS"


def golden_global_summary(results: list[NewCellResult]) -> str:
    results_map = _new_result_map(results)
    states = [
        parity_state_for_curve_scale(results_map, GOLDEN_CURVE, scale)
        for scale, _ in SCALES
    ]

    if any(state == "PARITY_COMPARISON_INCOMPLETE" for state in states):
        return "PARITY_GOLDEN_MEAN_INCOMPLETE"

    if all(state == "PARITY_SEPARATION_CONFIRMED" for state in states):
        return "PARITY_SEPARATION_CONFIRMED_GOLDEN_MEAN"

    return "PARITY_SEPARATION_NOT_CONFIRMED_GOLDEN_MEAN"


def _relative_difference_deg(
    results_map: dict[tuple[str, float, str], NewCellResult],
    comparator: CurveSpec,
    turns: float,
    scale: str,
) -> Optional[float]:
    comparator_delta = _delta_deg(results_map, comparator, turns, scale)
    reciprocal_delta = _delta_deg(results_map, RECIPROCAL_CURVE, turns, scale)

    if comparator_delta is None or reciprocal_delta is None:
        return None

    return comparator_delta - reciprocal_delta


# ---------------------------------------------------------------------------
# Output writers. Called only after explicit registered execution.
# ---------------------------------------------------------------------------

def _write_json(results: list[NewCellResult], output_path: Path) -> None:
    results_map = _new_result_map(results)

    parity_rows = []
    for curve in LOG_CURVES + (GOLDEN_CURVE,):
        for scale, _ in SCALES:
            parity_rows.append(
                {
                    "curve_id": curve.curve_id,
                    "scale": scale,
                    "state": parity_state_for_curve_scale(
                        results_map,
                        curve,
                        scale,
                    ),
                    "parity_contrast_deg": parity_contrast_deg(
                        results_map,
                        curve,
                        scale,
                    ),
                }
            )

    relative_log_rows = []
    for curve in LOG_CURVES + (GOLDEN_CURVE,):
        for turns in TURNS:
            for scale, _ in SCALES:
                relative_log_rows.append(
                    {
                        "curve_id": curve.curve_id,
                        "turns": turns,
                        "scale": scale,
                        "difference_vs_reciprocal_deg": _relative_difference_deg(
                            results_map,
                            curve,
                            turns,
                            scale,
                        ),
                    }
                )

    arch_rows = []
    for turns in TURNS:
        for scale, _ in SCALES:
            arch_rows.append(
                {
                    "turns": turns,
                    "scale": scale,
                    "difference_arch_minus_reciprocal_deg": _relative_difference_deg(
                        results_map,
                        ARCHIMEDES_CURVE,
                        turns,
                        scale,
                    ),
                }
            )

    payload = {
        "checkpoint": CHECKPOINT,
        "variant": VARIANT,
        "image_pixel_data_used": False,
        "new_cells_expected": 54,
        "new_cells_executed": len(results),
        "reference_turn_recomputed": False,
        "generic_log_global_summary": generic_log_global_summary(results),
        "golden_mean_global_summary": golden_global_summary(results),
        "new_results": [asdict(r) for r in results],
        "inherited_reference_results": reference_records(),
        "parity_analysis": parity_rows,
        "relative_log_vs_reciprocal": relative_log_rows,
        "archimedes_vs_reciprocal": arch_rows,
    }

    output_path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _write_csv(results: list[NewCellResult], output_path: Path) -> None:
    rows = [asdict(r) for r in results]
    if not rows:
        raise ValueError("No new truncation-parity results to write")

    with output_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def _fmt(value: Optional[float], digits: int = 12) -> str:
    if value is None:
        return "NA"
    return f"{value:.{digits}g}"


def _write_report(results: list[NewCellResult], output_path: Path) -> None:
    results_map = _new_result_map(results)

    lines = [
        "# First Hand S1 Truncation-Parity Results",
        "",
        f"**Checkpoint:** `{CHECKPOINT}`  ",
        "**Variant:** A only  ",
        "**L = 3*pi references recomputed:** no  ",
        "**Image pixel data used:** no",
        "",
        "## Primary parity summaries",
        "",
        f"Generic logarithmic grid: `{generic_log_global_summary(results)}`",
        "",
        f"Golden Mean: `{golden_global_summary(results)}`",
        "",
        "## Logarithmic parity states",
        "",
        "| Curve | Scale | State | P contrast (deg) |",
        "|---|---|---|---:|",
    ]

    for curve in LOG_CURVES + (GOLDEN_CURVE,):
        for scale, _ in SCALES:
            lines.append(
                "| "
                + " | ".join(
                    [
                        f"`{curve.curve_id}`",
                        scale,
                        f"`{parity_state_for_curve_scale(results_map, curve, scale)}`",
                        _fmt(parity_contrast_deg(results_map, curve, scale)),
                    ]
                )
                + " |"
            )

    lines.extend(
        [
            "",
            "## Reciprocal truncation sensitivity",
            "",
            "| Turns | Scale | Delta S1 (deg) | Origin |",
            "|---:|---|---:|---|",
        ]
    )

    for turns in TURNS:
        for scale, _ in SCALES:
            if turns == 1.5:
                value = REFERENCE_RECIPROCAL_DEG[scale]
                origin = "inherited"
            else:
                value = results_map[("RECIPROCAL", turns, scale)].delta_s1_deg
                origin = "new"
            lines.append(
                f"| {turns:g} | {scale} | {_fmt(value)} | {origin} |"
            )

    lines.extend(
        [
            "",
            "## Endpoint-matched Archimedean vs reciprocal",
            "",
            "| Turns | Scale | A - R (deg) |",
            "|---:|---|---:|",
        ]
    )

    for turns in TURNS:
        for scale, _ in SCALES:
            diff = _relative_difference_deg(
                results_map,
                ARCHIMEDES_CURVE,
                turns,
                scale,
            )
            lines.append(
                f"| {turns:g} | {scale} | {_fmt(diff)} |"
            )

    lines.extend(
        [
            "",
            "## Interpretation boundary",
            "",
            "This checkpoint tests truncation-parity behaviour of the Variant-A "
            "directed endpoint-tangent S1 proxy.",
            "",
            "It does not establish intent behind the source's 1.5-turn choice, "
            "literal recursive self-embedment, or the corresponding behaviour "
            "on Variant B / the dimpled-sphere torus.",
            "",
        ]
    )

    output_path.write_text("\n".join(lines), encoding="utf-8")


def write_registered_outputs(
    results: list[NewCellResult],
    output_dir: Path,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    _write_json(results, output_dir / "s1_truncation_parity_results.json")
    _write_csv(results, output_dir / "s1_truncation_parity_new_cells.csv")
    _write_report(results, output_dir / "s1_truncation_parity_report.md")


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Preregistered First Hand S1 truncation-parity evaluator"
    )
    parser.add_argument(
        "--execute-registered-parity",
        action="store_true",
        help="explicitly execute exactly the 54 newly registered parity cells",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("results/first_hand_s1_truncation_parity_v0_8"),
        help="result directory used only with explicit registered execution",
    )
    return parser.parse_args()


def main() -> int:
    args = _parse_args()

    if not args.execute_registered_parity:
        print(
            "No new truncation-parity cell evaluated. "
            "Use --execute-registered-parity only after the "
            "implementation-only commit has been frozen."
        )
        return 0

    results = evaluate_registered_new_cells()
    write_registered_outputs(results, args.output_dir)

    print(f"Wrote registered parity outputs to: {args.output_dir}")
    print(f"New cells executed: {len(results)}")
    print(f"Generic log summary: {generic_log_global_summary(results)}")
    print(f"Golden Mean summary: {golden_global_summary(results)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
