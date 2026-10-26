# Meru v0.9 / 3D-V5B — MOD-G2 Signed-Limit CPU Accounting and Provenance-Binding Qualification Charter

**Draft date:** 26 October 2026 (UTC)  
**Instrument:** `MERU_3D_V5B_MOD_G2_SIGNED_LIMIT_CPU_ACCOUNTING_AND_PROVENANCE_2026_10_26`  
**Document state:** **DRAFT — FOR HUMAN REVIEW; UNSIGNED; NO EXECUTION AUTHORISED**  
**Repository / branch:** `salahealer9/meru-geometry-audit` / `hebrew-projection-capacity-v0.9`  
**Proposed one-file path:** `docs/v0_9/meru_3d_v5b_mod_g2_exact_cpu_accounting_and_provenance_charter_2026_10_26.md`  
**Required direct parent at signing, subject to fresh verification:** `a50a13d5dc9bc0bcae98c8283322cb9f97f8aa11` (human-sealed G1 exact-scope PASS)  
**Expected human GPG fingerprint:** `D4EC014EEFCC90E619D2AA59A91239ABCF512130`

## 0. Exact objective and non-negotiable scope

**Qualification question:** Does the exact, version-pinned generic V5B CPU-charge record and verification boundary **reject all over-ceiling, ambiguously measured, omitted, duplicated or unbound cumulative CPU charges**, including attempts across precisions and logical branches, using precise unrounded comparisons against the *unchanged signed limits*? Does it accept fully valid, source-anchored generic charge histories without trusting a self-declared root hash or invented worker event?

The MOD-G2 task covers **signed-limit accounting and provenance binding of *recorded* CPU charges**. It does **not** qualify the actual operating-system watchdog, process-tree sampling/pre-emption, wall/RSS hard-stop enforcement (MOD-G5); complete preservation/replay of all unfinished scientific histories (MOD-G3); proof-theoretic/mathematical certificate correctness (MOD-G4); or integrated production runtime (MOD-G6). Do not conflate a ledger saying a worker was killed with evidence the kernel enforced a CPU limit. Do not claim a run-specific scientific result. No new actual scientific `RUN_01` or source/target-specific experiment is authorised.

**Target current technical reviewer disposition:** `MOD_G2_PASS_SCOPE_LIMITED` for the complete *original signed G2 accounting/provenance scope* if, and only if, all mandatory classes below are supported. `FAIL`, `INCOMPLETE`, `BLOCKED` or `EVIDENCE_LOSS_STOP` must be reported honestly otherwise. A scope-limited PASS is not permission to call G3–G6 passed. Developer alone cannot issue any G2 PASS; owner alone signs any subsequent separate gate seal.

## 1. Authoritative signed instruments and input pins

Read and authenticate complete signed Git documents, exact blob identities, lineage and all original resource constraints. The signed Git documents, **not** later paraphrases, control:

| Authority | Signed commit | Role |
|---|---|---|
| V5B scientific preregistration | `006b12e6800b29e41dc8e1854acdee528b822e22` | Fixed resource ceilings and scientific exclusions |
| DEV-R1 corrective preregistration | `54bdb1f6baab62fbf7be8b6057d2761a3286053d` | Historical A03 CPU/worker requirements |
| DEV-R1 / QC-R2 negative disposition | `e1da15b18ecaa4da2a0d15eed3d2864f1d6ea11b` | Immutable `R2-F01` and companion findings |
| Modular qualification framework | `5de3a2bac49e4cacbe49512f5674ead036c16091` | **MOD-G2 definition** and impact/invalidation rules |
| G0 full-foundation human seal | `af31614167c28f29a94b1078d9149461ea75b511` | Qualified G0 prerequisite, pinned custody and host reporting only |
| Original G1 charter | `6a87178fc61dd01e410c862eef869065484416cd` | Versioned record schema and secure parser boundary |
| G1 C1 continuation amendment | `3911c9f6beba6146f71f772435144fb20863b3ed` | No artificial G1 admin deadlines; prospective future-gate default |
| G1 exact-scope human seal | `a50a13d5dc9bc0bcae98c8283322cb9f97f8aa11` | **Proposed direct parent**; G1 schema/parser PASS *only* |

