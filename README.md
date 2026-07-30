# Meru Geometry Audit

A reproducible mathematical audit of the geometrical and combinatorial claims
associated with Stan Tenen's Meru Foundation research.

## Central research question

Does the geometry described by Stan Tenen provide a sufficiently specified
three-dimensional generator whose constrained projections reproduce the Hebrew
alphabet significantly better than matched geometric controls?

## Initial scope

The project will examine:

- the reciprocal spiral \(r=a/\theta\);
- alternative spiral turn counts;
- toroidal and dimpled spherical-torus embeddings;
- regular tetrahedral geometry;
- tetrahedral rotations;
- two-dimensional projections and silhouettes;
- claimed Hebrew-letter correspondences;
- ternary encoding of the 27 Hebrew forms;
- spatial arrangements of Genesis 1:1;
- the claimed \((3,10)\) torus-knot and tetrahelix construction;
- objective shape metrics and matched null models.

## Evidence boundary

This repository tests mathematical, geometrical, combinatorial, and statistical
claims.

A successful reconstruction would not by itself establish:

- extraterrestrial authorship;
- ancient-contact narratives;
- theological interpretations;
- anomalous physical effects of language;
- claims that words directly create matter or life.

See [`docs/claims/evidence_boundary.md`](docs/claims/evidence_boundary.md).

## Current status

The repository is currently at the geometric-baseline stage.

Implemented:

- reproducible primary-source manifests and checksums;
- formal claim register and evidence boundary;
- historical model-version separation;
- planar reciprocal spiral;
- regular tetrahedron with unit-circumradius normalisation;
- all 12 proper tetrahedral rotations;
- vertex-permutation representation of the rotation group;
- orthographic projection;
- canonical ring-torus parametrisation;
- standard coprime torus-knot parametrisation;
- exact baseline implementation of the \((3,10)\) torus knot;
- candidate C0 reciprocal-radius-to-poloidal-angle embedding;
- exact camera-direction orbit classification;
- signed and unoriented viewing-axis multiplicities;
- SO(2) and O(2) planar similarity alignment;
- cyclic-shift and traversal-reversal handling for closed curves;
- object-specific projection-equivalence classification;
- automated geometric, group-theoretic, and orbit-analysis tests;
- reproducible three-dimensional, projection, and error-matrix figures.

Not yet implemented:

- dimpled spherical-torus reconstruction;
- finite-width ribbon or flame geometry;
- source-derived Meru surface parameters;
- historical alphabet target data;
- silhouette extraction from finite-width models;
- broader shape-comparison metrics;
- geometric null models;
- confirmatory letter-matching tests.

## Repository structure

```text
docs/
  claims/          Formal claims, evidence boundaries, and model versions
  source_audit/    Primary-source chronology and extraction notes

data/
  raw/             Unmodified source-derived data
  derived/         Reproducible generated data

src/meru_geometry/
  reciprocal_spiral.py
  torus.py
  dimpled_torus.py
  embeddings.py
  tetrahedron.py
  rotations.py
  projections.py
  silhouettes.py
  letterforms.py
  shape_metrics.py
  null_models.py
  statistics.py

scripts/           Reproducible command-line analyses
figures/           Generated figures
tests/             Automated tests
references/        Bibliographic and source notes
````

## Installation

```bash
python3 -m venv .venv
source .venv/bin/activate

