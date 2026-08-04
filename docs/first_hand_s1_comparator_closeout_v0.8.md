# First Hand S1 Comparator Analytic Findings and Closeout

**Checkpoint:** `first_hand_s1_comparator_closeout_v0.8`  
**Status:** CLOSED — COMPARATOR MATRIX EXECUTED AND RECORDED  
**Phase:** analytic self-embedment audit  
**Prerequisite comparator preregistration:** `first_hand_s1_comparator_preregistration_v0.8`  
**Variant:** A — cube-octahedral / canonical inverse-gnomonic sphere only  
**Primary comparison domain:** finite AOG-DIAGRAM branch only  
**Reciprocal reference recomputed:** no  
**Image pixel data used:** no

## 1. Purpose

This note closes the preregistered First Hand S1 comparator checkpoint.

It records the scientific findings of the completed comparator matrix, preserves the preregistered decision rule, and fixes the interpretation boundary before any later extension is designed.

No comparator branch is rerun in this closeout.

No growth-rate range is extended.

No new logarithmic grid points are added.

No comparator normalization is changed.

No alternate spherical scale is introduced.

No AOG-PROSE comparator proxy is invented.

No dimpled-sphere / toroidal Variant-B construction is introduced.

The generated execution artifacts remain the authoritative numerical record:

- `results/first_hand_s1_comparators_v0_8/s1_comparator_results.csv`
- `results/first_hand_s1_comparators_v0_8/s1_comparator_results.json`
- `results/first_hand_s1_comparators_v0_8/s1_comparator_report.md`

---

## 2. Registered comparative question

The completed reciprocal S1 checkpoint had established large absolute directed tangent mismatches for the AOG-DIAGRAM branch:

### G30

\[
\Delta_{R,\mathrm{G30}}
=
144.5776221089075^\circ.
\]

### GHALF

\[
\Delta_{R,\mathrm{GHALF}}
=
144.2022631722743^\circ.
\]

The comparator checkpoint asked:

> Under the same finite Variant-A spherical map and the same intrinsic directed tangent statistic, does the reciprocal spiral produce a smaller endpoint tangent mismatch than source-relevant alternative spiral families?

The comparison used the signed statistic

\[
D_{C,k}
=
\Delta_{C,k}
-
\Delta_{R,k}.
\]

Thus:

\[
D_{C,k}>0
\]

means the reciprocal spiral has the smaller S1 mismatch,

while

\[
D_{C,k}<0
\]

means the comparator has the smaller S1 mismatch.

---

## 3. Registered comparator set

The preregistered named comparators were:

1. endpoint-matched Archimedean spiral;
2. endpoint-matched logarithmic spiral;
3. Golden Mean logarithmic spiral.

The checkpoint also included a frozen logarithmic sensitivity grid with multipliers

\[
m\in
\left\{
0.50,\,
0.75,\,
1.00,\,
1.25,\,
1.50,\,
2.00
\right\},
\]

applied to the preregistered endpoint-matched logarithmic rate

\[
b_*=
\frac{\ln(1+3\pi)}{3\pi}.
\]

The spherical scales remained exactly:

\[
k_{\rm G30}
=
\tan(\pi/6),
\]

and

\[
k_{\rm GHALF}
=
\tan(1/2).
\]

No additional scale was tested.

---

## 4. Primary checkpoint result

The registered primary summary is

`RECIPROCAL_NOT_STRICTLY_BEST_ALL_PRIMARY_CELLS`.

The strict primary comparative hypothesis therefore fails.

The reason is specific and reproducible:

> The endpoint-matched Archimedean comparator produces a smaller directed S1 mismatch than the reciprocal spiral at both registered spherical scales.

This prevents any conclusion that the reciprocal spiral is uniquely or universally superior under the registered Variant-A S1 criterion.

---

## 5. Primary named-comparator results

The six preregistered primary cells returned:

| Comparator | Scale | \(\Delta_{\rm S1}\) (deg) | Reciprocal (deg) | \(D\) (deg) | Comparison |
|---|---|---:|---:|---:|---|
| Archimedean endpoint-matched | G30 | 139.792738398922 | 144.577622108907 | -4.784883709985 | comparator better |
| Archimedean endpoint-matched | GHALF | 139.851231807260 | 144.202263172274 | -4.351031365014 | comparator better |
| Logarithmic endpoint-matched | G30 | 178.208966337804 | 144.577622108907 | +33.631344228897 | reciprocal better |
| Logarithmic endpoint-matched | GHALF | 178.364125086432 | 144.202263172274 | +34.161861914158 | reciprocal better |
| Golden Mean | G30 | 177.834515573404 | 144.577622108907 | +33.256893464497 | reciprocal better |
| Golden Mean | GHALF | 178.022998071395 | 144.202263172274 | +33.820734899121 | reciprocal better |

