# A10_P03 Full Endpoint-Matching Search — v0.7

## Purpose

Enumerate all provisional perfect matchings in the combined same-colour and cross-colour endpoint-candidate graph.

The search preserves:

- all 24 digitized visible fragments;
- all 31 reviewed crossing identities;
- all reviewed over-under assignments;
- all source-derived crossing locations;
- the manually resolved exact visit-order tie.

The frozen Gauss snapshots are not modified.

## Search boundary

Rejected endpoint rows are included as hypothetical graph alternatives. They are not treated as evidentially equivalent to accepted rows.

Several rejected rows carry substantive reasons such as `different_feature`, `colour_intersection`, `crossing_conflict`, or `colour_transition_conflict`.

## Search-space census

- Endpoint nodes: **48**
- Candidate edges: **47**
- Perfect matchings: **28**
- Single-cycle matchings: **16**
- Distinct parity syndromes: **4**

## Result

- Frozen-baseline violations: **16**
- Minimum violations: **16**
- Candidates attaining the minimum: **8**
- Zero-violation candidates: **0**

## Exhaustive table

| Rank | Matching | Baseline | Accepted edges | Changed edges | Components | Single cycle | Violations | Even pass |
|---:|---|---|---:|---:|---:|---|---:|---|
| 1 | `M01` | yes | 24 | 0 | 1 | yes | 16 | no |
| 2 | `M03` | no | 22 | 2 | 1 | yes | 16 | no |
| 3 | `M08` | no | 22 | 2 | 1 | yes | 16 | no |
| 4 | `M18` | no | 22 | 2 | 1 | yes | 16 | no |
| 5 | `M10` | no | 21 | 3 | 1 | yes | 16 | no |
| 6 | `M11` | no | 21 | 3 | 1 | yes | 16 | no |
| 7 | `M14` | no | 21 | 3 | 1 | yes | 16 | no |
| 8 | `M16` | no | 21 | 3 | 1 | yes | 16 | no |
| 9 | `M06` | no | 20 | 4 | 1 | yes | 18 | no |
| 10 | `M19` | no | 19 | 5 | 1 | yes | 18 | no |
| 11 | `M20` | no | 19 | 5 | 1 | yes | 18 | no |
| 12 | `M24` | no | 19 | 5 | 1 | yes | 18 | no |
| 13 | `M04` | no | 22 | 2 | 1 | yes | 20 | no |
| 14 | `M15` | no | 20 | 4 | 1 | yes | 20 | no |
| 15 | `M26` | no | 20 | 4 | 1 | yes | 20 | no |
| 16 | `M23` | no | 19 | 5 | 1 | yes | 20 | no |
| 17 | `M02` | no | 22 | 2 | 2 | no | — | no |
| 18 | `M17` | no | 22 | 2 | 2 | no | — | no |
| 19 | `M07` | no | 21 | 3 | 2 | no | — | no |
| 20 | `M12` | no | 21 | 3 | 2 | no | — | no |
| 21 | `M13` | no | 21 | 3 | 2 | no | — | no |
| 22 | `M05` | no | 20 | 4 | 2 | no | — | no |
| 23 | `M25` | no | 20 | 4 | 2 | no | — | no |
| 24 | `M27` | no | 20 | 4 | 2 | no | — | no |
| 25 | `M09` | no | 19 | 5 | 2 | no | — | no |
| 26 | `M21` | no | 19 | 5 | 2 | no | — | no |
| 27 | `M22` | no | 19 | 5 | 2 | no | — | no |
| 28 | `M28` | no | 18 | 6 | 2 | no | — | no |

## Best candidate details

### M01

- Frozen baseline: `True`
- Accepted edges retained: `24/24`
- Changed endpoint edges: `0`
- Selected rejected-edge reasons: `none`
- Selected rejected candidates: `none`
- Parity violations: `16`
- Violating events: `E01 E03 E05 E07 E09 E13 E14 E15 E16 E17 E21 E22 E23 E24 E28 E30`

### M03

