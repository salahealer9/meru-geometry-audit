# First Hand Variant-B Source Geometry Specification

**Checkpoint:** `first_hand_variant_b_source_geometry_specification_v0.8`  
**Status:** SOURCE-SPECIFICATION BOUNDARY — NO VARIANT-B NUMERICAL EXECUTION  
**Phase:** transition from sealed Variant-A endpoint tests to Variant-B reconstruction  
**Target:** Stan Tenen / Meru FIRST HAND dimpled-sphere construction  
**Supersedes:** the earlier uncommitted draft of the same filename  
**Image fitting in this checkpoint:** none

## 1. Purpose

This document fixes the source-supported scope of the Variant-B stage before any dimpled-sphere metric family is chosen or evaluated.

It incorporates the source clarification established after the Variant-A S1 and ambient-parallelism checkpoints:

1. Tenen explicitly makes endpoint parallelism a self-embedment criterion.
2. Tenen explicitly distinguishes self-embedment from self-similarity.
3. The negative logarithmic claim is stated for both an ordinary sphere and a Dimpled-Sphere.
4. The positive FIRST HAND self-embedment statement is not restricted to only one carrier in the relevant comparison passage.
5. Elsewhere, the specially shaped 1.5-turn FIRST HAND vortex is repeatedly associated with a dimpled-sphere torus.
6. The source claims logarithmic failure persists despite changes to Dimpled-Sphere shape.
7. No unique published metric equation for the Dimpled-Sphere carrier has been identified.
8. The published `10_3.wrl` asset is a 3,10 torus-knot model, not an explicit standalone carrier-surface mesh.

The purpose of the next stage is therefore not to select one convenient torus and call it "the" Meru geometry.

The next stage must preregister a **source-constrained swept Variant-B surface family**.

---

## 2. Primary source basis

### 2.1 Logarithmic / Golden Mean comparison

Stan Tenen, *Notes on Logarithmic and Golden Mean Spirals*:

`https://www.meru.org/coast/goldmean.html`

The source states that logarithmic spirals self-embed in two dimensions because they are self-similar.

It then states that when a logarithmic spiral is projected onto either:

- a sphere; or
- a Dimpled-Sphere,

it cannot self-embed because the outer part of the vortex cannot be parallel to the inner tip and the ends cannot line up.

The same page states that the specially shaped FIRST HAND vortices self-embed because their outer ends and inner tips are parallel.

The page also states that these FIRST HAND vortices are not self-similar.

### 2.2 Dimple-width and shape claims

The same Golden Mean page states that the displayed logarithmic spirals use Dimpled-Spheres with small, narrow holes so that most of the outside agrees with an ordinary sphere.

It further states:

- a wider hole makes the spiral twist deeper into the dimple;
- a narrower hole keeps the twist nearer the top;
- elongating the Dimpled-Sphere changes the outer end somewhat;
- nevertheless, the logarithmic vortex allegedly never self-embeds regardless of how the Dimpled-Sphere shape is changed.

This is a source-level shape-sensitivity claim.

### 2.3 Limited 1.5-turn 3-D form

Stan Tenen, *Some Notes on the Logarithmic and Golden Mean Spirals: Addendum*:

`https://meru.org/goldenrules/gmaddend.html`

The source distinguishes the Golden Mean spiral from Tenen's sculpture and describes the latter as:

- three-dimensional;
- limited to 1.5 turns;
- having the outer turns bent back.

Thus the finite 1.5-turn geometry is part of the historical FIRST HAND construction, not an arbitrary audit truncation.

### 2.4 Most asymmetric spiral

Stan Tenen, *The First Distinction and the Most Asymmetric Spiral*:

`https://www.meru.org/3220lecture/asymspir.html`

The source motivates the reciprocal / hyperbolic spiral as the asymmetric complement of the tetrahedron and explicitly contrasts it with the scale self-similarity of logarithmic spirals.

### 2.5 Dimpled-sphere torus and 3,10 knot

