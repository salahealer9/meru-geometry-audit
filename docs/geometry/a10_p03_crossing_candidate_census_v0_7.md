# A10_P03 Crossing-Candidate Census — v0.7

## Purpose

This diagnostic identifies non-adjacent visible fragments whose traced polylines intersect or approach closely enough to warrant manual source review.

It does not assign crossing identity, over-under order, or three-dimensional depth.

## Detection parameters

- Maximum polyline separation: `6.000 px`
- Minimum acute crossing angle: `12.000°`
- Adjacent fragments in the frozen v0.6 cycle are excluded.
- At most one closest approach is retained per visible segment pair in this initial census.

## Summary

- Total candidates: **33**
- Exact polyline intersections: **0**
- Near-crossing approaches: **33**

Zero exact intersections are expected because the digitisation records visible fragments and terminates around source occlusions. Genuine projected crossings therefore normally appear as short centreline gaps.

### Layer-pair counts

| Layer pair | Candidates |
|---|---:|
| `blue-green` | 12 |
| `blue-red` | 9 |
| `green-green` | 1 |
| `green-red` | 11 |

## Ranked candidates

| Rank | Candidate | Kind | Distance (px) | Angle (degrees) | Position |
|---:|---|---|---:|---:|---|
| 1 | `XING_G_S03_B_S04` | `near_crossing` | 1.476 | 71.167 | (121.44, 116.60) |
| 2 | `XING_G_S05_B_S04` | `near_crossing` | 1.503 | 68.729 | (112.02, 93.79) |
| 3 | `XING_R_S04_B_S03` | `near_crossing` | 1.749 | 14.657 | (115.49, 70.91) |
| 4 | `XING_R_S04_G_S06` | `near_crossing` | 2.011 | 45.301 | (113.10, 75.45) |
| 5 | `XING_R_S03_G_S07` | `near_crossing` | 2.088 | 25.561 | (116.96, 59.91) |
| 6 | `XING_G_S07_B_S03` | `near_crossing` | 2.108 | 77.274 | (113.30, 64.05) |
| 7 | `XING_R_S06_G_S04` | `near_crossing` | 2.303 | 78.090 | (110.13, 109.37) |
| 8 | `XING_R_S07_B_S05` | `near_crossing` | 2.303 | 81.028 | (107.08, 126.36) |
| 9 | `XING_R_S03_B_S03` | `near_crossing` | 2.330 | 41.497 | (115.75, 66.14) |
| 10 | `XING_R_S05_G_S05` | `near_crossing` | 2.427 | 52.765 | (115.06, 90.70) |
| 11 | `XING_G_S08_B_S02` | `near_crossing` | 2.456 | 84.810 | (117.45, 46.08) |
| 12 | `XING_G_S08_B_S01` | `near_crossing` | 2.481 | 44.330 | (96.71, 27.26) |
| 13 | `XING_R_S01_G_S10` | `near_crossing` | 2.496 | 32.649 | (131.30, 26.60) |
| 14 | `XING_R_S03_B_S02` | `near_crossing` | 2.728 | 73.927 | (113.31, 50.16) |
| 15 | `XING_R_S02_B_S01` | `near_crossing` | 2.730 | 29.707 | (112.42, 28.45) |
| 16 | `XING_G_S04_B_S04` | `near_crossing` | 2.822 | 71.935 | (123.52, 117.84) |
| 17 | `XING_G_S06_B_S03` | `near_crossing` | 2.996 | 48.964 | (114.94, 77.38) |
| 18 | `XING_R_S07_G_S02` | `near_crossing` | 3.038 | 31.426 | (104.00, 118.88) |
| 19 | `XING_R_S05_B_S04` | `near_crossing` | 3.245 | 28.428 | (116.72, 99.92) |
| 20 | `XING_R_S06_B_S04` | `near_crossing` | 3.411 | 76.331 | (115.86, 104.90) |
| 21 | `XING_R_S01_G_S09` | `near_crossing` | 3.534 | 23.813 | (123.63, 24.15) |
| 22 | `XING_G_S02_G_S04` | `near_crossing` | 3.580 | 88.807 | (110.78, 116.89) |
| 23 | `XING_G_S06_B_S04` | `near_crossing` | 3.690 | 61.261 | (113.45, 81.08) |
| 24 | `XING_R_S01_B_S01` | `near_crossing` | 3.711 | 20.281 | (123.52, 27.70) |
| 25 | `XING_R_S03_G_S08` | `near_crossing` | 3.724 | 59.787 | (102.53, 34.59) |
| 26 | `XING_R_S02_G_S08` | `near_crossing` | 3.774 | 64.314 | (106.62, 32.93) |
| 27 | `XING_G_S09_B_S01` | `near_crossing` | 3.887 | 18.156 | (95.91, 24.14) |
| 28 | `XING_R_S07_G_S04` | `near_crossing` | 3.950 | 69.885 | (108.12, 112.24) |
| 29 | `XING_R_S07_G_S01` | `near_crossing` | 4.096 | 84.611 | (100.51, 122.94) |
| 30 | `XING_G_S04_B_S05` | `near_crossing` | 4.341 | 70.559 | (113.95, 121.82) |
| 31 | `XING_R_S07_B_S06` | `near_crossing` | 4.455 | 87.275 | (103.22, 127.28) |
| 32 | `XING_G_S10_B_S01` | `near_crossing` | 5.373 | 14.035 | (129.44, 29.75) |
| 33 | `XING_G_S01_B_S06` | `near_crossing` | 5.548 | 19.425 | (100.19, 126.41) |

## Interpretation boundary

This is a geometric triage stage. Candidate status must be decided against the A10_P03 source panel.

False positives may include:

- nearby paths in different projected regions;
- endpoint junctions not representing crossings;
- nearly touching strands separated in depth;
- artefacts of sparse manual polyline sampling.

The next stage will generate candidate-specific source crops and a tracked manual crossing inventory.

## Generated outputs

- `figures/a10_p03_crossing_candidates.png`
- `data/derived/a10_p03_crossing_candidates.csv` (local ignored output)
