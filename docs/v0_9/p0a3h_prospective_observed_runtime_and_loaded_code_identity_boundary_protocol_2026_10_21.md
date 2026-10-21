# P0A3H — Prospective Observed-Runtime Identity and Trust-Boundary Qualification (Bounded Pre-Freeze Lane)

**Project:** Meru Geometry Audit v0.9 — Hebrew projection capacity programme
**Repository:** `salahealer9/meru-geometry-audit`
**Branch:** `hebrew-projection-capacity-v0.9`
**Date:** 2026-10-21
**Required direct parent for protocol-only human-signed preregistration:** `d9d0d6ad5b7cc310ed14af774355aeaa2652ea89`
**Expected human GPG signer fingerprint:** `D4EC014EEFCC90E619D2AA59A91239ABCF512130`
**Before actual human signing:** `P0A3H_PROTOCOL_DRAFT_NON_AUTHORIZING`
**Git scope:** add precisely this one protocol document. **Agent: NO GIT WRITE / COMMIT / PUSH; NO private human key.**

## 0. Scientific purpose and strict epistemic limit

After the signed P0A3G-R2-C3 administrative closeout, the most material remaining pre-freeze issue is the **identity of the executable environment and actually loaded code**, not another run of the previously exposed twenty R2 tests. The P0A3G software's existing `loaded_check()` has only narrow Python function-code comparisons, and all R2 positive records still disclose `LOADED_CODE_IDENTITY_UNVERIFIED`. It does not attest arbitrary loaded classes, globals, closures, bytecode, import machinery, in-memory changes, native libraries, interpreter internals or hostile time-of-check/time-of-use (TOCTOU) substitution. All R2 authority signatures were test-only. Existing `DEPLOYMENT` requests intentionally fail closed with `REAL_HUMAN_SIGNED_AUTHORITY_ABSENT`.

**Question preregistered here:** Can a separate, bounded observer/launcher, which does **not import or modify the existing candidate**, produce independently checkable evidence that the file, environment, process and import identities observed around **one prospective generic execution** match a previously witnessed lock, and distinguish specified intentional substitutions and evidence failures? The goal is **measured process/environment consistency under cooperative-host assumptions**, NOT proof that all runtime instructions are immutable or production-ready.

**No permissible P0A3H outcome may say `LOADED_CODE_IDENTITY_VERIFIED` without an actually justified complete attestation model.** The original candidate's disclosure `LOADED_CODE_IDENTITY_UNVERIFIED` remains accurate. A passing P0A3H only warrants `P0A3H_BOUNDED_OBSERVED_RUNTIME_EVIDENCE_SUPPORTED` in the precisely tested cooperative Linux/CPython envelope, with an explicit residual threat register. The same agent can implement the observer but cannot independently certify its own result.

Historical outcomes remain permanent and distinct:

- Exact abstract ordered-open-path 2D SO(2) QO theorem, P0A3D signed `59eb47f7500d57866e4935822b78a555d3bcb515`, unchanged.
- P0A3F-R1 negative QC: `P0A3F_R1_INDEPENDENT_QC_NOT_QUALIFIED`.
- Original P0A3G pre-lock violation: `P0A3G_INDEPENDENT_QC_NOT_QUALIFIED`.
- Original R2 technical outcome: 14/14 historical plus six supplementary methods passed with zero unexplained streams; **historical** overall `P0A3G_R2_INDEPENDENT_QC_NOT_FULLY_QUALIFIED` because of `R2_QCF01_C2_PRIOR_RECEIPTS_OMITTED`.
- Separate positive C3-only administrative QC: `P0A3G_R2_C3_ADMINISTRATIVE_RECEIPT_CHAIN_QC_PASS_WITH_HISTORICAL_C2_OMISSION_PRESERVED`, human-signed preservation **direct parent** `d9d0d6ad5b7cc310ed14af774355aeaa2652ea89`, closeout Git blob `32d9b60f9d9814e34d3fea6742f5bcf00d33c81a`.

**P0A4, Hebrew targets, glyphs, 3D/QH geometry, candidate/null selection, scientific tuning, deployment, production signing and code-only freeze are NOT authorized.** No R1/G/R2/C3 outcome may be retrospectively upgraded by this new phase.

## 1. Immutable input objects, authority and host constraints

