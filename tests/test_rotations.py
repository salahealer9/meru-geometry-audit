"""Tests for tetrahedral rotational symmetry."""

from __future__ import annotations

import numpy as np
import pytest

from meru_geometry.rotations import (
    apply_rotation,
    is_rotation_matrix,
    tetrahedral_rotation_group,
    tetrahedral_rotation_permutations,
)
from meru_geometry.tetrahedron import regular_tetrahedron


def permutation_parity(permutation: tuple[int, ...]) -> int:
    """Return zero for even and one for odd permutations."""
    inversions = sum(
        permutation[i] > permutation[j]
        for i in range(len(permutation))
        for j in range(i + 1, len(permutation))
    )
    return inversions % 2


def test_tetrahedral_group_has_order_twelve() -> None:
    rotations = tetrahedral_rotation_group()
    permutations = tetrahedral_rotation_permutations()

    assert rotations.shape == (12, 3, 3)
    assert len(permutations) == 12


def test_all_matrices_are_proper_rotations() -> None:
    rotations = tetrahedral_rotation_group()

    assert all(
        is_rotation_matrix(rotation)
        for rotation in rotations
    )


def test_all_permutations_are_even() -> None:
    permutations = tetrahedral_rotation_permutations()

    assert all(
        permutation_parity(permutation) == 0
        for permutation in permutations
    )


def test_rotations_realise_recorded_vertex_permutations() -> None:
    vertices = regular_tetrahedron()
    rotations = tetrahedral_rotation_group()
    permutations = tetrahedral_rotation_permutations()

    for rotation, permutation in zip(
        rotations,
        permutations,
        strict=True,
    ):
        mapped = apply_rotation(vertices, rotation)
        expected = vertices[np.asarray(permutation)]

        assert np.allclose(
            mapped,
            expected,
            atol=1.0e-10,
            rtol=0.0,
        )


def test_identity_rotation_is_present_and_first() -> None:
    rotations = tetrahedral_rotation_group()

    assert np.allclose(
        rotations[0],
        np.eye(3),
        atol=1.0e-12,
        rtol=0.0,
    )


def test_rotation_group_is_closed() -> None:
    rotations = tetrahedral_rotation_group()

    for left in rotations:
        for right in rotations:
            product = left @ right

            assert any(
                np.allclose(
                    product,
                    candidate,
                    atol=1.0e-10,
                    rtol=0.0,
                )
                for candidate in rotations
            )


def test_rotation_group_contains_twelve_unique_matrices() -> None:
    rotations = tetrahedral_rotation_group()

    for i in range(len(rotations)):
        for j in range(i + 1, len(rotations)):
            assert not np.allclose(
                rotations[i],
                rotations[j],
                atol=1.0e-10,
                rtol=0.0,
            )


def test_apply_rotation_preserves_norms() -> None:
    points = np.asarray(
        [
            [0.13, -0.27, 0.41],
            [-0.52, 0.18, 0.07],
        ]
    )

    for rotation in tetrahedral_rotation_group():
        rotated = apply_rotation(points, rotation)

        assert np.allclose(
            np.linalg.norm(rotated, axis=1),
            np.linalg.norm(points, axis=1),
            atol=1.0e-12,
        )


def test_reflection_is_not_a_rotation() -> None:
    reflection = np.diag([1.0, 1.0, -1.0])
    assert not is_rotation_matrix(reflection)


def test_invalid_rotation_application_raises() -> None:
    with pytest.raises(ValueError):
        apply_rotation(
            np.zeros((4, 3)),
            np.diag([1.0, 1.0, -1.0]),
        )
