#!/usr/bin/env python3
"""Meru 3D-V2: target-blind exact chamber-polytope covering-radius census.

Registered to Git commit db007d7429efbd41a4953b86f5eea7e026964aa8.
Independent standalone source. No archived Meru code is imported.
Requires Python 3.11 and SymPy (recorded at execution time).
All geometric feasibility, equality, deduplication and maximization are symbolic.
Floating arithmetic appears only in the supplementary angular display.
"""

from __future__ import annotations

import itertools
import json
import math
import platform
import sys
from datetime import datetime, timezone

import sympy as sp

PREREG_COMMIT = "db007d7429efbd41a4953b86f5eea7e026964aa8"
PREREG_BLOB = "3db104c82b961761dfd80b92f968f1538869bb36"
PREREG_PATH = (
    "docs/v0_9/meru_3d_v2_target_blind_spherical_"
    "covering_radius_protocol_2026_10_22.md"
)


def exact_sign(expression):
    """Return the exact sign; never silently fall back to a numeric tolerance."""
    z = sp.simplify(sp.radsimp(expression))
    if z == 0 or z.is_zero is True:
        return 0
    if z.is_positive is True:
        return 1
    if z.is_negative is True:
        return -1
    decision = sp.sign(z)
    if decision in (sp.S.NegativeOne, sp.S.Zero, sp.S.One):
        return int(decision)
    raise ArithmeticError(f"INCOMPLETE: could not decide exact sign of {z}")


def coord_json(vector):
    return [str(sp.simplify(t)) for t in vector]


def camera_strata():
    signs = (-1, 1)
    a0 = {tuple(s if j == i else 0 for j in range(3))
          for i in range(3) for s in signs}
    corners = set(itertools.product(signs, repeat=3))
    edges = {p for s, t in itertools.product(signs, repeat=2)
             for p in itertools.permutations((0, s, t))}
    ratios = {p for s, t in itertools.product(signs, repeat=2)
              for p in itertools.permutations((0, s, 2 * t))}
    return {"A0": a0, "C": corners, "E": edges, "T": ratios}


def planes_for(strata):
    # Every tuple (name, coefficients, RHS) means coeff dot (a,b,c) <= RHS.
    planes = [
        ("a>=b", (-1, 1, 0), sp.S.Zero),
        ("b>=c", (0, -1, 1), sp.S.Zero),
        ("c>=0", (0, 0, -1), sp.S.Zero),
        ("A0:a<=1", (1, 0, 0), sp.S.One),
    ]
    if "C" in strata:
        planes.append(("C:a+b+c<=sqrt(3)", (1, 1, 1), sp.sqrt(3)))
    if "E" in strata:
        planes.append(("E:a+b<=sqrt(2)", (1, 1, 0), sp.sqrt(2)))
    if "T" in strata:
        planes.append(("T:2a+b<=sqrt(5)", (2, 1, 0), sp.sqrt(5)))
    return planes


def enumerate_vertices(planes):
    vertices = []
    intersections = 0
    full_rank = 0
    feasible_intersections = 0
    for triple in itertools.combinations(planes, 3):
        intersections += 1
        matrix = sp.Matrix([row[1] for row in triple])
        if exact_sign(matrix.det()) == 0:
            continue
        full_rank += 1
        right = sp.Matrix([row[2] for row in triple])
        vector = tuple(sp.simplify(x) for x in matrix.LUsolve(right))
        admissible = all(
            exact_sign(bound - sum(coeff[i] * vector[i] for i in range(3))) >= 0
            for _, coeff, bound in planes
        )
        if not admissible:
            continue
        feasible_intersections += 1
        if not any(all(exact_sign(a - b) == 0 for a, b in zip(vector, old))
                   for old in vertices):
            vertices.append(vector)
    if not vertices:
        raise ArithmeticError("INCOMPLETE: no feasible vertices")
    vertices.sort(key=lambda v: tuple(sp.default_sort_key(x) for x in v))
    return vertices, {
        "triple_intersections": intersections,
        "full_rank_intersections": full_rank,
        "feasible_intersections_before_deduplication": feasible_intersections,
    }


def squared_norm(v):
    return sp.simplify(sum(x*x for x in v))


