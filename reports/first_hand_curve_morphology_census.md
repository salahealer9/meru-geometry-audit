# First Hand neutral curve morphology census

**Status:** post-hoc model-neutral descriptive supplement

Circle and ellipse values are imported unchanged from the sealed acquisition-QC sensitivity result. This supplement adds an equal-pass weighted orthogonal-line fit to every curve.

## Primary 2 px census

| Curve | Partition | Line RMS px | Circle RMS px | Ellipse RMS px | Line/Circle | Circle R / limb R | Ellipse b/a | Line bearing deg |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| `AOG-LM-P07-GC-Y0` | calibration_labelled_curve | 0.317838 | 0.317808 | 0.326229 | 1.000093 | 3589.780895 | 0.064678 | 59.525215 |
| `AOG-LM-P07-GC-Y1` | calibration_labelled_curve | 36.284846 | 1.082726 | 0.799017 | 33.512506 | 1.535413 | 0.564493 | 59.625282 |
| `AOG-LM-P07-GC-YAXIS` | calibration_labelled_curve | 0.346677 | 0.305422 | 0.305722 | 1.135074 | 152.659891 | 0.237966 | 150.027803 |
| `AOG-LM-P07-GC-X1` | calibration_labelled_curve | 42.306425 | 1.023443 | 0.921111 | 41.337344 | 1.413434 | 0.964279 | 1.242119 |
| `AOG-LM-P07-GC-SCAFFOLD-UR-UC-X1LL-LL` | independent_scaffold_holdout | 38.900233 | 0.905565 | 0.818643 | 42.956866 | 1.468405 | 0.913136 | 119.549594 |

## 1 / 2 / 4 px resampling sensitivity

### `AOG-LM-P07-GC-Y0`

| Spacing px | Line RMS px | Circle RMS px | Ellipse RMS px |
|---:|---:|---:|---:|
| 2.0 | 0.317838 | 0.317808 | 0.326229 |
| 1.0 | 0.317667 | 0.317633 | 0.326026 |
| 4.0 | 0.318966 | 0.318900 | 0.327336 |

### `AOG-LM-P07-GC-Y1`

| Spacing px | Line RMS px | Circle RMS px | Ellipse RMS px |
|---:|---:|---:|---:|
| 2.0 | 36.284846 | 1.082726 | 0.799017 |
| 1.0 | 36.283877 | 1.081977 | 0.798025 |
| 4.0 | 36.289235 | 1.086416 | 0.802172 |

### `AOG-LM-P07-GC-YAXIS`

| Spacing px | Line RMS px | Circle RMS px | Ellipse RMS px |
|---:|---:|---:|---:|
| 2.0 | 0.346677 | 0.305422 | 0.305722 |
| 1.0 | 0.346075 | 0.304799 | 0.305098 |
| 4.0 | 0.347204 | 0.306196 | 0.306502 |

### `AOG-LM-P07-GC-X1`

| Spacing px | Line RMS px | Circle RMS px | Ellipse RMS px |
|---:|---:|---:|---:|
| 2.0 | 42.306425 | 1.023443 | 0.921111 |
| 1.0 | 42.305448 | 1.023326 | 0.920650 |
| 4.0 | 42.310670 | 1.024340 | 0.922812 |

### `AOG-LM-P07-GC-SCAFFOLD-UR-UC-X1LL-LL`

| Spacing px | Line RMS px | Circle RMS px | Ellipse RMS px |
|---:|---:|---:|---:|
| 2.0 | 38.900233 | 0.905565 | 0.818643 |
| 1.0 | 38.899287 | 0.905754 | 0.818893 |
| 4.0 | 38.903736 | 0.905468 | 0.818488 |

## Interpretation boundary

A very large fitted circle radius is treated descriptively as the near-straight-line limit rather than as evidence for a physically meaningful enormous circle.

Differences among line, circle, and ellipse residuals are not a formal model-selection test.

`AOG-LM-P07-GC-SCAFFOLD-UR-UC-X1LL-LL` remains an independent scaffold holdout.

No projective map, spherical scale, great-circle certification, reciprocal-spiral verdict, S1, S1.5, or S2 is produced.
