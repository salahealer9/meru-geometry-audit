# First Hand two-pass curve geometry protocol

**Version:** v0.8.0  
**Status:** preregistered before numerical curve fitting  
**Raw-observation checkpoint:** `85ab104`  
**Input seal:** `data/derived/first_hand_arm_of_god/great_circle_segment_passes.sha256`

## Purpose

This stage measures agreement between the two independently acquired
curve passes and characterizes the image-space geometry of the visible
source strokes.

It is deliberately prior to:

- projective-map calibration;
- great-circle certification;
- projective gauge selection;
- spherical scale selection;
- reciprocal-spiral fitting;
- S1 tangent testing;
- S1.5 Darboux-frame testing;
- S2 recursive-nesting testing.

No self-embedment quantity may enter this stage.

## Frozen curve partitions

The four source-labelled coordinate curves are the calibration set:

```text
AOG-LM-P07-GC-Y0
AOG-LM-P07-GC-Y1
AOG-LM-P07-GC-YAXIS
AOG-LM-P07-GC-X1
````

The additional unlabelled scaffold curve is an independent holdout:

```text
AOG-LM-P07-GC-SCAFFOLD-UR-UC-X1LL-LL
```

The scaffold holdout must not be used to select a projective map,
projective gauge, orientation, affine scale, or spherical scale.

Its previously frozen node landmarks must not be used in fitting its
image-space curve. Node-to-curve incidence is evaluated only later as
a holdout test.

## Outer reference

The `AOG-LM-P07-EQUATOR-HORIZON-LIMB` is not reacquired or refitted from
the present five curves.

Its previously frozen neutral two-pass fit supplies the image-sphere
reference and normalization scale.

## Segment topology

Each `segment_id` is an observed visible fragment.

No analysis may connect two segments across:

* filled nodes;
* spiral occlusions;
* labels;
* arrows;
* ambiguous crossings;
* missing source strokes;
* or the equator-at-horizon boundary.

A fitted mathematical curve may be estimated jointly from several
visible segments belonging to the same registered source curve, but
the observed polyline itself is never bridged across an occlusion.

## Sampling-density invariance

Raw click count is not an evidential weight.

Each observed segment is interpreted as a piecewise-linear polyline.
Numerical evaluation samples that polyline uniformly in image-space
arc length.

The primary numerical sampling interval is:

```text
2 px
```

with both segment endpoints retained.

Changing how densely the operator clicked within an otherwise identical
stroke must therefore not materially alter the fit.

A secondary sampling sensitivity check uses:

```text
1 px
4 px
```

The scientific conclusion must not depend materially on choosing 1, 2,
or 4 px resampling.

## Pass weighting

Pass 1 and pass 2 receive equal total weight for each registered curve:

```text
weight(pass 1) = 0.5
weight(pass 2) = 0.5
```

Within a pass, contribution is proportional to visible polyline
arc length, not to the number of raw clicks and not to the number of
segments.

Thus a more densely clicked pass cannot dominate merely because it
contains more recorded vertices.

## Curve uncertainty

For every visible segment:

```text
sigma_curve =
    max(
        2 px,
        0.5 * local_stroke_width_px
    )
```

where `local_stroke_width_px` is the value recorded during acquisition.

This uncertainty is descriptive and does not imply independent Gaussian
pixel noise.

Results are reported both:

* in source-image pixels;
* and normalized by the previously frozen equator-at-horizon limb scale.

## Pass-to-pass agreement

Agreement is measured geometrically between the two piecewise-linear
traces, not by matching raw sequence indices.

For each registered curve compute directed point-to-polyline distances:

```text
pass 1 -> pass 2
pass 2 -> pass 1
```

after uniform arc-length resampling.

Report the symmetric distribution using at least:

```text
median
RMS
95th percentile
maximum
```

and the same quantities normalized by local curve uncertainty where
applicable.

The previously frozen manual-review rule remains active:

```text
median nearest-curve disagreement > 12 px
    -> manual review
```

A review trigger is not silently averaged away and is not automatically
a failure of the source geometry.

## Segment correspondence diagnostic

Because pass 1 and pass 2 were acquired independently, segment IDs encode
within-pass acquisition order rather than an assumed geometric identity.

The primary pass-agreement statistic therefore treats each curve as a
set of visible polylines and does not require S01 in one pass to match
S01 in the other.

Segment-count equality and possible segment correspondence may be
reported descriptively but may not be imposed to improve agreement.

## Model-neutral image-space fits

Each registered curve is characterized separately in each pass and in
an equal-pass combined fit.

Primary candidate families:

```text
circle
ellipse
```

These are image-space descriptive models.

A good circle or ellipse fit does not by itself establish that the
source stroke is the projection of a mathematical great circle.

For every candidate report:

* fitted parameters;
* arc-length-weighted RMS residual;
* median absolute residual;
* 95th-percentile absolute residual;
* maximum absolute residual;
* residual divided by local curve uncertainty;
* residual divided by the frozen image-sphere scale.

No candidate is declared geometrically exact from the hand-drawn plate.

## Combined fit

The combined objective for one curve has the form

```text
J = 0.5 * J_pass1 + 0.5 * J_pass2
```

where each `J_pass` is an arc-length-normalized objective over that
pass's visible segments.

Raw point counts therefore have no direct effect on pass weight.

## Circle-versus-ellipse interpretation

Circle and ellipse fits are descriptive diagnostics rather than a
binary hypothesis test.

An ellipse may absorb:

* page scanning deformation;
* drawing distortion;
* affine image distortion;
* or genuine non-circular source geometry.

Therefore improved ellipse residual alone does not establish a
non-great-circle construction.

## Limb-circularized sensitivity analysis

The primary analysis is performed in raw prepared-crop coordinates.

A secondary sensitivity analysis may apply the affine ellipse-to-circle
normalization determined exclusively from the previously frozen
equator-at-horizon limb.

The transform must not be re-estimated from the five internal curves.

Raw and limb-circularized results are both retained.

## Holdout boundary

The scaffold holdout receives the same descriptive two-pass agreement
and circle/ellipse census so that data quality can be assessed.

However it remains excluded from all calibration choices.

Only after the four labelled curves have frozen the admissible
projective calibration may the holdout be tested against:

* the recovered spherical scaffold;
* the upper-right rim node;
* the upper interior crossing;
* the X1-UC-LL incidence node;
* and the lower-left rim node.

## Hand-drawn-source interpretation

The page-7 source is a hand drawing.

Residuals comparable to stroke width, pass-to-pass variation, or
digitization sensitivity may support compatibility with an intended
construction but cannot certify exact mathematical incidence.

Conversely, small image-space departures from an exact construction are
not treated as decisive falsification without reference to these
uncertainties.

## Output boundary

This checkpoint may produce:

* two-pass agreement metrics;
* curve and segment metadata;
* circle-fit diagnostics;
* ellipse-fit diagnostics;
* raw-coordinate diagnostics;
* limb-circularized sensitivity diagnostics;
* and neutral visual overlays.

It must not produce:

* a preferred historical projection formula;
* a selected projective gauge;
* a selected spherical scale;
* a great-circle certification verdict;
* a reciprocal-spiral correspondence verdict;
* S1;
* S1.5;
* or S2.
