# A10_P03 Connectivity Graph — v0.6

## Inputs

- Visible traced segments: **24** coloured fragments.
- Accepted endpoint continuations: **15**.
- Reviewed confidence: **high** for all 15 connections.
- Review reason: `occlusion_supported` for all 15.

Every visible fragment is represented by an intrinsic edge between its start and end. Every accepted adjudication is represented by a second edge across the locally occluded gap.

## Layer summary

| Layer | Visible fragments | Accepted edges | Components | Free endpoints | Closed components | Branched components |
|---|---:|---:|---:|---:|---:|---:|
| Red centreline | 7 | 5 | 2 | 4 | 0 | 0 |
| Green centreline | 11 | 5 | 6 | 12 | 0 | 0 |
| Blue centreline | 6 | 5 | 1 | 2 | 0 | 0 |

## Connected components

### Red centreline

#### Component 1

- Segments: S01.
- Accepted connections: none.
- Traversal: `S01+`.
- Free endpoints: `S01S, S01E`.
- Closed: `false`.
- Branched: `false`.
- Visible traced length: 84.767 px.
- Straight-line endpoint-gap sum: 0.000 px.

#### Component 2

- Segments: S02, S03, S04, S05, S06, S07.
- Accepted connections: `R_S02E_S03S`, `R_S03E_S04E`, `R_S04S_S05S`, `R_S05E_S06E`, `R_S06S_S07S`.
- Traversal: `S02+ → S03+ → S04− → S05+ → S06− → S07+`.
- Free endpoints: `S02S, S07E`.
- Closed: `false`.
- Branched: `false`.
- Visible traced length: 163.358 px.
- Straight-line endpoint-gap sum: 36.837 px.

### Green centreline

#### Component 1

- Segments: S01.
- Accepted connections: none.
- Traversal: `S01+`.
- Free endpoints: `S01S, S01E`.
- Closed: `false`.
- Branched: `false`.
- Visible traced length: 79.517 px.
- Straight-line endpoint-gap sum: 0.000 px.

#### Component 2

- Segments: S02.
- Accepted connections: none.
- Traversal: `S02+`.
- Free endpoints: `S02S, S02E`.
- Closed: `false`.
- Branched: `false`.
- Visible traced length: 4.369 px.
- Straight-line endpoint-gap sum: 0.000 px.

#### Component 3

- Segments: S03, S04, S05, S06, S07.
- Accepted connections: `G_S03S_S04S`, `G_S04E_S05S`, `G_S05E_S06S`, `G_S06E_S07E`.
- Traversal: `S03− → S04+ → S05+ → S06+ → S07−`.
- Free endpoints: `S03E, S07S`.
- Closed: `false`.
- Branched: `false`.
- Visible traced length: 80.801 px.
- Straight-line endpoint-gap sum: 21.748 px.

#### Component 4

- Segments: S08.
- Accepted connections: none.
- Traversal: `S08+`.
- Free endpoints: `S08S, S08E`.
- Closed: `false`.
- Branched: `false`.
- Visible traced length: 36.849 px.
- Straight-line endpoint-gap sum: 0.000 px.

#### Component 5

- Segments: S09.
- Accepted connections: none.
- Traversal: `S09+`.
- Free endpoints: `S09S, S09E`.
- Closed: `false`.
- Branched: `false`.
- Visible traced length: 28.220 px.
- Straight-line endpoint-gap sum: 0.000 px.

#### Component 6

- Segments: S10, S11.
- Accepted connections: `G_S10E_S11S`.
- Traversal: `S10+ → S11+`.
- Free endpoints: `S10S, S11E`.
- Closed: `false`.
- Branched: `false`.
- Visible traced length: 50.601 px.
- Straight-line endpoint-gap sum: 4.476 px.

### Blue centreline

#### Component 1

- Segments: S01, S02, S03, S04, S05, S06.
- Accepted connections: `B_S01E_S02E`, `B_S02S_S03S`, `B_S03E_S04S`, `B_S04E_S05S`, `B_S05E_S06S`.
- Traversal: `S01+ → S02− → S03+ → S04+ → S05+ → S06+`.
- Free endpoints: `S01S, S06E`.
- Closed: `false`.
- Branched: `false`.
- Visible traced length: 322.882 px.
- Straight-line endpoint-gap sum: 33.453 px.

## Exact graph findings

- No accepted endpoint is used by more than one connection.
- No component contains a branch node.
- Every connected component is therefore an open path or an isolated visible segment.
- No colour is yet demonstrated to form a closed loop from the reviewed candidate set alone.

The blue fragments form one connected open chain. The red fragments form one six-segment chain plus one isolated segment. The green fragments remain distributed over six components.

## Minimum additional connectivity requirements

Because every present component is a non-branched path, joining \(c\) components into one open chain requires at least \(c-1\) additional endpoint pairings. Closing the result into one cycle requires at least \(c\) pairings.

| Layer | Current components | Additional edges for one chain | Additional edges for one cycle |
|---|---:|---:|---:|
| Red centreline | 2 | 1 | 2 |
| Green centreline | 6 | 5 | 6 |
| Blue centreline | 1 | 0 | 1 |

These are graph-theoretic lower bounds, not evidence that the required connections actually exist in the source.

## Interpretation boundary

The reviewed set contains only the five strongest ranked candidates per colour. An unmatched endpoint does not prove that the underlying source curve terminates there.

Further continuity may require:

- review of lower-ranked endpoint candidates;
- evidence from A10_P01 or A10_P02;
- a hidden connection outside the visible panel;
- a colour transition rather than same-colour continuation;
- clarification of the source's three-colour convention.

Accepted dashed edges are topological relations. They are not metric reconstructions of the hidden path.

## Generated outputs

- `figures/a10_p03_connectivity_graph.png`
- `data/derived/a10_p03_connectivity_components.csv` (local ignored output)
- `data/derived/a10_p03_unmatched_endpoints.csv` (local ignored output)
