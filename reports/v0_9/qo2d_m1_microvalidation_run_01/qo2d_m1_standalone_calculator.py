#!/usr/bin/env python3
"""QO2D-M1 target-blind, independent 8-case numerical microcalculator.

Standalone Python 3.11 stdlib only. Pre-execution source candidate: review and
human authorization required before first invocation. This is NOT a general
exact-algebraic verifier, an archived P0A3D implementation, or a P1 component.

The frozen analytic expected answers are NOT used by this calculator.
"""

from __future__ import annotations

from datetime import datetime, timezone
from decimal import Decimal, localcontext
from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path
import platform
import sys

PRECISION = 80
# Any negative 2-2s is an explicit numerical diagnostic; only an extremely
# small boundary-roundoff value (under 1e-40) may be set to zero, with a record.
BOUNDARY_ROUNDOFF = Decimal("1e-40")
PREREGISTRATION_COMMIT = "6bfa644bb161d8cd6d3866118efbbabce892c3f5"
PREREGISTRATION_PATH = (
    "docs/v0_9/qo2d_m1_target_blind_microvalidation_preregistration_2026_10_22.md"
)

L = [("0", "0"), ("1", "0"), ("1", "1")]
H = [("0", "0"), ("1", "0")]
CASES = [
    ("M01", L, [("3", "-2"), ("3", "3"), ("-2", "3")]),
    ("M02", L, [("0", "0"), ("1/2", "0"), ("1", "0"),
                ("1", "0"), ("1", "1/2"), ("1", "1")]),
    ("M03", L, [("0", "0"), ("1", "0"), ("1", "-1")]),
    ("M04", L, [("1", "1"), ("1", "0"), ("0", "0")]),
    ("M05", H, [("0", "0"), ("0", "1"), ("0", "0")]),
    ("M06", H, [("0", "0"), ("1/1024", "1"), ("1/512", "0")]),
    ("M07", [("0", "0"), ("0", "0")], H),
    ("M08", H, [("0", "0"), ("1/1000000000000", "0")]),
]

ZERO = Decimal(0)
ONE = Decimal(1)
TWO = Decimal(2)
THREE = Decimal(3)
SIX = Decimal(6)


def rational_decimal(literal: str) -> Decimal:
    fraction = Fraction(literal)
    return Decimal(fraction.numerator) / Decimal(fraction.denominator)


def add(a, b):
    return a[0] + b[0], a[1] + b[1]


def sub(a, b):
    return a[0] - b[0], a[1] - b[1]


def mul(a, scalar):
    return a[0] * scalar, a[1] * scalar


def dot(a, b):
    return a[0] * b[0] + a[1] * b[1]


def jrot(a):
    return -a[1], a[0]


def rotate(a, c, s):
    return c * a[0] - s * a[1], s * a[0] + c * a[1]


def affine_product_integral(a0, a1, b0, b1, width):
    """Integral of dot products of linear paths on one aligned interval."""
    return width * (
        TWO * dot(a0, b0) + dot(a0, b1)
        + dot(a1, b0) + TWO * dot(a1, b1)
    ) / SIX


def path_data(raw):
    points = [(rational_decimal(x), rational_decimal(y)) for x, y in raw]
    if len(points) < 2:
        raise ValueError("fewer than two vertices")
    edges = []
    skipped = []
    for i in range(len(points) - 1):
        length2 = dot(sub(points[i+1], points[i]), sub(points[i+1], points[i]))
        if length2 == ZERO:
            skipped.append(i)
        else:
            edges.append((points[i], points[i+1], length2.sqrt(), i))
    if not edges:
        raise ValueError("zero total planar arclength")
    length = sum((entry[2] for entry in edges), ZERO)
    cumulative = ZERO
    segments = []
    for i, (p0, p1, edge_length, source_index) in enumerate(edges):
        start = cumulative / length
        cumulative += edge_length
        finish = ONE if i == len(edges) - 1 else cumulative / length
        segments.append((start, finish, p0, p1, source_index))

    centroid = (ZERO, ZERO)
    second_moment = ZERO
    for start, finish, p0, p1, _ in segments:
        width = finish - start
        centroid = add(centroid, mul(add(p0, p1), width / TWO))
        second_moment += width * (
            dot(p0, p0) + dot(p0, p1) + dot(p1, p1)
        ) / THREE
    variance = second_moment - dot(centroid, centroid)
    if variance <= ZERO:
        raise ArithmeticError("nonpositive RMS variance at declared precision")
    return {
        "segments": segments, "centroid": centroid,
        "rms": variance.sqrt(), "zero_edge_indices": skipped,
        "length": length,
    }


def normalized_value(path, segment, u):
    start, finish, p0, p1, _ = segment
    frac = (u - start) / (finish - start)
    raw = add(p0, mul(sub(p1, p0), frac))
    return mul(sub(raw, path["centroid"]), ONE / path["rms"])


