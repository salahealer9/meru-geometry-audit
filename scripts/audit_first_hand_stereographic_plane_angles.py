#!/usr/bin/env python3
"""Stereographic spherical-plane reconstruction for First Hand page 7.

This checkpoint reconstructs spherical great-circle plane normals from
already-frozen page-space line/circle geometry under the already-tested
stereographic rendering hypothesis.

No curve is refitted.
No optimizer is called.
The scaffold holdout does not enter scale reconstruction.
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
    / "first_hand_stereographic_plane_angle_protocol.md"
)

MORPHOLOGY_JSON = (
    QC_DIR
    / "first_hand_curve_morphology_census.json"
)

MORPHOLOGY_SEAL = (
    QC_DIR
    / "first_hand_curve_morphology_census.sha256"
)

RENDERING_JSON = (
    QC_DIR
    / "first_hand_spherical_rendering_comparator.json"
)

RENDERING_SEAL = (
    QC_DIR
    / "first_hand_spherical_rendering_comparator.sha256"
)

SPHERICAL_MAP_JSON = (
    DATA_DIR
    / "spherical_map_family_audit.json"
)

OUTPUT_JSON = (
    QC_DIR
    / "first_hand_stereographic_plane_angles.json"
)

OUTPUT_REPORT = (
    ROOT
    / "reports"
    / "first_hand_stereographic_plane_angles.md"
)


Y0_ID = "AOG-LM-P07-GC-Y0"
Y1_ID = "AOG-LM-P07-GC-Y1"
YAXIS_ID = "AOG-LM-P07-GC-YAXIS"
X1_ID = "AOG-LM-P07-GC-X1"

HOLDOUT_ID = (
    "AOG-LM-P07-GC-SCAFFOLD-UR-UC-X1LL-LL"
)

LINE_IDS = (
    Y0_ID,
    YAXIS_ID,
)

CIRCLE_IDS = (
    Y1_ID,
    X1_ID,
)

LABELLED_IDS = (
    Y0_ID,
    Y1_ID,
    YAXIS_ID,
    X1_ID,
)

EXPECTED_MORPHOLOGY_CLASS = (
    "post_hoc_model_neutral_morphology_census"
)

EXPECTED_RENDERING_CLASS = (
    "preregistered_parameter_free_"
    "spherical_rendering_comparator"
)

SCALE_IDS = (
    "G30",
    "GHALF",
    "GUNIT",
    "GONE",
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


def canonical_json_sha256(
    value: Any,
) -> str:
    payload = json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")

    return hashlib.sha256(
        payload
    ).hexdigest()


def verify_sha256_manifest(
    manifest_path: Path,
    required_paths: tuple[Path, ...],
) -> dict[str, str]:
    """Verify a sha256sum-style manifest and required entries."""
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

        relative = (
            parts[-1]
            .lstrip("*")
        )

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


def unit(
    vector: np.ndarray,
) -> np.ndarray:
    vector = np.asarray(
        vector,
        dtype=np.float64,
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
            "Cannot normalize invalid vector."
        )

    return (
        vector
        / norm
    )


def verify_scale_registry(
    spherical_map: dict[str, Any],
) -> dict[str, Any]:
    """Verify the four already-frozen construction-scale candidates."""
    hypotheses = (
        spherical_map[
            "canonical_family"
        ][
            "scale_hypotheses"
        ]
    )

    if set(
        hypotheses
    ) != set(
        SCALE_IDS
    ):
        raise RuntimeError(
            "Frozen spherical-map scale registry changed."
        )

    expected_angles = {
        "G30": (
            math.radians(
                30.0
            )
        ),
        "GHALF": 0.5,
        "GUNIT": (
            math.pi
            / 4.0
        ),
        "GONE": 1.0,
    }

    result: dict[
        str,
        Any,
    ] = {}

    for scale_id in SCALE_IDS:
        item = (
            hypotheses[
                scale_id
            ]
        )

        angle = float(
            item[
                "unit_radius_central_angle_radians"
            ]
        )

        scale = float(
            item[
                "scale"
            ]
        )

        expected_angle = (
            expected_angles[
                scale_id
            ]
        )

        expected_scale = (
            math.tan(
                expected_angle
            )
        )

        if not math.isclose(
            angle,
            expected_angle,
            rel_tol=0.0,
            abs_tol=1.0e-14,
        ):
            raise RuntimeError(
                f"{scale_id} angle changed."
            )

        if not math.isclose(
            scale,
            expected_scale,
            rel_tol=0.0,
            abs_tol=1.0e-14,
        ):
            raise RuntimeError(
                f"{scale_id} scale changed."
            )

        result[
            scale_id
        ] = {
            "scale_k": scale,
            "predicted_delta_radians": (
                angle
            ),
            "predicted_delta_degrees": (
                math.degrees(
                    angle
                )
            ),
            "source_role": (
                item.get(
                    "source_role"
                )
            ),
        }

    return result


def verify_dependencies() -> dict[str, Any]:
    """Verify every frozen parent dependency."""
    if not PROTOCOL_PATH.exists():
        raise RuntimeError(
            f"Missing protocol: {PROTOCOL_PATH}"
        )

    verify_sha256_manifest(
        MORPHOLOGY_SEAL,
        (
            MORPHOLOGY_JSON,
        ),
    )

    verify_sha256_manifest(
        RENDERING_SEAL,
        (
            RENDERING_JSON,
        ),
    )

    morphology = (
        load_json(
            MORPHOLOGY_JSON
        )
    )

    rendering = (
        load_json(
            RENDERING_JSON
        )
    )

    spherical_map = (
        load_json(
            SPHERICAL_MAP_JSON
        )
    )

    if (
        morphology.get(
            "analysis_class"
        )
        != EXPECTED_MORPHOLOGY_CLASS
    ):
        raise RuntimeError(
            "Unexpected morphology analysis class."
        )

    if (
        rendering.get(
            "analysis_class"
        )
        != EXPECTED_RENDERING_CLASS
    ):
        raise RuntimeError(
            "Unexpected rendering-comparator class."
        )

    if (
        set(
            morphology[
                "curves"
            ]
        )
        != {
            *LABELLED_IDS,
            HOLDOUT_ID,
        }
    ):
        raise RuntimeError(
            "Frozen morphology curve set changed."
        )

    branch_allocation = (
        rendering[
            "branch_allocation"
        ]
    )

    if (
        tuple(
            branch_allocation[
                "line_branch"
            ]
        )
        != LINE_IDS
    ):
        raise RuntimeError(
            "Frozen line-branch allocation changed."
        )

    if (
        tuple(
            branch_allocation[
                "curved_labelled_circle_branch"
            ]
        )
        != CIRCLE_IDS
    ):
        raise RuntimeError(
            "Frozen circle-branch allocation changed."
        )

    if (
        branch_allocation[
            "curved_holdout_circle_branch"
        ]
        != HOLDOUT_ID
    ):
        raise RuntimeError(
            "Frozen holdout identity changed."
        )

    if (
        rendering[
            "holdout"
        ][
            "used_for_calibration"
        ]
        is not False
    ):
        raise RuntimeError(
            "Scaffold was unexpectedly used for calibration."
        )

    # Verify that the labelled comparator block still matches
    # the fingerprint taken before the holdout was evaluated.
    labelled_hash = (
        canonical_json_sha256(
            rendering[
                "labelled_curves"
            ]
        )
    )

    expected_labelled_hash = (
        rendering[
            "provenance"
        ][
            "labelled_result_block_sha256_before_holdout"
        ]
    )

    if (
        labelled_hash
        != expected_labelled_hash
    ):
        raise RuntimeError(
            "Labelled rendering-comparator block "
            "no longer matches its pre-holdout fingerprint."
        )

    morphology_limb = (
        morphology[
            "frozen_limb_reference"
        ]
    )

    rendering_limb = (
        rendering[
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
                morphology_limb[
                    key
                ]
            ),
            float(
                rendering_limb[
                    key
                ]
            ),
            rel_tol=0.0,
            abs_tol=1.0e-12,
        ):
            raise RuntimeError(
                "Frozen limb disagreement "
                f"for {key}."
            )

    scales = (
        verify_scale_registry(
            spherical_map
        )
    )

    return {
        "morphology": morphology,
        "rendering": rendering,
        "spherical_map": spherical_map,
        "scales": scales,
        "limb": morphology_limb,
        "protocol_sha256": (
            sha256_path(
                PROTOCOL_PATH
            )
        ),
        "morphology_sha256": (
            sha256_path(
                MORPHOLOGY_JSON
            )
        ),
        "rendering_sha256": (
            sha256_path(
                RENDERING_JSON
            )
        ),
        "spherical_map_sha256": (
            sha256_path(
                SPHERICAL_MAP_JSON
            )
        ),
    }


def normalized_circle_center(
    circle: dict[str, Any],
    limb: dict[str, Any],
) -> np.ndarray:
    """Frozen circle centre in normalized y-up stereographic coordinates."""
    radius = float(
        limb[
            "radius_px"
        ]
    )

    if not (
        math.isfinite(radius)
        and radius > 0.0
    ):
        raise ValueError(
            "Invalid frozen limb radius."
        )

    u = (
        float(
            circle[
                "center_x_px"
            ]
        )
        - float(
            limb[
                "center_x_px"
            ]
        )
    ) / radius

    # Prepared-crop y is downward; mathematical v is upward.
    v = -(
        float(
            circle[
                "center_y_px"
            ]
        )
        - float(
            limb[
                "center_y_px"
            ]
        )
    ) / radius

    return np.asarray(
        [
            u,
            v,
        ],
        dtype=np.float64,
    )


def finite_circle_plane_normal(
    circle: dict[str, Any],
    limb: dict[str, Any],
) -> dict[str, Any]:
    """Recover an unoriented great-circle plane normal from circle centre."""
    centre = (
        normalized_circle_center(
            circle,
            limb,
        )
    )

    raw = np.asarray(
        [
            -float(
                centre[0]
            ),
            -float(
                centre[1]
            ),
            1.0,
        ],
        dtype=np.float64,
    )

    normal = unit(
        raw
    )

    return {
        "branch": (
            "stereographic_finite_circle"
        ),
        "normalized_circle_center_u": float(
            centre[0]
        ),
        "normalized_circle_center_v": float(
            centre[1]
        ),
        "circle_radius_used_for_plane_normal": False,
        "raw_plane_normal": [
            float(value)
            for value
            in raw
        ],
        "unit_plane_normal": [
            float(value)
            for value
            in normal
        ],
        "plane_normal_unoriented": True,
    }


def line_plane_normal(
    line: dict[str, Any],
) -> dict[str, Any]:
    """Recover an unoriented nz=0 plane normal from frozen line direction."""
    dx_image = float(
        line[
            "direction_x"
        ]
    )

    dy_image = float(
        line[
            "direction_y"
        ]
    )

    # Image x is rightward and image y is downward.
    # Convert displacement vector to mathematical y-up coordinates.
    direction_y_up = unit(
        np.asarray(
            [
                dx_image,
                -dy_image,
            ],
            dtype=np.float64,
        )
    )

    page_normal = np.asarray(
        [
            -float(
                direction_y_up[
                    1
                ]
            ),
            float(
                direction_y_up[
                    0
                ]
            ),
        ],
        dtype=np.float64,
    )

    raw = np.asarray(
        [
            float(
                page_normal[0]
            ),
            float(
                page_normal[1]
            ),
            0.0,
        ],
        dtype=np.float64,
    )

    normal = unit(
        raw
    )

    return {
        "branch": (
            "stereographic_diameter_line"
        ),
        "image_direction_x": (
            dx_image
        ),
        "image_direction_y": (
            dy_image
        ),
        "mathematical_direction_u": float(
            direction_y_up[
                0
            ]
        ),
        "mathematical_direction_v": float(
            direction_y_up[
                1
            ]
        ),
        "line_offset_used_for_plane_normal": False,
        "raw_plane_normal": [
            float(value)
            for value
            in raw
        ],
        "unit_plane_normal": [
            float(value)
            for value
            in normal
        ],
        "plane_normal_unoriented": True,
    }


def unoriented_plane_angle_deg(
    normal_a: np.ndarray,
    normal_b: np.ndarray,
) -> float:
    """Unoriented angle between origin planes, in [0, 90] degrees."""
    a = unit(
        normal_a
    )

    b = unit(
        normal_b
    )

    cosine = float(
        np.clip(
            abs(
                np.dot(
                    a,
                    b,
                )
            ),
            0.0,
            1.0,
        )
    )

    return math.degrees(
        math.acos(
            cosine
        )
    )


def normal_array(
    reconstruction: dict[str, Any],
) -> np.ndarray:
    return np.asarray(
        reconstruction[
            "unit_plane_normal"
        ],
        dtype=np.float64,
    )


def k_from_delta_deg(
    delta_deg: float,
) -> float | None:
    """Return tan(delta) unless the angle is numerically at 90 degrees."""
    radians = math.radians(
        delta_deg
    )

    cosine = math.cos(
        radians
    )

    if abs(
        cosine
    ) <= 1.0e-14:
        return None

    return math.tan(
        radians
    )


def scale_candidate_comparison(
    delta_x_deg: float,
    delta_y_deg: float,
    scales: dict[str, Any],
) -> dict[str, Any]:
    """Compare frozen image-derived angles with frozen source candidates."""
    result: dict[
        str,
        Any,
    ] = {}

    for scale_id in SCALE_IDS:
        candidate = (
            scales[
                scale_id
            ]
        )

        predicted = float(
            candidate[
                "predicted_delta_degrees"
            ]
        )

        residual_x = (
            delta_x_deg
            - predicted
        )

        residual_y = (
            delta_y_deg
            - predicted
        )

        rms = math.sqrt(
            0.5
            * (
                residual_x
                * residual_x
                + residual_y
                * residual_y
            )
        )

        result[
            scale_id
        ] = {
            **candidate,
            "delta_x_minus_candidate_deg": (
                residual_x
            ),
            "delta_y_minus_candidate_deg": (
                residual_y
            ),
            "two_axis_angular_rms_deg": (
                rms
            ),
            "candidate_reoptimized": False,
        }

    return result


def reconstruct_planes(
    morphology: dict[str, Any],
    limb: dict[str, Any],
) -> dict[str, Any]:
    """Recover all four labelled spherical planes."""
    result: dict[
        str,
        Any,
    ] = {}

    for curve_id in LINE_IDS:
        result[
            curve_id
        ] = (
            line_plane_normal(
                morphology[
                    "curves"
                ][
                    curve_id
                ][
                    "line"
                ]
            )
        )

    for curve_id in CIRCLE_IDS:
        result[
            curve_id
        ] = (
            finite_circle_plane_normal(
                morphology[
                    "curves"
                ][
                    curve_id
                ][
                    "circle"
                ],
                limb,
            )
        )

    return result


def rendering_closure_context(
    rendering: dict[str, Any],
) -> dict[str, Any]:
    """Carry forward the already-frozen stereographic closure context."""
    labelled = (
        rendering[
            "labelled_curves"
        ]
    )

    return {
        Y0_ID: {
            "branch": "line",
            "line_to_frozen_sphere_center_px": float(
                labelled[
                    Y0_ID
                ][
                    "line_to_frozen_sphere_center_px"
                ]
            ),
            "line_to_frozen_sphere_center_over_R": float(
                labelled[
                    Y0_ID
                ][
                    "line_to_frozen_sphere_center_over_R"
                ]
            ),
        },
        YAXIS_ID: {
            "branch": "line",
            "line_to_frozen_sphere_center_px": float(
                labelled[
                    YAXIS_ID
                ][
                    "line_to_frozen_sphere_center_px"
                ]
            ),
            "line_to_frozen_sphere_center_over_R": float(
                labelled[
                    YAXIS_ID
                ][
                    "line_to_frozen_sphere_center_over_R"
                ]
            ),
        },
        Y1_ID: {
            "branch": "circle",
            "epsilon_power": float(
                labelled[
                    Y1_ID
                ][
                    "epsilon_power"
                ]
            ),
            "delta_R_px": (
                labelled[
                    Y1_ID
                ][
                    "delta_R_px"
                ]
            ),
            "delta_antipodal_deg": (
                labelled[
                    Y1_ID
                ][
                    "delta_antipodal_deg"
                ]
            ),
        },
        X1_ID: {
            "branch": "circle",
            "epsilon_power": float(
                labelled[
                    X1_ID
                ][
                    "epsilon_power"
                ]
            ),
            "delta_R_px": (
                labelled[
                    X1_ID
                ][
                    "delta_R_px"
                ]
            ),
            "delta_antipodal_deg": (
                labelled[
                    X1_ID
                ][
                    "delta_antipodal_deg"
                ]
            ),
        },
        "scaffold_holdout": {
            "curve_id": (
                HOLDOUT_ID
            ),
            "used_for_plane_angle_reconstruction": False,
            "epsilon_power": (
                rendering[
                    "holdout"
                ][
                    "result"
                ][
                    "epsilon_power"
                ]
            ),
            "delta_R_px": (
                rendering[
                    "holdout"
                ][
                    "result"
                ][
                    "delta_R_px"
                ]
            ),
            "delta_antipodal_deg": (
                rendering[
                    "holdout"
                ][
                    "result"
                ][
                    "delta_antipodal_deg"
                ]
            ),
        },
    }


def build_analysis() -> dict[str, Any]:
    dependencies = (
        verify_dependencies()
    )

    morphology = (
        dependencies[
            "morphology"
        ]
    )

    rendering = (
        dependencies[
            "rendering"
        ]
    )

    limb = (
        dependencies[
            "limb"
        ]
    )

    planes = (
        reconstruct_planes(
            morphology,
            limb,
        )
    )

    # Freeze the four reconstructed planes in memory before
    # calculating either coordinate separation.
    plane_block_sha256 = (
        canonical_json_sha256(
            planes
        )
    )

    delta_x = (
        unoriented_plane_angle_deg(
            normal_array(
                planes[
                    YAXIS_ID
                ]
            ),
            normal_array(
                planes[
                    X1_ID
                ]
            ),
        )
    )

    delta_y = (
        unoriented_plane_angle_deg(
            normal_array(
                planes[
                    Y0_ID
                ]
            ),
            normal_array(
                planes[
                    Y1_ID
                ]
            ),
        )
    )

    k_x = (
        k_from_delta_deg(
            delta_x
        )
    )

    k_y = (
        k_from_delta_deg(
            delta_y
        )
    )

    k_ratio = None

    if (
        k_x is not None
        and k_y is not None
        and abs(
            k_y
        ) > 1.0e-15
    ):
        k_ratio = (
            k_x
            / k_y
        )

    derived = {
        "delta_x_deg": (
            delta_x
        ),
        "delta_y_deg": (
            delta_y
        ),
        "delta_x_rad": (
            math.radians(
                delta_x
            )
        ),
        "delta_y_rad": (
            math.radians(
                delta_y
            )
        ),
        "delta_difference_deg": (
            delta_x
            - delta_y
        ),
        "absolute_delta_difference_deg": abs(
            delta_x
            - delta_y
        ),
        "k_x_tan_delta_x": (
            k_x
        ),
        "k_y_tan_delta_y": (
            k_y
        ),
        "k_x_over_k_y": (
            k_ratio
        ),
        "isotropy_equality_imposed": False,
        "single_k_selected": False,
    }

    # Scale candidates are consulted only after both
    # independently reconstructed angles exist.
    scale_comparison = (
        scale_candidate_comparison(
            delta_x,
            delta_y,
            dependencies[
                "scales"
            ],
        )
    )

    return {
        "checkpoint": (
            "first_hand_stereographic_"
            "plane_angle_reconstruction_v0.8"
        ),
        "analysis_class": (
            "preregistered_stereographic_"
            "plane_angle_reconstruction"
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
            "morphology_result": str(
                MORPHOLOGY_JSON.relative_to(
                    ROOT
                )
            ),
            "morphology_sha256": (
                dependencies[
                    "morphology_sha256"
                ]
            ),
            "rendering_comparator_result": str(
                RENDERING_JSON.relative_to(
                    ROOT
                )
            ),
            "rendering_comparator_sha256": (
                dependencies[
                    "rendering_sha256"
                ]
            ),
            "spherical_map_family_result": str(
                SPHERICAL_MAP_JSON.relative_to(
                    ROOT
                )
            ),
            "spherical_map_family_sha256": (
                dependencies[
                    "spherical_map_sha256"
                ]
            ),
            "frozen_limb_reference": (
                limb
            ),
            "reconstructed_plane_block_sha256_before_angles": (
                plane_block_sha256
            ),
        },
        "fit_partition": {
            "labelled_plane_reconstruction": list(
                LABELLED_IDS
            ),
            "scaffold_holdout": (
                HOLDOUT_ID
            ),
            "scaffold_used_for_plane_reconstruction": False,
            "scaffold_used_for_scale_comparison": False,
        },
        "method": {
            "curve_refits": 0,
            "optimizer_calls": 0,
            "line_normal_rule": (
                "convert frozen line direction to y-up; "
                "n=(-dv,du,0)"
            ),
            "circle_normal_rule": (
                "normalize frozen circle-centre displacement; "
                "n=(-cu,-cv,1)"
            ),
            "circle_radius_used_for_plane_normal": False,
            "line_offset_used_for_plane_normal": False,
            "plane_angle_rule": (
                "acos(abs(n1 dot n2))"
            ),
            "isotropic_equality_imposed": False,
        },
        "reconstructed_planes": (
            planes
        ),
        "image_derived_coordinate_separations": (
            derived
        ),
        "fixed_scale_comparison": (
            scale_comparison
        ),
        "rendering_closure_context": (
            rendering_closure_context(
                rendering
            )
        ),
        "scope": {
            "stereographic_plane_angles_computed": True,
            "new_curve_fit_computed": False,
            "new_rendering_fit_computed": False,
            "single_construction_scale_selected": False,
            "general_projective_gauge_selected": False,
            "scaffold_plane_identity_assigned": False,
            "reciprocal_spiral_projection_computed": False,
            "s1_computed": False,
            "s1_5_computed": False,
            "s2_computed": False,
        },
        "interpretation_boundary": (
            "The reported spherical plane angles are algebraic "
            "reconstructions under the stereographic page-rendering "
            "hypothesis using already-frozen line and circle geometry. "
            "They inherit the measured rendering misclosure, especially "
            "for GC-Y1. Agreement with a source-motivated scale is "
            "descriptive and does not prove the historical construction. "
            "No uncertainty interval or post-hoc equality threshold is "
            "introduced."
        ),
    }


def render_report(
    analysis: dict[str, Any],
) -> str:
    derived = (
        analysis[
            "image_derived_coordinate_separations"
        ]
    )

    lines = [
        "# First Hand stereographic spherical-plane reconstruction",
        "",
        "**Status:** preregistered algebraic plane-angle reconstruction",
        "",
        "No curve was refitted and no optimizer was called.",
        "",
        "## Reconstructed labelled planes",
        "",
        "| Curve | Branch | Unit plane normal |",
        "|---|---|---|",
    ]

    for curve_id in LABELLED_IDS:
        item = (
            analysis[
                "reconstructed_planes"
            ][
                curve_id
            ]
        )

        normal = (
            item[
                "unit_plane_normal"
            ]
        )

        lines.append(
            f"| `{curve_id}` | "
            f"{item['branch']} | "
            f"({normal[0]:.9f}, "
            f"{normal[1]:.9f}, "
            f"{normal[2]:.9f}) |"
        )

    lines += [
        "",
        "## Image-derived coordinate separations",
        "",
        f"- delta_x = `{derived['delta_x_deg']:.9f} deg`",
        f"- delta_y = `{derived['delta_y_deg']:.9f} deg`",
        (
            "- delta_x - delta_y = "
            f"`{derived['delta_difference_deg']:.9f} deg`"
        ),
        (
            "- |delta_x - delta_y| = "
            f"`{derived['absolute_delta_difference_deg']:.9f} deg`"
        ),
        (
            "- k_x = tan(delta_x) = "
            f"`{derived['k_x_tan_delta_x']:.12f}`"
            if derived[
                "k_x_tan_delta_x"
            ]
            is not None
            else "- k_x = `undefined`"
        ),
        (
            "- k_y = tan(delta_y) = "
            f"`{derived['k_y_tan_delta_y']:.12f}`"
            if derived[
                "k_y_tan_delta_y"
            ]
            is not None
            else "- k_y = `undefined`"
        ),
    ]

    if (
        derived[
            "k_x_over_k_y"
        ]
        is None
    ):
        lines.append(
            "- k_x / k_y = `undefined`"
        )
    else:
        lines.append(
            "- k_x / k_y = "
            f"`{derived['k_x_over_k_y']:.12f}`"
        )

    lines += [
        "",
        "No equality between delta_x and delta_y was imposed.",
        "",
        "## Frozen source-scale comparators",
        "",
        "| Candidate | Predicted delta deg | k | "
        "delta_x residual deg | delta_y residual deg | two-axis RMS deg |",
        "|---|---:|---:|---:|---:|---:|",
    ]

    for scale_id in SCALE_IDS:
        item = (
            analysis[
                "fixed_scale_comparison"
            ][
                scale_id
            ]
        )

        lines.append(
            f"| `{scale_id}` | "
            f"{item['predicted_delta_degrees']:.9f} | "
            f"{item['scale_k']:.12f} | "
            f"{item['delta_x_minus_candidate_deg']:.9f} | "
            f"{item['delta_y_minus_candidate_deg']:.9f} | "
            f"{item['two_axis_angular_rms_deg']:.9f} |"
        )

    closure = (
        analysis[
            "rendering_closure_context"
        ]
    )

    lines += [
        "",
        "## Rendering-closure context",
        "",
        (
            f"- Y0 line-centre miss: "
            f"`{closure[Y0_ID]['line_to_frozen_sphere_center_px']:.6f} px`"
        ),
        (
            f"- Y-axis line-centre miss: "
            f"`{closure[YAXIS_ID]['line_to_frozen_sphere_center_px']:.6f} px`"
        ),
        (
            f"- Y1 epsilon_power: "
            f"`{closure[Y1_ID]['epsilon_power']:.9f}`; "
            f"Delta_R = `{closure[Y1_ID]['delta_R_px']:.6f} px`"
        ),
        (
            f"- X1 epsilon_power: "
            f"`{closure[X1_ID]['epsilon_power']:.9f}`; "
            f"Delta_R = `{closure[X1_ID]['delta_R_px']:.6f} px`"
        ),
        "",
        "The Y1-derived spherical angle must be interpreted with its larger "
        "stereographic rendering misclosure in view.",
        "",
        "## Scaffold holdout",
        "",
        f"`{HOLDOUT_ID}` remains outside plane-angle and scale reconstruction.",
        "",
        (
            "Its previously frozen stereographic closure is retained only as "
            "independent rendering evidence."
        ),
        "",
        "## Scope boundary",
        "",
        "No single construction scale, general projective gauge, reciprocal "
        "spiral projection, S1, S1.5, or S2 is selected or computed.",
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
            "Preregistered First Hand stereographic "
            "spherical-plane reconstruction."
        )
    )

    parser.add_argument(
        "--check-inputs",
        action="store_true",
        help=(
            "Verify frozen dependencies without "
            "reconstructing any spherical plane angle."
        ),
    )

    args = parser.parse_args()

    if args.check_inputs:
        dependencies = (
            verify_dependencies()
        )

        print(
            "Neutral morphology result: VERIFIED"
        )

        print(
            "Stereographic rendering comparator: VERIFIED"
        )

        print(
            "Spherical-map scale registry: VERIFIED"
        )

        print(
            "Plane-angle protocol: PRESENT"
        )

        print(
            "Frozen limb radius:",
            f"{float(dependencies['limb']['radius_px']):.9f} px",
        )

        print(
            "Labelled plane reconstruction curves:",
            len(
                LABELLED_IDS
            ),
        )

        print(
            "Scaffold excluded from plane/scale reconstruction: YES"
        )

        print(
            "No spherical plane angle was computed."
        )

        return 0

    analysis = (
        build_analysis()
    )

    write_outputs(
        analysis
    )

    derived = (
        analysis[
            "image_derived_coordinate_separations"
        ]
    )

    print(
        "="
        * 96
    )

    print(
        "FIRST HAND STEREOGRAPHIC "
        "SPHERICAL-PLANE RECONSTRUCTION"
    )

    print(
        "="
        * 96
    )

    print(
        "delta_x (YAXIS vs X1):",
        f"{derived['delta_x_deg']:.9f} deg",
    )

    print(
        "delta_y (Y0 vs Y1):",
        f"{derived['delta_y_deg']:.9f} deg",
    )

    print(
        "|delta_x-delta_y|:",
        f"{derived['absolute_delta_difference_deg']:.9f} deg",
    )

    print(
        "k_x:",
        (
            "undefined"
            if derived[
                "k_x_tan_delta_x"
            ]
            is None
            else f"{derived['k_x_tan_delta_x']:.12f}"
        ),
    )

    print(
        "k_y:",
        (
            "undefined"
            if derived[
                "k_y_tan_delta_y"
            ]
            is None
            else f"{derived['k_y_tan_delta_y']:.12f}"
        ),
    )

    print(
        "-" * 96
    )

    for scale_id in SCALE_IDS:
        item = (
            analysis[
                "fixed_scale_comparison"
            ][
                scale_id
            ]
        )

        print(
            f"{scale_id}: "
            f"pred={item['predicted_delta_degrees']:.9f} deg, "
            f"dx-res={item['delta_x_minus_candidate_deg']:+.9f} deg, "
            f"dy-res={item['delta_y_minus_candidate_deg']:+.9f} deg, "
            f"RMS={item['two_axis_angular_rms_deg']:.9f} deg"
        )

    print(
        f"Wrote {OUTPUT_JSON}"
    )

    print(
        f"Wrote {OUTPUT_REPORT}"
    )

    print(
        "Scaffold holdout was not used."
    )

    print(
        "No single construction scale, spiral projection, "
        "or self-embedment score was computed."
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
