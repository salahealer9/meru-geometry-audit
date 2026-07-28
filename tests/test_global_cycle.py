"""Tests for the complete coloured global-cycle audit."""

from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path

import pytest

from meru_geometry.global_cycle import (
    audit_global_cycle,
    format_segment_visit,
)


ROOT = Path(__file__).resolve().parents[1]

DATA_DIR = (
    ROOT
    / "data"
    / "manual_digitizations"
    / "A10_P03"
)


def test_three_segments_form_one_cycle() -> None:
    segment_ids = {
        "red": [1],
        "green": [1],
        "blue": [1],
    }

    cross_colour = [
        {
            "candidate_id": "X_RG",
            "layer_a": "red",
            "segment_a": 1,
            "endpoint_a": "end",
            "layer_b": "green",
            "segment_b": 1,
            "endpoint_b": "start",
        },
        {
            "candidate_id": "X_GB",
            "layer_a": "green",
            "segment_a": 1,
            "endpoint_a": "end",
            "layer_b": "blue",
            "segment_b": 1,
            "endpoint_b": "start",
        },
        {
            "candidate_id": "X_RB",
            "layer_a": "blue",
            "segment_a": 1,
            "endpoint_a": "end",
            "layer_b": "red",
            "segment_b": 1,
            "endpoint_b": "start",
        },
    ]

    audit = audit_global_cycle(
        segment_ids,
        same_colour_connections=[],
        cross_colour_connections=cross_colour,
    )

    assert audit.is_single_cycle
    assert audit.vertex_count == 6
    assert audit.edge_count == 6
    assert audit.degree_map == {2: 6}
    assert audit.component_count == 1

    assert tuple(
        format_segment_visit(visit)
        for visit in audit.segment_traversal
    ) == (
        "R:S01+",
        "G:S01+",
        "B:S01+",
    )


def test_missing_transition_leaves_open_graph() -> None:
    audit = audit_global_cycle(
        {
            "red": [1],
            "green": [1],
            "blue": [],
        },
        same_colour_connections=[],
        cross_colour_connections=[
            {
                "candidate_id": "X_RG",
                "layer_a": "red",
                "segment_a": 1,
                "endpoint_a": "end",
                "layer_b": "green",
                "segment_b": 1,
                "endpoint_b": "start",
            }
        ],
    )

    assert not audit.is_single_cycle
    assert audit.degree_map == {
        1: 2,
        2: 2,
    }


def test_duplicate_edge_identifier_is_rejected() -> None:
    row = {
        "candidate_id": "DUPLICATE",
        "layer": "red",
        "segment_a": 1,
        "endpoint_a": "end",
        "segment_b": 2,
        "endpoint_b": "start",
    }

    with pytest.raises(
        ValueError,
        match="Duplicate graph edge",
    ):
        audit_global_cycle(
            {
                "red": [1, 2],
                "green": [],
                "blue": [],
            },
            same_colour_connections=[
                row,
                row,
            ],
            cross_colour_connections=[],
        )


def _load_segment_ids() -> dict[
    str,
    set[int],
]:
    result: dict[str, set[int]] = defaultdict(set)

    path = DATA_DIR / "digitization.csv"

    with path.open(
        newline="",
        encoding="utf-8",
    ) as handle:
        for row in csv.DictReader(handle):
            layer = row["layer"]

            if layer not in {
                "red",
                "green",
                "blue",
            }:
                continue

            result[layer].add(
                int(row["segment_id"]) + 1
            )

    return dict(result)


def _load_accepted(
    filename: str,
) -> list[dict[str, str]]:
    path = DATA_DIR / filename

    with path.open(
        newline="",
        encoding="utf-8",
    ) as handle:
        return [
            row
            for row in csv.DictReader(handle)
            if row["status"] == "accepted"
        ]


def test_a10_p03_dataset_is_one_global_cycle() -> None:
    same_colour = (
        _load_accepted(
            "endpoint_adjudication.csv"
        )
        + _load_accepted(
            "residual_endpoint_review.csv"
        )
    )

    cross_colour = _load_accepted(
        "cross_colour_endpoint_review.csv"
    )

    audit = audit_global_cycle(
        _load_segment_ids(),
        same_colour,
        cross_colour,
    )

    expected_traversal = (
        "R:S01+",
        "R:S02+",
        "R:S03+",
        "R:S04−",
        "R:S05+",
        "R:S06−",
        "R:S07+",
        "G:S11−",
        "G:S10−",
        "G:S09−",
        "G:S08−",
        "G:S07+",
        "G:S06−",
        "G:S05−",
        "G:S04−",
        "G:S03+",
        "G:S02−",
        "G:S01−",
        "B:S01+",
        "B:S02−",
        "B:S03+",
        "B:S04+",
        "B:S05+",
        "B:S06+",
    )

    assert audit.is_single_cycle
    assert audit.visible_segment_count == 24
    assert (
        audit.same_colour_connection_count
        == 21
    )
    assert (
        audit.cross_colour_transition_count
        == 3
    )
    assert audit.vertex_count == 48
    assert audit.edge_count == 48
    assert audit.component_count == 1
    assert audit.degree_map == {2: 48}

    assert tuple(
        format_segment_visit(visit)
        for visit in audit.segment_traversal
    ) == expected_traversal

    assert audit.cross_colour_transitions == (
        "X_RG_R_S07E_G_S11E",
        "X_GB_G_S01S_B_S01S",
        "X_RB_R_S01S_B_S06E",
    )