Retrieve and read the **complete signed P0A3H protocol** from GitHub by its new immutable commit; verify direct parent, expected signer fingerprint, branch tip, one-file addition and exact Git blob, using actual Git/GPG checks when possible. Independently authenticate earlier signed R2 protocol `7de01ab2c90afe52dd763652a9eaffd2e9a2cff9`, H04 corrigendum `4b488825ed35c7ac91a19abe62be068e75e9a076`, signed R2 incomplete QC `e491e1e9f96391cd512db0dd528765d63bc179c1`, C3 protocol `f5e31de09a8b79ddb1b5f0ba738443fc4012a390`, and C3 closeout. GitHub assertions, actual cryptographic validity and ownertrust are separate facts; report which are established.

Recover **read-only** original P0A3G R2-C1-REV1 candidate from the signed preservation under `reports/v0_9/p0a3g_r2_independent_qc_incomplete_checkpoint/`. Original R2-C1-REV1 ZIP **197,250 bytes**, SHA-256 **`b34a3cd2c27f9384adb7427fa6628d6c08e15712e73542bda80eaeef989009b1`**, with 51-file original `lock/SOURCE_LOCK.json` SHA-256 `abff7aa8df19f73e070d9f06ebd23334f8d98b45c1736d38399b845c69835902` and unchanged G/H external lock SHA-256 `2c8301fdfb8a313163713cacd3050a77a5a6a3d0b2f1b4f7d391791af967377b`. Match the 51 candidate files to signed P0A3G G-CFINAL original SHA-256 `8b0ec808ddea05d31422ad30308d3a5bbe8aaadb860cd613adf51bdcc9f33a6a`; do not substitute an agent-edited copy.

The three byte-frozen mathematical kernels are:

- `src/meru_geometry/v0_9/qo2d_exact/algebra.py` — `442065847937252db00d3f63b02184c15d57989f958f764c5c731cb385de6d2d`;
- `src/meru_geometry/v0_9/qo2d_exact/core.py` — `37701d034d98725673240a881420892893906c70387f68432b5993f8557dd420`;
- `reference/v0_9/qo2d_exact/arithmetic.py` — `72b3c37f02be65b2df7616a94e84601d66cf4af5b7a50e878724de647e5bf0ba`.

Generic pre-existing **R2-H01** request fixture in the witnessed lock: `r2_external/fixtures/R2_H01.request.json`, 735 bytes, SHA-256 `0807f2245f10dd3ebf819f2c9be1206587a4aa55cd0f4226163bf79f5cf898fa`. This is a previously exposed, signed-lock fixture, not a fresh statistical holdout and not a Hebrew input. Use it solely as a known benign process-launch payload; do not reinterpret its scientific validation.

Preferred cooperative host/runtime: Linux, CPython 3.12.3 `/usr/bin/python3.12 -I -S -B`, interpreter binary SHA-256 `e50d468e8b0adfb05733f5b87b3cff34829c4a8c1aea50c865aa8bdfe4bb150f`, and `/usr/bin/openssl` SHA-256 `b4f547c0f16272d1cc7f870330a6f2c243710c335e7a99c734ff7a0c6fdb2503`. Frozen R2 resource policy SHA-256 `9b7221fcfb54dc313874c9873423001ae7856b3a1889f12b92f9638abd904e09`; preserve its original 8-second worker wall, 6-second CPU, 256 MiB memory, 2 MiB file/stream, NOFILE 32, concurrency 1, recursion 256, 16 MiB attempt disk and 64 KiB request limits. The observer's own limits are additional and preregistered separately; do not weaken the candidate policy. Host/binary mismatch must be predeclared and blocks *same-host* qualification; an unsupported observer or incomplete `/proc` view must produce an explicit inconclusive state, not success.

All work is in **new isolated `P0A3H/` outside the signed Git checkout**. The original 51 candidate files, associated old sources/schemas/fixtures, old signed archives and original R2 evidence are **READ-ONLY**. Do not patch, import-wrap, monkeypatch, replace or edit the candidate, especially its `DEPLOYMENT` fail-closed behaviour. An altered candidate is a new, separately authorized engineering question, not P0A3H.

## 2. Threat model and evidence levels, defined in advance

**Protected claims / accepted assumptions:** a cooperative non-malicious Linux kernel and filesystem; observer/controller not intentionally compromised; SHA-256 collision resistance; trust in independently received locked object hashes and readback. Use isolated child processes and a controller-owned workspace with pinned absolute executable paths. Do not call the controller or an in-process `sys.modules` report an independently trusted hardware attestor. Record precise trust placement: observer and candidate may still share one host and one OS account; observation by a second process is separation of role, not adversarial isolation.

