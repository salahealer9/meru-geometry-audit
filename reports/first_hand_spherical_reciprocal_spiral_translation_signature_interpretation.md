# First Hand reciprocal-spiral translation-signature interpretation

**Checkpoint:** v0.8
**Status:** interpretation of frozen first-order translation-signature result
**Outcome:** `REPRODUCIBLE_PARTIAL_TRANSLATION_SIGNATURE`

## Primary result

The preregistered first-order translation basis was tested against the
already-frozen residual field of the centered isotropic reciprocal-spiral
model.

No parent-model parameter was refitted.

No nonlinear translated-isotropic model was fitted.

The independent primary length-weighted results are:

Pass 1:

    c_x                         = 0.152681322402
    c_y                         = -0.204631623887
    |c|                         = 0.255314879522
    direction                   = 306.727638909 deg
    parent SSE explained        = 0.264823719816
    remaining angular RMS       = 35.380220530 deg
    remaining angular p95       = 52.745359562 deg

Pass 2:

    c_x                         = 0.174215465673
    c_y                         = -0.221364349518
    |c|                         = 0.281697006937
    direction                   = 308.203020909 deg
    parent SSE explained        = 0.331608239708
    remaining angular RMS       = 32.251409076 deg
    remaining angular p95       = 52.516952003 deg

## Cross-pass replication

Primary coefficient-vector separation:

    0.027270926523

Relative magnitude difference:

    0.098255282908

Direction difference:

    1.475382000 deg

The first-order translation-signature direction therefore replicates
closely between the two independent source acquisitions.

The coefficient magnitude also replicates at approximately the ten-percent
level.

## Amount of residual explained

The two-dimensional first-order translation subspace explains:

    Pass 1: 26.4824 percent
    Pass 2: 33.1608 percent

of the frozen parent weighted angular SSE.

This is a substantial and independently reproduced component of the
centered-model failure.

However, most of the parent squared residual remains unexplained.

Therefore the present result does not establish that translation alone is
the complete missing transformation.

## Weighting sensitivity

Equal-segment results are:

Pass 1:

    |c|                         = 0.181936120591
    direction                   = 309.307753998 deg
    parent SSE explained        = 0.213820929759

Pass 2:

    |c|                         = 0.214431396911
    direction                   = 311.320419426 deg
    parent SSE explained        = 0.305921900176

The coefficient magnitude depends moderately on weighting, but the inferred
direction remains broadly stable.

The primary qualitative conclusion therefore does not depend on the
length-weighting choice.

## S04 sensitivity

S04 was retained in the primary calculation.

The preregistered S04-excluded sensitivity gives:

Pass 1:

    |c|                         = 0.257079658970
    direction                   = 307.389853870 deg
    parent SSE explained        = 0.256129443984

Pass 2:

    |c|                         = 0.286560629944
    direction                   = 309.991239833 deg
    parent SSE explained        = 0.328293354523

These results remain close to the all-segment primary result.

S04 therefore does not drive the recovered first-order translation
signature.

## Radial amplitude test

For both independent passes:

    eligible radial bands = 1

and therefore:

    RADIAL_AMPLITUDE_TEST_NOT_IDENTIFIABLE

The fixed phase-coverage requirements prevent a meaningful test of
constancy of:

    harmonic amplitude / F(rho)

across radius.

No radial bands are merged post hoc.

No claim is made that the expected F(rho) amplitude law has been confirmed
or rejected.

This limitation arises because the observed object is a single spiral:
radius and phase are strongly coupled, so most narrow radial bands do not
contain enough independent phase coverage.

## Interpretation

The frozen result is classified as:

    REPRODUCIBLE_PARTIAL_TRANSLATION_SIGNATURE

The centered-model residual contains a substantial two-dimensional component
having the precise first-order vector form expected from displacement of the
construction origin.

The recovered vector orientation reproduces closely between independently
digitized passes.

This strengthens the displaced-origin hypothesis.

It does not confirm a finite translated-isotropic reciprocal-spiral model,
because:

1. approximately 67--74 percent of parent weighted squared residual remains;
2. the radial F(rho) amplitude prediction is not identifiable from the
   available source trajectory;
3. the first-order approximation need not remain accurate at the recovered
   displacement magnitude.

## Exploratory phase context

For a first-order translation vector with direction phi_t:

    e approximately |t| F(rho) sin(phi_t - beta).

Its positive phase maximum therefore occurs approximately at:

    beta_max = phi_t - 90 degrees.

The primary coefficient vectors imply:

    Pass 1 beta_max approximately 216.73 deg
    Pass 2 beta_max approximately 218.20 deg.

The previously inspected exploratory harmonic-1 phase was near 211 degrees.

This comparison is post hoc contextual information only.

It was not used to fit or select the translation-signature coefficients and
is not confirmatory evidence.

## Decision for the next checkpoint

The result is sufficiently reproducible and substantial to justify activating
the already-preregistered full translated-isotropic reciprocal-spiral test.

That test must use the corrected objective specified in:

    first_hand_spherical_reciprocal_spiral_translated_isotropic_objective_addendum.md

The first-order coefficients from this result must NOT be used as optimizer
initial conditions, bounds, priors, or preferred directions.

The nonlinear optimizer must use only the independently frozen deterministic
search specification.

This preserves the translated-isotropic test as a genuine model-level test
rather than a refinement initialized from the observed residual direction.

