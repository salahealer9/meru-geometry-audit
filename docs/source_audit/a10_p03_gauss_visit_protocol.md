# A10_P03 Gauss-Visit Protocol

## Objective

Order the two visits to every confirmed A10_P03 crossing along the frozen
global cycle.

The completed crossing inventory contains 31 distinct events. A complete
O/U Gauss sequence therefore requires 62 visits.

## Frozen path

The segment order and direction are inherited from the v0.6 global-cycle
audit. The topology and traversal direction are not re-optimized.

## Local crossing position

For each side of a crossing, the candidate table records:

- visible segment;
- polyline piece index;
- fraction along that piece.

The location is converted to normalized arc length along the complete visible
polyline.

For a forward traversal:

\[
s_{\mathrm{traversal}}=s_{\mathrm{source}}.
\]

For a reverse traversal:

\[
s_{\mathrm{traversal}}=1-s_{\mathrm{source}}.
\]

## O/U visit labels

Every event must appear exactly twice:

- once with `O`, where the traversed strand is the reviewed over-strand;
- once with `U`, where the traversed strand is the reviewed under-strand.

## Ordering ties

Two visits can receive the same derived position when the digitization places
both at one visible-fragment endpoint.

Such visits must not be placed into an arbitrary scientific order.

The provisional sequence displays an unresolved group with braces:

```text
{E21O|E24U}
````

The ordering within braces is deterministic display order only.

## Close-order review

In addition to exact ties, consecutive visits separated by at most 0.03 of
their visible segment's normalized arc length are placed into a visual review
set.

The close-order review does not imply that the derived order is wrong. It
provides a source check before the canonical sequence is frozen.

## Current boundary

This stage derives an O/U visit sequence.

Crossing signs require a separate oriented-tangent convention and are not
assigned here. Consequently, this stage does not yet produce a signed Gauss
code, Dowker–Thistlethwaite code, or knot invariant.
