# First Hand Analytic S1 Preregistration

**Checkpoint:** `first_hand_analytic_s1_preregistration_v0.8`  
**Status:** PREREGISTERED — S1 NOT RUN  
**Phase:** analytic self-embedment audit  
**Primary source:** *The Arm of God*, Meru Foundation  
**Source asset:** `AOG_PDF_2005A`

## 1. Purpose

This checkpoint freezes the first analytic self-embedment diagnostic for the First Hand construction before any S1 result is computed.

The preceding page-7 digitisation phase is closed.

The published spiral drawing is now treated as an illustrative hand drawing rather than as a sufficiently precise metric specification of the reciprocal spiral. No further pixel reconstruction of the page-7 spiral may be used to fit, alter, optimise, select, or repair the analytic construction tested here.

The present checkpoint asks only:

> Under the preregistered spherical construction, what is the directed intrinsic tangent mismatch between the two endpoints of the exact unitary reciprocal spiral?

This is S1 only.

No S1.5, S2, comparator-map test, logarithmic-spiral comparator, golden-spiral comparator, toroidal construction, dimpled-sphere construction, three-copy Hand test, recursive nesting test, or Hebrew-letter projection test is performed in this checkpoint.

---

## 2. Exact planar generator

The source curve is fixed as

\[
r(\theta)=\frac{1}{\theta},
\qquad
\theta>0.
\]

Its Cartesian parameterisation is

\[
\gamma(\theta)
=
\left(
\frac{\cos\theta}{\theta},
\frac{\sin\theta}{\theta}
\right).
\]

No parameters of this curve are fitted.

The directed curve orientation for every endpoint test is

\[
\text{inner}\longrightarrow\text{outer},
\]

which corresponds to decreasing \(\theta\).

---

## 3. Frozen truncation branches

Two source-supported truncation conventions are retained independently.

### 3.1 AOG-PROSE

\[
\theta_{\rm outer}\to0^+,
\qquad
\theta_{\rm inner}=3\pi.
\]

Hence

\[
\theta_{\rm inner}-\theta_{\rm outer}
\to3\pi,
\]

giving exactly

\[
3\pi\ {\rm rad}
=
540^\circ
=
1.5\ {\rm turns}.
\]

The outer endpoint is an asymptotic planar endpoint and must be handled through its exact analytic spherical limit.

It must not be replaced by an arbitrary small positive numerical value of \(\theta\).

### 3.2 AOG-DIAGRAM

\[
\theta_{\rm outer}=1,
\qquad
\theta_{\rm inner}=1+3\pi.
\]

Hence

\[
\theta_{\rm inner}-\theta_{\rm outer}
=
3\pi,
\]

again giving exactly

\[
540^\circ
=
1.5\ {\rm turns}.
\]

These are two separate registered source interpretations.

They must not be averaged, merged, interpolated, silently reconciled, or selected between using the S1 result.

---

## 4. Canonical analytic spherical construction

The primary S1 construction is the isotropic inverse-gnomonic member of the previously established source-compatible central-projective family:

\[
M_k(x,y)
=
\frac{(kx,ky,1)}
{\sqrt{k^2x^2+k^2y^2+1}},
\qquad
k>0.
\]

This is a registered analytic model convention.

It is not asserted to be the uniquely recoverable historical projection used by the source.

Composing \(M_k\) with the exact reciprocal spiral gives

\[
M_k(\gamma(\theta))
=
\frac{
\left(
k\cos\theta/\theta,\,
k\sin\theta/\theta,\,
1
\right)
}{
\sqrt{
k^2/\theta^2+1
}
}.
\]

Because \(\theta>0\), multiplication of numerator and denominator by \(\theta\) is legitimate, yielding the exact closed form

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

This is the primary computational representation.

It contains no image-derived fitted parameters.

It also satisfies identically

\[
\|\Gamma_k(\theta)\|=1,
\]

so the image lies exactly on \(S^2\).

---

## 5. Registered spherical scale branches

The source leaves an unresolved unit-angle ambiguity.

The following two source-motivated scale conventions are therefore retained as separate S1 branches:

\[
\mathrm{G30}:
\qquad
k
=
\tan\left(\frac{\pi}{6}\right)
=
\frac{1}{\sqrt3},
\]

and

