# P0A3H-P1-A1 — Prospective Three-File Identity-Rebinding Scope Amendment

**Programme:** Meru Geometry Audit v0.9; P0A3H-P1 cross-host portability of the bounded exact planar 2D QO candidate.
**Date:** 2026-10-21. **Repository:** `salahealer9/meru-geometry-audit`; **branch:** `hebrew-projection-capacity-v0.9`.
**Required direct parent of this proposed human-signed amendment:** `4c1634e6660a02ebdea62195f13fc4810fd08d41` (signed P0A3H-P1 protocol).
**Original P1 protocol Git blob:** `557e778363c068b893855928f973dd3e9071597e`.
**Expected human GPG signer fingerprint:** `D4EC014EEFCC90E619D2AA59A91239ABCF512130`.
**Signing scope:** add **only** this Markdown document. No code change, existing-file modification, rollback, branch reset, source freeze, experiment, merge or force push. Only the human may stage, sign and push.

## 0. Reason for amendment and historical preservation

The original signed P1 §2 limits derivative-candidate edits to two files, `schemas/v0_9/p0a3g/resource_policy.json` and `src/meru_geometry/v0_9/qo2d_exact/identity.py`. Subsequent read-only, **pre-execution** inspection of the immutable original P0A3G R2-C1-REV1 archive found that the separately written reference checker's `reference/v0_9/qo2d_exact/identity.py` also enforces (i) the old P0A3G authority lineage in `PINS` and (ii) the fixed `/usr/lib/python3.12` standard-library root. Every positive check-worker run calls this gate; the original two-file change alone cannot meet P1's true new-lineage and measured Python 3.11 requirements. This is a prospectively detected **source-scope blocker**, not a failed P1 portability test.

The engineering agent stopped and reported **`P0A3H_P1_SCOPE_AMENDMENT_REQUIRED`** before derivative-source edits, candidate imports, test execution or P1-C0/C1 construction, according to its dated operator statement. The separate reviewer has independently read the original R2-C1-REV1 ZIP and verified the relevant fixed source bytes and checker call path. The no-execution history beyond available files remains an agent assertion, not independently observed host telemetry. This amendment does not overwrite or relabel the original P1 two-file preflight discovery.

**Retain the following original reports unchanged, as historical source evidence to be physically carried into future P1-C0:**

| Original submitted evidence | Size and SHA-256 |
|---|---|
| `P0A3H_P1_P0_STATIC_FEASIBILITY_REPORT.md` | 13,613 bytes; `50158e256f78748ba3fde6467c461869adbf5093830e008de8116a646c84789f` |
| `P0A3H_P1_P0_STATIC_FEASIBILITY_FINDINGS.json` | 3,263 bytes; `e46b172389d8ef4fc9975daa75a562ff4e60a1050487bd18fe5b4b5125f55179` |

No P1-C0 or P1-C1 existed at the time of that report. The previous P0A3H, L1, R2 and other incomplete/negative/administrative-only qualifications, and the signed L1 closeout `8f4163df75ad33f9892b72cd62b75dbda24f0505`, remain immutable. P0A4, Hebrew target work and H01–H07 remain unexecuted and unauthorized under this amendment.

## 1. Preserved source authority and independently confirmed blockage

- Signed original R2-C1-REV1 archive: **197,250 bytes**, SHA-256 `b34a3cd2c27f9384adb7427fa6628d6c08e15712e73542bda80eaeef989009b1`; original 51-file `lock/SOURCE_LOCK.json` SHA-256 `abff7aa8df19f73e070d9f06ebd23334f8d98b45c1736d38399b845c69835902`.
- Frozen checker identity file `reference/v0_9/qo2d_exact/identity.py`: SHA-256 `9bb68f707bb1c3bf5802276408b8ad4800f2b2f78a502f9217ad704bba04aa24`. Lines 16–17 contain `PINS` and exact old lineage; line 23 requires equality to these pins; line 48 recomputes eleven dependency hashes beneath `/usr/lib/python3.12`. `reference/v0_9/qo2d_exact/checker.py` line 96 calls its `external_identity.verify(...)` before accepting a certificate. `supervisor.py` checks the reference worker result before completion.
- Original candidate-side `src/meru_geometry/v0_9/qo2d_exact/identity.py`: SHA-256 `77aef8baaaa53e2642e6b13bbff86ca74401e749c6835aadd823a6ce074f7076`; contains the same old lineage and Python 3.12 root. Original resource policy: SHA-256 `9b7221fcfb54dc313874c9873423001ae7856b3a1889f12b92f9638abd904e09`.
- **All three immutable mathematical kernels remain byte-identical:** `src/meru_geometry/v0_9/qo2d_exact/algebra.py` `442065847937252db00d3f63b02184c15d57989f958f764c5c731cb385de6d2d`; `src/meru_geometry/v0_9/qo2d_exact/core.py` `37701d034d98725673240a881420892893906c70387f68432b5993f8557dd420`; `reference/v0_9/qo2d_exact/arithmetic.py` `72b3c37f02be65b2df7616a94e84601d66cf4af5b7a50e878724de647e5bf0ba`.

