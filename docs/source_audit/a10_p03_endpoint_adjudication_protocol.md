# A10_P03 Endpoint Adjudication Protocol

## Purpose

This protocol reviews possible continuations between visible same-colour
fragments in source panel A10_P03.

No candidate is accepted from distance or tangent agreement alone.

## Candidate set

The review set contains the five highest-ranked candidates for each colour:

- five red candidates;
- five green candidates;
- five blue candidates.

The ranking combines:

- endpoint distance;
- local tangent-continuity mismatch.

## Status values

### accepted

The source image supports the interpretation that the two endpoints are parts
of the same visible or directly occluded strand.

### rejected

The source image supports a different interpretation, such as:

- different strands;
- incompatible crossing structure;
- continuation in another direction;
- misleading proximity.

### ambiguous

The source resolution, overlap, or occlusion does not permit a reliable
decision.

### unreviewed

No manual decision has yet been recorded.

## Confidence values

- `high`
- `medium`
- `low`

Confidence measures the clarity of the source evidence, not the attractiveness
of the geometric connection.

## Reason codes

- `clear_continuation`
- `occlusion_supported`
- `crossing_conflict`
- `tangent_conflict`
- `different_feature`
- `insufficient_resolution`
- `other`

## Review rules

1. Inspect both the full panel and close-up.
2. Follow the source-coloured stroke rather than the dashed candidate line.
3. Check whether another visible strand occupies the proposed gap.
4. Do not infer continuity merely because endpoints are close.
5. Prefer `ambiguous` when depth ordering cannot be recovered.
6. Record a short note for every accepted or rejected candidate.
7. Do not alter the underlying digitisation during adjudication.

## Outputs

Tracked decision table:

- `data/manual_digitizations/A10_P03/endpoint_adjudication.csv`

Ignored local review images:

- `data/derived/source_inspection/endpoint_review/A10_P03/`
- `data/derived/source_inspection/endpoint_review/a10_p03_endpoint_review_sheet.png`
