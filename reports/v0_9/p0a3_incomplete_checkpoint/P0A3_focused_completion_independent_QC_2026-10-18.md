# P0A3 — Independent QC of focused completion cumulative candidate

**Date of review:** 2026-10-18  
**Project:** Meru Geometry Audit, v0.9 Hebrew projection-specificity/effective-capacity line  
**Disposition:** **INTEGRITY PASS; BOUNDED ENGINEERING QC PASS; FULL IMPLEMENTATION READINESS NOT QUALIFIED.**  
**Scientific/protocol status:** `P0A3_IMPLEMENTATION_INCOMPLETE`; `P0A3_TARGET_BLIND_IMPLEMENTATION_READY_FOR_REGISTERED_CERTIFICATION` **must not be assigned**.

## 1. Submitted identity and scope

Submitted file: `P0A3_focused_completion_cumulative_candidate(1).zip`.

- File bytes: **1,315,235**.
- SHA-256: `5afa2c146d8fa2b5e77e55590dc12ec578d495ecf9a94aa1f94d3aee16b7b80d` — independently recomputed and matched.
- ZIP: **116 entries; 4,227,634 uncompressed bytes; CRC PASS**; no duplicate paths, traversal paths or ZIP symlinks found.
- Internal `SHA256SUMS`: **115/115** hashes valid (all entries other than `SHA256SUMS` itself).
- `PACKAGE_INVENTORY.json`: **114/114** payload byte sizes and SHA-256 identities valid; metadata excluded from the payload as documented.
- Nested original implementation ZIP: SHA-256 `079c74ce69b9b94e26ccb346aadc4d1351922921774f7120e9db79e9f320835a`, byte-identical, original nested ZIP CRC PASS and 73 entries.
- Nested original independent QC ZIP: SHA-256 `df0b46479f58109e882e9a7a92d1dc1d8fd3f0aafa8d557f09b688abd841bf12` — exact retained identity.
- Cross-comparison with the original ZIP: **69** original paths remain byte-identical as top-level copies; **four** changed paths are the root README, inventory, manifest and append-only `dev_commands_and_results.log`; no original path missing. Original log retained as a byte-exact prefix. Original archive separately preserves all 73 files in their former layout.
- Historical DEV attempt 01–04 records, their prior-source snapshots, exit statuses, stderr/stdout logs and fixes remain intact; all six attempt-result log hashes verified. Attempts 05 and 06 are additional and retained, not substituted for earlier evidence.

## 2. Frozen authority and identity

Pinned branch: `hebrew-projection-capacity-v0.9` in `salahealer9/meru-geometry-audit`.

- Human-signed P0A3 protocol commit: `2425db592e80d5f688adc0facdea9e1042c05cdb`.
- Direct parent/P0A2 results freeze: `07b64003940072e00fb2ce969ebc3866a9a3dc4d`.
- P0A3 protocol blob: `38106180f7b2855992b70c925d64169dee0213ca`.
- GitHub independently returned the signed commit with `verification.verified=true`, exact parent and one added 214-line protocol file; remote branch pointed to this signed commit at review time.
- **20/20** pinned source Git blobs named in the continuation provenance record were independently re-fetched at the signed P0A3 commit and matched; embedded copies of the protocol, P0A2 decision closeout and P0A2 QC report also hash to their signed blob identities.
- Prior staged/frozen files were not edited by this QC; the repository itself was not checked out or modified. The agent's no-repository-write and no-target-exposure statements are consistent with the submitted evidence, but cannot establish universal host-wide absence of operations.

## 3. Independently executed bounded DEV verification

Only the revised, new DEV microcontract script was run in an isolated extracted package, not P0A0 S00–S12, any scientific benchmark or any candidate/null comparison:

```sh
cd /mnt/data/p0a3_cumulative_independent_qc/isolated
PYTHONPATH=src:. PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 LC_ALL=C.UTF-8 \
    python -B tests/dev_v0_9/test_completion_microcontracts.py
```

**Observed 21/21 passed; 0 failures; exit 0; 0.032 s** on the QC host. The full independent log is preserved in the companion QC package. This **does not** constitute registered numerical certification. The original 42-test suite was not rerun in this continuation; its passed result is retained as an earlier independently reviewed checkpoint, not claimed as a fresh run here.

Static AST parsing of all **22** delivered production/reference/DEV Python files succeeded. No `reference/v0_9` Python module statically imports `meru_geometry`, and no candidate Python module statically imports `registered_pilots`/`p0a0`. This is a source-level dependency check, **not** a proof of all possible dynamic runtime behaviour or wholly independent trust bases.

## 4. Mathematical and implementation review

**B01 — QO rational enclosures: PARTIALLY ADDRESSED.** `qo_exact_candidate.py` implements an exact-rational subdomain with rational **segment lengths**, endpoint polynomial integration, branch correlation/tie comparison, outward square-root score enclosures and a symbolic attained rotation. The separate `qo_rational.py` uses global-parameter antiderivatives rather than production's endpoint-product accumulation. `numerical_checker.py` independently recomputes branches, objective enclosures and the witness. It explicitly rejects irrational-length paths. This is **not** a general algebraic or all-camera QO implementation; no general exact/interval certificate is established.

