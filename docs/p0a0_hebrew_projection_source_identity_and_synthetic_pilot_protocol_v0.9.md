# P0A0 — Hebrew Projection Source Identity and Synthetic Engineering-Pilot Protocol

**Project:** Meru Geometry Audit  
**Development line:** `v0.9` — Hebrew projection specificity and capacity  
**Repository:** `salahealer9/meru-geometry-audit`  
**Target branch:** `hebrew-projection-capacity-v0.9`  
**Verified pre-preregistration branch HEAD:** `8bf0babfd91bdefb0792e93707fd0b0da1c09767`  
**Date drafted:** 2026-10-13  
**Status:** **DRAFT — NOT PREREGISTERED UNTIL GPG-SIGNED COMMIT**  
**Phase type:** source-identity freeze and engineering-only pilot specification  
**Hebrew-letter extraction/scoring:** **PROHIBITED**  
**Scientific candidate/null comparison:** **PROHIBITED**  
**Automated commit/push by execution agent:** **PROHIBITED**

## 0. Preregistration and execution boundaries

This document is a **protocol candidate**, not a report of results. It must be reviewed and frozen by GPG-signed commit on the named development branch **before** implementation work begins. The signed commit SHA, protocol Git blob SHA, and parent HEAD must be carried into the later agent execution handoff.

Three boundaries are distinct:

1. **P0A0 protocol freeze:** primary source identity, prohibited actions, synthetic adversarial case classes and their expected relationships, QC obligations, and stopping conditions are fixed. No pilot results precede this freeze.
2. **Later implementation-only freeze:** code, deterministic fixture coordinates, numerical tolerances, oracle algorithms and seeds must be documented and frozen **before** the registered pilot run. Exploration needed to write code must use segregated synthetic development fixtures and cannot be misrepresented as registered pilot results.
3. **Later synthetic execution and QC:** execute the frozen fixture set and record all passes, failures, degeneracies and numerical limits. Any fixes require a separately recorded amendment/new implementation freeze and another **synthetic-only** run.

P0A0 does not freeze the future confirmatory Hebrew target extraction/metrics, does not test alphabet-generation claims and does not authorize agent writes to GitHub. Do not label any P0A0 output `CONFIRMATORY` or `MERU_LETTERS_RECOVERED`.

## 1. Verified baseline and protected inheritance

The v0.9 branch and `main` were both verified at:

`8bf0babfd91bdefb0792e93707fd0b0da1c09767`

The signed `v0.8.0` tag refers to the merged checkpoint commit:

`85748bff0bfae383afcc0d885f4aec505a2885dd`

`pyproject.toml` and `CITATION.cff` remain at version `0.8.0`; **do not** prematurely release `0.9.0`. The 2026-10-13 correspondence outcome is recorded under `docs/correspondence/meru_foundation/provenance/`.

The GitHub baseline does **not** prove the local working tree is clean. The user must verify branch, HEAD, status, remote and file diff before signing.

The v0.8 published-corpus result remains:

`NO_REPRODUCIBLE_PUBLISHED_FIRST_HAND_CONSTRUCTION_RECOVERED`

Nothing in P0A0 may modify or rerun sealed v0.3–v0.8 science. The missing three algebraic function sets are **not** represented by our reconstruction candidates; the dimpled-sphere carrier family is **not** uniquely historical; and no post-hoc fitted shaping rule may be introduced. Future Meru correspondence, if any, is separate post-v0.8 archival evidence, not an input to this pilot.

## 2. Purpose and non-purpose

The eventual (separately preregistered) v0.9 question is:

> Do source-constrained Meru candidates exhibit Hebrew-letter projection specificity beyond progressively matched generic 3-D geometry, and is performance robust to the underdetermination established in v0.8?

Tenen's published observation that generic spirals/coiled wire can produce letter-like shadows is a **qualitative non-specificity prediction**, not an equation predicting equality of any future test statistic.

The **sole P0A0 engineering question** is:

> Can the projection, representation, normalization, metric and optimization machinery be exercised against independently designed adversarial **synthetic** cases without access to Hebrew-letter target geometry?

No Hebrew claims are tested here. No scientific candidate or null-ensemble score is computed. Method rejection or refinement based on synthetic oracle failure is legitimate **only before** Hebrew target access and must be reported rather than hidden.

## 3. Freeze the primary target-source identity — not its pixels

The primary Meru-authored eventual target **source** is the already archived **A09** record. These fields are copied from pre-existing repository metadata; this protocol does **not** claim a new independent image inspection.

