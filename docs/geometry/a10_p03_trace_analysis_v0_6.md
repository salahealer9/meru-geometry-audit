# A10_P03 Trace Analysis — v0.6

## Dataset

- Panel: `A10_P03`
- Last digitisation update: `2026-07-26T16:16:51+00:00`
- Total traced points: **303**
- Non-empty visible segments: **32**

All measurements below describe the two-dimensional source drawing.

## Layer geometry

| Layer | Segments | Points | Total visible length (px) | Mean segment tortuosity |
|---|---:|---:|---:|---:|
| Outer boundary | 1 | 40 | 415.524 | — |
| Dimple boundary | 7 | 56 | 245.728 | 1.0564 |
| Red centreline | 7 | 57 | 248.125 | 1.1853 |
| Green centreline | 11 | 83 | 280.357 | 1.1218 |
| Blue centreline | 6 | 67 | 322.882 | 1.2136 |

Visible centreline and dimple lengths do not include hidden or occluded continuations. The outer-boundary perimeter includes the closing edge from the final point to the initial point.

## Boundary diagnostics

### Outer boundary

| Centre x | Centre y | Semi-major | Semi-minor | Axis ratio | Angle (degrees) | Radial RMS |
|---:|---:|---:|---:|---:|---:|---:|
| 114.251 | 80.132 | 67.415 | 64.793 | 1.0405 | -179.470 | 0.01165 |

The outer boundary is well described by a near-circular ellipse.

### Dimple boundary

The visible dimple trace is not a closed ellipse. It forms a fragmented bilateral neck or hourglass profile interrupted by occlusions. A free ellipse fit is therefore structurally inappropriate and has not been reported.

The dimple will be analysed later as left and right neck profiles relative to the outer-boundary symmetry axis.

## Endpoint reconnection candidates

The following are the five strongest same-colour candidates under distance plus tangent-continuity ranking.

### Red centreline

| Rank | Endpoint A | Endpoint B | Distance (px) | Tangent mismatch (degrees) | Score |
|---:|---|---|---:|---:|---:|
| 1 | S3 end | S4 end | 5.846 | 11.739 | 6.227 |
| 2 | S6 start | S7 start | 6.455 | 4.102 | 6.602 |
| 3 | S5 end | S6 end | 7.676 | 24.289 | 8.712 |
| 4 | S2 end | S3 start | 7.731 | 37.895 | 9.359 |
| 5 | S4 start | S5 start | 9.129 | 10.698 | 9.671 |

### Green centreline

| Rank | Endpoint A | Endpoint B | Distance (px) | Tangent mismatch (degrees) | Score |
|---:|---|---|---:|---:|---:|
| 1 | S3 start | S4 start | 4.476 | 6.899 | 4.647 |
| 2 | S10 end | S11 start | 4.476 | 12.809 | 4.794 |
| 3 | S6 end | S7 end | 5.251 | 4.075 | 5.370 |
| 4 | S4 end | S5 start | 5.989 | 15.648 | 6.510 |
| 5 | S5 end | S6 start | 6.032 | 25.010 | 6.870 |

### Blue centreline

| Rank | Endpoint A | Endpoint B | Distance (px) | Tangent mismatch (degrees) | Score |
|---:|---|---|---:|---:|---:|
| 1 | S1 end | S2 end | 5.375 | 4.102 | 5.498 |
| 2 | S2 start | S3 start | 6.455 | 16.845 | 7.059 |
| 3 | S3 end | S4 start | 6.951 | 15.265 | 7.540 |
| 4 | S5 end | S6 start | 7.089 | 14.528 | 7.661 |
| 5 | S4 end | S5 start | 7.583 | 12.222 | 8.098 |

## Interpretation boundary

Endpoint rankings are diagnostic hypotheses only. No fragments have been joined automatically.

The trace does not yet establish:

- hidden strand continuity;
- over/under crossing order;
- a three-dimensional knot embedding;
- the source camera model;
- a dimpled-sphere surface equation;
- equivalence with the canonical (3,10) torus knot.

## Generated outputs

- `figures/a10_p03_normalized_trace.png`
- `figures/a10_p03_boundary_fits.png`
- `figures/a10_p03_endpoint_candidates.png`
- `data/derived/a10_p03_segment_metrics.csv` (local ignored output)
- `data/derived/a10_p03_endpoint_candidates.csv` (local ignored output)
