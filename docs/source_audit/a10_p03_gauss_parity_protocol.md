# A10_P03 Gauss-Parity Protocol

## Objective

Test the frozen A10_P03 Gauss word against the necessary even condition for a
classical one-component planar knot diagram.

## Input boundary

The audit reads the frozen source-reviewed O/U Gauss word and verifies that
the signed snapshot uses the same unsigned visit order.

It does not modify either snapshot.

## Even condition

For each crossing event with visits at positions \(i<j\), define

\[
N_{\mathrm{between}}=j-i-1.
\]

A necessary condition for classical planar realizability is

\[
N_{\mathrm{between}}\equiv0\pmod 2.
\]

Equivalently:

- \(i\) and \(j\) have opposite parity;
- the crossing chord has even degree in the interlacement graph.

All three diagnostics are computed independently and required to agree.

## Invariance

The event-level pass or failure is unchanged by:

- cyclically rotating the starting point of the Gauss word;
- reversing the orientation of the complete traversal;
- exchanging the labels `O` and `U`.

The condition depends on event ordering, not crossing sign.

## Interpretation boundary

Passing the even condition is necessary but not sufficient for a classical
Gauss word to be realizable by a planar immersed circle.

Failure prevents direct classical Dowker conversion and requires the
reconstruction assumptions to be revisited computationally.
