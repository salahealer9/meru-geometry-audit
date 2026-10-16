# P0A2 — Independent Quality Control of Target-Blind Numerical Design Review

**Date:** 2026-10-16  
**Disposition:** **PASS — RECOMMENDED FOR SEPARATE HUMAN GPG-SIGNED P0A2 DESIGN DECISION FREEZE, WITH EXPLICIT QUALIFICATIONS**  
**Scope:** independent, read-only examination of the signed target-blind design protocol, submitted review ZIP, frozen prior scientific sources, and symbolic mathematics. **No experimental, synthetic-pilot, solver, direction-enumerator, rendering, Hebrew-target or candidate-versus-null execution.**

## 1. Object and exact identity

- Input: `P0A2_target_blind_design_QC_package(1).zip`.
- **Outer ZIP SHA-256:** `e5b6aaf8c0c5e00a2ff68d0ec4a48c168a6c45cf89e00b4bfccaa39662183286`.
- Compressed size: **86,054 bytes**; 15 regular file members; summed uncompressed lengths **208,366 bytes**.
- Archive CRC integrity: **PASS** (`ZipFile.testzip()` returned `None`).
- `PACKAGE_INVENTORY.json`: **13/13** payload sizes and SHA-256 identities verified.
- `SHA256SUMS`: **14/14** entries verified (13 payloads plus the inventory); manifest correctly excludes itself. No unlisted ZIP member.
- Exact proposed destination: `reports/v0_9/p0a2_target_blind_design/` with 12 registered deliverables; README, inventory and checksum manifest remain package-root control files, not automatic repository additions.
- CSV schemas: **11 observation/operator records × 14 columns; 15 capacity-budget records × 11 columns; 4 solver records × 16 columns; 43 decision records × 9 columns**. IDs unique; all table cells populated; UTF-8/CSV/JSON parsed successfully.

## 2. Independently checked frozen authority

Read-only GitHub API checks at `salahealer9/meru-geometry-audit`, branch `hebrew-projection-capacity-v0.9`:

| Checkpoint | Git commit | Parent | GitHub signature |
|---|---|---|---|
| P0A2 protocol | `e917fa2974997703d6ccb60b0b25d0c668d12bd5` | `090a1db6c95976bbb5f0d69a3cc4a4603d165505` | Valid |
| P0A1 decision freeze | `090a1db6c95976bbb5f0d69a3cc4a4603d165505` | `5b0317f193c481d799e88b494ce370679fec43bc` | Valid |
| P0A1 preregistration | `5b0317f193c481d799e88b494ce370679fec43bc` | `5148712c07ac48742d3435dc14e01667280f94c3` | Valid |
| P0A0 results freeze | `5148712c07ac48742d3435dc14e01667280f94c3` | `24c00fc44e4d9d57adacd1e636e9e2d20d86a954` | Valid |
| P0A0 implementation freeze | `24c00fc44e4d9d57adacd1e636e9e2d20d86a954` | `d15865167b4e3c454e398bd498d9d681103096f7` | Valid |
| P0A0 preregistration | `d15865167b4e3c454e398bd498d9d681103096f7` | `8bf0babfd91bdefb0792e93707fd0b0da1c09767` | Valid |

- Remote branch HEAD at review: **`e917fa2974997703d6ccb60b0b25d0c668d12bd5`**; only the P0A2 protocol added at this checkpoint.
- P0A2 signed protocol Git blob: **`61585fb47cdb3ff2a3cfef07d3548fbd08084d0b`**; P0A1 protocol Git blob **`d0a20485e8a2793fae6ede040fc266e461c8f23f`**; P0A0 protocol Git blob **`0f8b663bfe2432685c9320a00c80fd6bcf436e38`**.
- **21/21 source-file Git blob identities** in `provenance_and_information_barrier.json` independently matched fresh pinned GitHub fetches, including the P0A0 registered JSONL, P0A1 methodological closeout, and inherited amendment report.
- The expected signer fingerprint in the signed lineage and preserved agent GPG status is **`D4EC014EEFCC90E619D2AA59A91239ABCF512130`**. This QC independently checked GitHub's six valid-signature results and commit parents; it did not independently rerun local GPG verification for all six (the agent package preserves its own local verification outputs).
- The package's signed v0.8 tag verification and older ancestry bridge were inspected in provenance and match prior frozen records; the present QC did not perform a fresh raw tag-object verification.

