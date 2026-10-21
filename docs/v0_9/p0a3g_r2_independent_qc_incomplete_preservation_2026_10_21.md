# P0A3G-R2 — Additive Preservation of Independent QC and Original Evidence (Human Signing Candidate)

**Prepared:** 2026-10-21. **Repository:** `salahealer9/meru-geometry-audit`. **Branch:** `hebrew-projection-capacity-v0.9`. **Required direct parent:** `4b488825ed35c7ac91a19abe62be068e75e9a076` (signed R2 H04 corrigendum). **Signer fingerprint:** `D4EC014EEFCC90E619D2AA59A91239ABCF512130`. **Git authority:** human review and `git commit -S` only; no agent commit/push. Status **UNSIGNED HUMAN CANDIDATE until verified, signed and pushed**. Freeze is purely additive: exactly eight files; no modifications of existing protocols, implementation source or historical evidence.

## 1. Exact antecedent and execution authority

- Signed R2 preregistration: `7de01ab2c90afe52dd763652a9eaffd2e9a2cff9`, blob `01cbd34f9000c50eb6810dcfd8d4dd27b6312992`.
- Signed binding H04 correction: `4b488825ed35c7ac91a19abe62be068e75e9a076`, blob `780fc70a11081fda4fa2aedc56bb2cab84e7fa3c`.
- Independent original first-lock rejection: R2-C1 SHA-256 `740da6990834846a579cc07dccdafcab23f147c5f00117c25505a1cbce847589`, not executed.
- Independently witnessed and human-released lock: R2-C1-REV1 SHA-256 `b34a3cd2c27f9384adb7427fa6628d6c08e15712e73542bda80eaeef989009b1`.
- One reported authorized attempt `P0A3G_R2_DEV_01`, 2026-10-21 15:35:48Z–15:36:46Z. A 14/14 G result, G decision `PROCEED_TO_H`, and a 6/6 H result are retained. No reviewer-run candidate execution.

All predecessor negative findings remain immutable: R1 raw stdout evidence loss, and the original P0A3G pre-lock full-suite execution violation. The P0A3D exact SO(2) theorem and three mathematical kernels are unchanged.

## 2. Original evidence preserved

The checkpoint in `reports/v0_9/p0a3g_r2_independent_qc_incomplete_checkpoint/` stores **byte-identical original supplied ZIPs** and the separate independent QC report/scripts/data, with cryptographic identities in `QC_INCOMPLETE_PRESERVATION_MANIFEST.sha256`:

| Object | Original SHA-256 |
|---|---|
| R2-C0 | `e99811f3eefd90a49726e9ea37d8eae8b739829cc90bc825f3dec489d731bbb5` |
| R2-C1 REJECTED (never executed) | `740da6990834846a579cc07dccdafcab23f147c5f00117c25505a1cbce847589` |
| R2-C1-REV1 (witnessed/released) | `b34a3cd2c27f9384adb7427fa6628d6c08e15712e73542bda80eaeef989009b1` |
| R2-C2 | `860d93dce952a73b65b097e3f7b4da420c0a327ee0ca8b6d4c213865db2d1cbb` |
| R2-CFINAL | `7c9770d15a3a578f61def2571813d84baadda34bfe3d31cfc1b5cdd722a51eb4` |

All actual uploaded archives pass CRC, full non-self SHA256SUMS and PACKAGE_INVENTORY validation. CFINAL contains byte-identical nested copies of C0, released C1-REV1 and C2 plus the original rejected C1. The exact original signed P0A3G G-CFINAL candidate 51-file tree matches all R2 source files; the seven external R2 files also match their witnessed lock; 1,270/1,270 attempt manifest entries match, no missing/unlisted files.

## 3. Independently supported new engineering evidence

- G evidence: 111 worker events / 222 streams; 199 fully matching raw streams and identity records, 21 registered fault-injection stream/identity records and 2 separately marked foreign-event harness identity records; five additional declared orphan/pending files; **zero unexplained**.
- H evidence: 28 events / 56 exact stream matches, **zero unexplained**.
- Corrected H04 exact invariants `alpha=-88/101`, `beta=27/101`, `qO^2=2-2*sqrt(8473)/101>0` agree with the signed mathematical correction, and three forged certificates are rejected.
- Independent Ed25519 public-key verification of the retained H06 **test-only** authority: original envelope verifies; one-byte scope-modified envelope fails verification. No real human-signed code authority exists.
- Twenty registered methods have retained PASS verdicts (14 G + six H). The independent QC did not rerun the candidate. All claims are bounded to the registered host and test-only authority envelope.

## 4. Signed-protocol completeness defect and QC disposition

**Blocking finding: `R2_QCF01_C2_PRIOR_RECEIPTS_OMITTED`.** Original signed R2 protocol Section 5 explicitly required **R2-C2 itself** to contain the untouched prior checkpoint receipts. Independent inspection of the original R2-C2 ZIP confirms they are absent. The executing agent disclosed that omission and did not overwrite C2. The missing copies exist intact in later R2-CFINAL `receipts/`, but cannot retrospectively satisfy the original C2 checkpoint's mandatory completeness gate. This is a *packaging/chronology failure*, not evidence of a false accepted certificate or a mathematical contradiction.

**Overall:** `P0A3G_R2_INDEPENDENT_QC_NOT_FULLY_QUALIFIED`; separate `P0A3G_R2_BOUNDENVELOPE_REPLICATION_EVIDENCE_SUPPORTED` and `P0A3G_R2_C2_PRIOR_RECEIPT_COMPLETENESS_NOT_QUALIFIED`. No success label can imply complete signed protocol compliance. Historical P0A3G and R1 negative findings remain immutable.

No production code freeze, no real external trust-root approval, `LOADED_CODE_IDENTITY_UNVERIFIED`, no hostile host/power-loss/multiwriter guarantee or arbitrary-input proof. **P0A4 remains NOT RUN and NOT AUTHORIZED**, as do Hebrew targets, candidate/null tuning and QH/3D extensions.

## 5. Decision / future authority

This preservation records both the substantial test success and the exact incompleteness. It makes **no code change and grants no new execution authority**. Do not repackage or rename the original published C2 as if it contained receipts. Any administrative supplement may cross-reference the retained receipts but must not rewrite its history. A future strict overall qualification needs a separate prospective authority and appropriately witnessed checkpoint conditions. Independent QC is not a substitute for human signature or an actual code-only freeze.

**Status until signature:** `P0A3G_R2_INCOMPLETE_QC_PRESERVATION_UNSIGNED`. The human alone may verify all file identities and decide whether to sign this exact additive preservation.
