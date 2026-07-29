"""Enumeration of endpoint perfect matchings and reviewed exact ties."""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from dataclasses import dataclass

from meru_geometry.gauss_visits import CrossingVisit


Node = tuple[str, int, str]


@dataclass(frozen=True)
class EndpointPerfectMatching:
    """One perfect matching of the available endpoint graph."""

    matching_id: str
    candidate_ids: tuple[str, ...]
    endpoint_count: int
    total_score: float
    total_distance_px: float
    maximum_distance_px: float
    accepted_edge_count: int


def endpoint_pair(
    row: Mapping[str, object],
) -> tuple[Node, Node]:
    """Return the two endpoint nodes represented by one candidate."""
    node_a = (
        str(row["layer_a"]),
        int(row["segment_a"]),
        str(row["endpoint_a"]),
    )

    node_b = (
        str(row["layer_b"]),
        int(row["segment_b"]),
        str(row["endpoint_b"]),
    )

    if node_a == node_b:
        raise ValueError(
            f"{row['candidate_id']}: self-edge is not allowed."
        )

    for node in (node_a, node_b):
        if node[2] not in {
            "start",
            "end",
        }:
            raise ValueError(
                f"{row['candidate_id']}: invalid endpoint {node[2]!r}."
            )

    return node_a, node_b


def enumerate_endpoint_perfect_matchings(
    candidate_rows: Iterable[
        Mapping[str, object]
    ],
) -> tuple[EndpointPerfectMatching, ...]:
    """Enumerate every exact endpoint-covering candidate matching."""
    rows = [
        dict(row)
        for row in candidate_rows
    ]

    if not rows:
        raise ValueError(
            "At least one endpoint candidate is required."
        )

    row_by_identifier: dict[
        str,
        dict[str, object],
    ] = {}

    edge_nodes: dict[
        str,
        tuple[Node, Node],
    ] = {}

    all_nodes: set[Node] = set()

    for row in rows:
        identifier = str(
            row["candidate_id"]
        )

        if identifier in row_by_identifier:
            raise ValueError(
                f"Duplicate candidate identifier: {identifier}"
            )

        nodes = endpoint_pair(row)

        row_by_identifier[
            identifier
        ] = row

        edge_nodes[
            identifier
        ] = nodes

        all_nodes.update(nodes)

    if len(all_nodes) % 2:
        raise ValueError(
            "A perfect matching requires an even number of endpoints."
        )

    incident: dict[
        Node,
        list[str],
    ] = {
        node: []
        for node in all_nodes
    }

    for identifier, (
        node_a,
        node_b,
    ) in edge_nodes.items():
        incident[node_a].append(
            identifier
        )

        incident[node_b].append(
            identifier
        )

    for identifiers in incident.values():
        identifiers.sort()

    signatures: set[
        tuple[str, ...]
    ] = set()

    def recurse(
        remaining: frozenset[Node],
        selected: tuple[str, ...],
    ) -> None:
        if not remaining:
            signatures.add(
                tuple(
                    sorted(selected)
                )
            )
            return

        first = min(remaining)

        for identifier in incident[first]:
            node_a, node_b = edge_nodes[
                identifier
            ]

            other = (
                node_b
                if node_a == first
                else node_a
            )

            if other not in remaining:
                continue

            recurse(
                remaining
                - {
                    first,
                    other,
                },
                selected
                + (
                    identifier,
                ),
            )

    recurse(
        frozenset(all_nodes),
        (),
    )

    raw_results = []

    for signature in signatures:
        selected_rows = [
            row_by_identifier[
                identifier
            ]
            for identifier in signature
        ]

        raw_results.append(
            {
                "candidate_ids": signature,
                "endpoint_count": len(
                    all_nodes
                ),
                "total_score": sum(
                    float(row["score"])
                    for row in selected_rows
                ),
                "total_distance_px": sum(
                    float(row["distance_px"])
                    for row in selected_rows
                ),
                "maximum_distance_px": max(
                    float(row["distance_px"])
                    for row in selected_rows
                ),
                "accepted_edge_count": sum(
                    str(row.get("status", ""))
                    == "accepted"
                    for row in selected_rows
                ),
            }
        )

    raw_results.sort(
        key=lambda result: (
            result["total_score"],
            result["total_distance_px"],
            result["candidate_ids"],
        )
    )

    return tuple(
        EndpointPerfectMatching(
            matching_id=(
                f"M{index:02d}"
            ),
            candidate_ids=result[
                "candidate_ids"
            ],
            endpoint_count=int(
                result["endpoint_count"]
            ),
            total_score=float(
                result["total_score"]
            ),
            total_distance_px=float(
                result["total_distance_px"]
            ),
            maximum_distance_px=float(
                result["maximum_distance_px"]
            ),
            accepted_edge_count=int(
                result["accepted_edge_count"]
            ),
        )
        for index, result in enumerate(
            raw_results,
            start=1,
        )
    )


