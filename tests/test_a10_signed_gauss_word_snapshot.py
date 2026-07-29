"""Integrity tests for the frozen A10_P03 signed Gauss word."""

from __future__ import annotations

import csv
import hashlib
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

DATA_DIR = (
    ROOT
    / "data"
    / "manual_digitizations"
    / "A10_P03"
)

UNSIGNED_PATH = (
    DATA_DIR
    / "gauss_word.csv"
)

SIGNED_PATH = (
    DATA_DIR
    / "signed_gauss_word.csv"
)

HASH_PATH = (
    DATA_DIR
    / "signed_gauss_word.sha256"
)

SIGN_REVIEW_PATH = (
    DATA_DIR
    / "crossing_sign_review.csv"
)


def load_csv(
    path: Path,
) -> list[dict[str, str]]:
    """Load one tracked CSV table."""
    with path.open(
        newline="",
        encoding="utf-8",
    ) as handle:
        return list(
            csv.DictReader(handle)
        )


def test_signed_snapshot_matches_unsigned_visit_order() -> None:
    unsigned = load_csv(
        UNSIGNED_PATH
    )

    signed = load_csv(
        SIGNED_PATH
    )

    assert len(unsigned) == 62
    assert len(signed) == 62

    assert [
        row["token"]
        for row in unsigned
    ] == [
        row["unsigned_token"]
        for row in signed
    ]

    assert [
        int(row["order"])
        for row in signed
    ] == list(range(1, 63))


def test_signed_snapshot_has_complete_event_signs() -> None:
    rows = load_csv(
        SIGNED_PATH
    )

    by_event: dict[
        str,
        list[dict[str, str]],
    ] = defaultdict(list)

    for row in rows:
        by_event[
            row["event_id"]
        ].append(
            row
        )

    assert len(by_event) == 31

    for event_rows in by_event.values():
        assert len(event_rows) == 2

        assert Counter(
            row["role"]
            for row in event_rows
        ) == Counter(
            {
                "O": 1,
                "U": 1,
            }
        )

        assert {
            int(row["crossing_sign"])
            for row in event_rows
        } == {
            -1,
        }

    assert len(
        {
            row["signed_token"]
            for row in rows
        }
    ) == 62


def test_manual_sign_reviews_are_embedded() -> None:
    signed = load_csv(
        SIGNED_PATH
    )

    reviews = load_csv(
        SIGN_REVIEW_PATH
    )

    assert len(reviews) == 4
    assert all(
        row["status"] == "accepted"
        for row in reviews
    )

    reviewed_events = {
        row["event_id"]
        for row in reviews
    }

    assert reviewed_events == {
        "E03",
        "E21",
        "E24",
        "E27",
    }

    for row in signed:
        if row["event_id"] in reviewed_events:
            assert (
                row["sign_basis"]
                == "manual_low_angle_review"
            )

            assert (
                row["sign_review_id"]
                == row["event_id"]
            )

        else:
            assert (
                row["sign_basis"]
                == "derived_stable_all_spans"
            )

            assert row["sign_review_id"] == ""


def test_signed_gauss_word_matches_recorded_digest() -> None:
    rows = load_csv(
        SIGNED_PATH
    )

    tokens = tuple(
        row["signed_token"]
        for row in rows
    )

    payload = (
        "\n".join(tokens) + "\n"
    ).encode("utf-8")

    computed = hashlib.sha256(
        payload
    ).hexdigest()

    recorded = (
        HASH_PATH.read_text(
            encoding="utf-8"
        )
        .strip()
        .split()[0]
    )

    assert computed == recorded
