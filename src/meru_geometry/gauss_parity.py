"""Necessary Gauss-parity checks for classical planar knot diagrams."""

from __future__ import annotations

from collections import Counter, defaultdict
from collections.abc import Iterable, Mapping
from dataclasses import dataclass


@dataclass(frozen=True)
class GaussParityEvent:
    """Parity and interlacement data for one crossing event."""

    event_id: str
    first_order: int
    second_order: int
    first_role: str
    second_role: str
    visits_between: int
    interlacement_degree: int
    passes_even_condition: bool

    @property
    def opposite_position_parity(self) -> bool:
        """Return whether the two visits occupy opposite parities."""
        return (
            self.first_order % 2
            != self.second_order % 2
        )

    @property
    def interlacement_degree_even(self) -> bool:
        """Return whether the chord has even interlacement degree."""
        return (
            self.interlacement_degree % 2
            == 0
        )


@dataclass(frozen=True)
class GaussParityAudit:
    """Complete necessary-parity audit of one Gauss word."""

    visit_count: int
    events: tuple[GaussParityEvent, ...]

    @property
    def event_count(self) -> int:
        """Return the number of distinct crossing events."""
        return len(self.events)

    @property
    def violating_events(
        self,
    ) -> tuple[GaussParityEvent, ...]:
        """Return events failing the classical even condition."""
        return tuple(
            event
            for event in self.events
            if not event.passes_even_condition
        )

    @property
    def passing_events(
        self,
    ) -> tuple[GaussParityEvent, ...]:
        """Return events satisfying the necessary even condition."""
        return tuple(
            event
            for event in self.events
            if event.passes_even_condition
        )

    @property
    def violation_count(self) -> int:
        """Return the number of parity violations."""
        return len(self.violating_events)

    @property
    def passes_even_condition(self) -> bool:
        """Return whether every event passes the necessary condition."""
        return self.violation_count == 0


def _event_interlaces(
    first_a: int,
    second_a: int,
    first_b: int,
    second_b: int,
) -> bool:
    """Return whether two Gauss chords have alternating endpoints."""
    return (
        first_a
        < first_b
        < second_a
        < second_b
    ) or (
        first_b
        < first_a
        < second_b
        < second_a
    )


def audit_gauss_parity(
    rows: Iterable[Mapping[str, object]],
) -> GaussParityAudit:
    """Audit the necessary even condition for a Gauss word.

    For a classical one-component planar immersion, the two
    occurrences of every crossing must have an even number of visits
    between them. Equivalently, they occupy opposite position
    parities and their chord has even interlacement degree.
    """
    ordered_rows = sorted(
        (
            dict(row)
            for row in rows
        ),
        key=lambda row: int(row["order"]),
    )

    if not ordered_rows:
        raise ValueError(
            "A Gauss word must contain at least one visit."
        )

    orders = [
        int(row["order"])
        for row in ordered_rows
    ]

    if orders != list(
        range(1, len(ordered_rows) + 1)
    ):
        raise ValueError(
            "Gauss-word orders must be contiguous from one."
        )

    occurrences: dict[
        str,
        list[tuple[int, str]],
    ] = defaultdict(list)

    first_seen: dict[str, int] = {}

    for row in ordered_rows:
        order = int(row["order"])
        event_id = str(
            row["event_id"]
        ).strip()

        role = str(
            row["role"]
        ).strip()

        if not event_id:
            raise ValueError(
                f"Order {order}: event_id is blank."
            )

        if role not in {
            "O",
            "U",
        }:
            raise ValueError(
                f"{event_id}: invalid role {role!r}."
            )

        first_seen.setdefault(
            event_id,
            order,
        )

        occurrences[event_id].append(
            (
                order,
                role,
            )
        )

    positions: dict[
        str,
        tuple[int, int],
    ] = {}

    roles: dict[
        str,
        tuple[str, str],
    ] = {}

    for event_id, event_visits in occurrences.items():
        if len(event_visits) != 2:
            raise ValueError(
                f"{event_id}: expected exactly two visits; "
                f"found {len(event_visits)}."
            )

        event_visits.sort(
            key=lambda visit: visit[0]
        )

        event_roles = Counter(
            role
            for _order, role in event_visits
        )

        if event_roles != Counter(
            {
                "O": 1,
                "U": 1,
            }
        ):
            raise ValueError(
                f"{event_id}: expected one O and one U visit."
            )

        positions[event_id] = (
            event_visits[0][0],
            event_visits[1][0],
        )

        roles[event_id] = (
            event_visits[0][1],
            event_visits[1][1],
        )

    event_ids = sorted(
        occurrences,
        key=lambda event_id: first_seen[event_id],
    )

    events: list[
        GaussParityEvent
    ] = []

    for event_id in event_ids:
        first_order, second_order = positions[
            event_id
        ]

        first_role, second_role = roles[
            event_id
        ]

        visits_between = (
            second_order
            - first_order
            - 1
        )

        interlacement_degree = sum(
            _event_interlaces(
                first_order,
                second_order,
                positions[other_id][0],
                positions[other_id][1],
            )
            for other_id in event_ids
            if other_id != event_id
        )

        passes = (
            visits_between % 2
            == 0
        )

        opposite_position_parity = (
            first_order % 2
            != second_order % 2
        )

        degree_even = (
            interlacement_degree % 2
            == 0
        )

        if not (
            passes
            == opposite_position_parity
            == degree_even
        ):
            raise RuntimeError(
                f"{event_id}: equivalent parity diagnostics "
                "disagree."
            )

        events.append(
            GaussParityEvent(
                event_id=event_id,
                first_order=first_order,
                second_order=second_order,
                first_role=first_role,
                second_role=second_role,
                visits_between=visits_between,
                interlacement_degree=(
                    interlacement_degree
                ),
                passes_even_condition=passes,
            )
        )

    return GaussParityAudit(
        visit_count=len(ordered_rows),
        events=tuple(events),
    )


def validate_classical_even_condition(
    audit: GaussParityAudit,
) -> None:
    """Reject a Gauss word failing the necessary even condition."""
    if audit.passes_even_condition:
        return

    identifiers = ", ".join(
        event.event_id
        for event in audit.violating_events
    )

    raise ValueError(
        "Classical Gauss even condition failed for "
        f"{audit.violation_count} events: {identifiers}"
    )
