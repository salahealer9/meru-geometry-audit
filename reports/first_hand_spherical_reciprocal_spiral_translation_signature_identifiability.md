# First Hand reciprocal-spiral translation-signature identifiability synthesis

**Checkpoint:** v0.8
**Status:** synthesis after frozen first-order translation-signature result
**Primary outcome:** `REPRODUCIBLE_PARTIAL_TRANSLATION_SIGNATURE`
**Radial-law outcome:** `RADIAL_AMPLITUDE_LAW_NOT_IDENTIFIABLE_FROM_THIS_TRAJECTORY`

## Translation-signature replication

The primary first-order coefficient directions are:

    Pass 1 = 306.727638909 deg
    Pass 2 = 308.203020909 deg

with cross-pass directional separation:

    1.475382000 deg.

Sensitivity calculations remain in the same broad directional sector:

Equal-segment:

    Pass 1 = 309.307753998 deg
    Pass 2 = 311.320419426 deg

S04 excluded:

    Pass 1 = 307.389853870 deg
    Pass 2 = 309.991239833 deg

The orientation of the first-order translation component is therefore
substantially more stable than its magnitude.

## Magnitude sensitivity

Recovered coefficient magnitudes across the frozen primary and sensitivity
calculations span approximately:

    0.182 -- 0.287.

The magnitude should therefore not be promoted to a single calibrated
translation estimate.

The robust first-order finding is primarily directional.

## Explained residual

The primary translation-signature subspace explains:

    Pass 1 = 0.264823719816
    Pass 2 = 0.331608239708

of the frozen parent weighted angular SSE.

Remaining angular RMS is:

    Pass 1 = 35.380220530 deg
    Pass 2 = 32.251409076 deg.

Translation is therefore a substantial but incomplete component of the
centered-model failure.

The majority of the parent squared residual remains unexplained.

## Radial amplitude identifiability

The preregistered radial-band harmonic test is not identifiable on this
source trajectory.

Only one fixed radial band satisfies the preregistered phase-coverage and
conditioning requirements in each pass.

As radius increases, accessible phase coverage within a fixed narrow radial
band collapses because radius and phase are coupled along the spiral
trajectory.

Increasing the number of samples along the same curve would not create the
missing independent phase coverage.

Therefore:

    RADIAL_AMPLITUDE_LAW_NOT_IDENTIFIABLE_FROM_THIS_TRAJECTORY

is the correct outcome.

No neighboring radial bands are merged post hoc.

## Single eligible-band constraint

The one eligible radial band gives approximately:

    Pass 1 amplitude / F_bar = 0.243
    Pass 2 amplitude / F_bar = 0.235.

The values replicate at approximately the few-percent level.

This is retained as a local reproducible constraint.

It cannot establish or reject constancy of amplitude/F_bar with radius
because only one radial band is eligible.

## Identifiability clarification

The failure of the radial-band amplitude test does not imply that a
one-dimensional curve can identify only one model parameter.

A parametric curve can identify multiple parameters when their induced
basis functions are linearly independent along the observed trajectory.

The specific limitation here is that conditioning on a narrow radial range
leaves insufficient independent phase variation.

Thus the single spiral does not independently span the two coordinates:

    radius
    phase

required by the proposed conditional radial-amplitude test.

This is a rank/coverage limitation, not a general dimensional prohibition
on multiparameter inference from curves.

## S04

S04 remains unusual in its within-segment cross-pass Pearson correlation.

However, removing S04 produces only small changes in the recovered
translation-signature direction and explained fraction.

Therefore:

    S04_DOES_NOT_DRIVE_TRANSLATION_SIGNATURE.

S04 remains in all primary calculations.

## Coordinate-framework relation

The recovered translation-signature direction lies several degrees from
previously frozen directions in the page-7 coordinate framework.

This proximity is post-hoc contextual information only.

It is not treated as a calibrated directional identity or as confirmatory
evidence.

## Experimental sequencing

The already-preregistered translated-isotropic reciprocal-spiral model
remains a spiral-only model test.

The labelled coordinate curves:

    Y0
    Y1
    YAXIS
    X1

must not enter its parameter fit.

This preserves the coordinate framework as an independent later prediction.

Preferred sequence:

    frozen spiral observations
        ->
    translated-isotropic spiral-only fit
        ->
    freeze translated result
        ->
    zero-refit coordinate-curve prediction
        ->
    only later consider a joint spiral + coordinate synthesis model.

A joint fit introduced before the zero-refit prediction would sacrifice
the strongest available independent test of the translated construction.

## Decision

The first-order result is sufficiently reproducible to justify activation
of the already-preregistered full translated-isotropic spiral-only model.

The first-order coefficient values must not be used as optimizer starting
points, preferred directions, narrowed bounds, priors, or tuning information.

The deterministic optimizer and corrected normalized objective specified
before this result was exposed remain controlling.