| Field | Frozen value |
|---|---|
| Asset ID / source ID | `A09` / `S06` |
| Title | `First Hand Hebrew chart` |
| Image URL | `https://www.meru.org/Gestures/frsthand873.jpg` |
| Source page | `https://www.meru.org/Gestures/Alphachart.html` |
| Source registry | `references/key_geometric_assets.csv` |
| Snapshot manifest | `references/geometric_asset_snapshot_manifest.csv` |
| Local-only raw snapshot path | `data/raw/geometric_assets/A09_frsthand873.jpg` |
| Image format / mode | JPEG / RGB |
| Dimensions | `826 × 787` pixels |
| Bytes | `542620` |
| SHA-256 | `a091cbe95b9042cddb93bb5a57a07b406d5d1a6053e481faf2746b38a22dab68` |
| Recorded retrieval | `2026-07-26T13:43:53+00:00` |
| Repository redistribution policy | `Local snapshot only; metadata committed` |

**Read-only identity check:** parse the A09 row from both frozen CSVs and compare to this table. Detect missing, duplicate or inconsistent rows. The source registries must not be edited to force agreement.

The raw image is intentionally excluded from Git by `.gitignore`. If the exact local file exists, it may be *stream-hashed and byte-counted without opening, decoding, displaying or transforming it*. State separately whether the manifest matches and whether the actual bytes were independently hashed. If absent, record `A09_SNAPSHOT_NOT_LOCALLY_PRESENT`: absence does **not** block the synthetic-only pilot. Do not download or inspect A09 to repair that absence during this phase.

**Forbidden:** loading source pixels, generating thumbnails, OCR, cropping, skeletonizing, tracing, fitting, embedding, rasterizing or scoring A09; using A06 or another genuine Hebrew chart as substitute synthetic data. The source itself acknowledges hand-drawn shadowgram tracings, distortions and truncated/simplified forms, so its pixels cannot be treated automatically as an exact geometric target.

Freeze **A09's identity**, not the later 22/27-symbol inclusion convention, target segmentation, stroke semantics, uncertainty model, or comparison font. A secondary independently sourced Meruba Ashurit chart must be chosen/frozen before the future confirmatory analysis, not in this pilot.

## 4. Code already present — additive engineering only

The repository actually contains:

- `src/meru_geometry/projections.py`: orthographic projection with finite-input and proper-rotation validation.
- `src/meru_geometry/rotations.py`: tetrahedral rotation infrastructure.
- `src/meru_geometry/projection_orbits.py`: camera-direction classes and planar SO(2)/O(2) similarity alignment for **equally sampled** curves, with optional closed-curve shifts/reversal.
- `docs/geometry/projection_orbit_results_v0_5.md`: 12 proper rotations yield **6 signed camera directions** or **3 unoriented viewing axes**, conditional on equivalence semantics.
- `shape_metrics.py`, `silhouettes.py`, `letterforms.py`, `null_models.py`, `statistics.py`: still placeholder modules, not a validated Hebrew scoring pipeline.

Preserve the validated v0.5 orbit behavior. Existing equal-sample Procrustes alignment is **not** automatically a valid metric for unlabeled multi-stroke images. Prefer small additive pure functions and isolated tests; any changes to inherited APIs require explicit justification and complete regression coverage.

## 5. What representation means

Fixtures must distinguish:

1. **Ordered curve/stroke:** parameterized or sampled path, traversal, endpoint and retracing data.
2. **Geometric support:** the 2-D set of occupied points, which discards stroke provenance and often orientation.
3. **Stroke graph:** components, stroke identities, endpoint counts and junction adjacency where available.
4. **Raster/ink silhouette:** depends on stroke width, antialiasing, resolution and possible occlusion.

For instance, two differently segmented paths can occupy identical geometric support; no support-only metric can infer the missing stroke labels. Declare this as **non-identifiability**, not metric failure to detect unavailable information. Similarly, a projected 3-D centreline is not equivalent to the shadow of a finite-width 3-D hand/ribbon.

## 6. Adversarial synthetic fixture registry

The following **case classes and logical oracle relationships** are fixed now. Exact synthetic coordinates, step sizes, seeds, raster dimensions, numeric tolerances, optimizer options and fixture hashes must be frozen in a distinct implementation-only checkpoint **before** the registered pilot run. No fixture may be derived from Hebrew strokes, Meru hand imagery, fonts, or existing letter-target extractions.

