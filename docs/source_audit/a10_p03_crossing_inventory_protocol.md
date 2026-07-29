# A10_P03 Crossing Inventory Protocol

## Objective

Construct a source-derived inventory of crossings in the completed A10_P03
drawing after freezing its planar cycle connectivity.

## Phase A — geometric candidate census

The census compares every pair of visible centreline fragments except pairs
adjacent in the frozen v0.6 global cycle.

A pair is retained when:

- its minimum traced-polyline separation is at most the selected pixel
  threshold; and
- its acute local crossing angle exceeds the selected angular threshold.

The census is diagnostic only.

## Frozen v0.7 core threshold

The primary candidate set uses:

- maximum separation: `6 px`;
- minimum acute crossing angle: `12°`.

This produces 33 core candidates.

Sensitivity checks produced:

| Threshold | Candidates |
|---|---:|
| `6 px / 12°` | 33 |
| `10 px / 12°` | 43 |
| `14 px / 10°` | 49 |

The 10 additional candidates between 6 and 10 pixels are retained conceptually
as an extended sensitivity set. They will be reviewed later if the core census
does not recover a complete crossing inventory.

## Why exact intersections are not expected

The manual digitisation records visible centreline fragments. At an occlusion,
the trace normally terminates on one side and resumes on the other.

A genuine projected crossing therefore appears in the digitised data as a
short gap between non-adjacent fragments rather than as two polylines that
mathematically intersect.

## Phase B — source adjudication

Every retained candidate will be reviewed against A10_P03 and labelled as:

- a genuine crossing;
- an ordinary continuation or colour-transition junction;
- different projected features;
- ambiguous from the source.

For a genuine crossing, the review will record:

- crossing coordinate;
- participating cycle segments;
- over-strand;
- under-strand;
- confidence;
- visibility or occlusion type;
- evidence note.

## Evidence priority

1. A10_P03 is the primary evidence.
2. The digitised centrelines locate and identify the fragments.
3. A10_P01 and A10_P02 may provide transformation context.
4. Geometric distance and angle do not determine crossing identity or depth.

## Current limitation

The initial detector retains only the closest approach for each pair of
visible fragments. Multiple crossings between the same fragment pair require
a later multi-event detector or manual addition.

## Interpretation boundary

A complete planar crossing inventory is necessary for knot-type analysis, but
it does not itself establish a unique three-dimensional embedding.
