# P0A3G-R2 — Exact Geometry Correction to H04 (Protocol-Only, Prospective Human-Signing Candidate)

**Project:** Meru Geometry Audit, v0.9 — Hebrew projection specificity/effective-viewing-capacity programme
**Prepared:** 2026-10-21
**Repository / branch:** `salahealer9/meru-geometry-audit` / `hebrew-projection-capacity-v0.9`
**Required direct parent of this correction:** `7de01ab2c90afe52dd763652a9eaffd2e9a2cff9`
**Original signed R2 protocol:** `docs/v0_9/p0a3g_r2_prospective_replication_and_independently_witnessed_source_lock_protocol_2026_10_21.md`
**Original R2 protocol Git blob:** `01cbd34f9000c50eb6810dcfd8d4dd27b6312992`
**Original R2 direct parent:** `0e86df64e30d081065bbeb75b6f53391e287f8f3`
**Expected human GPG fingerprint:** `D4EC014EEFCC90E619D2AA59A91239ABCF512130`
**Status before signing:** `P0A3G_R2_H04_CORRIGENDUM_UNSIGNED_NON_AUTHORIZING`
**Scope:** Add exactly this one Markdown document. Do not change, remove, reset or amend the bytes of any prior signed protocol, checkpoint or scientific record.

## 1. Stop condition and exact identified error

**No R2 engineering execution, candidate import, test invocation, dry run, or pre-execution C1 review release is authorized under the uncorrected H04 expectation.** Prior to any R2 activity, verify that this narrow correction has been human GPG-signed and pushed and that both signed documents have been read. If any R2 candidate invocation occurred before this corrective signature, preserve that activity as an incident and stop for explicit review; do not retroactively call it prospective under the correction.

The signed R2 protocol's Section 4, R2-H04 specified:

- `A = [(0,0),(3,0),(3,1)]`;
- original `B_old = [(0,0),(-3,0),(-3,-1)]`;
- claimed `B_old` was a reflection outside `SO(2)` and must have **strictly positive** `qO`.

That claim is **mathematically false**: `B_old = -A` at every vertex and thus at every corresponding arclength point. The matrix `-I` is rotation by 180 degrees with determinant `+1`, hence belongs to `SO(2)`. Since the paths are related by an allowed proper rotation, their separate centering/RMS-normalized curves admit `qO = 0` and a unique proper optimum. Requiring a positive score would wrongly reject the correct exact algorithm.

This error was found **after human-signing the original R2 protocol but before a reported R2 engineering run**. Preserve the original protocol unchanged; a later signature cannot erase the original authoring error. This additive correction is a prospective replacement of one H04 fixture and its predeclared expectation only.

## 2. Single binding correction — R2-H04 only

Replace **only** the R2-H04 fixture and expected result in Section 4 of the original R2 protocol, wherever restated in the later handoff or lock catalogue, with:

> **R2-H04 — Proper-rotation exclusion for a reflected open bend.**
> `A = [(0,0),(3,0),(3,1)]`,
> `B = [(0,0),(-3,0),(-3,1)]` (each coordinate a reduced rational with denominator 1).
> `B` is the reflection of `A` across the vertical axis, not an allowed proper-rotation image. The ordered noncollinear edge vectors of `A` are `(3,0)` and `(0,1)`; those of `B` are `(-3,0)` and `(0,1)`. No single `SO(2)` transformation can map both edge directions. **Expected:** valid exact certificate, `EXACT_UNIQUE_PROPER_ROTATION`, `qO > 0`; specifically, with the registered independent true-arclength centroid/RMS normalization and the signed sign convention,
> `alpha = -88/101`, `beta = 27/101`, `s = sqrt(8473)/101`, `qO^2 = 2 - 2*sqrt(8473)/101 > 0`, and `qO` is its positive square root. The independent reference must recompute this from the input rather than trust these asserted values. A zero-score certificate, a reflection-as-proper-rotation, or an incorrect exact score must be rejected. All raw streams must reconcile under the signed R2 fault and evidence policy.

Only **the sign of the final y coordinate of B**, from `-1` to `+1`, is changed. The original `A`, the 14 historical replication methods, H01–H03, H05–H06, run ordering, software/source-byte lock, runtime budgets, checkpoint gates, expected SHA identities, and the independence and no-retry constraints are unchanged.

If this corrigendum and the original R2 text differ, **the corrigendum takes precedence exclusively for H04**. The corrigendum must appear by exact identity in R2-C0 and R2-C1 provenance, external holdout construction source, expected-outcome catalogue, and the eventual independent-QC audit. The engineering agent cannot freely choose another H04 geometry.

## 3. Independent pre-execution exact fixture audit (NOT an R2 software test)

