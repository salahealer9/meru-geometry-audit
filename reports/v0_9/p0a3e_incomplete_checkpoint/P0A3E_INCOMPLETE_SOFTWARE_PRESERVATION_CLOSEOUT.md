# P0A3E — Incomplete Exact-2D-QO Software Engineering: Preservation Freeze Closeout

**Project:** Meru Geometry Audit, v0.9 — target-blind Hebrew projection-capacity programme
**Prepared:** 2026-10-20
**Branch:** `hebrew-projection-capacity-v0.9`
**Pre-sign status:** `HUMAN_INCOMPLETE_SOFTWARE_PRESERVATION_FREEZE_CANDIDATE`. This document is a human-signing candidate, **not yet an authoritative signed result**.
**Decision class:** additive archival preservation of an independently reviewed but **incomplete** P0A3E software candidate; **not a positive code-only implementation freeze**, and not registered numerical certification.

## 1. Frozen authority and direct-parent requirement

The **required direct parent** for this preservation commit is the signed P0A3E **one-file protocol-only preregistration**:

`c48c7a60777200a172ae3c72f5b0402162370ec7`

- P0A3E protocol: `docs/v0_9/p0a3e_exact_2d_qo_software_hardening_and_independent_certificate_qualification_protocol.md`
- Exact P0A3E protocol Git blob: `108866549d914005c391eedea234ca27cc8604b7`
- Protocol direct parent: `59eb47f7500d57866e4935822b78a555d3bcb515`, the signed P0A3D **positive theorem-result freeze**.
- Expected human GPG fingerprint: `D4EC014EEFCC90E619D2AA59A91239ABCF512130`.

On 2026-10-20 GitHub independently reported `verified=true` for P0A3E, its exact parent and single added 198-line protocol, and this feature branch at that commit. **GitHub signature attestation is distinct from local trusted-key verification**; the human operator must verify their local clean HEAD and key before staging. Historical signed protocol files, theorem proof and QC must never be retroactively edited to change their archival pre-sign banners.

## 2. Exact immutable evidence retained in this new checkpoint

The four original evidence objects are **byte-for-byte copies**; no new changes, parsing, repair or normalization have been applied to their contents.

| Preserved file | Bytes | SHA-256 |
|---|---:|---|
| `original_P0A3E_cumulative_implementation_candidate.zip` | 968,965 | `1e73c2685bd4eb8fba89e4e8ea609e97c7b4716805e83c64af374a4265522ea8` |
| `P0A3E_independent_software_QC_report_2026-10-20.md` | 12,182 | `176bdff51bd1c3027475858e58f1adff1fb69863473553ad8911603ea7278ba2` |
| `P0A3E_independent_QC_verification_2026-10-20.json` | 3,658 | `26ba49ac62953ffe86ebedba7724016b193d7d5ef234b0254b8ad9cb08c3e21e` |
| `original_P0A3E_independent_QC_review_2026-10-20.zip` | 21,497 | `6fd796d3eb99eb78191b7a3219ad557627012871d5c20c2ee504981160da3961` |

The cumulative original ZIP contains **303 entries**, **21,362,112 uncompressed bytes**, ZIP CRC PASS, **302/302 internal SHA-256 entries** and **301/301 payload inventory records** verified in independent QC, with safe unique paths and no ZIP symlinks. The independent QC review ZIP preserves both independently run DEV transcripts/evidence, including the **failed environment-incompatible run** and the **successful compatible-interpreter run**. These original objects stay archived, **not installed as approved production source**.

The earlier P0A3D 642,047-byte candidate (`c2f99b0e78849de16c8dc8167bdf5d584d4f64ab2c8a787d6a0ed507cfa9f378`), its 20-case DEV review and positive theorem freeze remain in their **earlier signed Git checkpoint**; the P0A3E ZIP references that immutable baseline rather than reclassifying it. P0A3E source preserved three central mathematical kernels byte-identically to the P0A3D originals: production `algebra.py`, production `core.py`, and reference `arithmetic.py` in their `qo2d_exact/` namespaces.

## 3. Independent QC findings — exact restricted meaning

**Archive/provenance:** PASS for byte identity, CRC, internal manifests, versioned evidence and GitHub P0A3E signed-source ancestry. This is not proof of correctness of executable Python or independent local trusted-key verification of every historical commit in this new freeze preparation.

**DEV chronology:** original `P0A3E_DEV_01` failed at method 12 because a DEV assertion wrongly required serialized radical expressions to be identical even when algebraically equal; the source/evidence and ordinary assertion correction were retained. `P0A3E_DEV_02` passed **32/32** engineering microchecks. No registered scientific cases were involved.

**Independent reproduction is environment-qualified:**

1. Default `/opt/pyvenv/bin/python` under the QC host returned **5 passed, 1 failed at method 6**: a 256 MiB child virtual-memory ceiling was lower than the interpreter's roughly 417 MiB initial virtual address space. The child failed closed with `RESOURCE_INCOMPLETE`, *not* an exact score; the failure is not erased.
2. With unchanged candidate source, tests, declared limits and exact arithmetic, `/usr/bin/python3` completed **32/32 PASS, exit 0** under a bounded external run. This independently supports bounded DEV reproducibility **in the compatible environment only**.

