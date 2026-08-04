"""Tests for the First Hand segment-aware curve digitizer."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

SCRIPT_PATH = (
    ROOT
    / "scripts"
    / "digitize_first_hand_great_circle_segments.py"
)


def load_module() -> Any:
    """Load the curve digitizer without running its CLI."""
    spec = importlib.util.spec_from_file_location(
        "first_hand_segment_curve_digitizer",
        SCRIPT_PATH,
    )

    assert spec is not None
    assert spec.loader is not None

    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module

    try:
        spec.loader.exec_module(module)
    finally:
        sys.modules.pop(spec.name, None)

    return module


def synthetic_rows(
    module: Any,
    *,
    pass_number: int = 1,
    points_per_curve: int = 12,
    points_per_segment: int = 4,
) -> list[dict[str, str]]:
    """Build a complete synthetic four-curve pass."""
    rows: list[dict[str, str]] = []

    for curve_index, landmark_id in enumerate(module.CURVE_IDS):
        point_index = 0
        segment_number = 1

        while point_index < points_per_curve:
            segment_count = min(
                points_per_segment,
                points_per_curve - point_index,
            )
            segment_id = f"S{segment_number:02d}"

            for sequence_index in range(segment_count):
                rows.append(
                    {
                        "crop_id": "CROP",
                        "crop_file_sha256": "a" * 64,
                        "crop_pixel_sha256": "b" * 64,
                        "landmark_id": landmark_id,
                        "pass_number": str(pass_number),
                        "operator": "Test Operator",
                        "segment_id": segment_id,
                        "sequence_index": str(sequence_index),
                        "x_px": str(
                            100
                            + curve_index * 10
                            + point_index
                            + sequence_index
                        ),
                        "y_px": str(200 + curve_index),
                        "local_stroke_width_px": "5",
                        "source_feature": "feature",
                        "operator_note": "",
                        "timestamp_utc": "2026-07-31T00:00:00Z",
                    }
                )

            point_index += segment_count
            segment_number += 1

    return rows


def test_registry_selects_exactly_four_later_stage_curves() -> None:
    """The tool must expose only the four labelled projected curves."""
    module = load_module()
    specs = module.read_curve_specs()

    assert [
        spec.landmark_id
        for spec in specs
    ] == list(module.CURVE_IDS)

    assert all(
        spec.status == module.CURVE_STATUS
        for spec in specs
    )
    assert all(
        spec.object_type == "open_curve"
        for spec in specs
    )


def test_output_schema_preserves_segment_identity() -> None:
    """The dedicated CSV must carry a segment_id field."""
    module = load_module()

    assert "segment_id" in module.OUTPUT_FIELDS
    assert module.OUTPUT_FIELDS.index(
        "segment_id"
    ) < module.OUTPUT_FIELDS.index(
        "sequence_index"
    )

    assert module.output_path_for_pass(
        1
    ).name == "great_circle_segments_pass1.csv"

    assert module.output_path_for_pass(
        2
    ).name == "great_circle_segments_pass2.csv"


def test_complete_synthetic_pass_validates() -> None:
    """Four curves with independent fragments must validate."""
    module = load_module()
    specs = module.read_curve_specs()
    rows = synthetic_rows(module)

    module.validate_rows(
        rows,
        specs=specs,
        expected_pass=1,
        require_complete_pass=True,
    )


def test_short_segment_is_rejected() -> None:
    """A fragment with fewer than four samples must fail."""
    module = load_module()
    specs = module.read_curve_specs()
    rows = synthetic_rows(module)

    rows = [
        row
        for row in rows
        if not (
            row["landmark_id"] == module.CURVE_IDS[0]
            and row["segment_id"] == "S01"
            and int(row["sequence_index"]) == 3
        )
    ]

    try:
        module.validate_rows(
            rows,
            specs=specs,
            expected_pass=1,
            require_complete_pass=True,
        )
    except RuntimeError as error:
        assert "requires at least" in str(error)
    else:
        raise AssertionError(
            "A three-point visible segment was accepted."
        )


def test_noncontiguous_sequence_is_rejected() -> None:
    """Segment points may not silently jump over an index."""
    module = load_module()
    specs = module.read_curve_specs()
    rows = synthetic_rows(module)

    target = next(
        row
        for row in rows
        if (
            row["landmark_id"] == module.CURVE_IDS[0]
            and row["segment_id"] == "S01"
            and row["sequence_index"] == "3"
        )
    )
    target["sequence_index"] = "4"

    try:
        module.validate_rows(
            rows,
            specs=specs,
            expected_pass=1,
            require_complete_pass=True,
        )
    except RuntimeError as error:
        assert "contiguous from zero" in str(error)
    else:
        raise AssertionError(
            "A noncontiguous segment was accepted."
        )


def test_under_sampled_curve_is_rejected() -> None:
    """A curve needs at least twelve points across its fragments."""
    module = load_module()
    specs = module.read_curve_specs()
    rows = synthetic_rows(module)

    rows = [
        row
        for row in rows
        if not (
            row["landmark_id"] == module.CURVE_IDS[0]
            and row["segment_id"] == "S03"
        )
    ]

    try:
        module.validate_rows(
            rows,
            specs=specs,
            expected_pass=1,
            require_complete_pass=True,
        )
    except RuntimeError as error:
        assert "total points" in str(error)
    else:
        raise AssertionError(
            "An eight-point curve was accepted."
        )


def test_rows_for_segment_uses_local_sequence_only() -> None:
    """Each new visible fragment must restart sequence_index at zero."""
    module = load_module()
    specs = module.read_curve_specs()
    crop = type(
        "Crop",
        (),
        {
            "crop_id": "CROP",
            "file_sha256": "a" * 64,
            "pixel_sha256": "b" * 64,
        },
    )()

    rows = module.rows_for_segment(
        spec=specs[0],
        crop=crop,
        pass_number=2,
        operator="Test Operator",
        segment_number=3,
        points=[
            (1.0, 2.0),
            (2.0, 3.0),
            (3.0, 4.0),
            (4.0, 5.0),
        ],
        stroke_width_px=5.0,
        note="",
        timestamp_utc="2026-07-31T00:00:00Z",
    )

    assert {
        row["segment_id"]
        for row in rows
    } == {"S03"}

    assert [
        row["sequence_index"]
        for row in rows
    ] == ["0", "1", "2", "3"]


def test_script_declares_blind_no_bridge_boundary() -> None:
    """The source-only and no-interpolation boundary must be explicit."""
    text = " ".join(
        SCRIPT_PATH.read_text(
            encoding="utf-8",
        )
        .lower()
        .split()
    )

    assert "never joins fragments" in text
    assert "untouched prepared source crop" in text
    assert "never loads either curve pass" in text
    assert "no hidden interpolation" in text
    assert "separate segment" in text
    assert "projective maps" in text
    assert "self-embedment results" in text

    module = load_module()

    domain_rule = " ".join(
        module.CURVE_DOMAIN_RULE
        .lower()
        .split()
    )

    assert "outside the equator-at-horizon limb" in domain_rule
    assert "exterior arrow or label leader" in domain_rule


def test_y0_guidance_includes_dashed_backside() -> None:
    """GC-Y0 must include its source-rendered dashed continuation."""
    module = load_module()

    rule = " ".join(
        module.Y0_DASHED_BACKSIDE_RULE
        .lower()
        .split()
    )

    assert "dashed back-hemisphere continuation" in rule
    assert "regular dash spacing as line style" in rule
    assert "genuine occlusion" in rule



def test_scaffold_curve_remains_holdout() -> None:
    """The fifth curve must remain independent of calibration."""
    module = load_module()

    by_id = {
        spec.landmark_id: spec
        for spec in module.read_curve_specs()
    }

    holdout = by_id[
        "AOG-LM-P07-GC-SCAFFOLD-UR-UC-X1LL-LL"
    ]

    assert holdout.fit_partition == "scaffold_holdout"

    assert (
        "no planar coordinate-line identity assigned in advance"
        in holdout.geometry_role
    )

    assert (
        "do not fit projective map or scale"
        in holdout.allowed_use
    )
