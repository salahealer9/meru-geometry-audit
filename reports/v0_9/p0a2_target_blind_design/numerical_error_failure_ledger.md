# D2/D4 — Numerical error, failure and certification ledger

**PRE-INDEPENDENT-QC. No scientific implementation or execution.** D2 contracts supply objectives; D3 supplies exact finite domains. D4 develops prospective whole-domain certification below. Every numerical tolerance/value not explicitly inherited as a frozen result is **NOT_ESTABLISHED**. Proof obligations are not completed software certificates.

## Certification states and scope

| Status | Required evidence | Current P0A2 meaning |
|---|---|---|
| GLOBAL_CERTIFIED | Exact mathematical full-domain proof/exhaustion with verified arithmetic semantics and valid observations | No solver receives this status. Exact symbolic subtheorems in D2/D3 are narrower. |
| BOUNDED_APPROXIMATION | Feasible upper bound U; independent global lower bound L over every admitted branch; U−L≤ε for frozen ε; separate observation/discretization uncertainty | Proposed evidence contract only; no U/L/ε was evaluated. |
| LOCAL_ONLY | Valid feasible objective and documented searched domain; no completeness guarantee | Could be retained after a future timeout/local search, never mislabeled a global minimum. |
| GLOBAL_CERTIFICATION_DEFERRED | Required full-domain/representation/arithmetic certificate not established | Current status of all four QO/QH × A/B solver combinations. |
| INVALID_INPUT | Malformed dimensions, nonfinite data, invalid graph IDs, illegal uncertainty or encoding | No numeric score; exact error field retained. |
| NOT_EVALUABLE | Missing observables, empty/zero extent, unsupported tiny scale, unachieved minimum, unavailable uncertainty needed for claim | No perfect-match substitute; distinguish from a legitimate finite degraded fit. |

[FROZEN RESULT] J S11: success true, local value 0.4 versus analytic global 0; P1 optimizer_certification_requirements.md, opening paragraph and “Status contract”. The frozen case is EXPECTED_BLIND_SPOT, not repaired, widened or replayed. Multistart, a dense heuristic grid and success=True cannot establish completeness.

## D4 common full-domain architecture

[TARGET-BLIND DESIGN CANDIDATE] For family F∈{A,B} and tier k∈{0,1,2}, QO searches G^F_k × SO(2) × D, D={id} primarily; optional independently justified D={id,ρ}. QH searches G^F_k × SO(2). The optional O(2) sensitivity instead uses axis representatives × SO(2) × {0,1} (and D for QO), not an unreported doubled opportunity. All directions must be normalized and valid. No shape parameters, continuous camera search, residual translation/scale, crop, mask, stroke assignments or closed shifts are included. Translation and strictly positive scale are fixed by the two independent normalizers, under the D2 assumptions. A later raw-scale-fit extension must prove attainment or return an explicit unattained-infimum result.

Finite camera enumeration is necessary but not sufficient: every remaining roll/discrete branch and all numerical error must be covered. Independent reference code, when separately authorized, must not call production alignment, sampling, nearest-neighbor, rendering or normalization helpers that it purports to verify. Shared mathematical input definitions are necessary; shared computational bugs are not an independent oracle. Freeze both source/config hashes and review the dependency graphs.

### QO × A and QO × B: analytic integral route

[MATH DERIVATION] For valid finite polylines, the D2 α/β formula solves roll exactly on each traversal branch. Normalized-arclength breakpoints partition [0,1]; both paths are affine on each common interval. Centroids, squared norms and cross-correlations are integrals of degree ≤2 polynomials. An exact algebraic calculation is possible for algebraic vertices and algebraic frames, including square roots of segment lengths; no sampled-angle optimizer is required by the mathematical definition. Exhausting all finite directions and traversal branches then gives a full-domain exact reference **in principle**, provided comparison/equality of algebraic results and all degeneracies are proved decidable and implemented correctly.

[TARGET-BLIND DESIGN CANDIDATE] Production may use outward interval integration and enclose α,β,qO. A separate exact symbolic piecewise-integration oracle plus a separately derived trigonometric maximization proof verifies small, newly registered fixtures. General interval certificates must report all branch lower/upper bounds; global L=min branch lower, U=min feasible branch upper, with feasible witness and U−L≤ε before BOUNDED_APPROXIMATION. A symbolic minimized value is not an arithmetic certificate for an approximate witness. Cancellation near qO=0 and square-root conditioning must be bounded without silent clipping. Exact ties require equality proof, not rounded equality.

