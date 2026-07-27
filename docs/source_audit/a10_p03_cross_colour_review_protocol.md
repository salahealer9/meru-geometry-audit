# A10_P03 Cross-Colour Endpoint Review Protocol

## Purpose

The current source-derived graph contains three non-branched open chains:

- one red chain;
- one green chain;
- one blue chain.

Each chain has exactly two free endpoints.

This review tests whether the chains join through colour transitions at the
remaining source intersections.

## Candidate set

With two free endpoints per colour, there are:

- 4 red-green candidates;
- 4 red-blue candidates;
- 4 green-blue candidates;
- 12 cross-colour candidates in total.

Same-colour pairings are excluded because they were reviewed during the
residual same-colour stage.

## Complete matching hypotheses

A complete matching uses all six endpoints exactly once.

There are eight complete cross-colour matchings. Each contains:

- one red-green edge;
- one red-blue edge;
- one green-blue edge.

If all three edges of one matching are source-supported, the three open colour
chains form one closed cycle.

## Decision rules

Use:

- `accepted` where the source supports continuation through a colour change;
- `rejected` where the endpoints represent different intersections, regions,
  or incompatible directions;
- `ambiguous` where the source cannot distinguish the alternatives.

Recommended reason codes include:

- `colour_transition_supported`;
- `colour_transition_conflict`;
- `colour_intersection`;
- `different_feature`;
- `crossing_conflict`;
- `insufficient_resolution`.

## Evidence priority

1. A10_P03 is the primary source.
2. A10_P01 and A10_P02 provide transformation context.
3. Distance and tangent score are ranking diagnostics only.

A candidate must not be accepted merely because its endpoints are close.

## Interpretation boundary

A successful three-edge matching would establish a source-supported
two-dimensional colour-transition cycle.

It would not establish:

- exact hidden path geometry;
- over-under depth at every crossing;
- a unique dimpled-surface embedding;
- equivalence with the canonical (3,10) knot.
