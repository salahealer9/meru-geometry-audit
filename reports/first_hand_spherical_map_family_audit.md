# First Hand spherical-map family audit

**Status:** Source-incidence certificate  
**Primary source:** `AOG_PDF_2005A`  
**Source SHA-256:** `80d52f4b6afefe65ae50e4c01378765c34ae4fde1ad44e8b299870c2e1d3e6fa`  
**Result:** A central-projective family is supported; no unique map or scale is certified

## Source constraints

The page-7 construction labels the planar lines

```text
x-axis
y-axis
x=1
y=1
```

as great-circle projections on a spherical coordinate surface. It also
states that the planar infinite end becomes finite where the relevant
great circles reach the equator.

This checkpoint tests only those incidence and infinity statements.

## Canonical candidate

The isotropic inverse gnomonic family is

\[
M_k(x,y)
=
\frac{(kx,ky,1)}
{\sqrt{k^2x^2+k^2y^2+1}},
\qquad
k>0.
\]

For every planar affine line

\[
ax+by+c=0,
\]

its image lies in

\[
\frac{a}{k}X
+
\frac{b}{k}Y
+
cZ
=
0.
\]

That plane passes through the sphere centre, so the image is a great
circle. This is an exact geometric property, not a fitted numerical
coincidence.

All four tested scales pass the source-incidence constraints:

| ID | \(k\) | central angle of planar unit radius | status |
|---|---:|---:|---|
| G30 | 0.577350269189626 | 30 degrees | PASS |
| GHALF | 0.54630248984379 | 0.5 radians | PASS |
| GUNIT | 1 | 45 degrees | PASS |
| GONE | 1.5574077246549 | 1 radian | PASS |

The maximum tested line-to-great-circle residual is

```text
5.34250667069375e-16
```

## Why the map is not unique

More generally, for any invertible matrix \(A\),

\[
M_A(x,y)
=
\operatorname{normalize}
\left(
A
\begin{bmatrix}
x\\y\\1
\end{bmatrix}
\right)
\]

maps planar lines to great circles.

For a planar line \(\ell^Tp=0\), the spherical image satisfies

\[
(A^{-T}\ell)^TX=0,
\]

which is again a plane through the sphere centre.

Therefore the source's line-incidence statements identify a
central-projective class. They do not, by themselves, eliminate
anisotropy, shear, projective gauge freedom, global spherical rotation,
or the scale \(k\).

The isotropic inverse gnomonic map is the simplest canonical member of
that class, not yet a uniquely recovered historical formula.

## Stereographic comparator

Inverse stereography correctly maps the planar coordinate axes through
the projection origin to great circles. It does not map the offset
lines \(x=1\) and \(y=1\) to great circles.

Their fitted great-circle RMS residuals are:

```text
x=1: 0.228632465737214
y=1: 0.228632465737214
```

It also sends planar infinity to the stereographic pole rather than to
the distinct equatorial directions depicted in the source.

Thus inverse stereography fails the tested page-7 incidence model.

## Angular-scale caution

Page 8 discusses both a 30-degree cube-octahedral division and
approximately half a radian as candidates for one unit angle.

Those statements motivate G30 and GHALF, but do not prove that the
planar reciprocal-spiral parameter unit is identical to the affine
scale \(k\) in the spherical map. The two quantities remain separate
until the source diagrams are calibrated.

No scale is selected by endpoint alignment in this checkpoint.

## Result boundary

Established:

- a central-projective map class satisfies the source incidence model;
- isotropic inverse gnomonic maps are canonical valid members;
- inverse stereography is not compatible with the tested offset-line
  great-circle statements;
- all tested isotropic scales remain observationally equivalent under
  incidence constraints alone.

Not established:

- one unique historical projection formula;
- projective gauge, anisotropy, orientation, or scale;
- correspondence to the drawn spiral silhouette;
- S1 tangent alignment;
- S1.5 frame alignment;
- S2 recursive nesting.

The next phase is source-image calibration. It must estimate projective
gauge and scale from the page-7 and page-8 drawings without using any
self-embedment score as a fitting objective.
