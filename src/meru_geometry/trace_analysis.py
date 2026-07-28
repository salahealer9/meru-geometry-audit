"""Quantitative analysis of manually digitised source-image traces."""

from __future__ import annotations

from collections.abc import Mapping
from typing import NamedTuple

import numpy as np
from numpy.typing import ArrayLike, NDArray
from scipy.optimize import least_squares


class PolylineMetrics(NamedTuple):
    """Basic geometry of one visible polyline segment."""

    point_count: int
    length: float
    chord_length: float
    tortuosity: float
    minimum_x: float
    maximum_x: float
    minimum_y: float
    maximum_y: float


class EllipseFit(NamedTuple):
    """Descriptive least-squares ellipse fit."""

    centre_x: float
    centre_y: float
    semi_major: float
    semi_minor: float
    angle_radians: float
    radial_rms: float
    success: bool


class EndpointCandidate(NamedTuple):
    """Possible connection between two visible segment endpoints."""

    segment_a: int
    endpoint_a: str
    segment_b: int
    endpoint_b: str
    distance: float
    tangent_mismatch_radians: float
    score: float


def _validate_points(
    points: ArrayLike,
    minimum_points: int = 2,
) -> NDArray[np.float64]:
    """Validate a planar point array."""
    array = np.asarray(points, dtype=np.float64)

    if array.ndim != 2 or array.shape[1] != 2:
        raise ValueError("points must have shape (n, 2).")
    if array.shape[0] < minimum_points:
        raise ValueError(
            f"points must contain at least {minimum_points} rows."
        )
    if not np.isfinite(array).all():
        raise ValueError("points must contain only finite values.")

    return array


def polyline_metrics(
    points: ArrayLike,
    closed: bool = False,
) -> PolylineMetrics:
    """Calculate basic metrics for an ordered planar polyline.

    For a closed polyline, the final-to-initial segment is included in the
    length. Its endpoint separation is retained in ``chord_length`` as the
    closure gap, while tortuosity is undefined and returned as NaN.
    """
    array = _validate_points(points)

    increments = np.diff(array, axis=0)
    open_length = float(
        np.sum(np.linalg.norm(increments, axis=1))
    )

    chord = float(
        np.linalg.norm(array[-1] - array[0])
    )

    if closed:
        length = open_length + chord
        tortuosity = float("nan")
    else:
        length = open_length

        if chord > np.finfo(np.float64).eps:
            tortuosity = length / chord
        elif length <= np.finfo(np.float64).eps:
            tortuosity = 1.0
        else:
            tortuosity = float("inf")

    return PolylineMetrics(
        point_count=array.shape[0],
        length=length,
        chord_length=chord,
        tortuosity=tortuosity,
        minimum_x=float(np.min(array[:, 0])),
        maximum_x=float(np.max(array[:, 0])),
        minimum_y=float(np.min(array[:, 1])),
        maximum_y=float(np.max(array[:, 1])),
    )


def normalize_panel_coordinates(
    points: ArrayLike,
    width_px: float,
    height_px: float,
) -> NDArray[np.float64]:
    """Centre panel coordinates and apply one aspect-preserving scale.

    The resulting coordinate system has its origin at the panel centre,
    positive x to the right, and positive y upward.
    """
    array = _validate_points(points, minimum_points=1)

    if not np.isfinite(width_px) or width_px <= 0.0:
        raise ValueError("width_px must be positive and finite.")
    if not np.isfinite(height_px) or height_px <= 0.0:
        raise ValueError("height_px must be positive and finite.")

    scale = max(float(width_px), float(height_px))

    centred = np.empty_like(array)
    centred[:, 0] = (
        array[:, 0] - float(width_px) / 2.0
    ) / scale
    centred[:, 1] = (
        float(height_px) / 2.0 - array[:, 1]
    ) / scale

    return centred


def fit_descriptive_ellipse(
    points: ArrayLike,
) -> EllipseFit:
    """Fit a rotated ellipse using nonlinear least squares.

    The residual is the normalized elliptical radius minus one. The fit is
    descriptive only; it does not imply that the source boundary is exactly
    elliptical.
    """
    array = _validate_points(points, minimum_points=5)

    centre_initial = np.mean(array, axis=0)
    centred = array - centre_initial

    covariance = np.cov(
        centred,
        rowvar=False,
        bias=True,
    )

    eigenvalues, eigenvectors = np.linalg.eigh(covariance)
    order = np.argsort(eigenvalues)[::-1]
    eigenvalues = eigenvalues[order]
    eigenvectors = eigenvectors[:, order]

    if eigenvalues[-1] <= np.finfo(np.float64).eps:
        raise ValueError("points do not span a non-degenerate ellipse.")

    semi_major_initial = np.sqrt(
        2.0 * eigenvalues[0]
    )
    semi_minor_initial = np.sqrt(
        2.0 * eigenvalues[1]
    )

    angle_initial = float(
        np.arctan2(
            eigenvectors[1, 0],
            eigenvectors[0, 0],
        )
    )

    initial = np.asarray(
        [
            centre_initial[0],
            centre_initial[1],
            np.log(semi_major_initial),
            np.log(semi_minor_initial),
            angle_initial,
        ],
        dtype=np.float64,
    )

    def residual(parameters: NDArray[np.float64]) -> NDArray[np.float64]:
        centre_x, centre_y, log_a, log_b, angle = parameters

        semi_a = np.exp(log_a)
        semi_b = np.exp(log_b)

        cosine = np.cos(angle)
        sine = np.sin(angle)

        delta_x = array[:, 0] - centre_x
        delta_y = array[:, 1] - centre_y

        local_x = cosine * delta_x + sine * delta_y
        local_y = -sine * delta_x + cosine * delta_y

        elliptical_radius = np.sqrt(
            (local_x / semi_a) ** 2
            + (local_y / semi_b) ** 2
        )

        return elliptical_radius - 1.0

    result = least_squares(
        residual,
        initial,
        method="trf",
        loss="linear",
    )

    centre_x, centre_y, log_a, log_b, angle = result.x

    semi_a = float(np.exp(log_a))
    semi_b = float(np.exp(log_b))

    if semi_b > semi_a:
        semi_a, semi_b = semi_b, semi_a
        angle += np.pi / 2.0

    angle = float(
        (angle + np.pi) % (2.0 * np.pi) - np.pi
    )

    radial_rms = float(
        np.sqrt(
            np.mean(
                residual(result.x) ** 2
            )
        )
    )

    return EllipseFit(
        centre_x=float(centre_x),
        centre_y=float(centre_y),
        semi_major=semi_a,
        semi_minor=semi_b,
        angle_radians=angle,
        radial_rms=radial_rms,
        success=bool(result.success),
    )


