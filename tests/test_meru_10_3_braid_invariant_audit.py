"""Regression tests for the Meru 10_3 braid and invariant audit."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

AUDIT_PATH = (
    ROOT
    / "data"
    / "derived"
    / "meru_3_10_digital"
    / "meru_10_3_braid_invariant_audit.json"
)

REPORT_PATH = (
    ROOT
    / "reports"
    / "meru_10_3_braid_invariant_audit.md"
)

EXPECTED_SHA256 = (
    "855c46cfeeb31e4394b7a4a294b397aa"
    "c4cbc14154e172a326e33243dd9e384b"
)

EXPECTED_POLYNOMIAL = (
    "t**18 - t**17 + t**15 - t**14 + t**12 - t**11 "
    "+ t**9 - t**7 + t**6 - t**4 + t**3 - t + 1"
)


def read_audit() -> dict[str, Any]:
    """Read the frozen braid audit."""
    return json.loads(
        AUDIT_PATH.read_text(
            encoding="utf-8",
        )
    )


def test_braid_audit_uses_frozen_native_source() -> None:
    """The braid must be reconstructed from the verified native bytes."""
    audit = read_audit()

    assert audit["source"]["sha256"] == EXPECTED_SHA256
    assert audit["source"]["filename"] == "f24de4a08a_10_3.wrl"

    assert audit["centreline"]["section_count"] == 300
    assert audit["centreline"]["points_per_section"] == 20
    assert audit["centreline"][
        "orientation_reversed_for_increasing_phase"
    ] is True


def test_projection_is_generic_and_exhaustive() -> None:
    """Every isolated crossing must be enumerated with strong margins."""
    projection = read_audit()["braid_projection"]

    assert projection["piecewise_linear_breakpoint_count"] == 301
    assert projection["crossing_count"] == 20

    assert projection[
        "minimum_crossing_margin_at_breakpoints"
    ] > 1.0

    assert projection["minimum_depth_gap"] > 30.0

    assert projection[
        "minimum_third_strand_projection_gap"
    ] > 40.0

    assert projection[
        "minimum_event_to_breakpoint_margin"
    ] > 0.005


def test_recovered_word_is_negative_three_ten_torus_braid() -> None:
    """The signed word must be the tenfold negative two-generator block."""
    braid = read_audit()["braid"]

    expected_word = [
        value
        for _ in range(10)
        for value in (
            -2,
            -1,
        )
    ]

    assert braid["signed_word"] == expected_word
    assert braid["writhe"] == -20
    assert braid["induced_permutation"] == [2, 0, 1]
    assert braid["closure_component_count"] == 1

    assert braid["all_negative"] is True
    assert braid["all_positive"] is False

    assert braid[
        "negative_3_10_torus_pattern_up_to_cyclic_shift"
    ] is True

    assert braid[
        "positive_3_10_torus_pattern_up_to_cyclic_shift"
    ] is False


def test_alexander_polynomial_matches_three_ten_torus_knot() -> None:
    """The Burau invariant must agree with the T(3,10) formula."""
    alexander = read_audit()["alexander"]

    assert alexander["computed_polynomial"] == EXPECTED_POLYNOMIAL
    assert alexander["expected_T_3_10_polynomial"] == (
        EXPECTED_POLYNOMIAL
    )

    assert alexander["matches_T_3_10"] is True
    assert alexander["degree"] == 18
    assert alexander["determinant_absolute_delta_minus_one"] == 3


def test_report_preserves_interpretive_boundaries() -> None:
    """The report must distinguish braid evidence from broader claims."""
    audit = read_audit()

    assert audit["scope"][
        "projection_is_piecewise_linear"
    ] is True

    assert audit["scope"][
        "crossing_roots_enumerated_on_every_piecewise_linear_interval"
    ] is True

    assert audit["scope"][
        "alexander_polynomial_distinguishes_mirror_image"
    ] is False

    assert audit["scope"][
        "chirality_evidence_comes_from_signed_braid_word"
    ] is True

    assert audit["scope"]["formal_exact_arithmetic"] is False

    normalized = " ".join(
        REPORT_PATH.read_text(
            encoding="utf-8",
        ).lower().split()
    )

    assert (
        "the native centreline is the negative three-strand "
        "torus braid"
        in normalized
    )

    assert (
        "the alexander polynomial is mirror-insensitive"
        in normalized
    )

    assert (
        "not a formal exact-arithmetic proof"
        in normalized
    )

    assert (
        "does not independently establish broader linguistic, "
        "cosmological or consciousness-related interpretations"
        in normalized
    )
