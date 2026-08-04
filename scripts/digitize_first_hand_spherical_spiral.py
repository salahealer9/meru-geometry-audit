#!/usr/bin/env python3
"""Blind segment-aware digitizer for the First Hand spherical spiral.

The tool displays only the untouched prepared page-7 spherical-projection
crop plus source-registry guidance for the spiral itself.

It never loads:
- the other spiral pass;
- frozen endpoint consensus coordinates;
- diagram landmark passes;
- great-circle acquisitions;
- neutral morphology;
- fitted maps;
- coordinate residuals;
- theoretical reciprocal-spiral projections.

Each continuously visible spiral fragment receives its own segment_id.
Hidden or unresolved portions are never interpolated.
"""

from __future__ import annotations

import argparse
import csv
import math
import sys
from pathlib import Path
from types import SimpleNamespace
from typing import Any, Sequence

import matplotlib.pyplot as plt
from PIL import Image


ROOT = Path(__file__).resolve().parents[1]

if str(ROOT) not in sys.path:
    sys.path.insert(
        0,
        str(ROOT),
    )

from scripts import digitize_first_hand_diagram_landmarks as core  # noqa: E402


OUTPUT_DIR = (
    ROOT
    / "data"
    / "derived"
    / "first_hand_arm_of_god"
)

SPIRAL_ID = (
    "AOG-LM-P07-SPIRAL-SPHERICAL"
)

CROP_ID = (
    "AOG_P07_SPHERICAL_PROJECTION"
)

EXPECTED_STATUS = (
    "preregistered_later_stage"
)

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

MINIMUM_POINTS_PER_SEGMENT = 4

SPIRAL_GUIDANCE = {
    "short_name": "SPHERICAL-SPIRAL",
    "instruction": (
        "Trace only the visible centreline of the thick "
        "reciprocal-spiral stroke inside the spherical panel."
    ),
    "breaks": (
        "Start a new segment at filled nodes, coordinate-line "
        "overprinting, labels, text, other source strokes, genuine "
        "visibility gaps, occlusions, or uncertain crossings. "
        "Do not interpolate any hidden continuation."
    ),
}

DOMAIN_RULE = (
    "Digitize only the source-visible thick spiral centreline at or "
    "inside the spherical limb. Do not trace annotation leaders, "
    "coordinate curves, the limb itself, or any theoretical continuation."
)


def output_path_for_pass(
    pass_number: int,
) -> Path:
    if pass_number not in {
        1,
        2,
    }:
        raise ValueError(
            "pass_number must be 1 or 2."
        )

    return (
        OUTPUT_DIR
        / f"spherical_spiral_segments_pass{pass_number}.csv"
    )


def seal_path_for_pass(
    pass_number: int,
) -> Path:
    if pass_number not in {
        1,
        2,
    }:
        raise ValueError(
            "pass_number must be 1 or 2."
        )

    return (
        OUTPUT_DIR
        / f"spherical_spiral_segments_pass{pass_number}.sha256"
    )


def read_spiral_spec() -> Any:
    specs = (
        core.read_landmark_registry()
    )

    matches = [
        spec
        for spec in specs
        if spec.landmark_id
        == SPIRAL_ID
    ]

    if len(matches) != 1:
        raise RuntimeError(
            "Expected exactly one spherical-spiral registry entry; "
            f"found {len(matches)}."
        )

    spec = matches[0]

    if (
        spec.crop_id
        != CROP_ID
    ):
        raise RuntimeError(
            "Spherical spiral is bound to an unexpected crop."
        )

    if (
        spec.object_type
        != "open_curve"
    ):
        raise RuntimeError(
            "Spherical spiral registry object must remain open_curve."
        )

    if (
        spec.status
        != EXPECTED_STATUS
    ):
        raise RuntimeError(
            "Spherical spiral registry status changed: "
            f"{spec.status!r}"
        )

    return spec


def required_total(
    spec: Any,
) -> int:
    value = int(
        spec.minimum_samples
    )

    return max(
        value,
        MINIMUM_POINTS_PER_SEGMENT,
    )


