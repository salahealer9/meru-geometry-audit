#!/usr/bin/env python3
"""Apply documented acquisition-QC exclusions to First Hand curve data.

This script never modifies the raw acquisition file.

The current QC rule concerns a post-hoc diagnosed input-event burst in
pass-2 X1 S01. Exclusion eligibility is established from acquisition
metadata and exact coordinate duplication, not from geometric residuals.
"""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

DATA_DIR = (
    ROOT
    / "data"
    / "derived"
    / "first_hand_arm_of_god"
)

QC_DIR = DATA_DIR / "qc"

RAW_PASS2 = (
    DATA_DIR
    / "great_circle_segments_pass2.csv"
)

EXCLUSION_PATH = (
    QC_DIR
    / "curve_acquisition_qc_exclusions.csv"
)

OUTPUT_PASS2 = (
    QC_DIR
    / "great_circle_segments_pass2_qc.csv"
)

OUTPUT_MANIFEST = (
    QC_DIR
    / "great_circle_segments_pass2_qc_manifest.json"
)

OUTPUT_SHA256 = (
    QC_DIR
    / "great_circle_segments_pass2_qc.sha256"
)

SUPPORTED_CODE = (
    "exact_duplicate_input_event_burst"
)


def sha256_path(path: Path) -> str:
    digest = hashlib.sha256()

    with path.open("rb") as handle:
        for block in iter(
            lambda: handle.read(1 << 20),
            b"",
        ):
            digest.update(block)

    return digest.hexdigest()


def read_csv(
    path: Path,
) -> tuple[
    list[str],
    list[dict[str, str]],
]:
    with path.open(
        newline="",
        encoding="utf-8",
    ) as handle:
        reader = csv.DictReader(handle)

        fieldnames = list(
            reader.fieldnames
            or []
        )

        rows = list(reader)

    if not fieldnames:
        raise RuntimeError(
            f"No CSV header in {path}"
        )

    return fieldnames, rows


def read_exclusions(
    path: Path,
) -> list[dict[str, str]]:
    _, rows = read_csv(path)

    required = {
        "pass_number",
        "landmark_id",
        "segment_id",
        "sequence_index_start",
        "sequence_index_end",
        "exclusion_code",
        "reason",
    }

    if not rows:
        raise RuntimeError(
            "QC exclusion manifest is empty."
        )

    missing = (
        required
        - set(rows[0])
    )

    if missing:
        raise RuntimeError(
            "QC exclusion manifest is missing fields: "
            + ", ".join(
                sorted(missing)
            )
        )

    return rows


def matching_segment_rows(
    rows: list[dict[str, str]],
    exclusion: dict[str, str],
) -> list[dict[str, str]]:
    return [
        row
        for row in rows
        if (
            int(row["pass_number"])
            == int(
                exclusion[
                    "pass_number"
                ]
            )
            and row["landmark_id"]
            == exclusion[
                "landmark_id"
            ]
            and row["segment_id"]
            == exclusion[
                "segment_id"
            ]
        )
    ]


