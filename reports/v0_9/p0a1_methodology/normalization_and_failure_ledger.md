# M4 — Normalization and failure ledger

**PRE-QC proposals recovered from the completed review; no parameter selection or implementation changes.** Evidence: `reports/v0_9/p0a0_registered_execution/p0a0_registered_pilot_once.jsonl` (J), case IDs below; `docs/v0_9/p0a0_implementation_specification.md` (S), representation contracts; `registered_pilots/p0a0/fixture_config.json` (F), read as text only.

## Measure and units

[MATH DERIVATION] With fixed nonnegative observation weights w_i summing to one,

\[
\mu=\sum_iw_ix_i,\quad r=\sqrt{\sum_iw_i\|x_i-\mu\|^2},\quad \tilde x_i=(x_i-\mu)/r
\]

is defined only on a justified r>0 numerical domain. Index-uniform weights, arclength quadrature, pixel-area measure and equal-component weights are different observations. Repeated samples change empirical centroids/RMS unless weights compensate. Length weighting may suppress a tiny component; equal-component weighting may amplify it. Neither is neutral preprocessing.

[METHODOLOGICAL PROPOSAL] A later contract must fix world/image units, sample measure, component inclusion, interpolation, centering, direction of fit, reference radius, scale permissions and uncertainty. Source-to-target relative RMS may be asymmetric. Independently RMS-normalizing both objects and then fitting scale again needs explicit justification. Normalizing in 3-D before projection differs from 2-D normalization after projection; projected collapse requires explicit failure handling.

| Path | Definition / sign | Units and range | Required error/scope contract |
|---|---|---|---|
| C1–C2 | Weighted RMS of matched coordinate residuals; lower is better | Length before normalization; dimensionless with positive reference radius; nonnegative; no universal upper bound asserted for all contracts | Correspondence/measure, source→target convention and strictly positive scale domain; S01 bounded transform evidence, S03 segment-only resampling evidence |
| C2 sampling | Ordered piecewise-linear arclength; open endpoints included, closed wrap/terminal duplication explicit | Total length positive; P0A0's 129 samples are historical, not selected for future targets | Exact consecutive duplicates removed only under declared semantics; positive increments retained or loss reported; smooth interpolation/chord/quadrature bounds require later oracle |
| C3 | Half sum of directed means of Euclidean nearest distances; lower is better | Length or declared dimensionless normalized units; nonnegative | Set/multiset and directional weights explicit; sampling/measure error distinct from nearest-distance arithmetic; not generally triangle-inequality metric |
| C4 | Maximum directed maximum nearest distance; lower is better | Length or normalized units; nonnegative for nonempty finite/compact sets | Continuous claim needs certified all-component sampling covers, not just many points; outliers retained unless independently modeled |
| C5 | Component, exposed endpoint, junction, stroke and labelled-endpoint counts reported separately; count discrepancy lower is better when defined | Dimensionless integers; not geometric length | Supplied incidence and uncertainty; graph error is not a floating tolerance; equal counts do not prove isomorphism |
| C6 | Binary-mask IoU or 1−IoU; explicitly higher/lower is better respectively | Dimensionless [0,1] for nonempty union | Common viewport/grid/pixel area, width-scale law, clipping, supersampling, threshold and interpolation; coverage variants require their own definition |
| C7 | Fixed weighted sum of separately reported terms; lower is better only with consistent term sign | Commensurate normalized terms or dimensioned conversion weights; range needs term bounds | Required observables cannot be omitted silently; common joint nuisance domain; no weights selected here |
| C8 | NOT_ESTABLISHED | Geometry, optics and observation units UNRESOLVED | Define and validate physical forward model before a numeric score contract |

[MATH DERIVATION] If finite A_s,B_s approximate compact A,B with certified Hausdorff errors δ_A,δ_B, triangle inequality gives

\[
|d_H(A,B)-d_H(A_s,B_s)|\le\delta_A+\delta_B.
\]

Add independently bounded arithmetic and optimization errors. This requires coverage of every component in both directions. No P0A0 cover certificate is supplied. Empirical Chamfer also needs a measure-discrepancy argument; the Hausdorff inequality does not automatically control changed weights. Cross-representation comparisons need declared forward operators and compatible units.

## Precision, uncertainty and thresholds

[FROZEN RESULT] F fixes binary64, absolute coordinate/coverage tolerance 1e-10, normalized-score tolerance 1e-9, and relative tolerance zero. These are engineering checks, not target uncertainty tolerances. J S08 records raw H=0.03125 and normalized H=0.039397874693101735, both above 0.01 and below 0.05. Those thresholds expose sensitivity, not optimal future values. S05's 33×33/257×257 grids, width 1/128 and supersample 1 likewise remain historical diagnostic settings.

