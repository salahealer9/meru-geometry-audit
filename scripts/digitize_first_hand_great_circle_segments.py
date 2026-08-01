#!/usr/bin/env python3
"""Blind segment-aware digitizer for four labelled First Hand curves plus one unlabelled scaffold holdout.

Each visible curve fragment receives its own ``segment_id``. The tool
never joins fragments across node blobs, labels, arrows, spiral
occlusions, gaps, or uncertain crossings. It displays only the untouched
prepared source crop and never loads either curve pass, the neutral
census, fitted curves, projective maps, or self-embedment results.
"""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path
from typing import Any, Iterable, Sequence

import matplotlib.pyplot as plt
from PIL import Image


ROOT = Path(__file__).resolve().parents[1]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts import digitize_first_hand_diagram_landmarks as core  # noqa: E402


OUTPUT_DIR = ROOT / "data" / "derived" / "first_hand_arm_of_god"

OUTPUT_FIELDS = [
    "crop_id",
    "crop_file_sha256",
    "crop_pixel_sha256",
    "landmark_id",
    "pass_number",
    "operator",
    "segment_id",
    "sequence_index",
    "x_px",
    "y_px",
    "local_stroke_width_px",
    "source_feature",
    "operator_note",
    "timestamp_utc",
]

CURVE_STATUS = "preregistered_later_stage"

CURVE_IDS = (
    "AOG-LM-P07-GC-Y0",
    "AOG-LM-P07-GC-Y1",
    "AOG-LM-P07-GC-YAXIS",
    "AOG-LM-P07-GC-X1",
    "AOG-LM-P07-GC-SCAFFOLD-UR-UC-X1LL-LL",
)

MINIMUM_POINTS_PER_SEGMENT = 4
MINIMUM_POINTS_PER_CURVE = 12

CURVE_DOMAIN_RULE = (
    "Digitize only the visible curve centreline at or inside the "
    "equator-at-horizon limb. "
    "Do not digitize any continuation outside the "
    "equator-at-horizon limb, including an exterior arrow "
    "or label leader. "
    "A collinear exterior continuation remains an annotation, "
    "not part of the spherical curve observation."
)

CURVE_DOMAIN_RULE = (
    "Digitize only the visible curve centreline at or inside the "
    "equator-at-horizon limb. Do not digitize any continuation outside "
    "the equator-at-horizon limb, including an exterior arrow or label "
    "leader, even when it is collinear with the in-sphere curve."
)

Y0_DASHED_BACKSIDE_RULE = (
    "For GC-Y0, include the dashed back-hemisphere continuation "
    "between the upper-left rim node and the central region. "
    "Treat regular dash spacing as line style within one visible run. "
    "Start a new segment only where a node, spiral stroke, or other "
    "genuine occlusion interrupts that dashed run."
)

CURVE_GUIDANCE = {
    "AOG-LM-P07-GC-Y0": {
        "short_name": "GC-Y0",
        "instruction": (
            "Trace only clearly visible centreline fragments of the "
            "labelled y=0 (x-axis) projected curve."
        ),
        "breaks": (
            "Break at the central r-arrow entanglement, filled nodes, "
            "spiral overlaps, labels, gaps, and uncertain crossings. "
            "Stop before the lower-right node blob and exclude the "
            "exterior arrow or label leader beyond the spherical limb."
        ),
    },
    "AOG-LM-P07-GC-Y1": {
        "short_name": "GC-Y1",
        "instruction": (
            "Trace only clearly visible centreline fragments of the "
            "labelled y=1 projected curve."
        ),
        "breaks": (
            "Break at filled nodes, spiral overlaps, labels, arrows, "
            "gaps, and uncertain crossings."
        ),
    },
    "AOG-LM-P07-GC-YAXIS": {
        "short_name": "GC-YAXIS",
        "instruction": (
            "Trace only clearly visible centreline fragments of the "
            "labelled y-axis projected curve."
        ),
        "breaks": (
            "Break around the central circular node, the separate "
            "y-axis incidence node, other node blobs, labels, spiral "
            "overlaps, gaps, and uncertain crossings."
        ),
    },
    "AOG-LM-P07-GC-X1": {
        "short_name": "GC-X1",
        "instruction": (
            "Trace only clearly visible centreline fragments of the "
            "labelled x=1 projected curve."
        ),
        "breaks": (
            "Break around both registered x=1 incidence nodes, other "
            "node blobs, labels, spiral overlaps, gaps, and uncertain "
            "crossings."
        ),
    },
    "AOG-LM-P07-GC-SCAFFOLD-UR-UC-X1LL-LL": {
        "short_name": "GC-SCAFFOLD-HOLDOUT",
        "instruction": (
            "Trace only clearly visible centreline fragments of the "
            "unlabelled scaffold curve running from the upper-right "
            "rim through the upper interior region toward the "
            "lower-left rim."
        ),
        "breaks": (
            "Break at filled nodes, reciprocal-spiral overlaps, "
            "labels, gaps, and uncertain crossings. Do not use "
            "previously digitized node coordinates as guides."
        ),
    },

}


