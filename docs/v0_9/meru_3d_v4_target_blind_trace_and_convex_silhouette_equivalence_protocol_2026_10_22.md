# Meru v0.9 — 3D-V4 Target-Blind Exact Traced-Polyline and Convex-Silhouette Equivalence Microstudy

**Date:** 22 October 2026  
**Status:** DRAFT FOR HUMAN REVIEW — NOT SIGNED; NO 3D-V4 EXPERIMENT EXECUTED  
**Repository:** `salahealer9/meru-geometry-audit`  
**Branch:** `hebrew-projection-capacity-v0.9`  
**Required direct parent if signed next:** `e2bad59a282b30ddd1f96ba213a449d02b2174e3` (human-signed 3D-V3 results freeze)  
**Expected human GPG fingerprint:** `D4EC014EEFCC90E619D2AA59A91239ABCF512130`

## 1. Scientific question and narrow scope

For the **same six target-blind finite orthographic camera grids** A/B × G0/G1/G2, how many distinct **unparameterised polygonal traces** and how many distinct **filled orthographic silhouettes of convex solids** remain after planar translation plus `SO(2)` or `O(2)` congruence? Unlike 3D-V3's fixed labelled point correspondence, V4 permits intrinsic polyline simplification, path reversal, cyclic starting-point choice for loops, and arbitrary polygon-corner correspondence consistent with a boundary cycle. It thereby measures two concrete kinds of unlabelled projected *geometry*, not merely landmark-label diversity.

**Distinct mathematical observables (never pool their counts):**

- **TR (traced polyline):** the *continuous piecewise-linear map up to monotone reparametrisation*, with an unmarked starting endpoint (so reversal is permitted). Subdivision of a straight segment is immaterial. Repeated traversals, retracing, intersections, and visit order **remain observable**. Thus `TR` is **not** equality of the bare occupied point set. For closed traces, cyclic changes of starting point are permitted.
- **CS (convex-solid silhouette):** the **filled planar convex hull** of an orthographic projection of an opaque 3D convex polytope. Its boundary is the geometrically determined cyclic sequence of extreme corners, independent of source vertex labels or hidden faces. Translation and planar congruence are allowed, but scale, shear and arbitrary image deformation are not. Because the solids are convex, this is a genuine binary orthographic silhouette without a visibility/occlusion ambiguity. It is **not** a physical cast shadow with finite illumination, nor a silhouette of a nonconvex wire.

These modalities may be compared qualitatively, but trace-class counts and filled-silhouette class counts measure different objects. No historical Meru source figure, 3D candidate, Hebrew letters, fonts, alphabet proxies, source drawing pixels, fitting, matching to targets, altered camera grids, learned parameters, raster similarity or Monte Carlo decision rule is admitted. No claims about first-hand historical construction, glyph specificity or physical optics follow from V4.

**Frozen predecessors:** the signed V1/V2/V3 protocols and result freezes; `docs/geometry/projection_orbit_results_v0_5.md`; `reports/v0_9/p0a2_target_blind_design/direction_family_candidates.md`. V3's labelled counts are a methodological comparator, **not V4's oracle**.

## 2. Exactly frozen cameras and transformations

Use the already signed primitive integer triples, with exact normalisation `n=t/√(t·t)`:

`A0`: six signed axes; `C`: eight `(±1,±1,±1)` corners; `E`: twelve signed permutations of `(1,1,0)`; `T`: 24 signed permutations of `(2,1,0)`. Family A: `A0`, `A0∪C`, `A0∪C∪E`; family B: `A0`, `A0∪E`, `A0∪E∪T`. Append strata in that order, each sorted lexicographically by integer triples. Expected signed camera counts: `6/14/26` and `6/18/42`; axis counts `3/7/13` and `3/9/21`. The G0 camera lists **and outputs** must coincide across families. `n` and `−n` must have matching O2 silhouettes and O2 traces whenever both are evaluable.

Orthographic projection along `n` is characterised exactly by the bilinear form

`B_n(U,V) = U·V − ((t·U)(t·V))/(t·t)`

and its oriented two-dimensional determinant

