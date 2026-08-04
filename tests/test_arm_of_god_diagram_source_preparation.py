"""Tests for deterministic Arm of God diagram source preparation."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
from typing import Any

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]

MANIFEST_PATH = (
    ROOT
    / "data"
    / "source_manifests"
    / "first_hand_arm_of_god"
    / "diagram_crop_manifest.csv"
)

AUDIT_PATH = (
    ROOT
    / "data"
    / "derived"
    / "first_hand_arm_of_god"
    / "diagram_source_preparation.json"
)

REPORT_PATH = (
    ROOT
    / "reports"
    / "arm_of_god_diagram_source_preparation.md"
)

EXPECTED_SOURCE_SHA256 = (
    "80d52f4b6afefe65ae50e4c01378765"
    "c34ae4fde1ad44e8b299870c2e1d3e6fa"
)

EXPECTED_IDS = {
    "AOG_P07_SEVEN_REGION_INSET",
    "AOG_P07_SPHERICAL_PROJECTION",
    "AOG_P07_HAND_REGION",
    "AOG_P08_HAND_VIEWS",
    "AOG_P08_UNIT_ANGLE_CUBOCTAHEDRON",
}


def sha256_path(path: Path) -> str:
    """Return the SHA-256 digest of one file."""
    digest = hashlib.sha256()

    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)

    return digest.hexdigest()


def pixel_sha256(image: Image.Image) -> str:
    """Hash canonical image dimensions, mode, and raw pixel bytes."""
    canonical = image.convert("RGB")

    digest = hashlib.sha256()
    digest.update(
        f"{canonical.width}x{canonical.height}|RGB|".encode("ascii")
    )
    digest.update(canonical.tobytes())

    return digest.hexdigest()


def read_manifest() -> list[dict[str, str]]:
    """Read the crop manifest."""
    with MANIFEST_PATH.open(
        newline="",
        encoding="utf-8",
    ) as handle:
        return list(
            csv.DictReader(
                handle
            )
        )


def read_audit() -> dict[str, Any]:
    """Read the source-preparation audit."""
    return json.loads(
        AUDIT_PATH.read_text(
            encoding="utf-8",
        )
    )


def test_crop_registry_is_complete_and_unique() -> None:
    """All five source excerpts must have stable unique IDs."""
    rows = read_manifest()
    ids = [
        row["crop_id"]
        for row in rows
    ]

    assert len(rows) == 5
    assert len(ids) == len(
        set(ids)
    )
    assert set(ids) == EXPECTED_IDS


def test_every_crop_is_tied_to_the_locked_source() -> None:
    """No crop may lose the PDF identity or raster convention."""
    rows = read_manifest()

    for row in rows:
        assert row["source_asset"] == "AOG_PDF_2005A"
        assert row["source_sha256"] == EXPECTED_SOURCE_SHA256
        assert row["dpi"] == "300"
        assert row["full_width_px"] == "2550"
        assert row["full_height_px"] == "3300"
        assert row["source_page"] in {"7", "8"}


def test_crop_boxes_and_output_dimensions_are_consistent() -> None:
    """Each prepared PNG must match its frozen half-open crop box."""
    rows = read_manifest()

    for row in rows:
        left = int(row["left_px"])
        top = int(row["top_px"])
        right = int(row["right_px"])
        bottom = int(row["bottom_px"])

        width = int(row["output_width_px"])
        height = int(row["output_height_px"])

        assert 0 <= left < right <= 2550
        assert 0 <= top < bottom <= 3300

        assert width == right - left
        assert height == bottom - top


def test_prepared_pngs_match_manifest_hashes() -> None:
    """File and canonical pixel hashes must protect every crop."""
    rows = read_manifest()

    for row in rows:
        path = ROOT / row["output_path"]

        assert path.exists()
        assert sha256_path(path) == row["file_sha256"]

        with Image.open(path) as opened:
            image = opened.convert("RGB")

        assert image.size == (
            int(row["output_width_px"]),
            int(row["output_height_px"]),
        )

        assert pixel_sha256(image) == row["pixel_sha256"]


def test_source_preparation_does_not_claim_calibration() -> None:
    """This checkpoint must remain prior to landmark fitting."""
    audit = read_audit()
    scope = audit["scope"]

    assert scope["source_preparation_only"] is True
    assert scope["landmarks_digitized"] is False
    assert scope["projection_scale_calibrated"] is False
    assert scope["projective_gauge_calibrated"] is False
    assert scope["self_embedment_scores_computed"] is False

    normalized = " ".join(
        REPORT_PATH.read_text(
            encoding="utf-8",
        ).lower().split()
    )

    assert (
        (
            "this checkpoint does **not**"
            in normalized
            or
            "this checkpoint does not"
            in normalized
        )
        and "digitize sphere" in normalized
    )

    assert (
        "the next checkpoint must preregister "
        "a landmark vocabulary"
        in normalized
    )
