# First Hand page-7 digitization phase closeout

**Checkpoint:** v0.8

**Phase status:** `DIGITIZATION_PHASE_COMPLETE`

**Transition:** analytic construction and self-embedment testing

## Purpose of this closeout

The page-7 source has now been subjected to:

- neutral landmark acquisition;
- two-pass great-circle acquisition;
- acquisition QC;
- curve morphology analysis;
- rendering-model reconstruction;
- coordinate-family consistency tests;
- two-pass spherical-spiral acquisition;
- spherical-spiral reproducibility analysis;
- centered reciprocal-spiral reconstruction;
- residual-morphology analysis;
- first-order translation-signature analysis;
- full translated-isotropic reciprocal-spiral reconstruction.

The purpose of the digitization phase was to determine how much of the
printed drawing can be treated as quantitative geometric evidence and to
recover enough source semantics to define the subsequent analytic tests.

That purpose has now been fulfilled.

## Coordinate-curve result retained

The labelled coordinate framework remains quantitatively informative.

In particular, under the tested equator-preserving central-projective
construction family, the X1 relation cannot be reconciled with the
YAXIS-derived direction merely by changing the positive X scale.

The frozen global minimum residual is approximately:

    20.715146971 degrees.

This result remains limited to the explicitly tested construction family.

It is not promoted to a statement about every possible interpretation of the
page-7 coordinate system.

## Spiral acquisition result retained

The visible thick spherical spiral was independently digitized twice.

The two acquisitions reproduce the same printed centerline very closely.

This establishes that subsequent spiral reconstruction failures are not
primarily consequences of inconsistent manual tracing.

It does not establish that the hand-drawn spiral is itself a metric rendering
of the source's exact analytic reciprocal spiral.

## Centered reciprocal reconstruction

The centered isotropic reciprocal-spiral reconstruction produced large,
systematic, strongly cross-pass-reproducible residuals.

The printed spiral therefore does not provide a high-accuracy realization of
that tested metric reconstruction.

## Translated reciprocal reconstruction

A full translated-isotropic reciprocal-spiral model produced a finite and
highly reproducible numerical optimum.

However:

1. its physical page-space residual did not improve over the centered model;
2. its page-space discrepancy remained large;
3. the post-fit intrinsic angular span of the clean visible trace was
   approximately 579 degrees rather than the source-stated 540-degree span;
4. the inferred nonlinear translation direction differed substantially from
   the earlier first-order translation-like residual direction.

Thus the translated-isotropic reconstruction is not adopted as a calibrated
metric model of the printed spiral.

## Interpretation of the hand drawing

The digitization results do not falsify the analytic source statement:

    r * theta = 1

or the stated angular truncation:

    Delta theta = 3*pi.

Instead they show that the thick page-7 spiral should not be treated as a
sufficiently precise metric surrogate from which those analytic quantities
can be reconstructed.

Accordingly:

    PAGE7_SPIRAL_TREATED_AS_ILLUSTRATIVE_FOR_ANALYTIC_TESTING

is the operational conclusion of the digitization phase.

This does not imply that every element of the page-7 drawing is merely
illustrative.

The more geometrically stable labelled framework and its source semantics
remain independent evidence.

## Source truncation branches retained

Two source-supported reciprocal-spiral parameter conventions remain active.

### Prose branch

    theta_outer -> 0+
    theta_inner = 3*pi

### Diagram branch

    theta_outer = 1
    theta_inner = 1 + 3*pi

Both satisfy exactly:

    Delta theta = 3*pi.

Therefore the source ambiguity changes the placement of the truncated branch
along the reciprocal spiral but not its stated 1.5-turn angular span.

Neither branch is selected by reference to the hand-drawn spiral.

## Reason for analytic pivot

The primary remaining claims are mathematical construction claims.

In particular, whether the exact reciprocal spiral:

    r(theta) = 1/theta

with a source-supported 3*pi truncation admits the claimed spherical or
self-embedded construction is a property of the exact mathematical model.

Further refinement of the hand-drawn spiral cannot settle that question.

The next phase therefore computes directly from the source-stated analytic
construction rather than attempting additional pixel-level reconstruction.

## Digitization outputs remain part of the audit

The analytic pivot does not discard the digitization phase.

The frozen digitization results retain independent value for:

- source-semantic identification;
- coordinate-curve consistency;
- distinguishing precise versus illustrative source features;
- documenting limitations of metric reconstruction from page 7;
- defining later zero-refit comparisons where appropriate.

No digitization result is rewritten or removed.

## Analytic phase

The analytic phase will begin from the exact reciprocal spiral:

    x(theta) = cos(theta)/theta
    y(theta) = sin(theta)/theta
    r(theta) = 1/theta.

The two source-supported 3*pi truncation branches will be tested separately.

The initial analytic target is the smooth spherical construction.

Self-embedment will be evaluated hierarchically:

    S1   directed tangent compatibility
    S1.5 local Darboux-frame compatibility
    S2   collision-free recursive nesting.

Comparator spiral families will subsequently be passed through the same
pipeline so that any successful self-embedment property can be tested for
specificity to the reciprocal spiral.

The dimpled-sphere / toroidal construction remains a separate analytic
variant and will not inherit the spherical map without an explicit
source-derived construction rule.

## Final digitization-phase conclusion

The page-7 investigation has reached its useful metric limit.

The appropriate next question is no longer:

    "Can the hand-drawn spiral be fitted more accurately?"

It is:

    "Does the exact source-stated construction possess the claimed
    geometric and self-embedding properties?"

That question will be answered computationally from the analytic model.

