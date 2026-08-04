# First Hand translated-isotropic reciprocal-spiral interpretation

**Checkpoint:** v0.8
**Status:** interpretation of frozen translated-isotropic spiral-only result

**Optimization outcome:** `FINITE_STABLE_TRANSLATION_OPTIMUM`

**Geometric outcome:** `TRANSLATED_ISOTROPIC_RECIPROCAL_SHAPE_NOT_SUPPORTED`

## Scope

The full translated-isotropic reciprocal-spiral model was fitted using only
the independently frozen spherical spiral traces.

The fit did not use:

- first-order translation-signature coefficients;
- coordinate curves;
- scaffold geometry;
- endpoint landmarks;
- the source 3*pi span.

The only nonlinear optimization variables were the two coordinates of the
translated construction origin.

For every candidate translation, the reciprocal-spiral scale and phase were
profiled analytically.

## Important parameter interpretation

The fitted quantity:

    k = |m|

is a multiplicative construction-plane scale.

It is NOT a reciprocal-spiral exponent.

The tested source curve remains:

    r proportional to 1/theta

throughout the translated-isotropic model.

Therefore the fitted values:

    Pass 1 k = 1.967848571007
    Pass 2 k = 1.983056988422

must not be interpreted as evidence for:

    r proportional to theta^-2.

No exponent was fitted in this checkpoint.

## Finite translation optimum

Primary length-weighted fits:

Pass 1:

    r_tau         = 0.024697224138
    phi_tau       = 234.825259944 deg
    t_x           = -0.028472125567
    t_y           = -0.040399612025
    |t|           = 0.049424594951
    J             = 0.028643967678
    weighted R^2  = 0.971356032322

Pass 2:

    r_tau         = 0.023116671758
    phi_tau       = 235.653553350 deg
    t_x           = -0.026098592688
    t_y           = -0.038192562694
    |t|           = 0.046258062924
    J             = 0.028743827698
    weighted R^2  = 0.971256172302

Both solutions are well inside the frozen primary search boundary.

## Expanded-bound stability

Increasing the radial search bound from:

    r_tau <= 0.98

to:

    r_tau <= 0.995

does not drive the solution toward infinity.

Primary/expanded construction-translation separations are:

    Pass 1 = 2.8410e-8
    Pass 2 = 1.3020e-8.

Neither expanded solution lies at its radial boundary.

The finite optimum is therefore numerically stable under the mandatory
expanded-bound sensitivity test.

The translation-at-infinity degeneracy identified before implementation
does not account for the recovered optimum.

## Cross-pass parameter replication

The independently fitted primary translations reproduce closely:

    construction translation separation = 0.003241099362
    tau-disk separation                 = 0.001617856351
    relative |t| difference             = 0.066188212100
    translation direction difference    = 0.828293406 deg
    relative k difference               = 0.007698699545
    alpha0 difference                   = 0.184278444 deg
    handedness agrees                   = True.

Thus the optimizer is recovering essentially the same finite parameter
region from the two independently acquired traces.

## Acquisition-level cross-prediction

Without refitting:

Pass-1 model evaluated on Pass 2:

    angular RMS = 27.685564465 deg
    page RMS    = 66.166327615 px
    page p95    = 145.169867514 px

Pass-2 model evaluated on Pass 1:

    angular RMS = 27.518512046 deg
    page RMS    = 66.833923540 px
    page p95    = 146.063096408 px.

This is excellent cross-pass acquisition replication.

Because the two passes digitize the same printed source curve, this should
not be described as independent physical-object generalization.

It establishes robustness to the independent acquisition pass.

## Angular improvement

Translated primary angular RMS:

    Pass 1 = 27.309138458 deg
    Pass 2 = 27.516910130 deg.

This is substantially below the approximately 39--41 degree RMS of the
frozen centered isotropic parent fits.

However, angular residual around a translated origin is not by itself an
adequate measure of printed-plane geometric reconstruction.

## Page-space geometric diagnostic

Translated-model page RMS:

    Pass 1 = 66.181120563 px
    Pass 2 = 66.711415834 px.

The frozen centered-model angular-chord RMS values were approximately:

    Pass 1 = 63.993468596 px
    Pass 2 = 64.256317126 px.

For the centered case t = 0, the translated-model page diagnostic reduces
to the same page-space chord metric:

    d_page =
        2 * R_limb * rho * |sin(delta_alpha/2)|.

