# First Hand spherical reciprocal-spiral trace acquisition protocol

**Checkpoint:** v0.8  
**Status:** protocol frozen before numerical acquisition  
**Analysis class:** source-trace acquisition  
**Primary source:** Arm of God, page 7

## Purpose

Acquire the visible centreline of the thick reciprocal-spiral projection in
the page-7 spherical diagram independently of all coordinate-map fits.

The resulting trace will later permit a spiral-led test:

    planar r*theta = 1
        ->
    candidate spherical construction map
        ->
    frozen stereographic rendering
        ->
    observed page-7 spherical spiral

The spiral trace must therefore be acquired before any spiral-derived map is
fitted.

## Scientific motivation

Previous coordinate analysis found:

- strong y-family central-projective consistency;
- source-confirmed X1 identity;
- no source-supported X1 scaffold reclassification;
- irreducible x-family incompatibility under scale freedom.

Those results remain frozen.

This acquisition asks no coordinate-consistency question.

It measures only the visible spherical spiral.

## Target object

Target:

    the thick black reciprocal-spiral projection drawn inside the
    page-7 spherical projection

Source crop:

    AOG_P07_SPHERICAL_PROJECTION

Prepared source image:

    data/source_snapshots/first_hand_arm_of_god/prepared/
    aog_p07_spherical_projection.png

The existing frozen crop and its hashes are authoritative.

## Acquisition object

Acquire the visual centreline of the thick spiral stroke.

Do not acquire:

- stroke edges;
- coordinate great circles;
- outer spherical limb;
- annotation leaders;
- text;
- black node boundaries;
- hidden portions behind occlusions.

## No model-guided tracing

During acquisition do not display or use:

- reciprocal-spiral model overlays;
- fitted circles;
- fitted great circles;
- cube-octahedral scaffold overlays;
- 30-degree guides;
- predicted spherical coordinates;
- prior X1/Y1/Y0/YAXIS residuals;
- candidate construction scales;
- spiral-derived coordinate predictions.

Source pixels alone determine the trace.

## Segment rule

Create a new segment whenever the visible spiral is interrupted by:

- a black node;
- coordinate-line overprinting;
- annotation text;
- another source stroke;
- an unresolved crossing;
- a genuine visibility gap.

Do not interpolate across hidden portions.

Every segment must be a continuously visible run.

## Crossing rule

At crossings classify the spiral continuation as:

    VISIBLE_CONTINUATION
    AMBIGUOUS_CONTINUATION
    OCCLUDED_OR_UNRESOLVED

If continuation is ambiguous, stop the current segment.

Do not choose a branch using expected spiral curvature.

## Centreline rule

Click approximately along the middle of the visible thick stroke.

The local uncertainty is:

    max(2 px, local half-stroke-width)

Record local stroke width during acquisition.

## Sampling rule

Sampling density may follow local visual curvature.

Raw click density will not be treated as statistical weighting.

Any later geometric comparison must uniformly resample each visible segment
before computing distance metrics.

## Two-pass acquisition

Perform two independent passes.

### Pass 1

Acquire all visible spiral segments.

Freeze and seal immediately.

### Pass 2

Perform only after Pass 1 is sealed.

Do not display Pass-1 points.

Acquire the spiral again from the source pixels.

Freeze and seal immediately.

Pass agreement measures acquisition reproducibility; it does not establish
geometric correctness.

## Endpoint semantics

The already-frozen lower-right shared rim node may be recorded as the visible
outer-terminus source landmark where the spiral converges with the labelled
y=0/y=1 curves.

Do not force an acquired point onto that node.

Measure any endpoint separation later.

The planar parameter ambiguity remains frozen:

    prose convention:
        theta_outer -> 0+
        theta_inner = 3*pi relative to outer end

    diagram convention:
        theta_outer = 1
        theta_inner = 1 + 3*pi

Neither convention is used to guide tracing.

## Inner endpoint

Record the innermost visible terminus exactly as printed.

Do not assume in advance that it corresponds to:

- a sphere pole;
- the chart origin;
- the central black-square landmark;
- a scaffold node;
- any particular theta value.

Those are later model tests.

## Required fields

Each raw record must contain:

    crop_id
    crop_file_sha256
    crop_pixel_sha256
    landmark_id
    pass_number
    operator
    segment_id
    sequence_index
    x_px
    y_px
    local_stroke_width_px
    source_feature
    operator_note
    timestamp_utc

Use landmark identifier:

    AOG-LM-P07-SPIRAL-SPHERICAL

## QC policy

Raw passes are immutable.

If an acquisition-system artifact occurs, correction requires:

1. explicit metadata-based diagnosis;
2. a separate exclusion ledger;
3. preservation of raw data;
4. a QC-derived file;
5. separate provenance and checksum.

No point may be excluded because it disagrees with a spiral model.

## Later permitted analyses

Only after both passes are frozen and QC is complete may later checkpoints:

1. quantify two-pass reproducibility;
2. construct a neutral morphology census;
3. compare the trace against candidate spherical projections of r*theta=1;
4. use the spiral to calibrate a construction-map family;
5. predict coordinate curves from a spiral-derived map.

## Critical interpretation boundary

The spiral may be used later to select or reject a coordinate-map model.

It may not retroactively alter the already-frozen source identity of
Y0, Y1, YAXIS, or X1.

If a spiral-derived model produces coordinate curves different from the
printed coordinate curves, that is a model/source comparison result rather
than permission to redefine the source curves.

## Model hierarchy after acquisition

The later analysis should proceed from least flexible to more flexible:

### S0 — source trace only

No theoretical spiral.

### S1 — frozen existing construction maps

Project r*theta=1 through already-defined source-constrained maps without
refitting them.

### S2 — spiral-calibrated low-dimensional construction family

Allow only preregistered low-dimensional parameters, calibrated from the
spiral and not from coordinate-curve residuals.

All four labelled coordinate curves then become independent predictions.

### S3 — spiral-induced/nonlinear chart

Consider only if the spiral itself rejects the existing central-projective
families and if a mathematically explicit construction can be motivated
without using X1 as a tuning target.

No flexible nonlinear chart may be introduced merely to repair X1.

## Interpretation boundary

A successful spiral-led reconstruction could show that the earlier
coordinate-first model was incomplete.

It would not erase the earlier result:

    under the tested equator-preserving central-projective coordinate
    interpretation, the source-labelled X-family is incompatible.

The two statements can coexist.

