# P0A3 — Target-Blind Numerical Implementation and Certification Architecture

**Project:** Meru Geometry Audit  
**Development line:** `v0.9` — Hebrew projection specificity and effective-viewing-capacity audit  
**Repository:** `salahealer9/meru-geometry-audit`  
**Branch:** `hebrew-projection-capacity-v0.9`  
**Drafted:** 2026-10-16  
**Status:** **DRAFT — not preregistered until human GPG-signed protocol-only commit**  
**Phase type:** additive target-blind *implementation-only engineering*, static proof-obligation design and bounded DEV-level software checks; **not registered scientific certification**  
**Hebrew target information:** **NO ACCESS / NO EXTRACTION / NO SCORING**  
**Agent Git authority:** **NO COMMIT / NO PUSH / NO MODIFICATION OF THE EXISTING REPOSITORY**

## 0. Scientific purpose and exact authority

P0A0 demonstrated synthetic engineering oracles and failure modes; P0A1 qualified representation/method families for design; P0A2 defined two conditional target-blind score candidates and two exact nested viewing-direction candidates, but certified no global numerical solver. P0A3 is the **first implementation-only engineering phase**: translate those frozen mathematical contracts into inspectable, reproducible *draft code* and independent reference/checker architecture, with strictly limited software-development checks and no new registered scientific execution.

**Question:** Can an implementation package for QO, QH and families A/B be made precise enough to undergo independent static/source QC and a *subsequent*, separately preregistered target-free numerical certification, without target-conditioned decisions or unsupported global-optimum claims?

Keep distinct: (i) source-attested facts; (ii) frozen mathematical theorems; (iii) engineering code implementing proposed contracts; (iv) independently checked proof obligations; (v) future registered numerical certificates; (vi) future target observations. Source code that executes is **not** thereby a certified mathematical result. A successful development test is **not** a preregistered certification experiment. A missing historical physical-shadow operator is not supplied by an orthographic point renderer.

This phase **does not choose** a final Hebrew score, comparison representation, G1/G2 hierarchy, epsilon, statistical threshold, candidate geometry, N0–N3 control law, rights interpretation, segmentation, historical FIRST HAND model or v0.9 scientific outcome. It implements both conditional alternatives in *separate* namespaces/paths, retaining all observed limitations. No matching of real letters, fonts used as proxy letters, Hebrew images, source-derived strokes or glyph pixels is authorized.

### Immutable authority: verify before implementation

| Checkpoint | Exact identifier |
|---|---|
| Signed v0.8 closeout | Tag `v0.8.0`; `NO_REPRODUCIBLE_PUBLISHED_FIRST_HAND_CONSTRUCTION_RECOVERED` |
| P0A0 protocol commit | `d15865167b4e3c454e398bd498d9d681103096f7` |
| P0A0 protocol Git blob | `0f8b663bfe2432685c9320a00c80fd6bcf436e38` |
| P0A0 implementation freeze | `24c00fc44e4d9d57adacd1e636e9e2d20d86a954` |
| P0A0 results freeze | `5148712c07ac48742d3435dc14e01667280f94c3` |
| Original P0A0 JSONL SHA-256 | `4b4b27b0d5d9a95ffe864e2d2c83433be0ddd544b6122ebbea294857326817d6` |
| P0A1 protocol commit | `5b0317f193c481d799e88b494ce370679fec43bc` |
| P0A1 protocol blob | `d0a20485e8a2793fae6ede040fc266e461c8f23f` |
| P0A1 methodology freeze | `090a1db6c95976bbb5f0d69a3cc4a4603d165505` |
| P0A2 protocol commit | `e917fa2974997703d6ccb60b0b25d0c668d12bd5` |
| P0A2 protocol Git blob | `61585fb47cdb3ff2a3cfef07d3548fbd08084d0b` |
| **P0A2 human-signed decision freeze: expected direct parent of P0A3 protocol** | **`07b64003940072e00fb2ce969ebc3866a9a3dc4d`** |
| Expected GPG signer fingerprint | `D4EC014EEFCC90E619D2AA59A91239ABCF512130` |

The remote P0A2 freeze commit was independently verified on 2026-10-16: exact parent `e917fa2974997703d6ccb60b0b25d0c668d12bd5`, GitHub signature valid, 21 additive report files, remote HEAD at the freeze commit. The subsequent P0A3 Work handoff must additionally verify the **actual signed P0A3 protocol-only commit and Git blob**. Historical `DRAFT`/`PRE-QC` labels in frozen reports must not be changed; later signed decisions govern their final status.

