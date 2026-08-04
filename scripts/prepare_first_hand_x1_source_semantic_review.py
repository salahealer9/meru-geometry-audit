#!/usr/bin/env python3
"""Prepare neutral source-review images for the First Hand X1 semantic audit.

This script performs no geometric fitting.

It uses only:
- the frozen prepared page-7 spherical-projection crop;
- frozen X1 pass-1 samples;
- the sealed QC-corrected X1 pass-2 samples.

Outputs are source-only crops and neutral point/segment-ID overlays.
No fitted circle, predicted curve, scaffold, radial guide, projective map,
or construction angle is drawn.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import shutil
from collections import defaultdict
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]

SOURCE_IMAGE = (
    ROOT
    / "data"
    / "source_snapshots"
    / "first_hand_arm_of_god"
    / "prepared"
    / "aog_p07_spherical_projection.png"
)

CROP_MANIFEST = (
    ROOT
    / "data"
    / "source_manifests"
    / "first_hand_arm_of_god"
    / "diagram_crop_manifest.csv"
)

PASS1_CSV = (
    ROOT
    / "data"
    / "derived"
    / "first_hand_arm_of_god"
    / "great_circle_segments_pass1.csv"
)

PASS2_QC_CSV = (
    ROOT
    / "data"
    / "derived"
    / "first_hand_arm_of_god"
    / "qc"
    / "great_circle_segments_pass2_qc.csv"
)

RAW_SEAL = (
    ROOT
    / "data"
    / "derived"
    / "first_hand_arm_of_god"
    / "great_circle_segment_passes.sha256"
)

QC_SEAL = (
    ROOT
    / "data"
    / "derived"
    / "first_hand_arm_of_god"
    / "qc"
    / "great_circle_segments_pass2_qc.sha256"
)

PROTOCOL = (
    ROOT
    / "docs"
    / "first_hand_x1_source_semantic_trace_audit_protocol.md"
)

OUTPUT_DIR = (
    ROOT
    / "data"
    / "derived"
    / "first_hand_arm_of_god"
    / "source_semantic_review"
    / "x1"
)

INVENTORY_CSV = OUTPUT_DIR / "x1_segment_inventory.csv"
OUTPUT_MANIFEST = OUTPUT_DIR / "x1_source_review_manifest.json"

X1_ID = "AOG-LM-P07-GC-X1"
CROP_ID = "AOG_P07_SPHERICAL_PROJECTION"

# Broad source-semantic region, intentionally not fitted to a theoretical curve.
# It contains the right side of the spherical panel and its printed annotations.
LABEL_REGION_FRACTIONS = (
    0.43,   # left
    0.04,   # top
    1.00,   # right
    0.78,   # bottom
)

SEGMENT_PADDING_PX = 100


def sha256_path(path: Path) -> str:
    digest = hashlib.sha256()

    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)

    return digest.hexdigest()


def verify_sha256sum_manifest(path: Path) -> dict[str, str]:
    if not path.exists():
        raise RuntimeError(f"Missing checksum manifest: {path}")

    result: dict[str, str] = {}

    for raw in path.read_text(encoding="utf-8").splitlines():
        raw = raw.strip()

        if not raw:
            continue

        parts = raw.split()

        if len(parts) < 2:
            raise RuntimeError(f"Malformed checksum line: {raw!r}")

        expected = parts[0]
        relative = parts[-1].lstrip("*")
        target = ROOT / relative

        if not target.exists():
            raise RuntimeError(f"Sealed file missing: {relative}")

        actual = sha256_path(target)

        if actual != expected:
            raise RuntimeError(
                f"SHA-256 mismatch for {relative}: "
                f"expected {expected}, got {actual}"
            )

        result[relative] = expected

    return result


def read_crop_manifest() -> dict[str, str]:
    with CROP_MANIFEST.open(
        newline="",
        encoding="utf-8",
    ) as handle:
        rows = list(csv.DictReader(handle))

    matches = [
        row
        for row in rows
        if row["crop_id"] == CROP_ID
    ]

    if len(matches) != 1:
        raise RuntimeError(
            f"Expected one manifest row for {CROP_ID}; "
            f"found {len(matches)}."
        )

    return matches[0]


def read_x1_rows(
    path: Path,
    expected_pass: int,
) -> list[dict[str, str]]:
    with path.open(
        newline="",
        encoding="utf-8",
    ) as handle:
        rows = [
            row
            for row in csv.DictReader(handle)
            if row["landmark_id"] == X1_ID
        ]

    if not rows:
        raise RuntimeError(f"No X1 rows in {path}")

    if {
        int(row["pass_number"])
        for row in rows
    } != {expected_pass}:
        raise RuntimeError(
            f"Unexpected pass identity in {path}"
        )

    if {
        row["crop_id"]
        for row in rows
    } != {CROP_ID}:
        raise RuntimeError(
            f"Unexpected crop identity in {path}"
        )

    return rows


def verify_inputs() -> dict[str, Any]:
    if not PROTOCOL.exists():
        raise RuntimeError(
            f"Missing semantic-audit protocol: {PROTOCOL}"
        )

    raw_seal = verify_sha256sum_manifest(RAW_SEAL)
    qc_seal = verify_sha256sum_manifest(QC_SEAL)

    manifest = read_crop_manifest()

    expected_image_sha = manifest["file_sha256"]
    actual_image_sha = sha256_path(SOURCE_IMAGE)

    if actual_image_sha != expected_image_sha:
        raise RuntimeError(
            "Prepared source image differs from frozen crop manifest."
        )

    pass1_relative = str(PASS1_CSV.relative_to(ROOT))
    pass2_qc_relative = str(PASS2_QC_CSV.relative_to(ROOT))

    if pass1_relative not in raw_seal:
        raise RuntimeError(
            "Frozen pass-1 CSV absent from raw acquisition seal."
        )

    if pass2_qc_relative not in qc_seal:
        raise RuntimeError(
            "QC pass-2 CSV absent from QC seal."
        )

    pass1 = read_x1_rows(PASS1_CSV, 1)
    pass2 = read_x1_rows(PASS2_QC_CSV, 2)

    for rows, label in (
        (pass1, "pass1"),
        (pass2, "pass2_qc"),
    ):
        crop_file_hashes = {
            row["crop_file_sha256"]
            for row in rows
        }

        crop_pixel_hashes = {
            row["crop_pixel_sha256"]
            for row in rows
        }

        if crop_file_hashes != {
            manifest["file_sha256"]
        }:
            raise RuntimeError(
                f"{label} uses unexpected crop-file hash."
            )

        if crop_pixel_hashes != {
            manifest["pixel_sha256"]
        }:
            raise RuntimeError(
                f"{label} uses unexpected crop-pixel hash."
            )

    return {
        "manifest": manifest,
        "pass1": pass1,
        "pass2_qc": pass2,
        "source_sha256": actual_image_sha,
        "protocol_sha256": sha256_path(PROTOCOL),
        "pass1_sha256": sha256_path(PASS1_CSV),
        "pass2_qc_sha256": sha256_path(PASS2_QC_CSV),
    }


def point(row: dict[str, str]) -> tuple[float, float]:
    return (
        float(row["x_px"]),
        float(row["y_px"]),
    )


def grouped_segments(
    rows: list[dict[str, str]],
) -> dict[str, list[dict[str, str]]]:
    result: dict[
        str,
        list[dict[str, str]],
    ] = defaultdict(list)

    for row in rows:
        result[row["segment_id"]].append(row)

    for segment_rows in result.values():
        segment_rows.sort(
            key=lambda row: int(row["sequence_index"])
        )

    return dict(sorted(result.items()))


def bounding_box(
    rows: list[dict[str, str]],
    width: int,
    height: int,
    padding: int,
) -> tuple[int, int, int, int]:
    xs = [
        float(row["x_px"])
        for row in rows
    ]

    ys = [
        float(row["y_px"])
        for row in rows
    ]

    left = max(
        0,
        int(min(xs)) - padding,
    )

    top = max(
        0,
        int(min(ys)) - padding,
    )

    right = min(
        width,
        int(max(xs)) + padding + 1,
    )

    bottom = min(
        height,
        int(max(ys)) + padding + 1,
    )

    return (
        left,
        top,
        right,
        bottom,
    )


def draw_marker(
    draw: ImageDraw.ImageDraw,
    x: float,
    y: float,
    pass_number: int,
) -> None:
    """Draw neutral point markers without connecting samples."""

    radius = 4

    if pass_number == 1:
        # Hollow circle.
        draw.ellipse(
            (
                x - radius,
                y - radius,
                x + radius,
                y + radius,
            ),
            outline=(220, 40, 40),
            width=2,
        )
    else:
        # Cross.
        draw.line(
            (
                x - radius,
                y,
                x + radius,
                y,
            ),
            fill=(20, 120, 220),
            width=2,
        )

        draw.line(
            (
                x,
                y - radius,
                x,
                y + radius,
            ),
            fill=(20, 120, 220),
            width=2,
        )


def draw_rows(
    image: Image.Image,
    rows: list[dict[str, str]],
    pass_number: int,
    offset_x: int = 0,
    offset_y: int = 0,
) -> None:
    draw = ImageDraw.Draw(image)

    for row in rows:
        x, y = point(row)

        draw_marker(
            draw,
            x - offset_x,
            y - offset_y,
            pass_number,
        )


def draw_segment_labels(
    image: Image.Image,
    rows_by_pass: dict[
        int,
        dict[str, list[dict[str, str]]],
    ],
    offset_x: int = 0,
    offset_y: int = 0,
) -> None:
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()

    all_ids = sorted(
        set(rows_by_pass[1])
        | set(rows_by_pass[2])
    )

    for segment_id in all_ids:
        candidates = []

        for pass_number in (1, 2):
            rows = rows_by_pass[
                pass_number
            ].get(
                segment_id,
                [],
            )

            if rows:
                candidates.append(
                    point(rows[0])
                )

        if not candidates:
            continue

        x = sum(
            item[0]
            for item in candidates
        ) / len(candidates)

        y = sum(
            item[1]
            for item in candidates
        ) / len(candidates)

        draw.rectangle(
            (
                x - offset_x + 6,
                y - offset_y - 13,
                x - offset_x + 42,
                y - offset_y + 2,
            ),
            fill=(255, 255, 255),
        )

        draw.text(
            (
                x - offset_x + 8,
                y - offset_y - 12,
            ),
            segment_id,
            fill=(0, 0, 0),
            font=font,
        )


def write_inventory(
    pass1: list[dict[str, str]],
    pass2: list[dict[str, str]],
) -> list[dict[str, Any]]:
    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    rows_out: list[
        dict[str, Any]
    ] = []

    for pass_number, rows in (
        (1, pass1),
        (2, pass2),
    ):
        groups = grouped_segments(rows)

        for segment_id, segment_rows in groups.items():
            xs = [
                float(row["x_px"])
                for row in segment_rows
            ]

            ys = [
                float(row["y_px"])
                for row in segment_rows
            ]

            notes = sorted(
                {
                    row["operator_note"]
                    for row in segment_rows
                    if row["operator_note"].strip()
                }
            )

            rows_out.append(
                {
                    "landmark_id": X1_ID,
                    "pass_number": pass_number,
                    "segment_id": segment_id,
                    "sample_count": len(segment_rows),
                    "min_x_px": min(xs),
                    "max_x_px": max(xs),
                    "min_y_px": min(ys),
                    "max_y_px": max(ys),
                    "operator_notes": " | ".join(notes),
                }
            )

    fieldnames = [
        "landmark_id",
        "pass_number",
        "segment_id",
        "sample_count",
        "min_x_px",
        "max_x_px",
        "min_y_px",
        "max_y_px",
        "operator_notes",
    ]

    with INVENTORY_CSV.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=fieldnames,
        )

        writer.writeheader()
        writer.writerows(rows_out)

    return rows_out


def generate_package(
    dependencies: dict[str, Any],
) -> dict[str, Any]:
    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    pass1 = dependencies["pass1"]
    pass2 = dependencies["pass2_qc"]

    pass1_segments = grouped_segments(pass1)
    pass2_segments = grouped_segments(pass2)

    rows_by_pass = {
        1: pass1_segments,
        2: pass2_segments,
    }

    with Image.open(SOURCE_IMAGE) as opened:
        source = opened.convert("RGB")

    width, height = source.size

    outputs: list[dict[str, Any]] = []

    # 01: byte-for-byte frozen source context.
    context_path = OUTPUT_DIR / "01_source_context.png"

    shutil.copyfile(
        SOURCE_IMAGE,
        context_path,
    )

    outputs.append(
        {
            "path": str(
                context_path.relative_to(ROOT)
            ),
            "role": "unaltered_frozen_source_context",
            "sha256": sha256_path(context_path),
        }
    )

    # 02: broad source-only semantic annotation region.
    fx0, fy0, fx1, fy1 = LABEL_REGION_FRACTIONS

    label_box = (
        int(round(width * fx0)),
        int(round(height * fy0)),
        int(round(width * fx1)),
        int(round(height * fy1)),
    )

    label_crop = source.crop(label_box)

    label_path = (
        OUTPUT_DIR
        / "02_x1_label_region_source_only.png"
    )

    label_crop.save(label_path)

    outputs.append(
        {
            "path": str(
                label_path.relative_to(ROOT)
            ),
            "role": "source_only_broad_x1_annotation_region",
            "crop_box_px": list(label_box),
            "sha256": sha256_path(label_path),
        }
    )

    # 03: full frozen-source overlay with points only.
    overlay = source.copy()

    draw_rows(
        overlay,
        pass1,
        1,
    )

    draw_rows(
        overlay,
        pass2,
        2,
    )

    draw_segment_labels(
        overlay,
        rows_by_pass,
    )

    overlay_path = (
        OUTPUT_DIR
        / "03_x1_frozen_trace_points_overlay.png"
    )

    overlay.save(overlay_path)

    outputs.append(
        {
            "path": str(
                overlay_path.relative_to(ROOT)
            ),
            "role": (
                "neutral_frozen_x1_points_and_segment_ids_overlay"
            ),
            "pass1_marker": "hollow_red_circle",
            "pass2_qc_marker": "blue_cross",
            "sample_connections_drawn": False,
            "sha256": sha256_path(overlay_path),
        }
    )

    inventory_rows = write_inventory(
        pass1,
        pass2,
    )

    outputs.append(
        {
            "path": str(
                INVENTORY_CSV.relative_to(ROOT)
            ),
            "role": "x1_segment_inventory",
            "sha256": sha256_path(INVENTORY_CSV),
        }
    )

    # 04+: per-segment source-only and overlay crops.
    all_segment_ids = sorted(
        set(pass1_segments)
        | set(pass2_segments)
    )

    segment_outputs: list[
        dict[str, Any]
    ] = []

    for index, segment_id in enumerate(
        all_segment_ids,
        start=1,
    ):
        combined = (
            pass1_segments.get(
                segment_id,
                [],
            )
            + pass2_segments.get(
                segment_id,
                [],
            )
        )

        box = bounding_box(
            combined,
            width,
            height,
            SEGMENT_PADDING_PX,
        )

        source_crop = source.crop(box)

        source_path = (
            OUTPUT_DIR
            / (
                f"segment_{index:02d}_"
                f"{segment_id}_source_only.png"
            )
        )

        source_crop.save(source_path)

        overlay_crop = source_crop.copy()

        draw_rows(
            overlay_crop,
            pass1_segments.get(
                segment_id,
                [],
            ),
            1,
            offset_x=box[0],
            offset_y=box[1],
        )

        draw_rows(
            overlay_crop,
            pass2_segments.get(
                segment_id,
                [],
            ),
            2,
            offset_x=box[0],
            offset_y=box[1],
        )

        overlay_segment_path = (
            OUTPUT_DIR
            / (
                f"segment_{index:02d}_"
                f"{segment_id}_overlay.png"
            )
        )

        overlay_crop.save(
            overlay_segment_path
        )

        segment_outputs.append(
            {
                "segment_id": segment_id,
                "crop_box_px": list(box),
                "source_only_path": str(
                    source_path.relative_to(ROOT)
                ),
                "source_only_sha256": (
                    sha256_path(source_path)
                ),
                "overlay_path": str(
                    overlay_segment_path.relative_to(ROOT)
                ),
                "overlay_sha256": (
                    sha256_path(
                        overlay_segment_path
                    )
                ),
                "sample_connections_drawn": False,
                "theoretical_geometry_drawn": False,
            }
        )

    outputs.extend(
        {
            "path": item["source_only_path"],
            "role": "segment_source_only",
            "segment_id": item["segment_id"],
            "sha256": item["source_only_sha256"],
        }
        for item in segment_outputs
    )

    outputs.extend(
        {
            "path": item["overlay_path"],
            "role": "segment_neutral_overlay",
            "segment_id": item["segment_id"],
            "sha256": item["overlay_sha256"],
        }
        for item in segment_outputs
    )

    manifest = {
        "checkpoint": (
            "first_hand_x1_source_semantic_review_preparation_v0.8"
        ),
        "analysis_class": (
            "neutral_source_semantic_review_asset_preparation"
        ),
        "source": {
            "crop_id": CROP_ID,
            "source_image_path": str(
                SOURCE_IMAGE.relative_to(ROOT)
            ),
            "source_file_sha256": (
                dependencies["source_sha256"]
            ),
            "source_pixel_sha256": (
                dependencies[
                    "manifest"
                ][
                    "pixel_sha256"
                ]
            ),
            "source_width_px": width,
            "source_height_px": height,
        },
        "frozen_inputs": {
            "protocol_path": str(
                PROTOCOL.relative_to(ROOT)
            ),
            "protocol_sha256": (
                dependencies["protocol_sha256"]
            ),
            "pass1_path": str(
                PASS1_CSV.relative_to(ROOT)
            ),
            "pass1_sha256": (
                dependencies["pass1_sha256"]
            ),
            "pass1_x1_rows": len(pass1),
            "pass2_qc_path": str(
                PASS2_QC_CSV.relative_to(ROOT)
            ),
            "pass2_qc_sha256": (
                dependencies["pass2_qc_sha256"]
            ),
            "pass2_qc_x1_rows": len(pass2),
        },
        "overlay_policy": {
            "points_only": True,
            "segments_connected": False,
            "fitted_circle": False,
            "fitted_line": False,
            "great_circle_overlay": False,
            "scaffold_overlay": False,
            "thirty_degree_guide": False,
            "predicted_x1": False,
            "projective_map": False,
        },
        "broad_label_region": {
            "selection_rule": (
                "fixed broad fractional region of prepared "
                "source image; not fitted to geometry"
            ),
            "fractions": list(
                LABEL_REGION_FRACTIONS
            ),
            "crop_box_px": list(
                label_box
            ),
        },
        "segment_padding_px": (
            SEGMENT_PADDING_PX
        ),
        "segment_inventory": (
            inventory_rows
        ),
        "segment_review_assets": (
            segment_outputs
        ),
        "outputs": outputs,
        "interpretation_boundary": (
            "These assets support source-semantic and visible-topology "
            "review only. They do not determine whether X1 is a valid "
            "coordinate curve, scaffold curve, or member of any fitted "
            "geometric model."
        ),
    }

    OUTPUT_MANIFEST.write_text(
        json.dumps(
            manifest,
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )

    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Prepare neutral X1 source-semantic review assets."
        )
    )

    parser.add_argument(
        "--check-inputs",
        action="store_true",
        help=(
            "Verify frozen source/acquisition dependencies "
            "without generating review images."
        ),
    )

    args = parser.parse_args()

    dependencies = verify_inputs()

    if args.check_inputs:
        print("Prepared page-7 spherical crop: VERIFIED")
        print("Raw great-circle acquisition seal: VERIFIED")
        print("QC-corrected pass-2 seal: VERIFIED")
        print("X1 semantic-audit protocol: PRESENT")
        print(
            "X1 pass-1 rows:",
            len(dependencies["pass1"]),
        )
        print(
            "X1 pass-2 QC rows:",
            len(dependencies["pass2_qc"]),
        )
        print(
            "Source crop SHA-256:",
            dependencies["source_sha256"],
        )
        print("No review image was generated.")
        return 0

    manifest = generate_package(
        dependencies
    )

    print("=" * 88)
    print("FIRST HAND X1 SOURCE-SEMANTIC REVIEW PACKAGE")
    print("=" * 88)
    print(
        "Source image:",
        manifest["source"]["source_image_path"],
    )
    print(
        "Dimensions:",
        f"{manifest['source']['source_width_px']}x"
        f"{manifest['source']['source_height_px']} px",
    )
    print(
        "Pass-1 X1 samples:",
        manifest["frozen_inputs"]["pass1_x1_rows"],
    )
    print(
        "Pass-2 QC X1 samples:",
        manifest["frozen_inputs"]["pass2_qc_x1_rows"],
    )
    print(
        "Segments:",
        len(
            manifest["segment_review_assets"]
        ),
    )
    print(
        "Output directory:",
        OUTPUT_DIR,
    )
    print(
        "No fitted geometry or predicted curve was drawn."
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
