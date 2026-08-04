# First Hand S1 Truncation-Parity Analytic Findings and Closeout

**Checkpoint:** `first_hand_s1_truncation_parity_closeout_v0.8`  
**Status:** CLOSED — TRUNCATION-PARITY MATRIX EXECUTED AND RECORDED  
**Phase:** analytic self-embedment audit  
**Variant:** A — cube-octahedral / canonical inverse-gnomonic sphere only  
**Primary question:** truncation-parity control of logarithmic endpoint-tangent S1  
**Existing 1.5-turn results:** inherited and not rerun  
**Image pixel data used:** no

## 1. Purpose

This note closes the preregistered First Hand S1 truncation-parity checkpoint.

It records the scientific findings of the completed 54-cell execution, combines them with the inherited immutable 1.5-turn reference values, and fixes the interpretation boundary before any later analytic extension is designed.

No truncation cell is rerun in this closeout.

No new span is added.

No logarithmic growth rate is added or optimized.

No spherical scale is added.

No Variant-B / dimpled-sphere construction is introduced.

The generated execution artifacts remain the authoritative numerical record:

- `results/first_hand_s1_truncation_parity_v0_8/s1_truncation_parity_results.json`
- `results/first_hand_s1_truncation_parity_v0_8/s1_truncation_parity_new_cells.csv`
- `results/first_hand_s1_truncation_parity_v0_8/s1_truncation_parity_report.md`

---

## 2. Registered analytic premise

For a logarithmic spiral

\[
r(u)=e^{-bu},
\qquad
\theta(u)=\theta_0+u,
\]

the planar tangent satisfies

\[
\mathbf{x}'(u)
=
e^{-bu}
R(\theta_0+u)
\begin{pmatrix}
-b\\
1
\end{pmatrix}.
\]

After an angular span \(L\),

\[
\mathbf{x}'(u+L)
=
e^{-bL}
R(L)\mathbf{x}'(u).
\]

Because \(e^{-bL}>0\), the endpoint tangent direction depends on \(R(L)\) but not on the growth rate \(b\).

For

\[
L=n\pi,
\]

\[
R(L)=(-1)^n I.
\]

Therefore:

- integer numbers of full turns predict planar endpoint tangent alignment;
- odd half-integer numbers of full turns predict planar endpoint tangent anti-alignment.

The source's 1.5-turn truncation corresponds to

\[
L=3\pi,
\]

so every logarithmic spiral has exactly antiparallel planar endpoint tangents at that truncation.

The spherical sensitivity checkpoint was preregistered to test whether the Variant-A projection and intrinsic transport preserve this parity structure.

---

## 3. Registered truncation set

The executed truncation set was

\[
T\in
\left\{
1.0,\,
1.5,\,
2.0,\,
2.5
\right\}
\text{ turns},
\]

equivalently

\[
L\in
\left\{
2\pi,\,
3\pi,\,
4\pi,\,
5\pi
\right\}.
\]

The parity classes were:

### Integer-turn class

\[
\mathcal{I}
=
\left\{
1.0,\,
2.0
\right\}
\text{ turns}.
\]

### Odd-half-integer-turn class

\[
\mathcal{H}
=
\left\{
1.5,\,
2.5
\right\}
\text{ turns}.
\]

The 1.5-turn values were inherited from the completed reciprocal/comparator checkpoints and were not rerun.

---

## 4. Primary parity result

The primary registered summaries are:

`PARITY_SEPARATION_CONFIRMED_ALL_LOG_GRID_CELLS`

and

`PARITY_SEPARATION_CONFIRMED_GOLDEN_MEAN`.

The preregistered parity-separation criterion is therefore confirmed for:

- all six fixed generic logarithmic growth rates;
- both registered spherical scales;
- the separately named Golden Mean spiral.

There are no exceptions in the registered matrix.

---

## 5. Size of the parity effect

The spherical Variant-A calculation preserves the planar parity theorem extremely strongly.

Across the generic logarithmic grid, integer-turn mismatches lie approximately in the range

\[
0.6508^\circ
\lesssim
\Delta_{\rm S1}
\lesssim
3.1415^\circ.
\]

By contrast, odd-half-integer-turn mismatches lie approximately in the range

\[
176.8585^\circ
\lesssim
\Delta_{\rm S1}
\lesssim
179.2378^\circ.
\]

Thus:

\[
\boxed{
\text{integer turns}
\Rightarrow
\text{near-alignment}
}
\]

while

\[
\boxed{
\text{odd half-integer turns}
\Rightarrow
\text{near-anti-alignment}
}.
\]

