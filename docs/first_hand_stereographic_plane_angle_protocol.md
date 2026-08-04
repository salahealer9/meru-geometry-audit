# First Hand stereographic spherical-plane reconstruction protocol

**Version:** v0.8.0
**Status:** preregistered before numerical plane-angle reconstruction
**Parent rendering comparator:** frozen before this protocol
**Primary source page:** 7

## Purpose

The preceding parameter-free rendering comparator found that the already
frozen page geometry is substantially more compatible with stereographic
great-circle invariants than with the fixed-limb orthographic rendering,
especially for GC-X1 and the independent scaffold holdout.

This checkpoint asks the next narrow question:

> What spherical great-circle plane angles are implied by the already
> frozen line and circle geometry under the stereographic rendering
> hypothesis?

No curve is refitted.

No page-sphere radius is refitted.

No reciprocal spiral is used.

No self-embedment score is calculated.

## Mapping distinction

This checkpoint concerns the reconstruction

    printed stereographic great-circle trace
        -> spherical great-circle plane.

It does not itself fit the earlier flat-construction-plane to sphere map.

Only after the plane angles are frozen may they be compared with the
source-constrained inverse-gnomonic construction family.

## Frozen inputs

Use only:

1. the frozen outer-limb centre and radius;
2. the frozen neutral morphology line fits;
3. the frozen neutral morphology circle fits;
4. the frozen stereographic rendering-comparator result.

The orthographic reconstruction remains preserved as an earlier
comparator but is not used to derive the stereographic plane angles.

## Labelled reconstruction set

Only the four source-labelled curves participate:

    AOG-LM-P07-GC-Y0
    AOG-LM-P07-GC-Y1
    AOG-LM-P07-GC-YAXIS
    AOG-LM-P07-GC-X1

The scaffold holdout is excluded from:

- plane-angle calibration;
- construction-scale inference;
- isotropy testing.

Its planar preimage remains unspecified.

## Frozen branch allocation

From the already-frozen neutral morphology and rendering-comparator
protocol:

### Stereographic line branch

    GC-Y0
    GC-YAXIS

### Stereographic finite-circle branch

    GC-Y1
    GC-X1

No branch assignment is changed after seeing plane-angle results.

## Coordinate normalization

Let the frozen sphere centre be

    O = (cx, cy)

and frozen equator radius be

    R.

Page pixels are converted to normalized y-up coordinates:

    u = (x_px - cx) / R
    v = -(y_px - cy) / R.

For displacement vectors, the translation is omitted and the page-y
component changes sign.

## Stereographic great-circle equation

For a unit sphere and normalized stereographic page coordinates, a
great-circle plane through the sphere centre with normal

    n = (nx, ny, nz)

projects as

    nz (u^2 + v^2 - 1)
      + 2 nx u
      + 2 ny v
      = 0.

Plane normals are unoriented:

    n and -n

represent the same spherical great circle.

## Finite-circle reconstruction

If

    nz != 0,

the projected great circle is a circle.

After division by nz:

    u^2 + v^2
      + 2 (nx/nz) u
      + 2 (ny/nz) v
      - 1
      = 0.

Therefore its normalized page-circle centre is

    c_u = -nx / nz
    c_v = -ny / nz.

For each frozen curved trace, calculate its frozen circle-centre
displacement from the frozen sphere centre and normalize by R.

The reconstructed plane normal is then taken as

    n_raw = (-c_u, -c_v, 1)

and normalized to unit length.

No use is made of the measured free-circle radius in reconstructing
the plane normal.

The radius remains an independent closure diagnostic from the preceding
rendering-comparator checkpoint.

This prevents the stereographic invariant from being fitted by construction.

## Line reconstruction

If

    nz = 0,

the projected great circle is a straight line through the stereographic
projection pole.

Let the frozen page-space line direction, converted to y-up normalized
coordinates, be

    d = (d_u, d_v).

Its page-space normal is

    m = (-d_v, d_u).

The reconstructed spherical plane normal is

    n_raw = (m_u, m_v, 0)

and is normalized to unit length.

The previously measured miss-distance of the frozen line from the frozen
sphere centre is not used to rotate or translate this normal.

It remains an independent rendering-closure residual.

## Reconstructed plane-angle pairs

Compute the unoriented angle between spherical planes using

    delta(n1,n2)
      = arccos(|n1 dot n2|),

with result in the interval

    [0 degrees, 90 degrees].

