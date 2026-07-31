"""Tests for the First Hand diagram landmark protocol."""

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

REQUIRED_PARTITIONS = {
    "calibration",
    "scale_calibration",
    "holdout",
    "external_holdout",
}

REQUIRED_IDS = {
    "AOG-LM-P07-SPHERE-BOUNDARY",
    "AOG-LM-P07-EQUATOR-ARC",
    "AOG-LM-P07-GC-Y0",
    "AOG-LM-P07-GC-Y1",
    "AOG-LM-P07-GC-X1",
    "AOG-LM-P07-GC-YAXIS",
    "AOG-LM-P07-INFINITY-Y0-Y1",
    "AOG-LM-P07-UNIT-R1-THETA1",
    "AOG-LM-P07-INNER-END-DIAGRAM",
    "AOG-LM-P07-SPIRAL-CENTRELINE",
    "AOG-LM-P07-THIRTY-DEGREE-ARC",
    "AOG-LM-P08-HAND-TOP-BOUNDARY",
    "AOG-LM-P08-HAND-SIDE-BOUNDARY",
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


def test_registry_has_unique_complete_ids() -> None:
    """The preregistered landmark vocabulary must remain stable."""
    rows = read_registry()

    ids = [
        row["landmark_id"]
        for row in rows
    ]

    assert len(rows) == len(REQUIRED_IDS)
    assert len(ids) == len(set(ids))
    assert set(ids) == REQUIRED_IDS

    assert all(
        row["status"] == "preregistered_not_digitized"
        for row in rows
    )


def test_registry_separates_fit_partitions() -> None:
    """Calibration, scale, and holdout objects must stay distinct."""
    rows = read_registry()

    partitions = {
        row["fit_partition"]
        for row in rows
    }

    assert partitions == REQUIRED_PARTITIONS

    by_id = {
        row["landmark_id"]: row
        for row in rows
    }

    assert (
        by_id[
            "AOG-LM-P07-SPIRAL-CENTRELINE"
        ]["fit_partition"]
        == "holdout"
    )

    assert (
        by_id[
            "AOG-LM-P07-UNIT-R1-THETA1"
        ]["fit_partition"]
        == "scale_calibration"
    )

    assert (
        by_id[
            "AOG-LM-P08-HAND-TOP-BOUNDARY"
        ]["fit_partition"]
        == "external_holdout"
    )


def test_protocol_blinds_digitization_from_model_results() -> None:
    """Landmark selection must precede overlays and fit scores."""
    text = normalized_protocol()

    assert "no theoretical curve" in text
    assert "projection overlay" in text
    assert "self-embedment score may be displayed" in text

    assert (
        "point landmarks are clicked twice "
        "in independent passes"
        in text
    )

    assert (
        "moving landmarks after seeing residuals"
        in text
    )


def test_protocol_freezes_scale_selection_boundary() -> None:
    """Scale must not be chosen from self-embedment performance."""
    text = normalized_protocol()

    for scale_id in (
        "g30",
        "ghalf",
        "gunit",
        "gone",
    ):
        assert scale_id in text

    assert (
        "no scale may be selected using "
        "s1, s1.5, s2, or the final hand shape"
        in text
    )

    assert (
        "a continuous scale fit may be reported only "
        "as a sensitivity analysis"
        in text
    )


def test_protocol_contains_no_coordinates_or_verdict() -> None:
    """This checkpoint must remain purely preregistrational."""
    text = normalized_protocol()

    assert (
        "this protocol contains no landmark coordinates"
        in text
    )

    assert "fitted parameters" in text
    assert "projection verdict" in text
    assert "scale selection" in text
    assert "self-embedment result" in text

    assert (
        "each registered geometric object receives "
        "equal top-level weight"
        in text
    )

    assert "metric-compatible" in text
    assert "schematic-compatible" in text
    assert "incompatible" in text