### Authoritative read-only evidence

- `reports/v0_9/p0a2_target_blind_design/P0A2_DESIGN_DECISION_CLOSEOUT.md`
- `reports/v0_9/p0a2_target_blind_design/P0A2_NUMERICAL_DESIGN_REVIEW.md`
- `reports/v0_9/p0a2_target_blind_design/score_normalization_candidates.md`
- `reports/v0_9/p0a2_target_blind_design/direction_family_candidates.md`
- `reports/v0_9/p0a2_target_blind_design/solver_certification_matrix.csv`
- `reports/v0_9/p0a2_target_blind_design/numerical_error_failure_ledger.md`
- `reports/v0_9/p0a2_target_blind_design/capacity_and_nuisance_budget.csv`
- `reports/v0_9/p0a2_target_blind_design/design_decision_register.csv`
- `reports/v0_9/p0a2_target_blind_design/fairness_and_future_estimands.md`
- `reports/v0_9/p0a2_target_blind_design/historical_target_dependency_map.md`
- `reports/v0_9/p0a2_target_blind_design/P0A2_independent_QC_report_2026-10-16.md`
- `reports/v0_9/p0a1_methodology/P0A1_METHODOLOGY_DECISION_CLOSEOUT.md`
- `reports/v0_9/p0a0_registered_execution/CASE_MATRIX.md`
- `reports/v0_9/p0a0_registered_execution/p0a0_registered_pilot_once.jsonl` (**inspect only, no replay**)
- `docs/geometry/projection_orbit_results_v0_5.md` and `docs/first_hand_construction_source_recovery_closeout_v0.8.md`

Preserve P0A2's six coexistently limited statuses: `P0A2_OBSERVATION_MODEL_UNRESOLVED`, `P0A2_SCORE_SELECTION_DEFERRED`, `P0A2_CAPACITY_CERTIFICATION_DEFERRED`, `P0A2_SOLVER_CERTIFICATION_DEFERRED`, `P0A2_CONTROL_FAIRNESS_NOT_SPECIFIED`, `P0A2_SOURCE_CONSTRAINT_UNRESOLVED`.

## 1. Hard execution and repository boundaries

1. Agent may **read** verified GitHub source, existing Python files and frozen reports. Author new files **only inside a separate delivery/work directory outside the repository**, export an additive reviewed ZIP and logs. The user alone stages, GPG-signs or pushes any approved code later. No agent checkout replacement, in-place source edits, `git add`, commits or pushes.
2. Never modify, call, replay or refit `registered_pilots/p0a0` S00–S12, or change its fixtures, logs, implementation, manifest, protocol, or case classifications. Do not import a P0A0 case evaluator as a development shortcut.
3. No registered scientific pilot, optimizer benchmark, numerical capacity/covering sweep, inference/detectability simulation, candidate-versus-null study, or Hebrew-target computation. No new scientific numerical result may be presented as P0A3 evidence.
4. **Permitted DEV-only checks**, after the P0A3 protocol is human-signed: narrowly bounded deterministic software unit tests on independently constructed generic mathematical microexamples to check parsing/API shape, basic analytic identities, invalid-input handling, exact finite-set membership/counts, and deterministic serialization. These may use fresh synthetic numeric inputs solely for debugging. They are **not registered numerical certification**, must not use the frozen P0A0 case coordinates/oracles, produce scientific performance claims, optimize a physical 3-D object, or select parameters by observed behavior. Record every command, test count, failure and repair; an agent may omit running DEV tests if environment constraints prevent a defensible separation.
5. New adversarial *registered* certification fixtures, generator seeds, solver thresholds, tolerances, numerical coverage measurements and stopping criteria require a **separate future signed target-free validation protocol**, an independently QC-approved code-only freeze, and explicit one-run authorization. No DEV log may substitute for that preregistration.
6. Strict target-information barrier: do not open, fetch, decode, display, OCR, skeletonize, trace or score A09/A06 or other Hebrew chart images, text fonts as surrogate glyph targets, prior extracted glyph arrays, and no Hebrew-derived shape data even if locally cached. A09 source metadata may be cited but is not proof of inspected image bytes; do not download the JPEG.
7. Historical optical/carrier facts remain unresolved, including the missing three function sets. No R3-S→R2-H physical shadow implementation shall be represented as historical reconstruction. Planar ink rendering and graph extraction are **out of P0A3's scientific implementation scope**.
8. No fresh Meru archival content without a separately signed provenance intake/amendment. Inherited missing-crop, two image-test exclusions, incomplete DEV log, P0A1 interrupted-draft recovery and GPG-agent setup caveats remain recorded.
9. If lineage, blob, original source/result hash or information-barrier integrity is genuinely violated: **STOP**, quarantine affected draft outputs, preserve diagnostics and ask for independent resolution. Do not work around or silently repair.

