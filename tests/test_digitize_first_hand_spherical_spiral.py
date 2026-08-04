"""Synthetic tests for the blind First Hand spherical-spiral digitizer."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest


ROOT = Path(__file__).resolve().parents[1]

SCRIPT = (
    ROOT
    / "scripts"
    / "digitize_first_hand_spherical_spiral.py"
)


def load_module():
    spec = importlib.util.spec_from_file_location(
        "first_hand_spherical_spiral_digitizer_test",
        SCRIPT,
    )

    assert spec is not None
    assert spec.loader is not None

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


def fake_spec():
    return SimpleNamespace(
        landmark_id="AOG-LM-P07-SPIRAL-SPHERICAL",
        crop_id="AOG_P07_SPHERICAL_PROJECTION",
        object_type="open_curve",
        status="preregistered_later_stage",
        minimum_samples=12,
        source_feature="synthetic spiral",
    )


def fake_crop():
    return SimpleNamespace(
        crop_id="AOG_P07_SPHERICAL_PROJECTION",
        file_sha256="a" * 64,
        pixel_sha256="b" * 64,
    )


def rows(
    module,
    *,
    pass_number=1,
    segments=3,
    points_per_segment=4,
):
    result = []

    for segment_number in range(
        1,
        segments + 1,
    ):
        points = [
            (
                10.0 * segment_number + index,
                20.0 * segment_number + index,
            )
            for index in range(
                points_per_segment
            )
        ]

        result.extend(
            module.rows_for_segment(
                spec=fake_spec(),
                crop=fake_crop(),
                pass_number=pass_number,
                operator="Test Operator",
                segment_number=segment_number,
                points=points,
                stroke_width_px=6.0,
                note="synthetic",
                timestamp_utc="2026-08-04T00:00:00Z",
            )
        )

    return result


def test_pass_paths_are_distinct():
    module = load_module()

    assert (
        module.output_path_for_pass(1)
        != module.output_path_for_pass(2)
    )

    assert (
        module.seal_path_for_pass(1)
        != module.seal_path_for_pass(2)
    )


def test_invalid_pass_number_rejected():
    module = load_module()

    with pytest.raises(
        ValueError
    ):
        module.output_path_for_pass(
            3
        )

    with pytest.raises(
        ValueError
    ):
        module.seal_path_for_pass(
            0
        )


def test_valid_three_segment_pass():
    module = load_module()

    data = rows(
        module
    )

    module.validate_rows(
        data,
        spec=fake_spec(),
        expected_pass=1,
    )


def test_wrong_landmark_rejected():
    module = load_module()

    data = rows(
        module
    )

    data[0][
        "landmark_id"
    ] = "WRONG"

    with pytest.raises(
        RuntimeError
    ):
        module.validate_rows(
            data,
            spec=fake_spec(),
            expected_pass=1,
        )


def test_noncontiguous_segment_ids_rejected():
    module = load_module()

    data = rows(
        module,
        segments=3,
    )

    for row in data:
        if (
            row[
                "segment_id"
            ]
            == "S02"
        ):
            row[
                "segment_id"
            ] = "S04"

    with pytest.raises(
        RuntimeError
    ):
        module.validate_rows(
            data,
            spec=fake_spec(),
            expected_pass=1,
        )


def test_noncontiguous_sequence_rejected():
    module = load_module()

    data = rows(
        module
    )

    data[1][
        "sequence_index"
    ] = "8"

    with pytest.raises(
        RuntimeError
    ):
        module.validate_rows(
            data,
            spec=fake_spec(),
            expected_pass=1,
        )


def test_segment_minimum_enforced():
    module = load_module()

    data = rows(
        module,
        segments=4,
        points_per_segment=3,
    )

    with pytest.raises(
        RuntimeError
    ):
        module.validate_rows(
            data,
            spec=fake_spec(),
            expected_pass=1,
        )


def test_rows_for_segment_preserves_schema():
    module = load_module()

    generated = (
        module.rows_for_segment(
            spec=fake_spec(),
            crop=fake_crop(),
            pass_number=2,
            operator="Operator",
            segment_number=3,
            points=[
                (1.25, 2.5),
                (2.25, 3.5),
                (3.25, 4.5),
                (4.25, 5.5),
            ],
            stroke_width_px=8.0,
            note="visible run",
            timestamp_utc="2026-08-04T00:00:00Z",
        )
    )

    assert list(
        generated[0]
    ) == module.OUTPUT_FIELDS

    assert (
        generated[0][
            "segment_id"
        ]
        == "S03"
    )

    assert (
        generated[0][
            "landmark_id"
        ]
        == module.SPIRAL_ID
    )


def test_pass_identity_is_enforced():
    module = load_module()

    data = rows(
        module,
        pass_number=2,
    )

    with pytest.raises(
        RuntimeError
    ):
        module.validate_rows(
            data,
            spec=fake_spec(),
            expected_pass=1,
        )


def test_digitizer_does_not_reference_frozen_endpoint_ids():
    source = SCRIPT.read_text(
        encoding="utf-8",
    )

    forbidden = (
        "AOG-LM-P07-SPHERE-INNER-END",
        "AOG-LM-P07-RIM-NODE-LR-SHARED",
    )

    for token in forbidden:
        assert token not in source


def test_digitizer_does_not_load_derived_endpoint_consensus():
    source = SCRIPT.read_text(
        encoding="utf-8",
    )

    assert (
        "expanded_neutral_landmark_consensus"
        not in source
    )

    assert (
        "diagram_landmarks_pass1"
        not in source
    )

    assert (
        "diagram_landmarks_pass2"
        not in source
    )


def test_digitizer_does_not_load_coordinate_or_model_results():
    source = SCRIPT.read_text(
        encoding="utf-8",
    )

    forbidden = (
        "great_circle_segments_pass1.csv",
        "great_circle_segments_pass2.csv",
        "stereographic_plane_angles.json",
        "linear_central_projective_reconstruction.json",
        "three_curve_x1_reconciliation.json",
    )

    for token in forbidden:
        assert token not in source
