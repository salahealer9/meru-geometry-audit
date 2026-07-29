# A10_P03 Source-Reviewed O/U Gauss Word — v0.7

## Result

The completed A10_P03 crossing inventory and four manual visit-order decisions define one unique O/U Gauss word along the frozen v0.6 global-cycle traversal.

- Crossing events: **31**
- Total visits: **62**
- Over visits: **31**
- Under visits: **31**
- Unresolved visit-order ties: **0**
- Ambiguous crossing assignments: **0**
- Token-sequence SHA-256: `cc13c50da01ad6f13e6dd3b552fb8907b1e937cf5fed7bf85183e7b05222a090`

## Canonical O/U Gauss word

```text
E13O E21O E24U E15U E26U E25U E14O E05O E09U E03U E04U E10O E19U E20U E07U E28U E18O E29O E31O E08O
E13U E21U E27U E12U E25O E26O E11O E05U E06U E04O E17O E23O E10U E02U E07O E28O E22O E30O E16U E01U
E22U E18U E29U E27O E12O E15O E24O E11U E14U E06O E09O E03O E17U E23U E02O E19O E20O E01O E16O E30U
E08U E31U
```

Every event label appears exactly twice: once with `O` and once with `U`.

## Manual order resolutions

| Review | Segment | Accepted order | Confidence |
|---|---|---|---|
| `ORDER_R_S01_E21O_E24U` | Red S01 | `E21O → E24U` | High |
| `ORDER_R_S07_E31O_E08O` | Red S07 | `E31O → E08O` | High |
| `ORDER_B_S01_E27O_E12O` | Blue S01 | `E27O → E12O` | High |
| `ORDER_B_S04_E01O_E16O` | Blue S04 | `E01O → E16O` | High |

The red S01 decision resolves an exact positional tie caused by both visits being represented at the same digitized fragment endpoint. The other three reviews confirm close but already distinct arc-length orders.

## Visits grouped by frozen segment

| Traversal segment | Visits in accepted order |
|---|---|
| `R:S01+` | `E13O E21O E24U` |
| `R:S02+` | `E15U E26U` |
| `R:S03+` | `E25U E14O E05O E09U` |
| `R:S04−` | `E03U E04U` |
| `R:S05+` | `E10O E19U` |
| `R:S06−` | `E20U E07U` |
| `R:S07+` | `E28U E18O E29O E31O E08O` |
| `G:S11−` | `—` |
| `G:S10−` | `E13U` |
| `G:S09−` | `E21U E27U` |
| `G:S08−` | `E12U E25O E26O E11O` |
| `G:S07+` | `E05U E06U` |
| `G:S06−` | `E04O E17O E23O` |
| `G:S05−` | `E10U E02U` |
| `G:S04−` | `E07O E28O E22O E30O E16U` |
| `G:S03+` | `E01U` |
| `G:S02−` | `E22U E18U` |
| `G:S01−` | `E29U` |
| `B:S01+` | `E27O E12O E15O E24O` |
| `B:S02−` | `E11U E14U` |
| `B:S03+` | `E06O E09O E03O E17U` |
| `B:S04+` | `E23U E02O E19O E20O E01O E16O` |
| `B:S05+` | `E30U E08U` |
| `B:S06+` | `E31U` |

## Reproducibility boundary

The canonical token sequence is frozen in:

- `data/manual_digitizations/A10_P03/gauss_word.csv`;
- `data/manual_digitizations/A10_P03/gauss_word.sha256`.

A normal execution validates the reconstructed word against these files. Replacing the snapshot requires the explicit `--update-snapshot` option.

## Interpretation boundary

This result establishes a unique source-reviewed O/U Gauss word for the reconstructed planar cycle.

It does not yet establish:

- oriented crossing signs;
- a signed Gauss code;
- a Dowker–Thistlethwaite code;
- an Alexander or Jones polynomial;
- equivalence with the canonical `(3,10)` torus knot;
- a unique three-dimensional embedding.

The next stage is to calculate an oriented tangent at both branches of every crossing and assign crossing signs under one documented coordinate convention.
