"""Structural checks for the full A10_P03 endpoint matching space."""

from __future__ import annotations

import csv
from pathlib import Path

from meru_geometry.endpoint_matching_search import (
    endpoint_pair,
    enumerate_endpoint_perfect_matchings,
)


ROOT = Path(__file__).resolve().parents[1]

DATA_DIR = (
    ROOT
    / "data"
    / "manual_digitizations"
    / "A10_P03"
)

CANDIDATE_PATHS = (
    DATA_DIR
    / "endpoint_adjudication.csv",
    DATA_DIR
    / "residual_endpoint_review.csv",
    DATA_DIR
    / "cross_colour_endpoint_review.csv",
)


def load_candidates() -> list[dict[str, str]]:
    """Load all three tracked endpoint-candidate tables."""
    rows: list[
        dict[str, str]
    ] = []

    identifiers: set[str] = set()

    for path in CANDIDATE_PATHS:
        with path.open(
            newline="",
            encoding="utf-8",
        ) as handle:
            table = list(
                csv.DictReader(handle)
            )

        for row in table:
            identifier = row[
                "candidate_id"
            ]

            assert (
                identifier
                not in identifiers
            )

            identifiers.add(
                identifier
            )

            row["_source_table"] = (
                path.name
            )

            rows.append(row)

    return rows


def test_a10_full_candidate_graph_has_28_matchings() -> None:
    rows = load_candidates()

    matchings = (
        enumerate_endpoint_perfect_matchings(
            rows
        )
    )

    assert len(rows) == 47
    assert len(matchings) == 28

    assert all(
        len(matching.candidate_ids)
        == 24
        for matching in matchings
    )

    assert all(
        matching.endpoint_count == 48
        for matching in matchings
    )


def test_every_matching_covers_all_48_endpoints_once() -> None:
    rows = load_candidates()

    row_by_identifier = {
        row["candidate_id"]: row
        for row in rows
    }

    matchings = (
        enumerate_endpoint_perfect_matchings(
            rows
        )
    )

    for matching in matchings:
        covered = []

        for identifier in (
            matching.candidate_ids
        ):
            node_a, node_b = (
                endpoint_pair(
                    row_by_identifier[
                        identifier
                    ]
                )
            )

            covered.extend(
                (
                    node_a,
                    node_b,
                )
            )

        assert len(covered) == 48
        assert len(set(covered)) == 48


def test_accepted_reconstruction_is_unique_baseline() -> None:
    rows = load_candidates()

    accepted_ids = {
        row["candidate_id"]
        for row in rows
        if row["status"]
        == "accepted"
    }

    assert len(accepted_ids) == 24

    matchings = (
        enumerate_endpoint_perfect_matchings(
            rows
        )
    )

    baseline = [
        matching
        for matching in matchings
        if set(
            matching.candidate_ids
        )
        == accepted_ids
    ]

    assert len(baseline) == 1

    assert (
        baseline[0].accepted_edge_count
        == 24
    )

    assert all(
        matching.accepted_edge_count
        < 24
        for matching in matchings
        if matching != baseline[0]
    )
