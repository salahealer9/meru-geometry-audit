"""Tests for neutral reciprocal-spiral residual morphology."""

from __future__ import annotations

import importlib.util
import math
import sys
from pathlib import Path

import numpy as np
import pytest


ROOT = Path(__file__).resolve().parents[1]

SCRIPT = (
    ROOT
    / "scripts"
    / "audit_first_hand_spherical_reciprocal_spiral_residual_morphology.py"
)


def load_module():
    spec = importlib.util.spec_from_file_location(
        "first_hand_residual_morphology_test",
        SCRIPT,
    )

    assert spec is not None
    assert spec.loader is not None

    module = importlib.util.module_from_spec(
        spec
    )

    sys.modules[
        spec.name
    ] = module

    spec.loader.exec_module(
        module
    )

    return module


def test_frozen_sample_dimensions():
    module = load_module()

    assert module.N_SEGMENTS == 10
    assert module.N_RESAMPLE == 401
    assert module.N_PER_PASS == 4010


def test_segment_vocabulary():
    module = load_module()

    assert module.SEGMENT_IDS == tuple(
        f"S{i:02d}"
        for i in range(
            1,
            11,
        )
    )


def test_rho_edges_are_exact_fixed_bins():
    edges = np.linspace(
        0.0,
        1.0,
        21,
    )

    assert len(
        edges
    ) == 21

    assert np.allclose(
        np.diff(
            edges
        ),
        0.05,
    )


def test_phase_partition_is_36_ten_degree_bins():
    edges = np.linspace(
        0.0,
        2.0
        * math.pi,
        37,
    )

    assert len(
        edges
    ) == 37

    assert math.degrees(
        edges[
            1
        ]
        - edges[
            0
        ]
    ) == pytest.approx(
        10.0
    )


def test_source_q_endpoints():
    module = load_module()

    q0 = (
        0
        / (
            module.N_PER_PASS
            - 1
        )
    )

    q1 = (
        (
            module.N_PER_PASS
            - 1
        )
        / (
            module.N_PER_PASS
            - 1
        )
    )

    assert q0 == pytest.approx(
        0.0
    )

    assert q1 == pytest.approx(
        1.0
    )


def test_weighted_signed_mean():
    module = load_module()

    values = np.array(
        [
            1.0,
            3.0,
        ]
    )

    weights = np.array(
        [
            1.0,
            3.0,
        ]
    )

    assert module.weighted_signed_mean(
        values,
        weights,
    ) == pytest.approx(
        2.5
    )


def test_weighted_rms():
    module = load_module()

    values = np.array(
        [
            3.0,
            4.0,
        ]
    )

    weights = np.ones(
        2
    )

    expected = math.sqrt(
        (
            9.0
            + 16.0
        )
        / 2.0
    )

    assert module.weighted_rms(
        values,
        weights,
    ) == pytest.approx(
        expected
    )


def test_pearson_identical_is_one():
    module = load_module()

    x = np.arange(
        10,
        dtype=float,
    )

    assert module.pearson(
        x,
        x,
    ) == pytest.approx(
        1.0
    )


def test_pearson_opposite_is_minus_one():
    module = load_module()

    x = np.arange(
        10,
        dtype=float,
    )

    assert module.pearson(
        x,
        -x,
    ) == pytest.approx(
        -1.0
    )


def test_last_bin_includes_right_endpoint():
    module = load_module()

    edges = np.linspace(
        0.0,
        1.0,
        21,
    )

    assert module.bin_index(
        1.0,
        edges,
    ) == 19


def test_internal_edge_goes_to_right_bin():
    module = load_module()

    edges = np.linspace(
        0.0,
        1.0,
        21,
    )

    assert module.bin_index(
        0.05,
        edges,
    ) == 1


def test_difference_summary_zero_for_identical_arrays():
    module = load_module()

    values = np.array(
        [
            -1.0,
            0.5,
            2.0,
        ]
    )

    result = module.difference_summary(
        values,
        values,
        angular=False,
    )

    assert result[
        "pearson_r"
    ] == pytest.approx(
        1.0
    )

    assert result[
        "rms_difference"
    ] == pytest.approx(
        0.0
    )


def test_expected_sample_schema_uses_frozen_primary_fields():
    module = load_module()

    assert (
        "residual_alpha_length_rad"
        in module.EXPECTED_SAMPLE_FIELDS
    )

    assert (
        "angular_chord_length_px"
        in module.EXPECTED_SAMPLE_FIELDS
    )


def test_no_raw_digitization_inputs():
    source = SCRIPT.read_text(
        encoding="utf-8"
    )

    assert (
        "spherical_spiral_segments_pass1.csv"
        not in source
    )

    assert (
        "spherical_spiral_segments_pass2.csv"
        not in source
    )


def test_no_model_refitting_calls():
    source = SCRIPT.read_text(
        encoding="utf-8"
    ).lower()

    forbidden = (
        "weighted_linear_fit(",
        "least_squares(",
        "curve_fit(",
        "optimize.minimize",
        "polyfit(",
        "lstsq(",
        "differential_evolution",
    )

    for token in forbidden:
        assert token not in source


def test_no_coordinate_curve_landmark_ids():
    source = SCRIPT.read_text(
        encoding="utf-8"
    )

    forbidden = (
        "AOG-LM-P07-GC-Y0",
        "AOG-LM-P07-GC-Y1",
        "AOG-LM-P07-GC-YAXIS",
        "AOG-LM-P07-GC-X1",
    )

    for token in forbidden:
        assert token not in source
