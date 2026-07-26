"""Tests for orthographic projection."""

from __future__ import annotations

import numpy as np
import pytest

from meru_geometry.projections import orthographic_project


def test_default_projection_drops_z_coordinate() -> None:
    points = np.asarray(
        [
            [1.0, 2.0, 3.0],
            [-4.0, 5.0, -6.0],
        ]
    )

    projected = orthographic_project(points)

    assert np.array_equal(
        projected,
        np.asarray(
            [
                [1.0, 2.0],
                [-4.0, 5.0],
            ]
        ),
    )


def test_rotation_is_applied_before_projection() -> None:
    points = np.asarray([[1.0, 2.0, 3.0]])

    rotation = np.asarray(
        [
            [0.0, -1.0, 0.0],
            [1.0, 0.0, 0.0],
            [0.0, 0.0, 1.0],
        ]
    )

    projected = orthographic_project(
        points,
        rotation=rotation,
    )

    assert np.allclose(
        projected,
        np.asarray([[-2.0, 1.0]]),
        atol=1.0e-12,
    )


def test_alternative_projection_axes() -> None:
    points = np.asarray([[1.0, 2.0, 3.0]])

    projected = orthographic_project(
        points,
        axes=(2, 0),
    )

    assert np.array_equal(
        projected,
        np.asarray([[3.0, 1.0]]),
    )


@pytest.mark.parametrize(
    "points",
    [
        np.zeros((2, 2)),
        np.zeros((2, 4)),
        np.full((2, 3), np.nan),
    ],
)
def test_invalid_point_arrays_raise(
    points: np.ndarray,
) -> None:
    with pytest.raises(ValueError):
        orthographic_project(points)


@pytest.mark.parametrize(
    "axes",
    [
        (0,),
        (0, 1, 2),
        (0, 0),
        (0, 3),
        ("x", "y"),
    ],
)
def test_invalid_axes_raise(
    axes: tuple[object, ...],
) -> None:
    with pytest.raises(ValueError):
        orthographic_project(
            np.zeros((2, 3)),
            axes=axes,
        )


def test_improper_rotation_raises() -> None:
    reflection = np.diag([1.0, 1.0, -1.0])

    with pytest.raises(ValueError):
        orthographic_project(
            np.zeros((2, 3)),
            rotation=reflection,
        )
