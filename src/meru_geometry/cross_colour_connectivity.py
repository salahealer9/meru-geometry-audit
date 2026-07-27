"""Cross-colour endpoint candidates and complete matching hypotheses."""

from __future__ import annotations

from collections import defaultdict
from collections.abc import (
    Iterable,
    Mapping,
    Sequence,
)
from dataclasses import dataclass
from itertools import combinations
from typing import Any

import numpy as np
from numpy.typing import ArrayLike

from meru_geometry.connectivity import Endpoint
from meru_geometry.endpoint_review import (
    VALID_CONFIDENCES,
    VALID_REASON_CODES,
    VALID_STATUSES,
)
from meru_geometry.residual_connectivity import (
    endpoint_coordinate,
    outward_endpoint_tangent,
)


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

LayerEndpoint = tuple[str, int, str]


@dataclass(frozen=True)
class CrossColourCandidate:
    """One proposed transition between two differently coloured chains."""

    layer_a: str
    segment_a: int
    endpoint_a: str
    layer_b: str
    segment_b: int
    endpoint_b: str
    distance: float
    tangent_mismatch_radians: float
    score: float


@dataclass(frozen=True)
class CrossColourMatching:
    """One complete pairing of all six free coloured endpoints."""

    candidates: tuple[CrossColourCandidate, ...]
    total_distance: float
    total_score: float
    maximum_edge_score: float


def candidate_endpoint_keys(
    candidate: CrossColourCandidate,
) -> tuple[LayerEndpoint, LayerEndpoint]:
    """Return the two layer-qualified endpoints of a candidate."""
    return (
        (
            candidate.layer_a,
            candidate.segment_a,
            candidate.endpoint_a,
        ),
        (
            candidate.layer_b,
            candidate.segment_b,
            candidate.endpoint_b,
        ),
    )


def _endpoint_sort_key(
    endpoint: LayerEndpoint,
) -> tuple[int, int, int]:
    """Return a deterministic ordering for coloured endpoints."""
    layer, segment_id, endpoint_name = endpoint

    return (
        LAYER_ORDER[layer],
        segment_id,
        0 if endpoint_name == "start" else 1,
    )


def _endpoint_token(
    layer: str,
    segment_id: int,
    endpoint_name: str,
) -> str:
    """Format one layer-qualified endpoint."""
    endpoint_code = {
        "start": "S",
        "end": "E",
    }

    if endpoint_name not in endpoint_code:
        raise ValueError(
            "endpoint must be 'start' or 'end'."
        )

    return (
        f"{LAYER_CODE[layer]}_"
        f"S{segment_id:02d}"
        f"{endpoint_code[endpoint_name]}"
    )


def cross_colour_candidate_identifier(
    candidate: CrossColourCandidate,
) -> str:
    """Return a stable identifier for a cross-colour candidate."""
    layer_pair = (
        f"{LAYER_CODE[candidate.layer_a]}"
        f"{LAYER_CODE[candidate.layer_b]}"
    )

    endpoint_a = _endpoint_token(
        candidate.layer_a,
        candidate.segment_a,
        candidate.endpoint_a,
    )

    endpoint_b = _endpoint_token(
        candidate.layer_b,
        candidate.segment_b,
        candidate.endpoint_b,
    )

    return (
        f"X_{layer_pair}_"
        f"{endpoint_a}_"
        f"{endpoint_b}"
    )


