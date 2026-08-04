#!/usr/bin/env python3
"""Prepare deterministic diagram crops from the locked Arm of God PDF."""

from __future__ import annotations

import csv
import hashlib
import json
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Any

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]

SOURCE_PATH = (
    ROOT
    / "data"
    / "source_snapshots"
    / "first_hand_arm_of_god"
    / "raw"
    / "ARMOFGODRef21sep0CPC.2005A.pdf"
)

SOURCE_MANIFEST_PATH = (
    ROOT
    / "data"
    / "source_manifests"
    / "first_hand_arm_of_god"
    / "official_asset_manifest.csv"
)

OUTPUT_DIR = (
    ROOT
    / "data"
    / "source_snapshots"
    / "first_hand_arm_of_god"
    / "prepared"
)

CROP_MANIFEST_PATH = (
    ROOT
    / "data"
    / "source_manifests"
    / "first_hand_arm_of_god"
    / "diagram_crop_manifest.csv"
)

JSON_AUDIT_PATH = (
    ROOT
    / "data"
    / "derived"
    / "first_hand_arm_of_god"
    / "diagram_source_preparation.json"
)

REPORT_PATH = (
    ROOT
    / "reports"
    / "arm_of_god_diagram_source_preparation.md"
)

EXPECTED_SOURCE_SHA256 = (
    "80d52f4b6afefe65ae50e4c01378765"
    "c34ae4fde1ad44e8b299870c2e1d3e6fa"
)

EXPECTED_SOURCE_BYTES = 1_343_797
EXPECTED_PAGES = 16
DPI = 300
EXPECTED_FULL_WIDTH = 2550
EXPECTED_FULL_HEIGHT = 3300


CROPS: tuple[dict[str, Any], ...] = (
    {
        "crop_id": "AOG_P07_SEVEN_REGION_INSET",
        "source_page": 7,
        "box": (250, 750, 2220, 1070),
        "filename": "aog_p07_seven_region_inset.png",
        "role": (
            "Seven-region 2-torus inset and its three-turn "
            "vortex-edge caption."
        ),
        "metric_use_policy": (
            "Source correspondence and later digitization only; "
            "not yet a metric reconstruction."
        ),
    },
    {
        "crop_id": "AOG_P07_SPHERICAL_PROJECTION",
        "source_page": 7,
        "box": (180, 900, 2290, 2160),
        "filename": "aog_p07_spherical_projection.png",
        "role": (
            "Planar reciprocal spiral beside the labelled "
            "cube-octahedral spherical projection."
        ),
        "metric_use_policy": (
            "Landmark calibration after a separate protocol; "
            "no self-embedment scoring at source-preparation stage."
        ),
    },
    {
        "crop_id": "AOG_P07_HAND_REGION",
        "source_page": 7,
        "box": (220, 2050, 2280, 3070),
        "filename": "aog_p07_hand_region.png",
        "role": (
            "Three-copy 120-degree construction and shaded "
            "Tefillin Hand region."
        ),
        "metric_use_policy": (
            "Source correspondence and region-boundary digitization only."
        ),
    },
    {
        "crop_id": "AOG_P08_HAND_VIEWS",
        "source_page": 8,
        "box": (350, 390, 2200, 1260),
        "filename": "aog_p08_hand_views.png",
        "role": (
            "Published side and top views of the Tefillin Hand."
        ),
        "metric_use_policy": (
            "Qualitative pose and topology constraints until "
            "landmarks and camera conventions are preregistered."
        ),
    },
    {
        "crop_id": "AOG_P08_UNIT_ANGLE_CUBOCTAHEDRON",
        "source_page": 8,
        "box": (300, 1250, 2250, 3000),
        "filename": "aog_p08_unit_angle_cuboctahedron.png",
        "role": (
            "Unit-angle discussion and cube-octahedral "
            "30-degree scaffold."
        ),
        "metric_use_policy": (
            "Source evidence for competing scale hypotheses; "
            "not permission to choose a scale from fit quality."
        ),
    },
)


