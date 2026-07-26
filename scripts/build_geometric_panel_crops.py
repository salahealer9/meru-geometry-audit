#!/usr/bin/env python3
"""Build reproducible local crops of selected Meru source panels.

The original and cropped source images remain local and excluded from Git.
A committed manifest records the crop bounds, output dimensions, and SHA-256
digests.
"""

from __future__ import annotations

import csv
import hashlib
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps


ROOT = Path(__file__).resolve().parents[1]

ASSET_MANIFEST = (
    ROOT
    / "references"
    / "geometric_asset_snapshot_manifest.csv"
)

PANEL_REGISTER = (
    ROOT
    / "references"
    / "geometric_asset_panels.csv"
)

OUTPUT_DIR = (
    ROOT
    / "data"
    / "derived"
    / "source_inspection"
    / "panels"
)

OUTPUT_MANIFEST = (
    ROOT
    / "references"
    / "geometric_panel_crop_manifest.csv"
)

CONTACT_SHEET = (
    ROOT
    / "data"
    / "derived"
    / "source_inspection"
    / "geometric_panel_contact_sheet.png"
)

CONTACT_COLUMNS = 2
CONTACT_CELL_WIDTH = 760
CONTACT_CELL_HEIGHT = 520
CONTACT_MARGIN = 24
CONTACT_LABEL_HEIGHT = 86


def sha256_file(path: Path) -> str:
    """Return a file's hexadecimal SHA-256 digest."""
    digest = hashlib.sha256()

    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)

    return digest.hexdigest()


def load_assets() -> dict[str, dict[str, str]]:
    """Return successful asset-manifest rows indexed by asset ID."""
    with ASSET_MANIFEST.open(
        newline="",
        encoding="utf-8",
    ) as handle:
        rows = list(csv.DictReader(handle))

    assets = {
        row["asset_id"]: row
        for row in rows
        if row["status"] == "success"
    }

    if not assets:
        raise RuntimeError("No successful source assets are available.")

    return assets


def load_panels() -> list[dict[str, str]]:
    """Read the registered source panels."""
    with PANEL_REGISTER.open(
        newline="",
        encoding="utf-8",
    ) as handle:
        rows = list(csv.DictReader(handle))

    if not rows:
        raise RuntimeError("The panel register is empty.")

    return rows


def validate_bounds(
    panel: dict[str, str],
    image_width: int,
    image_height: int,
) -> tuple[int, int, int, int]:
    """Validate and return a panel crop rectangle."""
    x0 = int(panel["x0"])
    y0 = int(panel["y0"])
    x1 = int(panel["x1"])
    y1 = int(panel["y1"])

    if not (0 <= x0 < x1 <= image_width):
        raise ValueError(
            f'{panel["panel_id"]}: invalid horizontal bounds '
            f"({x0}, {x1}) for width {image_width}."
        )

    if not (0 <= y0 < y1 <= image_height):
        raise ValueError(
            f'{panel["panel_id"]}: invalid vertical bounds '
            f"({y0}, {y1}) for height {image_height}."
        )

    return x0, y0, x1, y1


