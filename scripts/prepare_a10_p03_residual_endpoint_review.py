#!/usr/bin/env python3
"""Prepare graph-constrained review panels for unresolved A10 endpoints."""

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
from meru_geometry.endpoint_review import (
    MANUAL_FIELDS,
    validate_adjudication_rows,
)
from meru_geometry.residual_connectivity import (
    ResidualEndpointCandidate,
    best_merge_per_component_pair,
    closure_candidate,
    endpoint_coordinate,
    rank_free_endpoint_pairs,
    residual_candidate_identifier,
)


ROOT = Path(__file__).resolve().parents[1]

DIGITIZATION_PATH = (
    ROOT
    / "data"
    / "manual_digitizations"
    / "A10_P03"
    / "digitization.csv"
)

ADJUDICATION_PATH = (
    ROOT
    / "data"
    / "manual_digitizations"
    / "A10_P03"
    / "endpoint_adjudication.csv"
)

OUTPUT_TABLE = (
    ROOT
    / "data"
    / "manual_digitizations"
    / "A10_P03"
    / "residual_endpoint_review.csv"
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

OUTPUT_DIR = (
    ROOT
    / "data"
    / "derived"
    / "source_inspection"
    / "residual_endpoint_review"
    / "A10_P03"
)

CONTACT_SHEET = (
    ROOT
    / "data"
    / "derived"
    / "source_inspection"
    / "residual_endpoint_review"
    / "a10_p03_residual_endpoint_review_sheet.png"
)

LAYERS = ("red", "green", "blue")

COLOURS = {
    "red": "tab:red",
    "green": "tab:green",
    "blue": "tab:blue",
}

FIELDNAMES = [
    "candidate_id",
    "layer",
    "candidate_type",
    "rank",
    "component_a",
    "component_b",
    "segment_a",
    "endpoint_a",
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
    raw: dict[
        str,
        dict[int, list[tuple[int, float, float]]],
    ] = defaultdict(lambda: defaultdict(list))

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


def load_accepted() -> list[dict[str, str]]:
    """Load the 15 accepted first-stage endpoint connections."""
    with ADJUDICATION_PATH.open(
        newline="",
        encoding="utf-8",
    ) as handle:
        rows = list(csv.DictReader(handle))

    accepted = [
        row
        for row in rows
        if row["status"] == "accepted"
    ]

    if len(accepted) != 15:
        raise RuntimeError(
            f"Expected 15 accepted connections; found {len(accepted)}."
        )

    return accepted


def load_existing() -> dict[str, dict[str, str]]:
    """Load existing residual decisions by candidate ID."""
    if not OUTPUT_TABLE.exists():
        return {}

    with OUTPUT_TABLE.open(
        newline="",
        encoding="utf-8",
    ) as handle:
        return {
            row["candidate_id"]: row
            for row in csv.DictReader(handle)
        }


def select_candidates(
    segments: dict[str, dict[int, np.ndarray]],
    accepted: list[dict[str, str]],
) -> list[ResidualEndpointCandidate]:
    """Select the frozen 20-candidate second-stage review set."""
    components = {
        layer: build_endpoint_connectivity(
            segments[layer].keys(),
            [
                row
                for row in accepted
                if row["layer"] == layer
            ],
        )
        for layer in LAYERS
    }

    red = list(
        rank_free_endpoint_pairs(
            "red",
            segments["red"],
            components["red"],
            include_same_component=False,
        )
    )

    green_all = rank_free_endpoint_pairs(
        "green",
        segments["green"],
        components["green"],
        include_same_component=False,
    )

    green = list(
        best_merge_per_component_pair(
            green_all
        )
    )

    blue = [
        closure_candidate(
            "blue",
            segments["blue"],
            components["blue"][0],
            component_id=1,
        )
    ]

    if len(red) != 4:
        raise RuntimeError(
            f"Expected 4 red candidates; found {len(red)}."
        )

    if len(green) != 15:
        raise RuntimeError(
            f"Expected 15 green candidates; found {len(green)}."
        )

    return red + green + blue


def build_rows(
    candidates: list[ResidualEndpointCandidate],
) -> list[dict[str, object]]:
    """Create review rows while preserving manual fields."""
    existing = load_existing()
    layer_rank = defaultdict(int)
    rows: list[dict[str, object]] = []

    for candidate in candidates:
        layer_rank[candidate.layer] += 1

        identifier = residual_candidate_identifier(
            candidate
        )

        row: dict[str, object] = {
            "candidate_id": identifier,
            "layer": candidate.layer,
            "candidate_type": candidate.candidate_type,
            "rank": layer_rank[candidate.layer],
            "component_a": candidate.component_a,
            "component_b": candidate.component_b,
            "segment_a": candidate.segment_a,
            "endpoint_a": candidate.endpoint_a,
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

    validate_adjudication_rows(rows)
    return rows


def write_rows(
    rows: list[dict[str, object]],
) -> None:
    """Write the tracked residual-review table."""
    with OUTPUT_TABLE.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=FIELDNAMES,
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {OUTPUT_TABLE.relative_to(ROOT)}")


def load_image(path: Path) -> np.ndarray:
    """Load a local source panel as RGB."""
    if not path.exists():
        raise RuntimeError(
            f"Missing panel crop: {path.relative_to(ROOT)}"
        )

    with Image.open(path) as source:
        return np.asarray(
            source.convert("RGB")
        )


def draw_segments(
    axis: plt.Axes,
    segments: dict[str, dict[int, np.ndarray]],
    layer: str,
    highlighted: set[int],
) -> None:
    """Draw all source traces with one selected endpoint pair highlighted."""
    for trace_layer, layer_segments in segments.items():
        for segment_id, points in layer_segments.items():
            is_highlighted = (
                trace_layer == layer
                and segment_id in highlighted
            )

            axis.plot(
                points[:, 0],
                points[:, 1],
                color=COLOURS[trace_layer],
                linewidth=2.7 if is_highlighted else 0.8,
                alpha=1.0 if is_highlighted else 0.25,
                marker="o" if is_highlighted else None,
                markersize=3.0,
            )


def plot_candidate(
    row: dict[str, object],
    segments: dict[str, dict[int, np.ndarray]],
    p03: np.ndarray,
    p01: np.ndarray,
    p02: np.ndarray,
) -> Path:
    """Generate a four-panel residual-candidate review image."""
    layer = str(row["layer"])
    segment_a_id = int(row["segment_a"])
    segment_b_id = int(row["segment_b"])

    segment_a = segments[layer][segment_a_id]
    segment_b = segments[layer][segment_b_id]

    point_a = endpoint_coordinate(
        segment_a,
        str(row["endpoint_a"]),
    )

    point_b = endpoint_coordinate(
        segment_b,
        str(row["endpoint_b"]),
    )

    figure, axes = plt.subplots(
        2,
        2,
        figsize=(12, 10),
        constrained_layout=True,
    )

    for axis in (axes[0, 0], axes[0, 1]):
        axis.imshow(
            p03,
            origin="upper",
            interpolation="nearest",
        )

        draw_segments(
            axis,
            segments,
            layer,
            {segment_a_id, segment_b_id},
        )

        axis.plot(
            [point_a[0], point_b[0]],
            [point_a[1], point_b[1]],
            linestyle="--",
            linewidth=1.8,
            color=COLOURS[layer],
        )

        axis.scatter(
            [point_a[0], point_b[0]],
            [point_a[1], point_b[1]],
            s=70,
            color=COLOURS[layer],
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
    axes[1, 0].set_title(
        "A10_P01 ring-to-dimple transition"
    )
    axes[1, 0].set_axis_off()

    axes[1, 1].imshow(p02)
    axes[1, 1].set_title(
        "A10_P02 apparent winding-zero flip"
    )
    axes[1, 1].set_axis_off()

    figure.suptitle(
        f"{row['candidate_id']} — "
        f"{row['candidate_type']}\n"
        f"distance={float(row['distance_px']):.3f} px; "
        f"tangent mismatch="
        f"{float(row['tangent_mismatch_deg']):.2f}°; "
        f"status={row['status']}"
    )

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_path = (
        OUTPUT_DIR
        / f"{row['candidate_id']}.png"
    )

    figure.savefig(
        output_path,
        dpi=190,
    )
    plt.close(figure)

    return output_path


def build_contact_sheet(
    rows: list[dict[str, object]],
    image_paths: list[Path],
) -> None:
    """Build a local contact sheet for all 20 candidates."""
    columns = 4
    cell_width = 610
    cell_height = 500
    margin = 12
    label_height = 38

    row_count = math.ceil(
        len(image_paths) / columns
    )

    canvas = Image.new(
        "RGB",
        (
            columns * cell_width,
            row_count * cell_height,
        ),
        "white",
    )

    draw = ImageDraw.Draw(canvas)
    font = ImageFont.load_default()

    for index, (row, path) in enumerate(
        zip(rows, image_paths, strict=True)
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

        image_y = top + margin

        canvas.paste(
            thumbnail,
            (image_x, image_y),
        )

        label = (
            f"{row['candidate_id']} | "
            f"d={float(row['distance_px']):.1f}px | "
            f"Δθ={float(row['tangent_mismatch_deg']):.1f}°"
        )

        draw.text(
            (
                left + margin,
                top + cell_height - label_height + 8,
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

    CONTACT_SHEET.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    canvas.save(CONTACT_SHEET)

    print(f"Wrote {CONTACT_SHEET.relative_to(ROOT)}")


def main() -> None:
    """Create the complete graph-constrained residual review set."""
    segments = load_segments()
    accepted = load_accepted()

    candidates = select_candidates(
        segments,
        accepted,
    )

    rows = build_rows(candidates)
    write_rows(rows)

    p03 = load_image(P03_PATH)
    p01 = load_image(P01_PATH)
    p02 = load_image(P02_PATH)

    image_paths = []

    for row in rows:
        path = plot_candidate(
            row,
            segments,
            p03,
            p01,
            p02,
        )

        image_paths.append(path)
        print(f"Wrote {path.relative_to(ROOT)}")

    build_contact_sheet(
        rows,
        image_paths,
    )

    print()
    print("Candidates prepared:", len(rows))

    for layer in LAYERS:
        layer_rows = [
            row
            for row in rows
            if row["layer"] == layer
        ]

        print(
            f"{layer}:",
            len(layer_rows),
            "candidates",
        )

    print(
        "Unreviewed:",
        sum(
            row["status"] == "unreviewed"
            for row in rows
        ),
    )


if __name__ == "__main__":
    main()
