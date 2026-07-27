"""Tests for endpoint-candidate adjudication utilities."""

from __future__ import annotations

import numpy as np
import pytest

from meru_geometry.endpoint_review import (
    candidate_identifier,
    endpoint_coordinate,
    merge_adjudication_rows,
    validate_adjudication_rows,
)


def candidate_row() -> dict[str, object]:
    return {
        "layer": "red",
        "rank": 1,
        "segment_a": 3,
        "endpoint_a": "end",
        "segment_b": 4,
        "endpoint_b": "end",
        "distance": 5.8,
        "tangent_mismatch_radians": 0.2,
        "score": 6.2,
    }


def test_candidate_identifier_is_stable() -> None:
    identifier = candidate_identifier(
        "red",
        3,
        "end",
        4,
        "start",
    )

    assert identifier == "R_S03E_S04S"


def test_endpoint_coordinate() -> None:
    points = np.asarray(
        [
            [1.0, 2.0],
            [3.0, 4.0],
            [5.0, 6.0],
        ]
    )

    assert np.array_equal(
        endpoint_coordinate(points, "start"),
        np.asarray([1.0, 2.0]),
    )

    assert np.array_equal(
        endpoint_coordinate(points, "end"),
        np.asarray([5.0, 6.0]),
    )


def test_merge_creates_unreviewed_record() -> None:
    rows = merge_adjudication_rows(
        [candidate_row()]
    )

    assert len(rows) == 1
    assert rows[0]["candidate_id"] == "R_S03E_S04E"
    assert rows[0]["status"] == "unreviewed"
    assert rows[0]["confidence"] == ""


def test_merge_preserves_manual_decision() -> None:
    existing = {
        "candidate_id": "R_S03E_S04E",
        "status": "accepted",
        "confidence": "high",
        "reason_code": "clear_continuation",
        "notes": "Visible continuation across a short gap.",
        "reviewed_utc": "2026-07-27T12:00:00+00:00",
    }

    rows = merge_adjudication_rows(
        [candidate_row()],
        [existing],
    )

    assert rows[0]["status"] == "accepted"
    assert rows[0]["confidence"] == "high"
    assert (
        rows[0]["reason_code"]
        == "clear_continuation"
    )


def test_invalid_status_is_rejected() -> None:
    rows = merge_adjudication_rows(
        [candidate_row()]
    )

    rows[0]["status"] = "maybe"

    with pytest.raises(
        ValueError,
        match="invalid status",
    ):
        validate_adjudication_rows(rows)


def test_colour_intersection_reason_is_valid() -> None:
    rows = merge_adjudication_rows(
        [candidate_row()]
    )

    rows[0]["status"] = "rejected"
    rows[0]["confidence"] = "high"
    rows[0]["reason_code"] = "colour_intersection"
    rows[0]["notes"] = (
        "Endpoints are mixed-colour intersections, "
        "not same-line continuations."
    )

    validate_adjudication_rows(rows)
