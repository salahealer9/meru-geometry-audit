# P0A0 — Registered Synthetic Engineering Pilot: Results Freeze Closeout

**Project:** Meru Geometry Audit / v0.9 experimental-design line  
**Date of freeze-candidate preparation:** 2026-10-15  
**Status of this document:** RESULTS FREEZE CANDIDATE — becomes the human-approved results checkpoint only after a separately GPG-signed Git commit  
**Branch:** `hebrew-projection-capacity-v0.9`  
**Scope:** synthetic-only engineering execution and independent QC; **not** Hebrew target analysis

## 1. Immutable chain and execution identity

| Checkpoint | Identity |
|---|---|
| P0A0 scientific preregistration commit | `d15865167b4e3c454e398bd498d9d681103096f7` |
| Preregistered protocol Git blob | `0f8b663bfe2432685c9320a00c80fd6bcf436e38` |
| Human-signed implementation freeze commit | `24c00fc44e4d9d57adacd1e636e9e2d20d86a954` |
| Original agent execution ZIP SHA-256 | `5c1b371ddaa2803430705a87f6cba748f3f3cd929749f596a55e1cd53a387295` |
| Original raw registered JSONL SHA-256 | `4b4b27b0d5d9a95ffe864e2d2c83433be0ddd544b6122ebbea294857326817d6` |
| Original raw JSONL length | 12,052 bytes |

`original_execution_package.zip` in this directory is a byte-for-byte copy of the submitted source ZIP; its original upload filename was `p0a0_registered_synthetic_execution_QC_package(2).zip`. All source members were extracted without modifications; their original `SHA256SUMS`, `PACKAGE_INVENTORY.json` and recorded provenance remain intact. The additional `FREEZE_MANIFEST.sha256` hashes every other file in this results directory to guard the human stage/copy operation.

The registered runner's saved record contains one boundary header and exactly thirteen case records, S00 through S12 in order. The agent-supplied attempt and completion records document one invocation, zero retries, exit code 0. The evidence does not establish that no other run ever existed outside that environment.

## 2. Registered synthetic outcomes

| State | Count |
|---|---:|
| `PASS` | 5 |
| `EXPECTED_BLIND_SPOT` | 8 |
| `FAIL` | 0 |
| `NOT_EVALUABLE` | 0 |

No rejected or pathological case has been silently promoted to `PASS`. All eight blind spots remain visible in `CASE_MATRIX.md` and the immutable JSONL. Particularly consequential are stroke-label non-identifiability, finite raster resolution, detached-component and endpoint blindness in support-only metrics, sampling and local-feature sensitivity, a tiny-scale inherited alignment rejection, and an S11 **local objective of 0.4 against the analytic global optimum of 0**. Camera roll under free planar SO(2) does not increase effective projection-view capacity.

## 3. Independent quality control and decision

Independent QC of the submitted execution package on 2026-10-15 reports **42/42 read-only checks PASS**, including the original ZIP's hash/integrity, inner file checksums, frozen source identity, record completeness and representative oracle results. The independent report and machine verification are preserved unmodified in this directory.

The qualified engineering-only disposition is:

- `P0A0_SYNTHETIC_ENGINEERING_PILOT_READY`
- `P0A0_METRIC_PATHOLOGY_DOCUMENTED`
- `P0A0_OPTIMIZER_NOT_CERTIFIED`

These are **engineering-methodology findings**, not an alphabet-generation, statistical-specificity, historical-reconstruction or global-optimization certificate. No final Hebrew metric, viewing group G0/G1/G2 or null ensemble N0–N3 is selected by this freeze.

## 4. Preserved qualifications

- Two inherited image-dependent regression tests remained deselected in the previously frozen controlled regression (`1,281 passed, 2 deselected`); one historical missing crop remains unavailable. This execution did not re-run the inherited suite and cannot claim to have removed the limitation.
- A standalone inherited DEV log lacks its complete completion line; retain this as an evidence limitation despite independent amendment boundary checks.
- The initial public-key import recorded a nonzero return code; later GPG verification of protocol and implementation succeeded, as independently verified. Preserve, do not rewrite, the original key-setup record.
- The Meru A09 raw image snapshot was absent from the agent workspace; existing source metadata was checked, but A09 image bytes were not inspected, digitized, scored or downloaded.
- The single-invocation assertion, negative Hebrew-access assertion and protected-file preservation are supported by inspected submitted records and source behavior, not by an exhaustive host-level or historical audit.
- The P0A0 synthetic representations (ordered paths, supplied labeled graphs, planar stroke rasters) are not the historical 3-D hand/ribbon shadow or actual Hebrew targets.

## 5. Frozen preservation and next scientific boundary

Preserve all results and evidence as supplied; **do not** rerun S00–S12, edit the raw JSONL, change the earlier protocol, fixtures, scientific functions, numeric oracles, prior tests, or interpretation of a blind spot. The human results-freeze commit should add **only** this results directory and not modify prior tracked files. Any detected inconsistency after freezing is a separately documented QC amendment, not a silent edit.

The next permissible step is a *new* methodology/target-design preregistration for admissible representation, normalization, match metric, independent global-optimizer validation and actual G0/G1/G2 capacity levels. Separately preregister the A09 target-extraction convention and N0–N3 candidate-vs-null scientific protocol **before** any Hebrew pixels, source-derived letter traces or real-letter performance data are used.

**No P0A0 execution or new science is performed by preparing this freeze candidate.**