def _parse_bool(
    value: object,
) -> bool:
    """Parse one tracked CSV Boolean value."""
    text = str(value).strip()

    if text == "True":
        return True

    if text == "False":
        return False

    raise ValueError(
        f"Invalid Boolean value: {value!r}"
    )


def apply_exact_tie_reviews(
    visits: Iterable[CrossingVisit],
    review_rows: Iterable[
        Mapping[str, object]
    ],
    tolerance: float = 1.0e-12,
) -> tuple[CrossingVisit, ...]:
    """Apply source order to exact ties under any traversal direction.

    The accepted order is first converted back to source-forward order.
    It is then reversed when the candidate cycle traverses that visible
    segment backwards.
    """
    ordered = list(visits)

    token_to_visit = {
        visit.token: visit
        for visit in ordered
    }

    if len(token_to_visit) != len(ordered):
        raise ValueError(
            "Gauss-visit tokens must be unique."
        )

    for row in review_rows:
        if str(
            row.get(
                "review_kind",
                "",
            )
        ) != "exact_tie":
            continue

        review_id = str(
            row["review_id"]
        )

        if str(row["status"]) != "accepted":
            raise ValueError(
                f"{review_id}: exact tie is not accepted."
            )

        accepted_first = str(
            row["accepted_first"]
        )

        accepted_second = str(
            row["accepted_second"]
        )

        if (
            accepted_first not in token_to_visit
            or accepted_second not in token_to_visit
        ):
            raise ValueError(
                f"{review_id}: reviewed visits are absent."
            )

        first_visit = token_to_visit[
            accepted_first
        ]

        second_visit = token_to_visit[
            accepted_second
        ]

        if (
            first_visit.segment_key
            != second_visit.segment_key
        ):
            raise ValueError(
                f"{review_id}: visits are not on one segment."
            )

        if (
            abs(
                first_visit.source_fraction
                - second_visit.source_fraction
            )
            > tolerance
        ):
            raise ValueError(
                f"{review_id}: reviewed pair is not an exact tie."
            )

        if (
            first_visit.traversal_forward
            != second_visit.traversal_forward
        ):
            raise ValueError(
                f"{review_id}: inconsistent candidate directions."
            )

        reference_forward = _parse_bool(
            row["traversal_forward"]
        )

        source_first = (
            accepted_first
            if reference_forward
            else accepted_second
        )

        source_second = (
            accepted_second
            if reference_forward
            else accepted_first
        )

        candidate_forward = (
            first_visit.traversal_forward
        )

        desired_first = (
            source_first
            if candidate_forward
            else source_second
        )

        desired_second = (
            source_second
            if candidate_forward
            else source_first
        )

        first_index = next(
            index
            for index, visit in enumerate(
                ordered
            )
            if visit.token == desired_first
        )

        second_index = next(
            index
            for index, visit in enumerate(
                ordered
            )
            if visit.token == desired_second
        )

        if abs(
            first_index
            - second_index
        ) != 1:
            raise ValueError(
                f"{review_id}: tied visits are not consecutive."
            )

        if first_index > second_index:
            ordered[
                first_index
            ], ordered[
                second_index
            ] = (
                ordered[second_index],
                ordered[first_index],
            )

    return tuple(ordered)