def output_path_for_pass(pass_number: int) -> Path:
    """Return the dedicated segment-aware output path."""
    if pass_number not in {1, 2}:
        raise ValueError("pass_number must be 1 or 2.")
    return OUTPUT_DIR / f"great_circle_segments_pass{pass_number}.csv"


def read_curve_specs() -> list[Any]:
    """Return the four labelled curves and one scaffold holdout."""
    all_specs = core.read_landmark_registry()
    by_id = {spec.landmark_id: spec for spec in all_specs}

    missing = [landmark_id for landmark_id in CURVE_IDS if landmark_id not in by_id]
    if missing:
        raise RuntimeError(
            "Missing great-circle registry IDs: " + ", ".join(missing)
        )

    selected = [by_id[landmark_id] for landmark_id in CURVE_IDS]

    for spec in selected:
        if spec.status != CURVE_STATUS:
            raise RuntimeError(
                f"{spec.landmark_id} must retain status "
                f"{CURVE_STATUS!r}; received {spec.status!r}."
            )
        if spec.object_type != "open_curve":
            raise RuntimeError(f"{spec.landmark_id} must be an open_curve.")

    later_curve_ids = {
        spec.landmark_id
        for spec in all_specs
        if (
            spec.status == CURVE_STATUS
            and spec.object_type == "open_curve"
            and spec.landmark_id.startswith("AOG-LM-P07-GC-")
        )
    }

    if later_curve_ids != set(CURVE_IDS):
        raise RuntimeError(
            "The later-stage great-circle vocabulary differs from "
            "the four frozen curve IDs."
        )

    return selected


def select_specs(
    specs: Sequence[Any],
    requested_ids: Sequence[str],
) -> list[Any]:
    """Select all four curves or an explicit deterministic subset."""
    if not requested_ids:
        return list(specs)

    requested = set(requested_ids)
    available = {spec.landmark_id for spec in specs}
    unknown = sorted(requested - available)

    if unknown:
        raise RuntimeError(
            "Unknown great-circle landmark ID(s): " + ", ".join(unknown)
        )

    return [spec for spec in specs if spec.landmark_id in requested]


def read_existing_rows(path: Path) -> list[dict[str, str]]:
    """Read a segment-aware output file, if present."""
    if not path.exists():
        return []

    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames != OUTPUT_FIELDS:
            raise RuntimeError(f"Unexpected segment-aware schema in {path}.")
        return list(reader)


def write_rows(
    path: Path,
    rows: Sequence[dict[str, str]],
) -> None:
    """Write deterministic segment-aware rows."""
    path.parent.mkdir(parents=True, exist_ok=True)
    curve_order = {
        landmark_id: index
        for index, landmark_id in enumerate(CURVE_IDS)
    }
    ordered = sorted(
        rows,
        key=lambda row: (
            curve_order[row["landmark_id"]],
            row["segment_id"],
            int(row["sequence_index"]),
        ),
    )

    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=OUTPUT_FIELDS)
        writer.writeheader()
        writer.writerows(ordered)


