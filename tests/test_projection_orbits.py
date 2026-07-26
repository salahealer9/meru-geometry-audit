"""Tests for camera-direction and projection-orbit analysis."""

from __future__ import annotations

import numpy as np
import pytest

from meru_geometry.projection_orbits import (
    best_curve_alignment,
    camera_direction,
    camera_direction_classes,
    equivalence_classes_from_errors,
    frame_planar_transform,
    planar_similarity_alignment,
)
from meru_geometry.projections import orthographic_project
from meru_geometry.rotations import (
    apply_rotation,
    tetrahedral_rotation_group,
)


def planar_rotation(angle: float) -> np.ndarray:
    """Return a row-coordinate-compatible planar rotation matrix."""
    cosine = np.cos(angle)
    sine = np.sin(angle)

    return np.asarray(
        [
            [cosine, -sine],
            [sine, cosine],
        ]
    )


def test_tetrahedral_camera_orbit_has_six_signed_directions() -> None:
    rotations = tetrahedral_rotation_group()
    classes = camera_direction_classes(rotations)

    assert len(classes) == 6
    assert sorted(len(group) for group in classes) == [2] * 6


def test_tetrahedral_camera_orbit_has_three_unoriented_axes() -> None:
    rotations = tetrahedral_rotation_group()
    classes = camera_direction_classes(
        rotations,
        unoriented=True,
    )

    assert len(classes) == 3
    assert sorted(len(group) for group in classes) == [4] * 3


def test_camera_directions_are_coordinate_axis_directions() -> None:
    rotations = tetrahedral_rotation_group()

    expected = {
        (-1.0, 0.0, 0.0),
        (1.0, 0.0, 0.0),
        (0.0, -1.0, 0.0),
        (0.0, 1.0, 0.0),
        (0.0, 0.0, -1.0),
        (0.0, 0.0, 1.0),
    }

    measured = {
        tuple(camera_direction(rotation))
        for rotation in rotations
    }

    assert measured == expected


def test_same_signed_direction_gives_planar_rotation() -> None:
    rotations = tetrahedral_rotation_group()
    classes = camera_direction_classes(rotations)

    points = np.asarray(
        [
            [0.17, -0.32, 0.48],
            [-0.51, 0.23, 0.14],
            [0.29, 0.11, -0.37],
        ]
    )

    for group in classes:
        first, second = group

        transform = frame_planar_transform(
            rotations[first],
            rotations[second],
        )

        assert transform is not None
        assert np.linalg.det(transform) == pytest.approx(1.0)

        projected_first = orthographic_project(
            points,
            rotation=rotations[first],
        )
        projected_second = orthographic_project(
            points,
            rotation=rotations[second],
        )

        assert np.allclose(
            projected_first @ transform.T,
            projected_second,
            atol=1.0e-12,
            rtol=0.0,
        )


def test_same_unoriented_axis_gives_orthogonal_planar_transform() -> None:
    rotations = tetrahedral_rotation_group()
    classes = camera_direction_classes(
        rotations,
        unoriented=True,
    )

    points = np.asarray(
        [
            [0.17, -0.32, 0.48],
            [-0.51, 0.23, 0.14],
            [0.29, 0.11, -0.37],
        ]
    )

    for group in classes:
        for first in group:
            for second in group:
                transform = frame_planar_transform(
                    rotations[first],
                    rotations[second],
                )

                assert transform is not None
                assert abs(np.linalg.det(transform)) == pytest.approx(
                    1.0
                )

                projected_first = orthographic_project(
                    points,
                    rotation=rotations[first],
                )
                projected_second = orthographic_project(
                    points,
                    rotation=rotations[second],
                )

                assert np.allclose(
                    projected_first @ transform.T,
                    projected_second,
                    atol=1.0e-12,
                    rtol=0.0,
                )


def test_different_viewing_axes_have_no_frame_planar_transform() -> None:
    rotations = tetrahedral_rotation_group()
    axis_classes = camera_direction_classes(
        rotations,
        unoriented=True,
    )

    first = axis_classes[0][0]
    second = axis_classes[1][0]

    assert (
        frame_planar_transform(
            rotations[first],
            rotations[second],
        )
        is None
    )