def sha256_path(path: Path) -> str:
    """Return the SHA-256 digest of one file."""
    digest = hashlib.sha256()

    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)

    return digest.hexdigest()


def pixel_sha256(image: Image.Image) -> str:
    """Hash canonical image dimensions, mode, and raw pixel bytes."""
    canonical = image.convert("RGB")

    digest = hashlib.sha256()
    digest.update(
        f"{canonical.width}x{canonical.height}|RGB|".encode("ascii")
    )
    digest.update(canonical.tobytes())

    return digest.hexdigest()


def read_source_manifest() -> dict[str, str]:
    """Read and validate the locked source manifest."""
    with SOURCE_MANIFEST_PATH.open(
        newline="",
        encoding="utf-8",
    ) as handle:
        rows = list(csv.DictReader(handle))

    if len(rows) != 1:
        raise RuntimeError(
            f"Expected one source-manifest row; found {len(rows)}."
        )

    row = rows[0]

    if row["sha256"] != EXPECTED_SOURCE_SHA256:
        raise RuntimeError(
            "The source manifest does not contain the frozen SHA-256."
        )

    if int(row["bytes"]) != EXPECTED_SOURCE_BYTES:
        raise RuntimeError(
            "The source manifest does not contain the frozen byte size."
        )

    if int(row["pages"]) != EXPECTED_PAGES:
        raise RuntimeError(
            "The source manifest does not contain the frozen page count."
        )

    return row


def tool_version(command: str) -> str:
    """Return the first non-empty version line from a command."""
    completed = subprocess.run(
        [command, "-v"],
        check=False,
        capture_output=True,
        text=True,
    )

    combined = "\n".join(
        part for part in (completed.stdout, completed.stderr) if part
    )

    for line in combined.splitlines():
        stripped = line.strip()

        if stripped:
            return stripped

    return "unknown"


def render_pages() -> tuple[dict[int, Image.Image], str]:
    """Render source pages 7 and 8 at the frozen resolution."""
    executable = shutil.which("pdftoppm")

    if executable is None:
        raise RuntimeError(
            "pdftoppm is required but was not found on PATH."
        )

    version = tool_version(executable)

    with tempfile.TemporaryDirectory(
        prefix="aog-diagram-source-"
    ) as temporary_directory:
        prefix = Path(temporary_directory) / "page"

        subprocess.run(
            [
                executable,
                "-f",
                "7",
                "-l",
                "8",
                "-r",
                str(DPI),
                "-png",
                str(SOURCE_PATH),
                str(prefix),
            ],
            check=True,
        )

        rendered: dict[int, Image.Image] = {}

        for page in (7, 8):
            path = Path(
                f"{prefix}-{page:02d}.png"
            )

            if not path.exists():
                raise RuntimeError(
                    f"Expected rendered page was not produced: {path}"
                )

            with Image.open(path) as opened:
                image = opened.convert("RGB")

            if image.size != (
                EXPECTED_FULL_WIDTH,
                EXPECTED_FULL_HEIGHT,
            ):
                raise RuntimeError(
                    "Unexpected source-page raster dimensions: "
                    f"page {page} has {image.size}, expected "
                    f"{EXPECTED_FULL_WIDTH}x{EXPECTED_FULL_HEIGHT}."
                )

            rendered[page] = image

    return rendered, version


source_manifest = read_source_manifest()

if not SOURCE_PATH.exists():
    raise RuntimeError(
        f"Missing locally preserved source PDF: {SOURCE_PATH}"
    )

actual_source_sha256 = sha256_path(SOURCE_PATH)
actual_source_bytes = SOURCE_PATH.stat().st_size

if actual_source_sha256 != EXPECTED_SOURCE_SHA256:
    raise RuntimeError(
        "The locally preserved PDF differs from the frozen source."
    )

if actual_source_bytes != EXPECTED_SOURCE_BYTES:
    raise RuntimeError(
        "The locally preserved PDF has an unexpected byte size."
    )

rendered_pages, pdftoppm_version = render_pages()

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

