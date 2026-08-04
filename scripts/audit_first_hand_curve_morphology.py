#!/usr/bin/env python3
"""Post-hoc neutral morphology census for First Hand page-7 curves.

Adds a weighted orthogonal-line description to the already-frozen
QC-derived circle/ellipse census.

No projective map, great-circle identity, spherical scale, reciprocal
spiral, or self-embedment result is produced.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path
from typing import Any, Sequence

import numpy as np


ROOT = Path(__file__).resolve().parents[1]

root_text = str(ROOT)

if root_text not in sys.path:
    sys.path.insert(
        0,
        root_text,
    )

from scripts import audit_first_hand_curve_geometry as base
from scripts import audit_first_hand_curve_geometry_qc as qc_runner


DATA_DIR = (
    ROOT
    / "data"
    / "derived"
    / "first_hand_arm_of_god"
)

QC_DIR = DATA_DIR / "qc"

QC_RESULT = (
    QC_DIR
    / "first_hand_curve_geometry_qc_sensitivity.json"
)

QC_RESULT_SEAL = (
    QC_DIR
    / "first_hand_curve_geometry_qc_sensitivity.sha256"
)

OUTPUT_JSON = (
    QC_DIR
    / "first_hand_curve_morphology_census.json"
)

OUTPUT_REPORT = (
    ROOT
    / "reports"
    / "first_hand_curve_morphology_census.md"
)


def load_frozen_qc_result() -> dict[str, Any]:
    """Load and verify the sealed acquisition-QC sensitivity result."""
    qc_runner.verify_sha256_manifest(
        QC_RESULT_SEAL
    )

    if not QC_RESULT.exists():
        raise RuntimeError(
            f"Missing frozen QC result: {QC_RESULT}"
        )

    result = json.loads(
        QC_RESULT.read_text(
            encoding="utf-8",
        )
    )

    if (
        result.get("analysis_class")
        != "post_hoc_acquisition_qc_sensitivity"
    ):
        raise RuntimeError(
            "Unexpected frozen QC-result class."
        )

    return result


def fit_line(
    sample_sets: Sequence[base.ResampledCurve],
    limb_radius_px: float,
) -> dict[str, Any]:
    """Equal-pass weighted orthogonal line fit."""
    points, sigma, weights = (
        base.combined_points(
            sample_sets
        )
    )

    center = np.sum(
        points
        * weights[:, None],
        axis=0,
    )

    centered = (
        points
        - center
    )

    covariance = (
        centered.T
        @ (
            centered
            * weights[:, None]
        )
    )

    eigenvalues, eigenvectors = (
        np.linalg.eigh(
            covariance
        )
    )

    direction = np.asarray(
        eigenvectors[:, -1],
        dtype=np.float64,
    )

    norm = float(
        np.linalg.norm(
            direction
        )
    )

    if not (
        math.isfinite(norm)
        and norm > 0.0
    ):
        raise RuntimeError(
            "Line fit produced invalid direction."
        )

    direction /= norm

    # Canonical unoriented line direction.
    if (
        direction[0] < 0.0
        or (
            abs(
                direction[0]
            )
            <= 1.0e-15
            and direction[1] < 0.0
        )
    ):
        direction *= -1.0

    normal = np.asarray(
        [
            -direction[1],
            direction[0],
        ],
        dtype=np.float64,
    )

    signed_residual = (
        centered
        @ normal
    )

    bearing = math.degrees(
        math.atan2(
            float(
                direction[1]
            ),
            float(
                direction[0]
            ),
        )
    )

    while bearing < 0.0:
        bearing += 180.0

    while bearing >= 180.0:
        bearing -= 180.0

    return {
        "model": (
            "orthogonal_line"
        ),
        "center_x_px": float(
            center[0]
        ),
        "center_y_px": float(
            center[1]
        ),
        "direction_x": float(
            direction[0]
        ),
        "direction_y": float(
            direction[1]
        ),
        "unoriented_bearing_deg": (
            bearing
        ),
        "weighted_covariance_eigenvalues": [
            float(value)
            for value in eigenvalues
        ],
        "residual_definition": (
            "signed orthogonal image-space "
            "distance to weighted TLS line"
        ),
        "residuals": (
            base.residual_summary(
                signed_residual,
                sigma,
                weights,
                limb_radius_px,
            )
        ),
    }


def analyze_line_at_spacing(
    pass1_segments: Sequence[base.Segment],
    pass2_segments: Sequence[base.Segment],
    spacing_px: float,
    limb_radius_px: float,
) -> dict[str, Any]:
    pass1 = base.resample_curve(
        pass1_segments,
        spacing_px,
    )

    pass2 = base.resample_curve(
        pass2_segments,
        spacing_px,
    )

    return fit_line(
        [
            pass1,
            pass2,
        ],
        limb_radius_px,
    )


def build_analysis() -> dict[str, Any]:
    """Build the QC-derived neutral morphology census."""
    base.verify_input_seal()
    qc_runner.verify_qc_derivative()

    frozen = (
        load_frozen_qc_result()
    )

    passes = {
        1: base.read_curve_pass(
            base.PASS_PATHS[1],
            1,
        ),
        2: base.read_curve_pass(
            qc_runner.QC_PASS2,
            2,
        ),
    }

    limb = (
        base.load_frozen_limb_reference()
    )

    limb_radius = float(
        limb[
            "radius_px"
        ]
    )

    frozen_limb = (
        frozen[
            "provenance"
        ][
            "frozen_limb_reference"
        ]
    )

    for key in (
        "center_x_px",
        "center_y_px",
        "radius_px",
    ):
        if not math.isclose(
            float(
                limb[
                    key
                ]
            ),
            float(
                frozen_limb[
                    key
                ]
            ),
            rel_tol=0.0,
            abs_tol=1.0e-12,
        ):
            raise RuntimeError(
                "Frozen limb reference changed "
                f"for field {key}."
            )

    curves: dict[str, Any] = {}

    for curve_id in base.CURVE_IDS:
        frozen_curve = (
            frozen[
                "curves"
            ][
                curve_id
            ]
        )

        frozen_fits = (
            frozen_curve[
                "image_space_fits"
            ][
                "equal_pass_combined"
            ]
        )

        line = (
            analyze_line_at_spacing(
                passes[1][curve_id],
                passes[2][curve_id],
                base.PRIMARY_SPACING_PX,
                limb_radius,
            )
        )

        circle = frozen_fits[
            "circle"
        ]

        ellipse = frozen_fits[
            "ellipse"
        ]

        line_rms = float(
            line[
                "residuals"
            ][
                "absolute_px"
            ][
                "rms"
            ]
        )

        circle_rms = float(
            circle[
                "residuals"
            ][
                "absolute_px"
            ][
                "rms"
            ]
        )

        ellipse_rms = float(
            ellipse[
                "residuals"
            ][
                "absolute_px"
            ][
                "rms"
            ]
        )

        circle_radius = float(
            circle[
                "radius_px"
            ]
        )

        sensitivity: dict[
            str,
            Any,
        ] = {}

        for spacing in (
            1.0,
            4.0,
        ):
            line_sensitivity = (
                analyze_line_at_spacing(
                    passes[1][curve_id],
                    passes[2][curve_id],
                    spacing,
                    limb_radius,
                )
            )

            frozen_sensitivity = (
                frozen_curve[
                    "sampling_sensitivity"
                ][
                    format(
                        spacing,
                        ".1f",
                    )
                ]
            )

            sensitivity[
                format(
                    spacing,
                    ".1f",
                )
            ] = {
                "line_absolute_px": (
                    line_sensitivity[
                        "residuals"
                    ][
                        "absolute_px"
                    ]
                ),
                "circle_absolute_px": (
                    frozen_sensitivity[
                        "combined_circle_absolute_px"
                    ]
                ),
                "ellipse_absolute_px": (
                    frozen_sensitivity[
                        "combined_ellipse_absolute_px"
                    ]
                ),
            }

        curves[
            curve_id
        ] = {
            "analysis_partition": (
                frozen_curve[
                    "analysis_partition"
                ]
            ),
            "line": line,
            "circle": circle,
            "ellipse": ellipse,
            "descriptive_comparison": {
                "line_rms_px": (
                    line_rms
                ),
                "circle_rms_px": (
                    circle_rms
                ),
                "ellipse_rms_px": (
                    ellipse_rms
                ),
                "line_over_circle_rms": (
                    line_rms
                    / circle_rms
                ),
                "line_minus_circle_rms_px": (
                    line_rms
                    - circle_rms
                ),
                "circle_minus_ellipse_rms_px": (
                    circle_rms
                    - ellipse_rms
                ),
                "circle_radius_over_frozen_limb_radius": (
                    circle_radius
                    / limb_radius
                ),
                "circle_radius_px": (
                    circle_radius
                ),
                "frozen_limb_radius_px": (
                    limb_radius
                ),
                "ellipse_axis_ratio_minor_over_major": (
                    float(
                        ellipse[
                            "axis_ratio_minor_over_major"
                        ]
                    )
                ),
            },
            "sampling_sensitivity": (
                sensitivity
            ),
        }

    return {
        "checkpoint": (
            "first_hand_curve_"
            "morphology_census_v0.8"
        ),
        "analysis_class": (
            "post_hoc_model_neutral_"
            "morphology_census"
        ),
        "input_result": str(
            QC_RESULT.relative_to(
                ROOT
            )
        ),
        "frozen_limb_reference": (
            limb
        ),
        "method": {
            "line_fit": (
                "equal-pass arc-length-weighted "
                "orthogonal total least squares"
            ),
            "line_fit_applied_to_all_curves": True,
            "primary_resampling_spacing_px": (
                base.PRIMARY_SPACING_PX
            ),
            "sensitivity_resampling_spacings_px": [
                1.0,
                4.0,
            ],
            "circle_ellipse_results_recomputed": False,
            "circle_ellipse_results_source": (
                str(
                    QC_RESULT.relative_to(
                        ROOT
                    )
                )
            ),
            "formal_model_selection_performed": False,
        },
        "curves": curves,
        "scope": {
            "neutral_line_circle_ellipse_census_computed": True,
            "projective_map_fitted": False,
            "projective_gauge_selected": False,
            "spherical_scale_selected": False,
            "great_circle_certification_issued": False,
            "reciprocal_spiral_verdict_issued": False,
            "s1_computed": False,
            "s1_5_computed": False,
            "s2_computed": False,
        },
        "interpretation_boundary": (
            "Line, circle, and ellipse fits are "
            "descriptive image-space models of a "
            "hand-drawn source. Large fitted circle "
            "radius may represent the straight-line "
            "limit. No fitted family is interpreted "
            "here as proof of great-circle identity "
            "or a specific spherical projection."
        ),
    }


def render_report(
    analysis: dict[str, Any],
) -> str:
    lines = [
        "# First Hand neutral curve morphology census",
        "",
        "**Status:** post-hoc model-neutral descriptive supplement",
        "",
        "Circle and ellipse values are imported unchanged from the sealed "
        "acquisition-QC sensitivity result. This supplement adds an "
        "equal-pass weighted orthogonal-line fit to every curve.",
        "",
        "## Primary 2 px census",
        "",
        "| Curve | Partition | Line RMS px | Circle RMS px | Ellipse RMS px | "
        "Line/Circle | Circle R / limb R | Ellipse b/a | Line bearing deg |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|",
    ]

    for curve_id in base.CURVE_IDS:
        curve = (
            analysis[
                "curves"
            ][
                curve_id
            ]
        )

        comparison = (
            curve[
                "descriptive_comparison"
            ]
        )

        lines.append(
            f"| `{curve_id}` | "
            f"{curve['analysis_partition']} | "
            f"{comparison['line_rms_px']:.6f} | "
            f"{comparison['circle_rms_px']:.6f} | "
            f"{comparison['ellipse_rms_px']:.6f} | "
            f"{comparison['line_over_circle_rms']:.6f} | "
            f"{comparison['circle_radius_over_frozen_limb_radius']:.6f} | "
            f"{comparison['ellipse_axis_ratio_minor_over_major']:.6f} | "
            f"{curve['line']['unoriented_bearing_deg']:.6f} |"
        )

    lines += [
        "",
        "## 1 / 2 / 4 px resampling sensitivity",
        "",
    ]

    for curve_id in base.CURVE_IDS:
        curve = (
            analysis[
                "curves"
            ][
                curve_id
            ]
        )

        comparison = (
            curve[
                "descriptive_comparison"
            ]
        )

        lines += [
            f"### `{curve_id}`",
            "",
            "| Spacing px | Line RMS px | Circle RMS px | Ellipse RMS px |",
            "|---:|---:|---:|---:|",
            (
                f"| 2.0 | "
                f"{comparison['line_rms_px']:.6f} | "
                f"{comparison['circle_rms_px']:.6f} | "
                f"{comparison['ellipse_rms_px']:.6f} |"
            ),
        ]

        for spacing in (
            "1.0",
            "4.0",
        ):
            item = (
                curve[
                    "sampling_sensitivity"
                ][
                    spacing
                ]
            )

            lines.append(
                f"| {spacing} | "
                f"{item['line_absolute_px']['rms']:.6f} | "
                f"{item['circle_absolute_px']['rms']:.6f} | "
                f"{item['ellipse_absolute_px']['rms']:.6f} |"
            )

        lines.append("")

    lines += [
        "## Interpretation boundary",
        "",
        "A very large fitted circle radius is treated descriptively as the "
        "near-straight-line limit rather than as evidence for a physically "
        "meaningful enormous circle.",
        "",
        "Differences among line, circle, and ellipse residuals are not a "
        "formal model-selection test.",
        "",
        f"`{base.HOLDOUT_ID}` remains an independent scaffold holdout.",
        "",
        "No projective map, spherical scale, great-circle certification, "
        "reciprocal-spiral verdict, S1, S1.5, or S2 is produced.",
        "",
    ]

    return "\n".join(
        lines
    )


def write_outputs(
    analysis: dict[str, Any],
) -> None:
    OUTPUT_JSON.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    OUTPUT_JSON.write_text(
        json.dumps(
            analysis,
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )

    OUTPUT_REPORT.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    OUTPUT_REPORT.write_text(
        render_report(
            analysis
        ),
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Model-neutral First Hand "
            "line/circle/ellipse morphology census."
        )
    )

    parser.add_argument(
        "--check-inputs",
        action="store_true",
        help=(
            "Verify sealed QC result and curve inputs "
            "without computing morphology."
        ),
    )

    args = parser.parse_args()

    if args.check_inputs:
        base.verify_input_seal()
        qc_runner.verify_qc_derivative()
        load_frozen_qc_result()

        print(
            "Raw pass seal: VERIFIED"
        )
        print(
            "QC derivative: VERIFIED"
        )
        print(
            "QC sensitivity result: VERIFIED"
        )
        print(
            "No morphology was computed."
        )

        return 0

    analysis = build_analysis()

    write_outputs(
        analysis
    )

    print("=" * 96)
    print(
        "FIRST HAND NEUTRAL CURVE MORPHOLOGY CENSUS"
    )
    print("=" * 96)

    for curve_id in base.CURVE_IDS:
        item = (
            analysis[
                "curves"
            ][
                curve_id
            ][
                "descriptive_comparison"
            ]
        )

        print(
            f"{curve_id}: "
            f"line={item['line_rms_px']:.6f} px, "
            f"circle={item['circle_rms_px']:.6f} px, "
            f"ellipse={item['ellipse_rms_px']:.6f} px, "
            f"line/circle={item['line_over_circle_rms']:.3f}, "
            f"Rcircle/Rlimb="
            f"{item['circle_radius_over_frozen_limb_radius']:.6f}"
        )

    print(
        f"Wrote {OUTPUT_JSON}"
    )
    print(
        f"Wrote {OUTPUT_REPORT}"
    )

    print(
        "No projective map, great-circle verdict, "
        "or self-embedment score was computed."
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
