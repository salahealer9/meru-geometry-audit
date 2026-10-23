# Meru v0.9 / 3D-V5B — MOD-G0-F01 Manifest-Coverage Corrective Preregistration

**Date:** 23 October 2026  
**Document status:** **HUMAN SIGNING CANDIDATE — UNSIGNED — NOT AUTHORISED FOR EXECUTION**  
**Identifier:** `MERU_V5B_MOD_G0_F01_CORRECTIVE_PREREG_2026_10_23`  
**Repository:** `salahealer9/meru-geometry-audit`  
**Scientific branch:** `hebrew-projection-capacity-v0.9`  
**Proposed additive path:** `docs/v0_9/meru_3d_v5b_mod_g0_f01_manifest_coverage_corrective_preregistration_2026_10_23.md`  
**Required direct parent — signed MOD-G0-C historical failure closeout:** `8d8eb31c7f3f4f6e9b1a603bbfa8e87b6d88c52f`, **only if the owner's local branch and freshly fetched remote branch both still point to this exact commit at signing time**. Otherwise STOP and revise the signing plan; do not force history to fit.  
**Expected human signing fingerprint:** `D4EC014EEFCC90E619D2AA59A91239ABCF512130`.

## 0. Controlling authority and what this document does not do

This is a **prospective, limited engineering correction and requalification charter**, not a retrospective edit to MOD-G0, a reinterpretation of the signed V5B scientific protocol, or a declaration that MOD-G0 has passed. It may be submitted for human approval and, subsequently, a *separate* one-file signed documentary preregistration. **Signing by itself does not authorise developer execution, independent QC, a gate seal, or scientific work.** Each execution needs the owner's distinct express authorisation. No current work is authorised by this draft.

Controlling immutable ancestry, in direct sequence:

| Object | Signed Git commit | Expected Git blob |
|---|---|---|
| V5B scientific protocol | `006b12e6800b29e41dc8e1854acdee528b822e22` | `2fab1e49b99473de4de2517e29225f4193c5b9ac` |
| DEV-R1 corrective protocol | `54bdb1f6baab62fbf7be8b6057d2761a3286053d` | `bed31bcd4be6c2418cfa8ad024be7e747d57b385` |
| Historical DEV-R1 / QC-R2 closeout | `e1da15b18ecaa4da2a0d15eed3d2864f1d6ea11b` | `179111872b3c4dca29736261be1453f0394b22ab` |
| Modular qualification amendment | `5de3a2bac49e4cacbe49512f5674ead036c16091` | `5625041fcd0c90621a22667cb18e8cd2c49670bb` |
| MOD-G0 authority / archival / host charter | `e8fb37660b78065537be06f561ad7208cd0fb0f6` | `700ef5d263484c6d98ce22cdc0332ea32c18062c` |
| **MOD-G0-C independent failure and evidence closeout** | **`8d8eb31c7f3f4f6e9b1a603bbfa8e87b6d88c52f`** | **`6e033c559c3d62ccddc4118d3b482d8f8f4b8f96`** |

The MOD-G0 charter text SHA-256 is `92f50d2ea25158a6e0ba5fdf92f9a27a1809983e22790961cf22237e959de46a`. The signed MOD-G0-C historical closeout is the sole immediate parent of this proposed F01 preregistration; its exact text SHA-256 is `28522145b23c7842bd9c38df774942fef573ad9245c7109b288512133089228b`. The closeout preserves `MOD_G0_FAIL` without qualification or execution authorisation. Before any work, independently retrieve the **full signed charter** directly from the pinned Git object. Distinguish GitHub `verified` attestation, local cryptographic verification with an imported public key, and the owner's *separately observed* local `TRUST_ULTIMATE`; do not claim a trust level not personally observed.

The original three 30-minute MOD-G0 execution slices have already been used. This is a request for **new, explicitly bounded future execution authority**, not an extension of that exhausted budget.

