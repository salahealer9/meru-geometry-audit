"""Regression tests for the A10_P03–tumble.gif correspondence."""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

CORRESPONDENCE_PATH = (
    ROOT
    / "data"
    / "manual_adjudications"
    / "A10_P03"
    / "A10_P03_tumble_correspondence.csv"
)

MANIFEST_PATH = (
    ROOT
    / "data"
    / "source_manifests"
    / "meru_3_10_digital"
    / "official_asset_manifest.csv"
)

REPORT_PATH = (
    ROOT
    / "reports"
    / "A10_P03_tumble_correspondence.md"
)

TUMBLE_URL = (
    "https://www.meru.org/compuimages/tumble.gif"
)

EXPECTED_SHA256 = (
    "a61a01353d51d3c09bc57b8c5f13d492"
    "3a5f020d7dd35f33b466e2b282ea3303"
)


def read_csv(
    path: Path,
) -> list[dict[str, str]]:
    """Read one CSV table."""
    with path.open(
        newline="",
        encoding="utf-8",
    ) as handle:
        return list(csv.DictReader(handle))


def test_correspondence_uses_frozen_animation_source() -> None:
    """The correspondence must reference the catalogued GIF bytes."""
    rows = read_csv(CORRESPONDENCE_PATH)

    assert len(rows) == 1

    row = rows[0]

    assert row["source_animation_url"] == TUMBLE_URL
    assert row["source_animation_sha256"] == EXPECTED_SHA256
    assert row["animation_frame_count"] == "96"

    manifest = {
        item["canonical_url"]: item
        for item in read_csv(MANIFEST_PATH)
    }

    assert TUMBLE_URL in manifest
    assert manifest[TUMBLE_URL]["sha256"] == EXPECTED_SHA256


def test_frame_and_transformation_are_frozen() -> None:
    """Frame zero must retain the exact vertical reflection."""
    row = read_csv(CORRESPONDENCE_PATH)[0]

    assert row["candidate_frame"] == "0"
    assert row["transformation"] == "vertical reflection"
    assert row["coordinate_map"] == "x'=x; y'=H-1-y"

    assert row["in_plane_rotation_degrees"] == "0"
    assert row["horizontal_translation_pixels"] == "0"
    assert row["vertical_translation_pixels"] == "0"
    assert row["scale_factor"] == "1"


def test_correspondence_is_schematic_not_metric() -> None:
    """The adjudication must retain its limited evidential role."""
    row = read_csv(CORRESPONDENCE_PATH)[0]

    assert row["correspondence_status"] == (
        "strong structural schematic correspondence"
    )

    assert row["confidence"] == "high"

    assert row["interpretive_use"] == (
        "historical and schematic source correspondence only"
    )

    assert (
        "must not be treated as a complete planar knot diagram"
        in row["prohibited_use"]
    )


def test_report_closes_the_hand_drawing_reconstruction_stage() -> None:
    """The report must direct future certification to native geometry."""
    normalized = " ".join(
        REPORT_PATH.read_text(
            encoding="utf-8",
        ).split()
    )

    assert (
        "Strong structural schematic correspondence."
        in normalized
    )

    assert (
        "It is not suitable as an independent source for:"
        in normalized
    )

    assert (
        "complete classical Gauss word"
        in normalized
    )

    assert (
        "No further crossing-by-crossing reconstruction should "
        "be forced from A10_P03."
        in normalized
    )

    assert (
        "Subsequent mathematical certification should use the "
        "recovered native `10_3.wrl` geometry."
        in normalized
    )
