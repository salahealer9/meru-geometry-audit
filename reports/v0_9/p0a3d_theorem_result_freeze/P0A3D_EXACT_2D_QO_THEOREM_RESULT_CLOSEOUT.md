# P0A3D — Exact 2D QO Mathematical Theorem: Independent-QC Result Freeze

**Project:** Meru Geometry Audit — v0.9 target-blind Hebrew projection-capacity programme  
**Prepared:** 2026-10-20  
**Git branch:** `hebrew-projection-capacity-v0.9`  
**Before human signing:** `HUMAN_THEOREM_RESULT_FREEZE_CANDIDATE` — **NOT YET A SIGNED RESULT**.  
**Decision class:** source-independent **exact mathematical theorem**, positively reviewed; executable implementation retained **INCOMPLETE** and **UNQUALIFIED**. No new experiment.

## 1. Exact signed authority and human commit boundary

This is an additive result checkpoint whose **required direct parent** is the human GPG-signed, protocol-only P0A3D preregistration:

`92de104cab58339df370acf96b8d849ecc2d888b`

The P0A3D protocol Git blob is `39944862b7ec7565188584c97695fdf925538f8a`, at `docs/v0_9/p0a3d_exact_2d_qo_core_proof_and_implementation_protocol.md`. Its parent is the signed P0A3C incomplete preservation commit `923bab7855deaee6be49dd299bbdb0d6251844c1`. The expected author key fingerprint is `D4EC014EEFCC90E619D2AA59A91239ABCF512130`.

On 2026-10-20 the P0A3D protocol-only commit, parent and single-file scope, verified GitHub commit signature and matching remote branch tip were independently checked. The local operator must *recheck* clean branch, signed parent and correct staging before signing. The signed Git commit after human approval—not this unsigned closeout—is the authoritative result-freeze identity. Do not rewrite previous preregistration documents to update historical `DRAFT` labels.

## 2. Exact theorem approved *conditionally upon human-signed freeze*

**Name / scope:** `P0A3D_QO_2D_OPEN_RATIONAL_VERTEX_SO2_EXACT`.

**Inputs:** exactly two independently supplied, genuinely ordered, finite open 2D polygonal paths with rational-coordinate vertices, strictly positive total Euclidean planar arclength, and independently valid arclength RMS normalization. Path endpoints/traversal are fixed even when first and last vertex coordinates coincide. Consecutive zero segments may be removed as duration-zero *events with provenance*; genuine returns and retracing preserve traversed arclength multiplicity. The theorem is an exact mathematical statement over all finite valid inputs; finite implementation resource limits are **not** exclusions from its abstract domain.

**Single nuisance group:** proper planar rotations `SO(2)` only. Independent translations and positive scales are removed by the prescribed normalized arclength centroids and RMS radii. No reflection, reversal, time warp, phase shift, arbitrary correspondence, stroke permutation, camera, cropping, deformation or source/target-dependent fitting is searched.

For normalized arclength `u∈[0,1]`, let `A(u)` and `B(u)` be the independently centered and RMS-normalized paths, with `J(x,y)=(-y,x)`. Define exact real-algebraic quantities

`alpha = ∫ B(u)·A(u) du`, `beta = ∫ B(u)·J(A(u)) du`, `s = sqrt(alpha² + beta²)`.

**Accepted mathematical theorem under these premises:**

1. Exact real-algebraic constructions with decidable equality/sign exist for the segment lengths (including irrational lengths), arclength breakpoints, piecewise polynomial correlation integrals, centroids, strictly positive RMS radii, `alpha`, `beta`, `s`, score, and proper-rotation witness.
2. `0 ≤ s ≤ 1` and the global attained optimum over the *entire admitted* `SO(2)` is `qO = sqrt(2 − 2s)`.
3. If `s>0`, the unique optimal rotation is `[[alpha/s, −beta/s],[beta/s, alpha/s]]` with determinant +1 and directly attained squared residual `2−2s`.
4. If `s=0` *exactly*, every proper rotation is optimal; the canonical witness is the identity and `qO=sqrt(2)`. Arbitrarily small **nonzero** correlation is not a whole-roll tie.
5. A finite recursive sign/equality algorithm for dependent positive square-root towers descends to rational arithmetic; the zero-conjugate inversion case is handled without dividing by zero. This is an existence/termination statement in the unlimited exact-arithmetic model, **not** a practical uniform runtime bound.

The original submitted proof, preserved as `P0A3D_ORIGINAL_THEOREM_PROOF.md`, is an **exact byte-for-byte extraction** of `reports/v0_9/p0a3d_exact_qo_core/THEOREM_PROOF.md` inside the original candidate ZIP. It is not a post-QC rewrite. The independently assessed algebraic sign, reducible tower/inversion, positivity, union-of-breakpoints integration, `SO(2)` maximum, attained witness and near-zero counterexample appear in the accompanying dated independent QC report.

**Positive mathematical QC outcome:** the independent reviewer found no material gap in the complete constructive proof *within that domain* and recommends `P0A3D_EXACT_2D_QO_THEOREM_INDEPENDENTLY_VERIFIED` as the **theorem-level result status**, conditional upon human review and signing this additive result freeze. This project-specific verification is not a claim of external publication, formal-machine proof, or certified executable software.

## 3. Evidence identities and independent review

