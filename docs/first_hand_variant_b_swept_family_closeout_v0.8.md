# First Hand Variant-B Swept-Family Analytic Closeout

**Checkpoint:** `first_hand_variant_b_swept_family_closeout_v0.8`  
**Status:** CLOSED — REGISTERED 400-CELL VARIANT-B SWEEP EXECUTED  
**Phase:** Variant-B source-constrained carrier sweep  
**Carrier family:** normalized elliptic fat torus  
**Historical span:** 1.5 turns  
**Registered carrier cells:** 25  
**Registered spiral branches:** 8  
**Registered scales:** 2  
**Registered endpoint cells:** 400  
**Technical failures:** 0  
**Parallel transport used:** no  
**Image pixel data used:** no  
**Adaptive refinement used:** no

## 1. Purpose

This note closes the preregistered Variant-B swept-family checkpoint.

The checkpoint tested one explicit, source-constrained but non-unique Dimpled-Sphere reconstruction family against Stan Tenen's endpoint-parallelism criterion.

The registered matrix crossed:

- 25 embedded genus-1 carrier surfaces;
- one reciprocal FIRST HAND candidate;
- six fixed generic logarithmic comparators;
- one Golden Mean logarithmic comparator;
- two frozen G30/GHALF mapping scales.

The resulting execution contained exactly

\[
25\times8\times2
=
400
\]

registered geometric cells.

No parameter fitting, interpolation, root finding, adaptive refinement, endpoint movement, image fitting, or post-hoc carrier extension was used.

---

## 2. Carrier family

The registered carrier was

\[
X_{w,e}(u,v)
=
\left(
(R+a\cos u)\cos v,\,
(R+a\cos u)\sin v,\,
ea\sin u
\right),
\]

with

\[
R=\frac{1+w}{2},
\qquad
a=\frac{1-w}{2}.
\]

Therefore

\[
R+a=1
\]

and

\[
R-a=w.
\]

The registered throat values were

\[
w\in
\{
0.02,\,
0.05,\,
0.10,\,
0.20,\,
0.30
\},
\]

and the registered axial elongations were

\[
e\in
\{
1.4,\,
1.6,\,
1.8,\,
2.0,\,
2.2
\}.
\]

All 25 registered carriers satisfied the analytic admissibility conditions and were embedded genus-1 tori.

The preregistered exterior sphere-likeness diagnostic ranged from

\[
0.0182727362283
\]

to

\[
0.151325076026.
\]

This diagnostic was descriptive only and was not used to remove any cell.

---

## 3. Primary registered outcome states

The reciprocal branch closed with:

`NO_REGISTERED_RECIPROCAL_DIRECTED_PARALLEL_CELL`

and

`NO_REGISTERED_RECIPROCAL_LINE_PARALLEL_CELL`.

The logarithmic branches closed with:

`NO_REGISTERED_LOG_DIRECTED_COUNTEREXAMPLE`

and

`NO_REGISTERED_LOG_LINE_COUNTEREXAMPLE`.

There were

\[
0
\]

technical failures.

Thus no registered reciprocal, generic logarithmic, or Golden Mean cell achieved exact endpoint parallelism under either preregistered ambient semantic definition.

---

## 4. Reciprocal fixed-grid minima

Across the 50 reciprocal carrier/scale cells, the smallest directed mismatch was

\[
\Delta_{\rm R,dir}^{\min}
=
120.011101077^\circ,
\]

at

`VB-W20-E22-RECIPROCAL-GHALF`.

The smallest unoriented line mismatch was

\[
\Delta_{\rm R,line}^{\min}
=
35.9536384884^\circ,
\]

at

`VB-W02-E22-RECIPROCAL-G30`.

Therefore the reciprocal candidate remained far from exact endpoint parallelism throughout the registered grid.

---

## 5. Logarithmic fixed-grid minima

The per-family minima were:

