"""Integration checks for the A10 cross-colour matching space."""

from __future__ import annotations

import csv
from pathlib import Path

from meru_geometry.endpoint_matching_search import (
    enumerate_endpoint_perfect_matchings,
)


ROOT = Path(__file__).resolve().parents[1]

PATH = (
    ROOT
    / "data"
    / "manual_digitizations"
    / "A10_P03"
    / "cross_colour_endpoint_review.csv"
)

BASELINE_IDS = {
    "X_RG_R_S07E_G_S11E",
    "X_RB_R_S01S_B_S06E",
    "X_GB_G_S01S_B_S01S",
}


def test_a10_cross_colour_candidate_space() -> None:
    with PATH.open(
        newline="",
        encoding="utf-8",
    ) as handle:
        rows = list(
            csv.DictReader(handle)
        )

    matchings = (
        enumerate_endpoint_perfect_matchings(
            rows
        )
    )

    assert len(rows) == 12
    assert len(matchings) == 8

    baseline = [
        matching
        for matching in matchings
        if set(
            matching.candidate_ids
        ) == BASELINE_IDS
    ]

    assert len(baseline) == 1
    assert (
        baseline[0].accepted_edge_count
        == 3
    )
