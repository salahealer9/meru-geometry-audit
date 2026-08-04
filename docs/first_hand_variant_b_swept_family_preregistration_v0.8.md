# First Hand Variant-B Swept-Family Preregistration

**Checkpoint:** `first_hand_variant_b_swept_family_preregistration_v0.8`  
**Status:** PREREGISTERED — NO VARIANT-B ENDPOINT ANGLES RUN  
**Phase:** confirmatory Variant-B carrier sweep  
**Source-primary criterion:** ambient endpoint parallelism  
**Historical span:** 1.5 turns  
**Carrier family:** normalized elliptic fat torus of revolution  
**Image pixel data:** prohibited  
**Adaptive parameter refinement:** prohibited in this checkpoint

## 1. Purpose

This checkpoint preregisters the first explicit Variant-B metric family and a finite source-constrained sweep before any Variant-B endpoint-parallelism value is evaluated.

The source geometry is metrically underdetermined.

Accordingly, this checkpoint does **not** claim to reconstruct a unique historical Dimpled-Sphere.

Instead, it fixes one minimal analytic carrier family with:

- genus \(1\);
- a sphere-like fat exterior;
- a central axial hole / dimple;
- explicit throat width;
- explicit axial elongation;
- a smooth embedded surface for all registered parameter cells;
- a finite preregistered sweep over narrow through wider holes and modest through elongated axial shapes.

The same frozen carrier family and spiral-to-surface map are used for:

1. the reciprocal FIRST HAND candidate;
2. six fixed generic logarithmic comparators;
3. the Golden Mean logarithmic comparator.

No endpoint angle may be previewed before this preregistration and the implementation-only checkpoint are frozen.

---

## 2. Source questions

The sweep addresses two distinct source claims.

### 2.1 Positive reciprocal claim

The FIRST HAND vortex is said to self-embed because its outer end and inner tip are parallel.

Within the present analytic family, the audit asks:

> Does any preregistered Variant-B reciprocal cell satisfy ambient endpoint parallelism?

A success would be a success **within this reconstruction family**, not proof that the family is historically unique.

### 2.2 Negative logarithmic claim

The source states that logarithmic vortices do not self-embed on a sphere or Dimpled-Sphere because their outer and inner ends cannot be parallel, and further states that changing the Dimpled-Sphere shape does not repair that failure.

Within the present family, the audit asks:

> Does any preregistered logarithmic or Golden Mean cell provide a counterexample to that negative claim?

A single admissible exact-parallel cell would be a counterexample within the registered family.

Failure to find such a cell does **not** prove the universal source statement over every possible Dimpled-Sphere geometry.

---

## 3. Carrier family

For throat parameter

\[
w\in(0,1)
\]

and axial elongation

\[
e>0,
\]

define

\[
R(w)=\frac{1+w}{2},
\]

and

\[
a(w)=\frac{1-w}{2}.
\]

The carrier surface is

\[
X_{w,e}(u,v)
=
\begin{pmatrix}
\left(R+a\cos u\right)\cos v\\
\left(R+a\cos u\right)\sin v\\
e\,a\sin u
\end{pmatrix},
\]

with

\[
u,v\in[0,2\pi).
\]

The cylindrical radius is

\[
\rho(u)
=
R+a\cos u.
\]

The vertical coordinate is

\[
z(u)
=
e\,a\sin u.
\]

The outer equatorial radius is normalized exactly:

\[
R+a=1.
\]

The inner equatorial / throat radius is exactly:

\[
R-a=w.
\]

Thus \(w\) has a direct geometric interpretation:

> normalized minimum distance from the carrier surface to the symmetry axis.

No additional scale normalization is fitted.

---

## 4. Embedded-genus-1 proof

For every registered carrier,

\[
0<w<1.
\]

Therefore

\[
R-a=w>0.
\]

Hence

\[
\rho(u)\ge w>0
\]

for every meridional parameter \(u\).

The meridian

\[
\frac{(\rho-R)^2}{a^2}
+
\frac{z^2}{(ea)^2}
=
1
\]

is a simple ellipse entirely contained in the open half-plane

\[
\rho>0.
\]

Revolving a simple closed meridian contained in \(\rho>0\) about the \(z\)-axis produces a smooth embedded torus.

Therefore every registered \((w,e)\) cell is:

- non-self-intersecting;
- non-pinched;
- smooth;
- orientable;
- genus \(1\).

No endpoint result is needed to decide carrier admissibility.

---

## 5. Interpretation of the two carrier parameters

### 5.1 Throat width \(w\)

Small \(w\) corresponds to a narrow axial hole / dimple.

Large \(w\) corresponds to a wider hole.

The registered values are:

\[
w
\in
\{
0.02,\,
0.05,\,
0.10,\,
0.20,\,
0.30
\}.
\]

For descriptive reporting only:

- `NARROW`: \(w=0.02,0.05\);
- `MODERATE`: \(w=0.10,0.20\);
- `WIDE`: \(w=0.30\).

These labels do not alter admissibility or endpoint criteria.

### 5.2 Axial elongation \(e\)

The parameter \(e\) stretches the meridian along the symmetry axis without changing the normalized outer or inner equatorial radii.

The registered values are:

\[
e
\in
\{
1.4,\,
1.6,\,
1.8,\,
2.0,\,
2.2
\}.
\]

This sweep includes both relatively compact and visibly elongated fat-torus carriers.

No additional \(e\) value may be added after endpoint results are seen.

---

## 6. Registered carrier matrix

The Cartesian product

\[
\mathcal C
=
\mathcal W
\times
\mathcal E
\]

contains

\[
5\times5=25
\]

registered carrier cells.

All 25 are admissible by construction.

No carrier cell may be removed from the endpoint analysis because it produces an unfavorable result.

No carrier cell may be added after execution.

---

## 7. Exterior sphere-likeness diagnostic

The source says a narrow Dimpled-Sphere can agree with an ordinary sphere over most of the outside.

The present family is not claimed to converge exactly to a unique sphere in the limit \(w\to0\).

Instead, outer sphere-likeness is reported explicitly rather than assumed.

On the exterior meridional half

\[
u\in
\left[
-\frac{\pi}{2},
\frac{\pi}{2}
\right],
\]

define the radial distance from the origin

\[
q_{w,e}(u)
=
\sqrt{
\left(R+a\cos u\right)^2
+
\left(ea\sin u\right)^2
}.
\]

Because the outer equator is normalized to radius \(1\), define

\[
E_{\rm sph}(w,e)
=
\left[
\frac{1}{\pi}
\int_{-\pi/2}^{\pi/2}
\left(
q_{w,e}(u)-1
\right)^2
du
\right]^{1/2}.
\]

This is a descriptive carrier-shape diagnostic.

It is **not** used to exclude cells.

The sweep must report \(E_{\rm sph}\) for all 25 carriers.

No threshold is introduced after endpoint results are known.

---

## 8. Historical angular interval

The historical primary branch remains

\[
\theta
\in
[
1,\,
1+3\pi
].
\]

Thus

\[
L=3\pi
\]

and the total angular span is

\[
540^\circ
=
1.5\text{ turns}.
\]

No truncation sensitivity is included in this checkpoint.

The curve direction remains:

\[
\text{inner}\longrightarrow\text{outer},
\]

corresponding to decreasing \(\theta\).

---

## 9. Registered Variant-B radial laws

All radial laws satisfy

\[
r(1)=1.
\]

### 9.1 Reciprocal FIRST HAND branch

\[
r_R(\theta)
=
\frac{1}{\theta}.
\]

No reciprocal parameter is fitted.

### 9.2 Generic logarithmic family

Let

\[
L=3\pi,
\]

and define the frozen base rate

\[
b_*
=
\frac{\ln(1+3\pi)}{3\pi}.
\]

Use exactly the six previously registered multipliers:

\[
m
\in
\{
0.50,\,
0.75,\,
1.00,\,
1.25,\,
1.50,\,
2.00
\}.
\]

For each,

\[
b_m=mb_*,
\]

and

\[
r_{L,m}(\theta)
=
\exp
\left[
-b_m(\theta-1)
\right].
\]

These rates are held fixed across all 25 carrier shapes.

No new logarithmic rate is introduced.

No rate is optimized.

### 9.3 Golden Mean logarithmic branch

Let

\[
\phi
=
\frac{1+\sqrt5}{2},
\]

and

\[
b_\phi
=
\frac{2\ln\phi}{\pi}.
\]

Then

