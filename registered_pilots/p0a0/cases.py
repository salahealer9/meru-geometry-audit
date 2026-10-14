"""REGISTERED PILOT SOURCE ONLY. Not a pytest module. Do not invoke pre-freeze.

Each case returns observations. Assertion failures remain FAIL in the runner;
known absence of observable information is EXPECTED_BLIND_SPOT, never a pass
claim for that capability. No fixture/metric call at import time.
"""
import math
import numpy as np
from meru_geometry.p0a0 import engineering as e, oracles as o
from meru_geometry.p0a0.boundaries import require, parse_pi_bounds
from meru_geometry.projections import orthographic_project
from meru_geometry.projection_orbits import (
    camera_direction_classes, frame_planar_transform, planar_similarity_alignment)
from meru_geometry.rotations import tetrahedral_rotation_group
from fixtures import generate


def near(x, y, tol):
    if not np.allclose(x, y, atol=tol, rtol=0):
        raise AssertionError(f"oracle discrepancy: {x!r} versus {y!r}, atol={tol}")


def rejects(fn):
    try:
        fn()
    except ValueError:
        return 'ValueError'
    raise AssertionError('invalid input did not raise ValueError')


def graph(path):
    return e.graph_counts(path, [[i,i+1] for i in range(len(path)-1)], [list(range(len(path)))])


