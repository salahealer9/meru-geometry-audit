"""Integrity tests for the frozen A10_P03 O/U Gauss word."""

from __future__ import annotations

import csv
import hashlib
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

SNAPSHOT_PATH = (
    ROOT
    / "data"
    / "manual_digitizations"
    / "A10_P03"
    / "gauss_word.csv"
)

HASH_PATH = (
    ROOT
    / "data"
    / "manual_digitizations"
    / "A10_P03"
    / "gauss_word.sha256"
)

REVIEW_PATH = (
    ROOT
    / "data"
    / "manual_digitizations"
    / "A10_P03"
    / "gauss_order_review.csv"
)


def load_csv(
    path: Path,
) -> list[dict[str, str]]:
    """Load one tracked CSV table."""
    with path.open(
        newline="",
        encoding="utf-8",
    ) as handle:
        return list(csv.DictReader(handle))


def test_frozen_gauss_word_has_complete_ou_visits() -> None:
    rows = load_csv(
        SNAPSHOT_PATH
    )

    assert len(rows) == 62

    assert [
        int(row["order"])
        for row in rows
    ] == list(range(1, 63))

    tokens = [
        row["token"]
        for row in rows
    ]

    assert len(set(tokens)) == 62

    by_event: dict[
        str,
        list[str],
    ] = defaultdict(list)

    for row in rows:
        by_event[
            row["event_id"]
        ].append(
            row["role"]
        )

    assert len(by_event) == 31

    for roles in by_event.values():
        assert Counter(roles) == Counter(
            {
                "O": 1,
                "U": 1,
            }
        )


def test_frozen_word_respects_all_manual_order_reviews() -> None:
    snapshot = load_csv(
        SNAPSHOT_PATH
    )

    reviews = load_csv(
        REVIEW_PATH
    )

    positions = {
        row["token"]: int(row["order"])
        for row in snapshot
    }

    assert len(reviews) == 4
    assert all(
        row["status"] == "accepted"
        for row in reviews
    )

    for row in reviews:
        assert (
            positions[row["accepted_first"]]
            < positions[row["accepted_second"]]
        )


def test_frozen_gauss_word_matches_recorded_digest() -> None:
    rows = load_csv(
        SNAPSHOT_PATH
    )

    tokens = tuple(
        row["token"]
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
