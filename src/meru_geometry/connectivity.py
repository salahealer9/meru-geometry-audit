"""Connectivity analysis for adjudicated visible trace fragments."""

from __future__ import annotations

from collections import deque
from collections.abc import Iterable, Mapping
from dataclasses import dataclass


Endpoint = tuple[int, str]
EdgeKey = tuple[str, str]


@dataclass(frozen=True)
class SegmentTraversal:
    """One segment encountered during a component traversal."""

    segment_id: int
    forward: bool
    entry_endpoint: str
    exit_endpoint: str


@dataclass(frozen=True)
class ConnectivityComponent:
    """One connected component of visible and accepted hidden edges."""

    segment_ids: tuple[int, ...]
    accepted_connection_ids: tuple[str, ...]
    free_endpoints: tuple[Endpoint, ...]
    closed: bool
    branched: bool
    traversal: tuple[SegmentTraversal, ...]


def format_endpoint(endpoint: Endpoint) -> str:
    """Format an endpoint using one-based segment notation."""
    segment_id, endpoint_name = endpoint
    suffix = "S" if endpoint_name == "start" else "E"
    return f"S{segment_id:02d}{suffix}"


def _validate_endpoint(endpoint: Endpoint) -> None:
    """Validate a segment endpoint."""
    segment_id, endpoint_name = endpoint

    if segment_id < 1:
        raise ValueError("segment identifiers must be positive.")

    if endpoint_name not in {"start", "end"}:
        raise ValueError(
            "endpoint names must be 'start' or 'end'."
        )


def _endpoint_sort_key(endpoint: Endpoint) -> tuple[int, int]:
    """Return a deterministic endpoint ordering."""
    segment_id, endpoint_name = endpoint
    return (
        segment_id,
        0 if endpoint_name == "start" else 1,
    )


