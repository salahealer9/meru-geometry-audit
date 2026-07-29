"""Tests for oriented crossing-sign calculations."""

from __future__ import annotations

import numpy as np
import pytest

from meru_geometry.crossing_signs import (
    crossing_sign,
    crossing_sign_stability,
    derive_crossing_signs,
    oriented_tangent,
    writhe,
)


def crossing_row() -> dict[str, object]:
    """Return one minimal reviewed crossing."""
    return {
        "candidate_id": "XING_R_S01_B_S01",
        "status": "crossing",
        "event_id": "E01",
        "layer_a": "red",
        "segment_a": 1,
        "layer_b": "blue",
        "segment_b": 1,
        "over_layer": "red",
        "over_segment": 1,
        "under_layer": "blue",
        "under_segment": 1,
        "piece_index_a": 0,
        "fraction_a": 0.5,
        "piece_index_b": 0,
        "fraction_b": 0.5,
    }


def test_positive_crossing_sign() -> None:
    sign, determinant, angle = crossing_sign(
        np.asarray([1.0, 0.0]),
        np.asarray([0.0, 1.0]),
    )

    assert sign == 1
    assert determinant == pytest.approx(1.0)
    assert angle == pytest.approx(90.0)


def test_negative_crossing_sign() -> None:
    sign, determinant, angle = crossing_sign(
        np.asarray([1.0, 0.0]),
        np.asarray([0.0, -1.0]),
    )

    assert sign == -1
    assert determinant == pytest.approx(-1.0)
    assert angle == pytest.approx(90.0)


def test_reversing_entire_knot_preserves_sign() -> None:
    first = crossing_sign(
        np.asarray([1.0, 0.0]),
        np.asarray([0.0, 1.0]),
    )[0]

    reversed_orientation = crossing_sign(
        np.asarray([-1.0, 0.0]),
        np.asarray([0.0, -1.0]),
    )[0]

    assert first == reversed_orientation


def test_swapping_over_and_under_flips_sign() -> None:
    first = crossing_sign(
        np.asarray([1.0, 0.0]),
        np.asarray([0.0, 1.0]),
    )[0]

    swapped = crossing_sign(
        np.asarray([0.0, 1.0]),
        np.asarray([1.0, 0.0]),
    )[0]

    assert first == -swapped


def test_image_y_down_is_converted_to_cartesian() -> None:
    tangent = oriented_tangent(
        np.asarray(
            [
                [0.0, 0.0],
                [0.0, 4.0],
            ]
        ),
        piece_index=0,
        piece_fraction=0.5,
        traversal_forward=True,
        span_px=2.0,
        image_y_down=True,
    )

    assert tangent == pytest.approx(
        (0.0, -1.0)
    )


def test_derive_crossing_signs_uses_traversal_direction() -> None:
    segments = {
        ("red", 1): np.asarray(
            [
                [0.0, 0.0],
                [4.0, 0.0],
            ]
        ),
        ("blue", 1): np.asarray(
            [
                [2.0, -2.0],
                [2.0, 2.0],
            ]
        ),
    }

    directions = {
        ("red", 1): True,
        ("blue", 1): True,
    }

    result = derive_crossing_signs(
        [crossing_row()],
        segments,
        directions,
        span_px=2.0,
    )

    assert len(result) == 1
    assert result[0].sign == -1
    assert writhe(result) == -1


def test_sign_stability_across_spans() -> None:
    segments = {
        ("red", 1): np.asarray(
            [
                [0.0, 0.0],
                [4.0, 0.0],
            ]
        ),
        ("blue", 1): np.asarray(
            [
                [2.0, -3.0],
                [2.0, 3.0],
            ]
        ),
    }

    directions = {
        ("red", 1): True,
        ("blue", 1): True,
    }

    stability = crossing_sign_stability(
        [crossing_row()],
        segments,
        directions,
        spans_px=(1.0, 2.0, 4.0),
    )

    assert stability == {
        "E01": (-1, -1, -1)
    }
