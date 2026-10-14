"""Additive synthetic operations; no file, image, font or network readers.

Graph topology is supplied, never inferred from a raster or point cloud.
Support distances below concern sampled supports, not continuous Hausdorff.
"""
from dataclasses import dataclass
import math
import numpy as np
from scipy.optimize import minimize_scalar
from meru_geometry.projection_orbits import best_curve_alignment


def points(value, dimension=2, minimum=2):
    a = np.asarray(value, dtype=np.float64)
    if a.ndim != 2 or a.shape[1] != dimension or len(a) < minimum:
        raise ValueError("invalid point array shape")
    if not np.isfinite(a).all():
        raise ValueError("nonfinite points")
    if np.max(np.abs(a), initial=0) > 1e100:
        raise ValueError("coordinates outside supported numerical range")
    return a


def positive(value, name):
    x = float(value)
    if not math.isfinite(x) or x <= 0:
        raise ValueError(name + " must be finite and positive")
    return x


def count(value, name, minimum=2):
    if isinstance(value, (bool, np.bool_)) or not isinstance(value, (int, np.integer)) or value < minimum:
        raise ValueError(name + " must be an integer in range")
    return int(value)


def normalize(path):
    """Sample-mean/RMS normalization, explicitly sampling-density sensitive."""
    a = points(path)
    centre = a.mean(axis=0)
    q = a-centre
    radius = float(np.sqrt(np.mean(np.sum(q*q, axis=1))))
    if not np.isfinite(radius) or radius < 1e-14:
        raise ValueError("extent below absolute 1e-14 numerical floor")
    return q/radius, centre, radius


def resample(path, samples=129, closed=False):
    """Polyline arclength; remove consecutive exact duplicates, not short edges.

    Open sampling includes both ends. Closed sampling excludes the final end.
    Curved inputs denote their piecewise-linear interpolant, not an unknown curve.
    """
    n = count(samples, "samples")
    a = points(path)
    a = a[np.r_[True, np.any(np.diff(a, axis=0) != 0, axis=1)]]
    if closed and not np.array_equal(a[0], a[-1]):
        a = np.vstack((a, a[0]))
    lengths = np.linalg.norm(np.diff(a, axis=0), axis=1)
    total = float(lengths.sum())
    if not math.isfinite(total) or total < 1e-14:
        raise ValueError("path length below absolute 1e-14 numerical floor")
    s = np.r_[0., np.cumsum(lengths)]
    if np.any(np.diff(s) <= 0):
        raise ValueError("arclength increment lost to floating-point resolution")
    at = np.linspace(0, total, n, endpoint=not closed)
    return np.column_stack([np.interp(at, s, a[:, axis]) for axis in (0, 1)])


def ordered_match(source, target, *, closed=False, reversal=False, reflection=False, samples=None):
    """Inherited alignment with explicit semantics and stricter extent checks.

    Inherits the nonnegative scale boundary s=0, which represents a non-match.
    No cyclic shifts are considered for an open path.
    """
    a, b = points(source), points(target)
    if samples is not None:
        a, b = resample(a, samples, closed), resample(b, samples, closed)
    normalize(a); normalize(b)
    return best_curve_alignment(a, b, closed=closed, allow_reversal=reversal,
                                allow_reflection=reflection)


def support_distance(source, target):
    """Symmetric mean nearest-neighbour distance and sampled Hausdorff.

    No transformation optimization; duplicate multiplicities affect the mean.
    """
    a, b = points(source, minimum=1), points(target, minimum=1)
    d = np.linalg.norm(a[:, None, :]-b[None, :, :], axis=2)
    x, y = d.min(axis=1), d.min(axis=0)
    return {"chamfer": float((x.mean()+y.mean())/2),
            "hausdorff": float(max(x.max(), y.max()))}


def graph_counts(vertices, edges, strokes):
    """Combinatorial graph, supplied with all junctions explicitly split.

    Distinct vertex IDs remain distinct even at identical coordinates. Edges
    are undirected and unique; each belongs to exactly one ordered stroke.
    Stroke lists contain vertex IDs, so endpoints include segmentation labels.
    Interior crossings are not discovered. No snapping or gap closing occurs.
    """
    v = points(vertices, minimum=1)
    def index(i):
        if isinstance(i, bool) or not isinstance(i, (int, np.integer)) or not 0 <= i < len(v):
            raise ValueError("invalid vertex index")
        return int(i)
    pairs = []
    for e in edges:
        if len(e) != 2:
            raise ValueError("edge must have two indices")
        i, j = map(index, e)
        if i == j or np.array_equal(v[i], v[j]):
            raise ValueError("zero-length edge")
        pairs.append(tuple(sorted((i, j))))
    if not pairs or len(set(pairs)) != len(pairs):
        raise ValueError("empty or repeated edge")
    used = []
    labelled_ends = 0
    for stroke in strokes:
        if len(stroke) < 2:
            raise ValueError("stroke needs two indices")
        ids = list(map(index, stroke))
        used.extend(tuple(sorted(e)) for e in zip(ids[:-1], ids[1:]))
        labelled_ends += 0 if ids[0] == ids[-1] else 2
    if sorted(used) != sorted(pairs):
        raise ValueError("strokes must partition supplied edges")
    neighbours = [set() for _ in v]
    for i, j in pairs:
        neighbours[i].add(j); neighbours[j].add(i)
    if any(not x for x in neighbours):
        raise ValueError("isolated vertices unsupported; represent nonzero component edges")
    unseen = set(range(len(v))); components = 0
    while unseen:
        todo = [min(unseen)]; components += 1
        while todo:
            i = todo.pop()
            if i in unseen:
                unseen.remove(i); todo.extend(neighbours[i])
    degrees = [len(x) for x in neighbours]
    return {"components": components, "exposed_endpoints": degrees.count(1),
            "junctions": sum(d > 2 for d in degrees), "strokes": len(strokes),
            "labelled_endpoints": labelled_ends}


