"""Camera-direction and planar projection-orbit analysis."""

from __future__ import annotations

from typing import NamedTuple, Sequence

import numpy as np
from numpy.typing import ArrayLike, NDArray

from meru_geometry.rotations import is_rotation_matrix


class PlanarAlignment(NamedTuple):
    """Best planar similarity alignment between two curves."""

    relative_rms: float
    absolute_rms: float
    scale: float
    orthogonal_matrix: NDArray[np.float64]
    translation: NDArray[np.float64]
    shift: int
    reversed_order: bool
    reflection_used: bool


def _validate_points_2d(
    points: ArrayLike,
    name: str,
) -> NDArray[np.float64]:
    """Validate and return a finite two-dimensional point array."""
    array = np.asarray(points, dtype=np.float64)

    if array.ndim != 2 or array.shape[1] != 2:
        raise ValueError(f"{name} must have shape (n, 2).")
    if array.shape[0] < 2:
        raise ValueError(f"{name} must contain at least two points.")
    if not np.isfinite(array).all():
        raise ValueError(f"{name} must contain only finite values.")

    return array


def camera_direction(
    rotation: ArrayLike,
    tolerance: float = 1.0e-12,
) -> NDArray[np.float64]:
    """Return the original-coordinate viewing direction for a rotation.

    The object is actively rotated and then projected onto the xy-plane.
    Therefore the corresponding viewing direction in the original coordinate
    system is ``rotation.T @ [0, 0, 1]``.
    """
    rotation_array = np.asarray(rotation, dtype=np.float64)

    if tolerance <= 0.0:
        raise ValueError("tolerance must be positive.")
    if not is_rotation_matrix(rotation_array):
        raise ValueError("rotation must be a proper 3D rotation matrix.")

    direction = rotation_array.T @ np.asarray(
        [0.0, 0.0, 1.0],
        dtype=np.float64,
    )

    direction /= np.linalg.norm(direction)
    direction[np.abs(direction) < tolerance] = 0.0

    return direction


def camera_direction_classes(
    rotations: ArrayLike,
    unoriented: bool = False,
    tolerance: float = 1.0e-10,
) -> tuple[tuple[int, ...], ...]:
    """Group rotations by signed direction or unoriented viewing axis.

    Parameters
    ----------
    rotations:
        Array of shape ``(m, 3, 3)``.
    unoriented:
        When true, directions ``n`` and ``-n`` are placed in the same class.
    tolerance:
        Euclidean matching tolerance for unit directions.

    Returns
    -------
    tuple
        Classes containing zero-based rotation indices.
    """
    rotation_array = np.asarray(rotations, dtype=np.float64)

    if (
        rotation_array.ndim != 3
        or rotation_array.shape[1:] != (3, 3)
    ):
        raise ValueError("rotations must have shape (m, 3, 3).")
    if rotation_array.shape[0] < 1:
        raise ValueError("rotations must contain at least one matrix.")
    if tolerance <= 0.0:
        raise ValueError("tolerance must be positive.")

    directions = [
        camera_direction(rotation, tolerance=tolerance)
        for rotation in rotation_array
    ]

    representatives: list[NDArray[np.float64]] = []
    classes: list[list[int]] = []

    for index, direction in enumerate(directions):
        matched_class: int | None = None

        for class_index, representative in enumerate(representatives):
            direct_error = np.linalg.norm(
                direction - representative
            )

            if unoriented:
                reverse_error = np.linalg.norm(
                    direction + representative
                )
                match_error = min(direct_error, reverse_error)
            else:
                match_error = direct_error

            if match_error <= tolerance:
                matched_class = class_index
                break

        if matched_class is None:
            representatives.append(direction)
            classes.append([index])
        else:
            classes[matched_class].append(index)

    return tuple(tuple(group) for group in classes)


