"""A10_P03 reviewed-order parity sensitivity baseline."""

from __future__ import annotations

import csv
from pathlib import Path

from meru_geometry.gauss_order_sensitivity import (
    enumerate_reviewed_order_sensitivity,
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

REVIEW_PATH = (
    DATA_DIR
    / "gauss_order_review.csv"
)

EXPECTED_BEST_REVERSALS = (
    "ORDER_B_S04_E01O_E16O",
    "ORDER_R_S01_E21O_E24U",
)

EXPECTED_BEST_VIOLATIONS = (
    "E03",
    "E05",
    "E07",
    "E09",
    "E13",
    "E14",
    "E15",
    "E17",
    "E22",
    "E23",
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


def test_a10_reviewed_order_sensitivity_baseline() -> None:
    results = (
        enumerate_reviewed_order_sensitivity(
            load_csv(
                GAUSS_PATH
            ),
            load_csv(
                REVIEW_PATH
            ),
        )
    )

    assert len(results) == 16

    baseline = [
        result
        for result in results
        if not result.reversed_review_ids
    ]

    assert len(baseline) == 1
    assert baseline[0].violation_count == 16

    minimum = min(
        result.violation_count
        for result in results
    )

    assert minimum == 12

    best = [
        result
        for result in results
        if result.violation_count
        == minimum
    ]

    assert len(best) == 1

    assert (
        best[0].reversed_review_ids
        == EXPECTED_BEST_REVERSALS
    )

    assert (
        best[0].violation_event_ids
        == EXPECTED_BEST_VIOLATIONS
    )
