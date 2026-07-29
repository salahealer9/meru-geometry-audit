#!/usr/bin/env python3
"""Find geometric crossing candidates in the A10_P03 traced cycle."""

from __future__ import annotations

import argparse
import csv
from collections import Counter, defaultdict
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

from meru_geometry.crossing_candidates import (
    CrossingCandidate,
    crossing_candidate_identifier,
    cycle_adjacency_pairs,
    find_crossing_candidates,
)
from meru_geometry.global_cycle import (
    audit_global_cycle,
)


ROOT = Path(__file__).resolve().parents[1]

DATA_DIR = (
    ROOT
    / "data"
    / "manual_digitizations"
    / "A10_P03"
)

DIGITIZATION_PATH = (
    DATA_DIR
    / "digitization.csv"
)

FIRST_STAGE_PATH = (
    DATA_DIR
    / "endpoint_adjudication.csv"
)

RESIDUAL_PATH = (
    DATA_DIR
    / "residual_endpoint_review.csv"
)

CROSS_COLOUR_PATH = (
    DATA_DIR
    / "cross_colour_endpoint_review.csv"
)

SOURCE_PANEL_PATH = (
    ROOT
    / "data"
    / "derived"
    / "source_inspection"
    / "panels"
    / "A10_P03.png"
)

CSV_PATH = (
    ROOT
    / "data"
    / "derived"
    / "a10_p03_crossing_candidates.csv"
)

FIGURE_PATH = (
    ROOT
    / "figures"
    / "a10_p03_crossing_candidates.png"
)

REPORT_PATH = (
    ROOT
    / "docs"
    / "geometry"
    / "a10_p03_crossing_candidate_census_v0_7.md"
)

LAYERS = (
    "red",
    "green",
    "blue",
)

COLOURS = {
    "red": "tab:red",
    "green": "tab:green",
    "blue": "tab:blue",
}


def load_segments() -> dict[
    tuple[str, int],
    np.ndarray,
]:
    """Load one-based visible centreline fragments."""
    raw: dict[
        tuple[str, int],
        list[tuple[int, float, float]],
    ] = defaultdict(list)

    with DIGITIZATION_PATH.open(
        newline="",
        encoding="utf-8",
    ) as handle:
        for row in csv.DictReader(handle):
            layer = row["layer"]

            if layer not in LAYERS:
                continue

            key = (
                layer,
                int(row["segment_id"]) + 1,
            )

            raw[key].append(
                (
                    int(row["point_index"]),
                    float(row["panel_x"]),
                    float(row["panel_y"]),
                )
            )

    result = {}

    for key, records in raw.items():
        records.sort(
            key=lambda record: record[0]
        )

        result[key] = np.asarray(
            [
                [record[1], record[2]]
                for record in records
            ],
            dtype=np.float64,
        )

    return result


def load_accepted(
    path: Path,
) -> list[dict[str, str]]:
    """Load accepted adjudication rows."""
    with path.open(
        newline="",
        encoding="utf-8",
    ) as handle:
        return [
            row
            for row in csv.DictReader(handle)
            if row["status"] == "accepted"
        ]


def build_cycle_traversal(
    segments: dict[
        tuple[str, int],
        np.ndarray,
    ],
) -> tuple[tuple[str, int], ...]:
    """Reproduce the v0.6 cycle and return its segment order."""
    segment_ids: dict[
        str,
        list[int],
    ] = defaultdict(list)

    for layer, segment_id in segments:
        segment_ids[layer].append(
            segment_id
        )

    same_colour = (
        load_accepted(FIRST_STAGE_PATH)
        + load_accepted(RESIDUAL_PATH)
    )

    cross_colour = load_accepted(
        CROSS_COLOUR_PATH
    )

    audit = audit_global_cycle(
        segment_ids,
        same_colour,
        cross_colour,
    )

    if not audit.is_single_cycle:
        raise RuntimeError(
            "The frozen v0.6 global cycle no longer validates."
        )

    return tuple(
        (
            visit.layer,
            visit.segment_id,
        )
        for visit in audit.segment_traversal
    )


