# First Hand Variant-B Throat-Width Trend Addendum

**Checkpoint:** `first_hand_variant_b_width_trend_addendum_v0.8`  
**Status:** POST-CLOSEOUT READ-ONLY ANALYTIC ADDENDUM  
**Parent checkpoint:** `first_hand_variant_b_swept_family_closeout_v0.8`  
**Data source:** frozen 400-cell Variant-B execution only  
**New geometric evaluations:** none  
**Interpolation / fitting / optimization:** none  
**Adaptive grid extension:** none

## 1. Purpose

This addendum records a preregistered read-only analysis of the already-frozen Variant-B 400-cell sweep.

The motivating source statement is that changing Dimpled-Sphere hole width changes where the vortex twists into the dimple, with wider holes producing deeper twisting.

The registered analytic question was deliberately narrower:

> At fixed spiral branch, elongation \(e\), and mapping scale \(k\), does endpoint mismatch vary monotonically across the five already-registered throat widths

\[
w=
\{0.02,0.05,0.10,0.20,0.30\}?
\]

No new carrier, endpoint, or spiral was evaluated.

---

## 2. Sequence definition

One width sequence fixes:

- spiral branch;
- elongation \(e\);
- mapping scale \(k\);

and varies only \(w\).

There are therefore

\[
8\times5\times2
=
80
\]

independent width sequences under each semantic definition.

Each sequence contains exactly five frozen mismatch values.

The classification rule was:

- `STRICTLY_INCREASING` if all four adjacent first differences are positive;
- `STRICTLY_DECREASING` if all four are negative;
- `TIED` if monotonicity holds with one or more exact zero differences;
- `NON_MONOTONE` if both positive and negative first differences occur.

---

## 3. Directed-semantics monotonicity result

Under directed ambient-vector semantics:

- `STRICTLY_INCREASING`: \(10/80\);
- `STRICTLY_DECREASING`: \(0/80\);
- `TIED`: \(0/80\);
- `NON_MONOTONE`: \(70/80\).

Thus:

\[
\boxed{70/80=87.5\%}
\]

of all directed width sequences are non-monotone.

The only fully monotone branch is:

`LOG-M050`

for which all ten \((e,k)\) sequences are strictly increasing in directed mismatch as \(w\) increases.

No other spiral family contains a monotone directed width sequence.

---

## 4. Directed within-sequence minimum locations

Across the 80 directed width sequences, the minimum occurs at:

\[
w=0.02:\ 49
\]

\[
w=0.05:\ 0
\]

\[
w=0.10:\ 2
\]

\[
w=0.20:\ 26
\]

\[
w=0.30:\ 3.
\]

The family-level pattern is:

- `GOLDEN-MEAN`: all \(10/10\) minima at \(w=0.02\);
- `LOG-M050`: all \(10/10\) minima at \(w=0.02\);
- `LOG-M075`: all \(10/10\) minima at \(w=0.02\);
- `LOG-M100`: all \(10/10\) minima at \(w=0.02\);
- `LOG-M125`: \(9/10\) at \(w=0.02\), \(1/10\) at \(w=0.30\);
- `LOG-M150`: \(8/10\) at \(w=0.20\), \(2/10\) at \(w=0.30\);
- `LOG-M200`: \(2/10\) at \(w=0.10\), \(8/10\) at \(w=0.20\);
- `RECIPROCAL`: all \(10/10\) minima at \(w=0.20\).

Thus the reciprocal branch has a particularly stable finite-grid directed optimum location:

\[
\boxed{w=0.20\text{ in all }10/10\text{ reciprocal }(e,k)\text{ sequences}}
\]

within the registered grid.

However, this is only a fixed-grid minimum.

It is not a continuous optimum and must not be called Tenen's "optimum hole."

---

## 5. Reciprocal directed width shape

Every reciprocal directed sequence follows the same qualitative pattern:

1. mismatch decreases strongly from \(w=0.02\) through \(w=0.20\);
2. mismatch then increases again at \(w=0.30\).

For example, at \(e=2.2\), GHALF:

\[
143.8061^\circ
\rightarrow
132.2371^\circ
\rightarrow
124.2602^\circ
\rightarrow
120.0111^\circ
\rightarrow
120.2800^\circ.
\]

The adjacent differences are approximately:

\[
-11.5691^\circ,\,
-7.9769^\circ,\,
-4.2490^\circ,\,
+0.2689^\circ.
\]

