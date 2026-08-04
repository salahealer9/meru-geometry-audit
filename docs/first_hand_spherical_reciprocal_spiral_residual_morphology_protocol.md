# First Hand spherical reciprocal-spiral residual morphology protocol

**Checkpoint:** v0.8  
**Status:** protocol frozen before residual-morphology calculation  
**Analysis class:** neutral post-fit residual morphology

## Purpose

Diagnose the structure of the already-frozen residual field from the primary
spiral-only reciprocal-shape test.

The purpose is not to improve the fit.

The questions are:

1. Is the model failure distributed broadly across the spiral or concentrated
   in particular visible source segments?

2. Is the residual a smooth systematic function of radial position?

3. Does residual structure repeat with printed winding phase?

4. Do the two independent acquisition passes reproduce the same residual
   morphology point by point?

A reproducible structured residual would indicate missing systematic geometry
rather than acquisition noise.

## Frozen parent result

Use only the already-frozen primary reciprocal-shape result:

    data/derived/first_hand_arm_of_god/qc/
    first_hand_spherical_reciprocal_spiral_shape.json

and its frozen transformed sample table:

    data/derived/first_hand_arm_of_god/qc/
    first_hand_spherical_reciprocal_spiral_shape_samples.csv

Parent analysis:

    alpha_unwrapped = a + m * F(rho)

with

    F(rho) = (1-rho^2)/(2*rho)

and primary weighting:

    visible-curve length

No model parameter is recomputed.

## Authoritative residual

For each transformed sample use the already-frozen primary field:

    residual_alpha_length_rad

and the corresponding already-frozen fixed-rho angular chord discrepancy:

    angular_chord_length_px

Do not recompute a, m, k, alpha0, or residuals from the raw traces.

The frozen sample CSV is the numerical parent object for this audit.

## Frozen sample correspondence

Each pass contains:

    10 segments

with

    401 uniformly arclength-resampled samples per segment.

Pair Pass 1 and Pass 2 only by:

    segment_id
    sample_index

because segment correspondence and resampling were frozen before the primary
shape calculation.

No numerical nearest-neighbour matching is permitted.

No cross-pass alignment is permitted.

## No new fit

Forbidden:

- refitting k;
- refitting alpha0;
- changing handedness;
- adding an angular offset;
- subtracting a fitted trend from the residual;
- fitting splines;
- fitting polynomials;
- fitting Fourier modes;
- fitting anisotropic maps;
- fitting a 2x2 map;
- fitting a 3x3 projective map;
- nonlinear warping;
- ICP;
- Procrustes registration.

All statistics below are descriptive summaries of the frozen residual field.

## A. Segment morphology

For each pass and each source segment S01 through S10 report:

    signed mean angular residual
    median absolute angular residual
    RMS angular residual
    p95 absolute angular residual
    maximum absolute angular residual

in degrees.

Also report:

    RMS angular chord discrepancy in pixels
    p95 angular chord discrepancy in pixels

For the primary length weighting compute each segment's fraction of total
weighted squared angular error:

    SSE_fraction_s =
        SSE_s / sum_s(SSE_s)

where the sample weights are the already-frozen primary length weights from
the sample table.

This identifies whether one or a few source runs dominate the failure.

No segment is excluded.

## B. Radial residual morphology

Use the frozen normalized page radius:

    rho

with the full preregistered model domain:

    0 <= rho <= 1.

Use exactly:

    20 equal-width bins

with edges:

    0.00, 0.05, 0.10, ..., 0.95, 1.00.

For each pass and each non-empty rho bin report:

    sample count
    total primary weight
    weighted signed mean residual
    weighted RMS residual
    weighted p95 absolute residual
    weighted RMS chord discrepancy

No adaptive binning is permitted.

Empty bins remain explicitly reported as empty.

## C. F(rho) morphology

Because

    F(rho) = (1-rho^2)/(2*rho)

is a monotonic transform of rho on the open unit disk, F-domain morphology is
descriptive and not independent evidence.

Use the already-frozen:

    F_rho

values.

Define a common pooled observed F range using the minimum and maximum values
already present in the two frozen sample tables.

Divide that closed pooled range into exactly:

    20 equal-width bins.

The pooled range is used only to make Pass 1 and Pass 2 directly comparable.

For each non-empty bin report the same descriptive quantities as for rho.

Do not treat rho-bin and F-bin results as independent statistical evidence.

## D. Printed winding phase morphology

Define printed page winding phase directly from the frozen observed azimuth:

    phase =
        alpha_unwrapped_rad mod (2*pi).

Do not use model-predicted alpha to define phase.

Divide [0, 2*pi) into exactly:

    36 equal phase bins

of:

    10 degrees each.

