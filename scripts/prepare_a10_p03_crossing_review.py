#!/usr/bin/env python3
"""Prepare source panels for manual review of A10_P03 crossings."""

from __future__ import annotations

import csv
import math
from collections import Counter, defaultdict
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageOps

from meru_geometry.crossing_review import (
    merge_crossing_review_rows,
)


ROOT = Path(__file__).resolve().parents[1]

DIGITIZATION_PATH = (
    ROOT
    / "data"
    / "manual_digitizations"
    / "A10_P03"
    / "digitization.csv"
)

CANDIDATE_PATH = (
    ROOT
    / "data"
    / "derived"
    / "a10_p03_crossing_candidates.csv"
)

INVENTORY_PATH = (
    ROOT
    / "data"
    / "manual_digitizations"
    / "A10_P03"
    / "crossing_inventory.csv"
)

SOURCE_PATH = (
    ROOT
    / "data"
    / "derived"
    / "source_inspection"
    / "panels"
    / "A10_P03.png"
)

OUTPUT_DIR = (
    ROOT
    / "data"
    / "derived"
    / "source_inspection"
    / "crossing_review"
    / "A10_P03"
)

SHEET_DIR = (
    ROOT
    / "data"
    / "derived"
    / "source_inspection"
    / "crossing_review"
)

INDEX_PATH = (
    SHEET_DIR
    / "a10_p03_crossing_review_index.md"
)

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
    "status",
    "confidence",
    "event_id",
    "over_layer",
    "over_segment",
    "under_layer",
    "under_segment",
    "visibility",
    "reason_code",
    "notes",
    "reviewed_utc",
]


def load_csv(
    path: Path,
) -> list[dict[str, str]]:
    """Load a CSV table or return an empty list."""
    if not path.exists():
        return []

    with path.open(
        newline="",
        encoding="utf-8",
    ) as handle:
        return list(csv.DictReader(handle))


def load_segments() -> dict[
    tuple[str, int],
    np.ndarray,
]:
    """Load one-based traced centreline segments."""
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

            if layer not in COLOURS:
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