- Frozen baseline: `False`
- Accepted edges retained: `22/24`
- Changed endpoint edges: `2`
- Selected rejected-edge reasons: `colour_transition_conflict:2`
- Selected rejected candidates: `X_RB_R_S07E_B_S06E X_RG_R_S01S_G_S11E`
- Parity violations: `16`
- Violating events: `E01 E04 E08 E10 E16 E17 E18 E19 E20 E22 E23 E25 E26 E29 E30 E31`

### M08

- Frozen baseline: `False`
- Accepted edges retained: `22/24`
- Changed endpoint edges: `2`
- Selected rejected-edge reasons: `colour_transition_conflict:2`
- Selected rejected candidates: `X_GB_G_S11E_B_S01S X_RG_R_S07E_G_S01S`
- Parity violations: `16`
- Violating events: `E01 E03 E05 E07 E09 E13 E14 E15 E16 E17 E21 E22 E23 E24 E28 E30`

### M18

- Frozen baseline: `False`
- Accepted edges retained: `22/24`
- Changed endpoint edges: `2`
- Selected rejected-edge reasons: `colour_transition_conflict:2`
- Selected rejected candidates: `X_GB_G_S01S_B_S06E X_RB_R_S01S_B_S01S`
- Parity violations: `16`
- Violating events: `E01 E03 E05 E07 E09 E13 E14 E15 E16 E17 E21 E22 E23 E24 E28 E30`

### M10

- Frozen baseline: `False`
- Accepted edges retained: `21/24`
- Changed endpoint edges: `3`
- Selected rejected-edge reasons: `colour_transition_conflict:3`
- Selected rejected candidates: `X_GB_G_S01S_B_S06E X_RB_R_S07E_B_S01S X_RG_R_S01S_G_S11E`
- Parity violations: `16`
- Violating events: `E01 E04 E08 E10 E16 E17 E18 E19 E20 E22 E23 E25 E26 E29 E30 E31`

### M11

- Frozen baseline: `False`
- Accepted edges retained: `21/24`
- Changed endpoint edges: `3`
- Selected rejected-edge reasons: `colour_transition_conflict:3`
- Selected rejected candidates: `X_GB_G_S11E_B_S06E X_RB_R_S07E_B_S01S X_RG_R_S01S_G_S01S`
- Parity violations: `16`
- Violating events: `E01 E04 E08 E10 E16 E17 E18 E19 E20 E22 E23 E25 E26 E29 E30 E31`

### M14

- Frozen baseline: `False`
- Accepted edges retained: `21/24`
- Changed endpoint edges: `3`
- Selected rejected-edge reasons: `colour_transition_conflict:3`
- Selected rejected candidates: `X_GB_G_S11E_B_S06E X_RB_R_S01S_B_S01S X_RG_R_S07E_G_S01S`
- Parity violations: `16`
- Violating events: `E01 E03 E05 E07 E09 E13 E14 E15 E16 E17 E21 E22 E23 E24 E28 E30`

### M16

- Frozen baseline: `False`
- Accepted edges retained: `21/24`
- Changed endpoint edges: `3`
- Selected rejected-edge reasons: `colour_transition_conflict:3`
- Selected rejected candidates: `X_GB_G_S11E_B_S01S X_RB_R_S07E_B_S06E X_RG_R_S01S_G_S01S`
- Parity violations: `16`
- Violating events: `E01 E04 E08 E10 E16 E17 E18 E19 E20 E22 E23 E25 E26 E29 E30 E31`

## Interpretation

No provisional endpoint perfect matching removes the Gauss-parity failure.

Therefore endpoint connectivity, across both same-colour and cross-colour alternatives currently represented in the candidate graph, is insufficient to explain the failure.

The next audit must move to the crossing inventory itself: missed crossings, duplicated crossing events, or incorrect crossing-to-fragment assignments.

Even a zero-violation result would provide only a necessary, not sufficient, classical-realizability condition.

## Generated output

- `data/derived/a10_p03_full_endpoint_matching_search.csv` (local exhaustive table)