def validate_exclusion(
    rows: list[dict[str, str]],
    exclusion: dict[str, str],
) -> dict[str, Any]:
    """Validate one acquisition-derived exclusion.

    For exact_duplicate_input_event_burst, the excluded range must:
    - be a prefix of the segment;
    - contain consecutive sequence indices;
    - contain at least two observations;
    - have exactly identical x/y strings;
    - have exactly identical timestamps;
    - have a retained point immediately after the burst.

    No pass-to-pass geometric residual is consulted.
    """
    code = exclusion[
        "exclusion_code"
    ]

    if code != SUPPORTED_CODE:
        raise RuntimeError(
            f"Unsupported exclusion code: {code}"
        )

    segment_rows = matching_segment_rows(
        rows,
        exclusion,
    )

    if not segment_rows:
        raise RuntimeError(
            "QC exclusion target segment "
            "does not exist."
        )

    segment_rows = sorted(
        segment_rows,
        key=lambda row: int(
            row["sequence_index"]
        ),
    )

    start = int(
        exclusion[
            "sequence_index_start"
        ]
    )

    end = int(
        exclusion[
            "sequence_index_end"
        ]
    )

    if start > end:
        raise RuntimeError(
            "QC exclusion start exceeds end."
        )

    all_indices = [
        int(row["sequence_index"])
        for row in segment_rows
    ]

    if start != all_indices[0]:
        raise RuntimeError(
            "Duplicate-event exclusion must "
            "begin at the segment prefix."
        )

    expected_indices = list(
        range(
            start,
            end + 1,
        )
    )

    excluded_rows = [
        row
        for row in segment_rows
        if start
        <= int(
            row[
                "sequence_index"
            ]
        )
        <= end
    ]

    observed_indices = [
        int(
            row[
                "sequence_index"
            ]
        )
        for row in excluded_rows
    ]

    if observed_indices != expected_indices:
        raise RuntimeError(
            "Excluded sequence indices are "
            "not exactly consecutive."
        )

    if len(excluded_rows) < 2:
        raise RuntimeError(
            "Duplicate-event burst must contain "
            "at least two records."
        )

    coordinates = {
        (
            row["x_px"],
            row["y_px"],
        )
        for row in excluded_rows
    }

    if len(coordinates) != 1:
        raise RuntimeError(
            "Duplicate-event burst does not have "
            "exactly identical coordinates."
        )

    timestamps = {
        row["timestamp_utc"]
        for row in excluded_rows
    }

    if len(timestamps) != 1:
        raise RuntimeError(
            "Duplicate-event burst does not have "
            "one identical timestamp."
        )

    next_rows = [
        row
        for row in segment_rows
        if int(
            row[
                "sequence_index"
            ]
        )
        == end + 1
    ]

    if len(next_rows) != 1:
        raise RuntimeError(
            "Expected exactly one retained "
            "observation immediately after "
            "duplicate-event burst."
        )

    duplicate_x = float(
        excluded_rows[0][
            "x_px"
        ]
    )
    duplicate_y = float(
        excluded_rows[0][
            "y_px"
        ]
    )

    retained_x = float(
        next_rows[0][
            "x_px"
        ]
    )
    retained_y = float(
        next_rows[0][
            "y_px"
        ]
    )

    transition_px = (
        (
            retained_x
            - duplicate_x
        )
        ** 2
        + (
            retained_y
            - duplicate_y
        )
        ** 2
    ) ** 0.5

    return {
        "pass_number": int(
            exclusion[
                "pass_number"
            ]
        ),
        "landmark_id": exclusion[
            "landmark_id"
        ],
        "segment_id": exclusion[
            "segment_id"
        ],
        "sequence_index_start": start,
        "sequence_index_end": end,
        "excluded_row_count": len(
            excluded_rows
        ),
        "duplicate_x_px": duplicate_x,
        "duplicate_y_px": duplicate_y,
        "duplicate_timestamp_utc": (
            excluded_rows[0][
                "timestamp_utc"
            ]
        ),
        "first_retained_sequence_index": (
            end + 1
        ),
        "transition_to_first_retained_px": (
            transition_px
        ),
        "exclusion_code": code,
        "reason": exclusion[
            "reason"
        ],
    }


def row_is_excluded(
    row: dict[str, str],
    exclusion: dict[str, str],
) -> bool:
    if (
        int(row["pass_number"])
        != int(
            exclusion[
                "pass_number"
            ]
        )
    ):
        return False

    if (
        row["landmark_id"]
        != exclusion[
            "landmark_id"
        ]
    ):
        return False

    if (
        row["segment_id"]
        != exclusion[
            "segment_id"
        ]
    ):
        return False

    index = int(
        row[
            "sequence_index"
        ]
    )

    return (
        int(
            exclusion[
                "sequence_index_start"
            ]
        )
        <= index
        <= int(
            exclusion[
                "sequence_index_end"
            ]
        )
    )


def apply_exclusions(
    rows: list[dict[str, str]],
    exclusions: list[dict[str, str]],
) -> list[dict[str, str]]:
    """Return QC-derived rows without changing raw sequence indices."""
    return [
        row.copy()
        for row in rows
        if not any(
            row_is_excluded(
                row,
                exclusion,
            )
            for exclusion
            in exclusions
        )
    ]