Let n,m be numbers of supplied source/target polyline segments, N=|G| and b the number of admitted discrete branches (1 primarily; 2 if reversal; an additional factor 2 for O(2) with N halved). Projection/length formation and merging sorted breakpoints require O(n+m) arithmetic operations per branch; integrated products likewise O(n+m). A proposed interval implementation therefore has O(Nb(n+m)) **field-operation** work per precision pass and O(n+m+Nb) memory retaining branch records. Exact algebraic bit complexity is NOT_ESTABLISHED; radical expression growth, equality tests and precision refinement can dominate. Let T_O(n,m,p) be the certified per-branch arithmetic cost at precision p and J the refinement passes: total ≤Nb∑_{j=1}^J T_O(n,m,p_j), with declared stopping/memory cap later. No universal finite J is claimed near unresolved ties or degeneracies.

### QH × A and QH × B: full-circle deterministic bound route

[MATH DERIVATION] For fixed normalized finite A,B, put ρ_A=max_a‖a‖. Rotating any a by geodesic angular difference Δ≤π moves it by 2‖a‖sin(Δ/2)≤ρ_AΔ. Thus

\[
|d_H(Q_\theta A,B)-d_H(Q_\phi A,B)|\le
d_H(Q_\theta A,Q_\phi A)\le\rho_A\,d_{S^1}(\theta,\phi).
\]

This bound holds for the complete fixed-view Hausdorff objective despite nearest-neighbor switches. It does not bound changing camera direction or normalization.

[TARGET-BLIND DESIGN CANDIDATE] Partition the entire roll circle into K closed cells covering boundaries and wrap-around, with centers θ_j and half-width at most h. Independently enclose each center value by [l_j,u_j], using all-pairs distance intervals. Every cell has lower bound L_j=max(0,l_j−ρ_A^upper h); a feasible center has upper bound U_j=u_j, provided rotation/witness error is included. Across all cells, directions and discrete mirror branches, L=min L_j and U=min U_j. Store every cell bound, branch ID and witness; no omitted cell. If u_j−l_j≤2η and h is common, U−L≤2η+ρ_max^upper h: at the cell attaining global L, global U is no larger than that cell's U. With ε>2η, K≥ceil(πρ_max^upper/(ε−2η)) is a sufficient symbolic uniform-cell condition. ε,η,K and ρ bounds are **not selected or evaluated here**.

An independent checker can validate coverage and certified Lipschitz bounds plus scalar all-pairs intervals without trusting the production search. For newly registered algebraic toy inputs, a second reference route may isolate critical distance/correspondence events with exact algebraic reasoning; it is optional until its completeness is proved. Using the production routine at tighter tolerance is not an oracle. Exact GLOBAL_CERTIFIED needs exact critical-event/exhaustion proof; the grid-bound route yields only an explicitly bounded approximation, not an exact global minimum.

For |A|=n, |B|=m, each center uses O(nm) pair-distance operations with streamed directed minima. With N cameras, b determinant branches and K cells per branch, work is O(NbKnm) interval arithmetic operations at fixed precision; memory O(n+m+NbK) retaining certificate records (or O(n+m) working memory plus a streamed immutable certificate). Bit cost is that operation count times certified precision cost; J refinements multiply via ∑ K_j C(p_j). K can be unbounded if no finite requested ε/extent/error hypothesis is available. Independent verification has comparable exhaustive certificate cost. Pairing equal wall time with unequal precision does not establish fair accuracy.

### Common ties, failures and discrepancy stop

Canonical order is family stratum/direction, mirror ε, traversal, then least angle in [0,2π) among **proved** exact minimizers. QO all-roll ties use angle zero. A mathematical minimizer on the circle has a canonical representative, but a QH numeric interval certificate need not isolate it: report all unresolved tied/near-tied cells and the canonical first **feasible witness**, not a falsely unique minimum. Preserve certificate intervals and discretization width. No visual tie-breaking.

