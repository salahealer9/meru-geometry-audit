# A10_P03 Residual Endpoint Review Protocol

## Purpose

This second-stage review considers only endpoints that remain free after the
15 accepted first-stage occlusion continuations.

No endpoint already used by an accepted connection is eligible.

## Frozen review set

The review set contains 20 candidates:

- red: all 4 inter-component endpoint pairings;
- green: the best-scoring endpoint pairing for each of the 15 unordered pairs
  among the 6 current green components;
- blue: the single pairing that would close its present open chain.

## Candidate types

### merge

A proposed connection between two currently separate components.

### close

A proposed connection between the two free endpoints of one open component.

## Evidence panels

Every candidate image contains:

1. the full A10_P03 source panel;
2. a magnified A10_P03 close-up;
3. A10_P01, showing the ring-to-dimple transition;
4. A10_P02, showing the stated apparent winding-zero flip.

A10_P01 and A10_P02 provide historical context but are not registered to the
A10_P03 pixel coordinate system.

## Decision values

- `accepted`
- `rejected`
- `ambiguous`
- `unreviewed`

Use the same confidence and reason-code vocabulary as the first adjudication.

## Review rule

Distance and tangent score only determine which hypotheses are inspected.

A candidate must be accepted or rejected from visible source evidence. Where
the source does not distinguish competing continuations, use `ambiguous`.

## Outputs

Tracked table:

- `data/manual_digitizations/A10_P03/residual_endpoint_review.csv`

Ignored local review images:

- `data/derived/source_inspection/residual_endpoint_review/A10_P03/`
- `data/derived/source_inspection/residual_endpoint_review/a10_p03_residual_endpoint_review_sheet.png`