## 3. Registered D0–D7 coverage and mathematical audit

**D0 — PASS.** Exact chain, sources, frozen raw result and archive identities, signature evidence and source barriers are recorded. Original P0A0 5 PASS / 8 EXPECTED_BLIND_SPOT / 0 FAIL / 0 NOT_EVALUABLE preserved. Inherited deselected image tests, missing crop, incomplete DEV log, prior nonzero key-import, A09 absent original bytes and recovered P0A1 package provenance remain visible. The agent's new isolated GPG key import returned 2 but was followed by its recorded valid commit/tag signatures; no rewriting of the failure to success. Its reported absent local checkout is not misrepresented as a clean checkout.

**D1 — PASS.** Exactly seven distinct representation classes (R3-C, R3-S, R2-O, R2-U, R2-G, R2-I, R2-H) and four distinct lanes (L1–L4) documented. Ordered-centerline projection, ink rendering, historical physical shadows and independent graph annotation are not conflated. L3 physical optics and L4 target annotations are not asserted as observed.

**D2 — PASS WITH CONDITIONAL OBSERVABLES.** QO defines normalized 2-D arclength-parametrized open polyline comparison, a fixed traversal group, and analytic SO(2) roll minimum. For normalized A,B the squared residual is `2−2(α cos θ+β sin θ)`; maximizing correlation gives `sqrt(2−2 sqrt(α²+β²))` with β derived using the counterclockwise quarter-turn J. This is correct under the explicit common arclength measure and positive RMS assumptions, and does not transfer to unlabeled targets. QH defines finite distinct-point support with independent uniform empirical centering/RMS and a symmetric finite-set Hausdorff minimum over the rotation circle. Its metric-on-orbits and pseudometric-on-raw-observations claims follow under the specified nondegenerate normalization and compact actions. Finite-support sampling density dependence, omitted graph labels, and non-attainment of a raw `s>0` least-squares fit when maximal correlation is zero are properly distinguished. No final target score or composite weight chosen.

**D3 — PASS FOR EXACT FINITE MEMBERSHIP, NOT COVERING CERTIFICATION.** Let A0 be the six unit coordinate axes, C the eight signed cube-corner directions, E the 12 normalized equal-magnitude coordinate-plane directions, and T the 24 normalized unequal `2:1` coordinate-plane directions. The nonzero-coordinate pattern and magnitude ratios make the four strata disjoint; therefore family A `A0 ⊂ A0∪C ⊂ A0∪C∪E` has **6/14/26** signed directions, and B `A0 ⊂ A0∪E ⊂ A0∪E∪T` has **6/18/42**. All strata are antipodally paired, yielding **3/7/13** and **3/9/21** axes under a separate O(2) quotient. These are symbolic cardinality proofs, not generated empirical counts or Meru historical viewing prescriptions. The frame lift selecting the least-absolute component axis has denominator ≥sqrt(2/3), yields a proper orthogonal rotation with `R_nᵀ e_z=n`, and handles ties/seams by explicit canonical conventions. The universal SO(2)\SO(3)≈S² and antipodal O(2) quotient are justified for compatible point-projection observations; not automatic for physical shadows. Separation/covering values and continuous camera error `Lδ` are **not established**, correctly deferred to later independent certificates. Nested-domain **infimum** monotonicity is valid with unchanged observation/metric/nuisance contracts.

**D4 — PASS FOR CERTIFICATION ARCHITECTURE, NOT NUMERICAL CERTIFICATION.** Exactly four score×family combinations (QO_A, QO_B, QH_A, QH_B), all explicitly **`GLOBAL_CERTIFICATION_DEFERRED`**. QO's finite-camera plus analytic-roll route still needs certified input, exact/interval integration and all-branch arithmetic. QH's per-view full-circle bound `|d_H(Q_θA,B)−d_H(Q_φA,B)|≤ρ_A d_{S¹}(θ,φ)` is valid for a *fixed normalized support*, but is correctly not extended without proof to camera-dependent normalization. The proposed `U−L≤2η+ρh` full-cell scheme requires exhaustive branch and interval coverage; no U/L/K/ε values were actually evaluated. Error propagation, degeneracies, ties, feasibility witnesses, timeout and refusal to call local minimizers global are adequately specified as future checks. S11 local 0.4 vs analytic global 0 is correctly preserved.

