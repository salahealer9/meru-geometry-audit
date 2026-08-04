#!/usr/bin/env python3
"""Certify the source-constrained spherical-map family for v0.8.0.

This audit promotes the exploratory spherical-map census into a permanent,
deterministic result. It tests source-level incidence constraints only. It
does not calculate endpoint self-embedment scores.
"""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path
from typing import Any, Callable

import numpy as np


ROOT = Path(__file__).resolve().parents[1]

MANIFEST_PATH = (
    ROOT
    / "data"
    / "source_manifests"
    / "first_hand_arm_of_god"
    / "official_asset_manifest.csv"
)

PLANAR_AUDIT_PATH = (
    ROOT
    / "data"
    / "derived"
    / "first_hand_arm_of_god"
    / "planar_reciprocal_spiral_audit.json"
)

OUTPUT_PATH = (
    ROOT
    / "data"
    / "derived"
    / "first_hand_arm_of_god"
    / "spherical_map_family_audit.json"
)

REPORT_PATH = (
    ROOT
    / "reports"
    / "first_hand_spherical_map_family_audit.md"
)

EXPECTED_ASSET_ID = "AOG_PDF_2005A"

EXPECTED_SHA256 = (
    "80d52f4b6afefe65ae50e4c01378765"
    "c34ae4fde1ad44e8b299870c2e1d3e6fa"
)

LINE_SAMPLE_COUNT = 2001
LINE_EXTENT = 20.0
INFINITY_RADIUS = 1.0e7

RESIDUAL_TOLERANCE = 1.0e-12
INFINITY_TOLERANCE = 2.0e-7

Vector = np.ndarray
MapFunction = Callable[[float, float], Vector]


def unit(vector: Vector) -> Vector:
    """Return a normalized vector."""
    norm = float(
        np.linalg.norm(
            vector
        )
    )

    if norm <= 0.0:
        raise ValueError(
            "Cannot normalize a zero vector."
        )

    return vector / norm


def read_single_csv_row(
    path: Path,
) -> dict[str, str]:
    """Read one-row CSV metadata."""
    with path.open(
        newline="",
        encoding="utf-8",
    ) as handle:
        rows = list(
            csv.DictReader(
                handle
            )
        )

    if len(rows) != 1:
        raise RuntimeError(
            f"Expected one row in {path}; found {len(rows)}."
        )

    return rows[0]


def inverse_gnomonic(
    x: float,
    y: float,
    *,
    scale: float,
) -> Vector:
    """Map the affine plane to the upper hemisphere by central projection."""
    if scale <= 0.0:
        raise ValueError(
            "scale must be positive."
        )

    return unit(
        np.array(
            [
                scale * x,
                scale * y,
                1.0,
            ],
            dtype=float,
        )
    )


def inverse_stereographic(
    x: float,
    y: float,
    *,
    scale: float,
) -> Vector:
    """Map the affine plane to the unit sphere by inverse stereography."""
    if scale <= 0.0:
        raise ValueError(
            "scale must be positive."
        )

    u = scale * x
    v = scale * y

    denominator = (
        1.0
        + u * u
        + v * v
    )

    return np.array(
        [
            2.0 * u / denominator,
            2.0 * v / denominator,
            (
                1.0
                - u * u
                - v * v
            )
            / denominator,
        ],
        dtype=float,
    )


def best_origin_plane_normal(
    points: Vector,
) -> tuple[Vector, float, float]:
    """Fit a plane through the sphere centre and return residual diagnostics."""
    if points.ndim != 2 or points.shape[1] != 3:
        raise ValueError(
            "points must have shape (n, 3)."
        )

    _, _, vh = np.linalg.svd(
        points,
        full_matrices=False,
    )

    normal = unit(
        vh[-1]
    )

    signed = points @ normal

    rms = float(
        np.sqrt(
            np.mean(
                signed * signed
            )
        )
    )

    maximum = float(
        np.max(
            np.abs(
                signed
            )
        )
    )

    return (
        normal,
        rms,
        maximum,
    )