Stan Tenen, *The 3,10 Torus Knot, Ring, Sphere, Tetrahelix and Hand*:

`https://www.meru.org/Posters/trsknotrngsphere.html`

The source states that the standard ring form of the 3,10 torus knot can be transformed to fit on the surface of a dimpled-sphere torus.

This wording distinguishes:

- the 3,10 knot itself; and
- the dimpled-sphere carrier surface.

### 2.6 VRML inventory

Meru Foundation, *VRMLs: Virtual Reality Simulations*:

`https://www.meru.org/compuimages/animations.html`

The page lists two VRML models:

- `3_1-1_3B.wrl` — intertwined vortices;
- `10_3.wrl` — 3,10 torus knot.

No separate explicit Dimpled-Sphere carrier-surface VRML is listed there.

### 2.7 Scientific Abstract

Stan Tenen, *Scientific Abstract of the Meru*:

`https://www.meru.org/abstract.html`

The source describes the "apple" as a torus in dimpled-sphere form and describes a 1.5-turn spiral path associated with the hand model.

---

## 3. Self-embedment is not self-similarity

The source explicitly distinguishes these concepts.

A logarithmic spiral is described as self-similar.

The FIRST HAND vortex is described as self-embedding but not self-similar.

Therefore:

> **A global similarity self-map is not the Meru-stated self-embedment criterion.**

A future similarity-map test could be introduced as an independent mathematical property, but it must not be presented as Tenen's own criterion.

The source-primary criterion is endpoint parallelism.

---

## 4. Variant-A scope is source-supported

The ordinary sphere is explicitly named in the source's negative logarithmic claim.

Therefore the completed Variant-A spherical analysis was not merely an external control construction.

It directly addressed one of the carrier types named by Tenen.

The sealed Variant-A results now show that, on the registered 1.5-turn reciprocal construction:

- directed intrinsic endpoint parallelism fails;
- directed ambient endpoint parallelism fails;
- unoriented ambient tangent-line parallelism fails.

The Variant-A stage therefore remains source-relevant.

Variant B is a further source-supported carrier geometry, not a replacement that invalidates Variant A.

---

## 5. Positive FIRST HAND claim and carrier scope

In the Golden Mean comparison passage, the positive statement that FIRST HAND vortices self-embed because their outer ends and inner tips are parallel is not explicitly restricted to one carrier surface.

However, other Meru material repeatedly associates the specially shaped 1.5-turn FIRST HAND vortex with a dimpled-sphere torus.

Therefore the audit must maintain two statements simultaneously:

1. Variant A was legitimately in scope for the source comparison.
2. Variant B remains essential because the characteristic FIRST HAND construction is repeatedly presented on a dimpled-sphere torus.

The audit must not retroactively declare Variant A "out of scope" merely because it failed.

---

## 6. Source-primary mathematical criterion for Variant B

The primary Variant-B self-embedment statistic should be **ambient endpoint parallelism**.

For unit endpoint tangents \(\tau_o,\tau_i\in\mathbb R^3\), preregister both:

### Directed ambient angle

\[
\Delta_{\rm amb}^{\rm dir}
=
\operatorname{atan2}
\left(
\|\tau_o\times\tau_i\|,
\tau_o\cdot\tau_i
\right).
\]

### Unoriented ambient line angle

\[
\Delta_{\rm amb}^{\rm line}
=
\operatorname{atan2}
\left(
\|\tau_o\times\tau_i\|,
|\tau_o\cdot\tau_i|
\right).
\]

These are source-primary because they directly operationalize the word "parallel" without requiring an additional path on the carrier surface.

Both definitions must be retained because the source does not formally resolve directed-vector versus tangent-line semantics.

---

## 7. Why intrinsic transport is secondary on Variant B

On the genus-1 dimpled-sphere carrier, tangent vectors at different points cannot be identified intrinsically without a chosen path.

Unlike the ordinary sphere's shorter-geodesic convention used in S1, a toroidal surface admits multiple homotopy classes between generic endpoints.

