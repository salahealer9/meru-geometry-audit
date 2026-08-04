# First Hand S1 Source-Criterion Addendum

**Checkpoint:** `first_hand_s1_source_criterion_addendum_v0.8`  
**Status:** SOURCE-INTERPRETATION ADDENDUM — NO NUMERICAL RE-EXECUTION  
**Phase:** clarification of the completed Variant-A S1 audit  
**Applies to:** sealed S1, comparator, and truncation-parity checkpoints  
**Numerical results altered:** no

## 1. Purpose

This addendum records a source-interpretation clarification discovered after the Variant-A S1, comparator, and truncation-parity checkpoints had already been sealed.

The clarification does not alter any numerical result, preregistration, implementation, execution artifact, or decision state.

It changes only how the completed S1 test should be described relative to Stan Tenen's own stated self-embedment criterion.

The historical closeout files remain untouched.

---

## 2. Source clarification

In *Some Notes on the Logarithmic and Golden Mean Spirals*, Stan Tenen states that:

- logarithmic spirals self-embed in two dimensions because they are self-similar;
- when projected onto a sphere or Dimpled-Sphere, a logarithmic spiral allegedly cannot self-embed because its outer part cannot be parallel to its inner tip;
- the ends of such a vortex allegedly cannot line up;
- the intended FIRST HAND vortices self-embed because their outer ends and inner tips are parallel;
- those same FIRST HAND vortices are explicitly not self-similar;
- if they were self-similar, that would disqualify them for the intended symmetry/asymmetry role.

Therefore the source itself makes **endpoint parallelism** a direct operational criterion for self-embedment.

This is stronger source support for the completed S1 test than had previously been stated.

---

## 3. Correction to the earlier "proxy" language

Earlier audit notes described S1 as a proxy for self-embedment.

That wording is now too weak.

The completed S1 checkpoint directly targeted the same geometric feature Tenen explicitly identifies as decisive for self-embedment:

\[
\text{outer-end tangent parallel to inner-tip tangent}.
\]

However, the source does not provide a complete mathematical definition of "parallel" for tangent directions based at different points on a curved carrier.

The S1 checkpoint therefore remains an **operationalization** of the source criterion rather than a verbatim mathematical formula supplied by the source.

The preferred description is:

> **S1 directly tests Tenen's stated endpoint-parallelism criterion under a preregistered directed intrinsic parallel-transport operationalization.**

It should no longer be described merely as an unrelated preliminary proxy.

---

## 4. What S1 added mathematically

Tenen's source statement leaves several geometric choices unspecified.

The completed S1 preregistration fixed them explicitly.

### 4.1 Directed rather than unoriented tangent comparison

S1 compared tangent **vectors**, not only tangent lines.

Thus anti-parallel endpoint directions were treated as incompatible.

The registered statistic was

\[
\Delta_{\rm S1}
=
\operatorname{atan2}
\left(
\|\widetilde{\tau}_o\times\tau_i\|,
\widetilde{\tau}_o\cdot\tau_i
\right)
\in[0,\pi].
\]

The transformation

\[
|\widetilde{\tau}_o\cdot\tau_i|
\]

was explicitly prohibited.

This means S1 interpreted "line up" as requiring directed endpoint orientation, not merely collinearity.

### 4.2 Intrinsic comparison

On Variant A, the outer and inner tangent vectors live in different tangent planes of the sphere.

S1 therefore did not compare their coordinate triples directly.

Instead, the outer tangent was parallel transported to the inner endpoint.

### 4.3 Frozen transport path

The transport path was the unique shorter great-circle geodesic between the two spherical endpoints.

This made the comparison well-defined on the genus-zero Variant-A sphere except in the antipodal case.

These choices sharpen the source statement into a reproducible mathematical test.

They were introduced by the audit, not specified explicitly by Tenen.

---

## 5. Consequence for the completed Variant-A reciprocal result

For the historical 1.5-turn AOG-DIAGRAM branch, the completed Variant-A reciprocal S1 results were:

\[
\Delta_{\rm S1}
=
144.5776221089075^\circ
\]

for G30, and

\[
\Delta_{\rm S1}
=
144.2022631722743^\circ
\]

for GHALF.

Under the registered directed intrinsic interpretation, these values are far from

\[
0^\circ.
\]

Therefore the completed Variant-A reciprocal result is not merely a poor score under an arbitrary audit proxy.

It is a failure of the source's stated endpoint-parallelism requirement **under the exact directed intrinsic operationalization that was preregistered**.

The correct wording is:

> On the registered Variant-A sphere construction, the reciprocal FIRST HAND candidate fails Tenen's stated endpoint-parallelism self-embedment criterion under the audit's directed intrinsic transport definition.

This conclusion remains Variant-A specific.

---

## 6. Source scope includes the ordinary sphere

The source explicitly states the negative logarithmic claim for both:

- an ordinary sphere; and
- a Dimpled-Sphere.

Therefore Variant A was not merely a control surface outside the source claim.

The completed spherical logarithmic comparison directly addresses one carrier surface named by Tenen.

At the historical 1.5-turn truncation, the registered logarithmic branches returned approximately

\[
176.9^\circ
\text{ to }
179.2^\circ
\]

under S1.

Thus the source's negative statement about logarithmic endpoint parallelism on the sphere is reproduced under the audit's directed intrinsic operationalization.

---

## 7. The truncation-parity result limits that support

The later preregistered truncation-parity checkpoint established that the logarithmic S1 failure at 1.5 turns is strongly controlled by truncation parity.

