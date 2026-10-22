# Meru 3D-V1 — Signed result-freeze candidate (finite direction census and separation)

**Date:** 22 October 2026.  
**Branch:** `hebrew-projection-capacity-v0.9`.  
**Required direct parent:** `0e5c1ea4837cf2d2a169fb03c97179e929c3a8ed` — human-signed 3D-V1 protocol.  
**Protocol blob:** `217c2b3a3ab06846acaf767636f1efb95ef0e348`.  
**Expected human signer:** `D4EC014EEFCC90E619D2AA59A91239ABCF512130`.

## Scientific result and scope

**Proposed result upon human signing:** `MERU_3D_V1_FINITE_DIRECTION_CENSUS_AND_SEPARATION_PASS`. A single first-run calculator execution reported exit code `0`, and a **separately written, non-importing, read-only independent enumeration** passed **200/200 exact arithmetic checks** against the preregistered direction sets, complete signed and axis pair tables, maximizing witnesses, antipodal structure, and per-stratum summaries. No registered source rerun was performed by the reviewer. The report is explicitly finite-grid and target-blind.

| Family | Tier | Signed directions | Axes | Signed unordered pairs | Axis unordered pairs | Exact maximum distinct signed dot | Minimum angular separation (display) |
|---|---|---:|---:|---:|---:|---|---:|
| A | G0 | 6 | 3 | 15 | 3 | `0` | 90° |
| A | G1 | 14 | 7 | 91 | 21 | `1/√3` | 54.735610317° |
| A | G2 | 26 | 13 | 325 | 78 | `2/√6` | 35.264389683° |
| B | G0 | 6 | 3 | 15 | 3 | `0` | 90° |
| B | G1 | 18 | 9 | 153 | 36 | `1/√2` | 45° |
| B | G2 | 42 | 21 | 861 | 210 | `3/√10` | 18.434948823° |

The A/B G0 entries refer to the same six-direction set. The axis angular minima equal the corresponding signed minima for these antipodally closed direction sets, but axis **counts differ**. Angle displays use floating point; all acceptance comparisons were exact and based on integer dot products/norms.

## Original evidence and independent inspection

The **unaltered local** directory `~/meru-3d-v1/evidence/run_01` is to be copied into `reports/v0_9/meru_3d_v1_run_01/`, without rerunning any experiment. Its 11 expected original files are `meru_3d_v1_standalone_calculator.py`, `preregistration_commit.txt`, `preregistration_blob.txt`, `python_version.txt`, `start_utc.txt`, `command.txt`, `results.json`, `stderr.txt`, `exit_code.txt`, `end_utc.txt`, and `SHA256SUMS.txt`.

Original operator-supplied `SHA256SUMS.txt` lists these three exact hashes:

```
1ef01cb26eb44ba145bb6d571c837b87f66e97fea1b69d3649b04854cf3a7428  meru_3d_v1_standalone_calculator.py
2fd5b37533ccf1d9b380c1741796dae3a0a1f07bce4877a1ac5ebfc6f8d01561  results.json
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  stderr.txt
```

The original script and `results.json` **were separately provided** to the independent reviewer and independently hashed to those values. The exit-code upload is a two-byte `0\n` record. The supplied stderr hash is the known SHA-256 of an empty file; its **actual original bytes must be confirmed locally** using `sha256sum -c` before signing. The uploaded checksum record has been checked against its stated identities. The first-run timestamps and shell command are preserved as operator records, not reconstructed or independently observed.

The earlier immutable review files are copied unchanged into this checkpoint:

- `MERU_3D_V1_INDEPENDENT_MATHEMATICAL_REVIEW_2026-10-22.md` — SHA-256 `a12d959bec3c60f2d02df09f834bf0f4eda4e6c145c626e2df1c6eb8b7b8c2ac`;
- `MERU_3D_V1_INDEPENDENT_QC_2026-10-22.zip` — SHA-256 `4dd392b96aa475d6de965f14e05025d859c0f56ec4b81323489bf5e8cfc2432c` (includes the separately written independent checker source and 200-check machine-readable audit).

An additive `EXPECTED_EVIDENCE_SHA256SUMS.txt` checks the copied source/results/stderr and the two independent-review artifacts; the locally retained original `SHA256SUMS.txt` is also preserved. Signed Git history anchors the assembled additive result set after the human verifies hashes and approves the exact staged diff.

**Scientific limitations:** The result concerns enumerated candidate finite viewing directions only. It does not establish continuous-sphere covering radii, object-specific silhouette diversity, a Meru 3D construction, camera-optics realism, Hebrew-letter specificity, general 3D QO/QH software correctness, or any P0A4/P1 release. The unresolved v0.8 FIRST HAND source-construction status remains in force. No prior science, original evidence or protocol is edited, and no additional experiment is authorized by this archival result freeze.

## Human-only administrative procedure

Require clean exact parent `0e5c1ea4837cf2d2a169fb03c97179e929c3a8ed`, branch and upstream agreement, valid signature, original first-run files with unchanged SHA-256, exact 15 new-file staged scope, and no unexpected changes. Human GPG-signs and pushes a single additive commit. Before signing, this file is a **candidate** and the PASS statement refers to independently reviewed submitted results, not a new signed freeze. If essential identity or byte checks fail, stop; do not reconstruct or rerun evidence.

**Next separately preregistered scientific question:** Meru 3D-V2 — spherical/projective covering radius for these already defined finite camera grids. Finite separation does not determine the continuous-space covering radius.