\[
\mathrm{GHALF}:
\qquad
k
=
\tan\left(\frac12\right).
\]

Numerically these correspond approximately to

\[
k_{\rm G30}\approx0.57735,
\]

and

\[
k_{\rm GHALF}\approx0.54630.
\]

Their difference is only about \(5.4\%\).

Accordingly, agreement between G30 and GHALF must not be interpreted as strong scale robustness.

The broader source ambiguity is substantially larger. In particular, a one-radian angular interpretation would correspond within this model convention to

\[
k=\tan(1)\approx1.5574,
\]

approximately \(2.70\) times the registered G30 scale.

That larger branch is deliberately excluded from this checkpoint.

This creates an acknowledged asymmetry: the AOG-DIAGRAM truncation uses the marker

\[
\theta_{\rm outer}=1,
\]

while the present scale matrix does not include \(k=\tan(1)\).

This is intentional scoping, not a claim that the one-radian scale interpretation has been ruled out.

`GUNIT`, `GONE`, continuously optimised \(k\), image-derived scales, anisotropic projective scales, and any additional scale comparators remain outside S1.

Neither registered scale may be selected because it produces a smaller tangent mismatch.

---

## 6. Exact prose outer limit

For AOG-PROSE,

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

Therefore

\[
\lim_{\theta\to0^+}\Gamma_k(\theta)
=
(1,0,0).
\]

Thus the planar infinite end becomes a finite equatorial spherical point analytically.

No epsilon truncation is permitted.

Define

\[
N_k(\theta)
=
(k\cos\theta,\,
k\sin\theta,\,
\theta),
\]

and

\[
s_k(\theta)
=
\sqrt{k^2+\theta^2}.
\]

Then

\[
\Gamma_k(\theta)
=
\frac{N_k(\theta)}{s_k(\theta)}.
\]

With

\[
N_k'(\theta)
=
(-k\sin\theta,\,
k\cos\theta,\,
1),
\]

the derivative is

