# First Hand parallel-family equatorial-incidence diagnostic

**Version:** v0.8.0  
**Status:** protocol frozen before repository implementation/execution  
**Analysis status:** deterministic post-hoc structural diagnostic  
**Primary source page:** 7

## Motivation

The frozen stereographic spherical-plane reconstruction and subsequent
linear central-projective reconstruction produced asymmetric behaviour
for the two source-labelled affine coordinate families.

The y-family,

    y = 0
    y = 1

showed close directional consistency.

The x-family,

    x = 0  (the printed y-axis)
    x = 1

did not.

A subsequent independent review identified a simpler invariant of an
equator-preserving central-projective map:

> spherical great circles representing a parallel affine-line pair must
> intersect in an equatorial direction.

This checkpoint calculates that invariant directly from the already-frozen
spherical plane normals.

It does not refit any curve and does not alter any previous result.

## Post-hoc status

The conceptual diagnostic was proposed after inspection of the frozen
stereographic plane-angle and linear-reconstruction results.

Approximate expected values have therefore already been discussed outside
this implementation.

Consequently this checkpoint is not presented as a new blind or
confirmatory test.

Its purpose is:

1. reproduce the claimed invariant directly from frozen repository data;
2. quantify the two parallel-family intersection directions consistently;
3. connect the y-family result to its previously registered equatorial
   infinity landmark;
4. preserve the x-family failure without adding a more flexible model.

## Frozen parent inputs

Use only already-frozen results.

### Spherical planes

From the frozen stereographic spherical-plane reconstruction:

    AOG-LM-P07-GC-Y0
    AOG-LM-P07-GC-Y1
    AOG-LM-P07-GC-YAXIS
    AOG-LM-P07-GC-X1

Each curve already has a reconstructed unit plane normal.

No normal is recomputed from raw trace points in this checkpoint.

### Frozen limb / equatorial geometry

Use the already-frozen sphere centre and radius only where needed to
express an equatorial azimuth as a page-limb location.

They are not fitted again.

### Frozen y-family infinity landmark

The previously registered lower-right shared rim node is the source-defined
visible meeting point of the labelled

    y = 0
    y = 1

curves.

Use its already-frozen consensus position / rim bearing as an independent
source-landmark comparison for the y-family only.

No rim node is assigned retrospectively to the x-family.

## Family definitions

The two affine parallel families are fixed as:

### y-family

    zero line:
        AOG-LM-P07-GC-Y0

    unit-offset line:
        AOG-LM-P07-GC-Y1

### x-family

    zero line:
        AOG-LM-P07-GC-YAXIS

    unit-offset line:
        AOG-LM-P07-GC-X1

These identities come from the printed source labels and are not changed
after inspecting the diagnostic.

## Central-projective parallelism condition

Consider an equator-preserving linear central-projective map

    S_L(p)
      = normalize(
            L p,
            1
        ).

For one affine coordinate family define a horizontal dual vector

    g = (g_x, g_y).

The zero-coordinate and unit-offset spherical planes have normals of the
form

    n_0 = (g_x, g_y, 0)

and

    n_1 = (g_x, g_y, -1)

up to nonzero scale and overall sign.

Their intersection direction is

    s_raw = n_0 x n_1.

Since

    n_0 x n_1
      = (-g_y, g_x, 0),

the intersection line lies exactly in

    z = 0.

Therefore an exact affine-parallel pair under this model must have an
equatorial spherical intersection direction.

## Frozen-plane intersection calculation

For each family use the already-frozen unit plane normals

    n_a
    n_b.

Compute

    s_raw = n_a x n_b

and

    s = s_raw / ||s_raw||.

Because each great-circle plane is unoriented,

    n and -n

represent the same plane.

Therefore

    s and -s

represent the same intersection line.

All diagnostics must be sign-invariant.

## Primary equatorial-incidence diagnostics

For each family report:

    |s_z|

and the absolute angular departure from the equatorial plane,

    epsilon_equator
      = asin(|s_z|)

in degrees.

For exact affine parallels:

    |s_z| = 0
    epsilon_equator = 0 degrees.

No PASS/FAIL threshold is introduced.

The deviations are reported continuously.

## Intersection-line azimuth

Let

    rho_xy = sqrt(s_x^2 + s_y^2).

When

    rho_xy > 0,

define the horizontal azimuth of the intersection line by

    alpha
      = atan2(s_y, s_x)

converted to degrees modulo 360.

Because s and -s describe the same line, also report the antipodal
direction

    alpha_antipode
      = (alpha + 180 degrees) mod 360.

For comparisons between unoriented intersection lines, use an azimuth
modulo 180 degrees.

For source-landmark comparison, use whichever antipodal direction is
nearest the preregistered landmark.

For a non-equatorial intersection, alpha is explicitly described as the
azimuth of the horizontal projection of the 3-D intersection direction.
It is not described as an actual equatorial intersection point.

## y-family source-landmark validation

Only the y-family has an independently registered source infinity point.

The lower-right shared rim node was registered before this diagnostic as
the visible meeting point of:

    y = 0
    y = 1

on the equator-at-horizon limb.

For the y-family report:

1. predicted intersection-line azimuth;
2. antipodal azimuth;
3. frozen lower-right node rim bearing;
4. minimum circular angular separation between the node bearing and the
   two antipodal predicted directions.

Define

    delta_node_deg

as that minimum separation.

No node location is fitted.

No rotation is applied to improve the comparison.

### Optional page-space representation

Using the frozen sphere centre

    (c_x, c_y)

and radius

    R,

the horizontal azimuth direction may also be represented on the limb by

    x_pred = c_x + R cos(alpha)
    y_pred = c_y - R sin(alpha)

for the antipodal branch nearest the frozen lower-right node.

If the frozen node consensus pixel position is available from the parent
result, report the Euclidean page-space separation

    delta_node_px.

This is descriptive only.

The angular bearing comparison is the primary landmark diagnostic.

## x-family boundary

No rim node is selected for the x-family after seeing the result.

For the x-family report only:

    |s_z|
    epsilon_equator
    horizontal-projection azimuth
    antipodal azimuth.

A nearby sixfold/scaffold bearing may be discussed later only under a
separately frozen source-semantic or scaffold-association analysis.

This checkpoint does not declare the x=1 trace to be a scaffold curve.

## Relation to the previous eta diagnostic

The preceding linear central-projective reconstruction reported

    eta_y

between the Y1 circle-centre dual direction and the observed Y0 normal,
and

    eta_x

between the X1 circle-centre dual direction and the observed YAXIS normal.

The present equatorial-incidence diagnostic is mathematically related to
that same parallel-family condition.

It is therefore not counted as independent statistical evidence from the
eta values.

Its purpose is to express the failure geometrically in terms of where the
two reconstructed spherical great circles intersect.

The y-family comparison to the independently digitized lower-right rim
node is a distinct source-landmark consistency check, although the
numerical diagnostic itself remains post-hoc in this checkpoint.

## Rendering-quality context

Carry forward the already-frozen stereographic rendering diagnostics:

### Y1

    epsilon_power
    Delta_R
    Delta_antipodal

### X1

    epsilon_power
    Delta_R
    Delta_antipodal

This preserves the observed asymmetry:

- Y1 has stronger directional parallel-family consistency but weaker
  stereographic circle closure.
- X1 has stronger stereographic circle closure but weaker parallel-family
  directional consistency.

No one metric is allowed to overwrite the other.

## Acquisition-quality boundary

Do not use the obsolete pre-QC X1 duplicate-input-burst residuals as
evidence against the X1 trace.

The frozen QC-corrected acquisition result remains authoritative for
trace reproducibility.

Thus this checkpoint tests geometry, not acquisition reliability.

## No reclassification of X1

The source registry identifies the traced object as the printed curve
labelled

    x = 1.

That semantic identity remains unchanged in this checkpoint.

Possible later interpretations include:

1. the page contains an internally inconsistent coordinate label;
2. the source intentionally overlays a coordinate role on a scaffold arc;
3. the graphical label-to-stroke association is ambiguous;
4. another source-construction convention is present.

None is selected here.

## Outputs

Produce a deterministic result containing at minimum:

### y-family

    unit plane normal Y0
    unit plane normal Y1
    normalized intersection direction
    |s_z|
    epsilon_equator_deg
    horizontal azimuth_deg
    antipodal azimuth_deg
    frozen lower-right node bearing_deg
    delta_node_deg
    optional delta_node_px

### x-family

    unit plane normal YAXIS
    unit plane normal X1
    normalized intersection direction
    |s_z|
    epsilon_equator_deg
    horizontal azimuth_deg
    antipodal azimuth_deg

### context

    prior eta_y
    prior eta_x

    Y1 rendering closure
    X1 rendering closure

## Interpretation categories

No numerical threshold is introduced.

### Near-equatorial family

A family whose

    epsilon_equator

is small may be described as approximately satisfying the equatorial
intersection requirement.

### Non-equatorial family

A substantial

    epsilon_equator

is a direct violation of the exact affine-parallel requirement under the
tested equator-preserving central-projective model.

### Source-landmark agreement

For the y-family, a small

    delta_node_deg

supports consistency between the reconstructed parallel-family infinity
direction and the independently frozen source landmark.

No analogous claim is made for x without a preregistered x-family
infinity landmark.

## Forbidden actions

This checkpoint performs no:

- curve refit;
- circle refit;
- line refit;
- stereographic rendering refit;
- 2x2 map refit;
- 3x3 projective fit;
- nonlinear map fit;
- reassignment of X1;
- scaffold classification of X1;
- construction-scale selection;
- reciprocal-spiral projection;
- S1;
- S1.5;
- S2.

## Decision after this checkpoint

After the equatorial-incidence diagnostic is frozen:

1. conduct a source-semantic audit of the printed x=1 label and traced
   stroke;
2. preserve the y-family reconstruction and x-family inconsistency as
   separate findings;
3. only then consider a clearly labelled post-hoc three-curve isotropic
   reconstruction in which X1 is evaluated as a prediction rather than
   used to define the candidate model.

The three-curve reconstruction must not be described as prospectively
held out with respect to X1, because the hypothesis was developed after
the X1 inconsistency was already observed.
