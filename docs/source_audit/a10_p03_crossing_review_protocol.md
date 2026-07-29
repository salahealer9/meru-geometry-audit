# A10_P03 Crossing Review Protocol

## Purpose

Review the 33 candidates in the frozen `6 px / 12°` geometric census and
construct a source-derived inventory of distinct crossing events.

## Candidate versus event

A geometric candidate is a pair of visible fragments.

A physical crossing event is one location in the source drawing.

Several candidate rows may describe the same physical event because the source
curve was digitised as separate visible fragments around occlusions.

Each confirmed crossing must therefore receive a stable event identifier:

- `E01`
- `E02`
- `E03`
- and so forth.

Only one row should serve as the primary record for a physical crossing.
Additional rows representing that event should use:

- status: `duplicate_candidate`;
- the same `event_id`;
- reason: `duplicate_event`.

## Status values

### crossing

The source supports a genuine projected crossing between the two candidate
segments.

A crossing record must identify:

- `event_id`;
- over-strand;
- under-strand;
- visibility;
- confidence;
- reason code;
- evidence note.

### continuation_junction

The candidate describes an already established same-colour continuation or
cross-colour transition rather than a crossing.

### different_feature

The segments are close in the image but belong to different projected regions
or do not meet.

### duplicate_candidate

The row describes a crossing already represented by another primary record.

### ambiguous

The source does not permit a reliable crossing or depth decision.

### unreviewed

No manual decision has been recorded.

## Visibility values

- `visible`: over-under order is directly readable;
- `partial`: only part of the crossing structure is visible;
- `occluded`: the crossing is inferred across a source gap;
- `unclear`: the source does not resolve visibility.

## Reason codes

- `source_crossing`
- `continuation_or_transition`
- `different_projected_region`
- `duplicate_event`
- `insufficient_resolution`
- `other`

## Review procedure

For each candidate:

1. inspect the raw source close-up;
2. inspect the trace-overlay close-up;
3. determine whether the two segments meet at one physical event;
4. distinguish a crossing from a continuation or colour-transition junction;
5. assign over-under order only when supported by the source;
6. assign or reuse an `event_id`;
7. mark duplicate candidate rows explicitly;
8. prefer `ambiguous` when depth ordering cannot be read reliably.

## Interpretation boundary

A reviewed planar crossing inventory supplies the combinatorial input needed
for Gauss-code and knot-type analysis.

It does not itself establish a unique three-dimensional embedding.
