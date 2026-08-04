# First Hand S1 Truncation-Parity Sensitivity Preregistration

**Checkpoint:** `first_hand_s1_truncation_parity_preregistration_v0.8`  
**Status:** PREREGISTERED — NEW TRUNCATION CELLS NOT RUN  
**Phase:** analytic self-embedment audit  
**Variant:** A — cube-octahedral / canonical inverse-gnomonic sphere only  
**Primary target:** logarithmic endpoint-tangent parity under truncation  
**Existing 1.5-turn results:** immutable references; not rerun  
**Image pixel data:** prohibited

## 1. Purpose

This checkpoint preregisters a truncation-sensitivity test motivated by an exact analytic property of logarithmic spirals.

The previous comparator checkpoint found that, on the finite AOG-DIAGRAM Variant-A construction:

- the reciprocal spiral had a smaller S1 directed endpoint tangent mismatch than every preregistered logarithmic and Golden Mean comparator;
- the endpoint-matched Archimedean spiral had a smaller mismatch than the reciprocal;
- every tested curve still failed absolute directed compatibility by a large margin.

The logarithmic comparator values clustered near \(180^\circ\).

An exact planar calculation shows that this near-antiparallel behaviour is structurally linked to the source's \(3\pi\), or 1.5-turn, truncation.

The present checkpoint therefore asks:

> Does the Variant-A spherical S1 statistic preserve the analytically predicted alternation between integer-turn and odd-half-integer-turn truncations for logarithmic spirals?

This is a truncation-parity sensitivity test.

It is not a new search for a best spiral.

It is not a continuous optimization over truncation length.

It does not alter the completed 1.5-turn comparator result.

---

## 2. Analytic premise frozen before execution

Consider a logarithmic spiral written on the finite AOG-DIAGRAM parameter domain as

\[
r(u)=e^{-bu},
\qquad
b>0,
\]

with polar angle

\[
\theta(u)=\theta_0+u.
\]

Its planar Cartesian curve is

\[
\mathbf{x}(u)
=
e^{-bu}
\begin{pmatrix}
\cos(\theta_0+u)\\
\sin(\theta_0+u)
\end{pmatrix}.
\]

Differentiating gives

\[
\mathbf{x}'(u)
=
e^{-bu}
R(\theta_0+u)
\begin{pmatrix}
-b\\
1
\end{pmatrix},
\]

where \(R(\alpha)\) is the planar rotation matrix through angle \(\alpha\).

Therefore, for an angular span \(L\),

\[
\mathbf{x}'(u+L)
=
e^{-bL}
R(L)
\mathbf{x}'(u).
\]

The positive factor

\[
e^{-bL}
\]

changes magnitude only.

The endpoint tangent direction is therefore determined by \(R(L)\) and is independent of the logarithmic growth rate \(b\).

For

\[
L=n\pi,
\]

\[
R(L)=(-1)^n I.
\]

Hence:

- if \(n\) is even, the planar endpoint tangent directions are parallel;
- if \(n\) is odd, the planar endpoint tangent directions are antiparallel.

Equivalently:

- integer numbers of full turns predict planar tangent alignment;
- odd half-integer numbers of full turns predict planar tangent anti-alignment.

In particular,

\[
L=3\pi
\]

implies exact planar anti-alignment for every logarithmic growth rate.

Thus

\[
\Delta_{\log}^{\rm planar}=180^\circ
\]

at the source's 1.5-turn truncation, independently of \(b\).

This analytic result is part of the preregistration and is fixed before the new spherical sensitivity cells are executed.

---

## 3. Scientific question

The primary scientific question is not whether a logarithmic spiral can be tuned to beat the reciprocal spiral.

The primary question is:

> When the same fixed logarithmic spirals are evaluated under the same Variant-A spherical map, does changing only the truncation span produce the predicted integer-turn versus odd-half-integer-turn alternation in S1?

The secondary questions are:

1. Does the reciprocal-versus-logarithmic ranking change when the truncation parity changes?
2. Does the endpoint-matched Archimedean-versus-reciprocal ranking remain stable across the same truncation set?

These secondary questions must not replace the primary parity test.

---

## 4. Frozen truncation set

The registered truncation set is

\[
T\in
\left\{
1.0,\,
1.5,\,
2.0,\,
2.5
\right\}
\text{ turns}.
\]

Equivalently,

\[
L\in
\left\{
2\pi,\,
3\pi,\,
4\pi,\,
5\pi
\right\}.
\]

The finite AOG-DIAGRAM phase convention remains

\[
\theta_0=1.
\]

For every span,