On timeout keep complete logs, evaluated/unvisited domains, last feasible witness and bounds; return LOCAL_ONLY if feasible but the global gap is not established, or BOUNDED_APPROXIMATION only if the retained proof already meets ε. Missing branches cannot be silently discarded. If an independent exact reference falls outside a claimed enclosure, L>U, a branch is omitted, a degeneracy rule changes or a promised bound lacks proof: STOP the certification claim, retain every diagnostic, mark discrepancy, and require a separately signed amendment and independent QC **before further certification work**. P0A2 itself authorizes no attempt.

## Error decomposition and sufficient propagation rules

[TARGET-BLIND DESIGN CANDIDATE] Report independently identified terms:
ε_obs (source/acquisition/annotation), ε_samp (sampling/interpolation/measure), ε_mesh (surface approximation), ε_raster (coverage/discretization), ε_optics (physical-model discrepancy), ε_fp (arithmetic/normalization/frames), ε_opt (optimization gap). Do not add incompatible units or double-count a renderer error already in an interval oracle.

If all terms are bounds in the **same final dimensionless score**, with common domain and uniform perturbation control, a telescoping triangle argument gives total discrepancy ≤ their sum. This conditional algebra is not a numerical bound. Otherwise record each term and the missing propagation theorem separately; do not manufacture a total.

| Lane/term | Bound available in principle | Current status / key obstruction |
|---|---|---|
| QO observation | Coupled path/order/endpoint uncertainty bound | NOT_ESTABLISHED for targets; point-set cover cannot bound order. |
| QO sampling | L² error under the same normalized parameterization bounds residual via triangle inequality; exact integration avoids quadrature error for supplied polylines | Smooth-to-polyline and arclength-reparametrization bounds NOT_ESTABLISHED. |
| QH sampling | Certified covers of already normalized sets give δ_A+δ_B | Raw empirical-normalizer/measure convergence NOT_ESTABLISHED; every component required. |
| QO/QH normalization | Positive extent bound and coupled observation moments permit stability bound below | No numerical lower extent or target uncertainty selected. |
| L1 mesh/raster/optics | Not part of QO/QH observation definition | NOT_APPLICABLE, not evidence of zero physical-model error. |
| L2 raster | Coverage enclosure and fixed width/viewport/threshold law | NOT_ESTABLISHED; threshold may defeat Lipschitz stability; no renderer selected. |
| L3 mesh/optics | Authenticated geometry and independently bounded full forward model | NOT_ESTABLISHED; historical geometry/scene missing. |
| Arithmetic | Outward interval operations and independent reference validation | NOT_ESTABLISHED; binary64 inherited checks are not uniform proof. |
| Optimization | Exact per-branch theorem plus arithmetic certificate, or full-domain L/U gap | GLOBAL_CERTIFICATION_DEFERRED for all combinations. |
| Continuous views | Uniform L and certified δ on the admitted common domain | COVERAGE_ERROR_UNCERTIFIED. |

[MATH DERIVATION] One sufficient normalization stability bound uses a common probability-space coupling x,y with ‖x−y‖_L²≤ε. Means differ by at most ε; centering is an orthogonal projection, so centered difference ≤ε and |r_x−r_y|≤ε. If both radii ≥r_min>0, then
‖N x−N y‖_L²≤ε/r_x+|r_y−r_x|/r_x≤2ε/r_min.
This is conditional on the common coupling/measure. The supremum-norm version follows with centered difference ≤2ε and radius difference ≤2ε, giving ≤4ε/r_min when using the same probability measure and sup error ≤ε. Neither applies automatically when QH cardinality/weights change at coincidence or a chart lacks correspondence. No uniform near-zero stability is asserted.

## Deterministic failure ledger