def evaluate(family, level, strata, all_strata):
    directions = set().union(*(all_strata[s] for s in strata))
    if not directions or any(tuple(-k for k in x) not in directions for x in directions):
        raise ArithmeticError("INCOMPLETE: signed antipodal closure failed")
    def canonical_axis(t):
        first_nonzero = next(k for k in t if k != 0)
        return t if first_nonzero > 0 else tuple(-k for k in t)

    axes = {canonical_axis(t) for t in directions}
    if len(directions) != 2 * len(axes):
        raise ArithmeticError("INCOMPLETE: axis quotient inconsistent")
    planes = planes_for(strata)
    vertices, census = enumerate_vertices(planes)
    max_squared = None
    winners = []
    descriptions = []
    for vertex in vertices:
        norm2 = squared_norm(vertex)
        active = [name for name, coeff, bound in planes
                  if exact_sign(bound - sum(coeff[i] * vertex[i] for i in range(3))) == 0]
        descriptions.append({"vertex": coord_json(vertex),
                             "norm_squared": str(norm2),
                             "active_planes": active})
        if max_squared is None or exact_sign(norm2 - max_squared) > 0:
            max_squared, winners = norm2, [vertex]
        elif exact_sign(norm2 - max_squared) == 0:
            winners.append(vertex)
    if exact_sign(max_squared) <= 0:
        raise ArithmeticError("INCOMPLETE: nonpositive maximal squared norm")
    cosine = sp.simplify(1 / sp.sqrt(max_squared))
    angle = math.degrees(math.acos(float(cosine.evalf(35))))
    return {
        "family": family, "level": level, "strata": list(strata),
        "signed_direction_count": len(directions), "unoriented_axis_count": len(axes),
        "antipodal_closure": True,
        "spherical_projective_radius_equal": True,
        "constraint_planes": [
            {"name": name, "coefficients": list(coeff), "rhs": str(rhs)}
            for name, coeff, rhs in planes],
        "intersection_census": census,
        "vertex_count": len(vertices), "vertices": descriptions,
        "max_squared_norm_exact": str(max_squared),
        "covering_cosine_exact": str(cosine),
        "covering_radius_degrees_approx": angle,
        "worst_chamber_vertices": [coord_json(v) for v in winners],
        "worst_unit_directions": [
            coord_json(tuple(sp.simplify(x / sp.sqrt(max_squared)) for x in v))
            for v in winners],
    }, max_squared


def main():
    sets = camera_strata()
    if [len(sets[k]) for k in ("A0", "C", "E", "T")] != [6, 8, 12, 24]:
        raise ArithmeticError("INCOMPLETE: wrong exact camera stratum sizes")
    rows = []
    maxima = {}
    for family, levels in (
        ("A", (("A0",), ("A0", "C"), ("A0", "C", "E"))),
        ("B", (("A0",), ("A0", "E"), ("A0", "E", "T"))),
    ):
        for index, strata in enumerate(levels):
            row, max2 = evaluate(family, f"G{index}", strata, sets)
            rows.append(row)
            maxima[(family, index)] = max2
    equal_g0 = exact_sign(maxima[("A", 0)] - maxima[("B", 0)]) == 0
    equal_b1_b2 = exact_sign(maxima[("B", 1)] - maxima[("B", 2)]) == 0
    output = {
        "study": "MERU_3D_V2", "interpretation": "Finite orthographic direction-grid geometry only",
        "preregistration_commit": PREREG_COMMIT,
        "preregistration_blob": PREREG_BLOB,
        "preregistration_path": PREREG_PATH,
        "python_version": sys.version,
        "sympy_version": sp.__version__,
        "platform": platform.platform(),
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "global_geometric_decisions": "Exact SymPy signs/equalities; undecidable raises error",
        "angle_display": "Approximate degrees only, not used for maxima or acceptance",
        "stratum_counts": {k: len(v) for k, v in sets.items()},
        "g0_identical_exact_squared_maxima": equal_g0,
        "b_g1_b_g2_equal_exact_squared_maxima": equal_b1_b2,
        "family_level_results": rows,
    }
    json.dump(output, sys.stdout, indent=2, sort_keys=True)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
