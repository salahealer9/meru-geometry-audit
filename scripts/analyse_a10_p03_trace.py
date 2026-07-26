#!/usr/bin/env python3
"""Analyse the manually digitised A10_P03 source geometry."""

from __future__ import annotations

import csv
import json
from collections import defaultdict
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np

from meru_geometry.trace_analysis import (
    EllipseFit,
    endpoint_connection_candidates,
    fit_descriptive_ellipse,
    normalize_panel_coordinates,
    polyline_metrics,
    sample_ellipse,
)


ROOT = Path(__file__).resolve().parents[1]

JSON_PATH = (
    ROOT
    / "data"
    / "manual_digitizations"
    / "A10_P03"
    / "digitization.json"
)

CSV_PATH = (
    ROOT
    / "data"
    / "manual_digitizations"
    / "A10_P03"
    / "digitization.csv"
)

METRICS_PATH = (
    ROOT
    / "data"
    / "derived"
    / "a10_p03_segment_metrics.csv"
)

CANDIDATES_PATH = (
    ROOT
    / "data"
    / "derived"
    / "a10_p03_endpoint_candidates.csv"
)

REPORT_PATH = (
    ROOT
    / "docs"
    / "geometry"
    / "a10_p03_trace_analysis_v0_6.md"
)

TRACE_FIGURE = (
    ROOT
    / "figures"
    / "a10_p03_normalized_trace.png"
)

BOUNDARY_FIGURE = (
    ROOT
    / "figures"
    / "a10_p03_boundary_fits.png"
)

CANDIDATE_FIGURE = (
    ROOT
    / "figures"
    / "a10_p03_endpoint_candidates.png"
)

LAYER_ORDER = (
    "outer_boundary",
    "dimple_boundary",
    "red",
    "green",
    "blue",
)

DISPLAY = {
    "outer_boundary": {
        "label": "Outer boundary",
        "colour": "black",
        "linewidth": 1.8,
    },
    "dimple_boundary": {
        "label": "Dimple boundary",
        "colour": "tab:orange",
        "linewidth": 1.5,
    },
    "red": {
        "label": "Red centreline",
        "colour": "tab:red",
        "linewidth": 1.5,
    },
    "green": {
        "label": "Green centreline",
        "colour": "tab:green",
        "linewidth": 1.5,
    },
    "blue": {
        "label": "Blue centreline",
        "colour": "tab:blue",
        "linewidth": 1.5,
    },
}


def load_segments() -> dict[str, dict[int, np.ndarray]]:
    """Load ordered panel-coordinate segments from the flat CSV."""
    raw: dict[
        str,
        dict[int, list[tuple[int, float, float]]],
    ] = defaultdict(lambda: defaultdict(list))

    with CSV_PATH.open(
        newline="",
        encoding="utf-8",
    ) as handle:
        for row in csv.DictReader(handle):
            raw[row["layer"]][int(row["segment_id"])].append(
                (
                    int(row["point_index"]),
                    float(row["panel_x"]),
                    float(row["panel_y"]),
                )
            )

    result: dict[str, dict[int, np.ndarray]] = {}

    for layer_name, layer_segments in raw.items():
        result[layer_name] = {}

        for segment_id, records in layer_segments.items():
            records.sort(key=lambda record: record[0])

            result[layer_name][segment_id] = np.asarray(
                [
                    [record[1], record[2]]
                    for record in records
                ],
                dtype=np.float64,
            )

    return result


def concatenate_segments(
    segments: dict[int, np.ndarray],
) -> np.ndarray:
    """Combine all points from one layer."""
    return np.concatenate(
        [
            segments[segment_id]
            for segment_id in sorted(segments)
        ],
        axis=0,
    )


def plot_trace(
    segments: dict[str, dict[int, np.ndarray]],
    width_px: float,
    height_px: float,
) -> None:
    """Plot the digitised geometry in normalized coordinates."""
    fig, axis = plt.subplots(figsize=(8, 8))

    for layer_name in LAYER_ORDER:
        first_segment = True

        for segment_id in sorted(
            segments.get(layer_name, {})
        ):
            points = normalize_panel_coordinates(
                segments[layer_name][segment_id],
                width_px,
                height_px,
            )

            style = DISPLAY[layer_name]

            axis.plot(
                points[:, 0],
                points[:, 1],
                color=style["colour"],
                linewidth=style["linewidth"],
                marker="o",
                markersize=2.3,
                label=(
                    style["label"]
                    if first_segment
                    else None
                ),
            )

            first_segment = False

    axis.set_aspect("equal")
    axis.set_xlabel("Normalized x")
    axis.set_ylabel("Normalized y")
    axis.set_title(
        "A10_P03 source-derived trace\n"
        "visible segments only"
    )
    axis.legend()
    axis.grid(True, alpha=0.2)

    fig.tight_layout()
    fig.savefig(TRACE_FIGURE, dpi=220)
    plt.close(fig)

    print(f"Wrote {TRACE_FIGURE.relative_to(ROOT)}")


