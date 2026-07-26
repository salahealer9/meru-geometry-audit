"""Tests for source-trace geometry analysis."""

from __future__ import annotations

import numpy as np
import pytest

from meru_geometry.trace_analysis import (
    endpoint_connection_candidates,
    fit_descriptive_ellipse,
    normalize_panel_coordinates,
    polyline_metrics,
    sample_ellipse,
)


def test_polyline_metrics() -> None:
    points = np.asarray(
        [
            [0.0, 0.0],
            [3.0, 0.0],
            [3.0, 4.0],
        ]
    )

    metrics = polyline_metrics(points)

    assert metrics.point_count == 3
    assert metrics.length == pytest.approx(7.0)
    assert metrics.chord_length == pytest.approx(5.0)
    assert metrics.tortuosity == pytest.approx(1.4)


def test_panel_coordinate_normalization() -> None:
    points = np.asarray(
        [
            [0.0, 0.0],
            [200.0, 100.0],
        ]
    )

    normalized = normalize_panel_coordinates(
        points,
        width_px=200.0,
        height_px=100.0,
    )

    assert np.allclose(
        normalized,
        np.asarray(
            [
                [-0.5, 0.25],
                [0.5, -0.25],
            ]
        ),
    )


def test_descriptive_ellipse_recovery() -> None:
    centre = np.asarray([4.0, -2.0])
    semi_major = 5.0
    semi_minor = 2.0
    angle = 0.37

    parameter = np.linspace(
        0.0,
        2.0 * np.pi,
        200,
        endpoint=False,
    )

    local = np.column_stack(
        (
            semi_major * np.cos(parameter),
            semi_minor * np.sin(parameter),
        )
    )

    rotation = np.asarray(
        [
            [np.cos(angle), -np.sin(angle)],
            [np.sin(angle), np.cos(angle)],
        ]
    )

    points = local @ rotation.T + centre

    fit = fit_descriptive_ellipse(points)

    assert fit.success
    assert fit.centre_x == pytest.approx(
        centre[0],
        abs=1.0e-8,
    )
    assert fit.centre_y == pytest.approx(
        centre[1],
        abs=1.0e-8,
    )
    assert fit.semi_major == pytest.approx(
        semi_major,
        abs=1.0e-8,
    )
    assert fit.semi_minor == pytest.approx(
        semi_minor,
        abs=1.0e-8,
    )
    assert fit.radial_rms < 1.0e-10

    sampled = sample_ellipse(fit, n_points=100)
    assert sampled.shape == (100, 2)


def test_endpoint_candidates_rank_nearby_continuation_first() -> None:
    segments = {
        0: np.asarray(
            [
                [0.0, 0.0],
                [1.0, 0.0],
                [2.0, 0.0],
            ]
        ),
        1: np.asarray(
            [
                [3.0, 0.0],
                [4.0, 0.0],
                [5.0, 0.0],
            ]
        ),
        2: np.asarray(
            [
                [20.0, 10.0],
                [21.0, 10.0],
                [22.0, 10.0],
            ]
        ),
    }

    candidates = endpoint_connection_candidates(
        segments,
        maximum_candidates=1,
    )

    assert len(candidates) == 1
    assert {
        candidates[0].segment_a,
        candidates[0].segment_b,
    } == {0, 1}
    assert candidates[0].distance == pytest.approx(1.0)


def test_empty_segment_mapping_returns_no_candidates() -> None:
    assert endpoint_connection_candidates({}) == ()


def test_closed_polyline_metrics_include_closing_edge() -> None:
    points = np.asarray(
        [
            [0.0, 0.0],
            [1.0, 0.0],
            [1.0, 1.0],
            [0.0, 1.0],
        ]
    )

    metrics = polyline_metrics(
        points,
        closed=True,
    )

    assert metrics.length == pytest.approx(4.0)
    assert metrics.chord_length == pytest.approx(1.0)
    assert np.isnan(metrics.tortuosity)
