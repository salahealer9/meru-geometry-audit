# First Hand curve geometry — acquisition-QC sensitivity

**Status:** post-hoc acquisition-QC sensitivity

The sealed primary raw-data result is preserved unchanged.

The only observation change is the documented exclusion of pass-2 X1 S01 sequence indices 0–77, representing 78 exact duplicate same-timestamp acquisition events.

## Primary versus QC pass agreement

| Curve | Raw median | Raw RMS | Raw P95 | QC median | QC RMS | QC P95 |
|---|---:|---:|---:|---:|---:|---:|
| `AOG-LM-P07-GC-Y0` | 0.172122 | 0.364852 | 0.670148 | 0.172122 | 0.364852 | 0.670148 |
| `AOG-LM-P07-GC-Y1` | 0.252148 | 0.470462 | 0.965620 | 0.252148 | 0.470462 | 0.965620 |
| `AOG-LM-P07-GC-YAXIS` | 0.227375 | 0.571250 | 0.918736 | 0.227375 | 0.571250 | 0.918736 |
| `AOG-LM-P07-GC-X1` | 0.310396 | 66.169279 | 197.455996 | 0.254857 | 0.406347 | 0.724291 |
| `AOG-LM-P07-GC-SCAFFOLD-UR-UC-X1LL-LL` | 0.275083 | 0.444380 | 0.830368 | 0.275083 | 0.444380 | 0.830368 |

## QC-derived descriptive fits

| Curve | Circle RMS px | Ellipse RMS px | Ellipse b/a |
|---|---:|---:|---:|
| `AOG-LM-P07-GC-Y0` | 0.317808 | 0.326229 | 0.064678029 |
| `AOG-LM-P07-GC-Y1` | 1.082726 | 0.799017 | 0.564493262 |
| `AOG-LM-P07-GC-YAXIS` | 0.305422 | 0.305722 | 0.237965890 |
| `AOG-LM-P07-GC-X1` | 1.023443 | 0.921111 | 0.964279213 |
| `AOG-LM-P07-GC-SCAFFOLD-UR-UC-X1LL-LL` | 0.905565 | 0.818643 | 0.913135662 |

## Interpretation boundary

This sensitivity result does not replace the primary raw-data result.

`AOG-LM-P07-GC-SCAFFOLD-UR-UC-X1LL-LL` remains an independent holdout.

No projective map, projective gauge, spherical scale, great-circle certification, reciprocal-spiral verdict, S1, S1.5, or S2 is produced.

The source is hand-drawn; image-space residuals do not certify exact mathematical incidence.
