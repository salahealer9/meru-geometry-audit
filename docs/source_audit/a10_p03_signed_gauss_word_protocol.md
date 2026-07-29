# A10_P03 Signed Gauss-Word Protocol

## Objective

Combine the frozen O/U Gauss word with the accepted oriented sign of every
A10_P03 crossing event.

## Inputs

The finalization uses:

- the source-reviewed 62-visit O/U Gauss word;
- the frozen 24-segment traversal;
- the 31 reviewed over-under assignments;
- tangent-derived crossing signs;
- the four accepted low-angle sign reviews.

## Project notation

A signed visit token has the ASCII form:

```text
E<event><role><sign>
````

where:

* `O` is an over-strand visit;
* `U` is an under-strand visit;
* `+` is a positive oriented crossing;
* `-` is a negative oriented crossing.

Example:

```text
E13O-
```

means the over-strand visit to negative crossing event E13.

This token format is an explicit project convention. It avoids relying on an
unstated external Gauss-code notation.

## Required invariants

The frozen sequence must contain:

* 31 distinct crossing events;
* 62 ordered visits;
* exactly one `O` and one `U` visit per event;
* one common sign on both visits to each event;
* no degenerate signs;
* no unresolved ordering decisions;
* no unresolved sign decisions.

## Sign basis

The low-angle events `E03`, `E21`, `E24` and `E27` use the basis:

```text
manual_low_angle_review
```

All other events use:

```text
derived_stable_all_spans
```

Every event must retain the same sign across tangent spans of 2, 4, 6, 8, 10
and 12 pixels.

## Snapshot control

The canonical snapshot is written only with:

```text
--update-snapshot
```

Normal execution recomputes the signed word and rejects any difference from
the tracked snapshot or its SHA-256 digest.

## Interpretation boundary

The signed O/U Gauss word characterizes the reconstructed planar diagram
under the documented coordinate, orientation and sign conventions.

It does not itself establish a canonical knot name, minimal crossing number,
polynomial invariant, or unique three-dimensional embedding.
