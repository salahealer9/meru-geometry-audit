"""Regression tests for the First Hand spherical-map family audit."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

AUDIT_PATH = (
    ROOT
    / "data"
    / "derived"
    / "first_hand_arm_of_god"
    / "spherical_map_family_audit.json"
)

REPORT_PATH = (
    ROOT
    / "reports"
    / "first_hand_spherical_map_family_audit.md"
)

EXPECTED_SHA256 = (
    "80d52f4b6afefe65ae50e4c01378765"
    "c34ae4fde1ad44e8b299870c2e1d3e6fa"
)


def read_audit() -> dict[str, Any]:
    """Read the permanent spherical-map audit."""
    return json.loads(
        AUDIT_PATH.read_text(
            encoding="utf-8",
        )
    )


def test_spherical_map_audit_is_tied_to_locked_source() -> None:
    """The result must remain tied to the same primary-source bytes."""
    audit = read_audit()

    assert audit["source"]["asset_id"] == "AOG_PDF_2005A"
    assert audit["source"]["sha256"] == EXPECTED_SHA256
    assert audit["checks"]["source_identity_pass"] is True
    assert audit["checks"]["planar_audit_dependency_pass"] is True


def test_all_frozen_gnomonic_scales_pass_incidence_constraints() -> None:
    """Incidence alone must not select among the four scale hypotheses."""
    audit = read_audit()

    variants = audit[
        "canonical_family"
    ][
        "variant_results"
    ]

    assert set(variants) == {
        "G30",
        "GHALF",
        "GUNIT",
        "GONE",
    }

    assert all(
        item[
            "all_source_incidence_constraints_pass"
        ]
        is True
        for item in variants.values()
    )

    assert audit["checks"][
        "all_tested_gnomonic_scales_pass"
    ] is True

    assert audit["checks"][
        "gnomonic_max_line_residual"
    ] < 1.0e-12


def test_stereographic_comparator_fails_offset_line_constraints() -> None:
    """Inverse stereography must not pass the source-labelled offset lines."""
    audit = read_audit()
    comparator = audit["comparator"]

    assert comparator[
        "line_constraints"
    ][
        "x_axis"
    ][
        "passes"
    ] is True

    assert comparator[
        "line_constraints"
    ][
        "y_axis"
    ][
        "passes"
    ] is True

    assert comparator[
        "line_constraints"
    ][
        "x_equals_1"
    ][
        "passes"
    ] is False

    assert comparator[
        "line_constraints"
    ][
        "y_equals_1"
    ][
        "passes"
    ] is False

    assert comparator[
        "all_source_incidence_constraints_pass"
    ] is False

    assert audit["checks"][
        "stereographic_offset_lines_fail"
    ] is True


def test_projective_family_is_not_overclaimed_as_unique() -> None:
    """The audit must preserve the remaining projective freedom."""
    audit = read_audit()

    broader = audit[
        "broader_projective_family"
    ]

    assert "A @ (x,y,1)" in broader["formula"]

    assert broader[
        "anisotropy_shear_and_projective_gauge_excluded_by_current_constraints"
    ] is False

    assert broader[
        "global_spherical_rotation_identified"
    ] is False

    assert audit["checks"][
        "unique_map_identified"
    ] is False

    assert audit["checks"][
        "scale_calibrated"
    ] is False


def test_no_self_embedment_score_is_used_for_map_selection() -> None:
    """Map-family selection must precede all S1/S1.5/S2 testing."""
    audit = read_audit()

    assert audit["checks"][
        "self_embedment_scores_computed"
    ] is False

    scope = audit["scope"]

    assert scope[
        "s1_endpoint_alignment_verdict"
    ] is None

    assert scope[
        "s1_5_frame_alignment_verdict"
    ] is None

    assert scope[
        "s2_recursive_nesting_verdict"
    ] is None

    normalized = " ".join(
        REPORT_PATH.read_text(
            encoding="utf-8",
        ).lower().split()
    )

    assert (
        "no scale is selected by endpoint alignment"
        in normalized
    )

    assert (
        "the isotropic inverse gnomonic map is the simplest "
        "canonical member of that class"
        in normalized
    )

    assert (
        "the next phase is source-image calibration"
        in normalized
    )