Parallel transport may differ between those classes through holonomy.

Therefore an intrinsic Variant-B endpoint statistic is not path-free.

If intrinsic transport is studied later, its path must be preregistered.

Possible admissible designs include:

1. transport along the vortex curve itself;
2. transport along a geodesic in an explicitly specified homotopy class;
3. a finite preregistered set of homotopy classes reported separately.

No intrinsic path may be chosen after seeing which one best aligns the endpoints.

A failure state must exist for path/class dependence if more than one class is registered.

Intrinsic transport is a secondary audit diagnostic, not the source-primary Variant-B criterion.

---

## 8. The `10_3.wrl` distinction

The previous Meru audit established a genus-1 result for the `10_3.wrl` asset.

That result concerns the geometry/topology of the published 3,10 knot model.

It must not be cited as if `10_3.wrl` were an independently published metric mesh of the Dimpled-Sphere carrier.

The Meru VRML inventory identifies `10_3.wrl` as:

> the 3,10 torus knot.

The 1992/1996 poster separately says that the ring form of that knot is transformed to fit on the **surface of a dimpled-sphere torus**.

Therefore:

> **knot model and carrier surface are distinct objects in the source description.**

The Variant-B carrier must be constructed explicitly by the audit unless an independent source asset for that carrier is found.

---

## 9. Metric underdetermination

The currently reviewed source material does not uniquely specify a metric equation for the Dimpled-Sphere.

In particular, it does not uniquely fix:

- a meridian profile;
- throat radius;
- throat depth;
- outer radius;
- dimple curvature;
- axial elongation;
- transition smoothness between outer sphere-like region and throat;
- a unique embedding map from the planar reciprocal spiral to the carrier;
- a unique correspondence between dimple width and vortex depth.

Thus Variant B is:

> **topologically and morphologically constrained, but metrically underdetermined.**

This must be exposed explicitly in the audit.

---

## 10. Source-constrained carrier requirements

Any admissible Variant-B surface family must satisfy all of the following.

### B01 — Genus

The carrier must be a torus:

\[
g=1.
\]

### B02 — Dimpled-sphere morphology

The carrier must have:

- a sphere-like exterior;
- a central dimple / throat;
- a continuous toroidal passage.

A generic thin ring torus is not automatically source-equivalent.

### B03 — Axis and symmetry declaration

If an axisymmetric family is chosen, that assumption must be stated as an audit reconstruction choice unless directly sourced.

No symmetry may be smuggled in as historical fact.

### B04 — Narrow-dimple exterior agreement

The family must possess a regime in which narrowing the dimple makes most of the outer surface approach an ordinary sphere, consistent with the source description.

### B05 — Dimple-width control

At least one explicit parameter must control hole / throat width.

### B06 — Depth or elongation control

Because the source discusses wider holes, deeper twisting, and elongated Dimpled-Sphere shapes, the preregistration should include at least one independent depth/elongation parameter unless a single parameter analytically controls both.

### B07 — Smoothness

The surface family must have enough regularity to define endpoint tangents and local surface geometry everywhere used by the vortex.

### B08 — Nondegeneracy

Parameter combinations that pinch the throat, self-intersect the carrier, destroy genus 1, or create undefined tangent geometry must be classified as inadmissible before endpoint results are evaluated.

---

## 11. The next checkpoint must be a sweep, not a selected fit

The source makes a broad negative statement about logarithmic vortices:

> changing the Dimpled-Sphere shape does not make the outer end parallel to the inner tip.

Therefore selecting one dimple shape would test only one example and would undersample the source's own claim.

The next preregistration should define a **finite, explicit, source-constrained parameter grid** over the admissible carrier family.

The grid must be frozen before any endpoint angle is evaluated.

No adaptive refinement is allowed in the confirmatory sweep.

No parameter point may be added because it appears likely to improve endpoint alignment.

---

## 12. What a finite sweep can and cannot establish

