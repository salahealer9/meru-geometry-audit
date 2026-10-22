# Meru v0.9 — 3D-V2 Exact Finite Grid Covering Radius: Results Freeze

**Date:** 22 October 2026
**Branch:** `hebrew-projection-capacity-v0.9`
**Required direct parent:** `db007d7429efbd41a4953b86f5eea7e026964aa8` (signed 3D-V2 preregistration)
**Protocol blob:** `3db104c82b961761dfd80b92f968f1538869bb36`
**Signed human key fingerprint:** `D4EC014EEFCC90E619D2AA59A91239ABCF512130`
**Outcome:** `MERU_3D_V2_EXACT_FINITE_GRID_COVERING_RADIUS_PASS`

## Immutable original run

Copy the human-executed `~/meru-3d-v2/evidence/run_01/` directory byte-for-byte to `reports/v0_9/meru_3d_v2_run_01/`. The original script, stdout JSON, stderr, exit code, protocol identifiers, version records, timestamps and SHA-256 manifest must remain unchanged. Do not rerun or reformat the original experiment. The signed protocol was GitHub-verified at commit `db007d7429efbd41a4953b86f5eea7e026964aa8` / blob `3db104c82b961761dfd80b92f968f1538869bb36`.

Original script: `fd63b10bd38536f83f5b6a6d35061006559e23bd5584a3dfdb7c90b59756e1d4`. Original JSON: `92af306506afe95292170a00470f99b62f13f02a3687dab81467de34d349e4b3`. The original manifest records empty stderr (`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`); that actual local file must still pass `sha256sum -c` during packaging.

## Independent mathematical decision

The attached independent read-only QC report, source and machine-readable check JSON reconstruct all chamber polytope vertices, compare all exact oracles, and establish the five distinct radii (G0 shared by both families), with **146/146 independent checks passed**. No archived Meru calculator or target data was imported or executed in the independent QC.

The six registered result records are A G0/G1/G2 and B G0/G1/G2. Radius squared-norm maxima are respectively `3`, `5-2*sqrt(3)`, `9-2*sqrt(2)-2*sqrt(6)`, `3`, `3/2`, `3/2`. B G2 adds 24 directions to B G1 without improving its worst-case spherical covering radius.

## Interpretation limit

The result certifies only exact spherical/projective covering radii of preregistered finite orthographic viewing grids. It does not establish object-specific projected shape diversity, historical source correctness, 3D Meru reconstruction, or Hebrew-letter specificity. All upstream signed scientific files remain unchanged.

## Subsequent work

The next separate, target-blind preregistration may address 3D object-specific projection equivalence on independent controls with a common forward model and matched freedoms; it must not infer actual silhouette counts from directional coverage alone.