## 1. Historical result to preserve, not overwrite

On 23 October 2026 the separate Astra High MOD-G0-C review ended **`MOD_G0_FAIL`**, subsequently recorded in the signed historical closeout at commit `8d8eb31c7f3f4f6e9b1a603bbfa8e87b6d88c52f`. The controlling immutable review artifact is:

- `MERU_MOD_G0_C_QC-C-CP3_FINAL_2026-10-23.zip` — **14,529,680 bytes**, SHA-256 **`ecaf6b14545fc432c33e6d263b991441eaf015778a3173ec67a62790e589ffb2`**, with independently preserved QC-C-CP0, CP1, CP2 and CP3 evidence and external final-delivery receipt.
- Within it, `STATIC_VERIFIER_FINDING.md` — SHA-256 **`1a15870f173d8847e1571799b1804591e91531d262ab8c125aed4e96366768a9`**.
- Authenticated original custodian package `MERU_V5B_MOD_G0_AB_CUSTODY_HANDOFF_2026-10-23.zip` — **816,990 bytes**, SHA-256 **`ff21850e30262c4678e97dd9d4bfc913d0be54e2b7480426ad2ebe8b65bf7d47`**.
- Exact historical subject file inside the QC-C evidence: `custodian_readonly/scripts/g0a_verify.py` — **19,418 bytes**, SHA-256 **`0d9b1ce871de441520726fc91d09608e3a286d4ee665e8293421a51479eede65`**.

**Finding `QC-C-F01` (SOURCE-CONFIRMED, not dynamically tested against the custodian program):** In the historical `verify_zip()` source, line 100 computes unlisted ordinary payload members (`unlisted_in_scope`), but the rejection predicate at line 104 considers only missing, mismatched or unparsable manifests. Consequently, an archive with the correct caller-supplied outer identity and an additional unlisted ordinary payload can reach `INTACT` at line 107. The independently constructed inert fixture `fixtures/C19.zip` is **404 bytes**, SHA-256 **`178685e41d7c41c8334778acca6460bdfc1f1d76f2b9de135e3d03d41fba3589`**. Independently rejected by Astra's oracle, it was **not run against the archived custodian script**. The same source has a related *no-recognized-manifest* route (`mans=[]`) to `INTACT`; Astra's `fixtures/C28.zip` is **123 bytes**, SHA-256 **`1e4c619e2fbc1a35c18bc200c6b21b040c9fb28c46897ea2740553285a41e7e5`**.

The finding does **not** assert corruption, changed hashes or invalid manifests in any original submitted archive. The original signed authorities, archive identities and checkpoints authenticate within their documented scope; G0-B host-capability reporting also has limited positive support. Neither observation repairs `QC-C-F01`. The original `MOD_G0_FAIL`, 22 scoped PASS / 1 FAIL / 2 INCOMPLETE QC-C checklist, and all historical QC-R2 `29 PASS / 8 FAIL / 5 INCOMPLETE`, `R2-F01`–`R2-F06`, including permanently absent R2-F05 logs, are **immutable history**.

## 2. One corrective question and acceptance claim

**Question:** Can a newly versioned, explicitly scoped **MOD-G0 archive verifier candidate** reliably refuse to describe a ZIP as *fully integrity-verified / manifest-complete* unless every in-scope ordinary payload has been authenticated by the manifest coverage contract applicable to that archive, while preserving separately registered outer-byte integrity and legitimate, precisely enumerated manifest self-exclusions?

The intended successful claim is strictly:

> For a registered archive class that requires an internal complete-coverage manifest, the corrected G0 verifier returns a positive *complete-manifest* decision only if the expected manifest is present and parsed strictly, every required in-scope payload member is covered exactly as required by that class, every listed member is present and hash-matches, and no unlisted payload is present, subject solely to approved explicit exclusions. Negative examples fail closed. This does not prove correctness of material *inside* the archive or host resource enforcement.

