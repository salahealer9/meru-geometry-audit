# Meru digital 3,10 source catalogue

**Retrieval date:** 2026-07-29  
**Status:** Native digital primary sources recovered  
**Repository policy:** Source bytes retained locally and excluded from Git

## Purpose

This catalogue records the official Meru web pages, rotating animation
and native VRML assets recovered for the audit of the published
“3,10 torus knot” construction.

The assets were retrieved directly from URLs under `meru.org`.
SHA-256 hashes identify the exact local research copies used in the
audit.

## Recovered resources

| Resource | Role | Bytes | SHA-256 | Technical detail |
|---|---|---:|---|---|
| `3-10knot.html` | official source page | 14478 | `957714d2540fe71988f39dfc64fa995aa74a01aafc1e43c8f7a493c245c289dc` | retrieved official HTML page |
| `animatedgif.html` | official source page | 21181 | `0f3d46f74445bd0f0828349166ca539ab27678e706e73f91d3a983fa694deb2d` | retrieved official HTML page |
| `animations.html` | official source page | 18357 | `1d68b1bdd7fa74bd1107635eb7b5b2c096123594d8ed370d807703b7c979e9d7` | retrieved official HTML page |
| `tumble.gif` | rotating rendered animation | 957858 | `a61a01353d51d3c09bc57b8c5f13d4923a5f020d7dd35f33b466e2b282ea3303` | GIF 320x240; 96 frames |
| `1_3-3_1B.wrl` | companion native 3-D model candidate | 198807 | `82833c46baddc1b6709a7ff9b7e9c81692203eed7cda63d5b9792dd9ac42ba3a` | #VRML V2.0 utf8 |
| `10_3.wrl` | primary native 3-D model candidate | 429161 | `855c46cfeeb31e4394b7a4a294b397aac4cbc14154e172a326e33243dd9e384b` | #VRML V2.0 utf8 |

## Primary native-model candidate

The file `10_3.wrl` is the principal native-model candidate because it
is explicitly linked by the official Meru computer-animation material
and its filename corresponds to the published 10/3 or 3/10 object.

This filename and source context identify the author's intended asset.
They do not by themselves prove that the encoded geometry is
topologically equivalent to the mathematical torus knot T(3,10).

## Separate 3-around-1 / 1-around-3 asset

The file `1_3-3_1B.wrl` is linked by Meru under the separate
“3-Around-1 and 1-Around-3” construction associated with its Tree of
Life research. It is not presented as an alternative native model of
the 3,10 torus knot.

Direct structural inspection finds two closed genus-one tube meshes
and eight marker spheres. The asset remains catalogued as contextual
Meru source material, but it is excluded from the A10_P03-to-3,10
model correspondence analysis.

## Source-preservation policy

The downloaded HTML, GIF and VRML bytes are third-party source
materials. They remain in the locally ignored directory:

```text
data/source_snapshots/meru_3_10_digital/raw/
````

The public repository tracks only:

* canonical source URLs;
* retrieval metadata;
* media types and byte counts;
* cryptographic hashes;
* format information;
* and independently generated audit outputs.

## Interpretive boundary

The rotating GIF demonstrates that Meru published a coherent
computer-rendered three-dimensional construction. It does not by
itself determine:

* how many topological components the native model contains;
* whether the visible coloured surfaces are ribbons, tubes or separate
  objects;
* whether a unique centreline is explicitly encoded;
* whether the construction is embedded without self-intersection;
* whether it is isotopic to T(3,10);
* or whether it corresponds exactly to the hand-drawn A10_P03 panel.

Those questions require direct structural and topological analysis of
the VRML geometry.

## Next audit stage

The next stage will parse both VRML files and record:

* VRML node and transform structure;
* coordinate arrays and indexed geometry;
* material groups;
* connected mesh components;
* boundary components;
* animation nodes and routes;
* and any explicit or recoverable closed curve candidates.

No knot-type conclusion will be made from the published label alone.
