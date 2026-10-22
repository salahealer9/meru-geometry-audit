# THIRD_REVIEW_BLIND_PROOF

**Package:** `MERU_3D_V5_R2_A1_THIRD_REVIEW_STAGE1_BLIND_MATH_2026-10-22.zip`
**Stage:** 1 — blind mathematical review. Generic symbolic mathematics only.
**Date:** 2026-10-22
**Reviewer role:** third reviewer, independent of the reviewer who proposed the SO(2)/O(2) orientation correction.
**Reviewer identity:** AI model, session configured as `claude-opus-5` (the serving model may differ from the configured identifier and may change mid-session; this is stated as a limit, not a credential).

## 0. Stage-1 input provenance

Only the Stage-1 package was opened. Its three documents hash as supplied:

```
920db57a8de187f39b4c69db96267183b5754e9feb9749a15b45b3aee3508880  00_READ_FIRST.md
15870070aae6cf25bc7897a2310f59ada004ea501a2ce38ee850a13e359384be  01_BLIND_MATH_CHALLENGE.md
dd954e6820aaeea5261cac1e041e9842ea55c4302090ec410682fde436fe0945  README.md
```

`sha256sum -c` verified all three. The archive contained **no** `02_OPEN_ONLY_AFTER_BLIND_PROOF/` directory, so no Stage-2 file was present to open.

**Material deliberately not read** (available to this session but left unopened, by the blind-first commitment):
the attached project's documents, which include `v5_r2/MERU_3D_V5_SECOND_INDEPENDENT_READ_ONLY_REVIEW_2026-10-22.zip.b64.txt`,
`v5_r2_a1/…FOCUSED_REQUALIFICATION…`, `v5_r2/checkpoints/CP2_FINDINGS_BEFORE_DELIVERABLES.md`,
`v5_r2_a1/checkpoints/A1_CP0_IDENTITIES.md`, `p0a3g*` archives; the repository `salahealer9/meru-geometry-audit`;
the amendment commit `9daaf5a7…` and its blob `a1ed423f…`. No project document was read or searched, no commit was
fetched, no prior reviewer script was executed. No Meru source curve, camera census, candidate/null test, Hebrew
material or V5B execution was touched. All proofs below were constructed from the challenge statement alone.

**Verification method.** Every algebraic claim was re-derived by hand and then independently re-checked with
generic symbolic computation (`sympy` 1.14.0) under `python3 -I`. All counterexamples are constructed in **exact
rational arithmetic**; no floating-point comparison is used anywhere in this report. Scripts: `t01.py`,
`t02_t03.py`, `t04.py`, `t05_t06.py`, `t07_extra.py`.

## 1. Verdict summary

| Item | Verdict | One-line result |
|---|---|---|
| **T01** | **PASS** | `B_t` is the projected Gram form and `D_t` the projected signed area, for *every* proper frame; antipodal normals always give exact planar mirror images, with `det R = −1` identically. |
| **T02** | **PASS (as stated)** / **FAIL under a trace reading** | True for arclength-synchronised parametrized congruence, with a regularity-free proof. False for point-set congruence: a circular arc is a counterexample. |
| **T03** | **PASS (obligation met); proposition INVALID with reversal** | Exact rational noncollinear counterexample: an isoceles "V" with `Fg = Rot(π)·Rg + (6/5,0)`. Characterisation: palindromic turning data. |
| **T04** | **PASS for `W≠0` under exact arclength quartiles; converse DISPROVED; FAIL for index/approximate quartiles** | `W` invariant under translation, SO(2) and reanchored reversal; negated by every improper isometry. `W=0` does **not** imply equality (exact counterexample). An index-quartile implementation can emit a **false UNEQUAL certificate**. |
| **T05** | **PASS with qualifications** | `G` complete for O(2); `(G,A)` complete for SO(2), the rank-≤1 case working only because `A≡0` and the two classes coincide there. Kernels are *not* reversal-invariant. Finite sampling can never certify EQUAL — exact counterexample given. |
| **T06** | **PASS, conditionally** | Closure consistency is a theorem *given* sound certificates, and doubles as an unsoundness detector. Certified bound `χ(H) ≤ N ≤ k`. |
| **T07** | **PASS — three genuine counterexamples found**, one of them a soundness break | See §8. |
| **T08** | **PASS** | §9–§11. |

**The central mathematical content of the SO(2)/O(2) correction is confirmed.** The correction is not merely
defensible, it is forced: `B_t` is blind to orientation by construction (§2.4). The findings below do not
overturn it; they bound its scope and expose one soundness-critical precondition that Stage 1 cannot check.

## 2. T01 — projected Gram form, signed determinant, antipodal normals

### 2.1 Setting without coordinate specialisation

Let `t ∈ Z³ \ {0}`, `n = t/‖t‖`, and let `(e1,e2,n)` be a positively oriented orthonormal 3-frame, i.e. the
matrix `M` with rows `e1ᵀ, e2ᵀ, nᵀ` lies in `SO(3)`. Projection is `p_t(X) = (e1·X, e2·X)`.

To avoid any convenient choice, the symbolic check parametrizes `M` by a **full quaternion parametrization of
SO(3)** — polynomial entries over `(w,x,y,z) ≠ 0`, reaching every element of `SO(3)` and hence every proper frame —
and then *additionally* applies an arbitrary camera roll `(cos φ, sin φ)`. Both were verified orthogonal with
`det = +1`.

### 2.2 The projected Gram form is exactly `B_t`

`e1e1ᵀ + e2e2ᵀ = I − nnᵀ = P`, the orthogonal projector onto `n^⊥`, because `{e1,e2}` is *any* orthonormal basis
of `n^⊥`. Hence

```
p_t(U)·p_t(V) = Uᵀ(e1e1ᵀ + e2e2ᵀ)V = U·V − (n·U)(n·V) = U·V − (t·U)(t·V)/(t·t) = B_t(U,V).     (1)
```

Verified symbolically for the generic quaternion frame and for arbitrary roll `φ`. **Note what this proves:
`B_t` is invariant under the full `O(2)` of in-plane frame changes.** It cannot distinguish a proper frame from
an improper one. This is the precise sense in which a Gram-only pipeline silently implements `O(2)`.

