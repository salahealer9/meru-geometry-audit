# QO2D-M1 — Eight-case mathematical microvalidation results freeze

**Date:** 22 October 2026  
**Programme:** Meru Geometry Audit v0.9, target-blind 2D ordered open-path QO study  
**Repository:** `salahealer9/meru-geometry-audit`  
**Branch:** `hebrew-projection-capacity-v0.9`  
**Required direct parent of this additive result commit:** `6bfa644bb161d8cd6d3866118efbbabce892c3f5` (GPG-signed preregistration; GitHub signature attested valid during review).  
**Expected human GPG fingerprint:** `D4EC014EEFCC90E619D2AA59A91239ABCF512130`.

## Scientific disposition

**`QO2D_M1_EIGHT_CASE_MICROVALIDATION_PASS` — restricted numerical agreement with eight preregistered synthetic mathematical benchmarks.** Seven evaluable cases match the independent analytical values to absolute tolerance 1e−10 for correlation components, score, witness matrix, determinant and directly integrated squared residual. One invalid case is rejected as preregistered. The uploaded program exited with code 0. This is a mathematical microvalidation, *not* an all-input software correctness certificate.

| Case | Frozen analytical result | Observed disposition |
|---|---|---|
| M01 | QO=0; rotation +90° | MATCH |
| M02 | QO=0; identity, one zero edge | MATCH |
| M03 | QO=2/sqrt(5), reflection prohibited | MATCH |
| M04 | QO=2/sqrt(5), traversal reversal prohibited | MATCH |
| M05 | QO=sqrt(2); exact tie, identity witness | MATCH; exact tie follows from independent mathematics |
| M06 | QO=sqrt(2−2/sqrt(262145)); unique identity | MATCH; positive correlation |
| M07 | Zero total arclength, no score or witness | NOT_EVALUABLE_AS_EXPECTED |
| M08 | QO=0 at exact level; tiny positive segment | MATCH; reported finite-precision score about 3.162e−40 |

## Original evidence, authorship and limitations

Preregistered protocol: `docs/v0_9/qo2d_m1_target_blind_microvalidation_preregistration_2026_10_22.md`, committed in the exact parent `6bfa644bb161d8cd6d3866118efbbabce892c3f5`. Operator-uploaded original `results.json` SHA-256 `df5fe38a226c630868fd076c69a7621245f21663445e859a2541e84e6a76c4ba`; `exit_code.txt` SHA-256 `9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa`; matching Python script SHA-256 `08c1c87aa4e972cddfc49fc37192a7a36252a70e5712d1ce960b21b1cf743831`. The numerical review SHA-256 is `a0a9a4d52654318e14c3d39dffb63ec7dc2fe033e69bab59a94c57e6a338467b`. The source run records Python 3.11.2, 80 decimal digits, and UTC timestamp `2026-10-22T07:41:35.443347+00:00`.

The independent numerical *oracle method* used separate analytical values, not the calculator's output as its own standard; however, **the script and the review were both prepared with ChatGPT assistance**. This is not evidence of institutional reviewer independence. The user supplied `results.json` and `exit_code.txt`; the operator-reported empty stderr and additional time/hash metadata were not uploaded for external inspection. At preservation, copy those **original local files** from the operator's `evidence/run_01/` and verify `stderr.txt` is byte-empty. Do not synthesize a substitute stderr or rewrite original logs. This is evidence-content review, not continuous observation of the operator host.

The results do **not** establish correctness for all ordered paths, exact zero from floating-point outputs, 3D Meru historical reconstruction, Hebrew glyph specificity, model-vs-null comparison or a production-ready mathematical application. P0A3D abstract theorem and prior unqualified software statuses remain separate. P0A3H-P1 remains `P0A3H_P1_ADMINISTRATIVELY_CLOSED_INCOMPLETE` and is not reopened. No P0A4 or target-image permission is granted by signing this result.

## Preserved objects and signing boundary

The `reports/v0_9/qo2d_m1_microvalidation_run_01/` folder holds the exact originally recorded operator run evidence (copied from `~/meru-qo2d-m1/evidence/run_01/`), original standalone calculator, the dated numerical review, the checksum list and evidence-copy scope note. Raw files must be **copied, not regenerated or executed again**. `EVIDENCE_SHA256SUMS.txt` checks the separately obtained original `results.json`, `exit_code.txt`, calculator, reviewer report and the operator's empty stderr. The other original metadata files are included as retained operator records and are not independently authenticated by prior uploads.

This freeze adds documentation and evidence only; it modifies no previous scientific file. Before signing, the human verifies a clean prior worktree, the exact named parent, all expected checksums and no unexpected staged files, then creates one additive `git commit -S` and pushes. The document is a **signing candidate** until that commit is independently verified.

## Next programme — separately scoped

With M1 numerically reviewed and signed, proceed to a new target-blind **3D effective viewing-capacity study**: quotient-identified camera directions, normalized 2D projection observables, and matched geometric controls. Establish view equivalence and degeneracy handling before any scoring. No real Hebrew target use without a separate rights/observation/target preregistration.
