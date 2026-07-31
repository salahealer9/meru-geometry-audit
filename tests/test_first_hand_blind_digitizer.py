"""Tests for the blind digitizer under revised landmark semantics."""

from __future__ import annotations

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
    """Load the digitizer without running its CLI."""
    spec = importlib.util.spec_from_file_location(
        "first_hand_blind_digitizer_revised",
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


def test_every_registered_crop_resolves() -> None:
    """All registry crop IDs must exist in the crop manifest."""
    module = load_module()

    landmarks = module.read_landmark_registry(
        REGISTRY_PATH
    )
    crops = module.read_crop_manifest(
        CROP_MANIFEST_PATH
    )

    assert {
        item.crop_id
        for item in landmarks
    } <= set(crops)


def test_default_selection_uses_only_initial_active_status() -> None:
    """Default selection must omit later, deferred, and external rows."""
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
        item.status == "preregistered_not_digitized"
        for item in selected
    )

    selected_ids = {
        item.landmark_id
        for item in selected
    }

    assert "AOG-LM-P07-GC-Y0" not in selected_ids
    assert "AOG-LM-P07-THIRTY-DEGREE-ARC" not in selected_ids
    assert "AOG-LM-P08-HAND-TOP-BOUNDARY" not in selected_ids


def test_explicit_selection_can_reach_later_stage_row() -> None:
    """A later-stage row remains addressable when deliberately named."""
    module = load_module()
    landmarks = module.read_landmark_registry(
        REGISTRY_PATH
    )

    selected = module.select_specs(
        all_specs=landmarks,
        landmark_ids=["AOG-LM-P07-GC-Y0"],
        partitions=module.DEFAULT_PARTITIONS,
    )

    assert len(selected) == 1
    assert selected[0].landmark_id == "AOG-LM-P07-GC-Y0"
    assert selected[0].status == "preregistered_later_stage"


def test_points_receive_one_click_per_pass() -> None:
    """Two-pass consensus comes from one point click in each pass."""
    module = load_module()

    landmarks = {
        item.landmark_id: item
        for item in module.read_landmark_registry(
            REGISTRY_PATH
        )
    }

    assert module.expected_samples_per_pass(
        landmarks["AOG-LM-P07-RIM-NODE-UL"]
    ) == 1

    assert module.expected_samples_per_pass(
        landmarks["AOG-LM-P07-CENTRAL-REFERENCE-NODE"]
    ) == 1

    assert module.expected_samples_per_pass(
        landmarks["AOG-LM-P07-EQUATOR-HORIZON-LIMB"]
    ) is None


def test_script_preserves_blind_boundary() -> None:
    """The source-only implementation must remain explicit."""
    text = SCRIPT_PATH.read_text(
        encoding="utf-8",
    ).lower()

    assert "model data:  not loaded" in text
    assert "source image is shown untouched" in text
    assert "previous-pass clicks" in text
    assert "self-embedment result was computed" in text
