#!/usr/bin/env python3
"""Read-only exact QC for the registered Meru 3D-V3 JSON.

This code is independently authored. It never imports, invokes or modifies
its registered scientific calculator, and it does not produce new V3 trial data.
"""
import argparse
import hashlib
import itertools
import json
from collections import Counter
from fractions import Fraction as Q
from pathlib import Path


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def cross(a, b):
    return (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0])


def strata():
    a0 = sorted([tuple(s if k == i else 0 for k in range(3))
                 for i in range(3) for s in (-1, 1)])
    corners = sorted(itertools.product((-1, 1), repeat=3))
    edges = sorted({tuple(x) for z in range(3)
                    for signs in itertools.product((-1, 1), repeat=2)
                    for x in [tuple(0 if i == z else signs[i-(i>z)] for i in range(3))]})
    ratio = set()
    for z in range(3):
        ids = [i for i in range(3) if i != z]
        for a, b in ((1, 2), (2, 1)):
            for p, q in itertools.product((-1, 1), repeat=2):
                t = [0,0,0]; t[ids[0]]=p*a; t[ids[1]]=q*b
                ratio.add(tuple(t))
    return {'A0': a0, 'C': corners, 'E': edges, 'T': sorted(ratio)}


def cameras(strata_map, family, level):
    names = ['A0'] + (['C'] if family == 'A' else ['E']) * (level >= 1) + ([('E' if family == 'A' else 'T')] if level == 2 else [])
    return [(v, name) for name in names for v in strata_map[name]]


def controls():
    orig = {
        'F': [(0,0,0), (1,0,0), (0,2,0), (0,0,3)],
        'L': [(0,0,0), (1,0,0), (3,0,0)],
        'P': [(0,0,0), (1,0,0), (0,2,0)],
    }
    return {key: [tuple(Q(p[i])-sum(Q(q[i]) for q in pts)/len(pts) for i in range(3)) for p in pts]
            for key, pts in orig.items()}


def data_at(n, points, control):
    # Intrinsic 3D projection operator I - v v^t /(v.v), never construct planar frame.
    d = dot(n, n)
    p = [dot(n, y) for y in points]
    gram = tuple(tuple(dot(a,b) - p[i]*p[j]/d for j,b in enumerate(points)) for i,a in enumerate(points))
    crossnum = tuple(dot(n,cross(points[i],points[j])) for i in range(len(points)) for j in range(i+1,len(points)))
    rank = 2 if any(crossnum) else (1 if any(gram[i][i] for i in range(len(points))) else 0)
    status = 'NOT_EVALUABLE' if control == 'L' and rank == 0 else 'EVALUABLE'
    return gram, crossnum, d, rank, status


def exact_areas_equal(u, v):
    a, d = u
    b, e = v
    return (a == b == 0) or (a*b > 0 and a*a*e == b*b*d)


def normalize_q(q):
    return str(q)


class Recorder:
    def __init__(self): self.checks = 0; self.failures = []; self.topics = Counter()
    def check(self, condition, label, topic='general'):
        self.checks += 1; self.topics[topic]+=1
        if not condition:
            self.failures.append(label)


