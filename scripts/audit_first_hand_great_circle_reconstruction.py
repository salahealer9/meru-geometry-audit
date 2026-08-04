#!/usr/bin/env python3
"""Limb-constrained projected-great-circle reconstruction for First Hand page 7.

This implementation follows the protocol frozen before numerical
great-circle reconstruction.

Only the four source-labelled curves are fitted.  The unlabelled
scaffold remains outside fitting, scale selection, branch selection,
and projective calibration.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
from pathlib import Path
from typing import Any, Sequence

import numpy as np
from scipy.optimize import minimize


ROOT = Path(__file__).resolve().parents[1]

root_text = str(ROOT)

if root_text not in sys.path:
    sys.path.insert(
        0,
        root_text,
    )

from scripts import audit_first_hand_curve_geometry as base
from scripts import audit_first_hand_curve_geometry_qc as qc_runner
from scripts import audit_first_hand_expanded_neutral_geometry as expanded


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
    / "first_hand_great_circle_reconstruction_protocol.md"
)

MORPHOLOGY_JSON = (
    QC_DIR
    / "first_hand_curve_morphology_census.json"
)

MORPHOLOGY_SEAL = (
    QC_DIR
    / "first_hand_curve_morphology_census.sha256"
)

OUTPUT_JSON = (
    QC_DIR
    / "first_hand_great_circle_reconstruction.json"
)

OUTPUT_REPORT = (
    ROOT
    / "reports"
    / "first_hand_great_circle_reconstruction.md"
)

FIT_IDS = (
    "AOG-LM-P07-GC-Y0",
    "AOG-LM-P07-GC-Y1",
    "AOG-LM-P07-GC-YAXIS",
    "AOG-LM-P07-GC-X1",
)

HOLDOUT_ID = (
    "AOG-LM-P07-GC-SCAFFOLD-UR-UC-X1LL-LL"
)

LR_SHARED_ID = (
    "AOG-LM-P07-RIM-NODE-LR-SHARED"
)

CENTRAL_ID = (
    "AOG-LM-P07-CENTRAL-REFERENCE-NODE"
)

UPPER_CROSSING_ID = (
    "AOG-LM-P07-UPPER-INTERIOR-CROSSING"
)

RIM_IDS = (
    "AOG-LM-P07-RIM-NODE-UL",
    "AOG-LM-P07-RIM-NODE-UR",
    "AOG-LM-P07-RIM-NODE-R",
    "AOG-LM-P07-RIM-NODE-LR-SHARED",
    "AOG-LM-P07-RIM-NODE-LL",
    "AOG-LM-P07-RIM-NODE-L",
)

PHI_SEEDS_DEG = tuple(
    float(value)
    for value in range(
        0,
        180,
        15,
    )
)

Q_SEEDS = (
    0.00,
    0.10,
    0.25,
    0.50,
    0.75,
    0.95,
)

PRIMARY_SPACING_PX = 2.0
SENSITIVITY_SPACINGS_PX = (
    1.0,
    4.0,
)

COMPATIBILITY_RMS_PX = 2.0

Q_LINE_EPS = 1.0e-10
NORMAL_DEDUP_TOL = 1.0e-12
INTERSECTION_DEDUP_TOL = 1.0e-9

NEWTON_ITERATIONS = 14
NEWTON_MAX_STEP = 0.5

OPTIMIZER_MAXITER = 500
OPTIMIZER_FTOL = 1.0e-14
OPTIMIZER_GTOL = 1.0e-10


def sha256_path(
    path: Path,
) -> str:
    digest = hashlib.sha256()

    with path.open(
        "rb"
    ) as handle:
        for block in iter(
            lambda: handle.read(
                1 << 20
            ),
            b"",
        ):
            digest.update(
                block
            )

    return digest.hexdigest()


def canonical_json_sha256(
    value: Any,
) -> str:
    payload = json.dumps(
        value,
        sort_keys=True,
        separators=(
            ",",
            ":",
        ),
        allow_nan=False,
    ).encode(
        "utf-8"
    )

    return hashlib.sha256(
        payload
    ).hexdigest()


def load_frozen_morphology() -> dict[str, Any]:
    """Verify and load the frozen neutral morphology census."""
    qc_runner.verify_sha256_manifest(
        MORPHOLOGY_SEAL
    )

    if not MORPHOLOGY_JSON.exists():
        raise RuntimeError(
            "Frozen morphology result is missing."
        )

    result = json.loads(
        MORPHOLOGY_JSON.read_text(
            encoding="utf-8",
        )
    )

    if (
        result.get(
            "analysis_class"
        )
        !=
        "post_hoc_model_neutral_morphology_census"
    ):
        raise RuntimeError(
            "Unexpected morphology result class."
        )

    return result


def verify_dependencies() -> dict[str, Any]:
    """Verify all frozen dependencies without fitting great circles."""
    if not PROTOCOL_PATH.exists():
        raise RuntimeError(
            f"Missing frozen protocol: {PROTOCOL_PATH}"
        )

    raw = (
        base.verify_input_seal()
    )

    qc = (
        qc_runner.verify_qc_derivative()
    )

    morphology = (
        load_frozen_morphology()
    )

    limb = (
        base.load_frozen_limb_reference()
    )

    frozen_limb = (
        morphology[
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
                limb[key]
            ),
            float(
                frozen_limb[key]
            ),
            rel_tol=0.0,
            abs_tol=1.0e-12,
        ):
            raise RuntimeError(
                "Frozen limb changed for "
                f"{key}."
            )

    if (
        set(FIT_IDS)
        != set(
            base.CALIBRATION_IDS
        )
    ):
        raise RuntimeError(
            "Great-circle fit set does not "
            "match the frozen labelled-curve set."
        )

    if (
        HOLDOUT_ID
        != base.HOLDOUT_ID
    ):
        raise RuntimeError(
            "Unexpected scaffold holdout ID."
        )

    if (
        HOLDOUT_ID
        in FIT_IDS
    ):
        raise RuntimeError(
            "Scaffold holdout entered calibration set."
        )

    return {
        "raw_curve_inputs": raw,
        "qc_derivative": qc,
        "morphology_sha256": (
            sha256_path(
                MORPHOLOGY_JSON
            )
        ),
        "protocol_sha256": (
            sha256_path(
                PROTOCOL_PATH
            )
        ),
        "frozen_limb": limb,
    }


def pixel_to_normalized(
    points_px: np.ndarray,
    limb: dict[str, float],
) -> np.ndarray:
    """Convert crop pixels to y-up unit-limb coordinates."""
    center = np.asarray(
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

    result = (
        np.asarray(
            points_px,
            dtype=np.float64,
        )
        - center[None, :]
    ) / radius

    result[
        :,
        1,
    ] *= -1.0

    return result


def normalized_to_pixel(
    points_uv: np.ndarray,
    limb: dict[str, float],
) -> np.ndarray:
    """Convert y-up unit-limb coordinates back to crop pixels."""
    points_uv = np.asarray(
        points_uv,
        dtype=np.float64,
    )

    radius = float(
        limb[
            "radius_px"
        ]
    )

    cx = float(
        limb[
            "center_x_px"
        ]
    )

    cy = float(
        limb[
            "center_y_px"
        ]
    )

    return np.column_stack(
        (
            cx
            + radius
            * points_uv[:, 0],
            cy
            - radius
            * points_uv[:, 1],
        )
    )


def canonical_phi(
    phi: float,
) -> float:
    """Canonical unoriented ellipse angle in [0, pi)."""
    value = math.fmod(
        float(phi),
        math.pi,
    )

    if value < 0.0:
        value += math.pi

    if math.isclose(
        value,
        math.pi,
        rel_tol=0.0,
        abs_tol=1.0e-14,
    ):
        value = 0.0

    return value


def ellipse_axes(
    phi: float,
) -> tuple[
    np.ndarray,
    np.ndarray,
]:
    """Return unit major/minor directions for one projected ellipse."""
    phi = canonical_phi(
        phi
    )

    c = math.cos(
        phi
    )

    s = math.sin(
        phi
    )

    major = np.asarray(
        [
            c,
            s,
        ],
        dtype=np.float64,
    )

    minor = np.asarray(
        [
            -s,
            c,
        ],
        dtype=np.float64,
    )

    return (
        major,
        minor,
    )


def projected_great_circle_points(
    phi: float,
    q: float,
    t: np.ndarray,
) -> np.ndarray:
    """Evaluate the normalized orthographic great-circle projection."""
    if not (
        0.0
        <= q
        <= 1.0
    ):
        raise ValueError(
            "q must lie in [0, 1]."
        )

    major, minor = (
        ellipse_axes(
            phi
        )
    )

    t = np.asarray(
        t,
        dtype=np.float64,
    )

    return (
        np.cos(t)[:, None]
        * major[None, :]
        + q
        * np.sin(t)[:, None]
        * minor[None, :]
    )


def _distance_from_local_candidates(
    x: np.ndarray,
    y: np.ndarray,
    q: float,
    t: np.ndarray,
) -> np.ndarray:
    """Squared local-coordinate distances for candidate ellipse parameters."""
    c = np.cos(
        t
    )

    s = np.sin(
        t
    )

    dx = (
        c
        - x[:, None]
    )

    dy = (
        q
        * s
        - y[:, None]
    )

    return (
        dx * dx
        + dy * dy
    )


def projected_great_circle_distance_normalized(
    points_uv: np.ndarray,
    phi: float,
    q: float,
) -> np.ndarray:
    """Nearest Euclidean distance to the complete normalized ellipse.

    A vectorized closest-parameter Newton solve is initialized from
    several geometrically distinct deterministic seeds.  Cardinal
    ellipse points are retained as explicit candidates.

    q=0 is treated exactly as the closed diameter segment.
    """
    points_uv = np.asarray(
        points_uv,
        dtype=np.float64,
    )

    if (
        points_uv.ndim != 2
        or points_uv.shape[1] != 2
    ):
        raise ValueError(
            "points_uv must have shape (n, 2)."
        )

    if not (
        math.isfinite(q)
        and 0.0
        <= q
        <= 1.0
    ):
        raise ValueError(
            "q must be finite and in [0, 1]."
        )

    major, minor = (
        ellipse_axes(
            phi
        )
    )

    x = (
        points_uv
        @ major
    )

    y = (
        points_uv
        @ minor
    )

    if q <= Q_LINE_EPS:
        closest_x = np.clip(
            x,
            -1.0,
            1.0,
        )

        dx = (
            x
            - closest_x
        )

        return np.sqrt(
            dx * dx
            + y * y
        )

    # A point on the parametric ellipse has
    # t = atan2(y/q, x).  This is therefore the natural
    # first Newton seed for points close to the source locus.
    t_parametric = np.arctan2(
        y / q,
        x,
    )

    t_polar = np.arctan2(
        y,
        x,
    )

    candidates = np.column_stack(
        (
            t_parametric,
            t_polar,
            t_parametric
            + 0.5
            * math.pi,
            t_parametric
            - 0.5
            * math.pi,
        )
    )

    for _ in range(
        NEWTON_ITERATIONS
    ):
        s = np.sin(
            candidates
        )

        c = np.cos(
            candidates
        )

        # Derivative of squared distance / 2.
        gradient = (
            (
                q * q
                - 1.0
            )
            * s
            * c
            + x[:, None]
            * s
            - q
            * y[:, None]
            * c
        )

        curvature = (
            (
                q * q
                - 1.0
            )
            * (
                c * c
                - s * s
            )
            + x[:, None]
            * c
            + q
            * y[:, None]
            * s
        )

        safe = (
            np.abs(
                curvature
            )
            > 1.0e-12
        )

        step = np.zeros_like(
            candidates
        )

        step[
            safe
        ] = (
            gradient[
                safe
            ]
            / curvature[
                safe
            ]
        )

        step = np.clip(
            step,
            -NEWTON_MAX_STEP,
            NEWTON_MAX_STEP,
        )

        candidates -= step

    cardinal = np.tile(
        np.asarray(
            [
                0.0,
                0.5
                * math.pi,
                math.pi,
                1.5
                * math.pi,
            ],
            dtype=np.float64,
        ),
        (
            len(
                points_uv
            ),
            1,
        ),
    )

    all_candidates = np.column_stack(
        (
            candidates,
            cardinal,
        )
    )

    squared = (
        _distance_from_local_candidates(
            x,
            y,
            q,
            all_candidates,
        )
    )

    best = np.min(
        squared,
        axis=1,
    )

    return np.sqrt(
        np.maximum(
            best,
            0.0,
        )
    )


def plane_normal_branches(
    phi: float,
    q: float,
) -> dict[str, Any]:
    """Return the orthographic front/back plane-normal ambiguity."""
    _, minor = (
        ellipse_axes(
            phi
        )
    )

    xy_factor = math.sqrt(
        max(
            0.0,
            1.0
            - q * q,
        )
    )

    xy = (
        xy_factor
        * minor
    )

    plus = np.asarray(
        [
            float(
                xy[0]
            ),
            float(
                xy[1]
            ),
            float(q),
        ],
        dtype=np.float64,
    )

    minus = np.asarray(
        [
            float(
                xy[0]
            ),
            float(
                xy[1]
            ),
            -float(q),
        ],
        dtype=np.float64,
    )

    return {
        "plus_z": (
            plus.tolist()
        ),
        "minus_z": (
            minus.tolist()
        ),
        "branches_distinct": bool(
            np.linalg.norm(
                plus
                - minus
            )
            > NORMAL_DEDUP_TOL
        ),
        "plane_normal_sign_equivalence_retained": True,
    }


def _fit_objective(
    parameters: np.ndarray,
    points_uv: np.ndarray,
    weights: np.ndarray,
    limb_radius_px: float,
) -> float:
    phi = canonical_phi(
        float(
            parameters[0]
        )
    )

    q = float(
        parameters[1]
    )

    distances_norm = (
        projected_great_circle_distance_normalized(
            points_uv,
            phi,
            q,
        )
    )

    distances_px = (
        limb_radius_px
        * distances_norm
    )

    return float(
        np.sum(
            weights
            * distances_px
            * distances_px
        )
    )


def fit_projected_great_circle(
    sample_sets: Sequence[
        base.ResampledCurve
    ],
    limb: dict[str, float],
    *,
    phi_seeds_deg: Sequence[
        float
    ] = PHI_SEEDS_DEG,
    q_seeds: Sequence[
        float
    ] = Q_SEEDS,
) -> dict[str, Any]:
    """Fit one fixed-limb projected great-circle model."""
    points_px, sigma_px, weights = (
        base.combined_points(
            sample_sets
        )
    )

    points_uv = (
        pixel_to_normalized(
            points_px,
            limb,
        )
    )

    limb_radius = float(
        limb[
            "radius_px"
        ]
    )

    runs: list[
        dict[str, Any]
    ] = []

    converged: list[
        tuple[
            float,
            Any,
            float,
            float,
        ]
    ] = []

    upper_phi = np.nextafter(
        math.pi,
        0.0,
    )

    for phi_seed_deg in (
        phi_seeds_deg
    ):
        for q_seed in (
            q_seeds
        ):
            phi_seed = (
                math.radians(
                    float(
                        phi_seed_deg
                    )
                )
            )

            q_seed_value = float(
                q_seed
            )

            if not (
                0.0
                <= phi_seed
                < math.pi
            ):
                raise ValueError(
                    "phi seed outside [0, pi)."
                )

            if not (
                0.0
                <= q_seed_value
                <= 1.0
            ):
                raise ValueError(
                    "q seed outside [0, 1]."
                )

            result = minimize(
                _fit_objective,
                x0=np.asarray(
                    [
                        phi_seed,
                        q_seed_value,
                    ],
                    dtype=np.float64,
                ),
                args=(
                    points_uv,
                    weights,
                    limb_radius,
                ),
                method="L-BFGS-B",
                bounds=(
                    (
                        0.0,
                        upper_phi,
                    ),
                    (
                        0.0,
                        1.0,
                    ),
                ),
                options={
                    "maxiter": (
                        OPTIMIZER_MAXITER
                    ),
                    "ftol": (
                        OPTIMIZER_FTOL
                    ),
                    "gtol": (
                        OPTIMIZER_GTOL
                    ),
                    "maxls": 50,
                },
            )

            phi_fit = (
                canonical_phi(
                    float(
                        result.x[0]
                    )
                )
            )

            q_fit = float(
                np.clip(
                    result.x[1],
                    0.0,
                    1.0,
                )
            )

            objective = (
                _fit_objective(
                    np.asarray(
                        [
                            phi_fit,
                            q_fit,
                        ],
                        dtype=np.float64,
                    ),
                    points_uv,
                    weights,
                    limb_radius,
                )
            )

            run = {
                "start_phi_deg": (
                    float(
                        phi_seed_deg
                    )
                ),
                "start_q": (
                    q_seed_value
                ),
                "success": bool(
                    result.success
                ),
                "status": int(
                    result.status
                ),
                "message": str(
                    result.message
                ),
                "iteration_count": int(
                    result.nit
                ),
                "function_evaluations": int(
                    result.nfev
                ),
                "fitted_phi_deg": (
                    math.degrees(
                        phi_fit
                    )
                ),
                "fitted_q": (
                    q_fit
                ),
                "objective_weighted_mean_square_px2": (
                    objective
                ),
            }

            runs.append(
                run
            )

            if result.success:
                converged.append(
                    (
                        objective,
                        result,
                        phi_fit,
                        q_fit,
                    )
                )

    if not converged:
        raise RuntimeError(
            "No projected-great-circle "
            "multistart optimization converged."
        )

    converged.sort(
        key=lambda item: (
            item[0],
            item[2],
            item[3],
        )
    )

    (
        best_objective,
        best_result,
        phi,
        q,
    ) = converged[0]

    distances_norm = (
        projected_great_circle_distance_normalized(
            points_uv,
            phi,
            q,
        )
    )

    distances_px = (
        limb_radius
        * distances_norm
    )

    residuals = (
        base.residual_summary(
            distances_px,
            sigma_px,
            weights,
            limb_radius,
        )
    )

    best_start = None

    for run in runs:
        if (
            run[
                "success"
            ]
            and math.isclose(
                float(
                    run[
                        "objective_weighted_mean_square_px2"
                    ]
                ),
                best_objective,
                rel_tol=1.0e-12,
                abs_tol=1.0e-12,
            )
            and math.isclose(
                float(
                    run[
                        "fitted_phi_deg"
                    ]
                ),
                math.degrees(
                    phi
                ),
                rel_tol=0.0,
                abs_tol=1.0e-8,
            )
            and math.isclose(
                float(
                    run[
                        "fitted_q"
                    ]
                ),
                q,
                rel_tol=0.0,
                abs_tol=1.0e-10,
            )
        ):
            best_start = {
                "start_phi_deg": (
                    run[
                        "start_phi_deg"
                    ]
                ),
                "start_q": (
                    run[
                        "start_q"
                    ]
                ),
            }

            break

    return {
        "model": (
            "fixed_limb_orthographic_"
            "projected_great_circle"
        ),
        "phi_radians": phi,
        "phi_degrees": (
            math.degrees(
                phi
            )
        ),
        "q": q,
        "semi_major_px": (
            limb_radius
        ),
        "semi_minor_px": (
            q
            * limb_radius
        ),
        "diameter_line_limit": bool(
            q <= Q_LINE_EPS
        ),
        "plane_normal_branches": (
            plane_normal_branches(
                phi,
                q,
            )
        ),
        "residual_definition": (
            "Euclidean image-space distance "
            "to nearest point on complete "
            "fixed-limb projected great-circle locus"
        ),
        "residuals": residuals,
        "optimizer": {
            "method": (
                "L-BFGS-B"
            ),
            "parameter_bounds": {
                "phi_radians": [
                    0.0,
                    math.pi,
                ],
                "q": [
                    0.0,
                    1.0,
                ],
            },
            "phi_seed_degrees": [
                float(value)
                for value
                in phi_seeds_deg
            ],
            "q_seeds": [
                float(value)
                for value
                in q_seeds
            ],
            "run_count": (
                len(
                    runs
                )
            ),
            "converged_run_count": (
                sum(
                    bool(
                        run[
                            "success"
                        ]
                    )
                    for run
                    in runs
                )
            ),
            "best_start": (
                best_start
            ),
            "best_iteration_count": int(
                best_result.nit
            ),
            "best_function_evaluations": int(
                best_result.nfev
            ),
            "best_objective_weighted_mean_square_px2": (
                best_objective
            ),
            "runs": runs,
        },
    }


def fit_one_curve(
    pass1_segments: Sequence[
        base.Segment
    ],
    pass2_segments: Sequence[
        base.Segment
    ],
    limb: dict[str, float],
) -> dict[str, Any]:
    """Compute all protocol-required fits for one labelled curve."""
    pass1_primary = (
        base.resample_curve(
            pass1_segments,
            PRIMARY_SPACING_PX,
        )
    )

    pass2_primary = (
        base.resample_curve(
            pass2_segments,
            PRIMARY_SPACING_PX,
        )
    )

    result = {
        "pass1": (
            fit_projected_great_circle(
                [
                    pass1_primary
                ],
                limb,
            )
        ),
        "pass2_qc": (
            fit_projected_great_circle(
                [
                    pass2_primary
                ],
                limb,
            )
        ),
        "equal_pass_combined": (
            fit_projected_great_circle(
                [
                    pass1_primary,
                    pass2_primary,
                ],
                limb,
            )
        ),
        "sampling_sensitivity": {},
    }

    for spacing in (
        SENSITIVITY_SPACINGS_PX
    ):
        pass1 = (
            base.resample_curve(
                pass1_segments,
                spacing,
            )
        )

        pass2 = (
            base.resample_curve(
                pass2_segments,
                spacing,
            )
        )

        result[
            "sampling_sensitivity"
        ][
            format(
                spacing,
                ".1f",
            )
        ] = (
            fit_projected_great_circle(
                [
                    pass1,
                    pass2,
                ],
                limb,
            )
        )

    return result


def extract_frozen_descriptive_geometry(
    morphology: dict[str, Any],
    curve_id: str,
) -> dict[str, Any]:
    curve = (
        morphology[
            "curves"
        ][
            curve_id
        ]
    )

    return {
        "line_absolute_px": (
            curve[
                "line"
            ][
                "residuals"
            ][
                "absolute_px"
            ]
        ),
        "circle_absolute_px": (
            curve[
                "circle"
            ][
                "residuals"
            ][
                "absolute_px"
            ]
        ),
        "ellipse_absolute_px": (
            curve[
                "ellipse"
            ][
                "residuals"
            ][
                "absolute_px"
            ]
        ),
        "circle_radius_px": float(
            curve[
                "circle"
            ][
                "radius_px"
            ]
        ),
        "ellipse_axis_ratio_minor_over_major": float(
            curve[
                "ellipse"
            ][
                "axis_ratio_minor_over_major"
            ]
        ),
        "values_recomputed": False,
    }


def load_frozen_landmarks() -> dict[str, Any]:
    """Regenerate the already-frozen point census for later diagnostics."""
    (
        analysis,
        rows,
        coordinates,
    ) = (
        expanded.build_expanded_analysis()
    )

    by_id = {
        row[
            "landmark_id"
        ]: row
        for row in rows
    }

    required = {
        LR_SHARED_ID,
        CENTRAL_ID,
        UPPER_CROSSING_ID,
        *RIM_IDS,
    }

    missing = (
        required
        - set(
            coordinates
        )
    )

    if missing:
        raise RuntimeError(
            "Frozen landmark census missing: "
            + ", ".join(
                sorted(
                    missing
                )
            )
        )

    points: dict[
        str,
        Any,
    ] = {}

    for landmark_id in (
        sorted(
            required
        )
    ):
        point = np.asarray(
            coordinates[
                landmark_id
            ],
            dtype=np.float64,
        )

        row = by_id.get(
            landmark_id,
            {},
        )

        uncertainty_raw = row.get(
            "consensus_uncertainty_px"
        )

        points[
            landmark_id
        ] = {
            "x_px": float(
                point[0]
            ),
            "y_px": float(
                point[1]
            ),
            "consensus_uncertainty_px": (
                float(
                    uncertainty_raw
                )
                if uncertainty_raw
                not in {
                    None,
                    "",
                }
                else None
            ),
        }

    return {
        "points": points,
        "expanded_neutral_checkpoint": (
            analysis.get(
                "checkpoint"
            )
        ),
        "used_for_curve_fitting": False,
    }


def branch_vectors(
    fit: dict[str, Any],
) -> list[
    np.ndarray
]:
    branches = (
        fit[
            "plane_normal_branches"
        ]
    )

    vectors = [
        np.asarray(
            branches[
                "plus_z"
            ],
            dtype=np.float64,
        ),
        np.asarray(
            branches[
                "minus_z"
            ],
            dtype=np.float64,
        ),
    ]

    unique: list[
        np.ndarray
    ] = []

    for vector in vectors:
        vector = (
            vector
            / np.linalg.norm(
                vector
            )
        )

        if not any(
            np.linalg.norm(
                vector
                - existing
            )
            <= NORMAL_DEDUP_TOL
            for existing
            in unique
        ):
            unique.append(
                vector
            )

    return unique


def projected_intersections(
    fit_a: dict[str, Any],
    fit_b: dict[str, Any],
) -> np.ndarray:
    """Enumerate projected conic intersections via all plane branches."""
    candidates: list[
        np.ndarray
    ] = []

    for normal_a in (
        branch_vectors(
            fit_a
        )
    ):
        for normal_b in (
            branch_vectors(
                fit_b
            )
        ):
            direction = np.cross(
                normal_a,
                normal_b,
            )

            norm = float(
                np.linalg.norm(
                    direction
                )
            )

            if norm <= 1.0e-12:
                continue

            direction /= norm

            for sign in (
                1.0,
                -1.0,
            ):
                uv = (
                    sign
                    * direction[
                        :2
                    ]
                )

                if not any(
                    np.linalg.norm(
                        uv
                        - existing
                    )
                    <= INTERSECTION_DEDUP_TOL
                    for existing
                    in candidates
                ):
                    candidates.append(
                        uv
                    )

    if not candidates:
        raise RuntimeError(
            "Projected great-circle pair "
            "has no recoverable intersection."
        )

    return np.vstack(
        candidates
    )


def landmark_distance_to_curve_intersections(
    fit_a: dict[str, Any],
    fit_b: dict[str, Any],
    landmark: dict[str, Any],
    limb: dict[str, float],
) -> dict[str, Any]:
    intersections_uv = (
        projected_intersections(
            fit_a,
            fit_b,
        )
    )

    intersections_px = (
        normalized_to_pixel(
            intersections_uv,
            limb,
        )
    )

    target = np.asarray(
        [
            float(
                landmark[
                    "x_px"
                ]
            ),
            float(
                landmark[
                    "y_px"
                ]
            ),
        ],
        dtype=np.float64,
    )

    distances = (
        np.linalg.norm(
            intersections_px
            - target[
                None,
                :
            ],
            axis=1,
        )
    )

    index = int(
        np.argmin(
            distances
        )
    )

    return {
        "candidate_intersections_px": [
            [
                float(
                    point[0]
                ),
                float(
                    point[1]
                ),
            ]
            for point
            in intersections_px
        ],
        "candidate_count": int(
            len(
                intersections_px
            )
        ),
        "nearest_candidate_index": (
            index
        ),
        "nearest_distance_px": float(
            distances[
                index
            ]
        ),
        "landmark_x_px": float(
            target[0]
        ),
        "landmark_y_px": float(
            target[1]
        ),
        "landmark_consensus_uncertainty_px": (
            landmark[
                "consensus_uncertainty_px"
            ]
        ),
    }


def unoriented_plane_angle_deg(
    normal_a: np.ndarray,
    normal_b: np.ndarray,
) -> float:
    """Angle between unoriented origin planes, in [0, 90] degrees."""
    a = (
        normal_a
        / np.linalg.norm(
            normal_a
        )
    )

    b = (
        normal_b
        / np.linalg.norm(
            normal_b
        )
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


def branch_angle_census(
    fit_a: dict[str, Any],
    fit_b: dict[str, Any],
) -> dict[str, Any]:
    a_vectors = (
        branch_vectors(
            fit_a
        )
    )

    b_vectors = (
        branch_vectors(
            fit_b
        )
    )

    combinations: list[
        dict[str, Any]
    ] = []

    values: list[
        float
    ] = []

    for index_a, normal_a in enumerate(
        a_vectors
    ):
        for index_b, normal_b in enumerate(
            b_vectors
        ):
            angle = (
                unoriented_plane_angle_deg(
                    normal_a,
                    normal_b,
                )
            )

            combinations.append(
                {
                    "branch_a": (
                        index_a
                    ),
                    "branch_b": (
                        index_b
                    ),
                    "angle_deg": (
                        angle
                    ),
                }
            )

            values.append(
                angle
            )

    distinct: list[
        float
    ] = []

    for value in sorted(
        values
    ):
        if not any(
            math.isclose(
                value,
                existing,
                rel_tol=0.0,
                abs_tol=1.0e-9,
            )
            for existing
            in distinct
        ):
            distinct.append(
                value
            )

    return {
        "branch_combinations": (
            combinations
        ),
        "distinct_unoriented_angles_deg": (
            distinct
        ),
        "branch_selected": False,
    }


def build_incidence_diagnostics(
    curves: dict[str, Any],
    landmarks: dict[str, Any],
    limb: dict[str, float],
) -> dict[str, Any]:
    """Evaluate frozen point diagnostics only after curve fits exist."""
    fit = {
        curve_id: (
            curves[
                curve_id
            ][
                "great_circle_fits"
            ][
                "equal_pass_combined"
            ]
        )
        for curve_id
        in FIT_IDS
    }

    points = (
        landmarks[
            "points"
        ]
    )

    explicit_lr = (
        landmark_distance_to_curve_intersections(
            fit[
                "AOG-LM-P07-GC-Y0"
            ],
            fit[
                "AOG-LM-P07-GC-Y1"
            ],
            points[
                LR_SHARED_ID
            ],
            limb,
        )
    )

    candidate_origin = (
        landmark_distance_to_curve_intersections(
            fit[
                "AOG-LM-P07-GC-Y0"
            ],
            fit[
                "AOG-LM-P07-GC-YAXIS"
            ],
            points[
                CENTRAL_ID
            ],
            limb,
        )
    )

    candidate_unit_grid = (
        landmark_distance_to_curve_intersections(
            fit[
                "AOG-LM-P07-GC-X1"
            ],
            fit[
                "AOG-LM-P07-GC-Y1"
            ],
            points[
                UPPER_CROSSING_ID
            ],
            limb,
        )
    )

    second_infinity_candidates = (
        projected_intersections(
            fit[
                "AOG-LM-P07-GC-YAXIS"
            ],
            fit[
                "AOG-LM-P07-GC-X1"
            ],
        )
    )

    second_infinity_px = (
        normalized_to_pixel(
            second_infinity_candidates,
            limb,
        )
    )

    rim_distances: dict[
        str,
        Any,
    ] = {}

    for landmark_id in (
        RIM_IDS
    ):
        landmark = points[
            landmark_id
        ]

        target = np.asarray(
            [
                landmark[
                    "x_px"
                ],
                landmark[
                    "y_px"
                ],
            ],
            dtype=np.float64,
        )

        distances = (
            np.linalg.norm(
                second_infinity_px
                - target[
                    None,
                    :
                ],
                axis=1,
            )
        )

        rim_distances[
            landmark_id
        ] = {
            "nearest_distance_px": (
                float(
                    np.min(
                        distances
                    )
                )
            ),
            "consensus_uncertainty_px": (
                landmark[
                    "consensus_uncertainty_px"
                ]
            ),
        }

    nearest_rim = min(
        rim_distances,
        key=lambda landmark_id: (
            rim_distances[
                landmark_id
            ][
                "nearest_distance_px"
            ]
        ),
    )

    return {
        "landmarks_used_for_curve_fitting": False,
        "explicit_source_incidence_y0_y1_to_lower_right": (
            explicit_lr
        ),
        "candidate_origin_y0_yaxis_to_central_node": (
            candidate_origin
        ),
        "candidate_unit_grid_x1_y1_to_upper_crossing": (
            candidate_unit_grid
        ),
        "second_projective_infinity_yaxis_x1": {
            "candidate_intersections_px": [
                [
                    float(
                        point[0]
                    ),
                    float(
                        point[1]
                    ),
                ]
                for point
                in second_infinity_px
            ],
            "rim_node_distances": (
                rim_distances
            ),
            "nearest_rim_node": (
                nearest_rim
            ),
            "nearest_rim_node_distance_px": (
                rim_distances[
                    nearest_rim
                ][
                    "nearest_distance_px"
                ]
            ),
            "pass_fail_issued": False,
        },
    }


def build_analysis() -> dict[str, Any]:
    """Build the preregistered great-circle reconstruction."""
    dependencies = (
        verify_dependencies()
    )

    morphology = (
        load_frozen_morphology()
    )

    limb = (
        dependencies[
            "frozen_limb"
        ]
    )

    passes = {
        1: base.read_curve_pass(
            base.PASS_PATHS[
                1
            ],
            1,
        ),
        2: base.read_curve_pass(
            qc_runner.QC_PASS2,
            2,
        ),
    }

    curves: dict[
        str,
        Any,
    ] = {}

    for curve_id in (
        FIT_IDS
    ):
        fits = (
            fit_one_curve(
                passes[
                    1
                ][
                    curve_id
                ],
                passes[
                    2
                ][
                    curve_id
                ],
                limb,
            )
        )

        combined_rms = float(
            fits[
                "equal_pass_combined"
            ][
                "residuals"
            ][
                "absolute_px"
            ][
                "rms"
            ]
        )

        curves[
            curve_id
        ] = {
            "great_circle_fits": (
                fits
            ),
            "frozen_neutral_descriptive_geometry": (
                extract_frozen_descriptive_geometry(
                    morphology,
                    curve_id,
                )
            ),
            "compatibility": {
                "adopted_rms_floor_px": (
                    COMPATIBILITY_RMS_PX
                ),
                "combined_rms_px": (
                    combined_rms
                ),
                "compatible_at_adopted_image_space_uncertainty": bool(
                    combined_rms
                    <= COMPATIBILITY_RMS_PX
                ),
                "exact_great_circle_certified": False,
            },
        }

    # Fingerprint the complete fitted-curve block before any
    # point-landmark incidence diagnostic is evaluated.
    curve_fit_fingerprint = (
        canonical_json_sha256(
            curves
        )
    )

    landmarks = (
        load_frozen_landmarks()
    )

    incidence = (
        build_incidence_diagnostics(
            curves,
            landmarks,
            limb,
        )
    )

    combined_fits = {
        curve_id: (
            curves[
                curve_id
            ][
                "great_circle_fits"
            ][
                "equal_pass_combined"
            ]
        )
        for curve_id
        in FIT_IDS
    }

    plane_angles = {
        "delta_x_yaxis_vs_x1": (
            branch_angle_census(
                combined_fits[
                    "AOG-LM-P07-GC-YAXIS"
                ],
                combined_fits[
                    "AOG-LM-P07-GC-X1"
                ],
            )
        ),
        "delta_y_y0_vs_y1": (
            branch_angle_census(
                combined_fits[
                    "AOG-LM-P07-GC-Y0"
                ],
                combined_fits[
                    "AOG-LM-P07-GC-Y1"
                ],
            )
        ),
        "isotropic_equality_imposed": False,
        "branch_selected": False,
        "spherical_scale_selected": False,
    }

    combined_rms_values = np.asarray(
        [
            curves[
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
            for curve_id
            in FIT_IDS
        ],
        dtype=np.float64,
    )

    aggregate_rms = float(
        np.sqrt(
            np.mean(
                combined_rms_values
                * combined_rms_values
            )
        )
    )

    return {
        "checkpoint": (
            "first_hand_great_circle_"
            "reconstruction_v0.8"
        ),
        "analysis_class": (
            "preregistered_limb_constrained_"
            "great_circle_reconstruction"
        ),
        "protocol_checkpoint": (
            "3006a0e"
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
            "raw_input_seal": str(
                base.SEAL_PATH.relative_to(
                    ROOT
                )
            ),
            "qc_pass2": str(
                qc_runner.QC_PASS2.relative_to(
                    ROOT
                )
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
            "frozen_limb_reference": (
                limb
            ),
            "curve_fit_block_sha256_before_incidence": (
                curve_fit_fingerprint
            ),
        },
        "fit_partition": {
            "labelled_calibration_curves": list(
                FIT_IDS
            ),
            "excluded_scaffold_holdout": (
                HOLDOUT_ID
            ),
            "scaffold_used_for_fitting": False,
        },
        "rendering_hypothesis": {
            "name": (
                "orthographic_unit_sphere"
            ),
            "source_explicitly_specifies_camera": False,
            "failure_uniquely_disproves_great_circle_scaffold": False,
        },
        "method": {
            "normalized_coordinates": (
                "u=(x-cx)/R; v=-(y-cy)/R"
            ),
            "frozen_limb_refitted": False,
            "projected_great_circle_family": (
                "C(phi,q;t)=e_major*cos(t)+"
                "q*e_minor*sin(t)"
            ),
            "diameter_line_boundary_retained": True,
            "primary_residual": (
                "nearest Euclidean image-space "
                "distance to complete projected locus"
            ),
            "primary_resampling_spacing_px": (
                PRIMARY_SPACING_PX
            ),
            "sensitivity_spacings_px": list(
                SENSITIVITY_SPACINGS_PX
            ),
            "pass_weights": {
                "pass1": 0.5,
                "pass2_qc": 0.5,
            },
            "within_pass_weighting": (
                "visible polyline arc length"
            ),
            "curve_top_level_weighting": (
                "equal across four labelled curves"
            ),
            "optimizer": (
                "deterministic 72-start bounded L-BFGS-B"
            ),
            "formal_model_selection_performed": False,
        },
        "curves": curves,
        "aggregate_equal_curve_weight": {
            "combined_projected_great_circle_rms_px": (
                aggregate_rms
            ),
            "curve_count": (
                len(
                    FIT_IDS
                )
            ),
        },
        "incidence_diagnostics": (
            incidence
        ),
        "plane_angle_census": (
            plane_angles
        ),
        "scope": {
            "limb_constrained_great_circle_reconstruction_computed": True,
            "point_landmarks_used_for_curve_fit": False,
            "projective_map_fitted": False,
            "projective_gauge_selected": False,
            "spherical_scale_selected": False,
            "fixed_scale_candidate_verdict_issued": False,
            "reciprocal_spiral_projection_computed": False,
            "scaffold_prediction_computed": False,
            "great_circle_exactness_certified": False,
            "s1_computed": False,
            "s1_5_computed": False,
            "s2_computed": False,
        },
        "interpretation_boundary": (
            "Residuals at or below the adopted 2 px image-space "
            "uncertainty floor support compatibility with the "
            "fixed-limb orthographic projected-great-circle model. "
            "They do not certify that a hand-drawn stroke is an "
            "exact mathematical great circle. Failure of the "
            "orthographic reconstruction would not uniquely "
            "distinguish geometric inconsistency from schematic "
            "or alternative sphere rendering."
        ),
    }


def render_report(
    analysis: dict[str, Any],
) -> str:
    lines = [
        "# First Hand limb-constrained great-circle reconstruction",
        "",
        "**Status:** preregistered projected-great-circle reconstruction",
        "",
        "The frozen sphere limb is held fixed. Only the four source-labelled "
        "curves are fitted. The unlabelled scaffold remains outside fitting.",
        "",
        "## Equal-pass combined reconstruction",
        "",
        "| Curve | phi deg | q | semi-minor px | GC RMS px | "
        "Line RMS px | Circle RMS px | Ellipse RMS px | Compatibility |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---|",
    ]

    for curve_id in (
        FIT_IDS
    ):
        curve = (
            analysis[
                "curves"
            ][
                curve_id
            ]
        )

        fit = (
            curve[
                "great_circle_fits"
            ][
                "equal_pass_combined"
            ]
        )

        neutral = (
            curve[
                "frozen_neutral_descriptive_geometry"
            ]
        )

        rms = (
            fit[
                "residuals"
            ][
                "absolute_px"
            ][
                "rms"
            ]
        )

        compatible = (
            curve[
                "compatibility"
            ][
                "compatible_at_adopted_image_space_uncertainty"
            ]
        )

        lines.append(
            f"| `{curve_id}` | "
            f"{fit['phi_degrees']:.6f} | "
            f"{fit['q']:.9f} | "
            f"{fit['semi_minor_px']:.6f} | "
            f"{rms:.6f} | "
            f"{neutral['line_absolute_px']['rms']:.6f} | "
            f"{neutral['circle_absolute_px']['rms']:.6f} | "
            f"{neutral['ellipse_absolute_px']['rms']:.6f} | "
            f"{'COMPATIBLE' if compatible else 'ABOVE FLOOR'} |"
        )

    lines += [
        "",
        "Compatibility means only compatibility with the fixed-limb "
        "orthographic projected-great-circle model at the adopted 2 px "
        "image-space uncertainty scale. It is not an exactness certificate.",
        "",
        "## Plane-angle branch census",
        "",
    ]

    for name, census in (
        analysis[
            "plane_angle_census"
        ].items()
    ):
        if not isinstance(
            census,
            dict,
        ):
            continue

        if (
            "distinct_unoriented_angles_deg"
            not in census
        ):
            continue

        values = ", ".join(
            f"{value:.9f}"
            for value
            in census[
                "distinct_unoriented_angles_deg"
            ]
        )

        lines.append(
            f"- `{name}`: {values} degrees"
        )

    incidence = (
        analysis[
            "incidence_diagnostics"
        ]
    )

    lines += [
        "",
        "## Independent point-incidence diagnostics",
        "",
        (
            "- explicit lower-right Y0/Y1 incidence distance: "
            f"{incidence['explicit_source_incidence_y0_y1_to_lower_right']['nearest_distance_px']:.6f} px"
        ),
        (
            "- candidate central Y0/Y-axis incidence distance: "
            f"{incidence['candidate_origin_y0_yaxis_to_central_node']['nearest_distance_px']:.6f} px"
        ),
        (
            "- candidate upper X1/Y1 incidence distance: "
            f"{incidence['candidate_unit_grid_x1_y1_to_upper_crossing']['nearest_distance_px']:.6f} px"
        ),
        (
            "- nearest neutral rim node to Y-axis/X1 projective infinity: "
            f"`{incidence['second_projective_infinity_yaxis_x1']['nearest_rim_node']}` "
            f"at "
            f"{incidence['second_projective_infinity_yaxis_x1']['nearest_rim_node_distance_px']:.6f} px"
        ),
        "",
        "No point landmark was used in the curve fit.",
        "",
        "## Scope boundary",
        "",
        f"`{HOLDOUT_ID}` remains outside great-circle fitting and projective calibration.",
        "",
        "No projective map, projective gauge, spherical scale, fixed-scale "
        "candidate verdict, reciprocal-spiral projection, scaffold prediction, "
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
            "Preregistered fixed-limb "
            "First Hand projected-great-circle reconstruction."
        )
    )

    parser.add_argument(
        "--check-inputs",
        action="store_true",
        help=(
            "Verify frozen dependencies without "
            "computing any great-circle reconstruction."
        ),
    )

    args = parser.parse_args()

    if args.check_inputs:
        dependencies = (
            verify_dependencies()
        )

        print(
            "Raw curve pass seal: VERIFIED"
        )

        print(
            "QC derivative: VERIFIED"
        )

        print(
            "Neutral morphology result: VERIFIED"
        )

        print(
            "Great-circle protocol: PRESENT"
        )

        print(
            "Frozen limb radius:",
            f"{dependencies['frozen_limb']['radius_px']:.9f} px",
        )

        print(
            "Calibration curves:",
            len(
                FIT_IDS
            ),
        )

        print(
            "Scaffold holdout excluded: YES"
        )

        print(
            "No great-circle reconstruction was computed."
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
        * 96
    )

    print(
        "FIRST HAND LIMB-CONSTRAINED "
        "GREAT-CIRCLE RECONSTRUCTION"
    )

    print(
        "="
        * 96
    )

    for curve_id in (
        FIT_IDS
    ):
        curve = (
            analysis[
                "curves"
            ][
                curve_id
            ]
        )

        fit = (
            curve[
                "great_circle_fits"
            ][
                "equal_pass_combined"
            ]
        )

        stats = (
            fit[
                "residuals"
            ][
                "absolute_px"
            ]
        )

        compatible = (
            curve[
                "compatibility"
            ][
                "compatible_at_adopted_image_space_uncertainty"
            ]
        )

        print(
            f"{curve_id}: "
            f"phi={fit['phi_degrees']:.6f} deg, "
            f"q={fit['q']:.9f}, "
            f"RMS={stats['rms']:.6f} px, "
            f"P95={stats['p95']:.6f} px, "
            f"{'COMPATIBLE' if compatible else 'ABOVE FLOOR'}"
        )

    print(
        "Aggregate equal-curve RMS:",
        f"{analysis['aggregate_equal_curve_weight']['combined_projected_great_circle_rms_px']:.6f} px",
    )

    print(
        f"Wrote {OUTPUT_JSON}"
    )

    print(
        f"Wrote {OUTPUT_REPORT}"
    )

    print(
        "Scaffold holdout was not fitted."
    )

    print(
        "No projective map, scale, spiral verdict, "
        "or self-embedment score was computed."
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
