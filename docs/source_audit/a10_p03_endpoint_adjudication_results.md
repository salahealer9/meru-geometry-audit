# A10_P03 Endpoint Adjudication Results

## Review set

The manually reviewed set contains the five highest-ranked same-colour endpoint
candidates for each of the three source colours:

- red: 5;
- green: 5;
- blue: 5;
- total: 15.

## Outcome

| Status | Count |
|---|---:|
| Accepted | 15 |
| Rejected | 0 |
| Ambiguous | 0 |
| Unreviewed | 0 |

All accepted candidates were assigned:

- confidence: `high`;
- reason code: `occlusion_supported`.

## Review basis

Each candidate was inspected against both:

1. the complete A10_P03 source panel;
2. a magnified candidate-specific crop.

In every reviewed case, the same-colour fragments were judged to continue
across a locally occluding feature. The intervening feature was one of:

- another coloured centreline;
- the black dimple-boundary drawing.

The decisions were made from visible source evidence rather than endpoint
distance or tangent score alone.

## Accepted red continuations

| Candidate | Occluding feature |
|---|---|
| `R_S03E_S04E` | Blue centreline |
| `R_S06S_S07S` | Green centreline |
| `R_S05E_S06E` | Blue centreline |
| `R_S02E_S03S` | Green centreline |
| `R_S04S_S05S` | Green centreline |

## Accepted green continuations

| Candidate | Occluding feature |
|---|---|
| `G_S03S_S04S` | Blue centreline |
| `G_S10E_S11S` | Black upper-right dimple boundary |
| `G_S06E_S07E` | Blue centreline |
| `G_S04E_S05S` | Blue centreline |
| `G_S05E_S06S` | Red centreline |

## Accepted blue continuations

| Candidate | Occluding feature |
|---|---|
| `B_S01E_S02E` | Green centreline |
| `B_S02S_S03S` | Red centreline |
| `B_S03E_S04S` | Green centreline |
| `B_S05E_S06S` | Red centreline |
| `B_S04E_S05S` | Green centreline |

## Interpretation boundary

Acceptance establishes a source-supported local two-dimensional continuation.

It does not by itself establish:

- exact hidden geometry between the endpoints;
- over/under topology at every crossing;
- the depth of either strand;
- a unique three-dimensional embedding;
- equivalence with a canonical torus knot.

The accepted edges may now be used to construct a source-derived fragment
connectivity graph. Hidden interpolation remains separate from the observed
polyline data.
