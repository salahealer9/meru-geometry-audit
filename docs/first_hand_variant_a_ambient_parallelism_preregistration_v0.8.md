# First Hand Variant-A Ambient Endpoint-Parallelism Preregistration

**Checkpoint:** `first_hand_variant_a_ambient_parallelism_preregistration_v0.8`  
**Status:** PREREGISTERED — AMBIENT ENDPOINT VALUES NOT RUN  
**Phase:** source-semantics bridge after S1 clarification  
**Variant:** A — cube-octahedral / canonical inverse-gnomonic sphere only  
**Historical primary span:** 1.5 turns  
**Image pixel data:** prohibited  
**Intrinsic transport:** not used in the primary ambient statistics

## 1. Purpose

This checkpoint preregisters a small bridge test between:

- Stan Tenen's explicit source language that the outer end and inner tip of a self-embedding vortex are "parallel"; and
- the completed S1 audit, which operationalized that statement intrinsically by parallel-transporting the outer tangent to the inner endpoint on the sphere.

The source does not explicitly specify whether "parallel" means:

1. directed ambient three-dimensional tangent vectors;
2. unoriented ambient tangent lines;
3. intrinsic tangent agreement after transport on the carrier surface.

The completed S1 checkpoint already froze and evaluated interpretation (3), using directed tangent vectors and shorter-geodesic transport.

This checkpoint freezes interpretations (1) and (2) before any ambient endpoint angle is evaluated.

The purpose is semantic clarification, not model fitting.

---

## 2. Source criterion

The source identifies endpoint parallelism as the decisive condition for self-embedment:

> the outer end and inner tip must be parallel so the vortex ends can line up.

This checkpoint does not alter that source statement.

It only separates two mathematically standard meanings of "parallel" available in the common ambient space \(\mathbb{R}^3\).

---

## 3. Frozen Variant-A geometry

No new curve or surface geometry is introduced.

The checkpoint reuses the exact Variant-A construction already frozen in the reciprocal S1 work.

For scale \(k>0\), the spherical reciprocal branch is

\[
\Gamma_k(\theta)
=
\frac{
\left(
k\cos\theta,\,
k\sin\theta,\,
\theta
\right)
}{
\sqrt{k^2+\theta^2}
}.
\]

For the AOG-DIAGRAM branch:

\[
\theta_{\rm outer}=1,
\]

\[
\theta_{\rm inner}=1+3\pi.
\]

The directed curve orientation remains:

\[
\text{inner}\longrightarrow\text{outer},
\]

corresponding to decreasing \(\theta\).

The directed tangent is therefore

