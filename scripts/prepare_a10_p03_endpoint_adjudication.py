#!/usr/bin/env python3
"""Prepare source-image review panels for A10_P03 endpoint candidates."""

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

from meru_geometry.digitization import (
    load_panel_geometry,
)
from meru_geometry.endpoint_review import (
    endpoint_coordinate,
    merge_adjudication_rows,
)


ROOT = Path(__file__).resolve().parents[1]

PANEL_MANIFEST = (
    ROOT
    / "references"
    / "geometric_panel_crop_manifest.csv"
)

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
    / "a10_p03_endpoint_candidates.csv"
)

ADJUDICATION_PATH = (
    ROOT
    / "data"
    / "manual_digitizations"
    / "A10_P03"
    / "endpoint_adjudication.csv"
)

OUTPUT_DIR = (
    ROOT
    / "data"
    / "derived"
    / "source_inspection"
    / "endpoint_review"
    / "A10_P03"
)

CONTACT_SHEET_PATH = (
    ROOT
    / "data"
    / "derived"
    / "source_inspection"
    / "endpoint_review"
    / "a10_p03_endpoint_review_sheet.png"
)

COLOURS = {
    "red": "tab:red",
    "green": "tab:green",
    "blue": "tab:blue",
}

FIELDNAMES = [
    "candidate_id",
    "layer",
    "rank",
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


def load_csv_rows(path: Path) -> list[dict[str, str]]:
    """Read a CSV file or return an empty list when absent."""
    if not path.exists():
        return []

    with path.open(
        newline="",
        encoding="utf-8",
    ) as handle:
        return list(csv.DictReader(handle))


def load_segments() -> dict[str, dict[int, np.ndarray]]:
    """Load digitised segments indexed by layer and one-based segment ID."""
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

            if layer not in COLOURS:
                continue

            segment_id = int(row["segment_id"]) + 1

            raw[layer][segment_id].append(
                (
                    int(row["point_index"]),
                    float(row["panel_x"]),
                    float(row["panel_y"]),
                )
            )

    segments: dict[str, dict[int, np.ndarray]] = {}

    for layer, layer_segments in raw.items():
        segments[layer] = {}

        for segment_id, records in layer_segments.items():
            records.sort(key=lambda record: record[0])

            segments[layer][segment_id] = np.asarray(
                [
                    [record[1], record[2]]
                    for record in records
                ],
                dtype=np.float64,
            )

    return segments


def save_adjudication_rows(
    rows: list[dict[str, object]],
) -> None:
    """Write the tracked manual adjudication table."""
    ADJUDICATION_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with ADJUDICATION_PATH.open(
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
        f"Wrote {ADJUDICATION_PATH.relative_to(ROOT)}"
    )


def draw_all_segments(
    axis: plt.Axes,
    segments: dict[str, dict[int, np.ndarray]],
    highlighted_layer: str,
    highlighted_segments: set[int],
) -> None:
    """Draw every colour trace, highlighting the selected pair."""
    for layer, layer_segments in segments.items():
        for segment_id, points in layer_segments.items():
            highlighted = (
                layer == highlighted_layer
                and segment_id in highlighted_segments
            )

            axis.plot(
                points[:, 0],
                points[:, 1],
                color=COLOURS[layer],
                linewidth=2.6 if highlighted else 0.9,
                alpha=1.0 if highlighted else 0.28,
                marker="o" if highlighted else None,
                markersize=3.0,
            )


def plot_candidate(
    row: dict[str, object],
    image: np.ndarray,
    segments: dict[str, dict[int, np.ndarray]],
) -> Path:
    """Generate a full-panel and close-up review image."""
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
        1,
        2,
        figsize=(12, 5.5),
        constrained_layout=True,
    )

    for axis in axes:
        axis.imshow(
            image,
            origin="upper",
            interpolation="nearest",
        )

        draw_all_segments(
            axis,
            segments,
            highlighted_layer=layer,
            highlighted_segments={
                segment_a_id,
                segment_b_id,
            },
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
            s=65,
            color=COLOURS[layer],
            edgecolors="black",
            linewidths=0.7,
            zorder=10,
        )

        axis.annotate(
            (
                f"S{segment_a_id} "
                f"{row['endpoint_a']}"
            ),
            point_a,
            xytext=(5, -10),
            textcoords="offset points",
            fontsize=8,
        )

        axis.annotate(
            (
                f"S{segment_b_id} "
                f"{row['endpoint_b']}"
            ),
            point_b,
            xytext=(5, 8),
            textcoords="offset points",
            fontsize=8,
        )

        axis.set_aspect("equal")
        axis.set_xticks([])
        axis.set_yticks([])

    axes[0].set_title("Full source panel")

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
    span = maximum - minimum

    margin = max(
        7.0,
        0.18 * float(np.max(span)),
    )

    axes[1].set_xlim(
        minimum[0] - margin,
        maximum[0] + margin,
    )

    axes[1].set_ylim(
        maximum[1] + margin,
        minimum[1] - margin,
    )

    axes[1].set_title("Candidate close-up")

    figure.suptitle(
        f"{row['candidate_id']} — rank {row['rank']}\n"
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
    """Build one local review sheet containing all 15 candidates."""
    columns = 3
    cell_width = 680
    cell_height = 390
    margin = 14
    label_height = 42

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
            f"d={float(row['distance_px']):.2f}px | "
            f"Δθ={float(row['tangent_mismatch_deg']):.1f}°"
        )

        draw.text(
            (
                left + margin,
                top + cell_height - label_height + 10,
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

    CONTACT_SHEET_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    canvas.save(CONTACT_SHEET_PATH)

    print(
        f"Wrote {CONTACT_SHEET_PATH.relative_to(ROOT)}"
    )


def main() -> None:
    """Prepare the initial endpoint-adjudication package."""
    if not CANDIDATE_PATH.exists():
        raise SystemExit(
            "Endpoint-candidate CSV not found. Run "
            "scripts/analyse_a10_p03_trace.py first."
        )

    panel = load_panel_geometry(
        PANEL_MANIFEST,
        "A10_P03",
        repository_root=ROOT,
    )

    with Image.open(panel.local_path) as source:
        source.seek(0)
        image = np.asarray(
            source.convert("RGB")
        )

    candidate_rows = load_csv_rows(
        CANDIDATE_PATH
    )

    existing_rows = load_csv_rows(
        ADJUDICATION_PATH
    )

    adjudication_rows = merge_adjudication_rows(
        candidate_rows,
        existing_rows,
        top_n_per_layer=5,
    )

    save_adjudication_rows(adjudication_rows)

    segments = load_segments()
    image_paths: list[Path] = []

    for row in adjudication_rows:
        output_path = plot_candidate(
            row,
            image,
            segments,
        )

        image_paths.append(output_path)

        print(
            f"Wrote {output_path.relative_to(ROOT)}"
        )

    build_contact_sheet(
        adjudication_rows,
        image_paths,
    )

    print()
    print("Candidates prepared:", len(adjudication_rows))
    print("Accepted:", sum(
        row["status"] == "accepted"
        for row in adjudication_rows
    ))
    print("Rejected:", sum(
        row["status"] == "rejected"
        for row in adjudication_rows
    ))
    print("Ambiguous:", sum(
        row["status"] == "ambiguous"
        for row in adjudication_rows
    ))
    print("Unreviewed:", sum(
        row["status"] == "unreviewed"
        for row in adjudication_rows
    ))


if __name__ == "__main__":
    main()