def write_csv(
    candidates: tuple[
        CrossingCandidate,
        ...,
    ],
) -> None:
    """Write the local derived candidate table."""
    CSV_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    fieldnames = [
        "rank",
        "candidate_id",
        "layer_a",
        "segment_a",
        "layer_b",
        "segment_b",
        "candidate_kind",
        "panel_x",
        "panel_y",
        "distance_px",
        "crossing_angle_deg",
        "piece_index_a",
        "piece_index_b",
        "fraction_a",
        "fraction_b",
    ]

    with CSV_PATH.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=fieldnames,
            lineterminator="\n",
        )

        writer.writeheader()

        for rank, candidate in enumerate(
            candidates,
            start=1,
        ):
            writer.writerow(
                {
                    "rank": rank,
                    "candidate_id": (
                        crossing_candidate_identifier(
                            candidate
                        )
                    ),
                    "layer_a": candidate.key_a[0],
                    "segment_a": candidate.key_a[1],
                    "layer_b": candidate.key_b[0],
                    "segment_b": candidate.key_b[1],
                    "candidate_kind": (
                        candidate.candidate_kind
                    ),
                    "panel_x": candidate.point_x,
                    "panel_y": candidate.point_y,
                    "distance_px": (
                        candidate.distance
                    ),
                    "crossing_angle_deg": (
                        np.degrees(
                            candidate.crossing_angle_radians
                        )
                    ),
                    "piece_index_a": (
                        candidate.piece_index_a
                    ),
                    "piece_index_b": (
                        candidate.piece_index_b
                    ),
                    "fraction_a": (
                        candidate.fraction_a
                    ),
                    "fraction_b": (
                        candidate.fraction_b
                    ),
                }
            )

    print(f"Wrote {CSV_PATH.relative_to(ROOT)}")


def plot_candidates(
    segments: dict[
        tuple[str, int],
        np.ndarray,
    ],
    candidates: tuple[
        CrossingCandidate,
        ...,
    ],
) -> None:
    """Plot the complete diagnostic candidate census."""
    figure, axis = plt.subplots(
        figsize=(11, 9),
        constrained_layout=True,
    )

    if SOURCE_PANEL_PATH.exists():
        with Image.open(
            SOURCE_PANEL_PATH
        ) as source:
            axis.imshow(
                np.asarray(
                    source.convert("RGB")
                ),
                alpha=0.65,
            )

    for (
        layer,
        segment_id,
    ), points in segments.items():
        axis.plot(
            points[:, 0],
            points[:, 1],
            color=COLOURS[layer],
            linewidth=1.5,
            alpha=0.85,
        )

        midpoint = points[
            len(points) // 2
        ]

        axis.annotate(
            f"{layer[0].upper()}{segment_id}",
            midpoint,
            fontsize=6,
            color=COLOURS[layer],
        )

    for rank, candidate in enumerate(
        candidates,
        start=1,
    ):
        marker = (
            "o"
            if candidate.candidate_kind
            == "intersection"
            else "s"
        )

        axis.scatter(
            candidate.point_x,
            candidate.point_y,
            s=65,
            marker=marker,
            facecolors="white",
            edgecolors="black",
            linewidths=1.0,
            zorder=10,
        )

        axis.annotate(
            str(rank),
            (
                candidate.point_x,
                candidate.point_y,
            ),
            xytext=(4, 4),
            textcoords="offset points",
            fontsize=7,
            fontweight="bold",
            color="black",
            zorder=11,
        )

    axis.set_aspect("equal")
    axis.set_xlim(0, 190)
    axis.set_ylim(165, 0)
    axis.set_xticks([])
    axis.set_yticks([])

    axis.set_title(
        "A10_P03 geometric crossing-candidate census\n"
        "circles: polyline intersections; "
        "squares: close non-intersecting approaches"
    )

    figure.savefig(
        FIGURE_PATH,
        dpi=220,
    )

    plt.close(figure)

    print(
        f"Wrote {FIGURE_PATH.relative_to(ROOT)}"
    )


