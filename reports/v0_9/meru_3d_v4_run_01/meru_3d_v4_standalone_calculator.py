#!/usr/bin/env python3
"""Meru 3D-V4: one-shot, exact, target-blind trace/silhouette census.

Scientific protocol: Git commit d7b5359f857b5a294746dc6bce5a61e50d169022,
Git blob 2d57b85c066c76ae462929ece209385f5491ed78.

This script has no file-writing side effects. Its single invocation emits complete
JSON to stdout. Pre-execution source review must not execute this module.
"""
from __future__ import annotations

import itertools
import json
import platform
import sys
from datetime import datetime, timezone
from fractions import Fraction as Q

STUDY = "MERU_3D_V4"
COMMIT = "d7b5359f857b5a294746dc6bce5a61e50d169022"
BLOB = "2d57b85c066c76ae462929ece209385f5491ed78"
PROTOCOL = "docs/v0_9/meru_3d_v4_target_blind_trace_and_convex_silhouette_equivalence_protocol_2026_10_22.md"


def require(condition, message):
    if not condition:
        raise RuntimeError("INCOMPLETE_OR_FAILED: " + message)


def add(a, b):
    return tuple(x + y for x, y in zip(a, b))


def sub(a, b):
    return tuple(x - y for x, y in zip(a, b))


def dot(a, b):
    return sum((x * y for x, y in zip(a, b)), Q(0))


def cross(a, b):
    return (a[1]*b[2] - a[2]*b[1],
            a[2]*b[0] - a[0]*b[2],
            a[0]*b[1] - a[1]*b[0])


def centroid(points):
    k = len(points)
    return tuple(sum((p[j] for p in points), Q(0)) / k for j in range(3))


def fracstr(v):
    return str(v)


def vecstr(p):
    return [fracstr(v) for v in p]


def a0():
    return sorted([tuple(s if i == j else 0 for i in range(3))
                   for j in range(3) for s in (-1, 1)])


def corners():
    return sorted(itertools.product((-1, 1), repeat=3))


def edges():
    out = []
    for z in range(3):
        for signs in itertools.product((-1, 1), repeat=2):
            itr = iter(signs)
            out.append(tuple(0 if i == z else next(itr) for i in range(3)))
    return sorted(out)


def ratio_two():
    out = []
    for z in range(3):
        for magnitudes in ((1, 2), (2, 1)):
            for signs in itertools.product((-1, 1), repeat=2):
                itr = iter([magnitudes[i] * signs[i] for i in range(2)])
                out.append(tuple(0 if i == z else next(itr) for i in range(3)))
    return sorted(out)


STRATA = {"A0": a0(), "C": corners(), "E": edges(), "T": ratio_two()}
FAMILIES = {"A": (("A0",), ("A0", "C"), ("A0", "C", "E")),
            "B": (("A0",), ("A0", "E"), ("A0", "E", "T"))}

# No source vertex labels are retained as observable correspondences.
CONTROLS = {
    "TR-L": ("TR", [(0,0,0), (1,0,0), (3,0,0)], False),
    "TR-S": ("TR", [(0,0,0), (1,2,3), (3,5,4), (5,6,8), (8,9,10)], False),
    "TR-C": ("TR", [(0,0,0), (3,0,0), (4,2,1), (1,4,3), (-1,2,1), (0,0,0)], True),
    "CS-T": ("CS", [(0,0,0), (1,0,0), (0,2,0), (0,0,3)], False),
    "CS-B": ("CS", list(itertools.product((0,1), (0,2), (0,3))), False),
}
CONTROLS = {k: (kind, [tuple(Q(x) for x in v) for v in coords], closed)
            for k, (kind, coords, closed) in CONTROLS.items()}


class Camera:
    def __init__(self, triple, stratum):
        self.t = tuple(Q(x) for x in triple)
        self.triple = tuple(int(x) for x in triple)
        self.s = int(dot(self.t, self.t))
        self.stratum = stratum
        require(self.s in (1, 2, 3, 5), "invalid direction norm")

    def B(self, a, b):
        """Exact rational projected inner product; normalized t only implicitly."""
        return dot(a, b) - dot(self.t, a)*dot(self.t, b)/self.s

    def dnum(self, a, b):
        """Oriented area = dnum(a,b)/sqrt(s), exactly."""
        return dot(self.t, cross(a, b))

    def orient(self, p, q, r):
        """Sign of projected oriented triangle without evaluating a radical."""
        return self.dnum(sub(q, p), sub(r, p))

    def same_projection(self, p, q):
        return self.B(sub(p, q), sub(p, q)) == 0


