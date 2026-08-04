# First Hand spherical spiral two-pass reproducibility protocol

**Checkpoint:** v0.8  
**Status:** protocol frozen before cross-pass geometric comparison  
**Analysis class:** neutral acquisition-reproducibility audit

## Purpose

Quantify the reproducibility of two independently acquired centreline traces
of the thick spherical reciprocal spiral in the page-7 First Hand diagram.

The two raw passes were acquired independently from the untouched prepared
source crop and were frozen before cross-pass comparison.

This checkpoint does not test the theoretical reciprocal spiral.

It does not fit:

- r*theta = 1;
- any spherical construction map;
- any rendering map;
- any coordinate curve;
- any scaffold;
- any projective transformation.

Its sole primary question is:

> How reproducibly can the source-visible spherical spiral centreline be
> acquired from the printed diagram?

## Frozen raw inputs

Pass 1:

    data/derived/first_hand_arm_of_god/
    spherical_spiral_segments_pass1.csv

Seal:

    data/derived/first_hand_arm_of_god/
    spherical_spiral_segments_pass1.sha256

Pass 2:

    data/derived/first_hand_arm_of_god/
    spherical_spiral_segments_pass2.csv

Seal:

    data/derived/first_hand_arm_of_god/
    spherical_spiral_segments_pass2.sha256

Known acquisition totals at protocol freeze:

    Pass 1: 214 rows, 10 visible segments
    Pass 2: 229 rows, 10 visible segments

The equality of segment counts does not itself establish segment
correspondence.

## Raw-data immutability

The two raw CSV files are immutable.

No raw coordinate may be edited, deleted, replaced, reordered, or moved.

Any later correction must preserve the raw pass and create a derived QC file
plus an explicit exclusion ledger.

## QC rule

QC may identify only acquisition-system or data-integrity artifacts such as:

- exact repeated-event bursts;
- duplicated rows;
- impossible sequence numbering;
- malformed numeric fields;
- out-of-bounds coordinates;
- metadata inconsistency;
- demonstrable accidental repeated click events.

A point may not be excluded because:

- it disagrees with the other pass;
- it increases a residual;
- it disagrees with r*theta = 1;
- it disagrees with a candidate spherical map;
- it lies away from a fitted curve;
- it appears inconvenient for segment correspondence.

If no objective acquisition artifact is found, the raw passes become the
authoritative analysis inputs.

## Stage A — metadata-only QC

Before any cross-pass geometric calculation, inspect:

- row counts;
- segment IDs;
- sequence continuity;
- exact duplicate coordinates;
- repeated timestamps/events;
- local stroke-width fields;
- operator notes;
- crop hashes.

No inter-pass coordinate distances are computed during Stage A.

Any exclusion decision must be frozen before Stage B.

## Stage B — segment correspondence

Segment correspondence must be established before numerical cross-pass
distances are computed.

Permitted evidence:

- segment order;
- acquisition notes;
- source-visible start and end features;
- source topology;
- occlusion/crossing descriptions;
- source-only page-7 crop.

Forbidden evidence:

- cross-pass numerical distance;
- best-fit alignment;
- theoretical reciprocal spiral;
- coordinate-model prediction;
- scaffold prediction;
- endpoint-consensus coordinates.

### Correspondence classes

For every visible source run classify correspondence as one of:

    ONE_TO_ONE
    PASS1_SPLIT
    PASS2_SPLIT
    MANY_TO_MANY
    UNRESOLVED

A one-to-one pairing is not assumed merely because both passes contain the
same number of segments.

### Correspondence freeze

The completed segment-correspondence ledger must be committed before the
reproducibility-distance calculation.

No pairing may later be changed because another pairing produces a smaller
distance.

## Stage C — geometry representation

Each segment is represented as its ordered polyline in source-image pixels.

No smoothing spline, polynomial, circle, spiral, or theoretical curve is
fitted.

### Arclength parameterization

For each polyline:

1. compute cumulative Euclidean chord length;
2. normalize cumulative arclength to [0,1];
3. linearly resample along the polyline.

Use:

    N_RESAMPLE = 401

points per independently visible source segment.

The fixed 401-point resampling removes differences in raw click density.

Resampling does not bridge across separate source-visible segments.

## Primary one-to-one segment metric

For each one-to-one corresponding segment pair A and B:

1. uniformly arclength-resample A to 401 points;
2. uniformly arclength-resample B to 401 points;
3. for every resampled point of A compute its minimum Euclidean distance to
   the polyline B;
4. for every resampled point of B compute its minimum Euclidean distance to
   the polyline A.

The primary segment discrepancy sample is the union of the two directed
distance sets.

This is a symmetric point-to-polyline comparison.

It does not depend on:

- acquisition click density;
- acquisition speed;
- point-index correspondence;
- tracing direction.

## Segment-level reported metrics

For every resolved corresponding source run report:

    Pass-1 raw point count
    Pass-2 raw point count
    Pass-1 polyline length
    Pass-2 polyline length
    mean polyline length

and symmetric distance:

    median
    mean
    RMS
    p95
    maximum

all in source-image pixels.

