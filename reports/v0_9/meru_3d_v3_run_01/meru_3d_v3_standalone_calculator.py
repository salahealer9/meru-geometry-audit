#!/usr/bin/env python3
"""Meru v0.9 3D-V3: exact labelled orthographic projection equivalence.

Standalone Python 3.11 standard-library calculator. Frozen scientific protocol:
  67ccaa1f5292acee31e26e318e7bff3bc2e7f5ec
All comparisons use Fraction / integer arithmetic; no floats or image data.
This script is a pre-run candidate until the human approves its SHA-256.
"""
from __future__ import annotations

from fractions import Fraction as Q
from itertools import combinations, product
import json
import platform
import sys
from datetime import datetime, timezone

PREREG_COMMIT = "67ccaa1f5292acee31e26e318e7bff3bc2e7f5ec"
PREREG_BLOB = "f835cde4ec7890a66ef2a82f3f5699361752371e"
PREREG_PATH = (
    "docs/v0_9/meru_3d_v3_target_blind_labelled_projection_equivalence_protocol_2026_10_22.md"
)
PASS = "MERU_3D_V3_LABELLED_PROJECTION_EQUIVALENCE_PASS"
FAIL = "MERU_3D_V3_INCOMPLETE_OR_FAILED"

# Each tuple is (SO2 count, O2 count). F, L, P in that order.
ORACLES = {
    ("A", "G0"): ((6, 3), (1, 1), (4, 3), (4, 2)),
    ("A", "G1"): ((14, 7), (2, 2), (8, 5), (4, 10)),
    ("A", "G2"): ((26, 13), (3, 3), (14, 9), (8, 18)),
    ("B", "G0"): ((6, 3), (1, 1), (4, 3), (4, 2)),
    ("B", "G1"): ((18, 9), (2, 2), (10, 7), (8, 10)),
    ("B", "G2"): ((42, 21), (4, 4), (22, 15), (16, 26)),
}

CONTROLS = {
    "F": ((0, 0, 0), (1, 0, 0), (0, 2, 0), (0, 0, 3)),
    "L": ((0, 0, 0), (1, 0, 0), (3, 0, 0)),
    "P": ((0, 0, 0), (1, 0, 0), (0, 2, 0)),
}


def norm_squared(v):
    return sum(x * x for x in v)


def dot(u, v):
    return sum(a * b for a, b in zip(u, v))


def cross(u, v):
    return (u[1] * v[2] - u[2] * v[1],
            u[2] * v[0] - u[0] * v[2],
            u[0] * v[1] - u[1] * v[0])


def make_strata():
    a0 = set()
    for j in range(3):
        for s in (-1, 1):
            x = [0, 0, 0]
            x[j] = s
            a0.add(tuple(x))
    corners = set(product((-1, 1), repeat=3))
    edges, ratio_two = set(), set()
    for zero in range(3):
        other = [j for j in range(3) if j != zero]
        for signs in product((-1, 1), repeat=2):
            x = [0, 0, 0]
            for j, s in zip(other, signs):
                x[j] = s
            edges.add(tuple(x))
            for magnitudes in ((1, 2), (2, 1)):
                x = [0, 0, 0]
                for j, s, magnitude in zip(other, signs, magnitudes):
                    x[j] = s * magnitude
                ratio_two.add(tuple(x))
    strata = {"A0": sorted(a0), "C": sorted(corners),
              "E": sorted(edges), "T": sorted(ratio_two)}
    assert {k: len(v) for k, v in strata.items()} == {
        "A0": 6, "C": 8, "E": 12, "T": 24}
    assert len(set.union(*(set(v) for v in strata.values()))) == 50
    assert all(norm_squared(v) == {"A0": 1, "C": 3, "E": 2, "T": 5}[k]
               for k, triples in strata.items() for v in triples)
    return strata


def ordered_cameras(strata, family, level):
    orders = {"A": ("A0", "C", "E"), "B": ("A0", "E", "T")}
    selected = orders[family][:int(level[1]) + 1]
    return [(tuple(t), k) for k in selected for t in strata[k]]


def first_nonzero_positive(t):
    return next(x for x in t if x != 0) > 0


def centred_points(points):
    k = len(points)
    mean = tuple(sum(Q(p[j]) for p in points) / k for j in range(3))
    return [tuple(Q(p[j]) - mean[j] for j in range(3)) for p in points]