**Original historical negative archive:** `MERU_V5B_DEV_R1_QC_PREFLIGHT_R2_INCOMPLETE_2026-10-23.zip`, **198,501,765 bytes**, SHA-256 `64b48bd1b68f2a0ca9fa29247ec353009af521dcfc0b6e9b58820560070a4ef9`. Its `QC_R2_FINAL_REPORT.md` (10,407 B; SHA-256 `aa83be144274b936d2bb16d63ae5a6226a9744e84a9c96f531b845d7c05fe58b`) and `QC_R2_FINDINGS.json` (1,736 B; SHA-256 `b6046c655825443e58a58fa9126a7dc4d7b7e867223240979cf6a0fee6e9e5b7`) give the original review. The original DEV-R1 developer archive is nested at `intake/EVIDENCE/MERU_3D_V5B_DEV_R1_GENERIC_CORRECTIONS_2026-10-23.zip` (32,785,685 B, SHA-256 `2748cf262adda4d8fca8930056ebfe68be61cd33b20cbd8f7ddbb8f10a8912b6`). All source paths below are relative to that nested ZIP's top-level versioned directory.

**Original exact source preimages (never edit their archived bytes):**

- `source_DEV_R1/src/v5b_generic/validate.py`, SHA-256 `8fb2483baf8a74d8c80f21ab2cd4e72c3112c39b69b1f4ef8f94cf7cb619026f`, 34,937 bytes. In original `validate_ledger`, at line **608** `u > SIGNED_CEILINGS["view_cpu_s"] + 0.25` and at line **627** `pc > SIGNED_CEILINGS["pair_cpu_s"] + 0.25` improperly expand the threshold.
- `r1/replay_checker/v5b_r1_replay_check.py`, SHA-256 `b30c4675ba58f8cada491f52d5b6a07961d331d3347a895aaa1cb5d6a83cb1d2`, 51,677 bytes. Original `CEIL["kill_latency"] = 0.25` is added at lines **1055** and **1069** to cumulative view/pair allowances. A monitoring/killing latency description does *not* license higher recorded CPU ceilings.
- Original signed source/ledger `engine.py`, original G1 version-pinned derived validation/schema/parser files and their evidence are authoritative *dependencies* that must be authenticated and cross-mapped, not silently overwritten. Use the exact G1 D-CP2 archive SHA-256 `4539f5539b26422fdd5617be58e459aa164ced0e2b9c8e8d4c961013d1f3a26d`, G1 Q-CP2 `dfe72d1aeff0b1f3fd56bdffe9c341927747eb9ebe662f102e89abce94458db9`, plus the G1 human seal for their version pins.

**Historic adversarial byte fixtures** in original QC-R2 ZIP:

| Original file | SHA-256 | Immutable required old outcome |
|---|---|---|
| `results/forged_view_cpu_30_125.json` | `ed71861cafb932dde36bbfa9727763692fa2f6fc14c0720311f46521910f07fc` | Previously accepted despite 30.125 > 30 |
| `results/forged_pair_cpu_45_125.json` | `2c939d5df299445947e7930eaa38f8dd3ae65b173fcf3d3b7706c2c41ccbb1ed` | Previously accepted despite 45.125 > 45 |
| `results/RETAINED_RESOURCE_AUDIT.json` | `4558a9771d4aad6b14a11d9528fe6cc0bad654a4e1ee7630582764f805a87ddb` | Historical charge totals: views 30.008925 / 30.001904 seconds; both pre-empted/no certificates |

**Historical truth:** `R2-F01` establishes *forged ledger acceptance*. It does not show a truly over-budget production worker successfully certifying a scientific result. In the retained actual stress records, view overruns were marked as non-certifying outcomes; they still did **not** satisfy a `≤30` ceiling. Retained pair totals were below 45. Original `R2-F02` schema/forgery and `R2-F06` parser concerns are addressed by sealed G1 *within its admitted scope*, not silently imported as a G2 mathematical replay PASS; `R2-F03` belongs to G3, `R2-F04` to G5, historical evidence-loss `R2-F05` remains recorded.

## 2. Unchanged ceiling and charge semantics

The signed V5B ceilings are exactly:

- **View:** CPU charged to one camera view across *all* its allowed 128-bit and 256-bit attempts **≤ 30 seconds**.
- **Unordered pair:** CPU charged to a pair across *all four registered logical branches* and both allowed precision attempts **≤ 45 seconds**.
- **Registered full scientific execution:** **≤ 6,000 CPU seconds** including orchestration and independent result assembly, and separate **2-hour wall-clock watchdog**. G2 may validate a complete and properly typed *recorded* total when present, but **does not certify the live G5 watchdog** or invent orchestration charges if missing.
- **4 GiB RSS** remains a registered stop condition, outside G2's hard-enforcement proof.
- Precision and method constraints remain unchanged: at most one 128-bit and one 256-bit attempt as allowed by the controlling protocol, 4,096 directed subdivisions, 128 inversion bisections; G2 does not change scientific algorithms or prove their mathematical properties.

For certification-oriented G2 charge *representation and comparison*, define one versioned canonical unit (CPU seconds or exact integral subdivisions of a second, with lossless conversion) and accept **only finite, nonnegative, exactly representable** charge quantities. Use exact integer/rational/decimal arithmetic for addition and ordering—**no binary-float comparison, rounding, truncation, clamping, implicit default zero, post-hoc epsilon or `+0.25` latency allowance**. Decimal strings from authenticated existing records may be admitted under a *strict, explicitly versioned grammar* consistent with the sealed G1 schema. `NaN`, `Infinity`, booleans, negative/unsupported numbers and maltyped/missing fields are refusals. At equality with the registered limit, a valid record may pass *subject to other obligations*. Any strictly positive excess, however small, is over budget. Monotonic exact charges must not decrease when an attempt, branch, worker or orchestration event is appended.

The verifier must map each charge to a stable view ID or canonical unordered pair ID, specific precision, attempt/event, worker/executor identity, parent/child/partial/termination lifecycle and exact source hash where the registered record has those fields. Reject duplicate, missing or reused charge IDs; contradictory provenance; uncharged attempted work; duplicate charging (unless a documented non-overlapping semantic class explicitly requires it); non-monotonic resets; inconsistent sums; conflicting event/status/certificate claims; fabricated timestamps presented as CPU proof; forged mutable budgets; and resealed hashes masking structural inconsistencies. A signed-limit exceedance cannot be made compliant by changing the task budget, naming `PREEMPTED`, dropping a worker, or making the root hash self-consistent.

**Sampling/OS truth boundary:** A G2 validator proves consistency and limits for *declared, bound records*; it cannot infer honest kernel charge measurement from user-created strings alone. Explicitly label any claims about measured real CPU as `NOT_OBSERVED` unless supported by independent runtime receipts. The G5 host controller must later bind authoritative process accounting and stop behavior to these same semantic fields; a G2 seal alone does not certify that binding.

## 3. Frozen negative/positive test classes and required dispositions

Astra must freeze a machine-readable D-CP0 fixture/expected-class register **before modifying candidate code**; ChatGPT independently freezes a separate Q-CP0 register *before examining newly delivered candidate changes*, with any prior exposure disclosed. Required classes are fixed now:

| ID | Required condition | Exact expected result |
|---|---|---|
| G2-N01 | Original `forged_view_cpu_30_125.json`, resealed original bytes | Refuse CPU limit compliance, no positive certification |
| G2-N02 | Original `forged_pair_cpu_45_125.json`, resealed original bytes | Refuse CPU limit compliance, no positive certification |
| G2-N03 | Same view split across 128/256 attempts, each under 30 but sum over 30 | Refuse cumulative view total |
| G2-N04 | Pair split across all branches/precisions, each under 45 but sum over 45 | Refuse cumulative unordered-pair total |
| G2-N05 | Valid-looking task budget inflated over signed ceiling; root hashes resealed | Refuse; ceiling immutable |
| G2-N06 | Duplicate/omitted/reused worker and attempt IDs, omitted partial/pre-empted worker charge, orphaned event, wrong pair/view binding | Refuse positive full accounting; do not synthesize unseen charges |
| G2-N07 | Nonfinite, negative, bool, null, wrong-type, numeric overflow, malformed decimal/rational, JSON duplicate field | Refuse under precise schema; no implicit default |
| G2-N08 | Tiny strictly positive overrun: 30+ε, 45+ε, total 6000+ε, ε exact and representable | Refuse at any ε > 0 |
| G2-N09 | Truncation/rounding/float cancellation, inconsistent sum or units, multi-event reset/rollback | Refuse inconsistent/nonmonotone recorded charges |
| G2-N10 | Interrupted/killed/stale worker or failed attempt later presented as successful with certificate, without valid CPU binding | Refuse; preserve honest unresolved/over-budget status |
| G2-N11 | Forged wall timestamps/process labels treated as sufficient CPU proof | Refuse provenance/compliance claim absent bound CPU evidence |
| G2-N12 | False exact-total or accounting omission in a complete synthetic ledger, including orchestration/assembly when registered | Refuse complete total-compliance claim |
| G2-P01 | Exact valid boundary charges 30, 45, 6000 (with genuine complete identities and sums) | Accept *record accounting* at equality, not OS enforcement |
| G2-P02 | Authentic, original-hash-pinned, fully consistent generic ledgers with actual permitted attempt histories | Accept within declared G2 scope; no scientific proof inferred |
| G2-P03 | Split but in-budget 128/256 or four-branch records with monotonic exact sums | Accept; no false overcount or precision-specific bypass |
| G2-P04 | Pre-emption/abort documented honestly with exact over-budget charge and **no** certified result | Preserve and correctly classify as OVER_BUDGET/INCOMPLETE; do not falsely certify budget compliance or erase event |
| G2-P05 | Provably identical exact decimal/rational inputs with alternate approved canonical forms | Same arithmetic result and stable approved serialization |
| G2-P06 | Eligible genuine G1 strict-schema records remain valid; invalid historical G1 forged records remain refused | Preserve G1 input boundary and prevent regression |