A finite numerical sweep cannot prove a universal mathematical claim over all possible Dimpled-Sphere geometries.

Therefore:

### If every registered logarithmic cell fails

Allowed conclusion:

> No endpoint-parallel logarithmic case was found in the preregistered Variant-B family/grid.

Not allowed:

> Logarithmic spirals can never self-embed on any Dimpled-Sphere.

### If one admissible logarithmic cell succeeds

Then, within the registered mathematical family, that cell is a counterexample to the corresponding universal claim as operationalized.

Before treating it as historically decisive, the audit must still verify that:

- the carrier satisfies every preregistered source constraint;
- no post-hoc parameter tuning occurred;
- the spiral mapping rule remained frozen;
- the success is not a numerical degeneracy.

---

## 13. Reciprocal positive claim and logarithmic negative claim should be tested together

The Variant-B sweep should include at least two source-relevant spiral branches under the same carrier family and mapping rule:

1. reciprocal / hyperbolic FIRST HAND candidate;
2. logarithmic comparator family.

This permits simultaneous testing of:

### Positive source claim

The FIRST HAND reciprocal construction can satisfy endpoint parallelism.

### Negative source claim

Logarithmic constructions cannot satisfy endpoint parallelism despite changes to Dimpled-Sphere shape.

The same surface family, parameter grid, endpoint definitions, and ambient statistics must be used for both.

---

## 14. Logarithmic family design

The exact logarithmic family for Variant B must be frozen before execution.

The completed Variant-A comparator checkpoint already contains a source-relevant finite logarithmic grid.

Reusing that frozen grid is preferable to inventing new rates post hoc, unless the new preregistration supplies an independent reason for a different set.

The Golden Mean logarithmic branch should remain separately identified.

No continuous optimization over logarithmic growth rate should occur in the confirmatory Variant-B sweep.

---

## 15. Reciprocal branch design

The reciprocal / hyperbolic law must remain source-fixed.

The historical 1.5-turn span must remain the primary Variant-B branch.

No radial-law fitting to endpoint parallelism is allowed.

No endpoint may be moved to force alignment.

Any alternative truncation belongs to a later sensitivity checkpoint and must not be mixed into the primary Variant-B sweep.

---

## 16. Spiral-to-surface mapping is a critical preregistration choice

A Dimpled-Sphere surface family alone does not uniquely determine the vortex.

The next preregistration must provide an explicit map from the spiral parameter to the surface.

It must state how:

- angular progress around the carrier is defined;
- radial or meridional spiral progress maps to the surface profile;
- the inner tip is placed in the dimple/throat region;
- the outer end is placed on the sphere-like exterior;
- the 1.5-turn count is measured.

The mapping rule must be frozen before any endpoint angle is evaluated.

No remapping may be introduced after seeing results.

---

## 17. Historical "outer turns bent back" constraint

The Meru addendum describes the original sculpture as a limited 1.5-turn 3-D form with the outer turns bent back.

Therefore the next preregistration should state explicitly how the chosen surface mapping represents or fails to represent this feature.

A mapping in which the outer turn simply behaves like an unmodified planar radial spiral projected trivially onto a torus may not capture the source morphology.

This constraint should be operationalized geometrically before execution, not explained after the results.

---

## 18. Source drawings and image evidence

Image evidence may be used only under an explicit calibration protocol.

The previous decision to stop fitting the freehand page-7 spiral remains unchanged.

If source images are used to constrain Variant-B carrier morphology, the preregistration must distinguish:

- topology-level evidence;
- clean geometric boundaries;
- freehand illustrative lines;
- qualitative shape description;
- metric parameter extraction.

No dimple width, depth, or elongation may be chosen by eyeballing the endpoint-angle result.

---

## 19. Recommended finite carrier axes

The next preregistration should consider, but need not yet adopt, a parameterization containing at least:

\[
w
=
\text{dimensionless dimple/throat width},
\]

and

\[
e
=
\text{dimensionless axial depth or elongation}.
\]