def build_cross_colour_candidate(
    layer_a: str,
    endpoint_a: Endpoint,
    layer_b: str,
    endpoint_b: Endpoint,
    segments: Mapping[
        str,
        Mapping[int, ArrayLike],
    ],
) -> CrossColourCandidate:
    """Construct one cross-colour distance-and-tangent candidate."""
    if layer_a not in LAYER_ORDER:
        raise ValueError(f"Unsupported layer: {layer_a}")

    if layer_b not in LAYER_ORDER:
        raise ValueError(f"Unsupported layer: {layer_b}")

    if layer_a == layer_b:
        raise ValueError(
            "Cross-colour candidates require different layers."
        )

    if LAYER_ORDER[layer_b] < LAYER_ORDER[layer_a]:
        layer_a, layer_b = layer_b, layer_a
        endpoint_a, endpoint_b = endpoint_b, endpoint_a

    segment_a, endpoint_name_a = endpoint_a
    segment_b, endpoint_name_b = endpoint_b

    point_a = endpoint_coordinate(
        segments[layer_a][segment_a],
        endpoint_name_a,
    )

    point_b = endpoint_coordinate(
        segments[layer_b][segment_b],
        endpoint_name_b,
    )

    tangent_a = outward_endpoint_tangent(
        segments[layer_a][segment_a],
        endpoint_name_a,
    )

    tangent_b = outward_endpoint_tangent(
        segments[layer_b][segment_b],
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

        tangent_mismatch = (
            angle_a + angle_b
        ) / 2.0

    score = distance * (
        1.0 + tangent_mismatch / np.pi
    )

    return CrossColourCandidate(
        layer_a=layer_a,
        segment_a=segment_a,
        endpoint_a=endpoint_name_a,
        layer_b=layer_b,
        segment_b=segment_b,
        endpoint_b=endpoint_name_b,
        distance=distance,
        tangent_mismatch_radians=tangent_mismatch,
        score=score,
    )


def rank_cross_colour_pairs(
    segments: Mapping[
        str,
        Mapping[int, ArrayLike],
    ],
    free_endpoints: Mapping[
        str,
        Sequence[Endpoint],
    ],
) -> tuple[CrossColourCandidate, ...]:
    """Rank all pairings between differently coloured free endpoints."""
    candidates: list[CrossColourCandidate] = []

    ordered_layers = tuple(
        sorted(
            LAYER_ORDER,
            key=LAYER_ORDER.get,
        )
    )

    for layer_a, layer_b in combinations(
        ordered_layers,
        2,
    ):
        for endpoint_a in free_endpoints[layer_a]:
            for endpoint_b in free_endpoints[layer_b]:
                candidates.append(
                    build_cross_colour_candidate(
                        layer_a,
                        endpoint_a,
                        layer_b,
                        endpoint_b,
                        segments,
                    )
                )

    candidates.sort(
        key=lambda candidate: (
            candidate.score,
            candidate.distance,
            cross_colour_candidate_identifier(
                candidate
            ),
        )
    )

    return tuple(candidates)


def enumerate_cross_colour_matchings(
    candidates: Sequence[CrossColourCandidate],
) -> tuple[CrossColourMatching, ...]:
    """Enumerate complete non-overlapping matchings of all free endpoints."""
    endpoints: set[LayerEndpoint] = set()

    incident: dict[
        LayerEndpoint,
        list[CrossColourCandidate],
    ] = defaultdict(list)

    for candidate in candidates:
        endpoint_a, endpoint_b = (
            candidate_endpoint_keys(candidate)
        )

        endpoints.add(endpoint_a)
        endpoints.add(endpoint_b)

        incident[endpoint_a].append(candidate)
        incident[endpoint_b].append(candidate)

    matching_keys: set[tuple[str, ...]] = set()
    results: list[CrossColourMatching] = []

    def recurse(
        remaining: frozenset[LayerEndpoint],
        selected: tuple[
            CrossColourCandidate,
            ...,
        ],
    ) -> None:
        if not remaining:
            identifiers = tuple(
                sorted(
                    cross_colour_candidate_identifier(
                        candidate
                    )
                    for candidate in selected
                )
            )

            if identifiers in matching_keys:
                return

            matching_keys.add(identifiers)

            results.append(
                CrossColourMatching(
                    candidates=tuple(
                        sorted(
                            selected,
                            key=(
                                cross_colour_candidate_identifier
                            ),
                        )
                    ),
                    total_distance=float(
                        sum(
                            candidate.distance
                            for candidate in selected
                        )
                    ),
                    total_score=float(
                        sum(
                            candidate.score
                            for candidate in selected
                        )
                    ),
                    maximum_edge_score=float(
                        max(
                            candidate.score
                            for candidate in selected
                        )
                    ),
                )
            )

            return

        first = min(
            remaining,
            key=_endpoint_sort_key,
        )

        for candidate in incident[first]:
            endpoint_a, endpoint_b = (
                candidate_endpoint_keys(candidate)
            )

            other = (
                endpoint_b
                if endpoint_a == first
                else endpoint_a
            )

            if other not in remaining:
                continue

            recurse(
                remaining - {first, other},
                selected + (candidate,),
            )

    recurse(
        frozenset(endpoints),
        (),
    )

    results.sort(
        key=lambda matching: (
            matching.total_score,
            matching.maximum_edge_score,
            matching.total_distance,
            tuple(
                cross_colour_candidate_identifier(
                    candidate
                )
                for candidate in matching.candidates
            ),
        )
    )

    return tuple(results)


def validate_cross_colour_review_rows(
    rows: Iterable[Mapping[str, Any]],
) -> None:
    """Validate manual cross-colour endpoint-review records."""
    identifiers: set[str] = set()

    for row in rows:
        identifier = str(row["candidate_id"])

        if identifier in identifiers:
            raise ValueError(
                f"Duplicate candidate identifier: {identifier}"
            )

        identifiers.add(identifier)

        layer_a = str(row["layer_a"])
        layer_b = str(row["layer_b"])

        if layer_a not in LAYER_ORDER:
            raise ValueError(
                f"{identifier}: invalid layer {layer_a!r}."
            )

        if layer_b not in LAYER_ORDER:
            raise ValueError(
                f"{identifier}: invalid layer {layer_b!r}."
            )

        if layer_a == layer_b:
            raise ValueError(
                f"{identifier}: layers must differ."
            )

        status = str(row.get("status", ""))
        confidence = str(row.get("confidence", ""))
        reason_code = str(row.get("reason_code", ""))

        if status not in VALID_STATUSES:
            raise ValueError(
                f"{identifier}: invalid status {status!r}."
            )

        if confidence not in VALID_CONFIDENCES:
            raise ValueError(
                f"{identifier}: invalid confidence "
                f"{confidence!r}."
            )

        if reason_code not in VALID_REASON_CODES:
            raise ValueError(
                f"{identifier}: invalid reason code "
                f"{reason_code!r}."
            )
