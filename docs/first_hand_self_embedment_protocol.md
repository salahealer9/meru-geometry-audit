# First Hand construction and self-embedment protocol

**Version:** v0.8.0 Phase 0  
**Status:** Source-led preregistration architecture  
**Primary source:** `AOG_PDF_2005A`

## Primary research question

Do the public Meru sources define one or more reproducible First Hand
constructions, and do any of those constructions satisfy increasingly
strong geometric self-embedment predicates?

No claim is accepted or rejected solely because one source statement is
ambiguous. Every materially supported interpretation is reconstructed
separately.

No undocumented parameter may be adjusted solely to improve the final
self-embedment score.

## Frozen construction variants

### Variant P — planar reciprocal spiral

The source equation is

```text
r * theta = 1
r(theta) = 1 / theta
````

### Variant A — spherical construction

The planar reciprocal spiral is mapped to a smooth spherical coordinate
surface carrying the cube-octahedral great-circle framework shown in
the primary source.

The map is not yet frozen. Candidate maps must be selected from source
constraints and diagram correspondence before self-embedment results
are inspected.

### Truncation A — prose/asymptotic reading

The angular separation from the projected asymptotic outer endpoint to
the inner endpoint is `3*pi`.

This initially corresponds to:

```text
theta_outer -> 0+
theta_inner = 3*pi
```

The limiting endpoint must be handled analytically through the chosen
spherical compactification.

### Truncation B — diagram/unit-point reading

The marked finite unit point is:

```text
theta_outer = 1
r_outer = 1
```

and the inner endpoint is:

```text
theta_inner = 1 + 3*pi
r_inner = 1 / (1 + 3*pi)
```

The two truncation variants must not be silently merged.

## Projection-map selection rule

A candidate spherical map may be admitted only when it satisfies the
source-level constraints frozen before self-embedment testing:

1. the planar x-axis maps to a great circle;
2. the planar line y=1 maps to a great circle;
3. the two distinguished great circles meet at the stated equatorial
   finite image of the planar infinite end;
4. the resulting curve agrees structurally with the page-7 diagram;
5. the map is applied identically to reciprocal and comparator curves.

Where multiple maps survive, every surviving map is retained as a
separate construction variant.

## Self-embedment predicates

Let the oriented curve run from its inner endpoint to its outer
endpoint.

### S1 — directed endpoint-tangent alignment

```text
alpha_T = arccos(T_inner dot T_outer)
```

Antiparallel tangents do not pass.

A numerical threshold will be frozen in the execution preregistration
after the analytic map and numerical error model are fixed, but before
the construction results are evaluated.

### S1.5 — full endpoint-frame alignment

For a curve constrained to a surface, define its oriented Darboux
frame:

```text
T = unit tangent
N = oriented surface normal
B = N cross T
```

S1.5 requires compatibility of the complete endpoint frames under the
proposed nesting transformation. Tangent agreement alone is
insufficient because it leaves a free rotation about the tangent axis.

### S2 — collision-free recursive nesting

A similarity map

```text
F(x) = s R x + a
```

must place a smaller copy at the designated endpoint while satisfying:

1. endpoint coincidence;
2. directed tangent agreement;
3. complete frame agreement;
4. containment in the intended host region;
5. no improper intersections;
6. positive numerical clearance;
7. coherent repeated application.

Passing S1 does not imply S1.5, and passing S1.5 does not imply S2.

## Comparator rule

Every comparator receives the same:

* host surface;
* projection map;
* truncation convention;
* normalization;
* endpoint definitions;
* parameter-search budget;
* numerical tolerances;
* and pass/fail predicates.

Initial comparator families are:

* golden logarithmic spiral;
* general logarithmic spirals over a preregistered growth-rate range;
* Archimedean spiral;
* matched smooth control curves.

## Seven-region claim

The seven-region torus claim remains a separate reconstruction problem.

No regular seven-region torus map may be substituted for the source
diagram without first demonstrating source correspondence.

## Interpretation boundary

The protocol tests geometric construction, endpoint alignment, frame
alignment and recursive nesting.

It does not test the theological, historical or linguistic truth of
the metaphors used to motivate the construction.

Letter generation remains a documented Meru claim, but visual alphabet
resemblance alone is not treated as evidence that the construction is
mathematically unique.
