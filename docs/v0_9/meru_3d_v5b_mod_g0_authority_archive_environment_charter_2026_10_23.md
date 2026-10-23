# Meru v0.9 / 3D-V5B — MOD-G0 Authority, Archival Recovery and Environment-Capability Qualification Charter

**Document date:** 2026-10-23
**Status:** PROSPECTIVE, UNSIGNED REVIEW CANDIDATE — NOT AN EXECUTION AUTHORISATION
**Charter identifier:** `MERU_V5B_MOD_G0_CHARTER_2026_10_23`, proposed version `G0-C0`
**Repository / branch:** `salahealer9/meru-geometry-audit` / `hebrew-projection-capacity-v0.9`
**Proposed one-file path:** `docs/v0_9/meru_3d_v5b_mod_g0_authority_archive_environment_charter_2026_10_23.md`
**Required exact direct parent:** `5de3a2bac49e4cacbe49512f5674ead036c16091`
**Expected human GPG signer:** `D4EC014EEFCC90E619D2AA59A91239ABCF512130`

## 0. Authority, purpose and prospective status

The parent is the **signed and published prospective modular qualification amendment**. It sets a governance framework but authorises no gate execution by itself. This document supplies the narrower charter for **MOD-G0**; until its exact content is approved, signed in a separate one-file additive commit, published and then expressly authorised by the human, **no MOD-G0 agent execution is permitted**. A signature on this charter does not automatically authorise an agent to run G0, begin MOD-G1, qualify any implementation, or perform `RUN_01`.

**One independently decidable G0 question:** Can an independent custodian authenticate and freshly recover the immutable V5B protocol/source/review baseline, account for missing historical evidence without reconstruction, and produce a reproducible, conservative, read-only host-capability classification *before* allowing dependent tests?

This is an **archival/provenance and capability-reporting** qualification, not a statement that the certificate engine, symbolic algorithms, CPU/memory containment or any scientific geometry are correct. Label this gate `MOD-G0`, never the separate registered V5B scientific G0 object.

### Immutable signed Git anchors

| Historical artifact | Commit / immutable Git blob | Required relationship |
|---|---|---|
| V5B scientific protocol | `006b12e6800b29e41dc8e1854acdee528b822e22` / `2fab1e49b99473de4de2517e29225f4193c5b9ac` | Parent `4f94a0920213a0de6a26b90d663ba5e17a634c98` |
| DEV-R1 corrective protocol | `54bdb1f6baab62fbf7be8b6057d2761a3286053d` / `bed31bcd4be6c2418cfa8ad024be7e747d57b385` | Parent V5B protocol |
| Historical DEV-R1 / QC-R2 evidence closeout | `e1da15b18ecaa4da2a0d15eed3d2864f1d6ea11b` / `179111872b3c4dca29736261be1453f0394b22ab` | Parent DEV-R1 corrective protocol |
| Modular qualification amendment | `5de3a2bac49e4cacbe49512f5674ead036c16091` / `5625041fcd0c90621a22667cb18e8cd2c49670bb` | Parent historical closeout; G0 charter's required parent |

Verify the actual Git tree, exact one-file additions and required parenthood, all relevant historical signed predecessors, and all available local-GPG and GitHub attestation evidence. Distinguish (i) the cryptographic validity of a signature under a key imported from published provenance, (ii) GitHub `verified=true` attestation, and (iii) **the owner's separately observed local `TRUST_ULTIMATE`**. Never claim the third from the first two. A newly imported key with `TRUST_UNDEFINED` is not a substitute for human ownertrust.

### Immutable ZIP and fixture anchors

| Evidence object | Expected SHA-256 | Size when registered |
|---|---|---:|
| Original generic DEV0 (`MERU_3D_V5B_DEV_GENERIC_2026-10-22.zip`) | `2f40663b8a1c5c83e7cfaee73c24ae458cd081d4db697e1d6f56f848954ecddc` | 572,992 B |
| Original independent DEV0 negative QC (`MERU_V5B_INDEPENDENT_QC_PREFLIGHT_INCOMPLETE_2026-10-23.zip`) | `b074d5abc905e98452db5957478ba7995df40c2236f0f7bfc174e866fb24e985` | 5,767,215 B |
| Corrected developer DEV-R1 (`MERU_3D_V5B_DEV_R1_GENERIC_CORRECTIONS_2026-10-23.zip`) | `2748cf262adda4d8fca8930056ebfe68be61cd33b20cbd8f7ddbb8f10a8912b6` | 32,785,685 B |
| Independent Astra QC-R2 (`MERU_V5B_DEV_R1_QC_PREFLIGHT_R2_INCOMPLETE_2026-10-23.zip`) | `64b48bd1b68f2a0ca9fa29247ec353009af521dcfc0b6e9b58820560070a4ef9` | 198,501,765 B |

