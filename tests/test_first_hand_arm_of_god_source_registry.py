"""Tests for the Arm of God source lock and v0.8 protocol."""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

MANIFEST_PATH = (
    ROOT
    / "data"
    / "source_manifests"
    / "first_hand_arm_of_god"
    / "official_asset_manifest.csv"
)

CLAIMS_PATH = (
    ROOT
    / "data"
    / "source_claims"
    / "first_hand_arm_of_god_claims.csv"
)

PROTOCOL_PATH = (
    ROOT
    / "docs"
    / "first_hand_self_embedment_protocol.md"
)

REPORT_PATH = (
    ROOT
    / "reports"
    / "arm_of_god_source_lock.md"
)

EXPECTED_URL = (
    "https://www.meru.org/NewReleases/"
    "ARMOFGODRef21sep0CPC.2005A.pdf"
)

EXPECTED_SHA256 = (
    "80d52f4b6afefe65ae50e4c01378765"
    "c34ae4fde1ad44e8b299870c2e1d3e6fa"
)


def read_csv(
    path: Path,
) -> list[dict[str, str]]:
    """Read a CSV file."""
    with path.open(
        newline="",
        encoding="utf-8",
    ) as handle:
        return list(
            csv.DictReader(
                handle
            )
        )


def test_primary_source_identity_is_frozen() -> None:
    """The source registry must retain the audited PDF identity."""
    rows = read_csv(
        MANIFEST_PATH
    )

    assert len(rows) == 1

    row = rows[0]

    assert row["asset_id"] == "AOG_PDF_2005A"
    assert row["canonical_url"] == EXPECTED_URL
    assert row["sha256"] == EXPECTED_SHA256
    assert row["bytes"] == "1343797"
    assert row["pages"] == "16"
    assert row["media_type"] == "application/pdf"

    assert (
        "raw bytes locally preserved and ignored"
        in row["tracking_policy"]
    )


def test_claim_registry_has_unique_required_rows() -> None:
    """Every initial source claim must have a unique stable ID."""
    rows = read_csv(
        CLAIMS_PATH
    )

    ids = [
        row["claim_id"]
        for row in rows
    ]

    assert len(ids) == len(
        set(ids)
    )

    assert set(ids) == {
        f"AOG-C{index:02d}"
        for index in range(
            1,
            11,
        )
    }

    assert {
        row["source_page"]
        for row in rows
    } <= {
        "5",
        "5-7",
        "6",
        "7",
        "8",
        "9",
    }


def test_endpoint_conventions_remain_separate() -> None:
    """The prose and diagram truncations must not be conflated."""
    rows = {
        row["claim_id"]: row
        for row in read_csv(
            CLAIMS_PATH
        )
    }

    assert rows["AOG-C05"]["variant"] == (
        "TRUNCATION_PROSE"
    )

    assert "3*pi" in rows[
        "AOG-C05"
    ][
        "parameters_fixed"
    ]

    assert rows["AOG-C06"]["variant"] == (
        "TRUNCATION_DIAGRAM"
    )

    assert "[1, 1+3*pi]" in rows[
        "AOG-C06"
    ][
        "parameters_fixed"
    ]


def test_protocol_freezes_the_three_predicate_ladder() -> None:
    """S1, S1.5 and S2 must remain distinct."""
    normalized = " ".join(
        PROTOCOL_PATH.read_text(
            encoding="utf-8",
        ).split()
    )

    assert (
        "S1 — directed endpoint-tangent alignment"
        in normalized
    )

    assert (
        "Antiparallel tangents do not pass."
        in normalized
    )

    assert (
        "S1.5 — full endpoint-frame alignment"
        in normalized
    )

    assert (
        "S2 — collision-free recursive nesting"
        in normalized
    )

    assert (
        "Passing S1 does not imply S1.5, "
        "and passing S1.5 does not imply S2."
        in normalized
    )


def test_source_lock_contains_no_geometric_verdict() -> None:
    """Phase 0 must remain a source lock rather than a result."""
    normalized = " ".join(
        REPORT_PATH.read_text(
            encoding="utf-8",
        ).lower().split()
    )

    assert (
        "this checkpoint records source identity "
        "and test architecture only"
        in normalized
    )

    assert (
        "contains no verdict on"
        in normalized
    )

    assert (
        "both interpretations are retained"
        in normalized
    )

    assert (
        "classified as internally ambiguous rather than rejected"
        in normalized
    )
