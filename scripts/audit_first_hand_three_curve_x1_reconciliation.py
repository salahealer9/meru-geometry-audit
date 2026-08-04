#!/usr/bin/env python3
"""First Hand three-curve X1 reconstruction and anisotropic reconciliation.

Post-hoc deterministic diagnostic.

Construction inputs:
    Y1      -> finite-offset magnitude
    YAXIS   -> x-family horizontal direction

Y0 is retained as frozen coordinate context.
X1 is excluded from construction and is used only as:
    - isotropic holdout comparison;
    - explicitly post-hoc anisotropic residual target.

No geometric input is refitted.
No numerical optimizer determines the anisotropic minimum.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]

DATA_DIR = (
    ROOT
    / "data"
    / "derived"
    / "first_hand_arm_of_god"
)

QC_DIR = DATA_DIR / "qc"

PROTOCOL = (
    ROOT
    / "docs"
    / "first_hand_three_curve_x1_reconciliation_protocol.md"
)

PLANE_JSON = (
    QC_DIR
    / "first_hand_stereographic_plane_angles.json"
)

PLANE_SEAL = (
    QC_DIR
    / "first_hand_stereographic_plane_angles.sha256"
)

Q1_LEDGER = (
    ROOT
    / "reports"
    / "first_hand_x1_source_semantic_question1_ledger.md"
)

Q2_LEDGER = (
    ROOT
    / "reports"
    / "first_hand_x1_source_semantic_question2_ledger.md"
)

OUTPUT_JSON = (
    QC_DIR
    / "first_hand_three_curve_x1_reconciliation.json"
)

OUTPUT_SWEEP_CSV = (
    QC_DIR
    / "first_hand_three_curve_x1_reconciliation_sweep.csv"
)

OUTPUT_SWEEP_PNG = (
    QC_DIR
    / "first_hand_three_curve_x1_reconciliation_sweep.png"
)

OUTPUT_REPORT = (
    ROOT
    / "reports"
    / "first_hand_three_curve_x1_reconciliation.md"
)


Y0_ID = "AOG-LM-P07-GC-Y0"
Y1_ID = "AOG-LM-P07-GC-Y1"
YAXIS_ID = "AOG-LM-P07-GC-YAXIS"
X1_ID = "AOG-LM-P07-GC-X1"

EXPECTED_PLANE_CLASS = (
    "preregistered_stereographic_plane_angle_reconstruction"
)

Q1_OUTCOME = "X1_LABEL_TRACE_CONFIRMED"
Q2_OUTCOME = "SCAFFOLD_ROLE_NOT_SUPPORTED_BY_SOURCE"

SWEEP_LOG10_K_MIN = -3.0
SWEEP_LOG10_K_MAX = 3.0
SWEEP_POINTS = 1201


def sha256_path(path: Path) -> str:
    digest = hashlib.sha256()

    with path.open("rb") as handle:
        for block in iter(
            lambda: handle.read(1 << 20),
            b"",
        ):
            digest.update(block)

    return digest.hexdigest()


def load_json(path: Path) -> dict[str, Any]:
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
    if not manifest_path.exists():
        raise RuntimeError(
            f"Missing SHA-256 manifest: {manifest_path}"
        )

    verified: dict[str, str] = {}

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
        target = ROOT / relative

        if not target.exists():
            raise RuntimeError(
                f"Sealed file missing: {relative}"
            )

        actual = sha256_path(target)

        if actual != expected:
            raise RuntimeError(
                "SHA-256 mismatch for "
                f"{relative}: expected {expected}, "
                f"got {actual}"
            )

        verified[relative] = expected

    for required in required_paths:
        relative = str(
            required.relative_to(ROOT)
        )

        if relative not in verified:
            raise RuntimeError(
                "Required frozen file absent from seal: "
                f"{relative}"
            )

    return verified


def unit_vector(
    values: np.ndarray,
) -> np.ndarray:
    vector = np.asarray(
        values,
        dtype=np.float64,
    )

    norm = float(
        np.linalg.norm(vector)
    )

    if not (
        math.isfinite(norm)
        and norm > 0.0
    ):
        raise ValueError(
            "Cannot normalize invalid vector."
        )

    return vector / norm


def stable_unoriented_plane_angle_deg(
    normal_a: np.ndarray,
    normal_b: np.ndarray,
) -> float:
    """Angle between unoriented 3-D planes in [0,90] degrees."""
    a = unit_vector(normal_a)
    b = unit_vector(normal_b)

    cross_norm = float(
        np.linalg.norm(
            np.cross(a, b)
        )
    )

    dot = abs(
        float(
            np.dot(a, b)
        )
    )

    return math.degrees(
        math.atan2(
            cross_norm,
            dot,
        )
    )


def predicted_plane_normal_from_g(
    g: np.ndarray,
) -> np.ndarray:
    """Plane g·(X,Y)-Z=0, represented with fixed +Z normal convention."""
    g = np.asarray(
        g,
        dtype=np.float64,
    )

    if g.shape != (2,):
        raise ValueError(
            "g must be a 2-vector."
        )

    return unit_vector(
        np.asarray(
            [
                -float(g[0]),
                -float(g[1]),
                1.0,
            ],
            dtype=np.float64,
        )
    )


def isotropic_candidates(
    y1_center: np.ndarray,
    yaxis_plane_normal: np.ndarray,
) -> dict[str, Any]:
    """Construct both isotropic X1 sign branches without using observed X1."""
    centre = np.asarray(
        y1_center,
        dtype=np.float64,
    )

    if centre.shape != (2,):
        raise ValueError(
            "Y1 centre must be a 2-vector."
        )

    r_y = float(
        np.linalg.norm(centre)
    )

    if not (
        math.isfinite(r_y)
        and r_y > 0.0
    ):
        raise ValueError(
            "Invalid Y1 centre magnitude."
        )

    k_y = 1.0 / r_y

    yaxis = unit_vector(
        np.asarray(
            yaxis_plane_normal,
            dtype=np.float64,
        )
    )

    if yaxis.shape != (3,):
        raise ValueError(
            "YAXIS plane normal must be a 3-vector."
        )

    horizontal = np.asarray(
        yaxis[:2],
        dtype=np.float64,
    )

    horizontal_norm = float(
        np.linalg.norm(horizontal)
    )

    if not (
        math.isfinite(horizontal_norm)
        and horizontal_norm > 0.0
    ):
        raise ValueError(
            "YAXIS has no horizontal plane-normal direction."
        )

    u_x = horizontal / horizontal_norm

    branches: dict[str, Any] = {}

    for name, sign in (
        ("plus_frozen_yaxis_normal", +1.0),
        ("minus_frozen_yaxis_normal", -1.0),
    ):
        g = sign * r_y * u_x

        branches[name] = {
            "sign": int(sign),
            "g_x": [
                float(g[0]),
                float(g[1]),
            ],
            "predicted_circle_center_u": float(g[0]),
            "predicted_circle_center_v": float(g[1]),
            "predicted_unit_plane_normal": [
                float(value)
                for value in predicted_plane_normal_from_g(g)
            ],
        }

    return {
        "r_y": r_y,
        "k_y": k_y,
        "u_x_from_frozen_yaxis": [
            float(u_x[0]),
            float(u_x[1]),
        ],
        "branches": branches,
    }


def attach_x1_holdout_residuals(
    isotropic: dict[str, Any],
    observed_x1_center: np.ndarray,
    observed_x1_normal: np.ndarray,
) -> dict[str, Any]:
    """Add X1 residuals after candidate construction."""
    centre = np.asarray(
        observed_x1_center,
        dtype=np.float64,
    )

    normal = unit_vector(
        np.asarray(
            observed_x1_normal,
            dtype=np.float64,
        )
    )

    result = json.loads(
        json.dumps(isotropic)
    )

    for branch in result[
        "branches"
    ].values():
        predicted_center = np.asarray(
            [
                branch[
                    "predicted_circle_center_u"
                ],
                branch[
                    "predicted_circle_center_v"
                ],
            ],
            dtype=np.float64,
        )

        predicted_normal = np.asarray(
            branch[
                "predicted_unit_plane_normal"
            ],
            dtype=np.float64,
        )

        branch[
            "x1_plane_angle_residual_deg"
        ] = stable_unoriented_plane_angle_deg(
            predicted_normal,
            normal,
        )

        branch[
            "x1_circle_center_displacement"
        ] = float(
            np.linalg.norm(
                predicted_center
                - centre
            )
        )

    return result


def analytic_anisotropic_branch(
    observed_x1_normal: np.ndarray,
    u_x: np.ndarray,
    sign: int,
) -> dict[str, Any]:
    """Exact minimum over r>0 for one sign branch.

    Predicted plane:
        (-sign*r*u_x[0], -sign*r*u_x[1], 1) / sqrt(1+r^2)

    Observed X1 plane normal is treated as unoriented.
    """
    if sign not in (-1, +1):
        raise ValueError(
            "sign must be +1 or -1."
        )

    n = unit_vector(
        np.asarray(
            observed_x1_normal,
            dtype=np.float64,
        )
    )

    u = unit_vector(
        np.asarray(
            u_x,
            dtype=np.float64,
        )
    )

    if u.shape != (2,):
        raise ValueError(
            "u_x must be a 2-vector."
        )

    horizontal_dot = float(
        np.dot(
            n[:2],
            u,
        )
    )

    A = (
        -float(sign)
        * horizontal_dot
    )

    B = float(
        n[2]
    )

    correlation_r0 = abs(B)
    correlation_rinf = abs(A)

    angle_r0 = math.degrees(
        math.acos(
            float(
                np.clip(
                    correlation_r0,
                    0.0,
                    1.0,
                )
            )
        )
    )

    angle_rinf = math.degrees(
        math.acos(
            float(
                np.clip(
                    correlation_rinf,
                    0.0,
                    1.0,
                )
            )
        )
    )

    finite_interior = (
        A * B > 0.0
    )

    optimal_r: float | None
    optimal_k: float | None

    if finite_interior:
        optimal_r = A / B

        if not (
            math.isfinite(optimal_r)
            and optimal_r > 0.0
        ):
            raise RuntimeError(
                "Invalid analytic interior optimum."
            )

        maximum_correlation = math.sqrt(
            A * A
            + B * B
        )

        optimum_class = (
            "FINITE_INTERIOR"
        )

        optimal_k = (
            1.0
            / optimal_r
        )

    elif (
        correlation_r0
        >= correlation_rinf
    ):
        maximum_correlation = (
            correlation_r0
        )

        optimum_class = (
            "LIMIT_R_TO_ZERO"
        )

        optimal_r = None
        optimal_k = None

    else:
        maximum_correlation = (
            correlation_rinf
        )

        optimum_class = (
            "LIMIT_R_TO_INFINITY"
        )

        optimal_r = None
        optimal_k = None

    maximum_correlation = float(
        np.clip(
            maximum_correlation,
            0.0,
            1.0,
        )
    )

    minimum_angle = math.degrees(
        math.acos(
            maximum_correlation
        )
    )

    return {
        "sign": sign,
        "A": A,
        "B": B,
        "horizontal_dot_observed_x1_with_yaxis_direction": (
            horizontal_dot
        ),
        "optimum_class": optimum_class,
        "optimal_r_x": optimal_r,
        "optimal_k_x": optimal_k,
        "maximum_absolute_plane_correlation": (
            maximum_correlation
        ),
        "minimum_x1_plane_angle_residual_deg": (
            minimum_angle
        ),
        "limit_r_to_zero_plane_angle_deg": (
            angle_r0
        ),
        "limit_r_to_infinity_plane_angle_deg": (
            angle_rinf
        ),
    }


def sweep_branch_angles(
    observed_x1_normal: np.ndarray,
    u_x: np.ndarray,
    sign: int,
    log10_k_values: np.ndarray,
) -> np.ndarray:
    n = unit_vector(
        np.asarray(
            observed_x1_normal,
            dtype=np.float64,
        )
    )

    u = unit_vector(
        np.asarray(
            u_x,
            dtype=np.float64,
        )
    )

    angles = []

    for log10_k in log10_k_values:
        k = 10.0 ** float(
            log10_k
        )

        r = 1.0 / k

        g = (
            float(sign)
            * r
            * u
        )

        predicted = (
            predicted_plane_normal_from_g(
                g
            )
        )

        angles.append(
            stable_unoriented_plane_angle_deg(
                predicted,
                n,
            )
        )

    return np.asarray(
        angles,
        dtype=np.float64,
    )


def finite_circle_center(
    plane_result: dict[str, Any],
    curve_id: str,
) -> np.ndarray:
    item = (
        plane_result[
            "reconstructed_planes"
        ][curve_id]
    )

    if (
        item.get("branch")
        != "stereographic_finite_circle"
    ):
        raise RuntimeError(
            f"{curve_id} is not the expected finite-circle branch."
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


def frozen_plane_normal(
    plane_result: dict[str, Any],
    curve_id: str,
) -> np.ndarray:
    item = (
        plane_result[
            "reconstructed_planes"
        ][curve_id]
    )

    return unit_vector(
        np.asarray(
            item[
                "unit_plane_normal"
            ],
            dtype=np.float64,
        )
    )


def verify_semantic_ledger(
    path: Path,
    required_outcome: str,
) -> str:
    if not path.exists():
        raise RuntimeError(
            f"Missing semantic ledger: {path}"
        )

    text = path.read_text(
        encoding="utf-8",
    )

    selected = (
        f"[X] {required_outcome}"
    )

    if selected not in text:
        raise RuntimeError(
            f"Required frozen semantic outcome absent: "
            f"{required_outcome}"
        )

    return sha256_path(path)


def rendering_context(
    plane_result: dict[str, Any],
) -> dict[str, Any]:
    context = (
        plane_result[
            "rendering_closure_context"
        ]
    )

    output: dict[str, Any] = {}

    for curve_id in (
        Y1_ID,
        X1_ID,
    ):
        item = context[
            curve_id
        ]

        output[curve_id] = {
            "epsilon_power": float(
                item[
                    "epsilon_power"
                ]
            ),
            "delta_R_px": float(
                item[
                    "delta_R_px"
                ]
            ),
            "delta_antipodal_deg": float(
                item[
                    "delta_antipodal_deg"
                ]
            ),
        }

    return output


def verify_dependencies() -> dict[str, Any]:
    if not PROTOCOL.exists():
        raise RuntimeError(
            f"Missing protocol: {PROTOCOL}"
        )

    verify_sha256_manifest(
        PLANE_SEAL,
        (
            PLANE_JSON,
        ),
    )

    plane_result = load_json(
        PLANE_JSON
    )

    if (
        plane_result.get(
            "analysis_class"
        )
        != EXPECTED_PLANE_CLASS
    ):
        raise RuntimeError(
            "Unexpected stereographic plane-angle analysis class."
        )

    expected_ids = {
        Y0_ID,
        Y1_ID,
        YAXIS_ID,
        X1_ID,
    }

    actual_ids = set(
        plane_result[
            "reconstructed_planes"
        ]
    )

    if actual_ids != expected_ids:
        raise RuntimeError(
            "Frozen reconstructed-plane set changed."
        )

    y1_item = (
        plane_result[
            "reconstructed_planes"
        ][Y1_ID]
    )

    x1_item = (
        plane_result[
            "reconstructed_planes"
        ][X1_ID]
    )

    yaxis_item = (
        plane_result[
            "reconstructed_planes"
        ][YAXIS_ID]
    )

    if (
        y1_item.get("branch")
        != "stereographic_finite_circle"
    ):
        raise RuntimeError(
            "Y1 is not the expected finite-circle branch."
        )

    if (
        x1_item.get("branch")
        != "stereographic_finite_circle"
    ):
        raise RuntimeError(
            "X1 is not the expected finite-circle branch."
        )

    if (
        yaxis_item.get("branch")
        != "stereographic_diameter_line"
    ):
        raise RuntimeError(
            "YAXIS is not the expected diameter-line branch."
        )

    q1_sha = verify_semantic_ledger(
        Q1_LEDGER,
        Q1_OUTCOME,
    )

    q2_sha = verify_semantic_ledger(
        Q2_LEDGER,
        Q2_OUTCOME,
    )

    # Validate the exact frozen fields needed later without performing
    # the new reconstruction.
    for item, keys in (
        (
            y1_item,
            (
                "normalized_circle_center_u",
                "normalized_circle_center_v",
                "unit_plane_normal",
            ),
        ),
        (
            x1_item,
            (
                "normalized_circle_center_u",
                "normalized_circle_center_v",
                "unit_plane_normal",
            ),
        ),
        (
            yaxis_item,
            (
                "unit_plane_normal",
            ),
        ),
    ):
        for key in keys:
            if key not in item:
                raise RuntimeError(
                    f"Required frozen field absent: {key}"
                )

    return {
        "plane_result": plane_result,
        "protocol_sha256": sha256_path(
            PROTOCOL
        ),
        "plane_sha256": sha256_path(
            PLANE_JSON
        ),
        "q1_sha256": q1_sha,
        "q2_sha256": q2_sha,
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

    y1_center = finite_circle_center(
        plane_result,
        Y1_ID,
    )

    x1_center = finite_circle_center(
        plane_result,
        X1_ID,
    )

    yaxis_normal = frozen_plane_normal(
        plane_result,
        YAXIS_ID,
    )

    x1_normal = frozen_plane_normal(
        plane_result,
        X1_ID,
    )

    isotropic_constructed = (
        isotropic_candidates(
            y1_center,
            yaxis_normal,
        )
    )

    isotropic = (
        attach_x1_holdout_residuals(
            isotropic_constructed,
            x1_center,
            x1_normal,
        )
    )

    u_x = np.asarray(
        isotropic[
            "u_x_from_frozen_yaxis"
        ],
        dtype=np.float64,
    )

    anisotropic = {}

    for branch_name, sign in (
        (
            "plus_frozen_yaxis_normal",
            +1,
        ),
        (
            "minus_frozen_yaxis_normal",
            -1,
        ),
    ):
        anisotropic[
            branch_name
        ] = (
            analytic_anisotropic_branch(
                x1_normal,
                u_x,
                sign,
            )
        )

    branch_minima = {
        name: float(
            item[
                "minimum_x1_plane_angle_residual_deg"
            ]
        )
        for name, item in anisotropic.items()
    }

    existential_best = min(
        branch_minima.values()
    )

    coordinate_context = (
        plane_result[
            "image_derived_coordinate_separations"
        ]
    )

    return {
        "checkpoint": (
            "first_hand_three_curve_x1_reconciliation_v0.8"
        ),
        "analysis_class": (
            "deterministic_post_hoc_three_curve_x1_reconciliation"
        ),
        "analysis_status": (
            "post_hoc_coordinate_consistency_diagnostic"
        ),
        "provenance": {
            "protocol_path": str(
                PROTOCOL.relative_to(ROOT)
            ),
            "protocol_sha256": (
                dependencies[
                    "protocol_sha256"
                ]
            ),
            "plane_result_path": str(
                PLANE_JSON.relative_to(ROOT)
            ),
            "plane_result_sha256": (
                dependencies[
                    "plane_sha256"
                ]
            ),
            "question1_ledger_path": str(
                Q1_LEDGER.relative_to(ROOT)
            ),
            "question1_ledger_sha256": (
                dependencies[
                    "q1_sha256"
                ]
            ),
            "question2_ledger_path": str(
                Q2_LEDGER.relative_to(ROOT)
            ),
            "question2_ledger_sha256": (
                dependencies[
                    "q2_sha256"
                ]
            ),
        },
        "source_semantic_prerequisites": {
            "x1_label_trace_outcome": (
                Q1_OUTCOME
            ),
            "x1_scaffold_role_outcome": (
                Q2_OUTCOME
            ),
        },
        "construction_partition": {
            "finite_offset_magnitude_input": (
                Y1_ID
            ),
            "x_direction_input": (
                YAXIS_ID
            ),
            "y_zero_line_context": (
                Y0_ID
            ),
            "x1_used_to_construct_isotropic_candidate": False,
            "x1_used_as_isotropic_holdout": True,
            "x1_used_as_post_hoc_anisotropic_residual_target": True,
            "scaffold_used": False,
        },
        "frozen_coordinate_context": {
            "delta_x_deg": float(
                coordinate_context[
                    "delta_x_deg"
                ]
            ),
            "delta_y_deg": float(
                coordinate_context[
                    "delta_y_deg"
                ]
            ),
            "k_x_prior_descriptor": float(
                coordinate_context[
                    "k_x_tan_delta_x"
                ]
            ),
            "k_y_prior_descriptor": float(
                coordinate_context[
                    "k_y_tan_delta_y"
                ]
            ),
        },
        "observed_x1": {
            "normalized_circle_center_u": float(
                x1_center[0]
            ),
            "normalized_circle_center_v": float(
                x1_center[1]
            ),
            "unit_plane_normal": [
                float(value)
                for value in x1_normal
            ],
        },
        "isotropic_three_curve_candidate": (
            isotropic
        ),
        "anisotropic_scale_reconciliation": {
            "parameter": (
                "r_x > 0 with k_x = 1/r_x"
            ),
            "horizontal_direction_frozen_from": (
                YAXIS_ID
            ),
            "optimizer_used": False,
            "branches": anisotropic,
            "minimum_over_both_unoriented_sign_branches_deg": (
                existential_best
            ),
            "branch_selection_claimed": False,
        },
        "sweep_specification": {
            "log10_k_min": (
                SWEEP_LOG10_K_MIN
            ),
            "log10_k_max": (
                SWEEP_LOG10_K_MAX
            ),
            "points": (
                SWEEP_POINTS
            ),
            "primary_minimum_determined_by_sweep": False,
        },
        "rendering_closure_context": (
            rendering_context(
                plane_result
            )
        ),
        "interpretation_boundary": (
            "The isotropic candidate is an explicitly post-hoc "
            "three-curve prediction with two mandatory orientation "
            "branches. The anisotropic analysis asks only whether x-scale "
            "freedom can reconcile the source-confirmed X1 stroke with "
            "the frozen YAXIS-derived x-family direction. The analytic "
            "minimum is geometrically related to earlier x-family "
            "directional diagnostics and is not independent statistical "
            "evidence. No cause of any residual incompatibility is inferred."
        ),
        "scope": {
            "curve_refits": 0,
            "circle_refits": 0,
            "line_refits": 0,
            "optimizer_calls": 0,
            "general_2x2_refit": False,
            "general_3x3_fit": False,
            "nonlinear_fit": False,
            "x1_reclassified_as_scaffold": False,
            "construction_scale_candidate_selected": False,
            "spiral_projection_computed": False,
            "s1_computed": False,
            "s1_5_computed": False,
            "s2_computed": False,
        },
    }


def write_sweep(
    analysis: dict[str, Any],
) -> None:
    plane_result = load_json(
        PLANE_JSON
    )

    x1_normal = frozen_plane_normal(
        plane_result,
        X1_ID,
    )

    u_x = np.asarray(
        analysis[
            "isotropic_three_curve_candidate"
        ][
            "u_x_from_frozen_yaxis"
        ],
        dtype=np.float64,
    )

    log10_k = np.linspace(
        SWEEP_LOG10_K_MIN,
        SWEEP_LOG10_K_MAX,
        SWEEP_POINTS,
        dtype=np.float64,
    )

    plus_angles = (
        sweep_branch_angles(
            x1_normal,
            u_x,
            +1,
            log10_k,
        )
    )

    minus_angles = (
        sweep_branch_angles(
            x1_normal,
            u_x,
            -1,
            log10_k,
        )
    )

    OUTPUT_SWEEP_CSV.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with OUTPUT_SWEEP_CSV.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as handle:
        writer = csv.writer(
            handle
        )

        writer.writerow(
            [
                "log10_k_x",
                "k_x",
                "r_x",
                "plus_frozen_yaxis_normal_residual_deg",
                "minus_frozen_yaxis_normal_residual_deg",
            ]
        )

        for q, plus, minus in zip(
            log10_k,
            plus_angles,
            minus_angles,
            strict=True,
        ):
            k = 10.0 ** float(q)
            r = 1.0 / k

            writer.writerow(
                [
                    f"{float(q):.12f}",
                    f"{k:.16g}",
                    f"{r:.16g}",
                    f"{float(plus):.12f}",
                    f"{float(minus):.12f}",
                ]
            )

    fig, ax = plt.subplots(
        figsize=(9.0, 5.5)
    )

    ax.plot(
        log10_k,
        plus_angles,
        label="+ frozen YAXIS normal",
    )

    ax.plot(
        log10_k,
        minus_angles,
        label="- frozen YAXIS normal",
    )

    ax.set_xlabel(
        "log10(k_x)"
    )

    ax.set_ylabel(
        "Unoriented X1 plane-angle residual (deg)"
    )

    ax.set_title(
        "First Hand X1 anisotropic scale reconciliation"
    )

    ax.legend()

    fig.tight_layout()

    fig.savefig(
        OUTPUT_SWEEP_PNG,
        dpi=180,
    )

    plt.close(fig)


def render_report(
    analysis: dict[str, Any],
) -> str:
    iso = (
        analysis[
            "isotropic_three_curve_candidate"
        ]
    )

    aniso = (
        analysis[
            "anisotropic_scale_reconciliation"
        ]
    )

    closure = (
        analysis[
            "rendering_closure_context"
        ]
    )

    lines = [
        "# First Hand three-curve X1 reconstruction and anisotropic reconciliation",
        "",
        "**Status:** deterministic post-hoc coordinate-consistency diagnostic",
        "",
        "No source curve, line, circle, rendering model, or projective map was refitted.",
        "",
        "## Source-semantic prerequisites",
        "",
        f"- X1 label/trace: `{Q1_OUTCOME}`",
        f"- X1 scaffold role: `{Q2_OUTCOME}`",
        "",
        "## Three-curve isotropic candidate",
        "",
        f"- r_y from frozen Y1 centre: `{iso['r_y']:.12f}`",
        f"- k_y = 1/r_y: `{iso['k_y']:.12f}`",
        "",
        "YAXIS supplies only an unoriented horizontal normal, so both sign branches are mandatory.",
        "",
    ]

    for name, item in iso[
        "branches"
    ].items():
        lines.extend(
            [
                f"### {name}",
                "",
                (
                    "- predicted centre: "
                    f"`({item['predicted_circle_center_u']:.12f}, "
                    f"{item['predicted_circle_center_v']:.12f})`"
                ),
                (
                    "- X1 plane-angle residual: "
                    f"`{item['x1_plane_angle_residual_deg']:.9f} deg`"
                ),
                (
                    "- X1 centre displacement: "
                    f"`{item['x1_circle_center_displacement']:.12f}`"
                ),
                "",
            ]
        )

    lines.extend(
        [
            "No sign branch is selected as the source-correct orientation from X1 fit quality.",
            "",
            "## Anisotropic scale reconciliation",
            "",
            "Only x-scale is released. The YAXIS-derived horizontal direction remains fixed.",
            "",
        ]
    )

    for name, item in aniso[
        "branches"
    ].items():
        lines.extend(
            [
                f"### {name}",
                "",
                f"- optimum class: `{item['optimum_class']}`",
                (
                    "- global minimum plane-angle residual: "
                    f"`{item['minimum_x1_plane_angle_residual_deg']:.9f} deg`"
                ),
                (
                    "- r -> 0 residual: "
                    f"`{item['limit_r_to_zero_plane_angle_deg']:.9f} deg`"
                ),
                (
                    "- r -> infinity residual: "
                    f"`{item['limit_r_to_infinity_plane_angle_deg']:.9f} deg`"
                ),
            ]
        )

        if (
            item[
                "optimal_r_x"
            ]
            is not None
        ):
            lines.extend(
                [
                    f"- optimal r_x: `{item['optimal_r_x']:.12f}`",
                    f"- optimal k_x: `{item['optimal_k_x']:.12f}`",
                ]
            )

        lines.append("")

    lines.extend(
        [
            (
                "- minimum over both unoriented sign branches: "
                f"`{aniso['minimum_over_both_unoriented_sign_branches_deg']:.9f} deg`"
            ),
            "",
            "The analytic result, not the plotted sweep, determines the global minimum.",
            "",
            "## Rendering-closure context",
            "",
            f"- Y1 Delta_R: `{closure[Y1_ID]['delta_R_px']:.6f} px`",
            (
                "- Y1 antipodal deviation: "
                f"`{closure[Y1_ID]['delta_antipodal_deg']:.6f} deg`"
            ),
            f"- X1 Delta_R: `{closure[X1_ID]['delta_R_px']:.6f} px`",
            (
                "- X1 antipodal deviation: "
                f"`{closure[X1_ID]['delta_antipodal_deg']:.6f} deg`"
            ),
            "",
            "Y1 is the sole finite-offset magnitude input to the isotropic candidate and carries the previously frozen weaker rendering closure.",
            "",
            "## Interpretation boundary",
            "",
            "This checkpoint tests whether equal scale, and then arbitrary positive x-scale, can reconcile the source-confirmed X1 stroke with the YAXIS-derived x-family direction. It does not explain the cause of any incompatibility and does not assign X1 a scaffold role.",
            "",
        ]
    )

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

    write_sweep(
        analysis
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
            "First Hand three-curve X1 reconstruction and "
            "anisotropic scale reconciliation."
        )
    )

    parser.add_argument(
        "--check-inputs",
        action="store_true",
        help=(
            "Verify frozen dependencies without constructing "
            "the isotropic or anisotropic result."
        ),
    )

    args = parser.parse_args()

    if args.check_inputs:
        dependencies = (
            verify_dependencies()
        )

        plane_result = (
            dependencies[
                "plane_result"
            ]
        )

        print(
            "Stereographic plane-angle result: VERIFIED"
        )

        print(
            "Question-1 semantic ledger:",
            Q1_OUTCOME,
        )

        print(
            "Question-2 semantic ledger:",
            Q2_OUTCOME,
        )

        print(
            "Required frozen curves:",
            len(
                plane_result[
                    "reconstructed_planes"
                ]
            ),
        )

        print(
            "Isotropic construction inputs: Y1 + YAXIS"
        )

        print(
            "X1 construction input: NO"
        )

        print(
            "Mandatory isotropic sign branches: 2"
        )

        print(
            "Anisotropic primary minimum method: ANALYTIC"
        )

        print(
            "No reconstruction or X1 residual was computed."
        )

        return 0

    analysis = (
        build_analysis()
    )

    write_outputs(
        analysis
    )

    iso = (
        analysis[
            "isotropic_three_curve_candidate"
        ]
    )

    aniso = (
        analysis[
            "anisotropic_scale_reconciliation"
        ]
    )

    print("=" * 96)
    print(
        "FIRST HAND THREE-CURVE X1 RECONSTRUCTION "
        "AND ANISOTROPIC RECONCILIATION"
    )
    print("=" * 96)

    print(
        "r_y:",
        f"{iso['r_y']:.12f}",
    )

    print(
        "k_y:",
        f"{iso['k_y']:.12f}",
    )

    print("-" * 96)
    print("ISOTROPIC TWO-BRANCH PREDICTION")

    for name, item in iso[
        "branches"
    ].items():
        print(name)

        print(
            "  predicted centre:",
            f"({item['predicted_circle_center_u']:.12f}, "
            f"{item['predicted_circle_center_v']:.12f})",
        )

        print(
            "  X1 plane residual:",
            f"{item['x1_plane_angle_residual_deg']:.9f} deg",
        )

        print(
            "  X1 centre displacement:",
            f"{item['x1_circle_center_displacement']:.12f}",
        )

    print("-" * 96)
    print("ANISOTROPIC GLOBAL SCALE RECONCILIATION")

    for name, item in aniso[
        "branches"
    ].items():
        print(name)

        print(
            "  optimum class:",
            item[
                "optimum_class"
            ],
        )

        if (
            item[
                "optimal_r_x"
            ]
            is not None
        ):
            print(
                "  optimal r_x:",
                f"{item['optimal_r_x']:.12f}",
            )

            print(
                "  optimal k_x:",
                f"{item['optimal_k_x']:.12f}",
            )

        print(
            "  minimum X1 residual:",
            f"{item['minimum_x1_plane_angle_residual_deg']:.9f} deg",
        )

        print(
            "  r->0 residual:",
            f"{item['limit_r_to_zero_plane_angle_deg']:.9f} deg",
        )

        print(
            "  r->inf residual:",
            f"{item['limit_r_to_infinity_plane_angle_deg']:.9f} deg",
        )

    print("-" * 96)

    print(
        "minimum over both sign branches:",
        f"{aniso['minimum_over_both_unoriented_sign_branches_deg']:.9f} deg",
    )

    print(
        f"Wrote {OUTPUT_JSON}"
    )

    print(
        f"Wrote {OUTPUT_SWEEP_CSV}"
    )

    print(
        f"Wrote {OUTPUT_SWEEP_PNG}"
    )

    print(
        f"Wrote {OUTPUT_REPORT}"
    )

    print(
        "No optimizer, map refit, scaffold reassignment, "
        "spiral projection, or self-embedment score was computed."
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
