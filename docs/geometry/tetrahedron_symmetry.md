# Regular Tetrahedron and Its Proper Rotational Symmetries

## Purpose

This document specifies the first fully determined three-dimensional component
of the Meru Geometry Audit.

It does not attempt to reconstruct Stan Tenen's spiral, flame, ribbon, torus,
or hand model.

## Normalised tetrahedron

The baseline tetrahedron has vertices

\[
v_0=\frac{1}{\sqrt{3}}(1,1,1),
\]

\[
v_1=\frac{1}{\sqrt{3}}(1,-1,-1),
\]

\[
v_2=\frac{1}{\sqrt{3}}(-1,1,-1),
\]

\[
v_3=\frac{1}{\sqrt{3}}(-1,-1,1).
\]

Every vertex lies on the unit sphere:

\[
\lVert v_i\rVert=1.
\]

The centroid is the origin:

\[
\frac14\sum_{i=0}^{3}v_i=0.
\]

Every edge has length

\[
\ell=\sqrt{\frac{8}{3}}.
\]

The volume is

\[
V=\frac{8}{9\sqrt{3}}.
\]

## Rotational symmetry group

The orientation-preserving symmetry group of a regular tetrahedron contains
12 rotations.

It is isomorphic to the alternating group

\[
A_4.
\]

Each proper rotation induces an even permutation of the four vertices.

For a vertex permutation \(\sigma\), the corresponding rotation matrix
\(R_\sigma\) satisfies

\[
R_\sigma v_i=v_{\sigma(i)}.
\]

The implementation constructs candidate matrices from all 24 vertex
permutations and retains only matrices satisfying

\[
R^\mathsf{T}R=I
\]

and

\[
\det R=+1.
\]

The resulting set must:

- contain exactly 12 matrices;
- include the identity;
- map the tetrahedron onto itself;
- be closed under matrix multiplication;
- contain only proper orthogonal matrices.

## Rotation convention

Points are represented as row vectors in arrays of shape \((n,3)\).

An active rotation is applied as

\[
X' = XR^\mathsf{T}.
\]

Equivalently, for an individual column vector,

\[
x'=Rx.
\]

## Orthographic projection

After rotation, the default orthographic projection discards the \(z\)
coordinate:

\[
P(x,y,z)=(x,y).
\]

Thus the projection of a rotated object is

\[
P(Rx).
\]

Later Meru-model experiments will apply the same 12 rotations to an asymmetric
three-dimensional object. Unlike the tetrahedron itself, an asymmetric object
can yield distinct silhouettes under these orientations.

## Evidence boundary

The regular tetrahedron and its symmetry group are mathematically exact.

Their implementation does not establish that:

- Tenen used precisely this coordinate orientation;
- all claimed letters arise only from these 12 rotations;
- the Meru object was centred or scaled in this manner;
- the relevant historical projection was orthographic.

Those questions remain part of the source and reconstruction audit.
