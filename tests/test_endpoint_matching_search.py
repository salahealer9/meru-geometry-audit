"""Tests for endpoint-matching enumeration and exact-tie transfer."""

from __future__ import annotations

from itertools import combinations

from meru_geometry.endpoint_matching_search import (
    apply_exact_tie_reviews,
    enumerate_endpoint_perfect_matchings,
)
from meru_geometry.gauss_visits import (
    CrossingVisit,
)


def complete_three_colour_rows() -> list[
    dict[str, object]
]:
    """Return the complete cross-colour graph on six endpoints."""
    nodes = [
        ("red", 1, "start"),
        ("red", 2, "end"),
        ("green", 1, "start"),
        ("green", 2, "end"),
        ("blue", 1, "start"),
        ("blue", 2, "end"),
    ]

    rows = []

    for index, (
        node_a,
        node_b,
    ) in enumerate(
        combinations(nodes, 2),
        start=1,
    ):
        if node_a[0] == node_b[0]:
            continue

        rows.append(
            {
                "candidate_id": (
                    f"C{index:02d}"
                ),
                "layer_a": node_a[0],
                "segment_a": node_a[1],
                "endpoint_a": node_a[2],
                "layer_b": node_b[0],
                "segment_b": node_b[1],
                "endpoint_b": node_b[2],
                "distance_px": float(
                    index
                ),
                "score": float(index),
                "status": (
                    "accepted"
                    if index <= 3
                    else "rejected"
                ),
            }
        )

    return rows


def make_visit(
    event_id: str,
    *,
    forward: bool,
) -> CrossingVisit:
    """Return one visit at a shared exact-tie position."""
    return CrossingVisit(
        event_id=event_id,
        role="O",
        candidate_id=f"C_{event_id}",
        layer="red",
        segment_id=1,
        traversal_forward=forward,
        segment_order=0,
        source_fraction=0.25,
        traversal_fraction=(
            0.25
            if forward
            else 0.75
        ),
        global_position=0.25,
        panel_x=0.0,
        panel_y=0.0,
    )


def tie_review() -> dict[str, object]:
    """Return one accepted source order under forward traversal."""
    return {
        "review_id": "ORDER_R_S01_E01O_E02O",
        "review_kind": "exact_tie",
        "traversal_forward": "True",
        "status": "accepted",
        "accepted_first": "E01O",
        "accepted_second": "E02O",
    }


def test_complete_three_colour_space_has_eight_matchings() -> None:
    matchings = enumerate_endpoint_perfect_matchings(
        complete_three_colour_rows()
    )

    assert len(matchings) == 8

    assert all(
        len(matching.candidate_ids) == 3
        for matching in matchings
    )

    assert all(
        matching.endpoint_count == 6
        for matching in matchings
    )


def test_accepted_edge_count_is_recorded() -> None:
    matchings = enumerate_endpoint_perfect_matchings(
        complete_three_colour_rows()
    )

    assert all(
        0
        <= matching.accepted_edge_count
        <= 3
        for matching in matchings
    )


def test_exact_tie_follows_forward_candidate_direction() -> None:
    result = apply_exact_tie_reviews(
        (
            make_visit(
                "E02",
                forward=True,
            ),
            make_visit(
                "E01",
                forward=True,
            ),
        ),
        (
            tie_review(),
        ),
    )

    assert tuple(
        visit.token
        for visit in result
    ) == (
        "E01O",
        "E02O",
    )


def test_exact_tie_reverses_with_candidate_direction() -> None:
    result = apply_exact_tie_reviews(
        (
            make_visit(
                "E01",
                forward=False,
            ),
            make_visit(
                "E02",
                forward=False,
            ),
        ),
        (
            tie_review(),
        ),
    )

    assert tuple(
        visit.token
        for visit in result
    ) == (
        "E02O",
        "E01O",
    )


def test_same_colour_layer_schema_is_supported() -> None:
    """The generic enumerator must accept the one-layer schema."""
    rows = [
        {
            "candidate_id": "SAME_R_01",
            "layer": "red",
            "segment_a": 1,
            "endpoint_a": "start",
            "segment_b": 2,
            "endpoint_b": "end",
            "distance_px": 1.5,
            "score": 2.0,
            "status": "accepted",
        }
    ]

    matchings = enumerate_endpoint_perfect_matchings(
        rows
    )

    assert len(matchings) == 1

    assert matchings[0].candidate_ids == (
        "SAME_R_01",
    )

    assert matchings[0].endpoint_count == 2
    assert matchings[0].accepted_edge_count == 1
