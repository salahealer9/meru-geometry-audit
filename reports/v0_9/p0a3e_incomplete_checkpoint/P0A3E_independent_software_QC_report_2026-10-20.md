# P0A3E — Independent mathematical, software and provenance QC

**Date:** 2026-10-20. **Repository:** `salahealer9/meru-geometry-audit`, branch `hebrew-projection-capacity-v0.9`.

**Decision:** **ARCHIVE AND SIGNED-PROVENANCE PASS; BOUNDED DEV REPRODUCIBILITY PASS IN COMPATIBLE SYSTEM PYTHON; SOFTWARE QUALIFICATION INCOMPLETE.** No code-only readiness freeze, registered validation, or Meru/Hebrew experiment is approved.

## 1. What was actually examined

The original Library `P0A3E_cumulative_implementation_candidate.zip` was retrieved byte-for-byte, **968,965 bytes**, SHA-256 `1e73c2685bd4eb8fba89e4e8ea609e97c7b4716805e83c64af374a4265522ea8`. It contains **303 entries** totaling **21,362,112 uncompressed bytes**. The ZIP's CRC, unique safe relative member names and no-symlink condition passed. All **302/302** `SHA256SUMS` entries and all **301/301** payload inventory records (length and SHA-256) were checked independently. **21/21** Python files parse as AST. No PNG/JPEG/GIF/WebP or font files were found by filename/extension inventory. This establishes archive integrity, **not** program correctness or an exhaustive no-contamination forensic proof.

GitHub was independently queried. The signed P0A3E commit is `c48c7a60777200a172ae3c72f5b0402162370ec7`, one added 198-line protocol, direct parent `59eb47f7500d57866e4935822b78a555d3bcb515`; its pinned protocol blob is `108866549d914005c391eedea234ca27cc8604b7`. GitHub reports signature verification `valid`, and remote branch HEAD matched. The source lineage was already verified in the prior review; this review does not represent a new local trusted-key import/signature verification of every historical object. GitHub attestation and local `git verify-commit --raw` are distinct.

The exact original P0A3D source candidate was independently retrieved from Library: **642,047 bytes**, SHA-256 `c2f99b0e78849de16c8dc8167bdf5d584d4f64ab2c8a787d6a0ed507cfa9f378`; both source and ZIP CRC checks passed. Byte-for-byte comparison found three crucial mathematical modules **unchanged** in P0A3E:

- `src/meru_geometry/v0_9/qo2d_exact/algebra.py`
- `src/meru_geometry/v0_9/qo2d_exact/core.py`
- `reference/v0_9/qo2d_exact/arithmetic.py`

The original P0A3D theorem remains the authority; it was **not** re-proved or re-registered here. Historical P0A3D DEV attempts 01–04 survive in the signed P0A3D checkpoint, **not** newly rerun or silently represented as embedded P0A3E package payloads.

## 2. Retained P0A3E DEV chronology

The submitted artifact retains P0A3E_DEV_01: return code 1, **11 passed, one failed on test 12**; and P0A3E_DEV_02: return code 0, **32/32 passed**. Both stdout/stderr hashes match the recorded manifests and snapshots. Method 12's initial defect compared the serialized radical polynomial representations of two **semantically equal** algebraic values. The exact checker already reported equality by a zero decision. A traceable correction changed the **test assertion only**, not the production/reference numerical kernels or the frozen theorem. The original failed report, attempt-specific source content, diffs and worker artifacts were retained. Source manifest entries, lengths and hashes match the delivered sources. **No attempt is promoted to a registered scientific validation run.**

## 3. Our independent bounded DEV reproductions — important environment qualification