def evaluate(case, config):
    f = generate(case, config)
    tol = config['absolute_tolerance']; score_tol = config['score_tolerance']
    result = {'case':case, 'state':'PASS', 'oracle':f['oracle'],
              'representation':REPRESENTATIONS[case],
              'generator':'fixtures.generate / p0a0-fixtures-1',
              'provenance':config['provenance'], 'seed':config['seed'],
              'raw':{}, 'normalized':{'state':'NOT_APPLICABLE','reason':'no normalization claimed in this case'},
              'claimed_invariances':INVARIANCES[case],
              'sensitivity':{}, 'explanation':'All stated relationships checked; not a Hebrew metric certification.'}
    raw = result['raw']
    if case == 'S00':
        got = orthographic_project(f['points'], f['matrix'])
        expected = o.projection(f['points'].tolist(), f['matrix'].tolist())
        near(got,expected,tol)
        raw['max_coordinate_error'] = float(np.max(np.abs(got-expected)))
        raw['improper'] = rejects(lambda: orthographic_project(f['points'],f['improper']))
        for value in [float('nan'),float('inf'),-float('inf')]:
            p = f['points'].copy(); p[0,0] = value
            rejects(lambda: orthographic_project(p))
        raw['nonfinite_rejections'] = 3
    elif case == 'S01':
        a = e.ordered_match(f['path'],f['target'])
        near(a.relative_rms,0,score_tol); near(a.scale,f['scale'],tol)
        near(a.orthogonal_matrix,f['row_matrix'],tol); near(a.translation,f['translation'],tol)
        near(a.relative_rms,o.similarity_error(f['path'],f['target']),score_tol)
        raw.update(absolute_rms=a.absolute_rms,scale=a.scale,translation=a.translation.tolist())
        result['normalized'] = {'relative_rms':a.relative_rms}
    elif case == 'S02':
        a,b = [e.ordered_match(f['path'],f['target'],reflection=x) for x in (False,True)]
        near(a.relative_rms,o.similarity_error(f['path'],f['target']),score_tol)
        near(b.relative_rms,o.similarity_error(f['path'],f['target'],True),score_tol)
        require(a.relative_rms > 1e-3 and not a.reflection_used, "registered invariant 01 failed")
        require(b.reflection_used, "registered invariant 02 failed"); near(b.relative_rms,0,score_tol)
        raw.update(so2_absolute=a.absolute_rms,o2_absolute=b.absolute_rms)
        result['normalized'] = {'so2':a.relative_rms,'o2':b.relative_rms}
    elif case == 'S03':
        indexed = e.ordered_match(f['a'],f['b'])
        sampled = e.ordered_match(f['a'],f['b'],samples=config['arclength_samples'])
        expected = np.column_stack((np.linspace(0,5,129),np.linspace(0,2,129)))
        near(e.resample(f['a'],129),expected,tol); near(e.resample(f['b'],129),expected,tol)
        near(sampled.relative_rms,0,score_tol); require(indexed.relative_rms > .01, "registered invariant 03 failed")
        raw.update(index_absolute=indexed.absolute_rms,resampled_absolute=sampled.absolute_rms)
        result['normalized'] = {'index_relative':indexed.relative_rms,'resampled_relative':sampled.relative_rms}
        result.update(state='EXPECTED_BLIND_SPOT',explanation='Index correspondence is sample-sensitive; straight-polyline arclength path tested separately.')
    elif case == 'S04':
        vertices = f['vertices']; edges = config['cases'][case]['edges']
        a,b = [e.graph_counts(vertices,edges,f[k]) for k in ('one','two')]
        require(a['components']==b['components']==1, "registered invariant 04 failed")
        require(a['exposed_endpoints']==b['exposed_endpoints']==2, "registered invariant 05 failed")
        require((a['labelled_endpoints'],b['labelled_endpoints'])==(2,4), "registered invariant 06 failed")
        d = e.support_distance(vertices,vertices); near(list(d.values()),[0,0],tol)
        raw.update(support=d,one=a,two=b)
        result.update(state='EXPECTED_BLIND_SPOT',explanation='Identical support cannot identify segmentation labels; labels were supplied, never inferred.')
    elif case == 'S05':
        pieces = f['pieces']; allv = pieces.reshape(-1,2)
        a,b = graph(f['full']),e.graph_counts(allv,[[0,1],[2,3]],[[0,1],[2,3]])
        require(a['components']==1 and b['components']==2, "registered invariant 07 failed")
        near(pieces[1,0,0]-pieces[0,1,0],1/64,tol)
        raster = config['raster']; outputs=[]
        for shape in raster['shapes']:
            kw = {k:raster[k] for k in ('bounds','width','supersample')}; kw['shape']=shape
            x=e.rasterize([f['full']],**kw); y=e.rasterize(pieces,**kw)
            near(x,o.horizontal_coverage([[-1,1]],**kw),tol)
            near(y,o.horizontal_coverage([[-1,.125],[.140625,1]],**kw),tol)
            outputs.append({'shape':shape,'silhouette':e.silhouette_distance(x,y,raster['threshold']),
                            'different_pixels':int(np.count_nonzero(x!=y))})
        require(outputs[0]['different_pixels']==0 and outputs[1]['different_pixels']>0, "registered invariant 08 failed")
        raw.update(full_graph=a,gapped_graph=b,gap=1/64)
        result['sensitivity']={'rasters':outputs}
        result.update(state='EXPECTED_BLIND_SPOT',explanation='Coarse raster conceals gap; exact supplied topology and finer grid retain it. No gap closing.')
    elif case == 'S06':
        a=f['main']; b=np.vstack((a,f['extra']))
        ga=graph(a); gb=e.graph_counts(b,[[0,1],[1,2],[3,4]],[[0,1,2],[3,4]])
        d=e.support_distance(a,b); ref=o.nearest_support(a,b)
        near(list(d.values()),list(ref.values()),tol); near(d['hausdorff'],math.sqrt(2)/100,tol)
        require(ga['components']==1 and gb['components']==2 and d['chamfer']<.01, "registered invariant 09 failed")
        comp=e.component_composite(d['chamfer'],1,2,f['weight'])
        near(comp-d['chamfer'],.25,tol)
        raw.update(support=d,composite=comp,graphs=[ga,gb])
        result.update(state='EXPECTED_BLIND_SPOT',explanation='Small mean support error does not encode components. Composite explicitly uses supplied graph counts with synthetic weight 1/4.')
    elif case == 'S07':
        a=f['main']; b=np.vstack((a,f['spur'][1:]))
        ga=graph(a); gb=e.graph_counts(b,[[0,1],[1,2],[1,3]],[[0,1,2],[1,3]])
        require((ga['exposed_endpoints'],gb['exposed_endpoints'])==(2,3), "registered invariant 10 failed")
        require((ga['junctions'],gb['junctions'])==(0,1), "registered invariant 11 failed")
        d=e.support_distance(a,b); near(d['hausdorff'],1/32,tol)
        near(list(d.values()),list(o.nearest_support(a,b).values()),tol)
        raw.update(support=d,graphs=[ga,gb])
        result.update(state='EXPECTED_BLIND_SPOT',explanation='Support distance detects geometric change but has no endpoint-count observable; counts require supplied graph.')
    elif case == 'S08':
        a,b=f['plain'],f['notch']; d=e.support_distance(a,b)
        near(d['hausdorff'],1/32,tol); near(d['chamfer'],1/160,tol)
        near(list(d.values()),list(o.nearest_support(a,b).values()),tol)
        na,_,sa=e.normalize(a); nb,_,sb=e.normalize(b)
        nd=e.support_distance(na,nb)
        near(list(nd.values()),list(o.nearest_support(na,nb).values()),tol)
        raw.update(support=d,feature_height=1/32)
        result['normalized']={'support':nd,'rms_scales':[sa,sb]}
        result['sensitivity']={'thresholds':[{'threshold':t,'raw_hidden':d['hausdorff']<=t,
                                  'normalized_hidden':nd['hausdorff']<=t} for t in f['thresholds']]}
        require(not result['sensitivity']['thresholds'][0]['raw_hidden'], "registered invariant 12 failed")
        require(result['sensitivity']['thresholds'][1]['raw_hidden'], "registered invariant 13 failed")
        result.update(state='EXPECTED_BLIND_SPOT',explanation='Feature sensitivity is metric/normalization/threshold dependent; 0.05 raw threshold conceals the known notch.')
    elif case == 'S09':
        a=f['path']; reversed_path=a[::-1]; shifted=np.roll(a,f['shift'],axis=0)
        denied=e.ordered_match(a,reversed_path); allowed=e.ordered_match(a,reversed_path,reversal=True)
        closed=e.ordered_match(a,shifted,closed=True); opened=e.ordered_match(a,shifted)
        near(denied.relative_rms,o.similarity_error(a,reversed_path),score_tol)
        near(opened.relative_rms,o.similarity_error(a,shifted),score_tol)
        near([allowed.relative_rms,closed.relative_rms],[0,0],score_tol)
        require(denied.relative_rms>1e-4 and opened.relative_rms>1e-4, "registered invariant 14 failed")
        require(opened.shift==0 and closed.shift==f['shift'] and allowed.reversed_order, "registered invariant 15 failed")
        raw.update(allowed_reversal=allowed.reversed_order,closed_shift=closed.shift,open_shift=opened.shift)
        result['normalized']={'reversal_denied':denied.relative_rms,'reversal_allowed':allowed.relative_rms,
                              'closed_shift':closed.relative_rms,'open_shift':opened.relative_rms}
    elif case == 'S10':
        raw['zero_normalize']=rejects(lambda:e.normalize(f['zero']))
        raw['zero_arclength']=rejects(lambda:e.resample(f['zero']))
        for token in f['nonfinite_tokens']:
            invalid=np.array([[0.,0.],[float(token),1.]])
            rejects(lambda:e.resample(invalid)); rejects(lambda:e.support_distance(invalid,[[0,0]]))
        expected=np.column_stack((np.linspace(0,1,129),np.zeros(129)))
        near(e.resample(f['duplicates']),expected,tol)
        small=e.resample(f['small']); require(small[-1,0]==1e-12 and np.all(np.diff(small[:,0])>0), "registered invariant 16 failed")
        raw['inherited_small_alignment']=rejects(lambda:planar_similarity_alignment(f['small'],f['small']))
        tiny_graph=e.graph_counts([[0,0],[1,0],[2,0],[2,1e-12]],[[0,1],[2,3]],[[0,1],[2,3]])
        require(tiny_graph['components']==2, "registered invariant 17 failed")
        raw.update(duplicate_policy='consecutive exact duplicates removed for arclength only',tiny_graph=tiny_graph)
        result.update(state='EXPECTED_BLIND_SPOT',explanation='Inherited alignment rejects tiny centred energy. Tiny nonzero edges are retained by the new graph/arclength utilities; no NaN becomes a match.')
    elif case == 'S11':
        ref=o.axis_landmark_extrema(f['weight'])
        result_local=e.local_planar_search(parse_pi_bounds(f['local_bounds']),weight=f['weight'],xatol=f['xatol'],maxiter=f['maxiter'])
        near(e.planar_axis_landmark_objective(0,f['weight']),ref['global_value'],tol)
        near(e.planar_axis_landmark_objective(math.pi,f['weight']),ref['local_value'],tol)
        require(result_local['success'], "registered invariant 18 failed")
        near(result_local['value'],ref['local_value'],score_tol)
        require(result_local['value']-ref['global_value']>.39, "registered invariant 19 failed")
        raw.update(local=result_local,analytic_oracle=ref,optimizer_oracle_discrepancy=result_local['value']-ref['global_value'])
        result.update(state='EXPECTED_BLIND_SPOT',explanation='Deliberately bounded local search reaches competing local minimum; this is not a global optimizer certificate.')
    elif case == 'S12':
        rotations=tetrahedral_rotation_group(); duplicated=np.concatenate((rotations,rotations[:1]))
        require(len(camera_direction_classes(rotations))==len(camera_direction_classes(duplicated))==6, "registered invariant 20 failed")
        require(len(camera_direction_classes(rotations,unoriented=True))==3, "registered invariant 21 failed")
        expected={(1.,0.,0.),(-1.,0.,0.),(0.,1.,0.),(0.,-1.,0.),(0.,0.,1.),(0.,0.,-1.)}
        require({tuple(np.round(r[2],12)) for r in rotations}==expected, "registered invariant 22 failed")
        q=f['roll_row']; roll=np.eye(3); roll[:2,:2]=q.T
        errors=[]
        for r in rotations:
            x=orthographic_project(f['points'],r); y=orthographic_project(f['points'],roll@r)
            near(y,x@q,tol)
            near(y,o.projection(f['points'].tolist(),(roll@r).tolist()),tol)
            a=e.ordered_match(x,y); near(a.relative_rms,0,score_tol); errors.append(a.relative_rms)
        front=np.eye(3); back=np.diag([1.,-1.,-1.])
        transform=frame_planar_transform(front,back); near(np.linalg.det(transform),-1,tol)
        raw.update(signed_classes=6,axis_classes=3,duplicate_frames=13,opposite_planar_determinant=float(np.linalg.det(transform)))
        result['normalized']={'roll_relative_rms':errors}
    else:
        raise ValueError('unregistered case')
    return result


