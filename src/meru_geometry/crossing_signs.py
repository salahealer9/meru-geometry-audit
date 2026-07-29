"""Oriented crossing-sign calculations for planar knot diagrams."""

from __future__ import annotations

from collections import Counter
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass

import numpy as np
from numpy.typing import ArrayLike, NDArray


SegmentKey = tuple[str, int]


@dataclass(frozen=True)
class CrossingSign:
    """One oriented crossing-sign determination."""

    event_id: str
    candidate_id: str
    sign: int
    determinant: float
    crossing_angle_degrees: float
    over_key: SegmentKey
    under_key: SegmentKey
    over_tangent: tuple[float, float]
    under_tangent: tuple[float, float]
    tangent_span_px: float

    @property
    def sign_token(self) -> str:
        """Return a compact signed event token."""
        suffix = (
            "+"
            if self.sign > 0
            else "-"
            if self.sign < 0
            else "0"
        )

        return f"{self.event_id}{suffix}"


def _validate_polyline(
    points: ArrayLike,
) -> NDArray[np.float64]:
    """Validate and return one finite non-degenerate polyline."""
    array = np.asarray(
        points,
        dtype=np.float64,
    )

    if (
        array.ndim != 2
        or array.shape[1] != 2
        or array.shape[0] < 2
    ):
        raise ValueError(
            "Polyline points must have shape (n, 2), with n >= 2."
        )

    if not np.isfinite(array).all():
        raise ValueError(
            "Polyline coordinates must be finite."
        )

    lengths = np.linalg.norm(
        np.diff(array, axis=0),
        axis=1,
    )

    if np.any(
        lengths
        <= np.finfo(np.float64).eps
    ):
        raise ValueError(
            "Zero-length polyline pieces are not supported."
        )

    return array


def _point_at_arc_distance(
    points: NDArray[np.float64],
    cumulative: NDArray[np.float64],
    piece_lengths: NDArray[np.float64],
    distance: float,
) -> NDArray[np.float64]:
    """Interpolate one point at an arc distance along a polyline."""
    clipped = float(
        np.clip(
            distance,
            0.0,
            cumulative[-1],
        )
    )

    piece_index = int(
        np.searchsorted(
            cumulative,
            clipped,
            side="right",
        )
        - 1
    )

    piece_index = min(
        max(piece_index, 0),
        len(piece_lengths) - 1,
    )

    length = float(
        piece_lengths[piece_index]
    )

    fraction = (
        clipped - cumulative[piece_index]
    ) / length

    return (
        points[piece_index]
        + fraction
        * (
            points[piece_index + 1]
            - points[piece_index]
        )
    )


def oriented_tangent(
    points: ArrayLike,
    piece_index: int,
    piece_fraction: float,
    traversal_forward: bool,
    span_px: float = 6.0,
    image_y_down: bool = True,
) -> NDArray[np.float64]:
    """Estimate a unit tangent along the frozen traversal.

    A secant with total arc-length ``span_px`` is centred at the
    recorded piece location. At a visible-fragment endpoint, the
    estimate is clipped one-sidedly rather than extrapolated.
    """
    polyline = _validate_polyline(
        points
    )

    if not 0 <= piece_index < polyline.shape[0] - 1:
        raise ValueError(
            "piece_index is outside the polyline-piece range."
        )

    if not 0.0 <= piece_fraction <= 1.0:
        raise ValueError(
            "piece_fraction must lie between zero and one."
        )

    if span_px <= 0.0:
        raise ValueError(
            "span_px must be positive."
        )

    piece_lengths = np.linalg.norm(
        np.diff(polyline, axis=0),
        axis=1,
    )

    cumulative = np.concatenate(
        (
            np.asarray([0.0]),
            np.cumsum(piece_lengths),
        )
    )

    location = float(
        cumulative[piece_index]
        + piece_fraction
        * piece_lengths[piece_index]
    )

    half_span = span_px / 2.0

    start_distance = max(
        0.0,
        location - half_span,
    )

    end_distance = min(
        float(cumulative[-1]),
        location + half_span,
    )

    if (
        end_distance - start_distance
        <= np.finfo(np.float64).eps
    ):
        raise ValueError(
            "The tangent window has zero usable arc length."
        )

    start = _point_at_arc_distance(
        polyline,
        cumulative,
        piece_lengths,
        start_distance,
    )

    end = _point_at_arc_distance(
        polyline,
        cumulative,
        piece_lengths,
        end_distance,
    )

    tangent = end - start

    if not traversal_forward:
        tangent = -tangent

    # Source-panel coordinates have y increasing downward.
    # Convert to a right-handed Cartesian image plane.
    if image_y_down:
        tangent = np.asarray(
            [
                tangent[0],
                -tangent[1],
            ],
            dtype=np.float64,
        )

    norm = float(
        np.linalg.norm(tangent)
    )

    if norm <= np.finfo(np.float64).eps:
        raise ValueError(
            "The local tangent estimate is degenerate."
        )

    return tangent / norm


