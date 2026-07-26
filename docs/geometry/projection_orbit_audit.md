# Projection-Orbit Audit

## Purpose

This checkpoint determines how many genuinely distinct orthographic views are
generated when an object is acted upon by the 12 proper rotations of a regular
tetrahedron.

The distinction is important because 12 group elements do not necessarily
produce 12 independent viewing directions or 12 independent silhouettes.

## Projection convention

Three-dimensional points are represented as row vectors.

For a proper rotation \(R_i\), the rotated points are

\[
X_i = XR_i^\mathsf{T}.
\]

Orthographic projection onto the \(xy\)-plane gives

\[
P_i(X)=P(XR_i^\mathsf{T}).
\]

## Camera direction

Projection after rotating the object is equivalent to observing the original
object along the direction

\[
n_i=R_i^\mathsf{T}\hat z,
\]

where

\[
\hat z=(0,0,1)^\mathsf{T}.
\]

Two rotations can therefore represent the same viewing direction while
differing only by an in-plane rotation.

## Signed and unoriented directions

Signed camera directions distinguish front and back views:

\[
n\neq -n.
\]

Unoriented viewing axes identify them:

\[
n\sim -n.
\]

For the cube-aligned tetrahedron used in this repository, the camera-direction
orbit lies in

\[
\{\pm\hat x,\pm\hat y,\pm\hat z\}.
\]

The theoretical maximum capacities are therefore:

\[
6
\]

classes under orientation-preserving planar equivalence, and

\[
3
\]

classes when planar reflections are also treated as equivalent.

These are upper bounds for a generic object. Symmetries of a particular object
can reduce the number further.

## Exact frame-induced planar equivalence

Let \(R_a\) and \(R_b\) be two tetrahedral rotations and define

\[
S=R_bR_a^\mathsf{T}.
\]

When their camera directions are equal or opposite, \(S\) preserves the
projection plane and has block form

\[
S=
\begin{pmatrix}
Q & 0\\
0 & \varepsilon
\end{pmatrix},
\]

where

\[
Q\in O(2),
\qquad
\varepsilon\in\{+1,-1\}.
\]

Because \(\det S=+1\),

\[
\det Q=\varepsilon.
\]

Therefore:

- equal signed camera directions imply \(Q\in SO(2)\);
- opposite camera directions imply a planar reflection, \(\det Q=-1\).

This relationship is independent of the object being projected.

## Planar similarity alignment

For two projected curves \(X\) and \(Y\), the audit minimises

\[
\left\|sXQ+t-Y\right\|_{\mathrm{RMS}},
\]

where:

- \(t\in\mathbb R^2\) is a translation;
- \(s\geq 0\) is a non-negative uniform scale;
- \(Q\in SO(2)\) for rotation-only equivalence;
- \(Q\in O(2)\) when reflections are allowed.

The reported relative error divides the residual RMS by the centred RMS size
of the target curve.

When the best centred correlation under the permitted planar transformation is
zero or negative, the constrained optimum occurs at the boundary

\[
s=0.
\]

This produces relative RMS error \(1\), representing a complete failure to
match the centred shape rather than an exceptional numerical condition.

## Closed-curve freedom

For the closed \((3,10)\) torus knot, comparison additionally permits:

- cyclic shifts of the sampled parameter;
- reversal of traversal direction.

This prevents an arbitrary start parameter from creating false distinctions.

## Open-curve convention

The diagnostic probe and candidate C0 are treated as open ordered curves.

Their start and end structure is preserved. Cyclic shifts and reversal are not
allowed in the main classification.

## Objects audited

The checkpoint applies the method to:

1. the asymmetric tetrahedral diagnostic probe;
2. the canonical \((3,10)\) torus knot;
3. candidate C0, the reciprocal-radius-to-poloidal-angle embedding.

## Interpretation boundary

A reduction in projection classes does not refute the broader Meru model.

It shows that additional operations would be required to obtain more distinct
letterforms, potentially including:

- continuous rather than finite orientations;
- selective tracing;
- partial or truncated views;
- multiple components;
- a tetrahelix rather than one tetrahedron;
- hand gestures;
- deformations introduced during drawing.

Those possibilities must be documented from primary sources rather than added
silently to the reconstruction.
