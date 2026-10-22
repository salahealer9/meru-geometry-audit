# Meru v0.9 — 3D-V5-R2-A1 Additive Qualification Amendment

**Date:** 22 October 2026  
**Status:** DRAFT FOR HUMAN REVIEW — UNSIGNED — NOT A POSITIVE V5 QUALIFICATION  
**Repository:** `salahealer9/meru-geometry-audit`  
**Branch:** `hebrew-projection-capacity-v0.9`  
**Required direct parent for this proposed one-file signed amendment:** `2073a5618719230c6ec4d5aad7a2941825c7fd77`  
**Signed V5 protocol Git blob:** `9bc215654470785f625c799371168b36e88e1a2b`  
**Human signing fingerprint:** `D4EC014EEFCC90E619D2AA59A91239ABCF512130`  
**Proposed destination:** `docs/v0_9/meru_3d_v5_r2_a1_namespace_orientation_and_parity_qualification_amendment_2026_10_22.md`

## 0. Why this amendment exists

The signed V5 protocol requires a second genuinely independent read-only assessment of the first qualification review before positive closeout. The external reviewer returned

`MERU_3D_V5_SOURCE_MODEL_AND_NULL_DESIGN_INCOMPLETE`

rather than `QUALIFIED`. The findings identify two material but nonblocking problems in the *design and first-review interpretation*, plus missing parity-matrix fields. Preserve the original first review and the complete second review **without editing either archive**.

Authoritative review evidence:

- First review ZIP SHA-256: `42fa29c800d58a4df7f8230e48db4e4271b9521fb0d6e9fa1adfb603dedbc7f7`.
- Second review ZIP name: `MERU_3D_V5_SECOND_INDEPENDENT_READ_ONLY_REVIEW_2026-10-22.zip`.
- Second review ZIP SHA-256: `567e2017f4b6ef2717800ecd44ebedde100c6f5e84027180eee744c42f1ac13c`.
- Second review ledger: `V5_DISCREPANCY_AND_DEFERRAL_LEDGER.md`, D01–D11.
- Second review status: checklist 30 PASS, B35 FAIL, B41 UNVERIFIABLE for the first review's non-execution claim; no identity failure or target leakage identified.
- The review's isolated imported public key produced `VALIDSIG` with `TRUST_UNDEFINED`. This is **not** the same claim as the human's local `TRUST_ULTIMATE`. GitHub separately attested valid signatures.

This amendment is an **additive clarification** to the existing target-blind V5 qualification contract; it does not revise, reinterpret or replace the v0.8 and V1–V4 freezes, and does not authorize a V5B execution. The unsigned prospective freeze note must remain unsigned as a *positive* qualification until a focused read-only reviewer validates this amendment and its application.

## 1. A1/D01 — Distinguish the two non-interchangeable null namespaces

### 1.1 Earlier signed statistical-null ladder (unchanged)

P0A0 §9 (`docs/p0a0_hebrew_projection_source_identity_and_synthetic_pilot_protocol_v0.9.md`, blob `0f8b663bfe2432685c9320a00c80fd6bcf436e38`) and the P0A1 source-constraint ledger (`reports/v0_9/p0a1_methodology/source_constraint_ledger.md`, blob `79c99f826db184fcf95679b886abdee9644274d5`) reserve their **unprefixed** `N0`–`N3` names for future statistical-null designs:

| Original prefix-free label | Unchanged original meaning |
|---|---|
| `N0` | Arbitrary smooth 3-D curves, with a distribution/complexity law yet to be frozen |
| `N1` | Length/curvature/complexity-matched curves, with matching distributions/conditioning yet to be frozen |
| `N2` | Generic 1.5-turn vortices with non-fixed radial laws |
| `N3` | Same-carrier, same-span non-reciprocal controls |

These future generators, distributions, sample sizes, seeds, statistical calibration, and original Gate-6 prerequisites **remain unresolved**.

### 1.2 V5's diagnostic/control-class labels (clarified, no contents changed)

