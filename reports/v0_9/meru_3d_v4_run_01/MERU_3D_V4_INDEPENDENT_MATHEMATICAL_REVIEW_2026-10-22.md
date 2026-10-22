# Meru v0.9 — 3D-V4 Independent Mathematical Review

**Date:** 22 October 2026  
**Study:** `MERU_3D_V4` — target-blind traced-polyline and convex-silhouette equivalence  
**Protocol preregistration commit:** `d7b5359f857b5a294746dc6bce5a61e50d169022`  
**Protocol Git blob:** `2d57b85c066c76ae462929ece209385f5491ed78`  
**Human GPG fingerprint:** `D4EC014EEFCC90E619D2AA59A91239ABCF512130`  
**Review outcome (before separate human results-freeze signing):** `MERU_3D_V4_EXACT_TRACE_AND_CONVEX_SILHOUETTE_EQUIVALENCE_PASS`.

## 1. Evidence, independence, and identity

The original operator-supplied archive `MERU_3D_V4_RUN_01_EVIDENCE.tar.gz` has SHA-256 `e18ea8eff8d9d8075f4faf2016c1bbeaec3fcb8d1aa156db998a012ceede5f91`. Its `run_01/` directory contains **13 original files**, including a single preserved standalone script, JSON stdout, empty stderr, exit code, UTC timestamps, environment and Git identities. Its `SHA256SUMS.txt` passes in full:

- Frozen script `meru_3d_v4_standalone_calculator.py`: SHA-256 `d197e231e62da7a02c627732119212178dd65deb4c1d54b958219c67072a0520`.
- Original `results.json`: SHA-256 `a90cb2cce5edffe55bbd860850a255d0a54acf8cdb46b34027091fec982d154a`.
- Original `stderr.txt`: SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`, exactly zero bytes.
- `exit_code.txt` is `0`; the result JSON identifies the signed protocol commit/blob, Python 3.11.2 and the status `PASS_INTERNAL_ORACLES_AWAITING_INDEPENDENT_REVIEW`.

The remote GitHub branch was independently checked at the exact signed V4 preregistration commit with the required V3 results-freeze direct parent `e2bad59a282b30ddd1f96ba213a449d02b2174e3`; GitHub reports a valid signature. The operator's local terminal additionally reported `GOODSIG`, `VALIDSIG` and `TRUST_ULTIMATE` for the stated fingerprint. Distinguish GitHub verification from locally trusted-key verification.

**Independent procedure:** a **separately written** exact-arithmetic checker `meru_3d_v4_independent_exact_qc.py` was used on the original JSON *as read-only data*; the registered V4 calculator was not imported, executed, repaired or rerun. All control source coordinates and camera sets were re-entered from the signed protocol. The reviewer used a supporting-edge convex-hull construction, an independent iterative trace reduction, canonical congruence signatures under admissible cycle shifts/reversal, and exact `fractions.Fraction` projection forms. No numerical tolerance, raster, or sampling-based assertion is used. A first audit-only implementation was slow and was replaced by cached canonical signatures; a subsequent audit-only mismatch in the *display ordering of unoriented axis representatives* was corrected to global lexicographic presentation (the camera vectors and mathematical classes never differed). The final independent source and output are fully preserved; the registered run remains unchanged.

**Final independent QC:** `6,090/6,090` explicit assertions pass, with **30,320 separately constructed pairwise matrix entries** across **30 object/grid records**. These numbers are implementation-specific audit counts, not statistical trials. Re-running the separate checker on its portable archival copy gave the same passing output. Full counts, ranks, class-size multisets and exact result hash are in `MERU_3D_V4_INDEPENDENT_QC_2026-10-22.json`.

## 2. Mathematical completeness and independent methods

For each primitive signed camera triple `t`, set `q=t·t>0`, with orthographic bilinear form

`B_t(u,v)=u·v−(t·u)(t·v)/q`,

and proper-oriented projected determinant `D_t(u,v)=t·(u×v)/sqrt(q)`.

Both are independent of the arbitrary in-plane camera roll. All `B_t` evaluations and determinant numerators are exact rational values. For cross-camera equality of signed determinants, the checker compares **sign and rational squared magnitude**, `(sign(d),d²/q)`, which characterises the real number `d/sqrt(q)` exactly, including zero; no floating-point radical approximation is used.

**TR (continuous polygonal traces).** Starting independently from the three frozen rational paths, successive zero-projection edges are removed exactly, then positively collinear consecutive projected edges are merged until stable. Negative-dot antiparallel retracings are never merged away. The independent reduced continuous traces agree with all original per-camera reductions up to the protocol's endpoint reversal / closed cyclic presentation freedom. Projected ranks and every retained breakpoint are independently checked. Zero-rank TR-L appears **only at `±e_x`** and is explicitly excluded from equivalence; nonzero rank-one traces remain evaluable. For each possible admissible open-path order or closed-loop cyclic order/reversal, equality of the complete centred Gram matrix exactly characterises `O(2)` congruence of the ordered planar breakpoints. Requiring the complete orientation minors as well characterises `SO(2)` congruence, including the degenerate rank-one case. A PL trace with no surviving forward-collinear breakpoint has no extra intrinsic parameter that can alter its path under the admitted monotone reparametrisations; nontrivial re-traversal and visit order remain represented by retained turns.

**CS (filled convex silhouettes).** For each frozen solid, independently merge projected duplicate vertices via exact squared distance. Instead of a raster or an imported hull routine, enumerate **directed supporting edges**: an edge from distinct projected `i` to `j` is strict CCW hull boundary when all other points lie to its left, and any exactly collinear points lie within that entire edge. Those edges must form one simple cycle of strict extreme corners; an independent positive doubled-area check certifies orientation and nondegeneracy. The derived hull cycle, projected-distinct count, strict-corner count, full centred Gram matrix and all proper-oriented minors agree exactly with the registered per-camera outputs. A finite convex polygon is the filled convex hull of its extreme corners. Congruence of these unlabelled filled polygons is therefore equivalent to congruence of a boundary cycle: cyclic shifts for `SO(2)`, with reversed cycles additionally allowed for `O(2)`, tested by the complete Gram and oriented-minor invariants. Source vertex identities were not used to match two silhouettes.

The independently derived 30 SO2/O2 **full camera-pair equivalence matrices** agree entry-for-entry with the registered matrices. Their exact partitions and class-size multisets agree; all matrix entries involving an invalid view are `null` and no valid view is silently omitted. Independent rank, antipodal O2 equivalence, SO2-refines-O2, identical A/B G0, fixed line and G0 silhouette oracles, and nested-tier nondecrease checks all pass. These provide a finite complete census for *the stated* two observables; they do not amount to source-glyph matching or general nonconvex silhouette certification.

## 3. Discovered exact finite results

Each entry below is `SO(2) classes / O(2) classes` among evaluable signed cameras. **Only the line-control and G0 solid entries were preregistered as numerical oracles**; other entries are measurements of the frozen exact finite question, subsequently independently checked.

| Camera grid | Signed cameras / axes | TR-L | TR-S | TR-C | CS-T | CS-B |
|---|---:|---:|---:|---:|---:|---:|
| A G0 = B G0 | 6 / 3 | 1 / 1 | 6 / 3 | 6 / 3 | 6 / 3 | 3 / 3 |
| A G1 | 14 / 7 | 2 / 2 | 14 / 7 | 12 / 6 | 14 / 7 | 5 / 4 |
| A G2 | 26 / 13 | 3 / 3 | 26 / 13 | 23 / 12 | 26 / 13 | 8 / 7 |
| B G1 | 18 / 9 | 2 / 2 | 18 / 9 | 17 / 9 | 18 / 9 | 6 / 6 |
| B G2 | 42 / 21 | 4 / 4 | 42 / 21 | 41 / 21 | 41 / 21 | 12 / 12 |

All `TR-L` levels have exactly two NOT_EVALUABLE cameras, namely the signed x axes; each other `TR-L` view has rank one. Every `TR-S`, `TR-C`, `CS-T` and `CS-B` camera is rank two and evaluable. Every CS projection has strictly positive area.

Further exact observations:

- The asymmetric open spatial trace `TR-S` attains the full directional ceiling in every tier: each signed camera has its own `SO(2)` class, and antipodes form the `O(2)` classes.
- The closed trace `TR-C` has **additional SO2 identifications** due to intrinsic cyclic or traversal correspondence, even though its projections remain rank two: for example, A G1 has only 12 SO2 classes from 14 cameras; A G2 has 23 from 26.
- The filled box `CS-B` is much more redundant than the direction grid: B G2 has only 12 classes under either group from 42 signed cameras. Its symmetry is object-specific, not an invalidity of those directions.
- The asymmetric tetrahedron `CS-T` attains the ceiling through A G2 and B G1, but B G2 has **41 SO2 classes from 42 cameras**: signed camera pair `(-1,-2,0)` and `(1,2,0)` yields properly congruent unlabelled silhouettes. This geometric coincidence would be missed by assuming every antipodal projection is SO2-distinct or by matching source vertex labels.

## 4. Outcome, limitations, and freeze discipline

**Mathematical outcome:** `MERU_3D_V4_EXACT_TRACE_AND_CONVEX_SILHOUETTE_EQUIVALENCE_PASS`, contingent on human signing of the additive result-freeze files with the required exact direct parent, provenance and checksum checks. The independent review supports the registered questions at their stated finite resolution; neither the original calculator's internal PASS label nor high checker counts substitute for the geometric completeness arguments above.

**Important limitations:** TR counts preserve path order and retracings, not just the occupied image set; CS counts refer solely to filled convex hulls, not nonconvex wire occlusion or physical shadows. The study has no actual first-hand Meru object, no source-justified reciprocal-torus candidate, no Hebrew images/glyph proxies, no tuning to targets, and no statistical significance test. High or low class counts neither prove nor refute claims about intentional Hebrew-letter generation. The v0.8 first-hand construction question remains unresolved.

**Archive action:** copy all 13 original `run_01` files unchanged into `reports/v0_9/meru_3d_v4_run_01/`; add only the independent checker, its JSON, this review, the manifest, and the results-freeze note. No earlier signed scientific files or protocol are modified. The original calculator is *not* rerun. Human verifies the **18 added-file** staged scope and GPG-signs a direct-child commit of `d7b5359f857b5a294746dc6bce5a61e50d169022`.

**Next independent question:** a separately signed, target-blind study may address source-justified Meru candidate wire/curve geometry and independent null families, but only with explicit forward-model and geometric admissibility; any historic image or Hebrew target-use gate requires separate authorisation.
