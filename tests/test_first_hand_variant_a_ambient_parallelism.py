import math
import sys
from pathlib import Path

import numpy as np
import pytest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import first_hand_variant_a_ambient_parallelism as ambient  # noqa: E402


def test_registered_branch_count_and_ids_are_exact():
    assert len(ambient.REGISTERED_BRANCHES) == 2
    assert tuple(spec.branch_id for spec in ambient.REGISTERED_BRANCHES) == (
        "AMB-DIAGRAM-G30",
        "AMB-DIAGRAM-GHALF",
    )


def test_registered_scales_equal_frozen_s1_scales():
    by_scale = {spec.scale: spec.k for spec in ambient.REGISTERED_BRANCHES}
    assert by_scale == {
        "G30": ambient.K_G30,
        "GHALF": ambient.K_GHALF,
    }


def test_registered_endpoints_are_exact():
    assert ambient.THETA_OUTER == 1.0
    assert ambient.THETA_INNER == pytest.approx(
        1.0 + 3.0 * math.pi,
        rel=0.0,
        abs=0.0,
    )
    for spec in ambient.REGISTERED_BRANCHES:
        assert spec.theta_outer == 1.0
        assert spec.theta_inner == pytest.approx(
            1.0 + 3.0 * math.pi,
            rel=0.0,
            abs=0.0,
        )


def test_only_diagram_truncation_is_registered():
    assert {
        spec.truncation for spec in ambient.REGISTERED_BRANCHES
    } == {"AOG-DIAGRAM"}


def test_intrinsic_references_are_frozen_values():
    assert ambient.INTRINSIC_S1_REFERENCE_DEG == {
        "G30": 144.5776221089075,
        "GHALF": 144.2022631722743,
    }


def test_module_does_not_import_parallel_transport():
    assert "minimal_sphere_transport" not in ambient.__dict__
    assert "AntipodalTransportError" not in ambient.__dict__


def test_directed_equal_vectors_return_zero():
    record = ambient.ambient_angle_record([1.0, 0.0, 0.0], [1.0, 0.0, 0.0])
    assert record.delta_directed_rad == pytest.approx(0.0, abs=0.0)
    assert record.delta_line_rad == pytest.approx(0.0, abs=0.0)
    assert record.residual_directed == pytest.approx(0.0, abs=0.0)
    assert record.directed_state == "AMBIENT_DIRECTED_PARALLEL"
    assert record.line_state == "AMBIENT_LINE_PARALLEL"


def test_directed_antiparallel_returns_pi_but_line_returns_zero():
    record = ambient.ambient_angle_record([1.0, 0.0, 0.0], [-1.0, 0.0, 0.0])
    assert record.delta_directed_rad == pytest.approx(math.pi, abs=1e-15)
    assert record.delta_line_rad == pytest.approx(0.0, abs=1e-15)
    assert record.residual_directed == pytest.approx(2.0, abs=1e-15)
    assert record.directed_state == "AMBIENT_DIRECTED_NOT_PARALLEL"
    assert record.line_state == "AMBIENT_LINE_PARALLEL"


def test_orthogonal_vectors_return_half_pi_for_both():
    record = ambient.ambient_angle_record([1.0, 0.0, 0.0], [0.0, 1.0, 0.0])
    assert record.delta_directed_rad == pytest.approx(math.pi / 2.0, abs=1e-15)
    assert record.delta_line_rad == pytest.approx(math.pi / 2.0, abs=1e-15)


def test_angle_primitive_normalizes_inputs_without_changing_direction():
    record = ambient.ambient_angle_record([3.0, 0.0, 0.0], [0.0, -7.0, 0.0])
    assert record.delta_directed_rad == pytest.approx(math.pi / 2.0, abs=1e-15)
    assert record.delta_line_rad == pytest.approx(math.pi / 2.0, abs=1e-15)


