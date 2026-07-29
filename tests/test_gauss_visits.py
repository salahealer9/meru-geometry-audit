"""Tests for ordered crossing visits."""

from __future__ import annotations

import numpy as np
import pytest

from meru_geometry.gauss_visits import (
    CrossingVisit,
    build_crossing_visits,
    find_close_visit_pairs,
    find_order_ties,
    polyline_arc_fraction,
    provisional_gauss_tokens,
    unique_gauss_tokens,
)
from meru_geometry.global_cycle import SegmentVisit


def make_visit(
    event_id: str,
    role: str,
    fraction: float,
) -> CrossingVisit:
    """Construct a minimal red-segment visit."""
    return CrossingVisit(
        event_id=event_id,
        role=role,
        candidate_id=f"C_{event_id}",
        layer="red",
        segment_id=1,
        traversal_forward=True,
        segment_order=0,
        source_fraction=fraction,
        traversal_fraction=fraction,
        global_position=fraction,
        panel_x=0.0,
        panel_y=0.0,
    )


def crossing_row() -> dict[str, object]:
    """Return one reviewed crossing record."""
    return {
        "candidate_id": "XING_R_S01_B_S01",
        "status": "crossing",
        "event_id": "E01",
        "layer_a": "red",
        "segment_a": 1,
        "layer_b": "blue",
        "segment_b": 1,
        "over_layer": "blue",
        "over_segment": 1,
        "under_layer": "red",
        "under_segment": 1,
        "piece_index_a": 0,
        "fraction_a": 0.25,
        "piece_index_b": 0,
        "fraction_b": 0.25,
        "panel_x": 0.5,
        "panel_y": 0.5,
    }


def test_polyline_arc_fraction_uses_length() -> None:
    points = np.asarray(
        [
            [0.0, 0.0],
            [1.0, 0.0],
            [4.0, 0.0],
        ]
    )

    result = polyline_arc_fraction(
        points,
        piece_index=1,
        piece_fraction=0.5,
    )

    assert result == pytest.approx(
        2.5 / 4.0
    )


def test_build_visits_respects_reverse_traversal() -> None:
    segments = {
        ("red", 1): np.asarray(
            [
                [0.0, 0.0],
                [4.0, 0.0],
            ]
        ),
        ("blue", 1): np.asarray(
            [
                [0.0, 1.0],
                [4.0, 1.0],
            ]
        ),
    }

    traversal = (
        SegmentVisit(
            layer="red",
            segment_id=1,
            forward=True,
        ),
        SegmentVisit(
            layer="blue",
            segment_id=1,
            forward=False,
        ),
    )

    visits = build_crossing_visits(
        [crossing_row()],
        segments,
        traversal,
    )

    red = next(
        visit
        for visit in visits
        if visit.layer == "red"
    )

    blue = next(
        visit
        for visit in visits
        if visit.layer == "blue"
    )

    assert red.traversal_fraction == pytest.approx(
        0.25
    )

    assert blue.traversal_fraction == pytest.approx(
        0.75
    )


def test_build_visits_assigns_one_over_and_one_under() -> None:
    segments = {
        ("red", 1): np.asarray(
            [
                [0.0, 0.0],
                [1.0, 0.0],
            ]
        ),
        ("blue", 1): np.asarray(
            [
                [0.0, 1.0],
                [1.0, 1.0],
            ]
        ),
    }

    traversal = (
        SegmentVisit("red", 1, True),
        SegmentVisit("blue", 1, True),
    )

    visits = build_crossing_visits(
        [crossing_row()],
        segments,
        traversal,
    )

    assert {
        visit.role
        for visit in visits
    } == {
        "O",
        "U",
    }


def test_exact_order_tie_is_detected() -> None:
    visits = (
        make_visit("E01", "O", 1.0),
        make_visit("E02", "U", 1.0),
    )

    ties = find_order_ties(visits)

    assert len(ties) == 1
    assert {
        visit.token
        for visit in ties[0]
    } == {
        "E01O",
        "E02U",
    }


def test_close_consecutive_pair_is_reported() -> None:
    visits = (
        make_visit("E01", "O", 0.20),
        make_visit("E02", "U", 0.22),
        make_visit("E03", "O", 0.80),
    )

    pairs = find_close_visit_pairs(
        visits,
        maximum_gap=0.03,
    )

    assert len(pairs) == 1
    assert pairs[0].first.token == "E01O"
    assert pairs[0].second.token == "E02U"


def test_unique_tokens_reject_tie_but_provisional_preserves_it() -> None:
    visits = (
        make_visit("E01", "O", 1.0),
        make_visit("E02", "U", 1.0),
    )

    assert provisional_gauss_tokens(
        visits
    ) == (
        "{E01O|E02U}",
    )

    with pytest.raises(
        ValueError,
        match="unresolved",
    ):
        unique_gauss_tokens(visits)
