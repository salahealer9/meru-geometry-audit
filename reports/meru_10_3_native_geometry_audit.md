# Meru `10_3.wrl` native geometry audit

**Status:** Frozen source-derived native-geometry audit  
**Source:** `https://www.meru.org/compuimages/10_3.wrl`  
**Source SHA-256:** `855c46cfeeb31e4394b7a4a294b397aac4cbc14154e172a326e33243dd9e384b`  
**Source policy:** local untracked third-party research copy

## Purpose

This audit examines Meru's recovered native VRML asset directly rather
than inferring its hidden geometry solely from the hand-drawn A10_P03
panel.

The third-party source bytes remain locally excluded from Git. The
tracked manifest, this audit script, the derived JSON metrics and this
report make the analysis reproducible for a researcher possessing the
same SHA-256-identified source file.

## Native mesh structure

The VRML asset contains one `IndexedFaceSet` with:

```text
vertices: 6000
edges:    18000
faces:    12000
chi:      0
````

The mesh audit finds:

```text
connected components:    1
boundary edges:          0
non-manifold edges:      0
orientation conflicts:   0
zero-area triangles:     0
candidate genus:         1
```

It is therefore a connected, closed, consistently oriented
combinatorial genus-one surface.

## Source-defined tube parameterisation

The vertex indexing resolves unambiguously into:

```text
300 consecutive cross-sections
x 20 vertices per section
= 6000 vertices
```

The consecutive sections are nearly planar and circular:

```text
mean section radius:       5.0009260727
median section radius:     5.00128316563
section-radius CV:         0.00112822080977
median planarity ratio:    0.00698603492871
median circularity ratio:  1.00260250955
closure-step ratio:        0.982391506911
```

Their centroids define a source-derived closed polygonal centreline with
300 stations. No invented centreline fit
is required.

## Centreline embeddedness

The complete nonadjacent segment-pair census gives:

```text
nonadjacent intersections:  0
minimum remote distance:    14.8745406922
minimum remote pair:        [82, 172]
median tube diameter:       10.0025663313
clearance / diameter:       1.48707243717
```

Under the stated tolerance of
`1e-08`, the polygonal centreline is
embedded.

## Toroidal winding

The best toroidal coordinate axis is the model's
`y` axis.

```text
major winding:         3
minor winding:         -10
signed rounded pair:   [3, -10]
unsigned pair:         [3, 10]
major reversals:       0
minor reversals:       0
```

Both toroidal phases are monotonic. The recovered signed pair is
`(3,-10)` under the audit's coordinate convention, while the unsigned
pair is exactly `{3,10}`.

### Dominant transverse Fourier modes

|          Frequency | Amplitude |
| -----------------: | --------: |
| | 3 | 40.8244354151 |
| -7 | 9.81492905101 |
| 13 | 9.81347184126 |
| 23 | 2.35984831184 |
| -17 | 2.35968254277 |
| 33 | 0.567219140589 | |           |

### Dominant axial Fourier modes

|     Frequency | Amplitude |
| ------------: | --------: |
| | 10 | 19.2342539169 |
| -10 | 19.2342539169 |
| -20 | 4.62301643437 |
| 20 | 4.62301643437 |
| 30 | 1.11271277892 |
| -30 | 1.11271277892 | |           |

The transverse fundamental at frequency 3, its sidebands at
`3-10=-7` and `3+10=13`, and the axial fundamental at frequency 10
independently support the same winding interpretation.

## Conclusion

Meru's native `10_3.wrl` asset encodes a connected closed genus-one
tube whose source-defined cross-section centroids form an embedded
polygonal toroidal centreline. Relative to the recovered y-axis
toroidal coordinates, that centreline has monotonic winding pair
`(3,-10)` and unsigned pair `{3,10}`.

The published “3,10” designation is therefore encoded directly in the
native geometry rather than existing only as an accompanying label.
Under the stated toroidal-coordinate interpretation, the source
supports an embedded unsigned `T(3,10)` construction, with orientation
and chirality conventions kept explicit.

## Interpretive boundary

This result does not yet identify which complete model crossings are
suppressed in A10_P03. It also does not yet provide:

* a full model-to-panel viewpoint and crossing correspondence;
* an all-pairs triangle-triangle self-intersection certificate for the
  surrounding tube mesh;
* or a separately derived knot-diagram invariant fixing chirality.

The parity failure of the hand-derived A10_P03 visible word therefore
remains a valid demonstration that the 31-event sequence is incomplete
as a classical planar projection. Direct model-to-panel comparison is
the next stage.