def camera_grid(family, level):
    return [Camera(t, name) for name in FAMILIES[family][level]
            for t in STRATA[name]]


def projected_rank(camera, points):
    differences = [sub(p, points[0]) for p in points[1:]]
    if all(camera.B(v, v) == 0 for v in differences):
        return 0
    if any(camera.dnum(u, v) != 0 for u, v in itertools.combinations(differences, 2)):
        return 2
    return 1


def trace_reduce(cam, source, closed):
    """Remove projected zero edges, then only *forward* collinear stops."""
    points = list(source[:-1] if closed else source)
    if closed:
        require(source[0] == source[-1], "closed input endpoint mismatch")
        # First remove cyclic consecutive coincidences, never remove retracing.
        while len(points) > 1:
            removed = False
            for i in range(len(points)):
                if cam.same_projection(points[i], points[(i+1) % len(points)]):
                    del points[(i+1) % len(points)]
                    removed = True
                    break
            if not removed:
                break
    else:
        reduced = [points[0]]
        for p in points[1:]:
            if not cam.same_projection(reduced[-1], p):
                reduced.append(p)
        points = reduced

    if projected_rank(cam, source) == 0:
        return [], 0, "NOT_EVALUABLE"

    require(len(points) >= 2, "noncollapsed trace has fewer than two stops")
    while True:
        removed = False
        indices = (range(len(points)) if closed else range(1, len(points)-1))
        for i in indices:
            previous = points[(i-1) % len(points)]
            current = points[i]
            following = points[(i+1) % len(points)]
            u, v = sub(current, previous), sub(following, current)
            if cam.dnum(u, v) == 0 and cam.B(u, v) > 0:
                del points[i]
                removed = True
                break
        if not removed or len(points) <= 2:
            break

    for i in range(len(points)-1):
        require(not cam.same_projection(points[i], points[i+1]), "zero segment retained")
    if closed:
        require(not cam.same_projection(points[-1], points[0]), "cyclic zero edge retained")
    rank = projected_rank(cam, points)
    require(rank > 0, "simplification unexpectedly collapsed trace")
    return points, rank, "EVALUABLE"


def silhouette_hull(cam, points):
    """Exact gift wrapping from a certified extreme seed; output strict CCW corners."""
    unique, original_ids = [], []
    for i, p in enumerate(points):
        if not any(cam.same_projection(p, q) for q in unique):
            unique.append(p)
            original_ids.append(i)
    require(len(unique) >= 3 and projected_rank(cam, unique) == 2,
            "convex solid silhouette has nonpositive dimension")

    # Maximal squared distance from projected centroid is attained at an
    # extreme point (strict convexity); stable tie chooses the first.
    c = centroid(unique)
    seed = max(range(len(unique)), key=lambda i: (cam.B(sub(unique[i], c),
                                                    sub(unique[i], c)), -i))
    hull_indices = []
    current = seed
    while True:
        require(current not in hull_indices, "hull cycles without closing")
        hull_indices.append(current)
        other = next((j for j in range(len(unique)) if j != current), None)
        require(other is not None, "no candidate hull edge")
        for j in range(len(unique)):
            if j == current or j == other:
                continue
            orient = cam.orient(unique[current], unique[other], unique[j])
            if orient < 0 or (orient == 0 and
                cam.B(sub(unique[j], unique[current]), sub(unique[j], unique[current])) >
                cam.B(sub(unique[other], unique[current]), sub(unique[other], unique[current]))):
                other = j
        current = other
        if current == seed:
            break
        require(len(hull_indices) <= len(unique), "hull exceeded input points")

    hull = [unique[i] for i in hull_indices]
    require(len(hull) >= 3, "hull has fewer than three corners")
    sum_area_num = sum((cam.dnum(hull[i], hull[(i+1) % len(hull)])
                        for i in range(len(hull))), Q(0))
    require(sum_area_num > 0, "hull does not have positive CCW oriented area")
    # Full inclusion and strictness certificate for every supporting hull edge.
    for i in range(len(hull)):
        a, b, third = hull[i], hull[(i+1) % len(hull)], hull[(i+2) % len(hull)]
        require(cam.orient(a, b, third) > 0, "hull has a non-strict corner")
        require(all(cam.orient(a, b, p) >= 0 for p in unique),
                "hull omitted a point beyond a supporting edge")
    require(projected_rank(cam, hull) == 2, "hull is not two-dimensional")
    return hull, original_ids, hull_indices, unique, sum_area_num