def crossing_sign(
    over_tangent: ArrayLike,
    under_tangent: ArrayLike,
    tolerance: float = 1.0e-12,
) -> tuple[int, float, float]:
    """Return sign, normalized determinant and acute angle.

    Convention:

        epsilon = sign(det(t_over, t_under))

    in a right-handed Cartesian image plane with +z toward the viewer.
    """
    over = np.asarray(
        over_tangent,
        dtype=np.float64,
    )

    under = np.asarray(
        under_tangent,
        dtype=np.float64,
    )

    if (
        over.shape != (2,)
        or under.shape != (2,)
    ):
        raise ValueError(
            "Crossing tangents must be planar vectors."
        )

    over_norm = float(
        np.linalg.norm(over)
    )

    under_norm = float(
        np.linalg.norm(under)
    )

    if (
        over_norm <= np.finfo(np.float64).eps
        or under_norm <= np.finfo(np.float64).eps
    ):
        raise ValueError(
            "Crossing tangents must be non-zero."
        )

    over = over / over_norm
    under = under / under_norm

    determinant = float(
        over[0] * under[1]
        - over[1] * under[0]
    )

    if determinant > tolerance:
        sign = 1
    elif determinant < -tolerance:
        sign = -1
    else:
        sign = 0

    cosine = abs(
        float(
            np.clip(
                np.dot(
                    over,
                    under,
                ),
                -1.0,
                1.0,
            )
        )
    )

    angle = float(
        np.degrees(
            np.arccos(cosine)
        )
    )

    return sign, determinant, angle


def derive_crossing_signs(
    crossing_rows: Iterable[
        Mapping[str, object]
    ],
    segments: Mapping[
        SegmentKey,
        ArrayLike,
    ],
    traversal_forward: Mapping[
        SegmentKey,
        bool,
    ],
    span_px: float = 6.0,
) -> tuple[CrossingSign, ...]:
    """Derive oriented signs for all reviewed crossing rows."""
    results: list[
        CrossingSign
    ] = []

    event_ids: set[str] = set()

    for row in crossing_rows:
        if str(row["status"]) != "crossing":
            continue

        event_id = str(
            row["event_id"]
        ).strip()

        if not event_id:
            raise ValueError(
                "Crossing rows require event_id."
            )

        if event_id in event_ids:
            raise ValueError(
                f"Duplicate crossing event: {event_id}"
            )

        event_ids.add(event_id)

        key_a = (
            str(row["layer_a"]),
            int(row["segment_a"]),
        )

        key_b = (
            str(row["layer_b"]),
            int(row["segment_b"]),
        )

        over_key = (
            str(row["over_layer"]),
            int(row["over_segment"]),
        )

        under_key = (
            str(row["under_layer"]),
            int(row["under_segment"]),
        )

        if {
            over_key,
            under_key,
        } != {
            key_a,
            key_b,
        }:
            raise ValueError(
                f"{event_id}: over-under strands do not match "
                "the candidate segment pair."
            )

        tangent_by_key: dict[
            SegmentKey,
            NDArray[np.float64],
        ] = {}

        for side, key in (
            ("a", key_a),
            ("b", key_b),
        ):
            if key not in segments:
                raise ValueError(
                    f"{event_id}: missing segment {key}."
                )

            if key not in traversal_forward:
                raise ValueError(
                    f"{event_id}: missing traversal direction "
                    f"for {key}."
                )

            tangent_by_key[key] = oriented_tangent(
                segments[key],
                int(row[f"piece_index_{side}"]),
                float(row[f"fraction_{side}"]),
                traversal_forward[key],
                span_px=span_px,
                image_y_down=True,
            )

        over_tangent = tangent_by_key[
            over_key
        ]

        under_tangent = tangent_by_key[
            under_key
        ]

        (
            sign,
            determinant,
            angle,
        ) = crossing_sign(
            over_tangent,
            under_tangent,
        )

        results.append(
            CrossingSign(
                event_id=event_id,
                candidate_id=str(
                    row["candidate_id"]
                ),
                sign=sign,
                determinant=determinant,
                crossing_angle_degrees=angle,
                over_key=over_key,
                under_key=under_key,
                over_tangent=(
                    float(over_tangent[0]),
                    float(over_tangent[1]),
                ),
                under_tangent=(
                    float(under_tangent[0]),
                    float(under_tangent[1]),
                ),
                tangent_span_px=span_px,
            )
        )

    results.sort(
        key=lambda result: int(
            result.event_id[1:]
        )
    )

    return tuple(results)


def crossing_sign_stability(
    crossing_rows: Iterable[
        Mapping[str, object]
    ],
    segments: Mapping[
        SegmentKey,
        ArrayLike,
    ],
    traversal_forward: Mapping[
        SegmentKey,
        bool,
    ],
    spans_px: Sequence[float],
) -> dict[str, tuple[int, ...]]:
    """Return every event's sign across tangent-window spans."""
    rows = tuple(
        crossing_rows
    )

    if not spans_px:
        raise ValueError(
            "At least one tangent span is required."
        )

    per_span = [
        derive_crossing_signs(
            rows,
            segments,
            traversal_forward,
            span_px=float(span),
        )
        for span in spans_px
    ]

    event_order = [
        result.event_id
        for result in per_span[0]
    ]

    return {
        event_id: tuple(
            next(
                result.sign
                for result in results
                if result.event_id == event_id
            )
            for results in per_span
        )
        for event_id in event_order
    }


def writhe(
    crossing_signs: Iterable[
        CrossingSign
    ],
) -> int:
    """Return the sum of all non-degenerate crossing signs."""
    signs = [
        result.sign
        for result in crossing_signs
    ]

    if any(
        sign == 0
        for sign in signs
    ):
        raise ValueError(
            "Writhe is undefined while a crossing sign "
            "is degenerate."
        )

    return int(
        sum(signs)
    )


def sign_counts(
    crossing_signs: Iterable[
        CrossingSign
    ],
) -> Counter[int]:
    """Count positive, negative and degenerate signs."""
    return Counter(
        result.sign
        for result in crossing_signs
    )
