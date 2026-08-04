# First Hand translated-isotropic reciprocal-spiral protocol

**Checkpoint:** v0.8  
**Status:** protocol frozen before translated-isotropic fitting  
**Analysis class:** minimal spiral-led model expansion

## Motivation

The frozen centered isotropic reciprocal-spiral model produced a large,
highly reproducible systematic residual.

Subsequent neutral residual morphology showed:

    REPRODUCIBLE_SYSTEMATIC_RESIDUAL
    PHASE_STRUCTURED
    RADIAL_STRUCTURED

The phase residual contains a strong approximately once-per-turn structure.

The minimal next model therefore permits displacement of the construction
chart origin relative to the already-frozen stereographic rendering pole.

No anisotropic, general projective, or nonlinear deformation is introduced.

## Frozen observational inputs

Use only the already-frozen transformed spherical-spiral samples from:

    first_hand_spherical_reciprocal_spiral_shape_samples.csv

The source traces are not redigitized.

The frozen spherical limb centre and radius are not refitted.

## Inverse stereographic construction-plane coordinates

For every frozen normalized page sample:

    (u, v)

with:

    rho^2 = u^2 + v^2

define

    Q_x = 2*u / (1-rho^2)
    Q_y = 2*v / (1-rho^2).

No point is clipped or moved.

All previously observed samples satisfy:

    0 < rho < 1.

## Model

Test:

    Q(theta) =
        t +
        k * R(alpha0) *
        [cos(s*theta)/theta,
         sin(s*theta)/theta]

where:

    t      = (t_x, t_y)
    k      > 0
    alpha0 = arbitrary construction orientation
    s      = +1 or -1.

Relative to the previous centered isotropic model, only:

    t_x
    t_y

are new continuous degrees of freedom.

## Exact translated radial-angular invariant

For a candidate translation:

    W = Q - t

define

    R_t = norm(W)

and source-order unwrapped angle:

    beta = unwrap(atan2(W_y, W_x)).

For a translated isotropic image of r*theta=1:

    R_t = k/theta

and therefore:

    beta =
        a + m*(1/R_t)

with:

    k = abs(m)
    s = sign(m).

Thus for every fixed candidate t, solve:

    beta = a + m/R_t

by analytic weighted linear least squares.

Do not numerically optimize a or m.

## Primary weighting

Use the already-frozen primary visible-curve-length weights:

    weight_length

from the parent transformed sample table.

## Secondary weighting

Repeat with the already-frozen equal-segment weights:

    weight_equal_segment.

Do not choose the weighting according to outcome.

## Translation fitting

The only nonlinear fitted quantity is:

    t = (t_x, t_y).

For every candidate t:

1. calculate W = Q-t;
2. reject candidates for which any sampled R_t is numerically zero;
3. unwrap beta using frozen source order;
4. analytically solve a and m;
5. compute the primary weighted angular SSE.

Minimize that frozen objective over t.

The optimizer must be deterministic.

The exact optimizer, parameter scaling, initial conditions, bounds, and
termination tolerances must be frozen in the implementation before the
real-data translated fit is run.

No result-dependent restarts are permitted.

## Independent-pass fits

Fit Pass 1 and Pass 2 independently.

Report for each:

    t_x
    t_y
    |t|
    direction(t)
    a
    alpha0 mod 2*pi
    signed m
    handedness
    k
    weighted R^2
    angular median/RMS/p95/max
    angular-chord median/RMS/p95/max.

## Cross-pass replication

Report:

    Euclidean separation between t_pass1 and t_pass2
    relative translation-magnitude difference
    circular translation-direction difference
    |k1-k2|
    relative k difference
    alpha0 circular difference
    handedness agreement.

## Cross-prediction

Without refitting:

1. evaluate the Pass-1 fitted translated model on Pass 2;
2. evaluate the Pass-2 fitted translated model on Pass 1.

Report angular and chord residual summaries.

No offset or phase correction is permitted during cross-prediction.

## Centered-model nesting

The translated model contains the previous centered model at:

    t = (0,0).

Report the frozen centered-parent primary residual alongside the translated
result.

Do not alter the parent result.

## Intrinsic angular-span holdout

The frozen source reciprocal spiral has two endpoint conventions, but both
have the same intrinsic angular span:

    3*pi = 540 degrees.

Do not use 3*pi in fitting t, a, m, or k.

After each translated fit is frozen, report the observed source-order angular
span around the fitted construction origin:

    Delta_beta =
        beta_last - beta_first.

Compare descriptively with:

    +/- 3*pi.

Report:

    absolute span
    absolute span minus 3*pi
    discrepancy in degrees.

This is an independent post-fit diagnostic.

## Endpoint landmarks

Do not use:

    AOG-LM-P07-SPHERE-INNER-END
    AOG-LM-P07-RIM-NODE-LR-SHARED

to fit the translated model.

Endpoint comparisons remain later holdouts.

## Coordinate curves

Do not use:

    Y0
    Y1
    YAXIS
    X1
    scaffold

to fit or choose the translated model.

If the translated spiral model survives its own tests, the labelled
coordinate curves become later predictions.

## No model expansion beyond translation

Forbidden in this checkpoint:

- k_x != k_y;
- general 2x2 linear transformation;
- shear;
- general affine matrix;
- general 3x3 projective transformation;
- nonlinear radial correction;
- polynomial warp;
- spline warp;
- Fourier residual correction;
- theta reparameterization;
- changing r*theta=1.

## Interpretation

A substantially improved fit is not sufficient by itself.

Support for the translated-isotropic model requires consideration of:

- residual reduction;
- Pass-1 / Pass-2 parameter replication;
- cross-prediction;
- weighting sensitivity;
- intrinsic 3*pi span holdout.

Failure of these checks would argue against translation as the missing
geometric component.

Success would motivate a subsequent zero-refit prediction of the labelled
coordinate framework.

## Expected outputs

Primary JSON:

    data/derived/first_hand_arm_of_god/qc/
    first_hand_spherical_reciprocal_spiral_translated_isotropic.json

Per-pass diagnostics:

    data/derived/first_hand_arm_of_god/qc/
    first_hand_spherical_reciprocal_spiral_translated_isotropic_segments.csv

Diagnostic figure:

    data/derived/first_hand_arm_of_god/qc/
    first_hand_spherical_reciprocal_spiral_translated_isotropic.png

Report:

    reports/
    first_hand_spherical_reciprocal_spiral_translated_isotropic.md

First-run log:

    data/derived/first_hand_arm_of_god/qc/
    first_hand_spherical_reciprocal_spiral_translated_isotropic_first_run.log

Seal:

    data/derived/first_hand_arm_of_god/qc/
    first_hand_spherical_reciprocal_spiral_translated_isotropic.sha256

