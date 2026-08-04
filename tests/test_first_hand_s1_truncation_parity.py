import math
import sys
from pathlib import Path

import numpy as np
import pytest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import first_hand_s1_truncation_parity as parity  # noqa: E402


def test_registered_turn_set_is_exact():
    assert parity.TURNS == (1.0, 1.5, 2.0, 2.5)
    assert parity.NEW_TURNS == (1.0, 2.0, 2.5)
    assert parity.REFERENCE_TURN == 1.5
    assert parity.SPANS == {
        1.0: 2.0 * math.pi,
        1.5: 3.0 * math.pi,
        2.0: 4.0 * math.pi,
        2.5: 5.0 * math.pi,
    }


def test_registered_parity_classes_are_exact():
    assert parity.INTEGER_TURNS == (1.0, 2.0)
    assert parity.ODD_HALF_TURNS == (1.5, 2.5)
    assert parity.parity_class(1.0) == "INTEGER_TURN"
    assert parity.parity_class(2.0) == "INTEGER_TURN"
    assert parity.parity_class(1.5) == "ODD_HALF_INTEGER_TURN"
    assert parity.parity_class(2.5) == "ODD_HALF_INTEGER_TURN"


def test_fixed_logarithmic_rates_match_previous_preregistration():
    assert parity.LOG_MULTIPLIERS == (0.50, 0.75, 1.00, 1.25, 1.50, 2.00)
    assert parity.B_STAR == pytest.approx(
        math.log(1.0 + 3.0 * math.pi) / (3.0 * math.pi),
        rel=0.0,
        abs=0.0,
    )
    for multiplier in parity.LOG_MULTIPLIERS:
        assert parity.LOG_RATES[multiplier] == pytest.approx(
            multiplier * parity.B_STAR,
            rel=0.0,
            abs=0.0,
        )


def test_golden_rate_is_exact():
    expected = 2.0 * math.log(parity.PHI) / math.pi
    assert parity.B_GOLDEN == pytest.approx(expected, rel=0.0, abs=0.0)


def test_new_cell_count_is_exactly_54():
    assert len(parity.REGISTERED_NEW_CELLS) == 54


def test_no_new_cell_uses_reference_1_5_turn_span():
    assert all(cell.turns != 1.5 for cell in parity.REGISTERED_NEW_CELLS)
    assert all(
        cell.span_rad != pytest.approx(3.0 * math.pi)
        for cell in parity.REGISTERED_NEW_CELLS
    )


def test_new_cell_family_counts_are_exact():
    log_cells = [
        c for c in parity.REGISTERED_NEW_CELLS
        if c.family == "Logarithmic"
    ]
    golden_cells = [
        c for c in parity.REGISTERED_NEW_CELLS
        if c.family == "Golden Mean logarithmic"
    ]
    reciprocal_cells = [
        c for c in parity.REGISTERED_NEW_CELLS
        if c.family == "Reciprocal"
    ]
    arch_cells = [
        c for c in parity.REGISTERED_NEW_CELLS
        if c.family == "Archimedean"
    ]

    assert len(log_cells) == 36
    assert len(golden_cells) == 6
    assert len(reciprocal_cells) == 6
    assert len(arch_cells) == 6


def test_reference_log_grid_is_complete_and_immutable_shape():
    assert len(parity.REFERENCE_LOG_GRID_DEG) == 12
    assert set(scale for scale, _ in parity.REFERENCE_LOG_GRID_DEG) == {
        "G30",
        "GHALF",
    }
    assert set(mult for _, mult in parity.REFERENCE_LOG_GRID_DEG) == set(
        parity.LOG_MULTIPLIERS
    )


def test_reference_records_are_marked_inherited_and_only_1_5_turn():
    records = parity.reference_records()
    # 6 log + golden + reciprocal + arch = 9 curves x 2 scales = 18 refs.
    assert len(records) == 18
    assert all(r["record_origin"] == "inherited_reference" for r in records)
    assert all(r["turns"] == 1.5 for r in records)
    assert all(r["span_rad"] == pytest.approx(3.0 * math.pi) for r in records)


@pytest.mark.parametrize("multiplier", parity.LOG_MULTIPLIERS)
def test_planar_log_integer_turn_tangents_are_parallel(multiplier):
    b = parity.LOG_RATES[multiplier]
    t0 = parity.planar_log_tangent_vector(0.0, b)

    for span in (2.0 * math.pi, 4.0 * math.pi):
        t1 = parity.planar_log_tangent_vector(span, b)
        u0 = t0 / np.linalg.norm(t0)
        u1 = t1 / np.linalg.norm(t1)
        assert u1 == pytest.approx(u0, abs=2e-14)