def aligned_cells(a, b):
    knots = {ZERO, ONE}
    for path in (a, b):
        for start, finish, _, _, _ in path["segments"]:
            knots.add(start)
            knots.add(finish)
    ordered = sorted(knots)
    for lo, hi in zip(ordered, ordered[1:]):
        if hi <= lo:
            raise ArithmeticError("non-increasing aligned arclength partition")
        mid = (lo + hi) / TWO
        a_seg = next(seg for seg in a["segments"] if seg[0] <= mid <= seg[1])
        b_seg = next(seg for seg in b["segments"] if seg[0] <= mid <= seg[1])
        yield hi-lo, normalized_value(a, a_seg, lo), normalized_value(a, a_seg, hi), \
                     normalized_value(b, b_seg, lo), normalized_value(b, b_seg, hi)


def decimal_text(value):
    return format(value, "f")


def evaluate(case_id, a_raw, b_raw):
    try:
        a = path_data(a_raw)
        b = path_data(b_raw)
    except ValueError as exc:
        return {"case": case_id, "status": "NOT_EVALUABLE", "reason": str(exc),
                "score": None, "witness": None}

    cells = list(aligned_cells(a, b))
    alpha = sum((affine_product_integral(a0, a1, b0, b1, width)
                 for width, a0, a1, b0, b1 in cells), ZERO)
    beta = sum((affine_product_integral(jrot(a0), jrot(a1), b0, b1, width)
                for width, a0, a1, b0, b1 in cells), ZERO)
    strength = (alpha*alpha + beta*beta).sqrt()

    # A decimal-computed zero is a numerical observation, NOT an independent
    # proof that the exact algebraic correlation vanishes.
    decimal_zero = (alpha == ZERO and beta == ZERO)
    if decimal_zero:
        c, s = ONE, ZERO
    else:
        c, s = alpha / strength, beta / strength

    squared_from_correlation = TWO - TWO * strength
    boundary_correction = None
    square_to_sqrt = squared_from_correlation
    if square_to_sqrt < ZERO:
        if -square_to_sqrt <= BOUNDARY_ROUNDOFF:
            boundary_correction = "small_negative_roundoff_explicitly_set_to_zero"
            square_to_sqrt = ZERO
        else:
            raise ArithmeticError("materially negative QO squared radicand")
    score = square_to_sqrt.sqrt()

    direct_squared_residual = sum((
        width * (dot(e0, e0) + dot(e0, e1) + dot(e1, e1)) / THREE
        for width, a0, a1, b0, b1 in cells
        for e0, e1 in [(sub(rotate(a0, c, s), b0), sub(rotate(a1, c, s), b1))]
    ), ZERO)
    witness = [[c, -s], [s, c]]
    determinant = c*c + s*s
    return {
        "case": case_id, "status": "EVALUABLE",
        "alpha": decimal_text(alpha), "beta": decimal_text(beta),
        "strength": decimal_text(strength),
        "decimal_zero_correlation": decimal_zero,
        "witness": [[decimal_text(x) for x in row] for row in witness],
        "determinant": decimal_text(determinant),
        "squared_score_raw": decimal_text(squared_from_correlation),
        "roundoff_boundary_diagnostic": boundary_correction,
        "score": decimal_text(score),
        "direct_integrated_squared_residual": decimal_text(direct_squared_residual),
        "a_zero_edge_indices": a["zero_edge_indices"],
        "b_zero_edge_indices": b["zero_edge_indices"],
        "a_total_arclength": decimal_text(a["length"]),
        "b_total_arclength": decimal_text(b["length"]),
        "aligned_cells": len(cells),
    }


def main():
    with localcontext() as context:
        context.prec = PRECISION
        results = []
        for case_id, a_raw, b_raw in CASES:
            try:
                results.append(evaluate(case_id, a_raw, b_raw))
            except (ArithmeticError, LookupError, ValueError, ZeroDivisionError) as exc:
                results.append({"case": case_id, "status": "INCOMPLETE",
                                "reason": type(exc).__name__ + ": " + str(exc)})
        out = {
            "study": "QO2D-M1",
            "note": "Numerical evidence only; analytic oracles are external and preregistered",
            "preregistration_commit": PREREGISTRATION_COMMIT,
            "preregistration_path": PREREGISTRATION_PATH,
            "script_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
            "python_version": sys.version,
            "platform": platform.platform(),
            "precision_decimal_digits": context.prec,
            "boundary_roundoff_limit": str(BOUNDARY_ROUNDOFF),
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "cases": results,
        }
        print(json.dumps(out, indent=2, sort_keys=True))
        return 0 if all(r["status"] in {"EVALUABLE", "NOT_EVALUABLE"} for r in results) else 2


if __name__ == "__main__":
    raise SystemExit(main())
