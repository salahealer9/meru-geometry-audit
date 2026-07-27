# A10_P03 Cross-Colour Candidate Audit — v0.6

## Current graph boundary

The red, green and blue traces each form one non-branched open chain with two free endpoints.

| Layer | Free endpoints |
|---|---|
| Red | `S01S, S07E` |
| Green | `S01S, S11E` |
| Blue | `S01S, S06E` |

## Cross-colour edge candidates

All 12 pairings between differently coloured free endpoints are included.

| Rank | Candidate | Distance (px) | Tangent mismatch (degrees) | Score |
|---:|---|---:|---:|---:|
| 1 | `X_RG_R_S07E_G_S11E` | 2.831 | 3.797 | 2.890 |
| 2 | `X_RB_R_S01S_B_S06E` | 2.897 | 15.949 | 3.153 |
| 3 | `X_GB_G_S01S_B_S01S` | 3.501 | 10.062 | 3.696 |
| 4 | `X_GB_G_S11E_B_S06E` | 27.717 | 80.358 | 40.091 |
| 5 | `X_RB_R_S07E_B_S06E` | 27.356 | 90.000 | 41.033 |
| 6 | `X_RG_R_S01S_G_S11E` | 28.224 | 89.156 | 42.204 |
| 7 | `X_RG_R_S07E_G_S01S` | 91.629 | 88.569 | 136.715 |
| 8 | `X_RB_R_S07E_B_S01S` | 92.178 | 88.536 | 137.517 |
| 9 | `X_GB_G_S11E_B_S01S` | 91.857 | 95.303 | 140.493 |
| 10 | `X_GB_G_S01S_B_S06E` | 118.982 | 88.569 | 177.527 |
| 11 | `X_RG_R_S01S_G_S01S` | 119.636 | 90.794 | 179.982 |
| 12 | `X_RB_R_S01S_B_S01S` | 120.077 | 94.460 | 183.090 |

## Complete perfect matchings

A perfect matching uses all six free endpoints exactly once. There are eight such cross-colour matchings.

| Rank | Candidate edges | Total distance (px) | Total score | Maximum edge score |
|---:|---|---:|---:|---:|
| 1 | `X_GB_G_S01S_B_S01S`<br>`X_RB_R_S01S_B_S06E`<br>`X_RG_R_S07E_G_S11E` | 9.228 | 9.740 | 3.696 |
| 2 | `X_GB_G_S01S_B_S01S`<br>`X_RB_R_S07E_B_S06E`<br>`X_RG_R_S01S_G_S11E` | 59.080 | 86.934 | 42.204 |
| 3 | `X_GB_G_S11E_B_S01S`<br>`X_RB_R_S01S_B_S06E`<br>`X_RG_R_S07E_G_S01S` | 186.383 | 280.361 | 140.493 |
| 4 | `X_GB_G_S01S_B_S06E`<br>`X_RB_R_S07E_B_S01S`<br>`X_RG_R_S01S_G_S11E` | 239.384 | 357.248 | 177.527 |
| 5 | `X_GB_G_S11E_B_S06E`<br>`X_RB_R_S07E_B_S01S`<br>`X_RG_R_S01S_G_S01S` | 239.531 | 357.590 | 179.982 |
| 6 | `X_GB_G_S11E_B_S06E`<br>`X_RB_R_S01S_B_S01S`<br>`X_RG_R_S07E_G_S01S` | 239.422 | 359.895 | 183.090 |
| 7 | `X_GB_G_S11E_B_S01S`<br>`X_RB_R_S07E_B_S06E`<br>`X_RG_R_S01S_G_S01S` | 238.849 | 361.508 | 179.982 |
| 8 | `X_GB_G_S01S_B_S06E`<br>`X_RB_R_S01S_B_S01S`<br>`X_RG_R_S07E_G_S11E` | 241.890 | 363.508 | 183.090 |

## Interpretation boundary

The ranking is geometric triage only. A short endpoint gap does not establish a real colour transition.

A complete matching is a combinatorial hypothesis, not a source-supported reconstruction. Each of its three edges must be independently reviewed against A10_P03.

Acceptance of three mutually compatible transition edges would join the three open colour chains into one closed cycle. It would not by itself prove a unique three-dimensional knot embedding.
