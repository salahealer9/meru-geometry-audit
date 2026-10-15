# P0A0 — Independent QC of Registered Synthetic Execution

**Date of review:** 2026-10-15  
**Disposition:** **PASS — P0A0_SYNTHETIC_ENGINEERING_PILOT_READY (qualified)**  
**Additional recorded limitations:** `P0A0_METRIC_PATHOLOGY_DOCUMENTED`; `P0A0_OPTIMIZER_NOT_CERTIFIED` (global optimization)  
**Scientific claim:** engineering suitability of *synthetic-only* projection/representation diagnostics; **no Hebrew-letter or candidate-vs-null scientific results**.

## 1. Input and immutable identity

User-provided package: `p0a0_registered_synthetic_execution_QC_package(2).zip`.  
Outer ZIP SHA-256: `5c1b371ddaa2803430705a87f6cba748f3f3cd929749f596a55e1cd53a387295`.  
ZIP archive CRC/integrity: PASS.  
All **14 non-checksum payload files** have matching SHA-256 and byte lengths in `PACKAGE_INVENTORY.json`; the `SHA256SUMS` file verifies all 15 listed files (including the inventory). No extraneous package files were found.

Frozen scientific protocol commit: `d15865167b4e3c454e398bd498d9d681103096f7`.  
Protocol Git blob: `0f8b663bfe2432685c9320a00c80fd6bcf436e38`.  
Frozen implementation commit: `24c00fc44e4d9d57adacd1e636e9e2d20d86a954`.  
Parent of implementation: exactly the above scientific preregistration.  
GitHub branch: `hebrew-projection-capacity-v0.9`.  
GitHub commit signature verification: **valid**.  
Independent GitHub blob comparison: **12/12** manifest-bound implementation source artifacts match the source Git blob identities in the submitted provenance record.

Raw registered result: `p0a0_registered_pilot_once.jsonl`; **12,052 bytes**; SHA-256 `4b4b27b0d5d9a95ffe864e2d2c83433be0ddd544b6122ebbea294857326817d6`. No raw record was rewritten for this QC.

## 2. Independent inspection procedures

- Recomputed outer ZIP hash; tested every compressed member and each packaged SHA-256 checksum.
- Inspected the protocol, frozen-source identities and implementation-manifest bytes/paths through GitHub read-only access.
- Parsed the actual JSONL without importing or calling `registered_pilots.p0a0` code; verified one synthetic boundary header, exact freeze/manifest hashes, 13 distinct case IDs in order, state counts, required field schema, explanatory text and numerical finiteness.
- Compared recorded numerical outputs with *elementary independent expected relationships* from the frozen case definitions: known transformations, projection errors, sampling sensitivity, mirror handling, graph counts, simple sampled distances, pixel-difference classifications, local/global objective discrepancy, and tetrahedral view equivalence.
- Cross-checked preflight, single-attempt/completion records, postrun protected-file hashes and Git status/diff evidence. No scientific fixture generator, case evaluator, registered runner or optimizer was executed by this independent review.

**Read-only independent check tally: 42/42 PASS.** Machine-readable results: `P0A0_registered_execution_independent_verification_2026-10-15.json`.

## 3. Recorded case matrix and substantive interpretation

| Case | State | Independent check and interpretation |
|---|---|---|
| S00 | PASS | Orthographic projection discrepancy zero; improper rotation and nonfinite inputs rejected. |
| S01 | PASS | Known scale 2.5 and translation `(4,-7)` recovered; relative RMS ~2.45e-16. |
| S02 | PASS | SO(2) mirror nonmatch relative RMS ~0.558; O(2) match ~1.86e-16, with no silent reflection. |
| S03 | EXPECTED_BLIND_SPOT | Sample-index discrepancy ~0.503; arclength resampling ~1.55e-15 on the frozen straight polyline. No blanket resampling theorem. |
| S04 | EXPECTED_BLIND_SPOT | Identical support despite separately labelled stroke endpoints 2 vs 4; segmentation is not inferable from support. |
| S05 | EXPECTED_BLIND_SPOT | 1/64 gap is invisible at 33×33 (0 differing pixels) but yields 7 differing pixels at 257×257; raster resolution matters. |
| S06 | EXPECTED_BLIND_SPOT | Detached component leaves mean sampled support score ~0.002414; a separately supplied graph count produces a fixed 0.25 synthetic penalty. Not a selected Hebrew metric. |
| S07 | EXPECTED_BLIND_SPOT | Supplied graph distinguishes 2 vs 3 exposed endpoints and 0 vs 1 junction; support metric does not infer topology. |
| S08 | EXPECTED_BLIND_SPOT | Local 1/32 notch detected by sampled Hausdorff; threshold 0.05 conceals it; normalization affects score. |
| S09 | PASS | Traversal reversal and closed cyclic shifts work only when authorized; open cyclic shifts are not applied. |
| S10 | EXPECTED_BLIND_SPOT | Invalid/zero input handled explicitly; tiny nonzero graph edge retained, but inherited alignment's small-energy floor rejects tiny paths. |
| S11 | EXPECTED_BLIND_SPOT | Local search reports **0.4** near π, despite exact global minimum **0**; demonstrates local optimizer is **not** a global certificate. |
| S12 | PASS | Six signed/three unoriented tetrahedral viewing classes; roll alignment error ≤2.62e-16; roll does not add independent views under free SO(2). |

