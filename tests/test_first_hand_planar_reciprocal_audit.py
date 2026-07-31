"""Regression tests for the First Hand planar reciprocal-spiral audit."""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

AUDIT_PATH = (
    ROOT
    / "data"
    / "derived"
    / "first_hand_arm_of_god"
    / "planar_reciprocal_spiral_audit.json"
)

REPORT_PATH = (
    ROOT
    / "reports"
    / "first_hand_planar_reciprocal_spiral_audit.md"
)

EXPECTED_SHA256 = (
    "80d52f4b6afefe65ae50e4c01378765"
    "c34ae4fde1ad44e8b299870c2e1d3e6fa"
)


def read_audit() -> dict[str, Any]:
    """Read the frozen planar audit."""
    return json.loads(
        AUDIT_PATH.read_text(
            encoding="utf-8",
        )
    )


def test_planar_audit_uses_frozen_primary_source() -> None:
    """The calculation must remain tied to the locked PDF bytes."""
    audit = read_audit()

    assert audit["source"]["sha256"] == EXPECTED_SHA256
    assert audit["source"]["bytes"] == 1_343_797
    assert audit["source"]["asset_id"] == "AOG_PDF_2005A"

    assert audit["checks"]["source_identity_pass"] is True


def test_reciprocal_curve_and_asymptotes_are_frozen() -> None:
    """The analytic curve and point-to-line limits must remain stable."""
    audit = read_audit()

    assert audit["curve"]["polar_equation"] == "r*theta=1"
    assert audit["curve"]["radius_function"] == "r(theta)=1/theta"

    outer = audit["analytic_limits"][
        "theta_to_zero_positive"
    ]

    inner = audit["analytic_limits"][
        "theta_to_positive_infinity"
    ]

    assert outer["x"] == "positive infinity"
    assert outer["y"] == 1.0
    assert outer[
        "oriented_tangent_inner_to_outer"
    ] == [1.0, 0.0]

    assert inner["x"] == 0.0
    assert inner["y"] == 0.0
    assert inner["radius"] == 0.0

    assert audit["checks"][
        "outer_limit_y_convergence_pass"
    ] is True

    assert audit["checks"][
        "outer_limit_tangent_convergence_pass"
    ] is True


def test_both_three_pi_truncations_remain_distinct() -> None:
    """The prose and diagram endpoint conventions must not merge."""
    audit = read_audit()
    variants = audit["truncation_variants"]

    prose = variants["AOG_PROSE"]
    diagram = variants["AOG_DIAGRAM"]

    assert prose["theta_outer"] == "0+"
    assert math.isclose(
        prose["theta_inner"],
        3.0 * math.pi,
        rel_tol=0.0,
        abs_tol=1.0e-14,
    )

    assert diagram["theta_outer"] == 1.0
    assert math.isclose(
        diagram["theta_inner"],
        1.0 + 3.0 * math.pi,
        rel_tol=0.0,
        abs_tol=1.0e-14,
    )

    assert math.isclose(
        prose["turns"],
        1.5,
        rel_tol=0.0,
        abs_tol=1.0e-14,
    )

    assert math.isclose(
        diagram["turns"],
        1.5,
        rel_tol=0.0,
        abs_tol=1.0e-14,
    )

    assert audit["checks"]["variants_are_distinct"] is True


def test_planar_endpoint_metrics_are_numerically_stable() -> None:
    """The frozen endpoint coordinates and tangent mismatches must persist."""
    variants = read_audit()["truncation_variants"]

    prose = variants["AOG_PROSE"]
    diagram = variants["AOG_DIAGRAM"]

    assert math.isclose(
        prose["inner_endpoint"]["radius"],
        1.0 / (3.0 * math.pi),
        rel_tol=0.0,
        abs_tol=1.0e-14,
    )

    assert math.isclose(
        prose[
            "directed_planar_tangent_mismatch_degrees"
        ],
        96.05661059423021,
        rel_tol=0.0,
        abs_tol=1.0e-10,
    )

    assert math.isclose(
        diagram["finite_planar_arc_length"],
        2.567874846510595,
        rel_tol=0.0,
        abs_tol=1.0e-12,
    )

    assert math.isclose(
        diagram[
            "outer_endpoint_absolute_y_minus_one"
        ],
        0.1585290151921035,
        rel_tol=0.0,
        abs_tol=1.0e-14,
    )

    assert math.isclose(
        diagram[
            "directed_planar_tangent_mismatch_degrees"
        ],
        140.47934975805714,
        rel_tol=0.0,
        abs_tol=1.0e-10,
    )


def test_planar_audit_does_not_prejudge_self_embedment() -> None:
    """The planar baseline must defer all spherical nesting verdicts."""
    audit = read_audit()
    scope = audit["scope"]

    assert scope["self_embedment_verdict"] is None
    assert scope["s1_endpoint_alignment_verdict"] is None
    assert scope["s1_5_frame_alignment_verdict"] is None
    assert scope["s2_recursive_nesting_verdict"] is None
    assert scope["formal_exact_arithmetic"] is False

    normalized = " ".join(
        REPORT_PATH.read_text(
            encoding="utf-8",
        ).lower().split()
    )

    assert (
        "no s1, s1.5 or s2 verdict is issued here"
        in normalized
    )

    assert (
        "testing it in the plane would answer a different question"
        in normalized
    )

    assert (
        "deferred to spherical map"
        in normalized
        or
        "no self-embedment verdict"
        in normalized
    )