The DEV-R1 79-fixture register is `19c0eb9e125c8849aeed21fb1a43f560412429fe06f17d345bde591a43be53bb`. DEV-R1 CP_R1_5 is `24893cf0196925c30eca312d581842153477f07422c2d529b0dc0d9f3f703405`. The independent QC-R2 delivery receipt identifies the Library object `libfile_66e62ee5ed7481918c33c620aa6579e8` and reports four embedded reviewer checkpoints. These Library pointers are **retrieval aids**, not substitutes for byte-hash authentication. The reviewer must discover and record actual available source locations without inventing paths or replacing lost evidence.

**Unchanged historical conclusions:** DEV0 `V5B_DEV_GENERIC_QC_PREFLIGHT_INCOMPLETE`; DEV-R1 developer `DEV_R1_GENERIC_CORRECTIONS_READY_FOR_QC_R2` (developer only); Astra R2 `V5B_DEV_R1_QC_PREFLIGHT_R2_INCOMPLETE` (29 scoped PASS / 8 FAIL / 5 INCOMPLETE). Retain `R2-F01`–`R2-F06` and all negative test outcomes. `R2-F05` unlogged exploratory runs are permanently missing: record, never fabricate or replay under the old run identifiers.

## 1. Exactly permitted operations (read-only on scientific baselines)

**Allowed:** read-only remote Git metadata and Git objects; independent `git cat-file`, `git verify-commit`, GPG diagnostics in a disposable keyring, `sha256sum`, streaming ZIP member and checksum verification, safe readback of immutable archive copies, inspecting frozen manifests, read-only Python/OS dependency inventories, Linux `/proc` and namespace capability inspection, and running a **new G0-only** preflight and negative test harness in an isolated scratch directory. The G0 scripts, logs and reports are *new reviewer artifacts*, not edits to scientific files or the developer implementation.

**Prohibited:** commit/push/rebase/reset/tag on the scientific branch; changing signed protocols, code or historical ZIPs; installing/upgrading dependencies in the production checkout or changing host policy to make it pass; executing DEV0, DEV-R1 or Astra science/regression/test harnesses; importing or executing arbitrary Python from the ZIPs; evaluating any of the six registered spherical surrogates, any Hebrew/glyph/image/ribbon-shadow target, `RUN_01`, implementation freeze, independent mathematical G1–G6 tests, or altering pre-existing QC dispositions. Archives are untrusted file inputs: validate archive paths, duplicates, symlinks, decompression limits and structure *before* extraction; avoid executing content simply because it is present.

Do not call a local isolated provenance check a trusted-owner GPG check. Where the human's ultimate key-trust confirmation is required, identify it as a separately supplied observation; record the inability to reproduce it if unavailable.

## 2. Execution slices and acceptance controls

**One gate, three small slices; no simultaneous mathematical or resource-enforcement qualification.** Complete the slices sequentially, with bounded checkpoints and explicit stop conditions. A reviewer may stop earlier with `INCOMPLETE` or `BLOCKED`; never extend to other gates automatically.

### G0-A — Immutable provenance and recovery

1. Confirm clean branch and signed Git ancestry in a detached/read-only clone; attest exact commit/blob/tree identities, required parent links and one-file amendments. If a mutable remote has advanced, retain its state as a separate fact; do not substitute it for pinned commits.
2. Read back each of the four archival ZIPs from a durable location; verify exact length, SHA-256, safe members and every advertised internal checksum, with a cross-reference to the historical delivery receipts. Audit developer CP_R1_0–5 and independent reviewer CP0–CP3 predecessor/readback evidence to the extent recorded and accessible; report which checkpoint bytes were actually revalidated.
3. Build an append-only, machine-readable evidence registry: immutable object ID, size, hash, archive hierarchy, retrieval method/location, verification outcome/time, historical disposition, source/assumption dependencies and any genuine evidence loss. Include a `SUPPORTED_SCOPED_EVIDENCE` inventory for previous independent mathematical findings, **never a new mathematical certification**.