**Exact observed totals:** `5 PASS`, `8 EXPECTED_BLIND_SPOT`, `0 FAIL`, `0 NOT_EVALUABLE`.

The eight expected blind spots are **positive diagnostic results**, not certified capabilities. The data show why unlabeled curve support, pixel masks, and constrained local optimizers cannot automatically supply stroke topology, resolution-independent fidelity or global guarantees.

## 4. Single run, environment and preservation

The package's attempt and completion records consistently document **one registered invocation, zero retries**, return code **0**, start `2026-10-15T11:41:40.899646+00:00`, end `2026-10-15T11:41:41.746898+00:00`. The completed output has 14 records, no missing cases. Python was 3.12.14, `sys.flags.optimize=0`, NumPy 2.3.5, SciPy 1.17.0. Stdout and stderr are both empty, consistent with the frozen runner's normal behavior.

The submitted clean-worktree and staged-diff logs, the signed implementation commit, and the 12 hash-bound artifact comparisons all support **no registered implementation changes**, no commit or push, and synthetic-only execution. The A09 identity was checked in existing metadata without reading original image pixels. A09's actual snapshot was absent; no actual source-image byte-hash validation is claimed.

**Evidence boundary:** a package containing a single invocation and no retries is strong evidence for **one documented authorized run**, but cannot logically establish that no other execution ever occurred outside the submitted workspace. The negative statements about Hebrew-image access are supported by inspected implementation behavior, asset absence and supplied I/O logs; they are not a general operating-system audit.

## 5. Remaining documented coverage qualifications

1. The frozen controlled-regression log reports **1,281 passed, 2 deselected**. The two excluded source-image-dependent inherited tests are **not passes**, and the missing historical crop has not been repaired. The pilot execution did **not** rerun the inherited suite.
2. The frozen `AMENDMENT_QC.md` describes **59 DEV passes**, but the standalone `amendment_dev_checks.log` lacks the full completion summary (it contains 35 progress dots). This is a retained logging-evidence limitation. The prior independent implementation QC separately exercised 31 amendment tests; it does not convert the incomplete log into a completed 59-test log.
3. GPG key setup recorded a nonzero public-key import return code, but subsequent GPG `VALIDSIG` records for both commits and GitHub independent signature verification were successful. This is not a freeze blocker; preserve the return code as recorded rather than retrospectively rewriting it.
4. The registered S11 optimization demonstrates a *bounded local* success and a **global failure**; any later scientific optimization requires an independently justified global-search/verification strategy.
5. Synthetic straight polylines, graphs with provided labels and 2-D finite-width ink rasters are **not** equivalent to historically authenticated multi-stroke Hebrew target forms or a finite-width 3-D FIRST HAND shadow.

## 6. Decision against signed protocol §13

- A09 unique metadata identity: **PASS** (actual raw bytes absent and expressly nonblocking).
- Protocol and implementation frozen before pilot: **PASS**.
- All S00–S12 oracles/states preserved: **PASS**.
- Projection and relevant invariances checked against synthetic oracles: **PASS**.
- Representation limits and unobservable topology explicitly identified: **PASS**.
- Degenerate inputs and local-search limitations preserved: **PASS**.
- No regression *introduced by this execution*: supported by unchanged frozen code and inherited regression history; full regression rerun not conducted in this execution.
- At least one adequately characterized **synthetic ordered-curve projection/similarity path** suitable for designing a later protocol: **PASS**, subject to correspondence semantics, image/stroke representation and sampling policy.
- No Hebrew target analysis: **supported by the inspected boundary and preserved logs**.

**Authorized scientific-readiness classification:**

`P0A0_SYNTHETIC_ENGINEERING_PILOT_READY`

**Retained subsidiary findings:**

`P0A0_METRIC_PATHOLOGY_DOCUMENTED`

`P0A0_OPTIMIZER_NOT_CERTIFIED`

This classification closes **the synthetic engineering gate only**, not Hebrew target ingestion, metric selection, G0–G2 determination, N0–N3 null design, or confirmatory projection testing. Those decisions require a subsequent human-reviewed, GPG-signed protocol before accessing letter pixels or estimating letter matches.

## 7. Recommended preservation step

Preserve the immutable raw JSONL, original submitted ZIP checksum, case matrix, provenance, environment and the independent QC report in a **separate post-execution results freeze** on `hebrew-projection-capacity-v0.9`. Do **not** alter the frozen protocol, implementation sources, fixture config, case code, JSONL content or earlier logs. A human should review the exact staged paths before signing and pushing. After that, begin the next method/target-design protocol; do not run Hebrew matching or claim released v0.9.

**Review conduct:** read-only result/data validation only; no registered S00–S12 reexecution; no Git repository modifications, commits or pushes.
