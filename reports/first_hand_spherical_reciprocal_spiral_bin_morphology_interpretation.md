# First Hand reciprocal-spiral binned residual morphology interpretation

**Checkpoint:** v0.8  
**Status:** interpretation of frozen binned residual morphology  
**Descriptors:** `PHASE_STRUCTURED`, `RADIAL_STRUCTURED`

## Phase morphology

The already-frozen 10-degree phase bins show a smooth, strongly reproducible
one-cycle residual pattern.

Both passes are strongly negative near phase 0 degrees.

The residual rises through zero near approximately:

    100--110 degrees

and reaches a broad positive maximum around:

    200--250 degrees

before returning through zero near approximately:

    310--320 degrees

and becoming strongly negative again toward 360 degrees.

The pattern is reproduced independently in Pass 1 and Pass 2.

This is not consistent with a single localized tracing defect.

It is a phase-structured systematic residual.

## Radial morphology

The frozen rho bins also show strong reproducible structure.

The residual changes sign and amplitude systematically with normalized
page radius.

Both acquisitions recover the same broad radial morphology.

Because rho, source order, and reciprocal-spiral progression are related,
this radial morphology is not treated as statistically independent from
the phase morphology.

Descriptor:

    RADIAL_STRUCTURED

## Source-order morphology

The fixed source-order bins show repeated alternating residual lobes across
the visible spiral.

The pattern is reproduced across the two independent acquisitions.

This supports a distributed geometric mismatch rather than a single
problematic crossing, node, or digitization region.

## Segment replication caveat

Most source segments show strong to extremely strong pointwise cross-pass
residual replication.

S04 has weak/negative within-segment correlation, but S04 contributes only
a small fraction of the total parent-model error.

Its local behavior therefore does not explain the global systematic
residual.

## Combined descriptor

The frozen result is described as:

    REPRODUCIBLE_SYSTEMATIC_RESIDUAL
    PHASE_STRUCTURED
    RADIAL_STRUCTURED

No alternative map is established by these descriptors.

## Minimal next family

The phase morphology motivates testing displacement of the construction
chart origin relative to the fixed stereographic rendering pole.

For an isotropic reciprocal spiral subjected to a planar translation,

    q(theta) =
        t + k * R(alpha0) *
        [cos(theta)/theta, sin(theta)/theta]

the apparent page azimuth about the original rendering pole acquires a
once-per-turn phase distortion whose amplitude depends on radius.

This qualitatively matches the two principal features of the frozen
residual morphology:

1. a strong one-cycle phase pattern;
2. radial modulation.

This is a model-selection motivation, not evidence that translation is
the true transformation.

## Centered 2x2 comparison

A centered invertible 2x2 transformation remains less strongly motivated
as the next test because it preserves the antipodal directional relation

    beta(theta + pi) = beta(theta) +/- pi

and therefore cannot by itself change the intrinsic directional winding of
a complete 3*pi interval away from 3*pi.

A displaced origin can change the apparent winding measured about the
fixed rendering pole while retaining a 3*pi intrinsic reciprocal-spiral
winding about the translated construction origin.

## Next test

Preregister the minimal translated-isotropic construction:

    q(theta) =
        t + k * R(alpha0) *
        [cos(theta)/theta, sin(theta)/theta]

with only two genuinely new parameters:

    t_x
    t_y

relative to the previous centered model.

The fitted translation must be obtained from the spiral alone.

Coordinate curves, scaffold geometry, source endpoint landmarks, and the
3*pi endpoint-span condition remain excluded from fitting.

The intrinsic 3*pi span becomes a post-fit prediction.