For **all prospective V5 qualification documentation, including the existing first-review register, the 38-row matrix, and any V5B draft**, interpret V5 §4's `N0`–`N3` labels only through the explicit namespace `V5-N0`–`V5-N3`:

| New qualified name | V5 §4 meaning, unchanged in content | Relation to original ladder |
|---|---|---|
| `V5-N0` | Finite sanity/diagnostic fixtures from the V3/V4 scope plus a not-yet-defined deterministic 3-D nondegenerate comparator | Not the statistical `N0` ensemble |
| `V5-N1` | Finite Variant-A radial-law substitutions: frozen Archimedean, logarithmic, Golden Mean, where source domains permit | May be an example of a radial-law control; **not** an instantiated original `N1` distribution |
| `V5-N2` | Finite Variant-B same-carrier controls: six fixed logarithmic rates plus distinct Golden Mean, at identical `(w,e,k)` | May resemble original `N3`'s *type*; **not** a completed original `N3` distribution |
| `V5-N3` | Proposed generic curves under equal-complexity constraints; no finite list, generator, law, or seed fixed | `NULL_NOT_YET_INSTANTIATED` |

The occurrence of a V5-labelled control, including every currently design-eligible record, is **not evidence that any original P0A0/P0A1 `N0`–`N3` null tier or later Gate-6 requirement has been satisfied**. There is no one-to-one statistical equivalence between the two lists; mapping by informal resemblance is prohibited. V5 control rows are fixed design pairings, **not** independent null draws or a multiplicity-adjusted null population. Never rename or edit the original frozen V5 file or first-review CSV to make this correction appear retrospective; a future implementation shall explicitly cite this amendment when displaying the prefixed names.

`SOURCE_CONTRACT_UNRESOLVED` applies to the first review's omission before amendment verification. It can be cleared prospectively only after signing and read-only confirmation of this mapping.

## 2. A2/D02 — Complete the SO(2) orientation-sensitive certificate design

V5B is not authorised by this document. The future V5B protocol **must incorporate** the following mathematically valid certificate options and guard conditions, while registering whether reversal is allowed *before* inspecting any candidate projection.

### 2.1 Exact orthographic identities

For a nonzero primitive integer camera triple `t` and projected 3-D difference vectors `U,V`, define

`B_t(U,V) = U·V − (t·U)(t·V)/(t·t)`  
`D_t(U,V) = t·(U×V)/sqrt(t·t)`.

The source-signed proper camera lift has `B_{−t}=B_t` and `D_{−t}=−D_t`. Its `+t` and `−t` planar projections differ by a *reflection*, up to a common proper 2-D rotation/choice of frame. Therefore:

- Every projected length, endpoint-chord length, un-oriented Gram/distance kernel and reflection-even witness is **identical** for the antipodal pair.
- Such witnesses do **not** distinguish a mirror pair under SO(2), and are insufficient as an SO(2) inequivalence method.
- O(2) equality for antipodes follows from the same equivariant orthographic construction when evaluable. SO(2) equality **does not** follow.

### 2.2 Antipodal test when traversal reversal is *not* permitted

Let `g:[0,ℓ]→R²` be a nonconstant open projected curve in its **own arclength** parameter and `h=F g` its mirror, for `det(F)=-1`. Suppose equivalence permits one translation and SO(2), but not traversal reversal or rescaling.

**Lemma:** `g` and `h` are SO(2)-congruent without reversal **if and only if** `g` is contained in an affine line.

Proof: an arclength-preserving, order-preserving map `[0,ℓ]→[0,ℓ]` fixes each `s`. Proper congruence would equate the oriented determinants of every two anchored displacement vectors of `g` with their reflected counterparts. Reflection negates them; hence all determinants vanish and the affine span has dimension at most one. Conversely, on a line the reflected path is mapped to the original path by a suitable proper planar rotation plus translation. If the projection is constant (`ℓ=0`), report `NOT_EVALUABLE` rather than certifying this nonconstant-curve lemma.

