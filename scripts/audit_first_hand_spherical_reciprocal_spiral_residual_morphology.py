#!/usr/bin/env python3
"""Neutral residual-morphology audit for the frozen reciprocal-spiral shape fit.

This script analyzes only already-frozen residual fields.

It does NOT:
- refit k or alpha0;
- recompute the reciprocal-spiral fit;
- align the two passes;
- use coordinate curves or scaffold geometry;
- fit polynomial, Fourier, spline, anisotropic, projective, or nonlinear
  corrections.

The numerical parent object is the frozen transformed sample table produced
by the primary spherical reciprocal-spiral shape audit.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from collections import defaultdict
from pathlib import Path
from typing import Any, Iterable

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]

PROTOCOL = (
    ROOT
    / "docs"
    / "first_hand_spherical_reciprocal_spiral_residual_morphology_protocol.md"
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
    / "first_hand_spherical_reciprocal_spiral_residual_morphology.json"
)

OUT_SEGMENTS = (
    OUTPUT_DIR
    / "first_hand_spherical_reciprocal_spiral_residual_segments.csv"
)

OUT_BINS = (
    OUTPUT_DIR
    / "first_hand_spherical_reciprocal_spiral_residual_bins.csv"
)

OUT_CROSSPASS = (
    OUTPUT_DIR
    / "first_hand_spherical_reciprocal_spiral_residual_crosspass.csv"
)

OUT_PNG = (
    OUTPUT_DIR
    / "first_hand_spherical_reciprocal_spiral_residual_morphology.png"
)

OUT_REPORT = (
    ROOT
    / "reports"
    / "first_hand_spherical_reciprocal_spiral_residual_morphology.md"
)

ANALYSIS_CLASS = (
    "neutral_postfit_spherical_reciprocal_spiral_residual_morphology"
)

SEGMENT_IDS = tuple(
    f"S{i:02d}"
    for i in range(1, 11)
)

N_SEGMENTS = 10
N_RESAMPLE = 401
N_PER_PASS = N_SEGMENTS * N_RESAMPLE

TWO_PI = 2.0 * math.pi

REPRO_RMS_EQUAL_PX = 0.887258846871
REPRO_RMS_LENGTH_PX = 0.956050554591
SPIRAL_HALF_STROKE_PX = 7.0

EXPECTED_SAMPLE_FIELDS = [
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
            f"Missing frozen SHA-256 manifest: {manifest}"
        )

    target_resolved = target.resolve()
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
                f"Malformed SHA-256 record in {manifest}: {line!r}"
            )

        recorded_path = resolve_manifest_path(
            fields[1]
        )

        if recorded_path == target_resolved:
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
            f"Frozen parent artifact failed SHA-256 verification: {target}"
        )


def verify_protocol() -> None:
    text = PROTOCOL.read_text(
        encoding="utf-8"
    )

    required = (
        "No new fit",
        "20 equal-width bins",
        "36 equal phase bins",
        "segment_id",
        "sample_index",
        "Pearson correlation coefficient",
        "No numerical threshold",
    )

    for token in required:
        if token not in text:
            raise RuntimeError(
                f"Frozen residual protocol missing token: {token!r}"
            )


def verify_parent_json() -> dict[str, Any]:
    data = json.loads(
        PARENT_JSON.read_text(
            encoding="utf-8"
        )
    )

    expected_checkpoint = (
        "first_hand_spherical_reciprocal_spiral_shape_v0.8"
    )

    if data.get(
        "checkpoint"
    ) != expected_checkpoint:
        raise RuntimeError(
            "Unexpected frozen reciprocal-shape checkpoint."
        )

    model = data.get(
        "model",
        {},
    )

    if model.get(
        "linear_shape_relation"
    ) != "alpha_unwrapped=a+m*F(rho)":
        raise RuntimeError(
            "Frozen parent model identity differs from expected relation."
        )

    if model.get(
        "coordinate_curves_used"
    ) is not False:
        raise RuntimeError(
            "Frozen parent unexpectedly used coordinate curves."
        )

    return data


def parse_float(
    row: dict[str, str],
    field: str,
) -> float:
    value = float(
        row[field]
    )

    if not math.isfinite(
        value
    ):
        raise RuntimeError(
            f"Non-finite {field} in frozen sample table."
        )

    return value


def read_samples() -> list[dict[str, Any]]:
    with PARENT_SAMPLES.open(
        newline="",
        encoding="utf-8",
    ) as handle:
        reader = csv.DictReader(
            handle
        )

        if reader.fieldnames != EXPECTED_SAMPLE_FIELDS:
            raise RuntimeError(
                "Frozen reciprocal-shape sample schema differs "
                "from expected schema."
            )

        raw_rows = list(
            reader
        )

    if len(raw_rows) != 2 * N_PER_PASS:
        raise RuntimeError(
            f"Expected {2 * N_PER_PASS} frozen samples; "
            f"found {len(raw_rows)}."
        )

    rows: list[
        dict[str, Any]
    ] = []

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

        segment_number = int(
            segment_id[
                1:
            ]
        )

        global_index = (
            (
                segment_number
                - 1
            )
            * N_RESAMPLE
            + sample_index
        )

        q = (
            global_index
            / (
                N_PER_PASS
                - 1
            )
        )

        alpha_unwrapped = parse_float(
            raw,
            "alpha_unwrapped_rad",
        )

        phase = (
            alpha_unwrapped
            % TWO_PI
        )

        rows.append(
            {
                "pass_number": pass_number,
                "segment_id": segment_id,
                "segment_number": segment_number,
                "sample_index": sample_index,
                "global_index": global_index,
                "q": q,
                "rho": parse_float(
                    raw,
                    "rho",
                ),
                "F_rho": parse_float(
                    raw,
                    "F_rho",
                ),
                "alpha_unwrapped_rad": alpha_unwrapped,
                "phase_rad": phase,
                "weight_length": parse_float(
                    raw,
                    "weight_length",
                ),
                "residual_rad": parse_float(
                    raw,
                    "residual_alpha_length_rad",
                ),
                "chord_px": parse_float(
                    raw,
                    "angular_chord_length_px",
                ),
            }
        )

    seen = set()

    for row in rows:
        key = (
            row[
                "pass_number"
            ],
            row[
                "segment_id"
            ],
            row[
                "sample_index"
            ],
        )

        if key in seen:
            raise RuntimeError(
                f"Duplicate frozen sample key: {key}"
            )

        seen.add(
            key
        )

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

        if len(
            selected
        ) != N_PER_PASS:
            raise RuntimeError(
                f"Pass {pass_number} does not contain {N_PER_PASS} samples."
            )

        for segment_id in (
            SEGMENT_IDS
        ):
            segment_rows = [
                row
                for row in selected
                if row[
                    "segment_id"
                ] == segment_id
            ]

            indices = sorted(
                row[
                    "sample_index"
                ]
                for row in segment_rows
            )

            if indices != list(
                range(
                    N_RESAMPLE
                )
            ):
                raise RuntimeError(
                    f"Pass {pass_number} {segment_id} does not contain "
                    "exactly sample_index 0..400."
                )

    return rows


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
        or values.shape
        != weights.shape
        or len(
            values
        ) == 0
    ):
        raise ValueError(
            "weighted_quantile requires equal non-empty 1-D arrays."
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

    values_sorted = values[
        order
    ]

    weights_sorted = weights[
        order
    ]

    cumulative = np.cumsum(
        weights_sorted
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
            values_sorted
        )
        - 1,
    )

    return float(
        values_sorted[
            index
        ]
    )


def weighted_signed_mean(
    values: np.ndarray,
    weights: np.ndarray,
) -> float:
    return float(
        np.sum(
            weights
            * values
        )
        / np.sum(
            weights
        )
    )


def weighted_rms(
    values: np.ndarray,
    weights: np.ndarray,
) -> float:
    return math.sqrt(
        float(
            np.sum(
                weights
                * values
                * values
            )
            / np.sum(
                weights
            )
        )
    )


def summarize_residual(
    residual_rad: np.ndarray,
    chord_px: np.ndarray,
    weights: np.ndarray,
) -> dict[str, float]:
    residual_rad = np.asarray(
        residual_rad,
        dtype=float,
    )

    chord_px = np.asarray(
        chord_px,
        dtype=float,
    )

    weights = np.asarray(
        weights,
        dtype=float,
    )

    abs_residual = np.abs(
        residual_rad
    )

    return {
        "signed_mean_rad": weighted_signed_mean(
            residual_rad,
            weights,
        ),
        "signed_mean_deg": math.degrees(
            weighted_signed_mean(
                residual_rad,
                weights,
            )
        ),
        "median_abs_rad": weighted_quantile(
            abs_residual,
            weights,
            0.5,
        ),
        "median_abs_deg": math.degrees(
            weighted_quantile(
                abs_residual,
                weights,
                0.5,
            )
        ),
        "rms_rad": weighted_rms(
            residual_rad,
            weights,
        ),
        "rms_deg": math.degrees(
            weighted_rms(
                residual_rad,
                weights,
            )
        ),
        "p95_abs_rad": weighted_quantile(
            abs_residual,
            weights,
            0.95,
        ),
        "p95_abs_deg": math.degrees(
            weighted_quantile(
                abs_residual,
                weights,
                0.95,
            )
        ),
        "max_abs_rad": float(
            np.max(
                abs_residual
            )
        ),
        "max_abs_deg": math.degrees(
            float(
                np.max(
                    abs_residual
                )
            )
        ),
        "chord_rms_px": weighted_rms(
            chord_px,
            weights,
        ),
        "chord_p95_px": weighted_quantile(
            chord_px,
            weights,
            0.95,
        ),
    }


def pearson(
    x: np.ndarray,
    y: np.ndarray,
) -> float | None:
    x = np.asarray(
        x,
        dtype=float,
    )

    y = np.asarray(
        y,
        dtype=float,
    )

    if (
        len(
            x
        ) < 2
        or len(
            y
        ) != len(
            x
        )
    ):
        return None

    x_centered = (
        x
        - np.mean(
            x
        )
    )

    y_centered = (
        y
        - np.mean(
            y
        )
    )

    denominator = math.sqrt(
        float(
            np.sum(
                x_centered
                * x_centered
            )
            * np.sum(
                y_centered
                * y_centered
            )
        )
    )

    if denominator == 0.0:
        return None

    return float(
        np.sum(
            x_centered
            * y_centered
        )
        / denominator
    )


def difference_summary(
    a: np.ndarray,
    b: np.ndarray,
    *,
    angular: bool,
) -> dict[str, float | None]:
    a = np.asarray(
        a,
        dtype=float,
    )

    b = np.asarray(
        b,
        dtype=float,
    )

    difference = (
        a
        - b
    )

    absolute = np.abs(
        difference
    )

    result: dict[
        str,
        float | None,
    ] = {
        "pearson_r": pearson(
            a,
            b,
        ),
        "signed_mean_difference": float(
            np.mean(
                difference
            )
        ),
        "mean_absolute_difference": float(
            np.mean(
                absolute
            )
        ),
        "rms_difference": math.sqrt(
            float(
                np.mean(
                    difference
                    * difference
                )
            )
        ),
        "p95_absolute_difference": float(
            np.percentile(
                absolute,
                95.0,
            )
        ),
        "max_absolute_difference": float(
            np.max(
                absolute
            )
        ),
    }

    if angular:
        for key in (
            "signed_mean_difference",
            "mean_absolute_difference",
            "rms_difference",
            "p95_absolute_difference",
            "max_absolute_difference",
        ):
            value = result[
                key
            ]

            assert value is not None

            result[
                key
                + "_deg"
            ] = math.degrees(
                float(
                    value
                )
            )

    return result


def segment_results(
    rows: list[
        dict[str, Any]
    ],
) -> list[
    dict[str, Any]
]:
    output = []

    total_sse_by_pass = {}

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

        total_sse_by_pass[
            pass_number
        ] = float(
            sum(
                row[
                    "weight_length"
                ]
                * row[
                    "residual_rad"
                ]
                ** 2
                for row in pass_rows
            )
        )

    for pass_number in (
        1,
        2,
    ):
        for segment_id in (
            SEGMENT_IDS
        ):
            selected = [
                row
                for row in rows
                if (
                    row[
                        "pass_number"
                    ] == pass_number
                    and row[
                        "segment_id"
                    ] == segment_id
                )
            ]

            residual = np.array(
                [
                    row[
                        "residual_rad"
                    ]
                    for row in selected
                ],
                dtype=float,
            )

            chord = np.array(
                [
                    row[
                        "chord_px"
                    ]
                    for row in selected
                ],
                dtype=float,
            )

            weights = np.array(
                [
                    row[
                        "weight_length"
                    ]
                    for row in selected
                ],
                dtype=float,
            )

            summary = summarize_residual(
                residual,
                chord,
                weights,
            )

            sse = float(
                np.sum(
                    weights
                    * residual
                    * residual
                )
            )

            output.append(
                {
                    "pass_number": pass_number,
                    "segment_id": segment_id,
                    "sample_count": len(
                        selected
                    ),
                    "weight_total": float(
                        np.sum(
                            weights
                        )
                    ),
                    "sse_weighted_rad2": sse,
                    "sse_fraction": (
                        sse
                        / total_sse_by_pass[
                            pass_number
                        ]
                    ),
                    **summary,
                }
            )

    return output


def make_edges(
    minimum: float,
    maximum: float,
    bins: int,
) -> np.ndarray:
    if not (
        maximum
        > minimum
    ):
        raise ValueError(
            "Binning range must have positive width."
        )

    return np.linspace(
        minimum,
        maximum,
        bins
        + 1,
    )


def bin_index(
    value: float,
    edges: np.ndarray,
) -> int:
    if value == edges[
        -1
    ]:
        return len(
            edges
        ) - 2

    index = int(
        np.searchsorted(
            edges,
            value,
            side="right",
        )
        - 1
    )

    return index


def binned_results_for_axis(
    rows: list[
        dict[str, Any]
    ],
    *,
    axis_name: str,
    value_field: str,
    edges: np.ndarray,
) -> list[
    dict[str, Any]
]:
    output = []

    n_bins = len(
        edges
    ) - 1

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

        grouped: dict[
            int,
            list[
                dict[
                    str,
                    Any,
                ]
            ],
        ] = defaultdict(
            list
        )

        for row in pass_rows:
            value = float(
                row[
                    value_field
                ]
            )

            index = bin_index(
                value,
                edges,
            )

            if (
                index
                < 0
                or index
                >= n_bins
            ):
                raise RuntimeError(
                    f"{axis_name} value {value} lies outside frozen bin range."
                )

            grouped[
                index
            ].append(
                row
            )

        for index in range(
            n_bins
        ):
            selected = grouped.get(
                index,
                [],
            )

            base = {
                "axis": axis_name,
                "pass_number": pass_number,
                "bin_index": index,
                "bin_left": float(
                    edges[
                        index
                    ]
                ),
                "bin_right": float(
                    edges[
                        index
                        + 1
                    ]
                ),
                "is_last_bin": bool(
                    index
                    == n_bins
                    - 1
                ),
                "sample_count": len(
                    selected
                ),
            }

            if not selected:
                output.append(
                    {
                        **base,
                        "weight_total": 0.0,
                        "signed_mean_rad": None,
                        "signed_mean_deg": None,
                        "rms_rad": None,
                        "rms_deg": None,
                        "p95_abs_rad": None,
                        "p95_abs_deg": None,
                        "chord_rms_px": None,
                    }
                )

                continue

            residual = np.array(
                [
                    row[
                        "residual_rad"
                    ]
                    for row in selected
                ],
                dtype=float,
            )

            chord = np.array(
                [
                    row[
                        "chord_px"
                    ]
                    for row in selected
                ],
                dtype=float,
            )

            weights = np.array(
                [
                    row[
                        "weight_length"
                    ]
                    for row in selected
                ],
                dtype=float,
            )

            abs_residual = np.abs(
                residual
            )

            signed_mean = weighted_signed_mean(
                residual,
                weights,
            )

            rms = weighted_rms(
                residual,
                weights,
            )

            p95 = weighted_quantile(
                abs_residual,
                weights,
                0.95,
            )

            output.append(
                {
                    **base,
                    "weight_total": float(
                        np.sum(
                            weights
                        )
                    ),
                    "signed_mean_rad": signed_mean,
                    "signed_mean_deg": math.degrees(
                        signed_mean
                    ),
                    "rms_rad": rms,
                    "rms_deg": math.degrees(
                        rms
                    ),
                    "p95_abs_rad": p95,
                    "p95_abs_deg": math.degrees(
                        p95
                    ),
                    "chord_rms_px": weighted_rms(
                        chord,
                        weights,
                    ),
                }
            )

    return output


def pair_rows(
    rows: list[
        dict[str, Any]
    ],
) -> list[
    tuple[
        dict[str, Any],
        dict[str, Any],
    ]
]:
    by_pass: dict[
        int,
        dict[
            tuple[
                str,
                int,
            ],
            dict[
                str,
                Any,
            ],
        ],
    ] = {
        1: {},
        2: {},
    }

    for row in rows:
        key = (
            row[
                "segment_id"
            ],
            row[
                "sample_index"
            ],
        )

        by_pass[
            row[
                "pass_number"
            ]
        ][
            key
        ] = row

    keys1 = set(
        by_pass[
            1
        ]
    )

    keys2 = set(
        by_pass[
            2
        ]
    )

    if keys1 != keys2:
        raise RuntimeError(
            "Frozen Pass-1 and Pass-2 topological sample keys differ."
        )

    expected = {
        (
            segment_id,
            index,
        )
        for segment_id in SEGMENT_IDS
        for index in range(
            N_RESAMPLE
        )
    }

    if keys1 != expected:
        raise RuntimeError(
            "Frozen cross-pass sample keys differ from expected S01-S10 x 0..400."
        )

    ordered_keys = sorted(
        expected,
        key=lambda item: (
            int(
                item[
                    0
                ][
                    1:
                ]
            ),
            item[
                1
            ],
        ),
    )

    return [
        (
            by_pass[
                1
            ][
                key
            ],
            by_pass[
                2
            ][
                key
            ],
        )
        for key in ordered_keys
    ]


def crosspass_results(
    pairs: list[
        tuple[
            dict[str, Any],
            dict[str, Any],
        ]
    ],
) -> dict[
    str,
    Any,
]:
    residual1 = np.array(
        [
            pair[
                0
            ][
                "residual_rad"
            ]
            for pair in pairs
        ],
        dtype=float,
    )

    residual2 = np.array(
        [
            pair[
                1
            ][
                "residual_rad"
            ]
            for pair in pairs
        ],
        dtype=float,
    )

    chord1 = np.array(
        [
            pair[
                0
            ][
                "chord_px"
            ]
            for pair in pairs
        ],
        dtype=float,
    )

    chord2 = np.array(
        [
            pair[
                1
            ][
                "chord_px"
            ]
            for pair in pairs
        ],
        dtype=float,
    )

    positive_positive = 0
    negative_negative = 0
    opposite = 0
    zero_involving = 0

    for a, b in zip(
        residual1,
        residual2,
    ):
        if (
            a == 0.0
            or b == 0.0
        ):
            zero_involving += 1

        elif (
            a > 0.0
            and b > 0.0
        ):
            positive_positive += 1

        elif (
            a < 0.0
            and b < 0.0
        ):
            negative_negative += 1

        else:
            opposite += 1

    n = len(
        pairs
    )

    nonzero = (
        n
        - zero_involving
    )

    same_nonzero = (
        positive_positive
        + negative_negative
    )

    segment_replication = []

    for segment_id in (
        SEGMENT_IDS
    ):
        selected = [
            pair
            for pair in pairs
            if pair[
                0
            ][
                "segment_id"
            ] == segment_id
        ]

        r1 = np.array(
            [
                pair[
                    0
                ][
                    "residual_rad"
                ]
                for pair in selected
            ]
        )

        r2 = np.array(
            [
                pair[
                    1
                ][
                    "residual_rad"
                ]
                for pair in selected
            ]
        )

        c1 = np.array(
            [
                pair[
                    0
                ][
                    "chord_px"
                ]
                for pair in selected
            ]
        )

        c2 = np.array(
            [
                pair[
                    1
                ][
                    "chord_px"
                ]
                for pair in selected
            ]
        )

        segment_replication.append(
            {
                "segment_id": segment_id,
                "pair_count": len(
                    selected
                ),
                "angular": difference_summary(
                    r1,
                    r2,
                    angular=True,
                ),
                "chord": difference_summary(
                    c1,
                    c2,
                    angular=False,
                ),
            }
        )

    return {
        "pair_count": n,
        "angular": difference_summary(
            residual1,
            residual2,
            angular=True,
        ),
        "chord": difference_summary(
            chord1,
            chord2,
            angular=False,
        ),
        "sign_replication": {
            "positive_positive_count": positive_positive,
            "negative_negative_count": negative_negative,
            "opposite_sign_count": opposite,
            "zero_involving_count": zero_involving,
            "positive_positive_fraction": (
                positive_positive
                / n
            ),
            "negative_negative_fraction": (
                negative_negative
                / n
            ),
            "opposite_sign_fraction": (
                opposite
                / n
            ),
            "zero_involving_fraction": (
                zero_involving
                / n
            ),
            "same_nonzero_sign_fraction": (
                (
                    same_nonzero
                    / nonzero
                )
                if nonzero
                else None
            ),
        },
        "segments": segment_replication,
    }


def build_analysis() -> dict[
    str,
    Any,
]:
    parent, rows = (
        verify_dependencies()
    )

    segments = segment_results(
        rows
    )

    rho_edges = np.linspace(
        0.0,
        1.0,
        21,
    )

    f_values = np.array(
        [
            row[
                "F_rho"
            ]
            for row in rows
        ],
        dtype=float,
    )

    f_min = float(
        np.min(
            f_values
        )
    )

    f_max = float(
        np.max(
            f_values
        )
    )

    f_edges = make_edges(
        f_min,
        f_max,
        20,
    )

    phase_edges = np.linspace(
        0.0,
        TWO_PI,
        37,
    )

    q_edges = np.linspace(
        0.0,
        1.0,
        21,
    )

    bins = []

    bins.extend(
        binned_results_for_axis(
            rows,
            axis_name="rho",
            value_field="rho",
            edges=rho_edges,
        )
    )

    bins.extend(
        binned_results_for_axis(
            rows,
            axis_name="F_rho",
            value_field="F_rho",
            edges=f_edges,
        )
    )

    bins.extend(
        binned_results_for_axis(
            rows,
            axis_name="phase",
            value_field="phase_rad",
            edges=phase_edges,
        )
    )

    bins.extend(
        binned_results_for_axis(
            rows,
            axis_name="source_order_q",
            value_field="q",
            edges=q_edges,
        )
    )

    pairs = pair_rows(
        rows
    )

    crosspass = crosspass_results(
        pairs
    )

    return {
        "analysis_class": ANALYSIS_CLASS,
        "checkpoint": (
            "first_hand_spherical_reciprocal_spiral_residual_morphology_v0.8"
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
            "residual_field": (
                "frozen residual_alpha_length_rad"
            ),
            "chord_field": (
                "frozen angular_chord_length_px"
            ),
            "parent_fit_recomputed": False,
            "new_model_parameters": 0,
            "crosspass_alignment": False,
            "crosspass_pairing": (
                "exact (segment_id, sample_index)"
            ),
            "rho_bins": 20,
            "F_rho_bins": 20,
            "phase_bins": 36,
            "phase_bin_width_deg": 10.0,
            "source_order_bins": 20,
        },
        "binning": {
            "rho_edges": [
                float(
                    value
                )
                for value in rho_edges
            ],
            "F_rho_pooled_min": f_min,
            "F_rho_pooled_max": f_max,
            "F_rho_edges": [
                float(
                    value
                )
                for value in f_edges
            ],
            "phase_edges_rad": [
                float(
                    value
                )
                for value in phase_edges
            ],
            "source_order_q_edges": [
                float(
                    value
                )
                for value in q_edges
            ],
        },
        "segments": segments,
        "bins": bins,
        "crosspass": crosspass,
        "scale_context": {
            "continuous_trace_rms_equal_px": REPRO_RMS_EQUAL_PX,
            "continuous_trace_rms_length_px": REPRO_RMS_LENGTH_PX,
            "descriptive_half_stroke_px": SPIRAL_HALF_STROKE_PX,
            "statistical_threshold_assigned": False,
        },
        "interpretation_boundary": {
            "residual_morphology_only": True,
            "alternative_map_selected": False,
            "anisotropy_established": False,
            "projective_expansion_established": False,
            "nonlinear_chart_established": False,
        },
    }


def write_segment_csv(
    analysis: dict[
        str,
        Any,
    ],
) -> None:
    fields = [
        "pass_number",
        "segment_id",
        "sample_count",
        "weight_total",
        "sse_weighted_rad2",
        "sse_fraction",
        "signed_mean_deg",
        "median_abs_deg",
        "rms_deg",
        "p95_abs_deg",
        "max_abs_deg",
        "chord_rms_px",
        "chord_p95_px",
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
            "segments"
        ]:
            writer.writerow(
                {
                    field: (
                        format(
                            result[
                                field
                            ],
                            ".15g",
                        )
                        if isinstance(
                            result[
                                field
                            ],
                            float,
                        )
                        else result[
                            field
                        ]
                    )
                    for field in fields
                }
            )


def write_bins_csv(
    analysis: dict[
        str,
        Any,
    ],
) -> None:
    fields = [
        "axis",
        "pass_number",
        "bin_index",
        "bin_left",
        "bin_right",
        "is_last_bin",
        "sample_count",
        "weight_total",
        "signed_mean_deg",
        "rms_deg",
        "p95_abs_deg",
        "chord_rms_px",
    ]

    with OUT_BINS.open(
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
            "bins"
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
                    row[
                        field
                    ] = format(
                        value,
                        ".15g",
                    )

                elif value is None:
                    row[
                        field
                    ] = ""

                else:
                    row[
                        field
                    ] = value

            writer.writerow(
                row
            )


def write_crosspass_csv(
    analysis: dict[
        str,
        Any,
    ],
) -> None:
    fields = [
        "scope",
        "segment_id",
        "pair_count",
        "angular_pearson_r",
        "angular_signed_mean_diff_deg",
        "angular_mean_abs_diff_deg",
        "angular_rms_diff_deg",
        "angular_p95_abs_diff_deg",
        "angular_max_abs_diff_deg",
        "chord_pearson_r",
        "chord_signed_mean_diff_px",
        "chord_mean_abs_diff_px",
        "chord_rms_diff_px",
        "chord_p95_abs_diff_px",
        "chord_max_abs_diff_px",
    ]

    rows = []

    crosspass = analysis[
        "crosspass"
    ]

    def flatten(
        scope: str,
        segment_id: str,
        pair_count: int,
        angular: dict[
            str,
            Any,
        ],
        chord: dict[
            str,
            Any,
        ],
    ) -> dict[
        str,
        Any,
    ]:
        return {
            "scope": scope,
            "segment_id": segment_id,
            "pair_count": pair_count,
            "angular_pearson_r": angular[
                "pearson_r"
            ],
            "angular_signed_mean_diff_deg": angular[
                "signed_mean_difference_deg"
            ],
            "angular_mean_abs_diff_deg": angular[
                "mean_absolute_difference_deg"
            ],
            "angular_rms_diff_deg": angular[
                "rms_difference_deg"
            ],
            "angular_p95_abs_diff_deg": angular[
                "p95_absolute_difference_deg"
            ],
            "angular_max_abs_diff_deg": angular[
                "max_absolute_difference_deg"
            ],
            "chord_pearson_r": chord[
                "pearson_r"
            ],
            "chord_signed_mean_diff_px": chord[
                "signed_mean_difference"
            ],
            "chord_mean_abs_diff_px": chord[
                "mean_absolute_difference"
            ],
            "chord_rms_diff_px": chord[
                "rms_difference"
            ],
            "chord_p95_abs_diff_px": chord[
                "p95_absolute_difference"
            ],
            "chord_max_abs_diff_px": chord[
                "max_absolute_difference"
            ],
        }

    rows.append(
        flatten(
            "global",
            "ALL",
            crosspass[
                "pair_count"
            ],
            crosspass[
                "angular"
            ],
            crosspass[
                "chord"
            ],
        )
    )

    for result in crosspass[
        "segments"
    ]:
        rows.append(
            flatten(
                "segment",
                result[
                    "segment_id"
                ],
                result[
                    "pair_count"
                ],
                result[
                    "angular"
                ],
                result[
                    "chord"
                ],
            )
        )

    with OUT_CROSSPASS.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=fields,
        )

        writer.writeheader()

        for row in rows:
            formatted = {}

            for field in fields:
                value = row[
                    field
                ]

                if isinstance(
                    value,
                    float,
                ):
                    formatted[
                        field
                    ] = format(
                        value,
                        ".15g",
                    )

                elif value is None:
                    formatted[
                        field
                    ] = ""

                else:
                    formatted[
                        field
                    ] = value

            writer.writerow(
                formatted
            )


def write_figure(
    analysis: dict[
        str,
        Any,
    ],
) -> None:
    _, rows = (
        verify_dependencies()
    )

    figure, axes = plt.subplots(
        2,
        2,
        figsize=(
            13,
            9,
        ),
    )

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

        q = np.array(
            [
                row[
                    "q"
                ]
                for row in selected
            ]
        )

        rho = np.array(
            [
                row[
                    "rho"
                ]
                for row in selected
            ]
        )

        phase_deg = np.degrees(
            np.array(
                [
                    row[
                        "phase_rad"
                    ]
                    for row in selected
                ]
            )
        )

        residual_deg = np.degrees(
            np.array(
                [
                    row[
                        "residual_rad"
                    ]
                    for row in selected
                ]
            )
        )

        axes[
            0,
            0
        ].plot(
            q,
            residual_deg,
            ".",
            markersize=1.5,
            alpha=0.35,
            label=f"Pass {pass_number}",
        )

        axes[
            0,
            1
        ].plot(
            rho,
            residual_deg,
            ".",
            markersize=1.5,
            alpha=0.35,
            label=f"Pass {pass_number}",
        )

        axes[
            1,
            0
        ].plot(
            phase_deg,
            residual_deg,
            ".",
            markersize=1.5,
            alpha=0.35,
            label=f"Pass {pass_number}",
        )

    pairs = pair_rows(
        rows
    )

    r1 = np.degrees(
        np.array(
            [
                pair[
                    0
                ][
                    "residual_rad"
                ]
                for pair in pairs
            ]
        )
    )

    r2 = np.degrees(
        np.array(
            [
                pair[
                    1
                ][
                    "residual_rad"
                ]
                for pair in pairs
            ]
        )
    )

    axes[
        1,
        1
    ].plot(
        r1,
        r2,
        ".",
        markersize=2.0,
        alpha=0.4,
    )

    lo = float(
        min(
            np.min(
                r1
            ),
            np.min(
                r2
            ),
        )
    )

    hi = float(
        max(
            np.max(
                r1
            ),
            np.max(
                r2
            ),
        )
    )

    axes[
        1,
        1
    ].plot(
        [
            lo,
            hi,
        ],
        [
            lo,
            hi,
        ],
        linestyle="--",
        linewidth=1.0,
    )

    axes[
        0,
        0
    ].set_xlabel(
        "Frozen source-order q"
    )

    axes[
        0,
        0
    ].set_ylabel(
        "Primary angular residual (deg)"
    )

    axes[
        0,
        0
    ].set_title(
        "Residual vs source order"
    )

    axes[
        0,
        1
    ].set_xlabel(
        "rho"
    )

    axes[
        0,
        1
    ].set_ylabel(
        "Primary angular residual (deg)"
    )

    axes[
        0,
        1
    ].set_title(
        "Residual vs radial position"
    )

    axes[
        1,
        0
    ].set_xlabel(
        "Observed winding phase (deg)"
    )

    axes[
        1,
        0
    ].set_ylabel(
        "Primary angular residual (deg)"
    )

    axes[
        1,
        0
    ].set_title(
        "Residual vs printed phase"
    )

    axes[
        1,
        1
    ].set_xlabel(
        "Pass 1 residual (deg)"
    )

    axes[
        1,
        1
    ].set_ylabel(
        "Pass 2 residual (deg)"
    )

    axes[
        1,
        1
    ].set_title(
        "Pointwise cross-pass replication"
    )

    for axis in axes.flat:
        axis.grid(
            True,
            alpha=0.25,
        )

    for axis in (
        axes[
            0,
            0
        ],
        axes[
            0,
            1
        ],
        axes[
            1,
            0
        ],
    ):
        axis.legend()

    figure.tight_layout()

    figure.savefig(
        OUT_PNG,
        dpi=180,
    )

    plt.close(
        figure
    )


def render_report(
    analysis: dict[
        str,
        Any,
    ],
) -> str:
    crosspass = analysis[
        "crosspass"
    ]

    angular = crosspass[
        "angular"
    ]

    chord = crosspass[
        "chord"
    ]

    sign = crosspass[
        "sign_replication"
    ]

    lines = [
        "# First Hand spherical reciprocal-spiral residual morphology",
        "",
        "**Checkpoint:** v0.8",
        "",
        f"**Analysis class:** `{analysis['analysis_class']}`",
        "",
        "## Scope",
        "",
        "This audit describes the already-frozen residual field of the",
        "primary isotropic reciprocal-spiral shape test.",
        "",
        "No model parameter was recomputed or adjusted.",
        "",
        "## Frozen scale context",
        "",
        f"    continuous trace RMS_equal  = {REPRO_RMS_EQUAL_PX:.12f} px",
        f"    continuous trace RMS_length = {REPRO_RMS_LENGTH_PX:.12f} px",
        f"    descriptive half-stroke     = {SPIRAL_HALF_STROKE_PX:.12f} px",
        "",
        "## Segment morphology",
        "",
        "| Pass | Segment | SSE fraction | signed mean (deg) | RMS (deg) | p95 (deg) | chord RMS (px) |",
        "| ---: | --- | ---: | ---: | ---: | ---: | ---: |",
    ]

    for result in analysis[
        "segments"
    ]:
        lines.append(
            "| "
            f"{result['pass_number']} | "
            f"{result['segment_id']} | "
            f"{result['sse_fraction']:.6f} | "
            f"{result['signed_mean_deg']:.6f} | "
            f"{result['rms_deg']:.6f} | "
            f"{result['p95_abs_deg']:.6f} | "
            f"{result['chord_rms_px']:.6f} |"
        )

    lines.extend(
        [
            "",
            "## Pointwise cross-pass replication",
            "",
            f"    N pairs                         = {crosspass['pair_count']}",
            f"    angular Pearson r               = {angular['pearson_r']}",
            f"    angular signed mean difference  = {angular['signed_mean_difference_deg']:.12f} deg",
            f"    angular mean absolute difference= {angular['mean_absolute_difference_deg']:.12f} deg",
            f"    angular RMS difference          = {angular['rms_difference_deg']:.12f} deg",
            f"    angular p95 difference          = {angular['p95_absolute_difference_deg']:.12f} deg",
            f"    chord Pearson r                 = {chord['pearson_r']}",
            f"    chord RMS difference            = {chord['rms_difference']:.12f} px",
            f"    chord p95 difference            = {chord['p95_absolute_difference']:.12f} px",
            "",
            "## Residual-sign replication",
            "",
            f"    positive-positive fraction      = {sign['positive_positive_fraction']:.12f}",
            f"    negative-negative fraction      = {sign['negative_negative_fraction']:.12f}",
            f"    opposite-sign fraction          = {sign['opposite_sign_fraction']:.12f}",
            f"    zero-involving fraction         = {sign['zero_involving_fraction']:.12f}",
            f"    same nonzero sign fraction      = {sign['same_nonzero_sign_fraction']}",
            "",
            "## Fixed morphology partitions",
            "",
            "The machine-readable bin table contains:",
            "",
            "    20 fixed rho bins",
            "    20 common pooled F(rho) bins",
            "    36 fixed 10-degree observed-phase bins",
            "    20 fixed source-order bins",
            "",
            "Empty bins are retained explicitly.",
            "",
            "## Interpretation boundary",
            "",
            "This report establishes residual morphology only.",
            "",
            "It does not select an anisotropic, projective, nonlinear, or",
            "otherwise expanded construction map.",
            "",
            "Any model expansion requires a separately frozen protocol.",
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

    OUT_JSON.write_text(
        json.dumps(
            analysis,
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )

    write_segment_csv(
        analysis
    )

    write_bins_csv(
        analysis
    )

    write_crosspass_csv(
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
            "Neutral residual-morphology audit for the frozen "
            "First Hand spherical reciprocal-spiral shape result."
        )
    )

    parser.add_argument(
        "--check-inputs",
        action="store_true",
        help=(
            "Verify the frozen parent residual field without calculating "
            "residual morphology."
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

        pairs = pair_rows(
            rows
        )

        print(
            "Frozen reciprocal-shape JSON: VERIFIED"
        )

        print(
            "Frozen reciprocal-shape sample table: VERIFIED"
        )

        print(
            "Frozen residual-morphology protocol: VERIFIED"
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
            f"Exact topological cross-pass pairs: {len(pairs)}"
        )

        print(
            "Primary residual field: residual_alpha_length_rad"
        )

        print(
            "Primary chord field: angular_chord_length_px"
        )

        print(
            "Parent fit recomputed: NO"
        )

        print(
            "New model parameters: 0"
        )

        print(
            "No residual morphology statistic was computed."
        )

        return 0

    analysis = (
        build_analysis()
    )

    write_outputs(
        analysis
    )

    crosspass = analysis[
        "crosspass"
    ]

    angular = crosspass[
        "angular"
    ]

    chord = crosspass[
        "chord"
    ]

    sign = crosspass[
        "sign_replication"
    ]

    print(
        "="
        * 88
    )

    print(
        "FIRST HAND RECIPROCAL-SPIRAL RESIDUAL MORPHOLOGY"
    )

    print(
        "="
        * 88
    )

    for pass_number in (
        1,
        2,
    ):
        print(
            f"PASS {pass_number} — SEGMENT SSE FRACTIONS"
        )

        selected = [
            result
            for result in analysis[
                "segments"
            ]
            if result[
                "pass_number"
            ] == pass_number
        ]

        for result in selected:
            print(
                f"  {result['segment_id']}: "
                f"SSE fraction={result['sse_fraction']:.6f}  "
                f"signed mean={result['signed_mean_deg']:.6f} deg  "
                f"RMS={result['rms_deg']:.6f} deg  "
                f"chord RMS={result['chord_rms_px']:.6f} px"
            )

        print(
            "-"
            * 88
        )

    print(
        "POINTWISE CROSS-PASS REPLICATION"
    )

    print(
        f"  pairs: {crosspass['pair_count']}"
    )

    print(
        "  angular Pearson r: "
        f"{angular['pearson_r']}"
    )

    print(
        "  angular RMS difference: "
        f"{angular['rms_difference_deg']:.9f} deg"
    )

    print(
        "  angular p95 difference: "
        f"{angular['p95_absolute_difference_deg']:.9f} deg"
    )

    print(
        "  chord Pearson r: "
        f"{chord['pearson_r']}"
    )

    print(
        "  chord RMS difference: "
        f"{chord['rms_difference']:.9f} px"
    )

    print(
        "  chord p95 difference: "
        f"{chord['p95_absolute_difference']:.9f} px"
    )

    print(
        "  same nonzero residual sign fraction: "
        f"{sign['same_nonzero_sign_fraction']}"
    )

    print(
        "  opposite-sign fraction: "
        f"{sign['opposite_sign_fraction']:.9f}"
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
        f"Wrote {OUT_BINS}"
    )

    print(
        f"Wrote {OUT_CROSSPASS}"
    )

    print(
        f"Wrote {OUT_PNG}"
    )

    print(
        f"Wrote {OUT_REPORT}"
    )

    print(
        "No parent-model refit or expanded construction model was used."
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
