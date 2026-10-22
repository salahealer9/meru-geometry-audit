#!/usr/bin/env python3
"""Meru v0.9 3D-V1: one-run target-blind finite viewing-direction census.

Standalone Python 3.11 / standard library only.  No Meru candidate, Hebrew
letter, projected object, or historical experiment is imported or evaluated.

Input definitions and output obligations are the human-signed 3D-V1 protocol,
commit 0e5c1ea4837cf2d2a169fb03c97179e929c3a8ed.

This code constructs all pairs and reports observed results.  It deliberately
DOES NOT embed the registered expected counts or extremal dot products; those
are compared independently after the one authorized execution.

Run exactly once after separate human authorization, redirecting JSON stdout
and stderr to immutable evidence files.  No file writes are performed here.
"""

from __future__ import annotations

import itertools
import json
import math
import platform
import sys
from datetime import datetime, timezone
from fractions import Fraction
from typing import Any

PREREGISTRATION_COMMIT = "0e5c1ea4837cf2d2a169fb03c97179e929c3a8ed"
PREREGISTRATION_BLOB = "217c2b3a3ab06846acaf767636f1efb95ef0e348"
PREREGISTRATION_PATH = (
    "docs/v0_9/meru_3d_v1_target_blind_viewing_direction_separation_protocol_2026_10_22.md"
)

# The exact symbolic input strata are predeclared, not generated from test results.
STRATUM_ORDER = {
    "A": {"G0": ("A0",), "G1": ("A0", "C"), "G2": ("A0", "C", "E")},
    "B": {"G0": ("A0",), "G1": ("A0", "E"), "G2": ("A0", "E", "T")},
}


def enumerated_strata() -> dict[str, list[tuple[int, int, int]]]:
    """Generate exact integer representative triples for A0, C, E and T."""
    a0: set[tuple[int, int, int]] = set()
    for coordinate in range(3):
        for sign in (-1, 1):
            p = [0, 0, 0]
            p[coordinate] = sign
            a0.add(tuple(p))

    corners = set(itertools.product((-1, 1), repeat=3))
    edges: set[tuple[int, int, int]] = set()
    ratios: set[tuple[int, int, int]] = set()
    for zero_at in range(3):
        nonzero_at = [k for k in range(3) if k != zero_at]
        for signs in itertools.product((-1, 1), repeat=2):
            p = [0, 0, 0]
            for i, sign in zip(nonzero_at, signs):
                p[i] = sign
            edges.add(tuple(p))
            for magnitudes in ((1, 2), (2, 1)):
                t = [0, 0, 0]
                for i, sign, magnitude in zip(nonzero_at, signs, magnitudes):
                    t[i] = sign * magnitude
                ratios.add(tuple(t))

    return {"A0": sorted(a0), "C": sorted(corners), "E": sorted(edges), "T": sorted(ratios)}


def signed_directions(
    strata: dict[str, list[tuple[int, int, int]]], names: tuple[str, ...]
) -> list[dict[str, Any]]:
    directions: list[dict[str, Any]] = []
    encountered: set[tuple[int, int, int]] = set()
    for stratum in names:
        for triple in strata[stratum]:
            if triple in encountered:
                raise ValueError("Duplicate signed direction across strata")
            encountered.add(triple)
            norm_sq = sum(t * t for t in triple)
            if norm_sq <= 0:
                raise ValueError("Zero direction")
            # Each registered representative is a primitive integer triple.
            if math.gcd(*triple) != 1:
                raise ValueError("Nonprimitive integer direction")
            directions.append(
                {"triple": list(triple), "norm_sq": norm_sq, "stratum": stratum}
            )
    if any(tuple(-t for t in triple) not in encountered for triple in encountered):
        raise ValueError("Signed-direction set is not antipodally closed")
    return directions


def is_positive_axis_representative(triple: list[int]) -> bool:
    return next(t for t in triple if t != 0) > 0


def exact_cosine_data(dot: int, normproduct: int) -> dict[str, Any]:
    """Canonical exact cosine as sign times sqrt(nonnegative reduced rational)."""
    if normproduct <= 0:
        raise ValueError("Nonpositive norm product")
    squared = Fraction(dot * dot, normproduct)
    sign = (dot > 0) - (dot < 0)
    if sign == 0:
        display = "0"
    elif squared == 1:
        display = "1" if sign > 0 else "-1"
    else:
        display = ("" if sign > 0 else "-") + (
            f"sqrt({squared.numerator}/{squared.denominator})"
        )
    return {
        "sign": sign,
        "squared_numerator": squared.numerator,
        "squared_denominator": squared.denominator,
        "display": display,
    }


def compare_cosines(d1: int, q1: int, d2: int, q2: int) -> int:
    """Compare d1/sqrt(q1) to d2/sqrt(q2), by integer arithmetic ONLY."""
    if q1 <= 0 or q2 <= 0:
        raise ValueError("Nonpositive norm product")
    s1, s2 = (d1 > 0) - (d1 < 0), (d2 > 0) - (d2 < 0)
    if s1 != s2:
        return (s1 > s2) - (s1 < s2)
    if s1 == 0:
        return 0
    lhs = d1 * d1 * q2
    rhs = d2 * d2 * q1
    return s1 * ((lhs > rhs) - (lhs < rhs))


