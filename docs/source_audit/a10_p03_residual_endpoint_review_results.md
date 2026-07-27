# A10_P03 Residual Endpoint Review Results

## Review set

The graph-constrained residual review contained:

- 4 red inter-component candidates;
- 15 green inter-component candidates;
- 1 blue closure candidate;
- 20 candidates in total.

All candidates have now been reviewed.

## Outcome

| Status | Count |
|---|---:|
| Accepted | 6 |
| Rejected | 14 |
| Ambiguous | 0 |
| Unreviewed | 0 |

Every decision was assigned high confidence.

## Red results

| Candidate | Decision | Reason |
|---|---|---|
| `R_M_C01_C02_S01E_S02S` | Accepted | `occlusion_supported` |
| `R_M_C01_C02_S01S_S07E` | Rejected | `colour_intersection` |
| `R_M_C01_C02_S01E_S07E` | Rejected | `colour_intersection` |
| `R_M_C01_C02_S01S_S02S` | Rejected | `colour_intersection` |

The accepted edge joins the two previous red components. All seven visible red
fragments therefore form one non-branched open chain.

## Green results

### Accepted connections

| Candidate | Reason |
|---|---|
| `G_M_C01_C02_S01E_S02S` | `occlusion_supported` |
| `G_M_C02_C03_S02E_S03E` | `occlusion_supported` |
| `G_M_C03_C04_S07S_S08S` | `occlusion_supported` |
| `G_M_C04_C05_S08E_S09S` | `occlusion_supported` |
| `G_M_C05_C06_S09E_S10S` | `occlusion_supported` |

The five accepted edges form the component path

\[
C_1\rightarrow C_2\rightarrow C_3\rightarrow C_4\rightarrow C_5\rightarrow C_6.
\]

This is the graph-theoretic minimum of \(6-1=5\) edges required to connect the
six previous components into one open chain. No endpoint is reused.

### Rejected connections

| Candidate | Reason |
|---|---|
| `G_M_C01_C03_S01E_S03E` | `crossing_conflict` |
| `G_M_C01_C04_S01E_S08S` | `different_feature` |
| `G_M_C01_C05_S01S_S09S` | `colour_intersection` |
| `G_M_C01_C06_S01E_S11E` | `colour_intersection` |
| `G_M_C02_C04_S02E_S08S` | `different_feature` |
| `G_M_C02_C05_S02E_S09E` | `different_feature` |
| `G_M_C02_C06_S02E_S11E` | `colour_intersection` |
| `G_M_C03_C05_S07S_S09E` | `different_feature` |
| `G_M_C03_C06_S07S_S10S` | `different_feature` |
| `G_M_C04_C06_S08S_S10S` | `different_feature` |

All eleven visible green fragments therefore form one non-branched open chain.

## Blue result

| Candidate | Decision | Reason |
|---|---|---|
| `B_C_C01_C01_S01S_S06E` | Rejected | `colour_intersection` |

The six blue fragments remain one non-branched open chain rather than a closed
blue cycle.

## Combined connectivity result

Combining the first-stage and residual accepted connections gives:

| Layer | Visible fragments | Accepted edges | Components | Free endpoints | Closed | Branched |
|---|---:|---:|---:|---:|---:|---:|
| Red | 7 | 6 | 1 | 2 | No | No |
| Green | 11 | 10 | 1 | 2 | No | No |
| Blue | 6 | 5 | 1 | 2 | No | No |

Thus all 24 coloured fragments are incorporated into exactly three
non-branched open chains.

The remaining free endpoints are:

- red: `S01S`, `S07E`;
- green: `S01S`, `S11E`;
- blue: `S01S`, `S06E`.

## Interpretation boundary

The source-derived connectivity does not support three independently closed
same-colour loops in A10_P03.

The free endpoints frequently occur at mixed-colour equatorial intersections.
This makes colour-transition continuity a plausible next hypothesis, but it
does not establish such transitions.

The accepted connections establish local topological continuity only. They do
not determine:

- exact hidden path geometry;
- three-dimensional depth ordering;
- a unique surface embedding;
- equivalence with a canonical \((3,10)\) torus knot.
