"""Regression tests for the Meru digital 3,10 source catalogue."""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

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
    / "meru_3_10_digital_source_catalogue.md"
)

EXPECTED_ASSETS = {
    "https://www.meru.org/compuimages/tumble.gif": {
        "byte_count": "957858",
        "sha256": (
            "a61a01353d51d3c09bc57b8c5f13d492"
            "3a5f020d7dd35f33b466e2b282ea3303"
        ),
        "media_type": "image/gif",
    },
    "https://www.meru.org/compuimages/1_3-3_1B.wrl": {
        "byte_count": "198807",
        "sha256": (
            "82833c46baddc1b6709a7ff9b7e9c816"
            "92203eed7cda63d5b9792dd9ac42ba3a"
        ),
        "media_type": "model/vrml",
    },
    "https://www.meru.org/compuimages/10_3.wrl": {
        "byte_count": "429161",
        "sha256": (
            "855c46cfeeb31e4394b7a4a294b397aa"
            "c4cbc14154e172a326e33243dd9e384b"
        ),
        "media_type": "model/vrml",
    },
}


def read_manifest() -> list[dict[str, str]]:
    """Read the tracked source manifest."""
    with MANIFEST_PATH.open(
        newline="",
        encoding="utf-8",
    ) as handle:
        return list(csv.DictReader(handle))


def test_catalogue_contains_all_recovered_resources() -> None:
    """The catalogue must retain all six recovered resources."""
    rows = read_manifest()

    assert len(rows) == 6
    assert all(
        row["status"] == "retrieved"
        for row in rows
    )


def test_native_and_animation_hashes_are_frozen() -> None:
    """The three digital assets must retain their exact hashes."""
    rows = {
        row["canonical_url"]: row
        for row in read_manifest()
    }

    for url, expected in EXPECTED_ASSETS.items():
        assert url in rows

        actual = rows[url]

        assert actual["byte_count"] == expected["byte_count"]
        assert actual["sha256"] == expected["sha256"]
        assert actual["media_type"] == expected["media_type"]


def test_vrml_assets_declare_vrml_97() -> None:
    """Both native models must be identified as VRML 97 files."""
    rows = read_manifest()

    vrml_rows = [
        row
        for row in rows
        if row["media_type"] == "model/vrml"
    ]

    assert len(vrml_rows) == 2

    for row in vrml_rows:
        assert "#VRML V2.0 utf8" in row["technical_detail"]


def test_source_bytes_remain_untracked_by_policy() -> None:
    """Every source snapshot must retain the local-only policy."""
    rows = read_manifest()

    assert all(
        row["snapshot_policy"]
        == "local untracked third-party research copy"
        for row in rows
    )


def test_report_preserves_the_topological_boundary() -> None:
    """The source label must not be treated as topology verification."""
    normalized = " ".join(
        REPORT_PATH.read_text(
            encoding="utf-8",
        ).split()
    )

    assert (
        "They do not by themselves prove that the encoded "
        "geometry is topologically equivalent"
        in normalized
    )

    assert (
        "No knot-type conclusion will be made from the "
        "published label alone."
        in normalized
    )


def test_one_three_asset_is_classified_separately() -> None:
    """The 1/3–3/1 model must not be classified as a 3,10 model."""
    rows = {
        row["canonical_url"]: row
        for row in read_manifest()
    }

    url = (
        "https://www.meru.org/compuimages/"
        "1_3-3_1B.wrl"
    )

    assert rows[url]["audit_role"] == (
        "separate 3-around-1 / 1-around-3 "
        "Tree of Life model"
    )

    normalized = " ".join(
        REPORT_PATH.read_text(
            encoding="utf-8",
        ).split()
    )

    assert (
        "It is not presented as an alternative native "
        "model of the 3,10 torus knot."
        in normalized
    )

    assert (
        "excluded from the A10_P03-to-3,10 model "
        "correspondence analysis"
        in normalized
    )