**Required observable evidence:** prelaunch source/tree and interpreter/runtime/environment byte identities; allowed input canonical bytes; PID/PPID/process-tree provenance; `/proc/<pid>/exe`, `cmdline`, selected `environ` policy digest, `maps`/mapped-library paths/digests where readable, file-descriptor/provenance snapshots where supported; trusted-launcher event time ordering; after-run source/tree and raw stdout/stderr bytes and status, including truly empty outputs; independent cross-reconciliation against the locked expectations. Linux `/proc` is sampled, not continuous; module inventories and in-process audit hooks, if used, are **self-reported supplemental evidence**, not full loaded-code proof. Record which native/shared objects and imports could **not** be observed, including race windows, `.pyc`, anonymous mappings, JIT/dynamic modules, `dlopen`, symlinks and file replacement. A missing mandatory observation is INCONCLUSIVE, not a fabricated match.

**Evidence hierarchy:**

- `FILE_BYTES_LOCKED`: source and binary files on disk matched at sampled points.
- `OBSERVED_PROCESS_ENVELOPE_CONSISTENT`: independent process snapshots and launch relationship match locked criteria under declared host assumptions.
- `LOADED_CODE_IDENTITY_UNVERIFIED`: full instructions actually executed are **not** proven; this remains stated alongside any preceding positive result.
- `PRODUCTION_CODE_AUTHORITY_ABSENT`: no real human private key / production signing / production trust root is installed. Existing `DEPLOYMENT` acceptance remains disabled.

No evidence from this same-host measurement may be relabelled as hostile-host security, comprehensive TOCTOU defence, process-memory attestation, trusted-boot attestation or production signing authority. Clearly separate positive *detectable injected faults* from unknown attacks.

## 3. Prospective construction: H-C0, witnessed H-C1, then ONE execution

**H-P0 intake:** Before invoking **any P0A3H candidate/observer/worker test** retrieve and authenticate all sources; inspect static source contracts and identify whether externally observing the exact existing candidate invocation is feasible without modifying any of the 51 files. Static reading, file hashing, manifests, Git/GPG, binary-version inspection, standalone source AST parsing **without import/execution**, and packaging are allowed. An impossible interface, missing required source, failed signature, or unsupported observation capability is an immediate `P0A3H_PREFLIGHT_INCOMPLETE` with preserved evidence. No silent redesign or candidate patches.

**H-C0 first immutable checkpoint:** source/register ledger, prior known exposure including R2 20/20, historical negative QC statuses, exact baseline/object identities, observer trust model, current OS/process-snapshot capabilities and a complete `NO_P0A3H_EXECUTION_YET` chronology. Durably preserve, fresh retrieve, check exact bytes/CRC/manifest/inventory before producing H-C1.

**H-P1 engineering/source lock:** implement a new *external observer/launcher*, raw-evidence reconciler, and read-only test dispatcher in a separate `h_external/` tree; they may not import or write the candidate. Identify all scripts, binary/interpreter paths, event/status schemas, policy, trust assumptions, negative-control injection mechanics, exact case order, time budgets and expected outcomes **before any test execution**. Source preparation may include static syntax/AST checks; **no prelock tests, smoke runs, parser calls, subprocess candidate launches, trial probes, import checks or previews**, even if labelled dry run. Any actual P0A3H test before independent H-C1 witness is a prospective protocol breach and must stop. Disclose all pre-existing R1/G/R2 test exposure, not as new H results.

**H-C1 mandatory external-witness archive:** include (i) exact 51-file unchanged original candidate and `SOURCE_LOCK.json`, (ii) complete separately versioned external code and SHA-256 lock, (iii) a complete execution order/commands/case matrix with exact acceptance and negative outcomes, (iv) pinned host binaries, test-only key policy, budgets and source provenance, (v) an external independent verifier (no candidate imports), (vi) H-C0 original identity, and (vii) pre-run chronology and human-readable exact lock receipt. Safe ZIP names, per-member hashes/sizes and inventory conventions, no hidden mutable dependencies. Preserve H-C0 and H-C1 separately in user-accessible durable storage and **freshly retrieve actual bytes**.

**NON-NEGOTIABLE PAUSE:** After H-C1 is durably read back, **STOP and transfer the original H-C0 and H-C1 ZIPs to the separate research chat for independent, prospective static witness review**. Do not execute any H method or import candidate while awaiting release. The human may release exactly one attempt **only after** independent QC of the actual H-C1 bytes, by relaying `P0A3H-C1 LOCK WITNESSED; SHA-256 <independently verified full hash>; AUTHORIZE ONE P0A3H_DEV_01`. A generic 'continue', self-issued release or modified H-C1 invalidates execution. If the reviewer rejects H-C1, retain it as historical negative and submit a new independently identified lock; never hide the rejected candidate.

## 4. Fixed bounded adversarial catalogue (exact case logic and expected classification)

