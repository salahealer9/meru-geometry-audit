"""Tests for the First Hand blind diagram digitizer."""

from __future__ import annotations

import csv
import importlib.util
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

SCRIPT_PATH = (
    ROOT
    / "scripts"
    / "digitize_first_hand_diagram_landmarks.py"
)

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


def load_module() -> Any:
    """Load the digitizer as a module without running its CLI."""
    spec = importlib.util.spec_from_file_location(
        "first_hand_blind_digitizer",
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


def test_digitizer_resolves_every_registered_crop() -> None:
    """All landmark crop IDs must exist in the frozen crop manifest."""
    module = load_module()

    landmarks = module.read_landmark_registry(
        REGISTRY_PATH
    )
    crops = module.read_crop_manifest(
        CROP_MANIFEST_PATH
    )

    assert landmarks
    assert crops

    assert {
        landmark.crop_id
        for landmark in landmarks
    } <= set(crops)


def test_per_pass_sample_rules_match_protocol() -> None:
    """Points get one independent click per pass; curves stay open-count."""
    module = load_module()

    landmarks = {
        item.landmark_id: item
        for item in module.read_landmark_registry(
            REGISTRY_PATH
        )
    }

    assert module.expected_samples_per_pass(
        landmarks["AOG-LM-P07-INFINITY-Y0-Y1"]
    ) == 1

    assert module.expected_samples_per_pass(
        landmarks["AOG-LM-P07-THIRTY-DEGREE-ARC"]
    ) == 3

    assert module.expected_samples_per_pass(
        landmarks["AOG-LM-P07-SPHERE-BOUNDARY"]
    ) is None

    assert module.expected_samples_per_pass(
        landmarks["AOG-LM-P07-SPIRAL-CENTRELINE"]
    ) is None


def test_default_selection_excludes_external_holdouts() -> None:
    """Page-8 Hand views must not enter the initial digitization."""
    module = load_module()
    landmarks = module.read_landmark_registry(
        REGISTRY_PATH
    )

    selected = module.select_specs(
        all_specs=landmarks,
        landmark_ids=[],
        partitions=module.DEFAULT_PARTITIONS,
    )

    assert selected

    assert all(
        item.fit_partition != "external_holdout"
        for item in selected
    )

    assert {
        item.fit_partition
        for item in selected
    } == {
        "calibration",
        "scale_calibration",
        "holdout",
    }


def test_digitizer_output_rows_preserve_source_identity() -> None:
    """Every output row must retain crop hashes and pass identity."""
    module = load_module()

    landmark = module.read_landmark_registry(
        REGISTRY_PATH
    )[0]

    crop = module.read_crop_manifest(
        CROP_MANIFEST_PATH
    )[landmark.crop_id]

    rows = module.rows_for_digitization(
        spec=landmark,
        crop=crop,
        pass_number=1,
        operator="Test Operator",
        points=[(12.5, 34.5), (20.0, 40.0)],
        stroke_width_px=6.0,
        note="test",
        timestamp_utc="2026-07-31T00:00:00Z",
    )

    assert len(rows) == 2

    for index, row in enumerate(rows):
        assert row["crop_id"] == crop.crop_id
        assert row["crop_file_sha256"] == crop.file_sha256
        assert row["crop_pixel_sha256"] == crop.pixel_sha256
        assert row["landmark_id"] == landmark.landmark_id
        assert row["pass_number"] == "1"
        assert row["operator"] == "Test Operator"
        assert row["sequence_index"] == str(index)
        assert row["local_stroke_width_px"] == "6"
        assert row["timestamp_utc"] == "2026-07-31T00:00:00Z"


def test_pass_file_schema_round_trip(tmp_path: Path) -> None:
    """The pass CSV schema must remain deterministic and validatable."""
    module = load_module()

    rows = [
        {
            "crop_id": "CROP",
            "crop_file_sha256": "a" * 64,
            "crop_pixel_sha256": "b" * 64,
            "landmark_id": "LANDMARK",
            "pass_number": "2",
            "operator": "Test Operator",
            "sequence_index": "0",
            "x_px": "12.5",
            "y_px": "34.5",
            "local_stroke_width_px": "5",
            "object_type": "point",
            "fit_partition": "calibration",
            "source_feature": "test feature",
            "operator_note": "",
            "timestamp_utc": "2026-07-31T00:00:00Z",
        }
    ]

    path = tmp_path / "pass2.csv"
    module.write_rows(path, rows)

    with path.open(
        newline="",
        encoding="utf-8",
    ) as handle:
        reader = csv.DictReader(handle)
        assert reader.fieldnames == module.OUTPUT_FIELDS

    validated = module.validate_output_file(
        path,
        expected_pass=2,
    )

    assert validated == rows


def test_script_declares_blind_source_only_boundary() -> None:
    """The implementation must explicitly keep model data unloaded."""
    text = SCRIPT_PATH.read_text(
        encoding="utf-8",
    ).lower()

    assert "model data:  not loaded" in text
    assert "source image is shown untouched" in text
    assert "previous-pass clicks" in text
    assert "self-embedment result was computed" in text
