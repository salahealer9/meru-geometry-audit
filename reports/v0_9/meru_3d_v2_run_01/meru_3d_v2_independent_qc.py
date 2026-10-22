#!/usr/bin/env python3
"""Independent, read-only Meru 3D-V2 polytope audit (never imports the submitted script)."""
import argparse
import hashlib
import itertools
import json
import math
import re
from pathlib import Path
import sympy as S

z=S.Integer(0); one=S.Integer(1); rt=S.sqrt
s2,s3,s5,s6,s10=rt(2),rt(3),rt(5),rt(6),rt(10)
allowed_re=re.compile(r'^[0-9\s+*/().-]*(?:sqrt\([0-9]+\)[0-9\s+*/().-]*)*$')
# Only a finite alphabet of arithmetic and sqrt(integer) expressions is permitted.
def parse(s):
    if not isinstance(s,str) or len(s)>160 or not re.fullmatch(r'[\da-z\s+*/().-]+',s) or any(w!='sqrt' for w in re.findall(r'[a-z]+',s)):
        raise ValueError('Unsafe or unexpected mathematical expression')
    return S.sympify(s, locals={'sqrt':S.sqrt},evaluate=True)
def eq(a,b): return S.simplify(a-b)==0

def sign_exact(x):
    y=S.simplify(x)
    if y==0:return 0
    if y.is_positive:return 1
    if y.is_negative:return -1
    ss=S.sign(y)
    if ss in (S.Integer(-1),S.Integer(0),S.Integer(1)):return int(ss)
    raise ValueError(f'Undecidable sign: {y}')

def leq(x,y):return sign_exact(x-y)<=0

def M(rows):return S.Matrix(rows)
chamber=[('a>=b',(-1,1,0),z),('b>=c',(0,-1,1),z),('c>=0',(0,0,-1),z)]
planes={
    'A0':('A0:a<=1',(1,0,0),one),
    'C':('C:a+b+c<=sqrt(3)',(1,1,1),s3),
    'E':('E:a+b<=sqrt(2)',(1,1,0),s2),
    'T':('T:2a+b<=sqrt(5)',(2,1,0),s5),
}
strata={('A','G0'):('A0',),('A','G1'):('A0','C'),('A','G2'):('A0','C','E'),
        ('B','G0'):('A0',),('B','G1'):('A0','E'),('B','G2'):('A0','E','T')}
expected={
    ('A','G0'):(4,6,3,3, [0,1,2,3],(1,1,1)),
    ('A','G1'):(6,14,7,5-2*s3, [0,1,1,3-s3,S.Rational(3,2),5-2*s3],(one,s3-1,z)),
    ('A','G2'):(8,26,13,9-2*s2-2*s6, [0,1,1,1,6-2*s6,4-2*s2,3-s3,9-2*s2-2*s6],(one,s2-1,s3-s2)),
    ('B','G0'):(4,6,3,3, [0,1,2,3],(1,1,1)),
    ('B','G1'):(6,18,9,S.Rational(3,2), [0,1,1,4-2*s2,7-4*s2,S.Rational(3,2)],(s2/2,s2/2,s2/2)),
    ('B','G2'):(8,42,21,S.Rational(3,2), [0,1,1,20-6*s10,10-4*s5,19-8*s5,33-10*s10,S.Rational(3,2)],(s2/2,s2/2,s2/2)),
}

def veceq(v,w):return all(eq(x,y) for x,y in zip(v,w))
def unique_append(seq,v):
    if not any(veceq(v,w) for w in seq):seq.append(v)

def matching_multiset(x,y):
    todo=list(y)
    for a in x:
        ii=next((i for i,b in enumerate(todo) if eq(a,b)),None)
        if ii is None:return False
        todo.pop(ii)
    return not todo

def enumerate_independent(k):
    active=chamber+[planes[t] for t in strata[k]]
    vertices=[]; triple_ct=0; full_ct=0; feasible_ct=0
    for selected in itertools.combinations(active,3):
        triple_ct+=1
        rows=[a[1] for a in selected]
        mat=M(rows)
        det=mat.det()
        if det==0:continue
        full_ct+=1
        # Independent closed-form Cramer's-rule intersection, no use of submitted solver.
        rhs=M([a[2] for a in selected])
        coords=[]
        for c in range(3):
            new=mat.copy()
            new[:,c]=rhs
            coords.append(S.simplify(new.det()/det))
        v=tuple(coords)
        if all(leq(sum(co[i]*v[i] for i in range(3)), bound) for _,co,bound in active):
            feasible_ct+=1
            unique_append(vertices,v)
    return active,vertices,{'triple_intersections':triple_ct,'full_rank_intersections':full_ct,'feasible_intersections_before_deduplication':feasible_ct}

