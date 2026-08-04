# First Hand S1 Analytic Findings and Closeout

**Checkpoint:** `first_hand_s1_analytic_closeout_v0.8`  
**Status:** CLOSED — S1 EXECUTED AND RECORDED  
**Phase:** analytic self-embedment audit  
**Prerequisite preregistration:** `first_hand_analytic_s1_preregistration_v0.8`  
**Preregistration commit:** `94ab667`  
**Implementation commit:** `ce31021`  
**Execution scope:** registered four-cell S1 matrix only  
**Image pixel data used in S1:** no

## 1. Purpose

This note closes the preregistered S1 analytic checkpoint for the First Hand construction.

It records the scientific findings of the already executed four-cell S1 matrix, verifies the internal consistency of the generated result record, and fixes the interpretation boundary before any later extension is preregistered.

No new S1 execution is performed in this closeout.

No branch is rerun.

No parameter is changed.

No comparator spiral, additional scale branch, alternative projection, S1.5 test, S2 test, toroidal construction, dimpled-sphere construction, or recursive nesting test is introduced here.

The generated execution artifacts remain the authoritative numerical record:

- `results/first_hand_s1_v0_8/s1_results.csv`
- `results/first_hand_s1_v0_8/s1_results.json`
- `results/first_hand_s1_v0_8/s1_report.md`

---

## 2. Registered question

S1 asked:

> Under the preregistered spherical construction, what is the directed intrinsic tangent mismatch between the two endpoints of the exact unitary reciprocal spiral?

The planar generator was fixed as

\[
r(\theta)=\frac{1}{\theta},
\qquad
\theta>0,
\]

with exact spherical image

\[
\Gamma_k(\theta)
=
\frac{
(k\cos\theta,\,
k\sin\theta,\,
\theta)
}{
\sqrt{k^2+\theta^2}
}.
\]

Endpoint tangents were compared intrinsically by parallel-transporting the directed outer tangent to the inner endpoint along the unique shorter great-circle geodesic.

The primary continuous statistic was

\[
\Delta_{\rm S1}
=
\operatorname{atan2}(c,d),
\]

where

\[
d
=
\widetilde{\tau}_o\cdot\tau_i
\]

and

\[
c
=
\left\|
\widetilde{\tau}_o\times\tau_i
\right\|.
\]

Exact directed compatibility was preregistered as

\[
\Delta_{\rm S1}=0,
\]

with floating-point zero tolerance

\[
\Delta_{\rm S1}\leq10^{-10}\ {\rm rad}.
\]

---

## 3. Registered branch results

The four preregistered branches returned:

| Branch | State | \(\Delta_{\rm S1}\) (rad) | \(\Delta_{\rm S1}\) (deg) | \(R_{\rm S1}\) |
|---|---|---:|---:|---:|
| `S1-PROSE-G30` | `S1_DIRECTED_NOT_COMPATIBLE` | 2.19990657980583 | 126.045362345934 | 1.78237234314068 |
| `S1-PROSE-GHALF` | `S1_DIRECTED_NOT_COMPATIBLE` | 2.17632829986781 | 124.694426417307 | 1.77155273403199 |
| `S1-DIAGRAM-G30` | `S1_DIRECTED_NOT_COMPATIBLE` | 2.52335553050458 | 144.577622108907 | 1.90520418062959 |
| `S1-DIAGRAM-GHALF` | `S1_DIRECTED_NOT_COMPATIBLE` | 2.51680428118355 | 144.202263172274 | 1.90320094791500 |

The registered cross-branch state is therefore

`S1_NO_REGISTERED_BRANCH_COMPATIBLE`.

No branch returned a technical failure.

No branch encountered antipodal transport ambiguity.

---

## 4. Primary finding

All four registered branches fail exact directed tangent compatibility.

The observed mismatch range is

\[
124.694426^\circ
\leq
\Delta_{\rm S1}
\leq
144.577622^\circ.
\]

The full range across the four registered cells is therefore approximately

\[
19.883196^\circ.
\]

These are not numerically marginal failures of the \(10^{-10}\)-radian compatibility predicate.

Every registered mismatch is greater than \(90^\circ\).