def frame_planar_transform(
    rotation_from: ArrayLike,
    rotation_to: ArrayLike,
    tolerance: float = 1.0e-10,
) -> NDArray[np.float64] | None:
    """Return the exact planar transform between compatible camera frames.

    The returned matrix ``Q`` satisfies

    ``projected_to = projected_from @ Q.T``

    whenever the two rotations correspond to the same signed camera direction
    or opposite directions along the same viewing axis.

    ``None`` is returned when the viewing axes differ.
    """
    from_array = np.asarray(rotation_from, dtype=np.float64)
    to_array = np.asarray(rotation_to, dtype=np.float64)

    if tolerance <= 0.0:
        raise ValueError("tolerance must be positive.")
    if not is_rotation_matrix(from_array):
        raise ValueError("rotation_from must be a proper rotation.")
    if not is_rotation_matrix(to_array):
        raise ValueError("rotation_to must be a proper rotation.")

    relative = to_array @ from_array.T

    mixing_error = max(
        float(np.max(np.abs(relative[:2, 2]))),
        float(np.max(np.abs(relative[2, :2]))),
    )

    if mixing_error > tolerance:
        return None

    if abs(abs(relative[2, 2]) - 1.0) > tolerance:
        return None

    planar = relative[:2, :2]

    if not np.allclose(
        planar.T @ planar,
        np.eye(2),
        atol=tolerance,
        rtol=0.0,
    ):
        return None

    return planar


def planar_similarity_alignment(
    source: ArrayLike,
    target: ArrayLike,
    allow_reflection: bool = False,
    allow_scale: bool = True,
) -> PlanarAlignment:
    """Align two equally sampled planar curves by similarity transform."""
    source_array = _validate_points_2d(source, "source")
    target_array = _validate_points_2d(target, "target")

    if source_array.shape != target_array.shape:
        raise ValueError("source and target must have the same shape.")

    source_mean = np.mean(source_array, axis=0)
    target_mean = np.mean(target_array, axis=0)

    source_centered = source_array - source_mean
    target_centered = target_array - target_mean

    source_energy = float(
        np.sum(source_centered * source_centered)
    )
    target_energy = float(
        np.sum(target_centered * target_centered)
    )

    if source_energy <= np.finfo(np.float64).eps:
        raise ValueError("source has zero centred extent.")
    if target_energy <= np.finfo(np.float64).eps:
        raise ValueError("target has zero centred extent.")

    cross_covariance = source_centered.T @ target_centered
    left, _, right_transpose = np.linalg.svd(
        cross_covariance
    )

    correction = np.eye(2)

    if (
        not allow_reflection
        and np.linalg.det(left @ right_transpose) < 0.0
    ):
        correction[-1, -1] = -1.0

    orthogonal = left @ correction @ right_transpose
    transformed_centered = source_centered @ orthogonal

    if allow_scale:
        denominator = float(
            np.sum(
                transformed_centered
                * transformed_centered
            )
        )
        numerator = float(
            np.sum(
                transformed_centered
                * target_centered
            )
        )
        unconstrained_scale = numerator / denominator

        # Under the non-negative similarity-scale constraint, an object pair
        # with zero or negative centred correlation has its optimum at the
        # boundary s = 0. This represents a non-match with relative RMS 1,
        # rather than an exceptional condition.
        scale = max(0.0, unconstrained_scale)
    else:
        scale = 1.0

    translation = (
        target_mean
        - scale * (source_mean @ orthogonal)
    )

    fitted = (
        scale * (source_array @ orthogonal)
        + translation
    )

    residual = fitted - target_array

    absolute_rms = float(
        np.sqrt(
            np.mean(
                np.sum(residual * residual, axis=1)
            )
        )
    )

    target_rms = float(
        np.sqrt(
            np.mean(
                np.sum(
                    target_centered * target_centered,
                    axis=1,
                )
            )
        )
    )

    relative_rms = absolute_rms / target_rms

    return PlanarAlignment(
        relative_rms=relative_rms,
        absolute_rms=absolute_rms,
        scale=float(scale),
        orthogonal_matrix=orthogonal,
        translation=translation,
        shift=0,
        reversed_order=False,
        reflection_used=bool(
            np.linalg.det(orthogonal) < 0.0
        ),
    )


def _strip_duplicate_endpoint(
    curve: NDArray[np.float64],
    tolerance: float,
) -> NDArray[np.float64]:
    """Remove a duplicated closing sample when present."""
    if np.linalg.norm(curve[0] - curve[-1]) <= tolerance:
        return curve[:-1]

    return curve


