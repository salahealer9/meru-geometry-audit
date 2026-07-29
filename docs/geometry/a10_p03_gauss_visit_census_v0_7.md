# A10_P03 Gauss-Visit Census — v0.7

## Purpose

Map both visits to every reviewed crossing onto the frozen v0.6 global-cycle traversal.

## Invariants

- Crossing events: **31**
- Total visits: **62**
- Over visits: **31**
- Under visits: **31**
- Frozen visible segments: **24**
- Exact unresolved positional ties: **1**
- Close consecutive visit pairs reviewed: **4**

Every crossing event appears exactly twice: once as an over visit and once as an under visit.

## Ordering method

Each candidate-side location is converted from its polyline piece index and piece fraction into normalized polyline arc length.

For reversed segments the local fraction is transformed by

\[
s_{\mathrm{traversal}}=1-s_{\mathrm{source}}.
\]

Visits are then ordered first by frozen segment order and then by traversal-oriented arc fraction.

## Frozen traversal

```text
R:S01+ → R:S02+ → R:S03+ → R:S04− → R:S05+ → R:S06− → R:S07+ → G:S11− → G:S10− → G:S09− → G:S08− → G:S07+ → G:S06− → G:S05− → G:S04− → G:S03+ → G:S02− → G:S01− → B:S01+ → B:S02− → B:S03+ → B:S04+ → B:S05+ → B:S06+
```

## Provisional O/U Gauss sequence

```text
E13O {E21O|E24U} E15U E26U E25U E14O E05O E09U E03U E04U E10O E19U E20U E07U E28U E18O E29O E31O
E08O E13U E21U E27U E12U E25O E26O E11O E05U E06U E04O E17O E23O E10U E02U E07O E28O E22O E30O E16U
E01U E22U E18U E29U E27O E12O E15O E24O E11U E14U E06O E09O E03O E17U E23U E02O E19O E20O E01O E16O
E30U E08U E31U
```

Braces denote visits whose current digitized positions are exactly tied. Their order has deliberately not been inferred.

## Exact unresolved ties

| Tie | Segment | Visits | Fraction |
|---|---|---|---:|
| `T01` | `R:S01` | `E21O / E24U` | 1.000000000 |

## Close-order review set

| Review | Kind | Segment | Derived display order | Fractional gap |
|---|---|---|---|---:|
| `ORDER_R_S01_E21O_E24U` | exact tie | `R:S01` | `E21O → E24U` | 0.000000000 |
| `ORDER_R_S07_E31O_E08O` | close | `R:S07` | `E31O → E08O` | 0.020195930 |
| `ORDER_B_S01_E27O_E12O` | close | `B:S01` | `E27O → E12O` | 0.004278183 |
| `ORDER_B_S04_E01O_E16O` | close | `B:S04` | `E01O → E16O` | 0.017201576 |

For the exact tie, the displayed order is merely deterministic table order and is not yet an accepted geometric order.

## Interpretation boundary

This census establishes 62 source-linked O/U visits and their segment-level placement.

It does not yet establish:

- a unique canonical Gauss word;
- crossing signs;
- a Dowker–Thistlethwaite code;
- a knot polynomial;
- equivalence with the canonical `(3,10)` torus knot.

The exact tie must be resolved and the three close orders visually confirmed before the unique Gauss word is frozen.

## Generated outputs

- `data/derived/a10_p03_gauss_visits.csv` (local derived table)
- `data/manual_digitizations/A10_P03/gauss_order_review.csv`
- `figures/a10_p03_gauss_order_review.png`