### 2.3 The signed determinant is exactly `D_t`

With `M ∈ SO(3)`, for any `U,V`: `det[MU | MV | Mn] = det(M)·det[U | V | n] = det[U|V|n] = n·(U×V)`.
Since `Mn = (0,0,1)ᵀ`, cofactor expansion along the third column leaves exactly the 2×2 minor
`(e1·U)(e2·V) − (e1·V)(e2·U)`. Therefore

```
det(p_t(U), p_t(V)) = n·(U×V) = t·(U×V)/√(t·t) = D_t(U,V).                                     (2)
```

The proof uses **only** `det M = +1`; it never selects a basis. Verified symbolically for the generic quaternion
frame and arbitrary roll. For a negatively oriented frame the same computation gives `−D_t`.

### 2.4 The orientation bit, isolated

```
B_t(U,U)·B_t(V,V) − B_t(U,V)² = D_t(U,V)².                                                     (3)
```
Verified symbolically. (3) is the cleanest statement of the whole correction: **the Gram form determines `|D_t|`
and nothing more; the sign of `D_t` is precisely the extra datum that `SO(2)` retains and `O(2)` discards.**
Any pipeline whose invariants are functions of `B_t` alone is mathematically incapable of separating a view from
its mirror, regardless of implementation quality.

### 2.5 Signs under `t → −t`

```
B_{−t} = B_t      (even in t)
D_{−t} = −D_t     (odd in t)
```
Both verified symbolically.

### 2.6 Antipodal projections are mirror images up to proper roll — PROVED

Let `A = (e1,e2,n)` and `A' = (f1,f2,−n)` be *any* two positively oriented frames for `n` and `−n`. Define
`R_{ij} = f_i·e_j`, `i,j ∈ {1,2}`. Since `{e1,e2}` and `{f1,f2}` are orthonormal bases of the same plane `n^⊥`,
`R ∈ O(2)` and `p_{−t}(X) = R·p_t(X)` pointwise (both frames annihilate the `n`-component). With `M, M' ∈ SO(3)`,

```
M' Mᵀ = [[R, 0], [0, −1]]   ⟹   +1 = det(M'Mᵀ) = −det R   ⟹   det R = −1.                     (4)
```

So **`R` is an improper planar isometry for every admissible pair of proper frames** — never merely for a
convenient one. Symbolically, the complete family of proper frames for `−n` is the roll family of `(e1,−e2,−n)`
(itself verified proper), giving `R = [[c, −s], [−s, −c]]` with `det R = −(c²+s²) = −1` identically, and
`p_{−t} = R p_t` pointwise. Consistency with §2.5: `D_{−t} = det R · D_t = −D_t`. ✔

**T01: PASS.** The projection along `−n` is the planar mirror image of the projection along `n`, up to a proper
camera roll, with no residual choice of frame able to change that.

### 2.7 Consequence for a direction census (derived, not computed)

`B_t` and `D_t` depend on `t` only through `n`, so `B_{ct} = B_t` and `D_{ct} = D_t` for every `c > 0`. A census
over `t ∈ Z³` must therefore be reduced to **primitive** representatives or the same projection is counted with
`gcd`-multiplicity. And `±t` give exact mirror images, so under `SO(2)` the antipodal pair must **not** be
identified a priori — nor automatically separated (see §4.3, §8.1). *No census was performed; this is a corollary
of (1)–(4).*

## 3. T02 — reflection congruence without traversal reversal

**Proposition.** For nonconstant open projected curves `g: [0,L] → R²` and `F` a planar isometry with
`det = −1`: `g` and `Fg` are `SO(2)`-congruent **iff** `dim aff span g ≤ 1`.

Read as stated in the package — `g` is "an arclength-indexed rectifiable nonconstant planar map", and the
equivalence is translation plus `SO(2)` — "`SO(2)`-congruent" means: `∃ Q ∈ SO(2), c ∈ R²` with
`Fg(s) = Q g(s) + c` **for all `s ∈ [0,L]`** (same parameter; no reversal; no scaling).

### 3.1 (⟸) rank ≤ 1 implies congruent

`g` nonconstant with `dim aff span ≤ 1` means `dim = 1`: `g(s) = a + φ(s)u`, `u` a unit vector, `φ` nonconstant.
Write `F(x) = Sx + b`, `S` orthogonal with `det S = −1`. Pick `Q ∈ SO(2)` with `Qu = Su` (a rotation carrying one
unit vector to another always exists — verified symbolically: `β = ψ − 2α` for the generic reflection of angle
`ψ` and `u` of angle `α`) and `c = Sa + b − Qa`. Then for all `s`:

```
Q g(s) + c = Qa + φ(s)Qu + Sa + b − Qa = Sa + b + φ(s)Su = F(a + φ(s)u) = Fg(s).   ✔
```

### 3.2 (⟹) congruent implies rank ≤ 1

Suppose `Fg(s) = Q g(s) + c` for all `s`, with `F(x) = Sx + b`. Then `(S − Q) g(s) = c − b` for all `s`, so
`g([0,L])` lies in the solution set of a fixed linear system. Factor `S − Q = Q(A − I)` with `A = Q⁻¹S`
orthogonal, `det A = −1` — a reflection, eigenvalues `{+1, −1}`. Hence `A − I` has eigenvalues `{0, −2}`:
**rank exactly 1**, verified symbolically (`det(A−I) ≡ 0` identically, `A−I ≢ 0`, eigenvalues `{−1,+1}` for `A`).
The solution set of `(A−I)x = w` is therefore empty or a coset of the one-dimensional `+1`-eigenline. It is
nonempty (it contains `g(0)`), so it is an affine **line**, and `dim aff span g ≤ 1`. ✔

**T02: PASS.** Both directions hold.

### 3.3 Translation, zigzags, arclength correspondence — addressed explicitly

- **Translation.** Handled intrinsically: the proof never assumes `F` is linear; the translation parts of `F` and
  of the congruence combine into the single constant `c − b`, which is why the conclusion is about the **affine**
  span, not the linear span.