**Source/QC matrix:** E1 strict public parsing **PARTIAL**; E2 exact executable predicates **DEV-SUPPORTED / UNQUALIFIED**; E3 independent certificate checker **DEV-SUPPORTED / UNQUALIFIED**; E4 external trusted code/config/checker anchor **UNQUALIFIED**; E5 worker/crash/resource **PARTIAL**; E6 generic bounded DEV/provenance **PASS**. The reference rebuilds exact arclength moments, correlation, `SO(2)` witness and *direct integrated residual* from the original ordered paths in tested cases, without directly importing production numerical helpers; it nevertheless shares Python/Fraction assumptions. The candidate's caller-provided `DEV_UNFROZEN_EXPECTATIONS` are not a human-signed or externally verified code freeze.

## 4. Final negative software disposition to preserve after human signature

After a human signs this unchanged seven-file additive preservation candidate, the permitted resulting statuses are:

- `P0A3E_INCOMPLETE_ENGINEERING_CHECKPOINT_PRESERVED`
- `P0A3E_ARCHIVE_INTEGRITY_PASS`
- `P0A3E_BOUNDED_DEV_REPRODUCIBILITY_PASS_ON_COMPATIBLE_INTERPRETER`
- `P0A3E_SOFTWARE_IMPLEMENTATION_INCOMPLETE`
- `P0A3E_EXACT_PREDICATE_UNQUALIFIED` (executable implementation)
- `P0A3E_REFERENCE_INDEPENDENCE_UNQUALIFIED` (full-domain software certification)
- `P0A3E_INPUT_FAILURE_ENVELOPE_INCOMPLETE`
- `P0A3E_RESOURCE_CRASH_ENVELOPE_INCOMPLETE`
- `P0A3E_EXTERNAL_TRUST_ANCHOR_UNQUALIFIED`
- `P0A3E_REGISTERED_VALIDATION_NOT_RUN`

**Do not assign** `P0A3E_EXACT_2D_QO_SOFTWARE_CANDIDATE_READY_FOR_REGISTERED_TARGET_FREE_VALIDATION`, any executable `GLOBAL_CERTIFIED`, `P0A4` completion or a genuine Hebrew specificity/historical projection finding. The independent QC does **not** approve a positive P0A3E code freeze. Frozen theorem status `P0A3D_EXACT_2D_QO_THEOREM_INDEPENDENTLY_VERIFIED` remains true **only for its generic abstract 2D ordered-open-path `SO(2)` domain**, and does not certify the P0A3E executable.

## 5. Scope exclusions and scientific observation barrier

No P0A0 S00–S12 replay, P0A4 registered testing, QH, G0/A/B or continuous-camera evaluation, Hebrew target/chart/glyph/font-proxy acquisition or matching, statistical candidate/null experiment, metric selection or model fitting was authorized by the P0A3E protocol or is authorized by this preservation freeze. The previous v0.8 result `NO_REPRODUCIBLE_PUBLISHED_FIRST_HAND_CONSTRUCTION_RECOVERED` stays intact; missing historical functions, physical shadow law, source rights/order and B07/B08 observation/fairness gates remain unresolved. Generic QO theorem or passing engineering checks provide no basis for Hebrew specificity.

## 6. Non-authorizing P0A3F proposal and human signing protocol

The companion `P0A3E_NEXT_P0A3F_SOFTWARE_QUALIFICATION_PLAN.md` is **only a proposed direction**, not an implementation instruction, preregistration or authority to run DEV/registered validation. A separately GPG-signed **P0A3F protocol-only** human commit anchored directly to the *actual new P0A3E preservation SHA* is required before any continuation.

Human operator shall: (1) verify clean checkout of `hebrew-projection-capacity-v0.9` with HEAD exactly the P0A3E signed protocol commit above; (2) verify expected GPG fingerprint and signed parent; (3) check delivered outer ZIP SHA-256 and CRC, seven safe additive entries and the six repo-root-relative hashes in `FREEZE_MANIFEST.sha256`; (4) stage **only** `reports/v0_9/p0a3e_incomplete_checkpoint/`, check diff and contents; (5) commit with `git commit -S`, verify exact parent, commit signature and clean tree; (6) push only the feature branch and provide full new SHA. A mismatch is a **hard stop**. Do not `reset`/overwrite unexpected worktree changes to force a preferred parent.

The original candidate and independent QC remain unchanged in the signed checkpoint. If P0A3F later repairs a blocker, it does not rewrite the archived negative P0A3E finding. No work agent is authorized to modify, commit or push the existing repository.

**Decision:** preserve incomplete-but-reproducible P0A3E engineering and independent QC, then preregister a smaller, explicitly separated software environment/trust qualification stage. No production code promotion and no registered experiment yet.