Thus the reciprocal family exhibits a robust U-shaped / interior-turnaround pattern over the registered width values.

The same minimum location \(w=0.20\) occurs for every registered elongation and both scales.

This is stronger than the earlier global boundary-minimum observation because it is a matched-sequence statement across the full reciprocal family.

---

## 6. Logarithmic width behavior is family-dependent

The logarithmic branches do not share a single width-response law.

Examples:

### `LOG-M050`

All ten directed sequences increase monotonically with width.

Therefore narrower registered throats are always closer to directed endpoint alignment for this branch.

### `LOG-M075`

All ten sequences are non-monotone.

They increase through most of the grid and turn downward near the widest values, while their minima remain at \(w=0.02\).

### `LOG-M100`

All ten sequences are non-monotone.

The directed mismatch rises strongly toward \(w=0.10\), then falls again toward wider throats, while the minimum remains at \(w=0.02\).

### `LOG-M150`

The minima move to the wider side:

- \(8/10\) at \(w=0.20\);
- \(2/10\) at \(w=0.30\).

### `LOG-M200`

The minima are interior to the registered width grid:

- \(2/10\) at \(w=0.10\);
- \(8/10\) at \(w=0.20\).

Thus width dependence changes qualitatively with logarithmic growth rate.

There is no single empirical rule of the form:

\[
\text{larger }w
\Rightarrow
\text{smaller directed endpoint mismatch}
\]

across the registered logarithmic family.

---

## 7. Line-semantics monotonicity result

Under unoriented tangent-line semantics:

- `STRICTLY_INCREASING`: \(0/80\);
- `STRICTLY_DECREASING`: \(10/80\);
- `TIED`: \(0/80\);
- `NON_MONOTONE`: \(70/80\).

Again:

\[
\boxed{70/80=87.5\%}
\]

of the sequences are non-monotone.

The only fully monotone branch is again `LOG-M050`, but now every one of its ten sequences is strictly decreasing.

---

## 8. Line within-sequence minimum locations

Across the 80 line-semantics width sequences, the minimum occurs at:

\[
w=0.02:\ 20
\]

\[
w=0.05:\ 30
\]

\[
w=0.10:\ 12
\]

\[
w=0.20:\ 8
\]

\[
w=0.30:\ 10.
\]

Family-level locations are:

- `GOLDEN-MEAN`: all \(10/10\) at \(w=0.05\);
- `LOG-M050`: all \(10/10\) at \(w=0.30\);
- `LOG-M075`: \(2/10\) at \(w=0.10\), \(8/10\) at \(w=0.20\);
- `LOG-M100`: all \(10/10\) at \(w=0.10\);
- `LOG-M125`: all \(10/10\) at \(w=0.05\);
- `LOG-M150`: all \(10/10\) at \(w=0.05\);
- `LOG-M200`: all \(10/10\) at \(w=0.02\);
- `RECIPROCAL`: all \(10/10\) at \(w=0.02\).

This distribution is substantially different from the directed minimum-location pattern.

---

## 9. Orientation identity across the full matrix

The frozen-matrix check gives:

\[
\tau_o\cdot\tau_i<0
\]

for all

\[
400/400
\]

registered cells.

The maximum numerical deviation from

\[
\Delta_{\rm dir}+\Delta_{\rm line}=180^\circ
\]

is only

\[
2.8421709430404\times10^{-14}\ {\rm deg}.
\]

Thus, to floating-point precision,

\[
\boxed{
\Delta_{\rm line}
=
180^\circ-\Delta_{\rm dir}
}
\]

for every cell in the registered Variant-B matrix.

Consequently the width-sequence first differences satisfy

\[
\Delta(\Delta_{\rm line})
=
-
\Delta(\Delta_{\rm dir})
\]

cell by cell.

Therefore:

- every directed increasing sequence becomes line decreasing;
- every directed decreasing sequence would become line increasing;
- every directed non-monotone sequence remains line non-monotone;
- directed and line extrema exchange maxima/minima within a fixed sequence.

This explains the exact reversal in monotonicity direction for `LOG-M050`.

---

## 10. Relation to Tenen's hole-width statement

The source statement:

> wider holes make the vortex twist deeper into the dimple

is a statement about geometric placement / depth.

The frozen Variant-B data show that this does **not** induce a simple monotonic endpoint-parallelism law.

Within the audit's carrier and mapping family:

