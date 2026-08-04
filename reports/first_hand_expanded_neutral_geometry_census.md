# First Hand expanded neutral geometry census

**Stage:** v0.8 neutral census plus frozen incidence addendum

## Scope

This report regenerates the original neutral census and adds the three separately preregistered and frozen incidence nodes. It does not fit a great-circle trace, interpolate hidden curves, select a projective map, choose a unit convention, reconcile truncations, or compute S1, S1.5, or S2.

## Provenance

- Original neutral point landmarks: `12`
- Incidence-addendum point landmarks: `3`
- Expanded point consensus: `15`
- Crop pixel SHA-256: `afb1df2172f081fa426f2f86c56912079116f6441ba64df367861d00375fddc4`

## Regenerated original neutral census

- Equal-pass limb centre: `(1255.126839, 694.602782) px`
- Equal-pass limb radius: `341.906450 px`
- Sixfold bearing RMS residual: `0.632826°`
- Central circular-node offset/radius: `0.02447182`

These values are regenerated directly from the frozen original passes; the provisional pre-addendum result files are not reused.

## Added incidence-node consensus

| Landmark | x (px) | y (px) | Pass separation (px) | Uncertainty (px) | Bearing from limb centre (deg) | Radial fraction |
|---|---:|---:|---:|---:|---:|---:|
| `AOG-LM-P07-X1-UC-LL-INTERSECTION` | 1079.428 | 805.490 | 1.670 | 6.750 | 212.257 | 0.607664 |
| `AOG-LM-P07-X1-UC-LR-INTERSECTION` | 1422.674 | 805.490 | 2.362 | 6.750 | 326.502 | 0.587639 |
| `AOG-LM-P07-YAXIS-UC-UCLR-INTERSECTION` | 1359.202 | 634.284 | 3.735 | 5.500 | 30.095 | 0.351826 |

## Node-defined 30-degree diagnostic

- Measured angle `angle(UCLR, central, LR)`: `27.637300°`
- Signed residual from 30°: `-2.362700°`
- Absolute residual from 30°: `2.362700°`
- Linearized coordinate sensitivity: `2.449469°`
- Central→UCLR length: `203.097142 px`
- Central→LR length: `340.594791 px`
- Ray-length ratio UCLR/LR: `0.596301`

The sensitivity is a first-order propagation of the protocol point scales, not a confidence interval. The 2.363-degree residual is smaller than the 2.449-degree linearized sensitivity scale. Because the source is hand-drawn, additional drafting, line-width, scanning, and page-deformation effects are not represented by that scale. The result is therefore compatible with an intended 30-degree construction, but it does not certify an exact 30-degree angle or an angle-preserving projective map. The ambiguous printed 30-degree arc remains deferred.

## Y-axis two-node diagnostic

- Central-to-separate-node distance: `128.474343 px`
- Bearing from central node: `30.899882°`
- Fitted limb-centre distance to the two-node line: `1.689707 px`
- Normalized centre-to-line distance: `0.004942`

The two nodes define only an image-space direction. Whether the printed y-axis trace follows the same projected great circle remains for segment-aware curve digitization.

## Two x=1 incidence nodes

- Node-pair chord length: `343.245597 px`
- Chord bearing: `0.000000°`

This chord is descriptive only. Two incidence nodes do not determine the full printed x=1 great-circle image.

## Interpretation boundary

No great-circle, projective-map, unit-angle, truncation, or self-embedment verdict is issued.
