#!/usr/bin/env python3
"""Spiral-led shape audit for the First Hand spherical reciprocal spiral.

Primary hypothesis under test:

    alpha_unwrapped = a + m * F(rho)

where

    F(rho) = (1 - rho**2) / (2*rho)

for a stereographically rendered isotropic central-projective image of

    r * theta = 1.

The continuous spherical spiral alone determines a and m.

This script deliberately does not use:
- Y0, Y1, YAXIS, or X1;
- scaffold geometry;
- coordinate-derived construction scales;
- endpoint theta conventions;
- endpoint landmarks;
- general anisotropic/projective/nonlinear models.
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

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]

if str(ROOT) not in sys.path:
    sys.path.insert(
        0,
        str(ROOT),
    )

from scripts import digitize_first_hand_spherical_spiral as digitizer  # noqa: E402
from scripts import audit_first_hand_spherical_spiral_reproducibility as repro  # noqa: E402


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

SEAL1 = PASS1.with_suffix(
    ".sha256"
)

SEAL2 = PASS2.with_suffix(
    ".sha256"
)

PROTOCOL = (
    ROOT
    / "docs"
    / "first_hand_spherical_reciprocal_spiral_shape_protocol.md"
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

STEREOGRAPHIC_RESULT = (
    ROOT
    / "data"
    / "derived"
    / "first_hand_arm_of_god"
    / "qc"
    / "first_hand_stereographic_plane_angles.json"
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
    / "first_hand_spherical_reciprocal_spiral_shape.json"
)

OUT_SEGMENTS = (
    OUTPUT_DIR
    / "first_hand_spherical_reciprocal_spiral_shape_segments.csv"
)

OUT_SAMPLES = (
    OUTPUT_DIR
    / "first_hand_spherical_reciprocal_spiral_shape_samples.csv"
)

OUT_PNG = (
    OUTPUT_DIR
    / "first_hand_spherical_reciprocal_spiral_shape.png"
)

OUT_REPORT = (
    ROOT
    / "reports"
    / "first_hand_spherical_reciprocal_spiral_shape.md"
)

ANALYSIS_CLASS = (
    "spiral_led_isotropic_central_projective_stereographic_reciprocal_shape"
)

SEGMENT_IDS = tuple(
    f"S{i:02d}"
    for i in range(
        1,
        11,
    )
)

N_RESAMPLE = 401

CENTER_X_PX = 1255.1268387556074
CENTER_Y_PX = 694.602781503521
LIMB_RADIUS_PX = 341.906449919406

TWO_PI = 2.0 * math.pi


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
            f"{manifest} must contain exactly one SHA-256 record."
        )

    fields = lines[
        0
    ].split(
        maxsplit=1
    )

    if len(fields) != 2:
        raise RuntimeError(
            f"Malformed SHA-256 record in {manifest}."
        )

    expected_hash = fields[
        0
    ]

    recorded_path = (
        resolve_manifest_path(
            fields[
                1
            ]
        )
    )

    if (
        recorded_path
        != target.resolve()
    ):
        raise RuntimeError(
            f"{manifest} does not seal {target}."
        )

    if (
        sha256_path(
            target
        )
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

    matches: list[
        str
    ] = []

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

        recorded_path = (
            resolve_manifest_path(
                fields[
                    1
                ]
            )
        )

        if (
            recorded_path
            == target_resolved
        ):
            matches.append(
                fields[
                    0
                ]
            )

    if len(
        matches
    ) != 1:
        raise RuntimeError(
            f"Expected exactly one seal entry for {target}; "
            f"found {len(matches)}."
        )

    if (
        sha256_path(
            target
        )
        != matches[
            0
        ]
    ):
        raise RuntimeError(
            f"SHA-256 verification failed for {target}."
        )


def verify_frozen_frame() -> None:
    data = json.loads(
        STEREOGRAPHIC_RESULT.read_text(
            encoding="utf-8"
        )
    )

    frame = (
        data[
            "provenance"
        ][
            "frozen_limb_reference"
        ]
    )

    checks = {
        "center_x_px": CENTER_X_PX,
        "center_y_px": CENTER_Y_PX,
        "radius_px": LIMB_RADIUS_PX,
    }

    for key, expected in (
        checks.items()
    ):
        actual = float(
            frame[
                key
            ]
        )

        if not math.isclose(
            actual,
            expected,
            rel_tol=0.0,
            abs_tol=1e-12,
        ):
            raise RuntimeError(
                f"Frozen limb-frame mismatch for {key}: "
                f"{actual} != {expected}"
            )


def verify_protocol() -> None:
    text = PROTOCOL.read_text(
        encoding="utf-8"
    )

    required = (
        "r * theta = 1",
        "N_RESAMPLE = 401",
        "alpha_unwrapped",
        "F(rho)",
        "Y0",
        "Y1",
        "YAXIS",
        "X1",
        "No model expansion",
    )

    for token in required:
        if token not in text:
            raise RuntimeError(
                f"Frozen shape protocol missing token: {token!r}"
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
]:
    for path in (
        PASS1,
        PASS2,
        SEAL1,
        SEAL2,
        PROTOCOL,
        REPRO_RESULT,
        REPRO_SEAL,
        STEREOGRAPHIC_RESULT,
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

    verify_protocol()

    verify_frozen_frame()

    if (
        repro.N_RESAMPLE
        != N_RESAMPLE
    ):
        raise RuntimeError(
            "Shape audit resampling count differs from frozen "
            "reproducibility implementation."
        )

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

    for pass_number, rows in (
        (
            1,
            rows1,
        ),
        (
            2,
            rows2,
        ),
    ):
        ids = {
            row[
                "segment_id"
            ]
            for row in rows
        }

        if ids != set(
            SEGMENT_IDS
        ):
            raise RuntimeError(
                f"Pass {pass_number} segment vocabulary differs "
                "from frozen S01-S10 topology."
            )

    return (
        rows1,
        rows2,
    )


def group_by_segment(
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

    for segment_id in (
        SEGMENT_IDS
    ):
        if segment_id not in grouped:
            raise RuntimeError(
                f"Missing frozen segment: {segment_id}"
            )

        grouped[
            segment_id
        ].sort(
            key=lambda row: int(
                row[
                    "sequence_index"
                ]
            )
        )

    return grouped


def points_from_rows(
    rows: Sequence[
        dict[
            str,
            str,
        ]
    ],
) -> np.ndarray:
    points = np.array(
        [
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
            ]
            for row in rows
        ],
        dtype=float,
    )

    if (
        points.ndim != 2
        or points.shape[
            1
        ] != 2
        or len(
            points
        ) < 2
    ):
        raise RuntimeError(
            "Invalid source polyline."
        )

    if not np.all(
        np.isfinite(
            points
        )
    ):
        raise RuntimeError(
            "Source polyline contains non-finite coordinates."
        )

    return points


def page_coordinates(
    xy_px: np.ndarray,
) -> tuple[
    np.ndarray,
    np.ndarray,
]:
    xy_px = np.asarray(
        xy_px,
        dtype=float,
    )

    u = (
        xy_px[
            :,
            0
        ]
        - CENTER_X_PX
    ) / LIMB_RADIUS_PX

    v = (
        CENTER_Y_PX
        - xy_px[
            :,
            1
        ]
    ) / LIMB_RADIUS_PX

    return (
        u,
        v,
    )


def radial_transform(
    rho: np.ndarray,
) -> np.ndarray:
    rho = np.asarray(
        rho,
        dtype=float,
    )

    if np.any(
        rho <= 0.0
    ):
        raise RuntimeError(
            "At least one source point has rho <= 0, "
            "where F(rho) is undefined. No point was deleted."
        )

    return (
        1.0
        - rho
        * rho
    ) / (
        2.0
        * rho
    )


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
        or len(
            values
        ) != len(
            weights
        )
        or len(
            values
        ) == 0
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


def weighted_linear_fit(
    x: np.ndarray,
    y: np.ndarray,
    weights: np.ndarray,
) -> dict[
    str,
    Any,
]:
    x = np.asarray(
        x,
        dtype=float,
    )

    y = np.asarray(
        y,
        dtype=float,
    )

    weights = np.asarray(
        weights,
        dtype=float,
    )

    if not (
        x.shape
        == y.shape
        == weights.shape
    ):
        raise ValueError(
            "x, y, and weights must have identical shapes."
        )

    if (
        x.ndim != 1
        or len(
            x
        ) < 2
    ):
        raise ValueError(
            "Weighted linear fit requires at least two observations."
        )

    if not (
        np.all(
            np.isfinite(
                x
            )
        )
        and np.all(
            np.isfinite(
                y
            )
        )
        and np.all(
            np.isfinite(
                weights
            )
        )
    ):
        raise ValueError(
            "Weighted linear fit inputs must be finite."
        )

    if np.any(
        weights <= 0.0
    ):
        raise ValueError(
            "All fit weights must be positive."
        )

    weight_sum = float(
        np.sum(
            weights
        )
    )

    x_bar = float(
        np.sum(
            weights
            * x
        )
        / weight_sum
    )

    y_bar = float(
        np.sum(
            weights
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
            weights
            * dx
            * dx
        )
    )

    if denominator <= 0.0:
        raise RuntimeError(
            "Degenerate F(rho) variance."
        )

    slope = float(
        np.sum(
            weights
            * dx
            * dy
        )
        / denominator
    )

    intercept = (
        y_bar
        - slope
        * x_bar
    )

    predicted = (
        intercept
        + slope
        * x
    )

    residual = (
        y
        - predicted
    )

    sse = float(
        np.sum(
            weights
            * residual
            * residual
        )
    )

    sst = float(
        np.sum(
            weights
            * dy
            * dy
        )
    )

    if sst <= 0.0:
        raise RuntimeError(
            "Degenerate angular variance."
        )

    r_squared = (
        1.0
        - sse
        / sst
    )

    if slope > 0.0:
        handedness = 1
    elif slope < 0.0:
        handedness = -1
    else:
        handedness = 0

    return {
        "intercept_rad": intercept,
        "alpha0_mod_2pi_rad": float(
            intercept
            % TWO_PI
        ),
        "slope_signed": slope,
        "handedness": handedness,
        "scale_k": abs(
            slope
        ),
        "weighted_r_squared": r_squared,
        "predicted": predicted,
        "residual": residual,
    }


def weighted_residual_summary(
    residual: np.ndarray,
    weights: np.ndarray,
) -> dict[
    str,
    float,
]:
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

    return {
        "median_abs_rad": weighted_quantile(
            absolute,
            weights,
            0.5,
        ),
        "mean_abs_rad": float(
            np.sum(
                weights
                * absolute
            )
            / weight_sum
        ),
        "rms_rad": rms,
        "p95_abs_rad": weighted_quantile(
            absolute,
            weights,
            0.95,
        ),
        "max_abs_rad": float(
            np.max(
                absolute
            )
        ),
        "median_abs_deg": math.degrees(
            weighted_quantile(
                absolute,
                weights,
                0.5,
            )
        ),
        "mean_abs_deg": math.degrees(
            float(
                np.sum(
                    weights
                    * absolute
                )
                / weight_sum
            )
        ),
        "rms_deg": math.degrees(
            rms
        ),
        "p95_abs_deg": math.degrees(
            weighted_quantile(
                absolute,
                weights,
                0.95,
            )
        ),
        "max_abs_deg": math.degrees(
            float(
                np.max(
                    absolute
                )
            )
        ),
    }


def weighted_scalar_summary(
    values: np.ndarray,
    weights: np.ndarray,
) -> dict[
    str,
    float,
]:
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


def build_transformed_pass(
    rows: Sequence[
        dict[
            str,
            str,
        ]
    ],
    pass_number: int,
) -> dict[
    str,
    Any,
]:
    grouped = group_by_segment(
        rows
    )

    samples: list[
        dict[
            str,
            Any,
        ]
    ] = []

    lengths: dict[
        str,
        float,
    ] = {}

    principal_by_segment: dict[
        str,
        np.ndarray,
    ] = {}

    for segment_id in (
        SEGMENT_IDS
    ):
        points = points_from_rows(
            grouped[
                segment_id
            ]
        )

        length = repro.polyline_length(
            points
        )

        lengths[
            segment_id
        ] = length

        resampled = (
            repro.resample_polyline(
                points,
                N_RESAMPLE,
            )
        )

        u, v = page_coordinates(
            resampled
        )

        rho = np.sqrt(
            u
            * u
            + v
            * v
        )

        alpha = np.arctan2(
            v,
            u,
        )

        principal_by_segment[
            segment_id
        ] = alpha.copy()

        for index in range(
            N_RESAMPLE
        ):
            samples.append(
                {
                    "pass_number": pass_number,
                    "segment_id": segment_id,
                    "sample_index": index,
                    "x_px": float(
                        resampled[
                            index,
                            0
                        ]
                    ),
                    "y_px": float(
                        resampled[
                            index,
                            1
                        ]
                    ),
                    "u": float(
                        u[
                            index
                        ]
                    ),
                    "v": float(
                        v[
                            index
                        ]
                    ),
                    "rho": float(
                        rho[
                            index
                        ]
                    ),
                    "alpha_principal_rad": float(
                        alpha[
                            index
                        ]
                    ),
                    "segment_length_px": length,
                }
            )

    alpha_principal = np.array(
        [
            sample[
                "alpha_principal_rad"
            ]
            for sample in samples
        ],
        dtype=float,
    )

    alpha_unwrapped = np.unwrap(
        alpha_principal,
        discont=math.pi,
    )

    rho = np.array(
        [
            sample[
                "rho"
            ]
            for sample in samples
        ],
        dtype=float,
    )

    count_rho_nonpositive = int(
        np.count_nonzero(
            rho <= 0.0
        )
    )

    count_rho_ge_one = int(
        np.count_nonzero(
            rho >= 1.0
        )
    )

    f_rho = radial_transform(
        rho
    )

    length_weights = np.array(
        [
            lengths[
                sample[
                    "segment_id"
                ]
            ]
            / N_RESAMPLE
            for sample in samples
        ],
        dtype=float,
    )

    equal_segment_weights = np.full(
        len(
            samples
        ),
        1.0 / N_RESAMPLE,
        dtype=float,
    )

    for index, sample in enumerate(
        samples
    ):
        sample[
            "alpha_unwrapped_rad"
        ] = float(
            alpha_unwrapped[
                index
            ]
        )

        sample[
            "F_rho"
        ] = float(
            f_rho[
                index
            ]
        )

        sample[
            "weight_length"
        ] = float(
            length_weights[
                index
            ]
        )

        sample[
            "weight_equal_segment"
        ] = float(
            equal_segment_weights[
                index
            ]
        )

    gap_diagnostics = []

    for left, right in zip(
        SEGMENT_IDS[
            :-1
        ],
        SEGMENT_IDS[
            1:
        ],
    ):
        alpha_left = float(
            principal_by_segment[
                left
            ][
                -1
            ]
        )

        alpha_right = float(
            principal_by_segment[
                right
            ][
                0
            ]
        )

        jump = circular_difference(
            alpha_right,
            alpha_left,
        )

        gap_diagnostics.append(
            {
                "from_segment": left,
                "to_segment": right,
                "signed_principal_jump_rad": jump,
                "absolute_principal_jump_rad": abs(
                    jump
                ),
                "absolute_principal_jump_deg": math.degrees(
                    abs(
                        jump
                    )
                ),
            }
        )

    return {
        "pass_number": pass_number,
        "samples": samples,
        "rho": rho,
        "F_rho": f_rho,
        "alpha_principal": alpha_principal,
        "alpha_unwrapped": alpha_unwrapped,
        "length_weights": length_weights,
        "equal_segment_weights": equal_segment_weights,
        "segment_lengths_px": lengths,
        "domain": {
            "rho_min": float(
                np.min(
                    rho
                )
            ),
            "rho_max": float(
                np.max(
                    rho
                )
            ),
            "count_rho_le_zero": count_rho_nonpositive,
            "count_rho_ge_one": count_rho_ge_one,
            "all_points_in_open_unit_disk": bool(
                count_rho_nonpositive == 0
                and count_rho_ge_one == 0
            ),
        },
        "topology": {
            "unwrapped_angular_span_rad": float(
                alpha_unwrapped[
                    -1
                ]
                - alpha_unwrapped[
                    0
                ]
            ),
            "unwrapped_angular_span_deg": math.degrees(
                float(
                    alpha_unwrapped[
                        -1
                    ]
                    - alpha_unwrapped[
                        0
                    ]
                )
            ),
            "gap_diagnostics": gap_diagnostics,
            "max_absolute_gap_jump_rad": max(
                diagnostic[
                    "absolute_principal_jump_rad"
                ]
                for diagnostic in gap_diagnostics
            ),
            "max_absolute_gap_jump_deg": max(
                diagnostic[
                    "absolute_principal_jump_deg"
                ]
                for diagnostic in gap_diagnostics
            ),
        },
    }


def fit_weighting(
    transformed: dict[
        str,
        Any,
    ],
    weighting_name: str,
) -> dict[
    str,
    Any,
]:
    if (
        weighting_name
        == "length"
    ):
        weights = transformed[
            "length_weights"
        ]

    elif (
        weighting_name
        == "equal_segment"
    ):
        weights = transformed[
            "equal_segment_weights"
        ]

    else:
        raise ValueError(
            f"Unknown weighting: {weighting_name}"
        )

    fit = weighted_linear_fit(
        transformed[
            "F_rho"
        ],
        transformed[
            "alpha_unwrapped"
        ],
        weights,
    )

    residual_summary = (
        weighted_residual_summary(
            fit[
                "residual"
            ],
            weights,
        )
    )

    chord_px = (
        2.0
        * LIMB_RADIUS_PX
        * transformed[
            "rho"
        ]
        * np.abs(
            np.sin(
                0.5
                * fit[
                    "residual"
                ]
            )
        )
    )

    chord_summary = (
        weighted_scalar_summary(
            chord_px,
            weights,
        )
    )

    return {
        "weighting": weighting_name,
        "intercept_rad": fit[
            "intercept_rad"
        ],
        "alpha0_mod_2pi_rad": fit[
            "alpha0_mod_2pi_rad"
        ],
        "alpha0_mod_2pi_deg": math.degrees(
            fit[
                "alpha0_mod_2pi_rad"
            ]
        ),
        "slope_signed": fit[
            "slope_signed"
        ],
        "handedness": fit[
            "handedness"
        ],
        "scale_k": fit[
            "scale_k"
        ],
        "weighted_r_squared": fit[
            "weighted_r_squared"
        ],
        "angular_residual": residual_summary,
        "angular_chord_discrepancy_px": chord_summary,
        "_predicted": fit[
            "predicted"
        ],
        "_residual": fit[
            "residual"
        ],
        "_chord_px": chord_px,
        "_weights": weights,
    }


def segment_diagnostics(
    transformed: dict[
        str,
        Any,
    ],
    fit: dict[
        str,
        Any,
    ],
) -> list[
    dict[
        str,
        Any,
    ]
]:
    samples = transformed[
        "samples"
    ]

    residual = fit[
        "_residual"
    ]

    chord = fit[
        "_chord_px"
    ]

    weights = fit[
        "_weights"
    ]

    results = []

    for segment_id in (
        SEGMENT_IDS
    ):
        indices = np.array(
            [
                index
                for index, sample
                in enumerate(
                    samples
                )
                if (
                    sample[
                        "segment_id"
                    ]
                    == segment_id
                )
            ],
            dtype=int,
        )

        segment_residual = residual[
            indices
        ]

        segment_chord = chord[
            indices
        ]

        segment_weights = weights[
            indices
        ]

        segment_rho = transformed[
            "rho"
        ][
            indices
        ]

        angular = (
            weighted_residual_summary(
                segment_residual,
                segment_weights,
            )
        )

        chord_summary = (
            weighted_scalar_summary(
                segment_chord,
                segment_weights,
            )
        )

        results.append(
            {
                "pass_number": transformed[
                    "pass_number"
                ],
                "segment_id": segment_id,
                "weighting": fit[
                    "weighting"
                ],
                "segment_length_px": transformed[
                    "segment_lengths_px"
                ][
                    segment_id
                ],
                "rho_min": float(
                    np.min(
                        segment_rho
                    )
                ),
                "rho_max": float(
                    np.max(
                        segment_rho
                    )
                ),
                "count_rho_le_zero": int(
                    np.count_nonzero(
                        segment_rho
                        <= 0.0
                    )
                ),
                "count_rho_ge_one": int(
                    np.count_nonzero(
                        segment_rho
                        >= 1.0
                    )
                ),
                "angular_residual": angular,
                "angular_chord_discrepancy_px": chord_summary,
            }
        )

    return results


def strip_private_arrays(
    fit: dict[
        str,
        Any,
    ],
) -> dict[
    str,
    Any,
]:
    return {
        key: value
        for key, value
        in fit.items()
        if not key.startswith(
            "_"
        )
    }


def build_analysis() -> dict[
    str,
    Any,
]:
    rows1, rows2 = (
        verify_dependencies()
    )

    transformed1 = (
        build_transformed_pass(
            rows1,
            1,
        )
    )

    transformed2 = (
        build_transformed_pass(
            rows2,
            2,
        )
    )

    fits = {}

    segment_results = []

    for transformed in (
        transformed1,
        transformed2,
    ):
        pass_key = (
            f"pass{transformed['pass_number']}"
        )

        length_fit = (
            fit_weighting(
                transformed,
                "length",
            )
        )

        equal_fit = (
            fit_weighting(
                transformed,
                "equal_segment",
            )
        )

        fits[
            pass_key
        ] = {
            "primary_length_weighted": strip_private_arrays(
                length_fit
            ),
            "secondary_equal_segment": strip_private_arrays(
                equal_fit
            ),
            "weighting_sensitivity": {
                "absolute_k_difference": abs(
                    length_fit[
                        "scale_k"
                    ]
                    - equal_fit[
                        "scale_k"
                    ]
                ),
                "relative_k_difference": (
                    2.0
                    * abs(
                        length_fit[
                            "scale_k"
                        ]
                        - equal_fit[
                            "scale_k"
                        ]
                    )
                    / (
                        length_fit[
                            "scale_k"
                        ]
                        + equal_fit[
                            "scale_k"
                        ]
                    )
                ),
            },
        }

        segment_results.extend(
            segment_diagnostics(
                transformed,
                length_fit,
            )
        )

        segment_results.extend(
            segment_diagnostics(
                transformed,
                equal_fit,
            )
        )

        for index, sample in enumerate(
            transformed[
                "samples"
            ]
        ):
            sample[
                "predicted_alpha_length_rad"
            ] = float(
                length_fit[
                    "_predicted"
                ][
                    index
                ]
            )

            sample[
                "residual_alpha_length_rad"
            ] = float(
                length_fit[
                    "_residual"
                ][
                    index
                ]
            )

            sample[
                "angular_chord_length_px"
            ] = float(
                length_fit[
                    "_chord_px"
                ][
                    index
                ]
            )

            sample[
                "predicted_alpha_equal_segment_rad"
            ] = float(
                equal_fit[
                    "_predicted"
                ][
                    index
                ]
            )

            sample[
                "residual_alpha_equal_segment_rad"
            ] = float(
                equal_fit[
                    "_residual"
                ][
                    index
                ]
            )

            sample[
                "angular_chord_equal_segment_px"
            ] = float(
                equal_fit[
                    "_chord_px"
                ][
                    index
                ]
            )

    primary1 = fits[
        "pass1"
    ][
        "primary_length_weighted"
    ]

    primary2 = fits[
        "pass2"
    ][
        "primary_length_weighted"
    ]

    k1 = primary1[
        "scale_k"
    ]

    k2 = primary2[
        "scale_k"
    ]

    intercept_difference = (
        circular_difference(
            primary1[
                "alpha0_mod_2pi_rad"
            ],
            primary2[
                "alpha0_mod_2pi_rad"
            ],
        )
    )

    samples = (
        transformed1[
            "samples"
        ]
        + transformed2[
            "samples"
        ]
    )

    return {
        "analysis_class": ANALYSIS_CLASS,
        "checkpoint": (
            "first_hand_spherical_reciprocal_spiral_shape_v0.8"
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
            "frozen_limb_reference": {
                "source": str(
                    STEREOGRAPHIC_RESULT.relative_to(
                        ROOT
                    )
                ),
                "source_sha256": sha256_path(
                    STEREOGRAPHIC_RESULT
                ),
                "center_x_px": CENTER_X_PX,
                "center_y_px": CENTER_Y_PX,
                "radius_px": LIMB_RADIUS_PX,
                "refitted": False,
            },
        },
        "model": {
            "planar_spiral": "r*theta=1",
            "construction_family": (
                "isotropic central-projective M_k(x,y)=normalize(k*x,k*y,1)"
            ),
            "rendering": (
                "normalized stereographic with equator at rho=1"
            ),
            "radial_transform": (
                "F(rho)=(1-rho^2)/(2*rho)"
            ),
            "linear_shape_relation": (
                "alpha_unwrapped=a+m*F(rho)"
            ),
            "scale_definition": "k=abs(m)",
            "handedness_definition": "sign(m)",
            "endpoint_theta_used": False,
            "coordinate_curves_used": False,
            "scaffold_used": False,
            "optimizer_calls": 0,
            "model_expansion": False,
        },
        "resampling": {
            "samples_per_segment": N_RESAMPLE,
            "segments_per_pass": len(
                SEGMENT_IDS
            ),
            "samples_per_pass": (
                N_RESAMPLE
                * len(
                    SEGMENT_IDS
                )
            ),
            "segment_gaps_interpolated": False,
        },
        "pass_diagnostics": {
            "pass1": {
                "domain": transformed1[
                    "domain"
                ],
                "topology": transformed1[
                    "topology"
                ],
            },
            "pass2": {
                "domain": transformed2[
                    "domain"
                ],
                "topology": transformed2[
                    "topology"
                ],
            },
        },
        "fits": fits,
        "cross_pass_primary_replication": {
            "absolute_k_difference": abs(
                k1
                - k2
            ),
            "relative_k_difference": (
                2.0
                * abs(
                    k1
                    - k2
                )
                / (
                    k1
                    + k2
                )
            ),
            "handedness_agrees": bool(
                primary1[
                    "handedness"
                ]
                == primary2[
                    "handedness"
                ]
            ),
            "circular_alpha0_difference_rad": abs(
                intercept_difference
            ),
            "circular_alpha0_difference_deg": math.degrees(
                abs(
                    intercept_difference
                )
            ),
        },
        "segment_diagnostics": segment_results,
        "interpretation_boundary": {
            "spiral_only_shape_fit": True,
            "source_endpoint_branch_selected": False,
            "coordinate_scale_comparison_performed": False,
            "coordinate_curve_prediction_performed": False,
            "historical_construction_proven": False,
        },
        "_samples": samples,
    }


def write_samples_csv(
    analysis: dict[
        str,
        Any,
    ],
) -> None:
    fields = [
        "pass_number",
        "segment_id",
        "sample_index",
        "x_px",
        "y_px",
        "u",
        "v",
        "rho",
        "alpha_principal_rad",
        "alpha_unwrapped_rad",
        "F_rho",
        "segment_length_px",
        "weight_length",
        "weight_equal_segment",
        "predicted_alpha_length_rad",
        "residual_alpha_length_rad",
        "angular_chord_length_px",
        "predicted_alpha_equal_segment_rad",
        "residual_alpha_equal_segment_rad",
        "angular_chord_equal_segment_px",
    ]

    with OUT_SAMPLES.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=fields,
        )

        writer.writeheader()

        for sample in analysis[
            "_samples"
        ]:
            row = {}

            for field in fields:
                value = sample[
                    field
                ]

                if isinstance(
                    value,
                    float,
                ):
                    row[
                        field
                    ] = format(
                        value,
                        ".15g",
                    )
                else:
                    row[
                        field
                    ] = value

            writer.writerow(
                row
            )


def write_segments_csv(
    analysis: dict[
        str,
        Any,
    ],
) -> None:
    fields = [
        "pass_number",
        "segment_id",
        "weighting",
        "segment_length_px",
        "rho_min",
        "rho_max",
        "count_rho_le_zero",
        "count_rho_ge_one",
        "angular_median_abs_deg",
        "angular_rms_deg",
        "angular_p95_abs_deg",
        "angular_max_abs_deg",
        "chord_median_px",
        "chord_rms_px",
        "chord_p95_px",
        "chord_max_px",
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

            chord = result[
                "angular_chord_discrepancy_px"
            ]

            writer.writerow(
                {
                    "pass_number": result[
                        "pass_number"
                    ],
                    "segment_id": result[
                        "segment_id"
                    ],
                    "weighting": result[
                        "weighting"
                    ],
                    "segment_length_px": format(
                        result[
                            "segment_length_px"
                        ],
                        ".15g",
                    ),
                    "rho_min": format(
                        result[
                            "rho_min"
                        ],
                        ".15g",
                    ),
                    "rho_max": format(
                        result[
                            "rho_max"
                        ],
                        ".15g",
                    ),
                    "count_rho_le_zero": result[
                        "count_rho_le_zero"
                    ],
                    "count_rho_ge_one": result[
                        "count_rho_ge_one"
                    ],
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
                    "chord_median_px": format(
                        chord[
                            "median"
                        ],
                        ".15g",
                    ),
                    "chord_rms_px": format(
                        chord[
                            "rms"
                        ],
                        ".15g",
                    ),
                    "chord_p95_px": format(
                        chord[
                            "p95"
                        ],
                        ".15g",
                    ),
                    "chord_max_px": format(
                        chord[
                            "max"
                        ],
                        ".15g",
                    ),
                }
            )


def write_figure(
    analysis: dict[
        str,
        Any,
    ],
) -> None:
    figure, axis = plt.subplots(
        figsize=(
            11,
            7,
        )
    )

    samples = analysis[
        "_samples"
    ]

    for pass_number in (
        1,
        2,
    ):
        selected = [
            sample
            for sample in samples
            if (
                sample[
                    "pass_number"
                ]
                == pass_number
            )
        ]

        x = np.array(
            [
                sample[
                    "F_rho"
                ]
                for sample in selected
            ],
            dtype=float,
        )

        y = np.array(
            [
                sample[
                    "alpha_unwrapped_rad"
                ]
                for sample in selected
            ],
            dtype=float,
        )

        fit = analysis[
            "fits"
        ][
            f"pass{pass_number}"
        ][
            "primary_length_weighted"
        ]

        order = np.argsort(
            x
        )

        predicted = (
            fit[
                "intercept_rad"
            ]
            + fit[
                "slope_signed"
            ]
            * x
        )

        axis.plot(
            x,
            y,
            ".",
            markersize=2.0,
            alpha=0.35,
            label=(
                f"Pass {pass_number} observations"
            ),
        )

        axis.plot(
            x[
                order
            ],
            predicted[
                order
            ],
            linewidth=1.5,
            label=(
                f"Pass {pass_number} length-weighted fit"
            ),
        )

    axis.set_xlabel(
        "F(rho) = (1 - rho²) / (2 rho)"
    )

    axis.set_ylabel(
        "Unwrapped page azimuth (rad)"
    )

    axis.set_title(
        "First Hand spherical spiral: reciprocal-shape linearity"
    )

    axis.grid(
        True,
        alpha=0.25,
    )

    axis.legend()

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
    fit: dict[
        str,
        Any,
    ],
) -> list[
    str
]:
    angular = fit[
        "angular_residual"
    ]

    chord = fit[
        "angular_chord_discrepancy_px"
    ]

    return [
        f"### {title}",
        "",
        f"    intercept a       = {fit['intercept_rad']:.12f} rad",
        f"    alpha0 mod 2*pi   = {fit['alpha0_mod_2pi_rad']:.12f} rad",
        f"    alpha0 mod 2*pi   = {fit['alpha0_mod_2pi_deg']:.12f} deg",
        f"    signed slope m    = {fit['slope_signed']:.12f}",
        f"    handedness        = {fit['handedness']:+d}",
        f"    spiral scale k    = {fit['scale_k']:.12f}",
        f"    weighted R^2      = {fit['weighted_r_squared']:.12f}",
        "",
        "Angular residual:",
        "",
        f"    median |residual| = {angular['median_abs_deg']:.12f} deg",
        f"    mean   |residual| = {angular['mean_abs_deg']:.12f} deg",
        f"    RMS residual      = {angular['rms_deg']:.12f} deg",
        f"    p95   |residual|  = {angular['p95_abs_deg']:.12f} deg",
        f"    max   |residual|  = {angular['max_abs_deg']:.12f} deg",
        "",
        "Fixed-rho angular chord discrepancy:",
        "",
        f"    median = {chord['median']:.12f} px",
        f"    RMS    = {chord['rms']:.12f} px",
        f"    p95    = {chord['p95']:.12f} px",
        f"    max    = {chord['max']:.12f} px",
        "",
    ]


def render_report(
    analysis: dict[
        str,
        Any,
    ],
) -> str:
    lines = [
        "# First Hand spherical reciprocal-spiral shape audit",
        "",
        "**Checkpoint:** v0.8",
        "",
        f"**Analysis class:** `{analysis['analysis_class']}`",
        "",
        "## Question",
        "",
        "Does the independently acquired spherical spiral satisfy the",
        "radial-angular relation required by a stereographically rendered",
        "isotropic central-projective image of `r*theta = 1`?",
        "",
        "The labelled coordinate curves and scaffold are not used.",
        "",
        "## Frozen page frame",
        "",
        f"    center_x = {CENTER_X_PX:.12f} px",
        f"    center_y = {CENTER_Y_PX:.12f} px",
        f"    R_limb   = {LIMB_RADIUS_PX:.12f} px",
        "",
        "## Model",
        "",
        "    F(rho) = (1-rho^2)/(2*rho)",
        "",
        "    alpha_unwrapped = a + m*F(rho)",
        "",
        "    k = abs(m)",
        "",
    ]

    for pass_number in (
        1,
        2,
    ):
        diagnostic = analysis[
            "pass_diagnostics"
        ][
            f"pass{pass_number}"
        ]

        lines.extend(
            [
                f"## Pass {pass_number}",
                "",
                "Radial domain:",
                "",
                f"    rho_min             = {diagnostic['domain']['rho_min']:.12f}",
                f"    rho_max             = {diagnostic['domain']['rho_max']:.12f}",
                f"    count rho <= 0      = {diagnostic['domain']['count_rho_le_zero']}",
                f"    count rho >= 1      = {diagnostic['domain']['count_rho_ge_one']}",
                f"    all in open disk    = {diagnostic['domain']['all_points_in_open_unit_disk']}",
                "",
                "Source-order angular topology:",
                "",
                f"    unwrapped span      = {diagnostic['topology']['unwrapped_angular_span_rad']:.12f} rad",
                f"    unwrapped span      = {diagnostic['topology']['unwrapped_angular_span_deg']:.12f} deg",
                f"    maximum gap jump    = {diagnostic['topology']['max_absolute_gap_jump_deg']:.12f} deg",
                "",
            ]
        )

        fits = analysis[
            "fits"
        ][
            f"pass{pass_number}"
        ]

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
                "Secondary equal-segment fit",
                fits[
                    "secondary_equal_segment"
                ],
            )
        )

        sensitivity = fits[
            "weighting_sensitivity"
        ]

        lines.extend(
            [
                "### Weighting sensitivity",
                "",
                f"    |delta k|           = {sensitivity['absolute_k_difference']:.12f}",
                f"    relative delta k    = {sensitivity['relative_k_difference']:.12f}",
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
            f"    |k1-k2|             = {replication['absolute_k_difference']:.12f}",
            f"    relative k diff     = {replication['relative_k_difference']:.12f}",
            f"    handedness agrees   = {replication['handedness_agrees']}",
            f"    alpha0 difference   = {replication['circular_alpha0_difference_rad']:.12f} rad",
            f"    alpha0 difference   = {replication['circular_alpha0_difference_deg']:.12f} deg",
            "",
            "## Interpretation boundary",
            "",
            "This is a spiral-only shape test.",
            "",
            "No source endpoint theta convention was imposed.",
            "",
            "No coordinate-derived scale was compared or selected.",
            "",
            "No Y0, Y1, YAXIS, X1, or scaffold curve was used to fit the result.",
            "",
            "No general anisotropic, 2x2, projective, or nonlinear model was fitted.",
            "",
            "Compatibility would support this specific geometric construction",
            "family but would not prove that it was the historical construction.",
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

    json_analysis = {
        key: value
        for key, value
        in analysis.items()
        if key != "_samples"
    }

    OUT_JSON.write_text(
        json.dumps(
            json_analysis,
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )

    write_segments_csv(
        analysis
    )

    write_samples_csv(
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
            "Spiral-led reciprocal-shape audit of the First Hand "
            "spherical spiral."
        )
    )

    parser.add_argument(
        "--check-inputs",
        action="store_true",
        help=(
            "Verify frozen dependencies without transforming or fitting "
            "the spherical spiral."
        ),
    )

    return parser


def main() -> int:
    args = (
        build_argument_parser()
        .parse_args()
    )

    if args.check_inputs:
        rows1, rows2 = (
            verify_dependencies()
        )

        print(
            "Pass 1 SHA-256 seal: VERIFIED"
        )

        print(
            "Pass 2 SHA-256 seal: VERIFIED"
        )

        print(
            "Frozen two-pass reproducibility result: VERIFIED"
        )

        print(
            "Frozen reciprocal-shape protocol: VERIFIED"
        )

        print(
            "Frozen stereographic limb frame: VERIFIED"
        )

        print(
            f"Pass 1: {len(rows1)} raw rows, 10 segments"
        )

        print(
            f"Pass 2: {len(rows2)} raw rows, 10 segments"
        )

        print(
            f"Fixed resampling: {N_RESAMPLE} points per segment"
        )

        print(
            "Coordinate curves used: NO"
        )

        print(
            "Endpoint theta conventions used: NO"
        )

        print(
            "No spiral transformation or shape fit was computed."
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
        "FIRST HAND SPHERICAL RECIPROCAL-SPIRAL SHAPE AUDIT"
    )

    print(
        "="
        * 88
    )

    for pass_number in (
        1,
        2,
    ):
        diagnostics = analysis[
            "pass_diagnostics"
        ][
            f"pass{pass_number}"
        ]

        fit = analysis[
            "fits"
        ][
            f"pass{pass_number}"
        ][
            "primary_length_weighted"
        ]

        secondary = analysis[
            "fits"
        ][
            f"pass{pass_number}"
        ][
            "secondary_equal_segment"
        ]

        print(
            f"PASS {pass_number}"
        )

        print(
            "  rho range: "
            f"{diagnostics['domain']['rho_min']:.9f} "
            "-> "
            f"{diagnostics['domain']['rho_max']:.9f}"
        )

        print(
            "  rho >= 1: "
            f"{diagnostics['domain']['count_rho_ge_one']}"
        )

        print(
            "  observed unwrapped angular span: "
            f"{diagnostics['topology']['unwrapped_angular_span_rad']:.9f} rad "
            f"({diagnostics['topology']['unwrapped_angular_span_deg']:.6f} deg)"
        )

        print(
            "  maximum inter-segment angular jump: "
            f"{diagnostics['topology']['max_absolute_gap_jump_deg']:.6f} deg"
        )

        print(
            "  PRIMARY length-weighted:"
        )

        print(
            "    k: "
            f"{fit['scale_k']:.12f}"
        )

        print(
            "    signed slope: "
            f"{fit['slope_signed']:.12f}"
        )

        print(
            "    handedness: "
            f"{fit['handedness']:+d}"
        )

        print(
            "    alpha0: "
            f"{fit['alpha0_mod_2pi_deg']:.9f} deg"
        )

        print(
            "    weighted R^2: "
            f"{fit['weighted_r_squared']:.12f}"
        )

        print(
            "    angular RMS: "
            f"{fit['angular_residual']['rms_deg']:.9f} deg"
        )

        print(
            "    angular p95: "
            f"{fit['angular_residual']['p95_abs_deg']:.9f} deg"
        )

        print(
            "    angular chord RMS: "
            f"{fit['angular_chord_discrepancy_px']['rms']:.9f} px"
        )

        print(
            "    angular chord p95: "
            f"{fit['angular_chord_discrepancy_px']['p95']:.9f} px"
        )

        print(
            "  SECONDARY equal-segment:"
        )

        print(
            "    k: "
            f"{secondary['scale_k']:.12f}"
        )

        print(
            "    weighted R^2: "
            f"{secondary['weighted_r_squared']:.12f}"
        )

        print(
            "    angular RMS: "
            f"{secondary['angular_residual']['rms_deg']:.9f} deg"
        )

        print(
            "-"
            * 88
        )

    replication = analysis[
        "cross_pass_primary_replication"
    ]

    print(
        "CROSS-PASS PRIMARY REPLICATION"
    )

    print(
        "  |k1-k2|: "
        f"{replication['absolute_k_difference']:.12f}"
    )

    print(
        "  relative k difference: "
        f"{replication['relative_k_difference']:.12f}"
    )

    print(
        "  handedness agrees: "
        f"{replication['handedness_agrees']}"
    )

    print(
        "  alpha0 circular difference: "
        f"{replication['circular_alpha0_difference_deg']:.9f} deg"
    )

    print(
        "-"
        * 88
    )

    print(
        f"Wrote {OUT_JSON}"
    )

    print(
        f"Wrote {OUT_SEGMENTS}"
    )

    print(
        f"Wrote {OUT_SAMPLES}"
    )

    print(
        f"Wrote {OUT_PNG}"
    )

    print(
        f"Wrote {OUT_REPORT}"
    )

    print(
        "No coordinate curve, endpoint theta convention, scaffold, "
        "or expanded model was used."
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
