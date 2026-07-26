"""Tests for the regular-tetrahedron baseline."""

from __future__ import annotations

import numpy as np
import pytest

from meru_geometry.tetrahedron import (
    regular_tetrahedron,
    tetrahedron_centroid,
    tetrahedron_edge_lengths,
    tetrahedron_edges,
    tetrahedron_volume,
)


def test_regular_tetrahedron_shape_centroid_and_radius() -> None:
    vertices = regular_tetrahedron()

    assert vertices.shape == (4, 3)
    assert np.allclose(
        tetrahedron_centroid(vertices),
        np.zeros(3),
        atol=1.0e-12,
    )
    assert np.allclose(
        np.linalg.norm(vertices, axis=1),
        np.ones(4),
        atol=1.0e-12,
    )


def test_regular_tetrahedron_has_six_equal_edges() -> None:
    vertices = regular_tetrahedron()
    edges = tetrahedron_edges()
    lengths = tetrahedron_edge_lengths(vertices)

    assert edges.shape == (6, 2)
    assert lengths.shape == (6,)
    assert np.allclose(
        lengths,
        np.sqrt(8.0 / 3.0),
        atol=1.0e-12,
    )


def test_unit_circumradius_volume() -> None:
    vertices = regular_tetrahedron()
    expected = 8.0 / (9.0 * np.sqrt(3.0))

    assert tetrahedron_volume(vertices) == pytest.approx(
        expected,
        abs=1.0e-12,
    )


def test_scaling_changes_length_and_volume_correctly() -> None:
    scale = 2.5
    vertices = regular_tetrahedron(circumradius=scale)

    expected_edge = scale * np.sqrt(8.0 / 3.0)
    expected_volume = scale**3 * 8.0 / (9.0 * np.sqrt(3.0))

    assert np.allclose(
        tetrahedron_edge_lengths(vertices),
        expected_edge,
        atol=1.0e-12,
    )
    assert tetrahedron_volume(vertices) == pytest.approx(
        expected_volume,
        abs=1.0e-12,
    )


@pytest.mark.parametrize(
    "circumradius",
    [0.0, -1.0, np.inf, np.nan],
)
def test_invalid_circumradius_raises(
    circumradius: float,
) -> None:
    with pytest.raises(ValueError):
        regular_tetrahedron(circumradius=circumradius)


@pytest.mark.parametrize(
    "vertices",
    [
        np.zeros((3, 3)),
        np.zeros((4, 2)),
        np.full((4, 3), np.nan),
    ],
)
def test_invalid_vertex_arrays_raise(
    vertices: np.ndarray,
) -> None:
    with pytest.raises(ValueError):
        tetrahedron_edge_lengths(vertices)