def sample_source_line(
    map_function: MapFunction,
    line_id: str,
) -> Vector:
    """Sample one source-labelled planar line and map it to the sphere."""
    parameter = np.linspace(
        -LINE_EXTENT,
        LINE_EXTENT,
        LINE_SAMPLE_COUNT,
        dtype=float,
    )

    planar_points: list[
        tuple[float, float]
    ] = []

    if line_id == "x_axis":
        planar_points = [
            (
                float(value),
                0.0,
            )
            for value in parameter
        ]
    elif line_id == "y_axis":
        planar_points = [
            (
                0.0,
                float(value),
            )
            for value in parameter
        ]
    elif line_id == "x_equals_1":
        planar_points = [
            (
                1.0,
                float(value),
            )
            for value in parameter
        ]
    elif line_id == "y_equals_1":
        planar_points = [
            (
                float(value),
                1.0,
            )
            for value in parameter
        ]
    else:
        raise ValueError(
            f"Unknown line ID: {line_id}"
        )

    return np.vstack(
        [
            map_function(
                x,
                y,
            )
            for x, y in planar_points
        ]
    )


def line_audit(
    map_function: MapFunction,
) -> dict[str, dict[str, Any]]:
    """Audit the four source-labelled planar lines."""
    result: dict[
        str,
        dict[str, Any],
    ] = {}

    for line_id in (
        "x_axis",
        "y_axis",
        "x_equals_1",
        "y_equals_1",
    ):
        points = sample_source_line(
            map_function,
            line_id,
        )

        normal, rms, maximum = (
            best_origin_plane_normal(
                points
            )
        )

        result[line_id] = {
            "best_origin_plane_normal": (
                normal.tolist()
            ),
            "great_circle_rms_residual": rms,
            "great_circle_max_abs_residual": maximum,
            "passes": (
                maximum
                <= RESIDUAL_TOLERANCE
            ),
        }

    return result


def infinity_audit(
    map_function: MapFunction,
) -> dict[str, Any]:
    """Audit positive projective-infinity behaviour in two planar directions."""
    radius = INFINITY_RADIUS

    horizontal_x_axis = map_function(
        radius,
        0.0,
    )

    horizontal_y_equals_1 = map_function(
        radius,
        1.0,
    )

    vertical_y_axis = map_function(
        0.0,
        radius,
    )

    vertical_x_equals_1 = map_function(
        1.0,
        radius,
    )

    horizontal_pair_distance = float(
        np.linalg.norm(
            horizontal_x_axis
            - horizontal_y_equals_1
        )
    )

    vertical_pair_distance = float(
        np.linalg.norm(
            vertical_y_axis
            - vertical_x_equals_1
        )
    )

    horizontal_equator_residual = float(
        max(
            abs(
                horizontal_x_axis[2]
            ),
            abs(
                horizontal_y_equals_1[2]
            ),
        )
    )

    vertical_equator_residual = float(
        max(
            abs(
                vertical_y_axis[2]
            ),
            abs(
                vertical_x_equals_1[2]
            ),
        )
    )

    infinity_direction_dot = float(
        np.dot(
            horizontal_x_axis,
            vertical_y_axis,
        )
    )

    return {
        "positive_horizontal_parallel_pair_distance": (
            horizontal_pair_distance
        ),
        "positive_vertical_parallel_pair_distance": (
            vertical_pair_distance
        ),
        "horizontal_equator_max_abs_z": (
            horizontal_equator_residual
        ),
        "vertical_equator_max_abs_z": (
            vertical_equator_residual
        ),
        "horizontal_vertical_infinity_direction_dot": (
            infinity_direction_dot
        ),
        "parallel_positive_ends_coalesce": (
            horizontal_pair_distance
            <= INFINITY_TOLERANCE
            and vertical_pair_distance
            <= INFINITY_TOLERANCE
        ),
        "positive_ends_approach_equator": (
            horizontal_equator_residual
            <= INFINITY_TOLERANCE
            and vertical_equator_residual
            <= INFINITY_TOLERANCE
        ),
        "distinguished_infinity_directions_remain_distinct": (
            abs(
                infinity_direction_dot
            )
            <= INFINITY_TOLERANCE
        ),
    }


