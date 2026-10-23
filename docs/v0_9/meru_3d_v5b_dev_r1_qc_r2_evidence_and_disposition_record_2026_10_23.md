# Meru 3D-V5B — DEV-R1 / independent QC-PREFLIGHT R2 historical evidence and disposition record

**Record date:** 2026-10-23  
**Record kind:** Historical evidence closeout; one-file additive documentation candidate.  
**Repository:** `salahealer9/meru-geometry-audit`  
**Scientific branch:** `hebrew-projection-capacity-v0.9`  
**Expected direct parent for a prospective signed evidence-record commit:** `54bdb1f6baab62fbf7be8b6057d2761a3286053d` (re-check branch HEAD and clean worktree at signing).  
**Historical QC-R2 disposition:** `V5B_DEV_R1_QC_PREFLIGHT_R2_INCOMPLETE`.  
**Implementation qualification:** **NOT QUALIFIED**.  
**Authorisations conveyed by this record:** **NONE**: no code correction, no implementation freeze, no `RUN_01`, no registered-surrogate evaluation, no Hebrew or image experiment.

## 1. Purpose and precedence

This file records the conclusion of the DEV-R1 corrective developer phase and the separate Astra High independent QC-PREFLIGHT R2 as historical evidence. It closes the *documentation of those completed reviews*, **not** the unresolved certification obligations. It does not alter, supersede, relax, reinterpret or retroactively amend either signed protocol; it is **not** a preregistration, corrective amendment, developer release, implementation freeze or scientific run authorisation.

The following remain authoritative in their original scope:

| Authority | Exact identity | Disposition / role |
|---|---|---|
| Signed V5B scientific protocol | Commit `006b12e6800b29e41dc8e1854acdee528b822e22`; blob `2fab1e49b99473de4de2517e29225f4193c5b9ac`; parent `4f94a0920213a0de6a26b90d663ba5e17a634c98` | Registered scientific requirements and limits, unchanged |
| Signed DEV-R1 corrective protocol | Commit `54bdb1f6baab62fbf7be8b6057d2761a3286053d`; blob `bed31bcd4be6c2418cfa8ad024be7e747d57b385`; direct parent V5B commit | Prospective A01–A07 corrective-development obligations, unchanged |
| DEV0 original independent QC | Archive and finding record listed in §2 | `V5B_DEV_GENERIC_QC_PREFLIGHT_INCOMPLETE`, permanently retained |
| DEV-R1 corrected developer delivery | Archive listed in §2 | `DEV_R1_GENERIC_CORRECTIONS_READY_FOR_QC_R2` **developer-side only**; never a QC pass |
| Astra High independent QC-PREFLIGHT R2 | Archive listed in §2 | **`V5B_DEV_R1_QC_PREFLIGHT_R2_INCOMPLETE`**; controlling evaluation of corrected DEV-R1 at this review gate |

Expected pinned signer fingerprint: `D4EC014EEFCC90E619D2AA59A91239ABCF512130`. The reviewer reported verification of six linked commit signatures and relevant Git blobs, with `VALIDSIG` against that fingerprint. GitHub valid-signature attestation, local cryptographic signature verification using an imported public key, and the human owner's `TRUST_ULTIMATE` are distinct assertions; the reviewer did **not** reproduce human ultimate ownertrust. A later human signing operation must separately confirm the trusted key and branch parent.

## 2. Immutable evidence inventory

**Do not replace, recalculate in place, or silently republish these artifacts with the same identities.** Hashes identify *bytes*, not correctness of every mathematical claim inside those bytes.

| Artifact | Bytes | SHA-256 | Record / retention |
|---|---:|---|---|
| Original DEV0 generic developer ZIP, `MERU_3D_V5B_DEV_GENERIC_2026-10-22.zip` | 572,992 | `2f40663b8a1c5c83e7cfaee73c24ae458cd081d4db697e1d6f56f848954ecddc` | Retained inside QC-R2 `intake/EVIDENCE/` |
| Original Astra DEV0 negative QC ZIP, `MERU_V5B_INDEPENDENT_QC_PREFLIGHT_INCOMPLETE_2026-10-23.zip` | 5,767,215 | `b074d5abc905e98452db5957478ba7995df40c2236f0f7bfc174e866fb24e985` | Retained inside QC-R2 `intake/EVIDENCE/` |
| Corrected developer DEV-R1 ZIP, `MERU_3D_V5B_DEV_R1_GENERIC_CORRECTIONS_2026-10-23.zip` | 32,785,685 | `2748cf262adda4d8fca8930056ebfe68be61cd33b20cbd8f7ddbb8f10a8912b6` | Retained inside QC-R2 `intake/EVIDENCE/`; separately delivered in project history |
| Independent Astra QC-R2 final ZIP, `MERU_V5B_DEV_R1_QC_PREFLIGHT_R2_INCOMPLETE_2026-10-23.zip` | **198,501,765** | **`64b48bd1b68f2a0ca9fa29247ec353009af521dcfc0b6e9b58820560070a4ef9`** | Personal Library: `/MERU_V5B_DEV_R1_QC_PREFLIGHT_R2_INCOMPLETE_2026-10-23.zip`, identified in external delivery receipt |

