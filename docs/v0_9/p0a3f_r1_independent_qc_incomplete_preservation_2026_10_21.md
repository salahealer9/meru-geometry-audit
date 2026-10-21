# P0A3F_RECOVERY_R1 — Independent QC Incomplete Preservation (HUMAN-SIGNING CANDIDATE)

**Project:** Meru Geometry Audit, v0.9 — Hebrew projection capacity research line
**Prepared:** 2026-10-21
**Branch:** `hebrew-projection-capacity-v0.9`
**Status before signing:** `R1_INDEPENDENT_QC_INCOMPLETE_PRESERVATION_CANDIDATE_NON_AUTHORIZING`
**Required direct parent:** `83b9e6dcd53b100c5ac8b081832e81659cd1884a`
**Expected human GPG signing fingerprint:** `D4EC014EEFCC90E619D2AA59A91239ABCF512130`
**Purpose:** Additive, immutable preservation of the original P0A3F_RECOVERY_R1 working checkpoints and independent QC negative outcome; **not** an amendment granting further engineering execution, a code-only freeze, or numerical/scientific validation authorization.

## 1. Authority and scope

This record depends on and does not alter:

- Signed exact mathematical theorem freeze P0A3D: `59eb47f7500d57866e4935822b78a555d3bcb515`.
- Signed P0A3E incomplete implementation checkpoint: `8ed3b988f716229bc9aee97d41ded0f524371193`.
- Signed P0A3F original protocol-only preregistration: `1d38ea6f53b9266d853df887a66331c59e4fc3ae`, protocol Git blob `9530a75d2346752a093367aeac24e13c5d2d6fac`.
- Signed P0A3F evidence-loss and narrow R1 recovery amendment: `83b9e6dcd53b100c5ac8b081832e81659cd1884a`, amendment Git blob `9fd9fba6ca509e3fcb72c2227d226847d218b354`.
- Expected signer fingerprint `D4EC014EEFCC90E619D2AA59A91239ABCF512130`.

This preservation decision was independently assessed after Work completed the separate prospective recovery lane `P0A3F_RECOVERY_R1` on 2026-10-21. The Work engineering candidate was **unsigned** and was submitted for independent QC, not self-approved. This QC report is itself unsigned independent review evidence until the human signs the additive preservation commit. A signed preservation commit documents the disposition, not positive verification of executable software.

## 2. Authentic original evidence preserved in this additive checkpoint

Exactly four **unchanged** retrieved R1 checkpoints and the **unchanged** independent QC package accompany this document. Check the manifest in the same directory and the Git binary blobs before signing.

| Evidence | Exact bytes | SHA-256 |
|---|---:|---|
| `reports/v0_9/p0a3f_r1_independent_qc_incomplete_checkpoint/original_P0A3F_RECOVERY_R1_R1-C0.zip` | 1,790,515 | `0487dcebb13e56cb49cb51886dae2ad0a673c023bf66b52084e7756a42c2f60d` |
| `reports/v0_9/p0a3f_r1_independent_qc_incomplete_checkpoint/original_P0A3F_RECOVERY_R1_R1-C1.zip` | 1,858,394 | `19b34f8d691e2ea3b127a6b2b8a16d4d9d5e925f47802094b4851b2c9644c812` |
| `reports/v0_9/p0a3f_r1_independent_qc_incomplete_checkpoint/original_P0A3F_RECOVERY_R1_R1-C2.zip` | 2,131,186 | `f18a32551d30b8b89f8eb85242e431c8fbb1cf213903aa5710da19fab8b320f7` |
| `reports/v0_9/p0a3f_r1_independent_qc_incomplete_checkpoint/original_P0A3F_RECOVERY_R1_R1-CFINAL.zip` | 2,165,809 | `6ec2b6e96234836d629398fb7fc781909de8b47b0bf80f5cae11202620ff2f15` |
| `reports/v0_9/p0a3f_r1_independent_qc_incomplete_checkpoint/original_P0A3F_RECOVERY_R1_INDEPENDENT_QC_2026-10-21.zip` | 13,000 | `aa810c66ac6454a1d04a30cc597612b61006bca0dc7d5c3340726efa4a6cf305` |

The four original ZIPs were each independently retrieved and verified for CRC, unique safe entries, internal checksum manifests and inventory entries. For C0/C1/C2/CFINAL respectively: member counts 133/169/392/408; non-self hash entries 132/168/391/407; payload inventory entries 131/167/390/406. This establishes integrity of the bytes **as retained**, not necessarily agreement of all retained bytes with each original worker event record. The separate original P0A3E cumulative baseline (968,965 bytes, SHA-256 `1e73c2685bd4eb8fba89e4e8ea609e97c7b4716805e83c64af374a4265522ea8`) remains under its earlier signed checkpoint and is not modified here.

