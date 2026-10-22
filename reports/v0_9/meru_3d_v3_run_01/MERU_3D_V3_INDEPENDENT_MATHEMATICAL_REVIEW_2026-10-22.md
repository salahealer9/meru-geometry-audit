# Meru v0.9 — 3D-V3 Independent Exact Mathematical Review

**Date:** 22 October 2026
**Scope:** Target-blind labelled orthographic projection equivalence; three frozen rational controls, six family/tier grid records (five distinct finite direction sets).
**Signed preregistration commit:** `67ccaa1f5292acee31e26e318e7bff3bc2e7f5ec`
**Protocol Git blob:** `f835cde4ec7890a66ef2a82f3f5699361752371e`
**Original calculator SHA-256:** `7e6fe6a83a37580ecde5a852b1d7391937fd74d3cac1f9555a711443f4821867`
**Original submitted JSON SHA-256:** `87664b25408c18c04368c72a03dd7fd18554b94f8e635308a11e7c1674aad960`
**Reported stderr:** Empty; original manifest gives SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.

## Decision and provenance limitation

**Independent mathematical QC: PASS, 21,683/21,683 exact checks.** The audit was separately written from the signed geometric definitions using Python's rational arithmetic. The registered calculator was **not imported or rerun**. The uploaded source, JSON, and their checksums were separately hashed and agree with the supplied manifests. The JSON asserts the registered `PASS` label, and names the correct signed commit/blob and Python environment.

**Original exit code not uploaded at review time.** Scientific results-freeze signing is conditional on *local* verification of `~/meru-3d-v3/evidence/run_01/exit_code.txt` as `0`, the complete original first-run evidence directory, original stderr bytes and manifest consistency. Do not construe the independently verified mathematical outcome as independent observation of the shell's exit status or first-run timestamp. If the local gate fails, stop; preserve existing evidence without committing a PASS result.

## Complete exact class-census result

Each control entry is the number of distinct *label-preserving* planar projection classes **SO(2) / O(2)** for evaluable cameras; original signed-camera and projective-axis counts are shown separately.

| Family / tier | Signed / axes | F (full 3D) | L (line) | P (triangle) | P rank-one / rank-two |
|---|---:|---:|---:|---:|---:|
| A G0 | 6 / 3 | 6 / 3 | 1 / 1 | 4 / 3 | 4 / 2 |
| A G1 | 14 / 7 | 14 / 7 | 2 / 2 | 8 / 5 | 4 / 10 |
| A G2 | 26 / 13 | 26 / 13 | 3 / 3 | 14 / 9 | 8 / 18 |
| B G0 | 6 / 3 | 6 / 3 | 1 / 1 | 4 / 3 | 4 / 2 |
| B G1 | 18 / 9 | 18 / 9 | 2 / 2 | 10 / 7 | 8 / 10 |
| B G2 | 42 / 21 | 42 / 21 | 4 / 4 | 22 / 15 | 16 / 26 |

- **F:** Every camera is rank two, and each signed camera has its own SO(2) class. Exactly antipodal pairs form the O(2) classes. Full affine span recovers `I−nnᵀ` from the complete labelled Gram data, hence Gram equality implies `m=±n`.
- **L:** Precisely the two cameras `(−1,0,0)` and `(1,0,0)` are rank-zero **NOT_EVALUABLE** at every tier. Every other camera has rank one. The only varying exact class parameter is `1−n_x²`, with identical SO(2) and O(2) partitions.
- **P:** Every camera is evaluable. The exact rank is one iff `n_z=0`, otherwise two. The Gram matrix fixes `(n_x,n_y)` up to an overall sign; the oriented minors distinguish the sign of `n_z` where rank is two. Rank-one edge-on projections remain distinct where their labelled Gram matrices differ.
- **Shared G0:** The A and B camera order, all per-camera invariants, pair matrices, partitions and class counts are identical.

## Independent derivation and completeness

Let `Y_i` be the original centred 3D labelled points, and let an integer camera triple be `v`, with positive integer `d=v·v` and unit direction `n=v/√d`. The complete projected labelled Gram entries are

`M_v(i,j) = Y_i·Y_j − (v·Y_i)(v·Y_j)/d`.

The oriented 2D pair-minors of a proper right-handed projection are

`A_v(i,j) = [v·(Y_i×Y_j)]/√d`, for `i<j`.

The checker generates all coordinate strata A0, C, E and T independently from the preregistered exact set-builder definitions, and centres F, L and P independently. Every Gram entry and cross-product numerator is evaluated with `fractions.Fraction`. Two exact oriented areas `a/√d` and `b/√e` are equal only if both are zero, or have the same sign and `a²e=b²d`. No floats, sampled camera frames, tolerances or target-dependent adjustments enter these decisions.

For ordered labelled planar point configurations, equality of complete Gram matrices is **necessary and sufficient** for an O(2) isometry on their occupied linear span, extendable to the whole plane. Where the span has rank two, equality of all nonzero oriented minors fixes the proper orientation and hence SO(2); at rank zero or one an isometry on the occupied span always admits a determinant-`+1` extension. Therefore complete Gram equality plus minor equality is necessary and sufficient for SO(2), not merely a heuristic discriminant. Fixed centring removes translations; no scale or label permutation is admitted.

The independent checker constructed the direct pairwise matrix for both equivalences for every control and every family/tier grid. It compared each matrix entry against the submitted JSON **entry by entry**, reconstructed ordered equivalence classes and camera-triple memberships, and compared class-size multisets, rank/status records, antipodal reflection laws, SO(2)-within-O(2) containment and equivalence transitivity. It independently checked every displayed per-camera Gram matrix and the entire oriented-minor numerator array. It separately checked all frozen numerical oracles and signed family/tier nesting/camera order. No class was created by rounding or pairwise-distance threshold.

### Machine-readable check census

| Audit topic | Checks |
|---|---:|
| Pairwise matrix entries | 18,192 |
| Per-camera metadata | 2,034 |
| Exact Gram/minor arrays and denominators | 1,008 |
| Mathematical equivalence/algebra guards | 109 |
| Rank, collapse and evaluability guards | 114 |
| Partition memberships, counts and sizes | 144 |
| Set/count/order guards | 35 |
| Whole-matrix comparisons | 36 |
| Provenance, declared outcome and general guards | 11 |
| **Total** | **21,683** |

The full audit results and separately authored checker are distributed alongside this document as `MERU_3D_V3_INDEPENDENT_QC_2026-10-22.json` and `meru_3d_v3_independent_exact_qc.py`. The 21,683 checks include individually tested matrix entries; they are not 21,683 independent scientific observations.

## Scientific limits and next boundary

V3 establishes exact equivalence of finite **labelled landmark configurations**, not equivalence of continuous open/closed curves, silhouettes, visible edges, shading or cast shadows. Different controls produce different numbers of geometrically noncongruent views, but that observation does not establish that any historic Meru figure yields Hebrew letterforms. Finite-camera capacity is not evidence of target specificity. A new signed V4 protocol must fix curve/silhouette definitions, degenerate-view handling and fair nuisance/negative-control contracts prior to any scientific run. The prior v0.8 source-construction limitation remains unchanged.
