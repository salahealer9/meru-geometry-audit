"""Tests for explicitly labelled candidate embeddings."""

from __future__ import annotations

import numpy as np
import pytest

from meru_geometry.embeddings import (
    candidate_reciprocal_torus_embedding,
)
from meru_geometry.torus import torus_implicit_residual


def test_candidate_array_shapes() -> None:
    candidate = candidate_reciprocal_torus_embedding(
        n_points=500,
    )

    assert candidate.theta.shape == (500,)
    assert candidate.reciprocal_radius.shape == (500,)
    assert candidate.radial_progress.shape == (500,)
    assert candidate.u.shape == (500,)
    assert candidate.v.shape == (500,)
    assert candidate.points.shape == (500, 3)


def test_default_candidate_has_one_and_a_half_toroidal_turns() -> None:
    candidate = candidate_reciprocal_torus_embedding()

    expected_span = 3.0 * np.pi

    assert candidate.theta[-1] - candidate.theta[0] == pytest.approx(
        expected_span
    )
    assert candidate.u[-1] - candidate.u[0] == pytest.approx(
        expected_span
    )


def test_reciprocal_radius_matches_definition() -> None:
    scale = 2.5

    candidate = candidate_reciprocal_torus_embedding(
        scale=scale,
    )

    assert np.allclose(
        candidate.reciprocal_radius,
        scale / candidate.theta,
        atol=1.0e-12,
    )


def test_reciprocal_radius_decreases_monotonically() -> None:
    candidate = candidate_reciprocal_torus_embedding()

    assert np.all(
        np.diff(candidate.reciprocal_radius) < 0.0
    )


def test_radial_progress_runs_from_zero_to_one() -> None:
    candidate = candidate_reciprocal_torus_embedding()

    assert candidate.radial_progress[0] == pytest.approx(0.0)
    assert candidate.radial_progress[-1] == pytest.approx(1.0)
    assert np.all(np.diff(candidate.radial_progress) > 0.0)


def test_poloidal_span_matches_requested_turn_count() -> None:
    candidate = candidate_reciprocal_torus_embedding(
        poloidal_turns=2.25,
    )

    assert candidate.v[-1] - candidate.v[0] == pytest.approx(
        2.0 * np.pi * 2.25
    )


def test_candidate_points_lie_on_canonical_torus() -> None:
    candidate = candidate_reciprocal_torus_embedding(
        major_radius=2.3,
        minor_radius=0.65,
    )

    residual = torus_implicit_residual(
        candidate.points,
        major_radius=2.3,
        minor_radius=0.65,
    )

    assert np.max(np.abs(residual)) < 1.0e-12


def test_phases_shift_parameter_angles() -> None:
    phase_u = 0.37
    phase_v = -0.28

    candidate = candidate_reciprocal_torus_embedding(
        phase_u=phase_u,
        phase_v=phase_v,
    )

    assert candidate.u[0] == pytest.approx(phase_u)
    assert candidate.v[0] == pytest.approx(phase_v)


@pytest.mark.parametrize(
    "kwargs",
    [
        {"theta_start": 0.0},
        {"theta_start": -0.5},
        {"toroidal_turns": 0.0},
        {"poloidal_turns": 0.0},
        {"scale": 0.0},
        {"major_radius": 0.5, "minor_radius": 0.75},
        {"minor_radius": 0.0},
        {"n_points": 1},
        {"n_points": 2.5},
        {"phase_u": np.inf},
    ],
)
def test_invalid_candidate_parameters_raise(
    kwargs: dict[str, object],
) -> None:
    with pytest.raises(ValueError):
        candidate_reciprocal_torus_embedding(
            **kwargs,  # type: ignore[arg-type]
        )
