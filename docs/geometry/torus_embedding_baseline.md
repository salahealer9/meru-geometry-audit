# Canonical Torus and Candidate Reciprocal-Spiral Embedding

## Purpose

This checkpoint introduces the canonical ring torus and the standard
parametrisation of a coprime \((p,q)\) torus knot.

It also introduces one explicitly labelled candidate mapping of the reciprocal
spiral onto the torus.

The canonical torus and torus-knot equations are exact mathematical baselines.
The reciprocal-spiral embedding is not claimed to reproduce Stan Tenen's exact
three-dimensional construction.

## Canonical ring torus

Let

\[
R>r>0,
\]

where \(R\) is the major radius and \(r\) is the minor radius.

The standard torus parametrisation is

\[
T(u,v)=
\begin{pmatrix}
(R+r\cos v)\cos u\\
(R+r\cos v)\sin u\\
r\sin v
\end{pmatrix}.
\]

Every point satisfies the implicit torus equation

\[
\left(\sqrt{x^2+y^2}-R\right)^2+z^2=r^2.
\]

This checkpoint restricts attention to a ring torus with \(R>r\). Horn,
spindle, and self-intersecting variants are not included.

## Coprime \((p,q)\) torus knot

For positive coprime integers \(p\) and \(q\), define

\[
\gamma_{p,q}(t)=T(pt+\phi_u,qt+\phi_v),
\qquad
0\leq t\leq 2\pi.
\]

Explicitly,

\[
x(t)=
\left(R+r\cos(qt+\phi_v)\right)
\cos(pt+\phi_u),
\]

\[
y(t)=
\left(R+r\cos(qt+\phi_v)\right)
\sin(pt+\phi_u),
\]

\[
z(t)=r\sin(qt+\phi_v).
\]

The Meru source describes a \((3,10)\) construction. The baseline implementation
therefore includes

\[
\gamma_{3,10}(t).
\]

Because

\[
\gcd(3,10)=1,
\]

the parametrised curve is a single closed torus knot rather than a
multi-component torus link.

The notation convention used here assigns:

- \(p\) to revolutions around the torus axis;
- \(q\) to revolutions around the tube.

The source audit must verify whether Meru uses the same ordering convention.

## Candidate reciprocal-spiral embedding

The planar source curve is

\[
\rho(\theta)=\frac{a}{\theta},
\qquad
\theta>0.
\]

For a selected starting angle \(\theta_0\) and toroidal turn count \(N_u\), let

\[
\theta_1=\theta_0+2\pi N_u.
\]

The candidate toroidal longitude is

\[
u(\theta)=\phi_u+\theta-\theta_0.
\]

Thus the toroidal longitude advances by exactly

\[
u(\theta_1)-u(\theta_0)=2\pi N_u.
\]

The reciprocal radius is normalised to a monotone progress variable

\[
s_\rho(\theta)=
\frac{\rho(\theta_0)-\rho(\theta)}
{\rho(\theta_0)-\rho(\theta_1)}.
\]

This satisfies

\[
s_\rho(\theta_0)=0,
\qquad
s_\rho(\theta_1)=1.
\]

The candidate poloidal angle is

\[
v(\theta)=\phi_v+2\pi N_v s_\rho(\theta),
\]

where \(N_v\) is a selected poloidal turn count.

The resulting candidate curve is

\[
C(\theta)=T\bigl(u(\theta),v(\theta)\bigr).
\]

## Why this is only a candidate

This mapping makes the reconstruction choices explicit, but the Meru sources
located so far do not uniquely specify:

- the torus surface equation;
- the major-to-minor radius ratio;
- the correspondence between reciprocal radius and toroidal latitude;
- the start angle;
- the number of poloidal turns;
- the phase;
- the handedness;
- whether the path lies on the surface or passes through the volume;
- whether the intended surface is a canonical or dimpled torus.

Accordingly, this model is labelled:

> Candidate C0 — reciprocal-radius-to-poloidal-angle embedding.

It is a reproducible hypothesis generator, not a faithful Meru reconstruction.

## Tetrahedral projections

Both the \((3,10)\) torus knot and the candidate reciprocal curve can be acted
upon by the 12 proper rotations of the tetrahedron.

For each rotation \(R_i\), the controlled orthographic projection is

\[
P_i(\gamma)=P(R_i\gamma),
\qquad
i=1,\ldots,12.
\]

These projections establish the computational pipeline needed for later
silhouette and letter-shape experiments.

## Evidence boundary

The implementation of the canonical torus does not establish that Tenen's
apple-like form is a standard torus.

The implementation of the \((3,10)\) knot establishes only the mathematical
content of that knot designation under the stated convention.

The candidate reciprocal embedding does not establish historical fidelity,
alphabetic significance, intentional encoding, or extraterrestrial origin.