The metrics are therefore directly comparable.

Translation does not reduce the physical page-space discrepancy.

Instead page RMS increases by approximately:

    Pass 1 = +2.188 px  (+3.42 percent)
    Pass 2 = +2.455 px  (+3.82 percent).

With the frozen limb radius:

    R_limb = 341.906449919406 px,

the translated page RMS is approximately:

    Pass 1 = 19.36 percent of R_limb
    Pass 2 = 19.51 percent of R_limb.

The translated p95 discrepancy is approximately:

    Pass 1 = 42.67 percent of R_limb
    Pass 2 = 42.51 percent of R_limb.

Thus the high weighted R^2 must not be interpreted as a high-accuracy
reconstruction of the printed curve.

The translated polar coordinate system explains a large fraction of angular
variance, but the actual page-space geometric discrepancy remains large and
does not improve over the centered model.

## Independent 3*pi span holdout

The source reciprocal-spiral branches retained for the audit both specify
an intrinsic angular span:

    3*pi = 540 degrees.

This value was excluded from all fitting.

Post-fit translated-origin spans are:

Pass 1:

    578.810767365 deg

with:

    +38.810767365 deg

relative to 540 degrees.

Pass 2:

    579.817898889 deg

with:

    +39.817898889 deg

relative to 540 degrees.

The discrepancy reproduces across passes to approximately one degree.

The clean acquired S10 trace was deliberately stopped before the obscured
lower-right endpoint region.

Therefore the fact that the already-visible clean trace exceeds the complete
source 3*pi span makes this a particularly strong incompatibility under the
tested translated-isotropic interpretation.

The independent source-span holdout fails.

## Weighting sensitivity

Equal-segment fits remain finite and broadly nearby:

Pass 1:

    r_tau   = 0.020430291973
    phi_tau = 239.352637562 deg
    |t|     = 0.040877646145
    J       = 0.015181932016

Pass 2:

    r_tau   = 0.018468406556
    phi_tau = 240.207577902 deg
    |t|     = 0.036949415895
    J       = 0.015139332200.

The objective value changes substantially with weighting while the inferred
origin remains in a similar region.

Because J uses the variance structure under the chosen weighting, values
from different weighting schemes should be reported separately rather than
treated as a single calibrated goodness-of-fit number.

## Relation to the first-order translation signature

The earlier first-order residual projection recovered directions near:

    307--311 degrees

depending on pass and weighting.

The full nonlinear translated model independently recovers directions near:

    235--240 degrees.

The primary first-order and nonlinear directions differ by approximately:

    72 degrees.

Under the frozen first-order derivation, the coefficient vector represented
the local translation direction after projection against the centered parent
design.

Accordingly, this directional disagreement is relevant.

In hindsight, the first-order result is best interpreted as a reproducible
translation-like component in the centered residual field rather than as a
successful estimate of the finite translation subsequently selected by the
full nonlinear model.

The nonlinear model was not initialized or constrained using the first-order
result, so this disagreement was not suppressed by the fitting procedure.

## Overall interpretation

The translated-isotropic model possesses a finite, highly stable, and
cross-pass reproducible numerical optimum.

That numerical stability is real.

However, the model fails the more important geometric checks:

1. physical page-space reconstruction does not improve over the centered
   isotropic model;
2. page-space residual remains very large relative to the frozen limb;
3. the independent 3*pi source-span holdout fails by approximately
   39--40 degrees;
4. the nonlinear translation direction is inconsistent with the earlier
   first-order translation-like direction.

Therefore:

    FINITE_STABLE_TRANSLATION_OPTIMUM

does not imply:

    SOURCE_CONSISTENT_TRANSLATED_RECIPROCAL_SPIRAL.

The scientific outcome of this checkpoint is:

    TRANSLATED_ISOTROPIC_RECIPROCAL_SHAPE_NOT_SUPPORTED.

## Consequence for model sequencing

The labelled coordinate curves should not now be used to rescue or refit the
translated-isotropic spiral model.

The intended zero-refit coordinate prediction was conditional on the
spiral-derived translated model surviving its own geometric tests.

It does not.

Any future model combining the spiral and coordinate curves must therefore
be preregistered as a new synthesis model rather than presented as validation
of this translated-isotropic construction.

No further map flexibility is justified solely by the desire to reduce the
present residual.