## 2. I0 — Freeze identity, requirements traceability and software boundary

Verify exact signed P0A3 protocol commit/blob, signed parent, branch, signer and complete frozen P0A0–P0A2 ancestry; check local worktree/head/upstream without resetting a divergent checkout. Verify all pinned read-only report blobs and inherited P0A0 result hashes; verify expected signed P0A2 scientific status without assuming unresolved matters are solved. Record the actual environment used for **development checks only**, and note whether separate production/reference dependency isolation is available. Do not install dependencies into the established repository environment without separate authorization.

Prepare a requirement-to-code/test/proof-obligation mapping for: QO, QH, A/B, four Q×family products, O1–O5/H1–H5/CAP1–CAP5/F1–F2 from the P0A2 numerical ledger, and all failure/status contracts. Record every design point left for a later signed decision rather than guessing a numeric constant.

## 3. I1 — Frozen-interface proposal, package layering and exact data contracts

Specify implementation APIs in a separate `src/meru_geometry/v0_9/`-style **proposed** additive namespace, avoiding modification or monkeypatching of P0A0/v0.3–v0.8 scientific modules. Expose conceptually distinct modules for `contracts`, `directions`, `projection`, `qo`, `qh`, `reference`, `certificates`, `serialization` and `exceptions`. Refine paths if justified in an auditable architecture note; do not use hidden API aliases to conflate representations.

Required immutable-like records:

- mathematical input IDs and type (`R3-C`, `R2-O`, `R2-U`); coordinates/segments/closure/order and explicit units; raw provenance fingerprint; input validation and zero-extent outcomes;
- exact direction-family ID, tier, stratum, integer triple, symbolic norm or exact algebraic representation, antipode, SO(2)/O(2) convention, canonical proper lift and possible seam;
- observation and normalization definitions and measures (planar arclength vs uniform distinct points); independently recorded centroid/RMS and precision/error status;
- score/family/camera/traversal/reflection option and full nuisance budget, with one **declared** group action per computation;
- certified result envelopes `(L,U,epsilon)` only when backed by a complete independent checker; a feasible witness or DEV `success` flag must never be called `GLOBAL_CERTIFIED`;
- deterministic `INVALID_INPUT`, `NOT_EVALUABLE`, `LOCAL_ONLY`, `BOUNDED_APPROXIMATION`, `GLOBAL_CERTIFIED`, `GLOBAL_CERTIFICATION_DEFERRED`, and `UNRESOLVED_PROOF` records with separate error and evidence fields;
- immutable machine-readable provenance/checksum/manifests and a versioned JSON schema, serializing nonfinite data as explicit errors, not JSON NaN/Infinity.

An implementation-ready API contract must specify shape, orientation (column-vector mathematical convention vs legacy row-vector code), matrix multiplication, coordinate/normalization arithmetic, required fields, error propagation, canonical ordering and tie/near-tie semantics, and how a downstream caller is prevented from silently requesting unavailable historical or target observations.

## 4. I2 — QO ordered-arclength branch: implement only the declared lane

Use frozen P0A2 `score_normalization_candidates.md`, “QO” and `numerical_error_failure_ledger.md` O1–O5. Define QO for one genuinely **open ordered** polyline on each side, normalized by planar arclength measure (`du`), with positive total length and RMS radius. Consecutive zero-length segments may be omitted under this explicit path interpretation, but retracing/nonconsecutive returns must remain; preserve an event/diagnostic ledger for projected collapses. No open cyclic shifts, arbitrary warps, multi-stroke assignment, cropping, component masking or hidden reflections. Reversal is a separately registered option, default disabled; O(2) belongs to a separately labeled sensitivity branch, not free extra views.