The comparison is therefore not a general loss or a general win for the reciprocal spiral.

It separates into two distinct findings:

- Archimedean performs modestly better than reciprocal;
- logarithmic and Golden Mean spirals perform substantially worse than reciprocal.

---

## 6. Archimedean result

The endpoint-matched Archimedean comparator gives:

### G30

\[
\Delta_{A,\mathrm{G30}}
=
139.792738398922^\circ,
\]

compared with the reciprocal value

\[
144.577622108907^\circ.
\]

Hence

\[
D_{A,\mathrm{G30}}
=
-4.784883709985^\circ.
\]

### GHALF

\[
\Delta_{A,\mathrm{GHALF}}
=
139.851231807260^\circ,
\]

compared with

\[
144.202263172274^\circ.
\]

Hence

\[
D_{A,\mathrm{GHALF}}
=
-4.351031365014^\circ.
\]

The Archimedean spiral therefore has the smaller S1 mismatch at both registered scales.

### 6.1 Why this is a particularly clean comparison

The endpoint-matched Archimedean comparator was constructed to share with the reciprocal DIAGRAM branch:

- the same angular phase;
- the same \(3\pi\) angular span;
- the same outer radius;
- the same inner radius;
- the same spherical scale;
- the same spherical outer endpoint;
- the same spherical inner endpoint.

Therefore the minimal great-circle transport path between the endpoint positions is also the same.

The difference in S1 is consequently not caused by different endpoint placement.

It arises from the tangent geometry generated by the different radial law.

This makes the Archimedean comparison especially informative within the registered S1 proxy.

### 6.2 Interpretation

The reciprocal spiral is not uniquely preferred by the registered endpoint-tangent criterion.

The Archimedean advantage is modest rather than dramatic:

\[
4.35^\circ
\text{ to }
4.78^\circ.
\]

However, it is consistent across both registered spherical scales.

That consistency is sufficient to reject the preregistered hypothesis of strict reciprocal superiority across all named primary comparator cells.

---

## 7. Endpoint-matched logarithmic result

The endpoint-matched logarithmic comparator gives:

### G30

\[
\Delta_{LM,\mathrm{G30}}
=
178.208966337804^\circ,
\]

so

\[
D_{LM,\mathrm{G30}}
=
+33.631344228897^\circ.
\]

### GHALF

\[
\Delta_{LM,\mathrm{GHALF}}
=
178.364125086432^\circ,
\]

so

\[
D_{LM,\mathrm{GHALF}}
=
+34.161861914158^\circ.
\]

The reciprocal therefore produces a substantially smaller S1 mismatch than the endpoint-matched logarithmic spiral at both registered scales.

The logarithmic mismatch is close to the theoretical directed maximum

\[
180^\circ.
\]

Its tangent dot products are correspondingly close to

\[
-1,
\]

and its vector residuals are correspondingly close to the maximum

\[
R_{\rm S1}=2.
\]

Thus the endpoint-matched logarithmic comparator is almost anti-parallel under the registered endpoint-tangent comparison.

---

## 8. Golden Mean result

The Golden Mean logarithmic spiral gives:

### G30

\[
\Delta_{G,\mathrm{G30}}
=
177.834515573404^\circ,
\]

so

\[
D_{G,\mathrm{G30}}
=
+33.256893464497^\circ.
\]

### GHALF

\[
\Delta_{G,\mathrm{GHALF}}
=
178.022998071395^\circ,
\]

so

\[
D_{G,\mathrm{GHALF}}
=
+33.820734899121^\circ.
\]

The reciprocal therefore also produces a substantially smaller S1 mismatch than the Golden Mean spiral at both registered scales.

As with the endpoint-matched logarithmic comparator, the Golden Mean endpoint tangents are almost maximally anti-aligned after intrinsic transport.

---

## 9. Golden Mean / logarithmic-family consistency check

The Golden Mean growth rate is

\[
b_\phi
=
\frac{2\ln\phi}{\pi}
\approx
0.306348962530033.
\]

The nearby preregistered logarithmic-grid value at multiplier

\[
m=1.25
\]

is

\[
b
\approx
0.310907254060594.
\]

Their S1 values are correspondingly close.

At G30:

\[
177.834515573404^\circ
\]

for Golden Mean versus

\[
177.806568720812^\circ
\]

for the \(m=1.25\) grid point.

The difference is approximately

\[
0.027947^\circ.
\]

At GHALF:

\[
178.022998071395^\circ
\]

for Golden Mean versus

\[
177.997547418842^\circ
\]