def group_rows(
    rows: Iterable[dict[str, str]],
) -> dict[str, dict[str, list[dict[str, str]]]]:
    """Group rows as landmark -> segment -> ordered samples."""
    grouped: dict[str, dict[str, list[dict[str, str]]]] = {}

    for row in rows:
        grouped.setdefault(row["landmark_id"], {}).setdefault(
            row["segment_id"], []
        ).append(row)

    for segments in grouped.values():
        for segment_rows in segments.values():
            segment_rows.sort(key=lambda row: int(row["sequence_index"]))

    return grouped


def required_curve_total(spec: Any) -> int:
    """Return the frozen total-point floor for one curve."""
    return max(MINIMUM_POINTS_PER_CURVE, int(spec.minimum_samples))


def validate_rows(
    rows: Sequence[dict[str, str]],
    *,
    specs: Sequence[Any],
    expected_pass: int | None,
    require_complete_pass: bool,
) -> None:
    """Validate segment separation, provenance, and sample floors."""
    if not rows:
        raise RuntimeError("The segment-aware pass file is empty.")

    spec_by_id = {spec.landmark_id: spec for spec in specs}

    pass_numbers = {int(row["pass_number"]) for row in rows}
    if len(pass_numbers) != 1:
        raise RuntimeError("A curve pass contains multiple pass numbers.")

    actual_pass = next(iter(pass_numbers))
    if actual_pass not in {1, 2}:
        raise RuntimeError(f"Invalid curve pass number: {actual_pass}")

    if expected_pass is not None and actual_pass != expected_pass:
        raise RuntimeError(
            f"Expected pass {expected_pass}; received pass {actual_pass}."
        )

    row_ids = {row["landmark_id"] for row in rows}
    unknown_ids = row_ids - set(spec_by_id)

    if unknown_ids:
        raise RuntimeError(
            "Unexpected landmark ID(s): " + ", ".join(sorted(unknown_ids))
        )

    if require_complete_pass and row_ids != set(CURVE_IDS):
        missing = sorted(set(CURVE_IDS) - row_ids)
        raise RuntimeError("Incomplete curve pass; missing: " + ", ".join(missing))

    if len({row["crop_file_sha256"] for row in rows}) != 1:
        raise RuntimeError("A curve pass contains multiple crop file hashes.")
    if len({row["crop_pixel_sha256"] for row in rows}) != 1:
        raise RuntimeError("A curve pass contains multiple crop pixel hashes.")

    grouped = group_rows(rows)
    seen_keys: set[tuple[str, str, int]] = set()

    for row in rows:
        segment_id = row["segment_id"]
        if not (
            len(segment_id) == 3
            and segment_id.startswith("S")
            and segment_id[1:].isdigit()
            and int(segment_id[1:]) >= 1
        ):
            raise RuntimeError(f"Invalid segment_id: {segment_id!r}")

        sequence_index = int(row["sequence_index"])
        key = (row["landmark_id"], segment_id, sequence_index)

        if key in seen_keys:
            raise RuntimeError(
                "Duplicate landmark/segment/sequence row: " f"{key}"
            )
        seen_keys.add(key)

        for coordinate_name in (
            "x_px",
            "y_px",
            "local_stroke_width_px",
        ):
            value = float(row[coordinate_name])
            if not (value == value and abs(value) < float("inf")):
                raise RuntimeError(f"Non-finite {coordinate_name}.")

        if float(row["local_stroke_width_px"]) <= 0.0:
            raise RuntimeError("Stroke width must be strictly positive.")

    for landmark_id, segments in grouped.items():
        spec = spec_by_id[landmark_id]

        segment_numbers = sorted(
            int(segment_id[1:]) for segment_id in segments
        )
        expected_segment_numbers = list(range(1, len(segment_numbers) + 1))

        if segment_numbers != expected_segment_numbers:
            raise RuntimeError(
                f"{landmark_id} segment IDs must be contiguous from S01."
            )

        total_points = 0

        for segment_id, segment_rows in segments.items():
            indices = [int(row["sequence_index"]) for row in segment_rows]

            if indices != list(range(len(indices))):
                raise RuntimeError(
                    f"{landmark_id}/{segment_id} sequence indices "
                    "must be contiguous from zero."
                )

            if len(segment_rows) < MINIMUM_POINTS_PER_SEGMENT:
                raise RuntimeError(
                    f"{landmark_id}/{segment_id} requires at least "
                    f"{MINIMUM_POINTS_PER_SEGMENT} points."
                )

            total_points += len(segment_rows)

        if total_points < required_curve_total(spec):
            raise RuntimeError(
                f"{landmark_id} requires at least "
                f"{required_curve_total(spec)} total points; "
                f"received {total_points}."
            )


