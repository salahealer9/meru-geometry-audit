# P0A0 registered synthetic engineering pilot — execution report

**Disposition: single registered run complete; independent human QC pending.**
The frozen runner was invoked exactly once. Its recorded states are **5 PASS,
8 EXPECTED_BLIND_SPOT, 0 FAIL, 0 NOT_EVALUABLE**. No state was changed or collapsed
into a generic pass. No repair, retuning, case rerun or additional registered
experiment was performed. `P0A0_SYNTHETIC_ENGINEERING_PILOT_READY` is not assigned.

## Authority and execution

Repository: https://github.com/salahealer9/meru-geometry-audit

Branch: `hebrew-projection-capacity-v0.9`

Scientific protocol: `d15865167b4e3c454e398bd498d9d681103096f7`, parent
`8bf0babfd91bdefb0792e93707fd0b0da1c09767`, protocol blob
`0f8b663bfe2432685c9320a00c80fd6bcf436e38`.

Implementation freeze: `24c00fc44e4d9d57adacd1e636e9e2d20d86a954`, parent exactly
the protocol commit. Both signatures were locally verified against signing and
primary fingerprint `D4EC014EEFCC90E619D2AA59A91239ABCF512130`.

The prior implementation workspace remained at the preregistration with untracked
proposed implementation files. It was left untouched. As the handoff authorizes,
a separate clean checkout was cloned directly from GitHub at the named branch,
whose HEAD was exactly the implementation freeze. Complete frozen protocol,
implementation specification, runner, fixtures, case source and numerical/oracle
implementation were read from that checkout, without importing/evaluating fixtures.
Historical PROPOSED strings were preserved; the signed commit is the authority.

Initial signature inspection found an empty current keyring. The previously
GitHub-sourced public-key file remained available; its primary fingerprint was
checked before import. Local verification of both commits then succeeded. This
was prerequisite key setup before formal preflight, not relaxation of a guard.
The runner subsequently applied its unchanged signature/fingerprint guard itself.
`signature_setup.json` preserves the setup and sanitized machine-status evidence;
personal UID/email text is excluded from this package.

Preflight passed: exact HEAD/parent/branch/upstream, clean worktree and index,
ancestry, protocol identity, all 12 implementation-manifest lengths/SHA-256s and
committed bytes, unique matching A09 metadata, matching NumPy/SciPy versions,
normal Python mode and nonexistence of the designated output. All 508 tracked
checkout files remained protected. Registered modules were not imported in preflight.

The one invocation was:

```bash
python scripts/p0a0_registered_pilot.py \
  --freeze-commit 24c00fc44e4d9d57adacd1e636e9e2d20d86a954 \
  --authorized-synthetic-run \
  --output ../p0a0_registered_pilot_once.jsonl
```

Working directory:
`/workspace/scratch/255e4cd6766b/meru-geometry-audit-pilot`.

UTC start: 2026-10-15T11:41:40.899646+00:00. UTC end:
2026-10-15T11:41:41.746898+00:00. Elapsed approximately 0.8473 seconds.
Return code **0**. Stdout and stderr each **0 bytes**, retained as empty files.
Python 3.12.14, NumPy 2.3.5, SciPy 1.17.0; `sys.flags.optimize=0`,
`PYTHONOPTIMIZE` absent. No numerical dependencies were installed or changed.
No inherited/DEV test suite was rerun in this execution phase.

## Raw evidence and structural checks

`p0a0_registered_pilot_once.jsonl` is **12,052 bytes**, preserved byte-for-byte.
SHA-256:

`4b4b27b0d5d9a95ffe864e2d2c83433be0ddd544b6122ebbea294857326817d6`

There are exactly **14 JSON records**: one boundary header and 13 distinct ordered
case IDs S00–S12. Header commit and manifest hash match preflight. Every case has
raw/normalized fields and an explicit state/explanation. NOT_APPLICABLE in a
normalization field is not a case-level NOT_EVALUABLE outcome. Every non-PASS
case is explained. No case was omitted, renamed or reclassified.

The signed implementation manifest SHA-256, also recorded by the runner, is:
`07a7e530f9bb3dc2005dc9ff5d158f95f1f6bc2b6fe7872d973e1a5198215fd0`.

`CASE_MATRIX.md` contains all 13 cases and their observed raw/normalized results.
Values are copied/formatted from the sole JSONL, not obtained by reevaluation.
Original precision remains available in the raw record. The runner checks some
transform, rejection and oracle relationships without serializing every residual,
array or transform matrix. Their assertion success is evidenced by the frozen
code path and absence of a FAIL; no unlogged numbers have been reconstructed.

## Engineering interpretation and limitations

**Projection and ordered similarity.** S00's scalar coordinate oracle matched
exactly and improper/nonfinite projection inputs were rejected. S01 recovered
scale 2.5 and translation (4,-7), with relative RMS approximately 2.45e-16. S02's
mirror mismatch was 0.557976 under SO(2), versus 1.86e-16 when reflection was
explicitly allowed. These are bounded tests of specified synthetic observations,
not a production validation for arbitrary unlabeled images.

