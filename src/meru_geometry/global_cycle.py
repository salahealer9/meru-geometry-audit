"""Global cycle audit for source-derived coloured trace fragments."""

from __future__ import annotations

from collections import Counter, deque
from collections.abc import Iterable, Mapping
from dataclasses import dataclass


Node = tuple[str, int, str]

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
class GlobalEdge:
    """One visible or adjudicated edge in the endpoint graph."""

    kind: str
    identifier: str
    node_a: Node
    node_b: Node


@dataclass(frozen=True)
class SegmentVisit:
    """One visible segment encountered during cycle traversal."""

    layer: str
    segment_id: int
    forward: bool


@dataclass(frozen=True)
class GlobalCycleAudit:
    """Complete invariant summary for the global endpoint graph."""

    visible_segment_count: int
    same_colour_connection_count: int
    cross_colour_transition_count: int
    vertex_count: int
    edge_count: int
    component_count: int
    degree_counts: tuple[tuple[int, int], ...]
    edges: tuple[GlobalEdge, ...]
    segment_traversal: tuple[SegmentVisit, ...]
    cross_colour_transitions: tuple[str, ...]
    is_single_cycle: bool

    @property
    def degree_map(self) -> dict[int, int]:
        """Return vertex-degree counts as a dictionary."""
        return dict(self.degree_counts)


def format_segment_visit(
    visit: SegmentVisit,
) -> str:
    """Format a traversal visit using source segment notation."""
    orientation = "+" if visit.forward else "−"

    return (
        f"{LAYER_CODE[visit.layer]}:"
        f"S{visit.segment_id:02d}"
        f"{orientation}"
    )


def _node_sort_key(
    node: Node,
) -> tuple[int, int, int]:
    """Return a deterministic endpoint ordering."""
    layer, segment_id, endpoint = node

    return (
        LAYER_ORDER[layer],
        segment_id,
        0 if endpoint == "start" else 1,
    )


def _validate_node(
    node: Node,
) -> None:
    """Validate one layer-qualified segment endpoint."""
    layer, segment_id, endpoint = node

    if layer not in LAYER_ORDER:
        raise ValueError(f"Unsupported layer: {layer}")

    if segment_id < 1:
        raise ValueError(
            "Segment identifiers must be positive."
        )

    if endpoint not in {"start", "end"}:
        raise ValueError(
            "Endpoint must be 'start' or 'end'."
        )


