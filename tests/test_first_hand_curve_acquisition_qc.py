"""Synthetic tests for First Hand acquisition-QC transformation."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]

SCRIPT = (
    ROOT
    / "scripts"
    / "apply_first_hand_curve_acquisition_qc.py"
)


def load_module():
    spec = importlib.util.spec_from_file_location(
        "first_hand_curve_acquisition_qc",
        SCRIPT,
    )

    if (
        spec is None
        or spec.loader is None
    ):
        raise RuntimeError(
            "Could not load QC module."
        )

    module = (
        importlib.util.module_from_spec(
            spec
        )
    )

    sys.modules[
        spec.name
    ] = module

    spec.loader.exec_module(
        module
    )

    return module


def row(
    index: int,
    x: str,
    y: str,
    timestamp: str = "2026-08-03T08:37:42Z",
) -> dict[str, str]:
    return {
        "pass_number": "2",
        "landmark_id": "X1",
        "segment_id": "S01",
        "sequence_index": str(index),
        "x_px": x,
        "y_px": y,
        "timestamp_utc": timestamp,
    }


def exclusion(
    start: int = 0,
    end: int = 2,
) -> dict[str, str]:
    return {
        "pass_number": "2",
        "landmark_id": "X1",
        "segment_id": "S01",
        "sequence_index_start": str(start),
        "sequence_index_end": str(end),
        "exclusion_code": (
            "exact_duplicate_input_event_burst"
        ),
        "reason": "synthetic duplicate burst",
    }


def test_exact_duplicate_prefix_is_valid() -> None:
    module = load_module()

    rows = [
        row(0, "10.0", "20.0"),
        row(1, "10.0", "20.0"),
        row(2, "10.0", "20.0"),
        row(3, "30.0", "40.0"),
        row(4, "31.0", "41.0"),
    ]

    result = module.validate_exclusion(
        rows,
        exclusion(),
    )

    assert (
        result[
            "excluded_row_count"
        ]
        == 3
    )

    assert (
        result[
            "first_retained_sequence_index"
        ]
        == 3
    )


def test_qc_preserves_original_sequence_indices() -> None:
    module = load_module()

    rows = [
        row(0, "10.0", "20.0"),
        row(1, "10.0", "20.0"),
        row(2, "10.0", "20.0"),
        row(3, "30.0", "40.0"),
        row(4, "31.0", "41.0"),
    ]

    result = module.apply_exclusions(
        rows,
        [
            exclusion()
        ],
    )

    assert [
        item[
            "sequence_index"
        ]
        for item in result
    ] == [
        "3",
        "4",
    ]


def test_nonidentical_coordinates_are_rejected() -> None:
    module = load_module()

    rows = [
        row(0, "10.0", "20.0"),
        row(1, "10.0", "20.0"),
        row(2, "10.1", "20.0"),
        row(3, "30.0", "40.0"),
    ]

    with pytest.raises(
        RuntimeError,
        match="identical coordinates",
    ):
        module.validate_exclusion(
            rows,
            exclusion(),
        )


def test_nonidentical_timestamps_are_rejected() -> None:
    module = load_module()

    rows = [
        row(
            0,
            "10.0",
            "20.0",
        ),
        row(
            1,
            "10.0",
            "20.0",
            "2026-08-03T08:37:43Z",
        ),
        row(
            2,
            "10.0",
            "20.0",
        ),
        row(
            3,
            "30.0",
            "40.0",
        ),
    ]

    with pytest.raises(
        RuntimeError,
        match="identical timestamp",
    ):
        module.validate_exclusion(
            rows,
            exclusion(),
        )


def test_nonprefix_exclusion_is_rejected() -> None:
    module = load_module()

    rows = [
        row(0, "1.0", "1.0"),
        row(1, "10.0", "20.0"),
        row(2, "10.0", "20.0"),
        row(3, "30.0", "40.0"),
    ]

    with pytest.raises(
        RuntimeError,
        match="segment prefix",
    ):
        module.validate_exclusion(
            rows,
            exclusion(
                start=1,
                end=2,
            ),
        )


def test_input_rows_are_not_mutated() -> None:
    module = load_module()

    rows = [
        row(0, "10.0", "20.0"),
        row(1, "10.0", "20.0"),
        row(2, "10.0", "20.0"),
        row(3, "30.0", "40.0"),
    ]

    original = [
        item.copy()
        for item in rows
    ]

    module.apply_exclusions(
        rows,
        [
            exclusion()
        ],
    )

    assert rows == original
