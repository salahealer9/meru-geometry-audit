# Meru v0.9 — 3D-V2 Target-Blind Exact Spherical Covering Radius

**Date:** 22 October 2026  
**Status:** PROTOCOL DRAFT FOR HUMAN REVIEW — NOT PREREGISTERED; NO V2 EXPERIMENT EXECUTED  
**Repository:** `salahealer9/meru-geometry-audit`  
**Branch:** `hebrew-projection-capacity-v0.9`  
**Required direct parent if signed next:** `22e3b1f622ef1e216ebb91a1746f6171da4f6f65` (signed Meru 3D-V1 result freeze)  
**Expected human GPG fingerprint:** `D4EC014EEFCC90E619D2AA59A91239ABCF512130`

## 1. Question, independence, and limits

For the *same target-blind candidate finite viewing-direction grids* defined in signed Meru 3D-V1, compute the **global spherical covering radius**

\[
\delta(G)=\max_{x\in S^2}\min_{n\in G}\arccos(x\cdot n)
          =\arccos\left(\min_{\|x\|=1}\max_{n\in G}x\cdot n\right).
\]

The inner maximum is the nearest-camera cosine, so the **minimum** over all unit directions determines the least well-covered point. This is *not* the minimum angular **separation** computed in V1. Test the nested families A (6/14/26 directions) and B (6/18/42 directions), keeping their exact signed and unoriented-axis conventions. These grids are mathematical design candidates, not recovered historical Meru camera prescriptions.

**Locked sources:** `docs/geometry/projection_orbit_results_v0_5.md`, `reports/v0_9/p0a2_target_blind_design/direction_family_candidates.md`, signed V1 protocol `docs/v0_9/meru_3d_v1_target_blind_viewing_direction_separation_protocol_2026_10_22.md`, and its signed result-freeze commit above. The signed QO2D-M1 scope and software-negative histories remain unchanged.

**Exclude:** Hebrew glyphs, target-derived coordinates or fonts, Meru candidate projections, physical shadows, renderer-dependent silhouettes, camera re-fitting to target images, target-vs-null comparisons, imported archived P0A3D/P1 software, alteration or rerunning of earlier experiments, and public-release software certification. No 3D object-specific effective-output count follows from direction coverage alone.

## 2. Exact finite sets and symmetry

Use the unchanged V1 integer-representative strata: `A0={±e_x,±e_y,±e_z}`, eight sign corners `C=(±1,±1,±1)/√3`, twelve sign edges `E=(±1,±1,0)/√2` and coordinate permutations, and 24 ratio-two directions `T=(±2,±1,0)/√5` and coordinate permutations. Families A: `A0`, `A0∪C`, `A0∪C∪E`; B: `A0`, `A0∪E`, `A0∪E∪T`.

All sets are invariant under independent coordinate sign changes and permutations. It therefore suffices to examine the closed fundamental chamber

\[
a\ge b\ge c\ge0,\qquad a^2+b^2+c^2=1.
\]

For a chamber vector `(a,b,c)` the maximum signed dot products contributed by the four strata are **exactly**

\[
H_{A0}=a,\quad H_C=(a+b+c)/\sqrt3,\quad
H_E=(a+b)/\sqrt2,\quad H_T=(2a+b)/\sqrt5.
\]

For each family/level, let `H_G` be the maximum of its applicable expressions. Every admitted set is antipodally closed, so `max_{n∈G}x·n=max_{[n]∈G/±}|x·n|`: **spherical and projective-axis covering radii coincide**, although signed direction counts and unoriented axis counts differ. This is an orthographic directional statement, not a physical-optics equivalence.

## 3. Elementary exact global-certification method

Avoid an uncontrolled numerical search over the sphere. By positive homogeneity, introduce the compact convex **chamber polytope**

\[
K_G=\{(a,b,c):a\ge b\ge c\ge0,\ H_G(a,b,c)\le1\}.
\]

Its bounding planes are chosen from:

- `a=b`, `b=c`, `c=0` (chamber boundaries);
- `a=1` (A0 support);
- `a+b+c=√3` (C support, family A G1/G2);
- `a+b=√2` (E support, family A G2 or family B G1/G2);
- `2a+b=√5` (T support, family B G2).

For every nonzero chamber unit vector `u`, `(u/H_G(u))∈K_G` and has norm `1/H_G(u)`. Conversely a maximal-norm point of `K_G` gives a worst-case unit direction. Consequently

\[
\rho(G):=\cos\delta(G)=\frac1{\max_{v\in K_G}\|v\|}.
\]

`K_G` is bounded (`0≤c≤b≤a≤1`) and convex. The convex squared norm attains its maximum at **at least one vertex**, so it suffices to enumerate every feasible intersection of triples of active bounding planes; discard rank-deficient triples, solve exact linear systems, check all inequalities exactly, and deduplicate **symbolically**. Do **not** certify global optimality solely by exhibiting one candidate witness, sampling a grid, or using decimal closeness to decide equality.

## 4. Frozen pre-run analytic expectations

The following are mathematical derivations made **before the proposed experimental script is executed**. They become fixed oracles only if this exact document is human-signed. Trivial common G0 is shown in both families.

