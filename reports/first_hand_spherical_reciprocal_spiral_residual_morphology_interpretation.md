# First Hand reciprocal-spiral residual morphology interpretation

**Checkpoint:** v0.8
**Status:** interpretation of frozen residual-morphology result
**Outcome:** `REPRODUCIBLE_SYSTEMATIC_RESIDUAL`

## Pointwise cross-pass replication

The frozen primary residual fields contain:

    4010 exact topological Pass-1 / Pass-2 pairs

Angular residual replication:

    Pearson r              = 0.989615180774
    RMS pass difference    = 6.563422908 deg
    p95 pass difference    = 14.742975956 deg

Angular-chord replication:

    Pearson r              = 0.989564268546
    RMS pass difference    = 5.266567288 px
    p95 pass difference    = 9.609956716 px

Residual-sign replication:

    same nonzero sign      = 0.976807980050
    opposite sign          = 0.023192020

The residual field therefore reproduces very strongly between independently
acquired traces.

## Relation to parent-model discrepancy

The frozen parent isotropic reciprocal-shape fits had approximately:

    angular RMS            = 39--41 deg
    angular-chord RMS      = 64 px

The cross-pass residual-field disagreement is much smaller:

    angular RMS difference = 6.56 deg
    chord RMS difference   = 5.27 px

The large parent-model residual therefore cannot reasonably be attributed
primarily to digitization instability.

It is a reproducible property of the printed source geometry under the
tested model.

## Segment concentration

Pass 1 weighted SSE fractions:

    S05 = 0.229990
    S06 = 0.205647
    S08 = 0.286434

Combined:

    0.722071

Pass 2 weighted SSE fractions:

    S05 = 0.230608
    S06 = 0.202558
    S08 = 0.308125

Combined:

    0.741291

Thus the same three source regions account for approximately 72--74% of
the weighted squared angular error in both independent passes.

The failure is nevertheless not confined to a single local source defect.

## Segment sign structure

Signed segment means have the same sign pattern in both passes:

    S01  +
    S02  -
    S03  -
    S04  +
    S05  +
    S06  +
    S07  -
    S08  -
    S09  -
    S10  +

This repeated alternation further supports systematic residual morphology.

## Primary interpretation

    REPRODUCIBLE_SYSTEMATIC_RESIDUAL

The isotropic reciprocal-spiral construction fails in a highly structured
and independently reproducible manner.

The result is compatible with a missing deterministic geometric
transformation.

It does not identify that transformation.

## Linear-anisotropy guardrail

A general invertible centered 2x2 planar linear transformation changes the
angular speed of directions but obeys

    beta(theta + pi) = beta(theta) +/- pi.

Therefore a complete source interval of length 3*pi retains an absolute
directional winding of 3*pi under such a map.

A centered 2x2 anisotropic expansion cannot by itself explain the observed
approximately 594-degree clean-trace winding as a transformation of the
frozen 540-degree source interval.

Accordingly, a 2x2 anisotropic fit should not be introduced merely because
the residual field is structured.

## Remaining diagnostic question

Before selecting an expanded construction family, inspect the already-frozen:

- radial residual bins;
- printed winding-phase residual bins;
- source-order residual bins;
- segment-level cross-pass correlations.

In particular, phase morphology may distinguish qualitatively between:

- directional anisotropy;
- displacement of the chart origin relative to the rendering pole;
- more general projective/nonlinear structure.

No alternative model is selected at this checkpoint.

