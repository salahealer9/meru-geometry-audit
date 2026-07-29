"""Regression checks for the frozen A10_P03 manual parity-event audit."""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

DATA_DIR = (
    ROOT
    / "data"
    / "manual_adjudications"
    / "A10_P03"
)

EVENT_PATH = (
    DATA_DIR
    / "manual_parity_event_audit.csv"
)

FAMILY_PATH = (
    DATA_DIR
    / "manual_parity_family_review.csv"
)

REPORT_PATH = (
    ROOT
    / "reports"
    / "A10_P03_manual_parity_event_audit.md"
)

EXPECTED_EVENTS = {
    "E01",
    "E03",
    "E05",
    "E07",
    "E09",
    "E13",
    "E14",
    "E15",
    "E16",
    "E17",
    "E21",
    "E22",
    "E23",
    "E24",
    "E28",
    "E30",
}

EXPECTED_RELATIONS = {
    "E01": ("Blue S04", "Green S03"),
    "E03": ("Blue S03", "Red S04"),
    "E05": ("Red S03", "Green S07"),
    "E07": ("Green S04", "Red S06"),
    "E09": ("Blue S03", "Red S03"),
    "E13": ("Red S01", "Green S10"),
    "E14": ("Red S03", "Blue S02"),
    "E15": ("Blue S01", "Red S02"),
    "E16": ("Blue S04", "Green S04"),
    "E17": ("Green S06", "Blue S03"),
    "E21": ("Red S01", "Green S09"),
    "E22": ("Green S04", "Green S02"),
    "E23": ("Green S06", "Blue S04"),
    "E24": ("Blue S01", "Red S01"),
    "E28": ("Green S04", "Red S07"),
    "E30": ("Green S04", "Blue S05"),
}


def read_csv(
    path: Path,
) -> list[dict[str, str]]:
    """Read one audit CSV."""
    with path.open(
        newline="",
        encoding="utf-8",
    ) as handle:
        return list(csv.DictReader(handle))


def test_manual_audit_has_exact_affected_event_set() -> None:
    """The audit must contain every and only parity-affected event."""
    rows = read_csv(EVENT_PATH)

    event_ids = [
        row["event_id"]
        for row in rows
    ]

    assert len(event_ids) == 16
    assert len(set(event_ids)) == 16
    assert set(event_ids) == EXPECTED_EVENTS


def test_manual_audit_preserves_crossing_relations() -> None:
    """The frozen event relations must match the reviewed relations."""
    rows = read_csv(EVENT_PATH)

    actual = {
        row["event_id"]: (
            row["over_strand"],
            row["under_strand"],
        )
        for row in rows
    }

    assert actual == EXPECTED_RELATIONS


def test_manual_audit_records_local_confirmation_only() -> None:
    """All local reviews passed without claiming a global repair."""
    rows = read_csv(EVENT_PATH)

    for row in rows:
        assert row["classical_even_condition"] == "violate"
        assert row["local_visit_order_confirmed"] == "yes"
        assert row["over_under_confirmed"] == "yes"
        assert (
            row["reviewed_segment_interior_complete"]
            == "yes"
        )
        assert row["additional_crossing_observed"] == "no"
        assert row["confidence"] == "high"


def test_family_review_preserves_unresolved_red_routes() -> None:
    """The known Red S04 route uncertainties must remain explicit."""
    rows = read_csv(FAMILY_PATH)

    unresolved = " ".join(
        row["unresolved_continuations"]
        for row in rows
    )

    assert "R:S03E <-> R:S04E" in unresolved
    assert "R:S04S <-> R:S05S" in unresolved


def test_report_states_the_interpretive_boundary() -> None:
    """The report must not promote the visible word to a knot diagram."""
    text = REPORT_PATH.read_text(
        encoding="utf-8",
    )

    # Markdown source may wrap prose across physical lines.
    normalized = " ".join(
        text.split()
    )

    assert (
        "These findings do not repair or validate the "
        "global Gauss word."
        in normalized
    )

    assert (
        "visible-crossing baseline extracted from an "
        "occluded or schematic surface rendering"
        in normalized
    )

    assert (
        "The present audit does not yet distinguish "
        "conclusively among those possibilities."
        in normalized
    )