def build_endpoint_connectivity(
    segment_ids: Iterable[int],
    accepted_connections: Iterable[Mapping[str, object]],
) -> tuple[ConnectivityComponent, ...]:
    """Build connectivity components from accepted endpoint pairings.

    Every visible segment contributes an intrinsic edge between its start and
    end endpoints. Every accepted adjudication contributes one hidden or
    occluded connection edge.

    An endpoint may participate in no more than one accepted connection.
    """
    identifiers = tuple(sorted(set(int(value) for value in segment_ids)))

    if not identifiers:
        return ()

    if any(identifier < 1 for identifier in identifiers):
        raise ValueError("segment identifiers must be positive.")

    adjacency: dict[
        Endpoint,
        list[tuple[Endpoint, EdgeKey]],
    ] = {}

    edges: dict[
        EdgeKey,
        tuple[Endpoint, Endpoint],
    ] = {}

    edge_kind: dict[EdgeKey, str] = {}

    for segment_id in identifiers:
        start = (segment_id, "start")
        end = (segment_id, "end")

        adjacency[start] = []
        adjacency[end] = []

        key = ("segment", f"S{segment_id:02d}")
        edges[key] = (start, end)
        edge_kind[key] = "segment"

        adjacency[start].append((end, key))
        adjacency[end].append((start, key))

    used_connection_endpoints: set[Endpoint] = set()
    connection_identifiers: set[str] = set()

    for row in accepted_connections:
        candidate_id = str(row["candidate_id"])

        if candidate_id in connection_identifiers:
            raise ValueError(
                f"Duplicate accepted connection: {candidate_id}"
            )

        connection_identifiers.add(candidate_id)

        endpoint_a = (
            int(row["segment_a"]),
            str(row["endpoint_a"]),
        )

        endpoint_b = (
            int(row["segment_b"]),
            str(row["endpoint_b"]),
        )

        _validate_endpoint(endpoint_a)
        _validate_endpoint(endpoint_b)

        if endpoint_a not in adjacency:
            raise ValueError(
                f"{candidate_id}: unknown endpoint "
                f"{format_endpoint(endpoint_a)}."
            )

        if endpoint_b not in adjacency:
            raise ValueError(
                f"{candidate_id}: unknown endpoint "
                f"{format_endpoint(endpoint_b)}."
            )

        if endpoint_a[0] == endpoint_b[0]:
            raise ValueError(
                f"{candidate_id}: a segment cannot connect to itself."
            )

        for endpoint in (endpoint_a, endpoint_b):
            if endpoint in used_connection_endpoints:
                raise ValueError(
                    f"{candidate_id}: endpoint "
                    f"{format_endpoint(endpoint)} is already connected."
                )

            used_connection_endpoints.add(endpoint)

        key = ("connection", candidate_id)
        edges[key] = (endpoint_a, endpoint_b)
        edge_kind[key] = "connection"

        adjacency[endpoint_a].append((endpoint_b, key))
        adjacency[endpoint_b].append((endpoint_a, key))

    unseen = set(adjacency)
    components: list[ConnectivityComponent] = []

    while unseen:
        root = min(unseen, key=_endpoint_sort_key)

        queue: deque[Endpoint] = deque([root])
        component_nodes: set[Endpoint] = set()

        while queue:
            current = queue.popleft()

            if current in component_nodes:
                continue

            component_nodes.add(current)

            for neighbour, _edge_key in adjacency[current]:
                if neighbour not in component_nodes:
                    queue.append(neighbour)

        unseen -= component_nodes

        component_edge_keys = {
            edge_key
            for node in component_nodes
            for _neighbour, edge_key in adjacency[node]
        }

        component_segment_ids = tuple(
            sorted(
                {
                    node[0]
                    for node in component_nodes
                }
            )
        )

        accepted_ids = tuple(
            sorted(
                key[1]
                for key in component_edge_keys
                if edge_kind[key] == "connection"
            )
        )

        free_endpoints = tuple(
            sorted(
                (
                    node
                    for node in component_nodes
                    if len(adjacency[node]) == 1
                ),
                key=_endpoint_sort_key,
            )
        )

        branched = any(
            len(adjacency[node]) > 2
            for node in component_nodes
        )

        closed = (
            bool(component_nodes)
            and not branched
            and all(
                len(adjacency[node]) == 2
                for node in component_nodes
            )
        )

        traversal: list[SegmentTraversal] = []

        if not branched:
            start_node = (
                free_endpoints[0]
                if free_endpoints
                else min(
                    component_nodes,
                    key=_endpoint_sort_key,
                )
            )

            current = start_node
            used_edges: set[EdgeKey] = set()

            while True:
                available = [
                    (neighbour, edge_key)
                    for neighbour, edge_key in adjacency[current]
                    if edge_key not in used_edges
                ]

                if not available:
                    break

                available.sort(
                    key=lambda item: (
                        0
                        if edge_kind[item[1]] == "segment"
                        else 1,
                        item[1],
                        _endpoint_sort_key(item[0]),
                    )
                )

                neighbour, edge_key = available[0]
                used_edges.add(edge_key)

                if edge_kind[edge_key] == "segment":
                    forward = current[1] == "start"

                    traversal.append(
                        SegmentTraversal(
                            segment_id=current[0],
                            forward=forward,
                            entry_endpoint=current[1],
                            exit_endpoint=neighbour[1],
                        )
                    )

                current = neighbour

                if (
                    closed
                    and current == start_node
                    and len(used_edges) == len(component_edge_keys)
                ):
                    break

            if used_edges != component_edge_keys:
                raise RuntimeError(
                    "A non-branched component could not be "
                    "traversed completely."
                )

        components.append(
            ConnectivityComponent(
                segment_ids=component_segment_ids,
                accepted_connection_ids=accepted_ids,
                free_endpoints=free_endpoints,
                closed=closed,
                branched=branched,
                traversal=tuple(traversal),
            )
        )

    components.sort(
        key=lambda component: component.segment_ids
    )

    return tuple(components)