def best_curve_alignment(
    source: ArrayLike,
    target: ArrayLike,
    closed: bool = False,
    allow_reversal: bool = False,
    allow_reflection: bool = False,
    allow_scale: bool = True,
    endpoint_tolerance: float = 1.0e-10,
) -> PlanarAlignment:
    """Find the best permitted planar alignment of two sampled curves.

    Closed curves may be cyclically shifted. Reversal is optional.
    """
    if endpoint_tolerance <= 0.0:
        raise ValueError("endpoint_tolerance must be positive.")

    source_array = _validate_points_2d(source, "source")
    target_array = _validate_points_2d(target, "target")

    if closed:
        source_array = _strip_duplicate_endpoint(
            source_array,
            endpoint_tolerance,
        )
        target_array = _strip_duplicate_endpoint(
            target_array,
            endpoint_tolerance,
        )

    if source_array.shape != target_array.shape:
        raise ValueError(
            "source and target must have the same effective shape."
        )

    shift_values: Sequence[int]

    if closed:
        shift_values = range(source_array.shape[0])
    else:
        shift_values = (0,)

    reversal_values = (
        (False, True)
        if allow_reversal
        else (False,)
    )

    best: PlanarAlignment | None = None

    for reversed_order in reversal_values:
        candidate = (
            source_array[::-1]
            if reversed_order
            else source_array
        )

        for shift in shift_values:
            shifted = np.roll(
                candidate,
                shift,
                axis=0,
            )

            alignment = planar_similarity_alignment(
                shifted,
                target_array,
                allow_reflection=allow_reflection,
                allow_scale=allow_scale,
            )

            enriched = PlanarAlignment(
                relative_rms=alignment.relative_rms,
                absolute_rms=alignment.absolute_rms,
                scale=alignment.scale,
                orthogonal_matrix=alignment.orthogonal_matrix,
                translation=alignment.translation,
                shift=int(shift),
                reversed_order=reversed_order,
                reflection_used=alignment.reflection_used,
            )

            if (
                best is None
                or enriched.relative_rms < best.relative_rms
            ):
                best = enriched

    if best is None:
        raise RuntimeError("No alignment candidate was evaluated.")

    return best


def pairwise_curve_alignment_errors(
    curves: Sequence[ArrayLike],
    closed: bool = False,
    allow_reversal: bool = False,
    allow_reflection: bool = False,
    allow_scale: bool = True,
) -> NDArray[np.float64]:
    """Return a symmetric matrix of best pairwise relative RMS errors."""
    if len(curves) < 1:
        raise ValueError("curves must contain at least one curve.")

    validated = [
        _validate_points_2d(curve, f"curves[{index}]")
        for index, curve in enumerate(curves)
    ]

    matrix = np.zeros(
        (len(validated), len(validated)),
        dtype=np.float64,
    )

    for first in range(len(validated)):
        for second in range(first + 1, len(validated)):
            alignment = best_curve_alignment(
                validated[first],
                validated[second],
                closed=closed,
                allow_reversal=allow_reversal,
                allow_reflection=allow_reflection,
                allow_scale=allow_scale,
            )

            matrix[first, second] = alignment.relative_rms
            matrix[second, first] = alignment.relative_rms

    return matrix


def equivalence_classes_from_errors(
    error_matrix: ArrayLike,
    tolerance: float = 1.0e-8,
) -> tuple[tuple[int, ...], ...]:
    """Return connected equivalence classes below an error threshold."""
    matrix = np.asarray(error_matrix, dtype=np.float64)

    if matrix.ndim != 2 or matrix.shape[0] != matrix.shape[1]:
        raise ValueError("error_matrix must be square.")
    if matrix.shape[0] < 1:
        raise ValueError("error_matrix must be non-empty.")
    if not np.isfinite(matrix).all():
        raise ValueError(
            "error_matrix must contain only finite values."
        )
    if tolerance < 0.0:
        raise ValueError("tolerance must be non-negative.")
    if not np.allclose(
        matrix,
        matrix.T,
        atol=1.0e-12,
        rtol=0.0,
    ):
        raise ValueError("error_matrix must be symmetric.")

    unseen = set(range(matrix.shape[0]))
    classes: list[tuple[int, ...]] = []

    while unseen:
        root = min(unseen)
        stack = [root]
        component: set[int] = set()

        while stack:
            current = stack.pop()

            if current in component:
                continue

            component.add(current)

            neighbours = {
                index
                for index in unseen
                if matrix[current, index] <= tolerance
            }

            stack.extend(sorted(neighbours, reverse=True))

        unseen -= component
        classes.append(tuple(sorted(component)))

    return tuple(classes)