def component_composite(chamfer, count_a, count_b, weight=0.25):
    """Transparent synthetic composite; no final scientific weight selected."""
    w = positive(weight, "weight")
    count(count_a, "count_a", 1); count(count_b, "count_b", 1)
    x = float(chamfer)
    if not np.isfinite(x) or x < 0:
        raise ValueError("invalid distance")
    return x+w*abs(count_a-count_b)


def rasterize(strokes, *, bounds, shape, width, supersample=1):
    """Round-capped Euclidean 2-D strokes, deterministic subpixel centre coverage.

    Return float64 coverage [0,1], rows ascending in y. This is a planar ink
    model, not a 3-D ribbon shadow. Thresholding belongs to the caller.
    """
    paths = [points(x) for x in strokes]
    if not paths:
        raise ValueError("no strokes")
    b = np.asarray(bounds, dtype=float)
    if b.shape != (4,) or not np.isfinite(b).all() or b[2] <= b[0] or b[3] <= b[1]:
        raise ValueError("invalid bounds")
    h, w = (count(x, "shape", 1) for x in shape)
    ss = count(supersample, "supersample", 1)
    if h*w*ss*ss > 4_000_000:
        raise ValueError("raster work budget exceeded")
    radius = positive(width, "width")/2
    x = b[0]+(np.arange(w*ss)+.5)*(b[2]-b[0])/(w*ss)
    y = b[1]+(np.arange(h*ss)+.5)*(b[3]-b[1])/(h*ss)
    xx, yy = np.meshgrid(x, y)
    q = np.column_stack((xx.ravel(), yy.ravel()))
    inside = np.zeros(len(q), dtype=bool)
    for path in paths:
        for a, z in zip(path[:-1], path[1:]):
            delta = z-a; denom = float(delta@delta)
            if denom == 0:
                raise ValueError("duplicate raster segment")
            u = np.clip((q-a)@delta/denom, 0, 1)
            inside |= np.sum((q-a-u[:, None]*delta)**2, axis=1) <= radius**2
    return inside.reshape(h, ss, w, ss).mean(axis=(1, 3))


def silhouette_distance(a, b, threshold=.5):
    x, y = np.asarray(a), np.asarray(b)
    if x.shape != y.shape or x.ndim != 2 or not x.size:
        raise ValueError("silhouettes must have equal nonempty shapes")
    if not np.isfinite(x).all() or not np.isfinite(y).all() or np.any(x < 0) or np.any(x > 1) or np.any(y < 0) or np.any(y > 1):
        raise ValueError("invalid coverage")
    t = positive(threshold, "threshold")
    if t > 1:
        raise ValueError("threshold > 1")
    x, y = x >= t, y >= t
    union = np.count_nonzero(x | y)
    if union == 0:
        return {"state": "NOT_EVALUABLE", "iou_distance": None, "reason": "both masks empty"}
    return {"state": "EVALUABLE", "iou_distance": 1-np.count_nonzero(x & y)/union}


def planar_axis_landmark_objective(theta, weight):
    """Unoriented axis normal error + weighted ordered unit-landmark chord."""
    t = float(theta); w = positive(weight, "weight")
    if not math.isfinite(t):
        raise ValueError("nonfinite angle")
    moved = np.array([math.cos(t), math.sin(t)])
    return float(moved[1]**2+w*np.sum((moved-np.array([1., 0.]))**2))


def local_planar_search(bounds, *, weight, xatol=1e-12, maxiter=200):
    lo, hi = map(float, bounds)
    if not np.isfinite([lo, hi]).all() or lo >= hi:
        raise ValueError("invalid local bounds")
    positive(xatol, "xatol"); count(maxiter, "maxiter", 1)
    result = minimize_scalar(planar_axis_landmark_objective, args=(weight,),
                             bounds=(lo, hi), method="bounded",
                             options={"xatol": xatol, "maxiter": maxiter})
    return {"angle": float(result.x), "value": float(result.fun),
            "success": bool(result.success), "nfev": int(result.nfev),
            "scope": "LOCAL_BOUNDED_ONLY"}
