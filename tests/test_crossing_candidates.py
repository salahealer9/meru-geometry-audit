"""Tests for geometric crossing-candidate detection."""

from __future__ import annotations

import numpy as np
import pytest

from meru_geometry.crossing_candidates import (
    closest_polyline_approach,
    crossing_candidate_identifier,
    cycle_adjacency_pairs,
    find_crossing_candidates,
)


def test_perpendicular_segments_intersect() -> None:
    first = np.asarray(
        [
            [-1.0, 0.0],
            [1.0, 0.0],
        ]
    )

    second = np.asarray(
        [
            [0.0, -1.0],
            [0.0, 1.0],
        ]
    )

    result = closest_polyline_approach(
        first,
        second,
    )

    assert result.intersects
    assert result.distance == pytest.approx(0.0)
    assert result.point_a == pytest.approx(
        (0.0, 0.0)
    )

    assert np.degrees(
        result.crossing_angle_radians
    ) == pytest.approx(90.0)


def test_parallel_segments_have_zero_crossing_angle() -> None:
    first = np.asarray(
        [
            [0.0, 0.0],
            [2.0, 0.0],
        ]
    )

    second = np.asarray(
        [
            [0.0, 1.0],
            [2.0, 1.0],
        ]
    )

    result = closest_polyline_approach(
        first,
        second,
    )

    assert result.distance == pytest.approx(1.0)

    assert np.degrees(
        result.crossing_angle_radians
    ) == pytest.approx(0.0)


def test_cycle_adjacency_includes_closing_pair() -> None:
    traversal = (
        ("red", 1),
        ("green", 1),
        ("blue", 1),
    )

    adjacency = cycle_adjacency_pairs(
        traversal
    )

    assert len(adjacency) == 3

    assert (
        ("red", 1),
        ("blue", 1),
    ) in adjacency


def test_adjacent_cycle_segments_are_excluded() -> None:
    segments = {
        ("red", 1): np.asarray(
            [
                [-1.0, 0.0],
                [1.0, 0.0],
            ]
        ),
        ("green", 1): np.asarray(
            [
                [0.0, -1.0],
                [0.0, 1.0],
            ]
        ),
    }

    candidates = find_crossing_candidates(
        segments,
        adjacent_pairs={
            (
                ("red", 1),
                ("green", 1),
            )
        },
        max_distance=1.0,
        min_angle_degrees=5.0,
    )

    assert candidates == ()


def test_non_adjacent_intersection_is_reported() -> None:
    segments = {
        ("red", 1): np.asarray(
            [
                [-1.0, 0.0],
                [1.0, 0.0],
            ]
        ),
        ("green", 2): np.asarray(
            [
                [0.0, -1.0],
                [0.0, 1.0],
            ]
        ),
    }

    candidates = find_crossing_candidates(
        segments,
        max_distance=1.0,
        min_angle_degrees=5.0,
    )

    assert len(candidates) == 1
    assert (
        crossing_candidate_identifier(
            candidates[0]
        )
        == "XING_R_S01_G_S02"
    )