def group_rows(
    rows: Sequence[
        dict[str, str]
    ],
) -> dict[
    str,
    list[dict[str, str]],
]:
    grouped: dict[
        str,
        list[dict[str, str]],
    ] = {}

    for row in rows:
        segment_id = (
            row[
                "segment_id"
            ]
        )

        grouped.setdefault(
            segment_id,
            [],
        ).append(
            row
        )

    for segment_rows in (
        grouped.values()
    ):
        segment_rows.sort(
            key=lambda row: int(
                row[
                    "sequence_index"
                ]
            )
        )

    return dict(
        sorted(
            grouped.items()
        )
    )


def read_rows(
    path: Path,
) -> list[dict[str, str]]:
    if not path.exists():
        raise RuntimeError(
            f"Missing spiral pass: {path}"
        )

    with path.open(
        newline="",
        encoding="utf-8",
    ) as handle:
        reader = (
            csv.DictReader(
                handle
            )
        )

        if (
            reader.fieldnames
            != OUTPUT_FIELDS
        ):
            raise RuntimeError(
                "Unexpected spherical-spiral CSV schema."
            )

        return list(
            reader
        )


def validate_rows(
    rows: Sequence[
        dict[str, str]
    ],
    *,
    spec: Any,
    expected_pass: int | None = None,
) -> None:
    if not rows:
        raise RuntimeError(
            "Spherical-spiral pass is empty."
        )

    landmark_ids = {
        row[
            "landmark_id"
        ]
        for row in rows
    }

    if landmark_ids != {
        SPIRAL_ID
    }:
        raise RuntimeError(
            "Spiral pass contains an unexpected landmark ID."
        )

    crop_ids = {
        row[
            "crop_id"
        ]
        for row in rows
    }

    if crop_ids != {
        CROP_ID
    }:
        raise RuntimeError(
            "Spiral pass contains an unexpected crop ID."
        )

    pass_numbers = {
        int(
            row[
                "pass_number"
            ]
        )
        for row in rows
    }

    if len(
        pass_numbers
    ) != 1:
        raise RuntimeError(
            "Spiral pass contains multiple pass numbers."
        )

    actual_pass = next(
        iter(
            pass_numbers
        )
    )

    if actual_pass not in {
        1,
        2,
    }:
        raise RuntimeError(
            f"Invalid spiral pass number: {actual_pass}"
        )

    if (
        expected_pass is not None
        and actual_pass
        != expected_pass
    ):
        raise RuntimeError(
            f"Expected pass {expected_pass}; "
            f"received pass {actual_pass}."
        )

    if len(
        {
            row[
                "crop_file_sha256"
            ]
            for row in rows
        }
    ) != 1:
        raise RuntimeError(
            "Spiral pass contains multiple crop-file hashes."
        )

    if len(
        {
            row[
                "crop_pixel_sha256"
            ]
            for row in rows
        }
    ) != 1:
        raise RuntimeError(
            "Spiral pass contains multiple crop-pixel hashes."
        )

    grouped = (
        group_rows(
            rows
        )
    )

    numbers = sorted(
        int(
            segment_id[1:]
        )
        for segment_id
        in grouped
        if (
            len(
                segment_id
            )
            == 3
            and segment_id.startswith(
                "S"
            )
            and segment_id[
                1:
            ].isdigit()
        )
    )

    if len(
        numbers
    ) != len(
        grouped
    ):
        raise RuntimeError(
            "Invalid spiral segment ID."
        )

    expected_numbers = list(
        range(
            1,
            len(
                numbers
            )
            + 1,
        )
    )

    if (
        numbers
        != expected_numbers
    ):
        raise RuntimeError(
            "Spiral segment IDs must be contiguous from S01."
        )

    seen_keys: set[
        tuple[
            str,
            int,
        ]
    ] = set()

    for segment_id, segment_rows in (
        grouped.items()
    ):
        if len(
            segment_rows
        ) < MINIMUM_POINTS_PER_SEGMENT:
            raise RuntimeError(
                f"{segment_id} requires at least "
                f"{MINIMUM_POINTS_PER_SEGMENT} points."
            )

        indices = [
            int(
                row[
                    "sequence_index"
                ]
            )
            for row in segment_rows
        ]

        if indices != list(
            range(
                len(
                    segment_rows
                )
            )
        ):
            raise RuntimeError(
                f"{segment_id} sequence indices "
                "must be contiguous from zero."
            )

        for row in segment_rows:
            key = (
                segment_id,
                int(
                    row[
                        "sequence_index"
                    ]
                ),
            )

            if key in seen_keys:
                raise RuntimeError(
                    "Duplicate spiral "
                    f"segment/sequence row: {key}"
                )

            seen_keys.add(
                key
            )

            x = float(
                row[
                    "x_px"
                ]
            )

            y = float(
                row[
                    "y_px"
                ]
            )

            width = float(
                row[
                    "local_stroke_width_px"
                ]
            )

            if not (
                math.isfinite(
                    x
                )
                and math.isfinite(
                    y
                )
            ):
                raise RuntimeError(
                    "Non-finite spiral coordinate."
                )

            if not (
                math.isfinite(
                    width
                )
                and width > 0.0
            ):
                raise RuntimeError(
                    "Invalid local spiral stroke width."
                )

            if (
                row[
                    "source_feature"
                ]
                != spec.source_feature
            ):
                raise RuntimeError(
                    "Spiral source-feature text changed."
                )

    if len(
        rows
    ) < required_total(
        spec
    ):
        raise RuntimeError(
            "Spiral pass has only "
            f"{len(rows)} points; "
            f"{required_total(spec)} required."
        )


