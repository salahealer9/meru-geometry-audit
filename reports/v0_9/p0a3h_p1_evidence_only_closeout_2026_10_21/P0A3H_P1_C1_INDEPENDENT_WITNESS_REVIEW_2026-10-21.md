# P0A3H-P1/A1 — Independent read-only P1-C1 source-lock witness review

**Review date:** 2026-10-21. **Status:** `P0A3H_P1_C1_PREEXECUTION_WITNESS_WITHHELD_PENDING_CONTROL_COMPLETENESS`.

**No release for `P0A3H_P1_DEV_01`.** This is a separate reviewer’s static source-and-archive assessment, not a signed protocol, not a registered P01–P06 trial, not a self-approved agent/source release, and not full execution security attestation.

## 1. Exact original objects

- Original uploaded `P0A3H_P1-C1.zip`: **308,794 bytes**, SHA-256 **`0ab255773debd5a68c21fa2555c954b347971d28902ee345beb1f254d02013d4`**.
- Original separately uploaded `P0A3H_P1-C1.zip.b64.txt`: **417,146 bytes**, SHA-256 `b27434e7b8dea722a2797f81d9bdb57090210ee40f3201bb848beb176ef5fc33`; independent decode equals C1 ZIP byte-for-byte.
- Original P1-C0: **348,416 bytes**, SHA-256 `067efd1e0fb66bc7bf5c61df186d43558ef2a81f223ca90912f67bca23439f5e`; its receipt is physically present in C1 and matches the uploaded original exactly (SHA-256 `469c1cc5d16555e5b8e56e906b4bd5a0dfc147a68c147d8eef932bacdc14bdd3`).
- Immutable authority: human-signed P1 `4c1634e6660a02ebdea62195f13fc4810fd08d41`; signed A1 `82dc0d2b2f2b81f90ec60dfed8e3aade19555d40`. Signing/lineage verification was established in preceding phase; this report is not independent trusted-key ownertrust certification.
- `P1_CANDIDATE_LOCK.json`: `18c7d153e236560e0e99738f50137f46bb1dae94beaf125340835dadacaf106e`.
- `P1_EXTERNAL_LOCK.json`: `9689d89685a8fda8c87964198cadda8c477b782d8a870bcdb14270d2f57e3f0d`.

## 2. Independent positive verification — archival and source scope

**71/71 independent read-only assertions passed** using a separate reviewer audit (see machine-readable results and source). The first audit script encountered two reviewer-only implementation errors before yielding a completed report; both were corrected without any C1 file edit or any C1 test invocation. The final audit reads bytes, manifests and Python ASTs; it does not import or execute any candidate, harness, verifier, fixture or registered test source.

- C1 ZIP: 149 safe, unique, regular members, CRC PASS, 148/148 SHA256SUMS lines, 147/147 inventory rows and all member size/digests match.
- C1 reference tree: 51/51 files byte-identical to signed-preserved original R2-C1-REV1 candidate and original `SOURCE_LOCK`; R2 original ZIP SHA-256 `b34a3cd2c27f9384adb7427fa6628d6c08e15712e73542bda80eaeef989009b1` independently recomputed.
- C1 derivative tree: same 51 source paths, all match derivative lock; only `schemas/v0_9/p0a3g/resource_policy.json`, production `src/meru_geometry/v0_9/qo2d_exact/identity.py`, and reference `reference/v0_9/qo2d_exact/identity.py` differ. All other 48 files unchanged; exact before/after 51-row ledger reproduced.
- Immutable kernels still byte-identical: `algebra.py` SHA-256 `442065847937252db00d3f63b02184c15d57989f958f764c5c731cb385de6d2d`; `core.py` `37701d034d98725673240a881420892893906c70387f68432b5993f8557dd420`; reference `arithmetic.py` `72b3c37f02be65b2df7616a94e84601d66cf4af5b7a50e878724de647e5bf0ba`.
- Production and reference P1 identities agree on P1 protocol, actual signed P1 parent, 18-commit ancestry, derivative source baseline and measured `/usr/lib/python3.11` root. Original authority schema remains untouched; unchanged resource caps independently compared.
- External lock: 23/23 source/fixture/comparator files match exact hashes/lengths. All six new external Python files parse under 3.11 grammar as text. No runtime compatibility claim is inferred from parsing.
- Fixture provenance: four R2 requests byte-match original R2-C1-REV1; P06A is the single static `max_vertices` 8→9 change and exceeds frozen cap 8.
- Crucially, all **eight** P05 comparator payloads are byte-identical to originals in `P0A3G_R2-C2.zip` SHA-256 `860d93dce952a73b65b097e3f7b4da420c0a327ee0ca8b6d4c213865db2d1cbb`. This historic ZIP has Git blob SHA-1 `954e27a424a2b047b026a98f390d5687ecc42521`, independently consistent with the file at signed preservation commit `e491e1e9f96391cd512db0dd528765d63bc179c1`. This verifies provenance bytes, **not** prospective cross-runtime equality.

## 3. Gate findings — why execution witness is withheld

