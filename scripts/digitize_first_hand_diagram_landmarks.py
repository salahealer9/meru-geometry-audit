#!/usr/bin/env python3
"""Blind two-pass digitizer for the First Hand source diagrams.

The tool displays only the frozen prepared source crop and registry
instructions. It never loads a theoretical curve, fitted overlay,
projection residual, or self-embedment score.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable, Sequence

import matplotlib.pyplot as plt
from PIL import Image


ROOT = Path(__file__).resolve().parents[1]

REGISTRY_PATH = (
    ROOT
    / "data"
    / "source_claims"
    / "first_hand_diagram_landmark_registry.csv"
)

CROP_MANIFEST_PATH = (
    ROOT
    / "data"
    / "source_manifests"
    / "first_hand_arm_of_god"
    / "diagram_crop_manifest.csv"
)

OUTPUT_DIR = (
    ROOT
    / "data"
    / "derived"
    / "first_hand_arm_of_god"
)

OUTPUT_FIELDS = [
    "crop_id",
    "crop_file_sha256",
    "crop_pixel_sha256",
    "landmark_id",
    "pass_number",
    "operator",
    "sequence_index",
    "x_px",
    "y_px",
    "local_stroke_width_px",
    "object_type",
    "fit_partition",
    "source_feature",
    "operator_note",
    "timestamp_utc",
]

DEFAULT_PARTITIONS = (
    "calibration",
    "scale_calibration",
    "holdout",
)


@dataclass(frozen=True)
class LandmarkSpec:
    """One preregistered landmark specification."""

    landmark_id: str
    crop_id: str
    source_page: int
    object_type: str
    source_feature: str
    geometry_role: str
    acquisition_mode: str
    minimum_samples: int
    fit_partition: str
    uncertainty_rule: str
    allowed_use: str
    exclusions: str
    status: str


@dataclass(frozen=True)
class CropSpec:
    """One frozen prepared source crop."""

    crop_id: str
    source_page: int
    output_path: Path
    file_sha256: str
    pixel_sha256: str
    width_px: int
    height_px: int


def sha256_path(path: Path) -> str:
    """Return the SHA-256 digest of a file."""
    digest = hashlib.sha256()

    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)

    return digest.hexdigest()


def pixel_sha256(image: Image.Image) -> str:
    """Hash canonical RGB pixels, including dimensions."""
    canonical = image.convert("RGB")

    digest = hashlib.sha256()
    digest.update(
        f"{canonical.width}x{canonical.height}|RGB|".encode("ascii")
    )
    digest.update(canonical.tobytes())

    return digest.hexdigest()


def utc_now() -> str:
    """Return a compact UTC timestamp."""
    return (
        datetime.now(timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )


def read_landmark_registry(
    path: Path = REGISTRY_PATH,
) -> list[LandmarkSpec]:
    """Read the preregistered landmark vocabulary."""
    with path.open(
        newline="",
        encoding="utf-8",
    ) as handle:
        rows = list(csv.DictReader(handle))

    specs: list[LandmarkSpec] = []

    for row in rows:
        specs.append(
            LandmarkSpec(
                landmark_id=row["landmark_id"],
                crop_id=row["crop_id"],
                source_page=int(row["source_page"]),
                object_type=row["object_type"],
                source_feature=row["source_feature"],
                geometry_role=row["geometry_role"],
                acquisition_mode=row["acquisition_mode"],
                minimum_samples=int(row["minimum_samples"]),
                fit_partition=row["fit_partition"],
                uncertainty_rule=row["uncertainty_rule"],
                allowed_use=row["allowed_use"],
                exclusions=row["exclusions"],
                status=row["status"],
            )
        )

    ids = [spec.landmark_id for spec in specs]

    if len(ids) != len(set(ids)):
        raise RuntimeError(
            "The landmark registry contains duplicate landmark IDs."
        )

    return specs


def read_crop_manifest(
    path: Path = CROP_MANIFEST_PATH,
) -> dict[str, CropSpec]:
    """Read prepared-crop identities and paths."""
    with path.open(
        newline="",
        encoding="utf-8",
    ) as handle:
        rows = list(csv.DictReader(handle))

    crops: dict[str, CropSpec] = {}

    for row in rows:
        crop_id = row["crop_id"]

        if crop_id in crops:
            raise RuntimeError(
                f"Duplicate crop ID in manifest: {crop_id}"
            )

        crops[crop_id] = CropSpec(
            crop_id=crop_id,
            source_page=int(row["source_page"]),
            output_path=ROOT / row["output_path"],
            file_sha256=row["file_sha256"],
            pixel_sha256=row["pixel_sha256"],
            width_px=int(row["output_width_px"]),
            height_px=int(row["output_height_px"]),
        )

    return crops


def verify_crop(crop: CropSpec) -> Image.Image:
    """Verify one prepared crop and return canonical RGB pixels."""
    if not crop.output_path.exists():
        raise RuntimeError(
            f"Prepared crop is missing: {crop.output_path}"
        )

    actual_file_sha256 = sha256_path(crop.output_path)

    if actual_file_sha256 != crop.file_sha256:
        raise RuntimeError(
            f"File hash mismatch for {crop.crop_id}."
        )

    with Image.open(crop.output_path) as opened:
        image = opened.convert("RGB")

    if image.size != (
        crop.width_px,
        crop.height_px,
    ):
        raise RuntimeError(
            f"Unexpected dimensions for {crop.crop_id}: "
            f"{image.size}."
        )

    actual_pixel_sha256 = pixel_sha256(image)

    if actual_pixel_sha256 != crop.pixel_sha256:
        raise RuntimeError(
            f"Pixel hash mismatch for {crop.crop_id}."
        )

    return image


def expected_samples_per_pass(spec: LandmarkSpec) -> int | None:
    """Return required sample count for one independent pass.

    Point landmarks receive one click per pass. The angular annotation
    receives its three preregistered points per pass. Curves use an open
    count and are checked against the registry minimum.
    """
    if spec.object_type == "point":
        return 1

    if spec.object_type == "angular_annotation":
        return spec.minimum_samples

    return None


def output_path_for_pass(pass_number: int) -> Path:
    """Return the frozen pass-specific output path."""
    if pass_number not in {1, 2}:
        raise ValueError(
            "pass_number must be 1 or 2."
        )

    return (
        OUTPUT_DIR
        / f"diagram_landmarks_pass{pass_number}.csv"
    )


def read_existing_rows(path: Path) -> list[dict[str, str]]:
    """Read an existing output file, if present."""
    if not path.exists():
        return []

    with path.open(
        newline="",
        encoding="utf-8",
    ) as handle:
        reader = csv.DictReader(handle)

        if reader.fieldnames != OUTPUT_FIELDS:
            raise RuntimeError(
                f"Unexpected output schema in {path}."
            )

        return list(reader)


def existing_landmark_ids(
    rows: Sequence[dict[str, str]],
) -> set[str]:
    """Return landmark IDs already present in one pass file."""
    return {
        row["landmark_id"]
        for row in rows
    }


def parse_positive_float(raw: str, label: str) -> float:
    """Parse a finite strictly positive float."""
    try:
        value = float(raw)
    except ValueError as error:
        raise ValueError(
            f"{label} must be numeric."
        ) from error

    if not (
        value > 0.0
        and value < float("inf")
    ):
        raise ValueError(
            f"{label} must be finite and strictly positive."
        )

    return value


def prompt_stroke_width(spec: LandmarkSpec) -> float:
    """Prompt for one local stroke-width estimate for the object."""
    while True:
        raw = input(
            "\nEstimated local visible stroke/node width in pixels "
            f"for {spec.landmark_id}: "
        ).strip()

        try:
            return parse_positive_float(
                raw,
                "stroke width",
            )
        except ValueError as error:
            print(
                f"Invalid value: {error}",
                file=sys.stderr,
            )


def prompt_note() -> str:
    """Prompt for an optional operator note."""
    return input(
        "Optional operator note "
        "(press Enter for none): "
    ).strip()


def acquisition_instruction(spec: LandmarkSpec) -> str:
    """Return concise on-screen acquisition instructions."""
    if spec.object_type == "point":
        action = (
            "LEFT CLICK once at the requested centre. "
            "The second independent click belongs to the other pass."
        )
    elif spec.object_type == "angular_annotation":
        action = (
            "LEFT CLICK in order: first endpoint, arc midpoint, "
            "second endpoint."
        )
    else:
        action = (
            "LEFT CLICK ordered centreline/contour points. "
            "RIGHT CLICK removes the most recent point. "
            "Press ENTER or MIDDLE CLICK when complete."
        )

    return (
        f"{action}\n\n"
        f"Feature: {spec.source_feature}\n"
        f"Acquisition: {spec.acquisition_mode}\n"
        f"Exclude: {spec.exclusions}"
    )


def collect_points(
    image: Image.Image,
    spec: LandmarkSpec,
    pass_number: int,
) -> list[tuple[float, float]]:
    """Collect one blind digitization pass for a landmark."""
    figure, axis = plt.subplots(
        num=(
            f"First Hand blind digitizer — pass {pass_number} — "
            f"{spec.landmark_id}"
        ),
        figsize=(13, 9),
    )

    axis.imshow(image)
    axis.set_xlim(0, image.width)
    axis.set_ylim(image.height, 0)
    axis.set_aspect("equal")
    axis.set_title(
        (
            f"PASS {pass_number} | {spec.landmark_id}\n"
            f"{spec.fit_partition} | page {spec.source_page}"
        ),
        fontsize=11,
    )
    axis.set_xlabel(
        acquisition_instruction(spec),
        fontsize=9,
    )

    # The source image is shown untouched: no fitted overlays, model
    # curves, previous-pass clicks, residuals, or theoretical landmarks.
    required = expected_samples_per_pass(spec)

    if required is None:
        points = plt.ginput(
            n=-1,
            timeout=0,
            show_clicks=True,
            mouse_add=1,
            mouse_pop=3,
            mouse_stop=2,
        )
    else:
        points = plt.ginput(
            n=required,
            timeout=0,
            show_clicks=True,
            mouse_add=1,
            mouse_pop=3,
            mouse_stop=2,
        )

    plt.close(figure)

    cleaned = [
        (
            float(x),
            float(y),
        )
        for x, y in points
    ]

    if required is None:
        if len(cleaned) < spec.minimum_samples:
            raise RuntimeError(
                f"{spec.landmark_id} requires at least "
                f"{spec.minimum_samples} samples; "
                f"received {len(cleaned)}."
            )
    elif len(cleaned) != required:
        raise RuntimeError(
            f"{spec.landmark_id} requires exactly "
            f"{required} samples in one pass; "
            f"received {len(cleaned)}."
        )

    for x, y in cleaned:
        if not (
            0.0 <= x < image.width
            and 0.0 <= y < image.height
        ):
            raise RuntimeError(
                f"Out-of-bounds point for {spec.landmark_id}: "
                f"({x}, {y})."
            )

    return cleaned


def rows_for_digitization(
    *,
    spec: LandmarkSpec,
    crop: CropSpec,
    pass_number: int,
    operator: str,
    points: Sequence[tuple[float, float]],
    stroke_width_px: float,
    note: str,
    timestamp_utc: str,
) -> list[dict[str, str]]:
    """Build output rows for one landmark pass."""
    rows: list[dict[str, str]] = []

    for sequence_index, (x, y) in enumerate(points):
        rows.append(
            {
                "crop_id": crop.crop_id,
                "crop_file_sha256": crop.file_sha256,
                "crop_pixel_sha256": crop.pixel_sha256,
                "landmark_id": spec.landmark_id,
                "pass_number": str(pass_number),
                "operator": operator,
                "sequence_index": str(sequence_index),
                "x_px": format(x, ".12g"),
                "y_px": format(y, ".12g"),
                "local_stroke_width_px": format(
                    stroke_width_px,
                    ".12g",
                ),
                "object_type": spec.object_type,
                "fit_partition": spec.fit_partition,
                "source_feature": spec.source_feature,
                "operator_note": note,
                "timestamp_utc": timestamp_utc,
            }
        )

    return rows


def write_rows(
    path: Path,
    rows: Sequence[dict[str, str]],
) -> None:
    """Write a complete pass file atomically."""
    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    temporary = path.with_suffix(
        path.suffix + ".tmp"
    )

    with temporary.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=OUTPUT_FIELDS,
        )
        writer.writeheader()
        writer.writerows(rows)

    temporary.replace(path)


def select_specs(
    *,
    all_specs: Sequence[LandmarkSpec],
    landmark_ids: Sequence[str],
    partitions: Sequence[str],
) -> list[LandmarkSpec]:
    """Select preregistered landmarks in registry order."""
    by_id = {
        spec.landmark_id: spec
        for spec in all_specs
    }

    if landmark_ids:
        unknown = [
            landmark_id
            for landmark_id in landmark_ids
            if landmark_id not in by_id
        ]

        if unknown:
            raise RuntimeError(
                "Unknown landmark ID(s): "
                + ", ".join(unknown)
            )

        requested = set(landmark_ids)

        return [
            spec
            for spec in all_specs
            if spec.landmark_id in requested
        ]

    allowed_partitions = set(partitions)

    return [
        spec
        for spec in all_specs
        if spec.fit_partition in allowed_partitions
    ]


def print_registry(
    specs: Iterable[LandmarkSpec],
) -> None:
    """Print the available landmark vocabulary."""
    for spec in specs:
        print(
            f"{spec.landmark_id:<38} "
            f"{spec.fit_partition:<18} "
            f"{spec.object_type:<32} "
            f"{spec.crop_id}"
        )


def validate_output_file(
    path: Path,
    *,
    expected_pass: int | None = None,
) -> list[dict[str, str]]:
    """Validate a digitizer output file without fitting any model."""
    rows = read_existing_rows(path)

    for row in rows:
        if expected_pass is not None:
            if int(row["pass_number"]) != expected_pass:
                raise RuntimeError(
                    f"Unexpected pass number in {path}: "
                    f"{row['pass_number']}"
                )

        parse_positive_float(
            row["local_stroke_width_px"],
            "local_stroke_width_px",
        )

        float(row["x_px"])
        float(row["y_px"])

        if not row["crop_file_sha256"]:
            raise RuntimeError(
                "Missing crop_file_sha256."
            )

        if not row["crop_pixel_sha256"]:
            raise RuntimeError(
                "Missing crop_pixel_sha256."
            )

    return rows


def build_argument_parser() -> argparse.ArgumentParser:
    """Build the command-line interface."""
    parser = argparse.ArgumentParser(
        description=(
            "Blind two-pass digitizer for preregistered "
            "First Hand source landmarks."
        )
    )

    parser.add_argument(
        "--pass-number",
        type=int,
        choices=(1, 2),
        help="Independent digitization pass.",
    )

    parser.add_argument(
        "--operator",
        help="Operator name recorded in each output row.",
    )

    parser.add_argument(
        "--landmark-id",
        action="append",
        default=[],
        help=(
            "Digitize one landmark ID. Repeat for multiple IDs. "
            "When omitted, registry partitions are used."
        ),
    )

    parser.add_argument(
        "--partitions",
        nargs="+",
        default=list(DEFAULT_PARTITIONS),
        choices=(
            "calibration",
            "scale_calibration",
            "holdout",
            "external_holdout",
        ),
        help=(
            "Registry partitions used when --landmark-id is omitted. "
            "External holdouts are excluded by default."
        ),
    )

    parser.add_argument(
        "--list",
        action="store_true",
        help="List registry landmarks and exit.",
    )

    parser.add_argument(
        "--validate",
        type=Path,
        help="Validate an existing pass CSV and exit.",
    )

    parser.add_argument(
        "--replace",
        action="store_true",
        help=(
            "Replace an existing landmark in the selected pass file. "
            "Without this flag, existing landmarks are skipped."
        ),
    )

    parser.add_argument(
        "--restart-pass",
        action="store_true",
        help=(
            "Discard the existing selected pass file before digitizing. "
            "Requires an explicit pass number."
        ),
    )

    return parser


def main() -> int:
    """Run the blind digitizer."""
    args = build_argument_parser().parse_args()

    specs = read_landmark_registry()
    crops = read_crop_manifest()

    missing_crop_ids = sorted(
        {
            spec.crop_id
            for spec in specs
            if spec.crop_id not in crops
        }
    )

    if missing_crop_ids:
        raise RuntimeError(
            "Registry crop IDs missing from crop manifest: "
            + ", ".join(missing_crop_ids)
        )

    if args.list:
        print_registry(specs)
        return 0

    if args.validate is not None:
        rows = validate_output_file(
            args.validate,
        )
        print(
            f"Validated {len(rows)} rows in {args.validate}"
        )
        return 0

    if args.pass_number is None:
        raise RuntimeError(
            "--pass-number is required for digitization."
        )

    if not args.operator:
        raise RuntimeError(
            "--operator is required for digitization."
        )

    output_path = output_path_for_pass(
        args.pass_number
    )

    if args.restart_pass and output_path.exists():
        output_path.unlink()

    existing_rows = read_existing_rows(
        output_path
    )

    if existing_rows:
        validate_output_file(
            output_path,
            expected_pass=args.pass_number,
        )

    selected = select_specs(
        all_specs=specs,
        landmark_ids=args.landmark_id,
        partitions=args.partitions,
    )

    if not selected:
        raise RuntimeError(
            "No landmarks matched the selection."
        )

    current_rows = list(existing_rows)
    current_ids = existing_landmark_ids(
        current_rows
    )

    print("=" * 78)
    print("FIRST HAND BLIND DIAGRAM DIGITIZER")
    print("=" * 78)
    print(f"Pass:       {args.pass_number}")
    print(f"Operator:   {args.operator}")
    print(f"Output:     {output_path}")
    print(
        "Model data:  NOT LOADED "
        "(source crop and registry instructions only)"
    )
    print(
        "Partitions:  "
        + ", ".join(args.partitions)
    )
    print(
        f"Selected:    {len(selected)} landmarks"
    )

    for index, spec in enumerate(selected, start=1):
        if (
            spec.landmark_id in current_ids
            and not args.replace
        ):
            print(
                f"[{index}/{len(selected)}] "
                f"SKIP existing {spec.landmark_id}"
            )
            continue

        crop = crops[spec.crop_id]
        image = verify_crop(crop)

        print("\n" + "-" * 78)
        print(
            f"[{index}/{len(selected)}] {spec.landmark_id}"
        )
        print(f"Crop:        {spec.crop_id}")
        print(f"Partition:   {spec.fit_partition}")
        print(f"Object:      {spec.object_type}")
        print(f"Feature:     {spec.source_feature}")
        print(f"Acquire:     {spec.acquisition_mode}")
        print(f"Exclude:     {spec.exclusions}")
        print(f"Uncertainty: {spec.uncertainty_rule}")

        input(
            "Press Enter to open the untouched source crop..."
        )

        points = collect_points(
            image=image,
            spec=spec,
            pass_number=args.pass_number,
        )

        stroke_width_px = prompt_stroke_width(
            spec
        )
        note = prompt_note()
        timestamp = utc_now()

        new_rows = rows_for_digitization(
            spec=spec,
            crop=crop,
            pass_number=args.pass_number,
            operator=args.operator,
            points=points,
            stroke_width_px=stroke_width_px,
            note=note,
            timestamp_utc=timestamp,
        )

        if spec.landmark_id in current_ids:
            current_rows = [
                row
                for row in current_rows
                if row["landmark_id"] != spec.landmark_id
            ]

        current_rows.extend(
            new_rows
        )

        write_rows(
            output_path,
            current_rows,
        )

        current_ids.add(
            spec.landmark_id
        )

        print(
            f"Saved {len(new_rows)} samples for "
            f"{spec.landmark_id}."
        )

    validated = validate_output_file(
        output_path,
        expected_pass=args.pass_number,
    )

    print("\n" + "=" * 78)
    print("PASS FILE SAVED")
    print("=" * 78)
    print(f"Rows:      {len(validated)}")
    print(f"Landmarks:{len(existing_landmark_ids(validated)):>5}")
    print(f"Path:      {output_path}")
    print(
        "No consensus, model fit, scale selection, "
        "or self-embedment result was computed."
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