| Spiral | Directed min (deg) | Line min (deg) |
|---|---:|---:|
| `LOG-M050` | 167.682531585 | 7.08894346569 |
| `LOG-M075` | 160.310260077 | 6.78843232493 |
| `LOG-M100` | 152.509157084 | 4.79031388167 |
| `LOG-M125` | 154.398057584 | 5.7381129598 |
| `LOG-M150` | 148.298767294 | 7.23663870941 |
| `LOG-M200` | 134.779869323 | 13.3425910249 |
| `GOLDEN-MEAN` | 153.960120335 | 6.44128402709 |

The global logarithmic directed minimum was

\[
134.779869323^\circ,
\]

at

`VB-W20-E22-LOG-M200-GHALF`.

The global logarithmic line minimum was

\[
4.79031388167^\circ,
\]

at

`VB-W10-E22-LOG-M100-G30`.

No logarithmic cell reached the exact-parallel tolerance.

---

## 6. Global-minimum comparison is not a matched-condition test

The reciprocal and logarithmic global minima occur on different carrier/scale cells.

Therefore comparing only the best reciprocal cell with the best logarithmic cell does not establish matched-condition dominance.

A post-execution read of the already-frozen 400-cell JSON was therefore performed by grouping results at identical:

\[
(w,e,k)
\]

conditions.

This did not evaluate new geometry.

It did not add any cell.

It did not alter any parameter.

It was a descriptive query of the already-executed registered matrix.

For each logarithmic branch and matched carrier/scale condition, define

\[
D_{\rm matched}
=
\Delta_{\log}
-
\Delta_R.
\]

Thus:

- \(D_{\rm matched}<0\): logarithmic branch is closer to parallel;
- \(D_{\rm matched}>0\): reciprocal branch is closer to parallel.

There are

\[
25\times2\times7
=
350
\]

matched reciprocal-versus-logarithmic comparisons under each semantic definition.

---

## 7. Matched directed comparison

Under directed ambient-vector semantics:

\[
\boxed{
\text{reciprocal is closer in }350/350\text{ matched comparisons}
}
\]

and

\[
\boxed{
\text{logarithmic is closer in }0/350
}
\]

with no ties.

The per-family results were:

| Log branch | Log closer | Reciprocal closer | Median \(D_{\rm matched}\) | Range |
|---|---:|---:|---:|---:|
| `GOLDEN-MEAN` | 0/50 | 50/50 | \(+37.797507^\circ\) | \(+11.140939\) to \(+44.760179^\circ\) |
| `LOG-M050` | 0/50 | 50/50 | \(+42.453461^\circ\) | \(+23.650568\) to \(+50.172153^\circ\) |
| `LOG-M075` | 0/50 | 50/50 | \(+43.887728^\circ\) | \(+16.263899\) to \(+51.554566^\circ\) |
| `LOG-M100` | 0/50 | 50/50 | \(+41.706294^\circ\) | \(+8.856848\) to \(+50.876352^\circ\) |
| `LOG-M125` | 0/50 | 50/50 | \(+37.177051^\circ\) | \(+11.598415\) to \(+43.920617^\circ\) |
| `LOG-M150` | 0/50 | 50/50 | \(+28.861811^\circ\) | \(+20.793082\) to \(+39.262368^\circ\) |
| `LOG-M200` | 0/50 | 50/50 | \(+16.591117^\circ\) | \(+11.895144\) to \(+23.943542^\circ\) |

The smallest directed reciprocal advantage occurred against `LOG-M100` at

`VB-W02-E22-G30`:

\[
D_{\rm matched}
=
+8.856848474^\circ.
\]

The largest directed reciprocal advantage occurred against `LOG-M075` at

`VB-W20-E22-GHALF`:

\[
D_{\rm matched}
=
+51.554566134^\circ.
\]

Therefore the directed ranking is not a global-minimum artifact.

Within this frozen Variant-B matrix, the reciprocal branch is uniformly closer to directed endpoint alignment than every registered logarithmic branch under the same carrier and scale conditions.

However, the reciprocal still fails the absolute source criterion strongly, with best directed mismatch

\[
120.011101077^\circ.
\]

