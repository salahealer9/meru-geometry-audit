# First Hand spherical spiral endpoint topology

**Checkpoint:** v0.8  
**Status:** frozen before endpoint-distance calculation  
**Analysis class:** source-topological endpoint selection

## Purpose

Define which acquired samples represent the visible inner and outer
termini of the spherical spiral before consulting the independently
frozen endpoint coordinates.

No endpoint distance is calculated in this ledger.

## Frozen dependencies

The continuous spherical spiral was independently acquired twice and the
two-pass reproducibility result has already been frozen.

Frozen correspondence:

    P1:S01 <-> P2:S01
    ...
    P1:S10 <-> P2:S10

All ten visible runs are ONE_TO_ONE.

## Inner endpoint selection

The frozen source topology identifies S01 as the first innermost visible
spiral run.

Therefore the visible inner endpoint sample is defined as:

    Pass 1:
        first ordered sample of S01
        sequence_index = 0

    Pass 2:
        first ordered sample of S01
        sequence_index = 0

Independent holdout:

    AOG-LM-P07-SPHERE-INNER-END

The holdout coordinate is not used to choose the sample.

## Outer endpoint selection

The frozen source topology identifies S10 as the final visible spiral run
approaching the lower-right rim region.

Therefore the visible outer endpoint sample is defined as:

    Pass 1:
        final ordered sample of S10

    Pass 2:
        final ordered sample of S10

Independent holdout:

    AOG-LM-P07-RIM-NODE-LR-SHARED

The holdout coordinate is not used to choose the sample.

## No snapping

The selected spiral samples remain at their acquired pixel coordinates.

Do not:

- replace them by the holdout coordinates;
- extend the spiral to the holdout;
- interpolate beyond the final acquired point;
- fit a tangent or curve to extrapolate an endpoint;
- move either endpoint along the visible stroke.

## Distances

After this topology ledger is frozen, report separately for each pass:

    d_inner =
        Euclidean distance(
            selected S01 initial sample,
            frozen inner-end consensus
        )

    d_outer =
        Euclidean distance(
            selected S10 final sample,
            frozen lower-right rim-node consensus
        )

Also report the two-pass mean endpoint coordinate and its distance to each
holdout as a descriptive consensus comparison.

The mean endpoint is not a fitted endpoint and is not substituted into the
raw acquisitions.

## Normalization

Report endpoint separations in:

    pixels

and normalized by the frozen spherical-limb radius:

    R_limb = 341.906449919 px

## Source-reading scales

Carry the independently frozen landmark uncertainty associated with each
holdout exactly as recorded in the neutral landmark consensus.

Carry the spiral local stroke-width acquisition scale associated with the
selected endpoint segment.

These quantities are descriptive scales only.

Do not convert them into Gaussian confidence intervals.

## Interpretation

Small endpoint separations would show consistency between two independently
acquired representations of the same source feature:

1. the earlier point-landmark acquisition;
2. the later continuous spiral acquisition.

They would not establish the reciprocal-spiral equation or any spherical
construction map.

Large separations would identify an endpoint-semantic or acquisition
difference that must be carried into subsequent spiral-model analysis.

## Forbidden use

This endpoint check does not use:

- r*theta = 1;
- theta endpoint conventions;
- 3*pi;
- 1 + 3*pi;
- coordinate-map fitting;
- great-circle fitting;
- scaffold geometry;
- X1 reconciliation;
- spiral-map calibration.