- **Rank-one zigzags.** A rank-one curve need not be injective, monotone or `C¹`. Verified: for
  `g(s) = (φ(s), 0)` with `φ` an arbitrary zigzag, `F₁ = diag(1,−1)` gives `F₁g = g` (take `Q = I`), and
  `F₂ = diag(−1,1)` gives `F₂g = Rot(π)·g` with `det Rot(π) = +1`. So zigzags *are* `SO(2)`-congruent to their
  mirrors. This is the case that defeats the tempting "tangent-angle is constant ⟹ straight segment" argument:
  a zigzag has tangent angle constant mod `π` but not mod `2π`, and admits no continuous tangent-angle lift.
  **The §3.2 proof is regularity-free** — it assumes nothing beyond `g` being a map — and therefore handles
  zigzags, corners, cusps, non-injectivity and non-rectifiable pathology correctly. Any proof routed through
  curvature or a turning function does **not**, and would mis-handle exactly this case. If the amendment's proof
  is curvature-based, that is a gap to check at Stage 2.
- **Arclength correspondence.** `F` is an isometry, so `Fg` is arclength-indexed with the same `L`; the
  parameter correspondence `s ↔ s` is forced, not chosen. **Lemma:** if `g` and `g∘σ` are both arclength-indexed
  on `[0,L]` with `σ` monotone onto, then `|σ(b) − σ(a)| = b − a` for all `a,b`, so `σ` is an isometry of
  `[0,L]`, i.e. `σ(s) = s` or `σ(s) = L − s`. Hence the package's "permissible monotone reparametrization is
  absorbed by arclength" is **correct**, and the residual freedom is **exactly one bit: traversal reversal**,
  which is why T03 is a genuinely separate question and must be declared, never inferred.

### 3.4 The proposition is FALSE under a trace (point-set) reading — counterexample

If "congruent" is read as congruence of the **image sets**, the proposition fails. Take the circular arc
`g(s) = (ρ cos(s/ρ), ρ sin(s/ρ))`, verified arclength-indexed (`‖g'‖ = 1`). Its trace is noncollinear, yet the
mirror image of a circular arc is a congruent circular arc of the same radius and angular span, which a rotation
carries onto the original — set-level congruence holds.

At the **parametrized** level it correctly fails: signed curvature is `+1/ρ` for `g` and `−1/ρ` for `Fg`
(both computed symbolically), and signed curvature as a function of arclength is a translation+`SO(2)` invariant.

**This is a real and consequential ambiguity, not a quibble.** The package's definition ("arclength-indexed …
planar map") selects the parametrized reading, under which T02 is true. But any implementation step that compares
traces as point sets — point-cloud matching, Hausdorff/Chamfer distance, convex-hull or shape-descriptor
comparison, rasterised overlap, sorted-point canonicalisation — silently reverts to the set reading, under which
the proposition is false and mirror pairs can be wrongly merged. **Recorded as unresolved assumption A1.**

## 4. T03 — the proposition with traversal reversal permitted

### 4.1 Why it must fail

With reversal `Rg(s) = g(L−s)` admitted, the equivalence is generated by translations, `SO(2)` and `R`
(a group: `R` is an involution and commutes with the isometries up to relabelling, acting on fixed-`L` curves).
Both reflection and reversal reverse orientation of the turning data, so their composition preserves it and can
be absorbed. For a curve with a tangent-angle lift `θ(s)`: `Fg` has angle `−θ(s) + const`, `Rg` has
`θ(L−s) + π`. So `Fg ≅_{SO(2)} Rg` iff `θ(s) + θ(L−s)` is constant, i.e. `κ(s) = κ(L−s)`:
**palindromic curvature**. Rank ≤ 1 is then sufficient but far from necessary.

### 4.2 Exact rational noncollinear counterexample

Isoceles "V", two unit segments, rational vertices:

```
v0 = (0,0)        v1 = (3/5, 4/5)        v2 = (6/5, 0)
|v1−v0| = |v2−v1| = 1   (exactly);   det(v1−v0, v2−v0) = −24/25 ≠ 0  ⟹  NONCOLLINEAR
```

With `F(x,y) = (x,−y)` and `Rg = (v2, v1, v0)`, solving `Q·Rg_i + c = Fg_i` exactly over `Q ∈ SO(2)` gave the
unique solution

```
Q = Rot(π) = −I  (det = +1, verified),   c = (6/5, 0),   satisfied at EVERY vertex.
```

So `Fg = Rot(π)·Rg + (6/5, 0)` **exactly**. The same exact solve **without** reversal returns the empty set,
confirming the curve is not mirror-congruent without reversal — consistent with T02.

### 4.3 Characterisation, verified

For a polyline with segment lengths `ℓ` and turning angles `β` (a complete translation+`SO(2)` invariant):
reflection ↦ `(ℓ, −β)`; reversal ↦ `(reverse ℓ, −reverse β)` — the reversal action verified symbolically on a
concrete polyline via exact unit-complex turning ratios (conjugation = angle negation). Hence

```
Fg ≅_{SO(2)} g    ⟺  every β_i ∈ {0, π}        (collinear)
Fg ≅_{SO(2)} Rg   ⟺  ℓ palindromic AND β palindromic
```

Any single-vertex curve has a trivially palindromic turning sequence, so **every** isoceles two-segment curve is
a counterexample; so is every circular arc, and every curve with a mirror symmetry about its arclength midpoint.
The counterexample family is large, not exotic.

**T03: obligation met. The T02 proposition is INVALID once reversal is permitted** — sufficiency survives,
necessity fails. The reversal policy is therefore load-bearing for class counts and must be declared per branch
and per comparison. **Recorded as unresolved assumption A2.** Note the direction of the risk: curves with
mirror-symmetric projections are exactly what highly symmetric source geometry tends to produce, so the
palindromic class is unlikely to be empty in practice.

## 5. T04 — the `W` witness

`W(g) = det(m−o, e−o) · (‖q1−o‖² − ‖q3−e‖²)`, with `o=g(0), e=g(L), m=g(L/2), q1=g(L/4), q3=g(3L/4)`.

### 5.1 Exact transformation laws (generic symbolic sample points)