def invariant_signature(cam, points):
    """Complete centred labelled Gram and oriented-minor matrices."""
    c = centroid(points)
    y = [sub(p, c) for p in points]
    gram = tuple(tuple(cam.B(u, v) for v in y) for u in y)
    areas = tuple(tuple(cam.dnum(u, v) for v in y) for u in y)
    return gram, areas


def radical_equal(a, s_a, b, s_b):
    """Decidable equality of a/sqrt(s_a), b/sqrt(s_b), no floats."""
    require(s_a > 0 and s_b > 0, "invalid positive radical denominator")
    return (a == b == 0 or
            ((a > 0) == (b > 0) and (a < 0) == (b < 0) and
             a*a*s_b == b*b*s_a))


def same_signature(cam_a, gram_a, area_a, cam_b, gram_b, area_b, order,
                   group):
    k = len(order)
    if len(gram_a) != k or len(gram_b) != k:
        return False
    for i in range(k):
        for j in range(k):
            if gram_a[i][j] != gram_b[order[i]][order[j]]:
                return False
            if group == "SO2" and not radical_equal(area_a[i][j], cam_a.s,
                                                area_b[order[i]][order[j]], cam_b.s):
                return False
    return True


def allowed_correspondences(size, closed, group):
    if not closed:
        yield tuple(range(size))
        yield tuple(reversed(range(size)))
    else:
        # TR closed: both reversal and cyclic origin. CS: CCW cycle requires
        # cyclic order under SO2, reversal only under O2.
        for direction in (1, -1):
            if direction == -1 and group == "SO2" and closed == "CS":
                continue
            for shift in range(size):
                yield tuple((shift + direction * j) % size for j in range(size))


def equivalent(cam_a, obs_a, cam_b, obs_b, group):
    if obs_a["status"] != "EVALUABLE" or obs_b["status"] != "EVALUABLE":
        return None
    pa, pb = obs_a["points"], obs_b["points"]
    if len(pa) != len(pb):
        return False
    if obs_a["rank"] != obs_b["rank"]:
        return False
    is_closed = ("CS" if obs_a["kind"] == "CS" else obs_a["closed"])
    for order in allowed_correspondences(len(pa), is_closed, group):
        if same_signature(cam_a, obs_a["gram"], obs_a["area"],
                          cam_b, obs_b["gram"], obs_b["area"], order, group):
            return True
    return False


def class_partition(matrix, evaluable):
    classes, visited = [], set()
    for i in range(len(matrix)):
        if not evaluable[i] or i in visited:
            continue
        group = [j for j in range(len(matrix)) if matrix[i][j] is True]
        require(i in group and not any(j in visited for j in group),
                "nonpartitioned equivalence row")
        require(all(matrix[j][k] is (k in group) for j in group
                    for k in range(len(matrix)) if evaluable[k]),
                "relation is not transitive or has inconsistent rows")
        visited.update(group)
        classes.append(group)
    require(visited == {i for i, ok in enumerate(evaluable) if ok},
            "classes failed to cover evaluable cameras")
    return classes


def record_observation(cam, control_id):
    kind, source, closed = CONTROLS[control_id]
    if kind == "TR":
        points, rank, status = trace_reduce(cam, source, closed)
        diagnostic = {"source_point_count": len(source),
                      "reduced_corner_count": len(points),
                      "reduced_vertices_3d_preimage": [vecstr(p) for p in points],
                      "closed": closed}
    else:
        points, original_ids, hull_ids, unique, area_num = silhouette_hull(cam, source)
        rank, status = 2, "EVALUABLE"
        diagnostic = {"input_point_count": len(source),
                      "projected_distinct_count": len(unique),
                      "strict_hull_corner_count": len(points),
                      "representative_input_ids": original_ids,
                      "hull_indices_into_projected_distinct": hull_ids,
                      "strict_ccw_hull_vertices_3d_preimage": [vecstr(p) for p in points],
                      "signed_double_area_numerator": str(area_num),
                      "signed_double_area_denominator_sqrt_squared": cam.s}
    gram, area = invariant_signature(cam, points) if status == "EVALUABLE" else ((), ())
    return {"kind": kind, "closed": closed, "points": points,
            "gram": gram, "area": area, "rank": rank, "status": status,
            "diagnostic": diagnostic}