\[
u_{\rm outer}=0,
\qquad
u_{\rm inner}=L,
\]

and

\[
\theta(u)=1+u.
\]

The directed orientation remains

\[
\text{inner}\longrightarrow\text{outer},
\]

corresponding to decreasing \(u\).

No other truncation value may be added after results are inspected.

No continuous scan in \(L\) is permitted.

---

## 5. Parity classes

The registered truncations are divided before execution into two parity classes.

### Integer-turn class

\[
\mathcal{I}
=
\left\{
2\pi,\,
4\pi
\right\}.
\]

These correspond to

\[
1.0
\quad\text{and}\quad
2.0
\]

full turns.

The exact planar logarithmic prediction is parallel endpoint tangents.

### Odd-half-integer-turn class

\[
\mathcal{H}
=
\left\{
3\pi,\,
5\pi
\right\}.
\]

These correspond to

\[
1.5
\quad\text{and}\quad
2.5
\]

full turns.

The exact planar logarithmic prediction is antiparallel endpoint tangents.

The previously executed \(3\pi\) values belong to \(\mathcal{H}\) and are immutable references.

---

## 6. Frozen Variant-A spherical map

The spherical construction remains exactly

\[
M_k(x,y)
=
\frac{(kx,ky,1)}
{\sqrt{k^2x^2+k^2y^2+1}},
\qquad
k>0.
\]

For a finite polar curve \(r(u)\),

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

No alternative projection is introduced.

No projective parameter is fitted.

---

## 7. Frozen spherical scales

The only registered spherical scales are the same two used in the completed S1 and comparator checkpoints:

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

No one-radian scale is run.

No GUNIT or GONE branch is run.

No scale optimization is permitted.

---

## 8. Fixed logarithmic family for the parity test

The logarithmic growth rates are held fixed while truncation length changes.

This is essential to isolate truncation parity from growth-rate selection.

The frozen base rate is the already preregistered 1.5-turn endpoint-matched logarithmic rate:

\[
b_*
=
\frac{\ln(1+3\pi)}{3\pi}
\approx
0.248725803248475.
\]

The fixed multiplier set remains

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
b_m=m b_*,
\]

and the curve is

\[
r_{L,m}(u)
=
e^{-b_m u}.
\]

The notation \(r_{L,m}\) indicates that the curve is truncated at the registered span \(L\); the radial law itself does not change with \(L\).

The \(b_m\) values must not be re-normalized to match a different reciprocal inner radius at each new truncation.

No new \(b\) value is introduced.

No interpolation or optimization over \(b\) is permitted.

---

## 9. Golden Mean branch

The Golden Mean logarithmic spiral remains a separately named source-relevant branch with fixed rate

\[
b_\phi
=
\frac{2\ln\phi}{\pi},
\qquad
\phi=\frac{1+\sqrt5}{2}.
\]

Thus

\[
r_G(u)
=
e^{-b_\phi u}.
\]

Its growth law remains fixed across all registered truncations.

It is included as a named logarithmic-family consistency branch.

Because the planar parity theorem is independent of \(b\), the same integer-turn / odd-half-integer-turn prediction applies to the Golden Mean branch.

---

## 10. Immutable 1.5-turn logarithmic references

The \(L=3\pi\) logarithmic and Golden Mean values have already been executed and recorded.

They must not be recomputed in this checkpoint.

The implementation must read or hard-code them as immutable reference inputs from:

`results/first_hand_s1_comparators_v0_8/s1_comparator_results.json`

The registered \(3\pi\) logarithmic-grid values are:

### G30

| Multiplier | \(\Delta_{\rm S1}\) (deg) |
|---:|---:|
| 0.50 | 179.167659486733 |
| 0.75 | 178.660992359022 |
| 1.00 | 178.208966337804 |
| 1.25 | 177.806568720812 |
| 1.50 | 177.448650628382 |
| 2.00 | 176.858854396348 |

### GHALF

| Multiplier | \(\Delta_{\rm S1}\) (deg) |
|---:|---:|
| 0.50 | 179.237820738579 |
| 0.75 | 178.776054725953 |
| 1.00 | 178.364125086432 |
| 1.25 | 177.997547418842 |
| 1.50 | 177.671776193867 |
| 2.00 | 177.136075394888 |

The registered Golden Mean \(3\pi\) references are:

\[
177.834515573404^\circ
\]

for G30, and

\[
178.022998071395^\circ
\]

for GHALF.

These values are immutable.

---

## 11. Primary new logarithmic execution matrix

For each of the six fixed logarithmic growth rates and both spherical scales, execute only the new spans

\[
L\in
\left\{
2\pi,\,
4\pi,\,
5\pi
\right\}.
\]

