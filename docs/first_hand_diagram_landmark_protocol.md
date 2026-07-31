# First Hand diagram landmark and uncertainty protocol

**Version:** v0.8.0 source-image calibration protocol  
**Status:** preregistered; no landmarks digitized  
**Primary crops:** `AOG_P07_SPHERICAL_PROJECTION`, `AOG_P08_HAND_VIEWS`

## Purpose

This protocol freezes which visual features may be measured from the
published *Arm of God* diagrams, how they are acquired, how uncertainty
is assigned, and which measurements may calibrate the spherical map.

The source drawing is treated as potentially schematic. A close image
fit is therefore evidence of diagram correspondence, not automatically
evidence that the underlying physical sculpture has the same geometry.

## Coordinate convention

Every digitized record uses prepared-crop pixel coordinates:

```text
origin:      upper-left
x:           increases rightward
y:           increases downward
units:       pixels in the frozen prepared PNG
point:       centre of the intended stroke or node
curve order: explicitly recorded when the source supplies an orientation
```

The exact crop ID and pixel SHA-256 must accompany every digitization.

## Acquisition rule

No theoretical curve, fitted great circle, projection overlay, residual,
or self-embedment score may be displayed while landmarks are selected.

Point landmarks are clicked twice in independent passes. Curve objects
are traced twice independently where practical. The second pass must
begin from the untouched source crop, not from the first trace.

Text, arrowheads, leader lines, and labels are never treated as geometry.
Black intersection blobs are used only for registry rows explicitly
classified as point landmarks.

## Uncertainty model

For point landmark clicks `p1` and `p2`, define the stored point as their
componentwise mean. Its isotropic pixel uncertainty is

```text
sigma_point = max(
    registry minimum,
    local visible node/stroke radius,
    0.5 * ||p1 - p2||
)
```

For curve samples, each vertex receives

```text
sigma_curve = max(
    registry minimum,
    local half-stroke-width
)
```

The uncertainty is descriptive rather than a claim of Gaussian image
noise. Results must be reported both in pixels and normalized by the
fitted image-sphere radius.

A disagreement above 8 px for a point or above 12 px median nearest-curve
distance for a traced curve triggers manual review and is not silently
averaged.

## Fit partitions

### Calibration

The sphere boundary and labelled great-circle scaffold may determine:

- image centre and radius or ellipse;
- global image rotation;
- visible great-circle planes;
- central-projective pose;
- and admissible projective gauge.

### Scale calibration

The labelled `r=1, theta=1` point and the independent 30-degree arc may
compare the frozen scale hypotheses:

```text
G30:    k = tan(30 degrees)
GHALF:  k = tan(0.5 radians)
GUNIT:  k = 1
GONE:   k = tan(1 radian)
```

No scale may be selected using S1, S1.5, S2, or the final Hand shape.

### Holdout

The projected spiral centreline and its visible inner endpoint are
withheld from projective-gauge calibration. They assess whether a map
fitted to the labelled scaffold also reproduces the published spiral.

### External holdout

The page-8 Hand views are withheld until the spherical map, scale,
truncation convention, and three-copy construction have all been frozen.

## Weighting rule

Dense tracing must not make one object dominate merely because it has
more sampled pixels. Each registered geometric object receives equal
top-level weight. Samples within one object share that object's weight.

Results must also be reported object by object; a single pooled score is
insufficient.

## Fit hierarchy

1. Fit the visible sphere boundary independently.
2. Fit the labelled great-circle scaffold and incidence points.
3. Compare the frozen discrete scale hypotheses using only the
   scale-calibration landmarks.
4. Evaluate the projected spiral as a holdout.
5. Evaluate the page-8 Hand views only after the three-copy region is
   generated.
6. Compute no self-embedment predicate during image calibration.

A continuous scale fit may be reported only as a sensitivity analysis
after the four frozen discrete hypotheses have been evaluated.

## Metrics

Point objects:

```text
Euclidean pixel residual
residual / fitted image-sphere radius
residual / registered sigma
```

Curve objects:

```text
symmetric Chamfer distance
95th-percentile bidirectional distance
maximum bidirectional distance
topology and ordering checks where applicable
```

For thick source strokes, distances are computed to the digitized
centreline, with the registered stroke uncertainty reported separately.

## Diagram exactness

The audit must test rather than assume whether the drawing is metrically
consistent. Three outcomes are allowed:

```text
metric-compatible:
    one source-constrained map explains the labelled scaffold within
    digitization uncertainty

schematic-compatible:
    incidence and topology agree, but metric residuals substantially
    exceed digitization uncertainty

incompatible:
    even the labelled incidence structure cannot be reproduced
```

A schematic-compatible result does not invalidate the underlying
construction; it means the published drawing cannot uniquely calibrate
its metric parameters.

## Prohibited choices

The following are not allowed:

- moving landmarks after seeing residuals;
- choosing a scale because it improves endpoint alignment;
- fitting the spiral before the scaffold;
- using the Hand silhouette to tune the spherical map;
- tracing label leaders as great-circle segments;
- deleting inconvenient landmarks without a recorded source-quality
  reason;
- silently changing from the prose truncation to the diagram truncation.

## Outputs of the later digitization stage

The future digitizer must write:

```text
data/derived/first_hand_arm_of_god/
    diagram_landmarks_pass1.csv
    diagram_landmarks_pass2.csv
    diagram_landmarks_consensus.csv
    diagram_landmark_uncertainty.json
```

Every row must include the crop ID, landmark ID, pass number, sequence
index, x, y, local stroke-width estimate, operator note, and source-image
pixel hash.

## Scope boundary

This protocol contains no landmark coordinates, fitted parameters,
projection verdict, scale selection, or self-embedment result.