def plot_boundary_fits(
    outer_points: np.ndarray,
    dimple_segments: dict[int, np.ndarray],
    outer_fit: EllipseFit,
) -> None:
    """Plot the outer ellipse and visible non-elliptical dimple profile."""
    fig, axis = plt.subplots(figsize=(8, 8))

    axis.scatter(
        outer_points[:, 0],
        outer_points[:, 1],
        s=18,
        label="Outer boundary points",
    )

    outer_curve = sample_ellipse(outer_fit)

    axis.plot(
        outer_curve[:, 0],
        outer_curve[:, 1],
        linewidth=1.8,
        label="Outer descriptive ellipse",
    )

    first_dimple_segment = True

    for segment_id in sorted(dimple_segments):
        points = dimple_segments[segment_id]

        axis.plot(
            points[:, 0],
            points[:, 1],
            marker="o",
            markersize=3.0,
            linewidth=1.3,
            label=(
                "Visible dimple-neck segments"
                if first_dimple_segment
                else None
            ),
        )

        first_dimple_segment = False

    axis.axvline(
        outer_fit.centre_x,
        linestyle="--",
        linewidth=1.0,
        alpha=0.7,
        label="Outer-fit symmetry axis",
    )

    horizontal_margin = 8.0
    vertical_margin = 8.0

    axis.set_xlim(
        float(np.min(outer_points[:, 0])) - horizontal_margin,
        float(np.max(outer_points[:, 0])) + horizontal_margin,
    )

    axis.set_ylim(
        float(np.max(outer_points[:, 1])) + vertical_margin,
        float(np.min(outer_points[:, 1])) - vertical_margin,
    )

    axis.set_aspect("equal")
    axis.set_xlabel("Panel x (pixels)")
    axis.set_ylabel("Panel y (pixels)")
    axis.set_title(
        "A10_P03 boundary diagnostics\n"
        "outer ellipse and visible dimple-neck profile"
    )
    axis.legend()
    axis.grid(True, alpha=0.2)

    fig.tight_layout()
    fig.savefig(BOUNDARY_FIGURE, dpi=220)
    plt.close(fig)

    print(f"Wrote {BOUNDARY_FIGURE.relative_to(ROOT)}")


def plot_candidates(
    segments: dict[str, dict[int, np.ndarray]],
    candidates_by_layer: dict[str, tuple],
) -> None:
    """Plot the strongest endpoint-reconnection candidates."""
    fig, axis = plt.subplots(figsize=(8, 8))

    for layer_name in ("red", "green", "blue"):
        colour = DISPLAY[layer_name]["colour"]
        first_segment = True

        for segment_id in sorted(segments[layer_name]):
            points = segments[layer_name][segment_id]

            axis.plot(
                points[:, 0],
                points[:, 1],
                color=colour,
                linewidth=1.4,
                marker="o",
                markersize=2.0,
                label=(
                    DISPLAY[layer_name]["label"]
                    if first_segment
                    else None
                ),
            )

            first_segment = False

        for rank, candidate in enumerate(
            candidates_by_layer[layer_name][:3],
            start=1,
        ):
            segment_a = segments[layer_name][
                candidate.segment_a
            ]
            segment_b = segments[layer_name][
                candidate.segment_b
            ]

            point_a = (
                segment_a[0]
                if candidate.endpoint_a == "start"
                else segment_a[-1]
            )

            point_b = (
                segment_b[0]
                if candidate.endpoint_b == "start"
                else segment_b[-1]
            )

            axis.plot(
                [point_a[0], point_b[0]],
                [point_a[1], point_b[1]],
                linestyle="--",
                linewidth=1.0,
                color=colour,
                alpha=0.75,
            )

            midpoint = (point_a + point_b) / 2.0

            axis.text(
                midpoint[0],
                midpoint[1],
                f"{layer_name[0].upper()}{rank}",
                fontsize=8,
                color=colour,
            )

    axis.set_aspect("equal")
    axis.invert_yaxis()
    axis.set_xlabel("Panel x (pixels)")
    axis.set_ylabel("Panel y (pixels)")
    axis.set_title(
        "A10_P03 nearest tangent-aware endpoint candidates\n"
        "diagnostic only — no segments automatically joined"
    )
    axis.legend()
    axis.grid(True, alpha=0.2)

    fig.tight_layout()
    fig.savefig(CANDIDATE_FIGURE, dpi=220)
    plt.close(fig)

    print(f"Wrote {CANDIDATE_FIGURE.relative_to(ROOT)}")


