# A10_P03 Reviewed Local-Order Sensitivity — v0.7

## Purpose

Test every reversal subset of the four accepted local Gauss-order decisions.

This is a diagnostic sensitivity analysis. Reversing a pair does not replace or weaken its source review.

## Search space

- Accepted order decisions: **4**
- Reversal combinations: **16**
- Frozen snapshots modified: **no**

## Result

- Frozen-baseline violations: **16**
- Minimum violations: **12**
- Candidates attaining the minimum: **1**
- Zero-violation candidates: **0**

## Exhaustive table

| Rank | Candidate | Baseline | Reversed reviews | Violations | Even pass |
|---:|---|---|---:|---:|---|
| 1 | `O09` | no | 2 | 12 | no |
| 2 | `O03` | no | 1 | 14 | no |
| 3 | `O04` | no | 1 | 14 | no |
| 4 | `O12` | no | 3 | 14 | no |
| 5 | `O15` | no | 3 | 14 | no |
| 6 | `O01` | yes | 0 | 16 | no |
| 7 | `O06` | no | 2 | 16 | no |
| 8 | `O07` | no | 2 | 16 | no |
| 9 | `O10` | no | 2 | 16 | no |
| 10 | `O11` | no | 2 | 16 | no |
| 11 | `O16` | no | 4 | 16 | no |
| 12 | `O02` | no | 1 | 18 | no |
| 13 | `O05` | no | 1 | 18 | no |
| 14 | `O13` | no | 3 | 18 | no |
| 15 | `O14` | no | 3 | 18 | no |
| 16 | `O08` | no | 2 | 20 | no |

## Best hypothetical result

### O09

- Reversed accepted reviews:

  - `ORDER_B_S04_E01O_E16O`
  - `ORDER_R_S01_E21O_E24U`

- Remaining violations:

```text
E03 E05 E07 E09 E13 E14 E15 E17 E22 E23 E28 E30
```

## Interpretation

No combination of the four reviewed local-order reversals removes the parity failure.

Therefore these local order decisions cannot, by themselves, explain the non-classical Gauss parity.

The best hypothetical result still contradicts accepted high-confidence source reviews and retains unresolved parity violations.

The next expansion should therefore examine same-colour continuation alternatives and crossing-inventory structure, rather than revisiting these four decisions in isolation.

## Generated output

- `data/derived/a10_p03_reviewed_order_sensitivity.csv` (local exhaustive table)