**No globally permissive default.** Archive classes using only a registered immutable outer SHA-256, or requiring a different/partial manifest convention, must be **identified positively by an independently pinned per-class contract**. They may receive a separately named `OUTER_IDENTITY_ONLY` / `MANIFEST_NOT_APPLICABLE` claim if supported; they must **never** be silently labelled `MANIFEST_COMPLETE` or accepted as an unqualified generic `INTACT`. If it is unclear whether a manifest is required, fail closed as `UNQUALIFIED_ARCHIVE_CLASS` / `NOT_OBSERVED`, not PASS. Do not introduce a blanket “all ZIPs must contain SHA256SUMS” rule that breaks authenticated historical classes without first identifying their exact signed conventions.

## 3. Authorised engineering footprint, if separately approved

The developer may **read** the immutable historical custodian ZIP, its source, the signed MOD-G0 charter and Astra's CP3 archive. All are immutable inputs. Work must occur in a new isolated scratch tree, with a detached/read-only baseline if Git objects are needed. **Do not edit or replace the historical `g0a_verify.py` inside the custodian ZIP, its manifests, logs or checkpoint archives.**

Only the following *new, versioned derivative outputs* may be created:

1. A corrected candidate of the G0-only ZIP verification component, derived from the exact historical source preimage and accompanied by its exact textual diff; maintain the existing outer-hash, path, duplicate, symlink, CRC and decompression guards unless an unavoidable, narrowly evidenced adjustment is separately approved.
2. A declarative `MANIFEST_COVERAGE_CONTRACT.json` listing, by exact immutable archive identity and class, required manifest name(s), relative scopes, permitted exclusions, expected cross-manifest relations and whether any archives are permitted *outer-identity-only* assessment. Every exception must have a documented reason and its authenticating outer SHA-256; no wildcard exclusions inferred merely from filenames or convenient locations. The independently reviewed historical special cases (manifest excluding itself, `SHA256SUMS` covering `MANIFEST`, intake `INPUT_IDENTITY.json` excluded locally but authenticated by a controlling outer manifest) must be evaluated explicitly before freezing the policy.
3. New G0-F01-only hostile and compatibility tests, an independently reproducible fixture generator, machine-readable coverage matrix, source/hash manifests, diff, raw stdout/stderr and exact exit-code logs, and durable release/checkpoint packages.

**No amendments** to the scientific V5B protocol, existing G0 charter, signed scientific branch implementation, geometry kernels, resource supervisor, registered surrogates, historical QC finding files or their identities. No opportunistic parser hardening, CPU semantics change, host-enforcement correction, general refactor or scientific computation is admitted by this F01 correction. Any discovered extra defect becomes a separate recorded finding requiring a new prospective decision.

## 4. Predeclared behavior and hostile requirements

The developer must commit to an expectation/fixture register (content-hashed and packaged in the initial checkpoint) **before writing or executing the corrected checker**; identify any newly discovered cases as exploratory, not retroactive preregistration. The later independent reviewer must separately seal its *own* expected outcomes and fixtures **before seeing the corrected implementation**. The reviewer's oracle must be independently written, not a call to the developer function.