Thus directed semantics reproduces the **relative ordering** favorable to the reciprocal without reproducing the claimed endpoint parallelism itself.

---

## 8. Matched unoriented-line comparison

Under unoriented ambient tangent-line semantics:

\[
\boxed{
\text{logarithmic is closer in }350/350\text{ matched comparisons}
}
\]

and

\[
\boxed{
\text{reciprocal is closer in }0/350
}
\]

with no ties.

The per-family results were:

| Log branch | Log closer | Reciprocal closer | Median \(D_{\rm matched}\) | Range |
|---|---:|---:|---:|---:|
| `GOLDEN-MEAN` | 50/50 | 0/50 | \(-37.797507^\circ\) | \(-44.760179\) to \(-11.140939^\circ\) |
| `LOG-M050` | 50/50 | 0/50 | \(-42.453461^\circ\) | \(-50.172153\) to \(-23.650568^\circ\) |
| `LOG-M075` | 50/50 | 0/50 | \(-43.887728^\circ\) | \(-51.554566\) to \(-16.263899^\circ\) |
| `LOG-M100` | 50/50 | 0/50 | \(-41.706294^\circ\) | \(-50.876352\) to \(-8.856848^\circ\) |
| `LOG-M125` | 50/50 | 0/50 | \(-37.177051^\circ\) | \(-43.920617\) to \(-11.598415^\circ\) |
| `LOG-M150` | 50/50 | 0/50 | \(-28.861811^\circ\) | \(-39.262368\) to \(-20.793082^\circ\) |
| `LOG-M200` | 50/50 | 0/50 | \(-16.591117^\circ\) | \(-23.943542\) to \(-11.895144^\circ\) |

Therefore the line-semantic ordering is also not a global-minimum artifact.

Within every matched registered carrier/scale condition, every logarithmic branch is closer to unoriented tangent-line parallelism than the reciprocal branch.

---

## 9. Exact semantic ranking reversal

The matched directed and line comparison summaries are exact sign reversals.

The executed endpoint pairs satisfy the anti-parallel-side relation

\[
d
=
\tau_o\cdot\tau_i
<
0,
\]

so

\[
\Delta_{\rm line}
=
180^\circ
-
\Delta_{\rm dir}.
\]

Hence for any matched reciprocal/logarithmic comparison:

\[
\Delta_{\log,\rm line}
-
\Delta_{R,\rm line}
=
-
\left(
\Delta_{\log,\rm dir}
-
\Delta_{R,\rm dir}
\right).
\]

Therefore the semantic ranking reversal is mathematically forced once both compared endpoint pairs lie on this side of orientation space.

This explains the complete \(350/350\) reversal:

- directed semantics uniformly favors the reciprocal;
- unoriented line semantics uniformly favors the logarithmic branches.

This is not numerical noise and not a consequence of comparing different best-fit carriers.

It is a structural consequence of the orientation-sensitive versus orientation-insensitive endpoint definitions on the executed matrix.

---

## 10. Interpretation of the semantic reversal

The audit must not select one semantic definition post hoc based on which family it favors.

Both were preregistered in Variant B because Tenen's word "parallel" does not itself resolve vector orientation.

However, the historical audit record predates Variant B:

- the original S1 preregistration intentionally used directed tangents;
- anti-parallel tangents were explicitly not allowed to count as compatible;
- the use of \(|d|\) was prohibited.

Therefore directed orientation was already regarded as the stronger operationalization before the present Variant-B results existed.

The Variant-B checkpoint nevertheless reports both semantics exactly as preregistered.

The correct interpretation is:

> If continuous oriented endpoint agreement is required, the reciprocal branch is uniformly closer than every registered logarithmic branch under matched conditions, but still fails the absolute criterion by at least \(120.01^\circ\).

and:

> If endpoint parallelism means only unoriented tangent-line collinearity, every registered logarithmic branch is uniformly closer than the reciprocal under matched conditions, although no logarithmic cell reaches exact parallelism.

