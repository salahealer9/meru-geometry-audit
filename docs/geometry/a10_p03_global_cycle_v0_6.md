# A10_P03 Global Cycle Audit — v0.6

## Result

All 24 visible coloured fragments form one connected, non-branched closed cycle under the manually adjudicated source continuations.

## Graph invariants

| Quantity | Value |
|---|---:|
| Visible segment edges | 24 |
| Same-colour connection edges | 21 |
| Cross-colour transition edges | 3 |
| Endpoint vertices | 48 |
| Total graph edges | 48 |
| Connected components | 1 |
| Degree-two vertices | 48 |

The graph satisfies

\[
|V|=48,\qquad |E|=48,\qquad \deg(v)=2\ \text{for every }v,\qquad c=1.
\]

A finite connected graph in which every vertex has degree two is a single cycle. The equality \(|E|=|V|\) is consistent with the same result.

## Canonical traversal

Starting at the beginning of red segment S01 and traversing its visible edge first gives:

```text
R:S01+ → R:S02+ → R:S03+ → R:S04− → R:S05+ → R:S06− → R:S07+ → G:S11− → G:S10− → G:S09− → G:S08− → G:S07+ → G:S06− → G:S05− → G:S04− → G:S03+ → G:S02− → G:S01− → B:S01+ → B:S02− → B:S03+ → B:S04+ → B:S05+ → B:S06+
```

Every visible segment appears exactly once in the traversal.

## Cross-colour transitions

- `X_RG_R_S07E_G_S11E`
- `X_GB_G_S01S_B_S01S`
- `X_RB_R_S01S_B_S06E`

The transitions occur at the three manually reviewed equatorial colour junctions. Together they connect the red, green and blue open chains into one closed cycle.

## Evidence chain

The global result combines:

1. the manual A10_P03 trace;
2. 15 first-stage accepted occlusion continuations;
3. 6 accepted residual same-colour continuations;
4. 3 accepted cross-colour transitions;
5. an exact endpoint graph audit.

No endpoint is used by more than one adjudicated connection, and no endpoint remains free.

## Interpretation boundary

This result establishes source-supported two-dimensional connectivity.

It does not establish:

- the exact shape of each hidden interpolation;
- complete over-under depth information;
- a unique three-dimensional embedding;
- a unique dimpled-surface equation;
- equivalence with a canonical \((3,10)\) torus knot;
- the claimed Hebrew-letter projection system.

## Generated output

- `figures/a10_p03_global_cycle.png`
