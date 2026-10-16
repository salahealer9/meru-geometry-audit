# D3 — Two exact capacity-family proposals

**PRE-INDEPENDENT-QC. Symbolic definitions and proofs only; no direction enumerator, grid, rendering or measurement was executed.** Counts are combinatorial derivations, not numerical results. Both families are [TARGET-BLIND DESIGN CANDIDATE], not final G1/G2, historical Meru prescriptions or tested optima. Applicable only to compatible orthographic L1 observations with free planar SO(2). L3 requires a separate optical equivariance proof.

## Universal quotient and frozen G0

[MATH DERIVATION] Let P(x,y,z)=(x,y), R∈SO(3), n=Rᵀe_z. If Sᵀe_z=Rᵀe_z, then A=SRᵀ fixes e_z. Orthogonality and det A=1 force A=diag(Q,1) with Q∈SO(2), hence PSX=QPRX. Conversely left multiplication by diag(Q,1) preserves n. The fibers are precisely SO(2) left cosets and SO(2)\SO(3)≅S². Axial roll is absorbed by planar roll for equivariant observables and normalizers.

If Sᵀe_z=−Rᵀe_z, A=diag(B,−1) with det B=−1. Opposite directions therefore differ universally by a planar reflection, not a proper rotation. The separately permitted O(2) quotient gives S²/(n∼−n)=RP². Object-specific symmetries may identify more observations but cannot change the universal quotient or justify target-conditioned view deletion. Fixed off-axis illumination/receiver geometry can invalidate this argument for physical shadows.

[FROZEN RESULT] V5, “Exact camera-direction orbit” / “Exact class structure”, and J S12 establish twelve proper tetrahedral frames but six signed directions G0={±e_x,±e_y,±e_z}. Frame classes are +z:{R01,R12}, +y:{R02,R11}, +x:{R03,R10}, −z:{R04,R09}, −x:{R05,R08}, −y:{R06,R07}. O(2) permits three axes. V5's empirical object-specific projection counts are distinct historical results, not universal identities; nothing was rerun.

## Exact symbolic membership

Use integer representative triples v and normalize by ‖v‖₂ **symbolically**. Define

\[
A_0=\{\pm e_x,\pm e_y,\pm e_z\},\qquad
C=\{(s_1,s_2,s_3)/\sqrt3:s_i\in\{-1,1\}\},
\]
\[
E=\{v/\sqrt2:v\text{ has one zero coordinate and the other two are independently }\pm1\},
\]
\[
T=\{v/\sqrt5:v\text{ has one zero coordinate; the other two have absolute values }2,1
\text{ in either order, with independent signs}\}.
\]

These set-builder definitions specify every exact coordinate; no numeric direction table or tolerance clustering is substituted.

| Family | G0 | G1 | G2 | Signed counts | O(2) axis counts |
|---|---|---|---|---|---|
| A: axes/corners/edges | A0 | A0∪C | A0∪C∪E | 6, 14, 26 | 3, 7, 13 |
| B: axes/edges/ratio-two | A0 | A0∪E | A0∪E∪T | 6, 18, 42 | 3, 9, 21 |

[MATH DERIVATION] A0 has 3 positions ×2 signs=6. C has 2³=8. E has 3 zero positions ×2² signs=12; swapping equal absolute nonzero entries creates no extra vector. T has 3 zero positions ×2 assignments of unequal magnitudes ×2² signs=24. Sign and absolute coordinate pattern can be recovered from the normalized vector, so these primitive integer triples are not positively proportional. The four strata have respectively two zeros, no zeros, one zero with equal absolute nonzeros, and one zero with nonzero ratio two: they are pairwise disjoint. Each added stratum is nonempty, proving G0⊊G1⊊G2. Every set is antipodally closed without fixed points, so O(2) counts halve exactly. This proves membership/nesting/counts, **not covering radii**.

Families differ genuinely: B1 has edges instead of corners and B2 has no fully nonzero triple, whereas A includes corners and no T. Different tier cardinalities rule out mere rotated relabeling. Both impose cubic sign/permutation symmetry, a design bias rather than historical evidence. A includes octant interiors; B spends more directions in coordinate planes and may leave weaker interior coverage. This is a structural critique, not a comparative covering theorem. B's larger counts increase certification cost. Final choice requires a priori certified geometry and tractability, never target performance.

## Canonical order, antipodes and precision

[TARGET-BLIND DESIGN CANDIDATE] Append-only stratum order: A0 then C then E for A; A0 then E then T for B. Within each stratum sort its **integer triples** lexicographically in x,y,z with ordinary integer order. Thus G0 has the same order in both. Pair v with −v exactly. For O(2), select the representative with first nonzero coordinate positive, preserving stratum/lexicographic order. An O(2) score must still include both planar determinant components: reducing cameras must not discard the reflection branch. Under the proved antipodal equivariance, all signed views with SO(2) offer the same object-to-target opportunity as axis representatives with O(2). Fixed-observation qO/qH still have different SO(2)/O(2) definitions.