for the \(m=1.25\) grid point.

The difference is approximately

\[
0.025451^\circ.
\]

This smooth agreement is consistent with the Golden Mean spiral being a specific member of the logarithmic family and provides an internal numerical sanity check on the comparator implementation.

---

## 10. Logarithmic sensitivity-grid result

All twelve preregistered logarithmic sensitivity cells have larger S1 mismatch than the reciprocal reference at the corresponding scale.

The registered grid summaries are therefore:

### G30

`RECIPROCAL_BEATS_ALL_REGISTERED_LOG_GRID_POINTS`

### GHALF

`RECIPROCAL_BEATS_ALL_REGISTERED_LOG_GRID_POINTS`

This result is robust across the entire preregistered finite grid.

However, it must not be generalized to the complete continuous logarithmic family.

---

## 11. Boundary trend in the logarithmic grid

The logarithmic grid exhibits a clear directional trend.

For G30, as the multiplier increases from

\[
m=0.50
\]

to

\[
m=2.00,
\]

the mismatch decreases from approximately

\[
179.167659^\circ
\]

to

\[
176.858854^\circ.
\]

For GHALF, it decreases from approximately

\[
179.237821^\circ
\]

to

\[
177.136075^\circ.
\]

Thus the smallest logarithmic mismatch in the registered grid occurs at the upper boundary

\[
m=2.00.
\]

This is methodologically important.

The preregistration explicitly prohibited extending the range after seeing the results.

Accordingly:

> The present checkpoint establishes reciprocal superiority only over the preregistered finite logarithmic grid, not over all possible logarithmic growth rates.

The monotonic movement toward the grid boundary may motivate a later preregistered range extension.

It does not authorize one inside the completed checkpoint.

---

## 12. Scale sensitivity

The overall comparator ordering is unchanged between G30 and GHALF.

At both scales:

- Archimedean is better than reciprocal;
- reciprocal is better than endpoint-matched logarithmic;
- reciprocal is better than Golden Mean;
- reciprocal beats every fixed logarithmic-grid point.

The narrow G30/GHALF scale ambiguity therefore does not alter the qualitative comparator result.

This remains a limited statement because the two scales differ only modestly.

The untested one-radian-scale interpretation remains outside this checkpoint.

---

## 13. What the comparator checkpoint establishes

Within the finite AOG-DIAGRAM Variant-A S1 construction:

1. the reciprocal spiral is **not** strictly best across all named source-relevant comparators;
2. the endpoint-matched Archimedean spiral produces a smaller directed endpoint tangent mismatch at both registered scales;
3. the reciprocal spiral produces a substantially smaller mismatch than the endpoint-matched logarithmic spiral;
4. the reciprocal spiral produces a substantially smaller mismatch than the Golden Mean spiral;
5. the reciprocal spiral produces a smaller mismatch than every logarithmic growth-rate point in the preregistered finite sensitivity grid;
6. the qualitative ordering is unchanged between G30 and GHALF.

This is the complete registered comparator finding.

---

## 14. What the comparator checkpoint does not establish

This checkpoint does not establish that the Archimedean spiral is globally superior to the reciprocal spiral.

It does not establish that the reciprocal spiral is globally superior to logarithmic spirals.

It does not establish that every logarithmic growth rate performs worse than reciprocal.

It does not establish literal recursive self-embedment.

It does not establish a unique historically intended spiral.

It does not establish the full three-copy First Hand construction.

It does not establish Hebrew-letter generation.

It does not establish or refute Variant B.

It does not establish or refute the dimpled-sphere torus.

It does not test a similarity-map nesting condition.

It does not test S1.5 or S2.

---

## 15. Relation to the source's comparative claim

The source presents the reciprocal spiral as possessing properties that ordinary logarithmic / Golden Mean alternatives do not.

The present Variant-A S1 proxy gives a mixed result.

### Supported within this narrow proxy

The reciprocal spiral is strongly distinguished from the registered logarithmic and Golden Mean comparators.

The difference is large:

\[
\approx33^\circ
\text{ to }
34^\circ.
\]

This is not a marginal ordering.

### Not supported within this narrow proxy

The reciprocal spiral is not uniquely superior among the tested comparator families.

The endpoint-matched Archimedean spiral performs modestly better at both scales.

Therefore the strongest preregistered claim,

> reciprocal strictly best across all named primary comparator cells,

is not reproduced.

The correct conclusion is consequently neither a blanket confirmation nor a blanket rejection of the source's comparative intuition.

The S1 proxy discriminates reciprocal strongly from the logarithmic / Golden family, but does not confer unique superiority because the Archimedean comparator performs better.

---

## 16. Variant-A / Variant-B firewall

