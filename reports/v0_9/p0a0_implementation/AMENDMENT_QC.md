# Bounded P0A0 implementation-only QC amendment

Status: **CORRECTIONS PREPARED FOR INDEPENDENT REVIEW — NOT FROZEN; NO FINAL QC APPROVAL CLAIMED.**

The existing workspace was resumed, not restarted. Before editing, the original
ZIP SHA-256 was verified as
`a6d54c700855140e7bec717ac58125cba1e5749aa7b04baaf00d778ca7323440`,
all its checksums passed, and all 22 packaged paths matched the current workspace.
The original ZIP remains unchanged. Its signed baseline and verification evidence
were reused; no historical mathematics or registered pilot was repeated.

## Corrections and scope

| Item | Correction | Bounded evidence |
|---|---|---|
| B01 | Replace 22 registered `assert` statements with explicit invariant calls; reject optimized Python both at runner entry and freeze verifier | 22/22 predicates AST-identical; explicit failure survives `-O`/`-OO`; runner rejects `-O`, `-OO`, `PYTHONOPTIMIZE=1` before arguments/IO |
| B02 | Supply S11 local search bounds from its unchanged serialized `local_bounds` through a restricted parser | Unrelated rational/pi DEV inputs accepted; malformed, inverted, zero-denominator and executable-expression strings rejected; no `eval`; registered source AST confirms config binding |
| R01 | Require successful raw Git verification and the exact expected signing fingerprint | Expected signer accepted; wrong signer/primary, absent/malformed/multiple VALIDSIG and verification failure rejected; mocked Git wiring stops before file/fixture access |
| R02 | Run DEV checks and the controlled suite with only the two named image tests deselected | 59 DEV passes; 1,281 controlled passes and 2 deselections; original negative logs retained byte-for-byte |

The signer is `D4EC014EEFCC90E619D2AA59A91239ABCF512130`. A different
signing subkey is rejected even if related to that primary key. This conservative
identity rule can be amended only through later authorized review if necessary.
Successful Git verification is still required; matching text alone does not
constitute cryptographic verification.

## Actual commands and results

```bash
PYTHONPATH=src python -m pytest -q \
  tests/test_p0a0_dev.py tests/test_p0a0_qc_boundaries_dev.py
```

**59 passed in 2.22 s:** the original 28 DEV tests plus 31 amendment boundary tests.
The optimized subprocess checks use unrelated boolean conditions or stop at the
runner's optimization guard. No registered module was imported or executed.

```bash
PYTHONPATH=src MPLBACKEND=Agg python -m pytest -q tests \
  --deselect=tests/test_arm_of_god_diagram_source_preparation.py::test_prepared_pngs_match_manifest_hashes \
  --deselect=tests/test_first_hand_expanded_neutral_geometry_audit.py::test_overlay_renders_from_verified_prepared_crop
```

**1,281 passed, 2 deselected in 7.50 s:** 1,222 inherited tests plus 59 DEV tests.
Only the two stated image-dependent tests were deselected. The original observed
**1,222 passed / 1 missing-crop failure / 1 deselection** log is unchanged. The
controlled result is not a claim that the image-dependent coverage gap is solved.
No crop was obtained, opened, synthesized or replaced. No inherited test was edited.

Static checks compiled nine Python files without executing registered source.
A complete AST comparison against the original cases source permits only:
(1) `assert` to explicit invariant wrapper, (2) the boundary-helper import, and
(3) the specified config bounds binding. With those transformations normalized,
the whole registered cases AST is identical. Every original mathematical predicate,
case ID and tolerance is preserved. Config, generator, engineering routines,
oracles, original DEV source and original verification records are byte-identical.
The exact hashes and evidence are in `amendment_static_preservation_checks.json`.

Environment: the same Python 3.12.14, NumPy 2.3.5, SciPy 1.17.0, pytest 9.1.1;
no dependency installation/change during this amendment. The complete original
pip inventory is retained and the current execution environment is recorded in
`amendment_environment.json`. Actual stdout logs are included separately.

## Preservation and remaining gates

- HEAD remains `d15865167b4e3c454e398bd498d9d681103096f7` on
  `hebrew-projection-capacity-v0.9`; protocol blob remains
  `0f8b663bfe2432685c9320a00c80fd6bcf436e38`.
- All 477 inherited tracked files are unchanged; no staged changes. No commit,
  push, tag, release or remote repository write. A09 metadata is unchanged and
  its local raw snapshot remains absent; no target image/geometry access occurred.
- The explicit condition wrapper still raises `AssertionError`, preserving the
  future runner's FAIL path and its original classification predicates. The
  substantive numerical algorithms, fixtures and independent oracles were not tuned.
- This is a complete replacement implementation-only package, not a patch-only
  ZIP. The manifests, package checksums, exact path inventories, documentation
  and proposed manual freeze commands have been updated. The original archive
  remains a separate unchanged record.
- The real signed implementation-freeze success path is still unexecuted because
  creating such a freeze is prohibited in this task. Signer parser/wiring checks
  use DEV status records and mocked Git calls; they do not fabricate a signed commit.
- Registered numerical behavior and the image-dependent regression coverage gap
  remain subject to the original constraints and later independent review.

`REGISTERED_S00_S12_PILOT_NOT_EXECUTED`

`NO_HEBREW_TARGET_ANALYSIS_PERFORMED`

`P0A0_IMPLEMENTATION_NOT_FROZEN`

No issue requiring changes beyond the authorized correction scope was encountered.
The amendment is submitted for independent review, not declared finally approved.