def write_report(
    state: dict,
    layer_summaries: dict[str, dict[str, float]],
    outer_fit: EllipseFit,
    candidates_by_layer: dict[str, tuple],
) -> None:
    """Write the v0.6 source-trace analysis report."""
    total_points = int(
        sum(
            summary["points"]
            for summary in layer_summaries.values()
        )
    )

    total_segments = int(
        sum(
            summary["segments"]
            for summary in layer_summaries.values()
        )
    )

    lines = [
        "# A10_P03 Trace Analysis — v0.6",
        "",
        "## Dataset",
        "",
        f"- Panel: `{state['panel_id']}`",
        f"- Last digitisation update: `{state['updated_utc']}`",
        f"- Total traced points: **{total_points}**",
        f"- Non-empty visible segments: **{total_segments}**",
        "",
        "All measurements below describe the two-dimensional source drawing.",
        "",
        "## Layer geometry",
        "",
        "| Layer | Segments | Points | Total visible length (px) | "
        "Mean segment tortuosity |",
        "|---|---:|---:|---:|---:|",
    ]

    for layer_name in LAYER_ORDER:
        summary = layer_summaries[layer_name]

        tortuosity_text = (
            f"{summary['mean_tortuosity']:.4f}"
            if np.isfinite(summary["mean_tortuosity"])
            else "—"
        )

        lines.append(
            f"| {DISPLAY[layer_name]['label']} | "
            f"{int(summary['segments'])} | "
            f"{int(summary['points'])} | "
            f"{summary['length']:.3f} | "
            f"{tortuosity_text} |"
        )

    lines.extend(
        [
            "",
            "Visible centreline and dimple lengths do not include hidden or "
            "occluded continuations. The outer-boundary perimeter includes "
            "the closing edge from the final point to the initial point.",
            "",
            "## Boundary diagnostics",
            "",
            "### Outer boundary",
            "",
            "| Centre x | Centre y | Semi-major | Semi-minor | "
            "Axis ratio | Angle (degrees) | Radial RMS |",
            "|---:|---:|---:|---:|---:|---:|---:|",
            f"| {outer_fit.centre_x:.3f} | "
            f"{outer_fit.centre_y:.3f} | "
            f"{outer_fit.semi_major:.3f} | "
            f"{outer_fit.semi_minor:.3f} | "
            f"{outer_fit.semi_major / outer_fit.semi_minor:.4f} | "
            f"{np.degrees(outer_fit.angle_radians):.3f} | "
            f"{outer_fit.radial_rms:.5f} |",
            "",
            "The outer boundary is well described by a near-circular ellipse.",
            "",
            "### Dimple boundary",
            "",
            "The visible dimple trace is not a closed ellipse. It forms a "
            "fragmented bilateral neck or hourglass profile interrupted by "
            "occlusions. A free ellipse fit is therefore structurally "
            "inappropriate and has not been reported.",
            "",
            "The dimple will be analysed later as left and right neck "
            "profiles relative to the outer-boundary symmetry axis.",
            "",
            "## Endpoint reconnection candidates",
            "",
            "The following are the five strongest same-colour candidates "
            "under distance plus tangent-continuity ranking.",
            "",
        ]
    )

    for layer_name in ("red", "green", "blue"):
        lines.extend(
            [
                f"### {DISPLAY[layer_name]['label']}",
                "",
                "| Rank | Endpoint A | Endpoint B | Distance (px) | "
                "Tangent mismatch (degrees) | Score |",
                "|---:|---|---|---:|---:|---:|",
            ]
        )

        for rank, candidate in enumerate(
            candidates_by_layer[layer_name][:5],
            start=1,
        ):
            lines.append(
                f"| {rank} | "
                f"S{candidate.segment_a + 1} "
                f"{candidate.endpoint_a} | "
                f"S{candidate.segment_b + 1} "
                f"{candidate.endpoint_b} | "
                f"{candidate.distance:.3f} | "
                f"{np.degrees(candidate.tangent_mismatch_radians):.3f} | "
                f"{candidate.score:.3f} |"
            )

        lines.append("")

    lines.extend(
        [
            "## Interpretation boundary",
            "",
            "Endpoint rankings are diagnostic hypotheses only. No fragments "
            "have been joined automatically.",
            "",
            "The trace does not yet establish:",
            "",
            "- hidden strand continuity;",
            "- over/under crossing order;",
            "- a three-dimensional knot embedding;",
            "- the source camera model;",
            "- a dimpled-sphere surface equation;",
            "- equivalence with the canonical (3,10) torus knot.",
            "",
            "## Generated outputs",
            "",
            "- `figures/a10_p03_normalized_trace.png`",
            "- `figures/a10_p03_boundary_fits.png`",
            "- `figures/a10_p03_endpoint_candidates.png`",
            "- `data/derived/a10_p03_segment_metrics.csv` "
            "(local ignored output)",
            "- `data/derived/a10_p03_endpoint_candidates.csv` "
            "(local ignored output)",
            "",
        ]
    )

    REPORT_PATH.write_text(
        "\n".join(lines),
        encoding="utf-8",
    )

    print(f"Wrote {REPORT_PATH.relative_to(ROOT)}")