Implement deterministic calculation of each polyline's piecewise-linear arclength parameterization, segment breakpoints, centroid and RMS integral, and common-breakpoint exact-polynomial-product expression (allowing a numerical production realization but retaining separate reference route). For each permitted traversal branch compute α,β, with square residual `2−2√(α²+β²)` and associated minimizing roll. If α=β=0, report whole-roll tie, canonical 0; if arithmetic uncertainty makes the radicand straddle zero, report interval/precision uncertainty instead of clamping silently. A floating q-value is an **engineering candidate**, not a global certificate without a rigorous enclosure/reference check.

Implement deterministic projection `R3-C → R2-O` for an explicit supplied 3-D centreline and exact camera-lift convention. Reject unsupported input status before scoring. Do not call this a hand/ribbon shadow, derive a target stroke path, or fit a 3-D deformation. Keep observation/projection errors separate from alignment/integration errors. If exact or rigorous integration cannot be implemented within this bounded phase, deliver code with explicit `GLOBAL_CERTIFICATION_DEFERRED` plus a specific missing proof/implementation checklist, never an invented exactness claim.

## 5. I3 — QH finite-support branch: implement only the declared lane

Use frozen P0A2 “QH” and H1–H5. Accept nonempty **finite sets of distinct planar points**, not disguised ordered paths or topology. Exact duplicate equality follows a declared arithmetic representation; never tolerance-merge nearby points. Uniform probability weights on the distinct set determine independent centroids/RMS; reject zero or uncertifiably small extent. Camera projection of supplied finite 3-D vertices is a finite observation with explicit coincidence/multiplicity policy, not an approximation to a full continuous 3-D silhouette.

Implement both directed finite sampled nearest-neighbour extrema and their symmetric maximum at a **fixed** angle; production acceleration, if any, must be accompanied by an exhaustive independent scalar all-pairs reference, with no shared nearest-neighbour routine. Never infer components/strokes/graphs from a Hausdorff score. Translation and scale are fixed by QH's two positive empirical RMS normalizers, not residual free-scale optimization. O(2) is a separate sensitivity. Incomplete/empty/degenerate supports give deterministic unscored statuses, not zero.

For the continuous **planar-roll** minimization, separate (a) feasible candidate evaluation, (b) a rigorously justified global lower bound on every covered angle cell, and (c) the independent certificate checker. The frozen P0A2 bound `|f(θ)-f(φ)|≤ρ_A d_{S¹}(θ,φ)` is admissible only for its *fixed normalized finite set* and correct angular error semantics. Implement certificate-record structure and complete-circle/wrap-around coverage obligations, with independent verification of cell bounds, witness feasibility, rounding and gaps. Do not assert that floating interval-like numbers produced by ordinary rounding are directed/outward bounds. Until such arithmetic and completeness are independently justified, return `GLOBAL_CERTIFICATION_DEFERRED` or `LOCAL_ONLY`, **not** `BOUNDED_APPROXIMATION` or `GLOBAL_CERTIFIED`.

## 6. I4 — Direction-family A/B generators, canonical frames and capacity semantics

Implement exact symbolic/int-triple family definitions, leaving the frozen mathematical sets unchanged:

- A0 = six ±coordinate axes;
- C = eight `(±1,±1,±1)/√3` corners;
- E = twelve normalized triples with one zero and two ±1 entries;
- T = twenty-four normalized triples with one zero and nonzero absolute values 1,2 in either order.

Family A is `A0`, `A0∪C`, `A0∪C∪E`: **6/14/26** signed directions. Family B is `A0`, `A0∪E`, `A0∪E∪T`: **6/18/42**. Normalize symbolically or use exact integer triples plus explicit square norms; no decimal tolerance merging. Freeze a canonical stratum-append order and integer-triple lexicographic order within strata, exact antipodes and O(2) representative rule. G0 must agree for both families. Stage-wise nesting and distinctness can be checked at the **DEV engineering** level, but the signed mathematical proof in P0A2 remains the authority; no new measured covering/separation claim follows from a passing test.

Construct the deterministic proper frame lift of P0A2: choose basis index minimizing `|n_j|` (x,y,z tie order), `u=(e_j−(e_j·n)n)/√(1−(e_j·n)²)`, `v=n×u`, rows `(u,v,n)`. Keep lift seams explicit; roll is redundant **only** for compatible orthographic SO(2)-equivariant observations. Numerically checking `det≈1` cannot replace a rounding-error proof. For opposite directions preserve reflection semantics. Add an independent manifest checker that reconstructs all signed triples without using the production generator; exact family ID/tier/hash/reference witnesses must be emitted in the code package.