python -m pip install --upgrade pip
python -m pip install -e .
```

For development:

```bash
python -m pip install -e ".[dev]"
```

## Run the baseline

Generate the reciprocal-spiral figure:

```bash
python scripts/plot_reciprocal_spiral.py
```

Run the tests:

```bash
python -m pytest -q
```

## Reconstruction policy

Where an original source leaves a geometric choice unspecified, the project
will distinguish clearly between:

* faithful reconstructions;
* inferred reconstructions;
* candidate variants;
* sensitivity tests;
* mathematical controls;
* null models.

No inferred parameter will be silently presented as part of Tenen's original
construction.

## Current development checkpoint

`v0.6.0 — Source-derived A10 closed-cycle reconstruction`

The v0.6.0 checkpoint reconstructs the visible two-dimensional connectivity
of the completed dimpled-sphere knot drawing in source panel A10_P03.

Main result:

- 24 visible coloured fragments;
- 21 manually adjudicated same-colour continuations;
- 3 manually adjudicated cross-colour transitions;
- 48 endpoint vertices and 48 graph edges;
- one connected component;
- degree 2 at every endpoint vertex;
- one connected, non-branched closed cycle containing every visible fragment.

Canonical cycle traversal:

```text
R:S01+ → R:S02+ → R:S03+ → R:S04− → R:S05+ → R:S06− →
R:S07+ → G:S11− → G:S10− → G:S09− → G:S08− → G:S07+ →
G:S06− → G:S05− → G:S04− → G:S03+ → G:S02− → G:S01− →
B:S01+ → B:S02− → B:S03+ → B:S04+ → B:S05+ → B:S06+
```

Reproduce the exact audit with:

```bash
python scripts/audit_a10_p03_global_cycle.py
```

The result establishes source-supported planar connectivity. It does not yet
establish a unique three-dimensional embedding, dimpled-surface equation,
complete crossing-depth assignment, equivalence with the canonical `(3,10)`
torus knot, or the claimed Hebrew-letter projection system.

`v0.5.0 — Tetrahedral projection-orbit audit`

This checkpoint contains:

- the verified source-reconstruction boundary;
- the tetrahedron, torus, and candidate-embedding baselines;
- exact recovery of the six signed tetrahedral camera directions;
- exact recovery of the three unoriented viewing axes;
- planar similarity alignment under SO(2) and O(2);
- cyclic-shift and traversal-reversal handling for closed curves;
- projection-class audits of the diagnostic probe, \((3,10)\) knot,
  and candidate C0;
- reproducible projection and pairwise-error figures;
- a generated mathematical results report.

The 12 proper tetrahedral rotations are therefore not interpreted as 12
independent viewing directions.

## Author

Salah-Eddin Gherbi
Independent Researcher, United Kingdom
ORCID: 0009-0005-4017-1095

<!-- v0.7.0-result-summary:start -->
## v0.7.0 — native Meru 3,10 geometry certificate

Version `v0.7.0` separates source correspondence from mathematical
certification and establishes the strongest source-grounded result of
the audit so far.

### Main findings

- Meru's native `10_3.wrl` asset is a closed, consistently oriented
  genus-one triangulated tube with 6,000 vertices, 12,000 triangular
  faces and 18,000 edges.
- The source-defined centreline has signed toroidal winding `(3, -10)`
  under the recorded coordinate convention and unsigned winding pair
  `{3, 10}`.
- An exhaustive tolerance-aware census accounts for all 71,994,000
  distinct face pairs and finds no surface intersections beyond the
  shared edges and vertices prescribed by the mesh.
- An independent piecewise-linear braid reconstruction gives

  \[
  (\sigma_2^{-1}\sigma_1^{-1})^{10},
  \]

  with 20 crossings, writhe `-20`, a one-component closure and the
  Alexander polynomial of \(T(3,10)\).
- A10_P03 is classified as a simplified schematic corresponding
  structurally to a vertically reflected `tumble.gif` frame `000`.
  It is not treated as a complete classical knot diagram.

### Principal reports

- [`reports/meru_10_3_native_geometry_audit.md`](reports/meru_10_3_native_geometry_audit.md)
- [`reports/meru_10_3_surface_embedding_audit.md`](reports/meru_10_3_surface_embedding_audit.md)
- [`reports/meru_10_3_braid_invariant_audit.md`](reports/meru_10_3_braid_invariant_audit.md)
- [`reports/A10_P03_tumble_correspondence.md`](reports/A10_P03_tumble_correspondence.md)

### Interpretation boundary

The geometric results are deterministic, source-identified and
reproducible, but they are numerical rather than formal
exact-arithmetic proofs. The negative braid signs are relative to the
explicitly recorded phase, viewing and generator conventions.

These results certify the topology and embedding of the recovered
native digital geometry. They do not independently establish broader
linguistic, cosmological, extraterrestrial or consciousness-related
claims associated with the Meru material.
<!-- v0.7.0-result-summary:end -->
