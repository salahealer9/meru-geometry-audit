"""Tests for the First Hand neutral geometry census."""

from __future__ import annotations

import importlib.util
import math
import sys
from pathlib import Path
from typing import Any

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = ROOT / "scripts/audit_first_hand_neutral_geometry.py"


def load_module() -> Any:
    spec = importlib.util.spec_from_file_location("first_hand_neutral_geometry_audit", SCRIPT_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    try:
        spec.loader.exec_module(module)
    finally:
        sys.modules.pop(spec.name, None)
    return module


def test_checksum_manifest_matches_frozen_passes() -> None:
    module = load_module()
    entries = module.verify_checksum_manifest()
    assert set(entries) == {
        "diagram_landmarks_pass1.csv",
        "diagram_landmarks_pass2.csv",
    }


def test_raw_passes_have_expected_neutral_vocabulary() -> None:
    module = load_module()
    for pass_number, path in module.PASS_PATHS.items():
        rows = module.validate_pass(pass_number, path)
        grouped = module.group_rows(rows)
        assert set(grouped) == module.EXPECTED_IDS
        assert len(grouped[module.LIMB_ID]) >= 30
        for landmark_id in module.EXPECTED_IDS - {module.LIMB_ID}:
            assert len(grouped[landmark_id]) == 1


def test_circle_fit_recovers_synthetic_circle() -> None:
    module = load_module()
    angles = np.linspace(0.0, 2.0 * math.pi, 72, endpoint=False)
    center = np.asarray([17.25, -4.75])
    radius = 31.5
    points = np.c_[center[0] + radius*np.cos(angles), center[1] + radius*np.sin(angles)]
    fitted = module.fit_circle(points)
    assert abs(fitted["center_x_px"] - center[0]) < 1e-9
    assert abs(fitted["center_y_px"] - center[1]) < 1e-9
    assert abs(fitted["radius_px"] - radius) < 1e-9


def test_equal_pass_weights_do_not_favour_dense_pass() -> None:
    module = load_module()
    weights = module.equal_pass_weights(49, 40)
    assert abs(float(np.sum(weights[:49])) - 0.5) < 1e-15
    assert abs(float(np.sum(weights[49:])) - 0.5) < 1e-15


def test_sixfold_fit_recovers_regular_hexagon() -> None:
    module = load_module()
    phase = 17.25
    fitted = module.fit_regular_sixfold([phase + 60.0*index for index in range(6)])
    assert abs(module.wrap_period(fitted["phase_deg_mod_60"] - phase, 60.0)) < 1e-10
    assert fitted["bearing_rms_residual_deg"] < 1e-10
    assert fitted["gap_rms_residual_from_60_deg"] < 1e-10


def test_point_consensus_uses_floor_width_and_separation() -> None:
    module = load_module()

    def make_row(landmark_id: str, pass_number: int, x: float, width: float) -> dict[str, str]:
        return {
            "crop_id": "CROP",
            "crop_file_sha256": "a" * 64,
            "crop_pixel_sha256": "b" * 64,
            "landmark_id": landmark_id,
            "pass_number": str(pass_number),
            "operator": "operator",
            "sequence_index": "0",
            "x_px": str(x),
            "y_px": "0",
            "local_stroke_width_px": str(width),
            "object_type": "point",
            "fit_partition": "calibration",
            "source_feature": "feature",
            "operator_note": "",
            "timestamp_utc": "2026-07-31T00:00:00Z",
        }

    pass1, pass2 = [], []
    for index, landmark_id in enumerate(sorted(module.EXPECTED_IDS - {module.LIMB_ID})):
        pass1.append(make_row(landmark_id, 1, float(index), 4.0))
        pass2.append(make_row(landmark_id, 2, float(index)+8.0, 6.0))
    consensus = module.point_consensus(pass1, pass2)
    assert len(consensus) == 12
    for row in consensus:
        assert float(row["pass_separation_px"]) == 8.0
        assert float(row["consensus_uncertainty_px"]) == 4.0


def test_end_to_end_analysis_preserves_neutral_boundary() -> None:
    module = load_module()
    analysis, consensus_rows, passes = module.build_analysis()
    assert len(consensus_rows) == 12
    assert set(passes) == {1, 2}
    assert "No projection, scale, truncation, or self-embedment verdict" in analysis["verdict"]
    assert analysis["rim_node_census"]["interpretation_boundary"]
    assert set(analysis["scope"]["does_not_compute"]) >= {
        "projective map fit",
        "great-circle identity or endpoint assignment",
        "unit-angle scale selection",
    }


def test_script_declares_source_only_scope() -> None:
    text = SCRIPT_PATH.read_text(encoding="utf-8").lower()
    assert "does not fit a projective map" in text
    assert "assign great-circle endpoints" in text
    assert "self-embedment verdict" in text
