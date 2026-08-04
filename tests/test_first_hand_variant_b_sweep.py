import math
import sys
from pathlib import Path

import numpy as np
import pytest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import first_hand_variant_b_sweep as vb  # noqa: E402


def test_registered_grid_values_are_exact():
    assert vb.W_VALUES == (0.02, 0.05, 0.10, 0.20, 0.30)
    assert vb.E_VALUES == (1.4, 1.6, 1.8, 2.0, 2.2)


def test_exact_registered_counts():
    assert len(vb.REGISTERED_CARRIERS) == 25
    assert len(vb.REGISTERED_SPIRALS) == 8
    assert len(vb.SCALES) == 2
    assert len(vb.REGISTERED_CELLS) == 400


def test_registered_spiral_ids_are_exact():
    assert tuple(s.spiral_id for s in vb.REGISTERED_SPIRALS) == (
        "RECIPROCAL",
        "LOG-M050",
        "LOG-M075",
        "LOG-M100",
        "LOG-M125",
        "LOG-M150",
        "LOG-M200",
        "GOLDEN-MEAN",
    )


def test_registered_scale_values_are_frozen():
    assert vb.K_G30 == pytest.approx(math.tan(math.pi / 6.0), abs=0.0)
    assert vb.K_GHALF == pytest.approx(math.tan(0.5), abs=0.0)


@pytest.mark.parametrize("carrier", vb.REGISTERED_CARRIERS)
def test_carrier_normalization_and_throat_identity(carrier):
    assert carrier.R + carrier.a == pytest.approx(1.0, abs=1e-15)
    assert carrier.R - carrier.a == pytest.approx(carrier.w, abs=1e-15)


@pytest.mark.parametrize("carrier", vb.REGISTERED_CARRIERS)
def test_all_registered_carriers_are_analytically_admissible(carrier):
    assert vb.carrier_is_analytically_admissible(carrier)


@pytest.mark.parametrize("carrier", vb.REGISTERED_CARRIERS)
@pytest.mark.parametrize(
    "u",
    [0.0, 0.37, math.pi / 2.0, 2.1, math.pi, 5.2],
)
def test_rho_is_strictly_positive_for_registered_carriers(carrier, u):
    rho = carrier.R + carrier.a * math.cos(u)
    assert rho >= carrier.w - 1.0e-15
    assert rho > 0.0


@pytest.mark.parametrize("carrier", vb.REGISTERED_CARRIERS)
@pytest.mark.parametrize(
    "u,v",
    [
        (0.23, 0.41),
        (1.2, 2.0),
        (2.5, 4.2),
        (4.7, 5.6),
    ],
)
def test_surface_cross_norm_matches_analytic_regular_factor(carrier, u, v):
    Xu, Xv = vb.carrier_partials(carrier, u, v)
    numerical = float(np.linalg.norm(np.cross(Xu, Xv)))
    analytic = vb.carrier_regular_cross_norm_analytic(carrier, u)

    assert analytic > 0.0
    assert numerical == pytest.approx(analytic, rel=2e-14, abs=2e-14)


@pytest.mark.parametrize("spiral", vb.REGISTERED_SPIRALS)
def test_all_radial_laws_start_at_one(spiral):
    assert spiral.radius(vb.THETA_OUTER) == pytest.approx(1.0, abs=1e-15)


@pytest.mark.parametrize("spiral", vb.REGISTERED_SPIRALS)
@pytest.mark.parametrize(
    "theta",
    [1.2, 2.7, 5.3, 8.8],
)
def test_all_registered_radial_laws_are_strictly_decreasing(spiral, theta):
    assert 1.0 < theta < vb.THETA_INNER
    assert spiral.radius_prime(theta) < 0.0


@pytest.mark.parametrize("spiral", vb.REGISTERED_SPIRALS)
@pytest.mark.parametrize("scale,k", vb.SCALES)
def test_mapping_outer_coordinate_is_frozen(spiral, scale, k):
    del scale
    u, v = vb.mapped_coordinates(vb.THETA_OUTER, spiral, k)
    assert u == pytest.approx(0.0, abs=1e-15)
    assert v == pytest.approx(0.0, abs=0.0)


@pytest.mark.parametrize("spiral", vb.REGISTERED_SPIRALS)
@pytest.mark.parametrize("scale,k", vb.SCALES)
def test_mapping_inner_azimuth_is_exactly_three_pi(spiral, scale, k):
    del spiral, scale, k
    assert vb.THETA_INNER - 1.0 == pytest.approx(
        3.0 * math.pi,
        rel=0.0,
        abs=0.0,
    )


