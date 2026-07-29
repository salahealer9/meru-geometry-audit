# A10_P03 Crossing-Sign Review Results

## Completed review

The four events selected by the low-angle diagnostic were reviewed against
the A10_P03 source panel, the reviewed over-under assignments, and the frozen
global-cycle orientations.

| Event | Over-strand | Under-strand | Accepted sign | Confidence |
|---|---|---|---:|---|
| `E03` | Blue S03 | Red S04 | `-1` | High |
| `E21` | Red S01 | Green S09 | `-1` | High |
| `E24` | Blue S01 | Red S01 | `-1` | High |
| `E27` | Blue S01 | Green S09 | `-1` | High |

## Convention

Tangents are evaluated in the right-handed Cartesian image plane

\[
(x,y)=(x_{\mathrm{image}},-y_{\mathrm{image}})
\]

with `+z` pointing toward the viewer. The crossing sign is

\[
\varepsilon=
\operatorname{sign}
\det
\left(
\mathbf t_{\mathrm{over}},
\mathbf t_{\mathrm{under}}
\right).
\]

Under this convention, clockwise rotation from the oriented over-strand
tangent to the oriented under-strand tangent gives a negative determinant.

## Decisions

### E03

Blue S03 is over red S04. Along the frozen orientations, rotating from the
solid blue tangent to the dashed red tangent is clockwise. The accepted sign
is therefore `-1`.

### E21

Red S01 is over green S09. Along the frozen orientations, rotating from the
solid red tangent to the dashed green tangent is clockwise. The accepted sign
is therefore `-1`.

### E24

Blue S01 is over red S01. Along the frozen orientations, rotating from the
solid blue tangent to the dashed red tangent is clockwise. The accepted sign
is therefore `-1`.

### E27

Blue S01 is over green S09. Along the frozen orientations, rotating from the
solid blue tangent to the dashed green tangent is clockwise. The accepted sign
is therefore `-1`.

## Result

All four low-angle events confirm their derived negative signs with high
confidence.

Together with the span-sensitivity analysis, this completes the oriented-sign
review:

- 31 crossing events;
- 31 negative signs;
- 0 positive signs;
- 0 degenerate signs;
- sign stability across all tested tangent spans;
- writhe `-31` under the documented convention.

## Interpretation boundary

The review confirms the oriented crossing signs of this reconstructed planar
diagram.

It does not yet establish the knot type, minimal crossing number, equivalence
with a canonical `(3,10)` torus knot, or a unique three-dimensional embedding.