The external `QC_R2_FINAL_DELIVERY_RECEIPT.json` reports the final archive as `VERIFIED_DURABLE`, with 185 ZIP members, 184 payload files checked and four embedded checkpoints verified; recorded personal Library file identity `libfile_66e62ee5ed7481918c33c620aa6579e8`. That Library ID and location are retrieval aids; the SHA-256 above is the immutable byte identity. Retain the separate receipt without embedding or retrospectively altering the final ZIP.

The QC-R2 archive contains the independent final report, 42-row checklist in CSV/JSON, finding register, execution coverage, independent proofs/oracles, original and revised reviewer scripts, attack ledgers, logs, reproducibility notes, protocol copies, original source archives and CP0–CP3 checkpoint ZIPs. Its `CHECKSUM_MANIFEST.json` covers the other 184 members. Independent intake for this documentary record recomputed the whole-ZIP SHA-256 above and checked the 42-row count/status distribution; this documentary intake **does not rerun QC mathematics**.

The DEV-R1 hostile-fixture register remained pinned to 79 fixtures, SHA-256 `19c0eb9e125c8849aeed21fb1a43f560412429fe06f17d345bde591a43be53bb`. The final DEV-R1 checkpoint CP_R1_5 has SHA-256 `24893cf0196925c30eca312d581842153477f07422c2d529b0dc0d9f3f703405`. The six-checkpoint developer chain and four-checkpoint independent reviewer chain are separate histories; neither substitutes for the other.

## 3. Chronological dispositions

1. **DEV0 generic implementation** was supplied as development evidence, with original developer tests passing 131/131 on its host. Independent Astra QC-PREFLIGHT found the original implementation **INCOMPLETE** (historical checklist 25 PASS and 10 FAIL out of 35, with findings A01–A07). This verdict remains intact; the original developer suite's green result was never independent certification.
2. **DEV-R1 corrective development**, under its own signed protocol and with the original developer, implemented remedies for A01–A07. Its final package reported 131/131 original tests on host and PID-namespace setups, 97/97 developer hostile tests, 10/10 generic ledgers accepted by its separate developer checker, and 14/14 hostile ledgers rejected. Its self-limited status was `DEV_R1_GENERIC_CORRECTIONS_READY_FOR_QC_R2`, **not** `PASS`.
3. **Astra High QC-PREFLIGHT R2**, independent of the developer, sealed its expectations before inspecting DEV-R1, checked provenance and archived evidence, and performed its own mathematics, replay and adversarial tests. Its controlling result is **`V5B_DEV_R1_QC_PREFLIGHT_R2_INCOMPLETE`**. It made no developer corrections, implementation freeze, Git commit/push, `RUN_01` or registered surrogate evaluation.

## 4. Complete independent QC-R2 checklist disposition

The signed-review scope used **35 historical P/Q checklist items plus 7 corrective A01–A07 items**, producing 42 rows in `QC_R2_CHECKLIST.csv` and `QC_R2_CHECKLIST.json`:

| Scoped outcome | Rows | Meaning |
|---|---:|---|
| `PASS` | **29** | Evidence supports only the stated item-specific bounded scope |
| `FAIL` | **8** | Mandatory criterion not met or demonstrated contrary to requirement |
| `INCOMPLETE` | **5** | Required test/evidence unavailable or not completed |
| **Overall** | **42** | **`V5B_DEV_R1_QC_PREFLIGHT_R2_INCOMPLETE`**; no global PASS |

Non-PASS row identifiers from the retained matrix:

- **FAIL:** `P12`, `P18`, `Q5`, `Q9`, `Q10`, `A02`, `A03`, `A04`.
- **INCOMPLETE:** `P19`, `P20`, `P22`, `A06`, `A07`.

These 13 non-PASS rows **overlap in their underlying causes**; they are not 13 independent implementation defects. All 29 individual PASS rows remain individually scoped evidence and are **not automatically sealed modular gates**.

