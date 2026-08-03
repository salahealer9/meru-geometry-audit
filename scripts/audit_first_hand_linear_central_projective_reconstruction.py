#!/usr/bin/env python3
"""First Hand linear central-projective reconstruction.

The two already-frozen stereographic offset-circle centres X1 and Y1
determine

    G = L^(-T)

without optimization.

The independently frozen Y-axis and Y0 line normals are then used only
for validation.

No curve is refitted.
No rendering parameter is fitted.
No scaffold information enters the reconstruction.
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
    / "first_hand_linear_central_projective_reconstruction_protocol.md"
)

PLANE_ANGLE_JSON = (
    QC_DIR
    / "first_hand_stereographic_plane_angles.json"
)

PLANE_ANGLE_SEAL = (
    QC_DIR
    / "first_hand_stereographic_plane_angles.sha256"
)

RENDERING_JSON = (
    QC_DIR
    / "first_hand_spherical_rendering_comparator.json"
)

RENDERING_SEAL = (
    QC_DIR
    / "first_hand_spherical_rendering_comparator.sha256"
)

OUTPUT_JSON = (
    QC_DIR
    / "first_hand_linear_central_projective_reconstruction.json"
)

OUTPUT_REPORT = (
    ROOT
    / "reports"
    / "first_hand_linear_central_projective_reconstruction.md"
)


Y0_ID = "AOG-LM-P07-GC-Y0"
Y1_ID = "AOG-LM-P07-GC-Y1"
YAXIS_ID = "AOG-LM-P07-GC-YAXIS"
X1_ID = "AOG-LM-P07-GC-X1"

HOLDOUT_ID = (
    "AOG-LM-P07-GC-SCAFFOLD-UR-UC-X1LL-LL"
)

CALIBRATION_CIRCLE_IDS = (
    X1_ID,
    Y1_ID,
)

VALIDATION_LINE_IDS = (
    YAXIS_ID,
    Y0_ID,
)

EXPECTED_PLANE_CLASS = (
    "preregistered_stereographic_"
    "plane_angle_reconstruction"
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
    """Verify sha256sum-style frozen manifest."""
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
                f"{relative}: expected {expected}, "
                f"got {actual}"
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
                f"from manifest: {relative}"
            )

    return found


def unit2(
    vector: np.ndarray,
) -> np.ndarray:
    vector = np.asarray(
        vector,
        dtype=np.float64,
    )

    if vector.shape != (2,):
        raise ValueError(
            "Expected two-vector."
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
            "Cannot normalize invalid two-vector."
        )

    return vector / norm


def unoriented_angle_deg(
    vector_a: np.ndarray,
    vector_b: np.ndarray,
) -> float:
    """Unoriented 2-D vector angle in [0,90] degrees.

    Use atan2(|det|, |dot|) rather than acos(|dot|).
    This is numerically stable for nearly parallel vectors and
    returns exact zero for exactly collinear floating-point vectors.
    """
    a = unit2(
        vector_a
    )

    b = unit2(
        vector_b
    )

    dot = abs(
        float(
            np.dot(
                a,
                b,
            )
        )
    )

    determinant = abs(
        float(
            a[0]
            * b[1]
            - a[1]
            * b[0]
        )
    )

    return math.degrees(
        math.atan2(
            determinant,
            dot,
        )
    )


def circle_centre_vector(
    plane_result: dict[str, Any],
    curve_id: str,
) -> np.ndarray:
    """Return frozen normalized stereographic circle centre."""
    item = (
        plane_result[
            "reconstructed_planes"
        ][
            curve_id
        ]
    )

    if (
        item[
            "branch"
        ]
        != "stereographic_finite_circle"
    ):
        raise RuntimeError(
            f"{curve_id} is not on the frozen circle branch."
        )

    return np.asarray(
        [
            float(
                item[
                    "normalized_circle_center_u"
                ]
            ),
            float(
                item[
                    "normalized_circle_center_v"
                ]
            ),
        ],
        dtype=np.float64,
    )


def observed_line_normal(
    plane_result: dict[str, Any],
    curve_id: str,
) -> np.ndarray:
    """Return frozen page-plane normal of a line branch."""
    item = (
        plane_result[
            "reconstructed_planes"
        ][
            curve_id
        ]
    )

    if (
        item[
            "branch"
        ]
        != "stereographic_diameter_line"
    ):
        raise RuntimeError(
            f"{curve_id} is not on the frozen line branch."
        )

    normal3 = np.asarray(
        item[
            "unit_plane_normal"
        ],
        dtype=np.float64,
    )

    if normal3.shape != (3,):
        raise RuntimeError(
            "Malformed frozen plane normal."
        )

    if not math.isclose(
        float(
            normal3[2]
        ),
        0.0,
        rel_tol=0.0,
        abs_tol=1.0e-12,
    ):
        raise RuntimeError(
            f"{curve_id} line normal has nonzero z component."
        )

    return unit2(
        normal3[:2]
    )


def reconstruct_linear_map(
    g_x: np.ndarray,
    g_y: np.ndarray,
) -> dict[str, Any]:
    """Reconstruct G=L^-T and L algebraically."""
    gx = np.asarray(
        g_x,
        dtype=np.float64,
    )

    gy = np.asarray(
        g_y,
        dtype=np.float64,
    )

    if (
        gx.shape != (2,)
        or gy.shape != (2,)
    ):
        raise ValueError(
            "g_x and g_y must be two-vectors."
        )

    G = np.column_stack(
        (
            gx,
            gy,
        )
    )

    det_G = float(
        np.linalg.det(
            G
        )
    )

    cond_G = float(
        np.linalg.cond(
            G
        )
    )

    try:
        inverse_G = np.linalg.inv(
            G
        )
    except np.linalg.LinAlgError:
        return {
            "G": G.tolist(),
            "det_G": det_G,
            "condition_number_G": cond_G,
            "inverse_available": False,
            "L": None,
            "det_L": None,
            "condition_number_L": None,
            "singular_values_L": None,
            "singular_value_ratio": None,
            "U": None,
            "Vt": None,
            "L_transpose_L": None,
        }

    L = inverse_G.T

    det_L = float(
        np.linalg.det(
            L
        )
    )

    cond_L = float(
        np.linalg.cond(
            L
        )
    )

    U, singular_values, Vt = (
        np.linalg.svd(
            L,
            full_matrices=True,
        )
    )

    if not (
        singular_values.shape
        == (2,)
    ):
        raise RuntimeError(
            "Unexpected SVD result."
        )

    singular_ratio = float(
        singular_values[0]
        / singular_values[1]
    )

    LtL = (
        L.T
        @ L
    )

    return {
        "G": [
            [
                float(value)
                for value in row
            ]
            for row in G
        ],
        "det_G": det_G,
        "condition_number_G": cond_G,
        "inverse_available": True,
        "L": [
            [
                float(value)
                for value in row
            ]
            for row in L
        ],
        "det_L": det_L,
        "condition_number_L": cond_L,
        "singular_values_L": [
            float(value)
            for value
            in singular_values
        ],
        "singular_value_ratio": (
            singular_ratio
        ),
        "U": [
            [
                float(value)
                for value in row
            ]
            for row in U
        ],
        "Vt": [
            [
                float(value)
                for value in row
            ]
            for row in Vt
        ],
        "L_transpose_L": [
            [
                float(value)
                for value in row
            ]
            for row in LtL
        ],
    }


def validation_diagnostics(
    g_x: np.ndarray,
    g_y: np.ndarray,
    observed_yaxis_normal: np.ndarray,
    observed_y0_normal: np.ndarray,
) -> dict[str, Any]:
    """Independent zero-coordinate line validation."""
    eta_x = (
        unoriented_angle_deg(
            observed_yaxis_normal,
            g_x,
        )
    )

    eta_y = (
        unoriented_angle_deg(
            observed_y0_normal,
            g_y,
        )
    )

    observed_zero_axis_angle = (
        unoriented_angle_deg(
            observed_yaxis_normal,
            observed_y0_normal,
        )
    )

    gamma_G = (
        unoriented_angle_deg(
            g_x,
            g_y,
        )
    )

    return {
        "eta_x_deg": (
            eta_x
        ),
        "eta_y_deg": (
            eta_y
        ),
        "predicted_yaxis_normal_from_X1": (
            unit2(
                g_x
            ).tolist()
        ),
        "observed_yaxis_normal": (
            unit2(
                observed_yaxis_normal
            ).tolist()
        ),
        "predicted_y0_normal_from_Y1": (
            unit2(
                g_y
            ).tolist()
        ),
        "observed_y0_normal": (
            unit2(
                observed_y0_normal
            ).tolist()
        ),
        "gamma_G_deg": (
            gamma_G
        ),
        "gamma_G_deviation_from_90_deg": (
            abs(
                90.0
                - gamma_G
            )
        ),
        "observed_zero_line_normal_angle_deg": (
            observed_zero_axis_angle
        ),
        "observed_zero_line_normal_deviation_from_90_deg": (
            abs(
                90.0
                - observed_zero_axis_angle
            )
        ),
        "post_hoc_pass_threshold_added": False,
    }


def centre_scale_diagnostics(
    g_x: np.ndarray,
    g_y: np.ndarray,
    plane_result: dict[str, Any],
) -> dict[str, Any]:
    """Compare circle-centre scales with earlier observed-angle scales."""
    norm_x = float(
        np.linalg.norm(
            g_x
        )
    )

    norm_y = float(
        np.linalg.norm(
            g_y
        )
    )

    if (
        norm_x <= 0.0
        or norm_y <= 0.0
    ):
        raise RuntimeError(
            "Degenerate centre vector."
        )

    k_x_center = (
        1.0
        / norm_x
    )

    k_y_center = (
        1.0
        / norm_y
    )

    delta_x_center = (
        math.degrees(
            math.atan(
                k_x_center
            )
        )
    )

    delta_y_center = (
        math.degrees(
            math.atan(
                k_y_center
            )
        )
    )

    prior = (
        plane_result[
            "image_derived_coordinate_separations"
        ]
    )

    k_x_angle = (
        prior[
            "k_x_tan_delta_x"
        ]
    )

    k_y_angle = (
        prior[
            "k_y_tan_delta_y"
        ]
    )

    if (
        k_x_angle is None
        or k_y_angle is None
    ):
        raise RuntimeError(
            "Prior angle-derived scales are undefined."
        )

    return {
        "norm_c_X1": norm_x,
        "norm_c_Y1": norm_y,
        "k_x_center": (
            k_x_center
        ),
        "k_y_center": (
            k_y_center
        ),
        "delta_x_center_predicted_deg": (
            delta_x_center
        ),
        "delta_y_center_predicted_deg": (
            delta_y_center
        ),
        "prior_delta_x_observed_deg": float(
            prior[
                "delta_x_deg"
            ]
        ),
        "prior_delta_y_observed_deg": float(
            prior[
                "delta_y_deg"
            ]
        ),
        "prior_k_x_tan_delta_x": float(
            k_x_angle
        ),
        "prior_k_y_tan_delta_y": float(
            k_y_angle
        ),
        "k_x_center_minus_angle_derived": (
            k_x_center
            - float(
                k_x_angle
            )
        ),
        "k_y_center_minus_angle_derived": (
            k_y_center
            - float(
                k_y_angle
            )
        ),
        "delta_x_center_minus_observed_deg": (
            delta_x_center
            - float(
                prior[
                    "delta_x_deg"
                ]
            )
        ),
        "delta_y_center_minus_observed_deg": (
            delta_y_center
            - float(
                prior[
                    "delta_y_deg"
                ]
            )
        ),
        "single_isotropic_scale_imposed": False,
    }


def fixed_scale_comparison(
    centre_scales: dict[str, Any],
    linear_map: dict[str, Any],
    plane_result: dict[str, Any],
) -> dict[str, Any]:
    """Descriptive comparison with already-frozen scale candidates."""
    frozen = (
        plane_result[
            "fixed_scale_comparison"
        ]
    )

    if set(
        frozen
    ) != set(
        SCALE_IDS
    ):
        raise RuntimeError(
            "Frozen fixed-scale registry changed."
        )

    singular_values = (
        linear_map[
            "singular_values_L"
        ]
    )

    result: dict[
        str,
        Any,
    ] = {}

    for scale_id in SCALE_IDS:
        item = (
            frozen[
                scale_id
            ]
        )

        candidate = float(
            item[
                "scale_k"
            ]
        )

        entry: dict[
            str,
            Any,
        ] = {
            "scale_k": candidate,
            "predicted_delta_degrees": float(
                item[
                    "predicted_delta_degrees"
                ]
            ),
            "k_x_center_minus_candidate": (
                float(
                    centre_scales[
                        "k_x_center"
                    ]
                )
                - candidate
            ),
            "k_y_center_minus_candidate": (
                float(
                    centre_scales[
                        "k_y_center"
                    ]
                )
                - candidate
            ),
            "candidate_reoptimized": False,
            "candidate_selected": False,
        }

        if singular_values is None:
            entry[
                "sigma_1_minus_candidate"
            ] = None

            entry[
                "sigma_2_minus_candidate"
            ] = None
        else:
            entry[
                "sigma_1_minus_candidate"
            ] = (
                float(
                    singular_values[0]
                )
                - candidate
            )

            entry[
                "sigma_2_minus_candidate"
            ] = (
                float(
                    singular_values[1]
                )
                - candidate
            )

        result[
            scale_id
        ] = entry

    return result


def verify_dependencies() -> dict[str, Any]:
    """Verify frozen parent checkpoints without doing reconstruction."""
    if not PROTOCOL_PATH.exists():
        raise RuntimeError(
            f"Missing protocol: {PROTOCOL_PATH}"
        )

    verify_sha256_manifest(
        PLANE_ANGLE_SEAL,
        (
            PLANE_ANGLE_JSON,
        ),
    )

    verify_sha256_manifest(
        RENDERING_SEAL,
        (
            RENDERING_JSON,
        ),
    )

    plane_result = (
        load_json(
            PLANE_ANGLE_JSON
        )
    )

    rendering = (
        load_json(
            RENDERING_JSON
        )
    )

    if (
        plane_result.get(
            "analysis_class"
        )
        != EXPECTED_PLANE_CLASS
    ):
        raise RuntimeError(
            "Unexpected plane-angle analysis class."
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

    expected_plane_ids = {
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
        != expected_plane_ids
    ):
        raise RuntimeError(
            "Frozen reconstructed-plane set changed."
        )

    partition = (
        plane_result[
            "fit_partition"
        ]
    )

    if (
        partition[
            "scaffold_used_for_plane_reconstruction"
        ]
        is not False
    ):
        raise RuntimeError(
            "Scaffold unexpectedly entered prior plane reconstruction."
        )

    if (
        partition[
            "scaffold_used_for_scale_comparison"
        ]
        is not False
    ):
        raise RuntimeError(
            "Scaffold unexpectedly entered prior scale comparison."
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
            "Scaffold unexpectedly entered rendering calibration."
        )

    actual_rendering_sha = (
        sha256_path(
            RENDERING_JSON
        )
    )

    parent_rendering_sha = (
        plane_result[
            "provenance"
        ][
            "rendering_comparator_sha256"
        ]
    )

    if (
        actual_rendering_sha
        != parent_rendering_sha
    ):
        raise RuntimeError(
            "Plane-angle result does not point to "
            "the currently sealed rendering comparator."
        )

    return {
        "plane_result": (
            plane_result
        ),
        "rendering": (
            rendering
        ),
        "protocol_sha256": (
            sha256_path(
                PROTOCOL_PATH
            )
        ),
        "plane_angle_sha256": (
            sha256_path(
                PLANE_ANGLE_JSON
            )
        ),
        "rendering_sha256": (
            actual_rendering_sha
        ),
    }


def rendering_closure_context(
    rendering: dict[str, Any],
) -> dict[str, Any]:
    labelled = (
        rendering[
            "labelled_curves"
        ]
    )

    return {
        X1_ID: {
            "epsilon_power": (
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
        Y1_ID: {
            "epsilon_power": (
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
        "scaffold_holdout": {
            "curve_id": (
                HOLDOUT_ID
            ),
            "used_for_linear_map_reconstruction": False,
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

    plane_result = (
        dependencies[
            "plane_result"
        ]
    )

    rendering = (
        dependencies[
            "rendering"
        ]
    )

    # Calibration information: only the two offset-circle centres.
    g_x = (
        circle_centre_vector(
            plane_result,
            X1_ID,
        )
    )

    g_y = (
        circle_centre_vector(
            plane_result,
            Y1_ID,
        )
    )

    linear_map = (
        reconstruct_linear_map(
            g_x,
            g_y,
        )
    )

    # Independent validation information is exposed only after L exists.
    observed_yaxis_normal = (
        observed_line_normal(
            plane_result,
            YAXIS_ID,
        )
    )

    observed_y0_normal = (
        observed_line_normal(
            plane_result,
            Y0_ID,
        )
    )

    validation = (
        validation_diagnostics(
            g_x,
            g_y,
            observed_yaxis_normal,
            observed_y0_normal,
        )
    )

    centre_scales = (
        centre_scale_diagnostics(
            g_x,
            g_y,
            plane_result,
        )
    )

    core = {
        "calibration_vectors": {
            "g_x_from_X1_circle_center": (
                g_x.tolist()
            ),
            "g_y_from_Y1_circle_center": (
                g_y.tolist()
            ),
            "circle_radii_used": False,
            "line_directions_used_to_construct_L": False,
        },
        "linear_map_reconstruction": (
            linear_map
        ),
        "independent_zero_line_validation": (
            validation
        ),
        "centre_scale_diagnostics": (
            centre_scales
        ),
    }

    core_fingerprint = (
        canonical_json_sha256(
            core
        )
    )

    # Fixed source candidates are consulted only after
    # G, L, line validation, and centre-derived scales exist.
    scale_comparison = (
        fixed_scale_comparison(
            centre_scales,
            linear_map,
            plane_result,
        )
    )

    return {
        "checkpoint": (
            "first_hand_linear_central_"
            "projective_reconstruction_v0.8"
        ),
        "analysis_class": (
            "preregistered_linear_central_"
            "projective_reconstruction"
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
            "plane_angle_result": str(
                PLANE_ANGLE_JSON.relative_to(
                    ROOT
                )
            ),
            "plane_angle_sha256": (
                dependencies[
                    "plane_angle_sha256"
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
            "core_reconstruction_sha256_before_fixed_scale_comparison": (
                core_fingerprint
            ),
        },
        "model": {
            "formula": (
                "S_L(p)=normalize((L p,1))"
            ),
            "dual_vectors": (
                "g_x=L^-T e_x; g_y=L^-T e_y"
            ),
            "stereographic_offset_circle_relation": (
                "c_X1=g_x; c_Y1=g_y"
            ),
            "matrix_relation": (
                "G=[g_x g_y]=L^-T; L=(G^-1)^T"
            ),
        },
        "partition": {
            "L_calibration": [
                X1_ID,
                Y1_ID,
            ],
            "independent_line_validation": [
                YAXIS_ID,
                Y0_ID,
            ],
            "scaffold_holdout": (
                HOLDOUT_ID
            ),
            "scaffold_used": False,
        },
        **core,
        "fixed_source_scale_comparison": (
            scale_comparison
        ),
        "rendering_closure_context": (
            rendering_closure_context(
                rendering
            )
        ),
        "scope": {
            "free_parameters_fitted": 0,
            "optimizer_calls": 0,
            "curve_refits": 0,
            "rendering_refits": 0,
            "general_3x3_projective_fit": False,
            "nonlinear_map_fit": False,
            "single_scale_selected": False,
            "source_candidate_selected": False,
            "scaffold_planar_identity_assigned": False,
            "reciprocal_spiral_projection_computed": False,
            "s1_computed": False,
            "s1_5_computed": False,
            "s2_computed": False,
        },
        "interpretation_boundary": (
            "X1 and Y1 alone reconstruct the candidate 2x2 "
            "linear central-projective gauge. YAXIS and Y0 are "
            "independent directional validations and are not used "
            "to improve L. No post-hoc validation threshold is "
            "introduced. Rendering closure, especially the larger "
            "Y1 misclosure, must remain visible when interpreting "
            "the reconstructed map."
        ),
    }


def render_report(
    analysis: dict[str, Any],
) -> str:
    linear = (
        analysis[
            "linear_map_reconstruction"
        ]
    )

    validation = (
        analysis[
            "independent_zero_line_validation"
        ]
    )

    scales = (
        analysis[
            "centre_scale_diagnostics"
        ]
    )

    closure = (
        analysis[
            "rendering_closure_context"
        ]
    )

    lines = [
        "# First Hand linear central-projective reconstruction",
        "",
        "**Status:** preregistered zero-parameter algebraic reconstruction",
        "",
        "The candidate map is reconstructed from the already-frozen X1 and Y1 "
        "stereographic circle centres only.",
        "",
        "No curve was refitted and no optimizer was called.",
        "",
        "## Reconstructed dual-coordinate matrix",
        "",
        "```text",
        "G =",
    ]

    for row in linear[
        "G"
    ]:
        lines.append(
            "    ["
            + ", ".join(
                f"{value:.12f}"
                for value in row
            )
            + "]"
        )

    lines += [
        "```",
        "",
        f"- det(G): `{linear['det_G']:.12f}`",
        f"- cond(G): `{linear['condition_number_G']:.9f}`",
        f"- inverse available: `{linear['inverse_available']}`",
        "",
    ]

    if (
        linear[
            "inverse_available"
        ]
    ):
        lines += [
            "## Reconstructed construction matrix",
            "",
            "```text",
            "L =",
        ]

        for row in linear[
            "L"
        ]:
            lines.append(
                "    ["
                + ", ".join(
                    f"{value:.12f}"
                    for value in row
                )
                + "]"
            )

        singular = (
            linear[
                "singular_values_L"
            ]
        )

        lines += [
            "```",
            "",
            f"- det(L): `{linear['det_L']:.12f}`",
            f"- cond(L): `{linear['condition_number_L']:.9f}`",
            f"- sigma_1: `{singular[0]:.12f}`",
            f"- sigma_2: `{singular[1]:.12f}`",
            f"- sigma_1 / sigma_2: `{linear['singular_value_ratio']:.12f}`",
            "",
        ]

    lines += [
        "## Independent zero-coordinate line validation",
        "",
        f"- eta_x, predicted X1 dual direction vs observed YAXIS normal: "
        f"`{validation['eta_x_deg']:.9f} deg`",
        f"- eta_y, predicted Y1 dual direction vs observed Y0 normal: "
        f"`{validation['eta_y_deg']:.9f} deg`",
        f"- angle(g_x, g_y): `{validation['gamma_G_deg']:.9f} deg`",
        f"- |90 - angle(g_x,g_y)|: "
        f"`{validation['gamma_G_deviation_from_90_deg']:.9f} deg`",
        f"- observed zero-line normal angle: "
        f"`{validation['observed_zero_line_normal_angle_deg']:.9f} deg`",
        "",
        "No PASS threshold was introduced.",
        "",
        "## Centre-derived coordinate scales",
        "",
        f"- ||c_X1||: `{scales['norm_c_X1']:.12f}`",
        f"- ||c_Y1||: `{scales['norm_c_Y1']:.12f}`",
        f"- k_x(center) = 1/||c_X1||: `{scales['k_x_center']:.12f}`",
        f"- k_y(center) = 1/||c_Y1||: `{scales['k_y_center']:.12f}`",
        f"- centre-predicted delta_x: "
        f"`{scales['delta_x_center_predicted_deg']:.9f} deg`",
        f"- centre-predicted delta_y: "
        f"`{scales['delta_y_center_predicted_deg']:.9f} deg`",
        f"- earlier observed delta_x: "
        f"`{scales['prior_delta_x_observed_deg']:.9f} deg`",
        f"- earlier observed delta_y: "
        f"`{scales['prior_delta_y_observed_deg']:.9f} deg`",
        "",
        "Differences between centre-predicted and observed plane angles are "
        "a direct measure of the independent zero-line directional mismatch.",
        "",
        "## Frozen rendering closure context",
        "",
        f"- X1 epsilon_power: `{closure[X1_ID]['epsilon_power']:.9f}`",
        f"- X1 Delta_R: `{closure[X1_ID]['delta_R_px']:.6f} px`",
        f"- X1 Delta_antipodal: "
        f"`{closure[X1_ID]['delta_antipodal_deg']:.6f} deg`",
        f"- Y1 epsilon_power: `{closure[Y1_ID]['epsilon_power']:.9f}`",
        f"- Y1 Delta_R: `{closure[Y1_ID]['delta_R_px']:.6f} px`",
        f"- Y1 Delta_antipodal: "
        f"`{closure[Y1_ID]['delta_antipodal_deg']:.6f} deg`",
        "",
        "The circle radii above did not enter reconstruction of G or L.",
        "",
        "## Fixed source-scale comparators",
        "",
        "| Candidate | k | kx(center)-k | ky(center)-k | "
        "sigma1-k | sigma2-k |",
        "|---|---:|---:|---:|---:|---:|",
    ]

    for scale_id in SCALE_IDS:
        item = (
            analysis[
                "fixed_source_scale_comparison"
            ][
                scale_id
            ]
        )

        sigma1 = (
            "undefined"
            if item[
                "sigma_1_minus_candidate"
            ]
            is None
            else f"{item['sigma_1_minus_candidate']:.9f}"
        )

        sigma2 = (
            "undefined"
            if item[
                "sigma_2_minus_candidate"
            ]
            is None
            else f"{item['sigma_2_minus_candidate']:.9f}"
        )

        lines.append(
            f"| `{scale_id}` | "
            f"{item['scale_k']:.12f} | "
            f"{item['k_x_center_minus_candidate']:.9f} | "
            f"{item['k_y_center_minus_candidate']:.9f} | "
            f"{sigma1} | "
            f"{sigma2} |"
        )

    lines += [
        "",
        "No candidate is selected merely because it is numerically nearest.",
        "",
        "## Holdout and scope",
        "",
        f"`{HOLDOUT_ID}` was not used to reconstruct or validate L.",
        "",
        "No unrestricted 3x3 projective fit, nonlinear map, reciprocal-spiral "
        "projection, S1, S1.5, or S2 is computed.",
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
            "Preregistered First Hand linear "
            "central-projective reconstruction."
        )
    )

    parser.add_argument(
        "--check-inputs",
        action="store_true",
        help=(
            "Verify frozen dependencies without "
            "reconstructing G or L."
        ),
    )

    args = parser.parse_args()

    if args.check_inputs:
        dependencies = (
            verify_dependencies()
        )

        print(
            "Stereographic plane-angle result: VERIFIED"
        )

        print(
            "Stereographic rendering comparator: VERIFIED"
        )

        print(
            "Linear central-projective protocol: PRESENT"
        )

        print(
            "L calibration curves: 2 (X1, Y1)"
        )

        print(
            "Independent line validation curves: 2 (YAXIS, Y0)"
        )

        print(
            "Scaffold excluded: YES"
        )

        print(
            "No linear construction map was reconstructed."
        )

        return 0

    analysis = (
        build_analysis()
    )

    write_outputs(
        analysis
    )

    linear = (
        analysis[
            "linear_map_reconstruction"
        ]
    )

    validation = (
        analysis[
            "independent_zero_line_validation"
        ]
    )

    scales = (
        analysis[
            "centre_scale_diagnostics"
        ]
    )

    print(
        "=" * 96
    )

    print(
        "FIRST HAND LINEAR CENTRAL-PROJECTIVE RECONSTRUCTION"
    )

    print(
        "=" * 96
    )

    print(
        "G ="
    )

    for row in linear[
        "G"
    ]:
        print(
            "  ["
            + ", ".join(
                f"{value:.12f}"
                for value in row
            )
            + "]"
        )

    print(
        f"det(G): {linear['det_G']:.12f}"
    )

    print(
        f"cond(G): {linear['condition_number_G']:.9f}"
    )

    print(
        f"inverse available: {linear['inverse_available']}"
    )

    if (
        linear[
            "inverse_available"
        ]
    ):
        print(
            "L ="
        )

        for row in linear[
            "L"
        ]:
            print(
                "  ["
                + ", ".join(
                    f"{value:.12f}"
                    for value in row
                )
                + "]"
            )

        print(
            "singular values:",
            ", ".join(
                f"{value:.12f}"
                for value
                in linear[
                    "singular_values_L"
                ]
            ),
        )

        print(
            "sigma1/sigma2:",
            f"{linear['singular_value_ratio']:.12f}",
        )

    print(
        "-" * 96
    )

    print(
        "eta_x (X1 predicts YAXIS):",
        f"{validation['eta_x_deg']:.9f} deg",
    )

    print(
        "eta_y (Y1 predicts Y0):",
        f"{validation['eta_y_deg']:.9f} deg",
    )

    print(
        "angle(g_x,g_y):",
        f"{validation['gamma_G_deg']:.9f} deg",
    )

    print(
        "|90-angle(g_x,g_y)|:",
        f"{validation['gamma_G_deviation_from_90_deg']:.9f} deg",
    )

    print(
        "-" * 96
    )

    print(
        "k_x(center):",
        f"{scales['k_x_center']:.12f}",
    )

    print(
        "k_y(center):",
        f"{scales['k_y_center']:.12f}",
    )

    print(
        "delta_x(center prediction):",
        f"{scales['delta_x_center_predicted_deg']:.9f} deg",
    )

    print(
        "delta_y(center prediction):",
        f"{scales['delta_y_center_predicted_deg']:.9f} deg",
    )

    print(
        "delta_x(observed line/circle):",
        f"{scales['prior_delta_x_observed_deg']:.9f} deg",
    )

    print(
        "delta_y(observed line/circle):",
        f"{scales['prior_delta_y_observed_deg']:.9f} deg",
    )

    print(
        f"Wrote {OUTPUT_JSON}"
    )

    print(
        f"Wrote {OUTPUT_REPORT}"
    )

    print(
        "No curve/refit, unrestricted projective map, "
        "spiral projection, or self-embedment score was computed."
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
