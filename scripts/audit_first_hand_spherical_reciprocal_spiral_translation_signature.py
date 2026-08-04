#!/usr/bin/env python3
"""First-order translation-signature audit for the First Hand spherical spiral.

This is a diagnostic of the already-frozen centered-model residual field.

It does NOT:
- refit the centered reciprocal-spiral model;
- optimize a translated-isotropic model;
- use raw digitization;
- use coordinate curves or scaffold geometry;
- use endpoint landmarks;
- introduce anisotropy, projective freedom, or nonlinear warping.
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


ROOT = Path(__file__).resolve().parents[1]

PROTOCOL = (
    ROOT
    / "docs"
    / "first_hand_spherical_reciprocal_spiral_translation_signature_protocol.md"
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
    / "first_hand_spherical_reciprocal_spiral_translation_signature.json"
)

OUT_RADIAL = (
    OUTPUT_DIR
    / "first_hand_spherical_reciprocal_spiral_translation_signature_radial.csv"
)

OUT_OCCUPANCY = (
    OUTPUT_DIR
    / "first_hand_spherical_reciprocal_spiral_translation_signature_occupancy.csv"
)

OUT_PNG = (
    OUTPUT_DIR
    / "first_hand_spherical_reciprocal_spiral_translation_signature.png"
)

OUT_REPORT = (
    ROOT
    / "reports"
    / "first_hand_spherical_reciprocal_spiral_translation_signature.md"
)

ANALYSIS_CLASS = (
    "first_order_reciprocal_spiral_translation_signature"
)

SEGMENT_IDS = tuple(
    f"S{i:02d}"
    for i in range(1, 11)
)

N_RESAMPLE = 401
N_SEGMENTS = 10
N_PER_PASS = N_RESAMPLE * N_SEGMENTS

TWO_PI = 2.0 * math.pi

RADIAL_EDGES = np.linspace(
    0.0,
    1.0,
    11,
)

PHASE_EDGES = np.linspace(
    0.0,
    TWO_PI,
    37,
)

MIN_PHASE_COVERAGE = math.pi
MAX_HARMONIC_CONDITION = 100.0

REQUIRED_SAMPLE_FIELDS = {
    "pass_number",
    "segment_id",
    "sample_index",
    "rho",
    "F_rho",
    "weight_length",
    "weight_equal_segment",
    "predicted_alpha_length_rad",
    "residual_alpha_length_rad",
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

    actual = sha256_path(
        target
    )

    if actual != matches[0]:
        raise RuntimeError(
            f"SHA-256 verification failed for {target}."
        )


def verify_protocol() -> None:
    text = PROTOCOL.read_text(
        encoding="utf-8"
    ).lower()

    required = (
        "first-order translation basis",
        "parent-design orthogonalization",
        "10 fixed bands",
        "phase_coverage",
        "insufficient_phase_coverage",
        "no nonlinear translated fit",
    )

    for token in required:
        if token not in text:
            raise RuntimeError(
                f"Frozen translation-signature protocol "
                f"missing token: {token!r}"
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
            f"Non-finite {field} in frozen parent table."
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
                "Frozen parent table missing fields: "
                + ", ".join(
                    sorted(missing)
                )
            )

        raw_rows = list(reader)

    if len(raw_rows) != 2 * N_PER_PASS:
        raise RuntimeError(
            f"Expected {2 * N_PER_PASS} frozen samples; "
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

        if pass_number not in (1, 2):
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
                "q": (
                    global_index
                    / (
                        N_PER_PASS
                        - 1
                    )
                ),
                "rho": parse_float(
                    raw,
                    "rho",
                ),
                "F_rho": parse_float(
                    raw,
                    "F_rho",
                ),
                "weight_length": parse_float(
                    raw,
                    "weight_length",
                ),
                "weight_equal_segment": parse_float(
                    raw,
                    "weight_equal_segment",
                ),
                "beta_hat": parse_float(
                    raw,
                    "predicted_alpha_length_rad",
                ),
                "residual": parse_float(
                    raw,
                    "residual_alpha_length_rad",
                ),
            }
        )

    keys = set()

    for row in rows:
        key = (
            row["pass_number"],
            row["segment_id"],
            row["sample_index"],
        )

        if key in keys:
            raise RuntimeError(
                f"Duplicate frozen sample key: {key}"
            )

        keys.add(key)

    for pass_number in (1, 2):
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
                row["sample_index"]
                for row in selected
                if row[
                    "segment_id"
                ] == segment_id
            )

            if indices != list(
                range(N_RESAMPLE)
            ):
                raise RuntimeError(
                    f"Pass {pass_number} {segment_id} "
                    "does not contain sample indices 0..400."
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

    model = data.get(
        "model",
        {},
    )

    if (
        model.get("linear_shape_relation")
        != "alpha_unwrapped=a+m*F(rho)"
    ):
        raise RuntimeError(
            "Frozen parent model identity mismatch."
        )

    return data


def verify_dependencies() -> tuple[
    dict[str, Any],
    list[dict[str, Any]],
]:
    for path in (
        PROTOCOL,
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

    verify_protocol()

    parent = verify_parent_json()

    rows = read_samples()

    return (
        parent,
        rows,
    )


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
        0.0 <= quantile <= 1.0
    ):
        raise ValueError(
            "quantile must lie in [0,1]."
        )

    if np.any(weights < 0.0):
        raise ValueError(
            "weights must be non-negative."
        )

    total = float(
        np.sum(weights)
    )

    if total <= 0.0:
        raise ValueError(
            "weights must have positive total."
        )

    order = np.argsort(
        values,
        kind="mergesort",
    )

    values = values[order]
    weights = weights[order]

    cumulative = np.cumsum(
        weights
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
        len(values) - 1,
    )

    return float(
        values[index]
    )


def weighted_residual_summary(
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

    weight_total = float(
        np.sum(weights)
    )

    mean_abs = float(
        np.sum(
            weights
            * absolute
        )
        / weight_total
    )

    rms = math.sqrt(
        float(
            np.sum(
                weights
                * residual
                * residual
            )
            / weight_total
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
        np.max(absolute)
    )

    return {
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


def solve_weighted_normal(
    design: np.ndarray,
    values: np.ndarray,
    weights: np.ndarray,
) -> np.ndarray:
    design = np.asarray(
        design,
        dtype=float,
    )

    values = np.asarray(
        values,
        dtype=float,
    )

    weights = np.asarray(
        weights,
        dtype=float,
    )

    normal = (
        design.T
        @ (
            weights[
                :,
                None
            ]
            * design
        )
    )

    rhs = (
        design.T
        @ (
            weights
            * values
        )
    )

    condition = float(
        np.linalg.cond(
            normal
        )
    )

    if (
        not math.isfinite(condition)
        or condition > 1e14
    ):
        raise RuntimeError(
            "Weighted normal system is singular or ill-conditioned."
        )

    return np.linalg.solve(
        normal,
        rhs,
    )


def orthogonalize_translation_basis(
    F_rho: np.ndarray,
    beta_hat: np.ndarray,
    weights: np.ndarray,
) -> tuple[
    np.ndarray,
    np.ndarray,
]:
    F_rho = np.asarray(
        F_rho,
        dtype=float,
    )

    beta_hat = np.asarray(
        beta_hat,
        dtype=float,
    )

    weights = np.asarray(
        weights,
        dtype=float,
    )

    X0 = np.column_stack(
        (
            np.ones_like(
                F_rho
            ),
            F_rho,
        )
    )

    G = np.column_stack(
        (
            -F_rho
            * np.sin(
                beta_hat
            ),
            F_rho
            * np.cos(
                beta_hat
            ),
        )
    )

    normal = (
        X0.T
        @ (
            weights[
                :,
                None
            ]
            * X0
        )
    )

    rhs = (
        X0.T
        @ (
            weights[
                :,
                None
            ]
            * G
        )
    )

    condition = float(
        np.linalg.cond(
            normal
        )
    )

    if (
        not math.isfinite(condition)
        or condition > 1e14
    ):
        raise RuntimeError(
            "Parent design orthogonalization is singular."
        )

    projection_coefficients = np.linalg.solve(
        normal,
        rhs,
    )

    G_perp = (
        G
        - X0
        @ projection_coefficients
    )

    return (
        G_perp,
        projection_coefficients,
    )


def translation_signature_fit(
    rows: Sequence[
        dict[str, Any]
    ],
    weight_field: str,
) -> dict[str, Any]:
    F_rho = np.array(
        [
            row["F_rho"]
            for row in rows
        ],
        dtype=float,
    )

    beta_hat = np.array(
        [
            row["beta_hat"]
            for row in rows
        ],
        dtype=float,
    )

    residual = np.array(
        [
            row["residual"]
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
            "Translation-signature weights must be positive."
        )

    G_perp, parent_projection = (
        orthogonalize_translation_basis(
            F_rho,
            beta_hat,
            weights,
        )
    )

    coefficients = solve_weighted_normal(
        G_perp,
        residual,
        weights,
    )

    fitted_signature = (
        G_perp
        @ coefficients
    )

    remaining = (
        residual
        - fitted_signature
    )

    parent_sse = float(
        np.sum(
            weights
            * residual
            * residual
        )
    )

    remaining_sse = float(
        np.sum(
            weights
            * remaining
            * remaining
        )
    )

    fraction_explained = (
        1.0
        - remaining_sse
        / parent_sse
    )

    c_x = float(
        coefficients[0]
    )

    c_y = float(
        coefficients[1]
    )

    magnitude = math.hypot(
        c_x,
        c_y,
    )

    direction = math.atan2(
        c_y,
        c_x,
    )

    parent_orthogonality = (
        np.column_stack(
            (
                np.ones_like(
                    F_rho
                ),
                F_rho,
            )
        ).T
        @ (
            weights[
                :,
                None
            ]
            * G_perp
        )
    )

    return {
        "weighting": weight_field,
        "sample_count": len(rows),
        "c_x": c_x,
        "c_y": c_y,
        "magnitude": magnitude,
        "direction_rad": direction,
        "direction_mod_2pi_rad": (
            direction
            % TWO_PI
        ),
        "direction_mod_2pi_deg": math.degrees(
            direction
            % TWO_PI
        ),
        "parent_weighted_sse_rad2": parent_sse,
        "remaining_weighted_sse_rad2": remaining_sse,
        "fraction_parent_sse_explained": fraction_explained,
        "remaining_residual": weighted_residual_summary(
            remaining,
            weights,
        ),
        "orthogonalization_max_abs": float(
            np.max(
                np.abs(
                    parent_orthogonality
                )
            )
        ),
        "parent_projection_coefficients": (
            parent_projection.tolist()
        ),
        "_signature": fitted_signature,
        "_remaining": remaining,
        "_weights": weights,
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


def compare_coefficient_vectors(
    fit1: dict[str, Any],
    fit2: dict[str, Any],
) -> dict[str, Any]:
    separation = math.hypot(
        fit1["c_x"]
        - fit2["c_x"],
        fit1["c_y"]
        - fit2["c_y"],
    )

    m1 = fit1[
        "magnitude"
    ]

    m2 = fit2[
        "magnitude"
    ]

    denominator = (
        m1
        + m2
    )

    relative = (
        2.0
        * abs(
            m1
            - m2
        )
        / denominator
        if denominator > 0.0
        else None
    )

    direction_difference = abs(
        circular_difference(
            fit1[
                "direction_rad"
            ],
            fit2[
                "direction_rad"
            ],
        )
    )

    return {
        "euclidean_coefficient_separation": separation,
        "relative_magnitude_difference": relative,
        "circular_direction_difference_rad": direction_difference,
        "circular_direction_difference_deg": math.degrees(
            direction_difference
        ),
    }


def phase_coverage(
    phases: np.ndarray,
) -> tuple[
    float,
    float,
]:
    phases = np.asarray(
        phases,
        dtype=float,
    ) % TWO_PI

    if len(phases) < 2:
        return (
            0.0,
            TWO_PI,
        )

    ordered = np.sort(
        phases
    )

    internal_gaps = np.diff(
        ordered
    )

    wrap_gap = (
        ordered[0]
        + TWO_PI
        - ordered[-1]
    )

    largest_gap = float(
        max(
            np.max(
                internal_gaps
            ),
            wrap_gap,
        )
    )

    coverage = (
        TWO_PI
        - largest_gap
    )

    return (
        coverage,
        largest_gap,
    )


def phase_bin_index(
    phase: float,
) -> int:
    phase = (
        phase
        % TWO_PI
    )

    index = int(
        np.searchsorted(
            PHASE_EDGES,
            phase,
            side="right",
        )
        - 1
    )

    return min(
        max(
            index,
            0,
        ),
        35,
    )


def radial_bin_index(
    rho: float,
) -> int:
    if rho == 1.0:
        return 9

    index = int(
        np.searchsorted(
            RADIAL_EDGES,
            rho,
            side="right",
        )
        - 1
    )

    return index


def harmonic_band_fit(
    rows: Sequence[
        dict[str, Any]
    ],
) -> dict[str, Any]:
    phases = np.array(
        [
            row["beta_hat"]
            % TWO_PI
            for row in rows
        ],
        dtype=float,
    )

    residual = np.array(
        [
            row["residual"]
            for row in rows
        ],
        dtype=float,
    )

    weights = np.array(
        [
            row["weight_length"]
            for row in rows
        ],
        dtype=float,
    )

    F_rho = np.array(
        [
            row["F_rho"]
            for row in rows
        ],
        dtype=float,
    )

    coverage, largest_gap = (
        phase_coverage(
            phases
        )
    )

    occupancy = np.zeros(
        36,
        dtype=int,
    )

    for phase in phases:
        occupancy[
            phase_bin_index(
                phase
            )
        ] += 1

    design = np.column_stack(
        (
            np.ones_like(
                phases
            ),
            np.cos(
                phases
            ),
            np.sin(
                phases
            ),
        )
    )

    weighted_design = (
        np.sqrt(
            weights
        )[
            :,
            None
        ]
        * design
    )

    condition = float(
        np.linalg.cond(
            weighted_design
        )
    )

    eligible = bool(
        coverage
        >= MIN_PHASE_COVERAGE
        and math.isfinite(
            condition
        )
        and condition
        <= MAX_HARMONIC_CONDITION
    )

    base: dict[str, Any] = {
        "sample_count": len(rows),
        "phase_coverage_rad": coverage,
        "phase_coverage_deg": math.degrees(
            coverage
        ),
        "largest_phase_gap_rad": largest_gap,
        "largest_phase_gap_deg": math.degrees(
            largest_gap
        ),
        "occupied_phase_bins": int(
            np.count_nonzero(
                occupancy
            )
        ),
        "phase_bin_occupancy": occupancy.tolist(),
        "weighted_design_condition_number": condition,
        "eligible": eligible,
        "status": (
            "ELIGIBLE"
            if eligible
            else "INSUFFICIENT_PHASE_COVERAGE"
        ),
        "F_bar": float(
            np.sum(
                weights
                * F_rho
            )
            / np.sum(
                weights
            )
        ),
    }

    if not eligible:
        base.update(
            {
                "c0_rad": None,
                "cosine_coefficient_rad": None,
                "sine_coefficient_rad": None,
                "amplitude_rad": None,
                "amplitude_deg": None,
                "phase_axis_rad": None,
                "phase_axis_deg": None,
                "amplitude_over_F_bar": None,
            }
        )

        return base

    coefficients = solve_weighted_normal(
        design,
        residual,
        weights,
    )

    c0 = float(
        coefficients[0]
    )

    cosine = float(
        coefficients[1]
    )

    sine = float(
        coefficients[2]
    )

    amplitude = math.hypot(
        cosine,
        sine,
    )

    phase_axis = math.atan2(
        sine,
        cosine,
    ) % TWO_PI

    F_bar = base[
        "F_bar"
    ]

    base.update(
        {
            "c0_rad": c0,
            "c0_deg": math.degrees(
                c0
            ),
            "cosine_coefficient_rad": cosine,
            "sine_coefficient_rad": sine,
            "amplitude_rad": amplitude,
            "amplitude_deg": math.degrees(
                amplitude
            ),
            "phase_axis_rad": phase_axis,
            "phase_axis_deg": math.degrees(
                phase_axis
            ),
            "amplitude_over_F_bar": (
                amplitude
                / F_bar
                if F_bar != 0.0
                else None
            ),
        }
    )

    return base


def radial_band_results(
    rows: Sequence[
        dict[str, Any]
    ],
) -> tuple[
    list[
        dict[str, Any]
    ],
    dict[str, Any],
]:
    output: list[
        dict[str, Any]
    ] = []

    summary: dict[
        str,
        Any
    ] = {}

    for pass_number in (
        1,
        2,
    ):
        pass_rows = [
            row
            for row in rows
            if row[
                "pass_number"
            ] == pass_number
        ]

        ratios = []

        for index in range(10):
            selected = [
                row
                for row in pass_rows
                if (
                    radial_bin_index(
                        row["rho"]
                    )
                    == index
                )
            ]

            base = {
                "pass_number": pass_number,
                "radial_bin_index": index,
                "rho_left": float(
                    RADIAL_EDGES[index]
                ),
                "rho_right": float(
                    RADIAL_EDGES[index + 1]
                ),
            }

            if not selected:
                result = {
                    **base,
                    "sample_count": 0,
                    "phase_coverage_rad": None,
                    "phase_coverage_deg": None,
                    "largest_phase_gap_rad": None,
                    "largest_phase_gap_deg": None,
                    "occupied_phase_bins": 0,
                    "weighted_design_condition_number": None,
                    "eligible": False,
                    "status": "EMPTY",
                    "F_bar": None,
                    "c0_rad": None,
                    "c0_deg": None,
                    "cosine_coefficient_rad": None,
                    "sine_coefficient_rad": None,
                    "amplitude_rad": None,
                    "amplitude_deg": None,
                    "phase_axis_rad": None,
                    "phase_axis_deg": None,
                    "amplitude_over_F_bar": None,
                }

            else:
                result = {
                    **base,
                    **harmonic_band_fit(
                        selected
                    ),
                }

            output.append(
                result
            )

            if (
                result[
                    "eligible"
                ]
                and result[
                    "amplitude_over_F_bar"
                ]
                is not None
            ):
                ratios.append(
                    float(
                        result[
                            "amplitude_over_F_bar"
                        ]
                    )
                )

        if len(ratios) >= 3:
            array = np.array(
                ratios,
                dtype=float,
            )

            mean = float(
                np.mean(
                    array
                )
            )

            std = float(
                np.std(
                    array,
                    ddof=0,
                )
            )

            summary[
                f"pass{pass_number}"
            ] = {
                "eligible_band_count": len(
                    ratios
                ),
                "status": (
                    "RADIAL_AMPLITUDE_TEST_IDENTIFIABLE"
                ),
                "amplitude_over_F_mean": mean,
                "amplitude_over_F_std": std,
                "amplitude_over_F_cv": (
                    std
                    / abs(mean)
                    if mean != 0.0
                    else None
                ),
                "amplitude_over_F_min": float(
                    np.min(
                        array
                    )
                ),
                "amplitude_over_F_max": float(
                    np.max(
                        array
                    )
                ),
            }

        else:
            summary[
                f"pass{pass_number}"
            ] = {
                "eligible_band_count": len(
                    ratios
                ),
                "status": (
                    "RADIAL_AMPLITUDE_TEST_NOT_IDENTIFIABLE"
                ),
                "amplitude_over_F_mean": None,
                "amplitude_over_F_std": None,
                "amplitude_over_F_cv": None,
                "amplitude_over_F_min": None,
                "amplitude_over_F_max": None,
            }

    return (
        output,
        summary,
    )


def occupancy_results(
    rows: Sequence[
        dict[str, Any]
    ],
) -> list[
    dict[str, Any]
]:
    output = []

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

        counts = np.zeros(
            (
                10,
                36,
            ),
            dtype=int,
        )

        for row in selected:
            radial_index = (
                radial_bin_index(
                    row["rho"]
                )
            )

            phase_index = (
                phase_bin_index(
                    row["beta_hat"]
                )
            )

            if (
                radial_index
                < 0
                or radial_index
                > 9
            ):
                raise RuntimeError(
                    "Frozen rho lies outside [0,1]."
                )

            counts[
                radial_index,
                phase_index,
            ] += 1

        for radial_index in range(10):
            for phase_index in range(36):
                output.append(
                    {
                        "pass_number": pass_number,
                        "radial_bin_index": radial_index,
                        "rho_left": float(
                            RADIAL_EDGES[
                                radial_index
                            ]
                        ),
                        "rho_right": float(
                            RADIAL_EDGES[
                                radial_index
                                + 1
                            ]
                        ),
                        "phase_bin_index": phase_index,
                        "phase_left_deg": (
                            10.0
                            * phase_index
                        ),
                        "phase_right_deg": (
                            10.0
                            * (
                                phase_index
                                + 1
                            )
                        ),
                        "sample_count": int(
                            counts[
                                radial_index,
                                phase_index,
                            ]
                        ),
                    }
                )

    return output


def strip_private(
    fit: dict[str, Any],
) -> dict[str, Any]:
    return {
        key: value
        for key, value
        in fit.items()
        if not key.startswith("_")
    }


def build_analysis() -> dict[str, Any]:
    parent, rows = (
        verify_dependencies()
    )

    fits: dict[
        str,
        Any
    ] = {}

    internal_fits: dict[
        tuple[
            int,
            str,
        ],
        dict[
            str,
            Any,
        ],
    ] = {}

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

        primary = translation_signature_fit(
            selected,
            "weight_length",
        )

        secondary = translation_signature_fit(
            selected,
            "weight_equal_segment",
        )

        without_s04 = [
            row
            for row in selected
            if row[
                "segment_id"
            ] != "S04"
        ]

        s04_sensitivity = (
            translation_signature_fit(
                without_s04,
                "weight_length",
            )
        )

        fits[
            f"pass{pass_number}"
        ] = {
            "primary_length_weighted": strip_private(
                primary
            ),
            "secondary_equal_segment": strip_private(
                secondary
            ),
            "s04_excluded_primary_sensitivity": strip_private(
                s04_sensitivity
            ),
            "weighting_sensitivity": {
                "coefficient_separation": math.hypot(
                    primary[
                        "c_x"
                    ]
                    - secondary[
                        "c_x"
                    ],
                    primary[
                        "c_y"
                    ]
                    - secondary[
                        "c_y"
                    ],
                ),
                "relative_magnitude_difference": (
                    2.0
                    * abs(
                        primary[
                            "magnitude"
                        ]
                        - secondary[
                            "magnitude"
                        ]
                    )
                    / (
                        primary[
                            "magnitude"
                        ]
                        + secondary[
                            "magnitude"
                        ]
                    )
                    if (
                        primary[
                            "magnitude"
                        ]
                        + secondary[
                            "magnitude"
                        ]
                    ) > 0.0
                    else None
                ),
                "direction_difference_deg": math.degrees(
                    abs(
                        circular_difference(
                            primary[
                                "direction_rad"
                            ],
                            secondary[
                                "direction_rad"
                            ],
                        )
                    )
                ),
            },
            "s04_sensitivity": {
                "coefficient_separation": math.hypot(
                    primary[
                        "c_x"
                    ]
                    - s04_sensitivity[
                        "c_x"
                    ],
                    primary[
                        "c_y"
                    ]
                    - s04_sensitivity[
                        "c_y"
                    ],
                ),
                "direction_difference_deg": math.degrees(
                    abs(
                        circular_difference(
                            primary[
                                "direction_rad"
                            ],
                            s04_sensitivity[
                                "direction_rad"
                            ],
                        )
                    )
                ),
                "fraction_explained_difference": (
                    s04_sensitivity[
                        "fraction_parent_sse_explained"
                    ]
                    - primary[
                        "fraction_parent_sse_explained"
                    ]
                ),
            },
        }

        internal_fits[
            (
                pass_number,
                "primary",
            )
        ] = primary

    crosspass_primary = compare_coefficient_vectors(
        internal_fits[
            (
                1,
                "primary",
            )
        ],
        internal_fits[
            (
                2,
                "primary",
            )
        ],
    )

    crosspass_secondary = (
        compare_coefficient_vectors(
            fits[
                "pass1"
            ][
                "secondary_equal_segment"
            ],
            fits[
                "pass2"
            ][
                "secondary_equal_segment"
            ],
        )
    )

    radial, radial_summary = (
        radial_band_results(
            rows
        )
    )

    occupancy = occupancy_results(
        rows
    )

    return {
        "analysis_class": ANALYSIS_CLASS,
        "checkpoint": (
            "first_hand_spherical_reciprocal_spiral_translation_signature_v0.8"
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
            "parent_checkpoint": parent[
                "checkpoint"
            ],
        },
        "method": {
            "parent_model_refitted": False,
            "nonlinear_optimizer_calls": 0,
            "new_nonlinear_parameters": 0,
            "basis": (
                "[-F(rho)*sin(beta_hat), "
                "F(rho)*cos(beta_hat)]"
            ),
            "parent_design": "[1,F(rho)]",
            "parent_design_orthogonalized": True,
            "primary_weighting": "weight_length",
            "secondary_weighting": (
                "weight_equal_segment"
            ),
            "S04_primary_excluded": False,
            "radial_band_count": 10,
            "phase_bin_count": 36,
            "minimum_phase_coverage_rad": (
                MIN_PHASE_COVERAGE
            ),
            "maximum_harmonic_condition_number": (
                MAX_HARMONIC_CONDITION
            ),
        },
        "fits": fits,
        "crosspass": {
            "primary_length_weighted": (
                crosspass_primary
            ),
            "secondary_equal_segment": (
                crosspass_secondary
            ),
        },
        "radial_bands": radial,
        "radial_amplitude_summary": (
            radial_summary
        ),
        "occupancy": occupancy,
        "interpretation_boundary": {
            "first_order_translation_signature_only": True,
            "translated_model_fitted": False,
            "coordinate_family_compared": False,
            "historical_intent_established": False,
        },
    }


def write_radial_csv(
    analysis: dict[str, Any],
) -> None:
    fields = [
        "pass_number",
        "radial_bin_index",
        "rho_left",
        "rho_right",
        "sample_count",
        "phase_coverage_deg",
        "largest_phase_gap_deg",
        "occupied_phase_bins",
        "weighted_design_condition_number",
        "eligible",
        "status",
        "F_bar",
        "c0_deg",
        "amplitude_deg",
        "phase_axis_deg",
        "amplitude_over_F_bar",
    ]

    with OUT_RADIAL.open(
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
            "radial_bands"
        ]:
            row = {}

            for field in fields:
                value = result.get(
                    field
                )

                if isinstance(
                    value,
                    float,
                ):
                    row[field] = format(
                        value,
                        ".15g",
                    )

                elif value is None:
                    row[field] = ""

                else:
                    row[field] = value

            writer.writerow(
                row
            )


def write_occupancy_csv(
    analysis: dict[str, Any],
) -> None:
    fields = [
        "pass_number",
        "radial_bin_index",
        "rho_left",
        "rho_right",
        "phase_bin_index",
        "phase_left_deg",
        "phase_right_deg",
        "sample_count",
    ]

    with OUT_OCCUPANCY.open(
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
            "occupancy"
        ]:
            row = {}

            for field in fields:
                value = result[
                    field
                ]

                if isinstance(
                    value,
                    float,
                ):
                    row[field] = format(
                        value,
                        ".15g",
                    )
                else:
                    row[field] = value

            writer.writerow(
                row
            )


def write_figure(
    analysis: dict[str, Any],
) -> None:
    figure, axes = plt.subplots(
        1,
        2,
        figsize=(
            12,
            5,
        ),
    )

    for pass_number in (
        1,
        2,
    ):
        radial = [
            row
            for row in analysis[
                "radial_bands"
            ]
            if (
                row[
                    "pass_number"
                ] == pass_number
                and row[
                    "eligible"
                ]
            )
        ]

        if radial:
            centers = np.array(
                [
                    0.5
                    * (
                        row[
                            "rho_left"
                        ]
                        + row[
                            "rho_right"
                        ]
                    )
                    for row in radial
                ]
            )

            ratios = np.array(
                [
                    row[
                        "amplitude_over_F_bar"
                    ]
                    for row in radial
                ]
            )

            axes[
                0
            ].plot(
                centers,
                ratios,
                "o-",
                label=f"Pass {pass_number}",
            )

    axes[
        0
    ].set_xlabel(
        "rho-band centre"
    )

    axes[
        0
    ].set_ylabel(
        "harmonic-1 amplitude / mean F(rho)"
    )

    axes[
        0
    ].set_title(
        "First-order radial scaling"
    )

    axes[
        0
    ].grid(
        True,
        alpha=0.25,
    )

    axes[
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

        axes[
            1
        ].arrow(
            0.0,
            0.0,
            fit[
                "c_x"
            ],
            fit[
                "c_y"
            ],
            length_includes_head=True,
            head_width=max(
                fit[
                    "magnitude"
                ]
                * 0.04,
                1e-4,
            ),
            label=f"Pass {pass_number}",
        )

        axes[
            1
        ].plot(
            fit[
                "c_x"
            ],
            fit[
                "c_y"
            ],
            "o",
        )

    axes[
        1
    ].axhline(
        0.0,
        linewidth=0.8,
    )

    axes[
        1
    ].axvline(
        0.0,
        linewidth=0.8,
    )

    axes[
        1
    ].set_xlabel(
        "c_x"
    )

    axes[
        1
    ].set_ylabel(
        "c_y"
    )

    axes[
        1
    ].set_title(
        "Independent translation-signature vectors"
    )

    axes[
        1
    ].grid(
        True,
        alpha=0.25,
    )

    axes[
        1
    ].set_aspect(
        "equal",
        adjustable="datalim",
    )

    figure.tight_layout()

    figure.savefig(
        OUT_PNG,
        dpi=180,
    )

    plt.close(
        figure
    )


def render_report(
    analysis: dict[str, Any],
) -> str:
    lines = [
        "# First Hand reciprocal-spiral translation signature",
        "",
        "**Checkpoint:** v0.8",
        "",
        f"**Analysis class:** `{analysis['analysis_class']}`",
        "",
        "## Scope",
        "",
        "This audit tests the first-order residual signature expected from",
        "displacement of the construction origin.",
        "",
        "The frozen centered reciprocal-spiral model was not refitted.",
        "",
        "No nonlinear translated model was optimized.",
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

        primary = fits[
            "primary_length_weighted"
        ]

        secondary = fits[
            "secondary_equal_segment"
        ]

        s04 = fits[
            "s04_excluded_primary_sensitivity"
        ]

        lines.extend(
            [
                f"## Pass {pass_number}",
                "",
                "### Primary length-weighted signature",
                "",
                f"    c_x                         = {primary['c_x']:.12f}",
                f"    c_y                         = {primary['c_y']:.12f}",
                f"    |c|                         = {primary['magnitude']:.12f}",
                f"    direction                   = {primary['direction_mod_2pi_deg']:.12f} deg",
                f"    parent SSE explained        = {primary['fraction_parent_sse_explained']:.12f}",
                f"    remaining angular RMS       = {primary['remaining_residual']['rms_deg']:.12f} deg",
                f"    remaining angular p95       = {primary['remaining_residual']['p95_abs_deg']:.12f} deg",
                "",
                "### Equal-segment sensitivity",
                "",
                f"    |c|                         = {secondary['magnitude']:.12f}",
                f"    direction                   = {secondary['direction_mod_2pi_deg']:.12f} deg",
                f"    parent SSE explained        = {secondary['fraction_parent_sse_explained']:.12f}",
                "",
                "### S04-excluded sensitivity",
                "",
                f"    |c|                         = {s04['magnitude']:.12f}",
                f"    direction                   = {s04['direction_mod_2pi_deg']:.12f} deg",
                f"    parent SSE explained        = {s04['fraction_parent_sse_explained']:.12f}",
                "",
            ]
        )

    primary_cross = analysis[
        "crosspass"
    ][
        "primary_length_weighted"
    ]

    lines.extend(
        [
            "## Cross-pass primary replication",
            "",
            f"    coefficient separation      = {primary_cross['euclidean_coefficient_separation']:.12f}",
            f"    relative magnitude diff     = {primary_cross['relative_magnitude_difference']}",
            f"    direction difference        = {primary_cross['circular_direction_difference_deg']:.12f} deg",
            "",
            "## Radial amplitude diagnostic",
            "",
        ]
    )

    for pass_number in (
        1,
        2,
    ):
        summary = analysis[
            "radial_amplitude_summary"
        ][
            f"pass{pass_number}"
        ]

        lines.extend(
            [
                f"### Pass {pass_number}",
                "",
                f"    eligible bands              = {summary['eligible_band_count']}",
                f"    status                      = {summary['status']}",
                f"    amplitude/F mean            = {summary['amplitude_over_F_mean']}",
                f"    amplitude/F std             = {summary['amplitude_over_F_std']}",
                f"    amplitude/F CV              = {summary['amplitude_over_F_cv']}",
                "",
            ]
        )

    lines.extend(
        [
            "## Interpretation boundary",
            "",
            "The numerical result measures only the first-order translation",
            "signature contained in the already-frozen centered-model residual.",
            "",
            "It does not establish a finite translated reciprocal-spiral model.",
            "",
            "The separately preregistered nonlinear translated-isotropic test",
            "remains dormant until this result is frozen and interpreted.",
            "",
        ]
    )

    return "\n".join(
        lines
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

    write_radial_csv(
        analysis
    )

    write_occupancy_csv(
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
            "First-order translation-signature audit for the "
            "First Hand spherical reciprocal spiral."
        )
    )

    parser.add_argument(
        "--check-inputs",
        action="store_true",
        help=(
            "Verify frozen inputs without computing the "
            "translation signature."
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
            "Frozen translation-signature protocol: VERIFIED"
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
            "Parent fit recomputed: NO"
        )

        print(
            "Nonlinear translated model fit: NO"
        )

        print(
            "Coordinate-family inputs used: NO"
        )

        print(
            "No translation-signature statistic was computed."
        )

        return 0

    analysis = build_analysis()

    write_outputs(
        analysis
    )

    print(
        "="
        * 88
    )

    print(
        "FIRST HAND RECIPROCAL-SPIRAL TRANSLATION SIGNATURE"
    )

    print(
        "="
        * 88
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

        secondary = fits[
            "secondary_equal_segment"
        ]

        s04 = fits[
            "s04_excluded_primary_sensitivity"
        ]

        radial = analysis[
            "radial_amplitude_summary"
        ][
            f"pass{pass_number}"
        ]

        print(
            f"PASS {pass_number}"
        )

        print(
            "  PRIMARY length-weighted:"
        )

        print(
            f"    c_x: {primary['c_x']:.12f}"
        )

        print(
            f"    c_y: {primary['c_y']:.12f}"
        )

        print(
            f"    |c|: {primary['magnitude']:.12f}"
        )

        print(
            "    direction: "
            f"{primary['direction_mod_2pi_deg']:.9f} deg"
        )

        print(
            "    parent SSE explained: "
            f"{primary['fraction_parent_sse_explained']:.12f}"
        )

        print(
            "    remaining angular RMS: "
            f"{primary['remaining_residual']['rms_deg']:.9f} deg"
        )

        print(
            "    remaining angular p95: "
            f"{primary['remaining_residual']['p95_abs_deg']:.9f} deg"
        )

        print(
            "  SECONDARY equal-segment:"
        )

        print(
            f"    |c|: {secondary['magnitude']:.12f}"
        )

        print(
            "    direction: "
            f"{secondary['direction_mod_2pi_deg']:.9f} deg"
        )

        print(
            "    parent SSE explained: "
            f"{secondary['fraction_parent_sse_explained']:.12f}"
        )

        print(
            "  S04-EXCLUDED sensitivity:"
        )

        print(
            f"    |c|: {s04['magnitude']:.12f}"
        )

        print(
            "    direction: "
            f"{s04['direction_mod_2pi_deg']:.9f} deg"
        )

        print(
            "    parent SSE explained: "
            f"{s04['fraction_parent_sse_explained']:.12f}"
        )

        print(
            "  RADIAL amplitude test:"
        )

        print(
            "    eligible bands: "
            f"{radial['eligible_band_count']}"
        )

        print(
            "    status: "
            f"{radial['status']}"
        )

        if (
            radial[
                "amplitude_over_F_cv"
            ]
            is not None
        ):
            print(
                "    amplitude/F mean: "
                f"{radial['amplitude_over_F_mean']:.12f}"
            )

            print(
                "    amplitude/F CV: "
                f"{radial['amplitude_over_F_cv']:.12f}"
            )

        print(
            "-"
            * 88
        )

    cross = analysis[
        "crosspass"
    ][
            "primary_length_weighted"
    ]

    print(
        "CROSS-PASS PRIMARY TRANSLATION-SIGNATURE REPLICATION"
    )

    print(
        "  coefficient separation: "
        f"{cross['euclidean_coefficient_separation']:.12f}"
    )

    print(
        "  relative magnitude difference: "
        f"{cross['relative_magnitude_difference']}"
    )

    print(
        "  direction difference: "
        f"{cross['circular_direction_difference_deg']:.9f} deg"
    )

    print(
        "-"
        * 88
    )

    print(
        f"Wrote {OUT_JSON}"
    )

    print(
        f"Wrote {OUT_RADIAL}"
    )

    print(
        f"Wrote {OUT_OCCUPANCY}"
    )

    print(
        f"Wrote {OUT_PNG}"
    )

    print(
        f"Wrote {OUT_REPORT}"
    )

    print(
        "Parent model refitted: NO"
    )

    print(
        "Nonlinear translated-isotropic model fit: NO"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
