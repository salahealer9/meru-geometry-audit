#!/usr/bin/env python3
"""Parameter-free spherical-rendering comparator for First Hand page 7.

Uses only already-frozen image-space morphology and the frozen
orthographic great-circle result.

No curve is refitted.  No optimizer is called.
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
    / "first_hand_spherical_rendering_comparator_protocol.md"
)

MORPHOLOGY_JSON = (
    QC_DIR
    / "first_hand_curve_morphology_census.json"
)

MORPHOLOGY_SEAL = (
    QC_DIR
    / "first_hand_curve_morphology_census.sha256"
)

ORTHOGRAPHIC_JSON = (
    QC_DIR
    / "first_hand_great_circle_reconstruction.json"
)

ORTHOGRAPHIC_SEAL = (
    QC_DIR
    / "first_hand_great_circle_reconstruction.sha256"
)

OUTPUT_JSON = (
    QC_DIR
    / "first_hand_spherical_rendering_comparator.json"
)

OUTPUT_REPORT = (
    ROOT
    / "reports"
    / "first_hand_spherical_rendering_comparator.md"
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

CURVED_LABELLED_IDS = (
    Y1_ID,
    X1_ID,
)

LABELLED_IDS = (
    Y0_ID,
    YAXIS_ID,
    Y1_ID,
    X1_ID,
)

EXPECTED_MORPHOLOGY_CLASS = (
    "post_hoc_model_neutral_morphology_census"
)

EXPECTED_ORTHOGRAPHIC_CLASS = (
    "preregistered_limb_constrained_"
    "great_circle_reconstruction"
)

INTERSECTION_TOL = 1.0e-10


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
    """Verify every entry in a sha256sum-style manifest."""
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

        path = ROOT / relative

        if not path.exists():
            raise RuntimeError(
                f"Sealed file missing: {relative}"
            )

        actual = sha256_path(
            path
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


def verify_dependencies() -> dict[str, Any]:
    """Verify frozen protocol, morphology, and orthographic result."""
    if not PROTOCOL_PATH.exists():
        raise RuntimeError(
            f"Missing protocol: {PROTOCOL_PATH}"
        )

    morphology_manifest = (
        verify_sha256_manifest(
            MORPHOLOGY_SEAL,
            (
                MORPHOLOGY_JSON,
            ),
        )
    )

    orthographic_manifest = (
        verify_sha256_manifest(
            ORTHOGRAPHIC_SEAL,
            (
                ORTHOGRAPHIC_JSON,
            ),
        )
    )

    morphology = load_json(
        MORPHOLOGY_JSON
    )

    orthographic = load_json(
        ORTHOGRAPHIC_JSON
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
        orthographic.get(
            "analysis_class"
        )
        != EXPECTED_ORTHOGRAPHIC_CLASS
    ):
        raise RuntimeError(
            "Unexpected orthographic analysis class."
        )

    morphology_curves = set(
        morphology[
            "curves"
        ]
    )

    expected_morphology_curves = {
        *LABELLED_IDS,
        HOLDOUT_ID,
    }

    if (
        morphology_curves
        != expected_morphology_curves
    ):
        raise RuntimeError(
            "Frozen morphology curve set changed."
        )

    orthographic_curves = set(
        orthographic[
            "curves"
        ]
    )

    if (
        orthographic_curves
        != set(
            LABELLED_IDS
        )
    ):
        raise RuntimeError(
            "Orthographic result must contain "
            "exactly the four labelled curves."
        )

    partition = (
        orthographic[
            "fit_partition"
        ]
    )

    if (
        partition[
            "scaffold_used_for_fitting"
        ]
        is not False
    ):
        raise RuntimeError(
            "Frozen orthographic result used "
            "the scaffold unexpectedly."
        )

    if (
        partition[
            "excluded_scaffold_holdout"
        ]
        != HOLDOUT_ID
    ):
        raise RuntimeError(
            "Unexpected orthographic holdout ID."
        )

    morphology_limb = (
        morphology[
            "frozen_limb_reference"
        ]
    )

    orthographic_limb = (
        orthographic[
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
                morphology_limb[key]
            ),
            float(
                orthographic_limb[key]
            ),
            rel_tol=0.0,
            abs_tol=1.0e-12,
        ):
            raise RuntimeError(
                "Frozen limb disagreement "
                f"for {key}."
            )

    radius = float(
        morphology_limb[
            "radius_px"
        ]
    )

    if not (
        math.isfinite(radius)
        and radius > 0.0
    ):
        raise RuntimeError(
            "Invalid frozen limb radius."
        )

    return {
        "morphology": morphology,
        "orthographic": orthographic,
        "limb": morphology_limb,
        "morphology_manifest": (
            morphology_manifest
        ),
        "orthographic_manifest": (
            orthographic_manifest
        ),
        "protocol_sha256": (
            sha256_path(
                PROTOCOL_PATH
            )
        ),
    }


def point_line_distance(
    point: np.ndarray,
    line_point: np.ndarray,
    line_direction: np.ndarray,
) -> float:
    """Orthogonal distance from a point to an infinite line."""
    point = np.asarray(
        point,
        dtype=np.float64,
    )

    line_point = np.asarray(
        line_point,
        dtype=np.float64,
    )

    direction = np.asarray(
        line_direction,
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
        raise ValueError(
            "Invalid line direction."
        )

    direction /= norm

    normal = np.asarray(
        [
            -direction[1],
            direction[0],
        ],
        dtype=np.float64,
    )

    return abs(
        float(
            np.dot(
                point
                - line_point,
                normal,
            )
        )
    )


def evaluate_line_branch(
    line: dict[str, Any],
    limb: dict[str, Any],
) -> dict[str, Any]:
    """Evaluate the stereographic centre-passing-line invariant."""
    sphere_center = np.asarray(
        [
            float(
                limb[
                    "center_x_px"
                ]
            ),
            float(
                limb[
                    "center_y_px"
                ]
            ),
        ],
        dtype=np.float64,
    )

    line_point = np.asarray(
        [
            float(
                line[
                    "center_x_px"
                ]
            ),
            float(
                line[
                    "center_y_px"
                ]
            ),
        ],
        dtype=np.float64,
    )

    line_direction = np.asarray(
        [
            float(
                line[
                    "direction_x"
                ]
            ),
            float(
                line[
                    "direction_y"
                ]
            ),
        ],
        dtype=np.float64,
    )

    radius = float(
        limb[
            "radius_px"
        ]
    )

    distance = (
        point_line_distance(
            sphere_center,
            line_point,
            line_direction,
        )
    )

    return {
        "branch": (
            "stereographic_great_circle_line"
        ),
        "frozen_line_refitted": False,
        "line_center_x_px": float(
            line[
                "center_x_px"
            ]
        ),
        "line_center_y_px": float(
            line[
                "center_y_px"
            ]
        ),
        "direction_x": float(
            line[
                "direction_x"
            ]
        ),
        "direction_y": float(
            line[
                "direction_y"
            ]
        ),
        "unoriented_bearing_deg": float(
            line[
                "unoriented_bearing_deg"
            ]
        ),
        "frozen_line_rms_px": float(
            line[
                "residuals"
            ][
                "absolute_px"
            ][
                "rms"
            ]
        ),
        "line_to_frozen_sphere_center_px": (
            distance
        ),
        "line_to_frozen_sphere_center_over_R": (
            distance
            / radius
        ),
    }


def circle_circle_intersections(
    center0: np.ndarray,
    radius0: float,
    center1: np.ndarray,
    radius1: float,
) -> dict[str, Any]:
    """Exact Euclidean intersection census for two frozen circles."""
    c0 = np.asarray(
        center0,
        dtype=np.float64,
    )

    c1 = np.asarray(
        center1,
        dtype=np.float64,
    )

    r0 = float(
        radius0
    )

    r1 = float(
        radius1
    )

    if not (
        r0 > 0.0
        and r1 > 0.0
    ):
        raise ValueError(
            "Circle radii must be positive."
        )

    delta = (
        c1
        - c0
    )

    distance = float(
        np.linalg.norm(
            delta
        )
    )

    scale = max(
        1.0,
        r0,
        r1,
        distance,
    )

    tolerance = (
        INTERSECTION_TOL
        * scale
    )

    if distance <= tolerance:
        if math.isclose(
            r0,
            r1,
            rel_tol=0.0,
            abs_tol=tolerance,
        ):
            return {
                "intersection_count": (
                    "coincident"
                ),
                "points_px": [],
            }

        return {
            "intersection_count": 0,
            "points_px": [],
        }

    if (
        distance
        > r0
        + r1
        + tolerance
    ):
        return {
            "intersection_count": 0,
            "points_px": [],
        }

    if (
        distance
        < abs(
            r0
            - r1
        )
        - tolerance
    ):
        return {
            "intersection_count": 0,
            "points_px": [],
        }

    a = (
        r0 * r0
        - r1 * r1
        + distance * distance
    ) / (
        2.0
        * distance
    )

    h_squared = (
        r0 * r0
        - a * a
    )

    if (
        h_squared
        < 0.0
        and abs(
            h_squared
        )
        <= tolerance
        * scale
    ):
        h_squared = 0.0

    if h_squared < 0.0:
        return {
            "intersection_count": 0,
            "points_px": [],
        }

    direction = (
        delta
        / distance
    )

    base_point = (
        c0
        + a
        * direction
    )

    if h_squared == 0.0:
        return {
            "intersection_count": 1,
            "points_px": [
                [
                    float(
                        base_point[0]
                    ),
                    float(
                        base_point[1]
                    ),
                ]
            ],
        }

    h = math.sqrt(
        h_squared
    )

    perpendicular = np.asarray(
        [
            -direction[1],
            direction[0],
        ],
        dtype=np.float64,
    )

    point_a = (
        base_point
        + h
        * perpendicular
    )

    point_b = (
        base_point
        - h
        * perpendicular
    )

    return {
        "intersection_count": 2,
        "points_px": [
            [
                float(
                    point_a[0]
                ),
                float(
                    point_a[1]
                ),
            ],
            [
                float(
                    point_b[0]
                ),
                float(
                    point_b[1]
                ),
            ],
        ],
    }


def angular_separation_deg(
    centre: np.ndarray,
    point_a: np.ndarray,
    point_b: np.ndarray,
) -> float:
    """Unsigned angular separation about a common centre."""
    centre = np.asarray(
        centre,
        dtype=np.float64,
    )

    a = (
        np.asarray(
            point_a,
            dtype=np.float64,
        )
        - centre
    )

    b = (
        np.asarray(
            point_b,
            dtype=np.float64,
        )
        - centre
    )

    norm_a = float(
        np.linalg.norm(
            a
        )
    )

    norm_b = float(
        np.linalg.norm(
            b
        )
    )

    if (
        norm_a <= 0.0
        or norm_b <= 0.0
    ):
        raise ValueError(
            "Angular-separation point lies at centre."
        )

    cosine = float(
        np.clip(
            np.dot(
                a,
                b,
            )
            / (
                norm_a
                * norm_b
            ),
            -1.0,
            1.0,
        )
    )

    return math.degrees(
        math.acos(
            cosine
        )
    )


def evaluate_circle_branch(
    circle: dict[str, Any],
    limb: dict[str, Any],
) -> dict[str, Any]:
    """Evaluate the parameter-free stereographic circle invariant."""
    sphere_center = np.asarray(
        [
            float(
                limb[
                    "center_x_px"
                ]
            ),
            float(
                limb[
                    "center_y_px"
                ]
            ),
        ],
        dtype=np.float64,
    )

    radius_sphere = float(
        limb[
            "radius_px"
        ]
    )

    circle_center = np.asarray(
        [
            float(
                circle[
                    "center_x_px"
                ]
            ),
            float(
                circle[
                    "center_y_px"
                ]
            ),
        ],
        dtype=np.float64,
    )

    radius_curve = float(
        circle[
            "radius_px"
        ]
    )

    centre_offset = float(
        np.linalg.norm(
            circle_center
            - sphere_center
        )
    )

    power_term = (
        radius_curve
        * radius_curve
        - centre_offset
        * centre_offset
    )

    delta_power = (
        power_term
        - radius_sphere
        * radius_sphere
    )

    epsilon_power = (
        delta_power
        / (
            radius_sphere
            * radius_sphere
        )
    )

    implied_radius = None
    delta_radius = None
    relative_delta_radius = None

    if power_term > 0.0:
        implied_radius = (
            math.sqrt(
                power_term
            )
        )

        delta_radius = (
            implied_radius
            - radius_sphere
        )

        relative_delta_radius = (
            delta_radius
            / radius_sphere
        )

    intersections = (
        circle_circle_intersections(
            sphere_center,
            radius_sphere,
            circle_center,
            radius_curve,
        )
    )

    separation = None
    delta_antipodal = None

    if (
        intersections[
            "intersection_count"
        ]
        == 2
    ):
        points = (
            intersections[
                "points_px"
            ]
        )

        separation = (
            angular_separation_deg(
                sphere_center,
                np.asarray(
                    points[0],
                    dtype=np.float64,
                ),
                np.asarray(
                    points[1],
                    dtype=np.float64,
                ),
            )
        )

        delta_antipodal = abs(
            180.0
            - separation
        )

    return {
        "branch": (
            "stereographic_great_circle_circle"
        ),
        "frozen_circle_refitted": False,
        "circle_center_x_px": float(
            circle[
                "center_x_px"
            ]
        ),
        "circle_center_y_px": float(
            circle[
                "center_y_px"
            ]
        ),
        "circle_radius_px": (
            radius_curve
        ),
        "frozen_circle_rms_px": float(
            circle[
                "residuals"
            ][
                "absolute_px"
            ][
                "rms"
            ]
        ),
        "centre_offset_d_px": (
            centre_offset
        ),
        "circle_radius_over_R": (
            radius_curve
            / radius_sphere
        ),
        "centre_offset_over_R": (
            centre_offset
            / radius_sphere
        ),
        "power_term_r2_minus_d2_px2": (
            power_term
        ),
        "delta_power_px2": (
            delta_power
        ),
        "epsilon_power": (
            epsilon_power
        ),
        "R_implied_px": (
            implied_radius
        ),
        "delta_R_px": (
            delta_radius
        ),
        "delta_R_over_R": (
            relative_delta_radius
        ),
        "equator_intersections": (
            intersections
        ),
        "antipodal_separation_deg": (
            separation
        ),
        "delta_antipodal_deg": (
            delta_antipodal
        ),
    }


def orthographic_rms(
    orthographic: dict[str, Any],
    curve_id: str,
) -> float:
    return float(
        orthographic[
            "curves"
        ][
            curve_id
        ][
            "great_circle_fits"
        ][
            "equal_pass_combined"
        ][
            "residuals"
        ][
            "absolute_px"
        ][
            "rms"
        ]
    )


def evaluate_labelled(
    morphology: dict[str, Any],
    orthographic: dict[str, Any],
    limb: dict[str, Any],
) -> dict[str, Any]:
    """Evaluate all four labelled curves before the holdout."""
    result: dict[
        str,
        Any,
    ] = {}

    for curve_id in LINE_IDS:
        item = (
            evaluate_line_branch(
                morphology[
                    "curves"
                ][
                    curve_id
                ][
                    "line"
                ],
                limb,
            )
        )

        item[
            "frozen_orthographic_gc_rms_px"
        ] = (
            orthographic_rms(
                orthographic,
                curve_id,
            )
        )

        result[
            curve_id
        ] = item

    for curve_id in CURVED_LABELLED_IDS:
        item = (
            evaluate_circle_branch(
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

        item[
            "frozen_orthographic_gc_rms_px"
        ] = (
            orthographic_rms(
                orthographic,
                curve_id,
            )
        )

        result[
            curve_id
        ] = item

    return result


def build_analysis() -> dict[str, Any]:
    dependencies = (
        verify_dependencies()
    )

    morphology = (
        dependencies[
            "morphology"
        ]
    )

    orthographic = (
        dependencies[
            "orthographic"
        ]
    )

    limb = (
        dependencies[
            "limb"
        ]
    )

    # Labelled curves are fully evaluated first.
    labelled = (
        evaluate_labelled(
            morphology,
            orthographic,
            limb,
        )
    )

    labelled_fingerprint = (
        canonical_json_sha256(
            labelled
        )
    )

    # Only now expose the already-frozen scaffold holdout
    # to the parameter-free invariant.
    holdout = (
        evaluate_circle_branch(
            morphology[
                "curves"
            ][
                HOLDOUT_ID
            ][
                "circle"
            ],
            limb,
        )
    )

    return {
        "checkpoint": (
            "first_hand_spherical_"
            "rendering_comparator_v0.8"
        ),
        "analysis_class": (
            "preregistered_parameter_free_"
            "spherical_rendering_comparator"
        ),
        "protocol_checkpoint": (
            "1fd428a"
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
                sha256_path(
                    MORPHOLOGY_JSON
                )
            ),
            "orthographic_result": str(
                ORTHOGRAPHIC_JSON.relative_to(
                    ROOT
                )
            ),
            "orthographic_sha256": (
                sha256_path(
                    ORTHOGRAPHIC_JSON
                )
            ),
            "frozen_limb_reference": (
                limb
            ),
            "labelled_result_block_sha256_before_holdout": (
                labelled_fingerprint
            ),
        },
        "mapping_distinction": {
            "construction_map_recomputed": False,
            "page_rendering_map_tested": (
                "stereographic"
            ),
            "construction_and_rendering_maps_conflated": False,
        },
        "branch_allocation": {
            "line_branch": list(
                LINE_IDS
            ),
            "curved_labelled_circle_branch": list(
                CURVED_LABELLED_IDS
            ),
            "curved_holdout_circle_branch": (
                HOLDOUT_ID
            ),
            "allocation_changed_after_result": False,
        },
        "method": {
            "free_parameters": 0,
            "optimizer_calls": 0,
            "curve_refits": 0,
            "line_invariant": (
                "distance from frozen sphere centre "
                "to frozen orthogonal line fit"
            ),
            "circle_invariant": (
                "r^2 - d^2 - R^2"
            ),
            "antipodal_invariant": (
                "angular separation of frozen curve-circle/"
                "equator-circle intersections"
            ),
            "post_hoc_binary_threshold_added": False,
        },
        "labelled_curves": (
            labelled
        ),
        "holdout": {
            "curve_id": (
                HOLDOUT_ID
            ),
            "used_for_calibration": False,
            "evaluated_after_labelled_block_frozen_in_memory": True,
            "result": (
                holdout
            ),
        },
        "scope": {
            "stereographic_rendering_invariants_computed": True,
            "orthographic_result_overwritten": False,
            "new_curve_fit_computed": False,
            "new_construction_map_fitted": False,
            "projective_gauge_selected": False,
            "construction_scale_selected": False,
            "fixed_scale_candidate_verdict_issued": False,
            "spherical_plane_angles_reconstructed": False,
            "reciprocal_spiral_projection_computed": False,
            "s1_computed": False,
            "s1_5_computed": False,
            "s2_computed": False,
        },
        "interpretation_boundary": (
            "This checkpoint evaluates parameter-free algebraic "
            "consequences of stereographic rendering using only "
            "previously frozen line, circle, and limb fits. "
            "Small closure residuals support compatibility but do "
            "not prove that the historical image was generated "
            "stereographically. Large residuals reject this exact "
            "rendering relation for the frozen measured geometry. "
            "No new post-hoc binary threshold is introduced."
        ),
    }


def render_report(
    analysis: dict[str, Any],
) -> str:
    limb = (
        analysis[
            "provenance"
        ][
            "frozen_limb_reference"
        ]
    )

    lines = [
        "# First Hand spherical-rendering invariant comparator",
        "",
        "**Status:** preregistered parameter-free comparator",
        "",
        f"Frozen limb radius: `{float(limb['radius_px']):.9f} px`",
        "",
        "No curve was refitted and no optimizer was called.",
        "",
        "## Near-linear labelled traces",
        "",
        "| Curve | Frozen line RMS px | Centre distance px | Centre distance / R | Orthographic GC RMS px |",
        "|---|---:|---:|---:|---:|",
    ]

    for curve_id in LINE_IDS:
        item = (
            analysis[
                "labelled_curves"
            ][
                curve_id
            ]
        )

        lines.append(
            f"| `{curve_id}` | "
            f"{item['frozen_line_rms_px']:.6f} | "
            f"{item['line_to_frozen_sphere_center_px']:.6f} | "
            f"{item['line_to_frozen_sphere_center_over_R']:.9f} | "
            f"{item['frozen_orthographic_gc_rms_px']:.6f} |"
        )

    lines += [
        "",
        "## Curved labelled traces",
        "",
        "| Curve | Circle RMS px | r px | d px | r/R | d/R | epsilon_power | Delta_R px | Antipodal separation deg | Delta antipodal deg | Orthographic GC RMS px |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]

    for curve_id in CURVED_LABELLED_IDS:
        item = (
            analysis[
                "labelled_curves"
            ][
                curve_id
            ]
        )

        delta_r = (
            "undefined"
            if item[
                "delta_R_px"
            ]
            is None
            else f"{item['delta_R_px']:.6f}"
        )

        separation = (
            "undefined"
            if item[
                "antipodal_separation_deg"
            ]
            is None
            else f"{item['antipodal_separation_deg']:.6f}"
        )

        delta_antipodal = (
            "undefined"
            if item[
                "delta_antipodal_deg"
            ]
            is None
            else f"{item['delta_antipodal_deg']:.6f}"
        )

        lines.append(
            f"| `{curve_id}` | "
            f"{item['frozen_circle_rms_px']:.6f} | "
            f"{item['circle_radius_px']:.6f} | "
            f"{item['centre_offset_d_px']:.6f} | "
            f"{item['circle_radius_over_R']:.6f} | "
            f"{item['centre_offset_over_R']:.6f} | "
            f"{item['epsilon_power']:.9f} | "
            f"{delta_r} | "
            f"{separation} | "
            f"{delta_antipodal} | "
            f"{item['frozen_orthographic_gc_rms_px']:.6f} |"
        )

    holdout = (
        analysis[
            "holdout"
        ][
            "result"
        ]
    )

    lines += [
        "",
        "## Independent scaffold holdout",
        "",
        f"Curve: `{analysis['holdout']['curve_id']}`",
        "",
        f"- frozen circle RMS: `{holdout['frozen_circle_rms_px']:.6f} px`",
        f"- radius r: `{holdout['circle_radius_px']:.6f} px`",
        f"- centre offset d: `{holdout['centre_offset_d_px']:.6f} px`",
        f"- r/R: `{holdout['circle_radius_over_R']:.6f}`",
        f"- d/R: `{holdout['centre_offset_over_R']:.6f}`",
        f"- epsilon_power: `{holdout['epsilon_power']:.9f}`",
    ]

    if (
        holdout[
            "delta_R_px"
        ]
        is None
    ):
        lines.append(
            "- radius-equivalent closure: `undefined`"
        )
    else:
        lines.append(
            "- Delta_R: "
            f"`{holdout['delta_R_px']:.6f} px`"
        )

    if (
        holdout[
            "antipodal_separation_deg"
        ]
        is None
    ):
        lines.append(
            "- antipodal separation: `undefined`"
        )
    else:
        lines += [
            "- antipodal separation: "
            f"`{holdout['antipodal_separation_deg']:.6f} deg`",
            "- Delta antipodal: "
            f"`{holdout['delta_antipodal_deg']:.6f} deg`",
        ]

    lines += [
        "",
        "The scaffold did not calibrate or modify the stereographic invariant.",
        "",
        "## Interpretation boundary",
        "",
        "The stereographic circle condition is `r^2 - d^2 = R^2`. "
        "The straight-line branch requires the frozen line to pass through "
        "the frozen sphere centre.",
        "",
        "No new binary acceptance threshold is introduced. These are continuous "
        "closure diagnostics on a hand-drawn source.",
        "",
        "This comparator concerns rendering of an already-spherical scaffold "
        "onto the page. It does not replace the earlier flat-to-sphere "
        "central-projective construction-map audit.",
        "",
        "No projective gauge, construction scale, reciprocal-spiral result, "
        "S1, S1.5, or S2 is produced.",
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
            "Parameter-free First Hand "
            "spherical-rendering invariant comparator."
        )
    )

    parser.add_argument(
        "--check-inputs",
        action="store_true",
        help=(
            "Verify frozen inputs without calculating "
            "stereographic invariants."
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
            "Orthographic great-circle result: VERIFIED"
        )

        print(
            "Rendering-comparator protocol: PRESENT"
        )

        print(
            "Frozen limb radius:",
            f"{float(dependencies['limb']['radius_px']):.9f} px",
        )

        print(
            "Labelled line branch:",
            len(
                LINE_IDS
            ),
        )

        print(
            "Labelled circle branch:",
            len(
                CURVED_LABELLED_IDS
            ),
        )

        print(
            "Scaffold holdout excluded from calibration: YES"
        )

        print(
            "No stereographic invariant was computed."
        )

        return 0

    analysis = (
        build_analysis()
    )

    write_outputs(
        analysis
    )

    print(
        "=" * 96
    )

    print(
        "FIRST HAND SPHERICAL-RENDERING "
        "INVARIANT COMPARATOR"
    )

    print(
        "=" * 96
    )

    for curve_id in LINE_IDS:
        item = (
            analysis[
                "labelled_curves"
            ][
                curve_id
            ]
        )

        print(
            f"{curve_id}: "
            f"line-centre distance="
            f"{item['line_to_frozen_sphere_center_px']:.6f} px, "
            f"d/R="
            f"{item['line_to_frozen_sphere_center_over_R']:.9f}"
        )

    for curve_id in CURVED_LABELLED_IDS:
        item = (
            analysis[
                "labelled_curves"
            ][
                curve_id
            ]
        )

        delta_r = (
            "undefined"
            if item[
                "delta_R_px"
            ]
            is None
            else f"{item['delta_R_px']:.6f} px"
        )

        antipodal = (
            "undefined"
            if item[
                "delta_antipodal_deg"
            ]
            is None
            else f"{item['delta_antipodal_deg']:.6f} deg"
        )

        print(
            f"{curve_id}: "
            f"epsilon_power={item['epsilon_power']:.9f}, "
            f"Delta_R={delta_r}, "
            f"Delta_antipodal={antipodal}"
        )

    holdout = (
        analysis[
            "holdout"
        ][
            "result"
        ]
    )

    holdout_delta_r = (
        "undefined"
        if holdout[
            "delta_R_px"
        ]
        is None
        else f"{holdout['delta_R_px']:.6f} px"
    )

    holdout_antipodal = (
        "undefined"
        if holdout[
            "delta_antipodal_deg"
        ]
        is None
        else f"{holdout['delta_antipodal_deg']:.6f} deg"
    )

    print(
        f"{HOLDOUT_ID} [HOLDOUT]: "
        f"epsilon_power={holdout['epsilon_power']:.9f}, "
        f"Delta_R={holdout_delta_r}, "
        f"Delta_antipodal={holdout_antipodal}"
    )

    print(
        f"Wrote {OUTPUT_JSON}"
    )

    print(
        f"Wrote {OUTPUT_REPORT}"
    )

    print(
        "No curve was refitted and no optimizer was called."
    )

    print(
        "No construction-map scale or "
        "self-embedment score was computed."
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
