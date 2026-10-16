# D2 — Two conditional score designs

**PRE-INDEPENDENT-QC. No score selected for Hebrew.** All proposed contracts below are [TARGET-BLIND DESIGN CANDIDATE]; proved statements are marked [MATH DERIVATION]. Evidence aliases and exact pinned paths are defined in the main review. Neither contract changes P0A1's C1–C8 dispositions or P0A0 code.

## Shared mathematical and observation boundary

These candidates belong to L1, not L3. QO requires genuinely ordered open paths; QH requires finite unordered support. No target supplies either representation in this review. A formula's well-defined domain is not evidence that a chart can supply its inputs. Target use requires gates G1–G6 in the dependency map, especially pre-pixel rights/annotation and independent second-chart uncertainty. L2 ink and L4 supplied-graph diagnostics may be reported **separately** after their own gates; they are not hidden terms of either objective.

For a probability measure μ on a planar observation x, write

\[
c_\mu(x)=\int x\,d\mu,\quad
r_\mu(x)^2=\int\|x-c_\mu(x)\|^2d\mu,\quad
N_\mu x=(x-c_\mu(x))/r_\mu(x).
\]

Only finite moments and **strictly positive** r are admissible. This fixes translation and positive scale independently on each observation. It is not target-relative normalization followed by another free scale fit. Measures must transform covariantly; duplicate policy is part of the observation, not a numerical convenience. No negative scale is permitted. In 2D a negative scalar equals a positive scalar plus a proper half-turn, not a mirror; a determinant-negative transformation still requires explicit O(2) permission.

Primary designs use SO(2), Q(θ) with θ∈[0,2π). O(2) sensitivity uses Q(θ)M^ε, ε∈{0,1}, M=diag(1,−1), and is a different registered estimand. No reflection is silently admitted. Exact ties use the direction order in D3, then ε=0 before 1, then unreversed before reversed. Intervals overlapping within unresolved arithmetic error are near-ties, not proved equalities.

## QO — Normalized ordered open-path arclength distance

### Complete domain and objective

[TARGET-BLIND DESIGN CANDIDATE] Input is two independently specified nonconstant open polygonal paths a and b, each with finite ordered vertices, finite real coordinates, positive total arclength, supplied endpoints/traversal and piecewise-linear interpolation. The primary contract is **one path on each side**, no stroke assignment. Repeated consecutive vertices describe zero-length segments and may be omitted without changing the continuous parametrized path; nonconsecutive returns and retracing remain. Supplied duplicate events with semantic meaning require a different representation, not this omission rule. Projected zero-length segments are explicitly retained as provenance events but consume zero arclength; total collapse is NOT_EVALUABLE. A malformed claimed graph is not repaired into a path.

Let a(u), b(u), u∈[0,1], be their normalized **planar arclength** parametrizations, including both endpoints. Set μ=du, A=N_du a, B=N_du b. This weights traversed arclength, including multiplicity of retracing; it does not weight vertex count, components equally or 3D arclength before projection. For D={id} primarily, or D={id,ρ} with ρ(u)=1−u only after a separately justified reversal permission, define

\[
q_O(a,b;D)=\min_{\tau\in D}\min_{\theta\in[0,2\pi)}
\left(\int_0^1\|Q(\theta)A(\tau(u))-B(u)\|^2du\right)^{1/2}.
\]

Direction is lower-is-closer; units are dimensionless. The declared continuum refers to the *supplied polyline interpolation*, not an unknown smooth original. For a 3D polyline X, define a_n=P R_n X with interpolation, and

\[
E_{O,F,k}(X,b)=\inf_{n\in G^F_k}q_O(a_n,b;D).
\]

This full-domain functional is evaluable only if every admitted view has its required normalization and bounds. A collapsed view is logged and blocks a complete minimum claim under this contract; it is not silently deleted or given zero. A separately frozen common degeneracy-domain rule may be designed later. For valid finite G and the compact roll circle and finite D, continuity gives attainment. No continuous camera guarantee follows.

### Analytic roll elimination and exact claim scope

[MATH DERIVATION] For each τ let

\[
\alpha=\int B\cdot A\circ\tau\,du,\qquad
\beta=\int B\cdot J(A\circ\tau)\,du,\quad
J(x,y)=(-y,x).
\]

Both normalized paths have squared L² norm one. The squared residual is 2−2(α cosθ+β sinθ). Cauchy–Schwarz bounds √(α²+β²)≤1, and the maximum correlation over θ is √(α²+β²). Thus each branch has exact mathematical minimum

\[
q_{O,\tau}=\sqrt{2-2\sqrt{\alpha^2+\beta^2}}.
\]

