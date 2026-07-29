"""Tests for reviewed Gauss-order sensitivity."""

from __future__ import annotations

import pytest

from meru_geometry.gauss_order_sensitivity import (
    enumerate_reviewed_order_sensitivity,
    load_reviewed_order_pairs,
    reverse_reviewed_pairs,
)


def gauss_rows() -> list[dict[str, object]]:
    """Return an interlaced two-event Gauss word."""
    visits = (
        ("A", "O"),
        ("B", "O"),
        ("A", "U"),
        ("B", "U"),
    )

    return [
        {
            "order": order,
            "event_id": event_id,
            "role": role,
            "token": (
                f"{event_id}{role}"
            ),
        }
        for order, (
            event_id,
            role,
        ) in enumerate(
            visits,
            start=1,
        )
    ]


def review_row(
    *,
    review_id: str = "ORDER_AO_BO",
    first: str = "AO",
    second: str = "BO",
) -> dict[str, object]:
    """Return one accepted adjacent order review."""
    return {
        "review_id": review_id,
        "review_kind": "close_order",
        "status": "accepted",
        "accepted_first": first,
        "accepted_second": second,
        "confidence": "high",
    }


def test_reversing_two_violating_events_repairs_them() -> None:
    results = (
        enumerate_reviewed_order_sensitivity(
            gauss_rows(),
            (
                review_row(),
            ),
        )
    )

    assert len(results) == 2

    assert results[0].violation_count == 0

    assert results[0].reversed_review_ids == (
        "ORDER_AO_BO",
    )

    assert results[1].violation_count == 2
    assert results[1].reversed_review_ids == ()


def test_nonadjacent_review_pair_is_rejected() -> None:
    pairs = load_reviewed_order_pairs(
        (
            review_row(
                first="AO",
                second="AU",
            ),
        )
    )

    with pytest.raises(
        ValueError,
        match="not adjacent",
    ):
        reverse_reviewed_pairs(
            gauss_rows(),
            pairs,
            (),
        )


def test_overlapping_review_pairs_are_rejected() -> None:
    with pytest.raises(
        ValueError,
        match="overlap",
    ):
        load_reviewed_order_pairs(
            (
                review_row(),
                review_row(
                    review_id="ORDER_BO_AU",
                    first="BO",
                    second="AU",
                ),
            )
        )


def test_no_reviews_produces_baseline_only() -> None:
    results = (
        enumerate_reviewed_order_sensitivity(
            gauss_rows(),
            (),
        )
    )

    assert len(results) == 1
    assert results[0].reversed_review_ids == ()
    assert results[0].violation_count == 2
