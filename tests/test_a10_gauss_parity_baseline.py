"""Baseline parity audit of the frozen A10_P03 Gauss word."""

from __future__ import annotations

import csv
from pathlib import Path

from meru_geometry.gauss_parity import (
    audit_gauss_parity,
)


ROOT = Path(__file__).resolve().parents[1]

DATA_DIR = (
    ROOT
    / "data"
    / "manual_digitizations"
    / "A10_P03"
)

GAUSS_PATH = (
    DATA_DIR
    / "gauss_word.csv"
)

SIGNED_PATH = (
    DATA_DIR
    / "signed_gauss_word.csv"
)

EXPECTED_VIOLATIONS = (
    "E01",
    "E03",
    "E05",
    "E07",
    "E09",
    "E13",
    "E14",
    "E15",
    "E16",
    "E17",
    "E21",
    "E22",
    "E23",
    "E24",
    "E28",
    "E30",
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


def test_frozen_a10_word_has_recorded_parity_baseline() -> None:
    audit = audit_gauss_parity(
        load_csv(
            GAUSS_PATH
        )
    )

    assert audit.visit_count == 62
    assert audit.event_count == 31
    assert len(audit.passing_events) == 15
    assert audit.violation_count == 16

    assert tuple(
        sorted(
            (
                event.event_id
                for event in audit.violating_events
            ),
            key=lambda event_id: int(
                event_id[1:]
            ),
        )
    ) == EXPECTED_VIOLATIONS


def test_signed_snapshot_uses_same_unsigned_sequence() -> None:
    unsigned = sorted(
        load_csv(
            GAUSS_PATH
        ),
        key=lambda row: int(row["order"]),
    )

    signed = sorted(
        load_csv(
            SIGNED_PATH
        ),
        key=lambda row: int(row["order"]),
    )

    assert [
        row["token"]
        for row in unsigned
    ] == [
        row["unsigned_token"]
        for row in signed
    ]