def write_report(
    candidates: tuple[
        CrossingCandidate,
        ...,
    ],
    max_distance: float,
    min_angle_degrees: float,
) -> None:
    """Write the candidate-census report."""
    kind_counts = Counter(
        candidate.candidate_kind
        for candidate in candidates
    )

    layer_pair_counts = Counter(
        "-".join(
            sorted(
                (
                    candidate.key_a[0],
                    candidate.key_b[0],
                )
            )
        )
        for candidate in candidates
    )

    lines = [
        "# A10_P03 Crossing-Candidate Census — v0.7",
        "",
        "## Purpose",
        "",
        "This diagnostic identifies non-adjacent visible fragments "
        "whose traced polylines intersect or approach closely enough "
        "to warrant manual source review.",
        "",
        "It does not assign crossing identity, over-under order, or "
        "three-dimensional depth.",
        "",
        "## Detection parameters",
        "",
        f"- Maximum polyline separation: `{max_distance:.3f} px`",
        f"- Minimum acute crossing angle: "
        f"`{min_angle_degrees:.3f}°`",
        "- Adjacent fragments in the frozen v0.6 cycle are excluded.",
        "- At most one closest approach is retained per visible "
        "segment pair in this initial census.",
        "",
        "## Summary",
        "",
        f"- Total candidates: **{len(candidates)}**",
        f"- Exact polyline intersections: "
        f"**{kind_counts.get('intersection', 0)}**",
        f"- Near-crossing approaches: "
        f"**{kind_counts.get('near_crossing', 0)}**",
        "",
        "Zero exact intersections are expected because the "
        "digitisation records visible fragments and terminates "
        "around source occlusions. Genuine projected crossings "
        "therefore normally appear as short centreline gaps.",
        "",
        "### Layer-pair counts",
        "",
        "| Layer pair | Candidates |",
        "|---|---:|",
    ]

    for layer_pair, count in sorted(
        layer_pair_counts.items()
    ):
        lines.append(
            f"| `{layer_pair}` | {count} |"
        )

    lines.extend(
        [
            "",
            "## Ranked candidates",
            "",
            "| Rank | Candidate | Kind | Distance (px) | "
            "Angle (degrees) | Position |",
            "|---:|---|---|---:|---:|---|",
        ]
    )

    for rank, candidate in enumerate(
        candidates,
        start=1,
    ):
        lines.append(
            f"| {rank} | "
            f"`{crossing_candidate_identifier(candidate)}` | "
            f"`{candidate.candidate_kind}` | "
            f"{candidate.distance:.3f} | "
            f"{np.degrees(candidate.crossing_angle_radians):.3f} | "
            f"({candidate.point_x:.2f}, "
            f"{candidate.point_y:.2f}) |"
        )

    lines.extend(
        [
            "",
            "## Interpretation boundary",
            "",
            "This is a geometric triage stage. Candidate status must "
            "be decided against the A10_P03 source panel.",
            "",
            "False positives may include:",
            "",
            "- nearby paths in different projected regions;",
            "- endpoint junctions not representing crossings;",
            "- nearly touching strands separated in depth;",
            "- artefacts of sparse manual polyline sampling.",
            "",
            "The next stage will generate candidate-specific source "
            "crops and a tracked manual crossing inventory.",
            "",
            "## Generated outputs",
            "",
            "- `figures/a10_p03_crossing_candidates.png`",
            "- `data/derived/a10_p03_crossing_candidates.csv` "
            "(local ignored output)",
            "",
        ]
    )

    REPORT_PATH.write_text(
        "\n".join(lines),
        encoding="utf-8",
    )

    print(f"Wrote {REPORT_PATH.relative_to(ROOT)}")


def parse_arguments() -> argparse.Namespace:
    """Parse command-line detection thresholds."""
    parser = argparse.ArgumentParser(
        description=__doc__,
    )

    parser.add_argument(
        "--max-distance",
        type=float,
        default=6.0,
        help=(
            "Maximum separation in source-panel pixels "
            "(default: 6)."
        ),
    )

    parser.add_argument(
        "--min-angle",
        type=float,
        default=12.0,
        help=(
            "Minimum acute crossing angle in degrees "
            "(default: 12)."
        ),
    )

    return parser.parse_args()


def main() -> None:
    """Run the initial A10_P03 crossing-candidate census."""
    arguments = parse_arguments()

    segments = load_segments()
    traversal = build_cycle_traversal(
        segments
    )

    adjacent_pairs = cycle_adjacency_pairs(
        traversal
    )

    candidates = find_crossing_candidates(
        segments,
        adjacent_pairs=adjacent_pairs,
        max_distance=arguments.max_distance,
        min_angle_degrees=arguments.min_angle,
    )

    write_csv(candidates)
    plot_candidates(
        segments,
        candidates,
    )

    write_report(
        candidates,
        max_distance=arguments.max_distance,
        min_angle_degrees=arguments.min_angle,
    )

    kind_counts = Counter(
        candidate.candidate_kind
        for candidate in candidates
    )

    print()
    print("Crossing-candidate census")
    print("=========================")
    print("Visible fragments:", len(segments))
    print(
        "Excluded cycle-adjacent pairs:",
        len(adjacent_pairs),
    )
    print("Candidates:", len(candidates))
    print(
        "Intersections:",
        kind_counts.get(
            "intersection",
            0,
        ),
    )
    print(
        "Near crossings:",
        kind_counts.get(
            "near_crossing",
            0,
        ),
    )


if __name__ == "__main__":
    main()