def evaluate_map(
    name: str,
    map_function: MapFunction,
) -> dict[str, Any]:
    """Evaluate one candidate map without self-embedment scoring."""
    lines = line_audit(
        map_function
    )

    infinity = infinity_audit(
        map_function
    )

    all_lines_pass = all(
        item["passes"]
        for item in lines.values()
    )

    all_infinity_constraints_pass = all(
        (
            infinity[
                "parallel_positive_ends_coalesce"
            ],
            infinity[
                "positive_ends_approach_equator"
            ],
            infinity[
                "distinguished_infinity_directions_remain_distinct"
            ],
        )
    )

    return {
        "name": name,
        "line_constraints": lines,
        "infinity_constraints": infinity,
        "all_source_incidence_constraints_pass": (
            all_lines_pass
            and all_infinity_constraints_pass
        ),
        "self_embedment_scores_computed": False,
    }


manifest = read_single_csv_row(
    MANIFEST_PATH
)

if manifest["asset_id"] != EXPECTED_ASSET_ID:
    raise RuntimeError(
        "Unexpected primary-source asset ID."
    )

if manifest["sha256"] != EXPECTED_SHA256:
    raise RuntimeError(
        "Unexpected primary-source SHA-256."
    )

planar_audit = json.loads(
    PLANAR_AUDIT_PATH.read_text(
        encoding="utf-8",
    )
)

if (
    planar_audit["source"]["sha256"]
    != EXPECTED_SHA256
):
    raise RuntimeError(
        "The planar audit and source manifest do not agree."
    )

scale_hypotheses = {
    "G30": {
        "scale": math.tan(
            math.radians(
                30.0
            )
        ),
        "unit_radius_central_angle_radians": (
            math.radians(
                30.0
            )
        ),
        "source_role": (
            "hypothesis motivated by the page-8 "
            "30-degree cube-octahedral division"
        ),
    },
    "GHALF": {
        "scale": math.tan(
            0.5
        ),
        "unit_radius_central_angle_radians": 0.5,
        "source_role": (
            "hypothesis motivated by the page-8 "
            "half-radian candidate"
        ),
    },
    "GUNIT": {
        "scale": 1.0,
        "unit_radius_central_angle_radians": (
            math.pi
            / 4.0
        ),
        "source_role": (
            "neutral affine scale baseline"
        ),
    },
    "GONE": {
        "scale": math.tan(
            1.0
        ),
        "unit_radius_central_angle_radians": 1.0,
        "source_role": (
            "hypothesis in which unit planar radius maps "
            "to one radian of central angle"
        ),
    },
}

gnomonic_variants: dict[
    str,
    dict[str, Any],
] = {}

for hypothesis_id, hypothesis in (
    scale_hypotheses.items()
):
    scale = float(
        hypothesis["scale"]
    )

    result = evaluate_map(
        name=(
            "inverse_gnomonic_"
            f"{hypothesis_id}"
        ),
        map_function=lambda x, y, scale=scale: (
            inverse_gnomonic(
                x,
                y,
                scale=scale,
            )
        ),
    )

    result["scale_hypothesis"] = (
        hypothesis
    )

    gnomonic_variants[
        hypothesis_id
    ] = result

stereographic_comparator = evaluate_map(
    name="inverse_stereographic_unit_scale",
    map_function=lambda x, y: (
        inverse_stereographic(
            x,
            y,
            scale=1.0,
        )
    ),
)

all_gnomonic_variants_pass = all(
    variant[
        "all_source_incidence_constraints_pass"
    ]
    for variant in gnomonic_variants.values()
)

gnomonic_max_line_residual = max(
    line_result[
        "great_circle_max_abs_residual"
    ]
    for variant in gnomonic_variants.values()
    for line_result in variant[
        "line_constraints"
    ].values()
)

stereographic_offset_line_rms = {
    line_id: (
        stereographic_comparator[
            "line_constraints"
        ][line_id][
            "great_circle_rms_residual"
        ]
    )
    for line_id in (
        "x_equals_1",
        "y_equals_1",
    )
}