| Original evidence stored unchanged in this new checkpoint | Bytes | SHA-256 |
|---|---:|---|
| `original_P0A3D_cumulative_proof_and_implementation_candidate.zip` | 642,047 | `c2f99b0e78849de16c8dc8167bdf5d584d4f64ab2c8a787d6a0ed507cfa9f378` |
| `P0A3D_independent_mathematical_and_engineering_QC_2026-10-20.md` | 11,866 | `d99e8d4513013f6b559b15d5dddd462d699cf4ac12a90aec750b5fb6bbc29520` |
| `P0A3D_independent_QC_verification_2026-10-20.json` | 2,903 | `5c909416845c81eb5f185166e35d4a3bf9aa8458dd7620bd3ce14d9c6b14a563` |
| `original_P0A3D_independent_QC_review_2026-10-20.zip` | 7,893 | `4da72ab4a3347cad19e746f42ae9799f6e410a97ceb8972ad74530e6723c1e20` |
| `P0A3D_ORIGINAL_THEOREM_PROOF.md` (extracted, unchanged) | 14,960 | `809e133019234081447908deafea722c3e05a9a8d503017e7c8fce7d46725451` |

The candidate ZIP contains **136 entries**, with **135/135** non-self SHA-256 manifest entries and **134/134** payload inventory entries independently checked. CRC passed. The independent reviewer verified 12 original detached signed commit objects and one signed v0.8 tag using the matching provided public key; the GitHub signature attestation and the user's trusted-key local `git verify-commit` are distinct verification contexts. Four P0A3D DEV attempts are retained, including attempt 03's two parser/error-handling failures and attempt 04's corrections. The independent QC reran only the predeclared bounded generic DEV suite (**20/20 PASS**) and did not execute scientific or Hebrew-target tests. Prior P0A3C evidence resides in the earlier signed checkpoint, referenced by exact identities rather than duplicated here.

## 4. Explicit independently QC-reviewed software-negative outcome

**Software remains:** `P0A3D_IMPLEMENTATION_INCOMPLETE`; `P0A3D_EXACT_PREDICATE_UNQUALIFIED` **as a software backend**; `P0A3D_REFERENCE_INDEPENDENCE_UNQUALIFIED` **for production certification**; `P0A3D_RESOURCE_NONCOMPLETION`; `P0A3D_REGISTERED_NUMERICAL_VALIDATION_NOT_RUN`.

Implementation candidates correctly pass restricted DEV cases, including irrational length, exact tie, tiny nonzero correlation and forged witness rejection, but these do not qualify arbitrary malformed input, nested certificate parser failure envelopes, unbounded integer/degree/recursion/resource blow-up, abrupt termination, fixed reference sign-isolation cap, external signed code/config pins, adversarial independent checker trust, or all eligible input instances. A mathematician's proof of an abstract exact method is different from a proof of the delivered executable implementation.

**Must NOT assign:** `P0A3D_EXACT_2D_QO_IMPLEMENTATION_CANDIDATE_FOR_REGISTERED_VALIDATION`, `GLOBAL_CERTIFIED` (software or experimental), `QO_A`, `QO_B`, `QH_A`, `QH_B` certification, `P0A3C_FINITE_CAMERA_IMPLEMENTATION_READY_FOR_REGISTERED_TARGET_FREE_CERTIFICATION`, any Hebrew-specific discovery or statistical claim.

The original ZIP stores source and DEV evidence for archive/provenance only; **DO NOT** install it as approved `src/`, `reference/` or tests in the existing repository. The original QC evidence objects are retained byte-for-byte, without retrospective alteration.

## 5. Permanent information and inference barriers

No P0A0 S00–S12 replay; no P0A4 registered target-free certification run; no Hebrew glyph pixels, fonts-as-proxies, extraction, registration or matching; no candidate/null control experiment, final primary metric selection, G0/A/B camera extension, QH whole-circle optimization or physical shadow claim is authorized by this signed **theorem result**. The v0.8 historical closeout remains `NO_REPRODUCIBLE_PUBLISHED_FIRST_HAND_CONSTRUCTION_RECOVERED`. P0A3C incomplete states and B07/B08 historical observation/rights and controls/fairness gates remain unresolved.

Even a perfect mathematical QO theorem assumes an independently supplied ordered path; it neither proves historical glyph path order nor makes the score a metric on unordered glyph supports. No Meru/Hebrew specificity follows.

## 6. Frozen decision, next-stage plan and human signing

`P0A3D_EXACT_2D_QO_THEOREM_INDEPENDENTLY_VERIFIED` may be recorded **only on completion of this human-reviewed signed result freeze**, with all §4 software-negative statuses simultaneously retained. The companion `P0A3D_NEXT_EXACT_QO_SOFTWARE_QUALIFICATION_PLAN.md` is an **informational proposal** for a future separately signed engineering-only protocol, not execution authority. It does not approve any P0A4 run or relax this theorem's mathematical scope.

Human operator shall: independently verify local clean branch `hebrew-projection-capacity-v0.9` and parent `92de104cab58339df370acf96b8d849ecc2d888b`; verify prior signature and expected signing fingerprint; check the outer freeze candidate ZIP checksum, CRC, and root-relative `FREEZE_MANIFEST.sha256`; stage *only* this new checkpoint directory; inspect every staged path and diff; create a human-signed additive result commit with valid expected GPG fingerprint; verify exact parent and clean worktree; then push the feature branch. A diverged HEAD, altered source bytes or manifest mismatch is a **HARD STOP**, never an invitation to overwrite or reset signed science.

**Decision:** preserve a positive *exact mathematical theorem finding* and an explicit negative *software-readiness finding* as separate, immutable evidence classes.