**D5 — PASS FOR FUTURE FAIRNESS CONTRACT ONLY.** Fifteen budget dimensions separate effective direction counts, planar SO(2)/O(2), scale, traversal, graph/crop freedoms, sampling, shape-family parameters, numerical accuracy and failure policy. Exact N0–N3 laws, matching, distributions, sample sizes, seeds and actual parity remain unspecified, so `P0A2_CONTROL_FAIRNESS_NOT_SPECIFIED` must coexist with any qualified design status. Symbolic fixed-corpus error matrices, null contrasts, candidate×capacity interaction, per-letter coherence, calibration and detectable-advantage formulas are clearly non-executed proposals; exchangeability-based Monte Carlo p-value forms are explicitly conditional, not asserted for fixed candidates. The 22 basic letters are not treated as IID; the 27-form convention is a separate later choice.

**D6 — PASS.** Five original source-provenance classes preserved; historical missing finished-form geometry and optics unaltered. A09 is metadata-only, the image absent and not stream-hashed; hand-drawn shadowgrams are not metric inverse observations. Signed future rights/second-chart, numerical method/implementation, independent new-fixture certification, candidate/control, confirmatory and first-pixel gates remain closed.

**D7 — PASS.** Forty-three decisions include all four lanes, both score designs, both direction families, four combinations, eight inherited P0A1 paths, excluded extensions and unresolved slots. Original independent-review checklist remains **unfilled**, appropriately reserved to this separate QC. No scientific conclusion has been cosmetically promoted to global certification or to a historical source finding.

## 4. Qualification decision and explicit exclusions

**Recommended, assignable only after human-signed freeze:**

`P0A2_TARGET_BLIND_NUMERICAL_DESIGN_READY_FOR_IMPLEMENTATION_PLANNING`

All six subsidiary limits must be retained simultaneously:

- `P0A2_OBSERVATION_MODEL_UNRESOLVED`
- `P0A2_SCORE_SELECTION_DEFERRED`
- `P0A2_CAPACITY_CERTIFICATION_DEFERRED`
- `P0A2_SOLVER_CERTIFICATION_DEFERRED`
- `P0A2_CONTROL_FAIRNESS_NOT_SPECIFIED`
- `P0A2_SOURCE_CONSTRAINT_UNRESOLVED`

**No blocker necessitating a P0A2 correction/amendment was found** in the reviewed symbolic mathematics, reporting, package integrity or source identities. This is a limited readiness-for-planning result; **no final primary Hebrew metric, chosen experimental G1/G2 levels, solver/global-minimum certificate, actual equalized N0–N3 controls, recovered 3-D historical FIRST HAND, image/rights permission, scientific numerical run, Hebrew score or v0.9 release** is thereby established.

The next appropriate act is a separate **human-reviewed GPG-signed P0A2 design-decision/results freeze**, preserving all original review bytes, this QC report, the original ZIP, manifests, caveats and unresolved gates. The independent QC is not itself the human signature.

## 5. Audit conduct and evidence limits

- Did not call the registered S00–S12 runner, or any P0A0 fixture/case evaluation.
- Did not generate candidate/control objects, directions, rendering, scoring, optimizer runs, numerical parameter sweeps or new synthetic scientific fixtures.
- Did not inspect/download Hebrew chart pixels, glyph shapes, proxy fonts, letter scores or copyrighted source-image bytes.
- Made only read-only GitHub source and commit queries and local packaging/CSV/JSON/hash checks; mathematical assertions were assessed analytically from the supplied formulas.
- The inspected archive contained no image/font/glyph/scientific-executable assets. Its declarations of no repository write, numerical execution and Hebrew access are supported by submitted provenance and package contents, **not** by an exhaustive external-host audit.

**Independent QC disposition: PASS WITH RETAINED QUALIFICATIONS. HUMAN FREEZE: PENDING.**
