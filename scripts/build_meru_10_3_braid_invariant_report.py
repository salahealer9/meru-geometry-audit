#!/usr/bin/env python3
"""Build the human-readable Meru 10_3 braid and invariant report."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

AUDIT_PATH = (
    ROOT
    / "data"
    / "derived"
    / "meru_3_10_digital"
    / "meru_10_3_braid_invariant_audit.json"
)

REPORT_PATH = (
    ROOT
    / "reports"
    / "meru_10_3_braid_invariant_audit.md"
)


def read_json(path: Path) -> dict[str, Any]:
    """Read one JSON object."""
    return json.loads(
        path.read_text(
            encoding="utf-8",
        )
    )


audit = read_json(
    AUDIT_PATH
)

source = audit["source"]
centreline = audit["centreline"]
projection = audit["braid_projection"]
braid = audit["braid"]
alexander = audit["alexander"]
scope = audit["scope"]

expected_word = [
    value
    for _ in range(10)
    for value in (
        -2,
        -1,
    )
]

checks = {
    "source_identity": (
        source["sha256"]
        == (
            "855c46cfeeb31e4394b7a4a294b397aa"
            "c4cbc14154e172a326e33243dd9e384b"
        )
    ),
    "crossing_count": (
        projection["crossing_count"]
        == 20
    ),
    "negative_torus_braid_word": (
        braid["signed_word"]
        == expected_word
        and braid[
            "negative_3_10_torus_pattern_up_to_cyclic_shift"
        ]
        is True
    ),
    "single_component_closure": (
        braid["closure_component_count"]
        == 1
    ),
    "alexander_match": (
        alexander["matches_T_3_10"]
        is True
    ),
    "generic_projection": (
        projection["minimum_crossing_margin_at_breakpoints"]
        > 1.0
        and projection["minimum_depth_gap"]
        > 30.0
        and projection["minimum_third_strand_projection_gap"]
        > 40.0
        and projection["minimum_event_to_breakpoint_margin"]
        > 0.005
    ),
}

certificate_pass = all(
    checks.values()
)

if not certificate_pass:
    failed = [
        name
        for name, passed in checks.items()
        if not passed
    ]

    raise RuntimeError(
        "Braid certificate failed: "
        + ", ".join(
            failed
        )
    )

word_latex = (
    r"(\sigma_2^{-1}\sigma_1^{-1})^{10}"
)

polynomial = alexander[
    "computed_polynomial"
]

report = rf"""# Meru `10_3.wrl` braid and knot-invariant audit

**Status:** Complete numerical braid reconstruction  
**Source:** `{source["filename"]}`  
**SHA-256:** `{source["sha256"]}`  
**Result:** **PASS**

## Question

Does the native centreline independently encode a three-strand torus
braid of type 3,10, without relying on the asset filename, Meru's written
designation or the earlier toroidal winding fit?

## Centreline and phase convention

The centreline is recovered as the centroid of each of the
{centreline["section_count"]} consecutive tube sections, each containing
{centreline["points_per_section"]} vertices.

The closed braid uses the following recorded convention:

```text
braid axis:             {projection["axis"]}
phase coordinate:       {projection["phase_coordinate"]}
diagram coordinate:     {projection["diagram_coordinate"]}
depth coordinate:       {projection["depth_coordinate"]}
viewer convention:      {projection["viewer_convention"]}
strand order:           {projection["strand_order_convention"]}
positive generator:     {projection["positive_generator_convention"]}
```

The native traversal was reversed to make the phase coordinate strictly
increasing:

```text
orientation reversed:   {centreline["orientation_reversed_for_increasing_phase"]}
minimum azimuth step:   {centreline["minimum_azimuth_step"]:.12g}
maximum azimuth step:   {centreline["maximum_azimuth_step"]:.12g}
major turns:            {centreline["exact_major_turns_used_for_closure"]}
```

This reversal fixes the traversal convention used to record the braid.
It does not change the underlying unoriented knot type.

## Exhaustive piecewise-linear crossing census

The phase origin was selected away from a crossing. The three projected
strand functions were then partitioned at the union of all native
piecewise-linear breakpoints, and every strand pair was tested on every
interval.

```text
piecewise-linear breakpoints:       {projection["piecewise_linear_breakpoint_count"]}
crossings:                           {projection["crossing_count"]}
start projection margin:            {projection["start_projection_margin"]:.12g}
minimum breakpoint crossing margin: {projection["minimum_crossing_margin_at_breakpoints"]:.12g}
minimum over/under depth gap:        {projection["minimum_depth_gap"]:.12g}
minimum third-strand gap:            {projection["minimum_third_strand_projection_gap"]:.12g}
minimum event/breakpoint gap:        {projection["minimum_event_to_breakpoint_margin"]:.12g}
```

All crossings are isolated from breakpoints, have a large nonzero depth
ordering and remain well separated from the third strand.

## Recovered braid

The signed word is

\[
\beta = {word_latex}.
\]

In explicit generator order:

```text
{braid["word_text"]}
```

Its diagnostics are:

```text
crossing number:       {projection["crossing_count"]}
writhe:                {braid["writhe"]}
induced permutation:   {braid["induced_permutation"]}
closure components:    {braid["closure_component_count"]}
all negative:          {braid["all_negative"]}
negative 3,10 pattern: {braid["negative_3_10_torus_pattern_up_to_cyclic_shift"]}
```

The closure permutation has one cycle, so the braid closes to one knot
rather than a multi-component link.

Under the exact projection and generator conventions recorded above,
the native centreline is the negative three-strand torus braid
\((\sigma_2^{{-1}}\sigma_1^{{-1}})^{{10}}\). Relative to the usual
positive braid convention, this is the mirror-handed representative of
the standard 3,10 torus knot. This handedness statement is
convention-relative: reflecting the diagram or reversing the chosen
viewing convention reverses every generator sign.

## Alexander polynomial

The reduced Burau calculation gives

```text
Delta(t) = {polynomial}
degree   = {alexander["degree"]}
|Delta(-1)| = {alexander["determinant_absolute_delta_minus_one"]}
```

The result agrees exactly with the torus-knot formula for \(T(3,10)\):

```text
{alexander["expected_T_3_10_polynomial"]}
```

The Alexander polynomial is mirror-insensitive and is not, by itself, a
unique classifier of all knots. Here it is an independent invariant
check supporting the stronger result supplied by the exact recovered
braid word.

## Result

The native `10_3.wrl` centreline independently yields:

- an exhaustive 20-crossing generic three-braid projection;
- the signed word
  \((\sigma_2^{{-1}}\sigma_1^{{-1}})^{{10}}\);
- a one-component closure;
- and the Alexander polynomial of \(T(3,10)\).

The published “3,10” designation is therefore encoded directly in the
native centreline both as a toroidal winding structure and as an
independently reconstructed braid and knot invariant.

## Scope boundary

This is a deterministic, tolerance-aware double-precision audit of the
piecewise-linear centreline. It is not a formal exact-arithmetic proof.

The signed chirality result is tied to the explicitly recorded phase,
viewing and generator conventions. The Alexander polynomial does not
distinguish a knot from its mirror image.

The result certifies the topology of the recovered native digital
geometry. It does not independently establish broader linguistic,
cosmological or consciousness-related interpretations attached to the
Meru model.
"""

REPORT_PATH.parent.mkdir(
    parents=True,
    exist_ok=True,
)

REPORT_PATH.write_text(
    report,
    encoding="utf-8",
)

print(
    f"Wrote {REPORT_PATH}"
)

print(
    "Braid and invariant certificate: "
    f"{certificate_pass}"
)