### G0-B — Host capabilities, not host suitability by assertion

1. Record UTC clock and timezone, OS distribution/kernel/build, architecture, container/VM characteristics, Python implementation/version/executable, environment/pip lockfiles and package versions (`python-flint`, FLINT/Arb, SymPy, mpmath, pytest), plus how available packages relate to the pinned developer and reviewer toolchains. Missing/mismatched packages mean **not qualified for those dependent tests**, not a mandate to install or silently substitute.
2. Inspect **read-only** `/proc` mount visibility, `/proc/<pid>/task/<tid>/children` access when permitted, NSpid mapping, PID namespace/user namespace relationships, access to memory cgroups and controllers, process-tree enumeration requirements, available kernel timing/accounting facilities and permissions for safe supervisors. Do not create a nested namespace or execute hostile resource stalls for G0; record a distinct capability result for each planned future G5 probe.
3. Emit conservative capability decisions `SUPPORTED_FOR_<named_claim>` (only with actually observed prerequisites) or `UNSUPPORTED`/`NOT_OBSERVED`, plus reason/evidence and test-host identity. Distinguish a supported *capability for attempting a test* from **proven enforcement**. A fail-closed refusal on this host is not evidence that hard CPU/RSS enforcement works on a compatible host. Allow a later new host to be independently checked and versioned without rewriting this record.

### G0-C — Independent QC and preservation

1. An independent checker, not the G0-A/B inventory author, seals expected outputs/negative fixtures *before* inspecting the G0 generator implementation, then independently verifies archive identities, fail-closed decisions and registry cross-links. No reuse of the author's verifier as the only QC oracle.
2. Publish a matrix of each required G0 check as `PASS_SCOPE_LIMITED`, `FAIL`, `INCOMPLETE` or `BLOCKED`; preserve uncertainty. Use `EVIDENCE_LOSS_STOP` for essential unrecoverable inputs. Negative fixtures and all failures survive unmodified.
3. Create an external, complete G0 evidence ZIP with scripts, fixed expectations, host receipts, coverage matrix, logs/stdout/stderr/exit codes, manifests, event chronology, checkpoint readbacks, dependency map and durable retrieval metadata. Do not needlessly duplicate the 198.5 MB historical QC ZIP if its original durable location and full-byte retrieval are independently proven and reproducible. Freshly download the **G0 evidence ZIP** and independently verify its complete contents before claiming the G0 reviewer outcome.

## 3. Predeclared independent hostile families (G0 only)

Before G0-A implementation inspection, freeze/hash a small fixture register with expected outcomes. At minimum: a changed outer ZIP byte; a changed internal member with stale manifest; a recomputed internal manifest under the wrong registered outer hash; an incorrect Git parent/blobs; a valid GPG signature under the wrong key; GitHub `verified=true` with no local ownertrust observation; a missing checkpoint predecessor; duplicate/unsafe ZIP paths and symlinks; changed dependency versions; an absent procfs children interface; and a missing memory controller. **No simulation result may be confused with an observed property of the real runtime.** An independent reviewer may add labeled exploratory adversaries and retain them as such.

## 4. Acceptance and evidence status

**G0-A archival/provenance PASS scope** requires full, fresh authentication of mandatory baseline archives and signed objects, proper detection of all hostile corruptions, truthful trust distinctions, checkpoint-accounting clarity and recoverable evidence registry. If a mandatory object is absent, report `BLOCKED` or `EVIDENCE_LOSS_STOP` as appropriate, not an invented pass. The historical missing exploratory logs are a disclosed limitation; they do not become available by requiring G0.

**G0-B host-capability-reporting PASS scope** requires a reproducible, conservative inventory that correctly says `UNSUPPORTED` on a host missing the required capabilities. The existence of an actually supported G5 execution host **is not** required to seal the narrow G0 archival-and-reporting claim; no positive runtime-enforcement claim is included in G0's seal. A future G5 execution must independently confirm an appropriately supported host under its own charter.

**G0-C independent review PASS scope** requires an independently authored/checking oracle, pre-sealed hostile expectations, complete coverage matrix, verified fresh readback, provenance of all tested inputs, and no unresolved critical baseline-integrity failure. A documentary `PASS_SCOPE_LIMITED` does not itself create a seal.

