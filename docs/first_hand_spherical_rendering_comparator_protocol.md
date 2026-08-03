# First Hand spherical-rendering invariant comparator

**Version:** v0.8.0
**Status:** preregistered before stereographic-invariant calculation
**Parent great-circle reconstruction:** frozen before this protocol
**Neutral morphology parent:** 05ebae0
**Primary source page:** 7

## Motivation

The preceding limb-constrained orthographic reconstruction produced a
structured mixed result.

The source-labelled traces GC-Y0 and GC-YAXIS were compatible with the
fixed-limb orthographic projected-great-circle family at the adopted
2 px image-space uncertainty scale.

GC-Y1 and GC-X1 were not. Their orthographic residuals were much larger
than both the adopted uncertainty scale and their previously frozen
free circle/ellipse residuals.

This protocol does not alter that result.

Instead it tests whether the already-measured page geometry is compatible
with a different rendering of a spherical great-circle scaffold:
stereographic projection.

This is a rendering comparator only. It is not the previously audited
flat-construction-plane to sphere map.

## Important distinction

Two mappings must remain separate.

### Construction map

The previously audited source-constrained map asks how planar construction
coordinates such as

    y=0
    y=1
    y-axis
    x=1

may map onto a spherical coordinate surface.

That audit selected a central-projective class as mathematically capable
of mapping affine lines to spherical great circles.

### Rendering map

The present checkpoint instead asks how an already-spherical great-circle
scaffold may have been rendered onto the two-dimensional printed page.

No implication from one mapping to the other is assumed.

## Frozen inputs

No source trace is refitted in this checkpoint.

The inputs are:

1. the frozen outer-limb centre and radius;
2. the frozen neutral morphology census;
3. its frozen weighted orthogonal-line fits;
4. its frozen free-circle fits;
5. the frozen orthographic great-circle reconstruction, used only as a
   comparator.

The raw two-pass observations and acquisition-QC history remain immutable.

## Frozen morphology branch allocation

The branch allocation is fixed from the already-published neutral
morphology result before any stereographic invariant is calculated.

### Near-linear labelled traces

    AOG-LM-P07-GC-Y0
    AOG-LM-P07-GC-YAXIS

These are evaluated against the stereographic great-circle line branch.

### Curved labelled traces

    AOG-LM-P07-GC-Y1
    AOG-LM-P07-GC-X1

These are evaluated against the stereographic great-circle circle branch.

### Independent curved holdout

    AOG-LM-P07-GC-SCAFFOLD-UR-UC-X1LL-LL

The scaffold receives the same invariant calculation as the curved
labelled traces but remains a holdout.

It does not calibrate, tune, or select any rendering parameter.

No branch assignment is changed after seeing the stereographic result.

## Frozen image sphere

Let the frozen outer limb have page centre

    O = (cx, cy)

and radius

    R.

No new sphere centre or radius is fitted.

Normalized coordinates are

    u = (x - cx) / R
    v = -(y - cy) / R.

Thus the frozen equator is

    u^2 + v^2 = 1.

## Stereographic great-circle invariant

Consider the unit sphere under stereographic projection onto the page
plane, normalized so that the sphere's equator maps to the unit circle.

A spherical great circle is the intersection of the sphere with a plane

    nx X + ny Y + nz Z = 0

through the sphere centre.

After stereographic projection its image satisfies

    nz (u^2 + v^2 - 1)
      + 2 nx u
      + 2 ny v
      = 0.

Two cases result.

### Finite-circle branch

If

    nz != 0,

the projected locus is a circle.

If its normalized page-space centre has distance d from the frozen sphere
centre and its radius is r, then

    r^2 - d^2 = 1.

In pixel units this becomes

    r_px^2 - d_px^2 = R_px^2.

Therefore define the signed power-closure residual

    Delta_power
      = r_px^2
        - d_px^2
        - R_px^2.

The dimensionless form is

    epsilon_power
      = Delta_power / R_px^2.

When

    r_px^2 - d_px^2 > 0,

also define the radius-equivalent closure

    R_implied
      = sqrt(r_px^2 - d_px^2)

and

    Delta_R
      = R_implied - R_px.

No circle is refitted to force Delta_power or Delta_R to zero.