def main() -> None:
    """Run the complete A10_P03 source-trace analysis."""
    state = json.loads(
        JSON_PATH.read_text(encoding="utf-8")
    )

    width_px = float(
        state["panel_dimensions"]["width_px"]
    )
    height_px = float(
        state["panel_dimensions"]["height_px"]
    )

    segments = load_segments()

    layer_summaries: dict[str, dict[str, float]] = {}
    metric_rows: list[dict[str, object]] = []

    for layer_name in LAYER_ORDER:
        layer_segments = segments[layer_name]

        layer_lengths: list[float] = []
        layer_tortuosities: list[float] = []
        layer_points = 0

        for segment_id in sorted(layer_segments):
            is_closed = layer_name == "outer_boundary"

            metrics = polyline_metrics(
                layer_segments[segment_id],
                closed=is_closed,
            )

            layer_lengths.append(metrics.length)

            if np.isfinite(metrics.tortuosity):
                layer_tortuosities.append(
                    metrics.tortuosity
                )

            layer_points += metrics.point_count

            metric_rows.append(
                {
                    "layer": layer_name,
                    "segment_id": segment_id + 1,
                    **metrics._asdict(),
                }
            )

        layer_summaries[layer_name] = {
            "segments": float(len(layer_segments)),
            "points": float(layer_points),
            "length": float(sum(layer_lengths)),
            "mean_tortuosity": (
                float(np.mean(layer_tortuosities))
                if layer_tortuosities
                else float("nan")
            ),
        }

    METRICS_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    metric_fields = [
        "layer",
        "segment_id",
        *PolylineMetricFields,
    ]

    with METRICS_PATH.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=metric_fields,
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(metric_rows)

    print(f"Wrote {METRICS_PATH.relative_to(ROOT)}")

    outer_points = concatenate_segments(
        segments["outer_boundary"]
    )

    outer_fit = fit_descriptive_ellipse(
        outer_points
    )

    candidates_by_layer = {
        layer_name: endpoint_connection_candidates(
            segments[layer_name]
        )
        for layer_name in ("red", "green", "blue")
    }

    candidate_rows: list[dict[str, object]] = []

    for layer_name, candidates in candidates_by_layer.items():
        for rank, candidate in enumerate(
            candidates,
            start=1,
        ):
            candidate_rows.append(
                {
                    "layer": layer_name,
                    "rank": rank,
                    "segment_a": candidate.segment_a + 1,
                    "endpoint_a": candidate.endpoint_a,
                    "segment_b": candidate.segment_b + 1,
                    "endpoint_b": candidate.endpoint_b,
                    "distance": candidate.distance,
                    "tangent_mismatch_radians": (
                        candidate.tangent_mismatch_radians
                    ),
                    "score": candidate.score,
                }
            )

    with CANDIDATES_PATH.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as handle:
        fieldnames = [
            "layer",
            "rank",
            "segment_a",
            "endpoint_a",
            "segment_b",
            "endpoint_b",
            "distance",
            "tangent_mismatch_radians",
            "score",
        ]

        writer = csv.DictWriter(
            handle,
            fieldnames=fieldnames,
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(candidate_rows)

    print(f"Wrote {CANDIDATES_PATH.relative_to(ROOT)}")

    plot_trace(
        segments,
        width_px,
        height_px,
    )

    plot_boundary_fits(
        outer_points,
        segments["dimple_boundary"],
        outer_fit,
    )

    plot_candidates(
        segments,
        candidates_by_layer,
    )

    write_report(
        state,
        layer_summaries,
        outer_fit,
        candidates_by_layer,
    )

    print()
    print("Outer ellipse:", outer_fit)
    print(
        "Dimple model:",
        "fragmented bilateral neck profile; "
        "ellipse fit not attempted",
    )

    for layer_name in ("red", "green", "blue"):
        print()
        print(
            f"{DISPLAY[layer_name]['label']} "
            "top endpoint candidate:"
        )
        print(candidates_by_layer[layer_name][0])


PolylineMetricFields = [
    "point_count",
    "length",
    "chord_length",
    "tortuosity",
    "minimum_x",
    "maximum_x",
    "minimum_y",
    "maximum_y",
]


if __name__ == "__main__":
    main()