For every pass and phase bin report:

    sample count
    total primary weight
    weighted signed mean angular residual
    weighted RMS angular residual
    weighted p95 absolute residual
    weighted RMS chord discrepancy

This is a descriptive periodic morphology audit only.

No Fourier model is fitted.

## E. Source-order morphology

Define deterministic source progression:

For segment number s in 1..10 and resampled index i in 0..400,

    q =
        ((s-1)*401 + i) / (10*401 - 1).

Thus:

    0 <= q <= 1

and q uses only frozen source order.

Divide q into exactly:

    20 equal-width bins.

Report the same weighted residual summaries.

This permits localization of broad residual structure without interpolation
across hidden source gaps.

The q coordinate does not imply physical arclength continuity across those
gaps.

## F. Pointwise cross-pass replication

Pair every Pass-1 sample with Pass-2 by:

    segment_id
    sample_index.

For the paired primary angular residuals report:

    N pairs
    Pearson correlation coefficient
    signed mean difference
    mean absolute difference
    RMS difference
    p95 absolute difference
    maximum absolute difference

in degrees.

For paired chord discrepancies report:

    Pearson correlation coefficient
    signed mean difference
    mean absolute difference
    RMS difference
    p95 absolute difference
    maximum absolute difference

in pixels.

No cross-pass offset is removed before these calculations.

## G. Residual sign replication

For every paired sample classify residual sign as:

    positive
    zero
    negative.

Use an exact numerical zero only for the zero class.

Report:

    positive-positive fraction
    negative-negative fraction
    opposite-sign fraction
    zero-involving fraction
    overall same-nonzero-sign fraction

This is descriptive only.

## H. Segment-level cross-pass replication

For each segment S01 through S10 report:

    Pearson correlation of paired angular residuals
    RMS Pass1-Pass2 residual difference
    signed mean Pass1-Pass2 residual difference

and the corresponding chord-discrepancy quantities.

This tests whether any locally unusual morphology is itself reproducible.

## I. Residual amplitude relative to acquisition reproducibility

Carry the already-frozen continuous-trace reproducibility context:

    RMS_equal  = 0.887258846871 px
    RMS_length = 0.956050554591 px

and descriptive spiral half-stroke scale:

    7 px.

Do not manufacture a statistical significance level from these numbers.

They are scale references only.

## Interpretation categories

The audit does not assign a model replacement.

Interpret descriptively among these possibilities:

### BROAD_SYSTEMATIC

Residual error is substantial across most source segments and shows
cross-pass reproducible structure.

### LOCALIZED_SYSTEMATIC

A small subset of source regions accounts for a large part of the residual
and those local structures replicate across passes.

### PHASE_STRUCTURED

Residual pattern shows repeated morphology with printed winding phase.

### RADIAL_STRUCTURED

Residual varies systematically across rho / F(rho).

### WEAKLY_STRUCTURED

Large residual exists but cross-pass residual morphology is weak or unstable.

More than one descriptor may apply.

No numerical threshold for these labels is chosen after viewing the result.

The numerical report is primary; verbal descriptors are secondary.

## Interpretation boundary

This audit may establish that the failure of the frozen isotropic model is:

- reproducible;
- localized or distributed;
- radial;
- phase-related;
- source-order related.

It cannot establish what alternative map generated the drawing.

In particular it does not establish:

- anisotropy;
- a 2x2 construction;
- a projective 3x3 construction;
- a nonlinear coordinate chart;
- a different reciprocal-spiral equation;
- historical intent.

Any expanded model requires a separate preregistration after this residual
morphology result is frozen.

## Expected outputs

Primary JSON:

    data/derived/first_hand_arm_of_god/qc/
    first_hand_spherical_reciprocal_spiral_residual_morphology.json

Segment table:

    data/derived/first_hand_arm_of_god/qc/
    first_hand_spherical_reciprocal_spiral_residual_segments.csv

Binned morphology table:

    data/derived/first_hand_arm_of_god/qc/
    first_hand_spherical_reciprocal_spiral_residual_bins.csv

Cross-pass paired table:

    data/derived/first_hand_arm_of_god/qc/
    first_hand_spherical_reciprocal_spiral_residual_crosspass.csv

Diagnostic figure:

    data/derived/first_hand_arm_of_god/qc/
    first_hand_spherical_reciprocal_spiral_residual_morphology.png

Report:

    reports/
    first_hand_spherical_reciprocal_spiral_residual_morphology.md

First-run log:

    data/derived/first_hand_arm_of_god/qc/
    first_hand_spherical_reciprocal_spiral_residual_morphology_first_run.log

Seal:

    data/derived/first_hand_arm_of_god/qc/
    first_hand_spherical_reciprocal_spiral_residual_morphology.sha256