At least one new independently resealed attack must exercise every hash-relevant negative class; original fixed historical fixtures count as originals, not newly created independent test samples. Use bounded inert synthetic records and small test magnitudes, **never** spend 30, 45 or 6,000 real CPU seconds to test comparators. A causal refusal is mandatory; do not require incidental first-error ordering unless an explicitly signed class makes it material. Critical false-positive acceptance vetoes G2 PASS; counts cannot hide it.

## 4. G1 seal preservation and implementation-change boundaries

G1 is already human-sealed **only for a specific source/record grammar**. Any G2 work touching `validate.py`, replay checker, schema, serialisation, accounting event shape or transitive dependencies shall first map exact G1 source hashes, declared exports and interfaces. Implement G2 only as a **new version-pinned derivative** in a separate scratch tree. Do not alter archive originals, signed Git worktree, final G1 D-CP2 or its seal.

- Prefer adding a **separable G2 accounting-verifier layer or clearly separated G2-owned helpers** bound to G1-validated canonical records. If legacy validators must change to remove their tolerance, preserve their exact old and new source, line-level diff, call graph and negative/positive regression mapping.
- If a G2 derivative changes *any behaviour or transitive dependency covered by the G1 seal*, perform a documented **G1 impact/invalidation decision before accepting or deploying that derivative**. The unchanged historical G1 seal remains historical truth, but the **modified derivative's G1 claim may require requalification**, `SEAL_SUSPENDED_PENDING_REQUALIFICATION` for an affected integration, or an owner-approved prospective compatibility test. Do not silently inherit the G1 seal for changed semantics.
- If a demanded G2 behaviour is incompatible with the exact G1 approved record grammar, preserve a blocking compatibility finding and obtain a human decision under the signed framework; do not relax G1 malicious-input refusals or smuggle unsupported record types into accepted syntax.

No agent source changes to the Git repository, no commit/push, no deletion of negative evidence and no unsigned protocol change. Any source patch is a separately hashed scratch derivative. The eventual G6 integrated qualification must explicitly check G1/G2 interoperability on its exact combined source snapshot.

## 5. Role separation, checkpoints and evidence custody

**Astra (developer/custodian), upon a separate owner authorisation:** authenticate authorities and original ZIP bytes; create durable **D-CP0** containing authenticated preimages, *pre-edit* frozen fixture/expectation register, exact unit/canonical grammar decision, dependency-impact plan and source boundaries; verify external fresh readback before editing. Build bounded derivative(s); run original negatives, new frozen and genuine positives, schema compatibility, exact arithmetic metamorphic/property tests, and independent toolchain checks; retain **all** source hashes, raw commands/stdout/stderr/exits, failed attempts, new test IDs and rejected cases. Save D-CP1 after first candidate and D-CP2 as final self-contained audited release, both externally uploaded and independently freshly retrieved. Provide complete input/record dependency inventory and source-map/diff; publish a developer-ready or honest non-PASS status, **not a G2 qualification verdict**.

