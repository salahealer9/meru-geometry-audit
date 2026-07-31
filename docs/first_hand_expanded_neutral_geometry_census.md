# First Hand expanded neutral geometry census

**Stage:** v0.8 expanded source-node census  
**Inputs:** frozen original passes and frozen incidence-addendum passes

## Purpose

This checkpoint regenerates the original neutral census from its frozen
raw passes and combines it with the three separately frozen incidence
points.

It does not reuse the provisional output files preserved under `/tmp`.
All reported values are regenerated from committed evidence.

## Inputs

```text
data/derived/first_hand_arm_of_god/
    diagram_landmarks_pass1.csv
    diagram_landmarks_pass2.csv
    diagram_landmark_passes.sha256

    diagram_incidence_addendum_pass1.csv
    diagram_incidence_addendum_pass2.csv
    diagram_incidence_addendum_passes.sha256
```

## Outputs

```text
data/derived/first_hand_arm_of_god/
    expanded_neutral_landmark_consensus.csv
    expanded_neutral_geometry_census.json

reports/
    first_hand_expanded_neutral_geometry_census.md

figures/
    first_hand_expanded_neutral_geometry_overlay.png
```

## Expanded point census

The output contains:

```text
12 original neutral point consensuses
3 incidence-addendum point consensuses
15 total point consensuses
```

The original outer-limb traces remain part of the regenerated neutral
analysis but are not duplicated as point rows.

## Node-defined angle

The script measures:

```text
angle(UCLR, central, LR)
```

and reports:

```text
angle
signed residual from 30 degrees
absolute residual from 30 degrees
central-to-UCLR ray length
central-to-LR ray length
ray-length ratio
linearized coordinate sensitivity
```

The sensitivity propagates the protocol point scales through a numerical
angle Jacobian under isotropic independent coordinate perturbations. It
is a first-order sensitivity scale, not a confidence interval.

The measurement is an image-space source diagnostic. It does not assume
that a later projective map preserves angles.

## Y-axis two-node diagnostic

The central filled circular node and the separate y-axis addendum node
define an image-space direction.

The script reports:

```text
node separation
bearing from the central node
distance from the fitted limb centre to the two-node line
normalized centre-to-line distance
```

This is not yet a fit to the printed y-axis curve.

## Two x=1 incidence nodes

The script reports the chord length and chord bearing between:

```text
X1-UC-LL
UCLR
```

Two points do not determine the full printed projected great circle, so
no curve conclusion is issued.

## Run chronology

Freeze the implementation first:

```bash
pytest -q \
  tests/test_first_hand_expanded_neutral_geometry_audit.py

pytest -q
```

Then execute:

```bash
python \
  scripts/audit_first_hand_expanded_neutral_geometry.py
```

The resulting report and figure may then be inspected before the
expanded numerical census is committed.

## Interpretation boundary

This checkpoint computes no:

```text
great-circle trace or curve fit
hidden-curve interpolation
projective-map selection
unit-angle selection
truncation reconciliation
S1
S1.5
S2
```

## Hand-drawn source interpretation

The source panel is a hand-drawn and subsequently reproduced diagram.
The measured node-defined angle is therefore interpreted at the
resolution of that source rather than as a machine-drafted exact
construction.

The measured angle is approximately 27.637 degrees, with a residual of
approximately -2.363 degrees from 30 degrees. This residual is smaller
than the approximately 2.449-degree linearized coordinate-sensitivity
scale.

That sensitivity includes the registered point-coordinate scales but
does not include all possible hand-drafting, line-width, scanning, or
page-deformation effects. The result is therefore compatible with an
intended 30-degree construction, but it does not certify an exact
30-degree angle.

The very small normalized distance from the fitted limb centre to the
two-node y-axis direction supports intentional central alignment in the
drawing. Identification of the complete printed curve as a projected
great circle remains reserved for the segment-aware curve stage.