| ID | Inert case / condition | Required result |
|---|---|---|
| F01-P01 | Registered complete-manifest archive, every payload covered and matching, exclusions explicitly authorised | `MANIFEST_COMPLETE` supported; outer identity separately checked |
| F01-N01 | `C19` equivalent: additional ordinary payload absent from checksum manifest, outer hash correctly registered to the fixture | Reject complete-manifest claim; report exact unlisted member |
| F01-N02 | `C28` equivalent: no recognised required internal manifest | Refuse complete-manifest claim; explicit missing-manifest reason |
| F01-N03 | Empty/parseable manifest with ordinary payload(s), or empty manifest substituted for required coverage | Reject, including zero verified entries where payloads require coverage |
| F01-N04 | Nested payload not covered due to manifest-directory scope or a sibling/parent-directory loophole | Reject under the applicable class scope |
| F01-N05 | One missing listed member, one altered listed payload, or digest parse error | Reject and preserve existing specific failure reason |
| F01-N06 | Missing required second manifest, contradictory SUMS/MANIFEST entries, malformed digest record or duplicate manifest declaration | Reject where the exact class contract requires both and unambiguous coverage |
| F01-N07 | Unlisted payload disguised as a manifest filename or hidden behind an overly broad basename exclusion | Reject unless it is the *exact* permitted meta-entry at the exact approved path |
| F01-N08 | Unapproved or unregistered archive class, purported exclusion lacking signed-byte binding | No `MANIFEST_COMPLETE`; fail closed or explicitly limited outer-only claim |
| F01-N09 | Wrong registered outer hash even if internal checksums are recomputed correctly | Preserve `OUTER_HASH_MISMATCH`; never upgrade to registered-archive acceptance |
| F01-C01 | Authentic custody archive with documented manifest self-exclusions | Preserve correctly bounded success |
| F01-C02 | Authentic historical QC-R2 archive and nested registered checkpoint classes | Preserve correct checks; do not erase disclosed no-manifest or local-exclusion limits |
| F01-C03 | Existing bounded negative guards: unsafe/duplicate/symlink ZIP members, CRC, compression limits | Preserve existing rejection paths; no hostile resource stress |

For every test, preserve raw fixture bytes or a deterministic recipe plus expected fixture SHA-256, actual result, classification, stdout/stderr and exit code. Pass/fail counts **without original artifacts and exact decisions** are insufficient. Any genuine legacy archive which the new contract cannot classify must remain `INCOMPLETE` with a reason and separate disposition, not be made to fit by adding a silent exclusion.

## 5. Independent requalification and dependency limits

After delivery of a candidate, a **different independent Astra High reviewer** (not the correcting developer) must authenticate the signed F01 preregistration, verify the exact historical source preimage and immutable CP3 baseline, seal and hash its own expectation register before inspecting the new candidate, then perform bounded adversarial and legitimate-archive tests. The reviewer must assess actual corrected code behavior and return raw results; *static reasoning alone is not equivalent to a dynamic pass*, though static review remains useful.

The review must verify the one-component patch surface, no immutable mutations, complete/partial-manifest semantics, documented class exclusions, all mandatory negative and compatibility outcomes, and fresh complete release readback. Rerun **only G0 custody checks causally affected by the verifier change**, plus narrowly essential dependency checks. Reuse old scoped G0-A/G0-B/G0-C evidence *only after checking its exact input hashes, unchanged assumptions, host identity and dependency map*. No transitive reuse of host-enforcement claims or mathematical qualifications.

The independent outcome must distinguish **(a)** corrected F01 behavior, **(b)** the surviving documentary G0-A/B subclaims, and **(c)** unresolved historical `NOT_OBSERVED`/`INCOMPLETE` items. A corrected F01 is **not automatically `MOD_G0_PASS_SCOPE_LIMITED`**; independent review and the owner's final scoped gate decision remain necessary. `MOD_G0_FAIL` from QC-C stays in the historical ledger forever.

Permitted *new review disposition*: `MOD_G0_F01_PASS_SCOPE_LIMITED`, `MOD_G0_F01_FAIL`, `MOD_G0_F01_INCOMPLETE`, `MOD_G0_F01_BLOCKED`, or `MOD_G0_F01_EVIDENCE_LOSS_STOP`. If and only if the independent evidence justifies it, the reviewer may also recommend a **new** overall MOD-G0 assessment under the signed charter, with exact residual limitations; it cannot issue `GATE_SEALED_SCOPE_LIMITED` itself.

## 6. New bounded execution slices and checkpoint-first preservation

