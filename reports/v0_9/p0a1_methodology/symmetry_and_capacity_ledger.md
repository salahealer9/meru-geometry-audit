# M3 and M5 — Symmetry and effective viewing capacity

**PRE-QC / NOT FROZEN.** Reconstituted from the completed pre-interruption review; no new mathematical experiment or decision. Narrative proposals do not authorize target processing. Frozen case evidence: `reports/v0_9/p0a0_registered_execution/p0a0_registered_pilot_once.jsonl` (J below). Implementation semantics: `docs/v0_9/p0a0_implementation_specification.md`, “Implementation and representation contracts” (S below).

## M3: action, quotient and observable contract

[MATH DERIVATION] With column vectors, the orientation-preserving planar similarity group is

\[
\operatorname{Sim}^+(2)=\mathbb R^2\rtimes(\mathbb R_{>0}\times SO(2)),\qquad (t,s,Q)x=t+sQx.
\]

Composition is \((t_1,s_1,Q_1)(t_2,s_2,Q_2)=(t_1+s_1Q_1t_2,s_1s_2,Q_1Q_2)\). Given a registered subgroup H acting on all retained observables, define A∼H B precisely when B=h·A for some h∈H. This is an equivalence relation; an optimized discrepancy need not be a metric on it. Source-to-target scaling/target-relative RMS can be asymmetric, and empirical Chamfer need not satisfy the triangle inequality. The inherited code uses row-vector transforms; conventions must be translated explicitly.

Similarity fitting removes declared nuisance variation. Forgetting depth, ordering, labels or subpixel information is many-to-one information loss, not an invertible group action. A transformation that lowers a score without preserving required observables is not automatically a permitted nuisance.

[METHODOLOGICAL PROPOSAL] Use a fixed, reproducible weighted-centroid rule with observation-based weights. Permit s>0 only if scale is observationally irrelevant. Zero scale collapses information and is not invertible. A negative scalar in two dimensions is redundant with a proper half-turn; it does not authorize a determinant-negative mirror. State the scale and determinant permissions independently.

[FROZEN RESULT] J S02: SO(2) relative RMS 0.5579760990825915 versus O(2) 1.8595793102131748e-16. Reflection changes the equivalence relation. SO(2) remains the proposed primary orientation convention; O(2) is a separately signed sensitivity, or a source-justified explicitly registered observation rule, never an undisclosed default or “extra views”.

| Representation | Proposed allowable actions, contingent on signed observation model | Preserved distinctions and capacity record |
|---|---|---|
| R3-C | SO(3) camera before orthographic projection; optional justified world translation/positive scale, distinct from planar fit | No bending, deletion or relabeling. Record camera domain, independent curve order and projected collapse. |
| R3-S | Rigid scene/camera changes only with light/receiver/material conventions | Fixed illumination can break roll symmetry. Thickness is geometry; a physical scale change must transform all relevant units coherently. No n-only quotient without proof. |
| R2-O | Planar permitted similarity; open reversal C2 only when observationally irrelevant; genuinely closed n-sample shifts Cn, or Dn if reversal allowed | No cyclic shift of an open curve, truncation, piece deletion, joining or preferred fragments. Closed endpoint duplication changes sampling measure. Stroke assignment is separate. |
| R2-U | Similarity on points with covariant fixed weights | Point ordering is already lost, so no artificial n! capacity for set index permutations. Component removal, densification or altered weights remain new methods. |
| R2-G | Similarity on coordinates preserving incidence/labels; explicitly allowed graph isomorphisms or stroke permutations | Coincident IDs remain distinct. For k exchangeable strokes k! is a pre-restriction assignment upper bound, not free hidden matching. Masks and partial assignments add further capacity. |
| R2-I | Transform declared continuous ink then rasterize, or declare one fixed pixel interpolation operator | Repeated interpolation loses information; continuous pixel rotation is not generally an exact group action. Record width-scale rule, crop, renderer and operation order. |
| R2-H | UNRESOLVED until optical/observation law proves allowed motions | No arbitrary drawing warps, camera reflection or front/back equivalence inferred from point projection. Scene and drawing uncertainties need their own contract. |

[FROZEN RESULT] J S09: reversal-denied relative RMS 0.997510873195539; reversal-allowed 2.9207593438878524e-16; closed shift 1.305986786265766e-16; open shift comparison 0.462422981170379. These support discrete permissions on the supplied paths, not arbitrary reparameterization or unlabeled stroke matching.

[METHODOLOGICAL PROPOSAL] For each representation with an optimization domain, use a source-independent canonical order: camera ID, reflection flag, stroke-permutation ID, traversal flag, closed shift. S preserves P0A0's first strict minimizer, unreversed before reversed and ascending shifts; its analytic angle oracle selects the smallest angle in [0,2π). Do not retrofit those records. Future continuous exact ties require a specified canonical domain and representative rule; overlapping numerical objective intervals are unresolved near-ties, not exact equivalence or grounds to choose a visually preferable match. Report tied classes and the selected representative.

[UNRESOLVED/REQUIRES LATER GATE] S allows inherited nonnegative scale, including zero-scale nonmatches; the future proposal is strictly positive. No code is changed. An s>0 optimization may have an unattained infimum at s→0. A future gate must prove positive attainment, preregister a justified positive bound, or return explicit NOT_EVALUABLE/unattained-infimum status. A bounded scale domain is not itself the similarity group. No scale interval or threshold is chosen here.

