"""Planar reciprocal-spiral geometry."""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray


def reciprocal_spiral(
    theta_min: float = 0.4,
    theta_max: float = 4.0 * np.pi,
    n_points: int = 2000,
    scale: float = 1.0,
) -> NDArray[np.float64]:
    """Sample the planar reciprocal spiral ``r = scale / theta``.

    The default angular interval is only a mathematical baseline. It is not
    currently claimed to reproduce Stan Tenen's exact model.

    Parameters
    ----------
    theta_min:
        Lower angular bound in radians. It must be strictly positive because
        the reciprocal spiral is singular at theta = 0.
    theta_max:
        Upper angular bound in radians.
    n_points:
        Number of sampled points.
    scale:
        Positive radial scale ``a`` in ``r = a / theta``.

    Returns
    -------
    numpy.ndarray
        Array of shape ``(n_points, 2)`` containing Cartesian coordinates.

    Raises
    ------
    ValueError
        If any parameter lies outside its permitted range.
    """
    if theta_min <= 0.0:
        raise ValueError("theta_min must be positive.")
    if theta_max <= theta_min:
        raise ValueError("theta_max must exceed theta_min.")
    if n_points < 2:
        raise ValueError("n_points must be at least 2.")
    if scale <= 0.0:
        raise ValueError("scale must be positive.")

    theta = np.linspace(theta_min, theta_max, n_points, dtype=np.float64)
    radius = scale / theta

    x = radius * np.cos(theta)
    y = radius * np.sin(theta)

    return np.column_stack((x, y))
