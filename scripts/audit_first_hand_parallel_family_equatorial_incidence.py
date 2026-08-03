#!/usr/bin/env python3
"""First Hand parallel-family equatorial-incidence diagnostic.

This is a deterministic post-hoc structural diagnostic.

It uses only already-frozen spherical plane normals and an already-frozen
source landmark. No curve, circle, line, rendering map, or projective map
is refitted.

For an affine-parallel pair under an equator-preserving central-projective
map, the two corresponding spherical great circles must intersect in the
equatorial plane z=0.

The y-family is additionally compared with its preregistered lower-right
projective-infinity rim node.

The x-family receives no retrospectively selected rim-node comparison.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
from typing import Any

import numpy as np


ROOT = Path(__file__).resolve().parents[1]

DATA_DIR = (
    ROOT
    / "data"
    / "derived"
    / "first_hand_arm_of_god"
)

QC_DIR = DATA_DIR / "qc"

PROTOCOL_PATH = (
    ROOT
    / "docs"
    / "first_hand_parallel_family_equatorial_incidence_protocol.md"
)

PLANE_JSON = (
    QC_DIR
    / "first_hand_stereographic_plane_angles.json"
)

PLANE_SEAL = (
    QC_DIR
    / "first_hand_stereographic_plane_angles.sha256"
)

LINEAR_JSON = (
    QC_DIR
    / "first_hand_linear_central_projective_reconstruction.json"
)

LINEAR_SEAL = (
    QC_DIR
    / "first_hand_linear_central_projective_reconstruction.sha256"
)

EXPANDED_JSON = (
    DATA_DIR
    / "expanded_neutral_geometry_census.json"
)

EXPANDED_SEAL = (
    DATA_DIR
    / "expanded_neutral_geometry_census_outputs.sha256"
)

OUTPUT_JSON = (
    QC_DIR
    / "first_hand_parallel_family_equatorial_incidence.json"
)

OUTPUT_REPORT = (
    ROOT
    / "reports"
    / "first_hand_parallel_family_equatorial_incidence.md"
)


Y0_ID = "AOG-LM-P07-GC-Y0"
Y1_ID = "AOG-LM-P07-GC-Y1"
YAXIS_ID = "AOG-LM-P07-GC-YAXIS"
X1_ID = "AOG-LM-P07-GC-X1"

LR_NODE_ID = (
    "AOG-LM-P07-RIM-NODE-LR-SHARED"
)

EXPECTED_PLANE_CLASS = (
    "preregistered_stereographic_"
    "plane_angle_reconstruction"
)

EXPECTED_LINEAR_CLASS = (
    "preregistered_linear_central_"
    "projective_reconstruction"
)


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


def load_json(
    path: Path,
) -> dict[str, Any]:
    if not path.exists():
        raise RuntimeError(
            f"Missing JSON input: {path}"
        )

    return json.loads(
        path.read_text(
            encoding="utf-8",
        )
    )


def verify_sha256_manifest(
    manifest_path: Path,
    required_paths: tuple[Path, ...],
) -> dict[str, str]:
    """Verify sha256sum-style manifest and required frozen entries."""
    if not manifest_path.exists():
        raise RuntimeError(
            f"Missing SHA-256 manifest: {manifest_path}"
        )

    found: dict[str, str] = {}

    for raw in manifest_path.read_text(
        encoding="utf-8",
    ).splitlines():
        raw = raw.strip()

        if not raw:
            continue

        parts = raw.split()

        if len(parts) < 2:
            raise RuntimeError(
                f"Malformed checksum line: {raw!r}"
            )

        expected = parts[0]
        relative = parts[-1].lstrip("*")

        path = (
            ROOT
            / relative
        )

        if not path.exists():
            raise RuntimeError(
                f"Sealed file missing: {relative}"
            )

        actual = (
            sha256_path(
                path
            )
        )

        if actual != expected:
            raise RuntimeError(
                "SHA-256 mismatch for "
                f"{relative}: expected "
                f"{expected}, got {actual}"
            )

        found[
            relative
        ] = expected

    for required in required_paths:
        relative = str(
            required.relative_to(
                ROOT
            )
        )

        if relative not in found:
            raise RuntimeError(
                "Required frozen file absent "
                f"from seal: {relative}"
            )

    return found


def unit3(
    vector: np.ndarray,
) -> np.ndarray:
    vector = np.asarray(
        vector,
        dtype=np.float64,
    )

    if vector.shape != (3,):
        raise ValueError(
            "Expected a 3-vector."
        )

    norm = float(
        np.linalg.norm(
            vector
        )
    )

    if not (
        math.isfinite(norm)
        and norm > 0.0
    ):
        raise ValueError(
            "Cannot normalize invalid 3-vector."
        )

    return vector / norm


def circular_distance_deg(
    angle_a: float,
    angle_b: float,
) -> float:
    """Smallest circular separation of two directed bearings."""
    delta = (
        float(angle_a)
        - float(angle_b)
        + 180.0
    ) % 360.0 - 180.0

    return abs(
        delta
    )


def unoriented_line_bearing_pair(
    vector: np.ndarray,
) -> tuple[float, float]:
    """Return deterministic antipodal azimuth pair for a 3-D line.

    The horizontal projection is treated as an unoriented line.
    The first value is canonical in [0,180), the second is its antipode.
    """
    vector = unit3(
        vector
    )

    rho = math.hypot(
        float(
            vector[0]
        ),
        float(
            vector[1]
        ),
    )

    if rho <= 1.0e-15:
        raise ValueError(
            "Intersection line has no usable horizontal projection."
        )

    raw = math.degrees(
        math.atan2(
            float(
                vector[1]
            ),
            float(
                vector[0]
            ),
        )
    ) % 360.0

    canonical = (
        raw
        % 180.0
    )

    antipode = (
        canonical
        + 180.0
    ) % 360.0

    return (
        canonical,
        antipode,
    )


def nearest_antipodal_branch(
    bearing_deg: float,
    azimuth_a_deg: float,
    azimuth_b_deg: float,
) -> dict[str, float]:
    """Select the antipodal line direction nearest a fixed source bearing."""
    distance_a = (
        circular_distance_deg(
            bearing_deg,
            azimuth_a_deg,
        )
    )

    distance_b = (
        circular_distance_deg(
            bearing_deg,
            azimuth_b_deg,
        )
    )

    if distance_a <= distance_b:
        return {
            "selected_azimuth_deg": (
                azimuth_a_deg
            ),
            "other_azimuth_deg": (
                azimuth_b_deg
            ),
            "angular_separation_deg": (
                distance_a
            ),
        }

    return {
        "selected_azimuth_deg": (
            azimuth_b_deg
        ),
        "other_azimuth_deg": (
            azimuth_a_deg
        ),
        "angular_separation_deg": (
            distance_b
        ),
    }


def intersection_diagnostic(
    normal_a: np.ndarray,
    normal_b: np.ndarray,
) -> dict[str, Any]:
    """Compute sign-invariant great-circle intersection diagnostics."""
    n_a = unit3(
        normal_a
    )

    n_b = unit3(
        normal_b
    )

    raw = np.cross(
        n_a,
        n_b,
    )

    raw_norm = float(
        np.linalg.norm(
            raw
        )
    )

    if not (
        math.isfinite(
            raw_norm
        )
        and raw_norm > 1.0e-14
    ):
        raise ValueError(
            "Great-circle planes are degenerate or nearly identical."
        )

    direction = (
        raw
        / raw_norm
    )

    absolute_z = abs(
        float(
            direction[2]
        )
    )

    absolute_z = float(
        np.clip(
            absolute_z,
            0.0,
            1.0,
        )
    )

    epsilon_equator = math.degrees(
        math.asin(
            absolute_z
        )
    )

    azimuth_a, azimuth_b = (
        unoriented_line_bearing_pair(
            direction
        )
    )

    return {
        "normal_a": [
            float(value)
            for value
            in n_a
        ],
        "normal_b": [
            float(value)
            for value
            in n_b
        ],
        "raw_cross_product": [
            float(value)
            for value
            in raw
        ],
        "cross_product_norm": (
            raw_norm
        ),
        "normalized_intersection_direction": [
            float(value)
            for value
            in direction
        ],
        "intersection_line_unoriented": True,
        "absolute_z": (
            absolute_z
        ),
        "epsilon_equator_deg": (
            epsilon_equator
        ),
        "horizontal_azimuth_canonical_deg": (
            azimuth_a
        ),
        "horizontal_azimuth_antipode_deg": (
            azimuth_b
        ),
        "azimuth_is_horizontal_projection_when_non_equatorial": True,
    }


def plane_normal(
    plane_result: dict[str, Any],
    curve_id: str,
) -> np.ndarray:
    item = (
        plane_result[
            "reconstructed_planes"
        ][
            curve_id
        ]
    )

    normal = np.asarray(
        item[
            "unit_plane_normal"
        ],
        dtype=np.float64,
    )

    return unit3(
        normal
    )


def find_lower_right_node(
    expanded: dict[str, Any],
) -> dict[str, Any]:
    nodes = (
        expanded[
            "original_neutral_census"
        ][
            "rim_node_census"
        ][
            "nodes"
        ]
    )

    matches = [
        node
        for node in nodes
        if node.get(
            "landmark_id"
        ) == LR_NODE_ID
    ]

    if len(
        matches
    ) != 1:
        raise RuntimeError(
            "Expected exactly one frozen lower-right rim node; "
            f"found {len(matches)}."
        )

    node = matches[0]

    required = {
        "bearing_deg",
        "consensus_x_px",
        "consensus_y_px",
        "radial_distance_px",
        "radial_residual_from_limb_circle_px",
    }

    missing = (
        required
        - set(
            node
        )
    )

    if missing:
        raise RuntimeError(
            "Lower-right node is missing fields: "
            + ", ".join(
                sorted(
                    missing
                )
            )
        )

    return node


def verify_limb_agreement(
    plane_result: dict[str, Any],
    expanded: dict[str, Any],
) -> dict[str, float]:
    """Verify the plane reconstruction and neutral census use the same limb."""
    plane_limb = (
        plane_result[
            "provenance"
        ][
            "frozen_limb_reference"
        ]
    )

    expanded_limb = (
        expanded[
            "original_neutral_census"
        ][
            "limb_geometry"
        ][
            "equal_pass_weight_circle"
        ]
    )

    aliases = {
        "center_x_px": "center_x_px",
        "center_y_px": "center_y_px",
        "radius_px": "radius_px",
    }

    result: dict[
        str,
        float,
    ] = {}

    for plane_key, expanded_key in aliases.items():
        a = float(
            plane_limb[
                plane_key
            ]
        )

        b = float(
            expanded_limb[
                expanded_key
            ]
        )

        if not math.isclose(
            a,
            b,
            rel_tol=0.0,
            abs_tol=1.0e-9,
        ):
            raise RuntimeError(
                "Frozen limb disagreement for "
                f"{plane_key}: plane={a}, expanded={b}"
            )

        result[
            plane_key
        ] = a

    return result


def y_family_node_comparison(
    diagnostic: dict[str, Any],
    node: dict[str, Any],
    limb: dict[str, float],
) -> dict[str, Any]:
    node_bearing = float(
        node[
            "bearing_deg"
        ]
    )

    branch = (
        nearest_antipodal_branch(
            node_bearing,
            float(
                diagnostic[
                    "horizontal_azimuth_canonical_deg"
                ]
            ),
            float(
                diagnostic[
                    "horizontal_azimuth_antipode_deg"
                ]
            ),
        )
    )

    selected = float(
        branch[
            "selected_azimuth_deg"
        ]
    )

    theta = math.radians(
        selected
    )

    predicted_x = (
        float(
            limb[
                "center_x_px"
            ]
        )
        + float(
            limb[
                "radius_px"
            ]
        )
        * math.cos(
            theta
        )
    )

    predicted_y = (
        float(
            limb[
                "center_y_px"
            ]
        )
        - float(
            limb[
                "radius_px"
            ]
        )
        * math.sin(
            theta
        )
    )

    node_x = float(
        node[
            "consensus_x_px"
        ]
    )

    node_y = float(
        node[
            "consensus_y_px"
        ]
    )

    pixel_separation = math.hypot(
        predicted_x
        - node_x,
        predicted_y
        - node_y,
    )

    return {
        "landmark_id": (
            LR_NODE_ID
        ),
        "frozen_node_bearing_deg": (
            node_bearing
        ),
        "frozen_node_consensus_x_px": (
            node_x
        ),
        "frozen_node_consensus_y_px": (
            node_y
        ),
        "frozen_node_radial_distance_px": float(
            node[
                "radial_distance_px"
            ]
        ),
        "frozen_node_radial_residual_from_limb_circle_px": float(
            node[
                "radial_residual_from_limb_circle_px"
            ]
        ),
        "selected_predicted_azimuth_deg": (
            selected
        ),
        "other_antipodal_azimuth_deg": float(
            branch[
                "other_azimuth_deg"
            ]
        ),
        "delta_node_deg": float(
            branch[
                "angular_separation_deg"
            ]
        ),
        "predicted_limb_x_px": (
            predicted_x
        ),
        "predicted_limb_y_px": (
            predicted_y
        ),
        "delta_node_px": (
            pixel_separation
        ),
        "node_used_to_fit_planes": False,
        "node_used_to_select_model": False,
    }


def rendering_context(
    plane_result: dict[str, Any],
) -> dict[str, Any]:
    context = (
        plane_result[
            "rendering_closure_context"
        ]
    )

    return {
        Y1_ID: {
            "epsilon_power": float(
                context[
                    Y1_ID
                ][
                    "epsilon_power"
                ]
            ),
            "delta_R_px": float(
                context[
                    Y1_ID
                ][
                    "delta_R_px"
                ]
            ),
            "delta_antipodal_deg": float(
                context[
                    Y1_ID
                ][
                    "delta_antipodal_deg"
                ]
            ),
        },
        X1_ID: {
            "epsilon_power": float(
                context[
                    X1_ID
                ][
                    "epsilon_power"
                ]
            ),
            "delta_R_px": float(
                context[
                    X1_ID
                ][
                    "delta_R_px"
                ]
            ),
            "delta_antipodal_deg": float(
                context[
                    X1_ID
                ][
                    "delta_antipodal_deg"
                ]
            ),
        },
    }


def verify_dependencies() -> dict[str, Any]:
    """Verify frozen inputs without computing any new intersection."""
    if not PROTOCOL_PATH.exists():
        raise RuntimeError(
            f"Missing protocol: {PROTOCOL_PATH}"
        )

    verify_sha256_manifest(
        PLANE_SEAL,
        (
            PLANE_JSON,
        ),
    )

    verify_sha256_manifest(
        LINEAR_SEAL,
        (
            LINEAR_JSON,
        ),
    )

    verify_sha256_manifest(
        EXPANDED_SEAL,
        (
            EXPANDED_JSON,
        ),
    )

    plane_result = (
        load_json(
            PLANE_JSON
        )
    )

    linear_result = (
        load_json(
            LINEAR_JSON
        )
    )

    expanded = (
        load_json(
            EXPANDED_JSON
        )
    )

    if (
        plane_result.get(
            "analysis_class"
        )
        != EXPECTED_PLANE_CLASS
    ):
        raise RuntimeError(
            "Unexpected stereographic plane analysis class."
        )

    if (
        linear_result.get(
            "analysis_class"
        )
        != EXPECTED_LINEAR_CLASS
    ):
        raise RuntimeError(
            "Unexpected linear reconstruction analysis class."
        )

    expected_planes = {
        Y0_ID,
        Y1_ID,
        YAXIS_ID,
        X1_ID,
    }

    if (
        set(
            plane_result[
                "reconstructed_planes"
            ]
        )
        != expected_planes
    ):
        raise RuntimeError(
            "Frozen reconstructed-plane set changed."
        )

    # Verify linear checkpoint is downstream of exactly this plane result.
    current_plane_sha = (
        sha256_path(
            PLANE_JSON
        )
    )

    parent_plane_sha = (
        linear_result[
            "provenance"
        ][
            "plane_angle_sha256"
        ]
    )

    if (
        current_plane_sha
        != parent_plane_sha
    ):
        raise RuntimeError(
            "Linear reconstruction does not point to the "
            "currently sealed plane-angle result."
        )

    node = (
        find_lower_right_node(
            expanded
        )
    )

    limb = (
        verify_limb_agreement(
            plane_result,
            expanded,
        )
    )

    validation = (
        linear_result[
            "independent_zero_line_validation"
        ]
    )

    return {
        "plane_result": (
            plane_result
        ),
        "linear_result": (
            linear_result
        ),
        "expanded": (
            expanded
        ),
        "lower_right_node": (
            node
        ),
        "limb": (
            limb
        ),
        "prior_eta_x_deg": float(
            validation[
                "eta_x_deg"
            ]
        ),
        "prior_eta_y_deg": float(
            validation[
                "eta_y_deg"
            ]
        ),
        "protocol_sha256": (
            sha256_path(
                PROTOCOL_PATH
            )
        ),
        "plane_sha256": (
            current_plane_sha
        ),
        "linear_sha256": (
            sha256_path(
                LINEAR_JSON
            )
        ),
        "expanded_sha256": (
            sha256_path(
                EXPANDED_JSON
            )
        ),
    }


def build_analysis() -> dict[str, Any]:
    dependencies = (
        verify_dependencies()
    )

    plane_result = (
        dependencies[
            "plane_result"
        ]
    )

    y_family = (
        intersection_diagnostic(
            plane_normal(
                plane_result,
                Y0_ID,
            ),
            plane_normal(
                plane_result,
                Y1_ID,
            ),
        )
    )

    x_family = (
        intersection_diagnostic(
            plane_normal(
                plane_result,
                YAXIS_ID,
            ),
            plane_normal(
                plane_result,
                X1_ID,
            ),
        )
    )

    y_node = (
        y_family_node_comparison(
            y_family,
            dependencies[
                "lower_right_node"
            ],
            dependencies[
                "limb"
            ],
        )
    )

    y_family[
        "family"
    ] = "y"

    y_family[
        "zero_curve_id"
    ] = Y0_ID

    y_family[
        "offset_curve_id"
    ] = Y1_ID

    y_family[
        "source_landmark_validation"
    ] = y_node

    x_family[
        "family"
    ] = "x"

    x_family[
        "zero_curve_id"
    ] = YAXIS_ID

    x_family[
        "offset_curve_id"
    ] = X1_ID

    x_family[
        "source_landmark_validation"
    ] = None

    return {
        "checkpoint": (
            "first_hand_parallel_family_"
            "equatorial_incidence_v0.8"
        ),
        "analysis_class": (
            "post_hoc_parallel_family_"
            "equatorial_incidence_diagnostic"
        ),
        "analysis_status": (
            "deterministic_post_hoc_structural_diagnostic"
        ),
        "provenance": {
            "protocol_path": str(
                PROTOCOL_PATH.relative_to(
                    ROOT
                )
            ),
            "protocol_sha256": (
                dependencies[
                    "protocol_sha256"
                ]
            ),
            "plane_result": str(
                PLANE_JSON.relative_to(
                    ROOT
                )
            ),
            "plane_sha256": (
                dependencies[
                    "plane_sha256"
                ]
            ),
            "linear_result": str(
                LINEAR_JSON.relative_to(
                    ROOT
                )
            ),
            "linear_sha256": (
                dependencies[
                    "linear_sha256"
                ]
            ),
            "expanded_neutral_result": str(
                EXPANDED_JSON.relative_to(
                    ROOT
                )
            ),
            "expanded_neutral_sha256": (
                dependencies[
                    "expanded_sha256"
                ]
            ),
            "frozen_limb_reference": (
                dependencies[
                    "limb"
                ]
            ),
        },
        "model_condition": {
            "statement": (
                "An affine-parallel pair under the tested "
                "equator-preserving central-projective model "
                "must have a great-circle intersection direction "
                "with z=0."
            ),
            "required_exact_absolute_z": 0.0,
            "required_exact_epsilon_equator_deg": 0.0,
            "post_hoc_pass_threshold_added": False,
        },
        "families": {
            "y_family": (
                y_family
            ),
            "x_family": (
                x_family
            ),
        },
        "prior_related_diagnostic": {
            "eta_y_deg": (
                dependencies[
                    "prior_eta_y_deg"
                ]
            ),
            "eta_x_deg": (
                dependencies[
                    "prior_eta_x_deg"
                ]
            ),
            "independent_statistical_evidence_claimed": False,
        },
        "rendering_closure_context": (
            rendering_context(
                plane_result
            )
        ),
        "scope": {
            "curve_refits": 0,
            "circle_refits": 0,
            "line_refits": 0,
            "optimizer_calls": 0,
            "stereographic_refit": False,
            "linear_map_refit": False,
            "general_3x3_projective_fit": False,
            "x_family_rim_node_selected": False,
            "x1_reclassified_as_scaffold": False,
            "construction_scale_selected": False,
            "reciprocal_spiral_projection_computed": False,
            "s1_computed": False,
            "s1_5_computed": False,
            "s2_computed": False,
        },
        "interpretation_boundary": (
            "The equatorial-incidence calculation is an algebraic "
            "restatement of the same affine-parallel condition tested "
            "directionally by the prior eta diagnostic and is therefore "
            "not counted as independent statistical evidence. The "
            "y-family comparison with the independently frozen lower-right "
            "rim landmark is a separate source-landmark consistency check. "
            "No x-family rim landmark is selected retrospectively."
        ),
    }


def render_report(
    analysis: dict[str, Any],
) -> str:
    y = (
        analysis[
            "families"
        ][
            "y_family"
        ]
    )

    x = (
        analysis[
            "families"
        ][
            "x_family"
        ]
    )

    node = (
        y[
            "source_landmark_validation"
        ]
    )

    prior = (
        analysis[
            "prior_related_diagnostic"
        ]
    )

    closure = (
        analysis[
            "rendering_closure_context"
        ]
    )

    lines = [
        "# First Hand parallel-family equatorial-incidence diagnostic",
        "",
        "**Status:** deterministic post-hoc structural diagnostic",
        "",
        "No curve, circle, line, rendering map, or projective map was refitted.",
        "",
        "## Exact model condition",
        "",
        "For an affine-parallel pair under the tested equator-preserving "
        "central-projective model, the two spherical great-circle planes "
        "must intersect in the equatorial plane:",
        "",
        "```text",
        "z_intersection = 0",
        "```",
        "",
        "No post-hoc PASS/FAIL threshold is introduced.",
        "",
        "## y-family: Y0 and Y1",
        "",
        f"- |s_z|: `{y['absolute_z']:.12f}`",
        f"- equatorial departure: `{y['epsilon_equator_deg']:.9f} deg`",
        (
            "- horizontal azimuth pair: "
            f"`{y['horizontal_azimuth_canonical_deg']:.9f} deg`, "
            f"`{y['horizontal_azimuth_antipode_deg']:.9f} deg`"
        ),
        "",
        "### Frozen lower-right infinity landmark",
        "",
        (
            "- frozen node bearing: "
            f"`{node['frozen_node_bearing_deg']:.9f} deg`"
        ),
        (
            "- nearest predicted antipodal direction: "
            f"`{node['selected_predicted_azimuth_deg']:.9f} deg`"
        ),
        (
            "- angular node separation: "
            f"`{node['delta_node_deg']:.9f} deg`"
        ),
        (
            "- page-space node separation: "
            f"`{node['delta_node_px']:.6f} px`"
        ),
        (
            "- frozen node radial residual from limb: "
            f"`{node['frozen_node_radial_residual_from_limb_circle_px']:.6f} px`"
        ),
        "",
        "The lower-right node was registered before this diagnostic as the "
        "visible common y=0/y=1 projective-infinity point.",
        "",
        "## x-family: YAXIS and X1",
        "",
        f"- |s_z|: `{x['absolute_z']:.12f}`",
        f"- equatorial departure: `{x['epsilon_equator_deg']:.9f} deg`",
        (
            "- horizontal-projection azimuth pair: "
            f"`{x['horizontal_azimuth_canonical_deg']:.9f} deg`, "
            f"`{x['horizontal_azimuth_antipode_deg']:.9f} deg`"
        ),
        "",
        "Because this intersection is not assumed equatorial, the reported "
        "azimuth is only the azimuth of its horizontal projection.",
        "",
        "No rim node is assigned to the x-family.",
        "",
        "## Relation to prior eta diagnostic",
        "",
        f"- prior eta_y: `{prior['eta_y_deg']:.9f} deg`",
        f"- prior eta_x: `{prior['eta_x_deg']:.9f} deg`",
        "",
        "These are mathematically related expressions of the same "
        "parallel-family constraint and are not treated as independent "
        "statistical evidence.",
        "",
        "## Frozen stereographic rendering context",
        "",
        f"- Y1 epsilon_power: `{closure[Y1_ID]['epsilon_power']:.9f}`",
        f"- Y1 Delta_R: `{closure[Y1_ID]['delta_R_px']:.6f} px`",
        (
            "- Y1 Delta_antipodal: "
            f"`{closure[Y1_ID]['delta_antipodal_deg']:.6f} deg`"
        ),
        f"- X1 epsilon_power: `{closure[X1_ID]['epsilon_power']:.9f}`",
        f"- X1 Delta_R: `{closure[X1_ID]['delta_R_px']:.6f} px`",
        (
            "- X1 Delta_antipodal: "
            f"`{closure[X1_ID]['delta_antipodal_deg']:.6f} deg`"
        ),
        "",
        "Rendering closure and affine-parallel directional closure remain "
        "separate diagnostics.",
        "",
        "## Interpretation boundary",
        "",
        "This checkpoint does not reclassify X1, fit a more flexible "
        "projective map, select a construction scale, or compute the "
        "reciprocal spiral or self-embedment metrics.",
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
            "First Hand parallel-family "
            "equatorial-incidence diagnostic."
        )
    )

    parser.add_argument(
        "--check-inputs",
        action="store_true",
        help=(
            "Verify frozen dependencies without computing "
            "any great-circle intersection."
        ),
    )

    args = parser.parse_args()

    if args.check_inputs:
        dependencies = (
            verify_dependencies()
        )

        node = (
            dependencies[
                "lower_right_node"
            ]
        )

        print(
            "Stereographic plane-angle result: VERIFIED"
        )

        print(
            "Linear central-projective result: VERIFIED"
        )

        print(
            "Expanded neutral census: VERIFIED"
        )

        print(
            "Equatorial-incidence protocol: PRESENT"
        )

        print(
            "Frozen lower-right node:",
            LR_NODE_ID,
        )

        print(
            "Frozen lower-right bearing:",
            f"{float(node['bearing_deg']):.9f} deg",
        )

        print(
            "y-family source-landmark comparison: ENABLED"
        )

        print(
            "x-family rim-node comparison: DISABLED"
        )

        print(
            "No great-circle intersection was computed."
        )

        return 0

    analysis = (
        build_analysis()
    )

    write_outputs(
        analysis
    )

    y = (
        analysis[
            "families"
        ][
            "y_family"
        ]
    )

    x = (
        analysis[
            "families"
        ][
            "x_family"
        ]
    )

    node = (
        y[
            "source_landmark_validation"
        ]
    )

    print(
        "=" * 96
    )

    print(
        "FIRST HAND PARALLEL-FAMILY "
        "EQUATORIAL-INCIDENCE DIAGNOSTIC"
    )

    print(
        "=" * 96
    )

    print(
        "y-family (Y0, Y1)"
    )

    print(
        "  |s_z|:",
        f"{y['absolute_z']:.12f}",
    )

    print(
        "  equatorial departure:",
        f"{y['epsilon_equator_deg']:.9f} deg",
    )

    print(
        "  azimuth pair:",
        f"{y['horizontal_azimuth_canonical_deg']:.9f} deg,",
        f"{y['horizontal_azimuth_antipode_deg']:.9f} deg",
    )

    print(
        "  frozen LR-node bearing:",
        f"{node['frozen_node_bearing_deg']:.9f} deg",
    )

    print(
        "  nearest predicted azimuth:",
        f"{node['selected_predicted_azimuth_deg']:.9f} deg",
    )

    print(
        "  node angular separation:",
        f"{node['delta_node_deg']:.9f} deg",
    )

    print(
        "  node page-space separation:",
        f"{node['delta_node_px']:.6f} px",
    )

    print(
        "-" * 96
    )

    print(
        "x-family (YAXIS, X1)"
    )

    print(
        "  |s_z|:",
        f"{x['absolute_z']:.12f}",
    )

    print(
        "  equatorial departure:",
        f"{x['epsilon_equator_deg']:.9f} deg",
    )

    print(
        "  horizontal-projection azimuth pair:",
        f"{x['horizontal_azimuth_canonical_deg']:.9f} deg,",
        f"{x['horizontal_azimuth_antipode_deg']:.9f} deg",
    )

    print(
        "-" * 96
    )

    prior = (
        analysis[
            "prior_related_diagnostic"
        ]
    )

    print(
        "prior eta_y:",
        f"{prior['eta_y_deg']:.9f} deg",
    )

    print(
        "prior eta_x:",
        f"{prior['eta_x_deg']:.9f} deg",
    )

    print(
        f"Wrote {OUTPUT_JSON}"
    )

    print(
        f"Wrote {OUTPUT_REPORT}"
    )

    print(
        "No x-family rim node was selected."
    )

    print(
        "No refit, construction-scale selection, spiral projection, "
        "or self-embedment score was computed."
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
