# First Hand linear central-projective reconstruction protocol

**Version:** v0.8.0
**Status:** preregistered before numerical linear-gauge reconstruction
**Parent:** frozen stereographic spherical-plane reconstruction
**Primary source page:** 7

## Purpose

The preceding stereographic spherical-plane reconstruction recovered

    delta_x = angle(GC-YAXIS, GC-X1)

and

    delta_y = angle(GC-Y0, GC-Y1)

independently.

The two angles were not equal, so the page-7 evidence does not justify
selecting a single isotropic inverse-gnomonic scale.

This checkpoint therefore tests the broader equator-preserving linear
central-projective construction family without fitting the four curves
jointly.

The central question is:

> Can the two frozen offset-coordinate circles, GC-X1 and GC-Y1,
> reconstruct a single linear central-projective map that independently
> predicts the two frozen zero-coordinate lines GC-YAXIS and GC-Y0?

## Mapping model

Let planar source coordinates be

    p = (x, y)^T.

Consider

    S_L(p)
      = normalize(
            L p,
            1
        )

with

    L in GL(2).

This is an equator-preserving central-projective map.

The affine origin maps to the distinguished spherical pole.

The line at planar infinity maps to the spherical equator.

No translation, nonlinear warp, or general 3x3 projective map is
introduced in this checkpoint.

## Source-coordinate line equations

Define

    e_x = (1,0)^T
    e_y = (0,1)^T.

Let

    g_x = L^(-T) e_x
    g_y = L^(-T) e_y.

Then the source-coordinate line families map to spherical planes:

    x = 0:
        g_x . (X,Y) = 0

    x = 1:
        g_x . (X,Y) - Z = 0

    y = 0:
        g_y . (X,Y) = 0

    y = 1:
        g_y . (X,Y) - Z = 0.

Thus each parallel planar pair shares the same horizontal plane-normal
component.

## Stereographic page consequence

Under the frozen normalized stereographic page rendering,

    u = (x_px - cx) / R
    v = -(y_px - cy) / R,

a great-circle plane

    g . (X,Y) - Z = 0

projects to a page circle whose normalized centre is exactly

    c = g.

Therefore:

    c_X1 = g_x
    c_Y1 = g_y.

The two frozen offset-circle centres determine

    G = [ c_X1  c_Y1 ]

where the two vectors are columns.

Provided det(G) != 0,

    G = L^(-T)

and therefore

    L = (G^(-1))^T.

No optimizer is required.

## Calibration partition

Only the two frozen finite-circle centres are used to reconstruct L:

    AOG-LM-P07-GC-X1
    AOG-LM-P07-GC-Y1.

Their previously frozen free-circle radii are NOT used.

Their trace points are NOT refitted.

The frozen stereographic circle-closure residuals remain independent
context only.

## Independent line validation

The reconstructed map predicts:

    GC-YAXIS page-line normal parallel to c_X1

and

    GC-Y0 page-line normal parallel to c_Y1.

The already-frozen Y-axis and Y0 line fits are not used to reconstruct L.

For each pair compute the unoriented page-normal angular residual:

    eta_x
      = angle(
            observed normal of GC-YAXIS,
            c_X1
        )

    eta_y
      = angle(
            observed normal of GC-Y0,
            c_Y1
        ).

Angles are reported in [0,90] degrees using absolute dot products.

No post-hoc PASS threshold is introduced.

These are the primary validation quantities.

## Scale consistency quantities

For an exact source-coordinate parallel family,

    delta_x
      = atan(1 / ||c_X1||)

and

    delta_y
      = atan(1 / ||c_Y1||).

Therefore derive directly from the frozen circle centres:

    k_x_center
      = 1 / ||c_X1||

    k_y_center
      = 1 / ||c_Y1||.

These are distinct from the previously reported

    tan(delta_x)
    tan(delta_y)

when the observed zero-line normal is not perfectly parallel to the
corresponding circle-centre vector.

Report both and their discrepancies.

Do not silently replace one with the other.

## Full reconstructed L

Report:

    G
    det(G)
    condition number of G
    L = (G^-1)^T
    det(L)
    condition number of L.

No element of L is optimized.

## Structural decomposition

Compute the singular-value decomposition

    L = U Sigma V^T

with singular values

    sigma_1 >= sigma_2 > 0.

Report:

    sigma_1
    sigma_2
    sigma_1 / sigma_2.

The ratio is a descriptive linear-anisotropy measure.

Also compute

    L^T L.

This checkpoint may report whether the recovered matrix is numerically
close to:

1. isotropic similarity:
       L approximately k R

2. orthogonal-axis anisotropy:
       L approximately R diag(k_x,k_y)

3. general linear/sheared gauge.

No classification threshold is introduced post hoc.

Instead report continuous diagnostics.

## Source-axis geometry

Using the reconstructed vectors c_X1 and c_Y1, report their unoriented
angle

    gamma_G.

Under an isotropic or rotation-plus-axis-anisotropic map, the corresponding
dual vectors are orthogonal.

Deviation from 90 degrees is therefore a direct shear/skew diagnostic.

Separately report the observed angle between the frozen Y-axis and Y0
page-line normals.

Do not force either angle to 90 degrees.

## Rendering closure remains independent

Carry forward, unchanged:

    X1 epsilon_power
    X1 Delta_R
    X1 Delta_antipodal

    Y1 epsilon_power
    Y1 Delta_R
    Y1 Delta_antipodal.

These quantities are not used to construct G or L.

This is especially important because Y1 has larger stereographic
misclosure than X1.

## Holdout boundary

The unlabelled scaffold remains excluded.

Its planar preimage is not independently known, so it cannot define a
column of L and cannot be used to improve the reconstruction.

Its previous stereographic rendering closure remains an independent
rendering holdout only.

## Fixed source-scale candidates

G30, GHALF, GUNIT, and GONE are not used to reconstruct L.

After L and the validation residuals are frozen, its singular values and
centre-derived coordinate scales may be compared descriptively with
already-frozen source candidates.

No source candidate is selected merely because it is the nearest of the
finite set.

## Interpretation

### Strong linear-central-projective support

If the X1/Y1-derived map predicts the independent Y-axis/Y0 directions
closely, then one linear central-projective construction explains all
four labelled coordinate traces under the stereographic page-rendering
hypothesis.

The resulting L may then be studied for isotropy, anisotropy, or shear.

### Directional mismatch

If eta_x or eta_y is substantial, the offset curves and zero-coordinate
lines do not support one exact equator-preserving linear central-projective
map.

The audit must then preserve that inconsistency rather than absorb it
with a more flexible fit.

### Singular reconstruction

If G is singular or numerically ill-conditioned, no stable L is claimed.

## No uncertainty manufacture

No iid uncertainty model is introduced.

No confidence intervals are inferred from the 2 px tracing floor.

Any later sensitivity analysis must be separately preregistered.

## Forbidden outputs

This checkpoint computes no:

- curve refit;
- rendering refit;
- nonlinear construction map;
- unrestricted 3x3 projective fit;
- reciprocal-spiral projection;
- spiral endpoint fit;
- S1;
- S1.5;
- S2.

## Decision after this checkpoint

Only if the independently predicted zero-coordinate lines are compatible
with the frozen observations should L be promoted as a candidate
construction gauge for the reciprocal-spiral stage.

Otherwise the page-7 construction remains geometrically underdetermined
or internally approximate.