def public_observation(cam, obs, index):
    out = {"index": index, "camera_triple": list(cam.triple),
           "camera_stratum": cam.stratum, "camera_norm_squared": cam.s,
           "status": obs["status"], "rank": obs["rank"], **obs["diagnostic"]}
    if obs["status"] == "EVALUABLE":
        out["exact_signature"] = {
            "centred_gram": [[fracstr(v) for v in row] for row in obs["gram"]],
            "oriented_minor_numerators": [[fracstr(v) for v in row] for row in obs["area"]],
            "oriented_minor_denominator_sqrt_squared": cam.s}
    return out


def control_result(cameras, control_id):
    observations = [record_observation(cam, control_id) for cam in cameras]
    evaluable = [o["status"] == "EVALUABLE" for o in observations]
    n = len(cameras)
    matrices, partitions = {}, {}
    for mode in ("SO2", "O2"):
        matrix = [[equivalent(cameras[i], observations[i], cameras[j], observations[j], mode)
                   for j in range(n)] for i in range(n)]
        for i in range(n):
            for j in range(n):
                require(matrix[i][j] == matrix[j][i], "equivalence asymmetry")
                require(matrix[i][j] is None if not (evaluable[i] and evaluable[j])
                        else isinstance(matrix[i][j], bool), "incorrect undefined pairs")
            if evaluable[i]:
                require(matrix[i][i] is True, "equivalence nonreflexive")
        classes = class_partition(matrix, evaluable)
        matrices[mode] = matrix
        partitions[mode] = classes
    for i in range(n):
        for j in range(n):
            if matrices["SO2"][i][j] is True:
                require(matrices["O2"][i][j] is True, "SO2 is not contained in O2")
            if cameras[i].triple == tuple(-v for v in cameras[j].triple):
                if evaluable[i] and evaluable[j]:
                    require(matrices["O2"][i][j] is True, "antipodal O2 violation")

    rank_counts = {str(rank): sum(o["rank"] == rank for o in observations)
                   for rank in (0, 1, 2)}
    result = {
        "observable": control_id,
        "camera_count": n,
        "evaluable_count": sum(evaluable),
        "not_evaluable_count": n - sum(evaluable),
        "not_evaluable_indices": [i for i, yes in enumerate(evaluable) if not yes],
        "not_evaluable_triples": [list(cameras[i].triple) for i, yes in enumerate(evaluable) if not yes],
        "rank_counts": rank_counts,
        "per_camera": [public_observation(c, o, i) for i, (c, o) in enumerate(zip(cameras, observations))],
    }
    for mode in ("SO2", "O2"):
        cs = partitions[mode]
        result[mode] = {
            "class_count": len(cs),
            "class_size_multiset": sorted(map(len, cs)),
            "classes_camera_indices": cs,
            "classes_camera_triples": [[list(cameras[i].triple) for i in cluster] for cluster in cs],
            "pairwise_equivalence_matrix": matrices[mode],
        }
        require(sum(map(len, cs)) == sum(evaluable), "class accounting failure")
    return result


