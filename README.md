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
- automated geometric, topological-boundary, and group-theoretic tests;
- reproducible three-dimensional and projection visualisations.

Not yet implemented:

- dimpled spherical-torus reconstruction;
- finite-width ribbon or flame geometry;
- source-derived Meru surface parameters;
- alphabet target data;
- silhouette extraction;
- shape-comparison metrics;
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

`v0.4.0 — Canonical torus and candidate embedding baseline`

This checkpoint contains:

- the verified source-reconstruction boundary;
- the exact tetrahedral rotation and projection framework;
- a canonical ring-torus parametrisation;
- a coprime \((p,q)\) torus-knot implementation;
- the exact mathematical \((3,10)\) baseline;
- candidate C0 for mapping the reciprocal spiral onto a torus;
- automated surface, closure, and embedding tests;
- reproducible three-dimensional and tetrahedral-projection figures.

The candidate C0 embedding is explicitly an inferred mathematical baseline,
not a faithful reconstruction of the unresolved Meru flame.

## Author

Salah-Eddin Gherbi
Independent Researcher, United Kingdom
ORCID: 0009-0005-4017-1095
