# Meru v0.9 — 3D-V3 Target-Blind Labelled-Projection Equivalence Microstudy

**Date:** 22 October 2026  
**Status:** DRAFT FOR HUMAN REVIEW — NOT SIGNED; NO 3D-V3 EXPERIMENT EXECUTED  
**Repository:** `salahealer9/meru-geometry-audit`  
**Branch:** `hebrew-projection-capacity-v0.9`  
**Required direct parent if signed next:** `6d1761f059de42ae1e5935eabacc495c80e83e72` (signed Meru 3D-V2 result freeze)  
**Expected GPG fingerprint:** `D4EC014EEFCC90E619D2AA59A91239ABCF512130`

## 1. Scientific question and scope

**Question.** For exactly the six already frozen finite-camera grids (A and B at G0/G1/G2), how many **label-preserving** planar orthographic projections of simple preregistered 3D landmark controls are genuinely distinct, (i) modulo proper planar `SO(2)` rotations and (ii) modulo all planar `O(2)` orthogonal transformations?

This is a deliberately small **object-specific diagnostic for labelled point configurations**, not a silhouette, glyph, tracing, curve-reparametrization, historical Meru or Hebrew-letter experiment. The two G0 camera sets are mathematically identical and constitute a mandatory cross-family reproducibility check. We shall not claim that landmark-class counts imply image, silhouette or unlabelled-shape counts.

**Frozen mathematical sources:** `docs/geometry/projection_orbit_results_v0_5.md`, `reports/v0_9/p0a2_target_blind_design/direction_family_candidates.md`, the signed 3D-V1 and 3D-V2 protocols and result-freeze commits. The historical v0.8 first-hand construction remains unresolved. V1 establishes direction distinctness; V2 establishes spherical covering radii; neither proves object-specific shape distinctness.

**Excluded:** Hebrew glyphs, proxy alphabets/fonts, chart pixel coordinates, source-derived target shapes, object-specific target fitting, image renders, silhouettes, 3D Meru candidate reconstructions, shadows with illumination, alternate camera models, parameter optimization, tolerance clustering, matching or reordering labelled points, curve cyclic shifts or reversal, vertex relabelling, reflection unless explicitly in `O(2)`, scaling, translations beyond fixed centring, statistical significance assertions and claims of source fidelity. All source-target comparisons require a later separate protocol.

## 2. Fixed camera grids and properly oriented forward map

Exactly reuse integer triples/normalization from V1/V2:

- `A0`: the six signed unit coordinate directions;
- `C`: the eight normalized body-corner directions `(±1,±1,±1)/sqrt(3)`;
- `E`: the twelve normalized `(±1,±1,0)/sqrt(2)` and permutations;
- `T`: the twenty-four normalized `(±2,±1,0)/sqrt(5)` and permutations.

Family A is `A0`, `A0∪C`, `A0∪C∪E`; family B is `A0`, `A0∪E`, `A0∪E∪T`. Keep the V1/D3 canonical stratum order and lexicographic order of integer triples, exact antipodal partner and first-nonzero-positive axial representative. Counts remain `6,14,26` and `6,18,42` signed directions, `3,7,13` and `3,9,21` axes.

For each `n`, project a fixed ordered point list `X_0,...,X_{k-1}` by any right-handed orthographic frame `R_n∈SO(3)` with `R_n^T e_z=n`, retaining its first two coordinates. Remove translation by centring **the original 3D points once**: `Y_i=X_i−(1/k)∑X_j`, then project `P R_n Y_i`. No fitting, independent normalization, scale division, point permutation, image crop or target-based adjustment. A deterministic frame lift is optional for presentation only; exact invariants below define decisions and eliminate roll/seam sensitivity.

The registered equivalences require the **same** ordered labels for both views:

- `SO2`: planar configurations are related by a proper planar rotation, determinant `+1`;
- `O2`: planar configurations are related by an arbitrary planar orthogonal map, determinant `±1`.

Translation has already been removed by fixed centring. Uniform scale is **not** a nuisance parameter. A lower-rank projection may be considered geometrically valid for control P below, but is always rank-labelled. There is no approximate/tolerance equivalence.

