# Meru v0.9 / 3D-V5B — MOD-G0-F01-R01 Prospective Reviewer Substitution and Two-Role Workflow Amendment

**Date:** 23 October 2026  
**Identifier:** `MERU_V5B_MOD_G0_F01_R01_REVIEWER_SUBSTITUTION_2026_10_23`  
**Status at preparation:** HUMAN REVIEW / SIGNING CANDIDATE — NO EXECUTION AUTHORISATION  
**Repository:** `salahealer9/meru-geometry-audit`  
**Branch:** `hebrew-projection-capacity-v0.9`  
**Proposed new file:** `docs/v0_9/meru_3d_v5b_mod_g0_f01_r01_reviewer_substitution_2026_10_23.md`  
**Required direct parent:** signed F01 preregistration commit `a72a9515830aed6ab9b162b55cd421a51d953224` (verify local HEAD and fresh remote branch HEAD before signing; never reset/rebase/force-push to obtain this parent).  
**Expected owner signing fingerprint:** `D4EC014EEFCC90E619D2AA59A91239ABCF512130`.

## 1. Narrow purpose and precedence

This is a **prospective, one-file amendment** to the *reviewer assignment and related information-barrier procedure only* in the signed MOD-G0-F01 protocol, not a new scientific protocol, correction to historical evidence, or retrospective declaration of success. The signed F01 authority is `a72a9515830aed6ab9b162b55cd421a51d953224`, whose direct parent is the signed MOD-G0-C failure closeout `8d8eb31c7f3f4f6e9b1a603bbfa8e87b6d88c52f`. The historical MOD-G0-C disposition remains **`MOD_G0_FAIL`**. The original signed G0 charter is `e8fb37660b78065537be06f561ad7208cd0fb0f6`.

In case of conflict, this R01 amendment governs **only** the identity and operational independence of the F01 reviewer, the prospective expectation-sealing procedure after disclosed preliminary exposure, and the future developer/reviewer role allocation. Every other exact restriction, manifest contract, hostile fixture, acceptance requirement, disposition, negative finding, budget and scientific exclusion in the signed F01 and ancestor protocols survives unchanged. Neither signing R01 nor any prior developer delivery authorises execution.

## 2. Explicit roles and historical boundary

- **Owner / scientific authority:** the human repository owner approves scope, signs documentary authority with the pinned key, separately authorises each execution and decides whether any subsequent gate seal is justified.
- **Developer for all future work:** **Astra**. Astra may code, test and deliver artifacts only under distinct owner authorisation. Astra must **not** certify its own modifications as independent reviewer. There shall be no further Claude development or additional agent-to-agent handoff.
- **Independent technical reviewer:** **ChatGPT (GPT-6)**, a separate reviewer from the developer, working with independently authored tests/oracles and direct artifact verification. The reviewer does not modify the developer's candidate, silently repair tests, issue a human GPG signature, or sign the gate seal. Limits of available host isolation, artifact access and tool environment must be reported rather than concealed.

**One-time F01 transition:** Claude's completed D-CP0/D-CP1/D-CP2 and the already delivered F01 developer candidate remain **immutable historical developer inputs**; they do not need to be rewritten or reproduced by Astra. ChatGPT may independently review that existing candidate under the new role assignment after the owner separately authorises the reviewer slice. If any substantive correction becomes necessary, **Astra**, not Claude, must prepare the future derivative under a new prospective scope/authorisation; ChatGPT cannot independently qualify a patch it wrote. Nothing in this amendment retroactively describes Claude as Astra or alters Claude's frozen 48/50 overall and 38/40 mandatory register result.

The two-role model is a declared **future policy preference**, not a blanket retrospective revision of MOD-G1–G6 or any other existing signed instrument. Each future signed gate charter must explicitly adopt compatible roles before execution.

## 3. Inputs preserved and limits already known

The existing F01 candidate is `MERU_V5B_MOD_G0_F01_DEVELOPER_RELEASE_2026-10-23.zip`, **426,586 bytes**, SHA-256 `872d589b3b9e66388b00634f8ae1a5ab3ebc2db110c408db68bdfeacdcb05cc3`; candidate `g0a_verify_f01.py` has SHA-256 `b3c9647e31588af91aa8abdc701f8d5b6d07c827da8f6d04c10e1273978316c1`. The original historical verifier preimage has SHA-256 `0d9b1ce871de441520726fc91d09608e3a286d4ee665e8293421a51479eede65`. The signed F01 text SHA-256 is `eb8fda3cc7b6995dc59db13c7ba60933193f0f9c529a4295a04924ac908975da`.

The controlling prior QC-C artifact is `MERU_MOD_G0_C_QC-C-CP3_FINAL_2026-10-23.zip`, **14,529,680 bytes**, SHA-256 `ecaf6b14545fc432c33e6d263b991441eaf015778a3173ec67a62790e589ffb2`. Developer checkpoints, separately verifiable by complete byte/hash and predecessor/readback receipts:

| Artifact | SHA-256 | Size |
|---|---|---:|
| D-CP0 | `c5eeaf3c67ec55a776fb77ee1267febb87aed2bb614d64897d5dbd66821dc416` | 108,745 bytes |
| D-CP1 | `cbad9d142a21581a27aaeb38987655244195c10420b291b985796f097c4aee4d` | 163,580 bytes |
| D-CP2 | `7d0e03f4fc3bb8172fa3dec46f07b85b98c278d759cd8bc1bb3e9192b285c9e3` | 588,276 bytes |