The two source-coordinate separations are

    delta_x
      = angle(GC-YAXIS, GC-X1)

and

    delta_y
      = angle(GC-Y0, GC-Y1).

No equality between them is imposed.

## Derived construction-scale quantities

Only after delta_x and delta_y have been independently reconstructed,
derive

    k_x = tan(delta_x)
    k_y = tan(delta_y).

Also report:

    delta_difference
      = delta_x - delta_y

    absolute_delta_difference
      = |delta_x - delta_y|

    k_ratio
      = k_x / k_y

when finite.

These are descriptive isotropy diagnostics.

No post-hoc threshold for equality is introduced.

## Isotropic inverse-gnomonic relation

The previously established canonical construction family is

    M_k(x,y)
      = normalize(k x, k y, 1).

Under this family:

    y-axis:   X = 0
    x=1:      X/k - Z = 0

and

    y=0:      Y = 0
    y=1:      Y/k - Z = 0.

Therefore the plane separations predicted by an isotropic construction
are

    delta_x = atan(k)
    delta_y = atan(k).

This relation is not used to reconstruct delta_x or delta_y.

It is evaluated only after both have been frozen independently.

## Fixed source-motivated scale comparators

After the image-derived angles have been calculated, compare them
descriptively against the already-frozen scale candidates:

### G30

    k = tan(30 degrees)
    predicted delta = 30 degrees

### GHALF

    k = tan(0.5 radians)
    predicted delta = 0.5 radians
                    approximately 28.6478897565 degrees

### GUNIT

    k = 1
    predicted delta = 45 degrees

### GONE

    k = tan(1 radian)
    predicted delta = 1 radian
                    approximately 57.2957795131 degrees

For each candidate report separately:

    delta_x - delta_candidate
    delta_y - delta_candidate

and optionally the RMS of those two angular deviations.

The candidates are not redefined or optimized.

## Source ambiguity

The page-8 source material supplies both an approximately 30-degree
cube-octahedral division and a half-radian approximately 29-degree
candidate.

Therefore a numerical result near that region must not be retroactively
described as uniquely selecting one historical convention unless the
measured uncertainty and residual separation genuinely support that
distinction.

The previously frozen source ambiguity remains part of the interpretation.

## Rendering-closure context

The plane-angle reconstruction must be reported together with the earlier
stereographic closure diagnostics:

    GC-Y0 line-centre miss
    GC-YAXIS line-centre miss
    GC-Y1 epsilon_power / Delta_R
    GC-X1 epsilon_power / Delta_R.

This is particularly important for GC-Y1, whose stereographic invariant
misclosure is larger than GC-X1.

A plane angle derived from an imperfect rendering fit is not presented as
exact historical geometry.

## No uncertainty manufacture

This checkpoint does not treat the fitted line and circle parameters as
independent iid measurements.

No formal confidence interval on delta_x, delta_y, k_x, or k_y is invented
from the 2 px point uncertainty floor.

Sensitivity analysis, if later required, must be separately defined using
the existing 1/2/4 px frozen morphology results or a preregistered
propagation method.

## Holdout boundary

The scaffold remains outside this checkpoint's scale reconstruction.

Its strong stereographic invariant closure is retained as independent
support for the rendering hypothesis, but without an independently known
planar-coordinate identity it cannot determine k.

## Interpretation outcomes

### Approximate isotropy

If delta_x and delta_y are close relative to the hand-drawn source
precision, the result may be described as compatible with an approximately
isotropic source-coordinate construction.

### Anisotropy

If delta_x and delta_y differ materially, report the corresponding
k_x and k_y separately.

Do not average them into a single k unless a later protocol explicitly
justifies doing so.

### Source-scale comparison

The fixed G30, GHALF, GUNIT, and GONE candidates are compared only after
the reconstructed angles are frozen.

No candidate is tuned to the observed result.

## Forbidden outputs

This checkpoint computes no:

- new curve fit;
- new stereographic rendering fit;
- general projective gauge;
- reciprocal-spiral projection;
- spiral endpoint reconstruction;
- S1 score;
- S1.5 score;
- S2 score.

## Next checkpoint

Only after the stereographic plane angles and fixed-scale comparisons are
frozen will the audit decide whether the evidence is strong enough to
choose a construction-scale branch for projecting the reciprocal spiral.

If no scale is sufficiently identified, the subsequent spiral audit must
retain multiple frozen scale variants rather than selecting one.