## 3. Exact complete invariants and proof obligation

For every camera `n` and centring convention above, form the complete labelled planar Gram matrix

`Gram_n(i,j) = Y_i·Y_j − (n·Y_i)(n·Y_j)`.

For every ordered index pair `i<j`, form the oriented planar minor

`Area_n(i,j) = n·(Y_i × Y_j)`.

Because `R_n` is proper, this is exactly the determinant of the projected two-dimensional pair. Gram equality is **necessary and sufficient** for an `O(2)` congruence of the finite labelled planar point sets. Gram **and all oriented minors** equal is necessary and sufficient for `SO(2)` congruence: for projected rank two the sign fixes orientation; for projected rank zero/one an `O(2)` isometry can be extended to a proper one with the same action on the occupied subspace. This must be independently justified, not merely asserted by program output.

Use exact rational/algebraic equality in a known number field (integer square roots are adequate for the frozen grids); never use decimals or sampled roll optimization to decide equivalence. The classes are exact equality partitions of camera indices (no threshold-driven nontransitive clustering). Independently enumerate all ordered camera pairs and verify each pair's class decision directly using these invariants; check equivalence-reflexivity/symmetry/transitivity as a secondary guard. `O(2)` must never identify fewer pairs than `SO(2)`; every `n,−n` must be O2-equivalent.

For every projected control report its exact planar rank from the Gram matrix (0, 1, 2), equivalence partitions, class counts, class-size multisets, class membership by ordered signed camera, signed/axis consistency, and complete pairwise equivalence matrices. This is a *diagnostic capacity*, not an independent-sample count.

## 4. Three frozen control geometries

Coordinates are fixed ordered, labelled rational triples in a common laboratory coordinate system; centring does not alter affine spans:

1. **Control F (full-affine-span asymmetric tetrahedral probe):** `[(0,0,0), (1,0,0), (0,2,0), (0,0,3)]`. Affinely spans `R^3`. Every orthographic projection has planar rank 2. Equality of the full labelled projected Gram matrices implies `nn^T=mm^T`, hence `m=±n`. Because the probe spans 3D and projected rank is 2, antipodes differ under SO2 but coincide under O2. Thus it saturates the **universal camera ceiling**: SO2 classes `|G|`, O2 classes `|G|/2`.
2. **Control L (fixed labelled line):** `[(0,0,0), (1,0,0), (3,0,0)]`. Its nonzero projected length factor squared is exactly `1−n_x²`. The two cameras `±e_x` collapse the line to rank 0 and are **reported as NOT_EVALUABLE**, not silently removed or counted as a view. All remaining projected configurations have rank 1; their SO2 and O2 classes coincide and are indexed exactly by distinct `n_x²` values. No division by the projected length.
3. **Control P (fixed labelled planar triangle):** `[(0,0,0), (1,0,0), (0,2,0)]`. All cameras are geometrically evaluable, including rank-one edge-on projections, which must be *explicitly rank-stratified rather than silently discarded*. The planar Gram invariant depends on `w w^T` for `w=(n_x,n_y)`; equality occurs iff `w'=±w`. For projected rank 2 (`n_z≠0`), SO2 additionally distinguishes the sign of `n_z` through the oriented minors; for rank 1 (`n_z=0`) the SO2 and O2 tests coincide. Do not equate all edge-on observations merely because they share rank 1.

No control is selected or redesigned after observing its class counts. In this phase the labelled points are diagnostics, **not** approximations to a physical wire, contour or Meru candidate.

## 5. Frozen pre-execution mathematical oracles

Each cell lists `SO2 classes / O2 classes` for evaluable cameras. `F` is always rank 2. `L` excludes exactly two rank-0 cameras (`±e_x`) at every tier; `P` retains rank-one views and gives their count separately.

