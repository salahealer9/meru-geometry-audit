# P0A0 implementation-only independent QC handoff

**Current package: bounded independent-QC amendment, awaiting independent review.**
See `AMENDMENT_QC.md` for B01/B02/R01 corrections and R02 validation:
59 DEV checks passed; the controlled suite passed 1,281 tests with exactly the two
known image-dependent tests deselected. The original missing-crop failure below
and all original verification logs are preserved unchanged. No registered pilot,
Hebrew analysis, commit, push or implementation freeze occurred.

The remaining original report records the initial implementation checkpoint.
Its historical counts and descriptions do not replace the amendment report.


Status: **IMPLEMENTATION PACKAGE PREPARED FOR INDEPENDENT QC; NOT FROZEN.**
The registered S00–S12 pilot is unexecuted. No engineering-pilot-ready state is
assigned. No Hebrew target analysis, scientific scoring, commit, staging, push,
PR, tag or release was performed.

## Verified authority

The scratch workspace initially had only the uploaded handoff and no checkout.
The named branch was cloned directly from GitHub without resetting user work.
The complete 290-line frozen protocol was read from that checkout and the exact
commit was also retrieved with the GitHub connector.

- Repository: `salahealer9/meru-geometry-audit`
- Branch and upstream: `hebrew-projection-capacity-v0.9`, same branch at origin.
- HEAD: `d15865167b4e3c454e398bd498d9d681103096f7`
- Parent: `8bf0babfd91bdefb0792e93707fd0b0da1c09767`
- Protocol Git blob: `0f8b663bfe2432685c9320a00c80fd6bcf436e38`
- Protocol SHA-256: `afee667eb578e329e80b8d28dc071ebebab3ae75a2e053b1f67d2c68f037743b`
- Signature: `git verify-commit` succeeds with fingerprint
  `D4EC014EEFCC90E619D2AA59A91239ABCF512130`.

The key was initially absent. Its public copy was retrieved from the named
GitHub user's `.gpg` endpoint and the fingerprint matched before import. Import
reported a gpg-agent startup warning but imported the public key successfully;
subsequent commit verification returned exit 0 and a good signature. Local
owner trust is unknown; this report does not claim a web-of-trust certification.
No private key was accessed. Signature evidence is recorded without publishing
personal email addresses.

## A09 source barrier

Text-only CSV parsing found exactly one A09 row in each frozen registry and
compared every applicable protocol identity field. The SHA-256 in that metadata
matches the protocol, but no actual image-byte hash was measured:

`A09_SNAPSHOT_NOT_LOCALLY_PRESENT`

A09 was not downloaded. No source image was decoded, displayed, cropped, traced,
OCRed or scored. No real letter coordinates or fonts entered new fixture design.
The package contains only new code, synthetic definitions and textual QC files;
no source-image bytes or original handoff/private correspondence are redistributed.
A09 retains its `Local snapshot only; metadata committed` policy.

## What is implemented

- Additive validation, sample RMS normalization, polyline arclength resampling,
  ordered matching wrapper, sampled support distances, supplied-graph counts,
  explicit component composite, finite-width planar rasterization, silhouette
  comparison and a bounded local angular optimizer.
- Distinct scalar projection/alignment/support/raster reference paths and an
  analytic stationary-point classification for the deliberately multimodal case.
- Full S00–S12 definitions and executable planned checks, with explicit
  EXPECTED_BLIND_SPOT relationships and raw/normalized/sensitivity fields.
- A future runner guarded by a distinct signed implementation commit, exact
  artifact bytes/hashes and a clean worktree; all cases remain outside pytest.
- 28 DEV-only tests using different inputs from registered fixtures. No inherited
  production API or placeholder was replaced.

The human-readable specification matrix is in
`docs/v0_9/p0a0_implementation_specification.md`. The proposed config and
implementation manifest are in `registered_pilots/p0a0/`.

## Actual verification, including negatives

1. Initial inherited test launch failed before collection because pytest was
   absent. The complete short log is retained. Pytest 9.1.1 and its dependencies
   were then installed; no repository dependency file was altered.
2. Inherited run (before implementation):

```bash
PYTHONPATH=src MPLBACKEND=Agg python -m pytest -q tests \
  --deselect=tests/test_arm_of_god_diagram_source_preparation.py::test_prepared_pngs_match_manifest_hashes
```

Observed: **1,222 passed, 1 failed, 1 deselected, 7.79 s**. The deselected test
explicitly opens historical source-image pixels. The failure was
`tests/test_first_hand_expanded_neutral_geometry_audit.py::test_overlay_renders_from_verified_prepared_crop`:
an ignored `aog_p07_spherical_projection.png` crop was missing. Its verifier
raised at the existence check, before byte reads or image decoding. The test
called its inherited analysis helper before reaching that check; no historical
phase outputs were regenerated or rewritten. This was an inherited test run,
not a rerun of a historical scientific phase script.

