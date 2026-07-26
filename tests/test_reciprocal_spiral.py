"""Tests for the reciprocal-spiral baseline."""

from __future__ import annotations

import numpy as np
import pytest

from meru_geometry.reciprocal_spiral import reciprocal_spiral


def test_reciprocal_spiral_shape() -> None:
    points = reciprocal_spiral(n_points=100)
    assert points.shape == (100, 2)


def test_reciprocal_spiral_values_are_finite() -> None:
    points = reciprocal_spiral()
    assert np.isfinite(points).all()


def test_initial_radius_matches_definition() -> None:
    theta_min = 0.5
    scale = 2.0

    points = reciprocal_spiral(
        theta_min=theta_min,
        theta_max=2.0,
        n_points=10,
        scale=scale,
    )

    measured_radius = np.linalg.norm(points[0])
    expected_radius = scale / theta_min

    assert measured_radius == pytest.approx(expected_radius)


@pytest.mark.parametrize(
    ("kwargs", "message"),
    [
        ({"theta_min": 0.0}, "theta_min must be positive"),
        ({"theta_min": -1.0}, "theta_min must be positive"),
        (
            {"theta_min": 2.0, "theta_max": 1.0},
            "theta_max must exceed theta_min",
        ),
        ({"n_points": 1}, "n_points must be at least 2"),
        ({"scale": 0.0}, "scale must be positive"),
    ],
)
def test_invalid_parameters_raise_value_error(
    kwargs: dict[str, float | int],
    message: str,
) -> None:
    with pytest.raises(ValueError, match=message):
        reciprocal_spiral(**kwargs)
