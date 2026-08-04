#!/usr/bin/env python3
"""Full translated-isotropic reciprocal-spiral audit.

This is the preregistered nonlinear spiral-only model test.

Model in inverse-stereographic construction-plane coordinates:

    Q(theta) =
        t +
        k * R(alpha0) *
        [cos(s*theta)/theta,
         sin(s*theta)/theta]

For fixed translation t:

    beta_unwrapped = a + m / R_t

with:

    R_t = ||Q - t||
    k   = |m|
    s   = sign(m)

The only nonlinear optimization variables are the translated construction
origin represented by normalized stereographic disk polar coordinates:

    (r_tau, phi_tau).

The fitted objective is the corrective preregistered normalized quantity:

    J = SSE / SST = 1 - weighted R^2.

No first-order translation-signature result is read or used.
No coordinate curve, scaffold, endpoint landmark, or endpoint theta branch
is used to fit the model.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from pathlib import Path
from typing import Any, Sequence

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import differential_evolution


ROOT = Path(__file__).resolve().parents[1]

PROTOCOL = (
    ROOT
    / "docs"
    / "first_hand_spherical_reciprocal_spiral_translated_isotropic_protocol.md"
)

ADDENDUM = (
    ROOT
    / "docs"
    / "first_hand_spherical_reciprocal_spiral_translated_isotropic_objective_addendum.md"
)

PARENT_JSON = (
    ROOT
    / "data"
    / "derived"
    / "first_hand_arm_of_god"
    / "qc"
    / "first_hand_spherical_reciprocal_spiral_shape.json"
)

PARENT_SAMPLES = (
    ROOT
    / "data"
    / "derived"
    / "first_hand_arm_of_god"
    / "qc"
    / "first_hand_spherical_reciprocal_spiral_shape_samples.csv"
)

PARENT_SEAL = (
    ROOT
    / "data"
    / "derived"
    / "first_hand_arm_of_god"
    / "qc"
    / "first_hand_spherical_reciprocal_spiral_shape.sha256"
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
    / "first_hand_spherical_reciprocal_spiral_translated_isotropic.json"
)

OUT_SEGMENTS = (
    OUTPUT_DIR
    / "first_hand_spherical_reciprocal_spiral_translated_isotropic_segments.csv"
)

OUT_PNG = (
    OUTPUT_DIR
    / "first_hand_spherical_reciprocal_spiral_translated_isotropic.png"
)

OUT_REPORT = (
    ROOT
    / "reports"
    / "first_hand_spherical_reciprocal_spiral_translated_isotropic.md"
)

ANALYSIS_CLASS = (
    "spiral_only_translated_isotropic_central_projective_stereographic_reciprocal"
)

SEGMENT_IDS = tuple(
    f"S{i:02d}"
    for i in range(1, 11)
)

N_RESAMPLE = 401
N_SEGMENTS = 10
N_PER_PASS = N_RESAMPLE * N_SEGMENTS

TWO_PI = 2.0 * math.pi
THREE_PI = 3.0 * math.pi

PRIMARY_R_TAU_MAX = 0.98
EXPANDED_R_TAU_MAX = 0.995

R_T_MIN = 1e-12
SST_MIN = 1e-18
BOUNDARY_TOL = 1e-8

DE_STRATEGY = "best1bin"
DE_MAXITER = 300
DE_POPSIZE = 15
DE_TOL = 1e-10
DE_ATOL = 1e-12
DE_MUTATION = (0.5, 1.0)
DE_RECOMBINATION = 0.7
DE_SEED = 20260804
DE_UPDATING = "immediate"
DE_WORKERS = 1
DE_POLISH = True

REQUIRED_SAMPLE_FIELDS = {
    "pass_number",
    "segment_id",
    "sample_index",
    "u",
    "v",
    "rho",
    "weight_length",
    "weight_equal_segment",
}


def sha256_path(path: Path) -> str:
    digest = hashlib.sha256()

    with path.open("rb") as handle:
        for block in iter(
            lambda: handle.read(1024 * 1024),
            b"",
        ):
            digest.update(block)

    return digest.hexdigest()


def resolve_manifest_path(recorded_name: str) -> Path:
    recorded = Path(
        recorded_name.lstrip("*").strip()
    )

    if not recorded.is_absolute():
        recorded = ROOT / recorded

    return recorded.resolve()


def verify_target_in_manifest(
    manifest: Path,
    target: Path,
) -> None:
    if not manifest.exists():
        raise RuntimeError(
            f"Missing SHA-256 manifest: {manifest}"
        )

    matches: list[str] = []

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
                f"Malformed SHA-256 record: {line!r}"
            )

        if (
            resolve_manifest_path(fields[1])
            == target.resolve()
        ):
            matches.append(
                fields[0]
            )

    if len(matches) != 1:
        raise RuntimeError(
            f"Expected exactly one seal entry for {target}; "
            f"found {len(matches)}."
        )

    if sha256_path(target) != matches[0]:
        raise RuntimeError(
            f"SHA-256 verification failed for {target}."
        )


def verify_protocols() -> None:
    protocol = PROTOCOL.read_text(
        encoding="utf-8"
    ).lower()

    addendum = ADDENDUM.read_text(
        encoding="utf-8"
    ).lower()

    protocol_required = (
        "translated-isotropic",
        "cross-prediction",
        "intrinsic angular-span holdout",
        "no model expansion beyond translation",
    )

    addendum_required = (
        "j(t) = sse / sst",
        "translation parameterization",
        "mandatory expanded-bound sensitivity",
        "differential evolution",
        "construction-plane transverse diagnostic",
    )

    for token in protocol_required:
        if token not in protocol:
            raise RuntimeError(
                f"Parent protocol missing token: {token!r}"
            )

    for token in addendum_required:
        if token not in addendum:
            raise RuntimeError(
                f"Objective addendum missing token: {token!r}"
            )


def parse_float(
    row: dict[str, str],
    field: str,
) -> float:
    value = float(
        row[field]
    )

    if not math.isfinite(value):
        raise RuntimeError(
            f"Non-finite {field} in frozen sample table."
        )

    return value


def read_samples() -> list[dict[str, Any]]:
    with PARENT_SAMPLES.open(
        newline="",
        encoding="utf-8",
    ) as handle:
        reader = csv.DictReader(handle)

        if reader.fieldnames is None:
            raise RuntimeError(
                "Frozen parent sample table has no header."
            )

        missing = (
            REQUIRED_SAMPLE_FIELDS
            - set(reader.fieldnames)
        )

        if missing:
            raise RuntimeError(
                "Frozen parent sample table missing fields: "
                + ", ".join(
                    sorted(missing)
                )
            )

        raw_rows = list(reader)

    if len(raw_rows) != 2 * N_PER_PASS:
        raise RuntimeError(
            f"Expected {2 * N_PER_PASS} samples; "
            f"found {len(raw_rows)}."
        )

    rows: list[dict[str, Any]] = []

    for raw in raw_rows:
        pass_number = int(
            raw["pass_number"]
        )

        segment_id = raw[
            "segment_id"
        ]

        sample_index = int(
            raw["sample_index"]
        )

        if pass_number not in (
            1,
            2,
        ):
            raise RuntimeError(
                f"Unexpected pass number: {pass_number}"
            )

        if segment_id not in SEGMENT_IDS:
            raise RuntimeError(
                f"Unexpected segment ID: {segment_id}"
            )

        if not (
            0
            <= sample_index
            < N_RESAMPLE
        ):
            raise RuntimeError(
                f"Unexpected sample index: {sample_index}"
            )

        u = parse_float(
            raw,
            "u",
        )

        v = parse_float(
            raw,
            "v",
        )

        rho = parse_float(
            raw,
            "rho",
        )

        if rho <= 0.0:
            raise RuntimeError(
                "Frozen sample has rho <= 0."
            )

        if rho >= 1.0:
            raise RuntimeError(
                "Frozen sample has rho >= 1."
            )

        if not math.isclose(
            math.hypot(
                u,
                v,
            ),
            rho,
            rel_tol=0.0,
            abs_tol=5e-12,
        ):
            raise RuntimeError(
                "Frozen u,v,rho relation is inconsistent."
            )

        segment_number = int(
            segment_id[1:]
        )

        global_index = (
            (segment_number - 1)
            * N_RESAMPLE
            + sample_index
        )

        rows.append(
            {
                "pass_number": pass_number,
                "segment_id": segment_id,
                "sample_index": sample_index,
                "global_index": global_index,
                "u": u,
                "v": v,
                "rho": rho,
                "weight_length": parse_float(
                    raw,
                    "weight_length",
                ),
                "weight_equal_segment": parse_float(
                    raw,
                    "weight_equal_segment",
                ),
            }
        )

    seen = set()

    for row in rows:
        key = (
            row["pass_number"],
            row["segment_id"],
            row["sample_index"],
        )

        if key in seen:
            raise RuntimeError(
                f"Duplicate sample key: {key}"
            )

        seen.add(key)

    for pass_number in (
        1,
        2,
    ):
        selected = [
            row
            for row in rows
            if row[
                "pass_number"
            ] == pass_number
        ]

        if len(selected) != N_PER_PASS:
            raise RuntimeError(
                f"Pass {pass_number} does not contain "
                f"{N_PER_PASS} samples."
            )

        for segment_id in SEGMENT_IDS:
            indices = sorted(
                row[
                    "sample_index"
                ]
                for row in selected
                if row[
                    "segment_id"
                ] == segment_id
            )

            if indices != list(
                range(N_RESAMPLE)
            ):
                raise RuntimeError(
                    f"Pass {pass_number} {segment_id} does not contain "
                    "sample_index 0..400."
                )

    rows.sort(
        key=lambda row: (
            row["pass_number"],
            row["global_index"],
        )
    )

    return rows


def verify_parent_json() -> dict[str, Any]:
    data = json.loads(
        PARENT_JSON.read_text(
            encoding="utf-8"
        )
    )

    if (
        data.get("checkpoint")
        != "first_hand_spherical_reciprocal_spiral_shape_v0.8"
    ):
        raise RuntimeError(
            "Unexpected frozen parent checkpoint."
        )

    if (
        data.get(
            "model",
            {},
        ).get(
            "linear_shape_relation"
        )
        != "alpha_unwrapped=a+m*F(rho)"
    ):
        raise RuntimeError(
            "Unexpected parent model identity."
        )

    return data


def verify_dependencies() -> tuple[
    dict[str, Any],
    list[dict[str, Any]],
]:
    for path in (
        PROTOCOL,
        ADDENDUM,
        PARENT_JSON,
        PARENT_SAMPLES,
        PARENT_SEAL,
    ):
        if not path.exists():
            raise RuntimeError(
                f"Missing frozen dependency: {path}"
            )

    verify_target_in_manifest(
        PARENT_SEAL,
        PARENT_JSON,
    )

    verify_target_in_manifest(
        PARENT_SEAL,
        PARENT_SAMPLES,
    )

    verify_protocols()

    parent = verify_parent_json()

    rows = read_samples()

    return (
        parent,
        rows,
    )


def rows_to_arrays(
    rows: Sequence[
        dict[str, Any]
    ],
    weight_field: str,
) -> dict[str, np.ndarray]:
    u = np.array(
        [
            row["u"]
            for row in rows
        ],
        dtype=float,
    )

    v = np.array(
        [
            row["v"]
            for row in rows
        ],
        dtype=float,
    )

    rho = np.array(
        [
            row["rho"]
            for row in rows
        ],
        dtype=float,
    )

    weights = np.array(
        [
            row[weight_field]
            for row in rows
        ],
        dtype=float,
    )

    if np.any(
        weights <= 0.0
    ):
        raise RuntimeError(
            f"{weight_field} contains non-positive values."
        )

    p = np.column_stack(
        (
            u,
            v,
        )
    )

    denominator = (
        1.0
        - rho
        * rho
    )

    Q = (
        2.0
        * p
        / denominator[
            :,
            None
        ]
    )

    return {
        "p": p,
        "Q": Q,
        "weights": weights,
    }


def render_construction_plane(
    Q: np.ndarray,
) -> np.ndarray:
    Q = np.asarray(
        Q,
        dtype=float,
    )

    q_norm = np.linalg.norm(
        Q,
        axis=1,
    )

    denominator = (
        np.sqrt(
            1.0
            + q_norm
            * q_norm
        )
        + 1.0
    )

    return (
        Q
        / denominator[
            :,
            None
        ]
    )


def tau_polar_to_translation(
    r_tau: float,
    phi_tau: float,
) -> dict[str, Any]:
    if not (
        0.0
        <= r_tau
        < 1.0
    ):
        raise ValueError(
            "r_tau must lie in [0,1)."
        )

    tau = np.array(
        [
            r_tau
            * math.cos(
                phi_tau
            ),
            r_tau
            * math.sin(
                phi_tau
            ),
        ],
        dtype=float,
    )

    denominator = (
        1.0
        - r_tau
        * r_tau
    )

    t = (
        2.0
        * tau
        / denominator
    )

    return {
        "r_tau": r_tau,
        "phi_tau_rad": phi_tau,
        "phi_tau_mod_2pi_rad": (
            phi_tau
            % TWO_PI
        ),
        "phi_tau_mod_2pi_deg": math.degrees(
            phi_tau
            % TWO_PI
        ),
        "tau_u": float(
            tau[0]
        ),
        "tau_v": float(
            tau[1]
        ),
        "t_x": float(
            t[0]
        ),
        "t_y": float(
            t[1]
        ),
        "t_magnitude": float(
            np.linalg.norm(
                t
            )
        ),
        "_t": t,
    }


def weighted_quantile(
    values: np.ndarray,
    weights: np.ndarray,
    quantile: float,
) -> float:
    values = np.asarray(
        values,
        dtype=float,
    )

    weights = np.asarray(
        weights,
        dtype=float,
    )

    if (
        values.ndim != 1
        or weights.ndim != 1
        or values.shape != weights.shape
        or len(values) == 0
    ):
        raise ValueError(
            "weighted_quantile requires equal non-empty 1-D arrays."
        )

    if not (
        0.0
        <= quantile
        <= 1.0
    ):
        raise ValueError(
            "quantile must lie in [0,1]."
        )

    if np.any(
        weights < 0.0
    ):
        raise ValueError(
            "weights must be non-negative."
        )

    total = float(
        np.sum(
            weights
        )
    )

    if total <= 0.0:
        raise ValueError(
            "weights must have positive total."
        )

    order = np.argsort(
        values,
        kind="mergesort",
    )

    sorted_values = values[
        order
    ]

    sorted_weights = weights[
        order
    ]

    cumulative = np.cumsum(
        sorted_weights
    )

    target = (
        quantile
        * total
    )

    index = int(
        np.searchsorted(
            cumulative,
            target,
            side="left",
        )
    )

    index = min(
        index,
        len(
            sorted_values
        )
        - 1,
    )

    return float(
        sorted_values[
            index
        ]
    )


def weighted_distance_summary(
    values: np.ndarray,
    weights: np.ndarray,
) -> dict[str, float]:
    values = np.asarray(
        values,
        dtype=float,
    )

    weights = np.asarray(
        weights,
        dtype=float,
    )

    weight_sum = float(
        np.sum(
            weights
        )
    )

    return {
        "median": weighted_quantile(
            values,
            weights,
            0.5,
        ),
        "mean": float(
            np.sum(
                weights
                * values
            )
            / weight_sum
        ),
        "rms": math.sqrt(
            float(
                np.sum(
                    weights
                    * values
                    * values
                )
                / weight_sum
            )
        ),
        "p95": weighted_quantile(
            values,
            weights,
            0.95,
        ),
        "max": float(
            np.max(
                values
            )
        ),
    }


def angular_summary(
    residual: np.ndarray,
    weights: np.ndarray,
) -> dict[str, float]:
    residual = np.asarray(
        residual,
        dtype=float,
    )

    weights = np.asarray(
        weights,
        dtype=float,
    )

    absolute = np.abs(
        residual
    )

    weight_sum = float(
        np.sum(
            weights
        )
    )

    signed_mean = float(
        np.sum(
            weights
            * residual
        )
        / weight_sum
    )

    mean_abs = float(
        np.sum(
            weights
            * absolute
        )
        / weight_sum
    )

    rms = math.sqrt(
        float(
            np.sum(
                weights
                * residual
                * residual
            )
            / weight_sum
        )
    )

    median = weighted_quantile(
        absolute,
        weights,
        0.5,
    )

    p95 = weighted_quantile(
        absolute,
        weights,
        0.95,
    )

    maximum = float(
        np.max(
            absolute
        )
    )

    return {
        "signed_mean_rad": signed_mean,
        "signed_mean_deg": math.degrees(
            signed_mean
        ),
        "median_abs_rad": median,
        "median_abs_deg": math.degrees(
            median
        ),
        "mean_abs_rad": mean_abs,
        "mean_abs_deg": math.degrees(
            mean_abs
        ),
        "rms_rad": rms,
        "rms_deg": math.degrees(
            rms
        ),
        "p95_abs_rad": p95,
        "p95_abs_deg": math.degrees(
            p95
        ),
        "max_abs_rad": maximum,
        "max_abs_deg": math.degrees(
            maximum
        ),
    }


def profile_linear_relation(
    inverse_radius: np.ndarray,
    beta: np.ndarray,
    weights: np.ndarray,
) -> dict[str, Any] | None:
    x = np.asarray(
        inverse_radius,
        dtype=float,
    )

    y = np.asarray(
        beta,
        dtype=float,
    )

    w = np.asarray(
        weights,
        dtype=float,
    )

    weight_sum = float(
        np.sum(
            w
        )
    )

    x_bar = float(
        np.sum(
            w
            * x
        )
        / weight_sum
    )

    y_bar = float(
        np.sum(
            w
            * y
        )
        / weight_sum
    )

    dx = (
        x
        - x_bar
    )

    dy = (
        y
        - y_bar
    )

    denominator = float(
        np.sum(
            w
            * dx
            * dx
        )
    )

    if denominator <= 0.0:
        return None

    m = float(
        np.sum(
            w
            * dx
            * dy
        )
        / denominator
    )

    a = (
        y_bar
        - m
        * x_bar
    )

    predicted = (
        a
        + m
        * x
    )

    residual = (
        y
        - predicted
    )

    sse = float(
        np.sum(
            w
            * residual
            * residual
        )
    )

    sst = float(
        np.sum(
            w
            * dy
            * dy
        )
    )

    if sst <= SST_MIN:
        return None

    objective = (
        sse
        / sst
    )

    return {
        "a": a,
        "m": m,
        "predicted": predicted,
        "residual": residual,
        "sse": sse,
        "sst": sst,
        "objective": objective,
        "weighted_r_squared": (
            1.0
            - objective
        ),
    }


def evaluate_translation_plane(
    Q: np.ndarray,
    p_observed: np.ndarray,
    weights: np.ndarray,
    t: np.ndarray,
    limb_radius_px: float,
) -> dict[str, Any] | None:
    W = (
        Q
        - t[
            None,
            :
        ]
    )

    R_t = np.linalg.norm(
        W,
        axis=1,
    )

    if np.any(
        R_t
        <= R_T_MIN
    ):
        return None

    beta_principal = np.arctan2(
        W[
            :,
            1
        ],
        W[
            :,
            0
        ],
    )

    beta = np.unwrap(
        beta_principal,
        discont=math.pi,
    )

    inverse_radius = (
        1.0
        / R_t
    )

    profile = profile_linear_relation(
        inverse_radius,
        beta,
        weights,
    )

    if profile is None:
        return None

    beta_hat = profile[
        "predicted"
    ]

    residual = profile[
        "residual"
    ]

    Q_hat = (
        t[
            None,
            :
        ]
        + R_t[
            :,
            None
        ]
        * np.column_stack(
            (
                np.cos(
                    beta_hat
                ),
                np.sin(
                    beta_hat
                ),
            )
        )
    )

    p_hat = render_construction_plane(
        Q_hat
    )

    page_distance_px = (
        limb_radius_px
        * np.linalg.norm(
            p_hat
            - p_observed,
            axis=1,
        )
    )

    transverse_Q = (
        2.0
        * R_t
        * np.abs(
            np.sin(
                0.5
                * residual
            )
        )
    )

    span = float(
        beta[
            -1
        ]
        - beta[
            0
        ]
    )

    absolute_span = abs(
        span
    )

    span_minus_three_pi = (
        absolute_span
        - THREE_PI
    )

    return {
        **profile,
        "R_t": R_t,
        "beta_principal": beta_principal,
        "beta": beta,
        "beta_hat": beta_hat,
        "Q_hat": Q_hat,
        "p_hat": p_hat,
        "page_distance_px": page_distance_px,
        "transverse_Q": transverse_Q,
        "span": {
            "signed_span_rad": span,
            "signed_span_deg": math.degrees(
                span
            ),
            "absolute_span_rad": absolute_span,
            "absolute_span_deg": math.degrees(
                absolute_span
            ),
            "absolute_span_minus_3pi_rad": (
                span_minus_three_pi
            ),
            "absolute_span_minus_3pi_deg": (
                math.degrees(
                    span_minus_three_pi
                )
            ),
            "absolute_discrepancy_from_3pi_rad": abs(
                span_minus_three_pi
            ),
            "absolute_discrepancy_from_3pi_deg": math.degrees(
                abs(
                    span_minus_three_pi
                )
            ),
        },
    }


def objective_from_tau(
    parameters: Sequence[float],
    Q: np.ndarray,
    p_observed: np.ndarray,
    weights: np.ndarray,
    limb_radius_px: float,
) -> float:
    r_tau = float(
        parameters[
            0
        ]
    )

    phi_tau = float(
        parameters[
            1
        ]
    )

    if not (
        0.0
        <= r_tau
        < 1.0
    ):
        return float(
            "inf"
        )

    translation = tau_polar_to_translation(
        r_tau,
        phi_tau,
    )

    evaluated = evaluate_translation_plane(
        Q,
        p_observed,
        weights,
        translation[
            "_t"
        ],
        limb_radius_px,
    )

    if evaluated is None:
        return float(
            "inf"
        )

    objective = float(
        evaluated[
            "objective"
        ]
    )

    if not math.isfinite(
        objective
    ):
        return float(
            "inf"
        )

    return objective


def optimize_translation(
    rows: Sequence[
        dict[str, Any]
    ],
    weight_field: str,
    r_tau_max: float,
    limb_radius_px: float,
) -> dict[str, Any]:
    arrays = rows_to_arrays(
        rows,
        weight_field,
    )

    Q = arrays[
        "Q"
    ]

    p_observed = arrays[
        "p"
    ]

    weights = arrays[
        "weights"
    ]

    result = differential_evolution(
        objective_from_tau,
        bounds=(
            (
                0.0,
                r_tau_max,
            ),
            (
                -math.pi,
                math.pi,
            ),
        ),
        args=(
            Q,
            p_observed,
            weights,
            limb_radius_px,
        ),
        strategy=DE_STRATEGY,
        maxiter=DE_MAXITER,
        popsize=DE_POPSIZE,
        tol=DE_TOL,
        atol=DE_ATOL,
        mutation=DE_MUTATION,
        recombination=DE_RECOMBINATION,
        seed=DE_SEED,
        updating=DE_UPDATING,
        workers=DE_WORKERS,
        polish=DE_POLISH,
    )

    r_tau = float(
        result.x[
            0
        ]
    )

    phi_tau = float(
        result.x[
            1
        ]
    )

    translation = tau_polar_to_translation(
        r_tau,
        phi_tau,
    )

    evaluated = evaluate_translation_plane(
        Q,
        p_observed,
        weights,
        translation[
            "_t"
        ],
        limb_radius_px,
    )

    if evaluated is None:
        raise RuntimeError(
            "Optimizer returned an invalid translated solution."
        )

    boundary_distance = (
        r_tau_max
        - r_tau
    )

    m = float(
        evaluated[
            "m"
        ]
    )

    if m > 0.0:
        handedness = 1
    elif m < 0.0:
        handedness = -1
    else:
        handedness = 0

    return {
        "weighting": weight_field,
        "r_tau_search_max": r_tau_max,
        "r_tau": r_tau,
        "phi_tau_rad": phi_tau,
        "phi_tau_mod_2pi_rad": translation[
            "phi_tau_mod_2pi_rad"
        ],
        "phi_tau_mod_2pi_deg": translation[
            "phi_tau_mod_2pi_deg"
        ],
        "tau_u": translation[
            "tau_u"
        ],
        "tau_v": translation[
            "tau_v"
        ],
        "t_x": translation[
            "t_x"
        ],
        "t_y": translation[
            "t_y"
        ],
        "t_magnitude": translation[
            "t_magnitude"
        ],
        "radial_bound_distance": boundary_distance,
        "at_radial_search_boundary": bool(
            boundary_distance
            <= BOUNDARY_TOL
        ),
        "a_rad": float(
            evaluated[
                "a"
            ]
        ),
        "alpha0_mod_2pi_rad": float(
            evaluated[
                "a"
            ]
            % TWO_PI
        ),
        "alpha0_mod_2pi_deg": math.degrees(
            float(
                evaluated[
                    "a"
                ]
                % TWO_PI
            )
        ),
        "m_signed": m,
        "handedness": handedness,
        "k": abs(
            m
        ),
        "objective_J": float(
            evaluated[
                "objective"
            ]
        ),
        "weighted_r_squared": float(
            evaluated[
                "weighted_r_squared"
            ]
        ),
        "weighted_sse_rad2": float(
            evaluated[
                "sse"
            ]
        ),
        "weighted_sst_rad2": float(
            evaluated[
                "sst"
            ]
        ),
        "angular_residual": angular_summary(
            evaluated[
                "residual"
            ],
            weights,
        ),
        "construction_plane_transverse": (
            weighted_distance_summary(
                evaluated[
                    "transverse_Q"
                ],
                weights,
            )
        ),
        "page_pixel_discrepancy": (
            weighted_distance_summary(
                evaluated[
                    "page_distance_px"
                ],
                weights,
            )
        ),
        "intrinsic_span_holdout": (
            evaluated[
                "span"
            ]
        ),
        "optimizer": {
            "success": bool(
                result.success
            ),
            "message": str(
                result.message
            ),
            "nit": int(
                result.nit
            ),
            "nfev": int(
                result.nfev
            ),
            "fun": float(
                result.fun
            ),
            "strategy": DE_STRATEGY,
            "maxiter": DE_MAXITER,
            "popsize": DE_POPSIZE,
            "tol": DE_TOL,
            "atol": DE_ATOL,
            "mutation": list(
                DE_MUTATION
            ),
            "recombination": DE_RECOMBINATION,
            "seed": DE_SEED,
            "updating": DE_UPDATING,
            "workers": DE_WORKERS,
            "polish": DE_POLISH,
        },
        "_evaluation": evaluated,
        "_weights": weights,
        "_p_observed": p_observed,
        "_Q": Q,
        "_t": translation[
            "_t"
        ],
    }


def fixed_model_evaluation(
    rows: Sequence[
        dict[str, Any]
    ],
    weight_field: str,
    fitted_model: dict[str, Any],
    limb_radius_px: float,
) -> dict[str, Any]:
    arrays = rows_to_arrays(
        rows,
        weight_field,
    )

    Q = arrays[
        "Q"
    ]

    p_observed = arrays[
        "p"
    ]

    weights = arrays[
        "weights"
    ]

    t = np.array(
        [
            fitted_model[
                "t_x"
            ],
            fitted_model[
                "t_y"
            ],
        ],
        dtype=float,
    )

    W = (
        Q
        - t[
            None,
            :
        ]
    )

    R_t = np.linalg.norm(
        W,
        axis=1,
    )

    if np.any(
        R_t
        <= R_T_MIN
    ):
        raise RuntimeError(
            "Cross-prediction encountered R_t <= threshold."
        )

    beta = np.unwrap(
        np.arctan2(
            W[
                :,
                1
            ],
            W[
                :,
                0
            ],
        ),
        discont=math.pi,
    )

    beta_hat = (
        fitted_model[
            "a_rad"
        ]
        + fitted_model[
            "m_signed"
        ]
        / R_t
    )

    residual = (
        beta
        - beta_hat
    )

    Q_hat = (
        t[
            None,
            :
        ]
        + R_t[
            :,
            None
        ]
        * np.column_stack(
            (
                np.cos(
                    beta_hat
                ),
                np.sin(
                    beta_hat
                ),
            )
        )
    )

    p_hat = render_construction_plane(
        Q_hat
    )

    page_distance_px = (
        limb_radius_px
        * np.linalg.norm(
            p_hat
            - p_observed,
            axis=1,
        )
    )

    transverse_Q = (
        2.0
        * R_t
        * np.abs(
            np.sin(
                0.5
                * residual
            )
        )
    )

    span = float(
        beta[
            -1
        ]
        - beta[
            0
        ]
    )

    absolute_span = abs(
        span
    )

    return {
        "weighting": weight_field,
        "sample_count": len(
            rows
        ),
        "angular_residual": angular_summary(
            residual,
            weights,
        ),
        "construction_plane_transverse": (
            weighted_distance_summary(
                transverse_Q,
                weights,
            )
        ),
        "page_pixel_discrepancy": (
            weighted_distance_summary(
                page_distance_px,
                weights,
            )
        ),
        "intrinsic_span_about_training_origin": {
            "signed_span_rad": span,
            "signed_span_deg": math.degrees(
                span
            ),
            "absolute_span_rad": absolute_span,
            "absolute_span_deg": math.degrees(
                absolute_span
            ),
            "absolute_span_minus_3pi_deg": math.degrees(
                absolute_span
                - THREE_PI
            ),
        },
        "branch_adjustment_applied": False,
        "angular_offset_refitted": False,
        "phase_refitted": False,
    }


def circular_difference(
    a: float,
    b: float,
) -> float:
    return math.atan2(
        math.sin(
            a - b
        ),
        math.cos(
            a - b
        ),
    )


def relative_difference(
    a: float,
    b: float,
) -> float | None:
    denominator = (
        abs(
            a
        )
        + abs(
            b
        )
    )

    if denominator == 0.0:
        return None

    return (
        2.0
        * abs(
            a
            - b
        )
        / denominator
    )


def compare_primary_fits(
    fit1: dict[str, Any],
    fit2: dict[str, Any],
) -> dict[str, Any]:
    t_separation = math.hypot(
        fit1[
            "t_x"
        ]
        - fit2[
            "t_x"
        ],
        fit1[
            "t_y"
        ]
        - fit2[
            "t_y"
        ],
    )

    tau_separation = math.hypot(
        fit1[
            "tau_u"
        ]
        - fit2[
            "tau_u"
        ],
        fit1[
            "tau_v"
        ]
        - fit2[
            "tau_v"
        ],
    )

    translation_direction_difference = abs(
        circular_difference(
            math.atan2(
                fit1[
                    "t_y"
                ],
                fit1[
                    "t_x"
                ],
            ),
            math.atan2(
                fit2[
                    "t_y"
                ],
                fit2[
                    "t_x"
                ],
            ),
        )
    )

    alpha_difference = abs(
        circular_difference(
            fit1[
                "alpha0_mod_2pi_rad"
            ],
            fit2[
                "alpha0_mod_2pi_rad"
            ],
        )
    )

    return {
        "construction_translation_separation": (
            t_separation
        ),
        "tau_disk_separation": tau_separation,
        "relative_translation_magnitude_difference": (
            relative_difference(
                fit1[
                    "t_magnitude"
                ],
                fit2[
                    "t_magnitude"
                ],
            )
        ),
        "translation_direction_difference_rad": (
            translation_direction_difference
        ),
        "translation_direction_difference_deg": (
            math.degrees(
                translation_direction_difference
            )
        ),
        "absolute_k_difference": abs(
            fit1[
                "k"
            ]
            - fit2[
                "k"
            ]
        ),
        "relative_k_difference": relative_difference(
            fit1[
                "k"
            ],
            fit2[
                "k"
            ],
        ),
        "alpha0_circular_difference_rad": (
            alpha_difference
        ),
        "alpha0_circular_difference_deg": math.degrees(
            alpha_difference
        ),
        "handedness_agrees": bool(
            fit1[
                "handedness"
            ]
            == fit2[
                "handedness"
            ]
        ),
    }


def compare_bound_sensitivity(
    primary: dict[str, Any],
    expanded: dict[str, Any],
) -> dict[str, Any]:
    return {
        "construction_translation_separation": math.hypot(
            primary[
                "t_x"
            ]
            - expanded[
                "t_x"
            ],
            primary[
                "t_y"
            ]
            - expanded[
                "t_y"
            ],
        ),
        "tau_disk_separation": math.hypot(
            primary[
                "tau_u"
            ]
            - expanded[
                "tau_u"
            ],
            primary[
                "tau_v"
            ]
            - expanded[
                "tau_v"
            ],
        ),
        "objective_difference_expanded_minus_primary": (
            expanded[
                "objective_J"
            ]
            - primary[
                "objective_J"
            ]
        ),
        "primary_at_boundary": primary[
            "at_radial_search_boundary"
        ],
        "expanded_at_boundary": expanded[
            "at_radial_search_boundary"
        ],
        "primary_r_tau": primary[
            "r_tau"
        ],
        "expanded_r_tau": expanded[
            "r_tau"
        ],
        "primary_t_magnitude": primary[
            "t_magnitude"
        ],
        "expanded_t_magnitude": expanded[
            "t_magnitude"
        ],
    }


def segment_diagnostics(
    rows: Sequence[
        dict[str, Any]
    ],
    fit: dict[str, Any],
) -> list[dict[str, Any]]:
    evaluation = fit[
        "_evaluation"
    ]

    weights = fit[
        "_weights"
    ]

    residual = evaluation[
        "residual"
    ]

    transverse = evaluation[
        "transverse_Q"
    ]

    page_px = evaluation[
        "page_distance_px"
    ]

    results = []

    for segment_id in SEGMENT_IDS:
        indices = np.array(
            [
                index
                for index, row
                in enumerate(
                    rows
                )
                if row[
                    "segment_id"
                ] == segment_id
            ],
            dtype=int,
        )

        segment_weights = weights[
            indices
        ]

        results.append(
            {
                "segment_id": segment_id,
                "sample_count": len(
                    indices
                ),
                "angular_residual": angular_summary(
                    residual[
                        indices
                    ],
                    segment_weights,
                ),
                "construction_plane_transverse": (
                    weighted_distance_summary(
                        transverse[
                            indices
                        ],
                        segment_weights,
                    )
                ),
                "page_pixel_discrepancy": (
                    weighted_distance_summary(
                        page_px[
                            indices
                        ],
                        segment_weights,
                    )
                ),
            }
        )

    return results


def strip_private(
    fit: dict[str, Any],
) -> dict[str, Any]:
    return {
        key: value
        for key, value
        in fit.items()
        if not key.startswith(
            "_"
        )
    }


def build_analysis() -> dict[str, Any]:
    parent, all_rows = (
        verify_dependencies()
    )

    limb_radius_px = float(
        parent[
            "provenance"
        ][
            "frozen_limb_reference"
        ][
            "radius_px"
        ]
    )

    fits: dict[str, Any] = {}

    internal: dict[
        tuple[
            int,
            str,
        ],
        dict[
            str,
            Any,
        ],
    ] = {}

    segment_rows: list[
        dict[str, Any]
    ] = []

    for pass_number in (
        1,
        2,
    ):
        rows = [
            row
            for row in all_rows
            if row[
                "pass_number"
            ] == pass_number
        ]

        primary = optimize_translation(
            rows,
            "weight_length",
            PRIMARY_R_TAU_MAX,
            limb_radius_px,
        )

        expanded = optimize_translation(
            rows,
            "weight_length",
            EXPANDED_R_TAU_MAX,
            limb_radius_px,
        )

        secondary = optimize_translation(
            rows,
            "weight_equal_segment",
            PRIMARY_R_TAU_MAX,
            limb_radius_px,
        )

        internal[
            (
                pass_number,
                "primary",
            )
        ] = primary

        internal[
            (
                pass_number,
                "expanded",
            )
        ] = expanded

        internal[
            (
                pass_number,
                "secondary",
            )
        ] = secondary

        fits[
            f"pass{pass_number}"
        ] = {
            "primary_length_weighted": strip_private(
                primary
            ),
            "expanded_bound_primary": strip_private(
                expanded
            ),
            "secondary_equal_segment": strip_private(
                secondary
            ),
            "expanded_bound_sensitivity": (
                compare_bound_sensitivity(
                    primary,
                    expanded,
                )
            ),
            "weighting_sensitivity": (
                compare_primary_fits(
                    primary,
                    secondary,
                )
            ),
        }

        for result in segment_diagnostics(
            rows,
            primary,
        ):
            segment_rows.append(
                {
                    "pass_number": pass_number,
                    "model_variant": (
                        "primary_length_weighted"
                    ),
                    **result,
                }
            )

    primary1 = internal[
        (
            1,
            "primary",
        )
    ]

    primary2 = internal[
        (
            2,
            "primary",
        )
    ]

    pass1_rows = [
        row
        for row in all_rows
        if row[
            "pass_number"
        ] == 1
    ]

    pass2_rows = [
        row
        for row in all_rows
        if row[
            "pass_number"
        ] == 2
    ]

    cross_1_to_2 = fixed_model_evaluation(
        pass2_rows,
        "weight_length",
        primary1,
        limb_radius_px,
    )

    cross_2_to_1 = fixed_model_evaluation(
        pass1_rows,
        "weight_length",
        primary2,
        limb_radius_px,
    )

    return {
        "analysis_class": ANALYSIS_CLASS,
        "checkpoint": (
            "first_hand_spherical_reciprocal_spiral_translated_isotropic_v0.8"
        ),
        "provenance": {
            "protocol": {
                "path": str(
                    PROTOCOL.relative_to(
                        ROOT
                    )
                ),
                "sha256": sha256_path(
                    PROTOCOL
                ),
            },
            "objective_addendum": {
                "path": str(
                    ADDENDUM.relative_to(
                        ROOT
                    )
                ),
                "sha256": sha256_path(
                    ADDENDUM
                ),
            },
            "parent_result": {
                "path": str(
                    PARENT_JSON.relative_to(
                        ROOT
                    )
                ),
                "sha256": sha256_path(
                    PARENT_JSON
                ),
                "seal_verified": True,
            },
            "parent_samples": {
                "path": str(
                    PARENT_SAMPLES.relative_to(
                        ROOT
                    )
                ),
                "sha256": sha256_path(
                    PARENT_SAMPLES
                ),
                "seal_verified": True,
            },
            "frozen_limb_radius_px": (
                limb_radius_px
            ),
        },
        "method": {
            "nonlinear_variables": [
                "r_tau",
                "phi_tau",
            ],
            "nonlinear_parameter_count": 2,
            "a_profiled_analytically": True,
            "m_profiled_analytically": True,
            "objective": (
                "J=SSE/SST=1-weighted_R_squared"
            ),
            "primary_r_tau_max": (
                PRIMARY_R_TAU_MAX
            ),
            "expanded_r_tau_max": (
                EXPANDED_R_TAU_MAX
            ),
            "primary_weighting": (
                "weight_length"
            ),
            "secondary_weighting": (
                "weight_equal_segment"
            ),
            "first_order_signature_used_for_initialization": False,
            "first_order_signature_used_for_bounds": False,
            "coordinate_curves_used": False,
            "scaffold_used": False,
            "endpoint_landmarks_used": False,
            "three_pi_used_in_fit": False,
        },
        "optimizer_specification": {
            "strategy": DE_STRATEGY,
            "maxiter": DE_MAXITER,
            "popsize": DE_POPSIZE,
            "tol": DE_TOL,
            "atol": DE_ATOL,
            "mutation": list(
                DE_MUTATION
            ),
            "recombination": DE_RECOMBINATION,
            "seed": DE_SEED,
            "updating": DE_UPDATING,
            "workers": DE_WORKERS,
            "polish": DE_POLISH,
        },
        "centered_parent_primary": {
            "pass1": parent[
                "fits"
            ][
                "pass1"
            ][
                "primary_length_weighted"
            ],
            "pass2": parent[
                "fits"
            ][
                "pass2"
            ][
                "primary_length_weighted"
            ],
        },
        "fits": fits,
        "cross_pass_primary_replication": (
            compare_primary_fits(
                primary1,
                primary2,
            )
        ),
        "cross_prediction": {
            "pass1_model_on_pass2": (
                cross_1_to_2
            ),
            "pass2_model_on_pass1": (
                cross_2_to_1
            ),
        },
        "segment_diagnostics": (
            segment_rows
        ),
        "interpretation_boundary": {
            "spiral_only_fit": True,
            "finite_translation_established": False,
            "coordinate_predictions_computed": False,
            "three_pi_holdout_used_only_postfit": True,
            "historical_construction_proven": False,
        },
    }


def write_segments_csv(
    analysis: dict[str, Any],
) -> None:
    fields = [
        "pass_number",
        "model_variant",
        "segment_id",
        "sample_count",
        "angular_signed_mean_deg",
        "angular_median_abs_deg",
        "angular_rms_deg",
        "angular_p95_abs_deg",
        "angular_max_abs_deg",
        "transverse_Q_median",
        "transverse_Q_rms",
        "transverse_Q_p95",
        "transverse_Q_max",
        "page_px_median",
        "page_px_rms",
        "page_px_p95",
        "page_px_max",
    ]

    with OUT_SEGMENTS.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=fields,
        )

        writer.writeheader()

        for result in analysis[
            "segment_diagnostics"
        ]:
            angular = result[
                "angular_residual"
            ]

            transverse = result[
                "construction_plane_transverse"
            ]

            page = result[
                "page_pixel_discrepancy"
            ]

            writer.writerow(
                {
                    "pass_number": result[
                        "pass_number"
                    ],
                    "model_variant": result[
                        "model_variant"
                    ],
                    "segment_id": result[
                        "segment_id"
                    ],
                    "sample_count": result[
                        "sample_count"
                    ],
                    "angular_signed_mean_deg": format(
                        angular[
                            "signed_mean_deg"
                        ],
                        ".15g",
                    ),
                    "angular_median_abs_deg": format(
                        angular[
                            "median_abs_deg"
                        ],
                        ".15g",
                    ),
                    "angular_rms_deg": format(
                        angular[
                            "rms_deg"
                        ],
                        ".15g",
                    ),
                    "angular_p95_abs_deg": format(
                        angular[
                            "p95_abs_deg"
                        ],
                        ".15g",
                    ),
                    "angular_max_abs_deg": format(
                        angular[
                            "max_abs_deg"
                        ],
                        ".15g",
                    ),
                    "transverse_Q_median": format(
                        transverse[
                            "median"
                        ],
                        ".15g",
                    ),
                    "transverse_Q_rms": format(
                        transverse[
                            "rms"
                        ],
                        ".15g",
                    ),
                    "transverse_Q_p95": format(
                        transverse[
                            "p95"
                        ],
                        ".15g",
                    ),
                    "transverse_Q_max": format(
                        transverse[
                            "max"
                        ],
                        ".15g",
                    ),
                    "page_px_median": format(
                        page[
                            "median"
                        ],
                        ".15g",
                    ),
                    "page_px_rms": format(
                        page[
                            "rms"
                        ],
                        ".15g",
                    ),
                    "page_px_p95": format(
                        page[
                            "p95"
                        ],
                        ".15g",
                    ),
                    "page_px_max": format(
                        page[
                            "max"
                        ],
                        ".15g",
                    ),
                }
            )


def write_figure(
    analysis: dict[str, Any],
) -> None:
    figure, axes = plt.subplots(
        2,
        2,
        figsize=(
            12,
            10,
        ),
    )

    circle = plt.Circle(
        (
            0.0,
            0.0,
        ),
        1.0,
        fill=False,
        linestyle="--",
    )

    axes[
        0,
        0
    ].add_patch(
        circle
    )

    for pass_number in (
        1,
        2,
    ):
        fit = analysis[
            "fits"
        ][
            f"pass{pass_number}"
        ][
            "primary_length_weighted"
        ]

        expanded = analysis[
            "fits"
        ][
            f"pass{pass_number}"
        ][
            "expanded_bound_primary"
        ]

        axes[
            0,
            0
        ].plot(
            fit[
                "tau_u"
            ],
            fit[
                "tau_v"
            ],
            "o",
            label=(
                f"Pass {pass_number} primary"
            ),
        )

        axes[
            0,
            0
        ].plot(
            expanded[
                "tau_u"
            ],
            expanded[
                "tau_v"
            ],
            "x",
            label=(
                f"Pass {pass_number} expanded"
            ),
        )

    axes[
        0,
        0
    ].set_xlim(
        -1.05,
        1.05,
    )

    axes[
        0,
        0
    ].set_ylim(
        -1.05,
        1.05,
    )

    axes[
        0,
        0
    ].set_aspect(
        "equal",
        adjustable="box",
    )

    axes[
        0,
        0
    ].set_xlabel(
        "tau_u"
    )

    axes[
        0,
        0
    ].set_ylabel(
        "tau_v"
    )

    axes[
        0,
        0
    ].set_title(
        "Recovered construction-origin location"
    )

    axes[
        0,
        0
    ].legend()

    for pass_number in (
        1,
        2,
    ):
        fit = analysis[
            "fits"
        ][
            f"pass{pass_number}"
        ][
            "primary_length_weighted"
        ]

        parent = analysis[
            "centered_parent_primary"
        ][
            f"pass{pass_number}"
        ]

        axes[
            0,
            1
        ].bar(
            [
                2 * pass_number
                - 2,
                2 * pass_number
                - 1,
            ],
            [
                parent[
                    "angular_residual"
                ][
                    "rms_deg"
                ],
                fit[
                    "angular_residual"
                ][
                    "rms_deg"
                ],
            ],
        )

    axes[
        0,
        1
    ].set_xticks(
        [
            0,
            1,
            2,
            3,
        ],
        [
            "P1 centered",
            "P1 translated",
            "P2 centered",
            "P2 translated",
        ],
        rotation=20,
    )

    axes[
        0,
        1
    ].set_ylabel(
        "Angular RMS (deg)"
    )

    axes[
        0,
        1
    ].set_title(
        "Centered vs translated angular residual"
    )

    for pass_number in (
        1,
        2,
    ):
        fit = analysis[
            "fits"
        ][
            f"pass{pass_number}"
        ][
            "primary_length_weighted"
        ]

        axes[
            1,
            0
        ].plot(
            pass_number,
            fit[
                "page_pixel_discrepancy"
            ][
                "rms"
            ],
            "o",
        )

        axes[
            1,
            1
        ].plot(
            pass_number,
            fit[
                "intrinsic_span_holdout"
            ][
                "absolute_span_deg"
            ],
            "o",
        )

    axes[
        1,
        0
    ].set_xticks(
        [
            1,
            2,
        ],
        [
            "Pass 1",
            "Pass 2",
        ],
    )

    axes[
        1,
        0
    ].set_ylabel(
        "Page-space RMS discrepancy (px)"
    )

    axes[
        1,
        0
    ].set_title(
        "Translated-model page discrepancy"
    )

    axes[
        1,
        1
    ].axhline(
        540.0,
        linestyle="--",
        linewidth=1.0,
        label="3π = 540°",
    )

    axes[
        1,
        1
    ].set_xticks(
        [
            1,
            2,
        ],
        [
            "Pass 1",
            "Pass 2",
        ],
    )

    axes[
        1,
        1
    ].set_ylabel(
        "Absolute intrinsic span (deg)"
    )

    axes[
        1,
        1
    ].set_title(
        "Independent 3π span holdout"
    )

    axes[
        1,
        1
    ].legend()

    for axis in axes.flat:
        axis.grid(
            True,
            alpha=0.25,
        )

    figure.tight_layout()

    figure.savefig(
        OUT_PNG,
        dpi=180,
    )

    plt.close(
        figure
    )


def render_fit(
    title: str,
    fit: dict[str, Any],
) -> list[str]:
    angular = fit[
        "angular_residual"
    ]

    page = fit[
        "page_pixel_discrepancy"
    ]

    transverse = fit[
        "construction_plane_transverse"
    ]

    span = fit[
        "intrinsic_span_holdout"
    ]

    return [
        f"### {title}",
        "",
        f"    r_tau                   = {fit['r_tau']:.12f}",
        f"    phi_tau                 = {fit['phi_tau_mod_2pi_deg']:.12f} deg",
        f"    tau_u                   = {fit['tau_u']:.12f}",
        f"    tau_v                   = {fit['tau_v']:.12f}",
        f"    t_x                     = {fit['t_x']:.12f}",
        f"    t_y                     = {fit['t_y']:.12f}",
        f"    |t|                     = {fit['t_magnitude']:.12f}",
        f"    radial-bound distance   = {fit['radial_bound_distance']:.12e}",
        f"    at radial boundary      = {fit['at_radial_search_boundary']}",
        f"    a                       = {fit['a_rad']:.12f} rad",
        f"    alpha0                  = {fit['alpha0_mod_2pi_deg']:.12f} deg",
        f"    m                       = {fit['m_signed']:.12f}",
        f"    handedness              = {fit['handedness']:+d}",
        f"    k                       = {fit['k']:.12f}",
        f"    J                       = {fit['objective_J']:.12f}",
        f"    weighted R^2            = {fit['weighted_r_squared']:.12f}",
        "",
        f"    angular RMS             = {angular['rms_deg']:.12f} deg",
        f"    angular p95             = {angular['p95_abs_deg']:.12f} deg",
        f"    transverse-Q RMS        = {transverse['rms']:.12f}",
        f"    transverse-Q p95        = {transverse['p95']:.12f}",
        f"    page RMS                = {page['rms']:.12f} px",
        f"    page p95                = {page['p95']:.12f} px",
        "",
        f"    intrinsic span          = {span['absolute_span_deg']:.12f} deg",
        f"    span minus 3*pi         = {span['absolute_span_minus_3pi_deg']:.12f} deg",
        "",
    ]


def render_report(
    analysis: dict[str, Any],
) -> str:
    lines = [
        "# First Hand translated-isotropic reciprocal-spiral audit",
        "",
        "**Checkpoint:** v0.8",
        "",
        f"**Analysis class:** `{analysis['analysis_class']}`",
        "",
        "## Scope",
        "",
        "This is the preregistered full translated-isotropic spiral-only model.",
        "",
        "No first-order translation-signature coefficient was used for",
        "initialization, bounds, direction, or tuning.",
        "",
        "No coordinate curve, scaffold, endpoint landmark, or source endpoint",
        "theta convention was used to fit the model.",
        "",
        "The nonlinear search variables are only:",
        "",
        "    r_tau",
        "    phi_tau",
        "",
        "For every candidate translation, a and m are solved analytically.",
        "",
        "The corrected optimization objective is:",
        "",
        "    J = SSE / SST = 1 - weighted R^2.",
        "",
    ]

    for pass_number in (
        1,
        2,
    ):
        fits = analysis[
            "fits"
        ][
            f"pass{pass_number}"
        ]

        lines.extend(
            [
                f"## Pass {pass_number}",
                "",
            ]
        )

        lines.extend(
            render_fit(
                "Primary length-weighted fit",
                fits[
                    "primary_length_weighted"
                ],
            )
        )

        lines.extend(
            render_fit(
                "Mandatory expanded-bound fit",
                fits[
                    "expanded_bound_primary"
                ],
            )
        )

        lines.extend(
            render_fit(
                "Secondary equal-segment fit",
                fits[
                    "secondary_equal_segment"
                ],
            )
        )

        sensitivity = fits[
            "expanded_bound_sensitivity"
        ]

        lines.extend(
            [
                "### Expanded-bound sensitivity",
                "",
                f"    translation separation = {sensitivity['construction_translation_separation']:.12f}",
                f"    tau separation         = {sensitivity['tau_disk_separation']:.12f}",
                f"    objective difference   = {sensitivity['objective_difference_expanded_minus_primary']:.12e}",
                f"    primary at boundary    = {sensitivity['primary_at_boundary']}",
                f"    expanded at boundary   = {sensitivity['expanded_at_boundary']}",
                "",
            ]
        )

    replication = analysis[
        "cross_pass_primary_replication"
    ]

    lines.extend(
        [
            "## Cross-pass primary replication",
            "",
            f"    construction translation separation = {replication['construction_translation_separation']:.12f}",
            f"    tau-disk separation                 = {replication['tau_disk_separation']:.12f}",
            f"    relative |t| difference             = {replication['relative_translation_magnitude_difference']}",
            f"    translation direction difference    = {replication['translation_direction_difference_deg']:.12f} deg",
            f"    |k1-k2|                             = {replication['absolute_k_difference']:.12f}",
            f"    relative k difference               = {replication['relative_k_difference']}",
            f"    alpha0 difference                   = {replication['alpha0_circular_difference_deg']:.12f} deg",
            f"    handedness agrees                   = {replication['handedness_agrees']}",
            "",
            "## Zero-refit cross-prediction",
            "",
        ]
    )

    for label, result in analysis[
        "cross_prediction"
    ].items():
        lines.extend(
            [
                f"### {label}",
                "",
                f"    angular RMS          = {result['angular_residual']['rms_deg']:.12f} deg",
                f"    angular p95          = {result['angular_residual']['p95_abs_deg']:.12f} deg",
                f"    transverse-Q RMS     = {result['construction_plane_transverse']['rms']:.12f}",
                f"    page RMS             = {result['page_pixel_discrepancy']['rms']:.12f} px",
                f"    page p95             = {result['page_pixel_discrepancy']['p95']:.12f} px",
                f"    span                  = {result['intrinsic_span_about_training_origin']['absolute_span_deg']:.12f} deg",
                "",
            ]
        )

    lines.extend(
        [
            "## Interpretation boundary",
            "",
            "A lower objective is not sufficient by itself to support a finite",
            "translated construction origin.",
            "",
            "Interpretation must jointly consider:",
            "",
            "- residual reduction;",
            "- finite versus boundary-seeking translation;",
            "- expanded-bound stability;",
            "- Pass-1 / Pass-2 parameter replication;",
            "- zero-refit cross-prediction;",
            "- page-space geometric residual;",
            "- independent 3*pi span holdout.",
            "",
            "Coordinate curves remain completely unused and therefore available",
            "for a later zero-refit prediction if this model survives.",
            "",
        ]
    )

    return "\n".join(
        lines
    )


def ensure_no_existing_outputs() -> None:
    for path in (
        OUT_JSON,
        OUT_SEGMENTS,
        OUT_PNG,
        OUT_REPORT,
    ):
        if path.exists():
            raise RuntimeError(
                "Refusing to overwrite translated-isotropic "
                f"result artifact: {path}"
            )


def write_outputs(
    analysis: dict[str, Any],
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

    write_segments_csv(
        analysis
    )

    write_figure(
        analysis
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
            "Full translated-isotropic reciprocal-spiral audit."
        )
    )

    parser.add_argument(
        "--check-inputs",
        action="store_true",
        help=(
            "Verify frozen dependencies without evaluating or fitting "
            "the translated model."
        ),
    )

    return parser


def main() -> int:
    args = (
        build_argument_parser()
        .parse_args()
    )

    if args.check_inputs:
        parent, rows = (
            verify_dependencies()
        )

        print(
            "Frozen reciprocal-shape JSON: VERIFIED"
        )

        print(
            "Frozen reciprocal-shape sample table: VERIFIED"
        )

        print(
            "Translated-isotropic parent protocol: VERIFIED"
        )

        print(
            "Translated-isotropic objective addendum: VERIFIED"
        )

        print(
            "Parent checkpoint:",
            parent[
                "checkpoint"
            ],
        )

        print(
            f"Frozen samples: {len(rows)}"
        )

        print(
            f"Pass 1 samples: {sum(row['pass_number'] == 1 for row in rows)}"
        )

        print(
            f"Pass 2 samples: {sum(row['pass_number'] == 2 for row in rows)}"
        )

        print(
            "Primary tau-radius bound: "
            f"{PRIMARY_R_TAU_MAX}"
        )

        print(
            "Expanded tau-radius bound: "
            f"{EXPANDED_R_TAU_MAX}"
        )

        print(
            "Optimizer seed: "
            f"{DE_SEED}"
        )

        print(
            "Optimization objective: J = SSE / SST"
        )

        print(
            "First-order translation signature used: NO"
        )

        print(
            "Coordinate-family inputs used: NO"
        )

        print(
            "Endpoint landmarks used: NO"
        )

        print(
            "3*pi used in fitting: NO"
        )

        print(
            "No translated-isotropic statistic was computed."
        )

        return 0

    ensure_no_existing_outputs()

    analysis = build_analysis()

    write_outputs(
        analysis
    )

    print(
        "="
        * 96
    )

    print(
        "FIRST HAND TRANSLATED-ISOTROPIC RECIPROCAL-SPIRAL AUDIT"
    )

    print(
        "="
        * 96
    )

    for pass_number in (
        1,
        2,
    ):
        fits = analysis[
            "fits"
        ][
            f"pass{pass_number}"
        ]

        primary = fits[
            "primary_length_weighted"
        ]

        expanded = fits[
            "expanded_bound_primary"
        ]

        secondary = fits[
            "secondary_equal_segment"
        ]

        sensitivity = fits[
            "expanded_bound_sensitivity"
        ]

        print(
            f"PASS {pass_number}"
        )

        print(
            "  PRIMARY length-weighted:"
        )

        print(
            f"    r_tau: {primary['r_tau']:.12f}"
        )

        print(
            "    phi_tau: "
            f"{primary['phi_tau_mod_2pi_deg']:.9f} deg"
        )

        print(
            f"    t: ({primary['t_x']:.12f}, "
            f"{primary['t_y']:.12f})"
        )

        print(
            f"    |t|: {primary['t_magnitude']:.12f}"
        )

        print(
            f"    J: {primary['objective_J']:.12f}"
        )

        print(
            "    weighted R^2: "
            f"{primary['weighted_r_squared']:.12f}"
        )

        print(
            f"    k: {primary['k']:.12f}"
        )

        print(
            "    angular RMS: "
            f"{primary['angular_residual']['rms_deg']:.9f} deg"
        )

        print(
            "    page RMS: "
            f"{primary['page_pixel_discrepancy']['rms']:.9f} px"
        )

        print(
            "    page p95: "
            f"{primary['page_pixel_discrepancy']['p95']:.9f} px"
        )

        print(
            "    intrinsic span: "
            f"{primary['intrinsic_span_holdout']['absolute_span_deg']:.9f} deg"
        )

        print(
            "    span - 540 deg: "
            f"{primary['intrinsic_span_holdout']['absolute_span_minus_3pi_deg']:.9f} deg"
        )

        print(
            "    at radial boundary: "
            f"{primary['at_radial_search_boundary']}"
        )

        print(
            "  EXPANDED bound:"
        )

        print(
            f"    r_tau: {expanded['r_tau']:.12f}"
        )

        print(
            f"    |t|: {expanded['t_magnitude']:.12f}"
        )

        print(
            f"    J: {expanded['objective_J']:.12f}"
        )

        print(
            "    at radial boundary: "
            f"{expanded['at_radial_search_boundary']}"
        )

        print(
            "    primary/expanded translation separation: "
            f"{sensitivity['construction_translation_separation']:.12f}"
        )

        print(
            "  SECONDARY equal-segment:"
        )

        print(
            f"    r_tau: {secondary['r_tau']:.12f}"
        )

        print(
            "    phi_tau: "
            f"{secondary['phi_tau_mod_2pi_deg']:.9f} deg"
        )

        print(
            f"    |t|: {secondary['t_magnitude']:.12f}"
        )

        print(
            f"    J: {secondary['objective_J']:.12f}"
        )

        print(
            "-"
            * 96
        )

    replication = analysis[
        "cross_pass_primary_replication"
    ]

    print(
        "CROSS-PASS PRIMARY REPLICATION"
    )

    print(
        "  construction translation separation: "
        f"{replication['construction_translation_separation']:.12f}"
    )

    print(
        "  tau-disk separation: "
        f"{replication['tau_disk_separation']:.12f}"
    )

    print(
        "  relative |t| difference: "
        f"{replication['relative_translation_magnitude_difference']}"
    )

    print(
        "  translation direction difference: "
        f"{replication['translation_direction_difference_deg']:.9f} deg"
    )

    print(
        "  relative k difference: "
        f"{replication['relative_k_difference']}"
    )

    print(
        "  alpha0 difference: "
        f"{replication['alpha0_circular_difference_deg']:.9f} deg"
    )

    print(
        "  handedness agrees: "
        f"{replication['handedness_agrees']}"
    )

    print(
        "-"
        * 96
    )

    print(
        "ZERO-REFIT CROSS-PREDICTION"
    )

    for name, result in analysis[
        "cross_prediction"
    ].items():
        print(
            f"  {name}:"
        )

        print(
            "    angular RMS: "
            f"{result['angular_residual']['rms_deg']:.9f} deg"
        )

        print(
            "    page RMS: "
            f"{result['page_pixel_discrepancy']['rms']:.9f} px"
        )

        print(
            "    page p95: "
            f"{result['page_pixel_discrepancy']['p95']:.9f} px"
        )

    print(
        "-"
        * 96
    )

    print(
        f"Wrote {OUT_JSON}"
    )

    print(
        f"Wrote {OUT_SEGMENTS}"
    )

    print(
        f"Wrote {OUT_PNG}"
    )

    print(
        f"Wrote {OUT_REPORT}"
    )

    print(
        "First-order translation-signature result used: NO"
    )

    print(
        "Coordinate curves used: NO"
    )

    print(
        "3*pi used only as post-fit holdout."
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