Permitted overall outcome: `MOD_G0_PASS_SCOPE_LIMITED`, `MOD_G0_FAIL`, `MOD_G0_INCOMPLETE`, `MOD_G0_BLOCKED`, or `MOD_G0_EVIDENCE_LOSS_STOP`, with separate G0-A/B/C subclaim statuses. Only after independent QC and a **separate human-signed gate-seal record** may exact scoped claims receive `GATE_SEALED_SCOPE_LIMITED`. No automatic inherited qualification for MOD-G1 or any other gate; no implementation freeze or `RUN_01`.

## 5. Resources, checkpoints and interruption policy

This is a metadata and archival-checking task. **No expensive mathematical loops or hostile CPU/RSS stress.** Pre-register a maximum of **three 30-minute wall-time work slices**, with a mandatory stop and durable checkpoint at each boundary; any further slices require separate human authorisation. Use streaming hashes, inspect ZIPs without high-memory expansion, and record any inability to enforce/check those administrative time bounds honestly. These logistics **do not modify the original signed 30/45 CPU-second limits, 4 GiB RSS stop, 6,000 CPU-second registered scientific budget or two-hour science watchdog**.

Create `MOD_G0_CP0` before analysis, `MOD_G0_CP1` after G0-A, `MOD_G0_CP2` after G0-B, and a final `MOD_G0_CPF` after QC/packaging; record any early-stop checkpoint instead. Preserve exact checkpoint predecessor hashes and full manifests. The **first and final checkpoints must be retrieved afresh and verified byte-for-byte** from durable storage; all other checkpoints must say exactly whether a fresh readback occurred. Prefer pre-existing Library/archive locations instead of overwriting Project storage. If credits or host support run out, prioritise preserving logs, negative fixtures, partial evidence and a precise resume handoff; declare `INCOMPLETE`, not a convenient PASS. Missing essential evidence triggers `EVIDENCE_LOSS_STOP` under the applicable signed rules.

## 6. Gate ownership and downstream use

A **read-only evidence custodian** may carry out G0-A/B without modifying developer source. A **separate independent QC reviewer** assesses G0-C. Both preserve their original outputs and identities. The owner alone may sign a gate-seal record after inspecting complete independent evidence. This G0 charter cannot be treated as a signing request for a seal, and cannot be used to appoint the same agent as author and independent checker.

Downstream may cite a signed G0 seal only for the stated immutable Git/archive identities, provenance and accurately observed environment/toolchain facts. It may **not** infer certificate mathematical soundness, schema safety, CPU/memory enforcement, or qualification of a different host. If baseline objects, retrieval procedures, source dependencies, trust assertions or runtime assumptions change, record an impact analysis. Suspend affected qualification until explicit re-review, while preserving the original seal and the full historical negative QC intact.

## 7. Human signing and execution-admission guard

**Prospective signing is documentary only.** After human approval of *these exact file bytes*, verify that both local and freshly fetched remote `hebrew-projection-capacity-v0.9` point exactly to `5de3a2bac49e4cacbe49512f5674ead036c16091`. Require a clean worktree, exact content SHA-256, and exactly one additive file at the proposed path. Verify the prior signature in the owner's trusted keyring separately from public GitHub attestations. Do not rebase or reset to force parentage.

The owner may then sign an exact one-file commit with `D4EC014EEFCC90E619D2AA59A91239ABCF512130`, verify Git parent, blob, tree, signature and one-file diff, and separately push normally. Keep GitHub signature attestation and local trusted-key validation distinct. **If the parent/branch has changed, stop and review.** No Git push, agent execution or scientific test is authorised by this review draft.

**After the signed charter is published:** request a new, explicit human instruction authorising only G0-A/B custody work, subject to the execution bounds and source identities above, with a separate later G0-C independent QC assignment. Do not interpret signing the charter as that execution approval.

---

**Closing statement:** G0 qualifies **what evidence is authentic, recoverable and suitable to depend on**, plus what a specified host demonstrably supports or refuses. It does **not** qualify the mathematical engine, the resource supervisor, the registered six surrogates or any claim about Tenen's unrecovered construction. Historical negative evidence remains immutable; one bounded, separately independently reviewed claim at a time.