## 3. R1 engineering execution — what is and is not established

- One separately numbered prospective engineering attempt: `P0A3F_R1_DEV_01`. Its preserved test log reports **18/18** methods passed, four generic comparison fixtures, test-runner exit code zero and no source repair or second R1 DEV attempt.
- The source/test/config/fixture lock was preserved at R1-C1 before DEV; the independent review matched all 29 tracked code/test/schema files and 12 fixture bytes to the executed source snapshot and cumulative candidate.
- Stale-saved-verdict recovery was reported via an independent fresh checker in approximately **0.317110196 seconds** within the predeclared eight-second deadline. A separate actual eight-second timeout was reported as `RESOURCE_INCOMPLETE` with child exit code **−9** and no successful completed certificate.
- The three byte-frozen original P0A3D/P0A3E mathematical kernels are byte-identical in R1. The P0A3D abstract exact 2D QO theorem remains separately independently verified. No target-derived historical Hebrew claim or new registered validation follows from generic DEV.

**Qualification is not granted by the 18/18 runner summary.** An independent reviewer identified a blocking discrepancy in the raw worker evidence.

## 4. Independent QC finding QCF01 — HIGH; incomplete raw evidence

In `P0A3F_R1_DEV_01`, 37 recorded worker events contain 74 stdout/stderr stream identity records. Independent recomputation found **72/74 matches** and exactly **two mismatches** in stdout streams for the hostile certificate cases `forged_q` and `null_path_record`.

| Event case | Recorded stdout bytes | Recorded SHA-256 | Original archived stdout bytes | Archived SHA-256 |
|---|---:|---|---:|---|
| `forged_q` | 108 | `23bcfd677effd3a3b5ff73bfce72328c0bd19148a79617be8b896a4e1d802807` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `null_path_record` | 108 | `23bcfd677effd3a3b5ff73bfce72328c0bd19148a79617be8b896a4e1d802807` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |

The paths are `candidate/reports/v0_9/p0a3f_runtime_external_trust_qualification/attempts/P0A3F_R1_DEV_01/raw_workers/<case>/worker_0000_stdout.json`. Both original archived stdout files are zero-length **already in R1-C2 and remain so in R1-CFINAL**. The archives' ZIP checksums correctly attest to the actual zero-byte files; therefore intact ZIP manifests do **not** resolve this discrepancy with the contemporaneous event metadata. Associated stderr files match their records.

**The two expected 108-byte streams were not authentically recovered during independent QC. The cause is unknown.** This is neither a demonstrated false mathematical certificate nor evidence of intentional misconduct. Do not synthesize, backfill or retrospectively change raw worker streams, event JSON, hashes, DEV chronology or original archives.

Required negative classifications:

- `P0A3F_R1_DEV_01_RAW_WORKER_EVIDENCE_INCONSISTENT`
- `R1_CFINAL_RAW_EVIDENCE_COMPLETENESS_NOT_QUALIFIED`
- `P0A3F_R1_SOFTWARE_QUALIFICATION_INCOMPLETE`
- `P0A3F_R1_INDEPENDENT_QC_NOT_QUALIFIED`

## 5. Independent QC findings QCF02/QCF03 — further readiness barriers

**QCF02 — F1 external source/runtime authority unqualified.** The producer/reference identity path accepts `UNSIGNED_STAGING_PROPOSAL` plus `CALLER_OWNED_DEV_FIXTURE` only with `allow_dev=True`; normal unsigned deployment fails closed. This is conservatively correct for provisional engineering, but no independently qualified actual human-signed runtime authority path was established. `loaded_check()` covers limited function bytecode, not loader, classes, globals, native runtime or hostile filesystem substitution. A future signature alone does not establish that the running executable honours it.

**QCF03 — Remaining environmental/host/input boundaries.** R1 evidence is tied to the registered CPython 3.12.3 host and resource envelope. Independent QC occurred under Python 3.13.5, so a same-binary rerun of the original 18 methods **was not performed** and is not claimed. Broader process-tree containment after controller death, disk-full/power-loss/hostile filesystem/multiwriter durability, untrusted object APIs, arbitrary-input software completeness and comprehensive checker trust are not qualified.

## 6. Independent QC checks that passed

- Recomputed C0/C1/C2/CFINAL ZIP digests, CRC and manifests/inventories; all passed. Original P0A3E baseline digest matches prior freeze.
- Independently checked 17/17 supplied detached GPG signatures against expected signer fingerprint and 17 reconstructed Git signed-commit SHA-1 object identities. The QC keyring **did not establish human ownertrust**; that remains distinct from locally trusted GPG verification by the human signer.
- Confirmed all three immutable P0A3D/E exact mathematical kernels byte-identical; C1 pre-run lock and retained DEV source snapshot match; retained runner reports 18 passed.
- Independent exact generic fixture checks: R is a proper quarter-turn with translation; Z is equivalent under zero-edge/subdivision arclength; T has zero covariance and a whole-roll tie; N has strictly positive covariance and a unique proper rotation.
- Nine extra generic parser rejection microchecks passed on QC host Python 3.13.5; these do not establish pinned-host or arbitrary-input correctness.

