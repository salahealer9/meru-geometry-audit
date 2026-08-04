# First Hand S1 Comparator Preregistration

**Checkpoint:** `first_hand_s1_comparator_preregistration_v0.8`  
**Status:** PREREGISTERED — COMPARATORS NOT RUN  
**Phase:** analytic self-embedment audit  
**Prerequisite S1 checkpoint:** `first_hand_analytic_s1_preregistration_v0.8`  
**Prerequisite S1 closeout:** `first_hand_s1_analytic_closeout_v0.8`  
**Variant:** A — cube-octahedral / canonical inverse-gnomonic sphere only  
**Image pixel data:** prohibited

## 1. Purpose

This checkpoint preregisters the first comparative extension of the completed First Hand S1 analysis.

The completed reciprocal-spiral S1 checkpoint found no exact directed endpoint tangent compatibility in any of its four registered branches. That result is frozen and is not rerun or altered here.

The present checkpoint asks a narrower comparative question:

> Under the same Variant-A spherical map and the same intrinsic directed tangent statistic, does the reciprocal spiral produce a smaller endpoint tangent mismatch than source-relevant alternative spiral families?

This checkpoint tests comparative S1 behaviour only.

It does not test literal recursive self-embedment.

It does not test the dimpled-sphere torus.

It does not test S1.5, S2, three-copy Hand geometry, Hebrew-letter projections, or any alternative spherical map.

---

## 2. Source-led comparator set

The comparator set is fixed before execution from source material in which Stan Tenen contrasts the reciprocal / hyperbolic spiral with more regular alternatives.

The registered comparator set is:

1. Archimedean spiral;
2. logarithmic spiral;
3. Golden Mean spiral.

The Golden Mean spiral is mathematically a special case of the logarithmic family, but it is retained separately because it is explicitly named and discussed by the source.

No additional comparator may be introduced after results are inspected.

The Fibonacci / Golden Mean pseudo-spiral is excluded from this checkpoint because it is not a unique smooth algebraic spiral and its piecewise construction can make a tangent comparison construction-dependent.

---

## 3. Frozen spherical map

The spherical construction remains exactly the Variant-A isotropic inverse-gnomonic map used for the completed S1 checkpoint:

\[
M_k(x,y)
=
\frac{(kx,ky,1)}
{\sqrt{k^2x^2+k^2y^2+1}},
\qquad
k>0.
\]

For a planar polar curve with radius \(r(u)\) and absolute polar angle

\[
\theta(u)=\theta_0+u,
\]

the spherical curve is

\[
\Gamma_{k,r}(u)
=
\frac{
\left(
k r(u)\cos(\theta_0+u),
k r(u)\sin(\theta_0+u),
1
\right)
}{
\sqrt{1+k^2r(u)^2}
}.
\]

No general projective matrix is fitted.

No image-derived scale is used.

No alternative projection is introduced.

---

## 4. Why the primary comparator test uses AOG-DIAGRAM

The reciprocal S1 checkpoint retained two source-supported truncation conventions:

### AOG-PROSE

\[
\theta_{\rm outer}\to0^+,
\qquad
r_{\rm outer}\to\infty,
\qquad
\theta_{\rm inner}=3\pi.
\]

### AOG-DIAGRAM

\[
\theta_{\rm outer}=1,
\qquad
\theta_{\rm inner}=1+3\pi,
\]

with finite reciprocal radii

\[
r_{\rm outer}=1,
\qquad
r_{\rm inner}=\frac{1}{1+3\pi}.
\]

A standard Archimedean or logarithmic spiral with finite parameters cannot begin at radial infinity and arrive at a finite inner radius after only a finite \(3\pi\) change in its polar angle while remaining an ordinary member of that spiral family.

Therefore the AOG-PROSE reciprocal endpoint structure has no direct standard-family comparator under the same finite angular span.

This structural mismatch must not be silently repaired by:

- introducing an arbitrary finite outer cutoff;
- changing the angular span;
- reparameterising a logarithmic or Archimedean curve so that it acquires a reciprocal-type pole;
- moving the reciprocal prose endpoint away from infinity;
- selecting a finite radius from the page-7 drawing.

Accordingly:

> **The primary comparator matrix is restricted to the finite AOG-DIAGRAM branch.**

