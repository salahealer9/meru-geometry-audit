# P0A3G — Raw-Worker Evidence Closure and External-Trust Boundary Follow-Up (Protocol-Only Preregistration)

**Project:** Meru Geometry Audit, v0.9 — Hebrew projection specificity and effective-viewing-capacity programme
**Repository:** `salahealer9/meru-geometry-audit`
**Branch:** `hebrew-projection-capacity-v0.9`
**Prepared:** 2026-10-21
**Status:** `P0A3G_PROTOCOL_DRAFT_NON_AUTHORIZING`, until a human has reviewed, GPG-signed, verified and pushed this exact one-file protocol.
**Required direct parent:** `d95c50ea96744ce266058c51f85fff320d1a27df`
**Expected human GPG fingerprint:** `D4EC014EEFCC90E619D2AA59A91239ABCF512130`
**Agent Git authority after signing:** **NO COMMIT / NO PUSH / NO CHANGES TO THE EXISTING REPOSITORY.**

## 0. Frozen authority, actual problem and limits of this stage

The frozen P0A3D mathematical theorem is independently verified at signed commit `59eb47f7500d57866e4935822b78a555d3bcb515`. It concerns two independently supplied genuinely ordered finite open rational-vertex polygonal paths, true planar arclength, separate centroid/RMS normalization, and optimal proper planar rotations `SO(2)` only. For normalized paths A and B, J(x,y)=(-y,x), alpha=integral(B dot A), beta=integral(B dot JA), s=positive_sqrt(alpha^2+beta^2), qO=positive_sqrt(2-2s); exact s=0 has a whole-rotation tie and canonical identity witness. No new theorem, optimization or new historical observation is authorized.

Signed P0A3E incomplete software preservation: `8ed3b988f716229bc9aee97d41ded0f524371193`. Its original cumulative implementation archive is 968,965 bytes, SHA-256 `1e73c2685bd4eb8fba89e4e8ea609e97c7b4716805e83c64af374a4265522ea8`. The separately signed original P0A3F protocol is `1d38ea6f53b9266d853df887a66331c59e4fc3ae`, protocol blob `9530a75d2346752a093367aeac24e13c5d2d6fac`. Signed evidence-loss/R1 amendment `83b9e6dcd53b100c5ac8b081832e81659cd1884a`, blob `9fd9fba6ca509e3fcb72c2227d226847d218b354`. Signed P0A3F_RECOVERY_R1 **incomplete independent-QC preservation and required direct parent** is `d95c50ea96744ce266058c51f85fff320d1a27df`; its preserved closeout document Git blob is `bf1dacde71c5b3a0ac3919f070c1c57a74c4ce41`.

