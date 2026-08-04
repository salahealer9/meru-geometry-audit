# First Hand spherical reciprocal-spiral shape interpretation

**Checkpoint:** v0.8
**Status:** interpretation of frozen primary spiral-only result
**Outcome:** `ISOTROPIC_RECIPROCAL_SHAPE_NOT_SUPPORTED`

## Primary result

The independently acquired spherical spiral was tested against the
radial-angular invariant required by a stereographically rendered
isotropic central-projective image of

    r * theta = 1

using

    alpha_unwrapped = a + m * F(rho)

with

    F(rho) = (1-rho^2)/(2*rho).

No coordinate curve, scaffold curve, endpoint theta convention, or
coordinate-derived construction scale was used.

## Cross-pass replication

Pass 1:

    k = 1.768957243729
    handedness = +1
    weighted R^2 = 0.935638314990
    angular RMS = 41.263379334 deg
    angular p95 = 64.815527425 deg
    angular chord RMS = 63.993468596 px
    angular chord p95 = 108.270972267 px

Pass 2:

    k = 1.806808782103
    handedness = +1
    weighted R^2 = 0.941790997491
    angular RMS = 39.448741257 deg
    angular p95 = 64.380505521 deg
    angular chord RMS = 64.256317126 px
    angular chord p95 = 109.187918627 px

Cross-pass scale replication:

    |k1-k2| = 0.037851538375

Relative scale difference:

    0.021171149399

Circular alpha0 difference:

    2.160429830 deg

The same broad fitted relation therefore replicates closely across the two
independent acquisitions.

## Weighting sensitivity

Changing from the preregistered length weighting to equal-segment weighting
changes the fitted scale only slightly.

Pass 1:

    k_length = 1.768957243729
    k_equal  = 1.776394199464

Pass 2:

    k_length = 1.806808782103
    k_equal  = 1.808358801843

The primary conclusion is therefore not driven by segment-length weighting.

## Geometric residual

Despite weighted R^2 values near 0.94, the absolute geometric discrepancies
are large.

The two primary fits have approximately 39--41 degree angular RMS residuals
and approximately 64 px angular-chord RMS discrepancies.

These discrepancies are far larger than:

    continuous-trace two-pass reproducibility ~ 1 px

and the frozen descriptive continuous-spiral source scale:

    7 px

Therefore the high R^2 describes a broad monotonic radial-angular trend;
it does not constitute close geometric agreement with the printed spiral.

## Angular-span diagnostic

Observed clean-trace angular spans are:

    Pass 1 = 594.396922 deg
    Pass 2 = 593.991527 deg

The two frozen source truncation interpretations each span:

    3*pi = 540 deg

Thus the observed clean trace contains approximately 54 degrees more
azimuthal evolution than the complete source interval.

Within the tested isotropic central-projective + stereographic family,
polar azimuth is preserved. Construction scale k changes radial mapping
but cannot convert a 540-degree source angular interval into approximately
594 degrees.

This provides a scale-independent incompatibility with the tested
construction family.

## Domain

All transformed source samples satisfy:

    0 < rho < 1

in both passes.

Thus failure is not caused by points leaving the finite stereographic
open-disk domain.

## Post-fit scale context

The two primary spiral fits give a descriptive mean slope magnitude of
approximately:

    k_spiral_mean = 1.787883

This should not be promoted to a calibrated construction scale because the
underlying isotropic model has large systematic residuals.

It may nevertheless be retained as a descriptive best-linear-fit quantity
for later model comparison.

## Verdict

    ISOTROPIC_RECIPROCAL_SHAPE_NOT_SUPPORTED

The printed spherical spiral is highly reproducibly measurable, but its
observed radial-angular geometry is not closely reproduced by the tested
fixed-frame isotropic central-projective + stereographic projection of the
unitary reciprocal spiral.

This result rejects the tested model family, not the source drawing itself
and not every possible spherical realization of a reciprocal spiral.

Possible explanations remaining open include:

- a different spherical construction map;
- anisotropic or otherwise non-isotropic mapping;
- an undocumented transformation;
- an illustrative rather than exact construction drawing;
- a source convention not represented by the tested model.

No one of these explanations is selected by the present result.

## Next methodological step

Before expanding the model family, inspect the already-frozen residual field
without fitting anything new.

Determine whether the failure is:

- smoothly systematic with rho / F(rho);
- concentrated in particular source segments;
- associated with winding phase;
- localized near crossings or occluded regions.

Only after that neutral residual morphology audit should a more flexible
construction family be preregistered.

