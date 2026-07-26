"""Canonical torus surfaces and coprime torus knots."""

from __future__ import annotations

from math import gcd
from numbers import Integral

import numpy as np
from numpy.typing import ArrayLike, NDArray


def _validate_radii(
    major_radius: float,
    minor_radius: float,
) -> tuple[float, float]:
    """Validate and return the radii of a canonical ring torus."""
    major = float(major_radius)
    minor = float(minor_radius)

    if not np.isfinite(major):
        raise ValueError("major_radius must be finite.")
    if not np.isfinite(minor):
        raise ValueError("minor_radius must be finite.")
    if major <= 0.0:
        raise ValueError("major_radius must be positive.")
    if minor <= 0.0:
        raise ValueError("minor_radius must be positive.")
    if major <= minor:
        raise ValueError(
            "major_radius must exceed minor_radius for a ring torus."
        )

    return major, minor


def torus_surface(
    u: ArrayLike,
    v: ArrayLike,
    major_radius: float = 2.0,
    minor_radius: float = 0.75,
) -> NDArray[np.float64]:
    """Evaluate the canonical ring-torus parametrisation.

    Parameters
    ----------
    u:
        Toroidal longitude angle or array of angles.
    v:
        Poloidal tube angle or array of angles. The inputs are broadcast
        against one another.
    major_radius:
        Distance from the origin to the centre of the tube.
    minor_radius:
        Radius of the tube.

    Returns
    -------
    numpy.ndarray
        Array with final dimension three.
    """
    major, minor = _validate_radii(
        major_radius,
        minor_radius,
    )

    u_array = np.asarray(u, dtype=np.float64)
    v_array = np.asarray(v, dtype=np.float64)

    if not np.isfinite(u_array).all():
        raise ValueError("u must contain only finite values.")
    if not np.isfinite(v_array).all():
        raise ValueError("v must contain only finite values.")

    u_broadcast, v_broadcast = np.broadcast_arrays(
        u_array,
        v_array,
    )

    radial_distance = major + minor * np.cos(v_broadcast)

    x = radial_distance * np.cos(u_broadcast)
    y = radial_distance * np.sin(u_broadcast)
    z = minor * np.sin(v_broadcast)

    return np.stack((x, y, z), axis=-1)


def torus_implicit_residual(
    points: ArrayLike,
    major_radius: float = 2.0,
    minor_radius: float = 0.75,
) -> NDArray[np.float64]:
    """Evaluate the canonical torus implicit-equation residual.

    Points exactly on the torus have residual zero:

    ``(sqrt(x**2 + y**2) - R)**2 + z**2 - r**2 = 0``.
    """
    major, minor = _validate_radii(
        major_radius,
        minor_radius,
    )

    point_array = np.asarray(points, dtype=np.float64)

    if point_array.ndim < 1 or point_array.shape[-1] != 3:
        raise ValueError("points must have final dimension 3.")
    if not np.isfinite(point_array).all():
        raise ValueError("points must contain only finite values.")

    cylindrical_radius = np.hypot(
        point_array[..., 0],
        point_array[..., 1],
    )

    return (
        (cylindrical_radius - major) ** 2
        + point_array[..., 2] ** 2
        - minor**2
    )


def _validate_winding_number(
    value: int,
    name: str,
) -> int:
    """Validate a positive integer winding number."""
    if isinstance(value, bool) or not isinstance(value, Integral):
        raise ValueError(f"{name} must be a positive integer.")

    integer = int(value)

    if integer <= 0:
        raise ValueError(f"{name} must be a positive integer.")

    return integer


def torus_knot(
    p: int,
    q: int,
    major_radius: float = 2.0,
    minor_radius: float = 0.75,
    n_points: int = 4001,
    phase_u: float = 0.0,
    phase_v: float = 0.0,
    endpoint: bool = True,
) -> NDArray[np.float64]:
    """Sample a coprime ``(p, q)`` torus knot.

    The convention is

    ``u = p*t + phase_u``

    and

    ``v = q*t + phase_v``

    for ``0 <= t <= 2*pi``.

    Non-coprime winding numbers are rejected because they describe torus-link
    structure rather than a single knot under the usual terminology.
    """
    p_integer = _validate_winding_number(p, "p")
    q_integer = _validate_winding_number(q, "q")
    _validate_radii(major_radius, minor_radius)

    if gcd(p_integer, q_integer) != 1:
        raise ValueError("p and q must be coprime for a single torus knot.")

    if isinstance(n_points, bool) or not isinstance(n_points, Integral):
        raise ValueError("n_points must be an integer.")
    if n_points < 2:
        raise ValueError("n_points must be at least 2.")
    if not np.isfinite(phase_u):
        raise ValueError("phase_u must be finite.")
    if not np.isfinite(phase_v):
        raise ValueError("phase_v must be finite.")

    parameter = np.linspace(
        0.0,
        2.0 * np.pi,
        int(n_points),
        endpoint=endpoint,
        dtype=np.float64,
    )

    u = p_integer * parameter + phase_u
    v = q_integer * parameter + phase_v

    return torus_surface(
        u,
        v,
        major_radius=major_radius,
        minor_radius=minor_radius,
    )
