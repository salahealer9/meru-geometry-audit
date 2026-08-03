# First Hand two-pass curve geometry audit

**Status:** model-neutral image-space result

## Pass agreement

| Curve | Partition | Median px | RMS px | P95 px | Max px | Review |
|---|---|---:|---:|---:|---:|---|
| `AOG-LM-P07-GC-Y0` | calibration_labelled_curve | 0.172122 | 0.364852 | 0.670148 | 3.810242 | PASS |
| `AOG-LM-P07-GC-Y1` | calibration_labelled_curve | 0.252148 | 0.470462 | 0.965620 | 3.141359 | PASS |
| `AOG-LM-P07-GC-YAXIS` | calibration_labelled_curve | 0.227375 | 0.571250 | 0.918736 | 4.472629 | PASS |
| `AOG-LM-P07-GC-X1` | calibration_labelled_curve | 0.310396 | 66.169279 | 197.455996 | 283.447269 | PASS |
| `AOG-LM-P07-GC-SCAFFOLD-UR-UC-X1LL-LL` | independent_scaffold_holdout | 0.275083 | 0.444380 | 0.830368 | 3.095268 | PASS |

## Equal-pass combined descriptive fits

| Curve | Circle RMS px | Ellipse RMS px | Ellipse b/a |
|---|---:|---:|---:|
| `AOG-LM-P07-GC-Y0` | 0.317808 | 0.326229 | 0.064678029 |
| `AOG-LM-P07-GC-Y1` | 1.082726 | 0.799017 | 0.564493262 |
| `AOG-LM-P07-GC-YAXIS` | 0.305422 | 0.305722 | 0.237965890 |
| `AOG-LM-P07-GC-X1` | 41.488724 | 41.372473 | 0.786419419 |
| `AOG-LM-P07-GC-SCAFFOLD-UR-UC-X1LL-LL` | 0.905565 | 0.818643 | 0.913135662 |

## Scope boundary

`AOG-LM-P07-GC-SCAFFOLD-UR-UC-X1LL-LL` remains an independent holdout.

No projective map, projective gauge, spherical scale, great-circle certification, reciprocal-spiral verdict, S1, S1.5, or S2 is produced.

The source is hand-drawn; image-space residuals do not certify exact mathematical incidence.