The completed AOG-PROSE reciprocal results remain valid S1 findings, but no direct comparator inference is made against them in this checkpoint.

This is a structural non-comparability, not missing data.

---

## 5. Frozen finite comparison domain

Define

\[
L=3\pi.
\]

For the AOG-DIAGRAM comparison, use the branch-local parameter

\[
u=\theta-1,
\qquad
0\leq u\leq L.
\]

Thus

\[
\theta(u)=1+u.
\]

The outer endpoint is

\[
u_{\rm outer}=0,
\]

and the inner endpoint is

\[
u_{\rm inner}=L.
\]

All registered comparator curves therefore span exactly

\[
L=3\pi=540^\circ=1.5\ {\rm turns}.
\]

The directed comparison orientation remains

\[
\text{inner}\longrightarrow\text{outer},
\]

which corresponds to decreasing \(u\).

The reciprocal DIAGRAM reference curve is

\[
r_R(u)=\frac{1}{1+u}.
\]

Its endpoint radii are

\[
r_R(0)=1
\]

and

\[
r_R(L)=q_R
=
\frac{1}{1+L}
=
\frac{1}{1+3\pi}.
\]

The value \(q_R\) is used only as a preregistered geometric normalization target.

It is not fitted from S1 results.

---

## 6. Primary comparator A: endpoint-matched Archimedean spiral

The registered Archimedean comparator is the unique affine-radius spiral that matches the reciprocal DIAGRAM outer and inner radii over the same \(3\pi\) span:

\[
r_A(u)
=
1
-
\frac{1-q_R}{L}\,u.
\]

Therefore

\[
r_A(0)=1
\]

and

\[
r_A(L)=q_R.
\]

This is an ordinary Archimedean spiral written in the inward radial orientation required by the registered outer-to-inner parameter convention.

No pitch parameter is fitted.

The pitch is fixed entirely by the two preregistered endpoint-radius conditions.

---

## 7. Primary comparator B: endpoint-matched logarithmic spiral

The registered endpoint-matched logarithmic comparator is

\[
r_{LM}(u)
=
e^{-b_*u},
\]

where

\[
b_*
=
\frac{\ln(1/q_R)}{L}
=
\frac{\ln(1+3\pi)}{3\pi}.
\]

Hence

\[
r_{LM}(0)=1
\]

and

\[
r_{LM}(L)=q_R.
\]

Numerically,

\[
b_*
\approx
0.248725803248475.
\]

This comparator matches the reciprocal DIAGRAM angular span and both endpoint radii while differing in radial law.

No logarithmic growth parameter is fitted to S1.

---

## 8. Primary comparator C: Golden Mean spiral

Let

\[
\phi
=
\frac{1+\sqrt5}{2}.
\]

The standard Golden Mean logarithmic spiral is registered using the convention that its radius changes by a factor \(\phi\) every quarter-turn.

Its inward-oriented rate is therefore

\[
b_\phi
=
\frac{2\ln\phi}{\pi}.
\]

The registered curve is

\[
r_G(u)
=
e^{-b_\phi u}.
\]

Thus

\[
r_G(0)=1,
\]

and, because \(L=3\pi\) contains six quarter-turns,

\[
r_G(L)=\phi^{-6}.
\]

Numerically,

\[
b_\phi
\approx
0.306348962530033.
\]

Unlike the endpoint-matched Archimedean and logarithmic comparators, the Golden Mean comparator is not forced to share the reciprocal inner radius.

Its defining growth law is preserved exactly because the Golden Mean spiral is a specifically named source comparator.

No Golden Mean parameter is fitted.

---

## 9. Preregistered logarithmic-family sensitivity range

A single endpoint-matched logarithmic spiral does not characterize the entire logarithmic family.

To prevent post-hoc tuning of the logarithmic growth rate, a finite sensitivity grid is frozen before execution.

Define

\[
b_m = m\,b_*,
\]

with the preregistered multiplier set

\[
m\in
\left\{
0.50,\,
0.75,\,
1.00,\,
1.25,\,
1.50,\,
2.00
\right\}.
\]

For each multiplier,

\[
r_{L,m}(u)
=
e^{-b_m u}.
\]

The interval therefore spans

\[
0.5b_*
\leq
b
\leq
2b_*.
\]