At integer-turn truncations, the same fixed logarithmic spirals become nearly aligned:

\[
\Delta_{\rm S1}
\approx
0.65^\circ
\text{ to }
3.14^\circ.
\]

At odd-half-integer truncations, they become nearly anti-aligned:

\[
\Delta_{\rm S1}
\approx
176.86^\circ
\text{ to }
179.24^\circ.
\]

Therefore the source's negative logarithmic result is reproduced at the source's 1.5-turn truncation, but it is not a truncation-invariant property of the logarithmic family under S1.

This clarification remains unchanged.

---

## 8. Self-embedment is not self-similarity

The source explicitly distinguishes the two concepts.

The FIRST HAND vortices are said to self-embed while also being non-self-similar.

Self-similarity would conflict with the intended contrast between:

- tetrahedral symmetry; and
- spiral asymmetry.

Therefore:

> A global similarity self-map is not Tenen's stated self-embedment criterion.

No future audit checkpoint should present failure or success of a similarity-map condition as a direct test of Meru's stated endpoint-parallelism claim.

---

## 9. Stronger nesting conditions belong to the audit, not the source

Endpoint tangent parallelism is only a first-order local compatibility condition.

A stronger mathematical treatment of physical recursive nesting may reasonably test additional quantities such as:

- ambient endpoint position after placement;
- local surface-frame alignment;
- curvature compatibility;
- finite-thickness clearance;
- local or global non-intersection.

These may be scientifically valuable.

But they are **independent strengthened nesting criteria introduced by the audit**.

They must not be labeled as requirements explicitly stated by Tenen.

Accordingly, any future S1.5, S2, or finite-insertion test must include language equivalent to:

> **Independent strengthened nesting criterion; not a Meru-stated requirement.**

---

## 10. Ambient versus intrinsic parallelism remains unresolved by the source

The source says that vortex ends must be parallel and able to line up.

It does not explicitly state whether this means:

1. ambient three-dimensional tangent vectors are parallel;
2. tangent directions are intrinsically parallel after transport on the carrier surface;
3. tangent lines are parallel irrespective of orientation;
4. directed tangent vectors must agree in orientation.

The completed S1 test froze one defensible choice:

- directed;
- intrinsic;
- shorter-geodesic transport on the sphere.

That choice must remain historically associated with the sealed S1 checkpoint.

A separate preregistered bridge test may evaluate ambient directed and ambient unoriented endpoint parallelism without altering S1.

---

## 11. Why the sealed S1 closeout is not rewritten

The original S1 closeout reflected the source interpretation available at the time it was sealed.

Rewriting it after later source clarification would blur the chronology of the audit.

The correct reproducibility practice is therefore:

- preserve the original S1 closeout unchanged;
- preserve its generated results unchanged;
- add this explicit source-criterion clarification as a later document.

This addendum supersedes only the earlier **interpretive description** of S1 as merely a proxy.

It does not supersede the S1 mathematics or results.

---

## 12. Implication for the next checkpoint

Before constructing Variant B, the clean next test is a small Variant-A source-semantics bridge checkpoint.

Using the already frozen Variant-A endpoint tangents, preregister both:

### Ambient directed endpoint angle

\[
\Delta_{\rm amb}^{\rm dir}
=
\operatorname{atan2}
\left(
\|\tau_o\times\tau_i\|,
\tau_o\cdot\tau_i
\right).
\]

### Ambient unoriented line angle

\[
\Delta_{\rm amb}^{\rm line}
=
\arccos
\left(
|\tau_o\cdot\tau_i|
\right).
\]

These require no transport path because both tangent vectors are compared directly in the common ambient space

\[
\mathbb{R}^3.
\]

Both definitions must be preregistered before numerical evaluation so that neither can be selected post hoc.

---

## 13. Variant-B consequence

Variant B remains scientifically important because the source repeatedly discusses the Dimpled-Sphere and also makes a universal negative claim about logarithmic vortices under changes to its shape.

However, the Variant-B stage should not begin until the ambient-versus-intrinsic semantic bridge has been closed.

The later Variant-B design must also distinguish:

- source-primary endpoint parallelism;
- path-dependent intrinsic transport diagnostics on a genus-1 carrier;
- stronger physical nesting conditions introduced independently by the audit.

---

## 14. Closed addendum conclusion

The source clarification upgrades the interpretation of the completed S1 checkpoint.

The final statement is:

> **The Variant-A S1 checkpoint directly tests Tenen's explicit endpoint-parallelism self-embedment criterion under a preregistered directed intrinsic parallel-transport operationalization.**

It is therefore stronger than an arbitrary proxy.

At the source's historical 1.5-turn truncation:

- the reciprocal Variant-A candidate fails that operationalized criterion by roughly \(144^\circ\);
- the logarithmic candidates fail it by roughly \(177^\circ\) to \(179^\circ\);
- the later parity checkpoint demonstrates that the logarithmic failure is truncation-dependent.

The audit must continue to distinguish the source's stated first-order parallelism criterion from stronger nesting conditions introduced by the audit itself.

---

## 15. Phase status

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
\boxed{\text{S1 source-criterion clarification}}
\]

\[
\downarrow
\]

\[
\text{Variant-A ambient parallelism preregistration}
\]

\[
\downarrow
\]

\[
\text{ambient parallelism implementation freeze}
\]

\[
\downarrow
\]

\[
\text{ambient parallelism execution}
\]

\[
\downarrow
\]

\[
\text{revised Variant-B source specification}
\]

No existing numerical checkpoint is reopened by this addendum.
