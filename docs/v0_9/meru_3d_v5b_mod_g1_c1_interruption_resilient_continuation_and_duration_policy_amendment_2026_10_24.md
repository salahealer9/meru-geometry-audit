# Meru v0.9 / 3D-V5B — MOD-G1-C1 Interruption-Resilient Continuation and Administrative Duration Policy Amendment

**Date:** 24 October 2026  
**Instrument:** `MERU_V5B_MOD_G1_C1_RESUMABLE_CONTINUATION_2026_10_24`  
**Status before signature:** OWNER REVIEW / SIGNING CANDIDATE; NO EXECUTION AUTHORITY FROM SIGNATURE ALONE  
**Repository / branch:** `salahealer9/meru-geometry-audit` / `hebrew-projection-capacity-v0.9`  
**Exact proposed additive file:** `docs/v0_9/meru_3d_v5b_mod_g1_c1_interruption_resilient_continuation_and_duration_policy_amendment_2026_10_24.md`  
**Required direct parent:** signed MOD-G1 charter `6a87178fc61dd01e410c862eef869065484416cd`  
**Expected human signing fingerprint:** `D4EC014EEFCC90E619D2AA59A91239ABCF512130`

## 1. Purpose, precedence and limits of amendment

This **prospective, additive amendment** removes *self-imposed administrative duration limits* from the MOD-G1 developer and independent-review workflows, permits documented recovery and continuation after credit limits, workspace resets or session interruptions, and prevents a paused session from exhausting authority merely because calendar time passes. It records the developer's already completed but interrupted attempt as immutable history. It **does not backdate authority**, reclassify missing evidence, certify software, or change any scientific/resource-control obligation.

The original signed G1 charter, commit `6a87178fc61dd01e410c862eef869065484416cd` (Git blob `2a3bd837172a604bab4fbcb4a96d8900d4a6ea96`; text SHA-256 `b5016111c1050359e0e9c9b213e36502b5f69047ed2b2eaa4c16635b9b351494`), is the required **direct parent**. Its signed parent is the narrow G0 evidence seal `4bbfe8bb5302aa33f2a44ad3220e05ed6d69fdb0`. The governing modular framework is commit `5de3a2bac49e4cacbe49512f5674ead036c16091`.

**Precise replacement:** the G1 charter's Section 5 ceiling of one **90-minute wall-clock Astra developer slice** and one **60-minute wall-clock ChatGPT reviewer slice**, including a deadline-driven stop, is superseded *for G1 only*. Work no longer expires because of total wall time, active-work elapsed time, credit waiting, workspace absence, or pauses between interactions. No substitute arbitrary clock limit, maximum session count or calendar expiration is introduced. Insofar as the older modular framework calls for task-specific time/compute boundaries, for this G1 case the bounded work scope, frozen cases, input sizes, no-stress exclusions and scientific resource constraints constitute the work/compute boundary; **no developer or reviewer deadline is required**. All other signed G1 sections remain operative, including stop for essential missing evidence or unsafe/unsupported operations.

For **future unsigned modular-gate charters**, the prospective default is **no artificial developer/reviewer wall-clock or active-time caps**, unless the owner expressly requests and signs a different duration rule for that specific future scope. Such charters must specify finite scientific/test scope, resource safety and checkpoint/recovery obligations instead. This default does not override already signed charters for other gates or pre-authorise any future work.

## 2. Frozen interrupted G1 developer attempt — preservation, not regrading

The original 90-minute G1 developer authority was exhausted under its **then-operative** text. The developer correctly stopped when the platform reset the scratch workspace and the wall-clock deadline had expired; this amendment neither retrospectively extends that elapsed slice nor calls the original result READY, PASS or SEALED. The preserved developer disposition is **`MOD_G1_DEVELOPER_INCOMPLETE`**.

The original recovery archive is:

- `MERU_MOD_G1_DEVELOPER_INCOMPLETE_RECOVERY_2026-10-24.zip`: **183,569,676 bytes**, SHA-256 **`2de984493fd5f0e446a2fbc9a828eee8ec4b114fa50e4a4e3d4c1e3e78d988f1`**; independent fresh retrieval was possible from the owner's Library. Its 38 manifest-listed payload members all matched their sizes and SHA-256 values.
- `MERU_MOD_G1_D-CP0_2026-10-24.zip`: **51,880,151 bytes**, SHA-256 **`f608bc2515823a4917993295b311fc4e1f34c993f6b2b199d0b0b7b3dbc8177b`**; original Library identifier `libfile_75646cd1f1b4819180650af4c07fa3a7`; **204/204** manifest payload members verified.
- `MERU_MOD_G1_D-CP1_2026-10-24.zip`: **80,207,126 bytes**, SHA-256 **`ec3c1c06bfb6115c9dfff69c745c949a853e2e48163c29721d93419cd75a8acc`**; original Library identifier `libfile_4d40f1ec33648191a73260d861bbac0e`; **455/455** manifest payload members verified.
- The recovery package separately identified by owner Library ID `libfile_10327066d0d08191adb6b35a7cd0c05c`; external `MOD_G1_RECOVERY_FRESH_READBACK_RECEIPT.json` identifies its fresh readback. Exact original checkpoint bytes were embedded and authenticated. Partial `.openai-download-*` transport fragments also preserved in that package **are not original checkpoint substitutes**.

D-CP0 preserves the immutable source baseline, independently retrievable authority data, *pre-edit* sealed symbolic grammar and fixed test expectations. D-CP1 preserves the G1 derivative candidate, exact source diffs, original preimages, development scope, raw first-pass logs/fixtures/results and **163 distinct developer first-pass cases matching frozen expectations** (118 negative, 39 positive, six diagnostic). These are *developer observations only*, not an independent qualification.

The 104 public-boundary integration cases, one tiny-validator compatibility test and two historical standalone-CLI rejection observations after D-CP1 survive **only as transcript-derived secondary reports**; their original scripts and raw stdout/stderr/result files were not recovered. Do not count them as directly reproducible first-pass evidence, invent their raw files or silently reuse their attempt IDs. The frozen **second pass, final source and call-path audit, and D-CP2 were not completed**. No G1 gate PASS, reviewer QC, implementation freeze or scientific execution has occurred.

Historical `R2-F02` (confirmed forged-record acceptance) and `R2-F06` (unexploited static `eval` concern) remain the G1 targets. Other old failures remain within their separate gates. The limited G0 seal and original `MOD_G0_FAIL` retain their exact original scope and historical identities.

## 3. Prospective resumption authorisation model — no repeated expiration

**Signing this amendment is documentary only.** After publication, the owner must separately and explicitly authorise **Astra to continue the remaining MOD-G1 developer work from authenticated D-CP1**. That authorisation shall be *task-scoped and resumable*, **not time-scoped**. Once given, a credit cutoff, context switch, transient system interruption or lost scratch workspace **pauses**, rather than consumes, the authorisation. The same authorised G1 task may be resumed as often as needed from the latest verified durable checkpoint, **without a new time-extension amendment or additional owner authorisation merely because an interruption occurred**.

An interruption does not allow unobserved work to be treated as finished. At every recovery, Astra must verify signed authority and the actual surviving checkpoint/input bytes; reconcile attempt IDs, hashes and the last durable event; use a clean new scratch workspace; and clearly separate unchanged historical output from newly executed work. If a session can no longer access the required original files, safely execute bounded tests, or persist/checkpoint material, it must stop at an honest BLOCKED/INCOMPLETE state rather than fabricate continuity. Explicit owner revocation or a substantive scope change also stops the current authorisation. **No automatic progression to G2–G6 or science.**

Astra's *remaining authorised G1 scope*, when separately admitted, is limited to: recover D-CP1 candidate and original records; restore or independently reimplement missing benign test drivers without representing them as originals; repeat the missing post-CP1 public-boundary/standalone tests under **new** attempt IDs and preserve their actual raw results; perform the originally planned unchanged frozen second pass; complete the source, grammar, parser-route and integration audits; and package a new final **D-CP2 with external fresh readback** and exact complete derivative/diff. Negative results, unsuccessful attempts and any new substantive code changes must be retained, not repaired silently or reclassified. Preserve the original historical 163 observations unchanged.

The original G1 candidate source/compatibility requirements, exact finite grammar, parser security refusal, historical forgeries, all G1-N01–N11/G1-P01–P04 classes and accepted-authentic constraints remain unaltered. New adverse findings may require a versioned corrective candidate within G1's existing authorized source scope, with preserved old evidence; any *material expansion* requires an additional prospective decision, not an inference from this administrative amendment.