The P0A3F_RECOVERY_R1 retained DEV log reports 18/18 methods passed on its prospectively locked compatible CPython 3.12.3 runtime, but independent QC identified **QCF01**, a HIGH-priority raw-evidence failure: in two of 37 worker events, `forged_q` and `null_path_record`, the recorded stdout is 108 bytes with SHA-256 `23bcfd677effd3a3b5ff73bfce72328c0bd19148a79617be8b896a4e1d802807`, whereas the archived files are **zero bytes**, SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`. 72/74 stream metadata identities agree; these two do not. This discrepancy occurs in the original R1-C2 and R1-CFINAL. The exact cause is UNKNOWN and no authentic replacement bytes were recovered by QC.

The signed negative statuses remain: `P0A3F_R1_DEV_01_RAW_WORKER_EVIDENCE_INCONSISTENT`, `R1_CFINAL_RAW_EVIDENCE_COMPLETENESS_NOT_QUALIFIED`, `P0A3F_R1_SOFTWARE_QUALIFICATION_INCOMPLETE`, `P0A3F_R1_INDEPENDENT_QC_NOT_QUALIFIED`. The *earlier distinct* lost original `P0A3F_DEV_01` remains transcript-only and evidentially unavailable. **Neither history may be rewritten or retroactively upgraded.** Signed R1 evidence archives have these exact SHA-256 values:

| R1 signed archive | SHA-256 |
|---|---|
| `original_P0A3F_RECOVERY_R1_R1-C0.zip` | `0487dcebb13e56cb49cb51886dae2ad0a673c023bf66b52084e7756a42c2f60d` |
| `original_P0A3F_RECOVERY_R1_R1-C1.zip` | `19b34f8d691e2ea3b127a6b2b8a16d4d9d5e925f47802094b4851b2c9644c812` |
| `original_P0A3F_RECOVERY_R1_R1-C2.zip` | `f18a32551d30b8b89f8eb85242e431c8fbb1cf213903aa5710da19fab8b320f7` |
| `original_P0A3F_RECOVERY_R1_R1-CFINAL.zip` | `6ec2b6e96234836d629398fb7fc781909de8b47b0bf80f5cae11202620ff2f15` |
| `original_P0A3F_RECOVERY_R1_INDEPENDENT_QC_2026-10-21.zip` | `aa810c66ac6454a1d04a30cc597612b61006bca0dc7d5c3340726efa4a6cf305` |

**Sole prospective engineering question:** Can a clean, separate engineering descendant of the unsigned R1 candidate (a) capture, index, independently rehash, preserve and retrieve every actual worker stdout/stderr byte without a claimed PASS on a mismatch, and (b) exercise a strictly external code-authority verification route with caller-controlled *test-only* signature fixtures, while retaining the existing exact mathematics and explicit resource/host limitations? This phase is deliberately narrower than full executable qualification. It cannot supply its own real human-signed code freeze or authorize P0A4.

## 1. Non-negotiable provenance, scope and hard stops

The agent must first independently retrieve **this newly signed P0A3G protocol directly from GitHub**, verify actual commit/blob, its exact parent `d95c50e...`, its one-file protocol-only scope and the expected GPG fingerprint; distinguish GitHub signature attestation, local GPG checks and downloaded unsigned ZIP hashes. Verify complete frozen predecessor lineage and signed v0.8 tag where accessible. Re-read the entire P0A3F original protocol, its R1 amendment, R1 signed QC closeout and independent QC report, and the original P0A3D/E theorem/implementation boundaries. Stop on any missing/wrong authorization or baseline identity. A draft banner subsequently left in an already signed protocol is historical text, not grounds to edit it.

All signed ZIPs and the entire Git repository are **READ ONLY**. Construct any revised code in a fresh isolated directory outside the Git checkout, starting from vetted copies of the **R1-CFINAL cumulative candidate**. Treat that candidate as an *unqualified engineering baseline*, not trusted software. Verify its SHA-256, CRC, 407/407 internal manifest identities, 406/406 inventory identities, source lock and relevant historical DEV/QC evidence. Also independently verify the P0A3E cumulative baseline and unchanged three mathematical kernels:

- `src/meru_geometry/v0_9/qo2d_exact/algebra.py`;
- `src/meru_geometry/v0_9/qo2d_exact/core.py`;
- `reference/v0_9/qo2d_exact/arithmetic.py`.

Those three kernels must remain byte-identical in the entire new candidate. Do not modify the exact domain, path ordering, score, arclength/RMS convention, nuisance group or independent-checker mathematical route. A false exact certificate accepted as true, theorem contradiction, prohibited target use, archive/signature mismatch or a frozen-kernel defect triggers **STOP_AND_QUARANTINE**, not a silent repair.

Absolute exclusions: no P0A0 S00-S12 replay; no P0A4 or other registered scientific validation; no historical Hebrew chart/glyph/image/font-proxy/source extraction; no candidate/null comparison or threshold tuning; no QH, 3D, G0/A/B cameras or physical shadow simulation; no agent commits/signatures/pushes; no hidden deployment, private-key extraction, or claimed historical Meru specificity.

## 2. G0 — Verified intake and limited authentic-evidence search

Before any engineering, verify the signed provenance, R1 evidence, source/environment hashes and independent QC QCF01–QCF03. Produce a dated read-only search ledger listing the actual locations and data channels checked for **authentic original R1 stdout**: signed archives, relevant Library files, retained controller outputs/transcripts and any accessible original raw backup paths. Search only bounded, authorized locations; do not claim all backups have been exhausted.

If a purported original 108-byte stream is found, preserve its original source metadata and exact bytes separately, independently recompute size/hash and establish genuine original-event provenance before describing it as authenticated recovered evidence. Do not splice it into any old archive or overwrite the historical finding. A newly generated 108-byte lookalike or a fresh rerun is **not** recovered historical evidence. Whether recovery succeeds or not, R1's existing signed negative QC remains an immutable historical decision.

Establish the exact pinned interpreter and host/runtime preflight; use R1's declared CPython 3.12.3 `/usr/bin/python3 -I -S -B`, selected executable hash and existing eight-second checker deadline where compatible. A different environment, caps or deadline requires a **prospective written justification and new baseline declaration before DEV**, without reclassifying R1; unsupported host conditions produce `ENVIRONMENT_UNQUALIFIED` with no certificate. No opportunistic post-result budget changes.

**G-C0 must be durably saved and freshly retrieved/verified before moving beyond G0.** It must contain the signed-source and ZIP verification ledger, authentic-evidence search log, selected interpreter/environment, baseline source/hashes, import/dependency snapshot, hard-stop and scope matrix. If Library or an equivalent user-accessible persistent artifact route is unavailable, STOP.

## 3. G1 — Raw-worker provenance and completion contract

Design and implement a **single accountable raw-stream capture boundary** in the isolated copy. The supervisor must retain the **actual bytes received from each worker stdout/stderr stream** (including empty, partial, non-UTF8 and abnormal exit), under unique attempt/run/worker/stream identifiers. Distinguish the raw stream bytes from decoded JSON, parsed certificate records and independently generated summaries. Do not reconstruct streams from JSON objects or compute metadata from a different in-memory serialization.

After completion of each bounded worker, compute stream byte count and SHA-256 **from a fresh read of the exact saved bytes**, compare them to the contemporaneous recorded event identity, and fail closed on inequality, absent stream path, unexpected emptiness, orphan records, case/worker collision, stale identifiers, swaps, duplicate files, truncation or post-write alteration. Preserve stdout and stderr, exit/signal, supervisor/caller/worker run identity, expected code/checker/schema/config/runtime identities, and typed final status. A saved file with a valid ZIP checksum but incompatible event record is **NOT VERIFIED**. No 18/18 or completed-certificate claim may be issued if any required raw artifact is unverified.

Define strict bounded stream length/retention, output-size limits, atomic write and fsync behavior, secure relative paths, symlink/duplicate rejection, immutable attempt directories and post-retrieval rehash. If a process exits with no stdout, record **actual zero-length stdout and its matching empty SHA**, not a fictional expected message; if nonempty output is expected by a particular prospectively declared fixture, missing output fails that fixture. Distinguish a real process-level kill from fault simulation. Include failure-injection coverage for event metadata that advertises 108 bytes while the retained stdout is zero bytes — explicitly the R1 QCF01 functional condition.

## 4. G2 — External authority boundary, without self-certification

Review R1's external expected-manifest, caller receipt, source/loaded-code and independent reference identity paths. Define or narrowly harden a **versioned canonical externally supplied code authority envelope** binding Git source ancestry, complete proposed candidate source and reference code, parser, schemas, configuration, runtime interpreter/resources, and accepted canonical input/certificate identities. The producer and reference checker must independently reject missing, altered, unsigned-as-signed, wrong-key, wrong-scope, expired/revoked-where-supported or wrong-run external authority, without issuing a completed exact certificate.

For bounded generic engineering DEV, the controller/test harness may provide a separately managed **test-only verification key and signed fixture** to exercise cryptographic signature verification. Mark that fixture `NON_PRODUCTION_TEST_AUTHORITY`, disclose its generation, trust-store assumptions and actual verification method, and ensure the candidate cannot silently replace the expected public key or sign its own approval. No actual human research-signing private key is supplied to Work. An unsigned `CALLER_OWNED_DEV_FIXTURE` may remain useful for negative and regression checks but is never a real code-only freeze. **No test signature is an authorized final deployment identity.** Any inaccessible runtime/loaded-instructions guarantee must remain `LOADED_CODE_IDENTITY_UNVERIFIED` with an exact threat-model statement, rather than a fabricated attestation.

Because the human code-only freeze occurs only **after** positive independent QC, G2 may establish a testable verification interface and recommend its later external trust-root/signing procedure; it **cannot** claim that a yet-unissued real human code signature was already verified. Identify this deployment gap explicitly in all dispositions. Do not expand scope into hostile kernel, native runtime or malicious filesystem certification without separate authority.

## 5. G3 — Prospective catalogue, source lock and durability before first DEV

Before any new DEV run, freeze a dated `P0A3G_DEV_CASES_PREDECLARED.md`, source/test/schema/config/fixture hashes, exact expected outcomes, status taxonomy, interpreter/binary identity, process tree and wall/CPU/memory/output/file/disk/recursion/concurrency budgets, full code diffs, run command and stop rules. The catalogue must use these **14 ordered engineering methods**, with exact fixture constructors bound in the lock before DEV:

| ID | Mandatory bounded expected outcome |
|---|---|
| G01 | Original signed source/archives, kernel hashes and R1 QC identities verified; no legacy evidence changed. |
| G02 | Correct nonempty worker stdout/stderr captured, independently re-read and recomputed length/hash matched. |
| G03 | New generic `forged_q` and `null_path_record` checker rejections produce authentic complete streams; no accepted false certificate. |
| G04 | Inject the R1-type 108-byte metadata/zero-byte retained-stdout mismatch; mandatory typed `EVIDENCE_STREAM_MISMATCH`, no success. |
| G05 | Truncated, altered and missing stdout/stderr records fail before checkpoint completion. |
| G06 | Swapped, duplicate, stale-run, wrong-worker and colliding case stream paths fail closed. |
| G07 | Interrupted write, short write, after-rename tampering and unverified retrieved archive fail closed; distinguish actual and simulated faults. |
| G08 | Real worker abnormal exit and genuine process timeout retain matching raw stream metadata and no completed certificate. |
| G09 | A normal saved-verdict recovery ignores stored verdict and completes only after independent fresh checker within the prospectively declared eight-second envelope. |
| G10 | An independent actual eight-second checker timeout returns `RESOURCE_INCOMPLETE` and no certificate. |
| G11 | Genuine caller-supplied test-only signed authority accepted solely in explicitly test mode after independent signature/key verification; wrong signer/key/mode/parent/hash rejected. |
| G12 | Missing authority, unsigned proposal presented as signed, tampered runtime or loaded-code mismatch reject without exact claim; disclose unattested loaded instructions. |
| G13 | Canonical byte/parser and independent reference negative regressions (forged score, invalid nested path, nonoptimal SO(2) witness) fail closed. |
| G14 | Existing generic R/Z/T/N mathematical relationships and immutable-kernel checks preserved; no new historical target, optimization or numerical threshold. |

If source analysis before this lock shows a case cannot be safely run on the stated host, declare its required negative/`NOT_TESTED` status prospectively and **STOP if that prevents mandatory completion**; do not delete or redefine cases. Subcases are subordinate to the 14 ordered methods and do not become new independent experiments. These are generic engineering tests only, never historical/statistical experiments. No case is allowed to pass on ZIP CRC or runner summary without independent per-worker stream/event identity checks.

**G-C1 must be durably saved and independently retrieved before G01 or any other DEV begins.** Include actual revised source, code/test diffs, full prospective catalogue and fixture constructors, locked budgets, schema/config/trust policy, and exact source hashes. If persistence/retrieval fails, STOP. R1 source and attempt numbers must remain unchanged.

## 6. G4 — Bounded DEV execution and immutable chronology

Execute the new registered 14-method catalogue only from the verified G-C1 lock in an isolated directory. Number attempts `P0A3G_DEV_01`, `P0A3G_DEV_02`, etc., never `P0A3F_R1_DEV_02` and never any historical D/E/F names. At most **three** prospective attempts against the same catalogue and predeclared envelope are permitted. If an attempt fails, record complete evidence, verify its **G-C2+ durable checkpoint**, and only then consider one separately documented code repair/diff and a newly numbered attempt. No failed attempt may be overwritten. If a substantive catalogue or policy change is scientifically necessary, STOP and seek new human-signed authority rather than retrospective alteration.

Store exact raw worker stdout/stderr, event records, byte/hash witnesses, process exits, signals, inputs, caller receipts, test-only keys' **public portions**, schemas, source/tests, environment, test-runner stdout/stderr and exit codes. No private keys, user credentials or sensitive host data. After every DEV or repair create a *new* immutable checkpoint, independently persist/retrieve and verify byte size, SHA-256, safe ZIP paths, complete internal manifest and stream/event reconciliation **before any further work**. An unverified raw stream is never counted toward a positive DEV outcome.

Do not execute unbounded arithmetic, targets or benchmarks. Mandatory negative status on budget exhaustion, unsupported environment or unverifiable streams. An actual false exact certificate, trust bypass or kernel contradiction immediately triggers quarantine and preservation of reproducer.

## 7. G5–G6 — Cumulative candidate, independent handoff and decisions

Package a cumulative unsigned candidate ZIP outside the Git repo. It must contain vetted full software/reference source (including the unchanged three kernels), exact baseline-to-revised diffs and hash table, protocol/GPG provenance identities, QCF01 original immutable evidence references, authentic recovery search ledger, external-signature authority threat-model report, canonical schema/config, G-C0/G-C1/G-C2+ identities, all prospective DEV attempts and raw streams, per-worker-event reconciliation CSV/JSON, exact runner transcripts, F1–F4 remaining-gap matrix, environment/pinning ledgers, and an **unfilled** independent QC checklist. Include README, immutable PACKAGE_INVENTORY and SHA256SUMS with self-hash exception; independently retrieve and verify the completed `G-CFINAL` against size/SHA/CRC/manifest/inventory and actual raw stream/event consistency. Do not merely report a filename or rely on an ephemeral workspace.

Dispositions must separate (i) signed mathematical theorem; (ii) R1 historical negative QC; (iii) new raw stream evidence closure; (iv) independent reference and input regression; (v) test-only vs real human-signed external trust; (vi) declared interpreter/host envelope; (vii) broader crash/power-loss/multiwriter protection; (viii) true loaded-code identity; (ix) candidate readiness; and (x) registered validation NOT RUN.

A complete candidate can be labelled **`P0A3G_ENGINEERING_CANDIDATE_SUBMITTED_FOR_INDEPENDENT_QC`** only if all mandatory checkpoints and deliverables exist and verify. Otherwise `P0A3G_ENGINEERING_INCOMPLETE` or `P0A3G_STOP_AND_QUARANTINE` with precise negative evidence. Even a perfect 14/14 engineering run is **not** `GLOBAL_CERTIFIED`, not full arbitrary-input software correctness and not a readiness/code-freeze authorization. Preserve the original R1 missing streams as a historical negative, regardless of successful new G results.

After delivery the user returns to the independent chat reviewer for substantive source, arithmetic, trust, logging, evidence and QC verification; Work shall not self-approve. Only if independent QC supports qualification may a **separate human-reviewed GPG-signed code-only freeze** of specific approved source, checker, schema, config, environment and external trust root be considered. A subsequent independent verification of that actual signing/deployment authority remains necessary before any readiness claim. Any unresolved mandatory barrier results in another accurately signed incomplete preservation, not favorable inference. P0A4 validation and future Hebrew/glyph/3D/QH studies are NOT AUTHORIZED here.

## 8. Human-only one-file protocol preregistration sequence

1. Human reviews this **complete** draft and confirms a clean feature branch at direct parent `d95c50ea96744ce266058c51f85fff320d1a27df`; verify signer fingerprint `D4EC014EEFCC90E619D2AA59A91239ABCF512130` locally. A changed branch head is a stop, not permission to reset.
2. Stage **only** `docs/v0_9/p0a3g_raw_worker_evidence_and_external_trust_followup_protocol_2026_10_21.md`. Verify exact downloaded SHA-256/Git blob, `git diff --cached --check` and exactly one added file. Do not stage this instruction README or any original evidence archive again.
3. Human alone `git commit -S` with the signed result's direct parent exactly `d95c50ea96744ce266058c51f85fff320d1a27df`, verify raw signature and GPG fingerprint, clean worktree and push only `hebrew-projection-capacity-v0.9`.
4. **Only after** the exact new signed commit/blob is independently checked shall a new Work execution handoff be authored and passed to a fresh Work conversation. Work then executes G0–G6 as authorized, with durable G-C0/G-C1/G-C2+/G-CFINAL gates and no Git writes.

**Decision of this proposed protocol:** permit one prospective, bounded new engineering lane to close the *new* raw-worker evidence integrity failure and exercise a non-production independently verifiable trust interface. Neither missing R1 stdout can be reconstructed by inference; no previously signed scientific or negative QC decision is changed.
