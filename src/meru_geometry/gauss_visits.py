"""Ordered crossing visits along a frozen global-cycle traversal."""

from __future__ import annotations

from collections import Counter, defaultdict
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass

import numpy as np
from numpy.typing import ArrayLike, NDArray

from meru_geometry.global_cycle import SegmentVisit


SegmentKey = tuple[str, int]


@dataclass(frozen=True)
class CrossingVisit:
    """One traversal visit to one crossing event."""

    event_id: str
    role: str
    candidate_id: str
    layer: str
    segment_id: int
    traversal_forward: bool
    segment_order: int
    source_fraction: float
    traversal_fraction: float
    global_position: float
    panel_x: float
    panel_y: float

    @property
    def segment_key(self) -> SegmentKey:
        """Return the layer-qualified segment identifier."""
        return self.layer, self.segment_id

    @property
    def token(self) -> str:
        """Return compact Gauss-visit notation."""
        return f"{self.event_id}{self.role}"


@dataclass(frozen=True)
class VisitOrderPair:
    """Two consecutive visits requiring an ordering check."""

    first: CrossingVisit
    second: CrossingVisit
    gap_fraction: float


def _validate_polyline(
    points: ArrayLike,
) -> NDArray[np.float64]:
    """Validate and return one finite planar polyline."""
    array = np.asarray(
        points,
        dtype=np.float64,
    )

    if (
        array.ndim != 2
        or array.shape[1] != 2
        or array.shape[0] < 2
    ):
        raise ValueError(
            "Polyline points must have shape (n, 2), with n >= 2."
        )

    if not np.isfinite(array).all():
        raise ValueError(
            "Polyline coordinates must be finite."
        )

    return array


def polyline_arc_fraction(
    points: ArrayLike,
    piece_index: int,
    piece_fraction: float,
) -> float:
    """Return normalized arc length at one polyline-piece position."""
    polyline = _validate_polyline(points)

    if not 0 <= piece_index < polyline.shape[0] - 1:
        raise ValueError(
            "piece_index is outside the polyline-piece range."
        )

    if not 0.0 <= piece_fraction <= 1.0:
        raise ValueError(
            "piece_fraction must lie between zero and one."
        )

    piece_lengths = np.linalg.norm(
        np.diff(polyline, axis=0),
        axis=1,
    )

    total_length = float(
        piece_lengths.sum()
    )

    if total_length <= np.finfo(np.float64).eps:
        raise ValueError(
            "Polyline must have positive total length."
        )

    distance = float(
        piece_lengths[:piece_index].sum()
        + piece_fraction
        * piece_lengths[piece_index]
    )

    return distance / total_length


def _ordered_visits(
    visits: Iterable[CrossingVisit],
) -> tuple[CrossingVisit, ...]:
    """Return deterministic traversal order."""
    return tuple(
        sorted(
            visits,
            key=lambda visit: (
                visit.segment_order,
                visit.traversal_fraction,
                visit.event_id,
                visit.role,
            ),
        )
    )