Also report normalized values divided by the frozen spherical-limb radius:

    R_limb = 341.906449919 px

The limb radius is used only as a dimensionless reporting scale.

It is not used for fitting or registration.

## No geometric registration

The two passes are already expressed in the same prepared source-image pixel
coordinate system.

Therefore do not perform:

- translation alignment;
- rotation alignment;
- scale alignment;
- Procrustes alignment;
- ICP;
- affine registration;
- projective registration.

Any raw positional disagreement is part of acquisition reproducibility.

## Aggregate metric A — equal-segment weighting

Let MSE_s be the mean squared symmetric point-to-polyline discrepancy for
resolved source segment s.

Define:

    RMS_equal =
        sqrt(mean_s(MSE_s))

Every resolved source segment therefore contributes equal weight regardless
of its printed length or number of raw clicks.

Also report the arithmetic mean of segment medians and segment p95 values as
descriptive summaries.

## Aggregate metric B — curve-length weighting

For each resolved source segment define:

    w_s =
        0.5 * (L_pass1,s + L_pass2,s)

where L is polyline arclength in pixels.

Define:

    RMS_length =
        sqrt(
            sum_s(w_s * MSE_s)
            /
            sum_s(w_s)
        )

This allows longer visible spiral runs to contribute proportionally to the
amount of source-visible curve they represent.

Both equal-segment and length-weighted results are mandatory.

Neither is selected after seeing the result.

## Split/merge correspondence

If Stage B identifies a genuine split or merge:

1. concatenate only source-topologically consecutive fragments belonging to
   the same continuously visible source run;
2. do not interpolate across an occlusion;
3. preserve the original segment IDs in provenance;
4. compare the union of visible polylines using the same symmetric
   point-to-polyline metric.

No split/merge operation may be introduced from numerical proximity alone.

## Unresolved segments

Any `UNRESOLVED` correspondence is excluded from the primary aggregate
reproducibility calculation but reported explicitly.

Report:

    number of unresolved source runs
    Pass-1 visible length excluded
    Pass-2 visible length excluded
    fraction of visible length excluded

No unresolved fragment is silently dropped.

## Local acquisition uncertainty

Each raw segment records local stroke width.

For each paired source run report:

    median recorded stroke width, Pass 1
    median recorded stroke width, Pass 2

and the frozen local acquisition floor:

    sigma_source =
        max(
            2 px,
            0.5 * median local stroke width
        )

This is a descriptive source-reading uncertainty scale.

Do not convert it into a Gaussian standard deviation or statistical
confidence interval.

## Endpoint holdouts

The following previously frozen neutral landmarks remain external to the
reproducibility calculation:

    AOG-LM-P07-RIM-NODE-LR-SHARED
    AOG-LM-P07-SPHERE-INNER-END

They are not used to:

- register the passes;
- orient the passes;
- establish segment correspondence;
- select points;
- alter segment boundaries.

Only after the primary cross-pass reproducibility result is frozen may the
visible spiral endpoints be compared against these independent landmarks.

## Endpoint comparison after reproducibility freeze

For each pass, identify the source-visible terminal sample belonging to the
outermost and innermost visible spiral runs using the frozen segment topology.

Then report Euclidean separation from:

    outer -> AOG-LM-P07-RIM-NODE-LR-SHARED
    inner -> AOG-LM-P07-SPHERE-INNER-END

Do not snap an endpoint to either landmark.

The consensus coordinates are independent checks, not fit targets.

## Forbidden theoretical use

During this checkpoint do not use:

- theta values;
- 3*pi;
- 1 + 3*pi;
- reciprocal radius;
- planar spiral coordinates;
- 30-degree angles;
- half-radian angles;
- cube-octahedral scaffold geometry;
- Y0/Y1/YAXIS/X1 reconstructed planes;
- candidate projective-map scales.

## Expected outputs

Derived QC, if required:

    data/derived/first_hand_arm_of_god/qc/
    spherical_spiral_pass1_qc.csv

    data/derived/first_hand_arm_of_god/qc/
    spherical_spiral_pass2_qc.csv

    data/derived/first_hand_arm_of_god/qc/
    spherical_spiral_qc_exclusions.csv

Correspondence:

    reports/
    first_hand_spherical_spiral_segment_correspondence.md

Numerical result:

    data/derived/first_hand_arm_of_god/qc/
    first_hand_spherical_spiral_reproducibility.json

    data/derived/first_hand_arm_of_god/qc/
    first_hand_spherical_spiral_reproducibility_segments.csv

    reports/
    first_hand_spherical_spiral_reproducibility.md

Diagnostic figure:

    data/derived/first_hand_arm_of_god/qc/
    first_hand_spherical_spiral_reproducibility.png

## Interpretation

Low two-pass residuals establish that the printed spherical spiral can be
reproducibly acquired from the source.

They do not establish that it is a projected reciprocal spiral.

High residuals indicate source-reading or acquisition ambiguity and must be
carried into later spiral-model tests.

No theoretical spiral comparison begins until this reproducibility
checkpoint and the independent endpoint comparison are frozen.

