"""Utilities for manual adjudication of endpoint-connection candidates."""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from typing import Any

import numpy as np
from numpy.typing import ArrayLike, NDArray


LAYER_ORDER = {
    "red": 0,
    "green": 1,
    "blue": 2,
}

LAYER_PREFIX = {
    "red": "R",
    "green": "G",
    "blue": "B",
}

VALID_STATUSES = {
    "unreviewed",
    "accepted",
    "rejected",
    "ambiguous",
}

VALID_CONFIDENCES = {
    "",
    "low",
    "medium",
    "high",
}

VALID_REASON_CODES = {
    "",
    "clear_continuation",
    "occlusion_supported",
    "crossing_conflict",
    "tangent_conflict",
    "different_feature",
    "insufficient_resolution",
    "other",
}

MANUAL_FIELDS = (
    "status",
    "confidence",
    "reason_code",
    "notes",
    "reviewed_utc",
)


def endpoint_coordinate(
    points: ArrayLike,
    endpoint: str,
) -> NDArray[np.float64]:
    """Return the selected endpoint of an ordered planar segment."""
    array = np.asarray(points, dtype=np.float64)

    if array.ndim != 2 or array.shape[1] != 2:
        raise ValueError("points must have shape (n, 2).")
    if array.shape[0] < 1:
        raise ValueError("points must contain at least one row.")
    if not np.isfinite(array).all():
        raise ValueError("points must contain only finite values.")

    if endpoint == "start":
        return array[0].copy()

    if endpoint == "end":
        return array[-1].copy()

    raise ValueError("endpoint must be 'start' or 'end'.")


def candidate_identifier(
    layer: str,
    segment_a: int,
    endpoint_a: str,
    segment_b: int,
    endpoint_b: str,
) -> str:
    """Return a stable identifier for one endpoint pair."""
    if layer not in LAYER_PREFIX:
        raise ValueError(f"Unsupported layer: {layer}")

    if segment_a < 1 or segment_b < 1:
        raise ValueError("segment numbers must be positive.")

    endpoint_codes = {
        "start": "S",
        "end": "E",
    }

    try:
        code_a = endpoint_codes[endpoint_a]
        code_b = endpoint_codes[endpoint_b]
    except KeyError as exc:
        raise ValueError(
            "endpoint names must be 'start' or 'end'."
        ) from exc

    return (
        f"{LAYER_PREFIX[layer]}_"
        f"S{segment_a:02d}{code_a}_"
        f"S{segment_b:02d}{code_b}"
    )


def validate_adjudication_rows(
    rows: Iterable[Mapping[str, Any]],
) -> None:
    """Validate manual endpoint-adjudication records."""
    identifiers: set[str] = set()

    for row in rows:
        identifier = str(row["candidate_id"])

        if identifier in identifiers:
            raise ValueError(
                f"Duplicate candidate identifier: {identifier}"
            )

        identifiers.add(identifier)

        layer = str(row["layer"])

        if layer not in LAYER_ORDER:
            raise ValueError(f"Unsupported layer: {layer}")

        status = str(row.get("status", ""))
        confidence = str(row.get("confidence", ""))
        reason_code = str(row.get("reason_code", ""))

        if status not in VALID_STATUSES:
            raise ValueError(
                f"{identifier}: invalid status {status!r}."
            )

        if confidence not in VALID_CONFIDENCES:
            raise ValueError(
                f"{identifier}: invalid confidence "
                f"{confidence!r}."
            )

        if reason_code not in VALID_REASON_CODES:
            raise ValueError(
                f"{identifier}: invalid reason code "
                f"{reason_code!r}."
            )


def merge_adjudication_rows(
    candidate_rows: Iterable[Mapping[str, Any]],
    existing_rows: Iterable[Mapping[str, Any]] = (),
    top_n_per_layer: int = 5,
) -> list[dict[str, object]]:
    """Create review records while preserving existing manual decisions."""
    if top_n_per_layer < 1:
        raise ValueError("top_n_per_layer must be positive.")

    existing_by_identifier = {
        str(row["candidate_id"]): dict(row)
        for row in existing_rows
    }

    merged: list[dict[str, object]] = []

    for candidate in candidate_rows:
        layer = str(candidate["layer"])
        rank = int(candidate["rank"])

        if layer not in LAYER_ORDER:
            continue

        if rank > top_n_per_layer:
            continue

        segment_a = int(candidate["segment_a"])
        segment_b = int(candidate["segment_b"])
        endpoint_a = str(candidate["endpoint_a"])
        endpoint_b = str(candidate["endpoint_b"])

        identifier = candidate_identifier(
            layer,
            segment_a,
            endpoint_a,
            segment_b,
            endpoint_b,
        )

        record: dict[str, object] = {
            "candidate_id": identifier,
            "layer": layer,
            "rank": rank,
            "segment_a": segment_a,
            "endpoint_a": endpoint_a,
            "segment_b": segment_b,
            "endpoint_b": endpoint_b,
            "distance_px": float(candidate["distance"]),
            "tangent_mismatch_deg": float(
                np.degrees(
                    float(
                        candidate[
                            "tangent_mismatch_radians"
                        ]
                    )
                )
            ),
            "score": float(candidate["score"]),
            "status": "unreviewed",
            "confidence": "",
            "reason_code": "",
            "notes": "",
            "reviewed_utc": "",
        }

        existing = existing_by_identifier.get(identifier)

        if existing is not None:
            for field in MANUAL_FIELDS:
                record[field] = existing.get(
                    field,
                    record[field],
                )

        merged.append(record)

    merged.sort(
        key=lambda row: (
            LAYER_ORDER[str(row["layer"])],
            int(row["rank"]),
        )
    )

    validate_adjudication_rows(merged)
    return merged