## M5: universal camera quotient proof

[MATH DERIVATION] Let P(x,y,z)=(x,y), R∈SO(3), and n=Rᵀe_z. If Sᵀe_z=Rᵀe_z, then A=SRᵀ fixes e_z. Because A is proper orthogonal, A=diag(Q,1) with Q∈SO(2). Consequently PSX=QPRX. Free planar SO(2) absorbs axial roll exactly. Conversely that left multiplication leaves n fixed. Thus SO(2)\SO(3) is the signed direction sphere S² for orthographic point projection with compatible retained observables.

If Sᵀe_z=−Rᵀe_z, then A=SRᵀ has block form diag(B,−1); det A=1 forces det B=−1. Opposite point-projection directions differ universally by a planar reflection, not a proper rotation. They collapse under the explicitly selected O(2) quotient, yielding S²/(n∼−n), the real projective plane. Some objects have additional proper symmetries connecting opposite views; these are object-specific stabilizers, not universal equivalences. These proofs do not establish the same quotient for perspective, material or illumination/occlusion-sensitive physical shadows.

[FROZEN RESULT] `docs/geometry/projection_orbit_results_v0_5.md`, “Exact camera-direction orbit” and “Exact class structure”, provides:

| Signed direction | Frozen frames | Unoriented axis |
|---|---|---|
| +z | R01, R12 | z |
| +y | R02, R11 | y |
| +x | R03, R10 | x |
| −z | R04, R09 | z |
| −x | R05, R08 | x |
| −y | R06, R07 | y |

J S12 preserves six signed classes, three axes, and opposite-frame planar determinant −1. Two frames per signed class account for the twelve proper tetrahedral frames. G0 therefore has six signed physical directions under free SO(2); three axes only under the separate O(2) quotient. Duplicate frames and axial rolls add no effective capacity. No frame was recomputed. The v0.5 “Object-specific projection classes” table uses declared curve semantics and an empirical threshold; those object counts are not exact universal quotient counts and were not re-evaluated here.

## Future reproducible G0 ⊆ G1 ⊆ G2 rule — no angles/sets chosen

[METHODOLOGICAL PROPOSAL]

1. Freeze the physical forward model, planar group and all other nuisance allowances first. Retain the six signed G0 anchors for SO(2). An O(2) sensitivity needs its own consistently quotiented hierarchy.
2. Later choose a target-independent deterministic direction-refinement family, named algorithm/version, coordinate frame, precision and canonical ordering. Preserve all old representatives and include G0 exactly. Freeze its generator hash and refinement indices before pixels. No generator is chosen or called here.
3. Define angular covering radius δ: every direction in the registered domain must be within δ of a representative. Also specify separation, exact-duplicate rules and justified precision handling. Signed angular distance uses arccos(n·m); the O(2) sensitivity uses arccos(|n·m|). A clustering tolerance is not a substitute for proof of equivalence.
4. Select future tiers using a predeclared target-free coverage/resolution justification. Prove nesting and strict quotient-distinct enlargement wherever claimed. Publish literal direction tables, count, canonical frame lifts and coverage/separation certificates. Actual G1/G2 levels, angles/counts, δ, arithmetic and algorithm remain UNRESOLVED.
5. A continuous domain needs a complete certified optimization/discretization policy. If a uniform angular Lipschitz bound L for the full objective is justified, a δ-net bounds finite-minimum versus continuous-infimum error by Lδ, plus other errors. This conditional proof supplies neither L nor δ here. Occlusion, thresholding and singular normalizations may defeat convenient regularity assumptions.
6. Report nominal frames, universal quotient count, coverage, planar group, translation/scale, stroke/traversal/fragmentation freedoms and solver status separately. Additional object-specific equivalences need independent proof/certification; do not infer them from favorable target matches or delete views adaptively.
7. Candidates and every N0–N3 control share directions, physical model, metric, sampling/normalization, discrete allowances, solver accuracy, stopping/failure rules and declared computational budget at each tier. Equal timeout alone does not guarantee equal accuracy. Any source-constrained versus common-capacity contrast must be a separate preregistered analysis.

## Minimum monotonicity and specificity

[MATH DERIVATION] For fixed object X, target T and objective E, let D_i include the entire camera and nuisance search domain. If D_0⊆D_1⊆D_2 and minima are attained, then

\[
\min_{d\in D_2}E(X,T;d)\le\min_{d\in D_1}E(X,T;d)\le\min_{d\in D_0}E(X,T;d).
\]

Each smaller-domain feasible point is also feasible in the larger domain, proving the inequality. Use infima when attainment is unproved; compactness/continuity or another attainment argument is needed before claiming a minimum. Strict extra capacity need not strictly improve a given optimum. Local numerical outputs need not obey the inequality; carrying an old incumbent forward only enforces nonworsening feasible upper bounds, not global certification.

Changing metric, resolution, normalization, weights, reflection, stroke permissions, physical model or exclusion policy breaks the fixed-objective/nested-domain comparison. A smaller minimum is a deterministic multiple-opportunity effect available to controls too; it proves no specificity. Later candidate-versus-null behavior and candidate×capacity interaction, under matched domains, remain separate scientific questions.
