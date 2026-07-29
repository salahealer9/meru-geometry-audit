#!/usr/bin/env python3
"""Audit nonincident faces of Meru's native 10_3 tube mesh."""
from __future__ import annotations

import csv
import hashlib
import json
import math
import re
from collections import Counter
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data/source_manifests/meru_3_10_digital/official_asset_manifest.csv"
RAW = ROOT / "data/source_snapshots/meru_3_10_digital/raw"
URL = "https://www.meru.org/compuimages/10_3.wrl"
EXPECTED_SHA256 = "855c46cfeeb31e4394b7a4a294b397aac4cbc14154e172a326e33243dd9e384b"
SECTIONS = 300
POINTS_PER_SECTION = 20
MAX_EXCLUSION_SEARCH = 20
OUT = ROOT / "data/derived/meru_3_10_digital/meru_10_3_surface_embedding_remote.json"
NUM = re.compile(r"[+-]?(?:(?:\d+\.\d*)|(?:\.\d+)|(?:\d+))(?:[eE][+-]?\d+)?")
INT = re.compile(r"-?\d+")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def strip_comments(text: str) -> str:
    return "\n".join(line.split("#", 1)[0] for line in text.splitlines())


def block(text: str, node: str) -> str:
    match = re.search(rf"\b{re.escape(node)}\s*\{{", text)
    if not match:
        raise RuntimeError(f"Missing {node} node")
    start = match.start()
    opening = text.find("{", start)
    depth = 0
    for i in range(opening, len(text)):
        if text[i] == "{":
            depth += 1
        elif text[i] == "}":
            depth -= 1
            if depth == 0:
                return text[start:i + 1]
    raise RuntimeError(f"Unbalanced {node} node")


def array(text: str, field: str) -> str:
    match = re.search(rf"\b{re.escape(field)}\s*\[", text)
    if not match:
        raise RuntimeError(f"Missing {field} array")
    opening = text.find("[", match.start())
    depth = 0
    for i in range(opening, len(text)):
        if text[i] == "[":
            depth += 1
        elif text[i] == "]":
            depth -= 1
            if depth == 0:
                return text[opening + 1:i]
    raise RuntimeError(f"Unbalanced {field} array")


def parse_mesh(text: str) -> tuple[np.ndarray, np.ndarray]:
    ifs = block(text, "IndexedFaceSet")
    coord = block(ifs, "Coordinate")
    values = np.asarray([float(x) for x in NUM.findall(array(coord, "point"))])
    vertices = values.reshape(-1, 3)

    polygons: list[list[int]] = []
    current: list[int] = []
    for value in (int(x) for x in INT.findall(array(ifs, "coordIndex"))):
        if value == -1:
            if current:
                polygons.append(current)
                current = []
        else:
            current.append(value)
    if current:
        polygons.append(current)

    faces: list[tuple[int, int, int]] = []
    for polygon in polygons:
        if len(polygon) < 3:
            raise RuntimeError("Face with fewer than three vertices")
        for i in range(1, len(polygon) - 1):
            faces.append((polygon[0], polygon[i], polygon[i + 1]))
    return vertices, np.asarray(faces, dtype=np.int64)


def topology(faces: np.ndarray) -> dict[str, int]:
    edges: Counter[tuple[int, int]] = Counter()
    for a, b, c in faces:
        for u, v in ((a, b), (b, c), (c, a)):
            edges[tuple(sorted((int(u), int(v))))] += 1
    v = len(np.unique(faces))
    e = len(edges)
    f = len(faces)
    return {
        "vertices": int(v),
        "edges": int(e),
        "faces": int(f),
        "boundary_edges": sum(n == 1 for n in edges.values()),
        "nonmanifold_edges": sum(n > 2 for n in edges.values()),
        "euler_characteristic": int(v - e + f),
    }