**B02 — Fixed-pose QH enclosures: PARTIALLY ADDRESSED.** `exact_bounds.py` computes normalized finite-set Hausdorff enclosures for rational coordinates and **rational unit-angle pairs**, including optional explicit mirror, with exact-rational outward root intervals. The independent `qh_exact.py` checks distances and extrema through exact quadratic-surd sign comparisons, and `numerical_checker.py` checks proposed objective and scale bounds against rederived geometry. Arbitrary numeric angles/inputs, uncertain observational measures and general G1/G2 algebraic observations are unsupported. Wide valid enclosures alone do not imply a useful optimization gap.

**B03 — Whole-circle QH: PARTIALLY ADDRESSED.** The `qh_circle_candidate.py` module defines four rational quarter-circle charts using `2 atan(t)`, dyadic cells, a Lipschitz cell lower bound and finite per-cell witness upper bounds. The independent checker reconstructs the expected cell plan and recomputes completed-cell numerical witnesses and bounds. A G0 SO(2) level-zero plan has 24 cells; the new DEV suite checks one cell and an incomplete/resumed plan. **No entire circle has been numerically evaluated or certified**, and no `BOUNDED_APPROXIMATION` or `GLOBAL_CERTIFIED` status is authorized. The caller's `epsilon`, precision and level are still unselected engineering inputs.

**B04 — Frames/capacity: PARTIALLY ADDRESSED.** Exact integer-triple formulae and outward entries for canonical proper frame lifts are implemented and independently checked. G0 axis projections are exact rational operations. Rigorous end-to-end propagation of G1/G2 frame error through normalization and the score, exact SEP/COV coverage certificates, and continuous-sphere `Lδ` guarantees remain absent. Exact finite family enumeration does **not** make G1/G2 implemented numeric comparators or final experimental tiers.

**B05 — Oracle independence: PARTIALLY ADDRESSED.** Separate production and reference arithmetic/integration/pair-distance/generator methods exist; reference does not import production numerical kernels. Both still depend on Python/Fraction and mathematical definitions; the restricted independent checker itself requires future independent source QC and registered numerical testing. Whole-domain oracle independence is not established.

**B06 — Checkpoint/interruption: PARTIALLY ADDRESSED.** External expected request, canonical manifest, request hash, complete pending-cell suffix, recomputed completed witnesses, sticky failures and a disallowed-certification status check are implemented; atomic checkpoint save performs file/directory fsync. The 21-test DEV suite rejects forged payload/status and missing cells. Hard preemption inside a cell, resource/bit-growth guarantees, actual crash recovery and a completed resumed circle remain unqualified. Hash-shaped production/reference/configuration/resource pins are **not cryptographically trusted merely by syntax**; an external frozen-byte provenance check is required before certification.

**B07 — Target observations/rights/optics: UNRESOLVED**, properly not invented. Source-guided Meru final shaping and historical physical-shadow law are absent, as are validated Hebrew target order/graph observations.

**B08 — Controls/design choice: UNRESOLVED**, properly retained. No final QO/QH primary metric, G1/G2 design, N0–N3 control laws, common operational budgets, detection threshold, sample counts or confirmatory statistic is frozen.

All four `QO_A`, `QO_B`, `QH_A`, `QH_B` products remain `GLOBAL_CERTIFICATION_DEFERRED`; their complete documented model domains are not implemented/certified. The rational G0-only work is valuable but cannot be relabeled full-domain qualification.

## 5. Negative findings and retention

No evidence within the inspected package of target pixels, extracted/proxy Hebrew glyphs, candidate-versus-null execution, registered P0A0 replay or agent commit/push. No new source-file image bytes were fetched for the independent QC. Inherited missing historical crop, two image-test exclusions, earlier incomplete DEV log, P0A1 interruption/reconstruction provenance, GPG-agent caveats and absent A09 raw-image verification remain unresolved and unchanged.

**No P0A3 information-barrier or provenance mismatch found in the material examined.** This finding is limited to available artifacts/operations, not a universal impossibility claim.

## 6. Decision and next authority

**Independent QC disposition:** `PASS_INTEGRITY_AND_RESTRICTED_ENGINEERING`; `P0A3_IMPLEMENTATION_READINESS_NOT_QUALIFIED`.

Preserve this cumulative ZIP, its original nested package and both QC layers unchanged. **Do not sign a certification-ready implementation freeze or authorize P0A4 registered execution from this package.** An optional human GPG-signed, explicitly **incomplete** engineering preservation freeze could record the current partial state without assigning the protocol's positive readiness status or authorizing further runs. Alternatively keep the package under review while separately scoping further completion. Neither option should silently change signed P0A0–P0A2 evidence.

For the next bounded completion, prioritize: (1) general algebraic/interval QO lengths and all-camera propagation; (2) rigorous G1/G2 QH camera projection/normalization enclosures; (3) full independent numerical checker for those domains; (4) interruption/resource controls with complete evidence; (5) a separately signed and independently reviewed target-free registered certification plan, **after** code-only freeze. The P0A3 protocol permits small engineering DEV checks, not a substitute for that registered validation. If full implementation proves impracticable, freeze the incomplete status explicitly rather than repeatedly extending unbounded development or claiming certification.

**No final P0A3 freeze, full-domain numerical certificate, actual Hebrew score or source-specificity conclusion is approved by this QC.**