\[
\Gamma_k'(\theta)
=
\frac{N_k'(\theta)}{s_k(\theta)}
-
\frac{\theta N_k(\theta)}
{s_k(\theta)^3}.
\]

The directed inner-to-outer unit tangent is defined as

\[
\tau_k(\theta)
=
-
\frac{\Gamma_k'(\theta)}
{\|\Gamma_k'(\theta)\|}.
\]

The minus sign is required because inner-to-outer motion corresponds to decreasing \(\theta\).

For the prose outer endpoint,

\[
\tau_{k,\rm outer}^{\rm prose}
=
\lim_{\theta\to0^+}\tau_k(\theta).
\]

This tangent must be obtained analytically or by an algebraically equivalent exact limiting expression.

It must not be estimated from finite-\(\theta\) sampling.

---

## 7. Intrinsic endpoint tangent comparison

The two endpoint tangents generally belong to different tangent planes of \(S^2\).

Therefore S1 must not compare them using an unqualified ambient-space dot product.

Let

\[
p_i
=
\Gamma_k(\theta_{\rm inner}),
\]

and

\[
p_o
=
\Gamma_k(\theta_{\rm outer}),
\]

with the exact limiting value used for \(p_o\) in AOG-PROSE.

The outer tangent is parallel-transported from \(p_o\) to \(p_i\) along the unique shorter great-circle geodesic joining the endpoint positions.

Equivalently, let \(R_{o\to i}\) denote the unique minimal three-dimensional rotation satisfying

\[
R_{o\to i}p_o=p_i,
\]

with rotation axis parallel to

\[
p_o\times p_i.
\]

Then

\[
\widetilde{\tau}_o
=
R_{o\to i}\tau_o.
\]

If

\[
p_o=p_i
\]

to numerical precision, the transport is the identity.

If \(p_o\) and \(p_i\) are antipodal to numerical precision, the shortest geodesic is non-unique and so is the associated parallel transport.

That branch must therefore return

`S1_TRANSPORT_UNDEFINED_ANTIPODAL`

rather than resolving the ambiguity through an arbitrary rotation axis.

---

## 8. What S1 does and does not represent

Parallel transport provides a canonical intrinsic comparison between two tangent vectors located at different points of \(S^2\).

It does **not** by itself represent literal recursive nesting.

A true “seed inside fruit” self-embedment condition would require specifying the similarity, projection, or other transformation that places one copy of the curve or Hand geometry inside another and then comparing the corresponding transformed tangent data under that embedding map.

That is a different mathematical condition.

Accordingly, S1 is an endpoint tangent-compatibility diagnostic only.

It is not a miniature proof of recursive self-similarity, nesting, or self-embedment.

---

## 9. Primary S1 statistics

After parallel transport, define

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

The directed tangent mismatch is

\[
\Delta_{\rm S1}
=
\operatorname{atan2}(c,d),
\qquad
0\leq\Delta_{\rm S1}\leq\pi.
\]

The equivalent directed vector residual is

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

is explicitly prohibited.

Using \(|d|\) would identify anti-parallel tangents with parallel tangents and would destroy the directed nature of S1.

---

## 10. Compatibility predicate

Exact mathematical directed tangent compatibility means

\[
\Delta_{\rm S1}=0,
\]

equivalently

\[
R_{\rm S1}=0.
\]

For floating-point execution only, the preregistered numerical-zero criterion is

\[
\Delta_{\rm S1}
\leq
10^{-10}\ {\rm rad}.
\]

This is solely an implementation tolerance for mathematical zero.

It is not an observational uncertainty, drawing tolerance, fitting tolerance, or allowance for source imprecision.

Every raw mismatch must still be reported in both radians and degrees.

### 10.1 Expected behaviour of the binary predicate

No structural argument presently forces the fixed reciprocal spiral, fixed truncation endpoints, and fixed spherical map branches to produce

\[
\Delta_{\rm S1}=0.
\]

Exact compatibility is therefore expected a priori to be a highly restrictive outcome.

The binary `COMPATIBLE / NOT_COMPATIBLE` predicate is consequently not the principal quantitative content of the checkpoint.

The primary scientific diagnostic is the preregistered continuous magnitude

\[
\Delta_{\rm S1},
\]

together with the equivalent residual

\[
R_{\rm S1}.
\]

This statement is made before execution and must not be altered in response to the observed S1 values.

A non-zero result is not to be portrayed as surprising merely because the binary criterion is stringent.

---

## 11. Registered S1 branch matrix

| S1 branch | Truncation | Spherical scale |
|---|---|---|
| `S1-PROSE-G30` | \(\theta_{\rm outer}\to0^+,\ \theta_{\rm inner}=3\pi\) | \(k=\tan(\pi/6)\) |
| `S1-PROSE-GHALF` | \(\theta_{\rm outer}\to0^+,\ \theta_{\rm inner}=3\pi\) | \(k=\tan(1/2)\) |
| `S1-DIAGRAM-G30` | \(\theta_{\rm outer}=1,\ \theta_{\rm inner}=1+3\pi\) | \(k=\tan(\pi/6)\) |
| `S1-DIAGRAM-GHALF` | \(\theta_{\rm outer}=1,\ \theta_{\rm inner}=1+3\pi\) | \(k=\tan(1/2)\) |

All four registered cells must eventually be evaluated and reported independently.

There is no best-branch search.

There is no averaging over branches.

There is no post-result selection of a preferred truncation.

There is no post-result selection of a preferred scale.

---

## 12. Result vocabulary

Each registered branch may return only one primary S1 state:

`S1_DIRECTED_COMPATIBLE`

`S1_DIRECTED_NOT_COMPATIBLE`

`S1_TRANSPORT_UNDEFINED_ANTIPODAL`

`S1_TECHNICAL_FAILURE`

An optional cross-branch summary may use only:

`S1_ALL_REGISTERED_BRANCHES_COMPATIBLE`

`S1_NO_REGISTERED_BRANCH_COMPATIBLE`

`S1_BRANCH_DEPENDENT`

`S1_INCOMPLETE`

A branch-dependent outcome does not authorise choosing the successful branch as the intended historical construction.

---

## 13. Required output record

Each branch result must record:

- branch identifier;
- truncation convention;
- exact endpoint parameter values or limiting endpoint specification;
- scale convention;
- value of \(k\);
- spherical endpoint positions;
- directed endpoint tangents;
- transport axis where applicable;
- transport angle where applicable;
- transported outer tangent;
- tangent dot product \(d\);
- cross-product norm \(c\);
- \(\Delta_{\rm S1}\) in radians;
- \(\Delta_{\rm S1}\) in degrees;
- \(R_{\rm S1}\);
- numerical-zero tolerance;
- final registered S1 state.

The output must also record explicitly that no page-7 spiral pixel data entered the analytic computation.

---

## 14. Prohibited operations

No optimisation is permitted.

No scale \(k\) may be fitted to minimise S1.

No phase may be fitted to minimise S1.

No orientation may be fitted to minimise S1.

No general projective matrix may be fitted using S1.

No page-7 spiral pixels may be used to alter the analytic curve.

No endpoint may be moved to improve tangent compatibility.

No truncation endpoint may be modified.

No \(3\pi\) span may be replaced by an approximately measured turn count.

No source discrepancy may be averaged away.

No source ambiguity may be silently repaired.

No result-driven reinterpretation of the prose or diagram branch is permitted.

No comparator projection is run.

No stereographic comparator is run.

No logarithmic-spiral comparator is run.

No golden-spiral comparator is run.

No `GUNIT`, `GONE`, or continuously varying scale sensitivity test is run.

No S1.5 frame-alignment test is run.

No S2 recursive-nesting test is run.

No three-copy \(120^\circ\) Hand construction is scored.

No toroidal seven-region-map compatibility is scored.

No dimpled-sphere construction is run.

No letter-projection claim is evaluated.

---

## 15. Interpretation boundary

A positive S1 result establishes only that the exact reciprocal spiral has directed endpoint tangent compatibility under the specified registered spherical branch.

A negative S1 result establishes only that exact directed endpoint tangent compatibility fails for that registered branch.

Neither result establishes that the source historically used the exact registered spherical map.

Neither result establishes the full First Hand geometry.

Neither result establishes recursive self-embedment.

Neither result establishes Hebrew-letter generation.

Neither result establishes the toroidal construction.

Neither result establishes the dimpled-sphere construction.

### 15.1 Relation to Tenen's comparative claim

The source claim of interest is comparative: the reciprocal spiral is presented as succeeding in a way that alternative spirals do not.

This S1 checkpoint contains no comparator spiral.

Therefore:

> **No positive or negative S1 result from this checkpoint alone supports or refutes the comparative source claim.**

A large reciprocal-spiral mismatch could still be smaller than the mismatch of every registered comparator.

A small reciprocal-spiral mismatch could still fail to distinguish it from alternative spirals.

Those questions belong exclusively to a later preregistered comparative checkpoint.

No conclusion about comparative superiority may be drawn from S1 alone.

### 15.2 Model-family limitation

The source-compatible central-projective family is broader than the canonical isotropic inverse-gnomonic member used here.

Therefore failure of one or all registered S1 branches must not automatically be generalised into failure of every possible central-projective realisation.

Likewise, success of a registered branch must not be generalised into unique recovery of the historical construction.

---

## 16. Execution boundary

This checkpoint ends with preregistration.

No S1 branch may be numerically evaluated before this document has been committed and frozen.

No value of

\[
\Delta_{\rm S1}
\]

may be previewed.

No value of

\[
R_{\rm S1}
\]

may be previewed.

No endpoint tangent dot product may be previewed.

No scratch script may be used to inspect whether a registered branch succeeds.

Symbolic verification of the preregistered identities and limiting formulas is permitted provided it does not evaluate the S1 branch outcomes.

The next checkpoint, and only the next checkpoint, may implement and execute the four registered S1 branches exactly as specified here.

Any later extension — including GUNIT/GONE scale sensitivity, S1.5, S2, comparator spirals, toroidal variants, or dimpled-sphere variants — requires its own preregistration before execution.

---

## 17. Frozen methodological sequence

The audit sequence is therefore:

\[
\text{source evidence}
\]

\[
\downarrow
\]

\[
\text{page-7 digitisation and reconstruction audit}
\]

\[
\downarrow
\]

\[
\text{digitisation closeout}
\]

\[
\downarrow
\]

\[
\text{exact analytic model}
\]

\[
\downarrow
\]

\[
\boxed{\text{S1 preregistration}}
\]

\[
\downarrow
\]

\[
\text{commit and freeze}
\]

\[
\downarrow
\]

\[
\text{S1 execution}
\]

No later stage may retroactively alter an earlier source interpretation or analytic convention because of the numerical outcome obtained downstream.
