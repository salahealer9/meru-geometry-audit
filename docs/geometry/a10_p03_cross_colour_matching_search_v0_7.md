# A10_P03 Cross-Colour Matching Search — v0.7

## Purpose

Enumerate every perfect matching of the six free cross-colour endpoints while preserving:

- all accepted same-colour continuations;
- the 31 reviewed crossing identities;
- reviewed over-under assignments;
- the source-derived crossing locations.

The frozen Gauss and signed-Gauss snapshots are not modified.

## Search space

- Cross-colour candidate edges: **12**
- Perfect matchings: **8**
- Single-cycle matchings: **8**

## Result

- Frozen-baseline parity violations: **16**
- Minimum violations in the matching space: **16**
- Matchings attaining the minimum: **8**

## Matching table

| Matching | Baseline | Accepted edges | Changed edges | Score | Single cycle | Violations | Even pass |
|---|---|---:|---:|---:|---|---:|---|
| `M01` | yes | 3 | 0 | 9.740 | yes | 16 | no |
| `M02` | no | 1 | 2 | 86.934 | yes | 16 | no |
| `M03` | no | 1 | 2 | 280.361 | yes | 16 | no |
| `M04` | no | 0 | 3 | 357.248 | yes | 16 | no |
| `M05` | no | 0 | 3 | 357.590 | yes | 16 | no |
| `M06` | no | 0 | 3 | 359.895 | yes | 16 | no |
| `M07` | no | 0 | 3 | 361.508 | yes | 16 | no |
| `M08` | no | 1 | 2 | 363.508 | yes | 16 | no |

## Candidate details

### M01

- Frozen baseline: `True`
- Candidate edges: `X_GB_G_S01S_B_S01S X_RB_R_S01S_B_S06E X_RG_R_S07E_G_S11E`
- Total source score: `9.740137`
- Parity violations: `16`
- Violating events: `E01 E03 E05 E07 E09 E13 E14 E15 E16 E17 E21 E22 E23 E24 E28 E30`
- Traversal: `R:S01+ → R:S02+ → R:S03+ → R:S04− → R:S05+ → R:S06− → R:S07+ → G:S11− → G:S10− → G:S09− → G:S08− → G:S07+ → G:S06− → G:S05− → G:S04− → G:S03+ → G:S02− → G:S01− → B:S01+ → B:S02− → B:S03+ → B:S04+ → B:S05+ → B:S06+`

### M02

- Frozen baseline: `False`
- Candidate edges: `X_GB_G_S01S_B_S01S X_RB_R_S07E_B_S06E X_RG_R_S01S_G_S11E`
- Total source score: `86.933683`
- Parity violations: `16`
- Violating events: `E01 E04 E08 E10 E16 E17 E18 E19 E20 E22 E23 E25 E26 E29 E30 E31`
- Traversal: `R:S01+ → R:S02+ → R:S03+ → R:S04− → R:S05+ → R:S06− → R:S07+ → B:S06− → B:S05− → B:S04− → B:S03− → B:S02+ → B:S01− → G:S01+ → G:S02+ → G:S03− → G:S04+ → G:S05+ → G:S06+ → G:S07− → G:S08+ → G:S09+ → G:S10+ → G:S11+`

### M03

- Frozen baseline: `False`
- Candidate edges: `X_GB_G_S11E_B_S01S X_RB_R_S01S_B_S06E X_RG_R_S07E_G_S01S`
- Total source score: `280.360691`
- Parity violations: `16`
- Violating events: `E01 E03 E05 E07 E09 E13 E14 E15 E16 E17 E21 E22 E23 E24 E28 E30`
- Traversal: `R:S01+ → R:S02+ → R:S03+ → R:S04− → R:S05+ → R:S06− → R:S07+ → G:S01+ → G:S02+ → G:S03− → G:S04+ → G:S05+ → G:S06+ → G:S07− → G:S08+ → G:S09+ → G:S10+ → G:S11+ → B:S01+ → B:S02− → B:S03+ → B:S04+ → B:S05+ → B:S06+`

### M04

