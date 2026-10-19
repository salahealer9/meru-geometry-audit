# P0A3C — Independent QC of cumulative implementation candidate

**Date:** 2026-10-19  
**Project:** Meru Geometry Audit / v0.9  
**Disposition:** **PASS — archive integrity, immutable lineage retention, bounded DEV reproducibility. PARTIAL — mathematical implementation; full readiness NOT QUALIFIED.**  
**Decision:** `P0A3C_IMPLEMENTATION_INCOMPLETE` and `P0A3C_INDEPENDENT_CHECKER_UNQUALIFIED`. **Do not assign** `P0A3C_FINITE_CAMERA_IMPLEMENTATION_READY_FOR_REGISTERED_TARGET_FREE_CERTIFICATION`. No P0A4 authorization or human freeze is implied.

## 1. Submitted archive and package integrity

Input `P0A3C_cumulative_implementation_candidate(1).zip` is **4,072,330 bytes**, SHA-256:

`4d327ac4cf057598d3377b93c9a22ed19bd69d3ef2dd1d59242d9001c3db3bbe`

Independently checked: **249** ZIP entries; **12,522,452** uncompressed bytes; all CRCs pass; no duplicate names, absolute/traversal names or ZIP symlinks; **248/248** SHA256SUMS entries match and cover every archive entry except their own manifest; **247/247** payload inventory file lengths and hashes match. No image or font file type is present. Inventory exclusions are declared and normal self-hash handling is explicit. The package is a *candidate*, not an automatically approved repository tree.

## 2. Frozen history and immutable preservation

Signed P0A3C preregistration independently checked on GitHub: commit `01270ec3bff3c9a6352c5dadc90d5d9f12da0c0d`; protocol blob `1a54a5c0626d329e1c7389ca389a907139b8413f`; direct parent `8adbc226b1ef7234a9bedab02ca515a6c11e5c4f`; valid GitHub signature, and verified remote branch tip at this commit during review. The ten signed commit IDs from P0A0 through P0A3C were independently checked using GitHub for valid signatures and correct adjacency. The author's exact local GPG signature transcript and further tree-reconstruction claims were inspected but **not independently rerun end-to-end** in this QC. The embedded P0A3C protocol's Git blob was independently recomputed from bytes and matches the signed blob. The embedded preservation plan and closeout also match their pinned Git blobs.

Inner preserved archives match the frozen identities:

| Preserved archive | SHA-256 verified |
|---|---|
| Original P0A3 focused cumulative candidate (116 entries) | `5afa2c146d8fa2b5e77e55590dc12ec578d495ecf9a94aa1f94d3aee16b7b80d` |
| 2026-10-18 independent QC archive | `ec9d816f17dd00cd0ea81e7195f218f02beee260dc8a8c8ff687aeade36b0568` |
| Earliest P0A3 implementation candidate | `079c74ce69b9b94e26ccb346aadc4d1351922921774f7120e9db79e9f320835a` |
| First independent QC archive | `df0b46479f58109e882e9a7a92d1dc1d8fd3f0aafa8d557f09b688abd841bf12` |

Compared against the preserved 116-entry baseline: **zero paths missing**, and **113 byte-identical copies** at the top-level archive; the three changes are precisely `README.md`, `PACKAGE_INVENTORY.json`, and `SHA256SUMS`. Thus **no earlier source/reference/test file was rewritten** in the top-level copies. The complete earlier original is also preserved inside the nested ZIP. The signed incomplete-checkpoint `FREEZE_MANIFEST.sha256` matches all six preserved companion files in their relocated package directory.

Historical DEV attempts 01–06 and their failure/correction records remain. The agent's attempt 07/08 logs record success in the same prospective 22-test suite; 07 omitted a separate dump of in-memory numerical task records, a correction disclosed before attempt 08. This is an evidence-retention correction, not proof of numerical correctness or a new mathematical failure.

## 3. Independent bounded DEV reproduction

Run only the **newly registered P0A3C DEV microcontract suite**, in an isolated extracted copy (`src/`, `reference/`, `tests/dev_v0_9/` only). No frozen P0A0 S00–S12 evaluator or scientific benchmark was executed.

`PYTHONPATH=src:. PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 LC_ALL=C.UTF-8 python -B tests/dev_v0_9/test_p0a3c_microcontracts.py`

Observed exit code **0**; **22 tests / 22 passed**, 0 failures/errors. Limits: 60-second subprocess timeout and 1 GiB address-space rlimit; the run completed in approximately 0.21 s. Independent stdout/stderr logs are attached. The 22 cases cover intervals, exact duplicates, positive/zero projected extent, A/B exact direction manifests, proper lifts, canonical task lists, four QO/QH component examples, forged-score rejection, external request pin rejection, incomplete and reordered checkpoint rejection, resume, boundary fault injection, bad JSON, sticky failures and request/size limits. This is a **DEV reexecution of 22 cases**, not a new 22-case scientific study, P0A4 certification or 44 independent test cases merely because attempts 07 and 08 both passed.

## 4. Independent mathematical and implementation review (B01–B08)