## 7. F0–F7 final independent-review dispositions

| Phase | R1 independent QC status |
|---|---|
| F0 | PASS for checked signed lineage, source provenance and frozen baseline identities; 17 detached signatures verified against expected fingerprint without new human ownertrust assertion. |
| F1 | **INCOMPLETE:** no operational real-signed-code external authority or complete loaded-code attestation. |
| F2 | **BOUNDED DEV evidence only:** CPython 3.12.3 source/environment records; same pinned interpreter independent replay not performed. |
| F3 | **BOUNDED DEV evidence only:** fresh-checker recovery and actual timeout recorded; broader crash-host contract incomplete. |
| F4 | **INCOMPLETE:** hostile input/checker DEV reported, but two raw stdout streams inconsistent; arbitrary-input qualification still incomplete. |
| F5 | **18/18 RECORDED DEV**, one prospective attempt; complete raw evidence criterion FAILED under QCF01. |
| F6 | Complete ZIP CRC/hash/inventory PASS; claim of complete raw worker evidence preservation FAILED under QCF01. |
| F7 | **INDEPENDENT_QC_NOT_QUALIFIED**; no readiness declaration, code-only freeze, or P0A4 authorization. |

## 8. Original historical failure remains separate

The distinct original `P0A3F_DEV_01` (without R1 prefix) remains `P0A3F_DEV_01_EVIDENCE_UNAVAILABLE`, `P0A3F_DEV_01_RECORDED_FAIL_NOT_QUALIFIED` and `P0A3F_EVIDENCE_LOSS_STOP_AND_QUARANTINE`. Its reported 22 passes and method-23 eight-second timeout derive from a transcript-only incident, with missing original source/log/catalogue bytes and unknown underlying cause. The R1 evidence discrepancy is **not** that original incident, and neither outcome is retroactively relabelled. All earlier P0A0–P0A3E findings remain unchanged.

## 9. Preservation decision, restrictions and next authorized steps

1. **Sign/push only this immutable incomplete-result preservation** after human review, exact byte-level verification and validation that its direct parent remains `83b9e6dcd53b100c5ac8b081832e81659cd1884a`. Never reset/overwrite the branch to force ancestry; stop on a changed branch head.
2. Preserve the four original R1 archives and the original independent QC ZIP under the exact manifest names/hashes; do not rewrite source or missing worker bytes. This archival action is **not** a new DEV execution or substantive software repair.
3. Conduct a bounded, read-only search of authentic original stdout backups/channels for the two 108-byte streams; record checked locations. A failure to find them is not proof that every possible backup is exhausted. Do not treat regenerated outputs as original historical bytes.
4. If authentic recovery is unavailable or insufficient, prepare a **separately human-signed prospective narrow corrective protocol** specifying new attempt numbering, immutable reference to R1 negative QC, prospective source/case/environment lock, exact stream-byte verification **before** checkpoint sealing, and durable early checkpoints before new DEV. Consider separately how F1 real signed-code authority and the remaining host assumptions can be qualified without changing frozen mathematical kernels.
5. Execute no corrective DEV solely on the strength of this closeout. All future execution requires its own signed authority and evidence gates; a fresh result cannot retroactively certify the missing R1 raw output.
6. After any new bounded corrective candidate, perform independent source/mathematical/software QC and only then consider a human-signed **code-only freeze** of verified actual source/checker/config/runtime trust authority. **P0A4 registered validation remains NOT RUN and not authorized.**

**Absolute exclusions remain:** no old P0A0 S00–S12 replay; no historical target/glyph/image/font proxy; no P0A4, G0/A/B, QH or 3D camera; no scientific parameter tuning, no theorem rewrite, no candidate/null statistical runs, no source-rights or observation claims, no deployment or agent self-certification.

## 10. Signer installation and status gate

**This is an unsigned staging candidate. The agent has NOT committed, signed or pushed anything.** Human should verify all new file paths, verify SHA256SUMS for the document and five original ZIP payloads, inspect staged diff and GPG-sign the additive preservation commit using the established key. The commit must be a pure addition to the branch with the direct parent listed above. No pre-existing Git file may be changed.

**Disposition to freeze after human signing:** `P0A3F_R1_INDEPENDENT_QC_NOT_QUALIFIED`; `P0A3F_R1_SOFTWARE_QUALIFICATION_INCOMPLETE`; earlier signed mathematical theorem unchanged; historical incident and all R1 evidence retained exactly as observed.
