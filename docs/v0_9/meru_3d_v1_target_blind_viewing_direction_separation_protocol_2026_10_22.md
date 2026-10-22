# Meru v0.9 — 3D-V1 Target-Blind Viewing-Direction Census and Separation

**Date:** 22 October 2026  
**Status:** DRAFT FOR HUMAN REVIEW; NOT SIGNED; NOT EXECUTED  
**Repository:** `salahealer9/meru-geometry-audit`  
**Branch:** `hebrew-projection-capacity-v0.9`  
**Required direct parent if signed immediately:** `7e05cd275bba83590f1cf1e6f8f88a157f70e2df` (QO2D-M1 signed results freeze)  
**Signer fingerprint:** `D4EC014EEFCC90E619D2AA59A91239ABCF512130`

## 1. Scientific purpose and strict interpretation

**Question:** For the two already published *candidate* nested finite camera-direction families A and B, what are (i) the exact numbers of distinct signed directions and unoriented axes and (ii) the exact minimal angular separations at levels G0, G1 and G2?

This is a deliberately limited, target-blind 3D **viewing-direction geometry** study, not a reconstruction of a historical hand, a three-dimensional shadow-model certification, a study of object-specific silhouettes, or a Hebrew-letter comparison. It is the first component of an effective viewing-capacity audit, not a measurement of final effective output complexity or statistical specificity. It does not choose family A or B by downstream matching performance.

**Frozen mathematical sources:** `docs/geometry/projection_orbit_results_v0_5.md` and `reports/v0_9/p0a2_target_blind_design/direction_family_candidates.md` (D3). The original v0.8 unresolved shaping rule and every earlier software qualification limitation remain unchanged. The QO2D-M1 result is a separate successful eight-case microvalidation, not authorization of 3D QO scoring.

**Prohibited:** Hebrew glyph or chart pixels, proxy fonts, source-derived glyph coordinates, score tuning, 3D Meru candidate projection fitting, historical-optics claims, candidate-vs-null shape comparisons, sampled 2D silhouette matching, P0A3D/P1 archived candidate imports, alteration/replay of signed historical experiments, or public-deployment claims.

## 2. Exact sets and quotient conventions

Define unit directions from exact nonzero integer triples; only positive proportionality identifies *signed* vectors. Let:

- `A0 = {±(1,0,0), ±(0,1,0), ±(0,0,1)}` (six coordinate directions).
- `C = {(s1,s2,s3)/√3 : si∈{−1,+1}}` (eight cube corners).
- `E = {v/√2 : exactly one coordinate is 0 and the other two are independently ±1}` (twelve edge directions).
- `T = {v/√5 : exactly one coordinate is 0 and the other two have absolute values 1 and 2 in either order with independently assigned signs}` (24 ratio-two directions).

**Family A:** `G0=A0`, `G1=A0∪C`, `G2=A0∪C∪E`.

**Family B:** `G0=A0`, `G1=A0∪E`, `G2=A0∪E∪T`.

The **signed-direction** quotient identifies camera frames differing only by proper in-plane `SO(2)` roll; its universal space is `S²`. The **unoriented-axis** quotient additionally identifies `n∼−n`, appropriate only when planar reflections `O(2)` are explicitly allowed; its universal space is `RP²`. Never equate an `SO(2)` camera with its antipode by default. Object-specific additional coincidences are not counted here.

For each finite signed set `G` define

`c(G)=|G|`, `a(G)=|G/{n∼−n}|`, `m(G)=max_{n≠m∈G}(n·m)`, and `σ(G)=arccos(m(G))`.

For axes use distinct antipodal pairs only and `m_axis(G)=max_{[n]≠[m]}|n·m|`, `σ_axis(G)=arccos(m_axis(G))`. The antipodal pairs representing the *same* axis must never be included in axis separation. Counts, extremal dot products and witnesses are exact; radians/degrees are presentation only.

## 3. Preregistered mathematical oracles

The counts follow from disjoint coordinate-support/magnitude patterns and antipodal closure:

| Family/level | Signed directions `c(G)` | Axes `a(G)` | Predicted maximum distinct signed dot `m(G)` | Predicted min separation `σ(G)` |
|---|---:|---:|---|---|
| A G0 (= B G0) | 6 | 3 | `0` | `π/2` |
| A G1 | 14 | 7 | `1/√3` | `arccos(1/√3)` |
| A G2 | 26 | 13 | `2/√6` | `arccos(2/√6)` |
| B G1 | 18 | 9 | `1/√2` | `π/4` |
| B G2 | 42 | 21 | `3/√10` | `arccos(3/√10)` |

For these antipodally closed finite families, `m_axis(G)=m(G)` and `σ_axis(G)=σ(G)` because every cross-axis absolute dot is realized with positive sign by an available antipode. This identity does **not** mean signed and axis counts are the same.

**Witness obligations:** A G0: any two orthogonal axes. A G1: an axis and cube-corner direction sharing its positive sign. A G2: `(1,1,1)/√3` and `(1,1,0)/√2` give `2/√6`. B G1: `(1,0,0)` and `(1,1,0)/√2` give `1/√2`. B G2: `(2,1,0)/√5` and `(1,1,0)/√2` give `3/√10`.

**Upper-bound obligation:** An attained pair alone is insufficient. Exhaustively classify every unordered pair's exact rational/surd dot product (or use an independent complete pair-table comparator) and show no pair exceeds the listed maximum. Duplicate signed vectors and self-pairs must be excluded, including at the joins between strata. Registered unordered pair counts are `15,91,325` for A G0/G1/G2 and `15,153,861` for B G0/G1/G2. Axis cross-pair counts are `3,21,78` for A and `3,36,210` for B.

The two new separation profiles are *mathematical geometric properties of proposed viewing grids*, not historical-source claims. More sampled directions improve opportunity to fit a target; they do not by themselves show specificity.

## 4. Minimal implementation and one-run procedure

1. **Before execution:** Human reviews this exact protocol and signs a *single additive Markdown commit* with the required direct parent, correct GPG fingerprint and unchanged earlier files. The signed text and Git blob freeze the formulas and expected counts. Do not treat the header's historical `DRAFT` text as subsequent authority to edit a signed file.
2. **Prepare one small standard-library Python 3.11 script outside the Git repository.** Enumerate signed integer triples explicitly and normalize symbolically by squared norms `1,2,3,5`, not floating near-equality. For each family/level, compute canonical signed triples, antipodal classes, total pair census and dot comparisons without `acos` during maximization. Compare two dot products exactly using signed integer numerators and square-free denominator handling (or exact rational squaring with rigorous sign logic). Generate the exact maximizing-pair witnesses and the full per-stratum/pair-type extremal summary.
3. **Review and freeze the script SHA-256 before invocation.** The human separately approves its **one recorded first run**. Preserve script, command, Python version, preregistration commit SHA and blob, script checksum, timestamp, stdout, stderr, exit code and output JSON. Refuse silent overwrites/reruns; a necessary repair is a separately named recorded attempt.
4. **Independent review:** Verify counts, pair census, antipodal closure, the listed maxima and witnesses directly from independently written enumeration/hand algebra without importing the submitted calculator. Exact matching, rather than an angular floating tolerance, is the acceptance gate. Approximate angles may be displayed but do not decide pass/fail.
5. **Outcome:** `MERU_3D_V1_FINITE_DIRECTION_CENSUS_AND_SEPARATION_PASS` only if every registered count, extremum, axis equivalence and witness checks; otherwise `MERU_3D_V1_INCOMPLETE_OR_FAILED`, with all original evidence retained. This is not a certificate for camera covering radii, continuous viewpoints, object-specific silhouette capacity or Meru/Hebrew specificity.

## 5. What comes after this study

The next separate question is **coverage**, rather than separation: how well do these fixed finite direction sets cover the sphere or projective plane? Covering radius `δ=max_{x∈S²} min_{n∈G} arccos(x·n)` is a continuous optimization and **is not calculated, approximated or certified in V1**. If V1 passes, plan a small independent coverage study with a clearly limited proof or approximation claim, before contemplating 3D object-specific projection equivalence and matched geometric controls. No claim of a universal camera-capacity advantage follows merely from larger grids.