`D_n(U,V) = (t·(U×V))/√(t·t)`.

`B_n` is rational for rational input vectors. For comparing oriented determinants, represent them exactly as `(signed rational numerator, positive integer squared denominator)` and test equality by sign plus equality of squared values; do not compare radicals using floating-point approximations. A proper camera frame with its viewing normal as third row realises `D_n` with the stated orientation. The invariants remove all dependence on a chosen camera roll or seam.

Allow **one common planar translation** and then `SO(2)` or `O(2)` only. Never fit uniform scale, reflect in SO2, add pointwise correspondence flexibility beyond the intrinsic polyline/polygon rules, permit source vertex relabelling on a trace, or delete cameras conditionally to increase diversity. Only exactly collapsed TR outputs may be `NOT_EVALUABLE`; report them explicitly.

## 3. Frozen controls (integer coordinates, no later redesign)

The following points are given in a single fixed Cartesian laboratory frame. Vertices are *input definitions*, not target-landmark labels in output comparisons.

| ID | Observable | Frozen geometric definition | Purpose |
|---|---|---|---|
| `TR-L` | Open traced polyline | `(0,0,0) → (1,0,0) → (3,0,0)` | Redundant straight-line negative control; subdivision must disappear; `±e_x` exactly collapse |
| `TR-S` | Open traced polyline | `(0,0,0) → (1,2,3) → (3,5,4) → (5,6,8) → (8,9,10)` | Asymmetric spatial bend pattern, with path reversal but without landmark labels |
| `TR-C` | Closed traced polyline | `(0,0,0) → (3,0,0) → (4,2,1) → (1,4,3) → (−1,2,1) → (0,0,0)` | Closed spatial loop; cyclic starting point and traversal reversal |
| `CS-T` | Filled convex-solid silhouette | Convex hull of `{(0,0,0),(1,0,0),(0,2,0),(0,0,3)}` | Asymmetric full-dimensional tetrahedral solid; boundary corners need not preserve 3D labels |
| `CS-B` | Filled convex-solid silhouette | Axis-aligned rectangular box `[0,1]×[0,2]×[0,3]` (all eight corner vertices) | Full-dimensional symmetric negative control, testing camera redundancy |

The two 3D solids have positive volume and every orthographic projection is two-dimensional. `TR-L` has rank zero **only** for `±e_x`; these two cameras must be marked `NOT_EVALUABLE` at every tier and excluded from trace equivalence classes. In both other TR controls, a rank-zero projection, if detected, is also explicitly `NOT_EVALUABLE`, never silently discarded. Any projected rank-one *nonzero* trace remains evaluable and must be rank-labelled. Self-intersection and edge-on views do not automatically invalidate a trace or a convex silhouette.

## 4. Exact canonicalisation of unparameterised TR traces

For each camera, project the *ordered full continuous polyline*. Use the following finite, exact reduction to remove parametrisation artefacts:

1. Remove every **zero-length projected edge** (successive coincident projected vertices, decided by `B_n(Δ,Δ)=0`). On an open trace retain endpoints of the remaining path; on a closed trace perform the analogous cyclic reduction.
2. Remove intermediate vertices lying on the **same forward-directed projected segment**: adjacent nonzero edge vectors `u,v` are positively collinear iff `D_n(u,v)=0` **and** `B_n(u,v)>0`. Merge them, including cyclic runs for a closed trace, until stable. Do **not** remove an opposite-directed collinear turn (`B_n(u,v)<0`), since that represents retracing. Never collapse a nontrivial closed back-and-forth trace into an empty object.
3. Flag `NOT_EVALUABLE` iff the *entire* projected trace has zero geometric extent. Otherwise retain the resulting reduced trace with ordered breakpoints; classify its projection rank exactly as `0/1/2` using the complete Gram matrix.
4. Two reduced open traces are equivalent iff their ordered vertices, **in forward or reversed order**, are congruent by the permitted planar group. For closed traces, also permit **every cyclic starting-vertex shift** in either traversal direction. Number of reduced corners must agree (including the identical two-endpoint straight segment case). Do **not** permit arbitrary vertex permutations, detours, edge retraversals, point-set matching or changing multiplicity.

