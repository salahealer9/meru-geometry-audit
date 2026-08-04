# First Hand spherical reciprocal-spiral shape protocol

**Checkpoint:** v0.8  
**Status:** protocol frozen before reciprocal-spiral shape calculation  
**Analysis class:** spiral-led source-shape diagnostic

## Primary question

Does the independently acquired page-7 spherical spiral have the radial-
angular structure required for a stereographically rendered isotropic
central-projective image of the unitary reciprocal spiral

    r * theta = 1

without using any labelled coordinate curve to calibrate the construction?

This is a spiral-led test.

The printed coordinate curves Y0, Y1, YAXIS, and X1 are not used.

The spherical scaffold is not used.

## Frozen planar source object

The already-audited planar curve is

    r(theta) = 1 / theta

with

    theta > 0

and Cartesian parameterization

    x(theta) = cos(theta) / theta
    y(theta) = sin(theta) / theta

The frozen traversal convention for source endpoint tests is inner-to-outer,
corresponding to decreasing theta.

## Source truncation ambiguity

Two source interpretations remain frozen:

### AOG_PROSE

    theta_outer -> 0+
    theta_inner = 3*pi

### AOG_DIAGRAM

    theta_outer = 1
    theta_inner = 1 + 3*pi

Both have angular span:

    3*pi

Neither truncation convention is used in the primary shape fit.

The primary shape test is therefore branch-independent.

No endpoint theta value is imposed.

## Frozen observational inputs

Use independently sealed continuous spherical-spiral acquisitions:

    spherical_spiral_segments_pass1.csv
    spherical_spiral_segments_pass2.csv

Metadata QC:

    QC_NONE_REQUIRED

Frozen correspondence:

    10 ONE_TO_ONE source runs

Frozen two-pass reproducibility:

    RMS_equal  = 0.887258846871 px
    RMS_length = 0.956050554591 px

The reproducibility result is descriptive context only and is not used to
fit the theoretical spiral.

## Frozen image frame

Use the already-frozen neutral spherical-limb reference:

    center_x_px = 1255.1268387556074
    center_y_px = 694.602781503521
    radius_px   = 341.906449919406

No sphere centre or radius is refitted from the spiral.

## Image coordinates

For every acquired source point (x_px, y_px), define mathematical page
coordinates

    u = (x_px - center_x_px) / radius_px
    v = (center_y_px - y_px) / radius_px

so that page y is converted to mathematical y-up convention.

Define

    rho = sqrt(u^2 + v^2)

and principal page azimuth

    alpha = atan2(v, u).

Any overall rigid orientation or reflection of the construction relative to
the printed page is absorbed by the fitted angular intercept and handedness.

## Construction family under test

Test only the already-defined isotropic central-projective family

    M_k(x,y) = normalize(k*x, k*y, 1)

with

    k > 0.

Under stereographic rendering to the normalized equator-at-unit-radius page
disk, the radial coordinate satisfies

    rho =
        (k*r) /
        (sqrt(1 + k^2*r^2) + 1).

Therefore

    k*r =
        2*rho / (1 - rho^2).

For the reciprocal spiral

    r = 1/theta,

so

    theta =
        k * (1 - rho^2) / (2*rho).

Define

    F(rho) =
        (1 - rho^2) / (2*rho).

The model therefore requires

    theta = k * F(rho).

Because the polar angle of the planar reciprocal spiral is theta, the
printed page azimuth must obey

    alpha_unwrapped =
        alpha0 + s*k*F(rho)

where

    alpha0 = arbitrary page-frame angular intercept
    s      = handedness, +1 or -1
    k      = positive construction scale.

Equivalently this is the linear relation

    alpha_unwrapped =
        a + m*F(rho)

with

    alpha0 = a modulo 2*pi
    s      = sign(m)
    k      = abs(m).

## Critical independence property

The slope and intercept are determined from the spherical spiral alone.

Do not use:

- Y0;
- Y1;
- YAXIS;
- X1;
- the scaffold;
- any earlier coordinate-derived k value;
- G30;
- GHALF;
- GUNIT;
- GONE;
- the prior 2x2 reconstruction;
- the X1 reconciliation result

to determine or choose the spiral-derived scale.

Any comparison with coordinate-derived scales occurs only after the primary
spiral result is frozen.

## Segment ordering

Use the already-frozen source topology:

    S01, S02, ..., S10

in inner-to-outer order.

No segment reordering is permitted.

## Arclength resampling

Raw click density is not statistical weight.

Resample each visible segment independently to

    N_RESAMPLE = 401

points at uniform image-plane polyline arclength.

Do not interpolate across segment gaps or occlusions.

## Azimuth unwrapping

Within each pass:

1. concatenate the resampled segments in frozen order S01 -> S10;
2. compute principal alpha = atan2(v,u);
3. apply deterministic 2*pi phase unwrapping in that frozen source order
   using the standard nearest-phase rule with discontinuity pi.

No theoretical spiral is used to choose phase wraps.

No integer winding offset is manually altered after viewing the fit.

A global addition of an integer multiple of 2*pi changes only alpha0 and
does not affect slope or residuals.

Report the maximum principal angular jump across each frozen inter-segment
gap as a topology diagnostic.

## Radial-domain audit

For every resampled point report whether:

    0 < rho < 1.

