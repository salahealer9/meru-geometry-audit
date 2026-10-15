# M6 — Optimization certification requirements

**PRE-QC / no optimizer executed.** Recovered requirements preserve the completed review's scope.

[FROZEN RESULT] `reports/v0_9/p0a0_registered_execution/p0a0_registered_pilot_once.jsonl`, S11: success true, local angle 3.1415926535897936, value **0.4**, six evaluations, `LOCAL_BOUNDED_ONLY`; analytic global value **0** at angle zero, discrepancy **0.4**. `docs/v0_9/p0a0_implementation_specification.md`, S11 row/contract, fixes basin [π−1/4,π+1/4]. That restricted basin excludes the full-domain global minimizer. This defeats a generic global claim, not the solver's declared local contract or every possible local algorithm. Values are copied, not recomputed; the case remains EXPECTED_BLIND_SPOT.

## Status contract

| Status | Evidence needed | Permissible claim / excluded shortcut |
|---|---|---|
| GLOBAL_CERTIFIED | Exact analytic proof, complete exact finite exhaustion or mathematically justified global-optimum certificate under explicit arithmetic semantics | Full declared domain; report rounding enclosure/uniqueness separately. A success flag, tighter tolerance, multistart or unproved grid is insufficient. |
| BOUNDED_APPROXIMATION | Feasible upper bound U and independently justified global lower bound L, U−L≤ε, with full-domain completeness and other error budgets | Explicit global ε-approximation, not an exact/unique minimum. Nonzero objective gap is not relabeled exact. |
| LOCAL_ONLY | Feasible candidate, actual restricted domain and termination history, no full-domain bound | Local value / feasible upper bound only; no claim of global reliability. |

[METHODOLOGICAL PROPOSAL] A future signed protocol must instantiate these requirements and resolve arithmetic semantics. No P0A1 summary assigns a new global certificate. S11 cannot be fixed by reexecuting it, widening its frozen bounds or treating its local success as certification.

| Required field | Future auditable content |
|---|---|
| Objective | Formula, representation, terms/weights, units, normalization, observational uncertainty, code and independent-oracle hashes |
| Domain | Finite or compact continuous set; parameter charts, seams/boundaries, camera sphere/axis quotient; noncompact and degeneracy exclusions; prove attainment or label infimum |
| Continuous nuisance | Camera, planar rotation, permitted scale/translation and any registered variables; coordinate poles and projection collapse covered; no unregistered shape deformation |
| Discrete nuisance | Reflection, reversal, closed shifts, stroke/component assignments, masks/fragments; exhaustive enumeration or valid pruning proof |
| Symmetry reduction | Prove objective/observable invariance; distinguish universal roll from object stabilizers, SO(2) from O(2) |
| Independent reference | Analytic global proof, exact exhaustive oracle, certified intervals/branch bounds or complete deterministic error proof; same routine at tighter settings is not independent |
| Error budget | Observation, sampling/mesh, raster, arithmetic and optimization gap separately propagated; grid completeness needs coverage/regularity; no unjustified double counting |
| Ties | Canonical discrete order; continuous minimizer set/representative; exact versus interval-overlap near-ties; no target-appearance tie break |
| Failure | INVALID_INPUT versus missing metadata NOT_EVALUABLE versus feasible LOCAL_ONLY versus certified result; retain timeouts, messages, branch failures, bounds and last feasible state |
| Reproducibility | Signed source/config hashes, arithmetic/dependencies, ordering, random seed only if later authorized, full diagnostics |
| Runtime/fairness | Predeclared budget plus common accuracy/failure policy across candidates/controls/tiers; equal wall time does not prove equal accuracy |
| Discrepancy | Stop claimed qualification when independent bound/reference is violated; preserve evidence, sign amendment and independently QC before new validation; never retune on target results |

## Objective-family qualification ledger

| Family | Existing independent basis | Missing full-domain guarantee | Proposed current disposition |
|---|---|---|---|
| Fixed-correspondence similarity C1/C2 | S01/S02 analytic trigonometric reference for frozen examples | Prove all admitted scale/rotation domains and discrete choices; resolve zero-scale infimum/S10 floor; C2 interpolation error | General downstream guarantee NOT_ESTABLISHED |
| Support C3/C4 | S04/S06–S08 scalar exhaustive distances at fixed poses | Nonsmooth nearest-neighbor changes; certify alignment, not just point distances; bound sampling and all nuisance branches | P0A1_OPTIMIZATION_CERTIFICATION_DEFERRED |
| Graph C5 | S04–S07 supplied graph counts | Counting requires validity, not continuous solver; added assignment/matching needs complete combinatorial oracle | Counts admissible with observables; matching deferred |
| Raster C6 | S05 horizontal capsule coverage | Threshold/pixel discontinuities; interpolation, exact finite search or rigorous coverage needed | Certification deferred |
| Composite C7 | S06 arithmetic penalty relation | Joint objective/domain; sum of separate minima is only a lower bound and may be unattainable jointly | No primary composite or certificate |
| Physical shadow C8 | No historical geometry/optics oracle | First establish model/observations; then optical and full-domain optimization proofs | NOT_ESTABLISHED |
| Future finite cameras | Finite enumeration possible in principle | Enumerate every distinct direction and certify remaining continuous/discrete alignment; finite camera count alone insufficient | No direction sets executed or certificate supplied |
| Future continuous camera domain | Analytic/interval methods possible in principle | Complete charts, singularity handling, regularity and global lower bound; multistart is still LOCAL_ONLY absent proof | Certification deferred |

No runtime value, new optimizer, target tolerance or scientific score is selected. A separately signed target-free synthetic certification phase may be needed, with its own implementation freeze and independent QC before any scored targets.
