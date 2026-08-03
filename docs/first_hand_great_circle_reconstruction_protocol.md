# First Hand limb-constrained great-circle reconstruction protocol

**Version:** v0.8.0
**Status:** preregistered before numerical great-circle reconstruction
**Parent repository checkpoint:** 05ebae0
**Primary source:** AOG_PDF_2005A
**Source page:** 7

## Purpose

This checkpoint bridges the completed model-neutral image-space morphology
census to the later planar-to-sphere projective calibration.

It asks one narrower question:

> Are the four source-labelled page-7 curves compatible, at the precision
> of the hand drawing, with projected great circles on the already-frozen
> spherical limb?

This stage does not fit a flat-to-sphere projective map and does not select
a spherical scale.

## Frozen dependencies

The following results predate this protocol and are not altered here:

- source-level spherical-map family audit;
- two-pass curve observations;
- acquisition-QC diagnosis and derivative;
- acquisition-QC sensitivity result;
- neutral line/circle/ellipse morphology census;
- frozen equal-pass outer-limb geometry.

The raw acquisition record remains immutable.

## Reconstruction set

The only curves used for great-circle reconstruction are the four
source-labelled traces:

- `AOG-LM-P07-GC-Y0`
- `AOG-LM-P07-GC-Y1`
- `AOG-LM-P07-GC-YAXIS`
- `AOG-LM-P07-GC-X1`

The unlabelled scaffold curve

`AOG-LM-P07-GC-SCAFFOLD-UR-UC-X1LL-LL`

is excluded from fitting.

Its unknown planar preimage prevents it from serving as a genuine
projective-map prediction at this stage.

## Frozen sphere normalization

Let the already-frozen outer-limb circle have image centre

    (cx, cy)

and radius

    R.

Prepared-crop pixels are transformed to Cartesian normalized sphere-image
coordinates by

    u = (x_px - cx) / R
    v = -(y_px - cy) / R

so that the frozen limb is the unit circle

    u^2 + v^2 = 1.

The limb centre and radius are never refitted from the labelled curves.

## Rendering hypothesis

The primary reconstruction hypothesis is an orthographic rendering of a
unit sphere.

This is a reconstruction model, not a claim that the source explicitly
specified an orthographic camera.

Failure of this hypothesis therefore has at least two possible
interpretations:

1. the source strokes are not compatible with a common great-circle
   scaffold at drawing precision; or
2. the page uses a different or schematic sphere rendering.

These possibilities must not be conflated.

## Projected great-circle family

A spherical great circle is the intersection of the unit sphere with a
plane through its centre.

Under orthographic rendering, every such great circle projects to a
centred ellipse whose:

- centre is the frozen sphere-image centre;
- semi-major axis equals the frozen limb radius R;
- semi-minor axis is q R, where 0 <= q <= 1;
- orientation is described by an unoriented angle phi.

In normalized coordinates define

    e_major = (cos(phi), sin(phi))
    e_minor = (-sin(phi), cos(phi)).

The projected great-circle locus is

    C(phi, q; t)
      = e_major cos(t)
        + q e_minor sin(t),

for

    0 <= t < 2*pi.

The limit

    q = 0

is a diameter line through the sphere-image centre.

Thus straight and curved labelled traces belong to one continuous model
family and are not assigned different models in advance.

## Relation to a spherical plane

For 0 <= q <= 1, a compatible unit plane normal may be represented as

    n_+ =
      sqrt(1-q^2) e_minor_x,
      sqrt(1-q^2) e_minor_y,
      +q

or

    n_- =
      sqrt(1-q^2) e_minor_x,
      sqrt(1-q^2) e_minor_y,
      -q.

The two signs are an unavoidable front/back tilt ambiguity of the
orthographic image.

No sign branch is silently selected.

Both branches are retained for the subsequent projective calibration.

The usual n <-> -n plane-normal equivalence is also respected.

## Primary residual

For every resampled observed point, the residual is the Euclidean
image-space distance to the nearest point on the complete projected
great-circle locus.

The primary residual is therefore

    d_i =
      R * min_t || p_i - C(phi, q; t) ||.

Algebraic conic residuals are not the primary fit statistic.

Hidden source strokes are not reconstructed and absence of observations
on part of the mathematical ellipse incurs no penalty.

## Weighting

The already-frozen curve acquisition rules remain in force:

- primary resampling spacing: 2 px;
- sensitivity spacings: 1 px and 4 px;
- pass 1 weight: 0.5;
- pass 2 weight: 0.5;
- within each pass: visible arc-length weighting;
- raw click count is not a statistical weight;
- local sigma is never below the existing 2 px curve floor.

Each source-labelled curve receives equal top-level weight when aggregate
diagnostics are reported.

No longer visible curve is allowed to dominate merely because it contains
more sampled arc length.

## Fits to compute

For every labelled curve compute:

1. pass-1 fit;
2. QC pass-2 fit;
3. equal-pass combined fit.

For each fit report:

