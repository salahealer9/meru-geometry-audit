# Meru v0.9 — 3D-V4 Exact Trace and Convex Silhouette: Results Freeze

**Date:** 22 October 2026  
**Feature branch:** `hebrew-projection-capacity-v0.9`  
**Required direct parent:** `d7b5359f857b5a294746dc6bce5a61e50d169022` — signed V4 preregistration  
**Frozen protocol Git blob:** `2d57b85c066c76ae462929ece209385f5491ed78`  
**Expected human signer:** `D4EC014EEFCC90E619D2AA59A91239ABCF512130`  
**Result:** `MERU_3D_V4_EXACT_TRACE_AND_CONVEX_SILHOUETTE_EQUIVALENCE_PASS`, subject to the signed archival checks below.

## Evidence identity and review

Original human first-run archive: SHA-256 `e18ea8eff8d9d8075f4faf2016c1bbeaec3fcb8d1aa156db998a012ceede5f91`. Preserve its original **13 `run_01` files byte-for-byte** under `reports/v0_9/meru_3d_v4_run_01/`. Its script SHA-256 is `d197e231e62da7a02c627732119212178dd65deb4c1d54b958219c67072a0520`, original JSON SHA-256 is `a90cb2cce5edffe55bbd860850a255d0a54acf8cdb46b34027091fec982d154a`, and stderr is exactly empty; exit code `0`. No registered execution was rerun or modified.

An independently written, non-importing, exact-arithmetic checker reconstructed all 30 frozen observable/grid records and compared 30,320 entries in the complete SO2/O2 camera-pair equivalence matrices; **6,090/6,090 independent checks pass**. The separately archived audit source, QC JSON, review and expected SHA-256 manifest provide details. Every fixed source oracle, every per-camera trace reduction and strict hull, rank/degeneracy census, partition, class size, antipodal law and nested-grid monotonicity condition passed.

| Grid | TR-L | TR-S | TR-C | CS-T | CS-B |
|---|---:|---:|---:|---:|---:|
| A/B G0 | 1/1 | 6/3 | 6/3 | 6/3 | 3/3 |
| A G1 | 2/2 | 14/7 | 12/6 | 14/7 | 5/4 |
| A G2 | 3/3 | 26/13 | 23/12 | 26/13 | 8/7 |
| B G1 | 2/2 | 18/9 | 17/9 | 18/9 | 6/6 |
| B G2 | 4/4 | 42/21 | 41/21 | 41/21 | 12/12 |

All table entries are distinct `SO(2)/O(2)` **geometric equivalence classes**, not counts of historical letterforms. The higher-tier non-line counts were intentionally not preregistered as numerical oracles; they were determined by the frozen run and then independently checked.

## Interpretation boundary

This V4 result concerns **continuous path-order-aware piecewise-linear traces** and **filled orthographic convex-solid silhouettes** of five target-blind controls. It is not a test of general nonconvex-wire silhouettes or occlusion, physical light-source shadows, historical Meru wire geometry or Hebrew-letter specificity. No previous signed results change. Source-first candidate geometry, null comparisons and any Hebrew target gate require distinct preregistered studies.

## Human signed results-freeze gate

Stage *only* the new result-freeze note and `reports/v0_9/meru_3d_v4_run_01/` containing the original 13 unchanged files plus four new review/QC/manifest additions. Verify current exact Git HEAD/upstream = signed preregistration, signed fingerprint, protocol Git blob, two checksum manifests, empty stderr, exit status, and **exactly 18 added files**. No modify/delete paths. The human GPG-signs and pushes a direct-child commit. Any failed check is a hard stop; never reconstruct or rerun the original experiment to force a PASS.