| ID | Registered case | Required oracle / observation |
|---|---|---|
| `S00` | Analytic 3-D sample and known camera matrices | Orthographic projection agrees with direct coordinate calculation; improper rotations/nonfinite inputs rejected. |
| `S01` | Exact translation, positive scaling, permitted in-plane rotation | Methods claiming these invariances match within frozen tolerance and return correct transformation. |
| `S02` | Genuinely chiral asymmetric planar curve versus its mirror | SO(2)-only alignment does **not** silently reflect; O(2)-allowed alignment can recover a mirror match. |
| `S03` | Same curve with strongly unequal point sampling density | Resampling-invariant methods remain stable; point-index methods failing are labeled sample-sensitive. |
| `S04` | One stroke versus two separately labeled strokes with the same geometric support | Support-only methods may tie; any topology-aware claim requires actually supplied stroke data. |
| `S05` | Connected path versus almost-connected disconnected paths | Component/gap detection and raster-resolution dependence must be reported without hidden gap closing. |
| `S06` | Large primary path with and without a small detached component | Identify component-blindness and whether a registered explicit component penalty remedies it. |
| `S07` | Similar support with different exposed endpoint count or extra spur | Diagnose endpoint blindness; do not describe unordered support error as endpoint-aware. |
| `S08` | Main path with and without a small hook/notch | Quantify local feature sensitivity and whether normalization/thresholding hides it. |
| `S09` | Reversed traversal and closed cyclic shift versus open path | Report invariance only when permitted; never permit cyclic shifts of an open curve by accident. |
| `S10` | Zero extent, duplicate samples, nonfinite input, very small components | Deterministic explicit validation; no NaN silently converted to a good score. |
| `S11` | Multimodal planar optimization with deliberately competing local minima | Compare optimizer against independently fixed analytic or exhaustive synthetic oracle; report failures/tie breaking. |
| `S12` | Duplicate tetrahedral camera frames, front/back axes, axial camera roll | Respect v0.5 orbit classes and test redundancy of roll when planar SO(2) is free. |

Every case must record: generator/config identity; observables and metadata; oracle; claimed metric invariances; normalized/raw outcomes; synthetic sensitivity; and a state `PASS`, `EXPECTED_BLIND_SPOT`, `FAIL` or `NOT_EVALUABLE`. Explain every non-pass. A documented `EXPECTED_BLIND_SPOT` is a useful **diagnostic**, not certification of an absent capability. Do not require all metrics to represent all observables.

## 7. Permitted exploratory methods (no metric chosen yet)

The pilot may evaluate, solely on synthetic data:

- ordered-curve Procrustes/relative RMS and arclength-resampled alternatives;
- symmetric Chamfer or Hausdorff-style support distances;
- explicit endpoint/component/junction diagnostics and transparent composites;
- simple finite-width synthetic stroke rasterization and silhouette metrics;
- exhaustive deterministic transformation enumeration versus continuous numerical optimizers.

This list does **not** freeze final metrics, weights, normalization, sampling, silhouette width, or threshold choices. Method selection must be justified by synthetic-oracle behavior **before** real-letter inspection, and must later be separately preregistered. A metric cannot become topology-sensitive merely by being labeled so.

## 8. Projection-freedom hierarchy — conceptual freeze only

The later scientific design is expected to compare:

- `G0`: constrained discrete tetrahedral views, with v0.5 direction equivalence honored;
- `G1`: a larger **effective** viewing set (to be defined later from a source/engineering justification);
- `G2`: an even broader **effective** viewing set (to be defined later).

**Neither G1 nor G2 is numerically frozen here.** Increasing freedom is a capacity experiment, *not* evidence of historical viewing instructions.

Critical degeneracy: under orthographic projection, axial camera roll is equivalent to planar image rotation. If SO(2) planar similarity is already optimized, adding roll **does not increase effective capacity**. A future G1 may not claim to increase capacity through roll alone while the image metric quotients out rotation. The synthetic pilot must exhibit this equivalence.

## 9. Later specificity study — recorded scope, not execution authority

Future candidate-vs-control science may use this ladder, each level requiring its own formal specification and comparability review:

- `N0`: arbitrary smooth 3-D curves;
- `N1`: length/curvature/complexity-matched curves;
- `N2`: generic 1.5-turn vortices with non-fixed radial laws;
- `N3`: same-carrier, same-span, non-reciprocal spiral controls.

The eventual study will also freeze *actual source-constrained candidate models*, without asserting they reproduce the three missing Tenen algebraic constructions. No numerical model evaluation is authorized by P0A0.

The eventual confirmatory preregistration must determine **before any real-letter scores**:

1. exact source target, component/tracing rules, primary 22-form versus 27-form question, chart uncertainty and secondary-chart sensitivity;
2. exact candidate/null generator sets, random seeds, null-ensemble sizes and sampling/normalization;
3. effective projection groups G0/G1/G2 (not redundant nominal views);
4. primary per-letter error matrix and aggregate statistic;
5. candidate-minus-null performance by level;
6. the **object-specificity × projection-freedom interaction** as a primary outcome;
7. per-letter coherence among source-constrained candidate models;
8. simulation-based minimum detectable advantage **per null and viewing level**, particularly N3;
9. multiplicity and finite-Monte-Carlo-resolution policy.

The 22 Hebrew basic letters form a **fixed corpus**, not 22 IID statistical replicates. Inferential randomization will be driven by null objects. An N3 null is "no detectable specificity at registered sensitivity," not proof of identity. Positive geometry-vs-null results do not establish ancient alphabet origin, Genesis derivation, theology or a unique historical Meru sculpture.

## 10. Repository, rights and provenance boundary

The repository is public. The frozen metadata explicitly mark Meru A09 image bytes as `Local snapshot only; metadata committed`; `.gitignore` excludes `data/raw/geometric_assets/`.

- **Do not** commit or redistribute original Meru source images, crops, letter traces, screenshots or embedded source-image bytes.
- Publish only source IDs, provenance, URLs, hashes, generated **independent synthetic** fixtures/code and synthetic QC results at this stage.
- Synthetic fixtures must not be approximations, stylistic transformations or tracings of genuine Meru or Hebrew glyphs.
- A future target extraction is distinct from permission to publish/relicense the extraction; decide rights and public output scope before confirmatory images are distributed.
- Do not commit personal email addresses beyond approved public institutional addresses, confidential correspondence, unpublished files or third-party attachments without permission. Preserve private source provenance/hash records separately where required.
- Any response from Meru belongs to a separate post-v0.8 archival-provenance workflow, not this experimental input set.

This research policy is deliberately conservative; it is not a legal opinion.

## 11. Hard prohibited operations

Until a separately signed confirmatory protocol permits them:

1. No A09 or other Hebrew-chart pixel decoding, cropping, OCR, skeletonization, stroke extraction, tracing, target registration, or scoring.
2. No display of candidate-vs-Hebrew projections, overlays, matching errors or letter recovery counts.
3. No tuning metrics, regularization, optimizer tolerances, camera sets or model shapes by looking at actual Hebrew forms, even informally.
4. No Hebrew-letter pilot subset, including "three letters then discard results".
5. No importing source-derived letter geometry into synthetic fixture generation.
6. No scientific candidate/null-ensemble run; no adaptive control family selection.
7. No rewriting frozen v0.8 mathematics, source null or earlier certificates.
8. No registered pilot-run results before implementation-only fixture/oracle/parameter freeze.
9. No silent suppression of unsuccessful metrics, degenerate cases or optimizer failures.
10. No unapproved agent commit, push, pull-request, tag, release or remote history change.

These restrictions apply to tool inputs, intermediate caches and debug outputs as well as published artifacts. Reading the pre-existing A09 metadata row is expressly allowed; opening its image pixels is not.

## 12. Required outputs for subsequent authorized agent work

### Source identity QC

- exact Git HEAD and clean/dirty local checkout state;
- unique-row A09 registry/manifest consistency check;
- local raw A09 file `present` or `absent`, with byte-count/SHA-256 check **only if bytes already exist**;
- no claim of image hash validation based on CSV alone;
- rights/redistribution policy statement;
- negative assertion `NO_HEBREW_TARGET_ANALYSIS_PERFORMED` supported by input/output inspection.

### Implementation-only freeze

- reproducible synthetic fixture generator and serialized fixture manifest for `S00`–`S12`;
- deterministic seeds, scales, image resolution, floating-point conventions, numerical tolerances and optimizer configuration;
- analytic/exhaustive synthetic oracles independent of the tested optimizer;
- additive pure projection/metric/normalization/rasterization code as necessary;
- tests mapping each case ID to oracles, plus existing full regression suite;
- exact Git/source hashes of the **implementation-only** snapshot sealed before registered synthetic pilot results;
- no real Hebrew input files in the implementation package.

### Later synthetic execution QC

- case-by-case matrix of `PASS` / `EXPECTED_BLIND_SPOT` / `FAIL` / `NOT_EVALUABLE`;
- algorithm-by-algorithm invariance and identifiability audit;
- optimizer–oracle discrepancy and numerical resolution sensitivity;
- camera-roll/equivalent-view diagnostic;
- all negative/pathological results and smallest unresolved implementation failures;
- environment, commands, random seeds, code/input hashes and actual test counts;
- a synthesis recommending candidate metric/representation approaches for **later** preregistration, without deciding them from Hebrew scores.