| transformation | effect on `W` | verified |
|---|---|---|
| (a) translation `g+τ` | `W` unchanged | `W(g+τ) − W(g) = 0` identically |
| (b) proper rotation `Qg`, `Q ∈ SO(2)` | `W` unchanged | `0` after `q_s² → 1−q_c²` |
| (c) mirror `Fg`, any `det = −1` isometry `Sx+b` | `W ↦ −W` | `W(Fg) + W(g) = 0`, including the translation part |
| (d) reanchored reversal `Rg` | `W` unchanged | `W(Rg) − W(g) = 0` identically |

Mechanism of (d): `s ↦ L−s` relabels the samples as `o′=e, e′=o, m′=m, q1′=q3, q3′=q1`. The determinant factor
flips sign (swapping two vertices of the triangle `(o,m,e)` reverses its signed area) **and** the norm factor
flips sign (`‖q3−e‖² − ‖q1−o‖²`). The two sign flips cancel. Both flips were verified separately. The design is
sound and the cancellation is exact, not approximate.

### 5.2 `W ≠ 0` is a sound `SO(2)`-antipodal witness, even with reversal — PROVED

Let `G = ⟨translations, SO(2), R⟩`. By (a),(b),(d), `W` is `G`-invariant. By (c), every improper isometry negates
it. If `g` were congruent to `Fg` under `G` — i.e. `Fg = Qg + c` or `Fg = Q·Rg + c` — then `W(Fg) = W(g)`, while
(c) gives `W(Fg) = −W(g)`. Hence `W(g) = −W(g)`, so `W(g) = 0`. Contrapositive:

```
W(g) ≠ 0   ⟹   g is NOT congruent to Fg under translations + SO(2), with or without reversal.   ✔
```

Composing with §2.6 (`p_{−t} = R_refl ∘ p_t`, `det R_refl = −1`), `W(p_t(curve)) ≠ 0` certifies
`p_t ≁ p_{−t}` under `SO(2)`. The chain closes. Note `W ≠ 0` forces noncollinearity automatically (a collinear
curve has `det(m−o, e−o) = 0`), and `W ≠ 0` says nothing about `O(2)` classes — `g` and `Fg` are always
`O(2)`-congruent. `W` is specifically an orientation witness, which is the right instrument.

### 5.3 `W = 0` does **NOT** imply equality — exact rational counterexample

`W = 0` is *necessary* for congruence (§5.2) but not sufficient. Four unit segments with rational directions
`(1,0), (3/5,4/5), (4/5,3/5), (24/25,7/25)`, arranged so that `o, m, e` are collinear:

```
v = (0,0), (1,0), (8/5,4/5), (12/5,7/5), (84/25,42/25)      all segment lengths exactly 1, L = 4
det(m−o, e−o) = 0    ⟹    W(g) = 0
```

Exact congruence solves over `Q ∈ SO(2)`, `c`:

```
g  → Fg   : no solution   (empty)
Rg → Fg   : no solution   (empty)
```

so `g` is **not** congruent to its mirror with or without reversal, yet `W(g) = 0`. Independent cross-check by
exact turning data: turning unit-complexes `3/5 + 4i/5`, `24/25 − 7i/25`, `117/125 − 44i/125`; `β₁ ≠ β₃`
(non-palindromic) and not all `β_i ∈ {0,π}` (noncollinear) — both conclusions reached in exact arithmetic with no
floating point.

Consistency check in the other direction: the reversal-congruent isoceles V of §4.2 has `W = 0` exactly, as the
theorem requires.

**Conclusion: `W` is a strictly one-sided, fail-closed witness.** `W ≠ 0` ⟹ UNEQUAL (sound). `W = 0` ⟹
**no information**; it must map to `UNRESOLVED_PAIR` and never to `EQUAL`. Any code path treating `W = 0` as
evidence of equality, or using `|W|` as a similarity score, is unsound.

### 5.4 FAIL — the invariance theorem does not survive index-based quartiles

§5.1(d) is a theorem about **exact arclength** quartiles; it relies on `{L/4, L/2, 3L/4}` being setwise
invariant under `s ↦ L−s`. Replace it with "quartiles by point index" and the symmetry breaks. On a
non-uniformly sampled 6-point polyline:

```
W by point index, forward  = 7/2
W by point index, reversed = 4            ⟹ NOT reversal-invariant
```

This is worse than a loss of elegance — **it breaks soundness and can emit a false UNEQUAL certificate.** The
`W ≠ 0` proof needs `W(Rg) = W(g)`. Without it, `−W(g) = W(Rg)` can hold with `W(g) ≠ 0`, i.e. a curve that *is*
reversal-congruent to its mirror can score `W ≠ 0`. Demonstrated on the isoceles V of §4.2 — a curve **proved**
congruent to its mirror via `Rot(π)` + reversal — sampled with one extra vertex on the first segment only:

```
sample list              : (0,0), (3/20, 1/5), (3/5, 4/5), (6/5, 0)
index-based W            = 6/25   ≠ 0      → would certify UNEQUAL
true arclength-quartile W = 0              → correctly UNRESOLVED
curve is in fact congruent to its mirror: Q = Rot(π), c = (6/5,0)   [exact]
```

**T04 verdict: `W ≠ 0` PASS under exact arclength quartiles; converse DISPROVED; FAIL for any
index-based or approximate-parameter quartile implementation.** This is the single most actionable finding of
this review, and it is an implementation precondition Stage 1 cannot check. **Recorded as C3/A5.**

### 5.5 Further structural requirements on `W`

- The quartile sample set must be **exactly symmetric** under `s ↦ L−s`. `{L/4, L/2, 3L/4}` qualifies;
  `{L/3, 2L/3}` would too; a mixed convention (e.g. `m` by index, `q1,q3` by arclength) does not.
- `W` is degree-4 homogeneous, hence **not scale-invariant**. Harmless while scaling is forbidden, but any
  length normalisation or unit change rescales `W` by `λ⁴`, so no absolute threshold on `|W|` is meaningful
  across curves. Only vanishing/non-vanishing and sign carry information.
- "Certified `W ≠ 0`" must mean exact or interval-certified. In floating point, `W` is a difference of products
  of coordinate differences and will be a small nonzero number for a genuinely mirror-congruent curve. **A
  floating-point `W ≠ 0` is not a certificate**; it needs exact rational/algebraic arithmetic or a rigorous
  interval bound `|W| > ε_bound` with a proven error model. **Recorded as A4.**