Astra must keep D-CP0 and D-CP1 immutable; append a **recovery/continuation checkpoint** after authentication if needed, then D-CP2 on completion. Every material attempt, even unsuccessful ones, is logged with unique IDs, real stdout/stderr/exit code, source hashes, UTC timestamps and checkpoint reference. Checkpoint packages require complete checksum manifests, exact predecessor pointers and a separately persistent upload plus fresh readback. Avoid duplicating the 183.6 MB evidence in every checkpoint when the durable pinned originals can be independently retrieved. Never call a truncated transport fragment complete custody.

## 4. Reviewer role and independent qualification (duration limit removed)

Following Astra's developer-ready handoff, the owner will **separately authorise ChatGPT (GPT-6) independent MOD-G1 review**, now **without the prior 60-minute administrative ceiling**. That task authorisation is likewise resumable across credit/session/workspace interruptions, tied to the actual registered G1 version, and does not expire through the passage of time. Reviewer and developer roles remain separate: **Astra develops; ChatGPT independently reviews; the human signs any justified gate seal.**

Before seeing new G1 candidate changes or detailed developer tests, ChatGPT independently freezes/hash-seals reviewer expectations and its oracle in Q-CP0, disclosing any unavoidable prior exposure to G1 findings. Then it independently tests the *actual* candidate against immutable historic hostile records, parser grammar/entry points and authentic positives; preserves raw outcomes and failed cases; and stores Q-CP1 and Q-CP2 with externally verified fresh readbacks. Review continues only within the approved G1 scope; no reviewer code modifications to Astra's implementation, no unearned PASS and no invisible source patches. An incomplete review remains incomplete until the evidence is actually finished.

Neither an Astra developer delivery nor a ChatGPT reviewer finding by itself seals G1. A later **human-signed, exact-scope gate seal** is a separate decision. Missing essential raw inputs remain NOT_OBSERVED/INCOMPLETE and cannot be promoted through a time-policy amendment.

## 5. Scientific limits and hard exclusions — unchanged

**Nothing in this amendment relaxes the scientific or safety ceilings** under the original signed V5B protocol, including the **30 CPU-seconds/view**, **45 CPU-seconds/unordered pair**, **6,000 CPU-second registered total**, **4 GiB RSS stop**, **two-hour scientific-run watchdog**, and the literal precision/subdivision/inversion rules. The later G2 and G5 gates retain responsibility for exact accounting and actual host enforcement. These signed limits concern the scientific instrument and its certification claims; they are **not** artificial administrative agent-work deadlines.

G1 continues to permit only **bounded synthetic/generic inputs**, finite predeclared test cohorts and resource-safe parser/schema validation. No large hostile CPU/memory stress, no unbounded fuzzing, no package modifications to production environments, no modification of historical source archives/signed protocols/negative findings, no arbitrary Python `eval` restoration, no moving unsupported shape categories into the accepted grammar to make tests pass. Developer/reviewer must describe real environment constraints and platform/tool limits rather than claim control over them. The agent cannot guarantee absence of external product usage caps; when platform credits run out, the task pauses and later resumes from durable bytes.

**NO AGENT GIT COMMIT OR PUSH. NO SCIENTIFIC SURROGATE/HEBREW/GLYPH/IMAGE/RIBBON WORK. NO G2–G6, IMPLEMENTATION FREEZE OR `RUN_01`. NO AUTOMATIC GATE SEAL.**

## 6. Signing and resulting state

Owner first verifies signed ancestry, branch `hebrew-projection-capacity-v0.9`, clean worktree, freshly checked remote HEAD exactly `6a87178fc61dd01e410c862eef869065484416cd`, and approved file SHA-256. Sign exactly **one new documentation file** at the prescribed path under key fingerprint `D4EC014EEFCC90E619D2AA59A91239ABCF512130`. Verify exact one-file addition, signature, direct parent and ordinary non-force push. If the branch has advanced, STOP and inspect rather than reset, rebase or force. Do not edit or delete any old commits, results or evidence objects.

**After valid signature and publication:** `MOD_G1_C1_RESUMABLE_CONTINUATION_POLICY_SIGNED; G1 DEVELOPER STILL INCOMPLETE; CONTINUATION AWAITS DISTINCT OWNER AUTHORITY`. No claim that recovered transcript-only evidence has been upgraded and no claim of passing independent review. Once separately authorised, the task-scoped continuation does **not** expire because of platform interruptions or elapsed calendar time.