Suggested later paths (to be fixed at implementation freeze): `docs/v0_9/`, `tests/test_v0_9_synthetic_*.py`, `scripts/`, `reports/v0_9/`. Do not overwrite earlier phase output paths.

## 13. Acceptance, negative outcomes and stopping rules

`P0A0_SYNTHETIC_ENGINEERING_PILOT_READY` may be assigned **only after subsequent authorized implementation and execution** and only when all of the following are true:

- A09 metadata identity has been verified without target-pixel use;
- implementation, fixtures and tolerances were frozen before registered pilot scores;
- every `S00`–`S12` case received an oracle and explicit state;
- analytic projection operations match their synthetic oracles within frozen tolerance;
- any claimed transformation invariance is supported; forbidden reflection/front-back/orbit identifications are not silently introduced;
- impossible-to-observe topology has been correctly called non-identifiable rather than falsely recovered;
- invalid inputs produce explicit failure/diagnostics rather than artificially good matches;
- optimizer failures and case degeneracies are preserved, not quietly fixed after viewing results;
- the inherited regression suite is preserved or any genuine regression failure is raised as a blocker;
- at least one adequately characterized projection/metric path exists for a **future** confirmatory-protocol design; and
- `NO_HEBREW_TARGET_ANALYSIS_PERFORMED` is true and auditable.

This state certifies *engineering suitability only*, not scientific success or a finalized Hebrew metric.

Other explicit outcome states:

- `P0A0_METRIC_PATHOLOGY_DOCUMENTED` — a synthetic degeneracy has been established; a method can be excluded or restricted in the next frozen design.
- `P0A0_OPTIMIZER_NOT_CERTIFIED` — global/bounded minimization reliability is insufficient; **no** Hebrew scoring is permitted.
- `P0A0_REPRESENTATION_INSUFFICIENT` — required component, endpoint or stroke information cannot be expressed/identified by proposed observables.
- `P0A0_SOURCE_IDENTITY_MISMATCH` — unique A09 identity fails the frozen manifest comparison: **STOP**, without silently modifying source data.
- `P0A0_INFORMATION_BARRIER_VIOLATION` — Hebrew target images/geometry influenced engineering choices: **STOP**, quarantine outputs and assess a new confirmatory boundary.
- `P0A0_IMPLEMENTATION_NOT_FROZEN` — registered pilot outputs would precede frozen fixture/code definitions: **DO NOT EXECUTE**.

The synthetic pilot stops after `S00`–`S12` are evaluated once according to the frozen implementation, or sooner on a mandatory blocker. Further adversarial cases require a named amendment/new synthetic checkpoint; no adaptive enlargement within an already frozen run. A negative engineering result is valid evidence and cannot be called a failed research phase.

## 14. Human review, signing and agent handoff gates

1. Verify `git switch hebrew-projection-capacity-v0.9`, `git rev-parse HEAD`, `git status --porcelain`, `git branch -vv`, and `git diff --check`. Confirm the frozen baseline before adding this document.
2. Review this protocol alongside `references/key_geometric_assets.csv`, `references/geometric_asset_snapshot_manifest.csv`, `docs/geometry/projection_orbit_results_v0_5.md`, the existing implementation modules, and `docs/first_hand_construction_source_recovery_closeout_v0.8.md`.
3. Stage **only this P0A0 protocol** and verify `git diff --cached --check` and `git diff --cached`.
4. Create a **GPG-signed preregistration commit** and push the v0.9 development branch. Record full commit SHA, parent SHA, protocol Git blob SHA, signature verification and alignment with `origin`.
5. Only after this freeze, separately prepare the bounded agent **implementation-only** handoff, specifying `NO COMMIT / NO PUSH`, the signed protocol SHA and both source identity safeguards and synthetic-only restrictions.
6. Review/freeze the implementation and synthetic fixtures **before** any registered pilot execution; then review exact run outputs before formulating the confirmatory Hebrew-target preregistration.

No pending reply from Meru blocks the engineering work; any eventual archival response follows a different scientific/provenance gate.

## 15. P0A0 status at issuance

**DRAFT — AWAITING HUMAN REVIEW AND GPG-SIGNED PREREGISTRATION.**

This protocol does not contain a pilot result. The next legitimate step is the **protocol-only freeze**, not a full experiment, Hebrew source digitization, candidate-vs-null run, or agent-driven commit.