def face_strips(faces: np.ndarray) -> tuple[np.ndarray, Counter[int]]:
    result = np.full(len(faces), -1, dtype=np.int64)
    counts: Counter[int] = Counter()
    for i, face in enumerate(faces):
        sections = sorted({int(v) // POINTS_PER_SECTION for v in face})
        if len(sections) != 2:
            continue
        a, b = sections
        if (a + 1) % SECTIONS == b:
            strip = a
        elif (b + 1) % SECTIONS == a:
            strip = b
        else:
            continue
        result[i] = strip
        counts[strip] += 1
    return result, counts


def cyclic_distance(a: int, b: int) -> int:
    d = abs(a - b)
    return min(d, SECTIONS - d)


def segment_distance(p0: np.ndarray, p1: np.ndarray, q0: np.ndarray, q1: np.ndarray) -> float:
    # Standard closest-points formula for two finite 3-D segments.
    u, v, w = p1 - p0, q1 - q0, p0 - q0
    a, b, c = float(u @ u), float(u @ v), float(v @ v)
    d, e = float(u @ w), float(v @ w)
    D = a * c - b * b
    small = 1e-15
    sN, sD = (0.0, 1.0) if D <= small else (b * e - c * d, D)
    tN, tD = (e, c) if D <= small else (a * e - b * d, D)

    if sN < 0.0:
        sN, tN, tD = 0.0, e, c
    elif sN > sD:
        sN, tN, tD = sD, e + b, c

    if tN < 0.0:
        tN = 0.0
        if -d < 0.0:
            sN = 0.0
        elif -d > a:
            sN = sD
        else:
            sN, sD = -d, a
    elif tN > tD:
        tN = tD
        if -d + b < 0.0:
            sN = 0.0
        elif -d + b > a:
            sN = sD
        else:
            sN, sD = -d + b, a

    sc = 0.0 if abs(sN) <= small else sN / sD
    tc = 0.0 if abs(tN) <= small else tN / tD
    return float(np.linalg.norm(w + sc * u - tc * v))


def clearance_by_cyclic_distance(
    centreline: np.ndarray,
) -> dict[int, tuple[float, tuple[int, int]]]:
    """Return the closest centreline-segment pair at each cyclic distance."""
    minima = {d: (math.inf, (-1, -1)) for d in range(1, SECTIONS // 2 + 1)}
    for i in range(SECTIONS):
        p0, p1 = centreline[i], centreline[(i + 1) % SECTIONS]
        for j in range(i + 1, SECTIONS):
            cyclic = cyclic_distance(i, j)
            distance = segment_distance(
                p0,
                p1,
                centreline[j],
                centreline[(j + 1) % SECTIONS],
            )
            if distance < minima[cyclic][0]:
                minima[cyclic] = (distance, (i, j))
    return minima


def gap(a0: float, a1: float, b0: float, b1: float) -> float:
    return max(b0 - a1, a0 - b1)


def overlap_2d(a: np.ndarray, b: np.ndarray, tol: float) -> tuple[bool, float]:
    max_gap = -math.inf
    for tri in (a, b):
        for i in range(3):
            edge = tri[(i + 1) % 3] - tri[i]
            axis = np.array([-edge[1], edge[0]], dtype=float)
            norm = float(np.linalg.norm(axis))
            if norm <= 1e-15:
                continue
            axis /= norm
            pa, pb = a @ axis, b @ axis
            max_gap = max(max_gap, gap(float(pa.min()), float(pa.max()), float(pb.min()), float(pb.max())))
    return max_gap <= tol, max_gap


def overlap_3d(a: np.ndarray, b: np.ndarray, tol: float) -> tuple[bool, float, bool]:
    ea = np.array([a[1] - a[0], a[2] - a[1], a[0] - a[2]])
    eb = np.array([b[1] - b[0], b[2] - b[1], b[0] - b[2]])
    na, nb = np.cross(ea[0], ea[1]), np.cross(eb[0], eb[1])
    nna, nnb = float(np.linalg.norm(na)), float(np.linalg.norm(nb))
    parallel = float(np.linalg.norm(np.cross(na, nb))) <= 1e-12 * nna * nnb
    unit_na = na / nna
    coplanar = parallel and float(np.max(np.abs((b - a[0]) @ unit_na))) <= tol

    if coplanar:
        drop = int(np.argmax(np.abs(unit_na)))
        hit, margin = overlap_2d(np.delete(a, drop, axis=1), np.delete(b, drop, axis=1), tol)
        return hit, margin, True

    axes = [na, nb] + [np.cross(x, y) for x in ea for y in eb]
    max_gap = -math.inf
    for axis in axes:
        norm = float(np.linalg.norm(axis))
        if norm <= 1e-14:
            continue
        axis /= norm
        pa, pb = a @ axis, b @ axis
        max_gap = max(max_gap, gap(float(pa.min()), float(pa.max()), float(pb.min()), float(pb.max())))
    return max_gap <= tol, max_gap, False


with MANIFEST.open(newline="", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))
row = [r for r in rows if r["canonical_url"] == URL]
if len(row) != 1:
    raise SystemExit(f"Expected one manifest row for {URL}; found {len(row)}")
source = RAW / row[0]["snapshot_filename"]
source_hash = sha256(source)
if source_hash != EXPECTED_SHA256:
    raise SystemExit("10_3.wrl hash does not match the frozen source")

vertices, faces = parse_mesh(strip_comments(source.read_text(encoding="utf-8", errors="replace")))
if vertices.shape != (6000, 3) or faces.shape != (12000, 3):
    raise SystemExit(f"Unexpected mesh shape: vertices={vertices.shape}, faces={faces.shape}")

mesh_topology = topology(faces)
triangles = vertices[faces]
areas = 0.5 * np.linalg.norm(np.cross(triangles[:, 1] - triangles[:, 0], triangles[:, 2] - triangles[:, 0]), axis=1)
strips, strip_counts = face_strips(faces)
centreline = vertices.reshape(SECTIONS, POINTS_PER_SECTION, 3).mean(axis=1)
offsets = vertices.reshape(SECTIONS, POINTS_PER_SECTION, 3) - centreline[:, None, :]
max_radius = float(np.linalg.norm(offsets, axis=2).max())
clearance_minima = clearance_by_cyclic_distance(centreline)
clearance_profile: list[dict[str, object]] = []
first_passing_exclusion: int | None = None
remote_distance = math.inf
remote_pair = (-1, -1)
remote_margin = -math.inf

for exclusion in range(1, MAX_EXCLUSION_SEARCH + 1):
    distance, pair = min(
        (value for cyclic, value in clearance_minima.items() if cyclic > exclusion),
        key=lambda item: item[0],
    )
    margin = distance - 2.0 * max_radius
    clearance_profile.append({
        "local_exclusion": exclusion,
        "minimum_remote_centreline_distance": distance,
        "minimum_remote_centreline_pair": list(pair),
        "remote_capsule_margin": margin,
    })
    if first_passing_exclusion is None and margin > 0.0:
        first_passing_exclusion = exclusion
        remote_distance, remote_pair, remote_margin = distance, pair, margin

if first_passing_exclusion is None:
    remote_distance, remote_pair = clearance_profile[-1]["minimum_remote_centreline_distance"], tuple(clearance_profile[-1]["minimum_remote_centreline_pair"])
    remote_margin = float(clearance_profile[-1]["remote_capsule_margin"])

scale = float(np.linalg.norm(vertices.max(axis=0) - vertices.min(axis=0)))
broad_tol = scale * 1e-12
narrow_tol = scale * 1e-10
mins = triangles.min(axis=1) - broad_tol
maxs = triangles.max(axis=1) + broad_tol
order = np.argsort(mins[:, 0], kind="mergesort")
active: list[int] = []
counts = Counter({
    "aabb_candidates": 0,
    "shared_edge": 0,
    "shared_vertex_only": 0,
    "vertex_disjoint": 0,
    "coplanar_disjoint": 0,
    "vertex_disjoint_overlaps": 0,
})
min_sat_margin = math.inf
overlap_examples: list[dict[str, object]] = []

for position, current_raw in enumerate(order, start=1):
    current = int(current_raw)
    active = [j for j in active if maxs[j, 0] >= mins[current, 0]]
    for previous in active:
        if (maxs[previous, 1] < mins[current, 1] or maxs[current, 1] < mins[previous, 1]
                or maxs[previous, 2] < mins[current, 2] or maxs[current, 2] < mins[previous, 2]):
            continue
        counts["aabb_candidates"] += 1
        f0, f1 = faces[previous], faces[current]
        shared = sum(int(v in f1) for v in f0)
        if shared >= 2:
            counts["shared_edge"] += 1
            continue
        if shared == 1:
            counts["shared_vertex_only"] += 1
            continue

        counts["vertex_disjoint"] += 1
        hit, margin, coplanar = overlap_3d(triangles[previous], triangles[current], narrow_tol)
        if coplanar:
            counts["coplanar_disjoint"] += 1
        if hit:
            counts["vertex_disjoint_overlaps"] += 1
            if len(overlap_examples) < 20:
                overlap_examples.append({
                    "face_pair": [previous, current],
                    "strip_pair": [int(strips[previous]), int(strips[current])],
                    "cyclic_strip_distance": cyclic_distance(int(strips[previous]), int(strips[current])),
                    "coplanar": bool(coplanar),
                    "sat_margin": float(margin),
                })
        else:
            min_sat_margin = min(min_sat_margin, float(margin))
    active.append(current)
    if position % 2000 == 0:
        print(f"Broad phase: {position:5d}/12000 triangles; {counts['aabb_candidates']:,} candidates")

result = {
    "source": {"filename": source.name, "sha256": source_hash, "canonical_url": URL},
    "mesh": {
        **mesh_topology,
        "minimum_triangle_area": float(areas.min()),
        "maximum_triangle_area": float(areas.max()),
        "zero_area_triangles": int(np.count_nonzero(areas <= 1e-14)),
    },
    "structured_tube": {
        "section_count": SECTIONS,
        "points_per_section": POINTS_PER_SECTION,
        "invalid_strip_faces": int(np.count_nonzero(strips < 0)),
        "strip_count": len(strip_counts),
        "triangles_per_strip_values": sorted(set(strip_counts.values())),
        "maximum_section_radius": max_radius,
        "minimum_passing_local_exclusion": first_passing_exclusion,
        "maximum_exclusion_searched": MAX_EXCLUSION_SEARCH,
        "clearance_profile": clearance_profile,
        "minimum_remote_centreline_distance": remote_distance,
        "minimum_remote_centreline_pair": list(remote_pair),
        "remote_capsule_margin": remote_margin,
        "remote_capsule_pass": bool(remote_margin > narrow_tol),
    },
    "triangle_pair_census": {
        "broad_tolerance": broad_tol,
        "narrow_tolerance": narrow_tol,
        **{key: int(value) for key, value in counts.items()},
        "minimum_positive_sat_separation_margin": None if not math.isfinite(min_sat_margin) else min_sat_margin,
        "overlap_examples": overlap_examples,
    },
    "scope": {
        "tests_all_aabb_overlapping_vertex_disjoint_face_pairs": True,
        "expected_shared_vertex_and_edge_incidences_are_excluded": True,
        "formal_exact_arithmetic": False,
    },
}
OUT.parent.mkdir(
    parents=True,
    exist_ok=True,
)

OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")

print("\n" + "=" * 78)
print("MERU 10_3 SURFACE-EMBEDDING PROBE")
print("=" * 78)
print(f"Source:                         {source.name}")
print(f"Vertices / triangles / edges:  {len(vertices)} / {len(faces)} / {mesh_topology['edges']}")
print(f"Euler characteristic:          {mesh_topology['euler_characteristic']}")
print(f"Boundary / nonmanifold edges:  {mesh_topology['boundary_edges']} / {mesh_topology['nonmanifold_edges']}")
print(f"Minimum triangle area:         {areas.min():.12g}")
print(f"Invalid structured faces:      {np.count_nonzero(strips < 0)}")
print(f"Triangles per strip:           {sorted(set(strip_counts.values()))}")
print(f"Maximum section radius:        {max_radius:.12g}")
print(f"First passing exclusion:       {first_passing_exclusion}")
print(f"Remote centreline distance:    {remote_distance:.12g} at {remote_pair}")
print(f"Remote capsule margin:         {remote_margin:.12g}")
print(f"Remote capsule certificate:    {remote_margin > narrow_tol}")
print(f"AABB candidate pairs:          {counts['aabb_candidates']:,}")
print(f"Shared-edge candidates:        {counts['shared_edge']:,}")
print(f"Shared-vertex-only candidates: {counts['shared_vertex_only']:,}")
print(f"Vertex-disjoint candidates:    {counts['vertex_disjoint']:,}")
print(f"Coplanar disjoint candidates:  {counts['coplanar_disjoint']:,}")
print(f"Vertex-disjoint overlaps:      {counts['vertex_disjoint_overlaps']:,}")
if math.isfinite(min_sat_margin):
    print(f"Minimum SAT separation margin: {min_sat_margin:.12g}")
print(f"Wrote {OUT}")