A failed essential source check, missing original report/ZIP, source identity mismatch, unavailable required local dependency or unsatisfied three-file adaptation is a **fail-closed preflight stop**; no invisible source replacement is permitted.

## 2. Exact amendment to P1 §2: three files, no fourth

**Supersede only the permitted derivative-candidate edit set in original P1 §2** with the following three files. All other text and rules of original signed P1 remain binding.

1. `schemas/v0_9/p0a3g/resource_policy.json` — **unchanged from P1's previously permitted delta:** only the four fields `interpreter`, `interpreter_sha256`, `openssl`, `openssl_sha256` may be rebound to actually measured pinned local binary identities. No resource/security cap or schema change.
2. `src/meru_geometry/v0_9/qo2d_exact/identity.py` — **unchanged from P1's previously permitted delta:** replace only the old Python 3.12 standard-library root with the genuinely measured Python 3.11 root; change only `PROTOCOL`, `PARENT`, `ANCESTRY`, `BASELINE` to the truthful, exactly registered P1 lineage values defined in §3 below. Do not change `authority()`, `verify()`, mode semantics, dependencies list, signature verification, source-map enumeration or fail-closed handling.
3. **Newly permitted** `reference/v0_9/qo2d_exact/identity.py` — change **only** the `PINS` values `protocol_commit`, `signed_parent`, `git_ancestry`, and `baseline_archive_sha256` so they exactly equal the values from the production identity module, and change **only** the Python 3.12 standard-library root literal inside its environment fingerprint construction to the exact same measured Python 3.11 root. Retain `PINS` `schema` (`p0a3g-authority-envelope-1`) and `loaded_code_identity` unchanged; retain all eleven dependency relative names, source enumerator, independent pure-Python Ed25519 verification, strict envelope/receipt schemas, fail-closed status, and `DEPLOYMENT` refusal. No other edits in this file.

A final static diff must demonstrate that **exactly these three original 51-file candidate members differ** (or a prospectively justified subset); the other original members and all three kernels remain byte-identical. Preserve complete old/new per-file SHA-256/byte lengths, syntactic edit locations and field-level comparisons in `P1_CANDIDATE_LOCK.json`, with the original and derivative trees isolated outside Git. No additional files may be inserted into the derivative's 51-file candidate scope. New external builders, synthetic fixtures and independent verifiers stay outside it. If any fourth file, new authority key/mode, relaxed bound, changed mathematical checker, or unanticipated runtime modification is needed, **STOP** and seek a separately signed, prospective A2 amendment; do not patch informally.

## 3. Deterministic identity and lineage choices (resolve open questions before C1)

This amendment prospectively selects **one** representation. Production `PROTOCOL`, `PARENT`, `ANCESTRY`, `BASELINE` and checker `PINS` must agree exactly:

- `PROTOCOL` / `PINS.protocol_commit` = **`4c1634e6660a02ebdea62195f13fc4810fd08d41`**, the human-signed foundational P1 portability protocol, **not** the old P0A3G commit.
- `PARENT` / `PINS.signed_parent` = **`8f4163df75ad33f9892b72cd62b75dbda24f0505`**, the actual direct parent of that P1 protocol commit.
- `ANCESTRY` / `PINS.git_ancestry` = the **complete ordered first-parent Git commit-SHA chain from P1 `4c1634e6...` (inclusive) back through signed P0A3D `59eb47f7500d57866e4935822b78a555d3bcb515` (inclusive)**, in newest-to-oldest order. Obtain these real full commits from Git; verify every parent edge and disclose any unsigned/non-first-parent/omitted intermediate. Lock the complete literal list in C1 before any P1 execution. Do not guess the list, truncate it to named anchors, or modify it after observing outcomes. A1 amendment's eventual commit is **not falsely represented as P1's parent**: instead pin its exact signed commit/blob separately in `P1_CANDIDATE_LOCK.json`, all external manifests, and witness/release records.
- `BASELINE` / `PINS.baseline_archive_sha256` = **`b34a3cd2c27f9384adb7427fa6628d6c08e15712e73542bda80eaeef989009b1`**, the exact source archive from which the *new derivative* is copied. The old `6ec2b6e96234836d629398fb7fc781909de8b47b0bf80f5cae11202620ff2f15` is retained only as the **historical R1-CFINAL referent** in provenance registers, never passed off as the P1 derivation input.

