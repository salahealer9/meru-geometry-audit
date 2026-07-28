"""Ranking of unresolved endpoint pairings between connectivity components."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from itertools import combinations

import numpy as np
from numpy.typing import ArrayLike, NDArray

from meru_geometry.connectivity import (
    ConnectivityComponent,
    Endpoint,
    format_endpoint,
)


LAYER_PREFIX = {
    "red": "R",
    "green": "G",
    "blue": "B",
}


@dataclass(frozen=True)
class ResidualEndpointCandidate:
    """One unresolved pairing between two currently free endpoints."""

    layer: str
    candidate_type: str
    component_a: int
    component_b: int
    segment_a: int
    endpoint_a: str
    segment_b: int
    endpoint_b: str
    distance: float
    tangent_mismatch_radians: float
    score: float


def _validate_segment(
    points: ArrayLike,
) -> NDArray[np.float64]:
    """Validate one visible planar segment."""
    array = np.asarray(points, dtype=np.float64)

    if array.ndim != 2 or array.shape[1] != 2:
        raise ValueError("segment points must have shape (n, 2).")
    if array.shape[0] < 2:
        raise ValueError("segment must contain at least two points.")
    if not np.isfinite(array).all():
        raise ValueError("segment points must be finite.")

    return array


def endpoint_coordinate(
    points: ArrayLike,
    endpoint: str,
) -> NDArray[np.float64]:
    """Return a segment endpoint coordinate."""
    array = _validate_segment(points)

    if endpoint == "start":
        return array[0].copy()

    if endpoint == "end":
        return array[-1].copy()

    raise ValueError("endpoint must be 'start' or 'end'.")


def outward_endpoint_tangent(
    points: ArrayLike,
    endpoint: str,
) -> NDArray[np.float64]:
    """Return the tangent pointing outward from a visible segment."""
    array = _validate_segment(points)

    if endpoint == "start":
        tangent = array[0] - array[1]
    elif endpoint == "end":
        tangent = array[-1] - array[-2]
    else:
        raise ValueError("endpoint must be 'start' or 'end'.")

    norm = float(np.linalg.norm(tangent))

    if norm <= np.finfo(np.float64).eps:
        raise ValueError("endpoint tangent is degenerate.")

    return tangent / norm


def _build_candidate(
    layer: str,
    segments: Mapping[int, ArrayLike],
    component_a: int,
    endpoint_a: Endpoint,
    component_b: int,
    endpoint_b: Endpoint,
) -> ResidualEndpointCandidate:
    """Construct one distance-and-tangent pairing candidate."""
    if layer not in LAYER_PREFIX:
        raise ValueError(f"Unsupported layer: {layer}")

    segment_a, endpoint_name_a = endpoint_a
    segment_b, endpoint_name_b = endpoint_b

    point_a = endpoint_coordinate(
        segments[segment_a],
        endpoint_name_a,
    )
    point_b = endpoint_coordinate(
        segments[segment_b],
        endpoint_name_b,
    )

    tangent_a = outward_endpoint_tangent(
        segments[segment_a],
        endpoint_name_a,
    )
    tangent_b = outward_endpoint_tangent(
        segments[segment_b],
        endpoint_name_b,
    )

    gap = point_b - point_a
    distance = float(np.linalg.norm(gap))

    if distance <= np.finfo(np.float64).eps:
        tangent_mismatch = 0.0
    else:
        direction = gap / distance

        angle_a = float(
            np.arccos(
                np.clip(
                    np.dot(tangent_a, direction),
                    -1.0,
                    1.0,
                )
            )
        )

        angle_b = float(
            np.arccos(
                np.clip(
                    np.dot(tangent_b, -direction),
                    -1.0,
                    1.0,
                )
            )
        )

        tangent_mismatch = (angle_a + angle_b) / 2.0

    score = distance * (
        1.0 + tangent_mismatch / np.pi
    )

    return ResidualEndpointCandidate(
        layer=layer,
        candidate_type=(
            "close"
            if component_a == component_b
            else "merge"
        ),
        component_a=component_a,
        component_b=component_b,
        segment_a=segment_a,
        endpoint_a=endpoint_name_a,
        segment_b=segment_b,
        endpoint_b=endpoint_name_b,
        distance=distance,
        tangent_mismatch_radians=tangent_mismatch,
        score=score,
    )


def rank_free_endpoint_pairs(
    layer: str,
    segments: Mapping[int, ArrayLike],
    components: Sequence[ConnectivityComponent],
    include_same_component: bool = False,
) -> tuple[ResidualEndpointCandidate, ...]:
    """Rank all permitted pairings among currently free endpoints."""
    free_endpoints: list[tuple[int, Endpoint]] = []

    for component_id, component in enumerate(
        components,
        start=1,
    ):
        for endpoint in component.free_endpoints:
            free_endpoints.append(
                (component_id, endpoint)
            )

    candidates: list[ResidualEndpointCandidate] = []

    for first, second in combinations(
        free_endpoints,
        2,
    ):
        component_a, endpoint_a = first
        component_b, endpoint_b = second

        if (
            component_a == component_b
            and not include_same_component
        ):
            continue

        candidates.append(
            _build_candidate(
                layer,
                segments,
                component_a,
                endpoint_a,
                component_b,
                endpoint_b,
            )
        )

    candidates.sort(
        key=lambda candidate: (
            candidate.score,
            candidate.distance,
            candidate.component_a,
            candidate.component_b,
            candidate.segment_a,
            candidate.segment_b,
        )
    )

    return tuple(candidates)


def best_merge_per_component_pair(
    candidates: Sequence[ResidualEndpointCandidate],
) -> tuple[ResidualEndpointCandidate, ...]:
    """Retain the best candidate for every unordered component pair."""
    best: dict[
        tuple[int, int],
        ResidualEndpointCandidate,
    ] = {}

    for candidate in candidates:
        if candidate.candidate_type != "merge":
            continue

        key = tuple(
            sorted(
                (
                    candidate.component_a,
                    candidate.component_b,
                )
            )
        )

        current = best.get(key)

        if (
            current is None
            or candidate.score < current.score
        ):
            best[key] = candidate

    selected = sorted(
        best.values(),
        key=lambda candidate: (
            candidate.component_a,
            candidate.component_b,
        ),
    )

    return tuple(selected)


def closure_candidate(
    layer: str,
    segments: Mapping[int, ArrayLike],
    component: ConnectivityComponent,
    component_id: int,
) -> ResidualEndpointCandidate:
    """Construct the only closure candidate for an open path component."""
    if len(component.free_endpoints) != 2:
        raise ValueError(
            "A closure candidate requires exactly two free endpoints."
        )

    return _build_candidate(
        layer,
        segments,
        component_id,
        component.free_endpoints[0],
        component_id,
        component.free_endpoints[1],
    )


def residual_candidate_identifier(
    candidate: ResidualEndpointCandidate,
) -> str:
    """Return a stable identifier for a residual candidate."""
    prefix = LAYER_PREFIX[candidate.layer]

    kind = (
        "M"
        if candidate.candidate_type == "merge"
        else "C"
    )

    endpoint_a = format_endpoint(
        (
            candidate.segment_a,
            candidate.endpoint_a,
        )
    )

    endpoint_b = format_endpoint(
        (
            candidate.segment_b,
            candidate.endpoint_b,
        )
    )

    return (
        f"{prefix}_{kind}_"
        f"C{candidate.component_a:02d}_"
        f"C{candidate.component_b:02d}_"
        f"{endpoint_a}_{endpoint_b}"
    )