# An independent finite-stratum construction to check coverage function and counts.
def direction_sets():
    A0={(s,0,0) for s in [-1,1]}|{(0,s,0) for s in [-1,1]}|{(0,0,s) for s in [-1,1]}
    C=set(itertools.product((-1,1), repeat=3))
    E=set()
    T=set()
    for perm in set(itertools.permutations((1,1,0))):
        support=[i for i,x in enumerate(perm) if x]
        for signs in itertools.product((-1,1),repeat=2):
            v=list(perm)
            for i,s in zip(support,signs): v[i]*=s
            E.add(tuple(v))
    for perm in set(itertools.permutations((1,2,0))):
        support=[i for i,x in enumerate(perm) if x]
        for signs in itertools.product((-1,1),repeat=2):
            v=list(perm)
            for i,s in zip(support,signs): v[i]*=s
            T.add(tuple(v))
    return {'A0':A0,'C':C,'E':E,'T':T}


def audit(result_file):
    payload=Path(result_file).read_bytes()
    data=json.loads(payload)
    checks=[]; rows=[]
    def check(label,condition):
        checks.append({'name':label,'pass':bool(condition)})
    strata_sets=direction_sets()
    for key,expected_count in [('A0',6),('C',8),('E',12),('T',24)]:
        check('stratum_count_'+key,len(strata_sets[key])==expected_count)
        check('stratum_antipodal_'+key,all(tuple(-x for x in d) in strata_sets[key] for d in strata_sets[key]))
        check('reported_stratum_'+key,data['stratum_counts'][key]==expected_count)
    check('declared_protocol_commit',data.get('preregistration_commit')=='db007d7429efbd41a4953b86f5eea7e026964aa8')
    check('declared_protocol_blob',data.get('preregistration_blob')=='3db104c82b961761dfd80b92f968f1538869bb36')
    check('declared_study',data.get('study')=='MERU_3D_V2')
    got_rows={(x['family'],x['level']):x for x in data['family_level_results']}
    check('result_keys_exact',set(got_rows)==set(strata))
    for k in strata:
        family,level=k
        label=family+'_'+level
        r=got_rows[k]
        active,verts,ic=enumerate_independent(k)
        vertex_count,count,axis_count, max_sq,norm_oracle,witness=expected[k]
        norms=[S.simplify(sum(t*t for t in v)) for v in verts]
        max_found=next((v for v in norms if all(leq(u,v) for u in norms)),None)
        maxima=[v for v,n in zip(verts,norms) if eq(n,max_found)] if max_found is not None else []
        assert max_found is not None
        reported_verts=[tuple(map(parse,v['vertex'])) for v in r['vertices']]
        reported_norms=[parse(v['norm_squared']) for v in r['vertices']]
        reported_winners=[tuple(map(parse,v)) for v in r['worst_chamber_vertices']]
        given_planes=[(p['name'],tuple(p['coefficients']),parse(p['rhs'])) for p in r['constraint_planes']]
        all_dirs=set().union(*(strata_sets[t] for t in strata[k]))
        # Signed and axis count from independent sets with signed negation.
        count_ax=len({min(d,tuple(-a for a in d)) for d in all_dirs})
        check(label+'_planes_equal', len(given_planes)==len(active) and all(p[0]==q[0] and p[1]==q[1] and eq(p[2],q[2]) for p,q in zip(given_planes,active)))
        check(label+'_counts_signed',len(all_dirs)==count==r['signed_direction_count'])
        check(label+'_counts_axes',count_ax==axis_count==r['unoriented_axis_count'])
        check(label+'_antipodal_closure',r['antipodal_closure'] and all(tuple(-x for x in d) in all_dirs for d in all_dirs))
        check(label+'_sphere_axis_equality',r['spherical_projective_radius_equal'])
        check(label+'_triple_census',r['intersection_census']==ic)
        check(label+'_vertex_count',len(verts)==vertex_count==r['vertex_count']==len(reported_verts))
        check(label+'_all_vertices_exact',len(reported_verts)==len(verts) and all(any(veceq(v,w) for w in reported_verts) for v in verts) and all(any(veceq(v,w) for w in verts) for v in reported_verts))
        check(label+'_reported_vertex_norms',all(eq(sum(x*x for x in v),n) for v,n in zip(reported_verts,reported_norms)))
        check(label+'_full_norm_multiset',matching_multiset(norms,norm_oracle) and matching_multiset(norms,reported_norms))
        check(label+'_global_max_exact',eq(max_found,max_sq) and eq(parse(r['max_squared_norm_exact']),max_found))
        check(label+'_winner_exact',len(maxima)==len(reported_winners)==1 and veceq(maxima[0],witness) and veceq(maxima[0],reported_winners[0]))
        check(label+'_cosine_exact',eq(parse(r['covering_cosine_exact'])**2,1/max_sq) and sign_exact(parse(r['covering_cosine_exact']))==1)
        check(label+'_angle_presentational', abs(r['covering_radius_degrees_approx'] - math.degrees(math.acos(1/math.sqrt(float(S.N(max_sq,16)))))) < 1e-9)
        # Check listed active planes are tight and all support inequalities at all extrema.
        for i,r_v in enumerate(r['vertices']):
            v=reported_verts[i]
            active_names={nm for nm,co,bnd in active if eq(sum(co[j]*v[j] for j in range(3)),bnd)}
            check(label+'_vertex_'+str(i)+'_active_planes',set(r_v['active_planes']).issubset(active_names))
        # Verify normalized worst directions.
        worst_unit=[tuple(map(parse,v)) for v in r['worst_unit_directions']]
        check(label+'_worst_unit',len(worst_unit)==1 and all(eq(worst_unit[0][i],maxima[0][i]/S.sqrt(max_sq)) for i in range(3)))
        rows.append({'family':family,'level':level,'vertices':len(verts),'signed':len(all_dirs),'axes':count_ax,'max_squared_norm':str(S.simplify(max_found)), 'cosine':str(S.simplify(1/S.sqrt(max_found))), 'radius_degrees':round(math.degrees(math.acos(1/math.sqrt(float(max_found.evalf(16))))),12),'worst_vertex':[str(t) for t in maxima[0]],'full_vertex_list':[{'point':[str(t) for t in v],'squared_norm':str(n)} for v,n in zip(verts,norms)],'census':ic})
    check('G0_shared_identical',data.get('g0_identical_exact_squared_maxima') and eq(expected['A','G0'][3],expected['B','G0'][3]))
    check('B_G1_G2_shared_radius',data.get('b_g1_b_g2_equal_exact_squared_maxima') and eq(expected['B','G1'][3],expected['B','G2'][3]))
    # Separate analytic lower bound at body diagonal; T gives cos=sqrt(3/5)<sqrt(2/3) (E).
    diagonal=(one/s3,one/s3,one/s3)
    H_E=(diagonal[0]+diagonal[1])/s2
    H_T=(2*diagonal[0]+diagonal[1])/s5
    check('B_analytic_diagonal_gap',eq(H_E**2,S.Rational(2,3)) and eq(H_T**2,S.Rational(3,5)) and leq(H_T,H_E))
    check('all_independent_checks_pass',all(c['pass'] for c in checks))
    return {'status':'PASS' if all(x['pass'] for x in checks) else 'FAIL', 'number_of_checks':len(checks),'passing_checks':sum(x['pass'] for x in checks),'failing_checks':[c for c in checks if not c['pass']],'results_sha256':hashlib.sha256(payload).hexdigest(),'origin':'separately implemented exact 3D chamber-polytope enumeration; original script not imported or executed','rows':rows,'checks':checks}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('results_json');p.add_argument('output_json');args=p.parse_args()
    out=audit(args.results_json)
    Path(args.output_json).write_text(json.dumps(out,indent=2)+'\n')
    print(out['status'],out['passing_checks'],'/',out['number_of_checks'])
    if out['status']!='PASS':print(json.dumps(out['failing_checks'],indent=2));raise SystemExit(1)
