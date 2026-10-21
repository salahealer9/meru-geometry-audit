# P0A3F — Evidence-Loss Incident Preservation and Narrow Recovery Amendment (HUMAN-SIGNING CANDIDATE)

**Project:** Meru Geometry Audit, v0.9, `hebrew-projection-capacity-v0.9`.
**Prepared:** 2026-10-21.
**Authority required:** a NEW human-reviewed GPG-signed additive commit. This unsigned candidate is **not** an execution authorization.
**Required direct parent:** `1d38ea6f53b9266d853df887a66331c59e4fc3ae` (the already signed P0A3F one-file preregistration).
**Frozen P0A3F protocol blob:** `9530a75d2346752a093367aeac24e13c5d2d6fac`.
**Expected signing fingerprint:** `D4EC014EEFCC90E619D2AA59A91239ABCF512130`.
**Amendment type:** loss acknowledgement and **prospectively controlled restart from an immutable signed baseline**. It is not a retrospective rewrite, result freeze, code-readiness approval, P0A4 scientific test, or authority to modify frozen mathematical kernels.

## 1. Incident being preserved, without reconstruction

The separate Library object `P0A3F_EVIDENCE_LOSS_INCIDENT_2026-10-21.zip` was retrieved on 2026-10-21 and independently checked: **6,842 bytes**, SHA-256 `8048fdf7c56d82b8f560f98cd7b40bea99eb66837ef1e7be49934a4d1303f88d`, six entries, CRC PASS and all five internal non-self manifest entries checked. This candidate places those **unchanged original incident bytes** at `reports/v0_9/p0a3f_evidence_loss_incident/original_P0A3F_EVIDENCE_LOSS_INCIDENT_2026-10-21.zip`. The incident ZIP records a **transcript-derived account**, not recovered source or original DEV telemetry.

**Observed and reported, NOT independently reexecuted or authenticated as an original DEV log:** the first P0A3F engineering attempt (`P0A3F_DEV_01`) reportedly reached method 23 of a prospectively declared 26-method catalogue; 22 methods passed and the 23rd failed (`test_23_torn_stale`, subcase `saved_verdict_ignored`). The expected recovered checked certificate was not produced; a `RESOURCE_INCOMPLETE` / `CONTROLLER_WALL_TIMEOUT` was reported, with checker process return code `-9` after an eight-second deadline. The precise source/log/test/catalogue bytes are missing. No second attempt or repair was run. The checker timeout's cause is **unknown**; the apparent fail-closed state is not enough to pass the recorded recovery acceptance test.

The only reported original-DEV catalogue/source-manifest identities are transcript-derived SHA-256 text (`8d22fecb4ab7087b005e667815c1666656a71887dfc0ba3ff536606896ed2f57` and `e17002324f4aabd1ce8066d7744c877ec2a360e1e19f585b31b49f9a2dc24d67`). **These are not verifiable against the missing bytes.** The newly packaged incident log must be marked `INCIDENT_REPORT_FROM_TRANSCRIPT`, not a recovered, verified or independently rerun original DEV_01 record.

No surviving P0A3F source snapshot, complete DEV_01 raw logs, failure artifact or full original DEV catalogue was found in the Work agent's checked locations. Its bounded search does not exclude inaccessible infrastructure backups. This amendment does not assert that all possible backup/restore avenues have been exhausted.

**Disposition of lost first attempt:** `P0A3F_DEV_01_EVIDENCE_UNAVAILABLE`; `P0A3F_DEV_01_RECORDED_FAIL_NOT_QUALIFIED`; `P0A3F_EVIDENCE_LOSS_STOP_AND_QUARANTINE`. Do not convert this to PASS, erase its failure, reproduce the lost bytes by inference, or count its 22 reported passes as evidence supporting a new acceptance decision.

## 2. Frozen and still authoritative provenance

The original P0A3F protocol and all previous signed research remain unchanged. Human operator and future Work agent must independently verify:

- P0A3F protocol-only signed commit `1d38ea6f53b9266d853df887a66331c59e4fc3ae`, direct parent `8ed3b988f716229bc9aee97d41ded0f524371193`, blob `9530a75d2346752a093367aeac24e13c5d2d6fac`, one-file scope and matching signer (distinguish GitHub signature attestation from locally trusted GPG verification).
- P0A3E signed incomplete preservation `8ed3b988f716229bc9aee97d41ded0f524371193`, original cumulative implementation ZIP **968,965 bytes**, SHA-256 `1e73c2685bd4eb8fba89e4e8ea609e97c7b4716805e83c64af374a4265522ea8`, 303 entries, 302/302 `SHA256SUMS` and 301/301 inventory identities and historical DEV_01/02 and independent QC records.
- P0A3D positive theorem-result freeze `59eb47f7500d57866e4935822b78a555d3bcb515`, original candidate ZIP SHA-256 `c2f99b0e78849de16c8dc8167bdf5d584d4f64ab2c8a787d6a0ed507cfa9f378`, prior exact theorem proof/QC.
- Full ordered signed P0A0–P0A3F lineage, signed v0.8 tag where accessible and the permanent source/rights/observation gates.