SEP/COV/ROUND certificates (CAP1–CAP5) remain incomplete unless the new independent code and proof obligations actually establish them; do not run a numerical covering sweep, select final G1/G2 or claim a physical-shadow quotient. Continuous `S²` optimization and claimed `Lδ` coverage bounds are **outside implementation certification** until a uniform L, certified δ and admissible nondegenerate domain are signed and proved.

## 7. I5 — Independent mathematical reference and certificate-verifier architecture

Deliver reference/checker source code with a dependency diagram showing **no call from a reference oracle to the production routine it checks**, including normalization, nearest-neighbour, arclength integration, direction generation and tie logic where independent execution matters. Independent code may share signed input schema, but not production numerical kernel or its cached results. If independence is incomplete, mark the specific claim `INDEPENDENT_ORACLE_NOT_ESTABLISHED`.

Minimum separations:

1. QO production piecewise accumulation vs independent rational/algebraic segment-integral derivation and trigonometric minimization checker; distinguish symbolic exactness of an input theorem from rigor of finite-precision output.
2. QH production pair extrema vs independent explicit pairwise-distance checker; rotation-cell interval bounds vs independent cell-coverage/geometry checker; no unproved global claim.
3. A/B generator vs independently constructed literal/exact integer-pattern membership tables and completeness counts; lift proof vs independently checked proper-matrix identities on eligible exact samples.
4. Certificate schemas report all branches/cells, lower/upper enclosures, feasible witnesses, uncertainty, omitted/invalid-input policy, residual and exact source/config identities. A claimed `GLOBAL_CERTIFIED` flag must be **unrepresentable** without a valid reference/proof object and independent verification; even then no P0A3 package is globally certified before later registered QC.
5. Reference and production dependency/package versions and arithmetic backends must be inventoried; no assertion of independence from mere different filenames.

Prepare static proof obligations and precise acceptance criteria for O1–O5, H1–H5, CAP1–CAP5, F1–F2 and any new obligations introduced in P0A3. Use explicit `PROVED_SYMBOLICALLY`, `IMPLEMENTED_UNVERIFIED`, `DEV_CHECKED_ONLY`, `DEFERRED`, `FAILED`, `NOT_ESTABLISHED` tags as appropriate. Do not turn a DEV test into a mathematical theorem or registered certificate.

## 8. I6 — Bounded DEV engineering checks and future validation preregistration

A Work agent may run bounded, deterministic **DEV-only** unit tests of *fresh generic microfixtures*, with tests named and categories declared before running. Authorized categories: API serialization/schema and branch enumeration; exact duplicate/coincident handling; rational-line/simple polygonal arclength identity; known planar rotations and translations independent of Hebrew forms; bad-dimension/nonfinite/zero extent rejection; independent exact integer triple sets/counts and nested tiers; frame-lift orthogonality/properness on non-Hebrew canonical inputs; finite-pair nearest-distance identity; certificate-structure rejection of incomplete cells/bounds. No P0A0 registered-case fixtures or optimizer benchmarking/replays. DEV scripts must not execute source-derived 3D geometry versus 2D target proxies.

A unit-test suite can evolve during implementation; preserve pre-run tests, post-fix diffs and full command/output logs, and distinguish exploratory versus post-fix tests. Record exact Python, packages, platform, environment, deterministic ordering, dependency lock/proposed pin inventory, CPU limits and run totals. No seeded numerical sweep or search-tolerance tuning may be disguised as DEV. If a proposed unit test risks becoming a new scientific probe, **do not execute it**; register it in a future validation protocol instead.

Design, **but do not run**, a new P0A4 target-free registered certification catalogue. It must be independently defined with input IDs/oracles and failure conditions before its one authorized execution; cover new path-density, label ambiguity, raster gap, component, endpoint, notch, reversal, tiny-scale, local-vs-global and camera-roll/capacity pathologies *without reusing or rerunning S00–S12*. Include exact/interval reference cases, near ties, symmetric and coincident views, all-camera invalidity, full circle seam and interval coverage, floating cancellation, bit-precision sensitivity, timeout and certificate completeness, and separate control-parity instrumentation. Do **not** assign new test outcomes, effect sizes, thresholds, seeds or tolerances from these descriptions; these are future preregistration obligations.

## 9. I7 — Failures, proof status and source/target/control fairness