The current `p0a3g-authority-envelope-1` and `p0a3g-caller-receipt-1` format strings remain **legacy field-schema identifiers**, not authority to accept P0A3G lineage. Their enforced P1 lineage values must be those above. The existing `schemas/v0_9/p0a3g/authority_envelope.schema.json` has old `const` literals and is **frozen historical schema data**, not a valid schema for new P1 envelopes. It must remain byte-identical and its non-use in the P1 runtime call path must be independently demonstrated through static review. Supply a **new, clearly named P1-specific external envelope validation schema** under `p1_external/` and pin its exact bytes/expected P1 values before release. If runtime use of the old JSON-schema constants is discovered, stop for A2; do not surreptitiously edit the old schema.

New signed P1 + A1 Git identities and the **new derivative source-file manifest** are mandatory in the external candidate-lock and test-authority receipts. A test-only envelope with old P0A3G lineage must be rejected even if its signature is otherwise syntactically correct. No production signing key, HUMAN_SIGNED_CODE_FREEZE mode acceptance, or real deployment identity can be introduced.

## 4. Continuation and pre-execution limits

After this one-file A1 amendment is **human-signed and independently authenticated**, P1-P0 may resume **only for static host/source validation and a new, separately named original P1-C0**. Preserve the original two-file-blocker reports listed in §0. The local operator must remeasure and lock real `/usr/bin/python3.11`, `/usr/bin/openssl`, eleven stdlib dependencies, path/realpath semantics and relevant OS/library/resource limits; the recorded prior CPython 3.11.2 and OpenSSL 3.0.22 identities are hypotheses to reconfirm, not dynamically changing pins. Archive exact original preregistration, this signed A1 amendment, literal P1 first-parent chain, original source/previous-QC negative statuses, engineering blocker reports, actual host readings, authorship and no-test chronology into P1-C0. Durably preserve and fresh-read back original C0; it may not be called a retrospectively constructed lock.

P1-P1 may then statically prepare the **three-file derivative** and the already registered P01–P06 portability adapters, test-only envelope builder, new P1 schema and external recorder. This is **source construction, not candidate execution**. No P1 candidate imports, worker launches, signature trials, dry runs, test execution, numerical previews, or regression calls until a complete P1-C1 is independently witnessed and a separate exact-digest **human** release is relayed in the original P1 format. All C1 sources/fixtures/verdicts, the new authority constants and module/environment source diffs must be locked before any test. Existing P1 P01–P06 methods, order, all resource and trust restrictions, C2's physical prior-receipt inclusion, CFINAL nesting, reviewer independence disclosures and outcome taxonomy remain unchanged.

The original H02–H05 challenges are **not** reintroduced into P1; P1's test programme is portability only. The same authoring AI cannot be represented as an organizationally independent reviewer of its own changes. If platform safety restrictions, impossible runtime contracts, scope mismatch or source-authentication discrepancies block preparation, stop; do not bypass controls. P0A4 and code freeze remain unauthorized; `LOADED_CODE_IDENTITY_UNVERIFIED` / `PRODUCTION_CODE_AUTHORITY_ABSENT` remain in force.

## 5. Explicit outcome and signature gate

Before signature this document is `P0A3H_P1_A1_DRAFT_NON_AUTHORIZING`. Once **the sole human** verifies the actual Git HEAD, clean worktree/index, direct parent `4c1634e6660a02ebdea62195f13fc4810fd08d41`, expected GPG fingerprint, immutable report/source hashes and a **one-new-Markdown-file-only** staged diff, human `git commit -S` and push establish `P0A3H_P1_A1_THREE_FILE_SCOPE_AMENDMENT_REGISTERED` (administrative only). The original P1 two-file scope becomes superseded solely to the extent explicitly set out in §2–3. The P1 feasibility discovery remains preserved as pre-execution `P0A3H_P1_SCOPE_AMENDMENT_REQUIRED` rather than changed to PASS; successful signature lifts only that named prospective *scope* blocker, subject to host preflight.

**No P1 registered tests, no engineering QC PASS, no deployment authority and no P0A4 authorization arise from signing A1.** The human must return the new signed SHA and verified direct-parent/remote push, after which an independent reviewer can issue a *preparation-only* local P1-C0 handoff. If parent identity, original evidence or source verification fails, STOP without signing or running anything.
