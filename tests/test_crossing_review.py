"""Tests for manual crossing-candidate review records."""

from __future__ import annotations

import pytest

from meru_geometry.crossing_review import (
    merge_crossing_review_rows,
    validate_crossing_review_rows,
)


def candidate_row() -> dict[str, object]:
    return {
        "candidate_id": "XING_R_S01_G_S02",
        "rank": 1,
        "layer_a": "red",
        "segment_a": 1,
        "layer_b": "green",
        "segment_b": 2,
        "candidate_kind": "near_crossing",
        "panel_x": 100.0,
        "panel_y": 80.0,
        "distance_px": 2.0,
        "crossing_angle_deg": 60.0,
        "piece_index_a": 2,
        "piece_index_b": 3,
        "fraction_a": 0.25,
        "fraction_b": 0.75,
    }


def test_merge_creates_unreviewed_record() -> None:
    rows = merge_crossing_review_rows(
        [candidate_row()]
    )

    assert len(rows) == 1
    assert rows[0]["status"] == "unreviewed"
    assert rows[0]["event_id"] == ""


def test_merge_preserves_manual_fields() -> None:
    existing = {
        "candidate_id": "XING_R_S01_G_S02",
        "status": "ambiguous",
        "confidence": "medium",
        "event_id": "",
        "over_layer": "",
        "over_segment": "",
        "under_layer": "",
        "under_segment": "",
        "visibility": "unclear",
        "reason_code": "insufficient_resolution",
        "notes": "Source does not determine depth.",
        "reviewed_utc": "2026-07-29T08:00:00+00:00",
    }

    rows = merge_crossing_review_rows(
        [candidate_row()],
        [existing],
    )

    assert rows[0]["status"] == "ambiguous"
    assert rows[0]["confidence"] == "medium"


def test_crossing_requires_over_under_fields() -> None:
    rows = merge_crossing_review_rows(
        [candidate_row()]
    )

    rows[0].update(
        {
            "status": "crossing",
            "confidence": "high",
            "event_id": "E01",
            "visibility": "visible",
            "reason_code": "source_crossing",
            "reviewed_utc": (
                "2026-07-29T08:00:00+00:00"
            ),
        }
    )

    with pytest.raises(
        ValueError,
        match="over- and under",
    ):
        validate_crossing_review_rows(rows)


def test_crossing_accepts_candidate_segments() -> None:
    rows = merge_crossing_review_rows(
        [candidate_row()]
    )

    rows[0].update(
        {
            "status": "crossing",
            "confidence": "high",
            "event_id": "E01",
            "over_layer": "red",
            "over_segment": 1,
            "under_layer": "green",
            "under_segment": 2,
            "visibility": "visible",
            "reason_code": "source_crossing",
            "notes": "Red visibly passes over green.",
            "reviewed_utc": (
                "2026-07-29T08:00:00+00:00"
            ),
        }
    )

    validate_crossing_review_rows(rows)


def test_unrelated_over_strand_is_rejected() -> None:
    rows = merge_crossing_review_rows(
        [candidate_row()]
    )

    rows[0].update(
        {
            "status": "crossing",
            "confidence": "high",
            "event_id": "E01",
            "over_layer": "blue",
            "over_segment": 4,
            "under_layer": "green",
            "under_segment": 2,
            "visibility": "visible",
            "reason_code": "source_crossing",
            "reviewed_utc": (
                "2026-07-29T08:00:00+00:00"
            ),
        }
    )

    with pytest.raises(
        ValueError,
        match="over-strand",
    ):
        validate_crossing_review_rows(rows)


def test_duplicate_candidate_requires_event_id() -> None:
    rows = merge_crossing_review_rows(
        [candidate_row()]
    )

    rows[0].update(
        {
            "status": "duplicate_candidate",
            "confidence": "high",
            "reason_code": "duplicate_event",
            "reviewed_utc": (
                "2026-07-29T08:00:00+00:00"
            ),
        }
    )

    with pytest.raises(
        ValueError,
        match="requires event_id",
    ):
        validate_crossing_review_rows(rows)
