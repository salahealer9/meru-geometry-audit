# QO2D-M1 — Target-Blind Mathematical Microvalidation

**Meru Geometry Audit v0.9 | 22 October 2026 | DRAFT — NOT EXECUTED**

**Repository/branch:** `salahealer9/meru-geometry-audit` / `hebrew-projection-capacity-v0.9`  
**Proposed file:** `docs/v0_9/qo2d_m1_target_blind_microvalidation_preregistration_2026_10_22.md`  
**Expected direct parent:** signed P1 administrative closeout `daa39bb6d41cacadfeb4e51f753e35cf2531dada`  
**Human signing fingerprint:** `D4EC014EEFCC90E619D2AA59A91239ABCF512130`

## 1. Question, source and boundaries

**Question:** Can one independently written, small Python calculator reproduce **eight predeclared analytic QO results** for synthetic ordered open polygonal paths, including reflection/reversal exclusions, exact ties, near-ties and invalid input?

The governing mathematical sources are the signed P0A3D theorem result, `reports/v0_9/p0a3d_theorem_result_freeze/P0A3D_EXACT_2D_QO_THEOREM_RESULT_CLOSEOUT.md` and its `P0A3D_ORIGINAL_THEOREM_PROOF.md`, together with `reports/v0_9/p0a2_target_blind_design/score_normalization_candidates.md`. The abstract theorem was independently reviewed, but the previously submitted *executable implementation remains incomplete/unqualified*. This study is **not** that software's certification or the previously planned P0A4 registered experiment.

**Forbidden:** Hebrew-letter/chart images, fonts as proxy targets, Meru 3D projections, target matching or tuning, 3D cameras, candidate-versus-null tests, and imports/execution of archived P0A3D or P1 candidate/controller code. The P0A3H-P1 lane is separately signed **closed incomplete** and is not reopened. All earlier signed records and mathematical kernels remain unchanged.

## 2. Exact QO definition

Inputs are two independently specified finite **ordered open paths** with rational 2D vertices and positive Euclidean arclength. Distinguish endpoints and traversal even when endpoint *coordinates* coincide. Consecutive duplicate vertices have zero duration and may be removed **with provenance**; genuine returns/retracing remain. Parametrize each path by its **own normalized planar arclength** `u∈[0,1]` (not vertex index).

Define for each path `x(u)` its centroid `c_x=∫x(u)du`, positive RMS `r_x=(∫||x(u)-c_x||²du)^(1/2)` and normalized path `X(u)=(x(u)-c_x)/r_x`. Let `A,B` be independently normalized. With `J(x,y)=(-y,x)`, define

\[
\alpha=\int_0^1 B\cdot A\,du,\quad
\beta=\int_0^1 B\cdot JA\,du,\quad
s=\sqrt{\alpha^2+\beta^2},\quad
q_O=\sqrt{2-2s}.
\]

Only proper rotations `SO(2)` are optimized. Independent centring and positive RMS normalization handle translation and scale. No reflection, reversal, cyclic shift, time warp, reordering, extra scale or correspondence search. For `s>0`, the unique optimal rotation is `Q=[[α/s,-β/s],[β/s,α/s]]`. For **exact** `s=0`, every proper rotation is optimal, with canonical identity witness. No numerical tolerance may turn a nonzero `s` into an exact tie.

## 3. Fixed analytic fixtures — no post-run edits

`L=[(0,0),(1,0),(1,1)]`, `H=[(0,0),(1,0)]`, `d=1/1024`. All coordinates are literal exact rationals; vertices are **not** equally weighted samples.

| Case | `a` | `b` | Exact `(α,β)` | Exact QO and optimal witness |
|---|---|---|---|---|
| **M01** | `L` | `[(3,-2),(3,3),(-2,3)]` | `(0,1)` | `0`, +90° rotation |
| **M02** | `L` | `[(0,0),(1/2,0),(1,0),(1,0),(1,1/2),(1,1)]` | `(1,0)` | `0`, identity; record duplicate event |
| **M03** | `L` | `[(0,0),(1,0),(1,-1)]` | `(0,-3/5)` | `2/√5`, −90° rotation; no reflection |
| **M04** | `L` | `[(1,1),(1,0),(0,0)]` | `(-3/5,0)` | `2/√5`, 180° rotation; no reversal |
| **M05** | `H` | `[(0,0),(0,1),(0,0)]` | `(0,0)` | `√2`; all rotations tied; report identity |
| **M06** | `H` | `[(0,0),(d,1),(2d,0)]` | `(1/√262145,0)` | `√(2−2/√262145)`; uniquely identity |
| **M07** | `[(0,0),(0,0)]` | `H` | Undefined | `NOT_EVALUABLE`; no score or witness |
| **M08** | `H` | `[(0,0),(1/1000000000000,0)]` | `(1,0)` | `0`, identity; positive tiny scale valid |

