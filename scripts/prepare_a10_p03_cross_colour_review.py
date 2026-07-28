#!/usr/bin/env python3
"""Prepare cross-colour endpoint and complete-matching review materials."""

from __future__ import annotations

import csv
import math
from collections import defaultdict
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageOps

from meru_geometry.connectivity import (
    build_endpoint_connectivity,
)
from meru_geometry.cross_colour_connectivity import (
    CrossColourCandidate,
    CrossColourMatching,
    candidate_endpoint_keys,
    cross_colour_candidate_identifier,
    enumerate_cross_colour_matchings,
    rank_cross_colour_pairs,
    validate_cross_colour_review_rows,
)
from meru_geometry.endpoint_review import MANUAL_FIELDS
from meru_geometry.residual_connectivity import (
    endpoint_coordinate,
)


ROOT = Path(__file__).resolve().parents[1]

DIGITIZATION_PATH = (
    ROOT
    / "data"
    / "manual_digitizations"
    / "A10_P03"
    / "digitization.csv"
)

FIRST_STAGE_PATH = (
    ROOT
    / "data"
    / "manual_digitizations"
    / "A10_P03"
    / "endpoint_adjudication.csv"
)

RESIDUAL_PATH = (
    ROOT
    / "data"
    / "manual_digitizations"
    / "A10_P03"
    / "residual_endpoint_review.csv"
)

REVIEW_PATH = (
    ROOT
    / "data"
    / "manual_digitizations"
    / "A10_P03"
    / "cross_colour_endpoint_review.csv"
)

CANDIDATE_TABLE = (
    ROOT
    / "data"
    / "derived"
    / "a10_p03_cross_colour_candidates.csv"
)

MATCHING_TABLE = (
    ROOT
    / "data"
    / "derived"
    / "a10_p03_cross_colour_matchings.csv"
)

REPORT_PATH = (
    ROOT
    / "docs"
    / "geometry"
    / "a10_p03_cross_colour_candidate_audit_v0_6.md"
)

PANEL_DIR = (
    ROOT
    / "data"
    / "derived"
    / "source_inspection"
    / "panels"
)

P03_PATH = PANEL_DIR / "A10_P03.png"
P01_PATH = PANEL_DIR / "A10_P01.png"
P02_PATH = PANEL_DIR / "A10_P02.png"

INDIVIDUAL_DIR = (
    ROOT
    / "data"
    / "derived"
    / "source_inspection"
    / "cross_colour_review"
    / "candidates"
)

MATCHING_DIR = (
    ROOT
    / "data"
    / "derived"
    / "source_inspection"
    / "cross_colour_review"
    / "matchings"
)

CANDIDATE_SHEET = (
    ROOT
    / "data"
    / "derived"
    / "source_inspection"
    / "cross_colour_review"
    / "a10_p03_cross_colour_candidate_sheet.png"
)

MATCHING_SHEET = (
    ROOT
    / "data"
    / "derived"
    / "source_inspection"
    / "cross_colour_review"
    / "a10_p03_cross_colour_matching_sheet.png"
)

LAYERS = ("red", "green", "blue")

COLOURS = {
    "red": "tab:red",
    "green": "tab:green",
    "blue": "tab:blue",
}

FIELDNAMES = [
    "candidate_id",
    "rank",
    "layer_a",
    "segment_a",
    "endpoint_a",
    "layer_b",
    "segment_b",
    "endpoint_b",
    "distance_px",
    "tangent_mismatch_deg",
    "score",
    "status",
    "confidence",
    "reason_code",
    "notes",
    "reviewed_utc",
]


def load_segments() -> dict[str, dict[int, np.ndarray]]:
    """Load one-based visible segment arrays."""
    raw = defaultdict(lambda: defaultdict(list))

    with DIGITIZATION_PATH.open(
        newline="",
        encoding="utf-8",
    ) as handle:
        for row in csv.DictReader(handle):
            layer = row["layer"]

            if layer not in LAYERS:
                continue

            segment_id = int(row["segment_id"]) + 1

            raw[layer][segment_id].append(
                (
                    int(row["point_index"]),
                    float(row["panel_x"]),
                    float(row["panel_y"]),
                )
            )

    result: dict[str, dict[int, np.ndarray]] = {}

    for layer, layer_segments in raw.items():
        result[layer] = {}

        for segment_id, records in layer_segments.items():
            records.sort(key=lambda record: record[0])

            result[layer][segment_id] = np.asarray(
                [
                    [record[1], record[2]]
                    for record in records
                ],
                dtype=np.float64,
            )

    return result