def validate_output_file(
    path: Path,
    *,
    expected_pass: int | None = None,
    require_complete_pass: bool = True,
) -> list[dict[str, str]]:
    """Validate a frozen segment-aware curve pass."""
    specs = read_curve_specs()
    rows = read_existing_rows(path)
    validate_rows(
        rows,
        specs=specs,
        expected_pass=expected_pass,
        require_complete_pass=require_complete_pass,
    )
    return rows


def collect_segment(
    *,
    image: Image.Image,
    spec: Any,
    pass_number: int,
    segment_number: int,
) -> list[tuple[float, float]]:
    """Collect one visible fragment from an untouched source crop."""
    guidance = CURVE_GUIDANCE[spec.landmark_id]

    figure, axis = plt.subplots(
        num=(
            "First Hand segment-aware curve digitizer — "
            f"pass {pass_number} — {guidance['short_name']} — "
            f"S{segment_number:02d}"
        ),
        figsize=(13, 9),
    )

    axis.imshow(image)
    axis.set_xlim(0, image.width)
    axis.set_ylim(image.height, 0)
    axis.set_aspect("equal")
    axis.set_title(
        (
            f"PASS {pass_number} | {spec.landmark_id} | "
            f"SEGMENT S{segment_number:02d}\n"
            "Untouched source crop — do not bridge hidden or "
            "uncertain portions"
        ),
        fontsize=11,
    )
    axis.set_xlabel(
        (
            "LEFT CLICK ordered centreline points. "
            "RIGHT CLICK removes the latest point. "
            "ENTER or MIDDLE CLICK finishes this visible segment.\n"
            f"{guidance['instruction']}\n"
            f"{guidance['breaks']}"
        ),
        fontsize=9,
    )

    # No prior pass, current-pass segment, node overlay, model curve,
    # fitted result, residual, or theoretical continuation is shown.
    points = plt.ginput(
        n=-1,
        timeout=0,
        show_clicks=True,
        mouse_add=1,
        mouse_pop=3,
        mouse_stop=2,
    )
    plt.close(figure)

    cleaned = [(float(x), float(y)) for x, y in points]

    if len(cleaned) < MINIMUM_POINTS_PER_SEGMENT:
        raise RuntimeError(
            f"One visible segment requires at least "
            f"{MINIMUM_POINTS_PER_SEGMENT} points; "
            f"received {len(cleaned)}."
        )

    for x, y in cleaned:
        if not (0.0 <= x < image.width and 0.0 <= y < image.height):
            raise RuntimeError(f"Out-of-bounds point: ({x}, {y}).")

    return cleaned


def prompt_yes_no(prompt: str) -> bool:
    """Return True for yes and False for no."""
    while True:
        answer = input(prompt).strip().lower()
        if answer in {"y", "yes"}:
            return True
        if answer in {"n", "no"}:
            return False
        print("Please enter y or n.", file=sys.stderr)


def rows_for_segment(
    *,
    spec: Any,
    crop: Any,
    pass_number: int,
    operator: str,
    segment_number: int,
    points: Sequence[tuple[float, float]],
    stroke_width_px: float,
    note: str,
    timestamp_utc: str,
) -> list[dict[str, str]]:
    """Build rows for one independent visible fragment."""
    segment_id = f"S{segment_number:02d}"

    return [
        {
            "crop_id": crop.crop_id,
            "crop_file_sha256": crop.file_sha256,
            "crop_pixel_sha256": crop.pixel_sha256,
            "landmark_id": spec.landmark_id,
            "pass_number": str(pass_number),
            "operator": operator,
            "segment_id": segment_id,
            "sequence_index": str(sequence_index),
            "x_px": format(x, ".12g"),
            "y_px": format(y, ".12g"),
            "local_stroke_width_px": format(stroke_width_px, ".12g"),
            "source_feature": spec.source_feature,
            "operator_note": note,
            "timestamp_utc": timestamp_utc,
        }
        for sequence_index, (x, y) in enumerate(points)
    ]