def build_contact_sheet(
    generated_rows: list[dict[str, str | int]],
) -> None:
    """Build a labelled local contact sheet of panel crops."""
    row_count = math.ceil(
        len(generated_rows) / CONTACT_COLUMNS
    )

    canvas = Image.new(
        "RGB",
        (
            CONTACT_COLUMNS * CONTACT_CELL_WIDTH,
            row_count * CONTACT_CELL_HEIGHT,
        ),
        "white",
    )

    draw = ImageDraw.Draw(canvas)
    font = ImageFont.load_default()

    for index, row in enumerate(generated_rows):
        grid_row = index // CONTACT_COLUMNS
        grid_column = index % CONTACT_COLUMNS

        left = grid_column * CONTACT_CELL_WIDTH
        top = grid_row * CONTACT_CELL_HEIGHT

        crop_path = ROOT / str(row["local_path"])

        with Image.open(crop_path) as source:
            image = source.convert("RGB")

        available_size = (
            CONTACT_CELL_WIDTH - 2 * CONTACT_MARGIN,
            CONTACT_CELL_HEIGHT
            - CONTACT_LABEL_HEIGHT
            - 2 * CONTACT_MARGIN,
        )

        fitted = ImageOps.contain(
            image,
            available_size,
            method=Image.Resampling.LANCZOS,
        )

        image_x = (
            left
            + (CONTACT_CELL_WIDTH - fitted.width) // 2
        )

        image_y = top + CONTACT_MARGIN

        canvas.paste(
            fitted,
            (image_x, image_y),
        )

        label_y = (
            top
            + CONTACT_CELL_HEIGHT
            - CONTACT_LABEL_HEIGHT
            + 8
        )

        label = (
            f'{row["panel_id"]} — {row["title"]}\n'
            f'asset={row["asset_id"]}; '
            f'crop=({row["x0"]},{row["y0"]})–'
            f'({row["x1"]},{row["y1"]}); '
            f'{row["width_px"]}×{row["height_px"]} px'
        )

        draw.multiline_text(
            (left + CONTACT_MARGIN, label_y),
            label,
            fill="black",
            font=font,
            spacing=4,
        )

        draw.rectangle(
            (
                left,
                top,
                left + CONTACT_CELL_WIDTH - 1,
                top + CONTACT_CELL_HEIGHT - 1,
            ),
            outline="grey",
            width=1,
        )

    CONTACT_SHEET.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    canvas.save(CONTACT_SHEET)

    print(
        f"Wrote {CONTACT_SHEET.relative_to(ROOT)}"
    )


def main() -> None:
    """Create all registered crops and their reproducibility manifest."""
    assets = load_assets()
    panels = load_panels()

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    generated_rows: list[dict[str, str | int]] = []

    for panel in panels:
        panel_id = panel["panel_id"]
        asset_id = panel["asset_id"]

        if asset_id not in assets:
            raise RuntimeError(
                f"{panel_id}: source asset {asset_id} "
                "is unavailable."
            )

        asset = assets[asset_id]
        source_path = ROOT / asset["local_path"]

        with Image.open(source_path) as source:
            source.seek(0)
            source_rgb = source.convert("RGB")

        x0, y0, x1, y1 = validate_bounds(
            panel,
            source_rgb.width,
            source_rgb.height,
        )

        cropped = source_rgb.crop(
            (x0, y0, x1, y1)
        )

        output_path = OUTPUT_DIR / f"{panel_id}.png"
        cropped.save(output_path)

        row: dict[str, str | int] = {
            "panel_id": panel_id,
            "asset_id": asset_id,
            "title": panel["title"],
            "priority": int(panel["priority"]),
            "research_role": panel["research_role"],
            "source_sha256": asset["sha256"],
            "x0": x0,
            "y0": y0,
            "x1": x1,
            "y1": y1,
            "width_px": cropped.width,
            "height_px": cropped.height,
            "sha256": sha256_file(output_path),
            "local_path": (
                output_path.relative_to(ROOT).as_posix()
            ),
        }

        generated_rows.append(row)

        print(
            f"Wrote {output_path.relative_to(ROOT)} "
            f"({cropped.width}x{cropped.height})"
        )

    fieldnames = [
        "panel_id",
        "asset_id",
        "title",
        "priority",
        "research_role",
        "source_sha256",
        "x0",
        "y0",
        "x1",
        "y1",
        "width_px",
        "height_px",
        "sha256",
        "local_path",
    ]

    with OUTPUT_MANIFEST.open(
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
        writer.writerows(generated_rows)

    print(
        f"Wrote {OUTPUT_MANIFEST.relative_to(ROOT)}"
    )

    build_contact_sheet(generated_rows)


if __name__ == "__main__":
    main()
