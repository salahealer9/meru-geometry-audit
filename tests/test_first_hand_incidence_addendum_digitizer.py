"""Tests for the blind First Hand incidence-addendum digitizer."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

SCRIPT_PATH = (
    ROOT
    / "scripts"
    / "digitize_first_hand_incidence_addendum.py"
)


def load_module() -> Any:
    """Load the addendum digitizer without running its CLI."""
    spec = importlib.util.spec_from_file_location(
        "first_hand_incidence_addendum_digitizer",
        SCRIPT_PATH,
    )

    assert spec is not None
    assert spec.loader is not None

    module = importlib.util.module_from_spec(
        spec
    )
    sys.modules[
        spec.name
    ] = module

    try:
        spec.loader.exec_module(
            module
        )
    finally:
        sys.modules.pop(
            spec.name,
            None,
        )

    return module


def test_registry_selects_exactly_three_addendum_points() -> None:
    """The dedicated tool must expose only the three frozen IDs."""
    module = load_module()

    specs = module.read_addendum_specs()

    assert [
        spec.landmark_id
        for spec in specs
    ] == list(
        module.ADDENDUM_IDS
    )

    assert all(
        spec.status
        == module.ADDENDUM_STATUS
        for spec in specs
    )

    assert all(
        spec.object_type == "point"
        for spec in specs
    )


def test_output_paths_are_separate_from_original_passes() -> None:
    """Addendum observations must never enter the original pass CSVs."""
    module = load_module()

    pass1 = module.output_path_for_pass(
        1
    )
    pass2 = module.output_path_for_pass(
        2
    )

    assert pass1 != pass2
    assert pass1.name == (
        "diagram_incidence_addendum_pass1.csv"
    )
    assert pass2.name == (
        "diagram_incidence_addendum_pass2.csv"
    )

    assert "diagram_landmarks_pass" not in pass1.name
    assert "diagram_landmarks_pass" not in pass2.name


def test_explicit_selection_preserves_registry_order() -> None:
    """Explicit subsets must remain source-order deterministic."""
    module = load_module()
    specs = module.read_addendum_specs()

    selected = module.select_specs(
        specs,
        [
            module.ADDENDUM_IDS[2],
            module.ADDENDUM_IDS[0],
        ],
    )

    assert [
        spec.landmark_id
        for spec in selected
    ] == [
        module.ADDENDUM_IDS[0],
        module.ADDENDUM_IDS[2],
    ]


def test_complete_rows_require_three_unique_points() -> None:
    """A frozen addendum pass must contain one row per node."""
    module = load_module()

    rows = []

    for landmark_id in module.ADDENDUM_IDS:
        rows.append(
            {
                "crop_id": "CROP",
                "crop_file_sha256": "a" * 64,
                "crop_pixel_sha256": "b" * 64,
                "landmark_id": landmark_id,
                "pass_number": "1",
                "operator": "Test Operator",
                "sequence_index": "0",
                "x_px": "10",
                "y_px": "20",
                "local_stroke_width_px": "6",
                "object_type": "point",
                "fit_partition": "calibration",
                "source_feature": "feature",
                "operator_note": "",
                "timestamp_utc": "2026-07-31T00:00:00Z",
            }
        )

    module.validate_addendum_rows(
        rows,
        expected_pass=1,
        require_complete=True,
    )


def test_incomplete_rows_are_allowed_only_for_resume() -> None:
    """Interrupted passes may resume but cannot validate as complete."""
    module = load_module()

    row = {
        "crop_id": "CROP",
        "crop_file_sha256": "a" * 64,
        "crop_pixel_sha256": "b" * 64,
        "landmark_id": module.ADDENDUM_IDS[0],
        "pass_number": "2",
        "operator": "Test Operator",
        "sequence_index": "0",
        "x_px": "10",
        "y_px": "20",
        "local_stroke_width_px": "6",
        "object_type": "point",
        "fit_partition": "calibration",
        "source_feature": "feature",
        "operator_note": "",
        "timestamp_utc": "2026-07-31T00:00:00Z",
    }

    module.validate_addendum_rows(
        [row],
        expected_pass=2,
        require_complete=False,
    )

    try:
        module.validate_addendum_rows(
            [row],
            expected_pass=2,
            require_complete=True,
        )
    except RuntimeError:
        pass
    else:
        raise AssertionError(
            "Incomplete pass was accepted as complete."
        )


def test_script_declares_blind_interpretation_boundary() -> None:
    """The implementation must not expose prior results while clicking."""
    text = " ".join(
        SCRIPT_PATH.read_text(
            encoding="utf-8",
        )
        .lower()
        .split()
    )

    assert "does not load the neutral census" in text
    assert "the other addendum pass" in text
    assert "angle results" in text
    assert "projective maps" in text
    assert "self-embedment scores" in text