This checkpoint concerns Variant A only.

Variant B, the dimpled-sphere torus, remains outside the executed comparator analysis.

The distinction is especially important because S1 is evaluated using endpoint tangents at the inner end of the curve.

That is precisely the region in which the dimpled-sphere geometry differs from the undimpled Variant-A sphere.

Therefore a claim that the two surfaces agree over most of the vortex is not sufficient to transfer the present endpoint-tangent ordering to Variant B.

Accordingly:

> No Archimedean, reciprocal, logarithmic, or Golden-Mean ordering established here may be assumed to hold on the dimpled-sphere torus.

Variant B requires its own explicit geometry and preregistered test.

---

## 17. AOG-PROSE comparison remains structurally unresolved

The primary comparator checkpoint deliberately used only AOG-DIAGRAM.

The AOG-PROSE reciprocal branch has

\[
r\to\infty
\]

at a finite angular endpoint.

Standard Archimedean and logarithmic spirals do not share that finite-angle radial-infinity structure.

The audit therefore did not manufacture an arbitrary finite cutoff or otherwise force them into a nominally equivalent prose branch.

That decision remains correct after observing the comparator results.

No post-hoc AOG-PROSE comparator is introduced in this closeout.

---

## 18. Methodological significance

The comparator checkpoint was completed without post-hoc model tuning.

The audit did not:

- optimize an Archimedean pitch;
- optimize a logarithmic growth rate;
- move a logarithmic grid boundary after observing the trend;
- add a new grid point;
- interpolate toward a more favorable logarithmic result;
- alter the Golden Mean definition;
- rerun the reciprocal reference;
- change the endpoint radii;
- change the \(3\pi\) angular span;
- change the angular phase;
- optimize the spherical scale;
- use the excluded one-radian scale;
- introduce an AOG-PROSE cutoff;
- use \(|d|\);
- change tangent orientation;
- introduce image-space fitting;
- transfer the result to Variant B.

The mixed result was accepted exactly as returned by the preregistered matrix.

This is a central methodological success of the checkpoint.

---

## 19. Closed comparator conclusion

The First Hand S1 comparator checkpoint is closed with:

`RECIPROCAL_NOT_STRICTLY_BEST_ALL_PRIMARY_CELLS`.

The endpoint-matched Archimedean spiral beats the reciprocal by approximately

\[
4.35^\circ
\text{ to }
4.78^\circ.
\]

The reciprocal beats the endpoint-matched logarithmic spiral by approximately

\[
33.63^\circ
\text{ to }
34.16^\circ.
\]

The reciprocal beats the Golden Mean spiral by approximately

\[
33.26^\circ
\text{ to }
33.82^\circ.
\]

The reciprocal also beats all twelve preregistered finite logarithmic-grid cells.

However, the logarithmic grid improves toward its upper registered boundary, so no inference is made about the continuous logarithmic family outside the frozen range.

The registered comparator result is therefore:

> **Within the finite Variant-A S1 endpoint-tangent proxy, the reciprocal spiral is strongly differentiated from logarithmic and Golden-Mean spirals, but it is not uniquely superior because the endpoint-matched Archimedean spiral performs modestly better at both registered scales.**

No stronger conclusion is drawn.

---

## 20. Next-stage boundary

This closeout does not itself select or execute the next test.

Several later questions remain methodologically distinct:

- whether the logarithmic sensitivity range should be extended under a new preregistration;
- whether the unresolved one-radian spherical-scale interpretation materially changes the ordering;
- whether S1.5 supplies a meaningful local-frame diagnostic;
- whether a similarity-map formulation can test recursive "seed inside fruit" self-embedment more directly;
- whether other members of the source-compatible central-projective family alter the result;
- whether Variant B reproduces or changes the Variant-A endpoint-tangent ordering.

Any such extension requires a separate preregistration before execution.

No later test may retroactively alter the completed S1 comparator result.

---

## 21. Phase status

The analytic workflow now stands at:

\[
\text{reciprocal S1 preregistration}
\]

\[
\downarrow
\]

\[
\text{reciprocal S1 implementation freeze}
\]

\[
\downarrow
\]

\[
\text{reciprocal S1 execution}
\]

\[
\downarrow
\]

\[
\text{reciprocal S1 closeout}
\]

\[
\downarrow
\]

\[
\text{comparator preregistration}
\]

\[
\downarrow
\]

\[
\text{comparator implementation freeze}
\]

\[
\downarrow
\]

\[
\text{registered comparator execution}
\]

\[
\downarrow
\]

\[
\boxed{\text{comparator analytic closeout}}
\]

The comparator ordering is now a fixed v0.8 audit finding and a boundary condition for later work, not a result to be optimized away.
