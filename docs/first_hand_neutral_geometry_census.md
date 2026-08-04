# First Hand neutral geometry census implementation

**Stage:** v0.8 neutral two-pass source geometry  
**Input boundary:** frozen crop plus two committed blind passes

## Purpose

This checkpoint converts the two raw point passes into a deterministic
consensus and performs only the source-neutral image-space measurements
frozen in the revised protocol.

It does not activate the four printed great-circle traces and does not
load the spherical-map or self-embedment audits.

## Outputs

```text
data/derived/first_hand_arm_of_god/
    neutral_landmark_consensus.csv
    neutral_geometry_census.json

reports/
    first_hand_neutral_geometry_census.md

figures/
    first_hand_neutral_geometry_overlay.png
```

## Point consensus

For every point landmark:

```text
consensus = (pass1 + pass2) / 2

uncertainty = max(
    registry floor,
    half the larger recorded full stroke/node width,
    half the pass-to-pass separation
)
```

The committed raw passes remain unchanged.

## Limb fitting

The outer limb is fitted independently in each pass. A pooled circle and
a descriptive pooled ellipse are also fitted.

Because the two traces contain different numbers of clicks, each pass
receives total pooled weight 0.5. The 49-point pass therefore does not
dominate the 40-point pass.

The circle uses geometric radial residuals. The ellipse uses a
normalized-radial residual converted to an approximate pixel scale; it
is not claimed to be an exact orthogonal point-to-ellipse distance.

## Sixfold diagnostic

Rim bearings use mathematical image angles:

```text
0 degrees: rightward
90 degrees: upward
angles increase counter-clockwise
```

A free-phase sixfold model reports the phase modulo 60 degrees, bearing
residuals, successive gaps, gap residuals, and sixth-harmonic strength.
This measures image-space regularity only and does not uniquely identify
a cuboctahedral construction.

## Neutral reference measurements

The census also reports:

```text
central-node offset from fitted limb centre
upper-crossing bearing and radial fraction
pass agreement for every point
panel-specific unit-marker coordinates
panel-specific inner-endpoint coordinates
```

Flat-panel and spherical-panel coordinates are retained separately.
Their raw crop-pixel separation is not treated as a physical or angular
discrepancy because the panels have different image frames.

## Execution boundary

Commit the implementation and tests before producing the census:

```bash
pytest -q tests/test_first_hand_neutral_geometry_audit.py
pytest -q
```

Then run:

```bash
python scripts/audit_first_hand_neutral_geometry.py
```

No projective, great-circle, scale, truncation, or self-embedment verdict
is issued by this checkpoint.
