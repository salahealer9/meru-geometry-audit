"""Tests for the revised First Hand landmark semantics."""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

REGISTRY_PATH = (
    ROOT
    / "data"
    / "source_claims"
    / "first_hand_diagram_landmark_registry.csv"
)

PROTOCOL_PATH = (
    ROOT
    / "docs"
    / "first_hand_diagram_landmark_protocol.md"
)

INITIAL_STATUS = "preregistered_not_digitized"

RIM_IDS = {
    "AOG-LM-P07-RIM-NODE-UL",
    "AOG-LM-P07-RIM-NODE-UR",
    "AOG-LM-P07-RIM-NODE-R",
    "AOG-LM-P07-RIM-NODE-LR-SHARED",
    "AOG-LM-P07-RIM-NODE-LL",
    "AOG-LM-P07-RIM-NODE-L",
}

GREAT_CIRCLE_IDS = {
    "AOG-LM-P07-GC-Y0",
    "AOG-LM-P07-GC-Y1",
    "AOG-LM-P07-GC-YAXIS",
    "AOG-LM-P07-GC-X1",
}


def read_registry() -> list[dict[str, str]]:
    """Read the landmark registry."""
    with REGISTRY_PATH.open(
        newline="",
        encoding="utf-8",
    ) as handle:
        return list(csv.DictReader(handle))


def normalized_protocol() -> str:
    """Return lowercase whitespace-normalized protocol text."""
    return " ".join(
        PROTOCOL_PATH.read_text(
            encoding="utf-8",
        )
        .lower()
        .split()
    )


def test_registry_ids_are_unique_and_rim_nodes_are_neutral() -> None:
    """The six rim nodes must be unique neutral source points."""
    rows = read_registry()
    ids = [row["landmark_id"] for row in rows]

    assert len(ids) == len(set(ids))
    assert RIM_IDS <= set(ids)

    by_id = {
        row["landmark_id"]: row
        for row in rows
    }

    for landmark_id in RIM_IDS:
        assert (
            "no coordinate-line meaning assigned in advance"
            in by_id[landmark_id]["geometry_role"]
            or
            landmark_id == "AOG-LM-P07-RIM-NODE-LR-SHARED"
        )


def test_shared_source_objects_are_not_duplicated() -> None:
    """The horizon limb and lower-right shared node each occur once."""
    rows = read_registry()
    ids = [row["landmark_id"] for row in rows]

    assert ids.count(
        "AOG-LM-P07-EQUATOR-HORIZON-LIMB"
    ) == 1

    assert ids.count(
        "AOG-LM-P07-RIM-NODE-LR-SHARED"
    ) == 1

    assert "AOG-LM-P07-SPHERE-BOUNDARY" not in ids
    assert "AOG-LM-P07-EQUATOR-ARC" not in ids
    assert "AOG-LM-P07-INFINITY-Y0-Y1" not in ids


def test_unit_and_inner_endpoint_variants_remain_separate() -> None:
    """Panel-specific unit markers and endpoints must not merge."""
    ids = {
        row["landmark_id"]
        for row in read_registry()
    }

    assert {
        "AOG-LM-P07-FLAT-UNIT-R1-THETA1RAD",
        "AOG-LM-P07-SPHERE-UNIT-R1-ONEMONTH",
        "AOG-LM-P07-FLAT-INNER-END",
        "AOG-LM-P07-SPHERE-INNER-END",
    } <= ids


def test_great_circles_are_later_stage_without_node_assignments() -> None:
    """Printed great circles stay valid but do not drive pass 1."""
    by_id = {
        row["landmark_id"]: row
        for row in read_registry()
    }

    for landmark_id in GREAT_CIRCLE_IDS:
        row = by_id[landmark_id]

        assert row["status"] == "preregistered_later_stage"
        assert (
            "no preregistered rim-node assignment"
            in row["geometry_role"]
        )


def test_thirty_degree_arc_is_explicitly_deferred() -> None:
    """The ambiguous angular annotation must not enter a blind pass."""
    by_id = {
        row["landmark_id"]: row
        for row in read_registry()
    }

    row = by_id[
        "AOG-LM-P07-THIRTY-DEGREE-ARC"
    ]

    assert row["status"] == "deferred_source_ambiguous"
    assert "do not digitize" in row["exclusions"]


def test_protocol_freezes_neutral_census_and_no_verdict() -> None:
    """The revised protocol must remain pre-model and source-neutral."""
    text = normalized_protocol()

    assert "initial neutral census" in text
    assert "a sixfold rim arrangement is tested rather than assumed" in text
    assert "general projective map may preserve incidences without preserving right angles" in text

    assert (
        "contains no landmark coordinates, fitted geometry, "
        "projection verdict, scale selection, or self-embedment result"
        in text
    )


def test_scaffold_curve_is_independent_holdout() -> None:
    """The added scaffold curve must not become a coordinate constraint."""
    by_id = {
        row["landmark_id"]: row
        for row in read_registry()
    }

    row = by_id[
        "AOG-LM-P07-GC-SCAFFOLD-UR-UC-X1LL-LL"
    ]

    assert row["status"] == "preregistered_later_stage"
    assert row["object_type"] == "open_curve"
    assert row["fit_partition"] == "scaffold_holdout"

    assert (
        "no planar coordinate-line identity assigned in advance"
        in row["geometry_role"]
    )

    assert (
        "do not fit projective map or scale"
        in row["allowed_use"]
    )
