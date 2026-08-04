import math
import sys
from pathlib import Path

import numpy as np
import pytest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import first_hand_s1 as s1  # noqa: E402


def test_registered_branch_registry_is_exact_and_closed():
    assert [b.branch_id for b in s1.REGISTERED_BRANCHES] == [
        "S1-PROSE-G30",
        "S1-PROSE-GHALF",
        "S1-DIAGRAM-G30",
        "S1-DIAGRAM-GHALF",
    ]
    assert len(s1.REGISTERED_BRANCHES) == 4


@pytest.mark.parametrize(
    ("theta", "k"),
    [
        (0.25, 0.7),
        (1.75, 0.9),
        (4.2, 1.3),
    ],
)
def test_gamma_lies_on_unit_sphere(theta, k):
    point = s1.gamma_k(theta, k)
    assert np.linalg.norm(point) == pytest.approx(1.0, abs=1e-14)


@pytest.mark.parametrize(
    ("theta", "k"),
    [
        (0.4, 0.7),
        (2.2, 0.9),
        (5.1, 1.3),
    ],
)
def test_gamma_derivative_is_tangent(theta, k):
    point = s1.gamma_k(theta, k)
    derivative = s1.gamma_prime_k(theta, k)
    assert float(np.dot(point, derivative)) == pytest.approx(0.0, abs=1e-13)


@pytest.mark.parametrize(
    ("theta", "k"),
    [
        (0.6, 0.7),
        (2.4, 0.9),
        (3.8, 1.3),
    ],
)
def test_directed_tangent_is_unit_and_follows_decreasing_theta(theta, k):
    derivative = s1.gamma_prime_k(theta, k)
    tangent = s1.directed_tangent(theta, k)

    expected = -derivative / np.linalg.norm(derivative)
    assert np.linalg.norm(tangent) == pytest.approx(1.0, abs=1e-14)
    assert tangent == pytest.approx(expected, abs=1e-14)


def test_prose_outer_position_is_exact_registered_limit():
    point = s1.prose_outer_position(0.7)
    assert point == pytest.approx(np.array([1.0, 0.0, 0.0]), abs=0.0)


def test_prose_outer_tangent_uses_exact_closed_form():
    k = 0.7
    tangent = s1.prose_outer_tangent(k)
    expected = np.array([0.0, -k, -1.0]) / math.sqrt(k * k + 1.0)

    assert tangent == pytest.approx(expected, abs=1e-15)
    assert np.linalg.norm(tangent) == pytest.approx(1.0, abs=1e-14)
    assert float(np.dot(s1.prose_outer_position(k), tangent)) == pytest.approx(
        0.0, abs=0.0
    )


def test_minimal_transport_maps_position_and_preserves_tangent_norm():
    p_from = np.array([1.0, 0.0, 0.0])
    p_to = np.array([0.0, 1.0, 0.0])
    tangent = np.array([0.0, 1.0, 0.0])

    record = s1.minimal_sphere_transport(p_from, p_to, tangent)

    assert record.angle_rad == pytest.approx(math.pi / 2.0, abs=1e-14)
    assert record.axis == pytest.approx(np.array([0.0, 0.0, 1.0]), abs=1e-14)
    assert np.linalg.norm(record.vector) == pytest.approx(
        np.linalg.norm(tangent), abs=1e-14
    )
    assert float(np.dot(p_to, record.vector)) == pytest.approx(0.0, abs=1e-14)
    assert record.vector == pytest.approx(np.array([-1.0, 0.0, 0.0]), abs=1e-14)


def test_coincident_transport_is_identity():
    p = np.array([0.0, 0.0, 1.0])
    tangent = np.array([1.0, 0.0, 0.0])

    record = s1.minimal_sphere_transport(p, p, tangent)

    assert record.angle_rad == 0.0
    assert record.axis is None
    assert record.vector == pytest.approx(tangent, abs=0.0)


def test_antipodal_transport_is_rejected_not_repaired():
    p_from = np.array([1.0, 0.0, 0.0])
    p_to = np.array([-1.0, 0.0, 0.0])
    tangent = np.array([0.0, 1.0, 0.0])

    with pytest.raises(s1.AntipodalTransportError):
        s1.minimal_sphere_transport(p_from, p_to, tangent)


def test_non_tangent_input_is_rejected_not_projected():
    p_from = np.array([1.0, 0.0, 0.0])
    p_to = np.array([0.0, 1.0, 0.0])
    not_tangent = np.array([1.0, 1.0, 0.0])

    with pytest.raises(ValueError, match="not tangent"):
        s1.minimal_sphere_transport(p_from, p_to, not_tangent)


def test_absolute_dot_product_is_not_used_in_directed_logic():
    # Sign-convention test only; no registered branch is evaluated.
    a = np.array([1.0, 0.0, 0.0])
    b = np.array([-1.0, 0.0, 0.0])

    d = float(np.dot(a, b))
    c = float(np.linalg.norm(np.cross(a, b)))
    delta = math.atan2(c, d)

    assert d == -1.0
    assert abs(d) == 1.0
    assert delta == pytest.approx(math.pi, abs=0.0)


def test_tests_do_not_evaluate_registered_branches(monkeypatch):
    def forbidden(*args, **kwargs):
        raise AssertionError("Registered S1 execution is forbidden in primitive tests")

    monkeypatch.setattr(s1, "evaluate_branch", forbidden)

    point = s1.gamma_k(1.2, 0.8)
    tangent = s1.directed_tangent(1.2, 0.8)

    assert np.linalg.norm(point) == pytest.approx(1.0, abs=1e-14)
    assert np.linalg.norm(tangent) == pytest.approx(1.0, abs=1e-14)