Numerically this is approximately

\[
0.1243629016
\leq
b
\leq
0.4974516065.
\]

This range is anchored to the reciprocal DIAGRAM endpoint contraction before comparator execution.

It is not selected from observed S1 outcomes.

The exact Golden Mean value \(b_\phi\) is evaluated separately even though it lies inside this broader range.

No interpolation, continuous minimisation, root finding, optimizer, or adaptive refinement in \(b\) is permitted.

The smallest mismatch among the fixed logarithmic grid points may be reported descriptively as the best **registered-grid** logarithmic result, but it must not be described as the mathematical optimum of the continuous logarithmic family.

---

## 10. Frozen spherical scales

The comparator checkpoint uses exactly the two scales already registered for S1:

\[
\mathrm{G30}:
\qquad
k=\tan(\pi/6),
\]

and

\[
\mathrm{GHALF}:
\qquad
k=\tan(1/2).
\]

No GUNIT branch is run.

No GONE / one-radian branch is run.

No continuously varying \(k\) is run.

The broader scale ambiguity remains reserved for a separate sensitivity checkpoint.

This separation prevents simultaneous expansion of both the curve-family dimension and the spherical-scale dimension.

---

## 11. Directed endpoint tangent calculation

For every comparator curve,

\[
\Gamma_{k,r}(u)
=
\frac{
\left(
k r(u)\cos(1+u),
k r(u)\sin(1+u),
1
\right)
}{
\sqrt{1+k^2r(u)^2}
}.
\]

The directed inner-to-outer tangent is