Specify deterministic invalid/unevaluable, interrupted and incomplete-certificate behavior at the API, module, manifest and final-result levels. Distinguish: mathematical nonattainment; finite valid low score; near-zero undefined normalization; numeric enclosure too wide; algorithm timeout; missing target observables; absent physical optics; incomplete angle-cell coverage; unverified independent oracle. None maps to a perfect match. Preserve non-finite input rejection and prohibit non-standard NaN/Infinity JSON emission.

The same QO/QH contracts, family/tier manifest, allowed nuisance options, exact/approximation goals, failure-state reporting and resource budget **must be exportable unchanged** for later candidate and N0–N3 controls. Their actual generators/distributions/shape-parameter laws are still undefined, so do not instantiate or test them. Do not claim actual parity until those distributions and source-constrained candidate object domains are frozen. The 22 Hebrew bases remain a fixed corpus and not independent statistical replicates; actual target extraction, 22-vs-27 convention, secondary chart, statistical calibration, detectable effects and multiplicity are later signed gates.

Retain the five source-provenance classes `SOURCE_ATTESTED`, `SOURCE_CONSTRAINED_INTERPRETATION`, `INDEPENDENT_DIAGNOSTIC`, `NULL_CONTROL`, `UNRESOLVED` in all technical documents, and label this new code `INDEPENDENT_DIAGNOSTIC` until specifically licensed for another observation model. Preserve v0.8 missing final deformation/three functions/hand-shadow law. Do not attribute A/B directions or L1 projections to Tenen as uniquely historical.

## 10. I8 — Implementation delivery, independent QC and decision register

Deliver an **additive implementation-candidate ZIP**; no agent repository modifications. Preferred layout (filenames may be minimally amended with an inventory mapping, not silently omitted):

- `docs/v0_9/p0a3_implementation_contracts.md` — public API, inputs, nuisance semantics, exceptions, no-target scope;
- `docs/v0_9/p0a3_production_reference_independence.md` — dependency/import DAG, shared boundary, independence failures;
- `docs/v0_9/p0a3_target_free_validation_design.md` — separately registered future test catalogue, not executed;
- `src/meru_geometry/v0_9/__init__.py`, `contracts.py`, `directions.py`, `projection.py`, `qo.py`, `qh.py`, `certificates.py`, `serialization.py` (proposed module shape);
- `reference/v0_9/` — independent reference algorithms/checkers, with all exact names inventoried;
- `tests/dev_v0_9/` — strictly DEV engineering tests using new generic microfixtures, no S00–S12 import;
- `reports/v0_9/p0a3_implementation/IMPLEMENTATION_ENGINEERING_REVIEW.md` — I0–I7 evidence and known limitations;
- `reports/v0_9/p0a3_implementation/requirements_to_code_and_proof.csv`;
- `reports/v0_9/p0a3_implementation/independent_oracle_matrix.csv`;
- `reports/v0_9/p0a3_implementation/certification_status_and_failure_ledger.md`;
- `reports/v0_9/p0a3_implementation/dependency_environment_manifest.json`;
- `reports/v0_9/p0a3_implementation/dev_commands_and_results.log` (possibly `NOT_RUN` with reason);
- `reports/v0_9/p0a3_implementation/provenance_and_information_barrier.json`;
- `reports/v0_9/p0a3_implementation/INDEPENDENT_QC_CHECKLIST.md`;
- ZIP-root `PACKAGE_INVENTORY.json`, `SHA256SUMS` (full payload file hashes/lengths), and human-readable `README.md`.

The ZIP must preserve UTF-8 file content, deterministic relative paths, SHA-256 and byte lengths. No zipped symlinks, traversals, secrets, hidden state, remote image assets, generated glyphs, figure renders, source correspondence, simulation output or P0A0 numeric replay. Include `git diff`/frozen-source preservation evidence **only if actually inspected**. Every observed DEV failure, incomplete module, unimplemented certificate and dependency uncertainty must be visible. Every result must say whether it is `PROVED_SYMBOLICALLY`, `IMPLEMENTED_UNVERIFIED`, `DEV_CHECKED_ONLY`, `NOT_ESTABLISHED` or `DEFERRED`; avoid substituting a blanket “tests pass”.

