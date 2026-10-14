"""Unrelated DEV-only unit diagnostics. Never import registered fixtures/cases."""
import math
import numpy as np
import pytest
from meru_geometry.p0a0 import engineering as e, oracles as o


def test_dev_arclength_diagonal_with_duplicates():
    x=e.resample([[11,-4],[11,-4],[14,0],[17,4]],7)
    np.testing.assert_allclose(x,np.column_stack((np.linspace(11,17,7),np.linspace(-4,4,7))))


def test_dev_closed_sampling_and_open_sampling_are_distinct():
    p=[[8,8],[9,8],[9,9],[8,9]]
    assert np.array_equal(e.resample(p,4,True),p)
    assert np.array_equal(e.resample(p,4,False)[-1],p[-1])


@pytest.mark.parametrize('value',[[],[[3,4]],[[1,float('nan')],[2,3]],[[1e110,0],[0,1]],[[2,2],[2,2]]])
def test_dev_invalid_normalization(value):
    with pytest.raises(ValueError): e.normalize(value)


@pytest.mark.parametrize('n',[0,1,3.5,True])
def test_dev_invalid_sample_count(n):
    with pytest.raises(ValueError): e.resample([[4,9],[7,13]],n)


def test_dev_scalar_support_reference():
    a=[[9,-3],[13,-7],[15,4]]; b=[[11,-5],[2,8]]
    got=e.support_distance(a,b); ref=o.nearest_support(a,b)
    assert got==pytest.approx(ref,abs=1e-12)


@pytest.mark.parametrize('reflection',[False,True])
def test_dev_analytic_alignment_reference(reflection):
    a=np.array([[7.,-9.],[11.,-2.],[8.,3.],[12.,8.],[3.,7.]])
    b=np.array([[-3.,2.],[4.,8.],[6.,9.],[7.,-2.],[-5.,-6.]])
    got=e.ordered_match(a,b,reflection=reflection)
    assert got.relative_rms==pytest.approx(o.similarity_error(a,b,reflection),abs=1e-12)


def test_dev_raster_exact_horizontal_reference():
    kw=dict(bounds=[2,-2,9,2],shape=[11,17],width=.37,supersample=3)
    got=e.rasterize([[[3,0],[7,0]]],**kw)
    np.testing.assert_array_equal(got,o.horizontal_coverage([[3,7]],**kw))


def test_dev_empty_silhouette_not_good_score():
    d=e.silhouette_distance(np.zeros((7,9)),np.zeros((7,9)))
    assert d['state']=='NOT_EVALUABLE' and d['iou_distance'] is None


def test_dev_raster_invalid_segment():
    with pytest.raises(ValueError):
        e.rasterize([[[2,4],[2,4]]],bounds=[0,0,8,8],shape=[9,9],width=1)


def test_dev_graph_cycle_plus_segment():
    g=e.graph_counts([[7,7],[9,7],[8,10],[20,1],[21,3]],
                     [[0,1],[1,2],[2,0],[3,4]],[[0,1,2,0],[3,4]])
    assert g==dict(components=2,exposed_endpoints=2,junctions=0,strokes=2,labelled_endpoints=2)


def test_dev_graph_requires_explicit_edge_partition():
    with pytest.raises(ValueError): e.graph_counts([[7,7],[8,8]],[[0,1]],[[1,0],[0,1]])


def test_dev_graph_no_coordinate_snapping():
    g=e.graph_counts([[7,7],[8,8],[8,8],[9,9]],[[0,1],[2,3]],[[0,1],[2,3]])
    assert g['components']==2


def test_dev_component_composite_is_transparent():
    assert e.component_composite(.7,4,2,.3)==pytest.approx(1.3)


def test_dev_local_search_scope_and_failure_reporting():
    got=e.local_planar_search([.3,.8],weight=.37,maxiter=1)
    assert got['scope']=='LOCAL_BOUNDED_ONLY' and not got['success']
    assert math.isfinite(got['value'])


@pytest.mark.parametrize('x',[float('nan'),float('inf'),-1,0])
def test_dev_invalid_objective_weight(x):
    with pytest.raises(ValueError): e.planar_axis_landmark_objective(.71,x)


def test_dev_scalar_projection_oracle():
    assert o.projection([[7,11,13]],[[1,0,0],[0,-1,0],[0,0,-1]])==[[7.,-11.]]


def test_dev_runner_rejects_protocol_only_boundary():
    import importlib.util
    from pathlib import Path
    p=Path(__file__).resolve().parents[1]/'scripts/p0a0_registered_pilot.py'
    spec=importlib.util.spec_from_file_location('dev_runner_gate',p)
    module=importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    with pytest.raises(ValueError,match='distinct full implementation-freeze'):
        module.verify_boundary(module.BASE)