The \(3\pi\) cell is supplied from the frozen previous result.

Thus the new generic-logarithmic execution contains

\[
6
\times
2
\times
3
=
36
\]

new cells.

The complete parity analysis combines those 36 new cells with the 12 immutable \(3\pi\) references.

The Golden Mean branch adds

\[
1
\times
2
\times
3
=
6
\]

new cells, with its two \(3\pi\) references reused unchanged.

---

## 12. Primary spherical parity statistic

For each fixed logarithmic growth rate \(b\), scale \(k\), and truncation \(L\), compute the same directed S1 statistic used previously:

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

\[
\Delta_{\rm S1}
=
\operatorname{atan2}(c,d).
\]

The equivalent vector residual is

\[
R_{\rm S1}
=
\left\|
\widetilde{\tau}_o-\tau_i
\right\|.
\]

The outer tangent is transported to the inner endpoint along the unique shorter great-circle geodesic exactly as in the frozen S1 evaluator.

No new transport rule is introduced.

The absolute value

\[
|d|
\]

remains prohibited.

---

## 13. Primary parity prediction

For every fixed logarithmic growth rate and every registered spherical scale, the preregistered prediction is:

\[
\Delta_{\rm S1}(2\pi)
<
\Delta_{\rm S1}(3\pi),
\]

\[
\Delta_{\rm S1}(4\pi)
<
\Delta_{\rm S1}(3\pi),
\]

\[
\Delta_{\rm S1}(2\pi)
<
\Delta_{\rm S1}(5\pi),
\]

and

\[
\Delta_{\rm S1}(4\pi)
<
\Delta_{\rm S1}(5\pi).
\]

Equivalently,

\[
\max_{L\in\mathcal{I}}
\Delta_{\rm S1}(L)
<
\min_{L\in\mathcal{H}}
\Delta_{\rm S1}(L).
\]

This is the primary registered parity-separation criterion.

It is deliberately stronger than merely requiring the mean integer-turn mismatch to be smaller than the mean odd-half-turn mismatch.

---

## 14. Primary parity states

For each fixed logarithmic growth rate and scale:

`PARITY_SEPARATION_CONFIRMED`

if

\[
\max_{L\in\mathcal{I}}
\Delta_{\rm S1}(L)
<
\min_{L\in\mathcal{H}}
\Delta_{\rm S1}(L).
\]

Otherwise:

`PARITY_SEPARATION_NOT_CONFIRMED`.

If a technical or transport failure prevents evaluation:

`PARITY_COMPARISON_INCOMPLETE`.

Across all six fixed logarithmic-grid rates and both scales, the global generic-log summary may use only:

`PARITY_SEPARATION_CONFIRMED_ALL_LOG_GRID_CELLS`

`PARITY_SEPARATION_NOT_CONFIRMED_ALL_LOG_GRID_CELLS`

`PARITY_LOG_GRID_INCOMPLETE`

The Golden Mean branch receives an analogous separate summary:

`PARITY_SEPARATION_CONFIRMED_GOLDEN_MEAN`

`PARITY_SEPARATION_NOT_CONFIRMED_GOLDEN_MEAN`

`PARITY_GOLDEN_MEAN_INCOMPLETE`

---

## 15. Secondary parity contrast

For descriptive purposes, define for each fixed \(b\) and \(k\):

\[
\bar{\Delta}_{\mathcal{I}}
=
\frac{
\Delta(2\pi)+\Delta(4\pi)
}{2},
\]

and

\[
\bar{\Delta}_{\mathcal{H}}
=
\frac{
\Delta(3\pi)+\Delta(5\pi)
}{2}.
\]

Then define

\[
P_{b,k}
=
\bar{\Delta}_{\mathcal{H}}
-
\bar{\Delta}_{\mathcal{I}}.
\]

Thus

\[
P_{b,k}>0
\]

means the odd-half-turn class has the larger average mismatch.

This quantity is descriptive and secondary.

The strict max/min parity-separation criterion remains primary.

---

## 16. Secondary reciprocal truncation sensitivity

The reciprocal curve is also evaluated at the new spans

\[
2\pi,\,
4\pi,\,
5\pi,
\]

with

\[
r_R(u)=\frac{1}{1+u}.
\]

For each span,

\[
u\in[0,L].
\]

The already executed

\[
L=3\pi
\]

AOG-DIAGRAM reciprocal values remain immutable references and are not rerun.

The new reciprocal execution therefore contains

\[
3
\times
2
=
6
\]

new cells.

No parity theorem is preregistered for the reciprocal spiral.

Its truncation dependence is reported descriptively.