Independent QC later assesses source identity, protocol conformance, mathematical semantic fidelity, independence of reference/checker implementations, full original-test non-replay boundary, explicit failure states, source/provenance restrictions and agent no-Git-write evidence. Even an approved code-only package is **not** a registered numerical certificate, not authorization for targets and not an automatic commit. Subsequent human signature would freeze accepted files **separately from this protocol** with preserved source/config digests; P0A4 target-free validation must preregister its cases/oracles/accuracy/stopping and use that signed implementation freeze as parent.

## 11. I9 — Decisions, stops and future handoff gates

The only eligible positive engineering **readiness** status (assignable after independent QC and a separately human GPG-signed implementation-only freeze) is:

`P0A3_TARGET_BLIND_IMPLEMENTATION_READY_FOR_REGISTERED_CERTIFICATION`

It means complete, inspectable **candidate code and engineering controls** are ready to be subjected to a separately registered target-free certification. It does **not** mean numeric correctness is certified, a global solver passes, final score or G1/G2 selected, physical shadows reconstructed, Hebrew matching authorized or scientific specificity established.

Limited or blocking outcomes may coexist:

- `P0A3_IMPLEMENTATION_INCOMPLETE` — missing mandatory candidate code/interface/serialization;
- `P0A3_REFERENCE_INDEPENDENCE_NOT_ESTABLISHED` — critical oracle shares unreviewed numerical kernel or could not independently validate;
- `P0A3_NUMERICAL_CERTIFICATION_DEFERRED` — all four QO/QH×A/B still lack registered certificates;
- `P0A3_OBSERVATION_MODEL_UNRESOLVED` — target order/graph, optics/hand shadow unestablished;
- `P0A3_EFFECTIVE_CAPACITY_LEVELS_UNSELECTED` — A/B only candidate designs, not final G1/G2;
- `P0A3_CONTROL_FAIRNESS_UNVERIFIED` — actual N0–N3 laws/budgets unchosen;
- `P0A3_PROVENANCE_MISMATCH` — STOP when signed/hash/frozen lineage mismatch;
- `P0A3_INFORMATION_BARRIER_VIOLATION` — STOP/QUARANTINE if actual/proxy Hebrew target data influenced code, numerical parameters or test outcomes;
- `P0A3_UNAUTHORIZED_EXECUTION` — STOP if P0A0 registered cases, unpreregistered scientific sweeps/optimizers, candidate-null or registered certification were run.

If a full implementation route is not achievable, retain a complete partial artifact and clear blocker register; do **not** assert readiness merely because some code compiles. No agent self-approval, no reviewer self-signature, no retrospective editing of signed P0A0–P0A2 data and no silent code repair after a code-only freeze.

### Human-controlled gate sequence

1. Review **this draft** against frozen P0A2 closeout, QO/QH definitions, two family proofs, four certificate status rows, input/rights/target barriers and all limited statuses.
2. Verify clean branch `hebrew-projection-capacity-v0.9`, exact HEAD **`07b64003940072e00fb2ce969ebc3866a9a3dc4d`**, expected signer and upstream. Confirm the only staged item will be the P0A3 protocol; no unrelated repository changes.
3. Add **only** `docs/v0_9/p0a3_target_blind_numerical_implementation_and_certification_architecture_protocol.md`, inspect the entire staged protocol and `git diff --cached --check`; create a **human GPG-signed protocol-only preregistration** and push the feature branch. Record full commit, parent, protocol Git blob and signer. Text saying DRAFT is archival once signed.
4. Only after that freeze, prepare a separate agent handoff with the **actual** signed commit/blob. The agent creates isolated implementation code and limited DEV evidence; **NO COMMIT / NO PUSH / no writes to prior repository**. Keep original test/result gates closed.
5. Independently QC the Work implementation ZIP. If approved, the human—not the agent—reviews/stages an additive **implementation-only freeze** of accepted files; any necessary protocol amendment must be separately signed before use.
6. Draft/sign an independent P0A4 target-free registered numerical-certification protocol referencing frozen implementation bytes, case/oracle versions, deterministic failures, limits and one authorized run. Freeze fixtures/test harness first, execute exactly as authorized, independently QC and preserve negatives. No P0A0 replay.
7. Only later independent rights/target extraction, candidate/N0–N3 parity/definition, detectable-effect and fixed-corpus confirmatory gates can authorize real Hebrew target computation. **Neither P0A3 nor P0A4 automatically opens the target barrier.**

**Current document state:** draft for human preregistration. Preparing it performs **no numerical execution or modification of the frozen scientific code**.