manifest_fields = [
    "crop_id",
    "source_asset",
    "source_page",
    "source_sha256",
    "dpi",
    "full_width_px",
    "full_height_px",
    "left_px",
    "top_px",
    "right_px",
    "bottom_px",
    "output_width_px",
    "output_height_px",
    "output_path",
    "file_sha256",
    "pixel_sha256",
    "role",
    "metric_use_policy",
]

manifest_rows: list[dict[str, str]] = []
json_rows: list[dict[str, Any]] = []

for crop in CROPS:
    page = int(crop["source_page"])
    left, top, right, bottom = crop["box"]

    if not (
        0
        <= left
        < right
        <= EXPECTED_FULL_WIDTH
        and 0
        <= top
        < bottom
        <= EXPECTED_FULL_HEIGHT
    ):
        raise RuntimeError(
            f"Invalid crop box for {crop['crop_id']}: {crop['box']}"
        )

    cropped = rendered_pages[page].crop(
        (left, top, right, bottom)
    ).convert("RGB")

    output_path = OUTPUT_DIR / str(
        crop["filename"]
    )

    cropped.save(
        output_path,
        format="PNG",
        optimize=False,
        compress_level=9,
    )

    relative_output_path = output_path.relative_to(
        ROOT
    ).as_posix()

    file_digest = sha256_path(
        output_path
    )

    pixel_digest = pixel_sha256(
        cropped
    )

    row = {
        "crop_id": str(crop["crop_id"]),
        "source_asset": source_manifest["asset_id"],
        "source_page": str(page),
        "source_sha256": actual_source_sha256,
        "dpi": str(DPI),
        "full_width_px": str(EXPECTED_FULL_WIDTH),
        "full_height_px": str(EXPECTED_FULL_HEIGHT),
        "left_px": str(left),
        "top_px": str(top),
        "right_px": str(right),
        "bottom_px": str(bottom),
        "output_width_px": str(cropped.width),
        "output_height_px": str(cropped.height),
        "output_path": relative_output_path,
        "file_sha256": file_digest,
        "pixel_sha256": pixel_digest,
        "role": str(crop["role"]),
        "metric_use_policy": str(crop["metric_use_policy"]),
    }

    manifest_rows.append(
        row
    )

    json_rows.append(
        {
            **row,
            "source_page": page,
            "dpi": DPI,
            "full_width_px": EXPECTED_FULL_WIDTH,
            "full_height_px": EXPECTED_FULL_HEIGHT,
            "left_px": left,
            "top_px": top,
            "right_px": right,
            "bottom_px": bottom,
            "output_width_px": cropped.width,
            "output_height_px": cropped.height,
        }
    )


CROP_MANIFEST_PATH.parent.mkdir(
    parents=True,
    exist_ok=True,
)

with CROP_MANIFEST_PATH.open(
    "w",
    newline="",
    encoding="utf-8",
) as handle:
    writer = csv.DictWriter(
        handle,
        fieldnames=manifest_fields,
    )

    writer.writeheader()
    writer.writerows(
        manifest_rows
    )


JSON_AUDIT_PATH.parent.mkdir(
    parents=True,
    exist_ok=True,
)

audit = {
    "source": {
        "asset_id": source_manifest["asset_id"],
        "filename": SOURCE_PATH.name,
        "bytes": actual_source_bytes,
        "pages": EXPECTED_PAGES,
        "sha256": actual_source_sha256,
    },
    "rendering": {
        "tool": "pdftoppm",
        "tool_version": pdftoppm_version,
        "dpi": DPI,
        "full_page_dimensions_px": [
            EXPECTED_FULL_WIDTH,
            EXPECTED_FULL_HEIGHT,
        ],
        "colour_mode": "RGB",
    },
    "crops": json_rows,
    "scope": {
        "landmarks_digitized": False,
        "projection_scale_calibrated": False,
        "projective_gauge_calibrated": False,
        "self_embedment_scores_computed": False,
        "source_preparation_only": True,
    },
}