def capture_curve(
    *,
    image: Image.Image,
    spec: Any,
    crop: Any,
    pass_number: int,
    operator: str,
) -> list[dict[str, str]]:
    """Capture all explicitly visible segments for one curve."""
    guidance = CURVE_GUIDANCE[spec.landmark_id]
    collected: list[dict[str, str]] = []
    segment_number = 1

    print("\n" + "=" * 78)
    print(f"{spec.landmark_id} — {guidance['short_name']}")
    print(f"Feature: {spec.source_feature}")
    print(guidance["instruction"])
    print(guidance["breaks"])
    print(
        "No hidden interpolation: each disconnected visible fragment "
        "must be a separate segment."
    )
    print(
        CURVE_DOMAIN_RULE
    )

    if spec.landmark_id == "AOG-LM-P07-GC-Y0":
        print(
            Y0_DASHED_BACKSIDE_RULE
        )

    while True:
        input(
            f"\nPress Enter to open untouched crop for "
            f"segment S{segment_number:02d}..."
        )

        try:
            points = collect_segment(
                image=image,
                spec=spec,
                pass_number=pass_number,
                segment_number=segment_number,
            )
        except RuntimeError as error:
            print(f"Segment rejected: {error}", file=sys.stderr)
            if prompt_yes_no("Retry this segment? [y/n]: "):
                continue
            raise RuntimeError(
                f"Cancelled {spec.landmark_id} before completion."
            ) from error

        stroke_width_px = core.prompt_stroke_width(spec)
        note = core.prompt_note()

        collected.extend(
            rows_for_segment(
                spec=spec,
                crop=crop,
                pass_number=pass_number,
                operator=operator,
                segment_number=segment_number,
                points=points,
                stroke_width_px=stroke_width_px,
                note=note,
                timestamp_utc=core.utc_now(),
            )
        )

        total_points = len(collected)
        required_total = required_curve_total(spec)

        print(
            f"Accepted S{segment_number:02d}: "
            f"{len(points)} points; "
            f"curve total {total_points}/{required_total} minimum."
        )

        if total_points < required_total:
            print(
                "Another visible segment is required to reach the "
                "frozen curve-total minimum."
            )
            segment_number += 1
            continue

        if prompt_yes_no(
            "Is there another disconnected visible fragment "
            "of this same labelled curve? [y/n]: "
        ):
            segment_number += 1
            continue

        break

    validate_rows(
        collected,
        specs=[spec],
        expected_pass=pass_number,
        require_complete_pass=False,
    )
    return collected


def print_registry(specs: Sequence[Any]) -> None:
    """Print the four curves and the segment-break rule."""
    for index, spec in enumerate(specs, start=1):
        guidance = CURVE_GUIDANCE[spec.landmark_id]
        print(f"{index}. {spec.landmark_id} ({guidance['short_name']})")
        print(f"   Feature: {spec.source_feature}")
        print(f"   Trace:   {guidance['instruction']}")
        print(f"   Break:   {guidance['breaks']}")
        print(
            f"   Minimum: {MINIMUM_POINTS_PER_SEGMENT} per segment; "
            f"{required_curve_total(spec)} total"
        )


def build_argument_parser() -> argparse.ArgumentParser:
    """Build the command-line interface."""
    parser = argparse.ArgumentParser(
        description=(
            "Blind segment-aware digitizer for the four "
            "First Hand labelled projected curves."
        )
    )

    parser.add_argument(
        "--pass-number",
        type=int,
        choices=(1, 2),
        help="Independent curve digitization pass.",
    )
    parser.add_argument(
        "--operator",
        help="Operator name stored in every row.",
    )
    parser.add_argument(
        "--landmark-id",
        action="append",
        default=[],
        help=(
            "Digitize one explicit curve ID. "
            "Repeat for multiple curves."
        ),
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List the four curves and exit.",
    )
    parser.add_argument(
        "--validate",
        type=Path,
        help="Validate a complete curve pass CSV and exit.",
    )
    parser.add_argument(
        "--replace",
        action="store_true",
        help=(
            "Replace the selected landmark(s) in this pass. "
            "Requires at least one --landmark-id."
        ),
    )
    parser.add_argument(
        "--restart-pass",
        action="store_true",
        help="Delete the selected curve pass file before acquisition.",
    )

    return parser


