"""Sensitivity of Gauss parity to reviewed adjacent visit orders."""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from itertools import combinations

from meru_geometry.gauss_parity import (
    audit_gauss_parity,
)


@dataclass(frozen=True)
class ReviewedOrderPair:
    """One accepted adjacent order decision."""

    review_id: str
    review_kind: str
    accepted_first: str
    accepted_second: str
    confidence: str


@dataclass(frozen=True)
class OrderSensitivityResult:
    """Parity result after reversing a subset of reviewed pairs."""

    candidate_id: str
    reversed_review_ids: tuple[str, ...]
    violation_event_ids: tuple[str, ...]
    visit_tokens: tuple[str, ...]

    @property
    def reversed_review_count(self) -> int:
        """Return the number of contradicted source reviews."""
        return len(
            self.reversed_review_ids
        )

    @property
    def violation_count(self) -> int:
        """Return the number of parity violations."""
        return len(
            self.violation_event_ids
        )

    @property
    def passes_even_condition(self) -> bool:
        """Return whether all crossings satisfy the even condition."""
        return self.violation_count == 0


def _row_token(
    row: Mapping[str, object],
) -> str:
    """Return and validate one unsigned O/U token."""
    event_id = str(
        row["event_id"]
    ).strip()

    role = str(
        row["role"]
    ).strip()

    if role not in {
        "O",
        "U",
    }:
        raise ValueError(
            f"{event_id}: invalid role {role!r}."
        )

    expected = (
        f"{event_id}{role}"
    )

    recorded = str(
        row.get(
            "token",
            expected,
        )
    ).strip()

    if recorded != expected:
        raise ValueError(
            f"Recorded token {recorded!r} does not "
            f"match {expected!r}."
        )

    return expected


def load_reviewed_order_pairs(
    review_rows: Iterable[
        Mapping[str, object]
    ],
) -> tuple[ReviewedOrderPair, ...]:
    """Load accepted exact-tie and close-order decisions."""
    pairs: list[
        ReviewedOrderPair
    ] = []

    identifiers: set[str] = set()

    for raw_row in review_rows:
        row = dict(raw_row)

        review_kind = str(
            row["review_kind"]
        )

        if review_kind not in {
            "exact_tie",
            "close_order",
        }:
            continue

        review_id = str(
            row["review_id"]
        ).strip()

        if not review_id:
            raise ValueError(
                "Order-review identifiers must not be blank."
            )

        if review_id in identifiers:
            raise ValueError(
                f"Duplicate order review: {review_id}"
            )

        identifiers.add(
            review_id
        )

        if str(row["status"]) != "accepted":
            raise ValueError(
                f"{review_id}: review is not accepted."
            )

        confidence = str(
            row["confidence"]
        ).strip()

        if not confidence:
            raise ValueError(
                f"{review_id}: confidence is missing."
            )

        accepted_first = str(
            row["accepted_first"]
        ).strip()

        accepted_second = str(
            row["accepted_second"]
        ).strip()

        if (
            not accepted_first
            or not accepted_second
            or accepted_first
            == accepted_second
        ):
            raise ValueError(
                f"{review_id}: invalid accepted token pair."
            )

        pairs.append(
            ReviewedOrderPair(
                review_id=review_id,
                review_kind=review_kind,
                accepted_first=(
                    accepted_first
                ),
                accepted_second=(
                    accepted_second
                ),
                confidence=confidence,
            )
        )

    pairs.sort(
        key=lambda pair: pair.review_id
    )

    used_tokens: set[str] = set()

    for pair in pairs:
        pair_tokens = {
            pair.accepted_first,
            pair.accepted_second,
        }

        overlap = (
            used_tokens
            & pair_tokens
        )

        if overlap:
            raise ValueError(
                "Reviewed order pairs overlap at tokens: "
                + ", ".join(
                    sorted(overlap)
                )
            )

        used_tokens.update(
            pair_tokens
        )

    return tuple(pairs)


