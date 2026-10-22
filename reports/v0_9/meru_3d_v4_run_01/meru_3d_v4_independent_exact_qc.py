#!/usr/bin/env python3
"""Independent target-blind audit of frozen Meru 3D-V4 run JSON.

This script is NOT the registered calculator, never imports or runs it, and
reconstructs the five controls and finite grids from preregistered formulas.
Uses independent oriented supporting-edge hull construction, iterative path
reduction, and fraction-only exact projected invariants. Comparisons use no
floating point and no tolerance. It reads the registered JSON as data only.
"""
import json, itertools, hashlib, sys
from collections import Counter
from fractions import Fraction as F
from pathlib import Path

HERE=Path(__file__).resolve().parent
DATA=HERE/'results.json'
OUT=HERE/'MERU_3D_V4_INDEPENDENT_QC_2026-10-22.json'
raw=DATA.read_bytes(); recorded=json.loads(raw)
checks=0; failures=[]; per=[]; matrix_comparisons=0

def check(cond, msg):
    global checks
    checks+=1
    if not cond:
        failures.append(msg)
        if len(failures)>60:raise RuntimeError('More than 60 failures: '+repr(failures[:4]))

def ip(a,b):return sum(x*y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def cross(a,b):return (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def norm(t):return ip(t,t)
def bform(t,a,b):return ip(a,b)-F(ip(t,a)*ip(t,b),norm(t))
def orient(t,a,b):return ip(t,cross(a,b))
def sign(x):return (x>0)-(x<0)
def radical_key(qnum,q):
    # qnum/sqrt(q): sign and exact squared absolute value determine real value
    qnum=F(qnum)
    return (sign(qnum),qnum*qnum/F(q))
def mean(points):
    n=len(points);return tuple(sum(p[j] for p in points)/n for j in range(3))
def signature(t,points):
    o=mean(points);c=[sub(p,o) for p in points]
    return (tuple(tuple(bform(t,x,y) for y in c) for x in c),
            tuple(tuple(radical_key(orient(t,x,y),norm(t)) for y in c) for x in c))
def signature_serial(t,points):
    o=mean(points);c=[sub(p,o) for p in points]
    return {'centred_gram':[[str(bform(t,x,y)) for y in c] for x in c],
            'oriented_minor_denominator_sqrt_squared':norm(t),
            'oriented_minor_numerators':[[str(orient(t,x,y)) for y in c] for x in c]}
def point_equal(t,a,b):return bform(t,sub(a,b),sub(a,b))==0

def grid():
    axes=set()
    for k in range(3):
        for v in [-1,1]:
            z=[0,0,0];z[k]=v;axes.add(tuple(z))
    corners=set(itertools.product((-1,1),repeat=3))
    edges=set(); two=set()
    for pos in range(3):
        ids=[i for i in range(3) if i!=pos]
        for a,b in itertools.product((-1,1),repeat=2):
            u=[0,0,0];u[ids[0]]=a;u[ids[1]]=b; edges.add(tuple(u))
            for x,y in [(1,2),(2,1)]:
                w=[0,0,0];w[ids[0]]=a*x;w[ids[1]]=b*y;two.add(tuple(w))
    assert list(map(len,[axes,corners,edges,two]))==[6,8,12,24]
    sa=sorted(axes);sc=sorted(corners);se=sorted(edges);st=sorted(two)
    return {'A':{'G0':sa,'G1':sa+sc,'G2':sa+sc+se},'B':{'G0':sa,'G1':sa+se,'G2':sa+se+st}}

controls={
 'TR-L':([(0,0,0),(1,0,0),(3,0,0)],False),
 'TR-S':([(0,0,0),(1,2,3),(3,5,4),(5,6,8),(8,9,10)],False),
 'TR-C':([(0,0,0),(3,0,0),(4,2,1),(1,4,3),(-1,2,1),(0,0,0)],True),
 'CS-T':([(0,0,0),(1,0,0),(0,2,0),(0,0,3)],False),
 'CS-B':(list(itertools.product((0,1),(0,2),(0,3))),False),
}
controls={k:([tuple(F(x) for x in p) for p in points],closed) for k,(points,closed) in controls.items()}

def rank(t,pts):
    if len(pts)<2:return 0
    diffs=[sub(p,pts[0]) for p in pts[1:]]
    nonzero=[v for v in diffs if bform(t,v,v)!=0]
    if not nonzero:return 0
    return 2 if any(orient(t,nonzero[0],v)!=0 for v in nonzero[1:]) else 1

def trace_reduce(t,points,closed):
    pts=list(points[:-1] if closed else points)
    # Independent finite deletion: cyclic/open successive repeated-vertex removal,
    # followed by iterative positive-collinear-corner deletion until no deletions.
    limit=100
    for iteration in range(limit):
        changed=False
        # zero-length steps
        for i in range(len(pts)-1+(1 if closed and len(pts)>1 else 0)):
            a=i%len(pts);z=(i+1)%len(pts)
            if point_equal(t,pts[a],pts[z]):
                pts.pop(z);changed=True;break
        if changed:continue
        if len(pts)>=3:
            seq=range(len(pts)) if closed else range(1,len(pts)-1)
            for i in seq:
                a=pts[(i-1)%len(pts)];b=pts[i];c=pts[(i+1)%len(pts)]
                u=sub(b,a);v=sub(c,b)
                if orient(t,u,v)==0 and bform(t,u,v)>0:
                    pts.pop(i);changed=True;break
        if not changed:break
    else:raise RuntimeError('trace reduction nontermination')
    if rank(t,pts)==0:return []
    return pts

def hull(t,src):
    # Unique projected points, chosen in source order (not imported from registered code).
    uniq=[]
    for p in src:
        if not any(point_equal(t,p,q) for q in uniq):uniq.append(p)
    if rank(t,uniq)!=2:raise AssertionError('A convex solid unexpectedly projected below rank 2')
    N=len(uniq);edges={}
    for i in range(N):
        for j in range(N):
            if i==j:continue
            v=sub(uniq[j],uniq[i]);sq=bform(t,v,v)
            if sq==0:continue
            ok=True
            for k in range(N):
                w=sub(uniq[k],uniq[i]);o=orient(t,v,w)
                if o<0:ok=False;break
                if o==0 and not (0<=bform(t,w,v)<=sq):ok=False;break
            if ok:
                if i in edges:raise AssertionError('Multiple strict outgoing hull edges')
                edges[i]=j
    if len(edges)<3:raise AssertionError('Insufficient strict supporting edges')
    start=min(edges);cycle=[start];visited={start}
    while True:
        nxt=edges[cycle[-1]]
        if nxt==start:break
        if nxt in visited:raise AssertionError('Premature hull cycle')
        cycle.append(nxt);visited.add(nxt)
    if set(cycle)!=set(edges):raise AssertionError('Disconnected hull edges')
    pts=[uniq[i] for i in cycle]
    double_area=sum(orient(t,pts[i],pts[(i+1)%len(pts)]) for i in range(len(pts)))
    if double_area<=0:raise AssertionError('Hull not CCW')
    return uniq,pts,double_area

def permutations(pts,closed,is_silhouette,so):
    N=len(pts)
    if is_silhouette or closed:
        seqs=[[pts[(i+j)%N] for j in range(N)] for i in range(N)]
        if not is_silhouette or not so:
            seqs += [[pts[(i-j)%N] for j in range(N)] for i in range(N)]
    else:seqs=[list(pts),list(reversed(pts))]
    return seqs

def canonical_key(t,pts,closed,is_silhouette,so):
    keys=[]
    for perm in permutations(pts,closed,is_silhouette,so):
        gram,area=signature(t,perm)
        keys.append((gram,area) if so else gram)
    return min(keys)

def partition(mat,valid):
    groups=[];seen=set()
    for i in valid:
        if i not in seen:
            g=[j for j in valid if mat[i][j]]
            assert all(mat[u][v] for u in g for v in g)
            groups.append(g);seen.update(g)
    assert seen==set(valid)
    return groups

allgrids=grid()
expected={'A':{'G0':(6,3),'G1':(14,7),'G2':(26,13)},'B':{'G0':(6,3),'G1':(18,9),'G2':(42,21)}}
line_oracle={'A':{'G0':1,'G1':2,'G2':3},'B':{'G0':1,'G1':2,'G2':4}}
resultmap={(r['family'],r['level']):r for r in recorded['family_level_results']}
check(len(recorded['family_level_results'])==6,'six records')
check(len(resultmap)==6,'unique records')
check(recorded['preregistration_commit']=='d7b5359f857b5a294746dc6bce5a61e50d169022','commit')
check(recorded['preregistration_blob']=='2d57b85c066c76ae462929ece209385f5491ed78','blob')
check(recorded['status']=='PASS_INTERNAL_ORACLES_AWAITING_INDEPENDENT_REVIEW','run preliminary status')

for fam in ('A','B'):
 for level in ('G0','G1','G2'):
    row=resultmap[(fam,level)];cameras=allgrids[fam][level];N=len(cameras)
    check(row['signed_camera_triples']==[list(t) for t in cameras],f'{fam} {level} exact grid order')
    check((row['signed_camera_count'],row['axis_count'])==expected[fam][level],f'{fam} {level} counts')
    axes=sorted(t for t in cameras if next(v for v in t if v!=0)>0)
    check(row['axis_representatives']==[list(x) for x in axes],f'{fam} {level} axes order')
    check(all(tuple(-z for z in t) in cameras for t in cameras),f'{fam} {level} antipodes')
    check(set(row['control_results'])==set(controls),f'{fam} {level} 5 controls')
    for control,(source,closed) in controls.items():
        rr=row['control_results'][control];tr=control.startswith('TR');is_silhouette=not tr
        check(rr['camera_count']==N and len(rr['per_camera'])==N, f'{fam} {level} {control} camera count')
        check(rr['observable']==control,f'{fam} {level} {control} observable')
        computed=[];ranks=[];valid=[];invalid=[];unique_list=[]
        for i,t in enumerate(cameras):
            entry=rr['per_camera'][i]
            check(entry['camera_triple']==list(t) and entry['index']==i,f'{fam} {level} {control} camera {i} identity')
            check(entry['camera_norm_squared']==norm(t),f'{fam} {level} {control} camera {i} q')
            if tr:
                p=trace_reduce(t,source,closed)
                r=rank(t,source)
                check(entry['rank']==r,f'{fam} {level} {control} camera {i} rank')
                check(entry['source_point_count']==len(source),f'{fam} {level} {control} camera {i} source count')
                check(entry['closed'] is closed,f'{fam} {level} {control} camera {i} closed')
                chk_ok=(r!=0)
                check(entry['status']==('EVALUABLE' if chk_ok else 'NOT_EVALUABLE'),f'{fam} {level} {control} camera {i} status')
                check(entry['reduced_corner_count']==len(p),f'{fam} {level} {control} camera {i} reduced count')
                if chk_ok:
                    frozen=[tuple(F(x) for x in q) for q in entry['reduced_vertices_3d_preimage']]
                    # validate by exact projected trace equality up to admissible path-reordering
                    check(any(all(point_equal(t,a,b) for a,b in zip(p,seq)) for seq in permutations(frozen,closed,False,False)) if len(p)==len(frozen) else False,f'{fam} {level} {control} camera {i} reduced geometric trace')
                    check(entry['exact_signature']==signature_serial(t,frozen),f'{fam} {level} {control} camera {i} exact invariants')
                else:
                    check(entry['reduced_vertices_3d_preimage']==[],f'{fam} {level} {control} camera {i} degenerate reduction')
            else:
                uq,p,double_area=hull(t,source)
                r=2;chk_ok=True
                check(entry['rank']==2 and entry['status']=='EVALUABLE',f'{fam} {level} {control} camera {i} hull rank/status')
                check(entry['input_point_count']==len(source),f'{fam} {level} {control} camera {i} input count')
                check(entry['projected_distinct_count']==len(uq),f'{fam} {level} {control} camera {i} unique vertices')
                check(entry['strict_hull_corner_count']==len(p),f'{fam} {level} {control} camera {i} hull corners')
                frozen=[tuple(F(x) for x in q) for q in entry['strict_ccw_hull_vertices_3d_preimage']]
                check(len(frozen)==len(p) and any(all(point_equal(t,a,b) for a,b in zip(p,seq)) for seq in permutations(frozen,True,True,True)),f'{fam} {level} {control} camera {i} strict CCW hull')
                check(entry['exact_signature']==signature_serial(t,frozen),f'{fam} {level} {control} camera {i} exact hull invariants')
                check(F(entry['signed_double_area_numerator'])==double_area and entry['signed_double_area_denominator_sqrt_squared']==norm(t),f'{fam} {level} {control} camera {i} positive hull area')
                # verify each registered index traces to a projected retained hull vertex
                refs=[uq[k] for k in entry['hull_indices_into_projected_distinct']]
                check(len(refs)==len(p) and any(all(point_equal(t,a,b) for a,b in zip(p,seq)) for seq in permutations(refs,True,True,True)),f'{fam} {level} {control} camera {i} hull index certificate')
            computed.append(p);ranks.append(r)
            if chk_ok:valid.append(i)
            else:invalid.append(i)
        check(rr['rank_counts']=={str(k):ranks.count(k) for k in range(3)},f'{fam} {level} {control} rank counts')
        check(rr['evaluable_count']==len(valid) and rr['not_evaluable_count']==len(invalid),f'{fam} {level} {control} evaluation accounting')
        check(rr['not_evaluable_indices']==invalid and rr['not_evaluable_triples']==[list(cameras[i]) for i in invalid],f'{fam} {level} {control} invalid identities')
        if control=='TR-L':
            check([cameras[i] for i in invalid]==[(-1,0,0),(1,0,0)],f'{fam} {level} TR-L excluded exact axes')
        if is_silhouette:check(all(k==2 for k in ranks),f'{fam} {level} {control} ranks all 2')
        for group in ('SO2','O2'):
            so=(group=='SO2')
            keys=[canonical_key(cameras[i],computed[i],closed,is_silhouette,so) if i in valid else None for i in range(N)]
            matrix=[[None if (i in invalid or j in invalid) else keys[i]==keys[j] for j in range(N)] for i in range(N)]
            matrix_comparisons+=N*N
            check(rr[group]['pairwise_equivalence_matrix']==matrix,f'{fam} {level} {control} {group} complete pair matrix')
            part=partition(matrix,valid)
            check(rr[group]['classes_camera_indices']==part,f'{fam} {level} {control} {group} complete partition')
            check(rr[group]['classes_camera_triples']==[[list(cameras[i]) for i in grp] for grp in part],f'{fam} {level} {control} {group} partition triples')
            check(rr[group]['class_count']==len(part),f'{fam} {level} {control} {group} class count')
            check(rr[group]['class_size_multiset']==sorted(map(len,part)),f'{fam} {level} {control} {group} class-size multiset')
            check(sum(map(len,part))==len(valid),f'{fam} {level} {control} {group} class-size sum')
            check(all(matrix[i][i] for i in valid),f'{fam} {level} {control} {group} reflexivity')
            check(all(matrix[i][j]==matrix[j][i] for i in valid for j in valid),f'{fam} {level} {control} {group} symmetry')
            check(all(not matrix[i][j] or not matrix[j][k] or matrix[i][k] for i in valid for j in valid for k in valid),f'{fam} {level} {control} {group} transitivity')
        smat=rr['SO2']['pairwise_equivalence_matrix'];omat=rr['O2']['pairwise_equivalence_matrix']
        check(all(not smat[i][j] or omat[i][j] for i in valid for j in valid),f'{fam} {level} {control} SO2 refinement')
        check(all(omat[i][cameras.index(tuple(-q for q in cameras[i]))] for i in valid),f'{fam} {level} {control} antipodal O2')
        if control=='TR-L':check(rr['SO2']['class_count']==line_oracle[fam][level] and rr['O2']['class_count']==line_oracle[fam][level],f'{fam} {level} line oracle')
        if level=='G0' and control=='CS-T':check((rr['SO2']['class_count'],rr['O2']['class_count'])==(6,3),f'{fam} {level} tetrahedron oracle')
        if level=='G0' and control=='CS-B':check((rr['SO2']['class_count'],rr['O2']['class_count'])==(3,3),f'{fam} {level} box oracle')
        per.append({'family':fam,'level':level,'control':control,'cameras':N,'evaluable':len(valid),'ranks':rr['rank_counts'],'SO2':rr['SO2']['class_count'],'O2':rr['O2']['class_count'],'SO2_sizes':rr['SO2']['class_size_multiset'],'O2_sizes':rr['O2']['class_size_multiset']})

for control in controls:
    x=resultmap[('A','G0')]['control_results'][control];y=resultmap[('B','G0')]['control_results'][control]
    check(x==y,f'G0 full {control} byte-structure equality')
for fam in ('A','B'):
    for name in controls:
        for group in ('SO2','O2'):
            vals=[resultmap[(fam,l)]['control_results'][name][group]['class_count'] for l in ('G0','G1','G2')]
            check(vals==sorted(vals),f'{fam} {name} {group} nested class monotonicity')

summary={'audit':'MERU_3D_V4_INDEPENDENT_EXACT_QC','status':'PASS' if not failures else 'FAIL','source':'independent code, no import/execution of registered calculator','original_result_sha256':hashlib.sha256(raw).hexdigest(),'checks':checks,'failed_checks':len(failures),'failures':failures,'matrix_entries_independently_calculated':matrix_comparisons,'geometry_records':len(per),'per_control_grid':per,'proof_scope':'Exact finite orthographic projected continuous PL-trace and filled convex-polytope congruence only'}
OUT.write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n')
print('QC status',summary['status'],'checks',checks,'failures',len(failures),'matrix cells',matrix_comparisons,'records',len(per));print('summary')
for x in per:print(x['family'],x['level'],x['control'],x['SO2'],x['O2'])
if failures:
 print('FAILURES:');print('\n'.join(failures[:60]));sys.exit(1)