Therefore **one certified nonzero oriented determinant** from three chosen points along the same projected trace proves `UNEQUAL` for the antipodal SO(2) pair *in the no-reversal branch*. Raw source parameter values are admissible for this **limited** rank witness because the two views have the same intrinsic arclength labelling; raw-index comparisons do **not** establish general cross-camera trace equivalence.

### 2.3 Antipodal and general tests when traversal reversal *is* permitted

The previous lemma cannot be applied after allowing reversal: a non-collinear path may be congruent to its mirror through an SO(2) motion combined with traversal reversal.

Use an oriented pseudoscalar that is invariant under traversal reversal. For an open, rectifiable nonconstant planar trace of total projected length `ℓ`, put:

- `o = g(0)`, `e = g(ℓ)`, `m = g(ℓ/2)`,
- `p₁ = g(ℓ/4)`, `p₃ = g(3ℓ/4)`,

where `g` is the arclength representative. Define

`W(g) = det(m−o, e−o) × ( |p₁−o|² − |p₃−e|² ).`

Under translation and every SO(2) rotation, `W` is invariant. Under the reversal `g_rev(s)=g(ℓ−s)`, **both factors reverse sign**, so `W(g_rev)=W(g)`. Under a planar reflection, only the determinant changes sign; therefore `W(Fg)=−W(g)`.

Consequently, a rigorously certified `W(g)≠0` proves that `g` and its mirror **cannot** be congruent under SO(2), even with reversal. More generally, rigorously disjoint enclosures for the two candidate values of `W` prove SO(2) inequivalence (under the registered reversal allowance).

This is a **sufficient witness for inequivalence, not a complete classification or equality oracle**. `W=0` is inconclusive. Certifying nonzero `W` requires globally justified enclosure of projected arclength, certified inversion of `s↦θ(s)` at quarter/mid/three-quarter length, and outward bounds on the final expression. If endpoint/quarter-point identification, degeneracy, or precision cannot be certified under the registered budget, return `UNRESOLVED_PAIR`; never substitute uniformly sampled raw `θ` points.

Additional orientation-odd witnesses or full oriented-kernel proofs may be incorporated only if specified and independently reviewed in the signed V5B protocol before first execution.

### 2.4 Equality requires whole-curve proof, not a near-zero test

For same-length open projected curves, use anchored arclength displacement functions

`v_g(s)=g(s)−g(0)`, `v_h(s)=h(s)−h(0)`

and the **whole** kernels

`G_g(s,t)=v_g(s)·v_g(t)`, `A_g(s,t)=det(v_g(s),v_g(t))`.

The full equality of `G_g=G_h` for **all** `s,t∈[0,ℓ]` characterises O(2) congruence after translation. Requiring additionally `A_g=A_h` characterises SO(2) congruence (rank-one/nonconstant cases admit a proper extension). A reversal-permitted comparison must also test `h_rev(s)=h(ℓ−s)` **and re-anchor at `h(ℓ)`**. Equivalent base-point-free squared-distance kernels can replace the Gram kernels for O(2) only.

These statements are **mathematical characterisations**, not a guarantee that a finite algorithm can certify equality of two arbitrary transcendental curves. Certified nonidentity can use a rigorously separated scalar invariant or a kernel witness at a proved arclength coordinate. `EQUAL` must use a valid symbolic identity / complete kernel proof / rigorously proved group symmetry. Finite samples and tight intervals alone cannot prove exact equality. If no proof resolves a pair, record `UNRESOLVED_PAIR`.

### 2.5 Matrices and failure closure

