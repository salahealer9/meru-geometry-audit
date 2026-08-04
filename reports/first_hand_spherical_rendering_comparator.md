# First Hand spherical-rendering invariant comparator

**Status:** preregistered parameter-free comparator

Frozen limb radius: `341.906449919 px`

No curve was refitted and no optimizer was called.

## Near-linear labelled traces

| Curve | Frozen line RMS px | Centre distance px | Centre distance / R | Orthographic GC RMS px |
|---|---:|---:|---:|---:|
| `AOG-LM-P07-GC-Y0` | 0.317838 | 5.570373 | 0.016292098 | 1.080070 |
| `AOG-LM-P07-GC-YAXIS` | 0.346677 | 0.104007 | 0.000304196 | 0.226116 |

## Curved labelled traces

| Curve | Circle RMS px | r px | d px | r/R | d/R | epsilon_power | Delta_R px | Antipodal separation deg | Delta antipodal deg | Orthographic GC RMS px |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `AOG-LM-P07-GC-Y1` | 1.082726 | 524.967602 | 405.700842 | 1.535413 | 1.186584 | -0.050489387 | -8.743111 | 177.561870 | 2.438130 | 13.803555 |
| `AOG-LM-P07-GC-X1` | 1.023443 | 483.262175 | 342.063392 | 1.413434 | 1.000459 | -0.003122798 | -0.534270 | 179.821159 | 0.178841 | 12.303530 |

## Independent scaffold holdout

Curve: `AOG-LM-P07-GC-SCAFFOLD-UR-UC-X1LL-LL`

- frozen circle RMS: `0.905565 px`
- radius r: `502.057295 px`
- centre offset d: `368.627887 px`
- r/R: `1.468405`
- d/R: `1.078154`
- epsilon_power: `-0.006201981`
- Delta_R: `-1.061898 px`
- antipodal separation: `179.670411 deg`
- Delta antipodal: `0.329589 deg`

The scaffold did not calibrate or modify the stereographic invariant.

## Interpretation boundary

The stereographic circle condition is `r^2 - d^2 = R^2`. The straight-line branch requires the frozen line to pass through the frozen sphere centre.

No new binary acceptance threshold is introduced. These are continuous closure diagnostics on a hand-drawn source.

This comparator concerns rendering of an already-spherical scaffold onto the page. It does not replace the earlier flat-to-sphere central-projective construction-map audit.

No projective gauge, construction scale, reciprocal-spiral result, S1, S1.5, or S2 is produced.