Using an isolated copy of the supplied source, with **no P0A0 or P0A4 tests**, the first rerun invoked `/opt/pyvenv/bin/python` with a 1 GiB outer address-space limit. It stopped at test 06: **5 passed, one failed** (`RESOURCE_INCOMPLETE` observed rather than the test's expected `NOT_EVALUABLE`). Investigation found that this host's default virtualenv Python starts with approximately **416,928 KiB** of virtual address space, already **above** the worker's frozen `RLIMIT_AS` ceiling of **268,435,456 bytes** (256 MiB). The worker consequently returned `WORKER_RUNTIME_LIMIT`, without a score or false certificate. This is an **environment-compatibility issue and fail-closed outcome**, not evidence of a mathematically false QO answer. The full failed log is preserved, not erased.

Without editing the source, expected hashes, resource policy, test source, DEV cases or arithmetic implementation, a second run used `/usr/bin/python3` (same nominal Python 3.13.5 version, with smaller process startup footprint):

```sh
cd /mnt/data/p0a3e_qc_workspace
PYTHONPATH=src:. PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 LC_ALL=C.UTF-8 \
  P0A3E_DEV_RUN=/mnt/data/p0a3e_qc_independent_system/run \
  P0A3E_DEV_EVIDENCE=/mnt/data/p0a3e_qc_independent_system/evidence.json \
  timeout 100s bash -c 'ulimit -v 1048576; /usr/bin/python3 -B tests/dev_v0_9/p0a3e/test_contracts.py'
```

Observed **32/32 passed; exit 0**, with independently retained complete stderr/stdout and JSON evidence. These included five generic 2D QO examples, canonical parsing, exact radical equality and inversion, nonoptimal rotation rejection, malformed certificate and external-identity rejection, controlled timeouts/SIGKILL, resource ceilings, atomic-save fault injection and resumed checkpoint verification. Repeating the same registered generic DEV suite is **engineering reproduction**, not a separate 32-case scientific experiment. It does not establish a universal runtime or resource guarantee.

## 4. Mathematical/software and independent-checker review

**E1 — Strict raw-input boundary: PARTIAL.** `src/.../wire.py` bounds raw request bytes, shallow lexical nesting/token counts, JSON duplicate keys, noncanonical rational strings, booleans-as-integers, signed integers and declared bit caps. `reference/.../wire.py` independently implements certificate/tower grammar and exact typed scalar checks. The tested public byte interfaces reject malformed inputs and preserve order. However upstream unbounded stream acquisition, parser/application/OS differences, unchecked internal object APIs and exhaustive adversarial nested grammar qualification remain unresolved. An error return rather than process failure is not guaranteed at every possible host-layer boundary.

**E2 — Exact algebraic predicates: DEV-SUPPORTED, SOFTWARE UNQUALIFIED.** The production mask-based square-root tower and reference dense-recursive algebra are unchanged from the signed P0A3D candidate. The source handles dependent radicals, exact zero and the nonzero zero-conjugate inverse by the frozen mathematical method; DEV reruns demonstrate these cases. This does **not** constitute formal verification of every reachable executable arithmetic branch or that all valid huge rational inputs can be computed under finite process budgets. Finite precision/resource inconclusiveness must stay `UNRESOLVED_EXACT_PREDICATE` or `RESOURCE_INCOMPLETE`, never an exact tie.

**E3 — Exact certificate checker: SUBSTANTIVE PARTIAL / DEV-SUPPORTED.** `reference/.../checker.py` reconstructs original ordered rational paths, arclength knots, centroids, variance, correlations, exact proper-rotation matrix and a **directly integrated** squared residual with an integration formulation distinct from production. It rejects forged score, reversed path, missing knots, malformed root chains, altered exact decisions and a valid-but-nonoptimal SO(2) rotation in bounded DEV examples. Independent source AST import inspection found **no direct reference import of production numerical modules** in six reference `.py` files. Nevertheless the checker shares CPython, standard-library `Fraction`, process identity/environment and the abstract arithmetic specification; the five generic comparisons and malicious-certificate cases do not qualify full-domain checker correctness. Reference's strict parser and arithmetic trust are still pending independent adversarial review.

**E4 — External trust anchors: NOT QUALIFIED.** The expected manifest is *caller-supplied*, and both production and reference independently check proposed hashes for source, schema, checker, environment and canonical original input. This is functional **unsigned DEV anchoring**, not verification of a newly human-signed P0A3E code-only authority. The `authority_mode` is explicitly `DEV_UNFROZEN_EXPECTATIONS`. Shared filesystem/root and time-of-check/time-of-use changes are not precluded, and no signed execution/loaded-module attestation is established. `identity.proposal` is not a substitute for a trusted frozen source manifest.

**E5 — Worker supervision and recovery: PARTIAL.** The parent launches production and checker workers separately, imposes wall deadlines, handles nonzero/signal/timeout states without a fabricated score, uses OS `RLIMIT` caps inside the child where supported, and re-checks a complete checkpoint via reference on resume. Temp file → `fsync` → atomic rename → directory `fsync` appears in implementation. Fault injections cover before write, after flush and after rename. **Important observed limit:** process startup can exceed the fixed address-space cap before `worker.py` installs its limit, so runtime reproducibility depends on the interpreter environment. No power-loss/kernel crash, outside-process aggregate disk quota, immutable loaded-module measurement, multi-writer safety or adversarial filesystem security is established. Both script-level and real OS ceilings need separate qualification for a deployment claim.

**E6 — Engineering DEV and evidence: PASS AS BOUNDED REPRODUCTION ONLY.** Prospectively declared case catalogue and policy are retained; two attempts and the initial failure are preserved. 32/32 reproduced on a compatible system interpreter with source unchanged. No approval follows merely from that count.

## 5. Scientific/protocol boundaries and independent disposition

The positive frozen **`P0A3D_EXACT_2D_QO_THEOREM_INDEPENDENTLY_VERIFIED`** remains unchanged. P0A3E introduces **no** 3D camera, G0/A/B branch, QH, source-derived Hebrew glyph, physical shadow law, control ensemble, statistical result or registered P0A4 validation. The v0.8 conclusion and B07/B08 historical observation/rights and candidate/control fairness gates remain unresolved. No Git writes/commits/pushes or prior P0A0 scientific replay were performed by this QC; the evidence available is consistent with the agent's restricted-action report, although unseen host operations cannot be universally disproved.

**Independent QC decisions:**

- `P0A3E_ARCHIVE_INTEGRITY_PASS`
- `P0A3E_BOUNDED_DEV_REPRODUCIBILITY_PASS_ON_COMPATIBLE_INTERPRETER`
- `P0A3E_SOFTWARE_IMPLEMENTATION_INCOMPLETE`
- `P0A3E_EXACT_PREDICATE_UNQUALIFIED` (as an executable)
- `P0A3E_REFERENCE_INDEPENDENCE_UNQUALIFIED` (for full-domain certification)
- `P0A3E_INPUT_FAILURE_ENVELOPE_INCOMPLETE`
- `P0A3E_RESOURCE_CRASH_ENVELOPE_INCOMPLETE`
- `P0A3E_EXTERNAL_TRUST_ANCHOR_UNQUALIFIED`
- `P0A3E_REGISTERED_VALIDATION_NOT_RUN`

**DO NOT assign** `P0A3E_EXACT_2D_QO_SOFTWARE_CANDIDATE_READY_FOR_REGISTERED_TARGET_FREE_VALIDATION`; a positive human-signed code-only freeze is not warranted from this evidence. No P0A4 execution or target access is authorized.

**Recommended next action:** preserve the 968,965-byte original ZIP and the present independent QC **without alteration**, as a separately signed *incomplete* engineering checkpoint if desired. A subsequent narrow hardening/qualification stage should first make the interpreter/runtime policy reproducible or fail before invoking incompatible work, replace unsigned DEV expectations with a human-approved external source/checker/config manifest at the correct point in the signing workflow, and qualify public-input/certificate failure envelopes and resource process isolation. Keep the P0A3D theorem fixed. If the user chooses an explicitly limited operational environment, record the limitation as an engineering deployment contract without narrowing the theorem's abstract rational-input domain. Only after source-level independent QC and a positive code-only freeze should a separately signed target-free registered validation be contemplated.

**Independent checks do not amount to formal proof of the executable, external peer review, or a genuine historical Hebrew projection result.**