def validate_output_file(
    path: Path,
    *,
    expected_pass: int | None = None,
) -> list[dict[str, str]]:
    spec = (
        read_spiral_spec()
    )

    rows = (
        read_rows(
            path
        )
    )

    validate_rows(
        rows,
        spec=spec,
        expected_pass=expected_pass,
    )

    return rows


def write_rows(
    path: Path,
    rows: Sequence[
        dict[str, str]
    ],
) -> None:
    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    temporary = (
        path.with_suffix(
            path.suffix
            + ".tmp"
        )
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

        writer.writerows(
            rows
        )

    temporary.replace(
        path
    )


def collect_segment(
    *,
    image: Image.Image,
    spec: Any,
    pass_number: int,
    segment_number: int,
) -> list[
    tuple[
        float,
        float,
    ]
]:
    figure, axis = plt.subplots(
        num=(
            "First Hand blind spherical-spiral digitizer — "
            f"pass {pass_number} — "
            f"S{segment_number:02d}"
        ),
        figsize=(
            13,
            9,
        ),
    )

    axis.imshow(
        image
    )

    axis.set_xlim(
        0,
        image.width,
    )

    axis.set_ylim(
        image.height,
        0,
    )

    axis.set_aspect(
        "equal"
    )

    axis.set_title(
        (
            f"PASS {pass_number} | {SPIRAL_ID} | "
            f"SEGMENT S{segment_number:02d}\n"
            "Untouched source crop — do not bridge hidden "
            "or uncertain spiral portions"
        ),
        fontsize=11,
    )

    axis.set_xlabel(
        (
            "LEFT CLICK ordered centreline points. "
            "RIGHT CLICK removes the latest point. "
            "ENTER or MIDDLE CLICK finishes this visible segment.\n"
            f"{SPIRAL_GUIDANCE['instruction']}\n"
            f"{SPIRAL_GUIDANCE['breaks']}"
        ),
        fontsize=9,
    )

    # Deliberately no:
    # - prior spiral pass;
    # - endpoint landmark;
    # - node overlay;
    # - coordinate-curve overlay;
    # - fitted map;
    # - theoretical reciprocal spiral.
    points = plt.ginput(
        n=-1,
        timeout=0,
        show_clicks=True,
        mouse_add=1,
        mouse_pop=3,
        mouse_stop=2,
    )

    plt.close(
        figure
    )

    cleaned = [
        (
            float(
                x
            ),
            float(
                y
            ),
        )
        for x, y
        in points
    ]

    if len(
        cleaned
    ) < MINIMUM_POINTS_PER_SEGMENT:
        raise RuntimeError(
            "One visible spiral segment requires at least "
            f"{MINIMUM_POINTS_PER_SEGMENT} points; "
            f"received {len(cleaned)}."
        )

    for x, y in cleaned:
        if not (
            0.0
            <= x
            < image.width
            and 0.0
            <= y
            < image.height
        ):
            raise RuntimeError(
                f"Out-of-bounds point: ({x}, {y})."
            )

    return cleaned


def prompt_yes_no(
    prompt: str,
) -> bool:
    while True:
        answer = (
            input(
                prompt
            )
            .strip()
            .lower()
        )

        if answer in {
            "y",
            "yes",
        }:
            return True

        if answer in {
            "n",
            "no",
        }:
            return False

        print(
            "Please enter y or n.",
            file=sys.stderr,
        )


def rows_for_segment(
    *,
    spec: Any,
    crop: Any,
    pass_number: int,
    operator: str,
    segment_number: int,
    points: Sequence[
        tuple[
            float,
            float,
        ]
    ],
    stroke_width_px: float,
    note: str,
    timestamp_utc: str,
) -> list[
    dict[
        str,
        str,
    ]
]:
    segment_id = (
        f"S{segment_number:02d}"
    )

    return [
        {
            "crop_id": (
                crop.crop_id
            ),
            "crop_file_sha256": (
                crop.file_sha256
            ),
            "crop_pixel_sha256": (
                crop.pixel_sha256
            ),
            "landmark_id": (
                SPIRAL_ID
            ),
            "pass_number": str(
                pass_number
            ),
            "operator": (
                operator
            ),
            "segment_id": (
                segment_id
            ),
            "sequence_index": str(
                sequence_index
            ),
            "x_px": format(
                x,
                ".12g",
            ),
            "y_px": format(
                y,
                ".12g",
            ),
            "local_stroke_width_px": format(
                stroke_width_px,
                ".12g",
            ),
            "source_feature": (
                spec.source_feature
            ),
            "operator_note": (
                note
            ),
            "timestamp_utc": (
                timestamp_utc
            ),
        }
        for sequence_index, (
            x,
            y,
        )
        in enumerate(
            points
        )
    ]


def capture_spiral(
    *,
    image: Image.Image,
    spec: Any,
    crop: Any,
    pass_number: int,
    operator: str,
) -> list[
    dict[
        str,
        str,
    ]
]:
    collected: list[
        dict[
            str,
            str,
        ]
    ] = []

    segment_number = 1

    print(
        "\n"
        + "="
        * 78
    )

    print(
        f"{SPIRAL_ID} — "
        f"{SPIRAL_GUIDANCE['short_name']}"
    )

    print(
        f"Feature: {spec.source_feature}"
    )

    print(
        SPIRAL_GUIDANCE[
            "instruction"
        ]
    )

    print(
        SPIRAL_GUIDANCE[
            "breaks"
        ]
    )

    print(
        DOMAIN_RULE
    )

    print(
        "No hidden interpolation: every disconnected visible "
        "fragment must be a separate segment."
    )

    while True:
        input(
            "\nPress Enter to open untouched crop for "
            f"segment S{segment_number:02d}..."
        )

        try:
            points = (
                collect_segment(
                    image=image,
                    spec=spec,
                    pass_number=pass_number,
                    segment_number=segment_number,
                )
            )
        except RuntimeError as error:
            print(
                f"Segment rejected: {error}",
                file=sys.stderr,
            )

            if prompt_yes_no(
                "Retry this segment? [y/n]: "
            ):
                continue

            raise RuntimeError(
                "Cancelled spherical spiral acquisition "
                "before completion."
            ) from error

        stroke_width_px = (
            core.prompt_stroke_width(
                spec
            )
        )

        note = (
            core.prompt_note()
        )

        new_rows = (
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

        collected.extend(
            new_rows
        )

        print(
            f"Accepted S{segment_number:02d}: "
            f"{len(points)} points; "
            f"spiral total {len(collected)}/"
            f"{required_total(spec)} minimum."
        )

        if len(
            collected
        ) < required_total(
            spec
        ):
            print(
                "Another visible segment is required to reach "
                "the frozen total-point minimum."
            )

            segment_number += 1
            continue

        if prompt_yes_no(
            "Is there another disconnected visible fragment "
            "of the spherical spiral? [y/n]: "
        ):
            segment_number += 1
            continue

        break

    validate_rows(
        collected,
        spec=spec,
        expected_pass=pass_number,
    )

    return collected


def build_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Blind segment-aware digitizer for the First Hand "
            "page-7 spherical reciprocal spiral."
        )
    )

    parser.add_argument(
        "--pass-number",
        type=int,
        choices=(
            1,
            2,
        ),
        help=(
            "Independent spherical-spiral digitization pass."
        ),
    )

    parser.add_argument(
        "--operator",
        help=(
            "Operator name stored in every row."
        ),
    )

    parser.add_argument(
        "--validate",
        type=Path,
        help=(
            "Validate a frozen spherical-spiral pass and exit."
        ),
    )

    parser.add_argument(
        "--check-inputs",
        action="store_true",
        help=(
            "Verify registry and prepared crop without starting "
            "acquisition."
        ),
    )

    return parser