\[
\tau_k(\theta)
=
-\frac{\Gamma_k'(\theta)}
{\|\Gamma_k'(\theta)\|}.
\]

No endpoint is moved.

No truncation is changed.

No reciprocal parameter is fitted.

---

## 4. Registered spherical scales

The only registered scales are the same frozen scales used throughout Variant-A S1:

### G30

\[
k_{\rm G30}
=
\tan(\pi/6)
=
\frac{1}{\sqrt3}.
\]

### GHALF

\[
k_{\rm GHALF}
=
\tan(1/2).
\]

No additional scale is introduced.

The broader one-radian interpretation remains outside this checkpoint.

---

## 5. Primary ambient directed statistic

Because both endpoint tangents are ordinary vectors in the same embedding space

\[
\mathbb{R}^3,
\]

they may be compared directly without tangent-space identification or parallel transport.

Define

\[
d_{\rm amb}
=
\tau_{\rm outer}\cdot\tau_{\rm inner},
\]

and

\[
c_{\rm amb}
=
\|\tau_{\rm outer}\times\tau_{\rm inner}\|.
\]

The preregistered directed ambient angle is

\[
\Delta_{\rm amb}^{\rm dir}
=
\operatorname{atan2}
\left(
c_{\rm amb},
d_{\rm amb}
\right)
\in[0,\pi].
\]

Interpretation:

\[
\Delta_{\rm amb}^{\rm dir}=0
\]

means the directed endpoint tangent vectors agree exactly.

\[
\Delta_{\rm amb}^{\rm dir}=\pi
\]

means they are exactly anti-parallel.

The directed ambient vector residual is

\[
R_{\rm amb}^{\rm dir}
=
\|\tau_{\rm outer}-\tau_{\rm inner}\|.
\]

Exact directed ambient compatibility requires

\[
\Delta_{\rm amb}^{\rm dir}=0.
\]

For floating-point classification only, the existing S1 numerical-zero tolerance may be reused:

\[
10^{-10}\ {\rm rad}.
\]

---

## 6. Co-primary ambient unoriented line statistic

Because the source uses the word "parallel" without explicitly specifying tangent orientation, an unoriented line interpretation is also preregistered before execution.

Define

\[
\Delta_{\rm amb}^{\rm line}
=
\arccos
\left(
\left|
\tau_{\rm outer}\cdot\tau_{\rm inner}
\right|
\right)
\in
\left[
0,\frac{\pi}{2}
\right].
\]

Equivalent robust implementation:

\[
\Delta_{\rm amb}^{\rm line}
=
\operatorname{atan2}
\left(
\|\tau_{\rm outer}\times\tau_{\rm inner}\|,
\left|
\tau_{\rm outer}\cdot\tau_{\rm inner}
\right|
\right).
\]

The `atan2` form is preferred in implementation.

Interpretation:

\[
\Delta_{\rm amb}^{\rm line}=0
\]

means the two tangent **lines** are parallel, regardless of whether the vectors point in the same or opposite directions.

Thus both

\[
\tau_{\rm outer}=\tau_{\rm inner}
\]

and

\[
\tau_{\rm outer}=-\tau_{\rm inner}
\]

count as exact unoriented line parallelism.

This statistic is preregistered independently of the directed statistic.

Neither may be selected post hoc as the "correct" source interpretation based on which yields a more favorable result.

---

## 7. Why both statistics are required

The source's word "parallel" is mathematically ambiguous when applied to physical ends.

Two plausible interpretations exist.

### Directed interpretation

If recursive insertion requires the vortex direction to continue consistently from one copy into another, then the tangent vectors should agree in orientation.

This is closer to the orientation convention already frozen in S1.

### Unoriented interpretation

If the source means only that the physical axes of the two ends line up, then anti-parallel tangent vectors describe the same tangent line and may count as parallel.

Because the source does not formalize this distinction, the audit must report both.

The checkpoint therefore has two co-primary semantic outcomes rather than a single post-hoc choice.

---

## 8. Registered execution cells

The historical primary execution contains exactly two geometric branches:

1. `AMB-DIAGRAM-G30`
2. `AMB-DIAGRAM-GHALF`

Each branch reports both:

- \(\Delta_{\rm amb}^{\rm dir}\);
- \(\Delta_{\rm amb}^{\rm line}\).

Thus there are two geometric executions and four reported primary angle values.

No comparator family is executed.

No truncation-sensitivity matrix is executed.

No AOG-PROSE branch is included in the primary checkpoint.

---

## 9. Why AOG-PROSE is excluded from this bridge checkpoint

The purpose of this checkpoint is to clarify the literal meaning of the source's "parallel" claim on the same finite historical AOG-DIAGRAM branch already central to the comparator and truncation analyses.

The AOG-PROSE branch has a limiting outer endpoint and a different endpoint definition.

It may be studied separately if needed, but mixing it into this small semantic bridge would introduce an unnecessary second ambiguity.

Therefore:

> This checkpoint is AOG-DIAGRAM only.

No later result may retroactively add the AOG-PROSE branch to this preregistration.

---

## 10. Registered states — directed ambient interpretation

For each scale:

`AMBIENT_DIRECTED_PARALLEL`

if

\[
\Delta_{\rm amb}^{\rm dir}
\le
10^{-10}\ {\rm rad}.
\]

Otherwise:

`AMBIENT_DIRECTED_NOT_PARALLEL`.

If the endpoint tangent cannot be evaluated:

`AMBIENT_DIRECTED_TECHNICAL_FAILURE`.

---

## 11. Registered states — unoriented ambient line interpretation

For each scale:

`AMBIENT_LINE_PARALLEL`

if

\[
\Delta_{\rm amb}^{\rm line}
\le
10^{-10}\ {\rm rad}.
\]

Otherwise:

`AMBIENT_LINE_NOT_PARALLEL`.

If the endpoint tangent cannot be evaluated:

`AMBIENT_LINE_TECHNICAL_FAILURE`.

---

## 12. Cross-scale summary states

### Directed

`AMBIENT_DIRECTED_PARALLEL_ALL_SCALES`

if both G30 and GHALF are directed-parallel.

`AMBIENT_DIRECTED_NOT_PARALLEL_ALL_SCALES`

if both fail directed parallelism.

`AMBIENT_DIRECTED_MIXED_SCALE_RESULT`

if only one scale is directed-parallel.

`AMBIENT_DIRECTED_INCOMPLETE`

if a technical failure prevents classification.

### Unoriented line

`AMBIENT_LINE_PARALLEL_ALL_SCALES`

if both G30 and GHALF are line-parallel.

`AMBIENT_LINE_NOT_PARALLEL_ALL_SCALES`

if both fail line parallelism.

`AMBIENT_LINE_MIXED_SCALE_RESULT`

if only one scale is line-parallel.

`AMBIENT_LINE_INCOMPLETE`

if a technical failure prevents classification.

---

## 13. Relationship to the completed intrinsic S1 result

The completed intrinsic directed S1 values are immutable references:

### G30

\[
\Delta_{\rm S1}^{\rm intrinsic}
=
144.5776221089075^\circ.
\]

### GHALF

\[
\Delta_{\rm S1}^{\rm intrinsic}
=
144.2022631722743^\circ.
\]

These values must not be recomputed by this checkpoint.

The ambient bridge may report their difference from the new directed ambient angle:

\[
E_k
=
\Delta_{\rm amb}^{\rm dir}
-
\Delta_{\rm S1}^{\rm intrinsic}.
\]

This is a descriptive diagnostic only.

It quantifies how much the endpoint-angle result depends on:

- direct ambient comparison; versus
- intrinsic comparison after spherical parallel transport.

No hypothesis is preregistered for the sign of \(E_k\).

---

## 14. Interpretation matrix

After execution, interpretation must follow this predeclared matrix.

### Case A — directed and line interpretations both fail

If

\[
\Delta_{\rm amb}^{\rm dir}>0
\]

and

\[
\Delta_{\rm amb}^{\rm line}>0
\]

at both scales, then the Variant-A reciprocal candidate fails the source's endpoint-parallelism criterion under both standard ambient interpretations.

This would strengthen the negative Variant-A conclusion beyond the intrinsic S1 operationalization.

### Case B — directed fails, line succeeds

If

\[
\Delta_{\rm amb}^{\rm dir}>0
\]

but

\[
\Delta_{\rm amb}^{\rm line}=0,
\]

then the endpoint tangent vectors are anti-parallel.

The source's wording would remain semantically ambiguous:

- directed continuity would fail;
- unoriented tangent-line parallelism would succeed.

No single "source verdict" may be chosen without additional historical evidence.

### Case C — directed succeeds

If

\[
\Delta_{\rm amb}^{\rm dir}=0,
\]

then both directed and line parallelism succeed automatically.

This would show that the Variant-A reciprocal candidate satisfies the source's endpoint-parallelism statement under direct ambient comparison even though the completed intrinsic S1 result differs.

That discrepancy would become a geometric interpretation issue, not a numerical one.

### Case D — scale disagreement

If G30 and GHALF produce different exact states, the source criterion is not robust to the registered scale ambiguity.

No preferred scale may be selected post hoc.

---

## 15. No fitting or optimization

This checkpoint is evaluation-only.

The following operations are prohibited:

- changing \(k\);
- fitting \(k\);
- moving either endpoint;
- changing the 1.5-turn span;
- changing \(\theta_{\rm outer}=1\);
- changing the reciprocal law;
- rotating one tangent independently to improve agreement;
- parallel transporting either tangent;
- using a dimpled-sphere model;
- switching between directed and unoriented definitions after results are seen;
- using image pixel data.

The endpoint tangents are those generated by the already frozen Variant-A curve.

---

## 16. Primitive implementation requirements

The implementation-only checkpoint must verify, without evaluating the two registered endpoint cells:

1. the registered scales equal the frozen G30 and GHALF values;
2. the registered endpoints equal
   \[
   1
   \quad\text{and}\quad
   1+3\pi;
   \]
3. the tangent orientation is inner-to-outer;
4. tangent vectors are unit length;
5. tangent vectors lie in the local tangent planes of the sphere;
6. the directed ambient angle satisfies
   \[
   \Delta_{\rm dir}
   =
   \operatorname{atan2}(\|a\times b\|,a\cdot b);
   \]
7. the line angle satisfies
   \[
   \Delta_{\rm line}
   =
   \operatorname{atan2}(\|a\times b\|,|a\cdot b|);
   \]
8. directed equality returns \(0\);
9. directed anti-parallelism returns \(\pi\);
10. line anti-parallelism returns \(0\);
11. no call to spherical parallel transport occurs;
12. no registered branch is evaluated during primitive tests.

---

## 17. Required execution outputs

The registered execution must produce:

- JSON;
- CSV;
- concise Markdown report.

For each scale, record:

- scale identifier;
- \(k\);
- outer endpoint;
- inner endpoint;
- outer tangent;
- inner tangent;
- tangent dot product;
- tangent cross-product norm;
- \(\Delta_{\rm amb}^{\rm dir}\) in radians and degrees;
- \(R_{\rm amb}^{\rm dir}\);
- directed state;
- \(\Delta_{\rm amb}^{\rm line}\) in radians and degrees;
- line state;
- inherited intrinsic S1 reference;
- descriptive ambient-minus-intrinsic difference;
- confirmation that parallel transport was not used;
- confirmation that image pixels were not used.

---

## 18. Interpretation boundary

This checkpoint tests only the semantic meaning of endpoint parallelism on the already frozen Variant-A reciprocal AOG-DIAGRAM construction.

It does not test:

- Variant B;
- dimple-width dependence;
- logarithmic comparators;
- truncation parity;
- full recursive insertion;
- curvature compatibility;
- finite-thickness clearance;
- self-similarity;
- Hebrew-letter generation.

It introduces no stronger nesting requirement.

---

## 19. Consequence for Variant B

The Variant-B preregistration should not be finalized until this bridge is closed.

The ambient statistics are especially useful for Variant B because they are path-independent in the embedding space.

On a genus-1 carrier, intrinsic parallel transport becomes path- and homotopy-class-dependent.

Therefore the likely later hierarchy is:

1. source-primary ambient endpoint parallelism;
2. separately identified intrinsic transport diagnostics with a preregistered path;
3. independently strengthened nesting tests introduced by the audit.

The present checkpoint resolves the first semantic layer on Variant A before that more complex geometry is introduced.

---

## 20. Execution boundary

This document ends at preregistration.

Before this preregistration is committed and frozen:

- no ambient directed endpoint angle may be evaluated;
- no ambient line endpoint angle may be evaluated;
- no ambient dot product may be previewed;
- no ambient cross-product norm may be previewed;
- no ambient-versus-intrinsic difference may be evaluated.

After preregistration freeze:

1. implement the evaluator;
2. run primitive tests only;
3. freeze the implementation-only commit;
4. execute the two registered branches exactly once.

---

## 21. Closed preregistration statement

The registered question is:

> **Does the historical 1.5-turn Variant-A reciprocal candidate satisfy Tenen's endpoint-parallelism criterion when "parallel" is interpreted directly in ambient \(\mathbb{R}^3\), under either a directed-vector or unoriented-line definition?**

Both definitions are frozen before execution.

Neither may be chosen post hoc.

The result will clarify source semantics without reopening or altering the completed intrinsic S1 checkpoint.
