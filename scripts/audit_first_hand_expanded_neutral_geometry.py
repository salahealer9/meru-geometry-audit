#!/usr/bin/env python3
"""Expanded First Hand neutral geometry census.

This stage regenerates the original neutral census from the two frozen
neutral passes and adds the three frozen incidence-addendum points. It
does not fit any great-circle trace, infer hidden curve segments, select
a projective map, choose a unit convention, reconcile truncations, or
compute S1, S1.5, or S2.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import sys
from pathlib import Path
from typing import Any, Iterable, Sequence

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image


ROOT = Path(__file__).resolve().parents[1]

if str(ROOT) not in sys.path:
    sys.path.insert(
        0,
        str(ROOT),
    )

from scripts import audit_first_hand_neutral_geometry as neutral  # noqa: E402
from scripts import digitize_first_hand_diagram_landmarks as digitizer  # noqa: E402


DATA_DIR = (
    ROOT
    / "data"
    / "derived"
    / "first_hand_arm_of_god"
)

ADDENDUM_PASS_PATHS = {
    1: DATA_DIR / "diagram_incidence_addendum_pass1.csv",
    2: DATA_DIR / "diagram_incidence_addendum_pass2.csv",
}

ADDENDUM_CHECKSUM_PATH = (
    DATA_DIR
    / "diagram_incidence_addendum_passes.sha256"
)

EXPANDED_CONSENSUS_PATH = (
    DATA_DIR
    / "expanded_neutral_landmark_consensus.csv"
)

EXPANDED_RESULT_PATH = (
    DATA_DIR
    / "expanded_neutral_geometry_census.json"
)

EXPANDED_REPORT_PATH = (
    ROOT
    / "reports"
    / "first_hand_expanded_neutral_geometry_census.md"
)

EXPANDED_FIGURE_PATH = (
    ROOT
    / "figures"
    / "first_hand_expanded_neutral_geometry_overlay.png"
)

ADDENDUM_IDS = (
    "AOG-LM-P07-X1-UC-LL-INTERSECTION",
    "AOG-LM-P07-X1-UC-LR-INTERSECTION",
    "AOG-LM-P07-YAXIS-UC-UCLR-INTERSECTION",
)

X1_UC_LL_ID = ADDENDUM_IDS[0]
UCLR_ID = ADDENDUM_IDS[1]
YAXIS_NODE_ID = ADDENDUM_IDS[2]

CENTRAL_ID = "AOG-LM-P07-CENTRAL-REFERENCE-NODE"
LR_ID = "AOG-LM-P07-RIM-NODE-LR-SHARED"

ADDENDUM_UNCERTAINTY_FLOOR_PX = 2.0


def sha256_path(path: Path) -> str:
    """Return a file SHA-256 digest."""
    digest = hashlib.sha256()

    with path.open("rb") as handle:
        for block in iter(
            lambda: handle.read(1 << 20),
            b"",
        ):
            digest.update(block)

    return digest.hexdigest()


def read_csv(path: Path) -> list[dict[str, str]]:
    """Read a CSV file."""
    with path.open(
        newline="",
        encoding="utf-8",
    ) as handle:
        return list(
            csv.DictReader(handle)
        )


def group_by_landmark(
    rows: Iterable[dict[str, str]],
) -> dict[str, list[dict[str, str]]]:
    """Group rows by landmark ID."""
    grouped: dict[str, list[dict[str, str]]] = {}

    for row in rows:
        grouped.setdefault(
            row["landmark_id"],
            [],
        ).append(row)

    for landmark_rows in grouped.values():
        landmark_rows.sort(
            key=lambda item: int(
                item["sequence_index"]
            )
        )

    return grouped


def verify_checksum_manifest(
    manifest_path: Path,
    expected_filenames: set[str],
) -> dict[str, str]:
    """Verify an exact frozen checksum manifest."""
    entries: dict[str, str] = {}

    for raw_line in manifest_path.read_text(
        encoding="utf-8",
    ).splitlines():
        line = raw_line.strip()

        if not line:
            continue

        digest, filename = line.split()

        if filename in entries:
            raise RuntimeError(
                f"Duplicate checksum entry: {filename}"
            )

        entries[filename] = digest

    if set(entries) != expected_filenames:
        raise RuntimeError(
            f"Unexpected checksum vocabulary in {manifest_path}; "
            f"expected={sorted(expected_filenames)}, "
            f"received={sorted(entries)}"
        )

    for filename, expected_digest in entries.items():
        path = manifest_path.parent / filename

        if not path.exists():
            raise RuntimeError(
                f"Checksum target is missing: {path}"
            )

        actual_digest = sha256_path(
            path
        )

        if actual_digest != expected_digest:
            raise RuntimeError(
                f"Checksum mismatch for {path}: "
                f"expected {expected_digest}, "
                f"received {actual_digest}"
            )

    return entries


def validate_addendum_pass(
    pass_number: int,
    path: Path,
) -> list[dict[str, str]]:
    """Validate one frozen three-point addendum pass."""
    rows = read_csv(
        path
    )

    if len(rows) != 3:
        raise RuntimeError(
            f"{path} must contain exactly three rows."
        )

    if {
        int(row["pass_number"])
        for row in rows
    } != {pass_number}:
        raise RuntimeError(
            f"Unexpected pass number in {path}."
        )

    ids = [
        row["landmark_id"]
        for row in rows
    ]

    if set(ids) != set(ADDENDUM_IDS):
        raise RuntimeError(
            f"Unexpected addendum vocabulary in {path}."
        )

    if len(ids) != len(set(ids)):
        raise RuntimeError(
            f"Duplicate addendum landmark in {path}."
        )

    for row in rows:
        if row["object_type"] != "point":
            raise RuntimeError(
                f"Non-point row in {path}."
            )

        if row["fit_partition"] != "calibration":
            raise RuntimeError(
                f"Unexpected fit partition in {path}."
            )

        if int(row["sequence_index"]) != 0:
            raise RuntimeError(
                f"Point sequence index must be zero in {path}."
            )

    if len({
        row["crop_file_sha256"]
        for row in rows
    }) != 1:
        raise RuntimeError(
            f"Multiple crop file hashes in {path}."
        )

    if len({
        row["crop_pixel_sha256"]
        for row in rows
    }) != 1:
        raise RuntimeError(
            f"Multiple crop pixel hashes in {path}."
        )

    return rows


def build_addendum_consensus(
    pass1_rows: Sequence[dict[str, str]],
    pass2_rows: Sequence[dict[str, str]],
) -> list[dict[str, str]]:
    """Build deterministic consensus rows for the three added points."""
    grouped1 = group_by_landmark(
        pass1_rows
    )
    grouped2 = group_by_landmark(
        pass2_rows
    )

    output: list[dict[str, str]] = []

    for landmark_id in ADDENDUM_IDS:
        row1 = grouped1[
            landmark_id
        ][0]
        row2 = grouped2[
            landmark_id
        ][0]

        if (
            row1["crop_file_sha256"]
            != row2["crop_file_sha256"]
        ):
            raise RuntimeError(
                f"Crop file hash mismatch for {landmark_id}."
            )

        if (
            row1["crop_pixel_sha256"]
            != row2["crop_pixel_sha256"]
        ):
            raise RuntimeError(
                f"Crop pixel hash mismatch for {landmark_id}."
            )

        point1 = np.asarray(
            [
                float(row1["x_px"]),
                float(row1["y_px"]),
            ],
            dtype=float,
        )
        point2 = np.asarray(
            [
                float(row2["x_px"]),
                float(row2["y_px"]),
            ],
            dtype=float,
        )

        consensus = (
            point1 + point2
        ) / 2.0

        separation = float(
            np.linalg.norm(
                point1 - point2
            )
        )

        width1 = float(
            row1[
                "local_stroke_width_px"
            ]
        )
        width2 = float(
            row2[
                "local_stroke_width_px"
            ]
        )

        uncertainty = max(
            ADDENDUM_UNCERTAINTY_FLOOR_PX,
            0.5 * max(
                width1,
                width2,
            ),
            0.5 * separation,
        )

        output.append(
            {
                "landmark_id": landmark_id,
                "source_feature": row1[
                    "source_feature"
                ],
                "fit_partition": row1[
                    "fit_partition"
                ],
                "pass1_x_px": format(
                    point1[0],
                    ".12g",
                ),
                "pass1_y_px": format(
                    point1[1],
                    ".12g",
                ),
                "pass2_x_px": format(
                    point2[0],
                    ".12g",
                ),
                "pass2_y_px": format(
                    point2[1],
                    ".12g",
                ),
                "consensus_x_px": format(
                    consensus[0],
                    ".12g",
                ),
                "consensus_y_px": format(
                    consensus[1],
                    ".12g",
                ),
                "pass_separation_px": format(
                    separation,
                    ".12g",
                ),
                "pass1_stroke_width_px": format(
                    width1,
                    ".12g",
                ),
                "pass2_stroke_width_px": format(
                    width2,
                    ".12g",
                ),
                "uncertainty_floor_px": format(
                    ADDENDUM_UNCERTAINTY_FLOOR_PX,
                    ".12g",
                ),
                "consensus_uncertainty_px": format(
                    uncertainty,
                    ".12g",
                ),
                "crop_file_sha256": row1[
                    "crop_file_sha256"
                ],
                "crop_pixel_sha256": row1[
                    "crop_pixel_sha256"
                ],
            }
        )

    return output


def consensus_lookup(
    rows: Sequence[dict[str, str]],
) -> dict[str, np.ndarray]:
    """Map each consensus row to its 2D coordinate."""
    return {
        row["landmark_id"]: np.asarray(
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
        for row in rows
    }


def uncertainty_lookup(
    rows: Sequence[dict[str, str]],
) -> dict[str, float]:
    """Map each consensus row to its protocol uncertainty."""
    return {
        row["landmark_id"]: float(
            row[
                "consensus_uncertainty_px"
            ]
        )
        for row in rows
    }


def angle_deg(
    first: np.ndarray,
    vertex: np.ndarray,
    second: np.ndarray,
) -> float:
    """Return the unsigned angle first-vertex-second in degrees."""
    vector1 = np.asarray(
        first,
        dtype=float,
    ) - np.asarray(
        vertex,
        dtype=float,
    )
    vector2 = np.asarray(
        second,
        dtype=float,
    ) - np.asarray(
        vertex,
        dtype=float,
    )

    norm1 = float(
        np.linalg.norm(
            vector1
        )
    )
    norm2 = float(
        np.linalg.norm(
            vector2
        )
    )

    if norm1 <= 0.0 or norm2 <= 0.0:
        raise ValueError(
            "Angle rays must have non-zero length."
        )

    cosine = float(
        np.dot(
            vector1,
            vector2,
        )
        / (
            norm1 * norm2
        )
    )

    cosine = min(
        1.0,
        max(
            -1.0,
            cosine,
        ),
    )

    return math.degrees(
        math.acos(
            cosine
        )
    )


def mathematical_bearing_deg(
    start: np.ndarray,
    end: np.ndarray,
) -> float:
    """Return a bearing with 0° rightward and 90° upward."""
    dx = float(
        end[0] - start[0]
    )
    dy_up = float(
        start[1] - end[1]
    )

    return (
        math.degrees(
            math.atan2(
                dy_up,
                dx,
            )
        )
        % 360.0
    )


def point_line_distance(
    point: np.ndarray,
    line_point1: np.ndarray,
    line_point2: np.ndarray,
) -> float:
    """Return the Euclidean distance from a point to an infinite line."""
    point = np.asarray(
        point,
        dtype=float,
    )
    line_point1 = np.asarray(
        line_point1,
        dtype=float,
    )
    line_point2 = np.asarray(
        line_point2,
        dtype=float,
    )

    direction = (
        line_point2 - line_point1
    )
    length = float(
        np.linalg.norm(
            direction
        )
    )

    if length <= 0.0:
        raise ValueError(
            "Line-defining points must be distinct."
        )

    displacement = (
        point - line_point1
    )

    cross = abs(
        float(
            direction[0]
            * displacement[1]
            - direction[1]
            * displacement[0]
        )
    )

    return (
        cross / length
    )


def numerical_angle_gradient(
    first: np.ndarray,
    vertex: np.ndarray,
    second: np.ndarray,
    step_px: float = 1.0e-3,
) -> np.ndarray:
    """Return a finite-difference gradient of the three-point angle.

    Coordinates are ordered:
    first_x, first_y, vertex_x, vertex_y, second_x, second_y.
    """
    packed = np.concatenate(
        (
            np.asarray(
                first,
                dtype=float,
            ),
            np.asarray(
                vertex,
                dtype=float,
            ),
            np.asarray(
                second,
                dtype=float,
            ),
        )
    )

    gradient = np.zeros(
        6,
        dtype=float,
    )

    for index in range(6):
        plus = packed.copy()
        minus = packed.copy()

        plus[index] += step_px
        minus[index] -= step_px

        value_plus = angle_deg(
            plus[0:2],
            plus[2:4],
            plus[4:6],
        )
        value_minus = angle_deg(
            minus[0:2],
            minus[2:4],
            minus[4:6],
        )

        gradient[index] = (
            value_plus - value_minus
        ) / (
            2.0 * step_px
        )

    return gradient


def linearized_angle_sensitivity_deg(
    first: np.ndarray,
    vertex: np.ndarray,
    second: np.ndarray,
    first_uncertainty_px: float,
    vertex_uncertainty_px: float,
    second_uncertainty_px: float,
) -> float:
    """Propagate isotropic point scales through the angle Jacobian.

    This is a linearized sensitivity scale, not a confidence interval.
    """
    gradient = numerical_angle_gradient(
        first,
        vertex,
        second,
    )

    coordinate_scales = np.asarray(
        [
            first_uncertainty_px,
            first_uncertainty_px,
            vertex_uncertainty_px,
            vertex_uncertainty_px,
            second_uncertainty_px,
            second_uncertainty_px,
        ],
        dtype=float,
    )

    return float(
        np.sqrt(
            np.sum(
                (
                    gradient
                    * coordinate_scales
                )
                ** 2
            )
        )
    )


def build_expanded_analysis() -> tuple[
    dict[str, Any],
    list[dict[str, str]],
    dict[str, np.ndarray],
]:
    """Regenerate neutral results and append the three-node census."""
    neutral_analysis, neutral_rows, _ = (
        neutral.build_analysis()
    )

    verify_checksum_manifest(
        ADDENDUM_CHECKSUM_PATH,
        {
            ADDENDUM_PASS_PATHS[1].name,
            ADDENDUM_PASS_PATHS[2].name,
        },
    )

    addendum_passes = {
        pass_number: validate_addendum_pass(
            pass_number,
            path,
        )
        for pass_number, path in ADDENDUM_PASS_PATHS.items()
    }

    neutral_crop_hash = neutral_analysis[
        "provenance"
    ][
        "crop_file_sha256"
    ]
    neutral_pixel_hash = neutral_analysis[
        "provenance"
    ][
        "crop_pixel_sha256"
    ]

    for rows in addendum_passes.values():
        if {
            row["crop_file_sha256"]
            for row in rows
        } != {
            neutral_crop_hash
        }:
            raise RuntimeError(
                "Addendum and neutral passes use different crop files."
            )

        if {
            row["crop_pixel_sha256"]
            for row in rows
        } != {
            neutral_pixel_hash
        }:
            raise RuntimeError(
                "Addendum and neutral passes use different crop pixels."
            )

    addendum_rows = build_addendum_consensus(
        addendum_passes[1],
        addendum_passes[2],
    )

    expanded_rows = [
        *neutral_rows,
        *addendum_rows,
    ]

    coordinates = consensus_lookup(
        expanded_rows
    )
    uncertainties = uncertainty_lookup(
        expanded_rows
    )

    central = coordinates[
        CENTRAL_ID
    ]
    uclr = coordinates[
        UCLR_ID
    ]
    lower_right = coordinates[
        LR_ID
    ]
    yaxis_node = coordinates[
        YAXIS_NODE_ID
    ]
    x1_uc_ll = coordinates[
        X1_UC_LL_ID
    ]

    limb_circle = neutral_analysis[
        "limb_geometry"
    ][
        "equal_pass_weight_circle"
    ]

    limb_center = np.asarray(
        [
            limb_circle[
                "center_x_px"
            ],
            limb_circle[
                "center_y_px"
            ],
        ],
        dtype=float,
    )
    limb_radius = float(
        limb_circle[
            "radius_px"
        ]
    )

    node_angle = angle_deg(
        uclr,
        central,
        lower_right,
    )

    angle_sensitivity = (
        linearized_angle_sensitivity_deg(
            uclr,
            central,
            lower_right,
            uncertainties[
                UCLR_ID
            ],
            uncertainties[
                CENTRAL_ID
            ],
            uncertainties[
                LR_ID
            ],
        )
    )

    central_to_uclr = float(
        np.linalg.norm(
            uclr - central
        )
    )
    central_to_lr = float(
        np.linalg.norm(
            lower_right - central
        )
    )

    yaxis_direction_bearing = (
        mathematical_bearing_deg(
            central,
            yaxis_node,
        )
    )

    limb_center_to_yaxis_line = (
        point_line_distance(
            limb_center,
            central,
            yaxis_node,
        )
    )

    addendum_nodes: dict[str, Any] = {}

    for row in addendum_rows:
        landmark_id = row[
            "landmark_id"
        ]
        point = coordinates[
            landmark_id
        ]

        radial_distance = float(
            np.linalg.norm(
                point - limb_center
            )
        )

        addendum_nodes[
            landmark_id
        ] = {
            "consensus_x_px": float(
                point[0]
            ),
            "consensus_y_px": float(
                point[1]
            ),
            "pass_separation_px": float(
                row[
                    "pass_separation_px"
                ]
            ),
            "consensus_uncertainty_px": float(
                row[
                    "consensus_uncertainty_px"
                ]
            ),
            "bearing_from_limb_center_deg": (
                mathematical_bearing_deg(
                    limb_center,
                    point,
                )
            ),
            "radial_distance_from_limb_center_px": (
                radial_distance
            ),
            "radial_fraction_of_limb_radius": (
                radial_distance
                / limb_radius
            ),
        }

    expanded_analysis: dict[str, Any] = {
        "analysis_id": (
            "first_hand_expanded_neutral_geometry_census_v0_8"
        ),
        "scope": {
            "uses_only": [
                "frozen prepared source crop",
                "two frozen original neutral passes",
                "two frozen three-point incidence-addendum passes",
            ],
            "does_not_compute": [
                "great-circle trace or curve fit",
                "hidden-curve interpolation",
                "projective-map selection",
                "unit-angle selection",
                "truncation reconciliation",
                "S1 tangent alignment",
                "S1.5 Darboux-frame alignment",
                "S2 recursive nesting",
            ],
        },
        "provenance": {
            "neutral_pass_checksum_manifest": str(
                neutral.CHECKSUM_PATH.relative_to(
                    ROOT
                )
            ),
            "neutral_pass_checksum_manifest_sha256": (
                sha256_path(
                    neutral.CHECKSUM_PATH
                )
            ),
            "addendum_pass_checksum_manifest": str(
                ADDENDUM_CHECKSUM_PATH.relative_to(
                    ROOT
                )
            ),
            "addendum_pass_checksum_manifest_sha256": (
                sha256_path(
                    ADDENDUM_CHECKSUM_PATH
                )
            ),
            "crop_id": neutral_analysis[
                "provenance"
            ][
                "crop_id"
            ],
            "crop_file_sha256": neutral_crop_hash,
            "crop_pixel_sha256": neutral_pixel_hash,
            "original_neutral_point_count": len(
                neutral_rows
            ),
            "incidence_addendum_point_count": len(
                addendum_rows
            ),
            "expanded_point_count": len(
                expanded_rows
            ),
        },
        "original_neutral_census": neutral_analysis,
        "incidence_addendum": {
            "nodes": addendum_nodes,
            "x1_node_pair": {
                "first_landmark_id": X1_UC_LL_ID,
                "second_landmark_id": UCLR_ID,
                "chord_length_px": float(
                    np.linalg.norm(
                        uclr - x1_uc_ll
                    )
                ),
                "chord_bearing_deg": (
                    mathematical_bearing_deg(
                        x1_uc_ll,
                        uclr,
                    )
                ),
                "interpretation_boundary": (
                    "This is an image-space chord between two "
                    "source-labelled x=1 incidence nodes, not a "
                    "great-circle or conic fit."
                ),
            },
            "node_defined_thirty_degree_diagnostic": {
                "vertex_landmark_id": CENTRAL_ID,
                "first_ray_landmark_id": UCLR_ID,
                "second_ray_landmark_id": LR_ID,
                "angle_deg": node_angle,
                "signed_residual_from_30_deg": (
                    node_angle - 30.0
                ),
                "absolute_residual_from_30_deg": abs(
                    node_angle - 30.0
                ),
                "linearized_coordinate_sensitivity_deg": (
                    angle_sensitivity
                ),
                "central_to_uclr_length_px": (
                    central_to_uclr
                ),
                "central_to_lr_length_px": (
                    central_to_lr
                ),
                "ray_length_ratio_uclr_over_lr": (
                    central_to_uclr
                    / central_to_lr
                ),
                "sensitivity_note": (
                    "The reported angular sensitivity is a "
                    "first-order propagation of the protocol point "
                    "uncertainty scales under isotropic independent "
                    "coordinate perturbations. It is not a confidence "
                    "interval."
                ),
                "compatibility_assessment": (
                    "compatible with an intended 30-degree construction "
                    "at the resolution of the hand-drawn source"
                ),
                "interpretation_boundary": (
                    "The measured residual is smaller than the linearized "
                    "coordinate-sensitivity scale. Because the source is "
                    "hand-drawn and drafting, line-width, scanning, and "
                    "page-deformation effects are not included in that "
                    "sensitivity, the result is compatible with an intended "
                    "30-degree construction. It does not assume an "
                    "angle-preserving projective map and does not certify "
                    "an exact 30-degree angle."
                ),
            },
            "yaxis_two_node_diagnostic": {
                "central_landmark_id": CENTRAL_ID,
                "separate_yaxis_landmark_id": YAXIS_NODE_ID,
                "node_separation_px": float(
                    np.linalg.norm(
                        yaxis_node - central
                    )
                ),
                "bearing_central_to_yaxis_node_deg": (
                    yaxis_direction_bearing
                ),
                "limb_center_distance_to_two_node_line_px": (
                    limb_center_to_yaxis_line
                ),
                "limb_center_distance_fraction_of_radius": (
                    limb_center_to_yaxis_line
                    / limb_radius
                ),
                "interpretation_boundary": (
                    "Two nodes define an image-space direction only. "
                    "Agreement with the printed y-axis curve remains "
                    "for the later segment-aware trace stage."
                ),
            },
        },
        "verdict": (
            "No great-circle, projective-map, unit-angle, "
            "truncation, or self-embedment verdict is issued."
        ),
    }

    return (
        expanded_analysis,
        expanded_rows,
        coordinates,
    )


def write_consensus_csv(
    path: Path,
    rows: Sequence[dict[str, str]],
) -> None:
    """Write the combined 15-point consensus CSV."""
    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with path.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=neutral.CONSENSUS_FIELDS,
        )
        writer.writeheader()
        writer.writerows(rows)


def write_json(
    path: Path,
    payload: dict[str, Any],
) -> None:
    """Write deterministic expanded JSON."""
    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    path.write_text(
        json.dumps(
            payload,
            indent=2,
            sort_keys=True,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )


def format_float(
    value: float,
    digits: int = 6,
) -> str:
    """Format a report number."""
    return f"{value:.{digits}f}"


def build_report(
    analysis: dict[str, Any],
) -> str:
    """Build the expanded-census Markdown report."""
    neutral_analysis = analysis[
        "original_neutral_census"
    ]
    neutral_limb = neutral_analysis[
        "limb_geometry"
    ][
        "equal_pass_weight_circle"
    ]
    neutral_sixfold = neutral_analysis[
        "rim_node_census"
    ][
        "sixfold_fit"
    ]
    neutral_central = neutral_analysis[
        "central_reference"
    ]

    addendum = analysis[
        "incidence_addendum"
    ]
    angle = addendum[
        "node_defined_thirty_degree_diagnostic"
    ]
    yaxis = addendum[
        "yaxis_two_node_diagnostic"
    ]
    x1_pair = addendum[
        "x1_node_pair"
    ]

    lines = [
        "# First Hand expanded neutral geometry census",
        "",
        "**Stage:** v0.8 neutral census plus frozen incidence addendum",
        "",
        "## Scope",
        "",
        (
            "This report regenerates the original neutral census and "
            "adds the three separately preregistered and frozen "
            "incidence nodes. It does not fit a great-circle trace, "
            "interpolate hidden curves, select a projective map, choose "
            "a unit convention, reconcile truncations, or compute "
            "S1, S1.5, or S2."
        ),
        "",
        "## Provenance",
        "",
        (
            "- Original neutral point landmarks: "
            f"`{analysis['provenance']['original_neutral_point_count']}`"
        ),
        (
            "- Incidence-addendum point landmarks: "
            f"`{analysis['provenance']['incidence_addendum_point_count']}`"
        ),
        (
            "- Expanded point consensus: "
            f"`{analysis['provenance']['expanded_point_count']}`"
        ),
        (
            "- Crop pixel SHA-256: "
            f"`{analysis['provenance']['crop_pixel_sha256']}`"
        ),
        "",
        "## Regenerated original neutral census",
        "",
        (
            "- Equal-pass limb centre: "
            f"`({format_float(neutral_limb['center_x_px'])}, "
            f"{format_float(neutral_limb['center_y_px'])}) px`"
        ),
        (
            "- Equal-pass limb radius: "
            f"`{format_float(neutral_limb['radius_px'])} px`"
        ),
        (
            "- Sixfold bearing RMS residual: "
            f"`{format_float(neutral_sixfold['bearing_rms_residual_deg'])}°`"
        ),
        (
            "- Central circular-node offset/radius: "
            f"`{format_float(neutral_central['offset_fraction_of_limb_radius'], 8)}`"
        ),
        "",
        (
            "These values are regenerated directly from the frozen "
            "original passes; the provisional pre-addendum result files "
            "are not reused."
        ),
        "",
        "## Added incidence-node consensus",
        "",
        "| Landmark | x (px) | y (px) | Pass separation (px) | Uncertainty (px) | Bearing from limb centre (deg) | Radial fraction |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]

    for landmark_id in ADDENDUM_IDS:
        item = addendum[
            "nodes"
        ][
            landmark_id
        ]

        lines.append(
            "| "
            f"`{landmark_id}` | "
            f"{format_float(item['consensus_x_px'], 3)} | "
            f"{format_float(item['consensus_y_px'], 3)} | "
            f"{format_float(item['pass_separation_px'], 3)} | "
            f"{format_float(item['consensus_uncertainty_px'], 3)} | "
            f"{format_float(item['bearing_from_limb_center_deg'], 3)} | "
            f"{format_float(item['radial_fraction_of_limb_radius'], 6)} |"
        )

    lines.extend(
        [
            "",
            "## Node-defined 30-degree diagnostic",
            "",
            (
                "- Measured angle "
                "`angle(UCLR, central, LR)`: "
                f"`{format_float(angle['angle_deg'])}°`"
            ),
            (
                "- Signed residual from 30°: "
                f"`{format_float(angle['signed_residual_from_30_deg'])}°`"
            ),
            (
                "- Absolute residual from 30°: "
                f"`{format_float(angle['absolute_residual_from_30_deg'])}°`"
            ),
            (
                "- Linearized coordinate sensitivity: "
                f"`{format_float(angle['linearized_coordinate_sensitivity_deg'])}°`"
            ),
            (
                "- Central→UCLR length: "
                f"`{format_float(angle['central_to_uclr_length_px'])} px`"
            ),
            (
                "- Central→LR length: "
                f"`{format_float(angle['central_to_lr_length_px'])} px`"
            ),
            (
                "- Ray-length ratio UCLR/LR: "
                f"`{format_float(angle['ray_length_ratio_uclr_over_lr'])}`"
            ),
            "",
            (
                "The sensitivity is a first-order propagation of the "
                "protocol point scales, not a confidence interval. The "
                "2.363-degree residual is smaller than the 2.449-degree "
                "linearized sensitivity scale. Because the source is "
                "hand-drawn, additional drafting, line-width, scanning, "
                "and page-deformation effects are not represented by that "
                "scale. The result is therefore compatible with an intended "
                "30-degree construction, but it does not certify an exact "
                "30-degree angle or an angle-preserving projective map. "
                "The ambiguous printed 30-degree arc remains deferred."
            ),
            "",
            "## Y-axis two-node diagnostic",
            "",
            (
                "- Central-to-separate-node distance: "
                f"`{format_float(yaxis['node_separation_px'])} px`"
            ),
            (
                "- Bearing from central node: "
                f"`{format_float(yaxis['bearing_central_to_yaxis_node_deg'])}°`"
            ),
            (
                "- Fitted limb-centre distance to the two-node line: "
                f"`{format_float(yaxis['limb_center_distance_to_two_node_line_px'])} px`"
            ),
            (
                "- Normalized centre-to-line distance: "
                f"`{format_float(yaxis['limb_center_distance_fraction_of_radius'])}`"
            ),
            "",
            (
                "The two nodes define only an image-space direction. "
                "Whether the printed y-axis trace follows the same "
                "projected great circle remains for segment-aware curve "
                "digitization."
            ),
            "",
            "## Two x=1 incidence nodes",
            "",
            (
                "- Node-pair chord length: "
                f"`{format_float(x1_pair['chord_length_px'])} px`"
            ),
            (
                "- Chord bearing: "
                f"`{format_float(x1_pair['chord_bearing_deg'])}°`"
            ),
            "",
            (
                "This chord is descriptive only. Two incidence nodes do "
                "not determine the full printed x=1 great-circle image."
            ),
            "",
            "## Interpretation boundary",
            "",
            (
                "No great-circle, projective-map, unit-angle, "
                "truncation, or self-embedment verdict is issued."
            ),
            "",
        ]
    )

    return "\n".join(
        lines
    )


def write_report(
    path: Path,
    analysis: dict[str, Any],
) -> None:
    """Write the expanded Markdown report."""
    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    path.write_text(
        build_report(
            analysis
        ),
        encoding="utf-8",
    )


def write_overlay(
    path: Path,
    analysis: dict[str, Any],
    rows: Sequence[dict[str, str]],
) -> None:
    """Write an expanded source-overlay diagnostic figure."""
    crop_id = analysis[
        "provenance"
    ][
        "crop_id"
    ]

    crops = digitizer.read_crop_manifest()

    if crop_id not in crops:
        raise RuntimeError(
            f"Prepared crop is missing from the manifest: {crop_id}"
        )

    verified_image = digitizer.verify_crop(
        crops[crop_id]
    )

    if hasattr(
        verified_image,
        "convert",
    ):
        image = verified_image.convert(
            "RGB"
        )
    else:
        image = Image.fromarray(
            np.asarray(
                verified_image
            )
        ).convert(
            "RGB"
        )

    coordinates = consensus_lookup(
        rows
    )
    uncertainties = uncertainty_lookup(
        rows
    )

    limb_circle = analysis[
        "original_neutral_census"
    ][
        "limb_geometry"
    ][
        "equal_pass_weight_circle"
    ]

    theta = np.linspace(
        0.0,
        2.0 * math.pi,
        1000,
    )

    circle_x = (
        limb_circle[
            "center_x_px"
        ]
        + limb_circle[
            "radius_px"
        ]
        * np.cos(
            theta
        )
    )
    circle_y = (
        limb_circle[
            "center_y_px"
        ]
        + limb_circle[
            "radius_px"
        ]
        * np.sin(
            theta
        )
    )

    figure, axis = plt.subplots(
        figsize=(14, 10)
    )

    axis.imshow(
        image
    )
    axis.plot(
        circle_x,
        circle_y,
        linewidth=1.2,
        label="Equal-pass limb circle",
    )

    original_ids = {
        row["landmark_id"]
        for row in rows
    } - set(
        ADDENDUM_IDS
    )

    for landmark_id in sorted(
        original_ids
    ):
        point = coordinates[
            landmark_id
        ]

        axis.errorbar(
            [point[0]],
            [point[1]],
            xerr=[
                uncertainties[
                    landmark_id
                ]
            ],
            yerr=[
                uncertainties[
                    landmark_id
                ]
            ],
            fmt=".",
            markersize=4,
            capsize=1,
        )

    short_labels = {
        X1_UC_LL_ID: "X1–UC–LL",
        UCLR_ID: "UCLR",
        YAXIS_NODE_ID: "y-axis node",
    }

    for landmark_id in ADDENDUM_IDS:
        point = coordinates[
            landmark_id
        ]
        uncertainty = uncertainties[
            landmark_id
        ]

        axis.errorbar(
            [point[0]],
            [point[1]],
            xerr=[uncertainty],
            yerr=[uncertainty],
            fmt="o",
            markersize=6,
            capsize=2,
            label=(
                "Incidence addendum"
                if landmark_id == ADDENDUM_IDS[0]
                else None
            ),
        )

        axis.annotate(
            short_labels[
                landmark_id
            ],
            xy=(
                point[0],
                point[1],
            ),
            xytext=(
                6,
                6,
            ),
            textcoords="offset points",
            fontsize=8,
        )

    central = coordinates[
        CENTRAL_ID
    ]
    uclr = coordinates[
        UCLR_ID
    ]
    lower_right = coordinates[
        LR_ID
    ]
    yaxis_node = coordinates[
        YAXIS_NODE_ID
    ]
    x1_uc_ll = coordinates[
        X1_UC_LL_ID
    ]

    axis.plot(
        [
            central[0],
            uclr[0],
        ],
        [
            central[1],
            uclr[1],
        ],
        linewidth=1.0,
        label="Central→UCLR ray",
    )
    axis.plot(
        [
            central[0],
            lower_right[0],
        ],
        [
            central[1],
            lower_right[1],
        ],
        linewidth=1.0,
        label="Central→LR ray",
    )
    axis.plot(
        [
            central[0],
            yaxis_node[0],
        ],
        [
            central[1],
            yaxis_node[1],
        ],
        linestyle="--",
        linewidth=1.0,
        label="Two-node y-axis direction",
    )
    axis.plot(
        [
            x1_uc_ll[0],
            uclr[0],
        ],
        [
            x1_uc_ll[1],
            uclr[1],
        ],
        linestyle="--",
        linewidth=1.0,
        label="Two-node x=1 chord",
    )

    angle_value = analysis[
        "incidence_addendum"
    ][
        "node_defined_thirty_degree_diagnostic"
    ][
        "angle_deg"
    ]

    axis.set_title(
        "First Hand expanded neutral geometry census\n"
        f"Node-defined angle = {angle_value:.3f}°"
    )
    axis.set_xlabel(
        "Prepared-crop x coordinate (px)"
    )
    axis.set_ylabel(
        "Prepared-crop y coordinate (px)"
    )
    axis.set_xlim(
        0,
        image.width,
    )
    axis.set_ylim(
        image.height,
        0,
    )
    axis.set_aspect(
        "equal"
    )
    axis.legend(
        loc="best",
        fontsize=8,
    )

    figure.tight_layout()

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    figure.savefig(
        path,
        dpi=180,
        bbox_inches="tight",
        metadata={
            "Title": (
                "First Hand expanded neutral "
                "geometry census"
            ),
            "Description": (
                "Frozen original and incidence-addendum "
                "point consensus with image-space diagnostics."
            ),
        },
    )

    plt.close(
        figure
    )


def build_argument_parser() -> argparse.ArgumentParser:
    """Build the command-line interface."""
    parser = argparse.ArgumentParser(
        description=(
            "Regenerate and expand the First Hand "
            "neutral geometry census."
        )
    )

    parser.add_argument(
        "--consensus-csv",
        type=Path,
        default=EXPANDED_CONSENSUS_PATH,
    )
    parser.add_argument(
        "--result-json",
        type=Path,
        default=EXPANDED_RESULT_PATH,
    )
    parser.add_argument(
        "--report",
        type=Path,
        default=EXPANDED_REPORT_PATH,
    )
    parser.add_argument(
        "--figure",
        type=Path,
        default=EXPANDED_FIGURE_PATH,
    )
    parser.add_argument(
        "--no-figure",
        action="store_true",
    )

    return parser


def main() -> int:
    """Run the expanded deterministic census."""
    args = build_argument_parser().parse_args()

    analysis, rows, _ = (
        build_expanded_analysis()
    )

    write_consensus_csv(
        args.consensus_csv,
        rows,
    )
    write_json(
        args.result_json,
        analysis,
    )
    write_report(
        args.report,
        analysis,
    )

    if not args.no_figure:
        write_overlay(
            args.figure,
            analysis,
            rows,
        )

    neutral_circle = analysis[
        "original_neutral_census"
    ][
        "limb_geometry"
    ][
        "equal_pass_weight_circle"
    ]
    angle = analysis[
        "incidence_addendum"
    ][
        "node_defined_thirty_degree_diagnostic"
    ]
    yaxis = analysis[
        "incidence_addendum"
    ][
        "yaxis_two_node_diagnostic"
    ]

    print(
        "First Hand expanded neutral geometry census: COMPLETE"
    )
    print(
        "Regenerated equal-pass circle centre: "
        f"({neutral_circle['center_x_px']:.6f}, "
        f"{neutral_circle['center_y_px']:.6f}) px"
    )
    print(
        "Node-defined angle(UCLR, central, LR): "
        f"{angle['angle_deg']:.6f} deg"
    )
    print(
        "Residual from 30 deg: "
        f"{angle['signed_residual_from_30_deg']:.6f} deg"
    )
    print(
        "Linearized angular sensitivity: "
        f"{angle['linearized_coordinate_sensitivity_deg']:.6f} deg"
    )
    print(
        "Limb-centre distance to two-node y-axis line/radius: "
        f"{yaxis['limb_center_distance_fraction_of_radius']:.8f}"
    )
    print(
        "No great-circle, projective-map, unit-angle, "
        "truncation, or self-embedment verdict was computed."
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