**Independent pre-run derivations.** For `L`, arclength centroid is `(3/4,1/4)` and squared RMS `5/24`. Its unnormalized cross-moments are `(0,-1/8)` for M03 and `(-1/8,0)` for M04, giving the normalized `−3/5` terms. These were independently rechecked by exact piecewise-polynomial integration during **draft review**, not by executing the proposed experimental script. A forbidden reflection (M03) or path reversal (M04) would produce a perfect correspondence, but is **not** part of QO. For M05, the centred tent ordinate is orthogonal to the linear abscissa: `s=0` exactly. For M06, the legs have length `√(1+d²)`, the x-coordinate is `2du` and the symmetric ordinate contributes no correlation: `s=2d/√(1+4d²)=1/√262145>0`. In M03, the proper optimal squared residual is `4/5`, while identity gives `2`.

## 4. One lightweight calculator, one recorded execution

1. **Preregister before running.** Human reviews this document and, if approved, signs **only this new Markdown file** in one additive Git commit. Do not change any existing protocol, theorem or code. The file's Git blob and signed commit identify the fixed expectations. This signing is a prerequisite to the registered M1 run, **not** authorization for P0A4 or P1.
2. **Prepare independent source.** Write **one small standalone Python 3.11 script** outside the repository using only `fractions.Fraction` for input literals and `decimal.Decimal` with **≥50 decimal digits** for positive square roots/integration. Compute normalized-arclength centroids, RMS, correlations by exact-on-each-cell polynomial endpoint formulas at declared numerical precision, optimal proper rotation and the **direct integrated squared residual**. No optimiser, sampled-index averaging, candidate import or elaborate security harness. Inspect it and record its SHA-256 **before first invocation**. The human separately approves running that exact script.
3. **Run once.** Invoke the frozen script once for M01→M08. Preserve script, command, input/protocol/script hashes, host Python version, precision, timestamp, stdout, stderr, exit code, calculated values, witness, direct residual and per-case status. No invisible reruns or tuning. Any repair leads to a separately named follow-up record without overwriting the first run.
4. **Independent arithmetic review.** For evaluable M01–M06/M08 compare `α`, `β`, `qO`, each witness-matrix entry, rotation determinant `+1`, and directly integrated **squared** residual `2−2s` separately to the frozen analytic oracle, each with absolute numerical error ≤`1e−10` (analytic irrational values evaluated independently at the same declared precision). The witness for M05 must be identity, accompanied by the analytic all-rotation tie. M06 must report `s>0` and unique optimum. M02 must record its zero edge. For M07 require explicit `NOT_EVALUABLE` due to zero length and **no** numeric result. M03/M04 must never score zero by introducing forbidden freedom. Decimal agreement does **not** prove an exact algebraic equality; exact tie claims rely on the independent analytic derivation.

Record each case as `MATCH`, `MISMATCH`, `NOT_EVALUABLE_AS_EXPECTED` or `INCOMPLETE`, with reasons and preserved evidence. If all seven valid cases match and M07 is rejected, the narrow conclusion is **`QO2D_M1_EIGHT_CASE_MICROVALIDATION_PASS`**. Otherwise record **`QO2D_M1_INCOMPLETE_OR_FAILED`**, including differences or resource failures. Neither result proves general software correctness, refutes the mathematical theorem, establishes Meru/Hebrew specificity or licenses actual target access.

## 5. Sign-off and next research question

At signing, verify the clean local branch/upstream, required direct parent `daa39bb6d41cacadfeb4e51f753e35cf2531dada`, correct GPG identity and a **one-new-file-only** staged diff. Only the human may sign/push. A different parent or unexpected file requires stopping and reviewing, never rewriting history. **No program execution or change to any previously frozen scientific source occurs during this protocol-preparation step.**

Once M1's one-run evidence has been examined, move to a **separate target-blind study of effective 3D viewing capacity**, with properly quotient-distinct views and matched geometric controls. Hebrew-target work remains gated by independent source/observation/rights decisions. There is no need to revive P1-grade deployment assurance unless a later public software release actually justifies it.
