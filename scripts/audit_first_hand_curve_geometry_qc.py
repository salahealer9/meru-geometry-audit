#!/usr/bin/env python3
"""Post-hoc acquisition-QC sensitivity audit for First Hand curves.

This runner reuses the frozen neutral curve-geometry engine while
substituting only the sealed QC-derived pass-2 observation file.

It does not overwrite the primary raw-data result.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

root_text = str(ROOT)

if root_text not in sys.path:
    sys.path.insert(
        0,
        root_text,
    )

from scripts import audit_first_hand_curve_geometry as base

DATA_DIR = (
    ROOT
    / "data"
    / "derived"
    / "first_hand_arm_of_god"
)

QC_DIR = DATA_DIR / "qc"

RAW_PASS2 = (
    DATA_DIR
    / "great_circle_segments_pass2.csv"
)

QC_PASS2 = (
    QC_DIR
    / "great_circle_segments_pass2_qc.csv"
)

QC_MANIFEST = (
    QC_DIR
    / "great_circle_segments_pass2_qc_manifest.json"
)

QC_SEAL = (
    QC_DIR
    / "great_circle_segments_pass2_qc.sha256"
)

EXCLUSION_MANIFEST = (
    QC_DIR
    / "curve_acquisition_qc_exclusions.csv"
)

PRIMARY_RESULT = (
    DATA_DIR
    / "first_hand_curve_geometry_audit.json"
)

PRIMARY_RESULT_SEAL = (
    DATA_DIR
    / "first_hand_curve_geometry_results.sha256"
)

OUTPUT_JSON = (
    QC_DIR
    / "first_hand_curve_geometry_qc_sensitivity.json"
)

OUTPUT_REPORT = (
    ROOT
    / "reports"
    / "first_hand_curve_geometry_qc_sensitivity.md"
)

QC_TARGET_ID = "AOG-LM-P07-GC-X1"


def sha256_path(
    path: Path,
) -> str:
    digest = hashlib.sha256()

    with path.open("rb") as handle:
        for block in iter(
            lambda: handle.read(1 << 20),
            b"",
        ):
            digest.update(block)

    return digest.hexdigest()


def verify_sha256_manifest(
    manifest_path: Path,
    root: Path = ROOT,
) -> dict[str, str]:
    """Verify a standard sha256sum-style manifest."""
    if not manifest_path.exists():
        raise RuntimeError(
            f"Missing checksum manifest: {manifest_path}"
        )

    verified: dict[str, str] = {}

    for raw_line in manifest_path.read_text(
        encoding="utf-8",
    ).splitlines():
        line = raw_line.strip()

        if not line:
            continue

        parts = line.split(
            None,
            1,
        )

        if len(parts) != 2:
            raise RuntimeError(
                f"Malformed checksum line: {raw_line!r}"
            )

        expected = parts[0]
        relative = parts[1].lstrip("*")

        target = (
            root
            / relative
        )

        if not target.exists():
            raise RuntimeError(
                f"Checksum target missing: {target}"
            )

        actual = sha256_path(
            target
        )

        if actual != expected:
            raise RuntimeError(
                f"Checksum mismatch for {target}: "
                f"expected {expected}, got {actual}"
            )

        verified[
            relative
        ] = actual

    if not verified:
        raise RuntimeError(
            f"Checksum manifest is empty: {manifest_path}"
        )

    return verified


def verify_qc_derivative() -> dict[str, Any]:
    """Verify the frozen post-hoc QC derivative and its provenance."""
    verified = verify_sha256_manifest(
        QC_SEAL
    )

    if not QC_MANIFEST.exists():
        raise RuntimeError(
            f"Missing QC manifest: {QC_MANIFEST}"
        )

    manifest = json.loads(
        QC_MANIFEST.read_text(
            encoding="utf-8",
        )
    )

    if (
        manifest.get("status")
        != "post_hoc_acquisition_qc_derivative"
    ):
        raise RuntimeError(
            "Unexpected QC derivative status."
        )

    if (
        manifest.get("raw_file")
        != str(
            RAW_PASS2.relative_to(
                ROOT
            )
        )
    ):
        raise RuntimeError(
            "QC manifest does not identify "
            "the expected raw pass-2 file."
        )

    if (
        manifest.get("qc_file")
        != str(
            QC_PASS2.relative_to(
                ROOT
            )
        )
    ):
        raise RuntimeError(
            "QC manifest does not identify "
            "the expected QC pass-2 file."
        )

    if (
        manifest.get("raw_file_sha256")
        != sha256_path(
            RAW_PASS2
        )
    ):
        raise RuntimeError(
            "QC manifest raw-file hash mismatch."
        )

    if (
        manifest.get("qc_file_sha256")
        != sha256_path(
            QC_PASS2
        )
    ):
        raise RuntimeError(
            "QC manifest derived-file hash mismatch."
        )

    if (
        manifest.get(
            "exclusion_manifest_sha256"
        )
        != sha256_path(
            EXCLUSION_MANIFEST
        )
    ):
        raise RuntimeError(
            "QC exclusion-manifest hash mismatch."
        )

    if (
        manifest.get("raw_row_count")
        != 666
        or manifest.get("qc_row_count")
        != 588
        or manifest.get("excluded_row_count")
        != 78
    ):
        raise RuntimeError(
            "Unexpected QC row-count provenance."
        )

    if (
        manifest.get(
            "sequence_indices_renumbered"
        )
        is not False
    ):
        raise RuntimeError(
            "QC sequence indices were unexpectedly renumbered."
        )

    if (
        manifest.get(
            "raw_file_modified"
        )
        is not False
    ):
        raise RuntimeError(
            "QC manifest does not preserve raw immutability."
        )

    validation = manifest.get(
        "validation",
        [],
    )

    if len(validation) != 1:
        raise RuntimeError(
            "Expected exactly one QC exclusion."
        )

    item = validation[0]

    expected = {
        "pass_number": 2,
        "landmark_id": QC_TARGET_ID,
        "segment_id": "S01",
        "sequence_index_start": 0,
        "sequence_index_end": 77,
        "excluded_row_count": 78,
        "exclusion_code": (
            "exact_duplicate_input_event_burst"
        ),
    }

    for key, value in expected.items():
        if item.get(key) != value:
            raise RuntimeError(
                f"Unexpected QC validation field "
                f"{key}: {item.get(key)!r}"
            )

    return {
        "checksum_files": verified,
        "manifest": manifest,
    }


def load_primary_result() -> dict[str, Any]:
    """Load the already-sealed primary raw-data result."""
    verify_sha256_manifest(
        PRIMARY_RESULT_SEAL
    )

    if not PRIMARY_RESULT.exists():
        raise RuntimeError(
            "Primary curve result is missing."
        )

    result = json.loads(
        PRIMARY_RESULT.read_text(
            encoding="utf-8",
        )
    )

    if (
        result.get("checkpoint")
        != "first_hand_curve_geometry_v0.8"
    ):
        raise RuntimeError(
            "Unexpected primary-result checkpoint."
        )

    return result


def build_analysis() -> dict[str, Any]:
    """Run the frozen geometry engine with QC-derived pass 2."""
    raw_verified = (
        base.verify_input_seal()
    )

    qc_verified = (
        verify_qc_derivative()
    )

    primary_result = (
        load_primary_result()
    )

    passes = {
        1: base.read_curve_pass(
            base.PASS_PATHS[1],
            1,
        ),
        2: base.read_curve_pass(
            QC_PASS2,
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

    curves: dict[str, Any] = {}

    for curve_id in base.CURVE_IDS:
        primary = (
            base.analyze_curve_at_spacing(
                curve_id,
                passes[1][curve_id],
                passes[2][curve_id],
                base.PRIMARY_SPACING_PX,
                limb_radius,
            )
        )

        primary[
            "analysis_partition"
        ] = (
            "calibration_labelled_curve"
            if curve_id
            in base.CALIBRATION_IDS
            else "independent_scaffold_holdout"
        )

        primary[
            "sampling_sensitivity"
        ] = {}

        for spacing in (
            base.SENSITIVITY_SPACINGS_PX
        ):
            result = (
                base.analyze_curve_at_spacing(
                    curve_id,
                    passes[1][curve_id],
                    passes[2][curve_id],
                    spacing,
                    limb_radius,
                )
            )

            primary[
                "sampling_sensitivity"
            ][
                format(
                    spacing,
                    ".1f",
                )
            ] = {
                "resampling_spacing_px": (
                    spacing
                ),
                "pass_agreement_symmetric_px": (
                    result[
                        "pass_agreement"
                    ][
                        "symmetric_px"
                    ]
                ),
                "combined_circle_absolute_px": (
                    result[
                        "image_space_fits"
                    ][
                        "equal_pass_combined"
                    ][
                        "circle"
                    ][
                        "residuals"
                    ][
                        "absolute_px"
                    ]
                ),
                "combined_ellipse_absolute_px": (
                    result[
                        "image_space_fits"
                    ][
                        "equal_pass_combined"
                    ][
                        "ellipse"
                    ][
                        "residuals"
                    ][
                        "absolute_px"
                    ]
                ),
            }

        curves[
            curve_id
        ] = primary

    comparison: dict[str, Any] = {}

    for curve_id in base.CURVE_IDS:
        raw_stats = (
            primary_result[
                "curves"
            ][
                curve_id
            ][
                "pass_agreement"
            ][
                "symmetric_px"
            ]
        )

        qc_stats = (
            curves[
                curve_id
            ][
                "pass_agreement"
            ][
                "symmetric_px"
            ]
        )

        comparison[
            curve_id
        ] = {
            "primary_raw": raw_stats,
            "qc_sensitivity": qc_stats,
            "delta_qc_minus_raw": {
                key: (
                    float(
                        qc_stats[
                            key
                        ]
                    )
                    - float(
                        raw_stats[
                            key
                        ]
                    )
                )
                for key in (
                    "median",
                    "rms",
                    "p95",
                    "maximum",
                )
            },
        }

        # Only X1 was altered by the QC derivative.
        # Every other curve must remain numerically unchanged.
        if (
            curve_id != QC_TARGET_ID
        ):
            for key in (
                "median",
                "rms",
                "p95",
                "maximum",
            ):
                if not math.isclose(
                    float(
                        qc_stats[
                            key
                        ]
                    ),
                    float(
                        raw_stats[
                            key
                        ]
                    ),
                    rel_tol=0.0,
                    abs_tol=1.0e-12,
                ):
                    raise RuntimeError(
                        "QC derivative unexpectedly "
                        f"changed {curve_id} {key}."
                    )

    review_ids = [
        curve_id
        for curve_id, curve
        in curves.items()
        if curve[
            "pass_agreement"
        ][
            "manual_review_required"
        ]
    ]

    return {
        "checkpoint": (
            "first_hand_curve_geometry_"
            "qc_sensitivity_v0.8"
        ),
        "analysis_class": (
            "post_hoc_acquisition_qc_sensitivity"
        ),
        "primary_result_preserved": True,
        "provenance": {
            "raw_input_sha256_manifest": str(
                base.SEAL_PATH.relative_to(
                    ROOT
                )
            ),
            "verified_raw_curve_inputs": (
                raw_verified
            ),
            "primary_result_sha256_manifest": str(
                PRIMARY_RESULT_SEAL.relative_to(
                    ROOT
                )
            ),
            "qc_derivative_sha256_manifest": str(
                QC_SEAL.relative_to(
                    ROOT
                )
            ),
            "qc_derivative_verification": (
                qc_verified
            ),
            "pass1_input": str(
                base.PASS_PATHS[
                    1
                ].relative_to(
                    ROOT
                )
            ),
            "pass2_input": str(
                QC_PASS2.relative_to(
                    ROOT
                )
            ),
            "frozen_limb_reference": limb,
        },
        "method": {
            "geometry_engine": (
                "scripts/"
                "audit_first_hand_curve_geometry.py"
            ),
            "primary_resampling_spacing_px": (
                base.PRIMARY_SPACING_PX
            ),
            "sensitivity_resampling_spacings_px": (
                list(
                    base.SENSITIVITY_SPACINGS_PX
                )
            ),
            "pass_weights": {
                "pass1": 0.5,
                "pass2": 0.5,
            },
            "within_pass_weighting": (
                "visible polyline arc length"
            ),
            "segment_correspondence_forced": False,
            "manual_review_median_threshold_px": (
                base.MANUAL_REVIEW_MEDIAN_PX
            ),
            "qc_exclusion_selected_from_model_residual": (
                False
            ),
        },
        "partitions": {
            "calibration_labelled_curves": (
                list(
                    base.CALIBRATION_IDS
                )
            ),
            "independent_scaffold_holdout": (
                base.HOLDOUT_ID
            ),
        },
        "curves": curves,
        "primary_vs_qc": comparison,
        "manual_review": {
            "triggered_curve_ids": (
                review_ids
            ),
            "any_triggered": bool(
                review_ids
            ),
        },
        "scope": {
            "post_hoc_qc_sensitivity_computed": True,
            "raw_primary_result_replaced": False,
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
            "This is a post-hoc acquisition-QC "
            "sensitivity analysis. The sealed primary "
            "raw-data result remains authoritative as "
            "the first execution record. The QC "
            "derivative removes only an independently "
            "documented exact duplicate input-event "
            "burst and does not constitute a new "
            "confirmatory analysis."
        ),
    }


def render_report(
    analysis: dict[str, Any],
) -> str:
    lines = [
        "# First Hand curve geometry — acquisition-QC sensitivity",
        "",
        "**Status:** post-hoc acquisition-QC sensitivity",
        "",
        "The sealed primary raw-data result is preserved unchanged.",
        "",
        "The only observation change is the documented exclusion of "
        "pass-2 X1 S01 sequence indices 0–77, representing 78 exact "
        "duplicate same-timestamp acquisition events.",
        "",
        "## Primary versus QC pass agreement",
        "",
        "| Curve | Raw median | Raw RMS | Raw P95 | QC median | QC RMS | QC P95 |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]

    for curve_id in base.CURVE_IDS:
        item = (
            analysis[
                "primary_vs_qc"
            ][
                curve_id
            ]
        )

        raw = item[
            "primary_raw"
        ]

        qc = item[
            "qc_sensitivity"
        ]

        lines.append(
            f"| `{curve_id}` | "
            f"{raw['median']:.6f} | "
            f"{raw['rms']:.6f} | "
            f"{raw['p95']:.6f} | "
            f"{qc['median']:.6f} | "
            f"{qc['rms']:.6f} | "
            f"{qc['p95']:.6f} |"
        )

    lines += [
        "",
        "## QC-derived descriptive fits",
        "",
        "| Curve | Circle RMS px | Ellipse RMS px | Ellipse b/a |",
        "|---|---:|---:|---:|",
    ]

    for curve_id in base.CURVE_IDS:
        fits = (
            analysis[
                "curves"
            ][
                curve_id
            ][
                "image_space_fits"
            ][
                "equal_pass_combined"
            ]
        )

        lines.append(
            f"| `{curve_id}` | "
            f"{fits['circle']['residuals']['absolute_px']['rms']:.6f} | "
            f"{fits['ellipse']['residuals']['absolute_px']['rms']:.6f} | "
            f"{fits['ellipse']['axis_ratio_minor_over_major']:.9f} |"
        )

    lines += [
        "",
        "## Interpretation boundary",
        "",
        "This sensitivity result does not replace the primary raw-data result.",
        "",
        f"`{base.HOLDOUT_ID}` remains an independent holdout.",
        "",
        "No projective map, projective gauge, spherical scale, "
        "great-circle certification, reciprocal-spiral verdict, "
        "S1, S1.5, or S2 is produced.",
        "",
        "The source is hand-drawn; image-space residuals do not "
        "certify exact mathematical incidence.",
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
            "Post-hoc First Hand acquisition-QC "
            "curve-geometry sensitivity audit."
        )
    )

    parser.add_argument(
        "--check-inputs",
        action="store_true",
        help=(
            "Verify raw and QC provenance and parse "
            "the two analysis passes without computing "
            "curve geometry."
        ),
    )

    args = parser.parse_args()

    if args.check_inputs:
        base.verify_input_seal()
        qc = verify_qc_derivative()
        load_primary_result()

        pass1 = base.read_curve_pass(
            base.PASS_PATHS[1],
            1,
        )

        pass2 = base.read_curve_pass(
            QC_PASS2,
            2,
        )

        print(
            "Primary raw result: VERIFIED"
        )
        print(
            "QC derivative: VERIFIED"
        )
        print(
            "QC exclusions:",
            len(
                qc[
                    "manifest"
                ][
                    "validation"
                ]
            ),
        )
        print(
            "Pass 1:",
            sum(
                len(value)
                for value
                in pass1.values()
            ),
            "segments,",
            len(pass1),
            "curves",
        )
        print(
            "QC pass 2:",
            sum(
                len(value)
                for value
                in pass2.values()
            ),
            "segments,",
            len(pass2),
            "curves",
        )
        print(
            "No curve geometry was computed."
        )

        return 0

    analysis = build_analysis()

    write_outputs(
        analysis
    )

    print("=" * 78)
    print(
        "FIRST HAND ACQUISITION-QC "
        "CURVE GEOMETRY SENSITIVITY"
    )
    print("=" * 78)

    for curve_id in base.CURVE_IDS:
        stats = (
            analysis[
                "curves"
            ][
                curve_id
            ][
                "pass_agreement"
            ][
                "symmetric_px"
            ]
        )

        print(
            f"{curve_id}: "
            f"median={stats['median']:.6f} px, "
            f"RMS={stats['rms']:.6f} px, "
            f"P95={stats['p95']:.6f} px"
        )

    print(
        "Manual review triggered:",
        analysis[
            "manual_review"
        ][
            "any_triggered"
        ],
    )

    print(
        f"Wrote {OUTPUT_JSON}"
    )
    print(
        f"Wrote {OUTPUT_REPORT}"
    )

    print(
        "Primary raw result was not overwritten."
    )

    print(
        "No projective map, scale, "
        "great-circle verdict, or "
        "self-embedment score was computed."
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
