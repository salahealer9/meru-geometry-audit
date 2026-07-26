"""Projection operations for three-dimensional geometry."""

from __future__ import annotations

from collections.abc import Sequence

import numpy as np
from numpy.typing import NDArray

from meru_geometry.rotations import apply_rotation, is_rotation_matrix


def orthographic_project(
    points: NDArray[np.float64],
    rotation: NDArray[np.float64] | None = None,
    axes: Sequence[int] = (0, 1),
) -> NDArray[np.float64]:
    """Orthographically project 3D points onto two coordinate axes.

    Parameters
    ----------
    points:
        Array whose final dimension is three.
    rotation:
        Optional active rotation applied before projection.
    axes:
        Two distinct coordinate indices retained after rotation. The default
        ``(0, 1)`` projects onto the xy-plane.

    Returns
    -------
    numpy.ndarray
        Array with the same leading dimensions as ``points`` and final
        dimension two.
    """
    point_array = np.asarray(points, dtype=np.float64)

    if point_array.ndim < 1 or point_array.shape[-1] != 3:
        raise ValueError("points must have final dimension 3.")
    if not np.isfinite(point_array).all():
        raise ValueError("points must contain only finite values.")

    axis_tuple = tuple(axes)

    if len(axis_tuple) != 2:
        raise ValueError("axes must contain exactly two indices.")
    if any(not isinstance(axis, (int, np.integer)) for axis in axis_tuple):
        raise ValueError("axes must contain integer indices.")
    if axis_tuple[0] == axis_tuple[1]:
        raise ValueError("axes must be distinct.")
    if any(axis not in (0, 1, 2) for axis in axis_tuple):
        raise ValueError("axes must be selected from 0, 1, and 2.")

    transformed = point_array

    if rotation is not None:
        rotation_array = np.asarray(rotation, dtype=np.float64)

        if not is_rotation_matrix(rotation_array):
            raise ValueError(
                "rotation must be a proper 3D rotation matrix."
            )

        transformed = apply_rotation(
            point_array,
            rotation_array,
        )

    return transformed[..., list(axis_tuple)]
