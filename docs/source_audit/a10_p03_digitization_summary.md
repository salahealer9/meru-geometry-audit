# A10_P03 Digitisation Summary

## Source panel

- Panel: A10_P03
- Source asset: A10
- Description: Complete (3,10) knot on a dimpled sphere
- Last updated: 2026-07-26T16:16:51+00:00
- Coordinate system: source-image pixel coordinates
- Reconstruction status: two-dimensional manual tracing only

## Digitised layers

| Layer | Non-empty segments | Points | Segment point counts |
|---|---:|---:|---|
| Red centreline | 7 | 57 | `[13, 3, 11, 3, 6, 3, 18]` |
| Green centreline | 11 | 83 | `[16, 3, 3, 14, 3, 7, 3, 12, 8, 3, 11]` |
| Blue centreline | 6 | 67 | `[21, 3, 9, 11, 3, 20]` |
| Outer boundary | 1 | 40 | `[40]` |
| Dimple boundary | 7 | 56 | `[3, 16, 7, 3, 3, 4, 20]` |
| Winding landmarks | 0 | 0 | `[0]` |
| **Total** | **32** | **303** | |

The winding-landmark layer retains one empty structural placeholder but contains
no digitised landmark points.

## Segmentation policy

Separate segments were used wherever:

- a coloured path was occluded;
- a crossing was ambiguous;
- a curve disappeared and later reappeared;
- the source image did not justify an interpolated connection.

All non-empty traced segments contain at least three points. No hidden path was
invented between disconnected visible fragments.

## Interpretation boundary

The digitisation represents visible two-dimensional source geometry only.

It does not establish:

- depth ordering at every crossing;
- a camera model;
- a three-dimensional surface equation;
- hidden continuations of occluded strands;
- metric precision beyond the source-image resolution.

## Review status

The coordinate overlay was visually reviewed against the source panel before
commit. The final reviewed dataset contains 303 points across
32 non-empty visible segments.