- Keep `SO(2)` and `O(2)` matrices separate. `SO(2)` equivalence implies `O(2)` equivalence, never the converse by default.
- `EQUAL` and `UNEQUAL` are logical certificate statuses, not thresholds.
- Equality is transitive; any certified `UNEQUAL` pair in the same `EQUAL` transitive component is a **contradiction** and must cause a fail-closed `FAILED` result.
- Unresolved pairs must not be treated as unequal or silently merged; compute **rigorous lower and upper class-count bounds** over all equivalence partitions compatible with the certified relations.
- The signed V5B protocol must establish explicit regularity/degeneracy policy, time and precision budgets, interval library/rounding contracts, stopping rules, certificate retention and independent non-importing verification before scientific execution.
- Do not treat the rational V4 polyline classifier as a certified continuous-analytic-curve classifier.

## 3. A3/D03–D11 — Additive parity and scope disposition

### 3.1 Source-derived parity supplement (not a projection measurement)

All design-eligible records in the accepted first-review **38-row** matrix retain their existing model/control identities. The 30 eligible rows remain *design eligible*, **not executable**. The supplement below supplies common fields formerly implicit or absent:

| Control family | Free fitted geometry parameters | Fixed family labels/parameters | Exact inherited domain | Endpoint matching |
|---|---:|---|---|---|
| Variant-A reciprocal | 0 | reciprocal, `k∈{G30,GHALF}` separately | `θ∈[1,1+3π]` (DIAGRAM only for matching) | reference |
| `V5-N1` A Archimedean | 0 | endpoint-determined affine law; same fixed `k` | same | both radial endpoints |
| `V5-N1` A logarithmic `m` | 0 | six fixed rates `m∈{0.5,0.75,1,1.25,1.5,2}`, same `k` | same | both endpoints only `m=1` |
| `V5-N1` A Golden Mean | 0 | `bφ=2 log(φ)/π`, same `k` | same | outer radial endpoint only |
| Variant-B reciprocal | 0 | `(w,e)` one of 25 predeclared cells, same `k`, frozen mapping | `θ∈[1,1+3π]` | reference |
| `V5-N2` B logarithmic `m` | 0 | six fixed rates; identical `(w,e,k)` and mapping | same | inner endpoint only for `m=1`; outer common for all |
| `V5-N2` B Golden Mean | 0 | fixed Golden Mean rate; identical `(w,e,k)` and mapping | same | outer endpoint only |

The **same equation for the map** does not imply a matched inner **position**: in B, `r_R(θ_i)=1/(1+3π)`, `r_{L,m}(θ_i)=(1+3π)^(−m)` and `r_φ(θ_i)=φ^(−6)`. The nonmatching inner endpoint is part of each frozen control, not a reason to optimize a different map. The A Golden Mean and `m≠1` rates likewise do not share the reciprocal's inner radius.

Every eligible comparison must register the same exact camera directions (G0 = six signed axes in the proposed first trial), translation-only rigid quotient (no scale), separate SO(2)/O(2), an identical reversal permission, same treatment of camera roll, equal numerical precision/work ceiling and fail-closed stopping rules. Chirality follows the inherited source-coordinate orientation and must not be separately fitted per object. Model-specific ranks, zero-length views and projection critical points are **NOT YET CERTIFIED** and must be established in the authorised V5B preflight; no rank is inferred from this read-only V5 review. Each numerical control is fixed by a frozen grid label, **not a fitted free parameter**; nevertheless the number of fixed shape degrees and the advantage from examining multiple alternative controls must be tracked and reported.

The `30 design eligible / 2 A-PROSE ineligible / 6 deferred` counts are an inventory of **pairings**, not a distribution, a proof of projection equivalence, or permission for a 30-case execution.

### 3.2 Dispositions retained from the independent review