The projection and intrinsic transport perturb the ideal planar values

\[
0^\circ
\quad\text{and}\quad
180^\circ
\]

by only a few degrees.

---

## 6. Parity contrast

The preregistered parity contrast

\[
P_{b,k}
=
\bar{\Delta}_{\mathcal H}
-
\bar{\Delta}_{\mathcal I}
\]

is positive and very large in every logarithmic branch.

Across the six generic logarithmic rates and both scales,

\[
173.7209^\circ
\lesssim
P_{b,k}
\lesssim
178.4662^\circ.
\]

For the Golden Mean spiral,

\[
P_{\phi,\mathrm{G30}}
=
175.685598^\circ,
\]

and

\[
P_{\phi,\mathrm{GHALF}}
=
176.060842^\circ.
\]

The spherical parity effect is therefore not marginal.

It dominates the S1 behaviour of the logarithmic family.

---

## 7. Golden Mean result

The Golden Mean branch follows the same pattern as the generic logarithmic family.

### Integer turns

At one turn:

\[
\Delta_{\rm S1}
=
2.117140^\circ
\]

for G30 and

\[
1.933691^\circ
\]

for GHALF.

At two turns:

\[
\Delta_{\rm S1}
=
2.172572^\circ
\]

for G30 and

\[
1.983349^\circ
\]

for GHALF.

### Odd half-integer turns

At 1.5 turns:

\[
177.834516^\circ
\]

for G30 and

\[
178.022998^\circ
\]

for GHALF.

At 2.5 turns:

\[
177.826393^\circ
\]

for G30 and

\[
178.015725^\circ
\]

for GHALF.

The Golden Mean branch therefore behaves exactly as expected for a named member of the logarithmic family.

---

## 8. Reciprocal truncation sensitivity

The reciprocal spiral also exhibits strong truncation dependence.

### Integer turns

At one turn:

\[
\Delta_R
=
33.099569^\circ
\]

for G30 and

\[
33.473281^\circ
\]

for GHALF.

At two turns:

\[
36.681449^\circ
\]

for G30 and

\[
37.057282^\circ
\]

for GHALF.

### Odd half-integer turns

At 1.5 turns:

\[
144.577622^\circ
\]

for G30 and

\[
144.202263^\circ
\]

for GHALF.

At 2.5 turns:

\[
142.529731^\circ
\]

for G30 and

\[
142.153715^\circ
\]

for GHALF.

Thus S1 is not truncation-invariant even for the reciprocal spiral.

The reciprocal mismatch changes by more than \(100^\circ\) between the integer-turn and odd-half-integer-turn classes.

---

## 9. Reciprocal-versus-logarithmic ranking reversal

The previous 1.5-turn comparator checkpoint found that the reciprocal spiral had a substantially smaller S1 mismatch than every registered logarithmic comparator.

The truncation-parity checkpoint shows that this ranking reverses at integer-turn truncations.

For every fixed logarithmic growth rate and both scales:

### Integer turns

\[
D_{\log-R}
=
\Delta_{\log}
-
\Delta_R
<
0.
\]

Therefore the logarithmic spiral has the smaller mismatch.

Across the registered grid, the logarithmic advantage is approximately

\[
30^\circ
\text{ to }
36^\circ.
\]

### Odd half-integer turns

\[
D_{\log-R}>0.
\]

Therefore the reciprocal spiral has the smaller mismatch.

Across the registered grid, the reciprocal advantage is approximately

\[
32^\circ
\text{ to }
37^\circ.
\]

This gives a direct truncation-parity reversal:

\[
\boxed{
\text{integer turns}
\Rightarrow
\text{logarithmic better than reciprocal}
}
\]

\[
\boxed{
\text{odd half-integer turns}
\Rightarrow
\text{reciprocal better than logarithmic}
}.
\]

This reversal occurs for every preregistered logarithmic growth rate at both registered scales.

---

## 10. Consequence for the earlier source comparison

The earlier comparator checkpoint reproduced the source-stated ordering in which reciprocal performed better than logarithmic / Golden Mean spirals under the source's 1.5-turn Variant-A construction.

That result remains valid.

However, the present checkpoint demonstrates that the ordering is not truncation-independent.

The 1.5-turn truncation itself lies in the parity class that analytically forces logarithmic planar endpoint anti-alignment.

At integer-turn truncations, the logarithmic family instead becomes near-aligned and strongly outperforms the reciprocal spiral under the same Variant-A S1 statistic.

The correct refined conclusion is therefore:

> The source-stated reciprocal-over-logarithmic ordering is reproduced under the source's 1.5-turn Variant-A truncation, but that ordering is conditional on the truncation parity and reverses at integer-turn truncations.

The source truncation and the S1 comparator conclusion are mathematically coupled.

No claim is made about why the source chose 1.5 turns.

---

## 11. Archimedean-versus-reciprocal ranking reversal

The endpoint-matched Archimedean comparison also reverses with truncation parity.

Define

\[
A_{L,k}
=
\Delta_A(L,k)
-
\Delta_R(L,k).
\]

Then:

| Turns | G30 \(A-R\) | GHALF \(A-R\) | Better curve |
|---:|---:|---:|---|
| 1.0 | \(+5.029643^\circ\) | \(+4.575661^\circ\) | reciprocal |
| 1.5 | \(-4.784884^\circ\) | \(-4.351031^\circ\) | Archimedean |
| 2.0 | \(+4.640043^\circ\) | \(+4.218312^\circ\) | reciprocal |
| 2.5 | \(-4.545475^\circ\) | \(-4.131722^\circ\) | Archimedean |

Thus:

\[
\boxed{
\text{integer turns}
\Rightarrow
\text{reciprocal beats endpoint-matched Archimedean}
}
\]

and

\[
\boxed{
\text{odd half-integer turns}
\Rightarrow
\text{endpoint-matched Archimedean beats reciprocal}
}.
\]

The previous statement that the Archimedean comparator beats reciprocal is therefore valid for the source's 1.5-turn truncation but is not a truncation-robust ordering.

---

## 12. Structural interpretation of the Archimedean result

At each registered truncation, the endpoint-matched Archimedean branch shares with the reciprocal:

- the same phase;
- the same angular span;
- the same outer radius;
- the same inner radius;
- the same spherical outer endpoint;
- the same spherical inner endpoint;
- the same great-circle transport path.

The alternating ranking therefore arises from the tangent geometry generated by the radial laws under the changing truncation span, not from differing endpoint positions.

This reinforces the conclusion that S1 is strongly sensitive to truncation geometry.

---

## 13. Absolute compatibility remains distinct

The parity results must not be confused with exact compatibility.

The preregistered absolute criterion remains

\[
\Delta_{\rm S1}=0
\]

up to the floating-point zero tolerance.

Even the near-aligned integer-turn logarithmic branches remain formally

`S1_DIRECTED_NOT_COMPATIBLE`.

Their mismatch is small but non-zero:

\[
\sim0.65^\circ
\text{ to }
3.14^\circ.
\]

Thus the correct language is:

- near-aligned;
- substantially closer to compatibility;
- smaller S1 mismatch.

The word "compatible" remains reserved for the registered exact criterion.

---

## 14. What this checkpoint establishes

Within Variant A:

1. the exact planar logarithmic truncation-parity theorem is strongly preserved by the spherical S1 construction;
2. every preregistered generic logarithmic branch shows strict parity separation;
3. the Golden Mean branch shows the same separation;
4. integer-turn logarithmic branches are near-aligned;
5. odd-half-integer logarithmic branches are near-anti-aligned;
6. reciprocal S1 itself is strongly truncation-dependent;
7. reciprocal-versus-logarithmic ranking reverses with truncation parity;
8. reciprocal-versus-endpoint-matched-Archimedean ranking also reverses with truncation parity.

These are fixed v0.8 findings.

---

## 15. What this checkpoint does not establish

This checkpoint does not establish that logarithmic spirals literally self-embed at integer turns.

It does not establish exact tangent compatibility for any logarithmic branch.

It does not establish that integer turns are historically relevant to the First Hand source construction.

It does not establish that the source intentionally selected 1.5 turns to disadvantage logarithmic spirals.

It does not establish a uniquely correct spiral family.

It does not establish the full First Hand construction.

It does not establish Hebrew-letter generation.

It does not establish literal recursive "seed inside fruit" nesting.

It does not establish S1.5 or S2.

It does not establish Variant-B behaviour.

---

## 16. Methodological interpretation of S1

The completed sensitivity analysis shows that S1 is useful as a diagnostic of a specified truncated construction but is not a truncation-invariant discriminator of spiral family.

The comparator ranking can change sign when the angular span changes while the curve family and spherical map remain fixed.

Therefore:

> S1 rankings must always be interpreted conditional on the registered truncation.

No future report should state simply that one spiral "beats" another under S1 without also stating the truncation at which the comparison was made.

This is now a methodological requirement of the audit.

---

## 17. Refined interpretation of the source claim

The source's reciprocal-versus-logarithmic comparison receives a qualified result.

