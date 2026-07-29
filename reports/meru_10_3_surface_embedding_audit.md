# Meru `10_3.wrl` surface-embedding audit

**Status:** Complete numerical simplicial-embedding census  
**Source:** `f24de4a08a_10_3.wrl`  
**SHA-256:** `855c46cfeeb31e4394b7a4a294b397aac4cbc14154e172a326e33243dd9e384b`  
**Result:** **PASS**

## Question

Does the complete native 12,000-triangle surface intersect itself
anywhere beyond the incidences prescribed by its triangle mesh?

## Mesh census

```text
vertices:             6,000
triangles:            12,000
edges:                18,000
Euler characteristic: 0
boundary edges:       0
nonmanifold edges:    0
zero-area triangles:  0
````

The structured tube contains 300 cyclic sections, 20 vertices per
section and 40 triangles per inter-section strip. No face violates that
structured indexing.

## Complete face-pair partition

There are `71,994,000` distinct pairs among the
12,000 triangular faces:

```text
shared-edge pairs:                    18,000
shared-vertex-only pairs:             54,000
vertex-disjoint AABB candidates:      21,622
vertex-disjoint AABB rejections:      71,900,378
total:                                71,994,000
```

Every distinct face pair is therefore assigned to exactly one audited
class.

## Vertex-disjoint faces

The inflated-AABB broad phase produced
`93,622` candidate pairs in total. After
removing legitimate incident pairs, `21,622`
vertex-disjoint pairs underwent the separating-axis narrow phase.

```text
vertex-disjoint overlaps:       0
minimum SAT separation margin:  0.0417362580905
narrow-phase tolerance:         2.20125146224e-08
margin / tolerance:             1.89602e+06
```

No vertex-disjoint triangular faces intersect.

The supplementary structured-tube capsule check first becomes strictly
positive at local exclusion 2, with remote capsule margin
`0.479796008211`.

## Incident faces

All `72,000` incident pairs were checked separately.

### Shared-edge pairs

```text
total:                    18,000
noncoplanar:              17,918
coplanar:                 82
excess intersections:    0
minimum edge sine:        4.68346010415e-06
angular tolerance:        1e-10
sine / tolerance:         46834.6
```

The 82 coplanar shared-edge pairs are legitimate adjacent triangles.
Their interiors lie on opposite sides of the common edge, and no pair
overlaps beyond that edge.

### Shared-vertex-only pairs

```text
total:                    54,000
noncoplanar:              54,000
coplanar:                 0
excess intersections:    0
minimum margin:           0.00173158076295
length tolerance:         2.20125146224e-08
margin / tolerance:       78663.5
```

No shared-vertex-only pair meets anywhere beyond its common vertex.

## Result

Under the recorded tolerance-aware double-precision predicates, the
complete native `10_3.wrl` triangle mesh is a simplicial embedding:

* vertex-disjoint faces are disjoint;
* edge-adjacent faces meet only in their common edge;
* vertex-adjacent faces meet only at their common vertex.

Together with the previously frozen topology audit, this establishes
that Meru's native `10_3.wrl` model is a numerically embedded closed
genus-one triangulated surface surrounding the recovered 3,10
centreline.

## Scope boundary

This is an exhaustive numerical face-pair census with explicit
tolerances and large positive separation margins. It is not a formal
exact-arithmetic proof.

The result certifies the geometry encoded in the recovered native VRML
asset. It does not independently establish every broader interpretive
claim made about the Meru construction.