def invariants(triple, points):
    # n=triple/sqrt(q), Gram_ij = Yi.Yj-(t.Yi)(t.Yj)/q.
    q = norm_squared(triple)
    ys = centred_points(points)
    tdot = [dot(triple, y) for y in ys]
    gram = tuple(tuple(dot(u, v) - du * dv / q
                       for v, dv in zip(ys, tdot))
                 for u, du in zip(ys, tdot))
    # Minor_ij = numerator_ij/sqrt(q); the numerator is rational.
    minors = tuple(dot(triple, cross(ys[i], ys[j]))
                   for i, j in combinations(range(len(ys)), 2))
    return gram, (q, minors)


def area_equal(a, b):
    """Exact equality of rational numerator / sqrt(integer norm squared)."""
    qa, ma = a
    qb, mb = b
    for x, y in zip(ma, mb):
        if x == 0 or y == 0:
            if x != y:
                return False
        elif (x > 0) != (y > 0) or x * x * qb != y * y * qa:
            return False
    return True


def planar_rank(gram):
    k = len(gram)
    assert all(gram[i][j] == gram[j][i]
               for i in range(k) for j in range(k))
    assert all(gram[i][i] >= 0 for i in range(k))
    if all(gram[i][i] == 0 for i in range(k)):
        assert all(x == 0 for row in gram for x in row)
        return 0
    for i, j in combinations(range(k), 2):
        det = gram[i][i] * gram[j][j] - gram[i][j] ** 2
        assert det >= 0  # Exact Gram of real projected points
        if det > 0:
            return 2
    return 1


def frac_text(x):
    return str(x)


def serialized_signature(gram, area):
    q, minors = area
    return {
        "gram": [[frac_text(x) for x in row] for row in gram],
        "oriented_minors_numerators": [frac_text(x) for x in minors],
        "oriented_minors_shared_sqrt_denominator_squared": q,
    }


def equivalence_matrices(signatures, evaluable):
    count = len(signatures)
    o2 = [[None] * count for _ in range(count)]
    so2 = [[None] * count for _ in range(count)]
    for i in range(count):
        for j in range(count):
            if not evaluable[i] or not evaluable[j]:
                continue
            gi, ai = signatures[i]
            gj, aj = signatures[j]
            o2[i][j] = (gi == gj)
            so2[i][j] = bool(o2[i][j] and area_equal(ai, aj))
    return so2, o2


def partitions(matrix, eligible):
    """Create exact first-encounter class partitions and check full equivalence."""
    n = len(matrix)
    for i in range(n):
        assert (matrix[i][i] is True) if eligible[i] else (matrix[i][i] is None)
        for j in range(n):
            assert matrix[i][j] == matrix[j][i]
            if not (eligible[i] and eligible[j]):
                assert matrix[i][j] is None
    classes = []
    claimed = set()
    for i in range(n):
        if not eligible[i] or i in claimed:
            continue
        members = [j for j in range(n) if matrix[i][j] is True]
        assert i in members
        assert all(j not in claimed for j in members)
        # All same-class indices have identical relation rows (transitivity).
        assert all(matrix[j] == matrix[i] for j in members)
        classes.append(members)
        claimed.update(members)
    assert claimed == {i for i in range(n) if eligible[i]}
    return classes