def build_crossing_visits(
    crossing_rows: Iterable[Mapping[str, object]],
    segments: Mapping[SegmentKey, ArrayLike],
    traversal: Sequence[SegmentVisit],
) -> tuple[CrossingVisit, ...]:
    """Map reviewed crossing strands onto the frozen cycle."""
    traversal_map: dict[
        SegmentKey,
        tuple[int, bool],
    ] = {}

    for segment_order, visit in enumerate(
        traversal
    ):
        key = (
            visit.layer,
            visit.segment_id,
        )

        if key in traversal_map:
            raise ValueError(
                f"Traversal repeats segment {key}."
            )

        traversal_map[key] = (
            segment_order,
            visit.forward,
        )

    visits: list[CrossingVisit] = []
    crossing_event_ids: set[str] = set()

    for row in crossing_rows:
        if str(row["status"]) != "crossing":
            continue

        event_id = str(row["event_id"]).strip()

        if not event_id:
            raise ValueError(
                "Crossing rows require an event_id."
            )

        if event_id in crossing_event_ids:
            raise ValueError(
                f"Duplicate primary crossing event: {event_id}"
            )

        crossing_event_ids.add(event_id)

        key_a = (
            str(row["layer_a"]),
            int(row["segment_a"]),
        )

        key_b = (
            str(row["layer_b"]),
            int(row["segment_b"]),
        )

        over_key = (
            str(row["over_layer"]),
            int(row["over_segment"]),
        )

        under_key = (
            str(row["under_layer"]),
            int(row["under_segment"]),
        )

        if over_key == under_key:
            raise ValueError(
                f"{event_id}: over- and under-strands must differ."
            )

        if {
            over_key,
            under_key,
        } != {
            key_a,
            key_b,
        }:
            raise ValueError(
                f"{event_id}: over-under assignment does not match "
                "the candidate segment pair."
            )

        for side, key in (
            ("a", key_a),
            ("b", key_b),
        ):
            if key not in segments:
                raise ValueError(
                    f"{event_id}: missing digitized segment {key}."
                )

            if key not in traversal_map:
                raise ValueError(
                    f"{event_id}: segment {key} is absent from "
                    "the frozen traversal."
                )

            source_fraction = polyline_arc_fraction(
                segments[key],
                int(row[f"piece_index_{side}"]),
                float(row[f"fraction_{side}"]),
            )

            (
                segment_order,
                traversal_forward,
            ) = traversal_map[key]

            traversal_fraction = (
                source_fraction
                if traversal_forward
                else 1.0 - source_fraction
            )

            role = (
                "O"
                if key == over_key
                else "U"
            )

            visits.append(
                CrossingVisit(
                    event_id=event_id,
                    role=role,
                    candidate_id=str(
                        row["candidate_id"]
                    ),
                    layer=key[0],
                    segment_id=key[1],
                    traversal_forward=(
                        traversal_forward
                    ),
                    segment_order=segment_order,
                    source_fraction=source_fraction,
                    traversal_fraction=(
                        traversal_fraction
                    ),
                    global_position=(
                        segment_order
                        + traversal_fraction
                    ),
                    panel_x=float(row["panel_x"]),
                    panel_y=float(row["panel_y"]),
                )
            )

    ordered = _ordered_visits(visits)

    by_event: dict[
        str,
        list[CrossingVisit],
    ] = defaultdict(list)

    for visit in ordered:
        by_event[visit.event_id].append(
            visit
        )

    for event_id, event_visits in by_event.items():
        if len(event_visits) != 2:
            raise ValueError(
                f"{event_id}: expected two visits; "
                f"found {len(event_visits)}."
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
                f"{event_id}: expected one over and one under visit."
            )

    return ordered


def group_visit_positions(
    visits: Iterable[CrossingVisit],
    tolerance: float = 1.0e-12,
) -> tuple[tuple[CrossingVisit, ...], ...]:
    """Group visits that share one derived traversal position."""
    if tolerance < 0.0:
        raise ValueError(
            "tolerance must be non-negative."
        )

    ordered = _ordered_visits(visits)
    groups: list[
        tuple[CrossingVisit, ...]
    ] = []

    index = 0

    while index < len(ordered):
        anchor = ordered[index]
        group = [anchor]
        cursor = index + 1

        while cursor < len(ordered):
            candidate = ordered[cursor]

            if (
                candidate.segment_order
                != anchor.segment_order
            ):
                break

            if (
                abs(
                    candidate.traversal_fraction
                    - anchor.traversal_fraction
                )
                > tolerance
            ):
                break

            group.append(candidate)
            cursor += 1

        groups.append(tuple(group))
        index = cursor

    return tuple(groups)


def find_order_ties(
    visits: Iterable[CrossingVisit],
    tolerance: float = 1.0e-12,
) -> tuple[tuple[CrossingVisit, ...], ...]:
    """Return non-singleton positional groups."""
    return tuple(
        group
        for group in group_visit_positions(
            visits,
            tolerance=tolerance,
        )
        if len(group) > 1
    )