@pytest.mark.parametrize("multiplier", parity.LOG_MULTIPLIERS)
def test_planar_log_odd_half_turn_tangents_are_antiparallel(multiplier):
    b = parity.LOG_RATES[multiplier]
    t0 = parity.planar_log_tangent_vector(0.0, b)

    for span in (3.0 * math.pi, 5.0 * math.pi):
        t1 = parity.planar_log_tangent_vector(span, b)
        u0 = t0 / np.linalg.norm(t0)
        u1 = t1 / np.linalg.norm(t1)
        assert u1 == pytest.approx(-u0, abs=2e-14)


def test_planar_parity_theorem_is_independent_of_b():
    for b in (0.01, 0.2, 0.8, 2.5):
        t0 = parity.planar_log_tangent_vector(0.0, b)
        u0 = t0 / np.linalg.norm(t0)

        t_even = parity.planar_log_tangent_vector(4.0 * math.pi, b)
        u_even = t_even / np.linalg.norm(t_even)

        t_odd = parity.planar_log_tangent_vector(5.0 * math.pi, b)
        u_odd = t_odd / np.linalg.norm(t_odd)

        assert u_even == pytest.approx(u0, abs=2e-14)
        assert u_odd == pytest.approx(-u0, abs=2e-14)


@pytest.mark.parametrize(
    "turns",
    [1.0, 2.0, 2.5],
)
@pytest.mark.parametrize(
    "curve",
    [
        parity.LOG_CURVES[0],
        parity.LOG_CURVES[-1],
        parity.GOLDEN_CURVE,
        parity.RECIPROCAL_CURVE,
        parity.ARCHIMEDES_CURVE,
    ],
)
@pytest.mark.parametrize(
    "k",
    [parity.K_G30, parity.K_GHALF],
)
def test_generic_spherical_curve_lies_on_unit_sphere(turns, curve, k):
    span = parity.SPANS[turns]
    # Primitive evaluation away from the S1 comparison; no transport is run.
    u = 0.37 * span
    point = parity.spherical_curve(u, span, k, curve)
    assert np.linalg.norm(point) == pytest.approx(1.0, abs=1e-14)


@pytest.mark.parametrize(
    "turns",
    [1.0, 2.0, 2.5],
)
@pytest.mark.parametrize(
    "curve",
    [
        parity.LOG_CURVES[0],
        parity.LOG_CURVES[-1],
        parity.GOLDEN_CURVE,
        parity.RECIPROCAL_CURVE,
        parity.ARCHIMEDES_CURVE,
    ],
)
@pytest.mark.parametrize(
    "k",
    [parity.K_G30, parity.K_GHALF],
)
def test_generic_spherical_derivative_is_tangent(turns, curve, k):
    span = parity.SPANS[turns]
    u = 0.41 * span
    point = parity.spherical_curve(u, span, k, curve)
    derivative = parity.spherical_curve_prime(u, span, k, curve)

    assert float(np.dot(point, derivative)) == pytest.approx(0.0, abs=2e-13)


@pytest.mark.parametrize("turns", [1.0, 2.0, 2.5])
def test_archimedean_endpoint_matching(turns):
    span = parity.SPANS[turns]
    q = parity.reciprocal_inner_radius(span)

    assert parity.archimedean_radius(0.0, span) == pytest.approx(1.0, abs=0.0)
    assert parity.archimedean_radius(span, span) == pytest.approx(q, abs=1e-15)
    assert parity.reciprocal_radius(0.0, span) == pytest.approx(1.0, abs=0.0)
    assert parity.reciprocal_radius(span, span) == pytest.approx(q, abs=1e-15)


@pytest.mark.parametrize("turns", [1.0, 2.0, 2.5])
def test_fixed_log_rate_is_not_renormalized_when_span_changes(turns):
    span = parity.SPANS[turns]
    curve = parity.LOG_CURVES[2]  # m = 1.00
    b = parity.B_STAR

    assert curve.growth_parameter == pytest.approx(b, rel=0.0, abs=0.0)
    assert curve.radius(span, span) == pytest.approx(
        math.exp(-b * span),
        abs=1e-15,
    )


def test_primitive_tests_do_not_evaluate_new_s1_cells(monkeypatch):
    def forbidden(*args, **kwargs):
        raise AssertionError(
            "New registered parity execution is forbidden in primitive tests"
        )

    monkeypatch.setattr(parity, "evaluate_new_cell", forbidden)

    span = parity.SPANS[1.0]
    curve = parity.LOG_CURVES[0]
    point = parity.spherical_curve(0.5, span, parity.K_G30, curve)
    tangent = parity.directed_tangent(0.5, span, parity.K_G30, curve)

    assert np.linalg.norm(point) == pytest.approx(1.0, abs=1e-14)
    assert np.linalg.norm(tangent) == pytest.approx(1.0, abs=1e-14)
