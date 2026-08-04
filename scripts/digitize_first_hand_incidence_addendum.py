#!/usr/bin/env python3
"""Blind point-only digitizer for the First Hand incidence addendum.

This tool acquires only the three post-census incidence nodes registered
with status ``preregistered_incidence_addendum``. It does not load the
neutral census, the other addendum pass, curve traces, fitted geometry,
angle results, projective maps, or self-embedment scores.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any, Sequence


ROOT = Path(__file__).resolve().parents[1]

if str(ROOT) not in sys.path:
    sys.path.insert(
        0,
        str(ROOT),
    )

from scripts import digitize_first_hand_diagram_landmarks as core  # noqa: E402


DATA_DIR = (
    ROOT
    / "data"
    / "derived"
    / "first_hand_arm_of_god"
)

ADDENDUM_STATUS = "preregistered_incidence_addendum"

ADDENDUM_IDS = (
    "AOG-LM-P07-X1-UC-LL-INTERSECTION",
    "AOG-LM-P07-X1-UC-LR-INTERSECTION",
    "AOG-LM-P07-YAXIS-UC-UCLR-INTERSECTION",
)


def output_path_for_pass(
    pass_number: int,
) -> Path:
    """Return the dedicated addendum output path."""
    if pass_number not in {1, 2}:
        raise ValueError(
            "pass_number must be 1 or 2."
        )

    return (
        DATA_DIR
        / (
            "diagram_incidence_addendum_"
            f"pass{pass_number}.csv"
        )
    )


def read_addendum_specs() -> list[Any]:
    """Return exactly the three preregistered point specifications."""
    all_specs = core.read_landmark_registry()

    by_id = {
        spec.landmark_id: spec
        for spec in all_specs
    }

    missing = [
        landmark_id
        for landmark_id in ADDENDUM_IDS
        if landmark_id not in by_id
    ]

    if missing:
        raise RuntimeError(
            "Missing incidence-addendum registry IDs: "
            + ", ".join(missing)
        )

    status_ids = {
        spec.landmark_id
        for spec in all_specs
        if spec.status == ADDENDUM_STATUS
    }

    if status_ids != set(ADDENDUM_IDS):
        raise RuntimeError(
            "The incidence-addendum status vocabulary "
            "does not match the three frozen IDs."
        )

    selected = [
        by_id[landmark_id]
        for landmark_id in ADDENDUM_IDS
    ]

    for spec in selected:
        if spec.object_type != "point":
            raise RuntimeError(
                f"{spec.landmark_id} is not a point landmark."
            )

        if (
            core.expected_samples_per_pass(
                spec
            )
            != 1
        ):
            raise RuntimeError(
                f"{spec.landmark_id} must receive "
                "one click per pass."
            )

    return selected


def select_specs(
    specs: Sequence[Any],
    landmark_ids: Sequence[str],
) -> list[Any]:
    """Select all addendum points or an explicit subset."""
    if not landmark_ids:
        return list(specs)

    requested = set(
        landmark_ids
    )
    available = {
        spec.landmark_id
        for spec in specs
    }

    unknown = sorted(
        requested - available
    )

    if unknown:
        raise RuntimeError(
            "Unknown addendum landmark ID(s): "
            + ", ".join(unknown)
        )

    return [
        spec
        for spec in specs
        if spec.landmark_id in requested
    ]


def validate_addendum_rows(
    rows: Sequence[dict[str, str]],
    *,
    expected_pass: int | None,
    require_complete: bool,
) -> None:
    """Validate pass identity and the point-only addendum vocabulary."""
    if not rows:
        raise RuntimeError(
            "The addendum pass file is empty."
        )

    pass_numbers = {
        int(row["pass_number"])
        for row in rows
    }

    if len(pass_numbers) != 1:
        raise RuntimeError(
            "An addendum file contains multiple pass numbers."
        )

    actual_pass = next(
        iter(pass_numbers)
    )

    if actual_pass not in {1, 2}:
        raise RuntimeError(
            f"Invalid addendum pass number: {actual_pass}"
        )

    if (
        expected_pass is not None
        and actual_pass != expected_pass
    ):
        raise RuntimeError(
            f"Expected pass {expected_pass}, "
            f"received pass {actual_pass}."
        )

    ids = [
        row["landmark_id"]
        for row in rows
    ]
    id_set = set(ids)

    if not id_set <= set(ADDENDUM_IDS):
        raise RuntimeError(
            "Unexpected landmark ID in the addendum pass."
        )

    if len(ids) != len(id_set):
        raise RuntimeError(
            "Each addendum point must occur exactly once per pass."
        )

    if require_complete:
        if id_set != set(ADDENDUM_IDS):
            missing = sorted(
                set(ADDENDUM_IDS) - id_set
            )
            raise RuntimeError(
                "Incomplete addendum pass; missing: "
                + ", ".join(missing)
            )

        if len(rows) != 3:
            raise RuntimeError(
                "A complete addendum pass must contain "
                "exactly three rows."
            )

    for row in rows:
        if row["object_type"] != "point":
            raise RuntimeError(
                "The addendum pass contains a non-point object."
            )

        if (
            row["fit_partition"]
            != "calibration"
        ):
            raise RuntimeError(
                "Unexpected fit partition in addendum pass."
            )

        if (
            int(
                row["sequence_index"]
            )
            != 0
        ):
            raise RuntimeError(
                "Each point row must have sequence_index 0."
            )


def validate_addendum_file(
    path: Path,
    *,
    expected_pass: int | None = None,
    require_complete: bool = True,
) -> list[dict[str, str]]:
    """Validate one dedicated addendum pass CSV."""
    rows = core.validate_output_file(
        path,
        expected_pass=expected_pass,
    )

    validate_addendum_rows(
        rows,
        expected_pass=expected_pass,
        require_complete=require_complete,
    )

    return rows


def print_registry(
    specs: Sequence[Any],
) -> None:
    """Print the three source-visible nodes and acquisition guidance."""
    for index, spec in enumerate(
        specs,
        start=1,
    ):
        print(
            f"{index}. {spec.landmark_id}"
        )
        print(
            f"   Feature: {spec.source_feature}"
        )
        print(
            f"   Exclude: {spec.exclusions}"
        )


def build_argument_parser() -> argparse.ArgumentParser:
    """Build the command-line interface."""
    parser = argparse.ArgumentParser(
        description=(
            "Blind point-only digitizer for the "
            "First Hand incidence addendum."
        )
    )

    parser.add_argument(
        "--pass-number",
        type=int,
        choices=(1, 2),
        help="Independent addendum digitization pass.",
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
            "Digitize one explicit addendum ID. "
            "Repeat for multiple IDs."
        ),
    )

    parser.add_argument(
        "--list",
        action="store_true",
        help="List the three addendum landmarks and exit.",
    )

    parser.add_argument(
        "--validate",
        type=Path,
        help="Validate a complete addendum pass CSV and exit.",
    )

    parser.add_argument(
        "--replace",
        action="store_true",
        help=(
            "Replace an existing point in the selected pass. "
            "Without this flag, existing points are skipped."
        ),
    )

    parser.add_argument(
        "--restart-pass",
        action="store_true",
        help=(
            "Delete the selected addendum pass file "
            "before collecting points."
        ),
    )

    return parser


def main() -> int:
    """Run the dedicated incidence-addendum digitizer."""
    args = build_argument_parser().parse_args()

    specs = read_addendum_specs()

    if args.list:
        print_registry(
            specs
        )
        return 0

    if args.validate is not None:
        rows = validate_addendum_file(
            args.validate,
            require_complete=True,
        )
        print(
            f"Validated {len(rows)} rows "
            f"in {args.validate}"
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

    if (
        args.restart_pass
        and output_path.exists()
    ):
        output_path.unlink()

    existing_rows = core.read_existing_rows(
        output_path
    )

    if existing_rows:
        validate_addendum_rows(
            existing_rows,
            expected_pass=args.pass_number,
            require_complete=False,
        )

    selected = select_specs(
        specs,
        args.landmark_id,
    )

    current_rows = list(
        existing_rows
    )
    current_ids = core.existing_landmark_ids(
        current_rows
    )

    crops = core.read_crop_manifest()

    print("=" * 78)
    print("FIRST HAND INCIDENCE ADDENDUM — BLIND POINT PASS")
    print("=" * 78)
    print(f"Pass:       {args.pass_number}")
    print(f"Operator:   {args.operator}")
    print(f"Output:     {output_path}")
    print("Points:     3 source-visible incidence nodes")
    print(
        "Not loaded: other addendum pass, neutral census, "
        "overlays, angle results, curve fits, projective map, "
        "or self-embedment scores"
    )

    for index, spec in enumerate(
        selected,
        start=1,
    ):
        if (
            spec.landmark_id in current_ids
            and not args.replace
        ):
            print(
                f"[{index}/{len(selected)}] "
                f"SKIP existing {spec.landmark_id}"
            )
            continue

        if spec.crop_id not in crops:
            raise RuntimeError(
                f"Missing prepared crop: {spec.crop_id}"
            )

        crop = crops[
            spec.crop_id
        ]
        image = core.verify_crop(
            crop
        )

        print("\n" + "-" * 78)
        print(
            f"[{index}/{len(selected)}] "
            f"{spec.landmark_id}"
        )
        print(
            f"Feature:     {spec.source_feature}"
        )
        print(
            f"Role:        {spec.geometry_role}"
        )
        print(
            f"Exclude:     {spec.exclusions}"
        )
        print(
            f"Uncertainty: {spec.uncertainty_rule}"
        )

        input(
            "Press Enter to open the untouched source crop..."
        )

        points = core.collect_points(
            image=image,
            spec=spec,
            pass_number=args.pass_number,
        )

        stroke_width_px = core.prompt_stroke_width(
            spec
        )
        note = core.prompt_note()

        new_rows = core.rows_for_digitization(
            spec=spec,
            crop=crop,
            pass_number=args.pass_number,
            operator=args.operator,
            points=points,
            stroke_width_px=stroke_width_px,
            note=note,
            timestamp_utc=core.utc_now(),
        )

        if len(new_rows) != 1:
            raise RuntimeError(
                "An incidence point must produce exactly one row."
            )

        if spec.landmark_id in current_ids:
            current_rows = [
                row
                for row in current_rows
                if (
                    row["landmark_id"]
                    != spec.landmark_id
                )
            ]

        current_rows.extend(
            new_rows
        )

        core.write_rows(
            output_path,
            current_rows,
        )

        current_ids.add(
            spec.landmark_id
        )

        print(
            f"Saved {spec.landmark_id}."
        )

    validated = validate_addendum_file(
        output_path,
        expected_pass=args.pass_number,
        require_complete=True,
    )

    print("\n" + "=" * 78)
    print("INCIDENCE ADDENDUM PASS SAVED")
    print("=" * 78)
    print(f"Rows:       {len(validated)}")
    print(f"Landmarks:  {len(core.existing_landmark_ids(validated))}")
    print(f"Path:       {output_path}")
    print(
        "No angle, curve fit, projective fit, "
        "or self-embedment result was computed."
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