REPRESENTATIONS={
 'S00':'ordered 3-D points/camera','S01':'ordered planar samples','S02':'ordered scalene triangle',
 'S03':'ordered piecewise-linear path','S04':'support plus labelled graph','S05':'graph plus finite-width raster',
 'S06':'sampled support plus supplied graph','S07':'sampled support plus supplied graph',
 'S08':'sampled support and normalized support','S09':'ordered open/closed paths',
 'S10':'invalid and tiny synthetic arrays','S11':'unoriented axis plus ordered landmark','S12':'camera frames plus ordered projections'}
INVARIANCES={
 'S00':['none; exact coordinate projection'],'S01':['translation','positive scale','SO2'],
 'S02':['SO2 only unless reflection explicitly enabled'],'S03':['polyline arclength density for same segment'],
 'S04':['support independent of stroke labels'],'S05':['none: raster resolution is explicit'],
 'S06':['none: component penalty requires graph'],'S07':['none: endpoints require graph'],
 'S08':['normalization translation and positive scale; thresholds explicit'],
 'S09':['reversal optional','cyclic shift closed only'],'S10':['none: explicit degeneracy rules'],
 'S11':['angle modulo 2pi; axis sign alone does not remove landmark'],
 'S12':['roll quotient under free SO2','front/back identified only under O2']}