### What is reproduced

Under the source's 1.5-turn Variant-A construction:

\[
\Delta_R
<
\Delta_{\log},
\]

by approximately

\[
32^\circ
\text{ to }
35^\circ
\]

for the previously registered logarithmic grid and Golden Mean branches.

### What the sensitivity analysis adds

The logarithmic disadvantage at 1.5 turns is strongly explained by an exact truncation-parity mechanism.

At integer turns:

\[
\Delta_{\log}
\ll
\Delta_R.
\]

Thus the relative ordering changes when only truncation parity changes.

The strongest defensible statement is:

> The source-stated reciprocal-over-logarithmic ordering is reproduced at the source's 1.5-turn Variant-A truncation, but it is not a truncation-invariant property of the spiral families and reverses at integer-turn truncations.

---

## 18. No inference about source intent

The mathematical coupling between the 1.5-turn truncation and logarithmic anti-alignment does not establish why the source selected 1.5 turns.

Possible historical or conceptual motivations are outside the present evidence.

The audit therefore does not infer:

- deliberate tuning;
- cherry-picking;
- intentional suppression of logarithmic alternatives;
- knowledge of the parity theorem.

Only the geometric consequence of the chosen truncation is established.

---

## 19. Variant-A / Variant-B firewall

This entire checkpoint concerns Variant A only.

Variant B modifies the inner geometry through the dimpled-sphere / toroidal construction.

S1 depends directly on the inner endpoint tangent and its transport relation.

Therefore the present parity values and comparator reversals cannot be transferred automatically to Variant B.

The exact planar logarithmic parity theorem remains true independently of the spherical surface.

But the corresponding spherical endpoint-tangent statistic on Variant B requires a separately defined and preregistered geometry.

---

## 20. Methodological significance

This checkpoint was completed without post-hoc adjustment.

The audit did not:

- add new turn counts;
- scan continuously over truncation;
- change logarithmic growth rates;
- re-normalize the logarithmic family at each span;
- optimize the Golden Mean branch;
- modify the reciprocal law;
- optimize Archimedean pitch against S1;
- rerun the inherited 1.5-turn cells;
- change spherical scales;
- change tangent orientation;
- use \(|d|\);
- change the transport rule;
- introduce new comparator families;
- introduce Variant B;
- use page-7 pixels.

The parity prediction was stated before execution and was then confirmed across the complete registered matrix.

This is a strong preregister-before-run result.

---

## 21. Closed truncation-parity conclusion

The checkpoint closes with:

`PARITY_SEPARATION_CONFIRMED_ALL_LOG_GRID_CELLS`

and

`PARITY_SEPARATION_CONFIRMED_GOLDEN_MEAN`.

The principal scientific conclusion is:

> **Variant-A S1 is strongly controlled by truncation parity. Logarithmic and Golden Mean spirals are near-aligned at integer-turn truncations and near-anti-aligned at odd-half-integer truncations. The reciprocal-versus-logarithmic ordering therefore reverses with parity.**

A second result is:

> **The reciprocal-versus-endpoint-matched-Archimedean ordering also reverses with parity.**

Accordingly, no S1 comparator ranking may now be treated as a truncation-independent property of the underlying spiral family.

---

## 22. Next-stage boundary

The truncation-parity checkpoint has exposed a structural limitation of S1 as a general comparator.

The next analytic stage should therefore not simply expand S1 across more spiral families.

A more direct test of the source's "seed inside fruit" self-embedment claim should instead specify an actual embedding or similarity map and test whether one copy of the construction is carried into another with the required positional and tangent/frame relationships.

Potential next stages include:

- a preregistered similarity-map self-embedment test;
- a formally defined S1.5 frame condition only if it contributes independently to that embedding question;
- later Variant-B reconstruction and testing.

Any such extension requires its own preregistration before execution.

No future stage may retroactively modify the completed truncation-parity result.

---

## 23. Phase status

The Variant-A analytic sequence now stands at:

\[
\text{reciprocal S1 checkpoint}
\]

\[
\downarrow
\]

\[
\text{comparator checkpoint}
\]

\[
\downarrow
\]

\[
\text{truncation-parity preregistration}
\]

\[
\downarrow
\]

\[
\text{truncation-parity implementation freeze}
\]

\[
\downarrow
\]

\[
\text{registered 54-cell parity execution}
\]

\[
\downarrow
\]

\[
\boxed{\text{truncation-parity analytic closeout}}
\]

The truncation-parity effect is now a fixed v0.8 audit finding and a boundary condition for all later interpretation of S1.