[METHODOLOGICAL PROPOSAL] Independently account for observation/extraction uncertainty, sampling/interpolation, mesh/raster approximation, arithmetic and optimization error. State domain hypotheses, how bounds combine and how scale magnifies length error. Binary64 agreement on isolated cases is not a uniform proof. Thresholds must be target-independent and justified by observation/approximation limits, with signed sensitivity/multiplicity rules. Hand drawing, crop, brush width and transcription uncertainty require a later source/extraction model; they cannot be tuned after viewing a letter.

## Deterministic proposed state contract

These operational states do not alter frozen case-level PASS/EXPECTED_BLIND_SPOT outcomes.

| Condition | Proposed treatment | Required diagnostic |
|---|---|---|
| Malformed dimensions, nonfinite values, invalid graph IDs/partition or invalid coverage | INVALID_INPUT, no score | Offending contract/field; never NaN→0 |
| Missing correspondence, graph, closure, calibration or physical model | NOT_EVALUABLE, no score | Missing observable and future authority; no fabricated labels |
| Empty/empty supports or empty-union masks | NOT_EVALUABLE | Empty observation reason, not perfect-match default |
| Empty/nonempty support for nearest-distance curves | NOT_EVALUABLE | Missing side/reason; infinity is not an ordinary finite degraded score |
| Valid empty/nonempty masks with nonempty union | Finite degraded IoU distance 1 | Raster-only convention; check clipping did not create emptiness |
| Zero extent or zero arclength | NOT_EVALUABLE for normalized path comparison | Retain degeneracy; point-object comparison would be a different contract |
| Tiny positive extent below inherited alignment floor | NOT_EVALUABLE within current solver domain | J S10 ValueError retained; nonzero geometry is not a successful tiny match |
| Exact consecutive duplicates | Only declared arclength duplicate removal; otherwise explicit input/measure decision | P0A0 removal was for arclength only; index weights and retracing can change |
| Self-overlap / projected crossing | Finite geometric score if valid; graph interpretation may remain NOT_EVALUABLE | Crossing does not imply junction, same vertex, depth order or stroke identity |
| Tiny detached component / spur | Retain finite support discrepancy and independently supplied graph diagnostics | S06/S07/S10: small is not absent; exclusion needs authority |
| Raster aliasing hides gap / threshold hides notch | Finite score with resolution/threshold limitation | S05/S08; zero mask error is not equal continuous shape |
| Timeout, nonconvergence, unbounded domain or unattained s>0 infimum | No claimed certified minimum; NOT_EVALUABLE for that claim, with optional feasible LOCAL_ONLY result | Failure, last feasible objective and bounds separately recorded |

## Failure → remedy → new freedom → validation

All remedies are prospective and require later authority; none is performed here.

| Failure / evidence | Proposed remedy | New freedom introduced | Mandatory validation / signing gate |
|---|---|---|---|
| Density-sensitive index fit, S03 | Arclength resampling | Interpolation, quadrature, count and endpoint convention | Independent polyline/smooth-curve bound, traversal provenance; signed target-free validation |
| Missing stroke labels, S04 | Independent supplied graph | Segmentation, crossings/junctions, partition and permutation | Licensed annotation, disagreement model and combinatorial oracle |
| Invisible gap, S05 | Predetermined finer resolution or uncertainty interval | Grid, viewport, subpixel rule | Coverage oracle and error budget before targets; no per-target escalation |
| Component dilution, S06 | Separate graph counts or alternative declared measure | Component weights, penalties, inclusion rules | Independent observability, target-free rationale and sensitivity; no inherited 1/4 constant |
| Endpoint/spur blindness, S07 | Supplied incidence diagnostics | Graph and junction semantics | Independent annotation/graph validity, not inferred support labels |
| Notch concealed, S08 | Preregister normalization/threshold sensitivity | Measure and tolerance family; multiplicity | Independent uncertainty rationale; retain all planned sensitivities |
| Tiny positive rejection, S10 | Future stable solver or justified rescaling | Precision, epsilon, scaling domain | New signed implementation/validation amendment and independent scale-limit oracle; do not patch now |
| Outliers/noise | Robust loss or exclusion only under model | Trim fraction, loss tuning, sample selection | Target-independent contamination model and retention audit |
| Broken strokes/gaps | Morphology, skeleton repair, joining/snapping only if justified | Structuring element, radius, connectivity, endpoints | Signed extraction method, independent topology/distortion validation |
| Jagged edges | Smoothing/antialiasing only if declared | Kernel, bandwidth, boundary rule, subpixel count | Independent small-feature bound and sensitivity before targets |
| Partial crop/missing stroke | Explicit missingness rather than preferred piece deletion | Crop, masks, partial correspondence | Source-licensed protocol, missingness model, matched control treatment |
| Local basin, S11 | Complete exhaustion, analytic proof or certified global bound | Domain completeness, accuracy/runtime policy | Independent certificate in separately signed validation; multistart alone insufficient |

No smoothing, repair, filtering, morphology, thresholding, component deletion or masking is innocuous. Preserve unsuccessful and limited results and count every added freedom.