- **D04:** the B endpoint-nonparity caveat above is mandatory for later matrices.
- **D05:** `V5-N0`'s deterministic 3-D comparator remains `NULL_NOT_YET_INSTANTIATED`; V3 labelled point sets are not automatically analytic traces; V4 polyline oracles may be reused as *predeclared diagnostic checks* without rerunning the frozen V4 scientific execution.
- **D06:** K and C0 remain reference/deferred lanes. Existing source-code defaults are **not historically registered metric geometry** and must not silently instantiate either lane.
- **D07:** where a first-review register row combines a literal source claim with an audit-selected mathematical family, split it into separate `SOURCE_ATTESTED` and `SOURCE_CONSTRAINED_INTERPRETATION` entries in the eventual additive qualification archive. Diagnostic comparator choices receive their own `NULL_CONTROL` labels. Never relabel a frozen row without an additive cross-reference.
- **D08:** correct the record's `r_{L},m}` transcription to `r_{L,m}` by an erratum, not an edit; the first package's assertion that it included a checker script was inaccurate. The kernel basepoint and re-anchoring and matrix contradiction rules are now made explicit in §2. An open *trace* may have a closed **parameter interval**. Nonconstant rectifiable curves may admit arclength representatives even with isolated zero-speed parameter points; computation must handle them conservatively.
- **D09:** V5B must prospectively choose its exact primary subset (three-curve minimal pilot versus all eight A controls), before implementation or data examination; no analysis-conditional expansion or favourable family selection.
- **D10:** the second review's v0.8 tag census closes the initial tag-check deferral (14/14 consulted pre-tag objects blob-identical).
- **D11:** comparing a reciprocal to the best of six fixed logarithmic members creates a six-choice comparison opportunity; do not report it as one independently selected null or as a multiplicity-free comparison.

### 3.3 Unchanged scope and gate limitations

The FINISHED FIRST HAND construction remains historically underdetermined; the v0.8 source-recovery result is unchanged. No source images, Hebrew charts, glyphs, fonts or alphabet proxies enter this amendment. Physical shadow/occlusion, SET-IMAGE, nonconvex ribbons, Variant-B projection runs, K/C0 metrics, `V5-N3` ensembles, G1/G2 candidate projection extensions and statistical null inference are all deferred.

The independent reviewer marked first-review non-execution `UNVERIFIABLE` on document evidence alone. This is a **bounded evidentiary limitation**, not affirmative evidence of forbidden execution; preserve the label and do not assert a proof of non-execution from an archive's absence of results.

## 4. Required read-only requalification, then separate human-controlled freeze

1. Human must first **review and approve this exact draft**, verify its downloaded SHA-256, verify clean feature branch and remote HEAD = V5 preregistration commit `2073a5618719230c6ec4d5aad7a2941825c7fd77`, and sign **one new Markdown file only** as a direct-child commit using the expected local trusted GPG key. No source/data or prior review file may be edited; preserve original first- and second-review archives byte-for-byte.
2. After signed amendment, a genuinely independent **read-only** reviewer shall check D01 namespaces against P0A0/P0A1, D02 mathematical proofs and sign/reversal cases, D03 common/parity rows and D04–D11 disposition. Report exact amended commit/blob, cryptographic hashes of original reviews, verified checklist outcome and any continuing objections. It may legitimately return `INCOMPLETE` or `BLOCKED`.
3. Only if the independent requalification is positive may the author prepare a **separate additive results/qualification freeze** listing the V5 protocol, amendment, first review ZIP, second review ZIP, focused recheck report, provenance ledgers and their verified hashes. The freeze's **direct parent must be the then-current signed amendment commit**, not the old V5 preregistration. Sign/push only after verification of all files, the correct GPG fingerprint and a clean additive diff. Keep `INCOMPLETE` on record as the original second-review verdict; report the later qualified status as a prospective corrective outcome, never a retroactive alteration.
4. The only possible positive qualification wording is `MERU_3D_V5_SOURCE_MODEL_AND_NULL_DESIGN_QUALIFIED`, *if* explicitly supported by the post-amendment independent audit. It licenses only a **new V5B preregistration**, not a V5B calculation.
5. V5B requires its own fully signed, first-run-specific plan, frozen implementation and bounded first execution, with complete evidence preservation, independent continuous-curve verification, and explicit target-access prohibition.

No Git commit/push or scientific execution is authorised or performed by preparing this amendment draft.