def sample_ellipse(
    ellipse: EllipseFit,
    n_points: int = 500,
) -> NDArray[np.float64]:
    """Sample a fitted ellipse for visualization."""
    if n_points < 4:
        raise ValueError("n_points must be at least 4.")

    parameter = np.linspace(
        0.0,
        2.0 * np.pi,
        n_points,
        endpoint=True,
    )

    local = np.column_stack(
        (
            ellipse.semi_major * np.cos(parameter),
            ellipse.semi_minor * np.sin(parameter),
        )
    )

    cosine = np.cos(ellipse.angle_radians)
    sine = np.sin(ellipse.angle_radians)

    rotation = np.asarray(
        [
            [cosine, -sine],
            [sine, cosine],
        ]
    )

    return (
        local @ rotation.T
        + np.asarray(
            [ellipse.centre_x, ellipse.centre_y]
        )
    )


def _endpoint_information(
    segment_id: int,
    points: NDArray[np.float64],
) -> list[tuple[int, str, NDArray[np.float64], NDArray[np.float64]]]:
    """Return endpoint positions and inward segment tangents."""
    array = _validate_points(points)

    start_tangent = array[1] - array[0]
    end_tangent = array[-2] - array[-1]

    start_norm = np.linalg.norm(start_tangent)
    end_norm = np.linalg.norm(end_tangent)

    if start_norm <= np.finfo(np.float64).eps:
        raise ValueError("segment has a degenerate start tangent.")
    if end_norm <= np.finfo(np.float64).eps:
        raise ValueError("segment has a degenerate end tangent.")

    return [
        (
            segment_id,
            "start",
            array[0],
            start_tangent / start_norm,
        ),
        (
            segment_id,
            "end",
            array[-1],
            end_tangent / end_norm,
        ),
    ]


def endpoint_connection_candidates(
    segments: Mapping[int, ArrayLike],
    maximum_candidates: int | None = None,
) -> tuple[EndpointCandidate, ...]:
    """Rank possible reconnections between disconnected same-layer segments.

    The score combines endpoint separation with tangent continuation mismatch.
    It is only a diagnostic ranking and does not automatically join segments.
    """
    if not segments:
        return ()

    endpoints: list[
        tuple[
            int,
            str,
            NDArray[np.float64],
            NDArray[np.float64],
        ]
    ] = []

    for segment_id, points in sorted(segments.items()):
        array = _validate_points(points)
        endpoints.extend(
            _endpoint_information(
                int(segment_id),
                array,
            )
        )

    candidates: list[EndpointCandidate] = []

    for first_index, first in enumerate(endpoints):
        for second in endpoints[first_index + 1 :]:
            segment_a, endpoint_a, point_a, inward_a = first
            segment_b, endpoint_b, point_b, inward_b = second

            if segment_a == segment_b:
                continue

            gap = point_b - point_a
            distance = float(np.linalg.norm(gap))

            if distance <= np.finfo(np.float64).eps:
                tangent_mismatch = 0.0
            else:
                direction = gap / distance

                outward_a = -inward_a
                outward_b = -inward_b

                angle_a = float(
                    np.arccos(
                        np.clip(
                            np.dot(outward_a, direction),
                            -1.0,
                            1.0,
                        )
                    )
                )

                angle_b = float(
                    np.arccos(
                        np.clip(
                            np.dot(outward_b, -direction),
                            -1.0,
                            1.0,
                        )
                    )
                )

                tangent_mismatch = (
                    angle_a + angle_b
                ) / 2.0

            score = distance * (
                1.0 + tangent_mismatch / np.pi
            )

            candidates.append(
                EndpointCandidate(
                    segment_a=segment_a,
                    endpoint_a=endpoint_a,
                    segment_b=segment_b,
                    endpoint_b=endpoint_b,
                    distance=distance,
                    tangent_mismatch_radians=tangent_mismatch,
                    score=score,
                )
            )

    candidates.sort(
        key=lambda candidate: (
            candidate.score,
            candidate.distance,
            candidate.segment_a,
            candidate.segment_b,
        )
    )

    if maximum_candidates is not None:
        if maximum_candidates < 1:
            raise ValueError(
                "maximum_candidates must be positive."
            )
        candidates = candidates[:maximum_candidates]

    return tuple(candidates)
