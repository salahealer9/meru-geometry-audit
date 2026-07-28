# Geometric Panel Selection — v0.6

## Inspection outcome

The four principal source images were inspected at their native resolutions:

| Asset | Dimensions | Primary value |
|---|---:|---|
| A03 | 579 × 880 | Early conceptual relationship among flame, torus, tetrahedron, and asymmetry |
| A04 | 640 × 957 | Seven-region ribbon topology, numbered regions, and boundary identifications |
| A05 | 543 × 880 | Historical depiction of the seven tetrahedral axes |
| A10 | 576 × 720 | Explicit transition from the canonical (3,10) ring to a dimpled-sphere construction |

## Primary digitisation target

The first coordinate target is:

> **A10_P01 — Ring-to-dimpled-sphere transition strip**

This panel was selected because it shows three successive forms:

1. a conventional ring representation;
2. an intermediate opened or transformed form;
3. a dimpled-sphere representation.

The three colour-coded strands remain visible through the transition, and
integer winding labels are supplied in the source diagram.

## First centreline target

The first detailed tracing target is:

> **A10_P03 — Complete 3,10 knot on dimpled sphere**

The red, green, and blue paths will be digitised as separate two-dimensional
polylines.

The digitised curves will represent only the source drawing in image
coordinates. They will not initially be interpreted as three-dimensional
coordinates.

## Topological control

The main topological comparison target is:

> **A04_P02 — Flattened numbered ribbon**

This panel supplies:

- numbered regions;
- boundary labels A, B, C, and D;
- the stated A-B and D-C identifications;
- the ribbon's one-sided Möbius interpretation;
- the source's seven-region structure.

It is better suited to topological auditing than metric fitting.

## Deferred assets

### A03

A03 combines several conceptually related but geometrically distinct panels.
Its central vortex is highly occluded and stylised. It is retained for
historical interpretation rather than first-pass coordinate fitting.

### A05

A05 provides direct historical evidence for three opposite-edge axes and four
vertex-face axes. Those axes are already available exactly from the regular
tetrahedron model, so the hand-drawn coordinates should not replace the exact
construction.

A05 will later be used as a source-consistency comparison.

## Reconstruction boundary

The first digitisation pass will recover:

\[
(x_i,y_i)
\]

in source-image coordinates only.

No camera model, depth coordinate, surface equation, or three-dimensional
embedding will be inferred during tracing.

The first pass will separately trace:

- red centreline;
- green centreline;
- blue centreline;
- visible dimple boundary;
- visible outer boundary;
- numbered winding landmarks.

Hidden curve segments and ambiguous crossings will be marked rather than
invented.
