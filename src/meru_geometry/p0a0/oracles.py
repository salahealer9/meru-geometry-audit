"""Independent scalar/analytic reference paths; no engineering imports or SVD."""
import math


def projection(points, matrix, axes=(0, 1)):
    return [[sum(float(matrix[i][j])*float(p[j]) for j in range(3)) for i in axes] for p in points]


def similarity_error(source, target, reflection=False):
    """Analytic minimum RMS: maximize a*cos(theta)+b*sin(theta).

    Reference enumerates det +1 and optionally det -1; no matrix decomposition.
    Nonnegative scale convention matches inherited API. Inputs already validated.
    """
    n = len(source)
    sx, sy = (sum(p[k] for p in source)/n for k in (0, 1))
    tx, ty = (sum(p[k] for p in target)/n for k in (0, 1))
    x = [(p[0]-sx, p[1]-sy) for p in source]
    y = [(p[0]-tx, p[1]-ty) for p in target]
    energy = sum(a*a+b*b for a, b in x)
    target_energy = sum(a*a+b*b for a, b in y)
    results = []
    for sign in ((1, -1) if reflection else (1,)):
        aa = sum(a*c+sign*b*d for (a,b),(c,d) in zip(x,y))
        bb = sum(a*d-sign*b*c for (a,b),(c,d) in zip(x,y))
        theta = math.atan2(bb, aa)
        co, si = math.cos(theta), math.sin(theta)
        scale = math.hypot(aa, bb)/energy
        # Explicit residual avoids cancellation in E_y - correlation^2/E_x.
        ss = sum((scale*(a*co-sign*b*si)-c)**2+
                 (scale*(a*si+sign*b*co)-d)**2 for (a,b),(c,d) in zip(x,y))
        results.append(math.sqrt(ss/target_energy))
    return min(results)


def nearest_support(a, b):
    """Scalar exhaustive loops, independent of broadcast distance kernel."""
    def directed(x, y):
        return [min(math.hypot(p[0]-q[0], p[1]-q[1]) for q in y) for p in x]
    x, y = directed(a,b), directed(b,a)
    return {"chamfer": (sum(x)/len(x)+sum(y)/len(y))/2,
            "hausdorff": max(max(x),max(y))}


def axis_landmark_extrema(weight):
    """For 0<w<1: f(c)=1-c^2+2w(1-c), c in [-1,1].

    Interior c=-w is a maximum. Only circle minima: angle 0 and pi.
    The derivative has factor sin(theta)*(cos(theta)+w). Global minimum
    is exactly zero, unique modulo 2pi; pi is strict local minimum 4w.
    """
    if not 0 < weight < 1:
        raise ValueError("oracle requires 0 < weight < 1")
    return {"global_angle": 0., "global_value": 0., "local_angle": math.pi,
            "local_value": 4*weight, "maximum_value": (1+weight)**2,
            "tie_rule": "smallest angle in [0,2*pi)"}


def horizontal_coverage(intervals, *, bounds, shape, width, supersample):
    """Scalar analytic capsule inequality for horizontal y=0 fixture strokes.

    No arbitrary-segment projection kernel. Used for S05 raster oracle.
    """
    left, bottom, right, top = bounds
    h, w = shape; ss = supersample; radius2 = (width/2)**2
    rows = []
    for i in range(h):
        row = []
        for j in range(w):
            hits = 0
            for di in range(ss):
                y = bottom+(i+(di+.5)/ss)*(top-bottom)/h
                for dj in range(ss):
                    x = left+(j+(dj+.5)/ss)*(right-left)/w
                    if any(y*y+max(a-x,0,x-b)**2 <= radius2 for a,b in intervals):
                        hits += 1
            row.append(hits/(ss*ss))
        rows.append(row)
    return rows
