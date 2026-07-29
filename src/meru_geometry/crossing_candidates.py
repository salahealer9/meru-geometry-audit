"""Geometric candidate detection for crossings between traced polylines."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from itertools import combinations

import numpy as np
from numpy.typing import ArrayLike, NDArray


SegmentKey = tuple[str, int]

LAYER_ORDER = {
    "red": 0,
    "green": 1,
    "blue": 2,
}

LAYER_CODE = {
    "red": "R",
    "green": "G",
    "blue": "B",
}


@dataclass(frozen=True)
class ClosestPolylineApproach:
    """Closest local approach between two piecewise-linear curves."""

    point_a: tuple[float, float]
    point_b: tuple[float, float]
    distance: float
    crossing_angle_radians: float
    piece_index_a: int
    piece_index_b: int
    fraction_a: float
    fraction_b: float
    intersects: bool


@dataclass(frozen=True)
class CrossingCandidate:
    """One candidate crossing between two non-adjacent visible fragments."""

    key_a: SegmentKey
    key_b: SegmentKey
    candidate_kind: str
    point_x: float
    point_y: float
    distance: float
    crossing_angle_radians: float
    piece_index_a: int
    piece_index_b: int
    fraction_a: float
    fraction_b: float


def _validate_polyline(
    points: ArrayLike,
) -> NDArray[np.float64]:
    """Validate and return a planar polyline."""
    array = np.asarray(points, dtype=np.float64)

    if array.ndim != 2 or array.shape[1] != 2:
        raise ValueError(
            "Polyline points must have shape (n, 2)."
        )

    if array.shape[0] < 2:
        raise ValueError(
            "A polyline must contain at least two points."
        )

    if not np.isfinite(array).all():
        raise ValueError(
            "Polyline coordinates must be finite."
        )

    return array


def _cross_2d(
    vector_a: NDArray[np.float64],
    vector_b: NDArray[np.float64],
) -> float:
    """Return the scalar two-dimensional cross product."""
    return float(
        vector_a[0] * vector_b[1]
        - vector_a[1] * vector_b[0]
    )


def _closest_point_on_segment(
    point: NDArray[np.float64],
    start: NDArray[np.float64],
    end: NDArray[np.float64],
) -> tuple[NDArray[np.float64], float]:
    """Return the closest point and parameter on a line segment."""
    direction = end - start
    denominator = float(
        np.dot(direction, direction)
    )

    if denominator <= np.finfo(np.float64).eps:
        return start.copy(), 0.0

    fraction = float(
        np.dot(point - start, direction)
        / denominator
    )

    fraction = float(
        np.clip(fraction, 0.0, 1.0)
    )

    closest = start + fraction * direction
    return closest, fraction


def _acute_angle(
    direction_a: NDArray[np.float64],
    direction_b: NDArray[np.float64],
) -> float:
    """Return the unsigned acute angle between two directions."""
    norm_a = float(np.linalg.norm(direction_a))
    norm_b = float(np.linalg.norm(direction_b))

    if (
        norm_a <= np.finfo(np.float64).eps
        or norm_b <= np.finfo(np.float64).eps
    ):
        raise ValueError(
            "Cannot calculate an angle from a zero-length segment."
        )

    cosine = float(
        np.dot(direction_a, direction_b)
        / (norm_a * norm_b)
    )

    cosine = abs(
        float(np.clip(cosine, -1.0, 1.0))
    )

    return float(np.arccos(cosine))


def _segment_approach(
    p0: NDArray[np.float64],
    p1: NDArray[np.float64],
    q0: NDArray[np.float64],
    q1: NDArray[np.float64],
    tolerance: float = 1.0e-10,
) -> tuple[
    NDArray[np.float64],
    NDArray[np.float64],
    float,
    float,
    bool,
]:
    """Return closest points between two planar line segments."""
    direction_p = p1 - p0
    direction_q = q1 - q0

    if (
        np.linalg.norm(direction_p)
        <= np.finfo(np.float64).eps
        or np.linalg.norm(direction_q)
        <= np.finfo(np.float64).eps
    ):
        raise ValueError(
            "Polyline pieces must have non-zero length."
        )

    denominator = _cross_2d(
        direction_p,
        direction_q,
    )

    offset = q0 - p0

    if abs(denominator) > tolerance:
        fraction_p = (
            _cross_2d(offset, direction_q)
            / denominator
        )

        fraction_q = (
            _cross_2d(offset, direction_p)
            / denominator
        )

        if (
            -tolerance <= fraction_p <= 1.0 + tolerance
            and -tolerance <= fraction_q <= 1.0 + tolerance
        ):
            fraction_p = float(
                np.clip(fraction_p, 0.0, 1.0)
            )

            fraction_q = float(
                np.clip(fraction_q, 0.0, 1.0)
            )

            point = (
                p0 + fraction_p * direction_p
            )

            return (
                point,
                point.copy(),
                fraction_p,
                fraction_q,
                True,
            )

    possibilities: list[
        tuple[
            float,
            NDArray[np.float64],
            NDArray[np.float64],
            float,
            float,
        ]
    ] = []

    q_point, q_fraction = (
        _closest_point_on_segment(
            p0,
            q0,
            q1,
        )
    )

    possibilities.append(
        (
            float(np.linalg.norm(p0 - q_point)),
            p0.copy(),
            q_point,
            0.0,
            q_fraction,
        )
    )

    q_point, q_fraction = (
        _closest_point_on_segment(
            p1,
            q0,
            q1,
        )
    )

    possibilities.append(
        (
            float(np.linalg.norm(p1 - q_point)),
            p1.copy(),
            q_point,
            1.0,
            q_fraction,
        )
    )

    p_point, p_fraction = (
        _closest_point_on_segment(
            q0,
            p0,
            p1,
        )
    )

    possibilities.append(
        (
            float(np.linalg.norm(p_point - q0)),
            p_point,
            q0.copy(),
            p_fraction,
            0.0,
        )
    )

    p_point, p_fraction = (
        _closest_point_on_segment(
            q1,
            p0,
            p1,
        )
    )

    possibilities.append(
        (
            float(np.linalg.norm(p_point - q1)),
            p_point,
            q1.copy(),
            p_fraction,
            1.0,
        )
    )

    (
        distance,
        point_p,
        point_q,
        fraction_p,
        fraction_q,
    ) = min(
        possibilities,
        key=lambda item: item[0],
    )

    return (
        point_p,
        point_q,
        fraction_p,
        fraction_q,
        distance <= tolerance,
    )


def closest_polyline_approach(
    points_a: ArrayLike,
    points_b: ArrayLike,
) -> ClosestPolylineApproach:
    """Find the closest piece-pair between two planar polylines."""
    polyline_a = _validate_polyline(points_a)
    polyline_b = _validate_polyline(points_b)

    best: ClosestPolylineApproach | None = None

    for index_a in range(
        polyline_a.shape[0] - 1
    ):
        p0 = polyline_a[index_a]
        p1 = polyline_a[index_a + 1]

        if np.linalg.norm(p1 - p0) <= 1.0e-12:
            continue

        for index_b in range(
            polyline_b.shape[0] - 1
        ):
            q0 = polyline_b[index_b]
            q1 = polyline_b[index_b + 1]

            if np.linalg.norm(q1 - q0) <= 1.0e-12:
                continue

            (
                point_a,
                point_b,
                fraction_a,
                fraction_b,
                intersects,
            ) = _segment_approach(
                p0,
                p1,
                q0,
                q1,
            )

            distance = float(
                np.linalg.norm(
                    point_a - point_b
                )
            )

            angle = _acute_angle(
                p1 - p0,
                q1 - q0,
            )

            approach = ClosestPolylineApproach(
                point_a=(
                    float(point_a[0]),
                    float(point_a[1]),
                ),
                point_b=(
                    float(point_b[0]),
                    float(point_b[1]),
                ),
                distance=distance,
                crossing_angle_radians=angle,
                piece_index_a=index_a,
                piece_index_b=index_b,
                fraction_a=fraction_a,
                fraction_b=fraction_b,
                intersects=intersects,
            )

            if best is None:
                best = approach
                continue

            if approach.distance < best.distance - 1.0e-10:
                best = approach
                continue

            if (
                abs(
                    approach.distance
                    - best.distance
                )
                <= 1.0e-10
                and approach.crossing_angle_radians
                > best.crossing_angle_radians
            ):
                best = approach

    if best is None:
        raise ValueError(
            "No non-degenerate polyline pieces were available."
        )

    return best


def normalized_pair(
    key_a: SegmentKey,
    key_b: SegmentKey,
) -> tuple[SegmentKey, SegmentKey]:
    """Return a deterministic unordered pair of segment keys."""
    def sort_key(
        key: SegmentKey,
    ) -> tuple[int, int]:
        layer, segment_id = key
        return (
            LAYER_ORDER[layer],
            segment_id,
        )

    return tuple(
        sorted(
            (key_a, key_b),
            key=sort_key,
        )
    )


def cycle_adjacency_pairs(
    traversal: Sequence[SegmentKey],
) -> set[tuple[SegmentKey, SegmentKey]]:
    """Return adjacent visible-segment pairs in a cyclic traversal."""
    if len(traversal) < 2:
        return set()

    result = set()

    for index, key_a in enumerate(traversal):
        key_b = traversal[
            (index + 1) % len(traversal)
        ]

        result.add(
            normalized_pair(key_a, key_b)
        )

    return result


def crossing_candidate_identifier(
    candidate: CrossingCandidate,
) -> str:
    """Return a stable identifier for one segment-pair candidate."""
    layer_a, segment_a = candidate.key_a
    layer_b, segment_b = candidate.key_b

    return (
        "XING_"
        f"{LAYER_CODE[layer_a]}_S{segment_a:02d}_"
        f"{LAYER_CODE[layer_b]}_S{segment_b:02d}"
    )


def find_crossing_candidates(
    segments: Mapping[
        SegmentKey,
        ArrayLike,
    ],
    adjacent_pairs: set[
        tuple[SegmentKey, SegmentKey]
    ] | None = None,
    max_distance: float = 10.0,
    min_angle_degrees: float = 12.0,
) -> tuple[CrossingCandidate, ...]:
    """Find close, non-adjacent segment pairs for manual review."""
    if max_distance < 0.0:
        raise ValueError(
            "max_distance must be non-negative."
        )

    if not 0.0 <= min_angle_degrees <= 90.0:
        raise ValueError(
            "min_angle_degrees must lie between 0 and 90."
        )

    adjacent = adjacent_pairs or set()
    minimum_angle = np.radians(
        min_angle_degrees
    )

    keys = sorted(
        segments,
        key=lambda key: (
            LAYER_ORDER[key[0]],
            key[1],
        ),
    )

    candidates: list[CrossingCandidate] = []

    for key_a, key_b in combinations(keys, 2):
        pair = normalized_pair(
            key_a,
            key_b,
        )

        if pair in adjacent:
            continue

        approach = closest_polyline_approach(
            segments[key_a],
            segments[key_b],
        )

        if approach.distance > max_distance:
            continue

        if (
            approach.crossing_angle_radians
            < minimum_angle
        ):
            continue

        point_a = np.asarray(
            approach.point_a,
            dtype=np.float64,
        )

        point_b = np.asarray(
            approach.point_b,
            dtype=np.float64,
        )

        midpoint = (
            point_a + point_b
        ) / 2.0

        candidates.append(
            CrossingCandidate(
                key_a=key_a,
                key_b=key_b,
                candidate_kind=(
                    "intersection"
                    if approach.intersects
                    else "near_crossing"
                ),
                point_x=float(midpoint[0]),
                point_y=float(midpoint[1]),
                distance=approach.distance,
                crossing_angle_radians=(
                    approach.crossing_angle_radians
                ),
                piece_index_a=(
                    approach.piece_index_a
                ),
                piece_index_b=(
                    approach.piece_index_b
                ),
                fraction_a=approach.fraction_a,
                fraction_b=approach.fraction_b,
            )
        )

    candidates.sort(
        key=lambda candidate: (
            0
            if candidate.candidate_kind
            == "intersection"
            else 1,
            candidate.distance,
            -candidate.crossing_angle_radians,
            crossing_candidate_identifier(
                candidate
            ),
        )
    )

    return tuple(candidates)