def _ordered_gauss_rows(
    gauss_rows: Iterable[
        Mapping[str, object]
    ],
) -> list[dict[str, object]]:
    """Return validated rows in contiguous visit order."""
    rows = sorted(
        (
            dict(row)
            for row in gauss_rows
        ),
        key=lambda row: int(
            row["order"]
        ),
    )

    if not rows:
        raise ValueError(
            "A Gauss word must contain visits."
        )

    orders = [
        int(row["order"])
        for row in rows
    ]

    if orders != list(
        range(1, len(rows) + 1)
    ):
        raise ValueError(
            "Gauss orders must be contiguous from one."
        )

    tokens = [
        _row_token(row)
        for row in rows
    ]

    if len(set(tokens)) != len(tokens):
        raise ValueError(
            "Gauss visit tokens must be unique."
        )

    return rows


def reverse_reviewed_pairs(
    gauss_rows: Iterable[
        Mapping[str, object]
    ],
    reviewed_pairs: Iterable[
        ReviewedOrderPair
    ],
    reversed_review_ids: Iterable[str],
) -> list[dict[str, object]]:
    """Reverse selected adjacent reviewed pairs."""
    rows = _ordered_gauss_rows(
        gauss_rows
    )

    pairs = tuple(
        reviewed_pairs
    )

    pair_by_identifier = {
        pair.review_id: pair
        for pair in pairs
    }

    reversed_ids = frozenset(
        reversed_review_ids
    )

    unknown = (
        reversed_ids
        - set(pair_by_identifier)
    )

    if unknown:
        raise ValueError(
            "Unknown reversed reviews: "
            + ", ".join(
                sorted(unknown)
            )
        )

    tokens = [
        _row_token(row)
        for row in rows
    ]

    for pair in pairs:
        try:
            first_index = tokens.index(
                pair.accepted_first
            )

            second_index = tokens.index(
                pair.accepted_second
            )
        except ValueError as error:
            raise ValueError(
                f"{pair.review_id}: reviewed token "
                "is absent from the Gauss word."
            ) from error

        if second_index != first_index + 1:
            raise ValueError(
                f"{pair.review_id}: accepted visits are "
                "not adjacent in their accepted order."
            )

        if pair.review_id in reversed_ids:
            rows[
                first_index
            ], rows[
                second_index
            ] = (
                rows[second_index],
                rows[first_index],
            )

            tokens[
                first_index
            ], tokens[
                second_index
            ] = (
                tokens[second_index],
                tokens[first_index],
            )

    for order, row in enumerate(
        rows,
        start=1,
    ):
        row["order"] = order

    return rows


def enumerate_reviewed_order_sensitivity(
    gauss_rows: Iterable[
        Mapping[str, object]
    ],
    review_rows: Iterable[
        Mapping[str, object]
    ],
) -> tuple[OrderSensitivityResult, ...]:
    """Enumerate every reversal subset of accepted order pairs."""
    frozen_rows = _ordered_gauss_rows(
        gauss_rows
    )

    pairs = load_reviewed_order_pairs(
        review_rows
    )

    identifiers = tuple(
        pair.review_id
        for pair in pairs
    )

    reversal_subsets = [
        subset
        for subset_size in range(
            len(identifiers) + 1
        )
        for subset in combinations(
            identifiers,
            subset_size,
        )
    ]

    results: list[
        OrderSensitivityResult
    ] = []

    for index, subset in enumerate(
        reversal_subsets,
        start=1,
    ):
        candidate_rows = (
            reverse_reviewed_pairs(
                frozen_rows,
                pairs,
                subset,
            )
        )

        audit = audit_gauss_parity(
            candidate_rows
        )

        results.append(
            OrderSensitivityResult(
                candidate_id=(
                    f"O{index:02d}"
                ),
                reversed_review_ids=(
                    tuple(subset)
                ),
                violation_event_ids=tuple(
                    event.event_id
                    for event in sorted(
                        audit.violating_events,
                        key=lambda event: event.event_id,
                    )
                ),
                visit_tokens=tuple(
                    _row_token(row)
                    for row in candidate_rows
                ),
            )
        )

    results.sort(
        key=lambda result: (
            result.violation_count,
            result.reversed_review_count,
            result.reversed_review_ids,
        )
    )

    return tuple(results)