result: dict[str, Any] = {
    "source": {
        "asset_id": manifest["asset_id"],
        "sha256": manifest["sha256"],
        "source_pages": [
            7,
            8,
        ],
    },
    "source_constraints_tested": {
        "labelled_planar_lines": [
            "x_axis",
            "y_axis",
            "x_equals_1",
            "y_equals_1",
        ],
        "mapped_lines_are_great_circles": True,
        "parallel_positive_ends_meet_at_finite_equatorial_points": True,
        "horizontal_and_vertical_infinity_directions_are_distinct": True,
    },
    "canonical_family": {
        "name": "isotropic inverse gnomonic family",
        "formula": (
            "M_k(x,y)=normalize((k*x,k*y,1)), k>0"
        ),
        "mathematical_status": (
            "all affine lines map to planes through the "
            "sphere centre and therefore to great circles"
        ),
        "scale_identified_by_incidence_constraints": False,
        "scale_hypotheses": (
            scale_hypotheses
        ),
        "variant_results": (
            gnomonic_variants
        ),
    },
    "broader_projective_family": {
        "formula": (
            "M_A(x,y)=normalize(A @ (x,y,1)), "
            "where A is invertible"
        ),
        "line_to_great_circle_proof": (
            "for planar line l^T p=0 and X parallel to A p, "
            "(A^{-T} l)^T X=0, a plane through the sphere centre"
        ),
        "implication": (
            "the source incidence statements select a "
            "central-projective class, not a unique coordinate map"
        ),
        "anisotropy_shear_and_projective_gauge_excluded_by_current_constraints": (
            False
        ),
        "global_spherical_rotation_identified": False,
    },
    "comparator": (
        stereographic_comparator
    ),
    "checks": {
        "source_identity_pass": True,
        "planar_audit_dependency_pass": True,
        "all_tested_gnomonic_scales_pass": (
            all_gnomonic_variants_pass
        ),
        "gnomonic_max_line_residual": (
            gnomonic_max_line_residual
        ),
        "stereographic_offset_lines_fail": all(
            residual
            > 1.0e-2
            for residual in (
                stereographic_offset_line_rms.values()
            )
        ),
        "unique_map_identified": False,
        "scale_calibrated": False,
        "self_embedment_scores_computed": False,
    },
    "interpretation": {
        "primary_source_constrained_candidate": (
            "inverse gnomonic / central-projective family"
        ),
        "verdict": (
            "the inverse gnomonic family satisfies the "
            "tested source incidence constraints exactly "
            "to numerical precision; inverse stereography does not"
        ),
        "non_verdict": (
            "this does not prove that Tenen used one unique "
            "gnomonic formula or fix the affine scale"
        ),
        "next_required_step": (
            "source-image calibration of projective gauge, "
            "orientation, and scale before any S1 score"
        ),
    },
    "scope": {
        "s1_endpoint_alignment_verdict": None,
        "s1_5_frame_alignment_verdict": None,
        "s2_recursive_nesting_verdict": None,
        "formal_exact_arithmetic": False,
    },
}

OUTPUT_PATH.parent.mkdir(
    parents=True,
    exist_ok=True,
)

OUTPUT_PATH.write_text(
    json.dumps(
        result,
        indent=2,
        sort_keys=True,
    )
    + "\n",
    encoding="utf-8",
)

g30 = scale_hypotheses["G30"]
ghalf = scale_hypotheses["GHALF"]

