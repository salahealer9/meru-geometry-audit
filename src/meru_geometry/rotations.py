"""Three-dimensional rotations and tetrahedral symmetry."""

from __future__ import annotations

from itertools import permutations
from typing import Sequence

import numpy as np
from numpy.typing import NDArray

from meru_geometry.tetrahedron import regular_tetrahedron


Permutation = tuple[int, int, int, int]


def is_rotation_matrix(
    matrix: NDArray[np.float64],
    tolerance: float = 1.0e-10,
) -> bool:
    """Return whether a matrix is a proper three-dimensional rotation."""
    array = np.asarray(matrix, dtype=np.float64)

    if array.shape != (3, 3):
        return False
    if not np.isfinite(array).all():
        return False
    if tolerance <= 0.0:
        raise ValueError("tolerance must be positive.")

    orthogonality_error = np.max(
        np.abs(array.T @ array - np.eye(3))
    )
    determinant_error = abs(np.linalg.det(array) - 1.0)

    return bool(
        orthogonality_error <= tolerance
        and determinant_error <= tolerance
    )


def apply_rotation(
    points: NDArray[np.float64],
    rotation: NDArray[np.float64],
) -> NDArray[np.float64]:
    """Apply an active rotation to one or more row-vector points."""
    point_array = np.asarray(points, dtype=np.float64)
    rotation_array = np.asarray(rotation, dtype=np.float64)

    if point_array.ndim < 1 or point_array.shape[-1] != 3:
        raise ValueError("points must have final dimension 3.")
    if not np.isfinite(point_array).all():
        raise ValueError("points must contain only finite values.")
    if not is_rotation_matrix(rotation_array):
        raise ValueError("rotation must be a proper 3D rotation matrix.")

    return point_array @ rotation_array.T


def _rotation_for_permutation(
    vertices: NDArray[np.float64],
    permutation: Sequence[int],
) -> NDArray[np.float64]:
    """Construct the linear map associated with a vertex permutation."""
    target = vertices[np.asarray(permutation, dtype=np.int64)]

    gram = vertices.T @ vertices
    rotation_transpose = np.linalg.solve(
        gram,
        vertices.T @ target,
    )

    return rotation_transpose.T


def _build_tetrahedral_rotation_group(
    tolerance: float,
) -> tuple[NDArray[np.float64], tuple[Permutation, ...]]:
    """Construct all proper rotations and their vertex permutations."""
    if tolerance <= 0.0:
        raise ValueError("tolerance must be positive.")

    vertices = regular_tetrahedron()

    matrices: list[NDArray[np.float64]] = []
    accepted_permutations: list[Permutation] = []

    for candidate in permutations(range(4)):
        permutation: Permutation = (
            candidate[0],
            candidate[1],
            candidate[2],
            candidate[3],
        )

        rotation = _rotation_for_permutation(
            vertices,
            permutation,
        )

        if not is_rotation_matrix(rotation, tolerance):
            continue

        mapped = apply_rotation(vertices, rotation)
        target = vertices[np.asarray(permutation)]

        if not np.allclose(
            mapped,
            target,
            atol=tolerance,
            rtol=0.0,
        ):
            continue

        duplicate = any(
            np.allclose(
                rotation,
                existing,
                atol=tolerance,
                rtol=0.0,
            )
            for existing in matrices
        )

        if duplicate:
            continue

        matrices.append(rotation)
        accepted_permutations.append(permutation)

    if len(matrices) != 12:
        raise RuntimeError(
            "Expected 12 tetrahedral proper rotations, "
            f"but constructed {len(matrices)}."
        )

    return (
        np.stack(matrices, axis=0),
        tuple(accepted_permutations),
    )


def tetrahedral_rotation_group(
    tolerance: float = 1.0e-10,
) -> NDArray[np.float64]:
    """Return the 12 proper rotational symmetries of a tetrahedron.

    Returns
    -------
    numpy.ndarray
        Array of shape ``(12, 3, 3)``.

    Notes
    -----
    The identity rotation is first because permutations are examined in
    lexicographic order.
    """
    matrices, _ = _build_tetrahedral_rotation_group(tolerance)
    return matrices


def tetrahedral_rotation_permutations(
    tolerance: float = 1.0e-10,
) -> tuple[Permutation, ...]:
    """Return the vertex permutations induced by the 12 rotations."""
    _, accepted_permutations = _build_tetrahedral_rotation_group(
        tolerance
    )
    return accepted_permutations