def write_csv(
    path: Path,
    fieldnames: list[str],
    rows: list[dict[str, str]],
) -> None:
    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with path.open(
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
        writer.writerows(rows)


def build_qc_dataset(
    raw_path: Path = RAW_PASS2,
    exclusion_path: Path = EXCLUSION_PATH,
) -> tuple[
    list[str],
    list[dict[str, str]],
    dict[str, Any],
]:
    fieldnames, raw_rows = read_csv(
        raw_path
    )

    exclusions = read_exclusions(
        exclusion_path
    )

    validation = [
        validate_exclusion(
            raw_rows,
            exclusion,
        )
        for exclusion
        in exclusions
    ]

    qc_rows = apply_exclusions(
        raw_rows,
        exclusions,
    )

    expected_removed = sum(
        item[
            "excluded_row_count"
        ]
        for item
        in validation
    )

    actual_removed = (
        len(raw_rows)
        - len(qc_rows)
    )

    if (
        actual_removed
        != expected_removed
    ):
        raise RuntimeError(
            "QC removal count does not match "
            "validated exclusion count."
        )

    manifest = {
        "status": (
            "post_hoc_acquisition_qc_derivative"
        ),
        "raw_file": str(
            raw_path.relative_to(
                ROOT
            )
        ),
        "raw_file_sha256": sha256_path(
            raw_path
        ),
        "exclusion_manifest": str(
            exclusion_path.relative_to(
                ROOT
            )
        ),
        "exclusion_manifest_sha256": (
            sha256_path(
                exclusion_path
            )
        ),
        "raw_row_count": len(
            raw_rows
        ),
        "qc_row_count": len(
            qc_rows
        ),
        "excluded_row_count": (
            actual_removed
        ),
        "sequence_indices_renumbered": False,
        "raw_file_modified": False,
        "validation": validation,
        "interpretation": (
            "QC exclusion is based on exact "
            "duplicate acquisition events and "
            "metadata, not geometric-model fit."
        ),
    }

    return (
        fieldnames,
        qc_rows,
        manifest,
    )


def write_outputs() -> dict[str, Any]:
    (
        fieldnames,
        qc_rows,
        manifest,
    ) = build_qc_dataset()

    write_csv(
        OUTPUT_PASS2,
        fieldnames,
        qc_rows,
    )

    manifest[
        "qc_file"
    ] = str(
        OUTPUT_PASS2.relative_to(
            ROOT
        )
    )

    manifest[
        "qc_file_sha256"
    ] = sha256_path(
        OUTPUT_PASS2
    )

    OUTPUT_MANIFEST.write_text(
        json.dumps(
            manifest,
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )

    checksum_lines = [
        (
            f"{sha256_path(OUTPUT_PASS2)}  "
            f"{OUTPUT_PASS2.relative_to(ROOT)}"
        ),
        (
            f"{sha256_path(OUTPUT_MANIFEST)}  "
            f"{OUTPUT_MANIFEST.relative_to(ROOT)}"
        ),
    ]

    OUTPUT_SHA256.write_text(
        "\n".join(
            checksum_lines
        )
        + "\n",
        encoding="utf-8",
    )

    return manifest


def main() -> int:
    manifest = write_outputs()

    print(
        "First Hand acquisition-QC derivative created."
    )

    print(
        "Raw rows:",
        manifest[
            "raw_row_count"
        ],
    )

    print(
        "Excluded rows:",
        manifest[
            "excluded_row_count"
        ],
    )

    print(
        "QC rows:",
        manifest[
            "qc_row_count"
        ],
    )

    for item in manifest[
        "validation"
    ]:
        print(
            "Validated:",
            item[
                "landmark_id"
            ],
            item[
                "segment_id"
            ],
            f"indices "
            f"{item['sequence_index_start']}"
            f"-"
            f"{item['sequence_index_end']}",
            f"transition="
            f"{item['transition_to_first_retained_px']:.6f} px",
        )

    print(
        "Raw acquisition file was not modified."
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