---

## 17. Secondary reciprocal-versus-logarithmic ordering

For each registered span \(L\), logarithmic growth rate \(b\), and scale \(k\), define

\[
D_{L,b,k}
=
\Delta_{\log}(L,b,k)
-
\Delta_R(L,k).
\]

Interpretation:

\[
D_{L,b,k}>0
\]

means reciprocal has the smaller S1 mismatch.

\[
D_{L,b,k}<0
\]

means the logarithmic comparator has the smaller mismatch.

The purpose of this secondary statistic is to determine whether the reciprocal-versus-logarithmic ordering changes with truncation parity.

No claim is preregistered that reciprocal must remain better.

In particular, a reversal at integer-turn spans is an allowed and scientifically informative result.

---

## 18. Secondary endpoint-matched Archimedean sensitivity

For each registered truncation span \(L\), define the reciprocal inner radius

\[
q_R(L)
=
\frac{1}{1+L}.
\]

The endpoint-matched Archimedean comparator at that span is

\[
r_A(u;L)
=
1
-
\frac{1-q_R(L)}{L}\,u.
\]

Therefore

\[
r_A(0;L)=1,
\]

and

\[
r_A(L;L)=q_R(L).
\]

At every span, the reciprocal and Archimedean branches therefore share:

- the same phase;
- the same angular span;
- the same outer planar radius;
- the same inner planar radius;
- the same spherical outer endpoint;
- the same spherical inner endpoint;
- the same great-circle transport path.

The Archimedean pitch is not fitted to S1.

It is fixed analytically by endpoint matching at each preregistered truncation.

The already executed \(3\pi\) Archimedean values remain immutable references.

The new Archimedean execution contains

\[
3
\times
2
=
6
\]

new cells.

---

## 19. Secondary reciprocal-versus-Archimedean statistic

For each registered span and scale, define

\[
A_{L,k}
=
\Delta_A(L,k)
-
\Delta_R(L,k).
\]

Thus

\[
A_{L,k}<0
\]

means Archimedean has the smaller mismatch.

\[
A_{L,k}>0
\]

means reciprocal has the smaller mismatch.

No direction is preregistered for the new spans.

The previous \(3\pi\) result, where Archimedean was better at both scales, remains an immutable reference rather than a hypothesis for the new cells.

---

## 20. Total new execution count

The new execution matrix contains:

### Generic logarithmic parity cells

\[
36
\]

new cells.

### Golden Mean parity cells

\[
6
\]

new cells.

### Reciprocal truncation cells

\[
6
\]

new cells.

### Endpoint-matched Archimedean truncation cells

\[
6
\]

new cells.

Total:

\[
54
\]

new cells.

All \(3\pi\) values are inherited from completed checkpoints and must not be recomputed.

---

## 21. Required outputs

Each new cell must record:

- curve identifier;
- curve family;
- truncation turns;
- truncation span \(L\);
- parity class;
- angular phase \(\theta_0=1\);
- scale identifier;
- \(k\);
- fixed growth parameter where applicable;
- logarithmic multiplier where applicable;
- outer and inner planar radii;
- spherical endpoint positions;
- directed endpoint tangents;
- transport axis and angle where applicable;
- transported outer tangent;
- \(d\);
- \(c\);
- \(\Delta_{\rm S1}\) in radians and degrees;
- \(R_{\rm S1}\);
- technical state;
- confirmation that image pixel data were not used.

The combined analysis record must distinguish:

- newly executed cells;
- inherited immutable \(3\pi\) reference cells.

The output must not make inherited values appear to have been rerun.

---

## 22. Prohibited operations

No new truncation value may be added after execution begins.

No continuous scan over truncation length is permitted.

No logarithmic \(b\) value may be added, removed, moved, or optimized.

No logarithmic rate may be re-normalized to match reciprocal endpoints at the new spans.

No Golden Mean growth law may be altered.

No reciprocal parameter may be fitted.

No Archimedean pitch may be optimized against S1.

No \(3\pi\) result may be rerun.

No previous result may be replaced.

No spherical scale may be added or optimized.

No one-radian scale may be introduced.

No endpoint may be moved.

No phase may be altered from

\[
\theta_0=1.
\]

No tangent sign may be flipped.

No \(|d|\) transformation is permitted.

No alternative transport rule is permitted.

No alternative projective map is permitted.

No AOG-PROSE comparator is introduced.

No dimpled-sphere or toroidal construction is introduced.

No new named comparator family is added.

No S1.5 or S2 analysis is run.

No page-7 image data are used.

---

## 23. Interpretation if parity separation is confirmed