def pair_census(directions: list[dict[str, Any]], *, unoriented: bool) -> dict[str, Any]:
    """Complete i<j census; maximize normalized cosine without floats.

    For the axis quotient, the entries must already be one representative per
    antipodal class.  Absolute dots compare axes with no same-axis pairs.
    """
    rows: list[list[int]] = []
    summary: dict[str, dict[str, Any]] = {}
    best: tuple[int, int] | None = None
    winning_pairs: list[list[int]] = []

    for i, j in itertools.combinations(range(len(directions)), 2):
        a, b = directions[i], directions[j]
        dot = sum(x * y for x, y in zip(a["triple"], b["triple"]))
        denominator = a["norm_sq"] * b["norm_sq"]
        numerator_for_order = abs(dot) if unoriented else dot
        rows.append([i, j, dot, denominator])  # entire exact unordered-pair table

        stratum_key = " x ".join(sorted((a["stratum"], b["stratum"])))
        if stratum_key not in summary:
            summary[stratum_key] = {"pair_count": 0, "best": None, "witness_pairs": []}
        entry = summary[stratum_key]
        entry["pair_count"] += 1
        local_best = entry["best"]
        if local_best is None or compare_cosines(
            numerator_for_order, denominator, *local_best
        ) > 0:
            entry["best"] = (numerator_for_order, denominator)
            entry["witness_pairs"] = [[i, j]]
        elif compare_cosines(numerator_for_order, denominator, *local_best) == 0:
            entry["witness_pairs"].append([i, j])

        if best is None or compare_cosines(numerator_for_order, denominator, *best) > 0:
            best = (numerator_for_order, denominator)
            winning_pairs = [[i, j]]
        elif compare_cosines(numerator_for_order, denominator, *best) == 0:
            winning_pairs.append([i, j])

    if best is None:
        raise ValueError("Need at least two distinct directions or axes")
    best_num, best_den = best
    best_cos = exact_cosine_data(best_num, best_den)

    groups: dict[str, Any] = {}
    for name, entry in sorted(summary.items()):
        local_num, local_den = entry["best"]
        groups[name] = {
            "pair_count": entry["pair_count"],
            "maximum_cosine": exact_cosine_data(local_num, local_den),
            "number_of_maximizing_pairs": len(entry["witness_pairs"]),
            "maximizing_pair_indices": entry["witness_pairs"],
        }

    numerical_cos = best_cos["sign"] * math.sqrt(
        best_cos["squared_numerator"] / best_cos["squared_denominator"]
    )
    # acos is used *only after* the exact maximum has been selected.
    degrees = math.degrees(math.acos(max(-1.0, min(1.0, numerical_cos))))

    return {
        "pair_count": len(rows),
        "complete_pair_table_columns": [
            "direction_index_i", "direction_index_j", "integer_dot", "norm_sq_product"
        ],
        "complete_pair_table": rows,
        "maximum_cosine": best_cos,
        "minimum_separation_degrees_approx": degrees,
        "number_of_maximizing_pairs": len(winning_pairs),
        "maximizing_pair_indices": winning_pairs,
        "maximizing_pair_triples": [
            [directions[i]["triple"], directions[j]["triple"]]
            for i, j in winning_pairs
        ],
        "stratum_pair_summary": groups,
    }


def main() -> None:
    strata = enumerated_strata()
    results: list[dict[str, Any]] = []
    for family in ("A", "B"):
        for level in ("G0", "G1", "G2"):
            members = signed_directions(strata, STRATUM_ORDER[family][level])
            axes = [
                member for member in members
                if is_positive_axis_representative(member["triple"])
            ]
            if len(axes) * 2 != len(members):
                raise ValueError("Incorrect antipodal-axis count")

            signed = pair_census(members, unoriented=False)
            axis = pair_census(axes, unoriented=True)
            smax = signed["maximum_cosine"]
            amax = axis["maximum_cosine"]
            same_maximum = smax == amax
            results.append(
                {
                    "family": family,
                    "level": level,
                    "strata": list(STRATUM_ORDER[family][level]),
                    "signed_direction_count": len(members),
                    "axis_count": len(axes),
                    "signed_directions": members,
                    "axis_representatives": axes,
                    "signed_pair_census": signed,
                    "axis_pair_census": axis,
                    "signed_and_axis_maxima_equal_exactly": same_maximum,
                }
            )

    output = {
        "study": "MERU_3D_V1",
        "record_kind": "RAW_REGISTERED_MEASUREMENT_AWAITING_INDEPENDENT_REVIEW",
        "preregistration_commit": PREREGISTRATION_COMMIT,
        "preregistration_blob": PREREGISTRATION_BLOB,
        "preregistration_path": PREREGISTRATION_PATH,
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "python_version": sys.version,
        "platform": platform.platform(),
        "method": "complete exact integer pair tables; no floating point in maximizing dot products",
        "angle_note": "approximate degrees are presentation only; exact cosine controls pass/fail",
        "family_level_results": results,
    }
    sys.stdout.write(json.dumps(output, indent=2, sort_keys=True, ensure_ascii=True) + "\n")


if __name__ == "__main__":
    main()