The following checks were done independently by algebraic integration of the **proposed input polygonal paths** over true normalized arclength. The candidate software and R2 test catalogue were **not invoked**; these are protocol-design checks, not registered R2 evidence. In the signed theorem convention, `alpha = integral B·A`, `beta = integral B·J(A)`, with separately centered/RMS-normalized A and B; `s = sqrt(alpha^2+beta^2)`, `qO^2 = 2-2s`.

| Supplement | Exact input/invariant audit | Correct registered expectation |
|---|---|---|
| **H01**, A `(0,0)→(2,0)→(2,1)`, B `(5,7)→(5,9)→(4,9)` | B is `J(A)+(5,7)`; `alpha=0`, `beta=1`, `s=1`, `qO^2=0`; positive RMS | Exact zero score, unique proper optimum |
| **H02**, A `(0,0)→(2,0)→(2,2)`, B `(0,0)→(0,0)→(1,0)→(2,0)→(2,2)` | Zero edge adds zero arclength; subdivision preserves the same ordered traversal; `alpha=1`, `beta=0`, `s=1`, `qO^2=0` | Exact zero score, unique proper optimum |
| **H03**, A `(-1,0)→(0,0)→(1,0)`, B `(0,1)→(0,0)→(0,1)` | Centered A is arclength-antisymmetric and centered B is arclength-symmetric; `alpha=beta=s=0`, `qO^2=2`. Each has positive RMS. Existing request ABI uses `OPEN_INTERVAL` traversal and does not prohibit coincident endpoint coordinates. | Exact all-rotation tie, identity canonical witness |
| **H04 original** | `B_old=-A`, an `SO(2)` rotation; `alpha=-1`, `beta=0`, `s=1`, `qO^2=0` | Original strictly-positive expectation **FALSE** |
| **H04 corrected** | Vertical reflection, positive path RMS; `alpha=-88/101`, `beta=27/101`, `s=sqrt(8473)/101` | `qO^2=2-2*sqrt(8473)/101 > 0`; unique proper optimum |

For corrected H04, the normalized arclength covariance of A before division by its total variance has `Var(x)=63/64`, `Var(y)=13/192`, and `Cov(x,y)=9/64`. Its determinant is `3/64 > 0`: the two-dimensional curve is not confined to a line. In particular, `8473 < 101^2=10201`, so `s < 1` and `qO > 0` rigorously. The identity is an exact consequence of the submitted coordinates; it is **not** an acceptable substitute for the later independent runtime check.

**H05 and H06**, which are *non-geometric* negative controls, were reviewed for prospective logic, **not executed**: H05 must detect an equal-length one-byte stream substitution against the original event digest; H06 must reject a post-signing canonical scope mutation via both independent test-only signature routes. Those controls and their signed exact requirements remain unchanged. Neither is evidence of production cryptographic authority.

## 4. Preserved boundaries and sequencing

All conditions of signed R2 Sections 0–7 remain mandatory: full independent signed-lineage retrieval, clean read-only Git checkout, exact byte-frozen 51-file P0A3G candidate (including the three mathematical kernels), historical G01 fixture checkout at detached `adacfdbc6efcca4922c8d087d029b67e9b0c5dc5`, environment identity, R2-C0 durable verification, then R2-C1 prospective source/test/fixture lock, user-accessible persistence, fresh retrieval and **hard STOP until the separate research chat has checked the real R2-C1 bytes**. No partial/full candidate invocation, smoke check or challenge preview before R2-C1 external reviewer release; one numbered attempt after a SHA-specific human release; no retry or repair. A corrupt or unavailable lock must stop, not encourage improvisation.

No actual human code authority, loaded-code attestation, global software readiness, P0A4, Hebrew-specific or 3D/QH validation is implied by this mathematical correction or by any future bounded R2 DEV outcome. The negative R1 and P0A3G QC records remain immutable and separate.

**Human-only registration:** review this complete prospective correction; require a clean Git branch whose HEAD is exactly `7de01ab2c90afe52dd763652a9eaffd2e9a2cff9`, and independently verify expected GPG fingerprint. Stage only this new file; check downloaded SHA-256, Git blob and `git diff --cached --check`. Human alone `git commit -S`, verify the new commit's direct parent, raw GPG signature and signer fingerprint, and push the feature branch. Do not rewrite or amend the previous signed R2 commit. Only after the new signed amendment has been independently verified may the execution handoff be issued.

**Status if signed:** `P0A3G_R2_H04_EXACT_GEOMETRY_CORRIGENDUM_REGISTERED`; the original mistaken H04 text remains preserved as historical evidence and is superseded **only** for a still-future R2 replication.