def main() -> int:
    args = (
        build_argument_parser()
        .parse_args()
    )

    spec = (
        read_spiral_spec()
    )

    crops = (
        core.read_crop_manifest()
    )

    if (
        spec.crop_id
        not in crops
    ):
        raise RuntimeError(
            f"Missing prepared crop: {spec.crop_id}"
        )

    crop = (
        crops[
            spec.crop_id
        ]
    )

    image = (
        core.verify_crop(
            crop
        )
    )

    if args.check_inputs:
        print(
            "Spherical spiral registry entry: VERIFIED"
        )

        print(
            "Prepared spherical-projection crop: VERIFIED"
        )

        print(
            "Landmark ID:",
            SPIRAL_ID,
        )

        print(
            "Crop ID:",
            CROP_ID,
        )

        print(
            "Minimum total points:",
            required_total(
                spec
            ),
        )

        print(
            "Minimum points per visible segment:",
            MINIMUM_POINTS_PER_SEGMENT,
        )

        print(
            "No prior spiral pass or endpoint consensus was loaded."
        )

        return 0

    if (
        args.validate
        is not None
    ):
        rows = (
            validate_output_file(
                args.validate
            )
        )

        grouped = (
            group_rows(
                rows
            )
        )

        print(
            f"Validated {len(rows)} rows, "
            f"{len(grouped)} visible segments "
            f"in {args.validate}"
        )

        return 0

    if (
        args.pass_number
        is None
    ):
        raise RuntimeError(
            "--pass-number is required for acquisition."
        )

    if not args.operator:
        raise RuntimeError(
            "--operator is required for acquisition."
        )

    output_path = (
        output_path_for_pass(
            args.pass_number
        )
    )

    seal_path = (
        seal_path_for_pass(
            args.pass_number
        )
    )

    if seal_path.exists():
        raise RuntimeError(
            "This spiral pass already has a frozen SHA-256 seal; "
            "refusing modification."
        )

    if output_path.exists():
        raise RuntimeError(
            "Spiral pass output already exists. "
            "This digitizer never overwrites a raw acquisition."
        )

    print(
        "="
        * 78
    )

    print(
        "FIRST HAND SPHERICAL SPIRAL — "
        "BLIND SEGMENT-AWARE PASS"
    )

    print(
        "="
        * 78
    )

    print(
        f"Pass:       {args.pass_number}"
    )

    print(
        f"Operator:   {args.operator}"
    )

    print(
        f"Output:     {output_path}"
    )

    print(
        "Loaded:     untouched prepared crop and "
        "spiral registry guidance"
    )

    print(
        "Not loaded: other spiral pass, endpoint consensus, "
        "great-circle traces, fitted geometry, projective maps, "
        "or theoretical reciprocal spiral"
    )

    rows = (
        capture_spiral(
            image=image,
            spec=spec,
            crop=crop,
            pass_number=args.pass_number,
            operator=args.operator,
        )
    )

    # The complete acquisition is validated in memory before any raw
    # pass file is created.
    validate_rows(
        rows,
        spec=spec,
        expected_pass=args.pass_number,
    )

    write_rows(
        output_path,
        rows,
    )

    validated = (
        validate_output_file(
            output_path,
            expected_pass=args.pass_number,
        )
    )

    grouped = (
        group_rows(
            validated
        )
    )

    print(
        "\n"
        + "="
        * 78
    )

    print(
        "SPHERICAL SPIRAL PASS SAVED"
    )

    print(
        "="
        * 78
    )

    print(
        f"Rows:       {len(validated)}"
    )

    print(
        f"Segments:   {len(grouped)}"
    )

    print(
        f"Path:       {output_path}"
    )

    print(
        "Raw pass has not yet been sealed."
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