The three unchanged P0A3D mathematical kernels are **byte-frozen** in the *new* recovery development copy: `src/meru_geometry/v0_9/qo2d_exact/algebra.py`, `src/meru_geometry/v0_9/qo2d_exact/core.py`, `reference/v0_9/qo2d_exact/arithmetic.py`. If a genuine false exact certificate or mathematical-kernel defect is discovered, stop/quarantine rather than silently changing those files.

## 3. Exact scope of this amendment

**One narrowly authorized exception to the original protocol's evidence-loss stop:** after independent confirmation of THIS NEW HUMAN-SIGNED amendment and incident evidence, the agent may **abandon the quarantined, irrecoverable P0A3F_DEV_01 as evidentially unusable** and establish **a new separately named prospective recovery execution lane** from the untouched signed P0A3E cumulative implementation baseline. This is a **new F0–F7 engineering execution**, not a resumption of lost source code or substitution of a fabricated historical DEV record.

All original signed P0A3F requirements for F0–F7, F1–F4 acceptance, immutable historical evidence, bounded resource/case registration, no production code self-certification, independent verifier and negative statuses remain binding. In any conflict, this amendment supersedes ONLY the clause prohibiting any fresh attempt after unrecoverable *new P0A3F* working evidence loss; it does **not** waive evidence/ZIP/signer checks or allow missing P0A3D/E baseline, theorem amendments, unregistered tests, or changed domain.

The new engineering attempt is labeled **`P0A3F_RECOVERY_R1`**. Number fresh attempts `P0A3F_R1_DEV_01`, `P0A3F_R1_DEV_02`, ...; never number them as original `P0A3F_DEV_01`/`DEV_02`. New source files/diffs and test results must be labeled **new, independently recreated engineering work**, never a recovery of the lost source snapshot. Historical failed P0A3F_DEV_01 is retained as a distinct transcript-only incident observation in the cumulative final ledgers.

## 4. Prospective locking and timeout-failure coverage

**Before the first new DEV run:** archive a dated pre-run lock recording (a) new exact catalogue and fixture constructors, (b) required expected outcomes and strict status taxonomy, (c) code/test/schema/config/source snapshots + hashes, (d) exact interpreter path/binary/env/VM preflight, (e) wall, CPU, memory, output, recursion, disk and worker/checker budget settings, (f) expected external trust interfaces and unsigned-versus-human-frozen source conditions, and (g) explicit failure/stop rules. This is a *prospective* fresh catalogue, never reconstructed or treated as identical to the missing original 26-method one.

The fresh catalogue MUST include a generic recovery scenario covering the incident's documented functional condition: a valid persisted output/certificate whose saved verification verdict is **not** trusted, requiring independent fresh checker verification before success. It must test both a checked-complete outcome **within the predeclared supported runtime envelope** and a bona-fide timeout/interruption outcome that **does not** return a successful certificate. Preserve the distinction: a correct `RESOURCE_INCOMPLETE` does not establish completion of the checked-recovery case. Do not silently increase the former eight-second deadline after observing a failure; if a different prospective bound is scientifically and operationally justified, record its rationale **before** new DEV execution, and keep the original eight-second timeout failure prominent in every disposition.

No claim about the lost attempt's checker-stall cause is permitted without independently recreated, newly obtained evidence. Preserve all reproduced failures and complete repaired-source diffs. A repeated false exact-certificate acceptance, prohibited input, or frozen mathematical-kernel issue triggers hard stop/quarantine.

## 5. Mandatory DURABLE checkpoints to survive interruption / credit exhaustion

A fresh ephemeral workspace **cannot be the sole copy** of source or DEV evidence. The agent must use available persistent Library or another user-accessible durable artifact channel and re-check the exact size and SHA-256 of each saved checkpoint before relying on it. Staged file availability must be independently confirmed via the destination's file metadata or a fresh retrieval (when possible). Merely printing a ZIP name in chat or reporting intent to upload it is **not** preservation.

Minimum checkpoint gates:

1. **R1-C0 — BEFORE development/DEV:** frozen signed baseline inventory and incident ZIP verification, selected interpreter, repository read-only state, restored starting source manifest and scope/requirements matrix. Save durable checkpoint and verify its retrieval/identity before proceeding beyond F0.
2. **R1-C1 — BEFORE first DEV:** actual edited source/ref/parser/worker/schema files, exact pre-run prospective catalogue, locked resource budgets and source snapshots. Save durably and verify identity; **no DEV** without this checkpoint.
3. **R1-C2+ — AFTER EVERY DEV attempt or distinct source repair:** original stdout/stderr, JSON summaries, inputs, complete raw worker artifacts and crash/timeout observations, source/test diffs and manifests (including failures). Preserve at least one new durable checkpoint before another DEV attempt or modification. Attempt numbers advance monotonically; no rewriting of the previous checkpoint.
4. **R1-CFINAL — cumulative release:** complete candidate ZIP with self-consistent manifest/inventory and exact source, DEV chronology and environment/provenance ledger; independently retrieve and verify deliverable before making any readiness claim.

If durable checkpoint persistence or retrieval verification cannot be performed, **STOP**, preserve the last confirmed checkpoint and report incomplete—not another undocumented continuation. To conserve execution credits, prioritize C0/C1 over optional DEV breadth, and avoid a large uninterrupted work session before saving evidence. All checkpoints are **unsigned working evidence**, never a substitute for a future independent QC and human-signed code-only freeze.

## 6. Retained exclusions, QC and signing gates

Absolute exclusions are unchanged: **NO COMMIT / NO PUSH / NO modifications of the existing repository**, no P0A0 S00–S12 replay, no P0A4 registered numerical validation, no Hebrew images/glyphs/fonts-as-proxies, no candidate/null work, no G0/A/B/3D cameras, no QH or physical shadow evaluation, no publication or deployment, no modifications to the 2D QO score, path ordering, RMS normalization or nuisance group.

All code development remains outside the Git checkout. Historic P0A3D/E evidence and this incident ZIP are READ ONLY. Independent source/mathematical/software QC follows final recovery candidate. Positive readiness requires separate independent review and then **a separate human GPG-signed CODE-ONLY freeze** establishing actual external expected source/checker/config/runtime authority. No unsigned Work proposal is allowed to self-certify as trusted.

Permitted resulting outcomes: `P0A3F_R1_ENGINEERING_CANDIDATE_SUBMITTED_FOR_QC` (only if full deliverable exists), `P0A3F_R1_SOFTWARE_QUALIFICATION_INCOMPLETE` if blocked, `P0A3F_DEV_01_EVIDENCE_UNAVAILABLE` permanently, `P0A3F_REGISTERED_VALIDATION_NOT_RUN`, and separately scoped F1–F4 negative/positive review findings. No `P0A3F_EXACT_2D_QO_SOFTWARE_CANDIDATE_READY_FOR_REGISTERED_TARGET_FREE_VALIDATION`, no `GLOBAL_CERTIFIED` and no historical inference may be granted by the Work agent.

## 7. Human signing / restart order (MANDATORY)

1. Read and human-review this entire amendment, the exact six-file incident ZIP, original signed P0A3F protocol and signed P0A3E incomplete checkpoint. The new amendment/incident commit must have **exact direct parent** `1d38ea6f53b9266d853df887a66331c59e4fc3ae` and be signed by the expected fingerprint. No resets or overwrites to force parent.
2. Stage **only** `docs/v0_9/p0a3f_evidence_loss_recovery_amendment_2026_10_21.md`, `reports/v0_9/p0a3f_evidence_loss_incident/original_P0A3F_EVIDENCE_LOSS_INCIDENT_2026-10-21.zip` and `reports/v0_9/p0a3f_evidence_loss_incident/INCIDENT_AND_AMENDMENT_MANIFEST.sha256`; verify outer candidate ZIP checksum, CRC, new-file paths and manifest SHA-256, inspect staged diff. Never modify a prior Git file.
3. Human alone signs and pushes the additive incident-and-amendment commit on `hebrew-projection-capacity-v0.9`. Verify complete new commit SHA, parent, signature, and exact Git blob of this amendment.
4. **Only after the new signed amendment** is independently verified, issue a **new Work handoff** pinned to its true signed commit/blob, requiring GitHub retrieval of both original P0A3F and amendment. Work reconstructs a clean P0A3E-based isolated R1 workspace and follows F0–F7 with the new checkpoint gates; no previously lost source is represented as preserved.
5. Independent reviewer examines retained incident ZIP, R1 checkpoints, candidate ZIP and new logs/diffs. Only independently qualified code may later enter a distinct human-signed code-only freeze and a still later separately registered target-free validation.

**Decision:** preserve the failure as historical evidence, accept that the original P0A3F engineering attempt is incomplete and unrecoverable from presently available records, and allow only a transparent **new prospectively locked** bounded engineering attempt once this amendment is signed. The source-first scientific history and exact theorem stay fixed.