- `W` requires a genuine arclength parametrization with `L > 0`; constant traces have no `L` (see §7.4).

## 6. T05 — completeness of the anchored Gram and determinant kernels

Let `v(s) = g(s) − g(0)`, `G(s,t) = v(s)·v(t)`, `A(s,t) = det(v(s), v(t))`, on the full `[0,L]²`.
Equality of `L` is a precondition: isometries preserve length, so `L` is itself an invariant and curves of
different length are automatically UNEQUAL — the cheapest sound witness available, and one that is lost if
curves are length-normalised (**A8**).

### 6.1 Necessity

Verified symbolically: `G` is invariant under both rotations and reflections (hence under all of `O(2)`);
`A` is invariant under rotations and **negated** by reflections. So `G` is an `O(2)` invariant and
`(G, A)` an `SO(2)` invariant. Necessity holds. Anchoring at `s = 0` is without loss of generality: any
parameter-respecting translation+`O(2)` congruence necessarily maps `g(0)` to `g′(0)`.

### 6.2 Sufficiency for `O(2)`

Suppose `G = G′`. Define a linear map on `span{v(s)}` by `v(s) ↦ v′(s)`. It is well defined and isometric: for
any finite combination, `‖Σ aᵢ v′(sᵢ)‖² = Σ aᵢaⱼ G′(sᵢ,sⱼ) = Σ aᵢaⱼ G(sᵢ,sⱼ) = ‖Σ aᵢ v(sᵢ)‖²`, so the kernel is
preserved and norms match. Extend the isometry of the span to all of `R²` by completing an orthonormal basis,
giving `Q ∈ O(2)` with `v′ = Qv`, hence `g′ = Qg + c`, `c = g′(0) − Qg(0)`. **`G` is complete for
translation + `O(2)`.** ✔

### 6.3 Sufficiency for `SO(2)` — and why the rank-one case needs separate words

- **Rank 2.** The isometry of the span extends **uniquely** to `R²`, so `Q` is uniquely determined and `det Q`
  is forced. Given also `A′ = A` with `A ≢ 0`, from `A′ = det Q · A` we get `det Q = +1`, so `Q ∈ SO(2)`. ✔
- **Rank ≤ 1.** Then `A ≡ 0` identically (determinants of pairwise-parallel vectors), verified, so `A` carries
  **no** information and cannot force `det Q = +1`. Completeness nevertheless holds, but for a different
  reason: by T02 (§3.1) a rank-≤1 curve is `SO(2)`-congruent to its own mirror, so the `O(2)`-class and the
  `SO(2)`-class **coincide**, and §6.2 already suffices.

**`(G, A)` is complete for translation + `SO(2)`, in all ranks** — but the proof is case-split, and the
rank-≤1 case is sound only because of T02. A pipeline that claims `(G,A)` completeness while *also* treating
`A ≡ 0` as evidence of anything orientation-related is confusing the two cases. `A ≡ 0` is exactly the
degenerate-rank flag, not an orientation verdict.

### 6.4 Reversal and reanchoring: the kernels are NOT reversal-invariant

Reversal moves the anchor from `g(0)` to `g(L)`. With `v_R(s) = g(L−s) − g(L) = v(L−s) − v(L)`:

```
G_R(s,t) = G(L−s, L−t) − G(L−s, L) − G(L, L−t) + G(L, L)
A_R(s,t) = A(L−s, L−t) − A(L−s, L) − A(L, L−t)                [A(L,L) = 0]
```

Both identities verified exactly on a concrete 5-point curve over the whole sample grid. Consequence: the
kernels are computable under reversal but **not invariant** under it. A reversal-permitting equivalence test
must explicitly check all four combinations `(identity / reversal) × (A / −A)`; it cannot be inferred from a
single kernel comparison. **Recorded as A2.**

### 6.5 Finite sampling can never certify EQUAL — exact counterexample

Let `g` and `g′` be these polylines, both of total length exactly 4:

```
g  : (0,0), (3/10,  2/5), (3/5,0), (8/5,0), (11/5,4/5), (3,7/5)
g′ : (0,0), (3/10, −2/5), (3/5,0), (8/5,0), (11/5,4/5), (3,7/5)
segment lengths both (1/2, 1/2, 1, 1, 1)
```

`g′` is `g` with the first sub-arc reflected across its own chord. At the sample parameters `s ∈ {0,1,2,3,4}` the
two curves are **pointwise identical** (verified exactly), so `G`, `A` **and** `W` agree exactly on the entire
`5×5` grid. Yet exact congruence solves give:

```
g → g′   (no reversal) : empty      g → Rg′  (reversal) : empty
```

(the reversal case is additionally excluded because the length sequence `(1/2,1/2,1,1,1)` is not palindromic).
**Two non-congruent curves of equal length, indistinguishable by any finite sampled kernel containing those
parameters.** The construction generalises to any finite sample set — reflect any sub-arc between consecutive
samples across its chord; the samples and `L` are preserved, the congruence class generically is not.

Therefore: finite sampled kernels can **falsify** (a single exactly-certified mismatch is a rigorous UNEQUAL
witness) but can **never verify**. The correct strengthening: if the kernels agree on a **countable dense**
subset of `[0,L]²` and the curves are continuous, they agree everywhere by continuity, and §6.2–6.3 apply. Dense
suffices; finite never does. Any "PASS at N samples" claim about a continuous theorem is a category error.

**T05: PASS with the qualifications above.**

## 7. T06 — fail-closed logic and class counting

### 7.1 Closure consistency is a theorem, given sound certificates

Let `~` be true congruence (an equivalence relation on the admissible curves — verified: the transformations
`{g ↦ Q g(σ(s)) + c : Q ∈ SO(2), σ ∈ {id, L−s}}` form a group acting on fixed-`L` curves, so the
reversal-permitting relation is an equivalence too). Let `E ⊆ ~` be the EQUAL certificates and
`U ⊆ complement(~)` the UNEQUAL certificates. The reflexive-symmetric-transitive closure of a subrelation of an
equivalence relation stays inside it, so `E* ⊆ ~`, hence

```
E* ∩ U = ∅.
```