| Family/tier | Signed cameras / axes | F: SO2 / O2 | L: SO2 / O2 | P: SO2 / O2 | P: rank 1 / rank 2 |
|---|---:|---:|---:|---:|---:|
| A G0 (=B G0) | 6 / 3 | 6 / 3 | 1 / 1 | 4 / 3 | 4 / 2 |
| A G1 | 14 / 7 | 14 / 7 | 2 / 2 | 8 / 5 | 4 / 10 |
| A G2 | 26 / 13 | 26 / 13 | 3 / 3 | 14 / 9 | 8 / 18 |
| B G1 | 18 / 9 | 18 / 9 | 2 / 2 | 10 / 7 | 8 / 10 |
| B G2 | 42 / 21 | 42 / 21 | 4 / 4 | 22 / 15 | 16 / 26 |

Pre-run combinatorial rationales: Control L groups cameras by `n_x²`: G0 gives `{0}` among evaluable directions; A G1 adds `{1/3}`, A G2 adds `{1/2}`; B G1 adds `{1/2}`, B G2 additionally adds `{1/5,4/5}`. Control P: at G0 the two `±z` views share an O2 class but form separate SO2 classes; `±x` and `±y` each give a distinct rank-one class. Corners C contribute 4 SO2 / 2 O2 new classes; edges E contribute 6 SO2 / 4 O2; T contributes 12 SO2 / 8 O2. The F ceiling follows from the affine-span proof above. All predictions are **preregistered analytical expectations, not measured results**.

**Additional exact acceptance obligations:** all six A/B family-tier rows including identical G0 partitions; count and identity of two L NOT_EVALUABLE cameras per tier; per-control rank census; every class membership/size/partition consistent with complete pairwise invariant equality; proper SO2/O2 containment and antipodal law; no overclaim beyond labelled rigid orthographic geometry. If a preregistered count fails, preserve the contradiction and record `INCOMPLETE_OR_FAILED`, do not revise the signed oracle.

## 6. Minimal execution and evidence discipline

1. **Human-sign this protocol first**, in one additive Markdown commit with exact direct parent `6d1761f059de42ae1e5935eabacc495c80e83e72`, branch/upstream agreement, and the stated GPG fingerprint. Frozen `DRAFT` wording is archival after signing. Do not touch any signed predecessor or execute science while signing.
2. **Prepare a short, standalone standard-library Python 3.11 calculator outside the repository.** Rational `fractions.Fraction` arithmetic suffices for the Gram and oriented-minor equality comparisons because `(n·Y_i)(n·Y_j)` and `n·(Y_i×Y_j)` involve normalized integer triples with norms `1,2,3,5`. Exact area values containing different square roots require exact symbolic representation or rigorously proved radical comparisons; an optional declared SymPy dependency may be used, but unknown equalities must raise **INCOMPLETE**. Prefer computing Gram entries as rational numerator/denominator and area entries as a pair `(integer/rational numerator, squared norm)` with signed exact comparison. No imports from earlier experimental calculators.
3. **Source review and source freeze before invocation.** Record script SHA-256 and versions. Human separately approves **one first execution**. Record protocol commit/blob, source bytes/hash, full command, UTC start/end, original stdout JSON, stderr, exit status, Python/dependency versions, checksums. Never overwrite `run_01` or silently rerun; an essential repair is a distinct recorded attempt.
4. **Independent read-only review:** without importing/rerunning the registered calculator, reconstruct the three controls, all camera sets, both exact invariant matrices and the resulting partitions in a separately written check or direct combinatorial argument; verify the completeness proof and every preregistered oracle. Count ranks and guard degenerate L cameras explicitly.
5. **Pass label:** `MERU_3D_V3_LABELLED_PROJECTION_EQUIVALENCE_PASS` iff all registered exact count, rank, partition, orientation and proof obligations pass; otherwise `MERU_3D_V3_INCOMPLETE_OR_FAILED`, retaining original evidence and discrepancies. Any operational failure is also fail-closed.

## 7. Next boundary

If V3 passes and is independently reviewed and signed, a **separate V4 protocol** may move from **labelled landmark congruence** to *unlabelled curves / genuine silhouette diversity*, using both independent generic controls and source-justified candidate geometry only after explicitly registering forward model, admissible source geometry, occlusion/collapse, reparametrization, nuisance freedom and negative controls. Historic Meru images and Hebrew targets remain excluded pending a separate, justified target-use gate. A higher camera count or a larger labelled-projection class count does not itself establish historical intent or specificity.