The overlay dependency was discovered through that failure. Its image-dependent
coverage remains unavailable and should also be excluded in any further
synthetic-only regression command. Neither failure nor deselection was converted
to a pass; missing source images were not acquired or fabricated. **A full green
inherited suite is not claimed.** This prerequisite gap predates the additive
implementation; all 477 inherited tracked files remain unchanged.

3. DEV run:

```bash
PYTHONPATH=src python -m pytest -q tests/test_p0a0_dev.py
```

Initial 27 checks passed; after adding the protocol-only runner-boundary rejection
check, **28 passed in 0.43 s**. Both logs are included. No registered fixture module
is imported by the DEV tests. The runner module is imported only to assert that
the original preregistration cannot serve as an implementation freeze.

4. Static parsing/compilation: all seven new Python source files passed. Config
has exactly 13 cases and every ID has a source branch. This check did not import
or execute registered cases. Default collection (`python -m pytest --collect-only
-q tests`, with PYTHONPATH=src) found **1,252 tests**: 1,224 inherited plus 28 DEV;
registered case count in collection is zero. Collection does not run tests.
5. Tracked and staged diffs are empty; `git diff --check` passes. HEAD, parent,
branch, protocol bytes and unique A09 metadata remain intact. No tracked changes,
no staging and no commits. New paths are listed in `changed_paths.txt`.

## Limitations and unresolved QC gates

- Independent review and a separate implementation freeze remain required.
  Registered numerical correctness has intentionally not been measured here.
  Source/definition review cannot substitute for that later execution.
- The inherited image-dependent coverage gap described above remains open. The
  reviewer should record its disposition under the image barrier before freezing;
  do not retrieve source imagery in this checkpoint to obtain a green test badge.
- Ordered matching retains the inherited tiny-energy rejection and nonnegative
  scale boundary. Small-feature behavior and raster resolution losses are
  documented proposed diagnostics, not yet observed registered outcomes.
- Sampled support distances are not continuous Hausdorff certificates. They do
  not encode stroke identities, connectivity or endpoints. Graph counts require
  explicitly supplied graph structure; they do not recover topology from images.
- Closed-curve shifts, traversal reversal and planar reflection are explicit
  options. Front/back is not silently merged under SO(2); roll adds no effective
  views when planar SO(2) is free. The inherited 6-direction/3-axis semantics stay.
- S11 certifies only its analytic synthetic reference landscape. The numerical
  optimizer is local/bounded, with a deliberately non-global basin. No general
  global optimization reliability or future scientific metric is certified.
- Floating-point tolerances are proposed for the documented bounded inputs,
  not proofs for arbitrary magnitudes. Point coordinates beyond 1e100 are rejected;
  extremely small total extent/length below 1e-14 is rejected. Tiny graph edges
  are retained. Antialiasing and 3-D finite-width occlusion are not certified.
- Binary64/libm/SciPy portability is tolerance-based. Byte hashes certify source
  and configuration, not bit-identical future floating-point scores on all hosts.
- The environment inventory is included. Shapely, trimesh and pyvista are declared
  by inherited pyproject but absent here and were not required by observed tests.
  NumPy/SciPy and the relevant tested package versions are pinned in the record.
- The future runner's complete signed-freeze success path cannot be exercised in
  this no-commit checkpoint. Its pre-freeze rejection path passed a DEV test.
  Human authorization is still necessary even when its acknowledgement flag is set.

There is no known unresolved *definition ambiguity* in the thirteen proposed
oracles. Independent QC may reject or amend them before any registered execution.
The known limitations above are explicit scope restrictions, not omitted results.

## Input/access/output review

New design inputs: frozen protocol text, source registry text, inherited code,
metadata/documentation and test source; independent elementary coordinates only.
Inherited tests read their existing numeric/text fixtures. Source-image paths
were checked for existence but image pixels were not opened. No image viewer,
OCR, glyph/font loader or source-download command was used. The new generator
has one fixed config reader and no target-data reader. New module imports perform
no registered generation. The package allowlist excludes raw data, caches,
images, historical source files and registered output records.

`NO_HEBREW_TARGET_ANALYSIS_PERFORMED`

`REGISTERED_S00_S12_PILOT_NOT_EXECUTED`

`P0A0_IMPLEMENTATION_NOT_FROZEN`

## Review and manual freeze

Extract into a separately inspected checkout at the exact preregistration;
review additions and verify `SHA256SUMS` before applying. Do not overwrite unrelated
user work. The package's source and config contain proposed fixtures, not scores.
The suggested commands in `docs/v0_9/p0a0_human_freeze_commands.sh` are for the
human after independent QC and disposition of the regression coverage gap.
They were not executed. They include explicit paths, review steps and a signed
commit command; no push command is included. A successful manual freeze still
does not itself authorize the later pilot execution.