def write_inventory(
    rows: list[dict[str, object]],
) -> None:
    """Write the tracked manual crossing inventory."""
    with INVENTORY_PATH.open(
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

    print(
        f"Wrote {INVENTORY_PATH.relative_to(ROOT)}"
    )


def closest_point(
    points: np.ndarray,
    piece_index: int,
    fraction: float,
) -> np.ndarray:
    """Reconstruct a closest-approach point on one polyline piece."""
    start = points[piece_index]
    end = points[piece_index + 1]

    return start + fraction * (
        end - start
    )


def draw_all_segments(
    axis: plt.Axes,
    segments: dict[
        tuple[str, int],
        np.ndarray,
    ],
    highlighted: set[
        tuple[str, int]
    ] = frozenset(),
) -> None:
    """Draw all traces, emphasizing the selected segment pair."""
    for key, points in segments.items():
        layer, _segment_id = key
        selected = key in highlighted

        axis.plot(
            points[:, 0],
            points[:, 1],
            color=COLOURS[layer],
            linewidth=2.8 if selected else 0.8,
            alpha=1.0 if selected else 0.22,
            marker="o" if selected else None,
            markersize=3.0,
        )


def plot_candidate(
    row: dict[str, object],
    source_image: np.ndarray,
    segments: dict[
        tuple[str, int],
        np.ndarray,
    ],
) -> Path:
    """Create a four-panel review image for one candidate."""
    key_a = (
        str(row["layer_a"]),
        int(row["segment_a"]),
    )

    key_b = (
        str(row["layer_b"]),
        int(row["segment_b"]),
    )

    points_a = segments[key_a]
    points_b = segments[key_b]

    closest_a = closest_point(
        points_a,
        int(row["piece_index_a"]),
        float(row["fraction_a"]),
    )

    closest_b = closest_point(
        points_b,
        int(row["piece_index_b"]),
        float(row["fraction_b"]),
    )

    midpoint = (
        closest_a + closest_b
    ) / 2.0

    margin = max(
        13.0,
        min(
            28.0,
            13.0
            + 2.0
            * float(row["distance_px"]),
        ),
    )

    x_min = midpoint[0] - margin
    x_max = midpoint[0] + margin
    y_min = midpoint[1] - margin
    y_max = midpoint[1] + margin

    figure, axes = plt.subplots(
        2,
        2,
        figsize=(11, 10),
        constrained_layout=True,
    )

    highlighted = {
        key_a,
        key_b,
    }

    axes[0, 0].imshow(source_image)

    draw_all_segments(
        axes[0, 0],
        segments,
        highlighted,
    )

    axes[0, 0].scatter(
        midpoint[0],
        midpoint[1],
        s=80,
        facecolors="white",
        edgecolors="black",
        linewidths=1.2,
        zorder=10,
    )

    axes[0, 0].set_title(
        "Full A10_P03 source panel"
    )

    axes[0, 1].imshow(source_image)

    axes[0, 1].set_xlim(
        x_min,
        x_max,
    )

    axes[0, 1].set_ylim(
        y_max,
        y_min,
    )

    axes[0, 1].set_title(
        "Raw source close-up"
    )

    axes[1, 0].imshow(source_image)

    draw_all_segments(
        axes[1, 0],
        segments,
        highlighted,
    )

    axes[1, 0].plot(
        [closest_a[0], closest_b[0]],
        [closest_a[1], closest_b[1]],
        linestyle="--",
        linewidth=1.8,
        color="black",
    )

    axes[1, 0].scatter(
        closest_a[0],
        closest_a[1],
        s=75,
        color=COLOURS[key_a[0]],
        edgecolors="black",
        linewidths=0.8,
        zorder=10,
    )

    axes[1, 0].scatter(
        closest_b[0],
        closest_b[1],
        s=75,
        color=COLOURS[key_b[0]],
        edgecolors="black",
        linewidths=0.8,
        zorder=10,
    )

    axes[1, 0].annotate(
        (
            f"{key_a[0][0].upper()}"
            f"S{key_a[1]:02d}"
        ),
        closest_a,
        xytext=(5, 6),
        textcoords="offset points",
        fontsize=8,
    )

    axes[1, 0].annotate(
        (
            f"{key_b[0][0].upper()}"
            f"S{key_b[1]:02d}"
        ),
        closest_b,
        xytext=(5, -12),
        textcoords="offset points",
        fontsize=8,
    )

    axes[1, 0].set_xlim(
        x_min,
        x_max,
    )

    axes[1, 0].set_ylim(
        y_max,
        y_min,
    )

    axes[1, 0].set_title(
        "Source with candidate traces"
    )

    draw_all_segments(
        axes[1, 1],
        {
            key_a: points_a,
            key_b: points_b,
        },
        highlighted,
    )

    axes[1, 1].plot(
        [closest_a[0], closest_b[0]],
        [closest_a[1], closest_b[1]],
        linestyle="--",
        linewidth=1.8,
        color="black",
    )

    axes[1, 1].scatter(
        [closest_a[0], closest_b[0]],
        [closest_a[1], closest_b[1]],
        s=80,
        facecolors="white",
        edgecolors="black",
        linewidths=1.2,
        zorder=10,
    )

    axes[1, 1].set_xlim(
        x_min,
        x_max,
    )

    axes[1, 1].set_ylim(
        y_max,
        y_min,
    )

    axes[1, 1].grid(
        True,
        alpha=0.2,
    )

    axes[1, 1].set_title(
        "Trace-only geometric diagnostic"
    )

    for axis in axes.flat:
        axis.set_aspect("equal")
        axis.set_xticks([])
        axis.set_yticks([])

    figure.suptitle(
        f"Rank {int(row['rank']):02d}: "
        f"{row['candidate_id']}\n"
        f"distance={float(row['distance_px']):.3f} px · "
        f"angle={float(row['crossing_angle_deg']):.2f}° · "
        f"status={row['status']}"
    )

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_path = (
        OUTPUT_DIR
        / (
            f"{int(row['rank']):02d}_"
            f"{row['candidate_id']}.png"
        )
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
    sheet_number: int,
) -> Path:
    """Build one eleven-candidate review sheet."""
    columns = 3
    cell_width = 650
    cell_height = 520
    label_height = 42
    margin = 12

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

        canvas.paste(
            thumbnail,
            (
                image_x,
                top + margin,
            ),
        )

        label = (
            f"{int(row['rank']):02d}. "
            f"{row['candidate_id']} | "
            f"d={float(row['distance_px']):.2f}px | "
            f"θ={float(row['crossing_angle_deg']):.1f}°"
        )

        draw.text(
            (
                left + margin,
                top + cell_height
                - label_height
                + 9,
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

    sheet_path = (
        SHEET_DIR
        / (
            "a10_p03_crossing_review_"
            f"sheet_{sheet_number:02d}.png"
        )
    )

    sheet_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    canvas.save(sheet_path)

    print(
        f"Wrote {sheet_path.relative_to(ROOT)}"
    )

    return sheet_path


def write_index(
    rows: list[dict[str, object]],
    paths: list[Path],
) -> None:
    """Write a local Markdown index for the review images."""
    lines = [
        "# A10_P03 Crossing Review Index",
        "",
        "The 33 geometric candidates may contain multiple rows for "
        "one physical crossing event.",
        "",
        "| Rank | Candidate | Distance | Angle | Image |",
        "|---:|---|---:|---:|---|",
    ]

    for row, path in zip(
        rows,
        paths,
        strict=True,
    ):
        relative = path.relative_to(
            INDEX_PATH.parent
        )

        lines.append(
            f"| {int(row['rank'])} | "
            f"`{row['candidate_id']}` | "
            f"{float(row['distance_px']):.3f} px | "
            f"{float(row['crossing_angle_deg']):.2f}° | "
            f"[open]({relative.as_posix()}) |"
        )

    INDEX_PATH.write_text(
        "\n".join(lines) + "\n",
        encoding="utf-8",
    )

    print(
        f"Wrote {INDEX_PATH.relative_to(ROOT)}"
    )


def main() -> None:
    """Prepare the complete 33-candidate crossing-review package."""
    if not CANDIDATE_PATH.exists():
        raise SystemExit(
            "Crossing-candidate CSV is missing. Run "
            "scripts/find_a10_p03_crossing_candidates.py first."
        )

    if not SOURCE_PATH.exists():
        raise SystemExit(
            f"Source panel is missing: "
            f"{SOURCE_PATH.relative_to(ROOT)}"
        )

    candidate_rows = load_csv(
        CANDIDATE_PATH
    )

    existing_rows = load_csv(
        INVENTORY_PATH
    )

    rows = merge_crossing_review_rows(
        candidate_rows,
        existing_rows,
    )

    if len(rows) != 33:
        raise RuntimeError(
            f"Expected the frozen 33-candidate census; "
            f"found {len(rows)} candidates."
        )

    write_inventory(rows)

    segments = load_segments()

    with Image.open(SOURCE_PATH) as source:
        source_image = np.asarray(
            source.convert("RGB")
        )

    image_paths: list[Path] = []

    for row in rows:
        path = plot_candidate(
            row,
            source_image,
            segments,
        )

        image_paths.append(path)

        print(
            f"Wrote {path.relative_to(ROOT)}"
        )

    for sheet_index, start in enumerate(
        range(0, len(rows), 11),
        start=1,
    ):
        build_contact_sheet(
            rows[start:start + 11],
            image_paths[start:start + 11],
            sheet_index,
        )

    write_index(
        rows,
        image_paths,
    )

    counts = Counter(
        str(row["status"])
        for row in rows
    )

    print()
    print("Crossing-review candidates:", len(rows))
    print("Statuses:", dict(counts))


if __name__ == "__main__":
    main()