No positive archive-integrity finding is, by itself, a positive security-qualification decision. Missing original evidence remains `NOT_OBSERVED` / `INCOMPLETE`; the reviewer must not invent, recreate or claim access to absent historical raw archives or logs.

## 4. Prospective reviewer procedure and independence disclosure

The reviewer has **already been exposed to the developer's written summary**, developer test totals and the descriptions of the two discrepancies, and has handled the release as an archive for identification purposes. **The review cannot honestly be described as fully blind to the developer's outcome reports.** This exposure must appear in the reviewer evidence. The reviewer must not assert it had never seen the reported outcomes.

Subject to that disclosed limitation, **before opening/inspecting the corrected candidate source for substantive review, executing that candidate, or examining its detailed test implementations**, ChatGPT will independently write and content-hash a new F01 reviewer expectation/acceptance register and independently constructed oracle/fixture specification, derived principally from the *signed F01 protocol* and immutable historic finding. The owner must separately authorise the review; the sealed register and its UTC time/hash must be included in a fresh reviewer Q-CP0 package. A failure to establish this prospective boundary becomes a declared methodological limitation, not a fabricated blind review.

The reviewer must then:

1. Authenticate the signed Git ancestry/one-file scopes, recorded source blobs, original evidence, developer release and D-CP chain (distinguishing owner's demonstrated GPG trust from reviewer-imported-key trust and GitHub attestations).
2. Develop an **independent** inert hostile-test oracle, not a wrapper around developer expected outputs; exercise the corrected candidate only with bounded data and without unsafe execution of archived candidate as trusted code. Report exact environment, commands, observed results, stderr/stdout, exits and resource limitations.
3. Verify manifest-required versus legitimate `OUTER_IDENTITY_ONLY` archive classes, explicit exclusions, complete payload coverage, path/duplicate/symlink/CRC guards and all signed F01 negative and compatibility classes; preserve incomplete evaluations where original complete evidence cannot be accessed.
4. Adjudicate F01-N07a and F01-N09 according to **the literal signed acceptance obligations**, not only the stricter developer-register primary-diagnostic ordering. Rejecting the archive while recording the required causal reason may satisfy the signed behavioral requirement, but only if no separate bypass, misleading accept classification or loss of coverage is found. Preserve the frozen developer deviations exactly; do not retroactively mark 48/50 as 50/50.
5. Carry forward the original `MOD_G0_FAIL` and all historical QC-C / QC-R2 findings. Distinguish corrected-verifier qualification from an overall G0 pass or a gate seal.

Reviewer's possible F01 outcomes remain `MOD_G0_F01_PASS_SCOPE_LIMITED`, `MOD_G0_F01_FAIL`, `MOD_G0_F01_INCOMPLETE`, `MOD_G0_F01_BLOCKED`, or `MOD_G0_F01_EVIDENCE_LOSS_STOP`. The reviewer may **recommend** a later human-signed scoped MOD-G0 decision but cannot pronounce `GATE_SEALED_SCOPE_LIMITED`.

## 5. Budget, checkpoint durability and no automatic continuation

The signed F01 protocol's **single prospective 30-minute independent reviewer wall-time allocation** is **reassigned from the formerly named Astra independent-review role to ChatGPT**; **no additional reviewer time or automatic extension is created**. The original completed Claude developer slice is historical and not reopened. A reviewer stopwatch/intake timestamp and explicit slice end are required; lack of reliable wall-time enforcement must be disclosed. No future Astra developer slice is authorised by this reviewer-role amendment.

A reviewer execution requires the owner's **separate explicit authorisation** after R01 is signed and published. Before substantive execution the reviewer must establish a genuinely persistent, separately retrievable checkpoint destination, verify Q-CP0 fresh readback, then preserve Q-CP1 and Q-CP2 with independent readback (or stop early with a durable partial checkpoint, raw negatives and honest disposition). Capture exact bytes, SHA-256, every member's digest, predecessor pointers, UTC timestamps and original stdout/stderr/exit codes. If storage, evidence, time, host isolation or access is insufficient, stop explicitly; never assume a model session or sandbox alone provides external durable archival custody.

No independent claim may exceed performed tests, present records or available environment. A reviewer report and newly frozen evidence must be submitted to the owner for a separate gate decision. No scientific experiment or automatic move to the next gate follows.

## 6. Immutable exclusions and signature

**NO COMMIT/PUSH BY AGENTS. NO EDITING HISTORICAL INPUTS. NO ALTERATION TO THE V5B SCIENTIFIC PROTOCOL OR G0 ORIGINAL CHARTER. NO GENERIC GEOMETRY/MATHEMATICAL/SURROGATE/HEBREW/GLYPH/IMAGE/RIBBON EXPERIMENTS. NO CPU/RSS STRESS. NO MOD-G1–G6. NO IMPLEMENTATION FREEZE. NO `RUN_01`. NO AUTOMATIC GATE SEAL.**

The owner may add **exactly this one new amendment file**, verify SHA-256, correct signed direct-parent lineage, clean baseline and a fresh remote branch head, and personally create a GPG-signed one-file commit. Any unanticipated Git ancestry change, malformed input identity or substantive contract discrepancy is a STOP for review, never a justification for rewriting history. No agent may commit or push on the owner's behalf.

**Signing R01 is documentary authority only.** Independent ChatGPT F01 reviewer execution begins only after the owner's distinct explicit instruction. Astra receives no new execution authority from R01. The final human G0 decision is reserved.