| Event | Decision and retained evidence |
|---|---|
| Nonfinite/malformed coordinates, invalid metadata | INVALID_INPUT; retain field/contract failure, no score. |
| Empty/empty or empty/nonempty QO/QH observations | NOT_EVALUABLE; never empty–empty perfect match, infinity-as-finite or NaN→0. |
| Zero path length, point-like support, collapsed projection | NOT_EVALUABLE; log direction and block whole-domain minimum claim, no silent view deletion. |
| Positive extent not separated from zero by certified arithmetic | NOT_EVALUABLE for certified normalization; preserve uncertainty interval. |
| Tiny positive geometry | Do not discard edges/components; future precision/rescaling must be separately validated. Inherited S10 rejection remains unchanged. |
| Missing order, stroke pairing, closure, incidence or scene | NOT_EVALUABLE for that method; do not manufacture data from another representation. |
| Multiple strokes or closed path offered to QO | Outside QO primary contract; defer extension, no arbitrary concatenation/open shift. |
| Duplicate positions | QO consecutive-zero-length semantics; QH exact-set semantics only. No tolerance merging or deleting retracing. |
| Outlier, spur, small detached component | Retain finite discrepancy and separate supplied graph limitation; no silent trimming. |
| Crop/alias/threshold conceals a feature | Observation limitation; no exact topology claim; renderer contract unselected. |
| Unattained s>0 infimum in a proposed raw-fit extension | Report infimum and nonattainment, not a minimum or zero-scale match; extension deferred. |
| Timeout or incomplete branches | Keep feasible result/bounds separately; not global unless complete gap proof survives. |
| Mandatory provenance mismatch or target contamination | STOP; preserve/quarantine outputs as applicable; human resolution required. |

## Proof obligation register and future validation only

| ID | Obligation | Independent route / later gate |
|---|---|---|
| O1 | QO input order, interpolation, normalizer domain and zero-segment semantics | Independent representation review; G1/G3. |
| O2 | Arclength/integral implementation and arithmetic enclosure | Exact algebraic piecewise integrals independent of production; G4. |
| O3 | Full roll/reversal branch proof, including α=β=0 | Independent trigonometric derivation and exhaustive finite branches; G4. |
| O4 | Sampling/reparametrization and near-zero errors | Analytic bounds under declared curve class; G3/G4; otherwise defer. |
| O5 | Full finite-camera certificate and exact/near-tie handling | Independently checked all-branch manifest; G4. |
| H1 | Finite set, duplicate measure and normalized input validity | Independent exact set audit; G3/G4. |
| H2 | Both directed nearest-distance extrema | Scalar exhaustive interval oracle distinct from production; G4. |
| H3 | Whole-circle Lipschitz bounds, coverage, L/U witness proof | Independent interval-certificate checker; G4. |
| H4 | Covers plus normalization/measure stability for continuous claims | Independent all-component geometry and moment bounds; G3/G4. |
| H5 | Nonsmooth/tie/timeout/degenerate branches complete | Adversarial new fixtures and retained failure logs; G4. |
| CAP1 | Exact memberships/counts/nesting | D3 symbolic proof supplied for QC; future exact-table verifier independent of generator. |
| CAP2 | Proper lifts, seam/tie/antipodal conventions | D3 symbolic proof supplied; future arithmetic certificate. |
| CAP3 | Exact separation | Complete pair certificate, independent of symmetry reduction; G4. |
| CAP4 | Covering radius | Complete spherical Voronoi or interval domain certificate; G4. |
| CAP5 | Uniform camera objective regularity for Lδ | Separate proof with all degeneracies; otherwise COVERAGE_ERROR_UNCERTIFIED. |
| F1 | Candidate/control domain and error parity | G5 definitions + independent budget review; not a count-only claim. |
| F2 | Rights, uncertainty and no target-dependent choices | G1/G2/G6 access/signature audit. |

[TARGET-BLIND DESIGN CANDIDATE] A later validation preregistration must choose **new target-free fixtures**, not S00–S12 replays: curved polylines with uneven sampling/retracing (S03 lesson); same support with different supplied partitions (S04); subpixel and width-sensitive gaps (S05); multi-component dilution, spur and threshold-sensitive features (S06–S08); independent reversal and closed/open negative controls (S09); positive-scale collapse/near-zero, exact duplicates and nonfinite rejection (S10); a separately derived multi-basin objective whose analytic solution is known (S11); duplicated frames, antipodes and frame seams on the new families (S12). These are categories and proof requirements, **not newly generated geometry or executed cases**.

Before any such run: independently review symbolic expectations; sign the new fixture/validation protocol with all data, errors and stopping rules; freeze production and truly independent oracle implementations/configuration; authorize **one** run; retain all successes, failures, diagnostics and attempt records; independent QC; then human decision. A failed certificate requires amendment, not retries/tuning or return to P0A0. No registered numerical execution is authorized by this package.