Thus the source claim is not vindicated under either interpretation:

- under directed semantics, the claimed reciprocal endpoint match is absent;
- under line semantics, the logarithmic families are systematically closer to the stated geometric condition than the reciprocal branch.

---

## 11. Relation to the 1.5-turn structure

The registered Variant-B mapping fixes

\[
v(\theta)=\theta-1,
\]

with

\[
v_i-v_o=3\pi.
\]

Therefore the azimuthal component undergoes an odd half-turn:

\[
3\pi
\equiv
\pi
\pmod{2\pi}.
\]

This introduces a built-in reversal of the toroidal direction between endpoints.

The mapped tangent is

\[
C'(\theta)
=
X_u u'(\theta)
+
X_v.
\]

Because the tangent includes both meridional and toroidal components, the exact planar logarithmic parity theorem established earlier does not transfer directly to Variant B.

The present results therefore support only the more limited statement:

> The frozen 1.5-turn mapping contains an azimuthal half-turn reversal that plausibly contributes strongly to the observed anti-parallel-side endpoint geometry.

A direct even-turn Variant-B test would require a new preregistration.

No such test is part of this checkpoint.

---

## 12. Variant-A comparison

The sealed Variant-A ambient reciprocal values were:

### G30

\[
\Delta_{\rm A,dir}
=
143.58427150706095^\circ,
\]

\[
\Delta_{\rm A,line}
=
36.415728492939074^\circ.
\]

### GHALF

\[
\Delta_{\rm A,dir}
=
143.29594953287508^\circ,
\]

\[
\Delta_{\rm A,line}
=
36.70405046712493^\circ.
\]

The best Variant-B reciprocal directed result uses GHALF:

\[
120.011101077^\circ.
\]

Compared with the corresponding Variant-A GHALF ambient result, the registered Variant-B family reduces the directed mismatch by approximately

\[
143.29594953287508^\circ
-
120.011101077^\circ
=
23.2848484559^\circ.
\]

The best Variant-B reciprocal line result uses G30:

\[
35.9536384884^\circ.
\]

Compared with Variant-A G30:

\[
36.415728492939074^\circ
-
35.9536384884^\circ
=
0.4620900045^\circ.
\]

Thus the largest apparent change is semantics-dependent.

More importantly, Variant B changed both:

- carrier geometry;
- spiral-to-surface mapping.

Therefore the difference cannot be attributed causally to "the dimple" alone.

The allowed statement is:

> The registered Variant-B realization improves the best directed reciprocal mismatch relative to the corresponding Variant-A ambient result, while changing the best line mismatch only slightly; the cause cannot be uniquely assigned because carrier and mapping changed together.

---

## 13. Boundary-minimum finding

Every one of the 16 reported fixed-grid minima touches at least one boundary of the registered \((w,e)\) parameter rectangle:

- 2 reciprocal minima;
- 14 logarithmic/Golden Mean minima.

The active boundaries include:

\[
w=0.02,
\]

\[
w=0.30,
\]

\[
e=1.4,
\]

and

\[
e=2.2.
\]

No reported family/semantics minimum occurs with both carrier coordinates strictly interior to the registered grid.

Therefore:

> **The registered sweep does not demonstrate bracketing of an interior optimum for any reported family/semantics combination.**

This does not prove that a continuous optimum lies outside the registered box.

It does show that the current finite grid is insufficient to establish an interior minimum.

Any widened parameter sweep, boundary extension, interpolation, or continuous optimization must be treated as a new checkpoint with a new preregistration.

The present results must not be extended adaptively.

---

## 14. Source-facing scope

This checkpoint does **not** recover a unique historical Dimpled-Sphere.

The elliptic fat-torus family is an audit reconstruction chosen because it satisfies explicit source-level morphological and topological constraints.

Therefore the result applies to:

> the registered reciprocal/logarithmic radial laws, the registered elliptic-fat-torus carrier family, the frozen 1.5-turn spiral-to-surface mapping, and the registered G30/GHALF scale conventions.