If α=β=0, every roll is tied; canonical representative θ=0. Otherwise θ=atan2(β,α) modulo 2π is the unique roll modulo a full turn. A tiny computed negative radicand must be enclosed/diagnosed, not blindly clipped as a perfect match. This is a theorem about exact inputs, **not a numerical implementation certificate**. Piecewise-linear normalized-arclength paths allow integration of piecewise quadratic products by splitting at the union of both breakpoint sets; no quadrature count is selected here. Reversal changes the breakpoints but remains finite. With algebraic vertices and exact algebraic frames, these operations have an algebraic reference route independent of a future floating solver.

The score is symmetric in a and b: invert Q and τ; reversal commutes with rotations and preserves du. It lies in [0,√2] under SO(2) (possibly smaller with permitted reversal/O(2)). L² distance is a metric on functions modulo equality almost everywhere. A compact group acting isometrically gives a metric on its orbits: zero infimum is attained, implies orbit equality; triangle inequality follows by composing the two minimizing isometries. Hence qO is a metric on normalized open-path rotation/reversal equivalence classes and a pseudometric on raw paths differing by permitted positive similarity or duplicate segmentation. This does not confer a metric on unlabeled glyphs, graphs or differently traversed supports. The projected object-to-target minimum E is directional and generally not a metric on 3D objects versus 2D targets.

### Discretization and reference obligations

[TARGET-BLIND DESIGN CANDIDATE] Prefer the exact continuous-polyline definition for specification; later implement interval-enclosed polynomial integration against an independently derived algebraic-integral oracle. If finite quadrature is used, nodes, weights, endpoint handling and a proved integral/residual error bound are separate frozen decisions; the sample-weighted approximation is not automatically the same metric. For unknown smooth curves, chord/interpolation and arclength-reparametrization stability must be certified independently. A Hausdorff cover alone does not bound order or arclength mismatch. S03's straight segment supports no general curved-path invariance.

Open cyclic shifts, arbitrary reparametrization, trimming, crop/masks, component deletion, stroke permutations, joining and warping are **not in QO's domain**. A closed-path variant would need a circle parameter and an explicitly continuous phase or justified finite phase domain, duplicate-endpoint policy and separate certification. It is deferred, not a closed-shift shortcut imported from S09. Multi-stroke input is NOT_EVALUABLE for QO until independently supplied pairing, weighting and all assignment freedoms have a new contract.

## QH — Normalized finite-support Hausdorff distance

### Complete domain and objective

[TARGET-BLIND DESIGN CANDIDATE] A and B are nonempty finite sets of distinct planar points, each with positive empirical RMS extent. The observation is **exactly the supplied set**, not a point multiset, stroke graph or continuous curve. Exact duplicates collapse as set identity; near-duplicates are not merged. A declared sampling operation must record duplicates before collapse. Use uniform probability mass on each distinct point separately: μ_A({a})=1/|A| and μ_B({b})=1/|B|. Independent centering/RMS yields Â and B̂. Counts need not match, and no correspondence is invented. Define

\[
d_H(U,V)=\max\{\max_{u\in U}\min_{v\in V}\|u-v\|,
                       \max_{v\in V}\min_{u\in U}\|v-u\|\},
\qquad
q_H(A,B)=\min_{\theta\in[0,2\pi)}d_H(Q(\theta)\widehat A,\widehat B).
\]

O(2) is separately defined by minimizing additionally over ε∈{0,1}. The primary qH is symmetric and dimensionless, lower-is-closer. It is ≥0 and finite for each valid input. There is **no universal size-independent finite upper range claimed** under this empirical RMS normalization; a sparse distant point can have large radius as cardinality grows. A valid instance bound is max_a‖â‖+max_b‖b̂‖. Continuity over compact SO(2) gives attainment.

[MATH DERIVATION] Hausdorff distance is a metric on nonempty compact subsets. Rotation acts isometrically, and compactness gives attainment, so qH is a metric on the rotation orbits of normalized finite sets; on raw finite sets it is a pseudometric modulo positive similarity. This proof does not apply to mean Chamfer, which is not proposed as a third certified metric. Distinct sampling of the same underlying curve may yield different qH: no sampling invariance is claimed. Labels, multiplicity and stroke incidence are absent by design; zero qH cannot establish them (S04).

For a 3D object, the sampling rule must be common across objects and views and fixed before target access. One conditional finite observation is the set of projections of a supplied finite vertex observation (not adaptive resampling selected for good matches). Write A_n={P R_n x_i}; exact coincident points become one point under the declared set rule. The cardinality and empirical normalizer can change at coincidences; no uniform camera continuity is assumed. Define E_H,F,k(X,B)=inf_{n∈G^F_k}qH(A_n,B), requiring every view valid as for QO. An alternative arclength or component-weighted support is a different, deferred normalizer, not silently substituted.

### Independent reference and approximation obligations

[TARGET-BLIND DESIGN CANDIDATE] At a fixed pose an independent reference performs explicit scalar all-pairs distances and both directed extrema, preferably with exact/algebraic or outward-rounded interval arithmetic; it must not call the production nearest-neighbor routine. Finite cameras do not remove continuous θ. D4 supplies a prospective full-circle lower/upper bound construction. Sampling source/target curves is a different error problem.