**ChatGPT (independent reviewer), only after a further separate owner authorisation:** authenticate signed charter, baselines, fixed historical fixtures and the completed developer release. Freeze the independent **Q-CP0** expectation/fixture register *before* seeing the new candidate changes/details; disclose any previous exposure and distinguish independently built tests from developer outputs. Independently implement an exact decimal/rational accounting oracle, check canonical source/provenance/worker binding and signed group limits, execute originals and fresh inert forgeries against both admitted production and standalone G2 entry points, verify G1 boundary compatibility and challenge source/serialization drift. Preserve independent raw evidence in Q-CP1 and final Q-CP2 with hashes, manifests, predecessor pointers, checked archive safety and separate external fresh readbacks. Do not modify Astra's code or approve it based solely on developer test scores.

No artificial developer/reviewer administrative wall time, active-work minute cap, expiration or maximum session count. A credit cutoff, chat interruption or scratch-workspace loss **pauses** an existing authorised task. Resume only from the latest authenticated durable checkpoint; any post-checkpoint unpreserved work is transcript-only and must not be counted as original raw evidence. Use real, bounded test cases and retain actual failures, not reconstructed successes. Essential missing inputs or inability to preserve evidence yields a candid stop state. Do not promise background execution.

## 6. Full G2 PASS, human seal and scientific exclusions

**Admission for a technical `MOD_G2_PASS_SCOPE_LIMITED`:** independently supported requirements for **every** mandatory G2-N01–N12/G2-P01–P06 class; strict limit comparisons at 30/45/6000 using exact semantics; original `R2-F01` falsification fixtures rejected by the **exact delivered G2 candidate**; full group/attempt/branch/precision monotonic charge bindings; genuine supported G1 record compatibility; all critical negative cases refused; original and new source/evidence inputs authenticated; **no unadjudicated G1 compatibility break**, source-integrity objection, missing mandatory evidence, or unsupported provenance/OS claim. All recorded limitations are expressed in the reviewer final matrix with evidence IDs and exact version fingerprints.

A complete G2 PASS is an **exact-scope accounting-verifier PASS only**: no hard kernel measurement guarantee, process kill latency, strict CPU wall/RSS containment, universal certificate proof, complete failed-work science replay, registered surrogate result, implementation freeze or `RUN_01` authority. Those require G3–G6 and later separately authorised acts. `R2-F01` historical failure remains immutable; a successful new version supersedes it only for the exact corrected pinned boundary. G1 historical seal is not rewritten or silently broadened.

After independent review and verified Q-CP2, the owner alone may consider a separate one-file signed exact-scope `MOD_G2` seal. That act is not authorised by this charter signature alone, nor does it authorise G3–G6. Preserve a `G2_dependency` registry analogous to G0/G1: signed authorities and seals, four original baseline ZIPs as required by exact G2 code lineage, original QC-R2/F01 forgeries/retained stress audit, G1 sealed source/reviewer checkpoints, Astra D-CP0/1/2, ChatGPT Q-CP0/1/2, terminal reports, hash manifests, external readback receipts, and historical negative attempts. Prefer exact original-byte references over duplicating large archives unnecessarily, but an offline external-drive collection must be independently verifiable by `sha256sum -c SHA256SUMS.txt` for each locally present required object.

## 7. Human signing guard; status after signature

This draft has **no effect** until the human owner reads/approves its exact final bytes and one-file GPG-signs it under the pinned key. Before signing: verify full text/hash, clean local tracked/untracked tree, correct branch, valid signature of the direct parent, fresh remote branch tip exactly `a50a13d5dc9bc0bcae98c8283322cb9f97f8aa11`, and one-file addition only at the proposed path. On a differing parent or evidence integrity failure **STOP** and review; do not reset, force, rebase, fabricate tests or change thresholds to get a PASS. An original scientific-run clock/CPU resource ceiling is not an administrative work-session deadline.

**After verified human signature and ordinary Git publication only:** `MOD_G2_ACCOUNTING_CHARTER_SIGNED — ASTRA/CHATGPT EXECUTION AWAITS SEPARATE OWNER AUTHORISATION`. No G2 software work, independent Q-CP0, G3–G6, scientific testing, implementation freeze, or `RUN_01` follows automatically.