The tested finite central-projective construction maps finite positive
radius to the open unit disk and approaches rho = 1 only asymptotically.

Therefore report:

    rho_min
    rho_max
    count(rho <= 0)
    count(rho >= 1)

Do not clip any point to the unit circle.

Do not delete a point because it violates the model domain.

Any domain violation remains part of the reported source/model comparison.

## Primary fit

Fit Pass 1 and Pass 2 independently.

For each pass, perform analytic weighted linear least squares:

    alpha_unwrapped = a + m*F(rho).

No numerical optimizer is used.

### Primary weighting: visible-curve length

Each segment is uniformly represented by 401 resampled points.

For segment s with measured polyline length L_s, assign every sample in that
segment weight proportional to

    L_s / N_RESAMPLE.

Thus total segment weight is proportional to source-visible printed length.

This is the primary fit.

### Secondary weighting: equal segment

Repeat the analytic fit with every one of the ten segments assigned equal
total weight.

This is a mandatory sensitivity result.

It is not selected according to fit quality.

## Primary fitted quantities

For each pass and each fixed weighting report:

    intercept a
    alpha0 = a modulo 2*pi
    signed slope m
    handedness s = sign(m)
    spiral-derived scale k = abs(m)

and residuals in unwrapped azimuth:

    median absolute residual
    mean absolute residual
    RMS residual
    p95 absolute residual
    maximum absolute residual

in both radians and degrees.

Also report weighted R^2 as a descriptive linearity statistic.

R^2 is not by itself a proof criterion.

## Image-space angular discrepancy

For every resampled observation define the fitted angular residual

    delta_alpha =
        alpha_unwrapped
        - (a + m*F(rho)).

At fixed observed rho, report the corresponding chord discrepancy

    d_angular_px =
        2 * radius_px * rho
        * abs(sin(delta_alpha / 2)).

This is a radial-circle angular discrepancy, not a nearest-curve distance.

Report weighted:

    median
    RMS
    p95
    maximum

in pixels.

Do not call this quantity a full orthogonal geometric residual.

## Cross-pass replication

Pass 1 and Pass 2 are independent fits.

Report:

    |k_pass1 - k_pass2|

and relative scale difference

    2*|k1-k2| / (k1+k2).

Report whether fitted handedness agrees.

Compare angular intercepts using circular difference modulo 2*pi.

No pooled fit is primary.

A pooled descriptive fit may be introduced only in a later checkpoint after
the two independent results are frozen.

## Equal-segment sensitivity

For each pass report the difference between the primary length-weighted scale
and the secondary equal-segment scale.

Do not choose whichever weighting gives the smaller residual.

## No source-scale comparison yet

Before the primary spiral result is frozen, do not compare the fitted k to:

    tan(30 degrees)
    tan(0.5)
    1
    tan(1)
    k_y from the coordinate curves
    k_x from the coordinate curves
    any 2x2 singular value or effective scale.

Those are later independent comparisons.

## No endpoint-branch comparison yet

Do not use the fitted model in this checkpoint to decide between:

    AOG_PROSE
    AOG_DIAGRAM.

Do not force the visible S01 or S10 samples to any source theta value.

Do not use the lower-right shared node to fit k.

Do not use the prior inner endpoint landmark to fit k.

Source truncation branches become independent post-fit tests only after the
shape result is frozen.

## No coordinate prediction yet

Do not use the spiral-derived k or alpha0 to predict:

- Y0;
- Y1;
- YAXIS;
- X1;
- scaffold curves

until the spiral-only result is sealed and committed.

This protects the coordinate curves as genuine later predictions.

## No model expansion

This checkpoint does not fit:

- anisotropic kx/ky;
- a general 2x2 map;
- a general projective 3x3 map;
- nonlinear warps;
- arbitrary spherical rotations beyond the page angular intercept;
- splines;
- empirical radial correction terms.

If the isotropic construction fails, more flexible families require a new
protocol.

## Interpretation

Strong linearity of

    alpha_unwrapped

against

    F(rho)

in both independently acquired passes, with mutually consistent fitted k and
alpha0, would support compatibility of the printed spiral with the tested
isotropic central-projective + stereographic image of r*theta=1.

It would not prove that this was Tenen's historical construction.

Poor linearity would reject or strongly disfavor this specific construction
family for the observed spiral, regardless of the earlier coordinate-curve
results.

## Expected outputs

Primary result:

    data/derived/first_hand_arm_of_god/qc/
    first_hand_spherical_reciprocal_spiral_shape.json

Per-pass/per-segment diagnostics:

    data/derived/first_hand_arm_of_god/qc/
    first_hand_spherical_reciprocal_spiral_shape_segments.csv

Transformed resampled observations:

    data/derived/first_hand_arm_of_god/qc/
    first_hand_spherical_reciprocal_spiral_shape_samples.csv

Diagnostic figure:

    data/derived/first_hand_arm_of_god/qc/
    first_hand_spherical_reciprocal_spiral_shape.png

Report:

    reports/
    first_hand_spherical_reciprocal_spiral_shape.md

First-run log:

    data/derived/first_hand_arm_of_god/qc/
    first_hand_spherical_reciprocal_spiral_shape_first_run.log

Seal:

    data/derived/first_hand_arm_of_god/qc/
    first_hand_spherical_reciprocal_spiral_shape.sha256

