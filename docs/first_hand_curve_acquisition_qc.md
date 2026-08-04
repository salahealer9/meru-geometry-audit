# First Hand curve acquisition QC

## Status

Post-hoc acquisition-QC investigation performed only after the raw
two-pass observations, analysis protocol, implementation, and first
successful numerical result had been frozen.

The raw acquisition files remain immutable.

## Trigger

The primary two-pass curve audit found anomalous X1 agreement:

- symmetric median: 0.310396 px
- symmetric RMS: 66.169279 px
- symmetric P95: 197.455996 px
- symmetric maximum: 283.447269 px

The preregistered median-only 12 px manual-review trigger did not fire.

## Localization

The discrepancy was entirely one-sided:

- pass 1 -> pass 2 RMS: 0.378072 px
- pass 2 -> pass 1 RMS: 93.576728 px

Segment-level diagnosis localized the discrepancy to:

- pass: 2
- curve: AOG-LM-P07-GC-X1
- segment: S01

All other X1 segments showed sub-pixel two-pass agreement.

## Raw acquisition anomaly

Pass-2 X1 S01 begins with sequence indices 0 through 77 at exactly the
same recorded coordinate:

- x = 704.765128489 px
- y = 882.940038685 px
- timestamp = 2026-08-03T08:37:42Z

The 78 records therefore have zero inter-point displacement.

Sequence index 78 is the first non-identical coordinate. The transition
from the duplicated location to index 78 is 283.947002 px.

Index 78 lies 3.410001 px from the independently acquired pass-1 X1
trace. Subsequent acquisition steps are ordinary several-pixel tracing
steps and return immediately to sub-pixel two-pass agreement.

The duplicated prefix therefore generates a spurious long polyline edge
that is not an observed source-curve trace.

## Post-hoc sensitivity

A diagnostic analysis excluded only pass-2 X1 S01 sequence indices
0 through 77 in memory. No raw CSV was modified.

Corrected X1 symmetric agreement:

- median: 0.254857 px
- RMS: 0.406347 px
- P95: 0.724291 px
- maximum: 3.410001 px

Directed agreement:

Pass 1 -> pass 2:

- median: 0.260548 px
- RMS: 0.378072 px
- P95: 0.723584 px
- maximum: 2.628143 px

Pass 2 -> pass 1:

- median: 0.252652 px
- RMS: 0.432779 px
- P95: 0.749964 px
- maximum: 3.410001 px

## Interpretation

The evidence supports classification of sequence indices 0 through 77
as a duplicated input-event burst rather than independent curve
observations.

The exclusion is based on acquisition metadata and exact coordinate
duplication, not on improving agreement with a geometric model.

The primary raw result remains preserved. Any QC-corrected result is a
separate post-hoc acquisition-QC sensitivity analysis and must not
replace or overwrite the primary result.
