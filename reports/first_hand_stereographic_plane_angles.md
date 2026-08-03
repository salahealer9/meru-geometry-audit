# First Hand stereographic spherical-plane reconstruction

**Status:** preregistered algebraic plane-angle reconstruction

No curve was refitted and no optimizer was called.

## Reconstructed labelled planes

| Curve | Branch | Unit plane normal |
|---|---|---|
| `AOG-LM-P07-GC-Y0` | stereographic_diameter_line | (0.861852438, 0.507159123, 0.000000000) |
| `AOG-LM-P07-GC-Y1` | stereographic_finite_circle | (0.656052966, 0.392821945, 0.644426431) |
| `AOG-LM-P07-GC-YAXIS` | stereographic_diameter_line | (-0.499579699, 0.866267929, 0.000000000) |
| `AOG-LM-P07-GC-X1` | stereographic_finite_circle | (-0.000444387, -0.707268874, 0.706944511) |

## Image-derived coordinate separations

- delta_x = `52.232240366 deg`
- delta_y = `40.124661708 deg`
- delta_x - delta_y = `12.107578658 deg`
- |delta_x - delta_y| = `12.107578658 deg`
- k_x = tan(delta_x) = `1.290691237560`
- k_y = tan(delta_y) = `0.842814100706`
- k_x / k_y = `1.531406791223`

No equality between delta_x and delta_y was imposed.

## Frozen source-scale comparators

| Candidate | Predicted delta deg | k | delta_x residual deg | delta_y residual deg | two-axis RMS deg |
|---|---:|---:|---:|---:|---:|
| `G30` | 30.000000000 | 0.577350269190 | 22.232240366 | 10.124661708 | 17.273987473 |
| `GHALF` | 28.647889757 | 0.546302489844 | 23.584350610 | 11.476771951 | 18.546399760 |
| `GUNIT` | 45.000000000 | 1.000000000000 | 7.232240366 | -4.875338292 | 6.167423456 |
| `GONE` | 57.295779513 | 1.557407724655 | -5.063539147 | -17.171117805 | 12.658726543 |

## Rendering-closure context

- Y0 line-centre miss: `5.570373 px`
- Y-axis line-centre miss: `0.104007 px`
- Y1 epsilon_power: `-0.050489387`; Delta_R = `-8.743111 px`
- X1 epsilon_power: `-0.003122798`; Delta_R = `-0.534270 px`

The Y1-derived spherical angle must be interpreted with its larger stereographic rendering misclosure in view.

## Scaffold holdout

`AOG-LM-P07-GC-SCAFFOLD-UR-UC-X1LL-LL` remains outside plane-angle and scale reconstruction.

Its previously frozen stereographic closure is retained only as independent rendering evidence.

## Scope boundary

No single construction scale, general projective gauge, reciprocal spiral projection, S1, S1.5, or S2 is selected or computed.
