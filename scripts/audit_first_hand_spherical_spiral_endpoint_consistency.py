#!/usr/bin/env python3
"""Independent endpoint-consistency audit for the First Hand spherical spiral.

The selected spiral endpoint samples are fixed entirely by the previously
frozen source-topological ledger:

    inner = first ordered sample of S01
    outer = final ordered sample of S10

The selected samples are compared against independently acquired neutral
landmark consensus coordinates.

No endpoint is snapped, fitted, extrapolated, or used to alter the spiral
trace.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import sys
from pathlib import Path
from typing import Any, Sequence

import numpy as np


ROOT = Path(__file__).resolve().parents[1]

if str(ROOT) not in sys.path:
    sys.path.insert(
        0,
        str(ROOT),
    )

from scripts import digitize_first_hand_spherical_spiral as digitizer  # noqa: E402


PASS1 = (
    ROOT
    / "data"
    / "derived"
    / "first_hand_arm_of_god"
    / "spherical_spiral_segments_pass1.csv"
)

PASS2 = (
    ROOT
    / "data"
    / "derived"
    / "first_hand_arm_of_god"
    / "spherical_spiral_segments_pass2.csv"
)

SEAL1 = PASS1.with_suffix(".sha256")
SEAL2 = PASS2.with_suffix(".sha256")

CONSENSUS = (
    ROOT
    / "data"
    / "derived"
    / "first_hand_arm_of_god"
    / "expanded_neutral_landmark_consensus.csv"
)

TOPOLOGY = (
    ROOT
    / "reports"
    / "first_hand_spherical_spiral_endpoint_topology.md"
)

REPRO_RESULT = (
    ROOT
    / "data"
    / "derived"
    / "first_hand_arm_of_god"
    / "qc"
    / "first_hand_spherical_spiral_reproducibility.json"
)

REPRO_SEAL = (
    ROOT
    / "data"
    / "derived"
    / "first_hand_arm_of_god"
    / "qc"
    / "first_hand_spherical_spiral_reproducibility.sha256"
)

OUTPUT_DIR = (
    ROOT
    / "data"
    / "derived"
    / "first_hand_arm_of_god"
    / "qc"
)

OUT_JSON = (
    OUTPUT_DIR
    / "first_hand_spherical_spiral_endpoint_consistency.json"
)

OUT_REPORT = (
    ROOT
    / "reports"
    / "first_hand_spherical_spiral_endpoint_consistency.md"
)

ANALYSIS_CLASS = (
    "independent_prior_landmark_spherical_spiral_endpoint_consistency"
)

INNER_ID = (
    "AOG-LM-P07-SPHERE-INNER-END"
)

OUTER_ID = (
    "AOG-LM-P07-RIM-NODE-LR-SHARED"
)

LIMB_RADIUS_PX = 341.906449919

EXPECTED_CONSENSUS_FIELDS = [
    "landmark_id",
    "source_feature",
    "fit_partition",
    "pass1_x_px",
    "pass1_y_px",
    "pass2_x_px",
    "pass2_y_px",
    "consensus_x_px",
    "consensus_y_px",
    "pass_separation_px",
    "pass1_stroke_width_px",
    "pass2_stroke_width_px",
    "uncertainty_floor_px",
    "consensus_uncertainty_px",
    "crop_file_sha256",
    "crop_pixel_sha256",
]


def sha256_path(
    path: Path,
) -> str:
    digest = hashlib.sha256()

    with path.open(
        "rb"
    ) as handle:
        for block in iter(
            lambda: handle.read(
                1024 * 1024
            ),
            b"",
        ):
            digest.update(
                block
            )

    return digest.hexdigest()


def resolve_manifest_path(
    recorded_name: str,
) -> Path:
    recorded = Path(
        recorded_name.lstrip("*").strip()
    )

    if not recorded.is_absolute():
        recorded = ROOT / recorded

    return recorded.resolve()


def verify_single_target_manifest(
    manifest: Path,
    target: Path,
) -> None:
    if not manifest.exists():
        raise RuntimeError(
            f"Missing SHA-256 seal: {manifest}"
        )

    lines = [
        line.strip()
        for line in manifest.read_text(
            encoding="utf-8"
        ).splitlines()
        if line.strip()
    ]

    if len(lines) != 1:
        raise RuntimeError(
            f"{manifest} must contain exactly one record."
        )

    fields = lines[0].split(
        maxsplit=1
    )

    if len(fields) != 2:
        raise RuntimeError(
            f"Malformed SHA-256 record in {manifest}."
        )

    expected_hash = fields[0]

    recorded_path = resolve_manifest_path(
        fields[1]
    )

    if (
        recorded_path
        != target.resolve()
    ):
        raise RuntimeError(
            f"{manifest} does not seal {target}."
        )

    actual_hash = sha256_path(
        target
    )

    if (
        actual_hash
        != expected_hash
    ):
        raise RuntimeError(
            f"SHA-256 verification failed for {target}."
        )


def verify_target_in_manifest(
    manifest: Path,
    target: Path,
) -> None:
    if not manifest.exists():
        raise RuntimeError(
            f"Missing SHA-256 manifest: {manifest}"
        )

    target_resolved = (
        target.resolve()
    )

    matches = []

    for line in manifest.read_text(
        encoding="utf-8"
    ).splitlines():
        line = line.strip()

        if not line:
            continue

        fields = line.split(
            maxsplit=1
        )

        if len(fields) != 2:
            raise RuntimeError(
                f"Malformed SHA-256 record in {manifest}: {line!r}"
            )

        expected_hash = fields[0]

        recorded_path = (
            resolve_manifest_path(
                fields[1]
            )
        )

        if (
            recorded_path
            == target_resolved
        ):
            matches.append(
                expected_hash
            )

    if len(matches) != 1:
        raise RuntimeError(
            f"Expected exactly one seal record for {target}; "
            f"found {len(matches)}."
        )

    if (
        sha256_path(
            target
        )
        != matches[0]
    ):
        raise RuntimeError(
            f"Frozen reproducibility result failed SHA-256 verification: "
            f"{target}"
        )


def read_consensus() -> dict[
    str,
    dict[
        str,
        str,
    ],
]:
    with CONSENSUS.open(
        newline="",
        encoding="utf-8",
    ) as handle:
        reader = csv.DictReader(
            handle
        )

        if (
            reader.fieldnames
            != EXPECTED_CONSENSUS_FIELDS
        ):
            raise RuntimeError(
                "Neutral-landmark consensus schema differs "
                "from the frozen expected schema."
            )

        rows = list(
            reader
        )

    result = {}

    for landmark_id in (
        INNER_ID,
        OUTER_ID,
    ):
        matches = [
            row
            for row in rows
            if (
                row[
                    "landmark_id"
                ]
                == landmark_id
            )
        ]

        if len(matches) != 1:
            raise RuntimeError(
                f"Expected one consensus row for {landmark_id}; "
                f"found {len(matches)}."
            )

        result[
            landmark_id
        ] = matches[0]

    if (
        result[
            INNER_ID
        ][
            "fit_partition"
        ]
        != "holdout"
    ):
        raise RuntimeError(
            "Inner endpoint must retain fit_partition=holdout."
        )

    if (
        result[
            OUTER_ID
        ][
            "fit_partition"
        ]
        != "calibration"
    ):
        raise RuntimeError(
            "Outer shared rim node must retain fit_partition=calibration."
        )

    return result


def group_rows(
    rows: Sequence[
        dict[
            str,
            str,
        ]
    ],
) -> dict[
    str,
    list[
        dict[
            str,
            str,
        ]
    ],
]:
    grouped: dict[
        str,
        list[
            dict[
                str,
                str,
            ]
        ],
    ] = {}

    for row in rows:
        grouped.setdefault(
            row[
                "segment_id"
            ],
            [],
        ).append(
            row
        )

    for segment_rows in (
        grouped.values()
    ):
        segment_rows.sort(
            key=lambda row: int(
                row[
                    "sequence_index"
                ]
            )
        )

    return grouped


def selected_endpoint_rows(
    rows: Sequence[
        dict[
            str,
            str,
        ]
    ],
) -> dict[
    str,
    dict[
        str,
        str,
    ],
]:
    grouped = group_rows(
        rows
    )

    if (
        "S01"
        not in grouped
        or "S10"
        not in grouped
    ):
        raise RuntimeError(
            "Frozen endpoint topology requires S01 and S10."
        )

    inner = grouped[
        "S01"
    ][
        0
    ]

    outer = grouped[
        "S10"
    ][
        -1
    ]

    if int(
        inner[
            "sequence_index"
        ]
    ) != 0:
        raise RuntimeError(
            "Inner endpoint must be sequence_index=0 of S01."
        )

    return {
        "inner": inner,
        "outer": outer,
    }


def point_from_spiral_row(
    row: dict[
        str,
        str,
    ],
) -> np.ndarray:
    return np.array(
        [
            float(
                row[
                    "x_px"
                ]
            ),
            float(
                row[
                    "y_px"
                ]
            ),
        ],
        dtype=float,
    )


def point_from_consensus_row(
    row: dict[
        str,
        str,
    ],
) -> np.ndarray:
    return np.array(
        [
            float(
                row[
                    "consensus_x_px"
                ]
            ),
            float(
                row[
                    "consensus_y_px"
                ]
            ),
        ],
        dtype=float,
    )


def euclidean_distance(
    a: np.ndarray,
    b: np.ndarray,
) -> float:
    return float(
        np.linalg.norm(
            np.asarray(
                a,
                dtype=float,
            )
            - np.asarray(
                b,
                dtype=float,
            )
        )
    )


def mean_point(
    a: np.ndarray,
    b: np.ndarray,
) -> np.ndarray:
    return 0.5 * (
        np.asarray(
            a,
            dtype=float,
        )
        + np.asarray(
            b,
            dtype=float,
        )
    )


def spiral_source_scale(
    row: dict[
        str,
        str,
    ],
) -> float:
    return max(
        2.0,
        0.5
        * float(
            row[
                "local_stroke_width_px"
            ]
        ),
    )


def verify_topology_ledger() -> None:
    text = TOPOLOGY.read_text(
        encoding="utf-8"
    )

    required = (
        "first ordered sample of S01",
        "sequence_index = 0",
        "final ordered sample of S10",
        INNER_ID,
        OUTER_ID,
        "## No snapping",
    )

    for token in required:
        if token not in text:
            raise RuntimeError(
                "Frozen endpoint topology ledger missing token: "
                f"{token!r}"
            )


def verify_dependencies() -> tuple[
    list[
        dict[
            str,
            str,
        ]
    ],
    list[
        dict[
            str,
            str,
        ]
    ],
    dict[
        str,
        dict[
            str,
            str,
        ]
    ],
]:
    for path in (
        PASS1,
        PASS2,
        SEAL1,
        SEAL2,
        CONSENSUS,
        TOPOLOGY,
        REPRO_RESULT,
        REPRO_SEAL,
    ):
        if not path.exists():
            raise RuntimeError(
                f"Missing frozen dependency: {path}"
            )

    verify_single_target_manifest(
        SEAL1,
        PASS1,
    )

    verify_single_target_manifest(
        SEAL2,
        PASS2,
    )

    verify_target_in_manifest(
        REPRO_SEAL,
        REPRO_RESULT,
    )

    verify_topology_ledger()

    rows1 = (
        digitizer.validate_output_file(
            PASS1,
            expected_pass=1,
        )
    )

    rows2 = (
        digitizer.validate_output_file(
            PASS2,
            expected_pass=2,
        )
    )

    consensus = (
        read_consensus()
    )

    raw_crop_file_hashes = {
        row[
            "crop_file_sha256"
        ]
        for row in (
            list(
                rows1
            )
            + list(
                rows2
            )
        )
    }

    raw_crop_pixel_hashes = {
        row[
            "crop_pixel_sha256"
        ]
        for row in (
            list(
                rows1
            )
            + list(
                rows2
            )
        )
    }

    if len(
        raw_crop_file_hashes
    ) != 1:
        raise RuntimeError(
            "Raw spiral passes do not share one crop-file hash."
        )

    if len(
        raw_crop_pixel_hashes
    ) != 1:
        raise RuntimeError(
            "Raw spiral passes do not share one crop-pixel hash."
        )

    expected_file_hash = next(
        iter(
            raw_crop_file_hashes
        )
    )

    expected_pixel_hash = next(
        iter(
            raw_crop_pixel_hashes
        )
    )

    for landmark_id, row in (
        consensus.items()
    ):
        if (
            row[
                "crop_file_sha256"
            ]
            != expected_file_hash
        ):
            raise RuntimeError(
                f"{landmark_id} uses a different crop-file hash."
            )

        if (
            row[
                "crop_pixel_sha256"
            ]
            != expected_pixel_hash
        ):
            raise RuntimeError(
                f"{landmark_id} uses a different crop-pixel hash."
            )

    return (
        rows1,
        rows2,
        consensus,
    )


def endpoint_result(
    *,
    endpoint_name: str,
    landmark_id: str,
    pass1_row: dict[
        str,
        str,
    ],
    pass2_row: dict[
        str,
        str,
    ],
    landmark_row: dict[
        str,
        str,
    ],
) -> dict[
    str,
    Any,
]:
    p1 = point_from_spiral_row(
        pass1_row
    )

    p2 = point_from_spiral_row(
        pass2_row
    )

    mean = mean_point(
        p1,
        p2,
    )

    reference = (
        point_from_consensus_row(
            landmark_row
        )
    )

    d1 = euclidean_distance(
        p1,
        reference,
    )

    d2 = euclidean_distance(
        p2,
        reference,
    )

    dmean = euclidean_distance(
        mean,
        reference,
    )

    pass_separation = (
        euclidean_distance(
            p1,
            p2,
        )
    )

    return {
        "endpoint": endpoint_name,
        "prior_landmark_id": landmark_id,
        "prior_landmark_fit_partition": landmark_row[
            "fit_partition"
        ],
        "selection_rule": (
            "S01 first ordered sample"
            if endpoint_name == "inner"
            else "S10 final ordered sample"
        ),
        "pass1": {
            "segment_id": pass1_row[
                "segment_id"
            ],
            "sequence_index": int(
                pass1_row[
                    "sequence_index"
                ]
            ),
            "x_px": float(
                p1[
                    0
                ]
            ),
            "y_px": float(
                p1[
                    1
                ]
            ),
            "local_stroke_width_px": float(
                pass1_row[
                    "local_stroke_width_px"
                ]
            ),
            "spiral_source_scale_px": spiral_source_scale(
                pass1_row
            ),
            "distance_to_prior_landmark_px": d1,
            "distance_to_prior_landmark_over_limb_radius": (
                d1
                / LIMB_RADIUS_PX
            ),
        },
        "pass2": {
            "segment_id": pass2_row[
                "segment_id"
            ],
            "sequence_index": int(
                pass2_row[
                    "sequence_index"
                ]
            ),
            "x_px": float(
                p2[
                    0
                ]
            ),
            "y_px": float(
                p2[
                    1
                ]
            ),
            "local_stroke_width_px": float(
                pass2_row[
                    "local_stroke_width_px"
                ]
            ),
            "spiral_source_scale_px": spiral_source_scale(
                pass2_row
            ),
            "distance_to_prior_landmark_px": d2,
            "distance_to_prior_landmark_over_limb_radius": (
                d2
                / LIMB_RADIUS_PX
            ),
        },
        "two_pass_spiral_endpoint": {
            "mean_x_px": float(
                mean[
                    0
                ]
            ),
            "mean_y_px": float(
                mean[
                    1
                ]
            ),
            "pass_separation_px": pass_separation,
            "mean_distance_to_prior_landmark_px": dmean,
            "mean_distance_to_prior_landmark_over_limb_radius": (
                dmean
                / LIMB_RADIUS_PX
            ),
        },
        "prior_landmark": {
            "consensus_x_px": float(
                reference[
                    0
                ]
            ),
            "consensus_y_px": float(
                reference[
                    1
                ]
            ),
            "prior_pass_separation_px": float(
                landmark_row[
                    "pass_separation_px"
                ]
            ),
            "uncertainty_floor_px": float(
                landmark_row[
                    "uncertainty_floor_px"
                ]
            ),
            "consensus_uncertainty_px": float(
                landmark_row[
                    "consensus_uncertainty_px"
                ]
            ),
        },
    }


def build_analysis() -> dict[
    str,
    Any,
]:
    rows1, rows2, consensus = (
        verify_dependencies()
    )

    selected1 = (
        selected_endpoint_rows(
            rows1
        )
    )

    selected2 = (
        selected_endpoint_rows(
            rows2
        )
    )

    inner = endpoint_result(
        endpoint_name="inner",
        landmark_id=INNER_ID,
        pass1_row=selected1[
            "inner"
        ],
        pass2_row=selected2[
            "inner"
        ],
        landmark_row=consensus[
            INNER_ID
        ],
    )

    outer = endpoint_result(
        endpoint_name="outer",
        landmark_id=OUTER_ID,
        pass1_row=selected1[
            "outer"
        ],
        pass2_row=selected2[
            "outer"
        ],
        landmark_row=consensus[
            OUTER_ID
        ],
    )

    return {
        "analysis_class": ANALYSIS_CLASS,
        "status": (
            "post_reproducibility_independent_endpoint_consistency"
        ),
        "provenance": {
            "pass1": {
                "path": str(
                    PASS1.relative_to(
                        ROOT
                    )
                ),
                "sha256": sha256_path(
                    PASS1
                ),
            },
            "pass2": {
                "path": str(
                    PASS2.relative_to(
                        ROOT
                    )
                ),
                "sha256": sha256_path(
                    PASS2
                ),
            },
            "neutral_landmark_consensus": {
                "path": str(
                    CONSENSUS.relative_to(
                        ROOT
                    )
                ),
                "sha256": sha256_path(
                    CONSENSUS
                ),
            },
            "endpoint_topology": {
                "path": str(
                    TOPOLOGY.relative_to(
                        ROOT
                    )
                ),
                "sha256": sha256_path(
                    TOPOLOGY
                ),
            },
            "reproducibility_result": {
                "path": str(
                    REPRO_RESULT.relative_to(
                        ROOT
                    )
                ),
                "sha256": sha256_path(
                    REPRO_RESULT
                ),
                "seal_verified": True,
            },
        },
        "method": {
            "limb_radius_px": LIMB_RADIUS_PX,
            "inner_selection": (
                "first ordered sample of S01"
            ),
            "outer_selection": (
                "final ordered sample of S10"
            ),
            "snapping": False,
            "curve_fitting": False,
            "endpoint_extrapolation": False,
            "registration": False,
            "theoretical_spiral_used": False,
            "coordinate_model_used": False,
        },
        "inner": inner,
        "outer": outer,
        "interpretation_boundary": {
            "tests_independent_source_endpoint_consistency": True,
            "establishes_reciprocal_spiral_equation": False,
            "establishes_spherical_map": False,
            "alters_raw_spiral_endpoint": False,
        },
    }


def render_endpoint_section(
    result: dict[
        str,
        Any,
    ],
) -> list[
    str
]:
    p1 = result[
        "pass1"
    ]

    p2 = result[
        "pass2"
    ]

    mean = result[
        "two_pass_spiral_endpoint"
    ]

    landmark = result[
        "prior_landmark"
    ]

    return [
        f"## {result['endpoint'].capitalize()} endpoint",
        "",
        f"Prior landmark: `{result['prior_landmark_id']}`",
        "",
        f"Prior landmark fit partition: `{result['prior_landmark_fit_partition']}`",
        "",
        f"Selection rule: {result['selection_rule']}",
        "",
        "Pass 1 selected spiral sample:",
        "",
        f"    ({p1['x_px']:.12f}, {p1['y_px']:.12f}) px",
        f"    distance to prior landmark = {p1['distance_to_prior_landmark_px']:.12f} px",
        "",
        "Pass 2 selected spiral sample:",
        "",
        f"    ({p2['x_px']:.12f}, {p2['y_px']:.12f}) px",
        f"    distance to prior landmark = {p2['distance_to_prior_landmark_px']:.12f} px",
        "",
        "Two-pass mean spiral endpoint:",
        "",
        f"    ({mean['mean_x_px']:.12f}, {mean['mean_y_px']:.12f}) px",
        f"    spiral endpoint pass separation = {mean['pass_separation_px']:.12f} px",
        f"    mean-endpoint distance to prior landmark = {mean['mean_distance_to_prior_landmark_px']:.12f} px",
        "",
        "Independent prior landmark consensus:",
        "",
        f"    ({landmark['consensus_x_px']:.12f}, {landmark['consensus_y_px']:.12f}) px",
        f"    prior landmark pass separation = {landmark['prior_pass_separation_px']:.12f} px",
        f"    consensus uncertainty = {landmark['consensus_uncertainty_px']:.12f} px",
        "",
        "Continuous-spiral descriptive source scale:",
        "",
        f"    Pass 1 = {p1['spiral_source_scale_px']:.12f} px",
        f"    Pass 2 = {p2['spiral_source_scale_px']:.12f} px",
        "",
        "No combined statistical threshold is assigned to these descriptive scales.",
        "",
    ]


def render_report(
    analysis: dict[
        str,
        Any,
    ],
) -> str:
    lines = [
        "# First Hand spherical spiral endpoint consistency",
        "",
        "**Checkpoint:** v0.8",
        "",
        f"**Analysis class:** `{analysis['analysis_class']}`",
        "",
        "## Scope",
        "",
        "The endpoint samples were selected from the already-frozen source",
        "topology before comparison with the independently acquired neutral",
        "landmark consensus coordinates.",
        "",
        "No endpoint was snapped, extrapolated, registered, or fitted.",
        "",
    ]

    lines.extend(
        render_endpoint_section(
            analysis[
                "inner"
            ]
        )
    )

    lines.extend(
        render_endpoint_section(
            analysis[
                "outer"
            ]
        )
    )

    lines.extend(
        [
            "## Interpretation boundary",
            "",
            "This checkpoint tests consistency between two independently",
            "acquired representations of the printed endpoint features:",
            "",
            "1. the earlier point-landmark acquisitions;",
            "2. the later continuous spherical-spiral acquisitions.",
            "",
            "It does not establish the reciprocal-spiral equation and does",
            "not select or calibrate a spherical construction map.",
            "",
        ]
    )

    return "\n".join(
        lines
    )


def write_outputs(
    analysis: dict[
        str,
        Any,
    ],
) -> None:
    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    OUT_JSON.write_text(
        json.dumps(
            analysis,
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )

    OUT_REPORT.write_text(
        render_report(
            analysis
        ),
        encoding="utf-8",
    )


def build_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Independent source-landmark endpoint consistency audit "
            "for the First Hand spherical spiral."
        )
    )

    parser.add_argument(
        "--check-inputs",
        action="store_true",
        help=(
            "Verify frozen dependencies and endpoint row identities "
            "without calculating endpoint distances."
        ),
    )

    return parser


def main() -> int:
    args = (
        build_argument_parser()
        .parse_args()
    )

    if args.check_inputs:
        rows1, rows2, consensus = (
            verify_dependencies()
        )

        selected1 = (
            selected_endpoint_rows(
                rows1
            )
        )

        selected2 = (
            selected_endpoint_rows(
                rows2
            )
        )

        print(
            "Pass 1 SHA-256 seal: VERIFIED"
        )

        print(
            "Pass 2 SHA-256 seal: VERIFIED"
        )

        print(
            "Frozen reproducibility result: VERIFIED"
        )

        print(
            "Endpoint topology ledger: VERIFIED"
        )

        print(
            "Neutral landmark consensus schema: VERIFIED"
        )

        print(
            "Inner prior landmark role:",
            consensus[
                INNER_ID
            ][
                "fit_partition"
            ],
        )

        print(
            "Outer prior landmark role:",
            consensus[
                OUTER_ID
            ][
                "fit_partition"
            ],
        )

        print(
            "Pass 1 inner row:",
            selected1[
                "inner"
            ][
                "segment_id"
            ],
            selected1[
                "inner"
            ][
                "sequence_index"
            ],
        )

        print(
            "Pass 1 outer row:",
            selected1[
                "outer"
            ][
                "segment_id"
            ],
            selected1[
                "outer"
            ][
                "sequence_index"
            ],
        )

        print(
            "Pass 2 inner row:",
            selected2[
                "inner"
            ][
                "segment_id"
            ],
            selected2[
                "inner"
            ][
                "sequence_index"
            ],
        )

        print(
            "Pass 2 outer row:",
            selected2[
                "outer"
            ][
                "segment_id"
            ],
            selected2[
                "outer"
            ][
                "sequence_index"
            ],
        )

        print(
            "No endpoint distance was computed."
        )

        return 0

    analysis = (
        build_analysis()
    )

    write_outputs(
        analysis
    )

    print(
        "="
        * 88
    )

    print(
        "FIRST HAND SPHERICAL SPIRAL ENDPOINT CONSISTENCY"
    )

    print(
        "="
        * 88
    )

    for endpoint_name in (
        "inner",
        "outer",
    ):
        result = analysis[
            endpoint_name
        ]

        print(
            endpoint_name.upper()
        )

        print(
            "  pass 1 distance: "
            f"{result['pass1']['distance_to_prior_landmark_px']:.12f} px"
        )

        print(
            "  pass 2 distance: "
            f"{result['pass2']['distance_to_prior_landmark_px']:.12f} px"
        )

        print(
            "  mean endpoint distance: "
            f"{result['two_pass_spiral_endpoint']['mean_distance_to_prior_landmark_px']:.12f} px"
        )

        print(
            "  spiral endpoint pass separation: "
            f"{result['two_pass_spiral_endpoint']['pass_separation_px']:.12f} px"
        )

        print(
            "  prior landmark consensus uncertainty: "
            f"{result['prior_landmark']['consensus_uncertainty_px']:.12f} px"
        )

        print(
            "-"
            * 88
        )

    print(
        f"Wrote {OUT_JSON}"
    )

    print(
        f"Wrote {OUT_REPORT}"
    )

    print(
        "No snapping, fitting, extrapolation, registration, "
        "theoretical spiral, or coordinate model was used."
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