def find_close_visit_pairs(
    visits: Iterable[CrossingVisit],
    maximum_gap: float = 0.03,
) -> tuple[VisitOrderPair, ...]:
    """Return close consecutive visits on the same visible segment."""
    if maximum_gap < 0.0:
        raise ValueError(
            "maximum_gap must be non-negative."
        )

    ordered = _ordered_visits(visits)
    pairs: list[VisitOrderPair] = []

    for first, second in zip(
        ordered,
        ordered[1:],
        strict=False,
    ):
        if (
            first.segment_order
            != second.segment_order
        ):
            continue

        gap = (
            second.traversal_fraction
            - first.traversal_fraction
        )

        if gap <= maximum_gap:
            pairs.append(
                VisitOrderPair(
                    first=first,
                    second=second,
                    gap_fraction=gap,
                )
            )

    return tuple(pairs)


def provisional_gauss_tokens(
    visits: Iterable[CrossingVisit],
    tie_tolerance: float = 1.0e-12,
) -> tuple[str, ...]:
    """Return tokens while preserving unresolved ties with braces."""
    tokens: list[str] = []

    for group in group_visit_positions(
        visits,
        tolerance=tie_tolerance,
    ):
        if len(group) == 1:
            tokens.append(
                group[0].token
            )
            continue

        tokens.append(
            "{"
            + "|".join(
                visit.token
                for visit in group
            )
            + "}"
        )

    return tuple(tokens)


def unique_gauss_tokens(
    visits: Iterable[CrossingVisit],
    tie_tolerance: float = 1.0e-12,
) -> tuple[str, ...]:
    """Return a unique Gauss sequence or reject unresolved ties."""
    ties = find_order_ties(
        visits,
        tolerance=tie_tolerance,
    )

    if ties:
        descriptions = [
            "/".join(
                visit.token
                for visit in group
            )
            for group in ties
        ]

        raise ValueError(
            "Gauss order is unresolved at: "
            + ", ".join(descriptions)
        )

    return tuple(
        visit.token
        for visit in _ordered_visits(visits)
    )


