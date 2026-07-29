"""Signed O/U Gauss words for oriented planar knot diagrams."""

from __future__ import annotations

from collections import Counter, defaultdict
from collections.abc import Iterable, Mapping
from dataclasses import dataclass


@dataclass(frozen=True)
class SignedGaussVisit:
    """One ordered O/U visit carrying its event crossing sign."""

    order: int
    event_id: str
    role: str
    crossing_sign: int
    candidate_id: str

    @property
    def unsigned_token(self) -> str:
        """Return the event and O/U visit token."""
        return f"{self.event_id}{self.role}"

    @property
    def event_token(self) -> str:
        """Return the event label with its oriented sign."""
        suffix = "+" if self.crossing_sign > 0 else "-"
        return f"{self.event_id}{suffix}"

    @property
    def signed_token(self) -> str:
        """Return the complete signed O/U visit token."""
        suffix = "+" if self.crossing_sign > 0 else "-"
        return f"{self.event_id}{self.role}{suffix}"


def validate_signed_gauss_visits(
    visits: Iterable[SignedGaussVisit],
    expected_event_count: int | None = None,
) -> None:
    """Validate one complete ordered signed O/U Gauss word."""
    ordered = tuple(visits)

    if not ordered:
        raise ValueError(
            "A signed Gauss word must contain at least one visit."
        )

    orders = [
        visit.order
        for visit in ordered
    ]

    if orders != list(
        range(1, len(ordered) + 1)
    ):
        raise ValueError(
            "Signed Gauss visit orders must be contiguous from one."
        )

    by_event: dict[
        str,
        list[SignedGaussVisit],
    ] = defaultdict(list)

    for visit in ordered:
        if visit.role not in {"O", "U"}:
            raise ValueError(
                f"{visit.event_id}: invalid visit role "
                f"{visit.role!r}."
            )

        if visit.crossing_sign not in {-1, 1}:
            raise ValueError(
                f"{visit.event_id}: crossing sign must be -1 or +1."
            )

        by_event[visit.event_id].append(
            visit
        )

    if (
        expected_event_count is not None
        and len(by_event) != expected_event_count
    ):
        raise ValueError(
            f"Expected {expected_event_count} crossing events; "
            f"found {len(by_event)}."
        )

    for event_id, event_visits in by_event.items():
        if len(event_visits) != 2:
            raise ValueError(
                f"{event_id}: expected exactly two visits."
            )

        roles = Counter(
            visit.role
            for visit in event_visits
        )

        if roles != Counter(
            {
                "O": 1,
                "U": 1,
            }
        ):
            raise ValueError(
                f"{event_id}: expected one O and one U visit."
            )

        signs = {
            visit.crossing_sign
            for visit in event_visits
        }

        if len(signs) != 1:
            raise ValueError(
                f"{event_id}: its two visits carry "
                "different crossing signs."
            )


    signed_tokens = [
        visit.signed_token
        for visit in ordered
    ]

    if len(set(signed_tokens)) != len(signed_tokens):
        raise ValueError(
            "Signed Gauss visit tokens must be unique."
        )


def build_signed_gauss_visits(
    gauss_rows: Iterable[Mapping[str, object]],
    event_signs: Mapping[str, int],
) -> tuple[SignedGaussVisit, ...]:
    """Attach one oriented event sign to every frozen O/U visit."""
    rows = sorted(
        (
            dict(row)
            for row in gauss_rows
        ),
        key=lambda row: int(row["order"]),
    )

    visits: list[SignedGaussVisit] = []

    for expected_order, row in enumerate(
        rows,
        start=1,
    ):
        order = int(row["order"])

        if order != expected_order:
            raise ValueError(
                "Gauss-word orders must be contiguous from one."
            )

        event_id = str(
            row["event_id"]
        ).strip()

        role = str(
            row["role"]
        ).strip()

        unsigned_token = f"{event_id}{role}"

        recorded_token = str(
            row.get("token", unsigned_token)
        ).strip()

        if recorded_token != unsigned_token:
            raise ValueError(
                f"Order {order}: recorded token "
                f"{recorded_token!r} does not match "
                f"{unsigned_token!r}."
            )

        if event_id not in event_signs:
            raise ValueError(
                f"Missing oriented sign for event {event_id}."
            )

        sign = int(
            event_signs[event_id]
        )

        if sign not in {-1, 1}:
            raise ValueError(
                f"{event_id}: crossing sign must be -1 or +1."
            )

        visits.append(
            SignedGaussVisit(
                order=order,
                event_id=event_id,
                role=role,
                crossing_sign=sign,
                candidate_id=str(
                    row["candidate_id"]
                ),
            )
        )

    represented_events = {
        visit.event_id
        for visit in visits
    }

    unused_signs = (
        set(event_signs)
        - represented_events
    )

    if unused_signs:
        raise ValueError(
            "Signs were supplied for events absent from the "
            "Gauss word: "
            + ", ".join(sorted(unused_signs))
        )

    result = tuple(visits)

    validate_signed_gauss_visits(
        result,
        expected_event_count=len(
            event_signs
        ),
    )

    return result