@pytest.mark.parametrize("spiral", vb.REGISTERED_SPIRALS)
@pytest.mark.parametrize("scale,k", vb.SCALES)
@pytest.mark.parametrize(
    "theta",
    [1.3, 3.1, 6.2, 9.4],
)
def test_registered_mapping_has_positive_meridional_derivative(
    spiral,
    scale,
    k,
    theta,
):
    del scale
    r = spiral.radius(theta)
    rp = spiral.radius_prime(theta)
    assert vb.meridional_derivative(r, rp, k) > 0.0


@pytest.mark.parametrize(
    "carrier",
    [
        vb.REGISTERED_CARRIERS[0],
        vb.REGISTERED_CARRIERS[12],
        vb.REGISTERED_CARRIERS[-1],
    ],
)
@pytest.mark.parametrize(
    "spiral",
    [
        vb.RECIPROCAL_SPIRAL,
        vb.GENERIC_LOG_SPIRALS[2],
        vb.GOLDEN_SPIRAL,
    ],
)
@pytest.mark.parametrize("scale,k", vb.SCALES)
@pytest.mark.parametrize(
    "theta",
    [1.7, 4.9, 8.1],
)
def test_mapped_tangent_orientation_matches_decreasing_theta(
    carrier,
    spiral,
    scale,
    k,
    theta,
):
    del scale
    h = 1.0e-7
    p_minus = vb.mapped_curve_point(theta - h, carrier, spiral, k)
    p_plus = vb.mapped_curve_point(theta + h, carrier, spiral, k)

    numerical_plus_theta = p_plus - p_minus
    numerical_plus_theta /= np.linalg.norm(numerical_plus_theta)

    tangent = vb.mapped_directed_tangent(theta, carrier, spiral, k)

    assert np.linalg.norm(tangent) == pytest.approx(1.0, abs=1e-14)
    assert float(np.dot(tangent, numerical_plus_theta)) < -0.999999999


def test_directed_and_line_ambient_primitives():
    parallel = vb.ambient_angle_record(
        [1.0, 0.0, 0.0],
        [1.0, 0.0, 0.0],
    )
    anti = vb.ambient_angle_record(
        [1.0, 0.0, 0.0],
        [-1.0, 0.0, 0.0],
    )

    assert parallel.delta_directed_rad == pytest.approx(0.0, abs=0.0)
    assert parallel.delta_line_rad == pytest.approx(0.0, abs=0.0)
    assert parallel.directed_state == "AMBIENT_DIRECTED_PARALLEL"
    assert parallel.line_state == "AMBIENT_LINE_PARALLEL"

    assert anti.delta_directed_rad == pytest.approx(math.pi, abs=1e-15)
    assert anti.delta_line_rad == pytest.approx(0.0, abs=1e-15)
    assert anti.directed_state == "AMBIENT_DIRECTED_NOT_PARALLEL"
    assert anti.line_state == "AMBIENT_LINE_PARALLEL"


def test_no_parallel_transport_symbol_is_imported():
    assert "minimal_sphere_transport" not in vb.__dict__
    assert "AntipodalTransportError" not in vb.__dict__


def test_no_arbitrary_parameter_cli_surface():
    source = (ROOT / "scripts" / "first_hand_variant_b_sweep.py").read_text()
    prohibited = (
        "--w",
        "--e",
        "--k",
        "--b",
        "--theta",
        "--optimize",
        "--interpolate",
        "--root",
        "--refine",
    )
    for token in prohibited:
        # Match an exact quoted option string, not prefixes such as
        # "--execute-registered-variant-b".
        assert f'"{token}"' not in source
        assert f"'{token}'" not in source


def test_sphere_likeness_metric_is_finite_and_nonnegative():
    for carrier in (
        vb.REGISTERED_CARRIERS[0],
        vb.REGISTERED_CARRIERS[12],
        vb.REGISTERED_CARRIERS[-1],
    ):
        value = vb.sphere_likeness_rms(carrier)
        assert math.isfinite(value)
        assert value >= 0.0


def test_primitive_suite_does_not_evaluate_registered_endpoint_cells(monkeypatch):
    def forbidden(*args, **kwargs):
        raise AssertionError(
            "Registered Variant-B endpoint execution is forbidden in primitive tests"
        )

    monkeypatch.setattr(vb, "evaluate_registered_cell", forbidden)

    carrier = vb.REGISTERED_CARRIERS[0]
    spiral = vb.RECIPROCAL_SPIRAL
    _, k = vb.SCALES[0]

    # Non-endpoint primitive sample only.
    point = vb.mapped_curve_point(4.0, carrier, spiral, k)
    tangent = vb.mapped_directed_tangent(4.0, carrier, spiral, k)

    assert point.shape == (3,)
    assert np.linalg.norm(tangent) == pytest.approx(1.0, abs=1e-14)


def test_cell_ids_are_unique():
    ids = [cell.cell_id for cell in vb.REGISTERED_CELLS]
    assert len(ids) == len(set(ids)) == 400