@pytest.mark.parametrize("theta", [0.7, 2.3, 5.1])
@pytest.mark.parametrize("k", [ambient.K_G30, ambient.K_GHALF])
def test_frozen_curve_primitives_are_unit_and_tangent_away_from_registered_endpoints(theta, k):
    # These are deliberately non-registered theta values. No endpoint result is previewed.
    point = ambient.gamma_k(theta, k)
    tangent = ambient.directed_tangent(theta, k)

    assert np.linalg.norm(point) == pytest.approx(1.0, abs=1e-14)
    assert np.linalg.norm(tangent) == pytest.approx(1.0, abs=1e-14)
    assert float(np.dot(point, tangent)) == pytest.approx(0.0, abs=2e-13)


@pytest.mark.parametrize("theta", [0.7, 2.3, 5.1])
@pytest.mark.parametrize("k", [ambient.K_G30, ambient.K_GHALF])
def test_directed_tangent_orientation_matches_inner_to_outer_definition(theta, k):
    h = 1e-7
    p_minus = ambient.gamma_k(theta - h, k)
    p_plus = ambient.gamma_k(theta + h, k)
    numerical_plus_theta = p_plus - p_minus
    numerical_plus_theta /= np.linalg.norm(numerical_plus_theta)

    tangent = ambient.directed_tangent(theta, k)

    # inner->outer is decreasing theta, hence opposite +theta derivative.
    assert float(np.dot(tangent, numerical_plus_theta)) < -0.999999999


def test_line_angle_is_invariant_under_single_vector_sign_flip():
    a = np.array([1.0, 2.0, -0.5])
    b = np.array([-0.2, 1.3, 4.0])

    record_ab = ambient.ambient_angle_record(a, b)
    record_a_minus_b = ambient.ambient_angle_record(a, -b)

    assert record_ab.delta_line_rad == pytest.approx(
        record_a_minus_b.delta_line_rad,
        abs=1e-15,
    )


def test_directed_angle_changes_to_supplement_under_single_vector_sign_flip():
    a = np.array([1.0, 2.0, -0.5])
    b = np.array([-0.2, 1.3, 4.0])

    record_ab = ambient.ambient_angle_record(a, b)
    record_a_minus_b = ambient.ambient_angle_record(a, -b)

    assert (
        record_ab.delta_directed_rad
        + record_a_minus_b.delta_directed_rad
    ) == pytest.approx(math.pi, abs=1e-15)


def test_zero_vector_is_rejected():
    with pytest.raises(ValueError):
        ambient.ambient_angle_record([0.0, 0.0, 0.0], [1.0, 0.0, 0.0])


def test_registered_execution_is_not_called_by_primitive_tests(monkeypatch):
    def forbidden(*args, **kwargs):
        raise AssertionError(
            "Registered ambient endpoint evaluation is forbidden in primitive tests"
        )

    monkeypatch.setattr(ambient, "evaluate_registered_branch", forbidden)

    record = ambient.ambient_angle_record(
        [1.0, 1.0, 0.0],
        [1.0, 0.0, 1.0],
    )
    assert record.delta_directed_rad > 0.0
    assert record.delta_line_rad > 0.0


def test_cross_scale_summary_helpers_with_synthetic_results():
    # Synthetic states only; no endpoint geometry is evaluated.
    class Dummy:
        def __init__(self, directed_state, line_state):
            self.directed_state = directed_state
            self.line_state = line_state

    both_fail = [
        Dummy("AMBIENT_DIRECTED_NOT_PARALLEL", "AMBIENT_LINE_NOT_PARALLEL"),
        Dummy("AMBIENT_DIRECTED_NOT_PARALLEL", "AMBIENT_LINE_NOT_PARALLEL"),
    ]

    assert ambient.directed_cross_scale_summary(both_fail) == (
        "AMBIENT_DIRECTED_NOT_PARALLEL_ALL_SCALES"
    )
    assert ambient.line_cross_scale_summary(both_fail) == (
        "AMBIENT_LINE_NOT_PARALLEL_ALL_SCALES"
    )