So the requirement "equivalence closure must never contradict an UNEQUAL certificate" is **automatically
satisfied** — it is a theorem, not an extra constraint to enforce. Its contrapositive is the useful part:

```
E* ∩ U ≠ ∅   ⟹   at least one certificate in E ∪ U is UNSOUND.
```

**This makes the no-contradiction check a genuine unsoundness detector, and it should be run as such rather
than assumed.** Given §6.5, the most likely source of a bad `E` entry is a finitely-sampled EQUAL; given §5.4,
the most likely source of a bad `U` entry is an index-quartile `W`.

### 7.2 Soundness of the three-valued status

- `EQUAL` only after a whole-curve proof — **sound and necessary**, by §6.5.
- `UNEQUAL` only with a rigorous witness — **sound**; admissible witnesses are `L` mismatch (§6), exactly
  certified kernel mismatch (§6.5), and `W ≠ 0` under exact arclength quartiles (§5.2).
- otherwise `UNRESOLVED_PAIR` — **sound**, and this is where `W = 0` must land (§5.3).

The three-valued design is correct. The asymmetry (cheap falsification, expensive verification) is intrinsic to
the problem, not a weakness of the protocol.

### 7.3 Certified class-count bounds

`E*` partitions the candidates into `k` blocks; each block lies inside a single true class, so `N ≤ k`. Build a
graph `H` on blocks with an edge whenever some `U`-pair joins two blocks. A true class assignment is a **proper
colouring** of `H`, so `N ≥ χ(H) ≥ ω(H)`. Certified bound:

```
χ(H) ≤ N ≤ k          (ω(H) a computable lower bound when χ is impractical)
```

Toy check: 4 blocks with `U`-edges `{B1B2, B2B3, B1B3}` gives `ω = 3`, `χ = 3`, bound `3 ≤ N ≤ 4`. Note the
correct lower bound is the **chromatic** number, not the clique number; reporting `ω` as the bound is sound but
may be loose, and reporting the number of `U`-edges or `U`-pairs would be wrong.

**T06: PASS, conditionally** — the logic is sound *given* per-certificate soundness, which is precisely what
§5.4, §6.5 and A1–A3 put at issue.

### 7.4 Rank-zero / NOT_EVALUABLE

An arclength-indexed curve has unit speed a.e., so it cannot be constant on a set of positive measure; a
"constant projected trace" means the 3D curve lies in a line parallel to `n`, giving `L = 0`, which the
package's own definition (nonzero `L`) excludes. `NOT_EVALUABLE` is therefore the mathematically correct
default. A declared rank-zero policy would be *sound* (all single points are congruent, and `O(2)`/`SO(2)`
classes coincide trivially) but **uninformative and potentially misleading**: it would make degenerate traces
from different viewing directions mutually EQUAL, inflating `E` with content-free merges that then propagate
through `E*` (§7.1). Keeping them out of the pairing logic entirely is the safer choice. **Recorded as A7.**

## 8. T07 — adversarial results

Three genuine counterexamples were found, plus two structural soundness gaps. None disproves the core
`SO(2)`/`O(2)` correction; one disproves a converse the protocol might rely on, and one breaks an
implementation-level soundness claim.

### 8.1 Counterexample 1 — T02's proposition fails under reversal (§4.2)
Exact rational noncollinear curve with `Fg = Rot(π)·Rg + (6/5,0)`. **Consequence:** neither blanket antipodal
rule is sound. "Always identify `±t`" is the original `O(2)` error (under-counts). "Never identify `±t`"
**over-counts**: it fails for rank-≤1 projections always, and for palindromic projections whenever reversal is
permitted. Only a certified per-pair test is sound, and the palindromic class is favoured by symmetric source
geometry.

### 8.2 Counterexample 2 — `W = 0` does not imply congruence (§5.3)
Exact rational 4-segment curve with `W = 0`, proved non-congruent to its mirror with and without reversal.
**Consequence:** `W = 0` must route to `UNRESOLVED_PAIR`, never to `EQUAL`, and `|W|` is not a similarity score.

### 8.3 Counterexample 3 — finite sampling cannot certify EQUAL (§6.5)
Two exactly-specified non-congruent curves of equal length with identical `G`, `A` and `W` on the whole sample
grid. **Consequence:** no finite-sample PASS of a continuous theorem; dense + continuity is the minimum
strengthening.

### 8.4 Soundness gap A — false UNEQUAL from index quartiles (§5.4)
Demonstrated: a curve **proved** congruent to its mirror scores index-based `W = 6/25 ≠ 0` while its true
arclength `W = 0`. **This is a false certificate, i.e. an unsound `U` entry**, the one thing §7.1 says must never
happen. Must be checked against the actual implementation at Stage 2.

### 8.5 Soundness gap B — "branchwise" equivalence (§10, A3)
The package permits the equivalence "explicitly branchwise". Independent isometries per branch do **not** compose
into a single planar isometry: rotating one branch and rotating another by a different angle is not realisable by
any one camera roll. So per-branch EQUAL does **not** establish congruence of the whole projected figures. The
converse direction is also affected: with `k` branches, an UNEQUAL verdict on the whole figure must rule out all
`k!` branch matchings, so a single per-branch `W ≠ 0` certifies whole-figure inequivalence **only** once the
matching is canonically fixed and that fixing is itself certified. The fail-closed asymmetry inverts for
multi-branch figures, which the protocol as stated does not appear to account for.

### 8.6 Assumptions I tried to weaken and failed to break

- **T01 (§2.2–2.6).** Attacked by generalising the frame (full quaternion `SO(3)` + arbitrary roll) rather than
  picking coordinates. The result is forced by `det M = +1` alone. No counterexample exists; the only residual
  risk is a **convention** error, not a mathematical one: `D_t`'s sign depends on building the frame as
  `(e1, e2 = n × e1, n)` — verified proper, since `det[e1; n×e1; n] = e1·((n×e1)×n) = ‖e1‖² = 1`. Using
  `e2 = e1 × n` silently flips every `D_t` and inverts every orientation verdict while leaving `B_t` untouched
  and all `|D_t|` self-consistent — a sign error that no Gram-based self-check can detect. **Recorded as A6.**