def accepted_rows(path: Path) -> list[dict[str, str]]:
    """Load accepted rows from one adjudication table."""
    with path.open(
        newline="",
        encoding="utf-8",
    ) as handle:
        return [
            row
            for row in csv.DictReader(handle)
            if row["status"] == "accepted"
        ]


def build_components(
    segments: dict[str, dict[int, np.ndarray]],
) -> dict[str, tuple]:
    """Build the three completed same-colour open chains."""
    accepted = (
        accepted_rows(FIRST_STAGE_PATH)
        + accepted_rows(RESIDUAL_PATH)
    )

    result = {}

    for layer in LAYERS:
        components = build_endpoint_connectivity(
            segments[layer].keys(),
            [
                row
                for row in accepted
                if row["layer"] == layer
            ],
        )

        if len(components) != 1:
            raise RuntimeError(
                f"{layer}: expected one component; "
                f"found {len(components)}."
            )

        if len(components[0].free_endpoints) != 2:
            raise RuntimeError(
                f"{layer}: expected two free endpoints."
            )

        result[layer] = components

    return result


def load_existing() -> dict[str, dict[str, str]]:
    """Load existing manual cross-colour decisions."""
    if not REVIEW_PATH.exists():
        return {}

    with REVIEW_PATH.open(
        newline="",
        encoding="utf-8",
    ) as handle:
        return {
            row["candidate_id"]: row
            for row in csv.DictReader(handle)
        }


def build_review_rows(
    candidates: tuple[CrossColourCandidate, ...],
) -> list[dict[str, object]]:
    """Create candidate rows while preserving manual fields."""
    existing = load_existing()
    rows: list[dict[str, object]] = []

    for rank, candidate in enumerate(
        candidates,
        start=1,
    ):
        identifier = cross_colour_candidate_identifier(
            candidate
        )

        row: dict[str, object] = {
            "candidate_id": identifier,
            "rank": rank,
            "layer_a": candidate.layer_a,
            "segment_a": candidate.segment_a,
            "endpoint_a": candidate.endpoint_a,
            "layer_b": candidate.layer_b,
            "segment_b": candidate.segment_b,
            "endpoint_b": candidate.endpoint_b,
            "distance_px": candidate.distance,
            "tangent_mismatch_deg": float(
                np.degrees(
                    candidate.tangent_mismatch_radians
                )
            ),
            "score": candidate.score,
            "status": "unreviewed",
            "confidence": "",
            "reason_code": "",
            "notes": "",
            "reviewed_utc": "",
        }

        previous = existing.get(identifier)

        if previous is not None:
            for field in MANUAL_FIELDS:
                row[field] = previous.get(
                    field,
                    row[field],
                )

        rows.append(row)

    validate_cross_colour_review_rows(rows)
    return rows