- Frozen baseline: `False`
- Candidate edges: `X_GB_G_S01S_B_S06E X_RB_R_S07E_B_S01S X_RG_R_S01S_G_S11E`
- Total source score: `357.248131`
- Parity violations: `16`
- Violating events: `E01 E04 E08 E10 E16 E17 E18 E19 E20 E22 E23 E25 E26 E29 E30 E31`
- Traversal: `R:S01+ → R:S02+ → R:S03+ → R:S04− → R:S05+ → R:S06− → R:S07+ → B:S01+ → B:S02− → B:S03+ → B:S04+ → B:S05+ → B:S06+ → G:S01+ → G:S02+ → G:S03− → G:S04+ → G:S05+ → G:S06+ → G:S07− → G:S08+ → G:S09+ → G:S10+ → G:S11+`

### M05

- Frozen baseline: `False`
- Candidate edges: `X_GB_G_S11E_B_S06E X_RB_R_S07E_B_S01S X_RG_R_S01S_G_S01S`
- Total source score: `357.589685`
- Parity violations: `16`
- Violating events: `E01 E04 E08 E10 E16 E17 E18 E19 E20 E22 E23 E25 E26 E29 E30 E31`
- Traversal: `R:S01+ → R:S02+ → R:S03+ → R:S04− → R:S05+ → R:S06− → R:S07+ → B:S01+ → B:S02− → B:S03+ → B:S04+ → B:S05+ → B:S06+ → G:S11− → G:S10− → G:S09− → G:S08− → G:S07+ → G:S06− → G:S05− → G:S04− → G:S03+ → G:S02− → G:S01−`

### M06

- Frozen baseline: `False`
- Candidate edges: `X_GB_G_S11E_B_S06E X_RB_R_S01S_B_S01S X_RG_R_S07E_G_S01S`
- Total source score: `359.895380`
- Parity violations: `16`
- Violating events: `E01 E03 E05 E07 E09 E13 E14 E15 E16 E17 E21 E22 E23 E24 E28 E30`
- Traversal: `R:S01+ → R:S02+ → R:S03+ → R:S04− → R:S05+ → R:S06− → R:S07+ → G:S01+ → G:S02+ → G:S03− → G:S04+ → G:S05+ → G:S06+ → G:S07− → G:S08+ → G:S09+ → G:S10+ → G:S11+ → B:S06− → B:S05− → B:S04− → B:S03− → B:S02+ → B:S01−`

### M07

- Frozen baseline: `False`
- Candidate edges: `X_GB_G_S11E_B_S01S X_RB_R_S07E_B_S06E X_RG_R_S01S_G_S01S`
- Total source score: `361.508445`
- Parity violations: `16`
- Violating events: `E01 E04 E08 E10 E16 E17 E18 E19 E20 E22 E23 E25 E26 E29 E30 E31`
- Traversal: `R:S01+ → R:S02+ → R:S03+ → R:S04− → R:S05+ → R:S06− → R:S07+ → B:S06− → B:S05− → B:S04− → B:S03− → B:S02+ → B:S01− → G:S11− → G:S10− → G:S09− → G:S08− → G:S07+ → G:S06− → G:S05− → G:S04− → G:S03+ → G:S02− → G:S01−`

### M08

- Frozen baseline: `False`
- Candidate edges: `X_GB_G_S01S_B_S06E X_RB_R_S01S_B_S01S X_RG_R_S07E_G_S11E`
- Total source score: `363.508034`
- Parity violations: `16`
- Violating events: `E01 E03 E05 E07 E09 E13 E14 E15 E16 E17 E21 E22 E23 E24 E28 E30`
- Traversal: `R:S01+ → R:S02+ → R:S03+ → R:S04− → R:S05+ → R:S06− → R:S07+ → G:S11− → G:S10− → G:S09− → G:S08− → G:S07+ → G:S06− → G:S05− → G:S04− → G:S03+ → G:S02− → G:S01− → B:S06− → B:S05− → B:S04− → B:S03− → B:S02+ → B:S01−`

## Interpretation

No cross-colour perfect matching removes all parity violations.

Therefore the colour-transition matching alone is insufficient to explain the parity failure. The next search must expand to constrained crossing-order, crossing-identity or same-colour continuation alternatives.

Passing this test would remain necessary but not sufficient for classical planar realizability.

## Generated output

- `data/derived/a10_p03_cross_colour_matching_search.csv` (local derived table)
