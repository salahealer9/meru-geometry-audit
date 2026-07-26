"""Tests for canonical torus geometry and torus knots."""

from __future__ import annotations

import numpy as np
import pytest

from meru_geometry.torus import (
    torus_implicit_residual,
    torus_knot,
    torus_surface,
)


def test_torus_surface_scalar_shape() -> None:
    point = torus_surface(0.0, 0.0)

    assert point.shape == (3,)
    assert np.allclose(
        point,
        np.asarray([2.75, 0.0, 0.0]),
        atol=1.0e-12,
    )


def test_torus_surface_broadcast_shape() -> None:
    u = np.linspace(0.0, 2.0 * np.pi, 7)[:, None]
    v = np.linspace(0.0, 2.0 * np.pi, 5)[None, :]

    points = torus_surface(u, v)

    assert points.shape == (7, 5, 3)


def test_parametric_points_satisfy_implicit_equation() -> None:
    u = np.linspace(0.0, 2.0 * np.pi, 37)
    v = np.linspace(-np.pi, np.pi, 37)

    points = torus_surface(
        u,
        v,
        major_radius=2.4,
        minor_radius=0.6,
    )

    residual = torus_implicit_residual(
        points,
        major_radius=2.4,
        minor_radius=0.6,
    )

    assert np.max(np.abs(residual)) < 1.0e-12


def test_3_10_torus_knot_is_closed() -> None:
    points = torus_knot(3, 10, n_points=4001)

    assert points.shape == (4001, 3)
    assert np.allclose(
        points[0],
        points[-1],
        atol=1.0e-12,
        rtol=0.0,
    )


def test_3_10_torus_knot_lies_on_torus() -> None:
    points = torus_knot(
        3,
        10,
        major_radius=2.25,
        minor_radius=0.55,
    )

    residual = torus_implicit_residual(
        points,
        major_radius=2.25,
        minor_radius=0.55,
    )

    assert np.max(np.abs(residual)) < 1.0e-12


def test_open_sampling_does_not_duplicate_endpoint() -> None:
    points = torus_knot(
        3,
        10,
        n_points=1000,
        endpoint=False,
    )

    assert not np.allclose(
        points[0],
        points[-1],
        atol=1.0e-10,
        rtol=0.0,
    )


@pytest.mark.parametrize(
    ("major_radius", "minor_radius"),
    [
        (0.0, 0.5),
        (-1.0, 0.5),
        (1.0, 0.0),
        (1.0, -0.5),
        (1.0, 1.0),
        (0.5, 1.0),
        (np.inf, 0.5),
        (2.0, np.nan),
    ],
)
def test_invalid_torus_radii_raise(
    major_radius: float,
    minor_radius: float,
) -> None:
    with pytest.raises(ValueError):
        torus_surface(
            0.0,
            0.0,
            major_radius=major_radius,
            minor_radius=minor_radius,
        )


@pytest.mark.parametrize(
    ("p", "q"),
    [
        (0, 1),
        (-1, 3),
        (3, 0),
        (3.5, 10),
        (True, 10),
    ],
)
def test_invalid_winding_numbers_raise(
    p: object,
    q: object,
) -> None:
    with pytest.raises(ValueError):
        torus_knot(p, q)  # type: ignore[arg-type]


def test_non_coprime_winding_numbers_raise() -> None:
    with pytest.raises(
        ValueError,
        match="must be coprime",
    ):
        torus_knot(4, 10)


@pytest.mark.parametrize(
    "n_points",
    [0, 1, 2.5, True],
)
def test_invalid_sample_count_raises(
    n_points: object,
) -> None:
    with pytest.raises(ValueError):
        torus_knot(
            3,
            10,
            n_points=n_points,  # type: ignore[arg-type]
        )


def test_invalid_implicit_point_array_raises() -> None:
    with pytest.raises(ValueError):
        torus_implicit_residual(np.zeros((5, 2)))