def write_csv(
    path: Path,
    rows: list[dict[str, object]],
    fieldnames: list[str],
) -> None:
    """Write a deterministic CSV table."""
    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with path.open(
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
        writer.writerows(rows)

    print(f"Wrote {path.relative_to(ROOT)}")


def load_image(path: Path) -> np.ndarray:
    """Load one local source panel."""
    if not path.exists():
        raise RuntimeError(
            f"Missing source panel: {path.relative_to(ROOT)}"
        )

    with Image.open(path) as source:
        return np.asarray(source.convert("RGB"))


def draw_all_segments(
    axis: plt.Axes,
    segments: dict[str, dict[int, np.ndarray]],
    highlighted: set[tuple[str, int]] = frozenset(),
) -> None:
    """Draw all coloured traces."""
    for layer, layer_segments in segments.items():
        for segment_id, points in layer_segments.items():
            selected = (
                layer,
                segment_id,
            ) in highlighted

            axis.plot(
                points[:, 0],
                points[:, 1],
                color=COLOURS[layer],
                linewidth=2.7 if selected else 0.9,
                alpha=1.0 if selected else 0.30,
                marker="o" if selected else None,
                markersize=3.0,
            )


def candidate_points(
    candidate: CrossColourCandidate,
    segments: dict[str, dict[int, np.ndarray]],
) -> tuple[np.ndarray, np.ndarray]:
    """Return the two source coordinates of a candidate."""
    point_a = endpoint_coordinate(
        segments[candidate.layer_a][
            candidate.segment_a
        ],
        candidate.endpoint_a,
    )

    point_b = endpoint_coordinate(
        segments[candidate.layer_b][
            candidate.segment_b
        ],
        candidate.endpoint_b,
    )

    return point_a, point_b


def plot_candidate(
    candidate: CrossColourCandidate,
    rank: int,
    segments: dict[str, dict[int, np.ndarray]],
    p03: np.ndarray,
    p01: np.ndarray,
    p02: np.ndarray,
) -> Path:
    """Generate a four-panel cross-colour candidate image."""
    point_a, point_b = candidate_points(
        candidate,
        segments,
    )

    segment_a = segments[
        candidate.layer_a
    ][candidate.segment_a]

    segment_b = segments[
        candidate.layer_b
    ][candidate.segment_b]

    figure, axes = plt.subplots(
        2,
        2,
        figsize=(12, 10),
        constrained_layout=True,
    )

    highlighted = {
        (
            candidate.layer_a,
            candidate.segment_a,
        ),
        (
            candidate.layer_b,
            candidate.segment_b,
        ),
    }

    for axis in (axes[0, 0], axes[0, 1]):
        axis.imshow(p03)
        draw_all_segments(
            axis,
            segments,
            highlighted,
        )

        axis.plot(
            [point_a[0], point_b[0]],
            [point_a[1], point_b[1]],
            linestyle="--",
            linewidth=2.0,
            color="black",
        )

        axis.scatter(
            point_a[0],
            point_a[1],
            s=85,
            color=COLOURS[candidate.layer_a],
            edgecolors="black",
            linewidths=0.8,
            zorder=10,
        )

        axis.scatter(
            point_b[0],
            point_b[1],
            s=85,
            color=COLOURS[candidate.layer_b],
            edgecolors="black",
            linewidths=0.8,
            zorder=10,
        )

        axis.set_aspect("equal")
        axis.set_xticks([])
        axis.set_yticks([])

    axes[0, 0].set_title("A10_P03 full panel")

    combined = np.concatenate(
        (
            segment_a,
            segment_b,
            point_a[None, :],
            point_b[None, :],
        ),
        axis=0,
    )

    minimum = np.min(combined, axis=0)
    maximum = np.max(combined, axis=0)

    margin = max(
        8.0,
        0.20 * float(np.max(maximum - minimum)),
    )

    axes[0, 1].set_xlim(
        minimum[0] - margin,
        maximum[0] + margin,
    )

    axes[0, 1].set_ylim(
        maximum[1] + margin,
        minimum[1] - margin,
    )

    axes[0, 1].set_title("A10_P03 close-up")

    axes[1, 0].imshow(p01)
    axes[1, 0].set_axis_off()
    axes[1, 0].set_title(
        "A10_P01 ring-to-dimple transition"
    )

    axes[1, 1].imshow(p02)
    axes[1, 1].set_axis_off()
    axes[1, 1].set_title(
        "A10_P02 winding-zero transition"
    )

    identifier = cross_colour_candidate_identifier(
        candidate
    )

    figure.suptitle(
        f"Rank {rank}: {identifier}\n"
        f"distance={candidate.distance:.3f} px; "
        f"tangent mismatch="
        f"{np.degrees(candidate.tangent_mismatch_radians):.2f}°"
    )

    INDIVIDUAL_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_path = (
        INDIVIDUAL_DIR
        / f"{identifier}.png"
    )

    figure.savefig(output_path, dpi=190)
    plt.close(figure)

    return output_path


def plot_matching(
    matching: CrossColourMatching,
    rank: int,
    segments: dict[str, dict[int, np.ndarray]],
    p03: np.ndarray,
) -> Path:
    """Plot one complete three-edge transition hypothesis."""
    figure, axis = plt.subplots(
        figsize=(9, 8),
        constrained_layout=True,
    )

    axis.imshow(p03)
    draw_all_segments(axis, segments)

    identifiers = []

    for edge_number, candidate in enumerate(
        matching.candidates,
        start=1,
    ):
        point_a, point_b = candidate_points(
            candidate,
            segments,
        )

        axis.plot(
            [point_a[0], point_b[0]],
            [point_a[1], point_b[1]],
            linestyle="--",
            linewidth=2.0,
            color="black",
        )

        axis.scatter(
            point_a[0],
            point_a[1],
            s=80,
            color=COLOURS[candidate.layer_a],
            edgecolors="black",
            linewidths=0.8,
            zorder=10,
        )

        axis.scatter(
            point_b[0],
            point_b[1],
            s=80,
            color=COLOURS[candidate.layer_b],
            edgecolors="black",
            linewidths=0.8,
            zorder=10,
        )

        midpoint = (
            point_a + point_b
        ) / 2.0

        axis.annotate(
            str(edge_number),
            midpoint,
            fontsize=10,
            fontweight="bold",
        )

        identifiers.append(
            f"{edge_number}. "
            f"{cross_colour_candidate_identifier(candidate)}"
        )

    axis.set_aspect("equal")
    axis.set_xticks([])
    axis.set_yticks([])

    axis.set_title(
        f"Complete matching {rank}\n"
        f"total score={matching.total_score:.3f}; "
        f"total distance={matching.total_distance:.3f} px"
    )

    axis.text(
        0.01,
        -0.08,
        "\n".join(identifiers),
        transform=axis.transAxes,
        fontsize=8,
        va="top",
    )

    MATCHING_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_path = (
        MATCHING_DIR
        / f"matching_{rank:02d}.png"
    )

    figure.savefig(output_path, dpi=190)
    plt.close(figure)

    return output_path


def build_contact_sheet(
    image_paths: list[Path],
    labels: list[str],
    output_path: Path,
    columns: int,
) -> None:
    """Build a local image contact sheet."""
    cell_width = 620
    cell_height = 500
    margin = 12
    label_height = 38

    rows = math.ceil(
        len(image_paths) / columns
    )

    canvas = Image.new(
        "RGB",
        (
            columns * cell_width,
            rows * cell_height,
        ),
        "white",
    )

    draw = ImageDraw.Draw(canvas)
    font = ImageFont.load_default()

    for index, (path, label) in enumerate(
        zip(image_paths, labels, strict=True)
    ):
        grid_row = index // columns
        grid_column = index % columns

        left = grid_column * cell_width
        top = grid_row * cell_height

        with Image.open(path) as source:
            thumbnail = ImageOps.contain(
                source.convert("RGB"),
                (
                    cell_width - 2 * margin,
                    cell_height
                    - label_height
                    - 2 * margin,
                ),
                method=Image.Resampling.LANCZOS,
            )

        image_x = (
            left
            + (cell_width - thumbnail.width) // 2
        )

        canvas.paste(
            thumbnail,
            (image_x, top + margin),
        )

        draw.text(
            (
                left + margin,
                top + cell_height
                - label_height
                + 8,
            ),
            label,
            fill="black",
            font=font,
        )

        draw.rectangle(
            (
                left,
                top,
                left + cell_width - 1,
                top + cell_height - 1,
            ),
            outline="grey",
            width=1,
        )

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    canvas.save(output_path)
    print(f"Wrote {output_path.relative_to(ROOT)}")


def write_report(
    candidates: tuple[CrossColourCandidate, ...],
    matchings: tuple[CrossColourMatching, ...],
    free_endpoints: dict[str, tuple],
) -> None:
    """Write the candidate and matching audit report."""
    lines = [
        "# A10_P03 Cross-Colour Candidate Audit — v0.6",
        "",
        "## Current graph boundary",
        "",
        "The red, green and blue traces each form one non-branched "
        "open chain with two free endpoints.",
        "",
        "| Layer | Free endpoints |",
        "|---|---|",
    ]

    for layer in LAYERS:
        endpoint_text = ", ".join(
            (
                f"S{segment_id:02d}"
                f"{'S' if endpoint == 'start' else 'E'}"
            )
            for segment_id, endpoint
            in free_endpoints[layer]
        )

        lines.append(
            f"| {layer.capitalize()} | "
            f"`{endpoint_text}` |"
        )

    lines.extend(
        [
            "",
            "## Cross-colour edge candidates",
            "",
            "All 12 pairings between differently coloured free "
            "endpoints are included.",
            "",
            "| Rank | Candidate | Distance (px) | "
            "Tangent mismatch (degrees) | Score |",
            "|---:|---|---:|---:|---:|",
        ]
    )

    for rank, candidate in enumerate(
        candidates,
        start=1,
    ):
        lines.append(
            f"| {rank} | "
            f"`{cross_colour_candidate_identifier(candidate)}` | "
            f"{candidate.distance:.3f} | "
            f"{np.degrees(candidate.tangent_mismatch_radians):.3f} | "
            f"{candidate.score:.3f} |"
        )

    lines.extend(
        [
            "",
            "## Complete perfect matchings",
            "",
            "A perfect matching uses all six free endpoints exactly "
            "once. There are eight such cross-colour matchings.",
            "",
            "| Rank | Candidate edges | Total distance (px) | "
            "Total score | Maximum edge score |",
            "|---:|---|---:|---:|---:|",
        ]
    )

    for rank, matching in enumerate(
        matchings,
        start=1,
    ):
        identifiers = "<br>".join(
            f"`{cross_colour_candidate_identifier(candidate)}`"
            for candidate in matching.candidates
        )

        lines.append(
            f"| {rank} | {identifiers} | "
            f"{matching.total_distance:.3f} | "
            f"{matching.total_score:.3f} | "
            f"{matching.maximum_edge_score:.3f} |"
        )

    lines.extend(
        [
            "",
            "## Interpretation boundary",
            "",
            "The ranking is geometric triage only. A short endpoint "
            "gap does not establish a real colour transition.",
            "",
            "A complete matching is a combinatorial hypothesis, not "
            "a source-supported reconstruction. Each of its three "
            "edges must be independently reviewed against A10_P03.",
            "",
            "Acceptance of three mutually compatible transition edges "
            "would join the three open colour chains into one closed "
            "cycle. It would not by itself prove a unique three-"
            "dimensional knot embedding.",
            "",
        ]
    )

    REPORT_PATH.write_text(
        "\n".join(lines),
        encoding="utf-8",
    )

    print(f"Wrote {REPORT_PATH.relative_to(ROOT)}")


def main() -> None:
    """Generate the complete cross-colour review package."""
    segments = load_segments()
    components = build_components(segments)

    free_endpoints = {
        layer: components[layer][0].free_endpoints
        for layer in LAYERS
    }

    candidates = rank_cross_colour_pairs(
        segments,
        free_endpoints,
    )

    matchings = enumerate_cross_colour_matchings(
        candidates
    )

    if len(candidates) != 12:
        raise RuntimeError(
            f"Expected 12 candidates; found {len(candidates)}."
        )

    if len(matchings) != 8:
        raise RuntimeError(
            f"Expected 8 matchings; found {len(matchings)}."
        )

    rows = build_review_rows(candidates)

    write_csv(
        REVIEW_PATH,
        rows,
        FIELDNAMES,
    )

    write_csv(
        CANDIDATE_TABLE,
        rows,
        FIELDNAMES,
    )

    matching_rows = []

    for rank, matching in enumerate(
        matchings,
        start=1,
    ):
        matching_rows.append(
            {
                "rank": rank,
                "candidate_ids": ";".join(
                    cross_colour_candidate_identifier(
                        candidate
                    )
                    for candidate in matching.candidates
                ),
                "total_distance_px": (
                    matching.total_distance
                ),
                "total_score": matching.total_score,
                "maximum_edge_score": (
                    matching.maximum_edge_score
                ),
            }
        )

    write_csv(
        MATCHING_TABLE,
        matching_rows,
        [
            "rank",
            "candidate_ids",
            "total_distance_px",
            "total_score",
            "maximum_edge_score",
        ],
    )

    p03 = load_image(P03_PATH)
    p01 = load_image(P01_PATH)
    p02 = load_image(P02_PATH)

    candidate_paths = []
    candidate_labels = []

    for rank, candidate in enumerate(
        candidates,
        start=1,
    ):
        path = plot_candidate(
            candidate,
            rank,
            segments,
            p03,
            p01,
            p02,
        )

        candidate_paths.append(path)
        candidate_labels.append(
            f"{rank:02d}. "
            f"{cross_colour_candidate_identifier(candidate)}"
        )

        print(f"Wrote {path.relative_to(ROOT)}")

    matching_paths = []
    matching_labels = []

    for rank, matching in enumerate(
        matchings,
        start=1,
    ):
        path = plot_matching(
            matching,
            rank,
            segments,
            p03,
        )

        matching_paths.append(path)
        matching_labels.append(
            f"Matching {rank:02d}: "
            f"score={matching.total_score:.2f}"
        )

        print(f"Wrote {path.relative_to(ROOT)}")

    build_contact_sheet(
        candidate_paths,
        candidate_labels,
        CANDIDATE_SHEET,
        columns=3,
    )

    build_contact_sheet(
        matching_paths,
        matching_labels,
        MATCHING_SHEET,
        columns=2,
    )

    write_report(
        candidates,
        matchings,
        free_endpoints,
    )

    print()
    print("Cross-colour candidates:", len(candidates))
    print("Complete perfect matchings:", len(matchings))
    print(
        "Unreviewed:",
        sum(
            row["status"] == "unreviewed"
            for row in rows
        ),
    )


if __name__ == "__main__":
    main()