- **T02 (⟹).** Tried to find a nonconstant noncollinear curve satisfying `(S−Q)g(s) = const`. Impossible:
  `rank(A−I) = 1` exactly, for every reflection. Tried to exploit missing regularity (zigzags, non-injective,
  cusps) — the proof is regularity-free, so these do not touch it; they only break *other* proof strategies.
  Tried to find an orientation-preserving reparametrization loophole — closed by the §3.3 lemma. The only way
  the proposition falls is by changing the **reading** (trace vs parametrized, §3.4) or the **group**
  (reversal, §4) — both of which I did break.
- **Scale prohibition.** Probed whether forbidding positive scale hides a loophole. It does not, and the
  prohibition is not load-bearing: `det(S − λQ) = (λ−1)(λ+1)`, so for `λ > 0, λ ≠ 1` the matrix is
  **invertible** and `(S − λQ)g(s) = const` forces `g` constant. With scale admitted, a nonconstant curve is
  never mirror-congruent at all. Forbidding scale is thus *conservative*; its real function is to preserve `L`
  as an invariant (§6, A8).
- **What remains undecidable or computation-dependent.** Exact congruence of two general analytic curves is not
  decidable from any finite amount of sampled data (§6.5); it is decidable for restricted classes
  (polylines with exact rational data, as every counterexample here demonstrates) and semi-decidable in the
  falsifying direction generally. `χ(H)` in §7.3 is NP-hard in general, so the lower class-count bound is
  computation-dependent and will usually be reported via `ω(H)` or a fractional relaxation. Certification of
  `W ≠ 0` and of kernel mismatch is arithmetic-dependent (exact vs interval vs floating point) — in floating
  point these are **not** certificates (A4).

**No empirical finite-sample PASS is asserted anywhere in this report.** All positive results are proofs over
generic symbols; all negative results are exact-arithmetic counterexamples.

## 9. T08 — source-independent proof statement

Let `t ∈ R³ \ {0}`, `n = t/‖t‖`, and let `p_t` be orthographic projection into a positively oriented orthonormal
camera frame `(e1,e2,n)`. Let curves be arclength-indexed rectifiable nonconstant maps `g: [0,L] → R²`, `L > 0`,
compared up to translation and `SO(2)`, scaling forbidden, reversal admitted or not by explicit declaration.

1. `p_t(U)·p_t(V) = B_t(U,V)` and `det(p_t(U), p_t(V)) = D_t(U,V)`, for **every** proper frame. `B_t` is
   `O(2)`-invariant; `D_t` is `SO(2)`-invariant and sign-flipped by improper frames.
2. `B_t(U,U)B_t(V,V) − B_t(U,V)² = D_t(U,V)²`. The Gram form determines `|D_t|` and nothing more; the sign of
   `D_t` is exactly the orientation datum. `B_t` is even in `t`, `D_t` is odd in `t`.
3. For every pair of proper frames for `n` and `−n`, `p_{−t} = R p_t` with `det R = −1`. Antipodal views are
   exact planar mirror images up to proper roll.
4. Without reversal, `g ≅_{SO(2)} Fg` **iff** `dim aff span g ≤ 1`. Proof is regularity-free. True for the
   parametrized reading; **false** for a point-set reading.
5. With reversal, (4) fails: necessity is lost. For piecewise-`C¹`/BV curves, `g ≅ Fg` under
   `⟨translations, SO(2), reversal⟩` iff the curve is collinear **or** its turning data is palindromic
   (`ℓ` and `β` palindromic; equivalently `κ(s) = κ(L−s)`).
6. `W` is invariant under translation, `SO(2)` and reanchored reversal, and negated by every improper isometry,
   **provided** the quartile samples are exact arclength and symmetric under `s ↦ L−s`. Hence certified
   `W ≠ 0` ⟹ `g ≁ Fg` even with reversal. The converse is false. Under non-arclength quartiles the invariance
   fails and `W ≠ 0` can be a false certificate.
7. Complete anchored `G` on `[0,L]²` (with `L` matched) is necessary and sufficient for translation+`O(2)`
   congruence. `(G,A)` is necessary and sufficient for translation+`SO(2)`, via rank 2 uniqueness, with the
   rank-≤1 case holding because `A ≡ 0` and the two classes coincide there by (4). Kernels are not
   reversal-invariant; they transform by the explicit formulas of §6.4. Finite sampling cannot certify
   equality; a dense sample plus continuity can.
8. The fail-closed status logic is sound given sound certificates; `E* ⊆ ~` so `E* ∩ U = ∅` is a theorem, and
   its violation is a detector of certificate unsoundness. Certified class counts satisfy `χ(H) ≤ N ≤ k`.

**Mathematical assumptions used:** finite-dimensional real Euclidean geometry; `det` of an orthogonal matrix is
`±1`; orthonormal-basis extension; Gram-matrix rigidity; for (5) only, existence of a tangent-angle lift
(piecewise-`C¹`/BV). Statements (1)–(4) and (6)–(8) need no regularity beyond the stated definitions.

**Explicitly outside this proof:** any property of Meru source curves, any camera census, candidate/null
numerics, historical reconstruction, V5B execution, and all repository/identity verification — all deferred to
Stage 2 by the blind protocol.

## 10. Unresolved assumptions and required declarations