A third parameter may be justified if required to control transition curvature independently.

Before execution the preregistration must define:

- exact mathematical meaning of each parameter;
- admissible intervals;
- finite registered grid values;
- topology/nonintersection constraints;
- normalization convention.

This document does not yet freeze numerical grid values.

---

## 20. Primary Variant-B outcome hierarchy

For every admissible carrier/spiral cell, report:

### Source-primary directed state

`AMBIENT_DIRECTED_PARALLEL`

or

`AMBIENT_DIRECTED_NOT_PARALLEL`.

### Source-primary unoriented-line state

`AMBIENT_LINE_PARALLEL`

or

`AMBIENT_LINE_NOT_PARALLEL`.

### Technical carrier state

Examples:

- `CARRIER_ADMISSIBLE`;
- `CARRIER_SELF_INTERSECTION`;
- `CARRIER_THROAT_DEGENERATE`;
- `VORTEX_MAPPING_UNDEFINED`;
- `ENDPOINT_TANGENT_UNDEFINED`.

Exact names must be frozen in the next preregistration.

---

## 21. Independent stronger nesting tests

The following are scientifically interesting but are not Meru-stated requirements:

- local frame matching;
- curvature matching;
- finite-thickness insertion;
- collision clearance;
- non-intersection;
- recursive placement maps;
- global similarity.

Any future checkpoint using them must be labeled:

> **Independent strengthened nesting criterion; not a Meru-stated requirement.**

These tests must not be allowed to replace or obscure the source-primary endpoint-parallelism result.

---

## 22. No post-hoc repair rule

Before Variant-B execution, the following must be prohibited unless explicitly preregistered:

- choosing dimple width to make reciprocal endpoints parallel;
- choosing elongation to improve a preferred family;
- changing the carrier family after seeing endpoint angles;
- changing the spiral-to-surface map after seeing endpoint angles;
- moving inner or outer endpoints;
- changing the 1.5-turn span;
- changing the reciprocal law;
- optimizing logarithmic rate;
- switching between directed and unoriented semantics after execution;
- choosing an intrinsic transport path because it gives a favorable answer;
- introducing source-image measurements after previewing the sweep;
- treating an inadmissible/self-intersecting carrier as a valid counterexample.

---

## 23. Required next preregistration components

The next document should be:

`first_hand_variant_b_swept_family_preregistration_v0.8.md`

It must freeze:

1. explicit analytic dimpled-sphere carrier family;
2. topology and nonintersection proof/conditions;
3. normalization;
4. width/depth/elongation parameters;
5. exact finite parameter grid;
6. narrow-dimple interpretation;
7. exact 1.5-turn reciprocal-to-surface map;
8. exact logarithmic-to-surface map under the same conventions;
9. Golden Mean branch if retained;
10. endpoint definitions;
11. ambient directed statistic;
12. ambient unoriented statistic;
13. numerical tolerance;
14. technical failure states;
15. no-adaptive-refinement rule;
16. optional secondary intrinsic path definition, if any;
17. required outputs;
18. allowed and prohibited interpretation language.

No Variant-B endpoint angle may be previewed before that preregistration is committed and pushed.

---

## 24. Revised source conclusion

The source-supported Variant-B target is:

> **A limited 1.5-turn three-dimensional FIRST HAND vortex associated with a dimpled-sphere torus, for which self-embedment is claimed on the basis that the outer end and inner tip are parallel.**

The source also makes a broad negative claim that logarithmic vortices fail this endpoint-parallelism condition even when the Dimpled-Sphere shape is changed.

Because no unique published metric carrier has been identified, the audit must test these statements over a preregistered source-constrained family rather than a hand-selected surface.

---

## 25. Phase status

The audit now stands at:

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
\boxed{\text{revised Variant-B source geometry specification}}
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
\text{implementation-only freeze}
\]

\[
\downarrow
\]

\[
\text{registered Variant-B sweep}
\]

No Variant-B numerical result is authorized by this source-specification document.
