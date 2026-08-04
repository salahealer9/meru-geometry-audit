import math
import sys
from pathlib import Path

import numpy as np
import pytest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import first_hand_s1_comparators as cmp  # noqa: E402


def test_primary_comparator_registry_is_exact():
    assert [c.comparator_id for c in cmp.PRIMARY_COMPARATORS] == [
        "ARCHIMEDES-ENDPOINT-MATCHED",
        "LOG-ENDPOINT-MATCHED",
        "GOLDEN-MEAN",
    ]


def test_primary_matrix_has_exactly_six_cells():
    assert len(cmp.PRIMARY_CELLS) == 6
    assert {(c.comparator_id, c.scale) for c in cmp.PRIMARY_CELLS} == {
        ("ARCHIMEDES-ENDPOINT-MATCHED", "G30"),
        ("ARCHIMEDES-ENDPOINT-MATCHED", "GHALF"),
        ("LOG-ENDPOINT-MATCHED", "G30"),
        ("LOG-ENDPOINT-MATCHED", "GHALF"),
        ("GOLDEN-MEAN", "G30"),
        ("GOLDEN-MEAN", "GHALF"),
    }


def test_log_grid_is_exact_and_closed():
    assert cmp.LOG_MULTIPLIERS == (0.50, 0.75, 1.00, 1.25, 1.50, 2.00)
    assert len(cmp.LOG_GRID_COMPARATORS) == 6
    assert len(cmp.LOG_GRID_CELLS) == 12
    assert len(cmp.REGISTERED_COMPARATOR_CELLS) == 18


def test_only_diagram_domain_is_registered():
    assert cmp.THETA0 == 1.0
    assert cmp.L == pytest.approx(3.0 * math.pi, abs=0.0)


def test_reciprocal_reference_values_are_frozen_not_recomputed():
    assert cmp.RECIPROCAL_DELTA_RAD == {
        "G30": 2.5233555305045834,
        "GHALF": 2.5168042811835494,
    }
    assert cmp.RECIPROCAL_DELTA_DEG == {
        "G30": 144.5776221089075,
        "GHALF": 144.2022631722743,
    }


def test_archimedean_endpoint_normalization():
    assert cmp.archimedean_radius(0.0) == pytest.approx(1.0, abs=0.0)
    assert cmp.archimedean_radius(cmp.L) == pytest.approx(
        cmp.Q_RECIPROCAL, abs=1e-15
    )


def test_endpoint_matched_log_normalization():
    curve = cmp.LOG_ENDPOINT_MATCHED
    assert curve.radius(0.0) == pytest.approx(1.0, abs=0.0)
    assert curve.radius(cmp.L) == pytest.approx(cmp.Q_RECIPROCAL, abs=1e-15)


def test_golden_mean_quarter_turn_definition():
    curve = cmp.GOLDEN_MEAN
    quarter_turn = math.pi / 2.0

    assert curve.radius(0.0) == pytest.approx(1.0, abs=0.0)
    assert curve.radius(quarter_turn) == pytest.approx(1.0 / cmp.PHI, abs=1e-15)
    assert curve.radius(cmp.L) == pytest.approx(cmp.PHI ** -6, abs=1e-15)


@pytest.mark.parametrize(
    "curve",
    [
        cmp.ARCHIMEDES,
        cmp.LOG_ENDPOINT_MATCHED,
        cmp.GOLDEN_MEAN,
    ],
)
@pytest.mark.parametrize("scale_k", [cmp.K_G30, cmp.K_GHALF])
@pytest.mark.parametrize("u", [0.0, 0.75, 2.0, 3.0 * math.pi])
def test_spherical_curve_lies_on_unit_sphere(curve, scale_k, u):
    point = cmp.spherical_curve(u, scale_k, curve.radius)
    assert np.linalg.norm(point) == pytest.approx(1.0, abs=1e-14)


@pytest.mark.parametrize(
    "curve",
    [
        cmp.ARCHIMEDES,
        cmp.LOG_ENDPOINT_MATCHED,
        cmp.GOLDEN_MEAN,
    ],
)
@pytest.mark.parametrize("scale_k", [cmp.K_G30, cmp.K_GHALF])
@pytest.mark.parametrize("u", [0.0, 0.75, 2.0, 3.0 * math.pi])
def test_spherical_derivative_is_tangent(curve, scale_k, u):
    point = cmp.spherical_curve(u, scale_k, curve.radius)
    derivative = cmp.spherical_curve_prime(
        u,
        scale_k,
        curve.radius,
        curve.radius_prime,
    )

    assert float(np.dot(point, derivative)) == pytest.approx(0.0, abs=1e-13)


@pytest.mark.parametrize(
    "curve",
    [
        cmp.ARCHIMEDES,
        cmp.LOG_ENDPOINT_MATCHED,
        cmp.GOLDEN_MEAN,
    ],
)
@pytest.mark.parametrize("scale_k", [cmp.K_G30, cmp.K_GHALF])
@pytest.mark.parametrize("u", [0.0, 1.0, 3.0 * math.pi])
def test_directed_tangent_is_unit_and_uses_decreasing_u(curve, scale_k, u):
    derivative = cmp.spherical_curve_prime(
        u,
        scale_k,
        curve.radius,
        curve.radius_prime,
    )
    tangent = cmp.directed_tangent_for_curve(u, scale_k, curve)

    expected = -derivative / np.linalg.norm(derivative)
    assert np.linalg.norm(tangent) == pytest.approx(1.0, abs=1e-14)
    assert tangent == pytest.approx(expected, abs=1e-14)


@pytest.mark.parametrize(
    "curve",
    [
        cmp.ARCHIMEDES,
        cmp.LOG_ENDPOINT_MATCHED,
        cmp.GOLDEN_MEAN,
    ],
)
def test_analytic_derivative_matches_centered_finite_difference_away_from_boundaries(
    curve,
):
    u = 1.4
    k = cmp.K_G30
    h = 1e-7

    analytic = cmp.spherical_curve_prime(
        u,
        k,
        curve.radius,
        curve.radius_prime,
    )
    finite = (
        cmp.spherical_curve(u + h, k, curve.radius)
        - cmp.spherical_curve(u - h, k, curve.radius)
    ) / (2.0 * h)

    assert analytic == pytest.approx(finite, abs=2e-9)


def test_grid_growth_rates_are_exact_preregistered_multiples():
    rates = [curve.growth_parameter for curve in cmp.LOG_GRID_COMPARATORS]
    expected = [m * cmp.B_ENDPOINT_MATCHED for m in cmp.LOG_MULTIPLIERS]
    assert rates == pytest.approx(expected, rel=0.0, abs=0.0)


def test_no_curve_uses_image_data_or_free_fit_parameters():
    for curve in cmp.ALL_COMPARATORS:
        assert callable(curve.radius)
        assert callable(curve.radius_prime)
        assert curve.comparator_id
        assert curve.normalization


def test_primitive_tests_do_not_evaluate_registered_comparator_cells(monkeypatch):
    def forbidden(*args, **kwargs):
        raise AssertionError(
            "Registered comparator execution is forbidden in primitive tests"
        )

    monkeypatch.setattr(cmp, "evaluate_comparator_cell", forbidden)

    curve = cmp.ARCHIMEDES
    point = cmp.spherical_curve(1.2, cmp.K_G30, curve.radius)
    tangent = cmp.directed_tangent_for_curve(1.2, cmp.K_G30, curve)

    assert np.linalg.norm(point) == pytest.approx(1.0, abs=1e-14)
    assert np.linalg.norm(tangent) == pytest.approx(1.0, abs=1e-14)