**Proposed maximum:** One additional **30-minute wall-time developer slice** for G0-F01 corrective work and **one separately authorised 30-minute wall-time independent reviewer slice** for G0-F01 QC. These are **new prospective allocations**, not leftover G0 time; they become effective only after the signed preregistration and the owner's *distinct explicit authorisation of each role*. No carryover, implied renewal or third slice. Stop early on insufficient storage, input evidence, time or host support. State actual measured elapsed time and any inability to enforce the administrative wall clock.

**Before substantive work**, each agent must establish a genuinely durable, separately retrievable artifact location and independently verify an initial checkpoint readback. If durability cannot be demonstrated, stop with `BLOCKED` before extensive work. All checkpoints are append-only; SHA-256, byte count, every member hash, predecessor pointer, UTC timestamp and fresh retrieval receipt are mandatory.

- **Developer D-CP0:** authenticated signed authority, historical source hash, immutable evidence index, frozen expected fixtures and exact scope/diff baseline. Independently store and read back before correction.
- **Developer D-CP1:** corrected candidate/diff, coverage contract, fixtures and raw test attempts including failures. Store and read back before final packaging.
- **Developer D-CP2:** release candidate, clean verification logs, file/manifests, dependency map and exact recovery handoff; fresh external readback required. Early stop produces an explicit partial checkpoint instead.
- **Independent Q-CP0:** authenticated candidate and immutable references; reviewer-sealed independent oracle/expectations and baseline inventory **before viewing corrected source**; durable fresh readback first.
- **Independent Q-CP1:** independent fixture execution, negative/compatibility evidence, scoped dependency verification and raw failures; durable fresh readback.
- **Independent Q-CP2:** final complete coverage matrix, immutable review report, separately verified release, chronology and recovery handoff; durable fresh readback. Stop within authorised time even if incomplete.

On credit or session interruption: preserve what actually completed, provide the most recent verified checkpoint exact identity and recovery procedure, never silently reconstruct raw records or reuse old execution identifiers, and request separate authorisation for any additional slice. If essential evidence is irretrievably missing, use `...EVIDENCE_LOSS_STOP` rather than fabricating continuity.

## 7. Freeze/admission, signing and prohibitions

Before any signing, the owner will review this exact text, resolve all open policy questions (including classes that legitimately lack manifests), calculate the exact text SHA-256 and Git blob, and verify the clean worktree plus **local and fresh remote** head equality to the stated direct parent. The proposed signed preregistration is **exactly one new documentation file and no other change**. Sign personally with the stated fingerprint; distinguish ownertrusted local verification from GitHub attestations. If the parent has moved, STOP; do not rebase/reset/force push to satisfy this document. Do not publish a review draft as if already authoritative.

**Hard exclusions throughout F01:** no replacement of historical G0-A/B or QC-C archives; no alteration of signed source or previous results; no Git commit/push by agents; no generic mathematical or scientific tests, no registered V5B surrogate/Hebrew/glyph/image/ribbon work; no actual CPU/RSS stress, no amendment to the original 30/45 CPU-second or 4 GiB limits; no MOD-G1–G6 work; no implementation freeze; no `RUN_01`; no automatic gate seal or next-gate authority.

**Closeout:** preserve the original QC-C FAIL and all positive/negative/incomplete evidence. After independent F01 requalification, inspect the newly frozen evidence and any remaining G0 dependencies. The human owner alone may then consider a **separately signed, scope-limited MOD-G0 seal**. Only after that distinct decision may a separately authorised MOD-G1 charter be considered.

---

**Signing decision needed:** The owner must approve these exact signing-candidate bytes, including the new direct-parent identity, the contract for manifest-required versus genuinely outer-only historical archive classes, the two proposed 30-minute allocations, and the one-file signing path. Until the owner's approval, signature, publication and a separate execution instruction: **UNSIGNED / UNAUTHORISED / NO EXECUTION**.