For an ordered candidate correspondence, centre that view's reduced vertices at their own arithmetic mean; compute the complete labelled `B_n` Gram matrix of centred vertex differences. Gram equality is necessary and sufficient for `O(2)` congruence. For `SO(2)`, require **all** centred pairwise `D_n` oriented minors equal as well. Proper planar rank-one congruences have zero minors and require no artificial orientation sign. These are exact equality tests, not optimisation or near-equality thresholds.

**Scope qualification:** `TR` recognises continuous PL paths modulo monotone reparametrisation (including reversal and loop cyclic origin); it does **not** assert equality of unparameterised point *sets* for arbitrarily overlapped/self-intersecting curves. A later, separate image-set/occlusion study would require its own equivalence definition.

## 5. Exact construction and equivalence of CS silhouettes

For each fixed convex 3D solid and signed direction:

1. Project all fixed 3D extreme input points. Merge points whose **projected squared distance is exactly zero** under `B_n`; tie-break only for internal deterministic indexing, never as a visible source label.
2. Build the **entire filled two-dimensional convex hull** and its ordered *strict extreme corners*. The oriented side test for three projected points `(i,j,k)` is `sign(t·((X_j−X_i)×(X_k−X_i)))`, independent of the positive camera normaliser. Points lying strictly within a straight hull edge are excluded as corners. Use exact side and projected dot comparisons, or an equivalent exact finite hull algorithm, to certify no extreme corner was omitted and no collinear interior point was retained. Distinctness uses only `B_n`.
3. Verify nonzero planar area and a coherent counterclockwise (`D_n>0`) cyclic hull order. For each view, record input-point count, projected-distinct count, strict hull-corner count, projected rank 2 and, optionally, rational Gram / oriented-minor signatures. Original 3D vertex identities must **not** constrain polygon matching.
4. Two filled polygons are congruent after translation iff there is a correspondence between all their strict extreme corners preserving their boundary cycle, with identical complete centred Gram matrices for O2; and identical Gram **plus oriented minors** for SO2. With counterclockwise representations, SO2 requires **cyclic shifts** of one hull cycle; O2 also permits **cycle reversal**. No other permutations, scale factors, image warps, arbitrary vertex matches or sampling/raster approximations are permitted.

The filled convex hull and its strict corners uniquely determine the projected silhouette, so these equalities are complete for the chosen `CS` contract. This certificate does *not* extend automatically to occluding/nonconvex wire geometries or finite-light physical shadows.

## 6. Locked pre-execution mathematical obligations and limited oracles

**This protocol deliberately preregisters the finite exact question, controls, algorithms and acceptance rules without guessing exploratory higher-tier class counts.** Unpredicted counts are measurements to be independently certified, not hypotheses to tune after seeing outputs. Specific exact pre-run oracles and consistency laws are:

- **Same grids:** `|G_A0|=|G_B0|=6`; `(14,26)` for A G1/G2 and `(18,42)` for B G1/G2; all sets antipodally closed; all canonical G0 results identical across families, including every camera's TR reduction, silhouette hull, equivalence matrix and partition.
- **Line negative control:** `TR-L` has exactly two `NOT_EVALUABLE` directions, `±e_x`, per tier, and all other views rank one. The **SO2/O2 class counts** are `A G0=B G0: 1/1`, `A G1: 2/2`, `A G2: 3/3`, `B G1: 2/2`, `B G2: 4/4`, determined by the distinct positive values of `1−n_x²`. Its intermediate source point is not a retained geometric kink except in a collapsed camera.
- **G0 convex silhouettes:** `CS-T` has **SO2/O2 = 6/3** at G0 because its three opposite axis-view pairs produce scalene right-triangle silhouettes with leg pairs `(2,3)`, `(1,3)`, `(1,2)`; opposite viewing senses are mirror rather than proper-congruent for these triangles. `CS-B` has **SO2/O2 = 3/3** at G0 because its opposite axis projections yield congruent rectangular silhouettes with distinct side-pairs `(2,3)`, `(1,3)`, `(1,2)`.
- **Every evaluable object/tier:** exact equivalence matrices reflexive, symmetric and transitive on the evaluable domain; `SO2` classes refine `O2` classes (not vice versa); antipodes are O2 equivalent; within the same fixed observable, group and family, nested tiers cannot *reduce* the number of distinct classes (equivalence rule and evaluability do not change).
- **Ranks and accounting:** class-size sums equal the exact number of evaluable cameras; null matrix entries are permitted **only** for NOT_EVALUABLE views. All silhouettes must have strictly positive 2D area; no suppressed degenerate/edge-on TR projection; signs and radical equality must be exact. Complete per-camera reductions/hulls, partitions and pairwise matrices must be preserved for the independent review.

