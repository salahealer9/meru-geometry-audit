# A10_P03 Digitisation Protocol

## Target

**A10_P03 — Complete (3,10) knot on dimpled sphere**

The panel is extracted from source asset A10.

The digitisation records visible two-dimensional source geometry only.

## Coordinate convention

Coordinates are recorded in two systems:

1. panel coordinates:
   - origin at the crop's upper-left;
   - x increases rightward;
   - y increases downward;

2. original A10 source coordinates:
   - obtained by adding the crop offset.

No depth coordinate is inferred.

## Layers

1. red centreline;
2. green centreline;
3. blue centreline;
4. outer dimpled-sphere boundary;
5. central dimple boundary;
6. numbered or winding landmarks.

## Segmentation rule

A new segment must be started whenever:

- a path becomes hidden;
- an occlusion prevents the centreline from being followed;
- a crossing is ambiguous;
- a colour disappears and later reappears;
- the drawing does not justify connecting two visible sections.

Hidden segments must not be invented.

## Sampling rule

Place points:

- at visible endpoints;
- at curvature extrema;
- before and after crossings;
- around sharp changes of direction;
- along smooth sections at roughly uniform visual spacing.

Do not fit or smooth the curve during digitisation.

## Boundary rule

The outer and dimple boundaries are conceptually closed, but the stored data
must not duplicate the first point at the end.

## Suggested tracing order

1. outer boundary;
2. dimple boundary;
3. red centreline;
4. green centreline;
5. blue centreline;
6. winding landmarks.

## Source-resolution warning

The crop is only 190 × 165 pixels.

Use the graphical zoom tool extensively. The digitiser continues to record
native source-pixel coordinates regardless of display magnification.

## Persistence

Every point, undo operation, segment change, and layer switch triggers an
automatic save.

Tracked research outputs:

- `data/manual_digitizations/A10_P03/digitization.json`;
- `data/manual_digitizations/A10_P03/digitization.csv`.

Local ignored preview:

- `data/derived/source_inspection/digitizations/A10_P03_overlay.png`.