def main() -> int:
    """Run the blind segment-aware curve digitizer."""
    args = build_argument_parser().parse_args()
    specs = read_curve_specs()

    if args.list:
        print_registry(specs)
        return 0

    if args.validate is not None:
        rows = validate_output_file(
            args.validate,
            require_complete_pass=True,
        )
        grouped = group_rows(rows)
        print(
            f"Validated {len(rows)} rows, "
            f"{sum(len(value) for value in grouped.values())} segments, "
            f"{len(grouped)} curves in {args.validate}"
        )
        return 0

    if args.pass_number is None:
        raise RuntimeError("--pass-number is required for acquisition.")
    if not args.operator:
        raise RuntimeError("--operator is required for acquisition.")
    if args.replace and not args.landmark_id:
        raise RuntimeError(
            "--replace requires at least one --landmark-id."
        )

    output_path = output_path_for_pass(args.pass_number)

    if args.restart_pass and output_path.exists():
        output_path.unlink()

    existing_rows = read_existing_rows(output_path)

    if existing_rows:
        validate_rows(
            existing_rows,
            specs=specs,
            expected_pass=args.pass_number,
            require_complete_pass=False,
        )

    selected = select_specs(specs, args.landmark_id)
    current_rows = list(existing_rows)
    completed_ids = {row["landmark_id"] for row in current_rows}
    crops = core.read_crop_manifest()

    print("=" * 78)
    print("FIRST HAND LABELLED CURVES — BLIND SEGMENT-AWARE PASS")
    print("=" * 78)
    print(f"Pass:       {args.pass_number}")
    print(f"Operator:   {args.operator}")
    print(f"Output:     {output_path}")
    print("Loaded:     untouched prepared crop and registry guidance only")
    print(
        "Not loaded: other curve pass, neutral overlay, fitted curves, "
        "projective maps, or self-embedment results"
    )

    for index, spec in enumerate(selected, start=1):
        already_present = spec.landmark_id in completed_ids

        if already_present and not args.replace:
            print(
                f"[{index}/{len(selected)}] "
                f"SKIP existing {spec.landmark_id}"
            )
            continue

        if spec.crop_id not in crops:
            raise RuntimeError(f"Missing prepared crop: {spec.crop_id}")

        crop = crops[spec.crop_id]
        image = core.verify_crop(crop)

        replacement_rows = capture_curve(
            image=image,
            spec=spec,
            crop=crop,
            pass_number=args.pass_number,
            operator=args.operator,
        )

        # Preserve the prior landmark until a complete replacement has
        # validated successfully.
        current_rows = [
            row
            for row in current_rows
            if row["landmark_id"] != spec.landmark_id
        ]
        current_rows.extend(replacement_rows)

        write_rows(output_path, current_rows)

        validate_rows(
            current_rows,
            specs=specs,
            expected_pass=args.pass_number,
            require_complete_pass=False,
        )

        completed_ids.add(spec.landmark_id)

        print(
            f"Saved complete {spec.landmark_id}: "
            f"{len(replacement_rows)} rows."
        )

    require_complete = not args.landmark_id

    validated = validate_output_file(
        output_path,
        expected_pass=args.pass_number,
        require_complete_pass=require_complete,
    )
    grouped = group_rows(validated)

    print("\n" + "=" * 78)
    print("SEGMENT-AWARE CURVE PASS SAVED")
    print("=" * 78)
    print(f"Rows:       {len(validated)}")
    print(
        f"Segments:   "
        f"{sum(len(value) for value in grouped.values())}"
    )
    print(f"Curves:     {len(grouped)}")
    print(f"Path:       {output_path}")
    print(
        "No fragment was joined across an occlusion, and no curve fit "
        "or projective verdict was computed."
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