The transported outer and inner directed tangents therefore form obtuse angles in every registered branch.

Equivalently, every reported tangent dot product is negative:

\[
-0.81490
\lesssim
d
\lesssim
-0.56920.
\]

Within the preregistered S1 construction, the endpoint tangents are more opposed than perpendicular rather than approximately aligned.

This is the principal S1 result.

---

## 5. Internal numerical consistency

The generated result record is internally consistent with the preregistered definitions.

For every branch,

\[
d=\cos(\Delta_{\rm S1}),
\]

\[
c=\sin(\Delta_{\rm S1}),
\]

and

\[
R_{\rm S1}
=
2\sin\left(\frac{\Delta_{\rm S1}}{2}\right)
\]

agree with the stored values to floating-point precision.

The endpoint positions lie on \(S^2\), the endpoint tangents are unit tangent vectors, and the transported outer tangent remains unit and tangent at the inner endpoint to numerical precision.

The prose outer endpoint was handled by the registered exact analytic limit

\[
p_o=(1,0,0),
\]

rather than by an epsilon approximation.

No image-space spiral measurements entered the S1 execution.

No evidence of a technical or implementation failure is present in the recorded four-cell execution.

---

## 6. Scale sensitivity within the registered matrix

The two registered scale branches are close:

\[
k_{\rm G30}
=
\tan(\pi/6)
\approx0.577350,
\]

\[
k_{\rm GHALF}
=
\tan(0.5)
\approx0.546302.
\]

Their effect on S1 is correspondingly small.

For AOG-PROSE,

\[
\Delta_{\rm S1}({\rm G30})
-
\Delta_{\rm S1}({\rm GHALF})
\approx
1.350936^\circ.
\]

For AOG-DIAGRAM,

\[
\Delta_{\rm S1}({\rm G30})
-
\Delta_{\rm S1}({\rm GHALF})
\approx
0.375359^\circ.
\]

Thus the G30/GHALF distinction changes the registered S1 mismatch by less than approximately \(1.4^\circ\).

This does not establish broad scale robustness.

The preregistration explicitly noted that G30 and GHALF span only a narrow portion of the unresolved source-scale ambiguity.

In particular, no conclusion is drawn here about the excluded one-radian-scale branch or any continuously varying \(k\).

---

## 7. Truncation sensitivity within the registered matrix

The source-supported truncation convention has a substantially larger effect than the G30/GHALF distinction.

At G30,

\[
\Delta_{\rm S1}({\rm DIAGRAM})
-
\Delta_{\rm S1}({\rm PROSE})
\approx
18.532260^\circ.
\]

At GHALF,

\[
\Delta_{\rm S1}({\rm DIAGRAM})
-
\Delta_{\rm S1}({\rm PROSE})
\approx
19.507837^\circ.
\]

Thus, within the registered matrix,

\[
\text{narrow scale sensitivity}
\ll
\text{truncation sensitivity}.
\]

However, both truncation families remain far from exact directed compatibility.

The prose/diagram discrepancy must therefore remain visible rather than being averaged or repaired.

The audit retains both as distinct source-supported branches.

---

## 8. What S1 establishes

S1 establishes the following limited result:

> Under the four preregistered combinations of the exact reciprocal spiral, the two retained \(3\pi\) truncation conventions, and the two registered isotropic inverse-gnomonic scale conventions, the directed endpoint tangents are not intrinsically compatible after minimal-geodesic parallel transport.

The failure is substantial in all four registered cells, with directed mismatch between approximately \(124.7^\circ\) and \(144.6^\circ\).

This conclusion is fully source-led within the registered model and does not depend on fitting the page-7 hand drawing.

---

## 9. What S1 does not establish

S1 does not establish that the reciprocal spiral is globally unsuitable for the First Hand construction.

S1 does not establish that every source-compatible central-projective spherical map fails.

S1 does not establish that every possible scale convention fails.

S1 does not establish that the source historically used the registered isotropic inverse-gnomonic map.

S1 does not establish or refute literal recursive self-embedment.

S1 does not test the similarity map required to place a smaller copy of the construction inside a larger one.

S1 does not establish or refute the full three-copy First Hand geometry.