### 4.1 Independent positive evidence (bounded)

The independent reviewer derived and tested relevant camera-frame, oriented-geometry, antipodal-rank, reversal/reanchoring, interval inversion and partition-count properties with an independent oracle. Its second replay processed **all 10 retained generic ledgers**, including **82,108 view events, 149,741 speed-cell inclusion checks, 111 inverse histories and 179 certified cells**. It independently checked intervals, split priorities, comparisons, source geometry and orientation-sensitive proof claims. **No genuine retained certified cell was independently invalidated.**

Additional bounded attacks demonstrated corrected rejection of same-branch and transitive contradictions, false piecewise-linear certificates and certain forged geometric claims. The historical near-radical witness was independently classified NONZERO. Those are meaningful improvements over DEV0; they do **not** establish complete universal certificate, execution-accounting or resource-enforcement soundness.

### 4.2 Finding-by-finding retained negative and unresolved evidence

| Independent finding | Evidentiary status | Supported outcome and boundary |
|---|---|---|
| `R2-F01` — unsigned CPU-accounting tolerance | **CONFIRMED** | Developer validators accepted resealed records of **30.125 s/view** and **45.125 s/pair**, exceeding the signed at-most **30 s** and **45 s** limits by using an unsigned 0.25 s allowance. Retained real stress records also contained charged view totals **30.008925 s** and **30.001904 s** above 30 s; these workers were pre-empted and yielded **no** certificates. Therefore over-budget record acceptance is demonstrated, not generation of a forged genuine archived certificate. |
| `R2-F02` — forged/missing execution evidence | **CONFIRMED** | Production validator accepted a fully resealed ledger containing a `NaN` CPU string and another with a missing pair-execution list. A valid hash chain cannot supply missing process provenance or validate finite nonnegative accounting. The same newly forged inputs were **not** dynamically re-tested against the developer standalone checker after mandatory runtime STOP. |
| `R2-F03` — unsuccessful history loss | **SOURCE-CONFIRMED** | Static code paths in `engine.py` discard partial noncompleted pair trails, retaining a count rather than full attempt history. Complete successful-ledger replay therefore does not prove failure-history retention; the newly found path was not dynamically exercised after the runtime STOP. |
| `R2-F04` — containment / strict resource qualification | **INCOMPLETE** | Reviewer host lacked required procfs children files; DEV-R1 correctly refused the host under fail-closed preflight. No bypass or substitute worker was used. Retained developer RSS peaks **4,202,796 KiB** and **4,206,008 KiB** exceeded the **4,194,304 KiB (4 GiB)** threshold by **8,492 KiB** and **11,704 KiB** respectively before recorded kills; polling/detection is not proof of never-exceed or pre-emptive enforcement. Actual new resource probes remain unexecuted on a compatible host. |
| `R2-F05` — historical raw development coverage | **CONFIRMED DISCLOSED GAP** | Developer disclosed unlogged smoke/trial/pytest iterations. Their exact missing intermediate logs cannot be reconstructed retrospectively and must remain a permanent qualification of the chronology. Existing preserved evidential logs remain usable within their scope. |
| `R2-F06` — symbolic-parser safety | **UNRESOLVED STATIC CONCERN** | `eval` with restricted builtins and a symbol namespace does not itself prove an AST-level allowlist for hostile Python expression syntax. **No exploit was demonstrated**. Parser input acceptance and fail-closed treatment require a distinct bounded security qualification. |

**Do not collapse different evidence statuses into one label.** `R2-F01`/`F02` demonstrate hostile-ledger validator acceptance; `F03` is static/source-confirmed; `F04` includes a real unsupported host and unqualified pre-emption; `F05` is irrecoverable historical incompleteness; `F06` remains an unexploited static concern.

### 4.3 Independent reviewer limitations and stop

The reviewer operated with Python **3.12.14** on Linux **6.18.55**, whereas the developer used Python **3.13.16** on Linux **6.18.44**; these are documented differences. Its unmodified 131-test reproduction produced **122 PASS, 5 containment-related FAIL and 4 reviewer-basetemp setup ERROR**, not 131/131. The new 97-test reproduction was interrupted on the host's fail-closed containment condition, with no completed 97-test count claimed. The original reviewer replay01 was inconclusive because of reviewer interval-enclosure reconstruction; reviewer-only replay02 corrected the enclosure method, with both versions, diffs and logs retained. No developer code was changed by the reviewer.

Remaining hostile replay, dependent-radical/exact-zero proof challenges, adversarial parser cases and actual CPU/RSS containment stress were recorded as not executed after the mandatory STOP. `A06` and `A07` remain INCOMPLETE in the checklist despite bounded positive mathematical examples and observed fail-closed preflight behaviour.