\[
\tau(u)
=
-
\frac{\Gamma_{k,r}'(u)}
{\|\Gamma_{k,r}'(u)\|}.
\]

The minus sign is mandatory because inner-to-outer motion corresponds to decreasing \(u\).

No absolute tangent direction is used.

No sign may be flipped after inspecting a result.

---

## 12. Intrinsic transport

The tangent comparison is exactly the same intrinsic construction used in the completed reciprocal S1 checkpoint.

Let

\[
p_o=\Gamma_{k,r}(0)
\]

and

\[
p_i=\Gamma_{k,r}(L).
\]

The directed outer tangent is parallel-transported from \(p_o\) to \(p_i\) along the unique shorter great-circle geodesic.

Let

\[
\widetilde{\tau}_o
\]

denote the transported outer tangent.

The same coincident-endpoint and antipodal-endpoint rules from the frozen S1 evaluator apply unchanged.

No new transport convention is introduced.

---

## 13. Comparator S1 statistic

For every registered comparator cell,

\[
d
=
\widetilde{\tau}_o\cdot\tau_i,
\]

\[
c
=
\left\|
\widetilde{\tau}_o\times\tau_i
\right\|,
\]

and

\[
\Delta_{\rm S1}
=
\operatorname{atan2}(c,d).
\]

The equivalent residual is

\[
R_{\rm S1}
=
\left\|
\widetilde{\tau}_o-\tau_i
\right\|.
\]

The absolute value

\[
|d|
\]

remains prohibited.

Anti-parallel tangents must remain a large directed mismatch.

The compatibility tolerance remains

\[
10^{-10}\ {\rm rad}
\]

for mathematical zero only.

---

## 14. Frozen reciprocal reference

The reciprocal comparator baseline is not recomputed.

The comparator analysis must read or otherwise use the already frozen AOG-DIAGRAM S1 results:

### G30

\[
\Delta_{R,\mathrm{G30}}
=
2.5233555305045834\ {\rm rad}
\]

\[
=
144.5776221089075^\circ.
\]

### GHALF

\[
\Delta_{R,\mathrm{GHALF}}
=
2.5168042811835494\ {\rm rad}
\]

\[
=
144.2022631722743^\circ.
\]

These values are immutable inputs from the completed S1 checkpoint.

The reciprocal branch must not be rerun, refitted, or regenerated as part of comparator execution.

---

## 15. Primary comparative statistic

For comparator \(C\) and spherical scale \(k\), define

\[
D_{C,k}
=
\Delta_{C,k}
-
\Delta_{R,k}.
\]

Interpretation:

\[
D_{C,k}>0
\]

means the reciprocal spiral has the smaller directed S1 mismatch.

\[
D_{C,k}=0
\]

means the two registered constructions tie numerically.

\[
D_{C,k}<0
\]

means the comparator has the smaller directed S1 mismatch.

The magnitude of \(D_{C,k}\) must be reported in radians and degrees.

No absolute value of \(D_{C,k}\) is used.

---

## 16. Primary comparison matrix

The primary named-comparator matrix contains six cells:

| Comparator | G30 | GHALF |
|---|---|---|
| endpoint-matched Archimedean | registered | registered |
| endpoint-matched logarithmic | registered | registered |
| Golden Mean | registered | registered |

The logarithmic sensitivity grid adds twelve secondary cells:

\[
6\ \text{fixed }b\text{ values}
\times
2\ \text{spherical scales}.
\]

No AOG-PROSE comparator cells are generated.

---

## 17. Registered comparative states

For each named comparator cell:

`RECIPROCAL_SMALLER_MISMATCH`

`COMPARATOR_SMALLER_MISMATCH`

`EQUAL_WITHIN_NUMERICAL_PRECISION`

`COMPARATOR_TRANSPORT_UNDEFINED_ANTIPODAL`

`COMPARATOR_TECHNICAL_FAILURE`

For each scale, the named-comparator summary may use:

`RECIPROCAL_STRICTLY_BEST_NAMED_COMPARATORS`

`RECIPROCAL_NOT_STRICTLY_BEST_NAMED_COMPARATORS`

`NAMED_COMPARATOR_COMPARISON_INCOMPLETE`

Across both scales, the primary checkpoint summary may use:

`RECIPROCAL_STRICTLY_BEST_ALL_PRIMARY_CELLS`

`RECIPROCAL_NOT_STRICTLY_BEST_ALL_PRIMARY_CELLS`

`PRIMARY_COMPARISON_INCOMPLETE`

For the fixed logarithmic sensitivity grid:

`RECIPROCAL_BEATS_ALL_REGISTERED_LOG_GRID_POINTS`

`REGISTERED_LOG_GRID_CONTAINS_EQUAL_OR_BETTER_POINT`

`LOG_GRID_COMPARISON_INCOMPLETE`

These labels describe only the registered Variant-A S1 proxy.

They are not global statements about spiral self-embedment.

---

## 18. Primary hypothesis and decision rule

The preregistered primary comparative hypothesis is:

> On the finite AOG-DIAGRAM Variant-A construction, the reciprocal spiral has a smaller directed S1 endpoint tangent mismatch than each of the three named source-relevant comparator constructions at both registered spherical scales.

Operationally, the primary hypothesis is satisfied only if

\[
D_{C,k}>0
\]

for every cell in the six-cell primary matrix.

There is no tolerance-based declaration of practical superiority.

A numerical tie does not count as reciprocal superiority.

Failure of one cell is sufficient for

`RECIPROCAL_NOT_STRICTLY_BEST_ALL_PRIMARY_CELLS`.

This deterministic decision rule is fixed before comparator execution.

---

## 19. Secondary logarithmic-family question

The secondary question is:

> Does any point in the fixed preregistered logarithmic growth-rate grid equal or outperform the reciprocal S1 mismatch at the same spherical scale?

For each scale, compare every registered

\[
\Delta_{L,m,k}
\]

with the frozen reciprocal

\[
\Delta_{R,k}.
\]

No continuous optimum is inferred.

No additional \(b\) values may be added after seeing the grid results.

If a grid endpoint appears to improve monotonically toward the edge of the registered range, that observation may motivate a later preregistration, but the present range must not be extended during this checkpoint.

---

## 20. Required outputs

Each comparator result must record:

- comparator identifier;
- comparator family;
- exact radial equation;
- normalization rule;
- growth parameter where applicable;
- \(u_{\rm outer}\);
- \(u_{\rm inner}\);
- absolute angular phase \(\theta_0=1\);
- spherical scale identifier;
- \(k\);
- outer and inner planar radii;
- spherical endpoint positions;
- directed endpoint tangents;
- transport axis and angle where applicable;
- transported outer tangent;
- \(d\);
- \(c\);
- \(\Delta_{\rm S1}\) in radians and degrees;
- \(R_{\rm S1}\);
- frozen reciprocal reference mismatch;
- \(D_{C,k}\) in radians and degrees;
- registered comparison state;
- confirmation that image pixel data were not used.

The output must distinguish the six primary named-comparator cells from the twelve secondary logarithmic-grid cells.

---

## 21. Prohibited operations

No comparator result may be previewed before this preregistration is committed and frozen.

No comparator growth rate may be optimized against S1.

No Archimedean pitch may be optimized.

No Golden Mean rate may be modified.

No logarithmic grid point may be added, removed, or moved after execution begins.

No continuous minimization over \(b\) is permitted.

No interpolation between logarithmic grid values may be used to claim a better comparator.

No radial normalization may be changed after results are observed.

No reciprocal result may be rerun or replaced.

No endpoint may be moved.

No angular span may be changed from \(3\pi\).

No phase may be optimized.

No tangent sign may be changed.

No \(|d|\) transformation is permitted.

No spherical scale may be optimized.

No GUNIT or GONE scale is run.

No AOG-PROSE comparator proxy is invented.

No dimpled-sphere or toroidal construction is run.

No S1.5 or S2 test is run.

No alternative projective map is run.

No page-7 pixel data are used.

No comparator may be selected or discarded because of its result.

---

## 22. Variant-A interpretation boundary

This comparator checkpoint concerns Variant A only: the canonical source-compatible spherical / cube-octahedral construction represented by the registered inverse-gnomonic map.

The result must not be transferred automatically to Variant B, the dimpled-sphere torus.

This distinction is especially important because the S1 statistic uses the inner endpoint, while the dimple modifies precisely the inner region of the surface.

Similarity of Variant A and Variant B over most of the outer vortex does not establish equivalence at the S1 measurement location.

Therefore:

> No comparator result in this checkpoint establishes the corresponding comparator ordering on the dimpled-sphere torus.

Variant B requires a separate preregistration and explicit geometric construction.

---

## 23. Source-claim interpretation boundary

The source makes broader claims about asymmetry, self-embedment, recursion, and the suitability of the reciprocal spiral.

The present deterministic comparison tests only one local proxy:

\[
\text{directed endpoint tangent mismatch after intrinsic transport}.
\]

If the reciprocal spiral has a smaller S1 mismatch than every registered comparator, that provides comparative support only for this specific Variant-A endpoint-tangent criterion.

It does not establish literal self-embedment.

It does not establish uniqueness.

It does not prove that logarithmic, Golden Mean, or Archimedean constructions fail every possible nesting criterion.

If one or more comparators equal or outperform the reciprocal spiral, then the source's claimed comparative specificity is not reproduced by this registered Variant-A S1 proxy.

That would still not by itself refute a distinct Variant-B or full recursive-nesting claim.

---

## 24. Structural meaning of the excluded PROSE comparison

The absence of AOG-PROSE comparator cells is itself a documented mathematical fact about the comparison design.

The reciprocal prose branch places radial infinity at a finite angular endpoint:

\[
\theta\to0^+,
\qquad
r\to\infty.
\]

Standard Archimedean and logarithmic spirals do not possess that same endpoint structure over a finite angular interval.

The audit therefore does not force them into artificial equivalence.

This structural distinction may be discussed after execution, but it must not be converted into an automatic advantage for either the reciprocal or comparator families.

---

## 25. Execution boundary

This document ends at preregistration.

Before it is committed and frozen:

- no Archimedean comparator may be evaluated;
- no endpoint-matched logarithmic comparator may be evaluated;
- no Golden Mean comparator may be evaluated;
- no logarithmic sensitivity-grid value may be evaluated;
- no comparator \(\Delta_{\rm S1}\), \(R_{\rm S1}\), \(d\), or \(D_{C,k}\) may be previewed.

Symbolic verification of the registered equations, endpoint normalizations, and derivative formulas is permitted provided no comparator S1 outcome is evaluated.

After this preregistration is frozen, the next checkpoint may implement the comparator evaluator without generating results.

Comparator execution must occur only after that implementation is itself committed and frozen.

---

## 26. Frozen workflow

The analytic sequence is:

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
\boxed{\text{comparator preregistration}}
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
\text{comparator execution}
\]

No downstream result may retroactively alter the registered comparator equations, growth-rate grid, normalization rules, reciprocal reference values, or interpretation boundaries.
