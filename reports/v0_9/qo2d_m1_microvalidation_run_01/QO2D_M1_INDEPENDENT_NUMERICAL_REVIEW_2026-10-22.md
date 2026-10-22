# QO2D-M1 — Independent Numerical Evidence Review

**Date:** 22 October 2026  
**Disposition:** `QO2D_M1_EIGHT_CASE_MICROVALIDATION_PASS` (restricted to the eight signed synthetic fixtures)

## Grounded inputs

- Human-signed preregistration commit: `6bfa644bb161d8cd6d3866118efbbabce892c3f5` (GitHub verified; proper direct parent `daa39bb6d41cacadfeb4e51f753e35cf2531dada`).
- Pre-registered eight analytic α, β, score, optimal rotation matrices, and direct squared residuals: signed `QO2D-M1` protocol (no target images).
- Operator-supplied `results.json`: SHA-256 `df5fe38a226c630868fd076c69a7621245f21663445e859a2541e84e6a76c4ba`.
- Operator-supplied `exit_code.txt`: `0`, SHA-256 `9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa`.
- Recorded source SHA-256 in JSON: `08c1c87aa4e972cddfc49fc37192a7a36252a70e5712d1ce960b21b1cf743831`, equal to the inspected calculator source bytes.
- Python 3.11.2; `Decimal` precision 80 digits; recorded run timestamp `2026-10-22T07:41:35.443347+00:00`.
- The operator reports `stderr.txt` is empty; it was not supplied for separate verification.

## Independent analytical-oracle comparison

An independent **read-only** review evaluated the preregistered closed-form expected values using separate 110-digit Decimal arithmetic and compared the uploaded case fields; it **did not execute or import** the experimental calculator. Per evaluable case, checked α, β, strength, score, all four rotation-matrix entries, determinant, formula squared residual and the calculator’s recorded direct-integrated squared residual, each against the independent analytic squared-residual oracle. Each of these is required to agree with its fixed oracle to absolute error ≤1×10⁻¹⁰. The zero/near-zero, reflection/reversal and invalid-input distinctions were also checked.

| Case | Review verdict | Largest absolute numeric difference | Additional condition |
|---|---|---:|---|
| M01 | `MATCH` | 3.333E-81 | All frozen fields within 1e−10 |
| M02 | `MATCH` | 1.200E-159 | All frozen fields within 1e−10 |
| M03 | `MATCH` | 2.342E-82 | All frozen fields within 1e−10 |
| M04 | `MATCH` | 2.342E-82 | All frozen fields within 1e−10 |
| M05 | `MATCH` | 1.000E-79 | All frozen fields within 1e−10 |
| M06 | `MATCH` | 1.520E-79 | All frozen fields within 1e−10 |
| M07 | `NOT_EVALUABLE_AS_EXPECTED` | — | Zero arclength; no score/witness |
| M08 | `MATCH` | 3.162E-40 | All frozen fields within 1e−10 |

## Qualifications

- M08 has a finite-precision score of about `3.16227766e-40` rather than exactly zero, with near-unity strength and a formula-based squared residual of `1e-79`; direct integrated squared residual is zero. This is well within the registered absolute tolerance. It must **not** be reported as an exact machine zero.
- M01 and M02 have zero score at recorded precision, with negligible nonzero direct residuals from Decimal rounding. M05's all-rotation tie is established **analytically** from the preregistered path symmetry, not by interpreting a Decimal-computed zero as a universal exact-arithmetic certificate. M06 has a strictly positive numeric correlation near `0.00195312127`.
- `exit_code=0` establishes successful program termination, **not** correctness independently. The eight-case QC derives from separate comparisons above.
- The reviewer received `results.json` and `exit_code.txt`, but not the complete local `evidence/run_01` folder or independent local-host testimony. Execution chronology and empty stderr are operator reports; this is an arithmetic and evidence-content review, **not** a general-purpose security audit or exact-software certification.
- The result confirms the eight synthetic mathematical benchmarks only. It does **not** validate arbitrary inputs, historical 3D Meru geometry, Hebrew glyph correspondence or a production application. The P1 closeout remains unchanged.

**Outcome:** Seven valid cases `MATCH`; one invalid case `NOT_EVALUABLE_AS_EXPECTED`; **eight registered case outcomes consistent with the signed mathematical protocol**. Preserve original `run_01` files without reruns or modification. This report is an independent assessment prepared after receiving the first-run outputs, not a new preregistration or a signed Git freeze.