def apply_order_reviews(
    visits: Iterable[CrossingVisit],
    review_rows: Iterable[Mapping[str, object]],
    require_complete: bool = True,
) -> tuple[CrossingVisit, ...]:
    """Apply accepted local visit-order decisions.

    The raw geometric order remains the default. A reviewed pair may
    confirm that order or reverse two consecutive visits on the same
    visible segment. Exact positional ties are thereby resolved without
    modifying their measured arc-length coordinates.
    """
    ordered = list(
        _ordered_visits(visits)
    )

    token_to_visit: dict[str, CrossingVisit] = {}

    for visit in ordered:
        if visit.token in token_to_visit:
            raise ValueError(
                f"Duplicate Gauss-visit token: {visit.token}"
            )

        token_to_visit[visit.token] = visit

    reviews = [
        dict(row)
        for row in review_rows
    ]

    seen_review_ids: set[str] = set()
    accepted_reviews: list[
        tuple[
            str,
            str,
            str,
            SegmentKey,
        ]
    ] = []

    for row in reviews:
        review_id = str(
            row.get("review_id", "")
        ).strip()

        if not review_id:
            raise ValueError(
                "Every order-review row requires review_id."
            )

        if review_id in seen_review_ids:
            raise ValueError(
                f"Duplicate order-review identifier: {review_id}"
            )

        seen_review_ids.add(review_id)

        status = str(
            row.get("status", "")
        ).strip()

        if status not in {
            "unreviewed",
            "accepted",
        }:
            raise ValueError(
                f"{review_id}: invalid review status {status!r}."
            )

        provisional_first = str(
            row.get("provisional_first", "")
        ).strip()

        provisional_second = str(
            row.get("provisional_second", "")
        ).strip()

        provisional_tokens = {
            provisional_first,
            provisional_second,
        }

        if (
            len(provisional_tokens) != 2
            or "" in provisional_tokens
        ):
            raise ValueError(
                f"{review_id}: provisional visit pair is incomplete."
            )

        missing = (
            provisional_tokens
            - set(token_to_visit)
        )

        if missing:
            raise ValueError(
                f"{review_id}: unknown provisional visit tokens: "
                + ", ".join(sorted(missing))
            )

        first_visit = token_to_visit[
            provisional_first
        ]

        second_visit = token_to_visit[
            provisional_second
        ]

        if (
            first_visit.segment_key
            != second_visit.segment_key
        ):
            raise ValueError(
                f"{review_id}: reviewed visits are not on "
                "the same visible segment."
            )

        row_key = (
            str(row.get("layer", "")).strip(),
            int(row["segment_id"]),
        )

        if row_key != first_visit.segment_key:
            raise ValueError(
                f"{review_id}: review-row segment does not "
                "match the visit pair."
            )

        if status == "unreviewed":
            if require_complete:
                raise ValueError(
                    f"Unresolved order review: {review_id}"
                )

            continue

        accepted_first = str(
            row.get("accepted_first", "")
        ).strip()

        accepted_second = str(
            row.get("accepted_second", "")
        ).strip()

        accepted_tokens = {
            accepted_first,
            accepted_second,
        }

        if accepted_tokens != provisional_tokens:
            raise ValueError(
                f"{review_id}: accepted visit pair differs "
                "from the provisional review pair."
            )

        if not str(
            row.get("confidence", "")
        ).strip():
            raise ValueError(
                f"{review_id}: accepted order requires confidence."
            )

        if not str(
            row.get("reviewed_utc", "")
        ).strip():
            raise ValueError(
                f"{review_id}: accepted order requires reviewed_utc."
            )

        accepted_reviews.append(
            (
                review_id,
                accepted_first,
                accepted_second,
                first_visit.segment_key,
            )
        )

    for (
        review_id,
        accepted_first,
        accepted_second,
        segment_key,
    ) in accepted_reviews:
        segment_tokens = [
            visit.token
            for visit in ordered
            if visit.segment_key == segment_key
        ]

        local_first = segment_tokens.index(
            accepted_first
        )

        local_second = segment_tokens.index(
            accepted_second
        )

        if abs(local_first - local_second) != 1:
            raise ValueError(
                f"{review_id}: reviewed visits are no longer "
                "consecutive on their segment."
            )

        if local_first < local_second:
            continue

        global_first = next(
            index
            for index, visit in enumerate(ordered)
            if visit.token == accepted_first
        )

        global_second = next(
            index
            for index, visit in enumerate(ordered)
            if visit.token == accepted_second
        )

        ordered[
            global_first
        ], ordered[
            global_second
        ] = (
            ordered[global_second],
            ordered[global_first],
        )

    final_token_positions = {
        visit.token: index
        for index, visit in enumerate(ordered)
    }

    for (
        review_id,
        accepted_first,
        accepted_second,
        _segment_key,
    ) in accepted_reviews:
        if (
            final_token_positions[accepted_first]
            >= final_token_positions[accepted_second]
        ):
            raise ValueError(
                f"{review_id}: accepted ordering was not applied."
            )

    return tuple(ordered)


def validate_complete_gauss_visits(
    visits: Iterable[CrossingVisit],
    expected_event_count: int | None = None,
) -> None:
    """Validate a complete ordered O/U Gauss-visit sequence."""
    ordered = tuple(visits)

    token_counts = Counter(
        visit.token
        for visit in ordered
    )

    duplicate_tokens = [
        token
        for token, count in token_counts.items()
        if count != 1
    ]

    if duplicate_tokens:
        raise ValueError(
            "Gauss-visit tokens are not unique: "
            + ", ".join(sorted(duplicate_tokens))
        )

    by_event: dict[
        str,
        list[CrossingVisit],
    ] = defaultdict(list)

    for visit in ordered:
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
                f"{event_id}: expected one over and one under visit."
            )