JSON_AUDIT_PATH.write_text(
    json.dumps(
        audit,
        indent=2,
        sort_keys=True,
    )
    + "\n",
    encoding="utf-8",
)


REPORT_PATH.parent.mkdir(
    parents=True,
    exist_ok=True,
)

table_lines = [
    "| Crop ID | Page | Box `(L,T,R,B)` | Output size | Role |",
    "|---|---:|---:|---:|---|",
]

for row in manifest_rows:
    table_lines.append(
        "| "
        f"`{row['crop_id']}` | "
        f"{row['source_page']} | "
        f"`({row['left_px']},{row['top_px']},"
        f"{row['right_px']},{row['bottom_px']})` | "
        f"{row['output_width_px']}×{row['output_height_px']} | "
        f"{row['role']} |"
    )

report = f"""# *The Arm of God* diagram source preparation

**Status:** Deterministic source-image preparation  
**Primary source:** `{source_manifest["asset_id"]}`  
**Source SHA-256:** `{actual_source_sha256}`  
**Rasterization:** `{DPI} DPI`, RGB, `{EXPECTED_FULL_WIDTH}×{EXPECTED_FULL_HEIGHT}` pixels  
**Renderer:** `{pdftoppm_version}`

## Purpose

Pages 7 and 8 contain the main visual evidence needed to constrain the
First Hand spherical construction:

- the planar reciprocal spiral;
- the labelled spherical great-circle scaffold;
- the three-copy 120-degree Hand region;
- the seven-region torus inset;
- the side and top Hand views;
- and the cube-octahedral unit-angle scaffold.

This checkpoint freezes source excerpts and pixel coordinates before any
landmark fitting, projective calibration, or self-embedment scoring.

## Prepared crops

{chr(10).join(table_lines)}

## Coordinate convention

All crop boxes use the full rendered page coordinate system:

```text
origin:          upper-left pixel
x direction:     right
y direction:     down
box convention:  [left, top, right, bottom)
page raster:     {EXPECTED_FULL_WIDTH} x {EXPECTED_FULL_HEIGHT}
resolution:      {DPI} DPI
```

The crop coordinates are source-preparation choices with generous
padding. They are not geometric landmarks and do not encode a preferred
projection model.

## Integrity

Each manifest row records:

- the frozen source-PDF digest;
- the source page and raster resolution;
- the crop box;
- output dimensions;
- PNG file SHA-256;
- canonical RGB pixel SHA-256;
- and the permitted evidential role of the crop.

The full rendered pages are temporary build products and are not
preserved in the repository.

## Scope boundary

This checkpoint does **not**:

- digitize sphere, great-circle, or spiral landmarks;
- calibrate the inverse-gnomonic scale;
- select a projective gauge;
- decide whether the page-7 drawing is metrically exact;
- compute S1, S1.5, or S2;
- or assert correspondence with a physical First Hand artefact.

The next checkpoint must preregister a landmark vocabulary and
measurement protocol before any source-image fitting is performed.
"""

REPORT_PATH.write_text(
    report,
    encoding="utf-8",
)

print("=" * 78)
print("ARM OF GOD DIAGRAM SOURCE PREPARATION")
print("=" * 78)
print(
    f"Source SHA-256:  {actual_source_sha256}"
)
print(
    f"Renderer:       {pdftoppm_version}"
)
print(
    "Page raster:    "
    f"{EXPECTED_FULL_WIDTH}x{EXPECTED_FULL_HEIGHT} at {DPI} DPI"
)
print(
    f"Prepared crops: {len(manifest_rows)}"
)

for row in manifest_rows:
    print(
        f"  {row['crop_id']:<38} "
        f"{row['output_width_px']}x{row['output_height_px']}"
    )

print("Landmarks digitized:            False")
print("Projection scale calibrated:    False")
print("Self-embedment scores computed: False")
print(f"Wrote {CROP_MANIFEST_PATH}")
print(f"Wrote {JSON_AUDIT_PATH}")
print(f"Wrote {REPORT_PATH}")
