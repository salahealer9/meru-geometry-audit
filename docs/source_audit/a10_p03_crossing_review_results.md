# A10_P03 Crossing Review Results

## Completed review

All 33 candidates in the frozen `6 px / 12°` geometric census have been manually reviewed against the A10_P03 source panel.

| Status | Count |
|---|---:|
| Crossing | 31 |
| Different feature | 2 |
| Continuation junction | 0 |
| Duplicate candidate | 0 |
| Ambiguous | 0 |
| Unreviewed | 0 |

The result is:

- **31 distinct visible crossing events**;
- **2 non-crossing parallel approaches**;
- no duplicate candidate events;
- no ambiguous crossing assignments;
- high confidence for every decision;
- visible over-under order for every confirmed crossing.

## Crossing events

| Event | Candidate | Over-strand | Under-strand | Position |
|---|---|---|---|---|
| `E01` | `XING_G_S03_B_S04` | Blue S04 | Green S03 | (121.44, 116.60) |
| `E02` | `XING_G_S05_B_S04` | Blue S04 | Green S05 | (112.02, 93.79) |
| `E03` | `XING_R_S04_B_S03` | Blue S03 | Red S04 | (115.49, 70.91) |
| `E04` | `XING_R_S04_G_S06` | Green S06 | Red S04 | (113.10, 75.45) |
| `E05` | `XING_R_S03_G_S07` | Red S03 | Green S07 | (116.96, 59.91) |
| `E06` | `XING_G_S07_B_S03` | Blue S03 | Green S07 | (113.30, 64.05) |
| `E07` | `XING_R_S06_G_S04` | Green S04 | Red S06 | (110.13, 109.37) |
| `E08` | `XING_R_S07_B_S05` | Red S07 | Blue S05 | (107.08, 126.36) |
| `E09` | `XING_R_S03_B_S03` | Blue S03 | Red S03 | (115.75, 66.14) |
| `E10` | `XING_R_S05_G_S05` | Red S05 | Green S05 | (115.06, 90.70) |
| `E11` | `XING_G_S08_B_S02` | Green S08 | Blue S02 | (117.45, 46.08) |
| `E12` | `XING_G_S08_B_S01` | Blue S01 | Green S08 | (96.71, 27.26) |
| `E13` | `XING_R_S01_G_S10` | Red S01 | Green S10 | (131.30, 26.60) |
| `E14` | `XING_R_S03_B_S02` | Red S03 | Blue S02 | (113.31, 50.16) |
| `E15` | `XING_R_S02_B_S01` | Blue S01 | Red S02 | (112.42, 28.45) |
| `E16` | `XING_G_S04_B_S04` | Blue S04 | Green S04 | (123.52, 117.84) |
| `E17` | `XING_G_S06_B_S03` | Green S06 | Blue S03 | (114.94, 77.38) |
| `E18` | `XING_R_S07_G_S02` | Red S07 | Green S02 | (104.00, 118.88) |
| `E19` | `XING_R_S05_B_S04` | Blue S04 | Red S05 | (116.72, 99.92) |
| `E20` | `XING_R_S06_B_S04` | Blue S04 | Red S06 | (115.86, 104.90) |
| `E21` | `XING_R_S01_G_S09` | Red S01 | Green S09 | (123.63, 24.15) |
| `E22` | `XING_G_S02_G_S04` | Green S04 | Green S02 | (110.78, 116.89) |
| `E23` | `XING_G_S06_B_S04` | Green S06 | Blue S04 | (113.45, 81.08) |
| `E24` | `XING_R_S01_B_S01` | Blue S01 | Red S01 | (123.52, 27.70) |
| `E25` | `XING_R_S03_G_S08` | Green S08 | Red S03 | (102.53, 34.59) |
| `E26` | `XING_R_S02_G_S08` | Green S08 | Red S02 | (106.62, 32.93) |
| `E27` | `XING_G_S09_B_S01` | Blue S01 | Green S09 | (95.91, 24.14) |
| `E28` | `XING_R_S07_G_S04` | Green S04 | Red S07 | (108.12, 112.24) |
| `E29` | `XING_R_S07_G_S01` | Red S07 | Green S01 | (100.51, 122.94) |
| `E30` | `XING_G_S04_B_S05` | Green S04 | Blue S05 | (113.95, 121.82) |
| `E31` | `XING_R_S07_B_S06` | Red S07 | Blue S06 | (103.22, 127.28) |

## Layer-pair summary

| Strand pair | Crossings |
|---|---:|
| `blue–green` | 10 |
| `blue–red` | 9 |
| `green–green` | 1 |
| `green–red` | 11 |

## Over-under summary

| Layer | Times over | Times under |
|---|---:|---:|
| Red | 9 | 11 |
| Green | 10 | 13 |
| Blue | 12 | 7 |

## Same-colour crossing

- `E22`: Green S04 passes over Green S02.

## Rejected geometric candidates

| Candidate | Reason |
|---|---|
| `XING_G_S10_B_S01` | The green and blue traces run locally parallel and do not form a crossing. |
| `XING_G_S01_B_S06` | The green and blue traces run locally parallel and do not form a crossing. |

## Interpretation boundary

The inventory establishes a source-supported planar crossing diagram with explicit over-under information at 31 events.

It does not yet establish:

- a canonical Gauss code;
- a Dowker–Thistlethwaite code;
- a knot polynomial;
- equivalence with the canonical `(3,10)` torus knot;
- a unique three-dimensional embedding.

The next step is to order the two visits to every crossing along the frozen global-cycle traversal and derive a validated Gauss word.