It does not establish the behavior of every possible Meru FIRST HAND construction.

---

## 15. Important limit from the source construction language

The Meru source material describes more than one route to a FIRST HAND vortex.

The source refers to several specially arranged algebraic constructions and at least one geometric construction.

It also describes the possibility of bending the vortex until its outer end becomes parallel to its inner tip.

Therefore a physical FIRST HAND sculpture may contain additional shape deformation not captured by the present closed-form reciprocal radial law plus frozen carrier mapping.

This creates a genuine scope limit for the analytic audit.

The present checkpoint can reject the registered realization as a reproduction of the claimed endpoint-parallel geometry.

It cannot, by itself, reject every hand-adjusted or differently constructed FIRST HAND object.

---

## 16. Strongest defensible reciprocal conclusion

The strongest result supported by the frozen Variant-B sweep is:

> **No exact reciprocal endpoint-parallel cell was found in the preregistered 25-carrier Variant-B family at either registered scale. The best directed mismatch remained \(120.0111^\circ\), and the best unoriented line mismatch remained \(35.9536^\circ\).**

Moreover:

> **Under matched carrier and scale conditions, the reciprocal branch is closer than every registered logarithmic branch in all 350 directed comparisons.**

Thus the source's intended reciprocal-versus-logarithmic ordering is reproduced under directed semantics, but the claimed absolute reciprocal endpoint match is not.

---

## 17. Strongest defensible logarithmic conclusion

No logarithmic branch reached exact endpoint parallelism.

Therefore the registered sweep contains no exact logarithmic counterexample to the source's universal negative claim.

However:

> **Under unoriented tangent-line semantics, every registered logarithmic branch is closer than the reciprocal branch in all 350 matched carrier/scale comparisons.**

The global logarithmic line mismatch reaches

\[
4.79031388167^\circ,
\]

compared with the reciprocal minimum of

\[
35.9536384884^\circ.
\]

Thus if "parallel" is interpreted as unoriented tangent-line alignment, the relative geometry strongly favors the very logarithmic families the source seeks to exclude, although none achieves exact equality in the frozen grid.

This is a major semantic sensitivity of the source criterion.

---

## 18. What is established

Within the registered Variant-B reconstruction:

1. all 400 cells executed successfully;
2. no reciprocal cell reached exact directed parallelism;
3. no reciprocal cell reached exact line parallelism;
4. no logarithmic cell reached exact directed parallelism;
5. no logarithmic cell reached exact line parallelism;
6. reciprocal beats every logarithmic comparator in all 350 matched directed comparisons;
7. logarithmic beats reciprocal in all 350 matched line comparisons;
8. the ranking reversal follows the anti-parallel-side geometry and the use or removal of tangent orientation;
9. all reported fixed-grid minima lie on at least one carrier-parameter boundary;
10. the registered grid does not bracket a demonstrated interior optimum;
11. the result does not identify a unique historical Dimpled-Sphere.

---

## 19. What is not established

This checkpoint does not establish:

- that no possible Dimpled-Sphere can make the reciprocal endpoints parallel;
- that Tenen's entire FIRST HAND construction is false;
- that logarithmic self-embedment is impossible on every Dimpled-Sphere;
- that the registered elliptic fat torus is the exact historical carrier;
- that the registered spiral-to-surface map is historically unique;
- that the dimple alone causes the Variant-A/Variant-B change;
- that directed or unoriented semantics is uniquely mandated by the source;
- the continuous optimum over \(w,e\);
- behavior beyond the registered parameter boundaries;
- behavior at an even number of turns;
- intrinsic genus-1 parallel transport;
- finite-thickness physical insertion;
- curvature/frame compatibility;
- Hebrew-letter generation.

---

## 20. Methodological consequence

The Variant-B sweep reveals that endpoint "parallelism" is not a semantically neutral scalar criterion.

On the executed anti-parallel-side geometry:

\[
\Delta_{\rm line}
=
180^\circ-\Delta_{\rm dir}.
\]

