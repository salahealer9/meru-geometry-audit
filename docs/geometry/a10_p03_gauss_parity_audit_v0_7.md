# A10_P03 Classical Gauss-Parity Audit — v0.7

## Purpose

Test the frozen 62-visit A10_P03 Gauss word against the necessary even condition for a classical one-component planar knot diagram.

## Necessary condition

For every crossing event, the number of visits lying between its two occurrences must be even.

Equivalent formulations are:

- the two occurrences occupy opposite position parities;
- the corresponding chord has even degree in the interlacement graph.

This condition is necessary but not sufficient for classical planar realizability.

## Result

- Frozen visits: **62**
- Crossing events: **31**
- Events passing: **15**
- Events violating: **16**
- Complete even-condition pass: **no**

## Violating events

| Event | First | Second | Between | Roles | Interlacement degree |
|---|---:|---:|---:|---|---:|
| `E01` | 40 | 58 | 17 | `U/O` | 17 |
| `E03` | 10 | 52 | 41 | `U/O` | 19 |
| `E05` | 8 | 28 | 19 | `O/U` | 19 |
| `E07` | 15 | 35 | 19 | `U/O` | 19 |
| `E09` | 9 | 51 | 41 | `U/O` | 19 |
| `E13` | 1 | 21 | 19 | `O/U` | 19 |
| `E14` | 7 | 49 | 41 | `O/U` | 19 |
| `E15` | 4 | 46 | 41 | `U/O` | 17 |
| `E16` | 39 | 59 | 19 | `U/O` | 17 |
| `E17` | 31 | 53 | 21 | `O/U` | 19 |
| `E21` | 2 | 22 | 19 | `O/U` | 19 |
| `E22` | 37 | 41 | 3 | `O/U` | 3 |
| `E23` | 32 | 54 | 21 | `O/U` | 19 |
| `E24` | 3 | 47 | 43 | `U/O` | 17 |
| `E28` | 16 | 36 | 19 | `U/O` | 19 |
| `E30` | 38 | 60 | 21 | `O/U` | 17 |

The violating event set is:

```text
E01 E03 E05 E07 E09 E13 E14 E15 E16 E17 E21 E22 E23 E24 E28 E30
```

## Interpretation

The current frozen sequence is therefore not eligible for direct conversion into a classical Dowker–Thistlethwaite code.

This result does not determine which earlier reconstruction decision is responsible. Possible causes include:

- an incorrect endpoint matching;
- an incorrect local visit order;
- two candidate rows representing one physical crossing;
- a missed crossing;
- an incorrect crossing-to-fragment assignment.

The digitisation, crossing inventory, over-under review and signed sequence remain preserved as the reproducible baseline being tested.

## Next computational stage

Enumerate admissible endpoint matchings and constrained local-order alternatives, rebuild each candidate traversal and score it by:

1. number of connected components;
2. branching or unused endpoints;
3. number of Gauss-parity violations;
4. agreement with reviewed source evidence;
5. number and cost of changed assumptions.

A zero-violation result would pass this necessary condition but would still require stronger realizability tests.

## Generated outputs

- `data/derived/a10_p03_gauss_parity_audit.csv` (local derived table)
- `figures/a10_p03_gauss_parity_audit.png`