\[
r_\phi(\theta)
=
\exp
\left[
-b_\phi(\theta-1)
\right].
\]

The Golden Mean branch remains separate from the generic six-point log grid.

---

## 10. Registered inverse-gnomonic radial scale conventions

The same two frozen scale conventions used throughout Variant A are retained only in the spiral-to-meridian map.

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
\tan(0.5).
\]

No third scale is introduced.

The one-radian interpretation remains outside this checkpoint.

---

## 11. Spiral-to-surface mapping

This mapping is frozen before endpoint execution.

For any registered radial law \(r(\theta)\) and scale \(k\), define the normalized inverse-gnomonic radial fraction

\[
s_k(r)
=
\frac{\arctan(kr)}
{\arctan(k)}.
\]

Because all registered curves satisfy \(0<r\le1\),

\[
0<s_k(r)\le1.
\]

Define the carrier meridional coordinate

\[
u_k(\theta)
=
\pi
\left[
1-s_k(r(\theta))
\right].
\]

Define the carrier azimuth

\[
v(\theta)
=
\theta-1.
\]

The Variant-B space curve is

\[
C_{w,e,k,r}(\theta)
=
X_{w,e}
\left(
u_k(\theta),
v(\theta)
\right).
\]

This rule is used identically for:

- reciprocal;
- all six generic logarithmic curves;
- Golden Mean.

No family receives a separately tuned surface map.

---

## 12. Mapping interpretation

At the outer endpoint,

\[
\theta=1,
\qquad
r=1.
\]

Therefore

\[
s_k=1,
\]

\[
u=0,
\]

and

\[
v=0.
\]

Thus every registered curve begins on the normalized outer equator of the carrier.

As \(\theta\) increases inward, each registered radial law decreases.

Therefore

\[
u_k(\theta)
\]

increases monotonically toward

\[
\pi,
\]

moving the vortex from the outer equatorial region over the meridian toward the inner dimple / throat side.

Meanwhile,

\[
v(\theta)
\]

increases by

\[
3\pi,
\]

so the curve completes exactly

\[
1.5
\]

azimuthal turns.

This is the preregistered mathematical representation of the source's limited 1.5-turn three-dimensional form with the outer geometry bending back toward the dimple.

No alternate mapping is allowed after execution.

---

## 13. Analytic mapping derivative

For a registered radial law \(r(\theta)\),

\[
u_k'(\theta)
=
-
\frac{
\pi k r'(\theta)
}{
\left(
1+k^2r(\theta)^2
\right)
\arctan(k)
}.
\]

Because every registered radial law has

\[
r'(\theta)<0,
\]

the meridional derivative satisfies

\[
u_k'(\theta)>0.
\]

Also,

\[
v'(\theta)=1.
\]

The outer-to-inner derivative is

\[
C'(\theta)
=
X_u\,u_k'(\theta)
+
X_v.
\]

The directed inner-to-outer tangent used in the source-primary comparison is