| ID | Independent outcome | Grounds and remaining gap |
|---|---|---|
| **B01 — QO** | **PARTIAL** | `p0a3c_geometry.path` and `p0a3c_scores.qo` use rational outward interval operations to enclose irrational algebraic camera/arclength quantities; the separate `p0a3c_oracle` integrates by a distinct global-polynomial route. The correlation/roll objective is derived correctly in the frozen mathematical specification. But fixed-precision intervals do not decide arbitrary exact-zero correlations/ties or always supply a proved attained witness and complete branch comparison on the mandatory eligible domain. |
| **B02 — QH** | **PARTIAL** | Rational numerator/algebraic camera projection, exact distinctness/empirical variance, outward normalized point boxes and two-way nearest-distance bounds exist. Reference `qh` independently reconstructs pair extrema using a different expression. Uniform near-degenerate eligibility, arithmetic backend qualification and all mandatory finite-precision cases are not established. |
| **B03 — full planar-roll domain** | **PARTIAL** | Four quarter-circle half-angle charts, wraparound identities, exhaustive prospective camera/cell manifest, and fixed-view Lipschitz lower-bound architecture are represented. One-cell DEV work/checker passes. **No completed entire-circle×all-camera numerical evaluation or independent registered certificate** is present. Timeouts/unsupported cells must block completion, not be omitted. |
| **B04 — A/B directions** | **PARTIAL** | Exact signed sets 6/14/26 and 6/18/42, canonical integer triples, independent symbolic frame identities and camera projection paths exist. The 22-test suite exercises selected nonaxial frames. All-camera **uniform** enclosure/degeneracy correctness and implementation qualification remain unresolved; SEP/COV and continuous-camera Lδ are separate deferred obligations. |
| **B05 — independent checker** | **PARTIAL/UNQUALIFIED** | `reference/v0_9/p0a3c_oracle.py` implements separate outward interval operations; `p0a3c_checker.py` recomputes selected original-input QO/QH results, witnesses, cell lower bounds and complete task partitions. Static reference imports do not directly import production numerical modules. However both rely on CPython/Fraction assumptions; reference-width containment can remain inconclusive; exact QO degeneracies and full-domain checker qualification are incomplete. Caller-created `live_pins()` is a DEV input, **not** an externally frozen trust anchor. |
| **B06 — resume/resource** | **PARTIAL** | Canonical pending/completed/failure partition, request and code identities, independent recomputation on load, same-directory atomic replace, flush and fsync, and controlled BEFORE/AFTER_REPLACE faults exist. Single-writer only; no tested hard kill/power failure; no enforced production runtime/bit-growth/memory cap; a completed result need not be automatically checkpointed before interruption. |
| **B07 — source/target observations** | **UNRESOLVED, separately gated** | Rights, actual chart extraction, independently justified ordered paths/graph semantics, missing three historical functions, shaping and physical shadow law remain unknown. |
| **B08 — controls/inference** | **UNRESOLVED, separately gated** | Actual source-constrained candidates and N0–N3 laws, matched model complexity/operational budgets, primary metric/tier, detectability and fixed-corpus inference are not selected. |

The delivered B01–B08 table has eight populated, unique rows and retains these limits; the requirements-to-code table has 24 populated rows, and independent-reference table six populated rows. **QO_A, QO_B, QH_A, QH_B remain incomplete on the mandatory full finite-camera engineering domain.** Mere presence of a generator, interval object or checker file does not prove a full mathematical numerical contract.

### Specific technical cautions

1. Fraction-backed rational interval operators provide *candidate enclosures*, but exact/proved distinctions at zero, ties and positive normalization thresholds require stronger predicates or independently demonstrated terminating refinement. Neither full-domain attainability/witness evidence nor a uniform resource envelope follows from the passed examples.
2. A full task manifest and midpoint cell calculation are not a complete verified numerical execution; the QH bound `f(theta) >= f(mid) − rho * angular_radius` still depends on valid normalization, a proved angular-radius bound and correctly outward-enclosed inputs for **every** cell. The implementation's four-chart mathematics is a prospective route, not a run result.
3. Although the checker uses different local numerical kernels for relevant computations, `live_pins()` itself cannot establish signed code trust; independent externally checked source/config identities are required before certification. No verification of hostile or dynamically imported code paths is claimed from static AST inspection alone.
4. B06 fault injection verifies two local save boundaries but does not prove real process-kill recovery or arbitrary-size resource safety.
5. The source contains no static image/font artifact and the audited DEV script uses generic rational coordinates, which is consistent with the information barrier. This is an inspected-evidence conclusion, not a claim to have audited every operation on the agent's host.

## 5. Final decision and controlled next step

**Independent QC:** `PASS_INTEGRITY_AND_BOUNDED_DEV`; `P0A3C_IMPLEMENTATION_INCOMPLETE`; `P0A3C_INDEPENDENT_CHECKER_UNQUALIFIED`; `P0A3C_GLOBAL_NUMERICAL_CERTIFICATION_DEFERRED`. Retain `P0A3C_CONTINUOUS_CAMERA_COVERAGE_DEFERRED`, `P0A3C_HISTORICAL_OBSERVATION_UNRESOLVED` and `P0A3C_CONTROL_FAIRNESS_UNVERIFIED` as applicable.

**DO NOT ASSIGN:** `P0A3C_FINITE_CAMERA_IMPLEMENTATION_READY_FOR_REGISTERED_TARGET_FREE_CERTIFICATION`, `GLOBAL_CERTIFIED`, or a registered `BOUNDED_APPROXIMATION`. **DO NOT authorize P0A4 or access Hebrew targets** from this package.

**Recommendation:** preserve the cumulative archive and this QC byte-for-byte under a **human-signed, explicitly incomplete checkpoint**, without installing its unqualified candidate code into live production `src/`. Since repeated broad completion attempts remain partial, the following protocol should either (a) target one mathematically separable proof/certification gap with finite acceptance criteria, or (b) explicitly narrow the implementation model to a well-defined, independently certifiable restricted domain and separately preregister its target-free validation. Neither option waives target rights, candidate/control fairness or the historically missing physical-shadow model.

No signed implementation freeze is prepared or executed by this QC. All further engineering and registered numerical work requires the appropriate human gate.
