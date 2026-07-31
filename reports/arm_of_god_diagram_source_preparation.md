# *The Arm of God* diagram source preparation

**Status:** Deterministic source-image preparation  
**Primary source:** `AOG_PDF_2005A`  
**Source SHA-256:** `80d52f4b6afefe65ae50e4c01378765c34ae4fde1ad44e8b299870c2e1d3e6fa`  
**Rasterization:** `300 DPI`, RGB, `2550×3300` pixels  
**Renderer:** `pdftoppm version 22.12.0`

## Purpose

Pages 7 and 8 contain the main visual evidence needed to constrain the
First Hand spherical construction:

- the planar reciprocal spiral;
- the labelled spherical great-circle scaffold;
- the three-copy 120-degree Hand region;
- the seven-region torus inset;
- the side and top Hand views;
- and the cube-octahedral unit-angle scaffold.

This checkpoint freezes source excerpts and pixel coordinates before any
landmark fitting, projective calibration, or self-embedment scoring.

## Prepared crops

| Crop ID | Page | Box `(L,T,R,B)` | Output size | Role |
|---|---:|---:|---:|---|
| `AOG_P07_SEVEN_REGION_INSET` | 7 | `(250,750,2220,1070)` | 1970×320 | Seven-region 2-torus inset and its three-turn vortex-edge caption. |
| `AOG_P07_SPHERICAL_PROJECTION` | 7 | `(180,900,2290,2160)` | 2110×1260 | Planar reciprocal spiral beside the labelled cube-octahedral spherical projection. |
| `AOG_P07_HAND_REGION` | 7 | `(220,2050,2280,3070)` | 2060×1020 | Three-copy 120-degree construction and shaded Tefillin Hand region. |
| `AOG_P08_HAND_VIEWS` | 8 | `(350,390,2200,1260)` | 1850×870 | Published side and top views of the Tefillin Hand. |
| `AOG_P08_UNIT_ANGLE_CUBOCTAHEDRON` | 8 | `(300,1250,2250,3000)` | 1950×1750 | Unit-angle discussion and cube-octahedral 30-degree scaffold. |

## Coordinate convention

All crop boxes use the full rendered page coordinate system:

```text
origin:          upper-left pixel
x direction:     right
y direction:     down
box convention:  [left, top, right, bottom)
page raster:     2550 x 3300
resolution:      300 DPI
```

The crop coordinates are source-preparation choices with generous
padding. They are not geometric landmarks and do not encode a preferred
projection model.

## Integrity

Each manifest row records:

- the frozen source-PDF digest;
- the source page and raster resolution;
- the crop box;
- output dimensions;
- PNG file SHA-256;
- canonical RGB pixel SHA-256;
- and the permitted evidential role of the crop.

The full rendered pages are temporary build products and are not
preserved in the repository.

## Scope boundary

This checkpoint does **not**:

- digitize sphere, great-circle, or spiral landmarks;
- calibrate the inverse-gnomonic scale;
- select a projective gauge;
- decide whether the page-7 drawing is metrically exact;
- compute S1, S1.5, or S2;
- or assert correspondence with a physical First Hand artefact.

The next checkpoint must preregister a landmark vocabulary and
measurement protocol before any source-image fitting is performed.
