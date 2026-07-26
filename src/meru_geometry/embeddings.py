"""Explicitly labelled candidate curve embeddings."""

from __future__ import annotations

from typing import NamedTuple

import numpy as np
from numpy.typing import NDArray

from meru_geometry.torus import torus_surface


class ReciprocalTorusCandidate(NamedTuple):
    """Sampled data for the C0 reciprocal-to-torus candidate."""

    theta: NDArray[np.float64]
    reciprocal_radius: NDArray[np.float64]
    radial_progress: NDArray[np.float64]
    u: NDArray[np.float64]
    v: NDArray[np.float64]
    points: NDArray[np.float64]


def candidate_reciprocal_torus_embedding(
    theta_start: float = 0.5,
    toroidal_turns: float = 1.5,
    poloidal_turns: float = 1.0,
    scale: float = 1.0,
    major_radius: float = 2.0,
    minor_radius: float = 0.75,
    n_points: int = 3000,
    phase_u: float = 0.0,
    phase_v: float = 0.0,
) -> ReciprocalTorusCandidate:
    """Construct candidate C0 for mapping ``r = scale/theta`` to a torus.

    This is an inferred baseline, not a faithful reconstruction of Tenen's
    three-dimensional vortex.

    The toroidal angle advances linearly with theta. The reciprocal radius is
    normalised from zero to one and mapped to the poloidal angle.
    """
    scalar_values = {
        "theta_start": theta_start,
        "toroidal_turns": toroidal_turns,
        "poloidal_turns": poloidal_turns,
        "scale": scale,
        "major_radius": major_radius,
        "minor_radius": minor_radius,
        "phase_u": phase_u,
        "phase_v": phase_v,
    }

    for name, value in scalar_values.items():
        if not np.isfinite(value):
            raise ValueError(f"{name} must be finite.")

    if theta_start <= 0.0:
        raise ValueError("theta_start must be positive.")
    if toroidal_turns <= 0.0:
        raise ValueError("toroidal_turns must be positive.")
    if poloidal_turns <= 0.0:
        raise ValueError("poloidal_turns must be positive.")
    if scale <= 0.0:
        raise ValueError("scale must be positive.")
    if major_radius <= minor_radius or minor_radius <= 0.0:
        raise ValueError(
            "major_radius must exceed a positive minor_radius."
        )
    if isinstance(n_points, bool) or not isinstance(n_points, int):
        raise ValueError("n_points must be an integer.")
    if n_points < 2:
        raise ValueError("n_points must be at least 2.")

    theta_end = (
        theta_start
        + 2.0 * np.pi * toroidal_turns
    )

    theta = np.linspace(
        theta_start,
        theta_end,
        n_points,
        dtype=np.float64,
    )

    reciprocal_radius = scale / theta

    radial_denominator = (
        reciprocal_radius[0]
        - reciprocal_radius[-1]
    )

    radial_progress = (
        reciprocal_radius[0]
        - reciprocal_radius
    ) / radial_denominator

    u = phase_u + theta - theta_start

    v = (
        phase_v
        + 2.0
        * np.pi
        * poloidal_turns
        * radial_progress
    )

    points = torus_surface(
        u,
        v,
        major_radius=major_radius,
        minor_radius=minor_radius,
    )

    return ReciprocalTorusCandidate(
        theta=theta,
        reciprocal_radius=reciprocal_radius,
        radial_progress=radial_progress,
        u=u,
        v=v,
        points=points,
    )