[MATH DERIVATION] If U_s,V_s are certified approximations to *already normalized* compact U,V, with Hausdorff covers δ_U,δ_V, then |dH(U,V)−dH(U_s,V_s)|≤δ_U+δ_V. The bound remains uniform under common isometric rotation and therefore bounds optimized values on a common domain. Raw covers alone do **not** control empirical centroid/RMS changes: a separately justified measure convergence/coupling and positive extent lower bound are needed. Tiny components cannot be silently omitted. Nearest-neighbor correctness on observed points does not certify unseen parts of a curve.

Order reversal and cyclic shift are not QH search variables: order is already discarded. Permuting point indices adds no capacity. Graph/stroke matching is absent, not solved. Cropping, masking, trimming, noise removal, morphology and smoothing are excluded. Outliers and tiny components remain. If the supplied support is itself incomplete, the result must retain that observation limitation rather than call it a full-shape score.

## Strictly positive scale versus the inherited fit

[FROZEN RESULT] P1 `symmetry_and_capacity_ledger.md`, M3, records inherited nonnegative scale and S10's tiny-energy rejection. Neither is changed.

[MATH DERIVATION] For centered genuinely corresponding arrays/functions x,y under fixed measure, let A=‖x‖²>0, B=‖y‖², c(Q)=⟨Qx,y⟩. The unnormalized squared fit is B+A s²−2s c(Q), s>0. For c(Q)>0 the optimum s=c(Q)/A is positive. For c(Q)≤0 the infimum B occurs as s↓0 and is not attained (when c=0 and A>0 it is still strictly greater than B for any s>0). After optimizing Q the same distinction uses max_Q c(Q). A compact free SO(2) makes this maximum nonnegative, but it can be zero. Adding s=0 changes the domain and destroys invertibility; choosing s_min>0 changes the estimand and requires independent justification. No negative scale or reflection repairs this boundary.

QO and QH avoid this residual fit by fixing both positive RMS scales, conditional on r>0. They deliberately **change the proposed normalization**, not repair the inherited algorithm or assert equivalence to inherited target-relative residuals. A singular/uncertain r is NOT_EVALUABLE. No tiny cutoff is chosen now. The numerical ledger supplies the needed error propagation and status distinctions.

## Separate diagnostics, not an undisclosed composite

[TARGET-BLIND DESIGN CANDIDATE] With independently supplied valid R2-G, report component/end/junction/stroke counts and discrepancies as a separate vector, retaining IDs and uncertainty; counts are not isomorphism. With a later frozen L2 renderer and compatible observation, one may separately report area-coverage discrepancy or a fully specified mask IoU distance. Neither raster score nor graph matching is specified for implementation by this review. Empty unions, width/grid dependence and threshold ambiguity require their own protocol. No combined objective or weighting vector is selected; especially no P0A0 1/4 weight. Missing diagnostics remain missing, not zero or omitted by renormalizing weights. If future composite terms share a pose, minimize their **joint** objective; a sum of independent minima is at best a lower bound, generally not a feasible joint score.

## Counterexamples and later selection rule

| Frozen case | Constraint retained by both candidates |
|---|---|
| J S03 | QO needs justified traversal and polyline semantics; QH's empirical normalizer remains density-sensitive. Neither generalizes one straight-segment oracle to every curve. |
| J S04 | Equal support cannot recover labels. QO order and L4 labels need independent authority. |
| J S05 | L2 raster score zero cannot certify a gap absent; no grid or width imported. |
| J S06 | Small shape error does not certify component agreement; separate graph diagnostics, no 1/4 default. |
| J S07 | Hausdorff mismatch is not an endpoint count. Tiny spurs remain geometrically and observationally distinct. |
| J S08 | Normalization and threshold alter the question; no inherited .01/.05 threshold adopted. |
| J S09 | Reversal explicit; no open cyclic shift; closed/multi-stroke extension deferred. |
| J S10 | Zero/tiny unsupported scale is not perfect match; no patch to inherited floor or tiny-edge deletion. |
| J S11–S12 | Whole-domain certificate still required; six signed G0 views are not twelve independent trials. |

[UNRESOLVED] Select no final score, normalization variant, reflection/reversal permission, target tolerance, width, grid, threshold, primary statistic, term weight or sample count here. A future signed decision must first establish observables from permitted metadata/independent annotation planning, then choose by measurement semantics, dimensional consistency, analytic stability and a separately authorized *new* target-free certification record. Choices must be frozen before target pixels/performance. If order cannot be independently justified, QO cannot become a glyph method; QH may remain a finite-support diagnostic but is not promoted to topology. No empirical preference between QO/QH or families A/B is asserted.

Future validation plans and proof IDs O1–O5/H1–H5 are in the numerical ledger. No implementation, scientific fixture generation, objective evaluation or solver execution was performed.
