# A10_P03 Crossing-Sign Protocol

## Objective

Assign an oriented sign to each of the 31 reviewed A10_P03 crossing events.

## Inputs

The calculation uses:

- the frozen 24-segment global-cycle traversal;
- the 31 reviewed over-under crossing assignments;
- each crossing side's polyline piece index and local fraction;
- the tracked manual digitisation.

No assumed knot type or three-dimensional surface enters the calculation.

## Coordinate convention

The source panel uses image coordinates with positive `y` downward.

Before evaluating a sign, each tangent is transformed to a right-handed
Cartesian image plane:

\[
(x,y)=(x_{\mathrm{image}},-y_{\mathrm{image}}).
\]

The viewing normal `+z` points toward the viewer.

## Crossing-sign convention

Let

- \(\mathbf t_{\mathrm{over}}\) be the over-strand tangent;
- \(\mathbf t_{\mathrm{under}}\) be the under-strand tangent;

with both tangents oriented along the frozen cycle traversal.

The sign is

\[
\varepsilon=
\operatorname{sign}
\det
\left(
\mathbf t_{\mathrm{over}},
\mathbf t_{\mathrm{under}}
\right).
\]

Thus:

- positive determinant: `+1`;
- negative determinant: `-1`;
- zero determinant: geometrically degenerate and unresolved.

## Tangent estimation

The primary tangent estimate is a secant spanning 6 pixels of polyline arc
length around the recorded crossing-side location.

At visible-fragment endpoints, the estimate is clipped one-sidedly.

Sensitivity is evaluated at spans:

```text
2 px, 4 px, 6 px, 8 px, 10 px, 12 px
````

A sign is stable when it remains unchanged across all six spans.

## Low-angle review

Any event whose minimum tangent angle over the sensitivity spans is below
25 degrees is placed into manual review.

The review checks:

* over-strand identity;
* under-strand identity;
* traversal direction of both strands;
* agreement with the derived determinant sign.

## Invariance checks

Reversing the orientation of the complete cycle reverses both tangents at each
crossing and therefore preserves every crossing sign.

Mirroring the source plane reverses every determinant and therefore reverses
every crossing sign.

## Interpretation boundary

The sign census characterizes this source-derived planar projection under one
explicit convention.

It does not establish the knot type, minimal crossing number, canonical
`(3,10)` equivalence, or a unique three-dimensional embedding.
