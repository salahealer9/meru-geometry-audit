"""Tests for the First Hand incidence-landmark addendum."""

from __future__ import annotations

import csv
import hashlib
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
    / "first_hand_incidence_addendum_protocol.md"
)

CHECKSUM_PATH = (
    ROOT
    / "data"
    / "derived"
    / "first_hand_arm_of_god"
    / "diagram_landmark_passes.sha256"
)

PASS_DIR = CHECKSUM_PATH.parent

CENTRAL_ID = "AOG-LM-P07-CENTRAL-REFERENCE-NODE"

ADDENDUM_IDS = {
    "AOG-LM-P07-X1-UC-LL-INTERSECTION",
    "AOG-LM-P07-X1-UC-LR-INTERSECTION",
    "AOG-LM-P07-YAXIS-UC-UCLR-INTERSECTION",
}


def read_registry() -> list[dict[str, str]]:
    """Read the landmark registry."""
    with REGISTRY_PATH.open(
        newline="",
        encoding="utf-8",
    ) as handle:
        return list(
            csv.DictReader(handle)
        )


def normalized_protocol() -> str:
    """Return lowercase whitespace-normalized protocol text."""
    return " ".join(
        PROTOCOL_PATH.read_text(
            encoding="utf-8",
        )
        .lower()
        .split()
    )


def sha256_path(path: Path) -> str:
    """Return a file SHA-256 digest."""
    digest = hashlib.sha256()

    with path.open("rb") as handle:
        for block in iter(
            lambda: handle.read(1 << 20),
            b"",
        ):
            digest.update(block)

    return digest.hexdigest()


def test_three_addendum_ids_are_unique_and_registered() -> None:
    """Exactly three new point rows must carry addendum status."""
    rows = read_registry()
    ids = [
        row["landmark_id"]
        for row in rows
    ]

    assert len(ids) == len(set(ids))
    assert ADDENDUM_IDS <= set(ids)

    addendum_rows = [
        row
        for row in rows
        if (
            row["status"]
            == "preregistered_incidence_addendum"
        )
    ]

    assert {
        row["landmark_id"]
        for row in addendum_rows
    } == ADDENDUM_IDS

    for row in addendum_rows:
        assert row["object_type"] == "point"
        assert row["minimum_samples"] == "2"
        assert (
            "one click per pass"
            in row["acquisition_mode"]
        )


def test_central_node_is_described_as_circular_not_square() -> None:
    """The stable central ID must retain corrected morphology."""
    rows = {
        row["landmark_id"]: row
        for row in read_registry()
    }

    central = rows[CENTRAL_ID]
    combined = " ".join(
        [
            central["source_feature"],
            central["geometry_role"],
            central["acquisition_mode"],
            central["allowed_use"],
            central["exclusions"],
        ]
    ).lower()

    assert "filled circular node" in combined
    assert "black square" not in combined
    assert "central black square" not in combined


def test_original_initial_status_count_remains_thirteen() -> None:
    """The original neutral-pass vocabulary must not be rewritten."""
    rows = read_registry()

    active = [
        row
        for row in rows
        if (
            row["status"]
            == "preregistered_not_digitized"
        )
    ]

    assert len(active) == 13

    assert not (
        ADDENDUM_IDS
        & {
            row["landmark_id"]
            for row in active
        }
    )


def test_frozen_pass_checksum_manifest_still_verifies() -> None:
    """The amendment must not alter original blind-pass evidence."""
    entries: dict[str, str] = {}

    for raw_line in CHECKSUM_PATH.read_text(
        encoding="utf-8",
    ).splitlines():
        if not raw_line.strip():
            continue

        digest, filename = raw_line.split()
        entries[filename] = digest

    assert set(entries) == {
        "diagram_landmarks_pass1.csv",
        "diagram_landmarks_pass2.csv",
    }

    for filename, expected in entries.items():
        assert sha256_path(
            PASS_DIR / filename
        ) == expected


def test_protocol_freezes_angle_and_interpretation_boundary() -> None:
    """The addendum must define the new diagnostic without fitting it."""
    text = normalized_protocol()

    assert "angle(uclr, central, lr)" in text
    assert "ambiguous printed 30-degree arc" in text
    assert "remains deferred" in text
    assert "distinct from the central circular node" in text
    assert "no addendum pass data exist" in text

    for forbidden in (
        "great-circle curve fit",
        "projective-map selection",
        "unit-angle selection",
        "truncation reconciliation",
        "s1",
        "s1.5",
        "s2",
    ):
        assert forbidden in text