The following **seven methods** shall each be implemented as a **separately prelocked, deterministic case**. For any case, if a predeclared injection does not actually reach the specified observation boundary, the outcome is `INVALID_NEGATIVE_CONTROL`, **not PASS**. All fault inputs are disposable copies; never alter the signed source archives, live frozen candidate tree or other tests' inputs. New isolated attempt, process and evidence directories per case; enforce one overall attempt with no repair, repeat or adaptive case selection.

| Method | Prescribed challenge | Predeclared acceptance / failure boundary |
|---|---|---|
| **H01** clean measured launch | Invoke exactly the previously locked R2-H01 generic request under `TEST_AUTHORITY` using ephemeral **non-production** keys only after release, with the byte-frozen candidate and external observer. | Real candidate execution plus exact raw evidence; permitted result is bounded evidence consistency only. Candidate's `LOADED_CODE_IDENTITY_UNVERIFIED` disclosure must survive; no human/deployment authority or independent scientific success claimed. |
| **H02** prelaunch candidate-file substitution | On a disposable launch copy, deliberately change one predetermined byte of a selected *non-kernel* candidate Python source, preserving a separate unmodified reference. Capture the injected before/after digests. | External prelaunch source lock detects exact mismatch; child must not launch or produce an accepted certificate. A rejected input that never reached the intended path is not counted as successful detection. |
| **H03** absolute interpreter substitution | Intentionally supply an alternate executable path/binary identity not matching the signed 3.12.3 pin in a disposable test specification. | Prelaunch external executable identity mismatch, no candidate launch, no success. Merely using the same pinned executable under an alias is insufficient unless the locked check expressly treats the alias as disallowed and reports its identity. |
| **H04** import-path shadowing | Prepare a disposable, attacker-named module with same import name as one preregistered expected candidate/import dependency and a distinct digest; make its intended import path observable without changing protected source. | A launched child's actually observed shadow import must be rejected or reported `UNQUALIFIED`; if the shadow is not loaded or cannot be observed reliably, outcome `INCONCLUSIVE/INVALID_NEGATIVE_CONTROL`, never a claimed detection. Cannot assert universal resistance to import substitution. |
| **H05** evidence/process-binding forgery | Reuse/copy one measured-event or process-identity record between two distinct registered run IDs/PIDs, leaving recorded hashes intact. | Independent verifier rejects foreign/stale event identity and withholds a completed bound measurement. Preserve pristine and forged original bytes, run IDs and source hashes. |
| **H06** trust-root boundary | Supply a valid **test-only** scope signature and its separately altered/revoked/incorrect-scope analogue; try the candidate's existing `DEPLOYMENT` mode with no human production key. | TEST_AUTHORITY positive verifies only as test-only; altered/revoked scope fails; DEPLOYMENT remains rejected as `REAL_HUMAN_SIGNED_AUTHORITY_ABSENT`. This phase must not add a production key or change the deployment gate. |
| **H07** incomplete observation/aborted child | Reproduce one deterministic premature termination or loss of a preregistered mandatory observer snapshot in a disposable run with bounded exit/time policy. | Missing mandatory evidence yields `OBSERVATION_INCOMPLETE` / `NO_BOUND_CLAIM`, no false positive despite any successful-looking candidate output. Preserve true raw partial/empty streams and exit signals. |

Before witnessing H-C1, the independent reviewer must inspect the actual adapters for each case and verify that it is feasible using the original fixed interfaces and these precise acceptance classes. Any impossible or ambiguous case is a **pre-execution blocker**, not permission to omit, substitute or reinterpret it. Mark ambiguous environmental facts as scope limits. Exact subprocess arguments, selected non-kernel source byte and module target, fixtures, negative-control byte positions and expected schema values must be frozen in H-C1 and independently checked. No in-band agent assertions alone qualify a negative test; direct saved bytes and out-of-process evidence are essential.

## 5. One released attempt, evidence durability and post-run independent QC

**H-P2:** On a SHA-specific human release, verify locked bytes and runtime again **before any candidate invocation**. Run exactly one prospective `P0A3H_DEV_01` attempt in the frozen H01→H07 order. Any unregistered run, failed mandatory case, interface mismatch, unexpected accepted signature, source alteration or unexplained stream/identity discrepancy yields preserved FAIL/QUARANTINE, not a patch, skipped case, discretionary retry or post-run lock change. Critical integrity/authority bypasses stop further candidate launches immediately; record remaining cases `NOT_RUN_AFTER_QUARANTINE`. Ordinary failure follows the prelocked fail-closed stopping rule. The same agent cannot sign, approve or rewrite outcomes.

