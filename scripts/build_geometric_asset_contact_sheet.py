#!/usr/bin/env python3
"""Build a local contact sheet for visual source inspection."""

from __future__ import annotations

import csv
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = (
    ROOT
    / "references"
    / "geometric_asset_snapshot_manifest.csv"
)
OUTPUT_PATH = (
    ROOT
    / "data"
    / "derived"
    / "source_inspection"
    / "geometric_asset_contact_sheet.png"
)

COLUMNS = 2
CELL_WIDTH = 680
CELL_HEIGHT = 480
IMAGE_MARGIN = 24
LABEL_HEIGHT = 78


def main() -> None:
    """Create a labelled contact sheet from successful snapshots."""
    with MANIFEST_PATH.open(
        newline="",
        encoding="utf-8",
    ) as handle:
        rows = [
            row
            for row in csv.DictReader(handle)
            if row["status"] == "success"
        ]

    if not rows:
        raise SystemExit("No successful assets found in manifest.")

    row_count = math.ceil(len(rows) / COLUMNS)

    canvas = Image.new(
        "RGB",
        (
            COLUMNS * CELL_WIDTH,
            row_count * CELL_HEIGHT,
        ),
        "white",
    )

    draw = ImageDraw.Draw(canvas)
    font = ImageFont.load_default()

    for index, row in enumerate(rows):
        grid_row = index // COLUMNS
        grid_column = index % COLUMNS

        left = grid_column * CELL_WIDTH
        top = grid_row * CELL_HEIGHT

        source_path = ROOT / row["local_path"]

        with Image.open(source_path) as source:
            source.seek(0)
            image = source.convert("RGB")

        image_box = (
            CELL_WIDTH - 2 * IMAGE_MARGIN,
            CELL_HEIGHT - LABEL_HEIGHT - 2 * IMAGE_MARGIN,
        )

        fitted = ImageOps.contain(image, image_box)

        image_x = left + (CELL_WIDTH - fitted.width) // 2
        image_y = top + IMAGE_MARGIN

        canvas.paste(fitted, (image_x, image_y))

        label_y = top + CELL_HEIGHT - LABEL_HEIGHT + 8

        label = (
            f"{row['asset_id']} — {row['title']}\n"
            f"{row['width_px']}×{row['height_px']} px; "
            f"{row['format']}; frames={row['frames']}"
        )

        draw.multiline_text(
            (left + IMAGE_MARGIN, label_y),
            label,
            fill="black",
            font=font,
            spacing=4,
        )

        draw.rectangle(
            (
                left,
                top,
                left + CELL_WIDTH - 1,
                top + CELL_HEIGHT - 1,
            ),
            outline="grey",
            width=1,
        )

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(OUTPUT_PATH)

    print(f"Wrote {OUTPUT_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