\[
\tau(\theta)
=
-
\frac{C'(\theta)}
{\|C'(\theta)\|}.
\]

No tangent direction may be flipped after execution.

---

## 14. Endpoint definitions

The registered endpoints are exactly:

### Outer

\[
\theta_o=1.
\]

### Inner

\[
\theta_i=1+3\pi.
\]

For every carrier, family, and scale, report:

\[
p_o
=
C(\theta_o),
\]

\[
p_i
=
C(\theta_i),
\]

\[
\tau_o
=
\tau(\theta_o),
\]

\[
\tau_i
=
\tau(\theta_i).
\]

No endpoint is optimized or moved.

---

## 15. Source-primary ambient directed statistic

For every cell, define

\[
d
=
\tau_o\cdot\tau_i,
\]

and

\[
c
=
\|\tau_o\times\tau_i\|.
\]

The directed ambient angle is

\[
\Delta_{\rm amb}^{\rm dir}
=
\operatorname{atan2}(c,d)
\in[0,\pi].
\]

The directed residual is

\[
R_{\rm amb}^{\rm dir}
=
\|\tau_o-\tau_i\|.
\]

Exact directed compatibility requires

\[
\Delta_{\rm amb}^{\rm dir}=0.
\]

The numerical classification tolerance is frozen at

\[
10^{-10}\ {\rm rad}.
\]

---

## 16. Source-primary ambient line statistic

The unoriented line angle is

\[
\Delta_{\rm amb}^{\rm line}
=
\operatorname{atan2}(c,|d|)
\in
\left[
0,\frac{\pi}{2}
\right].
\]

Exact line parallelism requires

\[
\Delta_{\rm amb}^{\rm line}=0
\]

up to the same numerical tolerance

\[
10^{-10}\ {\rm rad}.
\]

Directed and unoriented results must both be reported.

Neither may replace the other after execution.

---

## 17. Registered execution size

The carrier sweep contains:

\[
25
\]

carrier cells.

The spiral set contains:

\[
8
\]

registered branches:

- 1 reciprocal;
- 6 generic logarithmic;
- 1 Golden Mean.

The scale set contains:

\[
2
\]

values.

Therefore the endpoint execution contains exactly

\[
25\times8\times2
=
400
\]

registered geometric cells.

Each cell reports both ambient angle definitions.

No 401st cell may be introduced.

---

## 18. Per-cell states

### Directed

`AMBIENT_DIRECTED_PARALLEL`

if

\[
\Delta_{\rm amb}^{\rm dir}
\le10^{-10}\ {\rm rad}.
\]

Otherwise:

`AMBIENT_DIRECTED_NOT_PARALLEL`.

### Unoriented line

`AMBIENT_LINE_PARALLEL`

if

\[
\Delta_{\rm amb}^{\rm line}
\le10^{-10}\ {\rm rad}.
\]

Otherwise:

`AMBIENT_LINE_NOT_PARALLEL`.

### Technical

If the carrier or mapped curve cannot be evaluated:

`VARIANT_B_TECHNICAL_FAILURE`.

No technical failure may be silently converted to a geometric failure or success.

---

## 19. Reciprocal summary states

For directed semantics:

`RECIPROCAL_DIRECTED_PARALLEL_CELL_FOUND`

if at least one of the 50 reciprocal carrier/scale cells is directed-parallel.

Otherwise:

`NO_REGISTERED_RECIPROCAL_DIRECTED_PARALLEL_CELL`.

For unoriented semantics:

`RECIPROCAL_LINE_PARALLEL_CELL_FOUND`

if at least one reciprocal cell is line-parallel.

Otherwise:

`NO_REGISTERED_RECIPROCAL_LINE_PARALLEL_CELL`.

If technical failures prevent complete evaluation, append an explicit incomplete state rather than treating missing cells as failures.

---

## 20. Logarithmic counterexample summary states

The logarithmic set contains:

\[
7
\]

branches:

- six generic logs;
- Golden Mean.

For directed semantics:

`LOG_DIRECTED_COUNTEREXAMPLE_FOUND`

if any registered logarithmic cell is exactly directed-parallel.

Otherwise:

`NO_REGISTERED_LOG_DIRECTED_COUNTEREXAMPLE`.

For unoriented semantics:

`LOG_LINE_COUNTEREXAMPLE_FOUND`

if any registered logarithmic cell is exactly line-parallel.

Otherwise:

`NO_REGISTERED_LOG_LINE_COUNTEREXAMPLE`.

These are finite-grid statements only.

---

## 21. Descriptive minima

Because exact equality on a finite grid is stringent, the execution must also report descriptive minima without changing the registered success predicate.

For reciprocal, report:

\[
\min
\Delta_{\rm amb}^{\rm dir},
\]

and

\[
\min
\Delta_{\rm amb}^{\rm line},
\]

over all 50 reciprocal cells.

For each generic logarithmic branch and Golden Mean, report the same minima over its 50 carrier/scale cells.

Also report the global logarithmic minima across all 350 log-family cells.

The corresponding fixed-grid argmin identifiers may be reported descriptively.

No interpolation, root finding, or adaptive refinement is allowed in this checkpoint.

---

## 22. No continuous existence claim

The fixed-grid minimum is not a proof of the continuous minimum over

\[
w\in[0.02,0.30]
\]

and

\[
e\in[1.4,2.2].
\]

Therefore wording such as:

> the best possible dimple shape is ...

is prohibited.

Allowed wording is:

> the smallest mismatch among the preregistered grid cells is ...

Any later continuous optimization or root-bracketing requires a separate preregistration.

---

## 23. Carrier-shape stratification

Results may be summarized descriptively by the preregistered throat classes:

- NARROW;
- MODERATE;
- WIDE.

Results may also be summarized by elongation \(e\).

No class boundary may be changed after execution.

The sphere-likeness diagnostic

\[
E_{\rm sph}
\]

may be used to plot or describe how endpoint mismatch varies with carrier resemblance to an ordinary sphere.

It may not be used post hoc to delete cells.

---

## 24. Variant-A references

The completed Variant-A reciprocal ambient values are immutable context:

### G30

\[
\Delta_{\rm amb}^{\rm dir}
=
143.58427150706095^\circ,
\]

\[
\Delta_{\rm amb}^{\rm line}
=
36.415728492939074^\circ.
\]

### GHALF

\[
\Delta_{\rm amb}^{\rm dir}
=
143.29594953287508^\circ,
\]

\[
\Delta_{\rm amb}^{\rm line}
=
36.70405046712493^\circ.
\]

These values must not be recomputed by the Variant-B evaluator.

They may be displayed as fixed external references only.

No Variant-B parameter may be chosen because it minimizes distance from or improvement over these values.

---

## 25. Intrinsic transport is excluded from the primary sweep

No surface parallel transport is used in the 400-cell primary execution.

Therefore the checkpoint is independent of:

- geodesic choice;
- homotopy class;
- holonomy;
- transport-path optimization.

A later intrinsic Variant-B checkpoint, if desired, must preregister its path separately.

The vortex curve itself is a possible future transport path, but is not evaluated here.

---

## 26. Stronger nesting criteria are excluded

This checkpoint does not test:

- local frame matching;
- curvature matching;
- finite-thickness insertion;
- collision clearance;
- global non-intersection between nested copies;
- recursive placement maps;
- similarity self-maps.

Those are independent strengthened nesting conditions introduced by the audit, not Meru-stated requirements.

---

## 27. Implementation-only requirements

Before the 400 registered endpoint cells may be executed, the implementation checkpoint must verify without evaluating registered endpoint pairs:

1. exact carrier grid values;
2. exact 25-cell count;
3. \(R+a=1\);
4. \(R-a=w\);
5. \(\rho(u)>0\) for every registered carrier;
6. analytic regularity of \(X_u\times X_v\);
7. exact spiral branch count \(8\);
8. exact scale count \(2\);
9. exact total execution count \(400\);
10. radial laws match the frozen definitions;
11. \(r(1)=1\) for all curves;
12. \(r'(\theta)<0\) on the registered interval;
13. the mapping satisfies \(u(1)=0\) and \(v(1)=0\);
14. \(v(1+3\pi)=3\pi\);
15. \(u'(\theta)>0\);
16. tangent orientation is inner-to-outer;
17. directed ambient equality / anti-parallel primitive behavior;
18. unoriented line equality / anti-parallel primitive behavior;
19. no parallel-transport routine is imported;
20. no image data are read;
21. no arbitrary \(w,e,k,b\) CLI parameter is accepted;
22. default execution evaluates zero registered endpoint cells.

Primitive tests may evaluate carrier geometry and non-endpoint mapped-curve samples.

They may not evaluate a registered outer/inner endpoint pair.

---

## 28. Required outputs

The registered execution must create at least:

- `variant_b_sweep_results.json`
- `variant_b_sweep_results.csv`
- `variant_b_sweep_report.md`
- `variant_b_carrier_metrics.csv`

For every endpoint cell, record:

- cell ID;
- carrier ID;
- \(w\);
- throat class;
- \(e\);
- \(R\);
- \(a\);
- \(E_{\rm sph}\);
- spiral family;
- spiral ID;
- logarithmic multiplier if applicable;
- \(b\) if applicable;
- scale;
- \(k\);
- \(\theta_o\);
- \(\theta_i\);
- outer and inner radial values;
- outer and inner carrier coordinates \(u,v\);
- outer and inner 3-D positions;
- outer and inner directed tangents;
- dot product \(d\);
- cross norm \(c\);
- directed angle rad/deg;
- directed residual;
- directed state;
- line angle rad/deg;
- line state;
- technical error if any;
- `parallel_transport_used=false`;
- `image_pixel_data_used=false`.

---

## 29. Required report summaries

The Markdown report must include:

1. carrier-family definition;
2. proof that all 25 carriers are embedded genus-1 tori;
3. sphere-likeness range over the registered carriers;
4. reciprocal directed summary;
5. reciprocal line summary;
6. logarithmic directed counterexample summary;
7. logarithmic line counterexample summary;
8. reciprocal fixed-grid minima;
9. per-log-family fixed-grid minima;
10. global logarithmic minima;
11. carrier/scale IDs of descriptive minima;
12. technical-failure count;
13. explicit finite-grid interpretation boundary.

No stronger conclusion may be generated automatically.

---

## 30. Prohibited operations

The following are prohibited in this checkpoint:

- adding carrier parameter values;
- deleting registered carrier cells;
- changing the carrier family;
- changing normalization;
- changing \(w\) after seeing endpoint angles;
- changing \(e\) after seeing endpoint angles;
- changing the spiral-to-surface map;
- changing the historical 1.5-turn interval;
- changing reciprocal radial law;
- adding logarithmic rates;
- optimizing logarithmic rates;
- changing Golden Mean rate;
- adding another projection scale;
- adding AOG-PROSE;
- image fitting;
- endpoint fitting;
- endpoint movement;
- tangent sign flipping;
- post-hoc choice between directed and line semantics;
- parallel transport;
- geodesic optimization;
- homotopy-class optimization;
- interpolation;
- continuous optimization;
- root finding;
- adaptive grid refinement;
- S1.5;
- S2;
- finite insertion tests.

---

## 31. Allowed interpretation if reciprocal succeeds

If at least one registered reciprocal cell satisfies exact ambient parallelism, the allowed conclusion is:

> At least one carrier in the preregistered Variant-B analytic family reproduces Tenen's endpoint-parallelism criterion for the reciprocal FIRST HAND branch under the corresponding ambient definition.

Not allowed:

> The historical Dimpled-Sphere has been recovered.

Not allowed:

> Reciprocal self-embedment is proved universally.

---

## 32. Allowed interpretation if reciprocal does not succeed

If no reciprocal cell satisfies exact parallelism, the allowed conclusion is:

> No exact reciprocal endpoint-parallel cell was found in the preregistered 25-carrier Variant-B family at either registered scale.

The fixed-grid minimum may be reported.

Not allowed:

> No Dimpled-Sphere can make the reciprocal FIRST HAND self-embed.

The family is source-constrained but not unique.

---

## 33. Allowed interpretation if a logarithmic counterexample is found

If any admissible registered logarithmic cell satisfies exact parallelism:

> The preregistered Variant-B family contains a logarithmic counterexample to the source's universal negative endpoint-parallelism claim as operationalized by the corresponding ambient definition.

Before making that statement, the result must be independently verified against:

- carrier admissibility;
- frozen map;
- frozen endpoint interval;
- floating-point identities.

---

## 34. Allowed interpretation if no logarithmic counterexample is found

If all registered logarithmic cells fail:

> No logarithmic endpoint-parallel counterexample was found in the preregistered Variant-B family/grid.

Not allowed:

> Logarithmic self-embedment on every Dimpled-Sphere is impossible.

A finite sweep cannot prove the source's universal statement.

---

## 35. Execution boundary

This preregistration ends before any Variant-B endpoint comparison.

The required order is:

1. commit and push this preregistration;
2. implement the carrier, mapping, registry, and output code;
3. run primitive tests only;
4. commit and push the implementation-only boundary;
5. execute exactly the 400 registered endpoint cells;
6. inspect generated outputs without rerunning;
7. commit generated results separately;
8. write an analytic closeout.

No endpoint result may be previewed between steps 1 and 4.

---

## 36. Closed preregistration statement

The registered Variant-B experiment is:

> **A 25-carrier finite sweep of a normalized elliptic fat-torus Dimpled-Sphere family, crossed with the reciprocal FIRST HAND branch, six fixed generic logarithmic branches, the Golden Mean logarithmic branch, and the two frozen G30/GHALF mapping scales, using exactly the same preregistered 1.5-turn spiral-to-surface rule and both ambient endpoint-parallelism definitions.**

The execution matrix contains exactly:

\[
400
\]

geometric cells.

The family is deliberately simple, explicit, and underclaims historical uniqueness.

Its purpose is to test whether the source's reciprocal positive claim or logarithmic universal negative claim survives a controlled Variant-B carrier sweep without post-hoc shape tuning.