**H-C2:** Immediately package the **first and only** attempt (whether PASS/FAIL/INCONCLUSIVE) including H-C0 receipt, H-C1 receipt and actual externally witnessed human release, pre/post source lock, complete all-seven case ledger, processes and raw stdout/stderr, process-snapshot/provenance files, external reconciler outputs, unexpected outcomes, negative controls, resource/host status and first-attempt errors. **Previous checkpoint receipts must physically be present in H-C2 itself**, not only H-CFINAL: this specifically prevents recurrence of `R2_QCF01_C2_PRIOR_RECEIPTS_OMITTED`. Capture exact bytes, size, outer digest, CRC, per-file SHA256SUMS/inventory and freshly retrieve from persistent user-accessible storage. If any receipt is absent or unreadable, status **NOT QUALIFIED**; preserve the original H-C2 unchanged rather than backfill retrospectively.

**H-CFINAL:** Separate cumulative archive with the exact original H-C0, witnessed H-C1 and H-C2, immutable source baseline, all observed positives/negatives, explicit process/host threat limitations, exact signed-protocol identity, actual release receipt and an **empty independent-QC checklist**. Recheck original C2 inclusion and archive nesting; do not claim mere self-hashing proves every underlying observation. Publish original bytes and complete SHA-256 identities; preserve failures with equal care. All archives **unsigned engineering evidence** until independent QC and possible later human signature.

**H-P3 independent QC** (performed in separate research chat): re-read all original ZIPs, compare 51 candidate and external locks, verify externally witnessed pre-run chronology, re-compute stored file hashes and process/stream identities from raw files, confirm negative injections actually occurred, confirm only test-only authority and DEPLOYMENT refusal, assess missing snapshots/host assumptions, verify H-C2 contains actual old receipts and H-CFINAL nests originals, and compare results with the signed H01–H07 rules. No agent self-certification. Independent QC may decide:

- `P0A3H_BOUNDED_PROCESS_MEASUREMENT_QC_PASS_WITH_TRUST_LIMITATIONS` **only if** seven registered cases pass, every archive/receipt/identity boundary is independently qualified, and unsupported trust claims are absent;
- `P0A3H_INDEPENDENT_QC_INCOMPLETE` for any mandatory incompleteness or unqualified observation;
- `P0A3H_STOP_AND_QUARANTINE` for integrity, fraudulent history, forbidden production-key access or material trust bypass.

The engineering agent's maximum positive submission label is **`P0A3H_PROSPECTIVE_BOUNDED_OBSERVATION_SUBMITTED_FOR_INDEPENDENT_QC`**, not QC PASS. Negative outcomes must always be preserved and signed only by a human after review.

## 6. What comes after P0A3H (NOT authorized by this protocol)

Even a positive P0A3H does **not** lift `LOADED_CODE_IDENTITY_UNVERIFIED` in the strong sense or grant production authority. A next decision would require a **separate, human-owned code-only freeze and trust-root specification** tied to exact source, interpreter/runtime and external signer/key governance, with an independent read-only comparison of the proposed signed object. If genuine hostile-host loaded-code attestation is demanded, it requires an appropriate independently administered security/attestation design, not just more same-host Python tests. A mode change that enables production signing requires its own prospective signed protocol, implementation/testing and independent security/QC; it is expressly outside this phase.

**P0A4 remains NOT RUN / NOT AUTHORIZED**. No inference about Hebrew specificity follows from H01–H07.

## 7. Human signature and execution handoff

Before signing, the human checks feature-branch HEAD and remote equal **`d9d0d6ad5b7cc310ed14af774355aeaa2652ea89`**, clean index/worktree, exact downloaded ZIP and Markdown SHA-256, Git blob, one added protocol-only path, `git diff --cached --check`, and local GPG fingerprint `D4EC014EEFCC90E619D2AA59A91239ABCF512130`. Human alone `git commit -S`, checks parent, verifies the resulting signature and pushes. No existing signed object is changed. If branch tip advances, STOP and reconcile; no automatic rebasing or force-pushing.

**Only after** the new P0A3H protocol commit and source blob are independently verified may the research chat issue the agent's P0A3H handoff. That handoff must authorize **H-P0/H-P1 ONLY and a HARD STOP at H-C1 for external witness**. H-P2/H-P3 are contingent on a *second*, explicit SHA-specific human-relayed release. The agent cannot use this signed protocol by itself as an instruction to run tests.

**If human-signed protocol commit registered:** `P0A3H_PROSPECTIVE_BOUNDED_IDENTITY_BOUNDARY_PROTOCOL_REGISTERED` — not a test result, software freeze or production qualification.