| Grid | `|G|` / axes | Exact `max_{K_G}‖v‖²` | Exact covering cosine `ρ` | Covering radius, degrees (display only) |
|---|---:|---|---|---:|
| A G0 = B G0 | 6 / 3 | `3` | `1/√3` | 54.7356103172 |
| A G1 | 14 / 7 | `5−2√3` | `1/√(5−2√3)` | 36.2060231130 |
| A G2 | 26 / 13 | `9−2√2−2√6` | `1/√(9−2√2−2√6)` | 27.5692761305 |
| B G1 | 18 / 9 | `3/2` | `√(2/3)` | 35.2643896828 |
| B G2 | 42 / 21 | `3/2` | `√(2/3)` | 35.2643896828 |

**Worst-case chamber vertex `v`**, before normalizing to a unit direction:

- G0: `(1,1,1)`.
- A G1: `(1,√3−1,0)`.
- A G2: `(1,√2−1,√3−√2)`; note `1≥√2−1≥√3−√2≥0`.
- B G1/B G2: `(1/√2,1/√2,1/√2)`.

**Predicted number of distinct chamber-polytope vertices:** G0 `4`; A G1 `6`; A G2 `8`; B G1 `6`; B G2 `8`. The origin is included as a vertex. For an exact auxiliary vertex-census check, the **unordered multisets of squared vertex norms** are:

- G0: `{0,1,2,3}`.
- A G1: `{0,1,1,3−√3,3/2,5−2√3}`.
- A G2: `{0,1,1,1,6−2√6,4−2√2,3−√3,9−2√2−2√6}`.
- B G1: `{0,1,1,4−2√2,7−4√2,3/2}`.
- B G2: `{0,1,1,20−6√10,10−4√5,19−8√5,33−10√10,3/2}`.

The second-nearest A G2 maximal candidate has squared norm `3−√3`, only about `0.00464` below `9−2√2−2√6`: close alternatives must not be resolved by rough rounding.

**Special B result:** `G_B1⊂G_B2` implies `δ(B G2)≤δ(B G1)`. At the diagonal direction `(1,1,1)/√3`, nearest E-camera cosine is `√(2/3)` while nearest T-camera cosine is `3/√15=√(3/5)<√(2/3)`. Thus this same worst-case direction remains unfilled at B G2, forcing `δ(B G2)≥δ(B G1)`. **The radii are rigorously equal.** Increasing 18 to 42 signed cameras does not improve this particular worst-case coverage statistic. It can still affect other coverage measures.

These oracles specify mathematical targets, **not measured V2 outcomes**. They are not evidence of a source-derived Meru direction prescription, superiority of family A for Hebrew targets, or distinct projected letter counts.

## 5. One modest registered execution and evidence

1. **Preregister first:** the human reviews and signs **only this new Markdown file** in a one-file additive commit, with direct parent `22e3b1f622ef1e216ebb91a1746f6171da4f6f65` and GPG fingerprint above; push on the feature branch. Treat historical `DRAFT` text as archival once signed. No code or scientific experiment may be executed as part of signing.
2. **Prepare independent source:** one short, standalone Python 3.11 script **outside the repository**. Use exact symbolic operations for the six or seven small linear constraint systems and radical expressions (e.g. declared SymPy version if available); enumerate every three-plane intersection, check feasibility with exact sign/equality, deduplicate, compare squared norms exactly, and emit vertex lists and worst-case witnesses. No archived Meru candidate or V1 calculator imports. No Monte Carlo/sphere raster as a proof substitute. If a symbolic sign comparison cannot be decided, report **INCOMPLETE**, not a guessed Boolean. Independently inspect and record script SHA-256 before the first invocation; the human then separately approves running that exact source.
3. **Run once:** one registered execution, preserving command, signed commit + protocol Git blob, script and hash, Python/dependency versions, UTC times, complete JSON output, stdout/stderr, exit code and checksum manifest. Do not silently rerun, rewrite or tune. Repairs require a separately named attempt with original evidence preserved.
4. **Independent mathematical review:** verify the chamber reduction, compact-polytope equivalence, all feasible vertices (not only winners), exact maximum comparisons, global witnesses, the G0 identity across families, and B G1/B G2 equality using **independent** elementary algebra or separately written checks; do not import or reexecute submitted script. Approximate angles are supplementary only. Check all five distinct grids and both signed/axis conventions.
5. **Decision:** record `MERU_3D_V2_EXACT_FINITE_GRID_COVERING_RADIUS_PASS` only if every vertex count, exact norm multiset, maximum, witness and mathematical proof obligation agrees with the frozen oracle; otherwise `MERU_3D_V2_INCOMPLETE_OR_FAILED` with preserved deviations. A script reporting algebraic formulas is not by itself a proof; the independent polytope argument and all-vertex check are essential.

## 6. Subsequent question, not part of V2

After a successful signed V2 closeout, compare **object-specific projection equivalence** on independent generic 3D controls and the historically available candidate geometry with a common forward model, declared degeneracy policy and fair nuisance budget. This requires its own target-blind protocol. Neither finite-grid separation nor spherical covering establishes how many silhouettes are genuinely distinct under QO/SO(2) or whether any purported Hebrew correspondence is specific rather than flexible. All Hebrew images, glyph proxies, target-dependent tuning and statistical conclusions remain excluded here.