def audit_control(label, cameras, expected_class_counts):
    triples = [t for t, _ in cameras]
    sigs = [invariants(t, CONTROLS[label]) for t in triples]
    ranks = [planar_rank(g) for g, _ in sigs]
    ok = [not (label == "L" and rank == 0) for rank in ranks]
    # All other controls remain evaluable even when rank 1.
    so2, o2 = equivalence_matrices(sigs, ok)
    groups_so2 = partitions(so2, ok)
    groups_o2 = partitions(o2, ok)
    n = len(triples)
    for i in range(n):
        for j in range(n):
            if ok[i] and ok[j]:
                assert (so2[i][j] is not True) or (o2[i][j] is True)
                if tuple(-a for a in triples[i]) == triples[j]:
                    assert o2[i][j] is True
    if label == "F":
        assert all(rank == 2 for rank in ranks)
    if label == "L":
        assert [triples[i] for i, x in enumerate(ok) if not x] == [
            (-1, 0, 0), (1, 0, 0)]
        assert all(ranks[i] == 1 for i, is_ok in enumerate(ok) if is_ok)
    if label == "P":
        assert all(ok)
        assert all(ranks[i] == (2 if triples[i][2] != 0 else 1)
                   for i in range(n))
    if label == "L":
        assert so2 == o2
    # The full pair matrices include null rows/columns for L's rank-zero exclusions.
    assert len(groups_so2) == expected_class_counts[0] and len(groups_o2) == expected_class_counts[1]
    return {
        "control": label,
        "camera_count": n,
        "evaluable_count": sum(ok),
        "not_evaluable_count": sum(not x for x in ok),
        "not_evaluable_camera_indices": [i for i, x in enumerate(ok) if not x],
        "not_evaluable_camera_triples": [list(triples[i]) for i, x in enumerate(ok) if not x],
        "rank_counts": {str(k): ranks.count(k) for k in (0, 1, 2)},
        "per_camera": [
            {"index": i, "triple": list(t), "stratum": cameras[i][1],
             "norm_squared": norm_squared(t), "rank": ranks[i],
             "status": "EVALUABLE" if ok[i] else "NOT_EVALUABLE",
             "exact_invariants": serialized_signature(*sigs[i])}
            for i, t in enumerate(triples)
        ],
        "SO2": {"class_count": len(groups_so2),
                "class_size_multiset": sorted(map(len, groups_so2)),
                "classes_camera_indices": groups_so2,
                "classes_camera_triples": [[list(triples[i]) for i in g]
                                           for g in groups_so2],
                "pairwise_equivalence_matrix": so2},
        "O2": {"class_count": len(groups_o2),
               "class_size_multiset": sorted(map(len, groups_o2)),
               "classes_camera_indices": groups_o2,
               "classes_camera_triples": [[list(triples[i]) for i in g]
                                          for g in groups_o2],
               "pairwise_equivalence_matrix": o2},
    }


def main():
    strata = make_strata()
    rows = []
    for family in ("A", "B"):
        for level in ("G0", "G1", "G2"):
            cameras = ordered_cameras(strata, family, level)
            triples = [t for t, _ in cameras]
            assert len(triples) == len(set(triples))
            assert set(triples) == {tuple(-x for x in t) for t in triples}
            axes = [t for t in triples if first_nonzero_positive(t)]
            oracle = ORACLES[(family, level)]
            assert (len(triples), len(axes)) == (
                {"A": (6, 14, 26), "B": (6, 18, 42)}[family][int(level[1])],
                {"A": (3, 7, 13), "B": (3, 9, 21)}[family][int(level[1])]
            )
            control_results = {
                label: audit_control(label, cameras, oracle[i])
                for i, label in enumerate(("F", "L", "P"))
            }
            p = control_results["P"]
            assert (p["rank_counts"]["1"], p["rank_counts"]["2"]) == oracle[3]
            rows.append({
                "family": family, "level": level,
                "signed_camera_count": len(triples),
                "axis_count": len(axes),
                "signed_camera_triples": [list(t) for t in triples],
                "axis_representatives": [list(t) for t in axes],
                "control_results": control_results,
                "oracle_verified": True,
            })
    assert rows[0]["signed_camera_triples"] == rows[3]["signed_camera_triples"]
    assert rows[0]["control_results"] == rows[3]["control_results"]
    result = {
        "study": "MERU_3D_V3", "outcome": PASS,
        "preregistration_commit": PREREG_COMMIT,
        "preregistration_blob": PREREG_BLOB,
        "preregistration_path": PREREG_PATH,
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "python_version": sys.version,
        "platform": platform.platform(),
        "arithmetic": "Fraction exact rational Gram and sign-aware rational-square radical equality",
        "frame_policy": "Frame-free invariants; no numeric camera frame or planar fit",
        "unscored_policy": "Control L rank-zero cameras NOT_EVALUABLE; other ranks reported",
        "stratum_counts": {k: len(v) for k, v in strata.items()},
        "family_level_results": rows,
        "g0_identical_camera_order_and_results": True,
        "scope": "Target-blind labelled point controls only; not silhouettes or Hebrew shapes",
    }
    json.dump(result, sys.stdout, indent=2, sort_keys=True)
    sys.stdout.write("\n")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"{FAIL}: {type(exc).__name__}: {exc}", file=sys.stderr)
        raise