\[
\boxed{
\text{wider hole}
\not\Rightarrow
\text{monotonically improved endpoint alignment}
}
\]

and also:

\[
\boxed{
\text{wider hole}
\not\Rightarrow
\text{monotonically worsened endpoint alignment}
}
\]

for the overwhelming majority of registered sequences.

Only one spiral family, `LOG-M050`, is monotone over the entire registered width range.

Therefore Tenen's directional depth statement must not be conflated with a directional self-embedment/parallelism statement.

---

## 11. Implication for the claimed "optimum" hole

The source explicitly refers to a Dimpled-Sphere hole that is "optimum" but does not define its metric criterion in the known passage.

The present width analysis cannot identify that historical optimum.

However, it shows that, within the registered audit family, different spiral laws favor very different finite-grid throat widths.

Examples under line semantics:

- Golden Mean: \(w=0.05\);
- `LOG-M100`: \(w=0.10\);
- `LOG-M075`: mostly \(w=0.20\);
- `LOG-M050`: \(w=0.30\);
- reciprocal: \(w=0.02\).

Under directed semantics, the reciprocal instead favors \(w=0.20\) in all ten matched sequences.

Thus the meaning of "optimum" is inseparable from:

- the spiral family;
- the endpoint semantic definition;
- the mapping rule;
- and the objective being optimized.

Until Meru's own criterion is recovered, the source phrase "optimum hole" remains underdetermined.

---

## 12. Revision to the earlier boundary-minimum interpretation

The previously sealed Variant-B closeout correctly noted that all 16 global family/semantics minima touch at least one boundary of the two-dimensional \((w,e)\) grid.

The width-sequence analysis adds a useful qualification.

For reciprocal directed mismatch:

\[
w=0.20
\]

is the within-sequence minimum in all ten fixed-\((e,k)\) width scans.

Therefore the reciprocal directed width dependence is **internally bracketed in \(w\)** within the registered five-point width grid, even though the overall two-dimensional global minimum also occurs at the elongation boundary

\[
e=2.2.
\]

Similarly, some logarithmic branches show interior width minima even though their overall two-dimensional minima touch an \(e\) boundary.

Hence the earlier statement:

> the two-dimensional grid does not demonstrate a fully interior optimum

remains correct.

But it must not be strengthened to:

> the width optimum itself lies outside the registered range.

For several families, the frozen width scan shows the opposite.

---

## 13. Strongest defensible finding

The strongest result of this read-only analysis is:

> **Endpoint mismatch is generally non-monotone in the registered Dimpled-Sphere throat-width parameter. Seventy of eighty fixed-\((\text{spiral},e,k)\) sequences are non-monotone under either semantic definition. The source statement that wider holes move the twist deeper into the dimple therefore does not translate into a universal monotonic improvement or degradation of endpoint parallelism within the audit's Variant-B reconstruction.**

A second notable finding is:

> **For the reciprocal branch under directed semantics, every one of the ten fixed-\((e,k)\) width sequences reaches its smallest registered mismatch at \(w=0.20\), followed by a slight worsening at \(w=0.30\).**

This is a stable finite-grid feature, not a recovered historical optimum.

---

## 14. What this addendum does not establish

This analysis does not:

- identify Tenen's optimum hole;
- prove a continuous optimum at \(w=0.20\);
- estimate a derivative with respect to \(w\);
- interpolate between registered widths;
- extrapolate beyond \(w=0.02\) or \(w=0.30\);
- separate carrier effects from mapping effects;
- test a new carrier;
- resolve the source's underdetermined mapping;
- establish monotonic twist depth itself.

It concerns endpoint mismatch only.

---

## 15. Closed addendum conclusion

The read-only width analysis closes with:

\[
70/80
\]

non-monotone width sequences under directed semantics and

\[
70/80
\]

under line semantics.

All 400 cells lie on the anti-parallel side:

\[
\tau_o\cdot\tau_i<0.
\]

Therefore line and directed width trends are exact complements.

The result clarifies the Variant-B source comparison:

> **Hole width is geometrically consequential in the registered reconstruction, but its effect on endpoint alignment is strongly spiral-dependent and generally non-monotone. The source's qualitative claim that wider holes push the twist deeper cannot be converted into a monotonic endpoint-parallelism law.**

The claimed Meru "optimum" hole remains a source-recovery question.

No new Variant-B numerical execution is authorized by this addendum.
