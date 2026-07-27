"""Tests for cross-colour endpoint matching."""

from __future__ import annotations

import numpy as np
import pytest

from meru_geometry.cross_colour_connectivity import (
    candidate_endpoint_keys,
    cross_colour_candidate_identifier,
    enumerate_cross_colour_matchings,
    rank_cross_colour_pairs,
    validate_cross_colour_review_rows,
)


def sample_segments() -> dict[
    str,
    dict[int, np.ndarray],
]:
    return {
        "red": {
            1: np.asarray(
                [[0.0, 0.0], [1.0, 0.0]]
            ),
        },
        "green": {
            1: np.asarray(
                [[0.0, 2.0], [1.0, 2.0]]
            ),
        },
        "blue": {
            1: np.asarray(
                [[0.0, 4.0], [1.0, 4.0]]
            ),
        },
    }


def free_endpoints() -> dict[
    str,
    tuple[tuple[int, str], ...],
]:
    return {
        "red": (
            (1, "start"),
            (1, "end"),
        ),
        "green": (
            (1, "start"),
            (1, "end"),
        ),
        "blue": (
            (1, "start"),
            (1, "end"),
        ),
    }


def test_six_free_endpoints_give_twelve_edges() -> None:
    candidates = rank_cross_colour_pairs(
        sample_segments(),
        free_endpoints(),
    )

    assert len(candidates) == 12


def test_six_endpoints_give_eight_perfect_matchings() -> None:
    candidates = rank_cross_colour_pairs(
        sample_segments(),
        free_endpoints(),
    )

    matchings = enumerate_cross_colour_matchings(
        candidates
    )

    assert len(matchings) == 8


def test_matching_uses_every_endpoint_once() -> None:
    candidates = rank_cross_colour_pairs(
        sample_segments(),
        free_endpoints(),
    )

    matchings = enumerate_cross_colour_matchings(
        candidates
    )

    for matching in matchings:
        endpoints = [
            endpoint
            for candidate in matching.candidates
            for endpoint in candidate_endpoint_keys(
                candidate
            )
        ]

        assert len(endpoints) == 6
        assert len(set(endpoints)) == 6


def test_candidate_identifier_is_stable() -> None:
    candidates = rank_cross_colour_pairs(
        sample_segments(),
        free_endpoints(),
    )

    candidate = next(
        candidate
        for candidate in candidates
        if candidate.layer_a == "red"
        and candidate.endpoint_a == "start"
        and candidate.layer_b == "green"
        and candidate.endpoint_b == "start"
    )

    assert (
        cross_colour_candidate_identifier(candidate)
        == "X_RG_R_S01S_G_S01S"
    )


def test_duplicate_review_identifier_is_rejected() -> None:
    row = {
        "candidate_id": "X_RG_R_S01S_G_S01S",
        "layer_a": "red",
        "layer_b": "green",
        "status": "unreviewed",
        "confidence": "",
        "reason_code": "",
    }

    with pytest.raises(
        ValueError,
        match="Duplicate",
    ):
        validate_cross_colour_review_rows(
            [row, row]
        )
