# A10_P03 Oriented Crossing-Sign Census — v0.7

## Purpose

Assign an oriented sign to every source-reviewed crossing using the frozen global-cycle direction and reviewed over-under order.

## Coordinate and sign convention

The source image uses coordinates with positive `y` downward. Tangents are converted to a right-handed Cartesian image plane:

\[
(x,y)=(x_{\mathrm{image}},-y_{\mathrm{image}}).
\]

With `+z` pointing toward the viewer, the crossing sign is

\[
\varepsilon=\operatorname{sign}\det(\mathbf t_{\mathrm{over}},\mathbf t_{\mathrm{under}}).
\]

Under this convention, reversing the orientation of the entire cycle preserves every crossing sign. Mirroring the diagram reverses every sign.

## Tangent estimation

- Primary secant span: **6.0 px**
- Sensitivity spans: `2 px`, `4 px`, `6 px`, `8 px`, `10 px`, `12 px`
- Endpoint tangents are estimated one-sidedly.
- Every tangent is oriented along the frozen cycle traversal.

## Census result

- Crossing events: **31**
- Positive crossings: **0**
- Negative crossings: **31**
- Degenerate signs: **0**
- Writhe: **-31**
- Stable signs across all spans: **31/31**

## Event signs

| Event | Sign | Over-strand | Under-strand | Primary angle | Minimum angle | Stable |
|---|---:|---|---|---:|---:|---|
| `E01` | `−` | Blue S04 | Green S03 | 86.380° | 77.080° | yes |
| `E02` | `−` | Blue S04 | Green S05 | 56.909° | 54.698° | yes |
| `E03` | `−` | Blue S03 | Red S04 | 20.774° | 14.657° | yes |
| `E04` | `−` | Green S06 | Red S04 | 41.439° | 36.161° | yes |
| `E05` | `−` | Red S03 | Green S07 | 31.813° | 29.125° | yes |
| `E06` | `−` | Blue S03 | Green S07 | 69.161° | 64.325° | yes |
| `E07` | `−` | Green S04 | Red S06 | 74.743° | 73.317° | yes |
| `E08` | `−` | Red S07 | Blue S05 | 82.642° | 73.820° | yes |
| `E09` | `−` | Blue S03 | Red S03 | 52.776° | 41.961° | yes |
| `E10` | `−` | Red S05 | Green S05 | 57.247° | 48.218° | yes |
| `E11` | `−` | Green S08 | Blue S02 | 87.228° | 83.366° | yes |
| `E12` | `−` | Blue S01 | Green S08 | 42.680° | 40.320° | yes |
| `E13` | `−` | Red S01 | Green S10 | 34.239° | 32.649° | yes |
| `E14` | `−` | Red S03 | Blue S02 | 82.093° | 74.084° | yes |
| `E15` | `−` | Blue S01 | Red S02 | 31.697° | 30.447° | yes |
| `E16` | `−` | Blue S04 | Green S04 | 76.895° | 56.184° | yes |
| `E17` | `−` | Green S06 | Blue S03 | 44.983° | 30.512° | yes |
| `E18` | `−` | Red S07 | Green S02 | 42.652° | 33.349° | yes |
| `E19` | `−` | Blue S04 | Red S05 | 28.121° | 26.067° | yes |
| `E20` | `−` | Blue S04 | Red S06 | 76.815° | 76.331° | yes |
| `E21` | `−` | Red S01 | Green S09 | 23.774° | 20.640° | yes |
| `E22` | `−` | Green S04 | Green S02 | 84.859° | 84.334° | yes |
| `E23` | `−` | Green S06 | Blue S04 | 64.951° | 46.864° | yes |
| `E24` | `−` | Blue S01 | Red S01 | 20.281° | 20.281° | yes |
| `E25` | `−` | Green S08 | Red S03 | 50.565° | 42.339° | yes |
| `E26` | `−` | Green S08 | Red S02 | 57.677° | 55.008° | yes |
| `E27` | `−` | Blue S01 | Green S09 | 19.214° | 12.715° | yes |
| `E28` | `−` | Green S04 | Red S07 | 69.476° | 63.736° | yes |
| `E29` | `−` | Red S07 | Green S01 | 78.544° | 74.617° | yes |
| `E30` | `−` | Green S04 | Blue S05 | 76.841° | 71.308° | yes |
| `E31` | `−` | Red S07 | Blue S06 | 81.619° | 73.786° | yes |

## Low-angle review set

Events whose minimum sensitivity angle is below `25.0°` are placed into manual review.

| Event | Derived sign | Minimum angle |
|---|---:|---:|
| `E03` | `−` | 14.657° |
| `E21` | `−` | 20.640° |
| `E24` | `−` | 20.281° |
| `E27` | `−` | 12.715° |

## Interpretation boundary

The unanimous sign result is a strong structural property of this reviewed planar projection under the documented convention.

It does not by itself establish:

- the canonical knot type;
- equivalence with the `(3,10)` torus knot;
- minimal crossing number;
- a unique three-dimensional embedding.

The four lowest-angle events must be visually reviewed before the signed Gauss word is frozen.

## Generated outputs

- `data/derived/a10_p03_crossing_signs.csv` (local derived table)
- `data/manual_digitizations/A10_P03/crossing_sign_review.csv`
- `figures/a10_p03_crossing_sign_census.png`
- `figures/a10_p03_crossing_sign_review.png`
