"""Manual review records for source-derived crossing candidates."""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from typing import Any


VALID_LAYERS = {
    "red",
    "green",
    "blue",
}

VALID_STATUSES = {
    "unreviewed",
    "crossing",
    "continuation_junction",
    "different_feature",
    "duplicate_candidate",
    "ambiguous",
}

VALID_CONFIDENCES = {
    "",
    "low",
    "medium",
    "high",
}

VALID_VISIBILITIES = {
    "",
    "visible",
    "partial",
    "occluded",
    "unclear",
}

VALID_REASON_CODES = {
    "",
    "source_crossing",
    "continuation_or_transition",
    "different_projected_region",
    "duplicate_event",
    "insufficient_resolution",
    "other",
}

MANUAL_FIELDS = (
    "status",
    "confidence",
    "event_id",
    "over_layer",
    "over_segment",
    "under_layer",
    "under_segment",
    "visibility",
    "reason_code",
    "notes",
    "reviewed_utc",
)


def _optional_positive_integer(
    value: object,
    field_name: str,
) -> int | None:
    """Parse an optional positive integer field."""
    text = str(value).strip()

    if not text:
        return None

    try:
        result = int(text)
    except ValueError as exc:
        raise ValueError(
            f"{field_name} must be a positive integer or blank."
        ) from exc

    if result < 1:
        raise ValueError(
            f"{field_name} must be a positive integer or blank."
        )

    return result


def validate_crossing_review_rows(
    rows: Iterable[Mapping[str, Any]],
) -> None:
    """Validate candidate geometry and manual crossing decisions."""
    identifiers: set[str] = set()

    for row in rows:
        identifier = str(row["candidate_id"])

        if identifier in identifiers:
            raise ValueError(
                f"Duplicate candidate identifier: {identifier}"
            )

        identifiers.add(identifier)

        layer_a = str(row["layer_a"])
        layer_b = str(row["layer_b"])

        if layer_a not in VALID_LAYERS:
            raise ValueError(
                f"{identifier}: invalid layer_a {layer_a!r}."
            )

        if layer_b not in VALID_LAYERS:
            raise ValueError(
                f"{identifier}: invalid layer_b {layer_b!r}."
            )

        segment_a = int(row["segment_a"])
        segment_b = int(row["segment_b"])

        if segment_a < 1 or segment_b < 1:
            raise ValueError(
                f"{identifier}: segment identifiers must be positive."
            )

        status = str(row.get("status", ""))
        confidence = str(row.get("confidence", ""))
        visibility = str(row.get("visibility", ""))
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

        if visibility not in VALID_VISIBILITIES:
            raise ValueError(
                f"{identifier}: invalid visibility "
                f"{visibility!r}."
            )

        if reason_code not in VALID_REASON_CODES:
            raise ValueError(
                f"{identifier}: invalid reason code "
                f"{reason_code!r}."
            )

        event_id = str(
            row.get("event_id", "")
        ).strip()

        over_layer = str(
            row.get("over_layer", "")
        ).strip()

        under_layer = str(
            row.get("under_layer", "")
        ).strip()

        over_segment = _optional_positive_integer(
            row.get("over_segment", ""),
            "over_segment",
        )

        under_segment = _optional_positive_integer(
            row.get("under_segment", ""),
            "under_segment",
        )

        candidate_segments = {
            (layer_a, segment_a),
            (layer_b, segment_b),
        }

        if status == "unreviewed":
            if confidence or reason_code:
                raise ValueError(
                    f"{identifier}: an unreviewed row cannot "
                    "have confidence or a reason code."
                )

        else:
            if not confidence:
                raise ValueError(
                    f"{identifier}: reviewed rows require confidence."
                )

            if not reason_code:
                raise ValueError(
                    f"{identifier}: reviewed rows require a reason code."
                )

            if not str(
                row.get("reviewed_utc", "")
            ).strip():
                raise ValueError(
                    f"{identifier}: reviewed rows require reviewed_utc."
                )

        if status == "crossing":
            if not event_id:
                raise ValueError(
                    f"{identifier}: a crossing requires event_id."
                )

            if (
                not over_layer
                or over_segment is None
                or not under_layer
                or under_segment is None
            ):
                raise ValueError(
                    f"{identifier}: a crossing requires complete "
                    "over- and under-strand fields."
                )

            over_key = (
                over_layer,
                over_segment,
            )

            under_key = (
                under_layer,
                under_segment,
            )

            if over_key not in candidate_segments:
                raise ValueError(
                    f"{identifier}: over-strand is not one of "
                    "the candidate segments."
                )

            if under_key not in candidate_segments:
                raise ValueError(
                    f"{identifier}: under-strand is not one of "
                    "the candidate segments."
                )

            if over_key == under_key:
                raise ValueError(
                    f"{identifier}: over- and under-strands "
                    "must differ."
                )

            if not visibility:
                raise ValueError(
                    f"{identifier}: a crossing requires visibility."
                )

        elif status == "duplicate_candidate":
            if not event_id:
                raise ValueError(
                    f"{identifier}: a duplicate candidate "
                    "requires event_id."
                )

            if (
                over_layer
                or over_segment is not None
                or under_layer
                or under_segment is not None
            ):
                raise ValueError(
                    f"{identifier}: duplicate candidates must not "
                    "repeat over-under assignments."
                )

        else:
            if (
                over_layer
                or over_segment is not None
                or under_layer
                or under_segment is not None
            ):
                raise ValueError(
                    f"{identifier}: only genuine crossings may "
                    "contain over-under assignments."
                )


def merge_crossing_review_rows(
    candidate_rows: Iterable[Mapping[str, Any]],
    existing_rows: Iterable[Mapping[str, Any]] = (),
) -> list[dict[str, object]]:
    """Create review records while preserving manual decisions."""
    existing_by_identifier = {
        str(row["candidate_id"]): dict(row)
        for row in existing_rows
    }

    merged: list[dict[str, object]] = []

    for candidate in candidate_rows:
        identifier = str(
            candidate["candidate_id"]
        )

        row: dict[str, object] = {
            "candidate_id": identifier,
            "rank": int(candidate["rank"]),
            "layer_a": str(candidate["layer_a"]),
            "segment_a": int(candidate["segment_a"]),
            "layer_b": str(candidate["layer_b"]),
            "segment_b": int(candidate["segment_b"]),
            "candidate_kind": str(
                candidate["candidate_kind"]
            ),
            "panel_x": float(candidate["panel_x"]),
            "panel_y": float(candidate["panel_y"]),
            "distance_px": float(
                candidate["distance_px"]
            ),
            "crossing_angle_deg": float(
                candidate["crossing_angle_deg"]
            ),
            "piece_index_a": int(
                candidate["piece_index_a"]
            ),
            "piece_index_b": int(
                candidate["piece_index_b"]
            ),
            "fraction_a": float(
                candidate["fraction_a"]
            ),
            "fraction_b": float(
                candidate["fraction_b"]
            ),
            "status": "unreviewed",
            "confidence": "",
            "event_id": "",
            "over_layer": "",
            "over_segment": "",
            "under_layer": "",
            "under_segment": "",
            "visibility": "",
            "reason_code": "",
            "notes": "",
            "reviewed_utc": "",
        }

        previous = existing_by_identifier.get(
            identifier
        )

        if previous is not None:
            for field in MANUAL_FIELDS:
                row[field] = previous.get(
                    field,
                    row[field],
                )

        merged.append(row)

    merged.sort(
        key=lambda row: int(row["rank"])
    )

    validate_crossing_review_rows(merged)
    return merged
