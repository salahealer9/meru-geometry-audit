"""Tests for the classical Gauss even condition."""

from __future__ import annotations

import pytest

from meru_geometry.gauss_parity import (
    audit_gauss_parity,
    validate_classical_even_condition,
)


def rows(
    visits: tuple[
        tuple[str, str],
        ...,
    ],
) -> list[dict[str, object]]:
    """Construct ordered Gauss rows from event-role pairs."""
    return [
        {
            "order": order,
            "event_id": event_id,
            "role": role,
        }
        for order, (
            event_id,
            role,
        ) in enumerate(
            visits,
            start=1,
        )
    ]


def test_single_crossing_passes_even_condition() -> None:
    audit = audit_gauss_parity(
        rows(
            (
                ("A", "O"),
                ("A", "U"),
            )
        )
    )

    assert audit.event_count == 1
    assert audit.violation_count == 0

    event = audit.events[0]

    assert event.visits_between == 0
    assert event.interlacement_degree == 0
    assert event.opposite_position_parity


def test_interlaced_pair_fails_even_condition() -> None:
    audit = audit_gauss_parity(
        rows(
            (
                ("A", "O"),
                ("B", "O"),
                ("A", "U"),
                ("B", "U"),
            )
        )
    )

    assert audit.violation_count == 2

    for event in audit.events:
        assert event.visits_between == 1
        assert event.interlacement_degree == 1
        assert not event.passes_even_condition


def test_nested_pair_passes_even_condition() -> None:
    audit = audit_gauss_parity(
        rows(
            (
                ("A", "O"),
                ("B", "O"),
                ("B", "U"),
                ("A", "U"),
            )
        )
    )

    assert audit.violation_count == 0

    assert [
        event.interlacement_degree
        for event in audit.events
    ] == [
        0,
        0,
    ]


def test_duplicate_role_is_rejected() -> None:
    with pytest.raises(
        ValueError,
        match="one O and one U",
    ):
        audit_gauss_parity(
            rows(
                (
                    ("A", "O"),
                    ("A", "O"),
                )
            )
        )


def test_classical_validation_rejects_violations() -> None:
    audit = audit_gauss_parity(
        rows(
            (
                ("A", "O"),
                ("B", "O"),
                ("A", "U"),
                ("B", "U"),
            )
        )
    )

    with pytest.raises(
        ValueError,
        match="failed for 2 events",
    ):
        validate_classical_even_condition(
            audit
        )