def verify_global(results):
    expected_counts = {("A", "G0"): (6, 3), ("A", "G1"): (14, 7),
                       ("A", "G2"): (26, 13), ("B", "G0"): (6, 3),
                       ("B", "G1"): (18, 9), ("B", "G2"): (42, 21)}
    line_counts = {("A", "G0"): 1, ("A", "G1"): 2, ("A", "G2"): 3,
                   ("B", "G0"): 1, ("B", "G1"): 2, ("B", "G2"): 4}
    lookup = {(r["family"], r["level"]): r for r in results}
    require(len(lookup) == 6, "not six distinct family/tier records")
    for (family, level), row in lookup.items():
        n, axes = expected_counts[family, level]
        require((row["signed_camera_count"], row["axis_count"]) == (n, axes),
                "incorrect camera or axis count")
        cameras = [tuple(t) for t in row["signed_camera_triples"]]
        require(len(set(cameras)) == n and {tuple(-v for v in t) for t in cameras} == set(cameras),
                "duplicate or unmatched antipodal camera")
        line = row["control_results"]["TR-L"]
        require(line["not_evaluable_count"] == 2 and
                set(map(tuple, line["not_evaluable_triples"])) == {(-1,0,0), (1,0,0)},
                "line collapsed-camera oracle")
        require(line["rank_counts"] == {"0":2, "1":n-2, "2":0},
                "line rank oracle")
        require(all(item["reduced_corner_count"] == 2
                    for item in line["per_camera"] if item["status"] == "EVALUABLE"),
                "forward-collinear line subdivision was not removed")
        require(line["SO2"]["class_count"] == line_counts[family, level] and
                line["O2"]["class_count"] == line_counts[family, level],
                "line class oracle")
        for solid in ("CS-T", "CS-B"):
            item = row["control_results"][solid]
            require(item["not_evaluable_count"] == 0 and item["rank_counts"]["2"] == n,
                    "convex-solid dimension oracle")
        if level == "G0":
            tet, box = row["control_results"]["CS-T"], row["control_results"]["CS-B"]
            require((tet["SO2"]["class_count"], tet["O2"]["class_count"]) == (6, 3),
                    "G0 asymmetric tetrahedron silhouette oracle")
            require((box["SO2"]["class_count"], box["O2"]["class_count"]) == (3, 3),
                    "G0 rectangular-box silhouette oracle")
    # Ignore only family name, which is an administrative label at shared G0.
    require(lookup["A", "G0"]["signed_camera_triples"] ==
            lookup["B", "G0"]["signed_camera_triples"] and
            lookup["A", "G0"]["control_results"] == lookup["B", "G0"]["control_results"],
            "A/B G0 complete output mismatch")
    for fam in ("A", "B"):
        for observable in CONTROLS:
            for group in ("SO2", "O2"):
                counts = [lookup[fam, "G"+str(i)]["control_results"][observable][group]["class_count"]
                          for i in (0, 1, 2)]
                require(counts == sorted(counts), "nested grids lost an equivalence class")
            for level in (1, 2):
                before = lookup[fam, "G"+str(level-1)]
                after = lookup[fam, "G"+str(level)]
                old = before["control_results"][observable]
                new = after["control_results"][observable]
                m = before["signed_camera_count"]
                require(after["signed_camera_triples"][:m] == before["signed_camera_triples"],
                        "non-append-only camera grid")
                require(new["per_camera"][:m] == old["per_camera"],
                        "nested camera geometry changed")
                for group in ("SO2", "O2"):
                    require([row[:m] for row in new[group]["pairwise_equivalence_matrix"][:m]]
                            == old[group]["pairwise_equivalence_matrix"],
                            "nested equivalence relation changed")
    require([len(STRATA[s]) for s in ("A0", "C", "E", "T")] == [6, 8, 12, 24],
            "incorrect V1 strata cardinalities")


def main():
    records = []
    for family in ("A", "B"):
        for level in range(3):
            cameras = camera_grid(family, level)
            canon = [c.triple for c in cameras]
            axes = {tuple(v if next(z for z in t if z != 0) > 0 else -v for v in t)
                    for t in canon}
            row = {
                "family": family,
                "level": "G"+str(level),
                "signed_camera_count": len(cameras),
                "axis_count": len(axes),
                "signed_camera_triples": [list(t) for t in canon],
                "axis_representatives": [list(t) for t in sorted(axes)],
                "control_results": {control: control_result(cameras, control)
                                    for control in CONTROLS},
            }
            records.append(row)
    verify_global(records)
    result = {
        "study": STUDY,
        "status": "PASS_INTERNAL_ORACLES_AWAITING_INDEPENDENT_REVIEW",
        "preregistration_commit": COMMIT,
        "preregistration_blob": BLOB,
        "preregistration_path": PROTOCOL,
        "python_version": sys.version,
        "platform": platform.platform(),
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "arithmetic": "fractions.Fraction, exact orientation signs, sign-aware squared-radical equality",
        "observables": "TR path-order-aware continuous PL traces; CS filled convex projected hulls",
        "stratum_counts": {k: len(v) for k, v in STRATA.items()},
        "family_level_results": records,
        "higher_tier_counts": "determined by registered exact run, not preregistered predictions",
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
