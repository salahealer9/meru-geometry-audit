# First Hand linear central-projective reconstruction

**Status:** preregistered zero-parameter algebraic reconstruction

The candidate map is reconstructed from the already-frozen X1 and Y1 stereographic circle centres only.

No curve was refitted and no optimizer was called.

## Reconstructed dual-coordinate matrix

```text
G =
    [0.000628602157, -1.018041679680]
    [1.000458823865, -0.609568332751]
```

- det(G): `1.018125605529`
- cond(G): `1.815073259`
- inverse available: `True`

## Reconstructed construction matrix

```text
L =
    [-0.598716238390, -0.982647738582]
    [0.999917568275, 0.000617411205]
```

- det(L): `0.982197083120`
- cond(L): `1.815073259`
- sigma_1: `1.335200232564`
- sigma_2: `0.735617819084`
- sigma_1 / sigma_2: `1.815073259408`

## Independent zero-coordinate line validation

- eta_x, predicted X1 dual direction vs observed YAXIS normal: `30.008196754 deg`
- eta_y, predicted Y1 dual direction vs observed Y0 normal: `0.436938761 deg`
- angle(g_x, g_y): `59.052276590 deg`
- |90 - angle(g_x,g_y)|: `30.947723410 deg`
- observed zero-line normal angle: `89.497412106 deg`

No PASS threshold was introduced.

## Centre-derived coordinate scales

- ||c_X1||: `1.000459021345`
- ||c_Y1||: `1.186584347553`
- k_x(center) = 1/||c_X1||: `0.999541189259`
- k_y(center) = 1/||c_Y1||: `0.842755091168`
- centre-predicted delta_x: `44.986853025 deg`
- centre-predicted delta_y: `40.122684847 deg`
- earlier observed delta_x: `52.232240366 deg`
- earlier observed delta_y: `40.124661708 deg`

Differences between centre-predicted and observed plane angles are a direct measure of the independent zero-line directional mismatch.

## Frozen rendering closure context

- X1 epsilon_power: `-0.003122798`
- X1 Delta_R: `-0.534270 px`
- X1 Delta_antipodal: `0.178841 deg`
- Y1 epsilon_power: `-0.050489387`
- Y1 Delta_R: `-8.743111 px`
- Y1 Delta_antipodal: `2.438130 deg`

The circle radii above did not enter reconstruction of G or L.

## Fixed source-scale comparators

| Candidate | k | kx(center)-k | ky(center)-k | sigma1-k | sigma2-k |
|---|---:|---:|---:|---:|---:|
| `G30` | 0.577350269190 | 0.422190920 | 0.265404822 | 0.757849963 | 0.158267550 |
| `GHALF` | 0.546302489844 | 0.453238699 | 0.296452601 | 0.788897743 | 0.189315329 |
| `GUNIT` | 1.000000000000 | -0.000458811 | -0.157244909 | 0.335200233 | -0.264382181 |
| `GONE` | 1.557407724655 | -0.557866535 | -0.714652633 | -0.222207492 | -0.821789906 |

No candidate is selected merely because it is numerically nearest.

## Holdout and scope

`AOG-LM-P07-GC-SCAFFOLD-UR-UC-X1LL-LL` was not used to reconstruct or validate L.

No unrestricted 3x3 projective fit, nonlinear map, reciprocal-spiral projection, S1, S1.5, or S2 is computed.