Coordinates stay exact algebraic expressions. Later implementation must freeze conversion/precision with outward enclosures and certify unit-length, dot-product and orientation errors. No decimal merge tolerance or bit precision is selected now. Precision must follow analytic input bounds and an error budget, not targets. Exact intended ties remain ties; interval overlap means unresolved near-tie.

## Deterministic proper frame lift and seams

[MATH DERIVATION] Choose j∈{x,y,z} minimizing |n_j|, ties x then y then z. Set a=e_j and

\[
u=\frac{a-(a\cdot n)n}{\sqrt{1-(a\cdot n)^2}},\qquad v=n\times u,\qquad
R_n=\begin{pmatrix}u^T\\v^T\\n^T\end{pmatrix}.
\]

The minimum |n_j|≤1/√3, so the denominator is ≥√(2/3)>0. The rows are orthonormal and u×v=n, hence det R_n=+1 and R_nᵀe_z=n. The lift has seams at equal |n_j|; the exact tie rule fixes a unique representative. Limiting frames at a seam differ by planar roll. Continuity claims concern the **optimized SO(2)-invariant objective**, not raw lifted coordinates. No globally continuous frame field is assumed. At −n the same j and u are chosen and v changes sign, so P R_−n=diag(1,−1)P R_n exactly.

[TARGET-BLIND DESIGN CANDIDATE] Rounded frames must certify errors or use independently bounded reconstruction, not merely a floating determinant check. Exact order, signs, matrix column-vector convention, object axes and seam behavior must be frozen later. No lift has been evaluated in this phase.

## Separation and covering certificate plans — values NOT_ESTABLISHED

[TARGET-BLIND DESIGN CANDIDATE] For each family/tier define signed separation σ=min_{n≠m} arccos(n·m) and covering radius δ=max_{x∈S²}min_n arccos(x·n). For O(2) use arccos(|n·m|) on distinct axes and projective coverage. Exact finite distinctness proves σ>0, but no numerical value of σ or δ is asserted.

1. **SEP:** classify all pair orbits under signed coordinate permutations, prove completeness/multiplicity, compare exact algebraic dots and identify their maximum. Independent verification uses a complete literal pair table, not the production symmetry shortcut. Any arccos enclosure comes after exact dot ordering; antipodal duplicates are excluded for axes.
2. **COV:** construct spherical Voronoi cells V_i={x∈S²:x·n_i≥x·n_j for every j}; prove their hemispheres cover the sphere. Minimize x·n_i over each closed cell using complete active-set/critical-point analysis including vertices, arcs, interiors, degeneracies and ties, not just apparent vertices. Compare exact extrema or verified interval enclosures with exhaustive domain coverage. The independent route uses a different construction or complete interval subdivision. For antipodally closed sets, sphere coverage equals projective coverage with absolute dots.
3. **ROUND:** relate exact frames/directions to represented intervals and bound resulting angular/objective error. A norm tolerance is not a score bound.

No pair table, Voronoi solver or interval search was run. Values, final tiers and arithmetic precision are **NOT_ESTABLISHED**; CAP1–CAP5 remain explicit proof obligations in the numerical ledger.

## Fixed-domain infima and coverage caution

[MATH DERIVATION] For fixed X,T, objective E and nuisance domain H, D_k=G_k×H are nested, so inf_D2 E≤inf_D1 E≤inf_D0 E. Every smaller-domain feasible point stays feasible. Minima require defined observations and attainment, proved for valid finite QO/QH camera domains with compact roll and finite branches. Strict enlargement need not improve a given score. Local outputs may violate monotonicity; keeping an incumbent only ensures nonworsening feasible **upper bounds**. Changes in normalization, renderer, permissions or degenerate-view deletion break the fixed-domain comparison. Lower error is more opportunity, **not specificity**.

An optional continuous-camera extension is not selected. Cover S² by the closed minimum-coordinate patches above, including overlaps/seams. Use geodesic distance, not chart step sizes. Prove uniform positive projected extent and a bound |f(n)−f(m)|≤L d(n,m) for the complete f(n)=inf_h E(n,h). A sufficient hypothesis is a common nuisance domain and a uniform Lipschitz bound for E(·,h) for every h; infima preserve it. If G is a certified δ-net of that same domain,

\[
0\le\inf_{n\in G} f(n)-\inf_{n\in D}f(n)\le L\delta.
\]

Proof: take an ε-optimal n, a grid point within δ, apply the bound, then ε↓0. Neither L nor δ nor an admissible nondegenerate continuous domain is proved here. QO reparametrization at collapsed segments and QH empirical-mass changes at coincidences need special treatment; threshold rasters/occlusion can be discontinuous. Both families therefore have **COVERAGE_ERROR_UNCERTIFIED** for continuous-sphere claims.

## Common nuisance and object symmetry obligations

[TARGET-BLIND DESIGN CANDIDATE] Both families use the same QO/QH contracts, without adaptive directions, crop, deformation, hidden mirrors, extra matching or relaxed accuracy. Every candidate and N0–N3 control shares the family/tier, objective and failure rule. Additional object symmetries require independent proof, not favorable target matches. Cardinalities are not independent-trial counts or p-value corrections. See capacity_and_nuisance_budget.csv.