**W01 — BLOCKING — whole-attempt disk bound lacks external enforcement.** Signed P1 §3 retains a **whole-attempt disk ≤16 MiB** limit. The unchanged candidate's `supervisor.disk(d)` enforces its `run_disk_bytes=16,777,216` only *per candidate run directory*, while the P1 driver accumulates the extracted C1 trees and multiple P02–P06 run directories in a larger `WORK` hierarchy. `p1_external/P1_DRIVER.py` has no whole-worktree disk quota/check and sets its runner `RLIMIT_FSIZE` to **64 MiB per file** (not a cumulative disk quota). `p1_external/P1_C2_PACKAGER.py` also traverses unbounded aggregate attempt contents. Therefore the locked harness cannot substantiate the literal whole-attempt cap. A compliant independent containment mechanism with measured evidence and pinned semantics must be provided in a prospectively revised, fresh-witnessed C1, or an explicit human-signed reinterpretation is required; a silent post-lock reinterpretation is forbidden. If infeasible, fail closed `ENVIRONMENT_UNQUALIFIED` / `P0A3H_P1_INDEPENDENT_QC_INCOMPLETE`, not PASS.

**W02 — MATERIAL PRE-EXECUTION GATE GAP — human release not verified by the driver before first launch.** `P1_DRIVER.py` accepts only `--release-sha`, `--c1`, `--work`; it compares the C1 digest, but never requires or archives the distinct **human-relayed exact-digest release certificate before** `FIRST_P1_CANDIDATE_INVOCATION`. The C2 packager requires a release certificate **after** the attempt, leaving the pre-run authorization chronology dependent on operator assertion. Signed P1 §5 requires witness **and a separate human release**. Strengthen the revised driver to take/check original externally issued human-release bytes before any P01–P06 candidate invocation, preserve a prelaunch hash/timestamp and enforce byte-identity again in C2. A text match alone is not cryptographic human authentication; human-origin witnessing remains separate.

**W03 — REVIEW LIMITATION — P1-specific external schema is present but not used.** `p1_external/schemas/p1_authority_envelope.validation.schema.json` is source-locked and `p1_authority.validate_p1_envelope` is defined, but no other external module invokes that helper. P1 lineage is still enforced by the actual candidate authority gates, so this is *not* evidence that an old-lineage envelope would be accepted. It prevents claiming an independent schema-validation execution that the locked runner does not perform. Clarify intended role and, if required for P1's locked acceptance interpretation, make the schema check operational in a fresh C1 revision without weakening the actual authority gates.

**W04 — RESIDUAL UNKNOWN — no registered execution yet.** Local Python 3.11/OpenSSL Ed25519 compatibility, worker VmSize/startup margin, exact P05 3.11-versus-3.12 arithmetic outputs, controller timeouts, Linux resource enforcement and live raw-stream relationships remain unmeasured. This uncertainty alone is **not** an excuse for prelock rehearsals or modifying expected outcomes after execution. The locked first attempt may fail, and that failure must be preserved.

The P03 wrong-scope/revocation/old-lineage/tampered-signature cases and P04 `REAL_HUMAN_SIGNED_AUTHORITY_ABSENT` cause-chain route appear *statically congruent* with the frozen implementation. P06's over-cap request and pre-existing `dev_fault='timeout'` are within the signed P1 portability catalogue as a static interpretation, subject to first-attempt results. This static review does not claim they pass in runtime.

## 4. Disposition and next authorization

- **C1 original bytes:** authenticated and preserved; **ARCHIVAL/SOURCE-LOCK INTEGRITY PASS**.
- **Full pre-execution witness:** **WITHHELD** due to W01, with W02 to resolve before launch. This is **not** `P0A3H_P1_C1_LOCK_WITNESSED` and is **not** an exact-C1-SHA human release.
- **Registered `P0A3H_P1_DEV_01`:** **NOT AUTHORIZED**; absolutely no P01–P06 invocation or dry runs on either the authoring host or operator host.
- **Next:** retain original C1 ZIP/base64/receipt under original SHA; prepare a separately named **`P0A3H_P1-C1-REV1.zip`** (or preserve an explicit preflight-stop packet if W01 cannot be fulfilled). Revise external enforcement/authorization machinery and locks **before any experiment**; never edit the three-source-file derivative unless another signed scope amendment permits it. Recompute all source manifests, source diff, receipts and expected adapters; independently fresh-read back revised original; disclose author/code-review roles; submit BOTH original rejected C1 and REV1 for a fresh witness.
- **No Git commit/push, original archive overwrite or post-outcome reconstruction.** Original L1 and P1 historical conclusions unchanged. `LOADED_CODE_IDENTITY_UNVERIFIED`, `PRODUCTION_CODE_AUTHORITY_ABSENT`, no P0A4 or deployment authority remain in force.

**Authorship disclosure:** the derivative/external harness was authored by Claude, who also authored the original candidate; this review was written separately and recomputed source bytes/protocol comparison, but the reviewing assistant participated in drafting P1/A1 protocols and some earlier intake tooling. No organizationally independent runtime attestation or absence-of-hidden-runs proof is claimed.