report = rf"""# First Hand spherical-map family audit

**Status:** Source-incidence certificate  
**Primary source:** `{manifest["asset_id"]}`  
**Source SHA-256:** `{manifest["sha256"]}`  
**Result:** A central-projective family is supported; no unique map or scale is certified

## Source constraints

The page-7 construction labels the planar lines

```text
x-axis
y-axis
x=1
y=1
```

as great-circle projections on a spherical coordinate surface. It also
states that the planar infinite end becomes finite where the relevant
great circles reach the equator.

This checkpoint tests only those incidence and infinity statements.

## Canonical candidate

The isotropic inverse gnomonic family is

\[
M_k(x,y)
=
\frac{{(kx,ky,1)}}
{{\sqrt{{k^2x^2+k^2y^2+1}}}},
\qquad
k>0.
\]

For every planar affine line

\[
ax+by+c=0,
\]

its image lies in

\[
\frac{{a}}{{k}}X
+
\frac{{b}}{{k}}Y
+
cZ
=
0.
\]

That plane passes through the sphere centre, so the image is a great
circle. This is an exact geometric property, not a fitted numerical
coincidence.

All four tested scales pass the source-incidence constraints:

| ID | \(k\) | central angle of planar unit radius | status |
|---|---:|---:|---|
| G30 | {g30["scale"]:.15g} | 30 degrees | PASS |
| GHALF | {ghalf["scale"]:.15g} | 0.5 radians | PASS |
| GUNIT | 1 | 45 degrees | PASS |
| GONE | {scale_hypotheses["GONE"]["scale"]:.15g} | 1 radian | PASS |

The maximum tested line-to-great-circle residual is

```text
{gnomonic_max_line_residual:.15g}
```

## Why the map is not unique

More generally, for any invertible matrix \(A\),

\[
M_A(x,y)
=
\operatorname{{normalize}}
\left(
A
\begin{{bmatrix}}
x\\y\\1
\end{{bmatrix}}
\right)
\]

maps planar lines to great circles.

For a planar line \(\ell^Tp=0\), the spherical image satisfies

\[
(A^{{-T}}\ell)^TX=0,
\]

which is again a plane through the sphere centre.

Therefore the source's line-incidence statements identify a
central-projective class. They do not, by themselves, eliminate
anisotropy, shear, projective gauge freedom, global spherical rotation,
or the scale \(k\).

The isotropic inverse gnomonic map is the simplest canonical member of
that class, not yet a uniquely recovered historical formula.

## Stereographic comparator

Inverse stereography correctly maps the planar coordinate axes through
the projection origin to great circles. It does not map the offset
lines \(x=1\) and \(y=1\) to great circles.

Their fitted great-circle RMS residuals are:

```text
x=1: {stereographic_offset_line_rms["x_equals_1"]:.15g}
y=1: {stereographic_offset_line_rms["y_equals_1"]:.15g}
```

It also sends planar infinity to the stereographic pole rather than to
the distinct equatorial directions depicted in the source.

Thus inverse stereography fails the tested page-7 incidence model.

## Angular-scale caution

Page 8 discusses both a 30-degree cube-octahedral division and
approximately half a radian as candidates for one unit angle.

Those statements motivate G30 and GHALF, but do not prove that the
planar reciprocal-spiral parameter unit is identical to the affine
scale \(k\) in the spherical map. The two quantities remain separate
until the source diagrams are calibrated.

No scale is selected by endpoint alignment in this checkpoint.

## Result boundary

Established:

- a central-projective map class satisfies the source incidence model;
- isotropic inverse gnomonic maps are canonical valid members;
- inverse stereography is not compatible with the tested offset-line
  great-circle statements;
- all tested isotropic scales remain observationally equivalent under
  incidence constraints alone.

Not established:

- one unique historical projection formula;
- projective gauge, anisotropy, orientation, or scale;
- correspondence to the drawn spiral silhouette;
- S1 tangent alignment;
- S1.5 frame alignment;
- S2 recursive nesting.

The next phase is source-image calibration. It must estimate projective
gauge and scale from the page-7 and page-8 drawings without using any
self-embedment score as a fitting objective.
"""

REPORT_PATH.parent.mkdir(
    parents=True,
    exist_ok=True,
)

REPORT_PATH.write_text(
    report,
    encoding="utf-8",
)

print("=" * 78)
print("FIRST HAND SPHERICAL-MAP FAMILY AUDIT")
print("=" * 78)
print(
    "Primary source-constrained class: "
    "central-projective / inverse-gnomonic-compatible"
)
print(
    "All tested gnomonic scales pass:  "
    f"{all_gnomonic_variants_pass}"
)
print(
    "Maximum gnomonic line residual:   "
    f"{gnomonic_max_line_residual:.12g}"
)
print(
    "Stereographic x=1 RMS residual:   "
    f"{stereographic_offset_line_rms['x_equals_1']:.12g}"
)
print(
    "Stereographic y=1 RMS residual:   "
    f"{stereographic_offset_line_rms['y_equals_1']:.12g}"
)
print(
    "Unique map identified:            False"
)
print(
    "Scale calibrated:                 False"
)
print(
    "Self-embedment scores computed:   False"
)
print(
    f"Wrote {OUTPUT_PATH}"
)
print(
    f"Wrote {REPORT_PATH}"
)
