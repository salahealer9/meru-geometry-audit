# Changelog

<!-- v0.7.0-changelog:start -->
## [0.7.0] — 2026-07-30

### Added

- Official Meru digital-source catalogue with frozen source identities,
  sizes and SHA-256 hashes.
- Native `10_3.wrl` centreline recovery from the 300 consecutive
  20-vertex tube sections.
- Deterministic toroidal winding audit.
- Exhaustive numerical surface-embedding certificate for the complete
  12,000-triangle tube.
- Independent three-strand braid reconstruction and Alexander
  polynomial audit.
- A10_P03–`tumble.gif` schematic correspondence record.
- Regression tests covering source identity, topology, embedding,
  braid structure, knot invariant and interpretation boundaries.

### Verified

- 6,000 vertices, 12,000 triangular faces and 18,000 mesh edges.
- Closed, connected and consistently oriented genus-one mesh.
- Signed toroidal winding `(3, -10)` and unsigned pair `{3, 10}`.
- All 71,994,000 distinct triangular-face pairs accounted for.
- Zero vertex-disjoint face intersections.
- Zero excess intersections among shared-edge and shared-vertex face
  pairs.
- Recovered braid
  `(\sigma_2^-1 sigma_1^-1)^10`.
- Twenty crossings, writhe `-20` and one-component braid closure.
- Alexander polynomial equal to the \(T(3,10)\) polynomial, with degree
  18 and `|Delta(-1)| = 3`.
- Full regression suite: 227 tests passing.

### Clarified

- A10_P03 is a simplified schematic, not a complete planar knot
  diagram.
- `tumble.gif`, `10_3.wrl` and A10_P03 are related Meru
  representations but are not metrically identical geometries.
- `1_3-3_1B.wrl` belongs to the separate 3-around-1 / 1-around-3
  construction and is excluded from the 3,10 correspondence audit.
- Chirality statements are convention-relative.
- Numerical certificates are not described as formal exact-arithmetic
  proofs.
<!-- v0.7.0-changelog:end -->