**Sampling and path semantics.** In S03, point-index matching gave relative error
0.503076, whereas arclength resampling of the same straight polyline gave 1.55e-15.
This establishes the diagnostic on that exact segment; it does not certify
invariance to arbitrary discretization of unknown smooth curves. S09 recovered
reversal/closed shifts only under the declared options: reversal denied 0.997511,
open cyclic shift 0.462423, versus near-zero permitted matches. No open-path
cyclic shift was silently introduced.

**Topology and support non-identifiability.** S04's support errors tied at zero
although supplied stroke labels changed labelled endpoints from 2 to 4. In S06,
a detached component produced a small mean support error (0.00241421); the
explicit graph-count penalty raised the composite to 0.25241421. In S07, sampled
Hausdorff 0.03125 detects geometric change but does not identify endpoint counts;
those came from the supplied graph (2 versus 3 exposed endpoints, 0 versus 1
junction). No topology was inferred from support or raster. The composite's
weight 1/4 is a frozen synthetic diagnostic, not a selected scientific metric.
These sampled distances are not continuous-curve Hausdorff certificates.

**Resolution and local features.** S05's 1/64 gap was invisible at 33×33
(identical rasters, IoU distance 0). At 257×257 there were 7 differing pixels and
IoU distance 0.006789524733268659. Both rasters agreed with the independent
horizontal-capsule oracle within the frozen comparison tolerance. Supersample 1,
width 1/128 and fixed viewport are essential to these findings; no antialiasing
or 3-D ribbon-shadow equivalence is certified. In S08, raw sampled Hausdorff was
0.03125, normalized 0.039397874693101735; both exceeded .01 but fell below .05.
The feature can therefore be concealed by the registered larger threshold.
Normalization also changed the mean distance from .00625 to .015761060078392695.

**Degeneracy.** S10 retained tiny positive arclength increments/components,
handled exact consecutive duplicates according to the frozen policy, and raised
explicit errors for zero/nonfinite inputs. The inherited alignment's tiny-energy
floor rejected the tiny comparison as ValueError. This is a documented numerical
limit, not a successful tiny-shape match and not permission to lower the floor.

**Local optimization.** S11 returned angle 3.1415926535897936, value **0.4**,
6 function evaluations, local success true. The independent analytic global
minimum was **0** at angle 0, giving discrepancy **0.4**. The frozen bound selected
a deliberately competing local basin. Local solver success does not certify a
global optimum; no general global optimization reliability has been established.
This recorded limitation was expected and remains EXPECTED_BLIND_SPOT.

**Effective views.** S12 retained 6 signed camera directions and 3 unoriented
axes; duplication produced 13 nominal frames without increasing the signed
class count. The largest logged roll-alignment relative RMS was about 2.61e-16.
Opposite directions required a planar determinant -1 transform. Under free
planar SO(2), axial camera roll adds no effective projection capacity. No new
G0/G1/G2 viewing hierarchy or N0–N3 study was run.

## Inherited QC and documentation caveat

The frozen controlled-regression log records **1,281 passed, 2 deselected**.
The two image-dependent tests remain unexecuted coverage, not passes. The
original **1,222 passed / 1 missing-crop failure / 1 deselection** evidence was
retained in the signed implementation and is referenced in the provenance ledger.
No missing source crop was fetched, opened, synthesized or substituted.

The frozen amendment report states 59 DEV passes, and the historical conversation
records that count. However, the standalone `amendment_dev_checks.log` in the
signed checkout contains only **35 progress dots and no completion summary**.
It cannot independently substantiate the 59-pass count. This documentation
limitation is disclosed without altering frozen files or rerunning tests. The
controlled-suite completion summary is present. It does not invalidate the
current raw pilot record or its independently checked structure, but independent
QC should retain this distinction between report claims and log contents.

## Recommendation for later design

At least the explicit ordered-path projection/similarity route warrants
consideration in a later separately preregistered design, conditional on genuine
correspondence semantics, sampling definitions, degeneracy policy and permissible
transformations. The results do not make ordered matching suitable by default for
unlabeled multi-stroke images. Graph diagnostics require externally supplied,
justified graph structure; sampled-support/raster measures may be useful only
with their declared observational and resolution limits.

No Hebrew metric, component penalty, target extraction, scientific candidate,
null ensemble or confirmatory test is selected here. No global optimizer is
certified. Independent human QC must assess all protocol §13 criteria, the
expected blind spots, documentation caveat and inherited coverage gap before
assigning any engineering-readiness state or authorizing later work.

## Preservation and input/output barrier

Post-run Git status and both tracked/staged diffs are empty. HEAD and protocol
blob are unchanged; all 12 manifest-bound artifact hashes remain identical.
The earlier workspace and both implementation ZIPs were left untouched.

A09 had exactly one matching row in each CSV; its raw status remains
`A09_SNAPSHOT_NOT_LOCALLY_PRESENT`. No actual A09 byte hash was claimed from
metadata alone. No source image, font/glyph, tracing, OCR, Hebrew scoring or
candidate/null experiment entered this run. Only the frozen independent synthetic
config and code were evaluated. The package contains the immutable synthetic
JSONL, textual execution evidence, read-only reference metadata, matrix and QC
report. It does not redistribute original source images or private correspondence.

`NO_HEBREW_TARGET_ANALYSIS_PERFORMED`

`NO_COMMIT_NO_PUSH`

`FROZEN_PROTOCOL_AND_IMPLEMENTATION_UNCHANGED`
