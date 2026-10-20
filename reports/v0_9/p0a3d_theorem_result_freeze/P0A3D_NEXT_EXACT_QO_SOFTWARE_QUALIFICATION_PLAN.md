# P0A3D — Next Restricted Exact-QO Software Qualification Path (NON-AUTHORIZING)

**Prepared:** 2026-10-20. **Status:** discussion/roadmap only; **NOT a signed protocol, execution authority, new theorem, validation run, or license to modify frozen code**. To become executable, the next phase needs a new one-file, human-reviewed GPG-signed protocol anchored to the eventual P0A3D theorem-result freeze commit.

## Why separate engineering from mathematical proof

The P0A3D independent QC found a sound generic theorem for two rational-vertex ordered open 2D polylines under `SO(2)`, including dependent radical exact signs and an attained algebraic witness. The executable production and reference implementations are more advanced than P0A3C, but incomplete on hostile input and bounded runtime/failure domains. More passing happy-path DEV cases would not independently qualify them.

**Recommended next phase label (provisional): `P0A3E — Restricted Exact-2D-QO Software Hardening and Independent Certificate Qualification`.** The next protocol should specifically state that this is a **code-only engineering** phase; registered certification remains a later, separately authorized run. No new 3D/G0/A/B/QH extension.

| Priority | Falsifiable engineering acceptance requirement | Current limitation retained |
|---|---|---|
| E1 — Strict input and schema | Versioned canonical JSON, rational numerator/denominator strict types and reductions, finite ordered-vertex and endpoint metadata; fail-closed typed exceptions for booleans-as-ints, floats/NaN, huge integers and nested invalid structures; protect canonical input hashing from rejected records | Parser and schema qualification incomplete |
| E2 — Mathematical predicate fidelity | Production exact tower sign/equality/inverse under reducible adjunctions, comparison of arbitrary eligible valid nested radicals, correct exact-zero versus unknown; reference isolated predicates must independently reconstruct proof conditions | Exact software predicate unqualified despite abstract theorem |
| E3 — Exact witness validation | Independently reconstruct moments, correlations, optimal `SO(2)` matrix, determinant, residual and ties from original ordered paths; reject valid-but-nonoptimal witnesses, forged indices, missing knots, malformed algebraic proofs and dependency tampering | DEV checks only; not adversarial certification |
| E4 — Trust and source identity | Externally expected human-frozen code, config, schema, input and checker hashes; distinct source/reference dependency DAG and explicit common CPython/Fraction trust boundary; deterministic reproducible evidence | Self-reported/live hashes cannot establish external provenance |
| E5 — Resource and crash envelope | Bounded input parsing, subprocess/time/memory/recursion/intermediate-bit growth policy with conservative fail-closed `RESOURCE_INCOMPLETE`; explicit hard crash, timeout, killed process and temporary-file semantics; no fabricated score/certificate | No uniform runtime/resource guarantee or complete failure typing |
| E6 — Independent engineering QC | Prospective bounded DEV microcontracts, negative/adversarial cases, independent source review, exact historical attempt preservation, full manifests and stop conditions; all failures and fixes retained | Passing 20 DEV cases is not sufficient |

## Proposed acceptance and stop rules

1. Bind the **exact original 642,047-byte P0A3D ZIP**, original proof, dated independent QC and new theorem-result freeze SHA before work. Preserve original DEV attempts 01–04 byte-for-byte. Do not change frozen theorem inputs, normalization, `SO(2)` nuisance scope or statuses retroactively.
2. Develop in an isolated directory; agent makes **NO COMMIT / NO PUSH / NO REPOSITORY CHANGES**. Only bounded new generic engineering DEV fixtures with prospectively frozen caps; no P0A0 replays, statistical experiments, benchmark tuning or actual Hebrew sources.
3. Define failure conditions and external hash anchoring before DEV; never turn exact predicate `INCOMPLETE` into `EXACT_ZERO`, accept a numerically overlapping interval as proof of algebraic equality, or silently exclude otherwise valid rational-coordinate paths.
4. An independent reviewer must inspect algorithm and common trust base; if the target engineering domain is not fully supported, preserve `IMPLEMENTATION_INCOMPLETE`, not `READY` because many unit tests passed.
5. A separately human-signed **code-only implementation freeze** may record a qualified candidate *only after positive source/engineering QC*. Later a **separate preregistered target-free adversarial validation** with new independent fixtures, fixed stopping/budgets and one authorized run is needed. A theorem-level approval does not confer software certification.

## Later conditional extension ladder

After successful independent exact 2D QO software qualification: (i) preregister a *target-free* code certification run, QC and freeze; (ii) separately derive G0 view projection and degeneracy branch rules; (iii) independently extend finite A/B cameras and exact branch minima; (iv) separately treat QH and all-circle certificates; (v) separately establish historical source/shadow/rights and independently justified ordered observations; and (vi) specify and preregister fair N0–N3 candidate/control laws, detectable effects and statistics **before** historical target access. None is authorized by the present roadmap.

**Honest near-term goal:** a small, independently reviewable exact arithmetic + certificate-checking service for the theorem already established, not another unbounded multi-domain build.