S1 does not establish or refute Hebrew-letter generation.

S1 does not establish or refute the toroidal or dimpled-sphere construction.

---

## 10. Comparative-claim boundary

The source claim of interest is not merely that the reciprocal spiral has some absolute property.

It is comparative: the reciprocal spiral is presented as succeeding where other candidate spirals do not.

No comparator spiral was included in S1.

Therefore:

> No positive or negative S1 result from this checkpoint alone supports or refutes the source's comparative reciprocal-versus-comparator claim.

A reciprocal-spiral mismatch of \(125^\circ\) to \(145^\circ\) could still be smaller than the mismatch obtained by registered comparator spirals.

Conversely, even a much smaller reciprocal mismatch would be uninformative about comparative specificity if other spiral families performed similarly.

Comparative discrimination requires its own preregistration and execution.

No comparator inference is made in this closeout.

---

## 11. Recursive-nesting boundary

The S1 transport criterion compares tangent directions intrinsically at two different points of the sphere.

That is not the same mathematical operation as recursive "seed inside fruit" nesting.

Literal self-embedment would require a specified transformation that places one copy of the relevant curve or Hand geometry inside another.

The appropriate tangent condition would then compare directions under the derivative of that embedding or similarity transformation.

Parallel transport does not supply that embedding map.

Therefore the large S1 mismatch does not by itself settle the recursive-nesting claim.

That question belongs to a later separately preregistered test.

---

## 12. Methodological significance

The main methodological value of this checkpoint is that the result was obtained without any post-hoc geometric repair.

The audit did not:

- refit the hand-drawn spiral;
- change the reciprocal law;
- move either endpoint;
- alter the \(3\pi\) span;
- optimise \(k\);
- select a favourable truncation after seeing results;
- use \(|d|\) to turn anti-parallel directions into apparent agreement;
- replace intrinsic tangent comparison with an unqualified ambient-space dot product;
- introduce a comparator after observing the reciprocal result;
- silently resolve the source's prose/diagram ambiguity.

The preregistered model was executed as frozen, and the resulting mismatch was accepted as obtained.

This preserves the audit's source-led, preregister-before-run methodology.

---

## 13. Closed S1 conclusion

The S1 checkpoint is closed with:

`S1_NO_REGISTERED_BRANCH_COMPATIBLE`.

The four registered directed tangent mismatches are:

- `S1-PROSE-G30`: \(126.045362^\circ\)
- `S1-PROSE-GHALF`: \(124.694426^\circ\)
- `S1-DIAGRAM-G30`: \(144.577622^\circ\)
- `S1-DIAGRAM-GHALF`: \(144.202263^\circ\)

The narrow registered scale distinction has little effect relative to the truncation distinction.

The source-supported prose/diagram truncation ambiguity remains materially important.

Neither ambiguity rescues exact S1 compatibility within the registered matrix.

No stronger historical, comparative, recursive, toroidal, dimpled-sphere, or Hebrew-letter claim is inferred from this result.

---

## 14. Next-stage boundary

This closeout does not select or execute the next analytic test.

Any extension must be preregistered before execution.

Potential later stages already identified by the audit include:

- broader scale sensitivity, including the unresolved one-radian-scale interpretation;
- S1.5 or another explicitly defined local frame condition;
- a similarity-map test corresponding more directly to recursive self-embedment;
- preregistered reciprocal-versus-comparator testing;
- alternative source-compatible central-projective spherical maps;
- the separately scoped toroidal/dimpled-sphere variant.

The order and precise mathematical definitions of those stages must be fixed in a subsequent preregistration.

No downstream test may retroactively modify the completed S1 result.

---

## 15. Phase status

The analytic workflow now stands at:

\[
\text{page-7 digitisation closeout}
\]

\[
\downarrow
\]

\[
\text{S1 preregistration}
\]

\[
\downarrow
\]

\[
\text{S1 implementation freeze}
\]

\[
\downarrow
\]

\[
\text{registered S1 execution}
\]

\[
\downarrow
\]

\[
\boxed{\text{S1 analytic closeout}}
\]

The S1 result is now a fixed audit finding and a boundary condition for later work, not a parameter to be optimised away.