| id | item | status |
|---|---|---|
| **A1** | **Parametrized vs trace congruence.** T02 is true for arclength-synchronised comparison, false for point-set comparison (§3.4). Any trace-level step (Hausdorff/Chamfer, hull or descriptor matching, rasterised overlap, sorted-point canonicalisation) reverts to the false reading. | must be declared and audited |
| **A2** | **Reversal policy.** Changes the antipodal class count; palindromic curves collapse (§4). Must be declared per branch and per comparison; kernels must then test all four combinations (§6.4). | must be declared |
| **A3** | **Branchwise equivalence.** Per-branch EQUAL does not imply whole-figure congruence; UNEQUAL must rule out all `k!` matchings (§8.5). | unresolved, potentially soundness-critical |
| **A4** | **Arithmetic of certification.** "Certified `W ≠ 0`" and kernel mismatch need exact or interval arithmetic; floating point cannot certify (§5.5). | must be declared |
| **A5** | **Quartile construction.** `W`'s reversal-invariance holds only for exact arclength quartiles symmetric under `s ↦ L−s`. Index-based quartiles demonstrably produce false UNEQUAL certificates (§5.4). | **soundness-critical; verify implementation** |
| **A6** | **Frame-construction convention.** `e2 = n × e1` is required; `e2 = e1 × n` flips every `D_t` sign undetectably by any Gram-based check (§8.6). Degenerate guard needed when the seed vector is parallel to `n`. | must be declared and checked |
| **A7** | **Rank-zero policy.** `NOT_EVALUABLE` is correct; a declared rank-zero policy is sound but uninformative and pollutes `E*` (§7.4). | recommend keeping NOT_EVALUABLE |
| **A8** | **Scale prohibition.** Conservative and not load-bearing for T02, but it is what keeps `L` an invariant; length normalisation would discard the cheapest sound witness (§6, §8.6). | must be declared |
| **A9** | **Regularity class.** The T02 proof needs none; the §4.3 palindromic characterisation needs a tangent-angle lift (piecewise-`C¹`/BV). If the amendment's proof is curvature-based it will mis-handle zigzags (§3.3). | verify at Stage 2 |
| **A10** | **Direction de-duplication.** `B_t, D_t` depend on `t` only via `n`, so a `Z³` census must reduce to primitive representatives; `±t` must be neither merged nor split a priori (§2.7, §8.1). | verify at Stage 2 |

## 11. Limits of independence in this actual session

Stated plainly, because the whole purpose of this stage is to remove a procedural independence caveat and a
reviewer should not overstate the independence achieved.

**What genuinely held.** This is a fresh session with no access to any prior review in its context. All proofs
and all counterexamples above were constructed from the challenge statement alone. No prior reviewer script was
executed or consulted as an oracle. No Stage-2 file was opened — the archive contained none. The project's
attached documents, which include the second review and the focused requalification, were **available** to this
session and were deliberately **not** read or searched; no commit, blob or repository object was fetched. The
report was written and hashed before any Stage-2 request.

**What is weaker than it looks.**

1. **Model-lineage correlation.** I am an AI model. If the reviewer that proposed the orientation correction was
   also a Claude-family model, then "different session" is not "different reasoning process": shared training
   data and inductive biases could reproduce the same error in the same place, and neither of us can measure
   that from inside. This is the principal residual caveat and it **cannot** be discharged by this review. It
   would be reduced by a different provider's model and discharged only by an independent human mathematician.
   Mitigating the risk partially: the proofs above are short, elementary and mechanically checkable (`rank(A−I)=1`,
   `det R = −1`, the Gram identity), and every counterexample is exact rational data that any third party can
   re-verify in minutes without trusting me or any model.
2. **Honour-based ordering.** The blind-then-unblind ordering is a commitment, not a sandbox — as
   `00_READ_FIRST.md` states. The hash below proves *what* I wrote, not *that* I had not seen other material.
   The only genuine evidence for the latter is the absence of any read of those files in this session's
   tool-call record, which is auditable but is itself produced by the system under review.
3. **Self-authored verification.** I wrote the symbolic checks that confirm my own derivations. They are an
   error-detector against my algebra, not an independent authority. They were written to be adversarial (generic
   frames, exact arithmetic, congruence searches that *return empty*), but a shared conceptual error between my
   proof and my script would survive. All scripts and exact inputs are included so this can be re-run elsewhere.
4. **Scope.** This is generic mathematics only. Nothing here speaks to whether the V5/V5-R2-A1 implementation
   *does* what the mathematics requires — in particular A5, which is the finding most likely to matter.
5. **Identity verification: not attempted.** Per the protocol, signature, parent-chain and blob checks are
   Stage 2. At Stage 1 they are **UNVERIFIABLE**, not PASS. I did not fetch the commits named in
   `00_READ_FIRST.md` and I make no statement about them. I also note, without having checked it, the package's
   own caveat that a local `TRUST_ULTIMATE` is not implied by external GitHub or imported-keyring GPG status.

## 12. Prospective recommendation

The mathematical core of the SO(2)/O(2) correction is **independently confirmed**: T01 is forced, T02 is true as
stated under the package's own definition, and identity (3) shows a Gram-only invariant set *cannot* separate
mirror views — so the correction was necessary, not optional. T04's `W ≠ 0` is a sound antipodal witness and
T05's kernel completeness holds. I found no disproof of any claim the correction rests on, and I tried
(§8.6).

However I cannot recommend `MERU_3D_V5_SOURCE_MODEL_AND_NULL_DESIGN_QUALIFIED` from Stage 1. Prospective status:

> **`MERU_3D_V5_SOURCE_MODEL_AND_NULL_DESIGN_INCOMPLETE`** — pending Stage-2 resolution of C1–C5.

Not `BLOCKED`: nothing mathematical is broken. `INCOMPLETE` because the following are soundness-relevant and
**unverifiable at Stage 1 by construction**:

- **C1 (A5, soundness-critical).** Confirm `W`'s quartiles are exact arclength and symmetric under `s ↦ L−s`.
  An index-based or approximate implementation emits false UNEQUAL certificates — demonstrated in §5.4 on a
  curve proved mirror-congruent.
- **C2 (A1).** Confirm no comparison step operates on traces as point sets.
- **C3 (A4).** Confirm `W ≠ 0` and kernel mismatches are certified in exact or interval arithmetic, and that
  no finite-sample agreement is ever promoted to `EQUAL` (§6.5).
- **C4 (A2, A3, A10).** Confirm the declared reversal policy, that branchwise equivalence is not used to
  support whole-figure EQUAL, and that the direction set is reduced to primitive representatives with `±t`
  neither merged nor split a priori.
- **C5 (A6, A9).** Confirm the frame convention `e2 = n × e1`, and that the amendment's T02 proof is not
  curvature-based (which would mis-handle rank-one zigzags).

Historical reviewer 2's `INCOMPLETE` is immutable and is not disturbed by this review. Identity and signature
verification remain **UNVERIFIABLE** at this stage. No commit, push, signature, freeze, V5B execution or Hebrew
inspection was performed or prepared.

**Stage 1 is sealed on the SHA-256 recorded alongside this file.**
