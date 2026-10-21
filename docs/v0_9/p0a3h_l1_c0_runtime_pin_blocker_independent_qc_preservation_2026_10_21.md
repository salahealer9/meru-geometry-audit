# P0A3H-L1 — C0 Integrity Pass and Runtime-Pin Blocker: Additive Independent QC Preservation

**Prepared:** 2026-10-21. **HUMAN SIGNING CANDIDATE — unsigned until the human signs and pushes.**
**Repository/branch:** `salahealer9/meru-geometry-audit` / `hebrew-projection-capacity-v0.9`.
**Required direct Git parent:** `39364f5a4345c8b60a879f6411b8d80cc6c299c6` (signed L1 protocol; protocol Git blob `6a574b7a6b442ed909d9c294341b3865c8be6020`).
**Expected human GPG fingerprint:** `D4EC014EEFCC90E619D2AA59A91239ABCF512130`.
**Additions only:** precisely this document and six files in `reports/v0_9/p0a3h_l1_c0_runtime_pin_blocker_checkpoint/`; **no modification** to signed protocols, frozen kernels, original 51-file candidate, or old checkpoint archives.

## 1. Evidence and exact preserved objects

- Original L1-C0 ZIP: **105,474 bytes**, SHA-256 `774e58c72921bdf97cf14cd9628278c4bab1c327086e9297879c8a46b4117e3a`. Its prior read-only independent byte/source QC **PASS** is retained, including full 51/51 frozen source matching and 21-member/20-checksum/19-inventory archive integrity.
- Original L1-C0 receipt and original local readback JSON are preserved byte-identically, explicitly distinguishing same-host readback and operator no-execution assertions from independently observed telemetry.
- Original local runtime-pin audit JSON: **3646 bytes**, SHA-256 `3b7dcc3bc0f0f17e90cf28fb1d9d9c8cb1bc0bc37bae963a06da2d3f2a602ca8`. Its passive results were independently reconciled with source identities from original signed-preserved R2-C1-REV1/G-CFINAL, without importing or executing candidate code.
- The separate independent QC ZIP records the reviewer report and **34 deterministic positive file/record assertions** (not experimental trials). Exact immutable identities of the five evidence payloads are in the adjacent `P0A3H_L1_RUNTIME_BLOCKER_PRESERVATION_MANIFEST.sha256`.

## 2. Correct scientific and administrative scope

**Disposition: `P0A3H_L1_PREFLIGHT_INCOMPLETE` (`ABSOLUTE_RUNTIME_PINS_UNSATISFIED`).** Local audit records no `/usr/bin/python3.12`, wrong immutable `/usr/bin/openssl` digest, and missing 11/11 fixed Python 3.12 standard-library paths. These are candidate-internal absolute requirements of `resource_policy.json`, `supervisor.py` and `identity.py` as checked against original R2 source; cross-host permission does not implicitly override them. **L1-C0 byte/source QC PASS remains intact**. Neither the registered local seven-case attempt nor L1-C1 source lock occurred. `P0A3H_L1_DEV_01` and P0A4 are **NOT AUTHORIZED**, no method H01–H07 passes or fails scientifically, and the original P0A3H H-C0 safety interruption remains separate.

The operator's local file existence and no-test claims are evidence to be reviewed, not remotely witnessed process telemetry. This independent QC itself involved only static file reads/checks. No production signing, code-only freeze or full loaded-code identity attestation is claimed. Earlier R1/G/R2 negative conclusions, C3 administrative-only success, `LOADED_CODE_IDENTITY_UNVERIFIED` and `PRODUCTION_CODE_AUTHORITY_ABSENT` remain unchanged.

## 3. Future governance

This is **evidence-only preservation**, not execution authority or an implicit amendment. To proceed one must separately choose either (A) verified recovery of exact original pinned runtime bytes under a suitable isolated measured environment, **without changing the original source**, or (B) a **new human-signed prospective portability protocol**, disclosing changed runtime/source identity as a different software experiment. An ordinary package upgrade, symlink or silent hash patch cannot cure this failure. The separate H04 import-visibility feasibility gate also remains unresolved. Do not attempt H01–H07 before a fully witnessed new lock and explicit SHA-specific release.

**Human-only signing:** check exact required parent locally and remotely, valid signature/fingerprint, complete original manifest, stage only seven additions, `git diff --cached --check`, human `git commit -S`, verify valid new signature and parent, then push. No agent or assistant is authorized to sign or push.