def validate(path):
    rec = Recorder()
    actual = json.loads(path.read_text(encoding='utf-8'))
    smap = strata(); pts = controls()
    for n, count in [('A0',6),('C',8),('E',12),('T',24)]:
        rec.check(len(smap[n])==count, f'stratum {n} cardinality', 'sets')
        rec.check(len(smap[n])==len(set(smap[n])) and all(tuple(-z for z in p) in smap[n] for p in smap[n]),f'stratum {n} antipodal', 'sets')
    rec.check(actual.get('stratum_counts')=={k:len(v) for k,v in smap.items()}, 'original JSON stratum counts','sets')
    rec.check(actual.get('preregistration_commit')=='67ccaa1f5292acee31e26e318e7bff3bc2e7f5ec','signed prereg commit','provenance')
    rec.check(actual.get('preregistration_blob')=='f835cde4ec7890a66ef2a82f3f5699361752371e','signed prereg blob','provenance')
    rec.check(actual.get('study')=='MERU_3D_V3','study marker','provenance')
    rec.check(actual.get('outcome')=='MERU_3D_V3_LABELLED_PROJECTION_EQUIVALENCE_PASS','reported outcome marker','provenance')
    EXPECTED = {
      ('A','G0'): ((6,3),(6,3),(1,1),(4,3),4),
      ('A','G1'): ((14,7),(14,7),(2,2),(8,5),4),
      ('A','G2'): ((26,13),(26,13),(3,3),(14,9),8),
      ('B','G0'): ((6,3),(6,3),(1,1),(4,3),4),
      ('B','G1'): ((18,9),(18,9),(2,2),(10,7),8),
      ('B','G2'): ((42,21),(42,21),(4,4),(22,15),16),
    }
    gotrows = actual['family_level_results']
    rec.check(len(gotrows)==6,'six family-level entries','sets')
    rec.check([(r['family'],r['level']) for r in gotrows] == list(EXPECTED), 'family-level order','sets')
    summaries=[]
    g0s=[]
    for row in gotrows:
      family, level = row['family'],row['level']
      key=(family,level)
      if key not in EXPECTED: rec.check(False,f'unexpected family-tier {key}', 'sets'); continue
      ref=EXPECTED[key]
      cs=cameras(smap,family,int(level[1]))
      vs=[t for t,s in cs]
      axes=[]
      for name in (['A0']+(['C'] if family=='A' else ['E'])*(int(level[1])>=1)+([('E' if family=='A' else 'T')] if int(level[1])==2 else [])):
          for v in smap[name]:
              x=next(c for c in v if c !=0)
              if x>0: axes.append(v)
      rec.check(row['signed_camera_triples']==[list(v) for v in vs],f'{key} camera triple order','sets')
      rec.check(row['axis_representatives']==[list(v) for v in axes],f'{key} axis representatives','sets')
      rec.check(row['signed_camera_count']==ref[0][0] == len(vs),f'{key} signed count','sets')
      rec.check(row['axis_count']==ref[0][1] ==len(axes),f'{key} axis count','sets')
      rec.check(row['oracle_verified'] is True,f'{key} reported oracle flag','general')
      if level=='G0': g0s.append(row)
      for ci,(control,points) in enumerate(pts.items()):
        result=row['control_results'][control]
        inf=[data_at(v,points,control) for v in vs]
        rankcounts=Counter(t[3] for t in inf)
        ne=[i for i,t in enumerate(inf) if t[4]=='NOT_EVALUABLE']
        rec.check(result['camera_count']==len(vs),f'{key}-{control} cameras','rank')
        rec.check(result['rank_counts']=={str(i):rankcounts[i] for i in range(3)},f'{key}-{control} rank census','rank')
        rec.check(result['evaluable_count']==len(vs)-len(ne),f'{key}-{control} evaluable count','rank')
        rec.check(result['not_evaluable_count']==len(ne)==(2 if control=='L' else 0),f'{key}-{control} not eval count','rank')
        rec.check(result['not_evaluable_camera_indices']==ne,f'{key}-{control} not eval indices','rank')
        rec.check(result['not_evaluable_camera_triples']==[list(vs[i]) for i in ne],f'{key}-{control} not eval triples','rank')
        if control=='P': rec.check(rankcounts[1]==ref[4],f'{key} P rank-one oracle','rank')
        rec.check(len(result['per_camera'])==len(vs),f'{key}-{control} per-camera record size','camera')
        for i,(v,name) in enumerate(cs):
            t=inf[i]
            if i >= len(result['per_camera']): continue
            z=result['per_camera'][i]; gram,areas,d,rank,status=t
            for fld,want in [('index',i),('triple',list(v)),('stratum',name),('norm_squared',d),('rank',rank),('status',status)]:
                rec.check(z[fld]==want,f'{key}-{control} camera {i} {fld}','camera')
            inv=z['exact_invariants']
            rec.check(inv['gram']==[[normalize_q(x) for x in gr] for gr in gram],f'{key}-{control} camera {i} complete Gram','invariant')
            rec.check(inv['oriented_minors_numerators']==list(map(normalize_q,areas)),f'{key}-{control} camera {i} oriented minors','invariant')
            rec.check(inv['oriented_minors_shared_sqrt_denominator_squared']==d,f'{key}-{control} camera {i} common area denominator','invariant')
        ms={}
        for group in ('SO2','O2'):
            expected_mat=[]
            for i,a in enumerate(inf):
                rowm=[]
                for j,b in enumerate(inf):
                    if i in ne or j in ne:
                        rowm.append(None)
                    else:
                        gram_eq=(a[0]==b[0]);area_eq=all(exact_areas_equal((p,a[2]),(q,b[2])) for p,q in zip(a[1],b[1]))
                        rowm.append(bool(gram_eq and (group=='O2' or area_eq)))
                expected_mat.append(rowm)
            ms[group]=expected_mat
            obs=result[group]
            rec.check(obs['pairwise_equivalence_matrix']==expected_mat,f'{key}-{control} {group} complete pair matrix','pair-matrix')
            for i in range(len(vs)):
                for j in range(len(vs)):
                    rec.check(obs['pairwise_equivalence_matrix'][i][j]==expected_mat[i][j],f'{key}-{control} {group} pair [{i},{j}]','pairs')
            eligible=[i for i in range(len(vs)) if i not in ne]
            partitions=[];remaining=set(eligible)
            while remaining:
                i=min(remaining)
                klass=[j for j in eligible if expected_mat[i][j]]
                partitions.append(klass)
                remaining.difference_update(klass)
            rec.check(obs['classes_camera_indices']==partitions,f'{key}-{control} {group} exact classes','partitions')
            rec.check(obs['classes_camera_triples']==[[list(vs[i]) for i in klass] for klass in partitions],f'{key}-{control} {group} class triples','partitions')
            rec.check(obs['class_count']==len(partitions)==ref[ci+1][0 if group=='SO2' else 1],f'{key}-{control} {group} frozen count oracle','partitions')
            rec.check(obs['class_size_multiset']==sorted(map(len,partitions)),f'{key}-{control} {group} sizes','partitions')
            rec.check(all(expected_mat[i][i] and expected_mat[i][j]==expected_mat[j][i] for i in eligible for j in eligible),f'{key}-{control} {group} reflexive symmetric','algebra')
            rec.check(all(not(expected_mat[i][j] and expected_mat[j][k]) or expected_mat[i][k] for i in eligible for j in eligible for k in eligible),f'{key}-{control} {group} transitive','algebra')
        rec.check(all(not ms['SO2'][i][j] or ms['O2'][i][j] for i in range(len(vs)) for j in range(len(vs)) if i not in ne and j not in ne),f'{key}-{control} SO2 refines O2','algebra')
        rec.check(all(ms['O2'][i][vs.index(tuple(-a for a in vs[i]))] for i in range(len(vs)) if i not in ne),f'{key}-{control} antipodal O2','algebra')
      summaries.append({'family':family,'level':level,'signed':len(vs),'axes':len(axes),'counts':{control:{group:row['control_results'][control][group]['class_count'] for group in ('SO2','O2')} for control in pts},'P_rank_one':row['control_results']['P']['rank_counts']['1']})
    rec.check(len(g0s)==2 and g0s[0]['signed_camera_triples']==g0s[1]['signed_camera_triples'] and g0s[0]['control_results']==g0s[1]['control_results'],'identical G0 results','algebra')
    rec.check(actual.get('g0_identical_camera_order_and_results') is True,'original G0 identity claim','general')
    return {'study':'MERU_3D_V3_INDEPENDENT_READ_ONLY_QC','source_json_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'checked_source_json':str(path.name),'total_independent_checks':rec.checks,'passed':rec.checks-len(rec.failures),'failed':len(rec.failures),'failure_examples':rec.failures[:100],'check_counts_by_topic':dict(sorted(rec.topics.items())),'six_row_summaries':summaries,'result':'PASS' if not rec.failures else 'FAIL','notes':['Independent Fraction and integer-square radical-comparison implementation; no registered code imported or run','Complete per-camera Gram, oriented-minor, rank and status checks','Complete pairwise equality matrices checked entry by entry; class membership, size, SO2/O2 and antipodal guards verified','Operator-supplied exit_code.txt was not included in this upload; verify locally before signing.']}


if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('json_path',type=Path)
    ap.add_argument('output_path',type=Path)
    a=ap.parse_args()
    report=validate(a.json_path)
    a.output_path.write_text(json.dumps(report,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    print(json.dumps({k:report[k] for k in ('total_independent_checks','passed','failed','result','check_counts_by_topic')}))
    raise SystemExit(0 if report['result']=='PASS' else 2)
