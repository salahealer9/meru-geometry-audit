# Primary-Source Findings — Pass 1

## Scope

This document records the first source-verification pass for the Meru geometry
audit. It distinguishes statements explicitly made in Meru Foundation sources
from mathematical inferences introduced by this project.

## F01 — The planar generator is explicitly identifiable

The 1997 essay *The First Distinction and the Most Asymmetric Spiral* identifies
the proposed planar generator as the reciprocal or hyperbolic spiral.

The equation is displayed using an inline image for theta:

\[
r\theta=1,
\]

which is equivalent to

\[
r(\theta)=\frac{1}{\theta}.
\]

The source also describes the curve as approaching the horizontal line \(y=1\)
as the radial coordinate tends to infinity. This behaviour is consistent with

\[
x(\theta)=\frac{\cos\theta}{\theta},
\qquad
y(\theta)=\frac{\sin\theta}{\theta},
\]

under the appropriate limiting direction and angular convention.

### Audit conclusion

The repository's current implementation

\[
r(\theta)=\frac{a}{\theta}
\]

is a scale-generalised mathematical implementation of the source equation.

The source does not specify a unique finite angular interval, phase, handedness,
sampling convention, or three-dimensional embedding.

## F02 — The apparent turn-count discrepancy is largely terminological

The original 1986 working paper describes:

- a full ribbon counted as \(3\frac12\) turns;
- one half of that ribbon counted as \(1\frac34\) turns.

The archival editorial note states that the same vortex was later counted as
three turns rather than \(3\frac12\) turns because the counting convention was
changed for mathematical consistency.

Later sources consequently describe the half-vortex as \(1\frac12\) turns.

### Audit conclusion

The \(1\frac34\)-turn and \(1\frac12\)-turn descriptions should not initially be
implemented as two different geometries.

They should first be treated as two historical counting conventions for the
same intended path, pending verification from the diagrams or a surviving
digital model.

## F03 — The three-dimensional embedding remains unspecified

The 1997 source says that the reciprocal spiral is drawn or projected in three
dimensions on a spherical or dimpled-sphere torus.

No explicit function is provided for a map of the form

\[
F:\mathbb{R}^{2}\rightarrow\mathbb{R}^{3}.
\]

The following remain unspecified:

- the surface equation;
- torus or dimple parameters;
- the mapping from planar spiral parameter to surface coordinates;
- start and end points;
- ribbon width;
- ribbon twist;
- scale relative to the tetrahedron.

### Audit conclusion

A three-dimensional Meru flame cannot yet be labelled a faithful mathematical
reconstruction.

Any initial embedding must be labelled a candidate reconstruction.

## F04 — The letter chart contains acknowledged fitting freedom

The First Hand source states that its letter shapes are hand-drawn tracings of
shadowgrams of one physical model.

It also acknowledges:

- minor distortions introduced for clarity;
- distortions caused by drawing limitations;
- truncated views of the model;
- simplified partial views.

### Audit conclusion

The published chart is important historical evidence, but it cannot serve as an
unmodified confirmatory target set.

A later alphabet test must separately represent:

1. the complete physical-model silhouette;
2. the traced Meru letter shape;
3. the historical Hebrew comparison forms;
4. any crop, truncation, or simplification operation.

Those transformations must be penalised or included in the null model.

## F05 — The earliest projection claim is qualitative

The 1986 source asserts that one three-dimensional vortex or ribbon, viewed
from different perspectives within a tetrahedral framework, produces a Hebrew
and Arabic alphabetic font.

The source does not provide:

- coordinates for the object;
- a complete set of rotations;
- projection matrices;
- a letter-to-orientation table;
- objective similarity thresholds.

### Audit conclusion

The existence of the claim is verified.

The claimed complete alphabet generator is not yet independently reproducible.

## F06 — First reconstructible mathematical components

At the present source boundary, the components that can be reconstructed without
substantial interpretive freedom are:

1. the planar reciprocal spiral;
2. a regular tetrahedron;
3. the proper rotational symmetry group of the regular tetrahedron;
4. ordinary orthographic projection.

The dimpled-torus flame, finite-width ribbon, and letter correspondences remain
candidate reconstructions.

## Next implementation decision

The next clean mathematical checkpoint should implement:

- a normalised regular tetrahedron;
- its 12 proper rotational symmetries;
- validation of edge lengths, centroid, orientation, and group closure;
- orthographic projection of the tetrahedron.

This can be completed independently of the unresolved Meru vortex embedding.