The complete **higher-tier `TR-S`, `TR-C`, `CS-T`, `CS-B` counts, class-size multisets and camera memberships are intentionally `TO_BE_DETERMINED` by the registered exact run**. They are *not* preregistered predicted observations. This is an exact finite census with explicit internal falsification checks, not a statistical specificity test; the lack of a predicted higher-tier count must not be disguised as evidence of a pre-run discovery.

## 7. One bounded registered execution and fail-closed review

1. **Human review, then signing first:** sign this exact Markdown file in **one new additive commit**, with exact direct parent `e2bad59a282b30ddd1f96ba213a449d02b2174e3` and correct human GPG key; push feature branch. The textual DRAFT header is archival after signing. No V4 scientific code must run as part of this preregistration.
2. **Standalone implementation:** one modest Python 3.11 standard-library (preferably `fractions.Fraction`) calculator **outside the repo**, using only exact invariant decisions. It must cover 6 family/tier records × 5 frozen controls, emit camera lists, geometry simplifications/hulls, complete SO2/O2 pair matrices, partitions, sizes, rank/evaluability, diagnostic oracle decisions, and provenance. No archived Meru/V1/V2/V3 calculator imports. If the exact radical-comparison routine or hull/canonicalisation encounters an undecidable or inconsistent case, mark `INCOMPLETE` and preserve it; do not use decimals as a fallback.
3. **Frozen source and first run:** inspect the exact script and record SHA-256, Python version and command **before** the human approves a single execution. Preserve the full script, signed commit and Git blob, start/end UTC, stdout JSON, stderr, exit code and checksums in immutable `run_01`. Do not overwrite it or silently rerun after any failure; repairs require a separate named attempt with preserved original evidence.
4. **Independent, non-importing review:** reconstruct all 30 observable/grid records independently from the fixed coordinates, with full camera-pair matrices, exact camera-hull/trace data, class memberships, witness transformations (where useful), degeneracy treatment and complete-sufficiency arguments. Verify the stipulated G0 and line oracles *and* all discovered higher-tier results, using a separately written approach or proofs. Merely rerunning the original calculator is insufficient.
5. **Decision:** `MERU_3D_V4_EXACT_TRACE_AND_CONVEX_SILHOUETTE_EQUIVALENCE_PASS` only when the first-run evidence is intact, all frozen oracles hold, all determined class partitions/geometry compare exactly to the independent reconstruction, and every mathematical completeness obligation is discharged. Otherwise record `MERU_3D_V4_INCOMPLETE_OR_FAILED` with unchanged evidence and a precise discrepancy list. Do not update or reinterpret frozen scientific results to repair a mismatch.

## 8. Interpretation and future target gate

V4 extends V3 from labelled fixed-point configurations to **path-order-aware continuous PL traces** and **filled silhouettes of simple opaque convex solids**. It is not a certification of unlabelled general 3D wire shape, nonconvex occluded silhouettes, reciprocal-torus source candidate C0, handwriting/letter matching, or physical projected shadows.

Only after a successful signed V4 result freeze should the next protocol consider **source-justified candidate wire/curve geometry and independent null families** under a newly fixed interpretation of image-set equivalence, occlusion/collapse, admissible operations and model complexity. First-hand Meru source reconstruction remains a separate unresolved gate; Hebrew targets remain excluded until a later explicitly signed target-use protocol. A high or low projected-shape count alone is not evidence of intent or correspondence specificity.