def test_similarity_alignment_recovers_rotation_scale_translation() -> None:
    source = np.asarray(
        [
            [-0.7, -0.2],
            [0.4, -0.5],
            [0.9, 0.3],
            [-0.1, 0.8],
        ]
    )

    rotation = planar_rotation(0.43)
    scale = 1.7
    translation = np.asarray([0.35, -0.61])

    target = scale * (source @ rotation) + translation

    alignment = planar_similarity_alignment(
        source,
        target,
        allow_reflection=False,
        allow_scale=True,
    )

    assert alignment.relative_rms < 1.0e-12
    assert alignment.scale == pytest.approx(scale)
    assert np.allclose(
        alignment.orthogonal_matrix,
        rotation,
        atol=1.0e-12,
        rtol=0.0,
    )
    assert np.allclose(
        alignment.translation,
        translation,
        atol=1.0e-12,
        rtol=0.0,
    )
    assert not alignment.reflection_used


def test_reflection_requires_o2_alignment() -> None:
    source = np.asarray(
        [
            [-0.9, -0.4],
            [0.6, -0.3],
            [0.8, 0.7],
            [-0.2, 0.9],
        ]
    )

    reflection = np.diag([-1.0, 1.0])
    target = source @ reflection + np.asarray([0.2, -0.3])

    so2_alignment = planar_similarity_alignment(
        source,
        target,
        allow_reflection=False,
    )
    o2_alignment = planar_similarity_alignment(
        source,
        target,
        allow_reflection=True,
    )

    assert so2_alignment.relative_rms > 1.0e-3
    assert o2_alignment.relative_rms < 1.0e-12
    assert o2_alignment.reflection_used


def test_closed_curve_alignment_recovers_shift_and_reversal() -> None:
    parameter = np.linspace(
        0.0,
        2.0 * np.pi,
        64,
        endpoint=False,
    )

    source = np.column_stack(
        (
            np.cos(parameter)
            + 0.17 * np.cos(3.0 * parameter),
            0.73 * np.sin(parameter)
            + 0.11 * np.sin(2.0 * parameter),
        )
    )

    transformed = np.roll(
        source[::-1],
        13,
        axis=0,
    )

    transformed = (
        1.25
        * (
            transformed
            @ planar_rotation(0.31)
        )
        + np.asarray([0.4, -0.2])
    )

    alignment = best_curve_alignment(
        source,
        transformed,
        closed=True,
        allow_reversal=True,
        allow_reflection=False,
        allow_scale=True,
    )

    assert alignment.relative_rms < 1.0e-12
    assert alignment.reversed_order


def test_equivalence_classes_from_error_matrix() -> None:
    errors = np.asarray(
        [
            [0.0, 1.0e-12, 0.4, 0.5],
            [1.0e-12, 0.0, 0.3, 0.4],
            [0.4, 0.3, 0.0, 2.0e-12],
            [0.5, 0.4, 2.0e-12, 0.0],
        ]
    )

    classes = equivalence_classes_from_errors(
        errors,
        tolerance=1.0e-8,
    )

    assert classes == ((0, 1), (2, 3))


def test_invalid_camera_rotation_raises() -> None:
    with pytest.raises(ValueError):
        camera_direction(
            np.diag([1.0, 1.0, -1.0])
        )


def test_apply_rotation_still_preserves_camera_test_points() -> None:
    rotations = tetrahedral_rotation_group()
    point = np.asarray([[0.2, -0.3, 0.7]])

    for rotation in rotations:
        rotated = apply_rotation(point, rotation)
        assert np.linalg.norm(rotated) == pytest.approx(
            np.linalg.norm(point)
        )


def test_rotation_only_alignment_handles_zero_scale_boundary() -> None:
    """A symmetric reflected target can have zero SO(2) correlation."""
    source = np.asarray(
        [
            [1.0, 0.0],
            [0.0, 1.0],
            [-1.0, 0.0],
            [0.0, -1.0],
        ]
    )

    target = source @ np.diag([-1.0, 1.0])

    alignment = planar_similarity_alignment(
        source,
        target,
        allow_reflection=False,
        allow_scale=True,
    )

    assert alignment.scale == pytest.approx(
        0.0,
        abs=1.0e-15,
    )
    assert alignment.relative_rms == pytest.approx(
        1.0,
        abs=1.0e-12,
    )
    assert not alignment.reflection_used

    reflected_alignment = planar_similarity_alignment(
        source,
        target,
        allow_reflection=True,
        allow_scale=True,
    )

    assert reflected_alignment.relative_rms < 1.0e-12
    assert reflected_alignment.scale == pytest.approx(1.0)
    assert reflected_alignment.reflection_used
