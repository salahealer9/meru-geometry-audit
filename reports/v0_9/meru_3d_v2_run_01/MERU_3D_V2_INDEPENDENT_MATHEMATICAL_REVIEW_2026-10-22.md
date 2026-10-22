# Meru v0.9 — 3D-V2 Independent Mathematical Review

**Date:** 22 October 2026
**Study:** `MERU_3D_V2`
**Outcome:** `MERU_3D_V2_EXACT_FINITE_GRID_COVERING_RADIUS_PASS`
**Review status:** Independent read-only reconstruction of the first-run JSON, not a rerun of the registered calculator.
**Registered protocol commit:** `db007d7429efbd41a4953b86f5eea7e026964aa8`
**Protocol Git blob:** `3db104c82b961761dfd80b92f968f1538869bb36`
**Original calculator SHA-256:** `fd63b10bd38536f83f5b6a6d35061006559e23bd5584a3dfdb7c90b59756e1d4`
**Original JSON SHA-256:** `92af306506afe95292170a00470f99b62f13f02a3687dab81467de34d349e4b3`
**Reported original stderr:** Empty; original checksum manifest records the SHA-256 of zero bytes `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`. The stderr file itself was not separately uploaded for this review.
**Original exit code:** `0`, as provided by the user.
**Independent reviewer:** Separate Python/SymPy implementation; 146 / 146 checks passed.

## Mathematical result

| Family and level | Signed directions | Axes | Chamber vertices | Exact maximum squared norm | Covering radius (degrees; display only) |
|---|---:|---:|---:|---|---:|
| A G0 | 6 | 3 | 4 | `3` | 54.735610317° |
| A G1 | 14 | 7 | 6 | `5 - 2*sqrt(3)` | 36.206023113° |
| A G2 | 26 | 13 | 8 | `-2*sqrt(6) - 2*sqrt(2) + 9` | 27.569276130° |
| B G0 | 6 | 3 | 4 | `3` | 54.735610317° |
| B G1 | 18 | 9 | 6 | `3/2` | 35.264389683° |
| B G2 | 42 | 21 | 8 | `3/2` | 35.264389683° |

All values agree with the frozen mathematical oracle, including complete six-record vertex lists and exact unordered multisets of squared vertex norms. Family A's second expansion reduces the spherical covering radius to about 27.569276°, whereas Family B's second expansion does not improve its worst-case radius beyond about 35.264390°. These are properties of the preregistered **finite orthographic direction grids**, not claims about historical geometry or glyph matching.

## Independent exact audit method

1. Construct the signed integer direction strata `A0`, `C`, `E`, `T` independently from the stated definitions; verify stratum counts and antipodal closure, the unions at every level, and direction/axis counts.
2. Reduce each grid using coordinate permutation and independent sign symmetry to the chamber `a >= b >= c >= 0`. For any vector in the chamber, direct maximization over signed permutations gives the exact support functions `a`, `(a+b+c)/sqrt(3)`, `(a+b)/sqrt(2)`, and `(2a+b)/sqrt(5)`.
3. Introduce the convex bounded chamber polytope defined by the chamber inequalities and each relevant support inequality `H_i <= 1`. By positive homogeneity, the least-covered direction cosine is `1 / max_(v in K) ||v||`. The convex squared norm attains a maximum at a vertex of a compact polytope; thus checking every vertex proves a global upper bound, not merely local optimality.
4. In independent checker code, enumerate every unordered triple of bounding planes. Find each full-rank intersection by **Cramer's rule using exact 3-by-3 determinants**, check every defining half-space by exact SymPy radical sign decisions, and deduplicate equal triples symbolically. Any undecidable sign is an error, not a floating-point verdict.
5. Check every independent vertex against the registered program's complete vertex list; verify all supplied vertex norms, full squared-norm multisets, maximal norms, unique chamber winners, positive exact covering cosines, normalized worst directions, and active-plane reporting. Check the original signed/axis counts and antipodal closure separately.
6. Compare only the angle displays using a numerical tolerance; decimal degrees never enter the algebraic accept/reject decision. Confirm both shared G0 levels and the B G1/G2 identity.

**Independent result:** **146 / 146 checks passed**, with no failures. The machine-readable audit JSON and the independently written source are retained separately.

## Exact global witnesses

| Grid | Worst chamber-polytope vertex |
|---|---|
| A G0 = B G0 | `(1,1,1)` |
| A G1 | `(1,sqrt(3)-1,0)` |
| A G2 | `(1,sqrt(2)-1,sqrt(3)-sqrt(2))` |
| B G1 = B G2 | `(1/sqrt(2),1/sqrt(2),1/sqrt(2))` |

The B G1/B G2 result also has an independent analytical certificate. The B G2 grid contains B G1, so its covering radius cannot be larger. At the unit body diagonal `(1,1,1)/sqrt(3)`, the nearest E direction has cosine `sqrt(2/3)`, whereas the nearest T direction reaches only `sqrt(3/5)`, which is smaller. Hence the B G1 worst gap survives unchanged in B G2. Both radii equal `acos(sqrt(2/3))` exactly.

## Scope, dependencies, and evidence

- Original machine output declares Linux, Python 3.11.2 and SymPy 1.11.1. This independent review was performed in a separate analysis environment and does not assert binary or environment identity with the user's machine.
- The uploaded first-run `results.json` was independently hashed and matches the user's uploaded `SHA256SUMS.txt`; the previously frozen standalone source file also hashes to the recorded value. The uploaded exit-code file contains `0`. The user reported stderr empty, consistent with the checksum manifest; that original local file remains to be verified in situ prior to signed results freezing.
- The signed protocol was retrieved from GitHub under the stated commit; GitHub reports a valid signature, while the user supplied trusted-key local GPG validation at signing.
- No Meru 3D object, source drawing, physical shadow, Hebrew glyph, projection target, matched null, or covering-radius optimization beyond these fixed finite grids was examined. No universal statement about silhouette distinctness or specificity follows.
- This audit can support a signed V2 results freeze provided the original `run_01` folder is preserved unchanged, all original evidence hashes pass on the user's computer, and the intended single additive commit is verified.

## Artifact identities

- Independent QC script SHA-256: `14fb54cdd62210891356d0c7955115f67dca9ee55b6dd28cd1c26f361bfa780c`
- Independent QC JSON SHA-256: `f76d7daa05112b56de5da3525e2441d32626a4b10978d2119687e34b2347b271`
- First-run JSON SHA-256: `92af306506afe95292170a00470f99b62f13f02a3687dab81467de34d349e4b3`