If the spherical S1 results satisfy the preregistered parity-separation criterion across the fixed logarithmic family, the allowed conclusion is:

> The large logarithmic S1 mismatch observed at the source's 1.5-turn truncation is strongly controlled by truncation parity and is consistent with the exact planar endpoint-tangent alternation predicted for logarithmic spirals.

This would show that the previous logarithmic failure cannot be treated as a truncation-independent property of logarithmic spirals.

It would also show that the source's 1.5-turn choice and the comparator's endpoint-tangent behaviour are mathematically coupled.

It would not establish that the source deliberately selected 1.5 turns in order to disadvantage logarithmic spirals.

No claim about intent is permitted.

---

## 24. Interpretation if parity separation is not confirmed

If the strict spherical parity-separation criterion fails, the exact planar theorem remains true.

The allowed conclusion would instead be:

> The Variant-A projection and intrinsic transport modify the planar endpoint-tangent parity strongly enough that the preregistered spherical separation criterion is not uniformly preserved.

The planar identity must not be rejected because of a spherical failure.

The result would concern the behaviour of the spherical S1 proxy, not the correctness of the planar theorem.

---

## 25. Absolute-compatibility boundary

Every curve remains subject to the original S1 absolute compatibility criterion:

\[
\Delta_{\rm S1}=0
\]

up to the registered numerical-zero tolerance.

Relative ranking must not be confused with absolute compatibility.

A logarithmic spiral that improves dramatically at an integer-turn truncation may still fail absolute compatibility.

A reciprocal spiral that beats another family may still fail absolutely.

The report must always distinguish:

- absolute compatibility;
- parity behaviour;
- relative comparator ranking.

---

## 26. Variant-A / Variant-B firewall

This checkpoint concerns Variant A only.

Nothing in this truncation-parity analysis transfers automatically to the dimpled-sphere torus.

The S1 statistic depends on the inner endpoint geometry.

Variant B modifies precisely that region.

Therefore:

> No truncation-parity ordering established on Variant A may be assumed to hold on Variant B.

The dimpled-sphere torus requires a separate explicit construction and preregistration.

---

## 27. Relation to the source claim

The previous comparator checkpoint reproduced a source-stated relative ordering in which the reciprocal spiral had a smaller Variant-A S1 mismatch than logarithmic and Golden Mean spirals.

However, the exact planar theorem shows that the logarithmic endpoint relation at \(3\pi\) is forced to be antiparallel independently of growth rate.

The present checkpoint therefore tests whether the previously observed logarithmic disadvantage is substantially a consequence of the source truncation itself.

If integer-turn truncations dramatically reduce logarithmic S1, then the correct interpretation of the prior comparator result becomes narrower:

> The reciprocal outperformed logarithmic spirals under the source's 1.5-turn Variant-A truncation, but that ordering was obtained in a truncation regime that analytically forces logarithmic planar endpoint anti-alignment.

This does not erase the previous result.

It explains an important mechanism behind it.

---

## 28. Execution boundary

This document ends at preregistration.

Before this preregistration is committed and frozen:

- no \(2\pi\) logarithmic cell may be evaluated;
- no \(4\pi\) logarithmic cell may be evaluated;
- no \(5\pi\) logarithmic cell may be evaluated;
- no new Golden Mean truncation may be evaluated;
- no new reciprocal truncation may be evaluated;
- no new Archimedean truncation may be evaluated;
- no new \(\Delta_{\rm S1}\), \(R_{\rm S1}\), parity contrast, or relative-ranking statistic may be previewed.

Symbolic verification of the planar parity theorem and registered curve formulas is permitted provided no new spherical S1 outcome is evaluated.

After this preregistration is committed and frozen, the next checkpoint may implement the truncation-parity evaluator without generating results.

Execution must occur only after that implementation is itself committed and frozen.

---

## 29. Frozen workflow

The analytic sequence is now:

\[
\text{reciprocal S1 checkpoint}
\]

\[
\downarrow
\]

\[
\text{comparator checkpoint}
\]

\[
\downarrow
\]

\[
\text{analytic identification of logarithmic truncation parity}
\]

\[
\downarrow
\]

\[
\boxed{\text{truncation-parity preregistration}}
\]

\[
\downarrow
\]

\[
\text{truncation-parity implementation freeze}
\]

\[
\downarrow
\]

\[
\text{registered truncation-parity execution}
\]

No downstream result may retroactively alter:

- the fixed truncation set;
- the parity classes;
- the fixed logarithmic growth rates;
- the inherited \(3\pi\) references;
- the spherical scales;
- the primary parity decision rule;
- the interpretation boundaries.