def audit_global_cycle(
    segment_ids: Mapping[str, Iterable[int]],
    same_colour_connections: Iterable[
        Mapping[str, object]
    ],
    cross_colour_connections: Iterable[
        Mapping[str, object]
    ],
    start: Node = ("red", 1, "start"),
) -> GlobalCycleAudit:
    """Build and audit the complete coloured endpoint graph."""
    adjacency: dict[
        Node,
        list[tuple[Node, tuple[str, str]]],
    ] = {}

    edge_by_key: dict[
        tuple[str, str],
        GlobalEdge,
    ] = {}

    def add_edge(
        kind: str,
        identifier: str,
        node_a: Node,
        node_b: Node,
    ) -> None:
        _validate_node(node_a)
        _validate_node(node_b)

        if node_a == node_b:
            raise ValueError(
                f"{identifier}: self-edge is not allowed."
            )

        key = (kind, identifier)

        if key in edge_by_key:
            raise ValueError(
                f"Duplicate graph edge: {key}"
            )

        if node_a not in adjacency:
            raise ValueError(
                f"{identifier}: unknown endpoint {node_a}."
            )

        if node_b not in adjacency:
            raise ValueError(
                f"{identifier}: unknown endpoint {node_b}."
            )

        edge = GlobalEdge(
            kind=kind,
            identifier=identifier,
            node_a=node_a,
            node_b=node_b,
        )

        edge_by_key[key] = edge
        adjacency[node_a].append((node_b, key))
        adjacency[node_b].append((node_a, key))

    normalized_segment_ids: dict[
        str,
        tuple[int, ...],
    ] = {}

    for layer in LAYER_ORDER:
        identifiers = tuple(
            sorted(
                {
                    int(value)
                    for value in segment_ids.get(
                        layer,
                        (),
                    )
                }
            )
        )

        if any(
            identifier < 1
            for identifier in identifiers
        ):
            raise ValueError(
                "Segment identifiers must be positive."
            )

        normalized_segment_ids[layer] = identifiers

        for segment_id in identifiers:
            start_node = (
                layer,
                segment_id,
                "start",
            )

            end_node = (
                layer,
                segment_id,
                "end",
            )

            adjacency[start_node] = []
            adjacency[end_node] = []

    for layer in LAYER_ORDER:
        for segment_id in normalized_segment_ids[layer]:
            add_edge(
                "visible_segment",
                f"{layer}_S{segment_id:02d}",
                (
                    layer,
                    segment_id,
                    "start",
                ),
                (
                    layer,
                    segment_id,
                    "end",
                ),
            )

    same_colour_count = 0

    for row in same_colour_connections:
        layer = str(row["layer"])

        add_edge(
            "same_colour",
            str(row["candidate_id"]),
            (
                layer,
                int(row["segment_a"]),
                str(row["endpoint_a"]),
            ),
            (
                layer,
                int(row["segment_b"]),
                str(row["endpoint_b"]),
            ),
        )

        same_colour_count += 1

    cross_colour_count = 0

    for row in cross_colour_connections:
        add_edge(
            "cross_colour",
            str(row["candidate_id"]),
            (
                str(row["layer_a"]),
                int(row["segment_a"]),
                str(row["endpoint_a"]),
            ),
            (
                str(row["layer_b"]),
                int(row["segment_b"]),
                str(row["endpoint_b"]),
            ),
        )

        cross_colour_count += 1

    vertices = set(adjacency)

    degree_counter = Counter(
        len(adjacency[node])
        for node in vertices
    )

    unseen = set(vertices)
    component_count = 0

    while unseen:
        component_count += 1

        root = min(
            unseen,
            key=_node_sort_key,
        )

        queue: deque[Node] = deque([root])
        visited: set[Node] = set()

        while queue:
            current = queue.popleft()

            if current in visited:
                continue

            visited.add(current)

            for neighbour, _key in adjacency[current]:
                if neighbour not in visited:
                    queue.append(neighbour)

        unseen -= visited

    is_single_cycle = (
        bool(vertices)
        and component_count == 1
        and len(edge_by_key) == len(vertices)
        and degree_counter == Counter(
            {2: len(vertices)}
        )
    )

    segment_traversal: list[SegmentVisit] = []
    transition_traversal: list[str] = []

    if is_single_cycle:
        _validate_node(start)

        if start not in adjacency:
            raise ValueError(
                f"Traversal start is absent: {start}"
            )

        current = start
        used_edges: set[tuple[str, str]] = set()

        kind_order = {
            "visible_segment": 0,
            "same_colour": 1,
            "cross_colour": 2,
        }

        while len(used_edges) < len(edge_by_key):
            available = [
                (neighbour, key)
                for neighbour, key
                in adjacency[current]
                if key not in used_edges
            ]

            if not available:
                raise RuntimeError(
                    "Cycle traversal terminated early."
                )

            available.sort(
                key=lambda item: (
                    kind_order[item[1][0]],
                    item[1],
                    _node_sort_key(item[0]),
                )
            )

            neighbour, key = available[0]
            used_edges.add(key)

            kind, identifier = key

            if kind == "visible_segment":
                layer, segment_id, endpoint = current

                segment_traversal.append(
                    SegmentVisit(
                        layer=layer,
                        segment_id=segment_id,
                        forward=(
                            endpoint == "start"
                        ),
                    )
                )

            elif kind == "cross_colour":
                transition_traversal.append(
                    identifier
                )

            current = neighbour

        if current != start:
            raise RuntimeError(
                "Traversal used every edge but did not "
                "return to its starting endpoint."
            )

    visible_segment_count = sum(
        len(identifiers)
        for identifiers
        in normalized_segment_ids.values()
    )

    edges = tuple(
        sorted(
            edge_by_key.values(),
            key=lambda edge: (
                edge.kind,
                edge.identifier,
            ),
        )
    )

    return GlobalCycleAudit(
        visible_segment_count=visible_segment_count,
        same_colour_connection_count=(
            same_colour_count
        ),
        cross_colour_transition_count=(
            cross_colour_count
        ),
        vertex_count=len(vertices),
        edge_count=len(edges),
        component_count=component_count,
        degree_counts=tuple(
            sorted(degree_counter.items())
        ),
        edges=edges,
        segment_traversal=tuple(
            segment_traversal
        ),
        cross_colour_transitions=tuple(
            transition_traversal
        ),
        is_single_cycle=is_single_cycle,
    )