## 5. Scope and scientific interpretation

The reviewed object is **generic continuous ordered-path projection certification infrastructure**. This phase did **not** evaluate the six preregistered V5B spherical surrogate curves, generate a registered `RUN_01`, test Hebrew glyph targets, inspect source images or establish Tenen's unrecovered FIRST HAND toroidal/ribbon algebraic construction. Generic synthetic certificates are not historical Meru construction evidence. No figure, astronomical, source-reconstruction or class-count claim follows from this closeout.

The unsigned resource tolerance is **not** accepted by this record as an amendment to either signed protocol. The memory measurements must be judged under the precise original wording (`4 GiB RSS; if exceeded stop and mark incomplete`) and the DEV-R1 corrective requirement for pre-emptive enforcement; this record neither asserts an unsupported absolute continuous-memory guarantee nor silently permits an overshoot. Any interpretive change requires a separate prospective signed amendment and must not retroactively convert historical tests into passes.

## 6. Evidence preservation and future modular transition

The historical phases and both negative QC outcomes are closed as **immutable recorded events**. Their unresolved obligations remain open. The preservation rules are:

1. Preserve exact original archives, reviewer attempts, failures, incomplete probes, original report, both checklist representations, logs, proof scripts and checkpoint chains. Do not delete or silently revise negative evidence.
2. Keep the 198.5 MB QC-R2 ZIP in durable Library/archive storage. Only this text record should be added to the signed Git history; **do not commit the large ZIP, source code or replay-generated payloads merely to document the closeout**.
3. Preserve source/protocol/fixture/checkpoint hashes and record changes in a new artifact and a new prospective authorisation. Historic missing logs remain identified as missing; do not fabricate them or make old runs appear complete.
4. The proposed **V5B Modular Qualification and Evidence-Sealing Amendment** is a **separate future document**, to be signed **after** this historical record, with a fresh direct-parent identity. It may establish bounded gates, frozen dependencies, independent acceptance criteria, signed seals and mandatory requalification on changes, but **cannot retrospectively upgrade** R2 scoped PASS rows, relax existing scientific ceilings or authorise `RUN_01`.
5. A gate seal must identify its certified claim, exact code and environment/dependency hashes, counterexample corpus, full independently reproducible evidence, assumptions, exclusions and downstream dependency/invalidation conditions. A sealed positive proof is not valid under later code changes until its relevant dependencies are checked or requalified.

**Future work is not authorised by this evidence record.** In particular, no DEV-R2 corrections or G0–G6 execution may begin solely because this record was signed. Any work must follow the applicable signed protocols and a distinct prospective human-approved scope. Independent QC remains separate from implementation development.

## 7. Record admission and signing guard

This is a **review candidate** until the human author approves its exact bytes and performs a separate GPG-signed commit. To admit it as a one-file historical closeout:

- Confirm repository and branch `hebrew-projection-capacity-v0.9`; **do not** assume remote HEAD has remained unchanged since preparation. If HEAD differs from `54bdb1f6baab62fbf7be8b6057d2761a3286053d`, stop and reconcile prospective parentage before signing; do not silently rebase or overwrite.
- Require a clean worktree before adding exactly this one new Markdown file at `docs/v0_9/meru_3d_v5b_dev_r1_qc_r2_evidence_and_disposition_record_2026_10_23.md`. Record the local SHA-256 and Git blob identity of the reviewed file, and `git diff --check`.
- Stage **only** the one new file, verify `git diff --cached --name-status` shows one `A` record, and examine the complete staged content. Use the owner's existing GPG signing setup and expected fingerprint; never create or import replacement signing keys merely to make a check pass.
- Check the new commit's actual signer identity, `git verify-commit`, direct-parent hash, one-file change and remote state. A push, if separately chosen by the human after verification, is not automatically authorised by this draft.
- Label the commit explicitly as a **historical negative-QC evidence closeout**: not scientific qualification, not implementation freeze and not a new preregistration. Do not edit historical signed protocols or previous report bytes.

**Admission condition:** the only change is this documentary record; its contents exactly match the human-approved draft, and the human-signed Git identity is verified. The subsequent modular amendment must be a distinct, future signed commit with this evidence-closeout commit as its direct parent if this sequence is adopted.

---

**Final historical disposition:** `V5B_DEV_R1_QC_PREFLIGHT_R2_INCOMPLETE`. **No implementation freeze. No RUN_01. No registered surrogates or target experiments.**