Consequently, the semantic choice reverses the relative reciprocal/logarithmic ranking across the entire matched grid.

That result should be retained as a central methodological finding of v0.8.

It means future Meru audits must distinguish explicitly between:

- oriented tangent continuation;
- unoriented tangent-line collinearity;
- stronger physical nesting conditions.

These cannot be conflated.

---

## 21. No post-hoc grid extension

Because all reported minima touch registered parameter boundaries, it may be scientifically useful to study a broader carrier family later.

However, the current checkpoint is closed.

The following are forbidden as continuations of this execution:

- adding lower \(w\);
- adding higher \(w\);
- adding lower \(e\);
- adding higher \(e\);
- locally refining around a reported minimum;
- optimizing \(w,e\);
- root-finding for parallelism;
- selecting a new mapping based on the observed minima.

Any such study requires an independent preregistration.

---

## 22. Recommended next analytic direction

Before extending the carrier grid, the audit should return to the source and determine whether the "three specially arranged algebraic functions" or the geometric construction can be recovered in sufficiently explicit mathematical form.

This is preferable to immediately widening the present family because the current failure may arise from:

- carrier geometry;
- spiral-to-surface mapping;
- additional bending/deformation;
- or a genuinely different algebraic FIRST HAND construction.

A broader numerical sweep of the same reconstruction class cannot resolve that historical underdetermination by itself.

A separate Variant-B boundary-extension checkpoint may still be justified later, but it should not precede renewed source recovery unless the audit explicitly changes its goal from historical reconstruction to mathematical family exploration.

---

## 23. Closed checkpoint conclusion

The Variant-B swept-family checkpoint closes with:

`NO_REGISTERED_RECIPROCAL_DIRECTED_PARALLEL_CELL`

`NO_REGISTERED_RECIPROCAL_LINE_PARALLEL_CELL`

`NO_REGISTERED_LOG_DIRECTED_COUNTEREXAMPLE`

`NO_REGISTERED_LOG_LINE_COUNTEREXAMPLE`

and

\[
0
\]

technical failures.

The central analytic result is:

> **The registered reciprocal realization does not reproduce Tenen's claimed endpoint parallelism anywhere in the frozen Variant-B grid. Under directed semantics it nevertheless beats every registered logarithmic comparator in all 350 matched conditions; under unoriented line semantics the ranking reverses completely, and every logarithmic comparator beats the reciprocal in all 350 matched conditions.**

The strongest source-facing interpretation is therefore:

> **This checkpoint rejects one explicit, preregistered reciprocal + carrier + mapping realization as a successful reconstruction of the claimed FIRST HAND endpoint geometry. It does not falsify every possible Meru FIRST HAND construction, especially because the source itself allows multiple algebraic/geometric constructions and additional bending of the physical vortex.**

The boundary-minimum pattern further shows that this finite grid does not bracket an interior optimum, so any numerical extension must begin with a new preregistration.

---

## 24. Phase status

The analytic workflow now stands at:

\[
\text{Variant-A S1}
\]

\[
\downarrow
\]

\[
\text{Variant-A comparator analysis}
\]

\[
\downarrow
\]

\[
\text{Variant-A truncation-parity analysis}
\]

\[
\downarrow
\]

\[
\text{S1 source-criterion addendum}
\]

\[
\downarrow
\]

\[
\text{Variant-A ambient-parallelism bridge}
\]

\[
\downarrow
\]

\[
\text{Variant-B source geometry specification}
\]

\[
\downarrow
\]

\[
\text{Variant-B swept-family preregistration}
\]

\[
\downarrow
\]

\[
\text{Variant-B implementation freeze}
\]

\[
\downarrow
\]

\[
\text{registered 400-cell Variant-B execution}
\]

\[
\downarrow
\]

\[
\text{matched-cell read of frozen execution}
\]

\[
\downarrow
\]

\[
\boxed{\text{Variant-B swept-family analytic closeout}}
\]

The next phase should begin from renewed source recovery or a separately preregistered extension, not by modifying this closed sweep.
