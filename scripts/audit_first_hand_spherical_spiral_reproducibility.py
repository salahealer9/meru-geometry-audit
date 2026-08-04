#!/usr/bin/env python3
"""Neutral two-pass reproducibility audit for the First Hand spherical spiral.

This script compares the two independently frozen source traces only.

It does not:
- fit a reciprocal spiral;
- fit or register either acquisition;
- use endpoint holdouts;
- use coordinate-map or scaffold geometry;
- use click-index correspondence.

Each frozen one-to-one source segment is uniformly arclength-resampled and
compared by symmetric point-to-polyline distance.
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
    sys.path.insert(0, str(ROOT))

from scripts import digitize_first_hand_spherical_spiral as digitizer  # noqa: E402


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

SEAL1 = PASS1.with_suffix(".sha256")
SEAL2 = PASS2.with_suffix(".sha256")

PROTOCOL = (
    ROOT
    / "docs"
    / "first_hand_spherical_spiral_reproducibility_protocol.md"
)

METADATA_QC = (
    ROOT
    / "reports"
    / "first_hand_spherical_spiral_metadata_qc.md"
)

CORRESPONDENCE = (
    ROOT
    / "reports"
    / "first_hand_spherical_spiral_segment_correspondence.md"
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
    / "first_hand_spherical_spiral_reproducibility.json"
)

OUT_CSV = (
    OUTPUT_DIR
    / "first_hand_spherical_spiral_reproducibility_segments.csv"
)

OUT_PNG = (
    OUTPUT_DIR
    / "first_hand_spherical_spiral_reproducibility.png"
)

OUT_REPORT = (
    ROOT
    / "reports"
    / "first_hand_spherical_spiral_reproducibility.md"
)

ANALYSIS_CLASS = (
    "neutral_two_pass_spherical_spiral_acquisition_reproducibility"
)

N_RESAMPLE = 401

LIMB_RADIUS_PX = 341.906449919

PAIRINGS = tuple(
    (f"S{index:02d}", f"S{index:02d}")
    for index in range(1, 11)
)


def sha256_path(path: Path) -> str:
    digest = hashlib.sha256()

    with path.open("rb") as handle:
        for block in iter(
            lambda: handle.read(1024 * 1024),
            b"",
        ):
            digest.update(block)

    return digest.hexdigest()


def verify_sha256_manifest(
    manifest: Path,
    target: Path,
) -> None:
    if not manifest.exists():
        raise RuntimeError(
            f"Missing frozen seal: {manifest}"
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

    fields = lines[0].split(
        maxsplit=1
    )

    if len(fields) != 2:
        raise RuntimeError(
            f"Malformed SHA-256 record in {manifest}."
        )

    expected_hash = fields[0]
    recorded_name = fields[1].lstrip("*").strip()

    recorded_path = Path(
        recorded_name
    )

    if not recorded_path.is_absolute():
        recorded_path = ROOT / recorded_path

    if (
        recorded_path.resolve()
        != target.resolve()
    ):
        raise RuntimeError(
            f"{manifest} seals {recorded_path}, not {target}."
        )

    actual_hash = sha256_path(
        target
    )

    if actual_hash != expected_hash:
        raise RuntimeError(
            f"SHA-256 verification failed for {target}."
        )


def verify_correspondence_ledger() -> None:
    text = CORRESPONDENCE.read_text(
        encoding="utf-8"
    )

    for pass1_id, pass2_id in PAIRINGS:
        token = (
            f"P1:{pass1_id} <-> P2:{pass2_id}"
        )

        if token not in text:
            raise RuntimeError(
                f"Frozen correspondence missing: {token}"
            )

    required = (
        "ONE_TO_ONE:",
        "PASS1_SPLIT:",
        "PASS2_SPLIT:",
        "MANY_TO_MANY:",
        "UNRESOLVED:",
    )

    for token in required:
        if token not in text:
            raise RuntimeError(
                f"Correspondence ledger missing summary token: {token}"
            )


def verify_metadata_qc() -> None:
    text = METADATA_QC.read_text(
        encoding="utf-8"
    )

    if "QC_NONE_REQUIRED" not in text:
        raise RuntimeError(
            "Frozen metadata QC does not record QC_NONE_REQUIRED."
        )


def load_pass(
    path: Path,
    expected_pass: int,
) -> list[dict[str, str]]:
    return digitizer.validate_output_file(
        path,
        expected_pass=expected_pass,
    )


def group_by_segment(
    rows: Sequence[dict[str, str]],
) -> dict[str, list[dict[str, str]]]:
    grouped: dict[
        str,
        list[dict[str, str]],
    ] = {}

    for row in rows:
        grouped.setdefault(
            row["segment_id"],
            [],
        ).append(
            row
        )

    for segment_rows in grouped.values():
        segment_rows.sort(
            key=lambda row: int(
                row["sequence_index"]
            )
        )

    return dict(
        sorted(
            grouped.items()
        )
    )


def points_from_rows(
    rows: Sequence[dict[str, str]],
) -> np.ndarray:
    points = np.array(
        [
            [
                float(row["x_px"]),
                float(row["y_px"]),
            ]
            for row in rows
        ],
        dtype=float,
    )

    if (
        points.ndim != 2
        or points.shape[1] != 2
        or len(points) < 2
    ):
        raise RuntimeError(
            "Polyline requires at least two 2-D points."
        )

    if not np.all(
        np.isfinite(points)
    ):
        raise RuntimeError(
            "Polyline contains non-finite coordinates."
        )

    return points


def remove_consecutive_duplicates(
    points: np.ndarray,
) -> np.ndarray:
    if len(points) < 2:
        return points.copy()

    keep = np.ones(
        len(points),
        dtype=bool,
    )

    keep[1:] = (
        np.linalg.norm(
            np.diff(
                points,
                axis=0,
            ),
            axis=1,
        )
        > 0.0
    )

    cleaned = points[
        keep
    ]

    if len(cleaned) < 2:
        raise RuntimeError(
            "Polyline collapses to fewer than two unique points."
        )

    return cleaned


def polyline_length(
    points: np.ndarray,
) -> float:
    points = remove_consecutive_duplicates(
        points
    )

    return float(
        np.linalg.norm(
            np.diff(
                points,
                axis=0,
            ),
            axis=1,
        ).sum()
    )


def resample_polyline(
    points: np.ndarray,
    n_samples: int = N_RESAMPLE,
) -> np.ndarray:
    if n_samples < 2:
        raise ValueError(
            "n_samples must be at least 2."
        )

    points = remove_consecutive_duplicates(
        points
    )

    segment_lengths = np.linalg.norm(
        np.diff(
            points,
            axis=0,
        ),
        axis=1,
    )

    cumulative = np.concatenate(
        [
            np.array(
                [0.0]
            ),
            np.cumsum(
                segment_lengths
            ),
        ]
    )

    total = float(
        cumulative[-1]
    )

    if not (
        math.isfinite(total)
        and total > 0.0
    ):
        raise RuntimeError(
            "Polyline has zero or invalid arclength."
        )

    targets = np.linspace(
        0.0,
        total,
        n_samples,
    )

    indices = (
        np.searchsorted(
            cumulative,
            targets,
            side="right",
        )
        - 1
    )

    indices = np.clip(
        indices,
        0,
        len(points) - 2,
    )

    starts = cumulative[
        indices
    ]

    lengths = segment_lengths[
        indices
    ]

    fractions = (
        targets - starts
    ) / lengths

    return (
        points[
            indices
        ]
        + fractions[
            :,
            None,
        ]
        * (
            points[
                indices + 1
            ]
            - points[
                indices
            ]
        )
    )


def point_to_polyline_distances(
    query_points: np.ndarray,
    polyline: np.ndarray,
) -> np.ndarray:
    query_points = np.asarray(
        query_points,
        dtype=float,
    )

    polyline = remove_consecutive_duplicates(
        np.asarray(
            polyline,
            dtype=float,
        )
    )

    starts = polyline[
        :-1
    ]

    vectors = (
        polyline[
            1:
        ]
        - starts
    )

    squared_lengths = np.sum(
        vectors
        * vectors,
        axis=1,
    )

    if np.any(
        squared_lengths <= 0.0
    ):
        raise RuntimeError(
            "Target polyline contains zero-length segments."
        )

    offsets = (
        query_points[
            :,
            None,
            :,
        ]
        - starts[
            None,
            :,
            :,
        ]
    )

    parameters = np.sum(
        offsets
        * vectors[
            None,
            :,
            :,
        ],
        axis=2,
    ) / squared_lengths[
        None,
        :
    ]

    parameters = np.clip(
        parameters,
        0.0,
        1.0,
    )

    projections = (
        starts[
            None,
            :,
            :
        ]
        + parameters[
            :,
            :,
            None,
        ]
        * vectors[
            None,
            :,
            :,
        ]
    )

    squared_distances = np.sum(
        (
            query_points[
                :,
                None,
                :,
            ]
            - projections
        )
        ** 2,
        axis=2,
    )

    return np.sqrt(
        np.min(
            squared_distances,
            axis=1,
        )
    )


def symmetric_distance_sample(
    points_a: np.ndarray,
    points_b: np.ndarray,
) -> tuple[
    np.ndarray,
    np.ndarray,
    np.ndarray,
]:
    resampled_a = resample_polyline(
        points_a,
        N_RESAMPLE,
    )

    resampled_b = resample_polyline(
        points_b,
        N_RESAMPLE,
    )

    a_to_b = point_to_polyline_distances(
        resampled_a,
        resampled_b,
    )

    b_to_a = point_to_polyline_distances(
        resampled_b,
        resampled_a,
    )

    combined = np.concatenate(
        [
            a_to_b,
            b_to_a,
        ]
    )

    return (
        combined,
        resampled_a,
        resampled_b,
    )


def describe_distances(
    distances: np.ndarray,
) -> dict[str, float]:
    distances = np.asarray(
        distances,
        dtype=float,
    )

    if (
        distances.ndim != 1
        or len(distances) == 0
        or not np.all(
            np.isfinite(
                distances
            )
        )
    ):
        raise RuntimeError(
            "Invalid distance sample."
        )

    mse = float(
        np.mean(
            distances
            * distances
        )
    )

    return {
        "median_px": float(
            np.median(
                distances
            )
        ),
        "mean_px": float(
            np.mean(
                distances
            )
        ),
        "rms_px": math.sqrt(
            mse
        ),
        "p95_px": float(
            np.percentile(
                distances,
                95.0,
            )
        ),
        "max_px": float(
            np.max(
                distances
            )
        ),
        "mse_px2": mse,
    }


def aggregate_rms(
    segment_results: Sequence[
        dict[str, Any]
    ],
) -> dict[str, float]:
    if not segment_results:
        raise RuntimeError(
            "No resolved segment results."
        )

    mses = np.array(
        [
            result[
                "distance"
            ][
                "mse_px2"
            ]
            for result
            in segment_results
        ],
        dtype=float,
    )

    weights = np.array(
        [
            result[
                "mean_polyline_length_px"
            ]
            for result
            in segment_results
        ],
        dtype=float,
    )

    if np.any(
        weights <= 0.0
    ):
        raise RuntimeError(
            "All length weights must be positive."
        )

    equal_rms = math.sqrt(
        float(
            np.mean(
                mses
            )
        )
    )

    length_rms = math.sqrt(
        float(
            np.sum(
                weights
                * mses
            )
            / np.sum(
                weights
            )
        )
    )

    return {
        "rms_equal_segment_px": equal_rms,
        "rms_length_weighted_px": length_rms,
        "mean_segment_median_px": float(
            np.mean(
                [
                    result[
                        "distance"
                    ][
                        "median_px"
                    ]
                    for result
                    in segment_results
                ]
            )
        ),
        "mean_segment_p95_px": float(
            np.mean(
                [
                    result[
                        "distance"
                    ][
                        "p95_px"
                    ]
                    for result
                    in segment_results
                ]
            )
        ),
    }


def normalized_metrics(
    metrics: dict[str, float],
) -> dict[str, float]:
    result: dict[
        str,
        float,
    ] = {}

    for key, value in metrics.items():
        if key == "mse_px2":
            result[
                "mse_over_limb_radius_squared"
            ] = (
                value
                / (
                    LIMB_RADIUS_PX
                    ** 2
                )
            )
        elif key.endswith(
            "_px"
        ):
            result[
                key.replace(
                    "_px",
                    "_over_limb_radius",
                )
            ] = (
                value
                / LIMB_RADIUS_PX
            )

    return result


def median_width(
    rows: Sequence[
        dict[str, str]
    ],
) -> float:
    return float(
        np.median(
            [
                float(
                    row[
                        "local_stroke_width_px"
                    ]
                )
                for row
                in rows
            ]
        )
    )


def verify_dependencies() -> tuple[
    list[dict[str, str]],
    list[dict[str, str]],
]:
    for path in (
        PASS1,
        PASS2,
        PROTOCOL,
        METADATA_QC,
        CORRESPONDENCE,
    ):
        if not path.exists():
            raise RuntimeError(
                f"Missing frozen dependency: {path}"
            )

    verify_sha256_manifest(
        SEAL1,
        PASS1,
    )

    verify_sha256_manifest(
        SEAL2,
        PASS2,
    )

    verify_metadata_qc()

    verify_correspondence_ledger()

    rows1 = load_pass(
        PASS1,
        1,
    )

    rows2 = load_pass(
        PASS2,
        2,
    )

    groups1 = group_by_segment(
        rows1
    )

    groups2 = group_by_segment(
        rows2
    )

    expected1 = {
        pair[0]
        for pair in PAIRINGS
    }

    expected2 = {
        pair[1]
        for pair in PAIRINGS
    }

    if set(
        groups1
    ) != expected1:
        raise RuntimeError(
            "Pass-1 segment vocabulary differs from frozen correspondence."
        )

    if set(
        groups2
    ) != expected2:
        raise RuntimeError(
            "Pass-2 segment vocabulary differs from frozen correspondence."
        )

    return (
        rows1,
        rows2,
    )


def build_analysis() -> dict[str, Any]:
    rows1, rows2 = (
        verify_dependencies()
    )

    groups1 = (
        group_by_segment(
            rows1
        )
    )

    groups2 = (
        group_by_segment(
            rows2
        )
    )

    segments: list[
        dict[
            str,
            Any,
        ]
    ] = []

    for pass1_id, pass2_id in PAIRINGS:
        rows_a = groups1[
            pass1_id
        ]

        rows_b = groups2[
            pass2_id
        ]

        points_a = points_from_rows(
            rows_a
        )

        points_b = points_from_rows(
            rows_b
        )

        length_a = polyline_length(
            points_a
        )

        length_b = polyline_length(
            points_b
        )

        distances, _, _ = (
            symmetric_distance_sample(
                points_a,
                points_b,
            )
        )

        distance = describe_distances(
            distances
        )

        width_a = median_width(
            rows_a
        )

        width_b = median_width(
            rows_b
        )

        pooled_width = float(
            np.median(
                [
                    *[
                        float(
                            row[
                                "local_stroke_width_px"
                            ]
                        )
                        for row
                        in rows_a
                    ],
                    *[
                        float(
                            row[
                                "local_stroke_width_px"
                            ]
                        )
                        for row
                        in rows_b
                    ],
                ]
            )
        )

        sigma_source = max(
            2.0,
            0.5
            * pooled_width,
        )

        segments.append(
            {
                "pass1_segment_id": pass1_id,
                "pass2_segment_id": pass2_id,
                "correspondence_class": "ONE_TO_ONE",
                "pass1_raw_points": len(
                    rows_a
                ),
                "pass2_raw_points": len(
                    rows_b
                ),
                "pass1_polyline_length_px": length_a,
                "pass2_polyline_length_px": length_b,
                "mean_polyline_length_px": (
                    0.5
                    * (
                        length_a
                        + length_b
                    )
                ),
                "pass1_median_stroke_width_px": width_a,
                "pass2_median_stroke_width_px": width_b,
                "pooled_median_stroke_width_px": pooled_width,
                "sigma_source_px": sigma_source,
                "distance": distance,
                "distance_normalized": normalized_metrics(
                    distance
                ),
            }
        )

    aggregate = aggregate_rms(
        segments
    )

    aggregate_normalized = {
        key.replace(
            "_px",
            "_over_limb_radius",
        ): (
            value
            / LIMB_RADIUS_PX
        )
        for key, value
        in aggregate.items()
        if key.endswith(
            "_px"
        )
    }

    sigma_values = np.array(
        [
            result[
                "sigma_source_px"
            ]
            for result
            in segments
        ],
        dtype=float,
    )

    return {
        "analysis_class": ANALYSIS_CLASS,
        "status": (
            "post_blind_two_pass_neutral_reproducibility"
        ),
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
        "provenance": {
            "pass1": {
                "path": str(
                    PASS1.relative_to(
                        ROOT
                    )
                ),
                "sha256": sha256_path(
                    PASS1
                ),
                "rows": len(
                    rows1
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
                "rows": len(
                    rows2
                ),
            },
            "metadata_qc": {
                "path": str(
                    METADATA_QC.relative_to(
                        ROOT
                    )
                ),
                "sha256": sha256_path(
                    METADATA_QC
                ),
                "outcome": "QC_NONE_REQUIRED",
            },
            "correspondence": {
                "path": str(
                    CORRESPONDENCE.relative_to(
                        ROOT
                    )
                ),
                "sha256": sha256_path(
                    CORRESPONDENCE
                ),
                "resolved_one_to_one": 10,
                "unresolved": 0,
            },
        },
        "method": {
            "n_resample_per_segment": N_RESAMPLE,
            "distance": (
                "symmetric_point_to_resampled_polyline"
            ),
            "alignment_or_registration": False,
            "raw_click_index_matching": False,
            "smoothing_or_curve_fit": False,
            "theoretical_spiral_used": False,
            "coordinate_model_used": False,
            "endpoint_holdouts_used": False,
            "limb_radius_px": LIMB_RADIUS_PX,
        },
        "segments": segments,
        "aggregate": {
            **aggregate,
            **aggregate_normalized,
            "median_segment_sigma_source_px": float(
                np.median(
                    sigma_values
                )
            ),
            "min_segment_sigma_source_px": float(
                np.min(
                    sigma_values
                )
            ),
            "max_segment_sigma_source_px": float(
                np.max(
                    sigma_values
                )
            ),
        },
        "interpretation_boundary": {
            "establishes_source_trace_reproducibility_only": True,
            "establishes_reciprocal_spiral_model": False,
            "establishes_spherical_map": False,
            "establishes_coordinate_system": False,
            "endpoint_comparison_deferred": True,
        },
    }


def write_segment_csv(
    analysis: dict[str, Any],
) -> None:
    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    fields = [
        "segment_id",
        "pass1_raw_points",
        "pass2_raw_points",
        "pass1_polyline_length_px",
        "pass2_polyline_length_px",
        "mean_polyline_length_px",
        "pass1_median_stroke_width_px",
        "pass2_median_stroke_width_px",
        "sigma_source_px",
        "median_px",
        "mean_px",
        "rms_px",
        "p95_px",
        "max_px",
        "median_over_limb_radius",
        "rms_over_limb_radius",
        "p95_over_limb_radius",
        "max_over_limb_radius",
    ]

    with OUT_CSV.open(
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
            distance = result[
                "distance"
            ]

            normalized = result[
                "distance_normalized"
            ]

            writer.writerow(
                {
                    "segment_id": result[
                        "pass1_segment_id"
                    ],
                    "pass1_raw_points": result[
                        "pass1_raw_points"
                    ],
                    "pass2_raw_points": result[
                        "pass2_raw_points"
                    ],
                    "pass1_polyline_length_px": format(
                        result[
                            "pass1_polyline_length_px"
                        ],
                        ".12g",
                    ),
                    "pass2_polyline_length_px": format(
                        result[
                            "pass2_polyline_length_px"
                        ],
                        ".12g",
                    ),
                    "mean_polyline_length_px": format(
                        result[
                            "mean_polyline_length_px"
                        ],
                        ".12g",
                    ),
                    "pass1_median_stroke_width_px": format(
                        result[
                            "pass1_median_stroke_width_px"
                        ],
                        ".12g",
                    ),
                    "pass2_median_stroke_width_px": format(
                        result[
                            "pass2_median_stroke_width_px"
                        ],
                        ".12g",
                    ),
                    "sigma_source_px": format(
                        result[
                            "sigma_source_px"
                        ],
                        ".12g",
                    ),
                    "median_px": format(
                        distance[
                            "median_px"
                        ],
                        ".12g",
                    ),
                    "mean_px": format(
                        distance[
                            "mean_px"
                        ],
                        ".12g",
                    ),
                    "rms_px": format(
                        distance[
                            "rms_px"
                        ],
                        ".12g",
                    ),
                    "p95_px": format(
                        distance[
                            "p95_px"
                        ],
                        ".12g",
                    ),
                    "max_px": format(
                        distance[
                            "max_px"
                        ],
                        ".12g",
                    ),
                    "median_over_limb_radius": format(
                        normalized[
                            "median_over_limb_radius"
                        ],
                        ".12g",
                    ),
                    "rms_over_limb_radius": format(
                        normalized[
                            "rms_over_limb_radius"
                        ],
                        ".12g",
                    ),
                    "p95_over_limb_radius": format(
                        normalized[
                            "p95_over_limb_radius"
                        ],
                        ".12g",
                    ),
                    "max_over_limb_radius": format(
                        normalized[
                            "max_over_limb_radius"
                        ],
                        ".12g",
                    ),
                }
            )


def write_figure(
    analysis: dict[str, Any],
) -> None:
    segment_ids = [
        result[
            "pass1_segment_id"
        ]
        for result
        in analysis[
            "segments"
        ]
    ]

    rms = [
        result[
            "distance"
        ][
            "rms_px"
        ]
        for result
        in analysis[
            "segments"
        ]
    ]

    p95 = [
        result[
            "distance"
        ][
            "p95_px"
        ]
        for result
        in analysis[
            "segments"
        ]
    ]

    sigma = analysis[
        "aggregate"
    ][
        "median_segment_sigma_source_px"
    ]

    x = np.arange(
        len(
            segment_ids
        )
    )

    figure, axis = plt.subplots(
        figsize=(
            11,
            6,
        )
    )

    axis.plot(
        x,
        rms,
        marker="o",
        label="segment RMS",
    )

    axis.plot(
        x,
        p95,
        marker="s",
        label="segment p95",
    )

    axis.axhline(
        sigma,
        linestyle="--",
        label=(
            "descriptive half-stroke acquisition scale"
        ),
    )

    axis.set_xticks(
        x,
        segment_ids,
    )

    axis.set_xlabel(
        "Frozen one-to-one source segment"
    )

    axis.set_ylabel(
        "Two-pass symmetric distance (px)"
    )

    axis.set_title(
        "First Hand spherical spiral — two-pass acquisition reproducibility"
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


def render_report(
    analysis: dict[str, Any],
) -> str:
    aggregate = analysis[
        "aggregate"
    ]

    lines = [
        "# First Hand spherical spiral two-pass reproducibility",
        "",
        "**Checkpoint:** v0.8",
        "",
        f"**Analysis class:** `{analysis['analysis_class']}`",
        "",
        "## Frozen analysis conditions",
        "",
        "- Pass 1 and Pass 2 were independently acquired and sealed.",
        "- Metadata QC outcome: `QC_NONE_REQUIRED`.",
        "- Ten source-topological correspondences were frozen before distance calculation.",
        f"- Every segment is uniformly resampled to {N_RESAMPLE} points.",
        "- Primary metric: symmetric point-to-polyline distance.",
        "- No translation, rotation, scale, affine, projective, or ICP registration is applied.",
        "- No reciprocal-spiral, coordinate-map, scaffold, or endpoint-holdout information is used.",
        "",
        "## Segment results",
        "",
        "| Segment | P1 pts | P2 pts | mean length (px) | median (px) | RMS (px) | p95 (px) | max (px) | source scale (px) |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]

    for result in analysis[
        "segments"
    ]:
        distance = result[
            "distance"
        ]

        lines.append(
            "| "
            f"{result['pass1_segment_id']} | "
            f"{result['pass1_raw_points']} | "
            f"{result['pass2_raw_points']} | "
            f"{result['mean_polyline_length_px']:.6f} | "
            f"{distance['median_px']:.6f} | "
            f"{distance['rms_px']:.6f} | "
            f"{distance['p95_px']:.6f} | "
            f"{distance['max_px']:.6f} | "
            f"{result['sigma_source_px']:.6f} |"
        )

    lines.extend(
        [
            "",
            "## Aggregate reproducibility",
            "",
            "Equal-segment weighting:",
            "",
            f"    RMS_equal = {aggregate['rms_equal_segment_px']:.12f} px",
            "",
            "Curve-length weighting:",
            "",
            f"    RMS_length = {aggregate['rms_length_weighted_px']:.12f} px",
            "",
            "Descriptive equal-segment summaries:",
            "",
            f"    mean segment median = {aggregate['mean_segment_median_px']:.12f} px",
            f"    mean segment p95    = {aggregate['mean_segment_p95_px']:.12f} px",
            "",
            "Normalized by frozen spherical-limb radius:",
            "",
            f"    R_limb = {LIMB_RADIUS_PX:.12f} px",
            "",
            f"    RMS_equal / R_limb  = {aggregate['rms_equal_segment_over_limb_radius']:.12f}",
            f"    RMS_length / R_limb = {aggregate['rms_length_weighted_over_limb_radius']:.12f}",
            "",
            "Recorded source-reading scale:",
            "",
            f"    median sigma_source = {aggregate['median_segment_sigma_source_px']:.12f} px",
            "",
            "The source-reading scale is descriptive only and is not a",
            "Gaussian uncertainty, confidence interval, or post-hoc pass/fail",
            "threshold.",
            "",
            "## Interpretation boundary",
            "",
            "This checkpoint measures only the reproducibility with which the",
            "printed spherical spiral centreline can be acquired from the",
            "prepared source image.",
            "",
            "It does not establish that the trace is generated by `r*theta = 1`.",
            "",
            "It does not establish a spherical construction map.",
            "",
            "It does not resolve the previously frozen coordinate-family",
            "consistency results.",
            "",
            "Independent inner/outer endpoint holdouts remain unused and are",
            "deferred until this reproducibility result is frozen.",
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

    write_segment_csv(
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
            "Neutral two-pass reproducibility audit for the "
            "First Hand spherical spiral."
        )
    )

    parser.add_argument(
        "--check-inputs",
        action="store_true",
        help=(
            "Verify frozen dependencies without calculating "
            "cross-pass distances."
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

        groups1 = (
            group_by_segment(
                rows1
            )
        )

        groups2 = (
            group_by_segment(
                rows2
            )
        )

        print(
            "Pass 1 SHA-256 seal: VERIFIED"
        )

        print(
            "Pass 2 SHA-256 seal: VERIFIED"
        )

        print(
            "Metadata QC outcome: QC_NONE_REQUIRED"
        )

        print(
            "Frozen correspondence: 10 ONE_TO_ONE, 0 unresolved"
        )

        print(
            f"Pass 1: {len(rows1)} rows, {len(groups1)} segments"
        )

        print(
            f"Pass 2: {len(rows2)} rows, {len(groups2)} segments"
        )

        print(
            f"Fixed arclength resampling: {N_RESAMPLE} points per segment"
        )

        print(
            "No cross-pass distance was computed."
        )

        return 0

    analysis = (
        build_analysis()
    )

    write_outputs(
        analysis
    )

    aggregate = analysis[
        "aggregate"
    ]

    print(
        "="
        * 88
    )

    print(
        "FIRST HAND SPHERICAL SPIRAL TWO-PASS REPRODUCIBILITY"
    )

    print(
        "="
        * 88
    )

    for result in analysis[
        "segments"
    ]:
        distance = result[
            "distance"
        ]

        print(
            f"{result['pass1_segment_id']}: "
            f"median={distance['median_px']:.6f} px  "
            f"RMS={distance['rms_px']:.6f} px  "
            f"p95={distance['p95_px']:.6f} px  "
            f"max={distance['max_px']:.6f} px"
        )

    print(
        "-"
        * 88
    )

    print(
        "RMS equal-segment: "
        f"{aggregate['rms_equal_segment_px']:.12f} px"
    )

    print(
        "RMS length-weighted: "
        f"{aggregate['rms_length_weighted_px']:.12f} px"
    )

    print(
        "Median descriptive source scale: "
        f"{aggregate['median_segment_sigma_source_px']:.12f} px"
    )

    print(
        "-"
        * 88
    )

    print(
        f"Wrote {OUT_JSON}"
    )

    print(
        f"Wrote {OUT_CSV}"
    )

    print(
        f"Wrote {OUT_PNG}"
    )

    print(
        f"Wrote {OUT_REPORT}"
    )

    print(
        "No theoretical spiral, registration, coordinate model, "
        "scaffold model, or endpoint holdout was used."
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
