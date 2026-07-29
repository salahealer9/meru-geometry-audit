"""Tests for signed O/U Gauss words."""

from __future__ import annotations

import pytest

from meru_geometry.signed_gauss import (
    SignedGaussVisit,
    build_signed_gauss_visits,
    validate_signed_gauss_visits,
)


def gauss_rows() -> list[dict[str, object]]:
    """Return one complete one-crossing Gauss word."""
    return [
        {
            "order": 1,
            "event_id": "E01",
            "role": "O",
            "token": "E01O",
            "candidate_id": "XING_R_S01_B_S01",
        },
        {
            "order": 2,
            "event_id": "E01",
            "role": "U",
            "token": "E01U",
            "candidate_id": "XING_R_S01_B_S01",
        },
    ]


def test_build_signed_word_preserves_order_and_role() -> None:
    visits = build_signed_gauss_visits(
        gauss_rows(),
        {
            "E01": -1,
        },
    )

    assert tuple(
        visit.signed_token
        for visit in visits
    ) == (
        "E01O-",
        "E01U-",
    )


def test_build_signed_word_rejects_missing_sign() -> None:
    with pytest.raises(
        ValueError,
        match="Missing oriented sign",
    ):
        build_signed_gauss_visits(
            gauss_rows(),
            {},
        )


def test_build_signed_word_rejects_zero_sign() -> None:
    with pytest.raises(
        ValueError,
        match="must be -1 or \\+1",
    ):
        build_signed_gauss_visits(
            gauss_rows(),
            {
                "E01": 0,
            },
        )


def test_validation_rejects_duplicate_visit_role() -> None:
    visits = (
        SignedGaussVisit(
            order=1,
            event_id="E01",
            role="O",
            crossing_sign=-1,
            candidate_id="C01",
        ),
        SignedGaussVisit(
            order=2,
            event_id="E01",
            role="O",
            crossing_sign=-1,
            candidate_id="C01",
        ),
    )

    with pytest.raises(
        ValueError,
        match="one O and one U",
    ):
        validate_signed_gauss_visits(
            visits,
            expected_event_count=1,
        )
