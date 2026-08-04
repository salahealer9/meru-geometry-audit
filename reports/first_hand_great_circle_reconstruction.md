# First Hand limb-constrained great-circle reconstruction

**Status:** preregistered projected-great-circle reconstruction

The frozen sphere limb is held fixed. Only the four source-labelled curves are fitted. The unlabelled scaffold remains outside fitting.

## Equal-pass combined reconstruction

| Curve | phi deg | q | semi-minor px | GC RMS px | Line RMS px | Circle RMS px | Ellipse RMS px | Compatibility |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| `AOG-LM-P07-GC-Y0` | 120.475737 | 0.019397396 | 6.632095 | 1.080070 | 0.317838 | 0.317808 | 0.326229 | COMPATIBLE |
| `AOG-LM-P07-GC-Y1` | 120.905044 | 0.312915919 | 106.987971 | 13.803555 | 36.284846 | 1.082726 | 0.799017 | ABOVE FLOOR |
| `AOG-LM-P07-GC-YAXIS` | 29.960337 | 0.000970100 | 0.331684 | 0.226116 | 0.346677 | 0.305422 | 0.305722 | COMPATIBLE |
| `AOG-LM-P07-GC-X1` | 178.936460 | 0.385262289 | 131.723662 | 12.303530 | 42.306425 | 1.023443 | 0.921111 | ABOVE FLOOR |

Compatibility means only compatibility with the fixed-limb orthographic projected-great-circle model at the adopted 2 px image-space uncertainty scale. It is not an exactness certificate.

## Plane-angle branch census

- `delta_x_yaxis_vs_x1`: 37.704516730, 37.774488534 degrees
- `delta_y_y0_vs_y1`: 17.128773326, 19.351113885 degrees

## Independent point-incidence diagnostics

- explicit lower-right Y0/Y1 incidence distance: 4.008099 px
- candidate central Y0/Y-axis incidence distance: 2.141861 px
- candidate upper X1/Y1 incidence distance: 87.320638 px
- nearest neutral rim node to Y-axis/X1 projective infinity: `AOG-LM-P07-RIM-NODE-R` at 186.057500 px

No point landmark was used in the curve fit.

## Scope boundary

`AOG-LM-P07-GC-SCAFFOLD-UR-UC-X1LL-LL` remains outside great-circle fitting and projective calibration.

No projective map, projective gauge, spherical scale, fixed-scale candidate verdict, reciprocal-spiral projection, scaffold prediction, S1, S1.5, or S2 is produced.