- phi;
- q;
- projected semi-minor axis q R;
- great-circle plane-normal branches;
- RMS image residual;
- median image residual;
- P95 image residual;
- maximum image residual;
- sigma-normalized residual summary;
- limb-normalized residual summary.

Repeat the equal-pass combined fit at 1 px and 4 px resampling.

## Deterministic optimization

The fit is bounded by

    0 <= phi < pi
    0 <= q <= 1.

A deterministic multi-start search is required.

Initial phi values are

    0, 15, 30, ..., 165 degrees.

Initial q values are

    0.00
    0.10
    0.25
    0.50
    0.75
    0.95.

The globally lowest objective among converged starts is retained.

Optimizer success, objective value, starting seed, iteration count, and
termination status are recorded.

The exact q=0 diameter-line boundary must remain representable and may
not be replaced by an arbitrary positive lower bound.

## Relation to the previous neutral morphology census

The previously frozen free line, free circle, and free ellipse fits are
not recomputed.

For each labelled curve report the frozen descriptive residuals beside
the new limb-constrained projected-great-circle residual.

This comparison asks whether imposing the spherical constraints

- fixed centre;
- fixed major radius R;
- great-circle ellipse form

materially degrades the description.

No AIC, BIC, p-value, or formal probabilistic model-selection claim is
made because traced points from a hand drawing are spatially correlated
and drawing error is not an iid statistical sample.

## Compatibility language

A projected-great-circle RMS at or below the already-adopted 2 px curve
uncertainty floor may be described as

    compatible with the projected-great-circle model at the adopted
    image-space uncertainty scale.

It must not be described as certification that the hand-drawn stroke is
an exact mathematical great circle.

Residuals above the floor are reported quantitatively without replacing
the threshold after seeing the result.

## Frozen point-incidence diagnostics

No point landmark is used to fit phi or q.

Only after all four curve fits are frozen may the following independent
image-space incidence diagnostics be evaluated.

### Explicit source incidence

`GC-Y0` and `GC-Y1` visibly meet at the already-frozen lower-right shared
rim node:

    AOG-LM-P07-RIM-NODE-LR-SHARED

Report the predicted curve-intersection distance to that node.

### Candidate origin incidence

The intersection of

    GC-Y0
    GC-YAXIS

is compared with

    AOG-LM-P07-CENTRAL-REFERENCE-NODE.

The central node remains a candidate chart origin; agreement is a
diagnostic and not an assumption used in fitting.

### Candidate unit-grid incidence

The intersection of

    GC-X1
    GC-Y1

is compared with

    AOG-LM-P07-UPPER-INTERIOR-CROSSING.

Because the crossing was originally digitized neutrally, this remains a
candidate correspondence rather than an assumed identity.

### Second projective-infinity direction

The intersection of

    GC-YAXIS
    GC-X1

is compared with all six already-frozen neutral rim nodes.

Report the nearest rim node and every node distance.

No particular rim node is assigned in advance and no multiple-comparison
PASS is issued from this nearest-node diagnostic.

## Plane-angle outputs

After each individual great-circle fit is frozen, enumerate all allowed
front/back normal branches.

For every branch combination report the unoriented plane angles

    delta_x =
      angle(GC-YAXIS, GC-X1)

and

    delta_y =
      angle(GC-Y0, GC-Y1).

Do not select a branch or spherical scale in this checkpoint.

These angles become inputs to the later projective calibration.

Under the isotropic inverse-gnomonic hypothesis, the later prediction is

    delta_x = delta_y = atan(k),

but that equality is not imposed during the present reconstruction.

## Holdout boundary

The unlabelled scaffold curve remains outside:

- great-circle parameter fitting;
- branch selection;
- scale calibration;
- projective-gauge selection.

Its neutral morphology result remains preserved, but no projective
prediction is claimed until a planar preimage can be assigned from
independent source or construction evidence.

## Outputs

The eventual implementation will produce separate files:

    data/derived/first_hand_arm_of_god/qc/
        first_hand_great_circle_reconstruction.json

    reports/
        first_hand_great_circle_reconstruction.md

and a first-run log and SHA-256 seal.

No existing result file may be overwritten.

## Forbidden outputs at this checkpoint

This reconstruction computes no:

- unique flat-to-sphere map;
- isotropic-scale selection;
- anisotropic/projective-gauge selection;
- G30/GHALF/GUNIT/GONE verdict;
- reciprocal-spiral projection;
- scaffold prediction;
- S1 score;
- S1.5 score;
- S2 score.

## Next checkpoint

Only after this great-circle reconstruction is frozen will the recovered
plane families be used to compare nested source-constrained maps:

1. isotropic inverse gnomonic;
2. axis-anisotropic inverse gnomonic;
3. equator-preserving linear central-projective gauge.

The fixed source scale candidates G30, GHALF, GUNIT, and GONE will then
be evaluated against the recovered plane-angle geometry without using
the scaffold holdout to tune the result.