### Diameter-line branch

If

    nz = 0,

the stereographic image of the great circle is a straight line through
the frozen sphere centre.

For a previously frozen orthogonal line fit, define

    d_line

as the perpendicular distance from the frozen sphere centre to that line.

Also report

    epsilon_line = d_line / R_px.

No line is refitted through the sphere centre.

## Antipodal-intersection diagnostic

For every curved branch, calculate the intersections between:

1. the frozen free circle for the trace;
2. the frozen outer-limb circle.

If two real intersections exist, calculate their angular separation about
the frozen sphere centre.

For an exact stereographically rendered great circle, that separation is

    180 degrees.

Define

    Delta_antipodal
      = |180 degrees - separation|.

This diagnostic is geometrically equivalent to the circle invariant in
the exact case, but it is reported independently because it has a direct
visual interpretation.

If the two frozen circles do not intersect in two real points, report that
fact without inventing intersections.

## Primary quantities

### Y0 and Y-axis

Report:

- frozen line RMS;
- line-to-frozen-centre distance d_line;
- d_line / R;
- frozen orthographic great-circle RMS.

### Y1 and X1

Report:

- frozen free-circle RMS;
- free-circle centre;
- free-circle radius r;
- centre offset d from the frozen sphere centre;
- r / R;
- d / R;
- Delta_power;
- epsilon_power;
- R_implied when real;
- Delta_R when real;
- equator-circle intersection count;
- antipodal angular separation when defined;
- Delta_antipodal when defined;
- frozen orthographic great-circle RMS.

### Scaffold holdout

Report the same finite-circle stereographic invariants as Y1 and X1.

Do not calculate or import an orthographic fitted result for the scaffold,
because it was explicitly excluded from the orthographic calibration.

## No new optimization

This checkpoint contains:

    zero free geometric parameters
    zero optimizer calls
    zero curve refits.

Every tested quantity is an algebraic consequence of already-frozen
image-space geometry.

## Interpretation

Small stereographic invariant residuals would show that the observed
line/circle morphology is compatible with a stereographically rendered
great-circle family.

They would not prove that the historical drawing was generated by
stereographic projection.

Large invariant residuals would show that stereography also fails to
explain the source geometry at the corresponding scale.

Because the source is hand drawn, numerical deviations are reported
continuously rather than converted into a new post-hoc binary threshold.

The existing 2 px uncertainty floor is not mechanically transferred to
Delta_R as though the fitted circle parameters were independent
point measurements.

## Comparator boundary

The frozen orthographic result remains unchanged.

This checkpoint may state that one rendering has smaller descriptive
misclosure than another, but it does not erase or rewrite either result.

In particular, the orthographic failures for GC-Y1 and GC-X1 remain part
of the permanent record.

## Holdout rule

The scaffold is evaluated only after the stereographic invariant has been
defined completely.

It cannot:

- change the invariant;
- change the line/circle branch allocation;
- introduce a page scale;
- choose a projection pole;
- choose a projective gauge.

Its result is therefore an independent descriptive holdout.

## Forbidden outputs

This checkpoint computes no:

- new flat-to-sphere construction map;
- projective gauge;
- construction-map scale;
- G30/GHALF/GUNIT/GONE verdict;
- spherical plane-angle calibration;
- reciprocal-spiral projection;
- self-embedment S1;
- Darboux S1.5;
- recursive S2.

## Decision after this checkpoint

Three broad outcomes are possible.

### Outcome A — strong stereographic compatibility

The two axial traces pass close to the frozen sphere centre and the
three curved traces approximately satisfy

    r^2 - d^2 = R^2,

including the independent scaffold holdout.

This would justify a later stereographic spherical-plane reconstruction.

### Outcome B — labelled compatibility but holdout failure

Y0, Y-axis, Y1, and X1 are compatible but the scaffold is not.

That would weaken any claim that the whole visible scaffold shares one
stereographic great-circle construction.

### Outcome C — general failure

The finite-circle invariant fails substantially for the curved traces.

The appropriate conclusion would then be that the page is schematic,
uses some other rendering, or does not preserve one exact spherical
great-circle construction.

No more flexible projection is introduced automatically merely to improve
the fit.
