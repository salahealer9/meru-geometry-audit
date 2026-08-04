#!/usr/bin/env python3
"""Audit the planar reciprocal spiral and its two source-defined truncations."""

from __future__ import annotations

import csv
import hashlib
import json
import math
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

MANIFEST_PATH = (
    ROOT
    / "data"
    / "source_manifests"
    / "first_hand_arm_of_god"
    / "official_asset_manifest.csv"
)

RAW_SOURCE_PATH = (
    ROOT
    / "data"
    / "source_snapshots"
    / "first_hand_arm_of_god"
    / "raw"
    / "ARMOFGODRef21sep0CPC.2005A.pdf"
)

OUTPUT_PATH = (
    ROOT
    / "data"
    / "derived"
    / "first_hand_arm_of_god"
    / "planar_reciprocal_spiral_audit.json"
)

REPORT_PATH = (
    ROOT
    / "reports"
    / "first_hand_planar_reciprocal_spiral_audit.md"
)

EXPECTED_URL = (
    "https://www.meru.org/NewReleases/"
    "ARMOFGODRef21sep0CPC.2005A.pdf"
)

EXPECTED_SHA256 = (
    "80d52f4b6afefe65ae50e4c01378765"
    "c34ae4fde1ad44e8b299870c2e1d3e6fa"
)

EXPECTED_BYTES = 1_343_797

OUTER_LIMIT_SAMPLES = (
    1.0e-1,
    1.0e-2,
    1.0e-3,
    1.0e-4,
    1.0e-5,
    1.0e-6,
)


def sha256_path(path: Path) -> str:
    """Return the SHA-256 digest of one file."""
    digest = hashlib.sha256()

    with path.open("rb") as handle:
        for block in iter(
            lambda: handle.read(1 << 20),
            b"",
        ):
            digest.update(block)

    return digest.hexdigest()


def read_manifest_row() -> dict[str, str]:
    """Read and validate the single primary-source manifest row."""
    with MANIFEST_PATH.open(
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
            f"Expected one source-manifest row; found {len(rows)}."
        )

    row = rows[0]

    if row["canonical_url"] != EXPECTED_URL:
        raise RuntimeError(
            "The source manifest does not contain the expected canonical URL."
        )

    if row["sha256"] != EXPECTED_SHA256:
        raise RuntimeError(
            "The source manifest does not contain the expected SHA-256."
        )

    if int(row["bytes"]) != EXPECTED_BYTES:
        raise RuntimeError(
            "The source manifest does not contain the expected byte size."
        )

    return row


def gamma(theta: float) -> tuple[float, float]:
    """Return the planar reciprocal spiral in Cartesian coordinates."""
    if theta <= 0.0:
        raise ValueError(
            "theta must be strictly positive."
        )

    radius = 1.0 / theta

    return (
        radius
        * math.cos(
            theta
        ),
        radius
        * math.sin(
            theta
        ),
    )


def derivative(theta: float) -> tuple[float, float]:
    """Return d gamma / d theta."""
    if theta <= 0.0:
        raise ValueError(
            "theta must be strictly positive."
        )

    denominator = (
        theta
        * theta
    )

    return (
        (
            -theta
            * math.sin(
                theta
            )
            - math.cos(
                theta
            )
        )
        / denominator,
        (
            theta
            * math.cos(
                theta
            )
            - math.sin(
                theta
            )
        )
        / denominator,
    )


def oriented_tangent_inner_to_outer(
    theta: float,
) -> tuple[float, float]:
    """Return the unit tangent when theta decreases from inner to outer."""
    derivative_x, derivative_y = derivative(
        theta
    )

    tangent_x = -derivative_x
    tangent_y = -derivative_y

    norm = math.hypot(
        tangent_x,
        tangent_y,
    )

    if norm <= 0.0:
        raise RuntimeError(
            "A zero tangent was encountered."
        )

    return (
        tangent_x / norm,
        tangent_y / norm,
    )


def angle_degrees(
    first: tuple[float, float],
    second: tuple[float, float],
) -> float:
    """Return the directed vector mismatch angle in degrees."""
    dot = (
        first[0]
        * second[0]
        + first[1]
        * second[1]
    )

    dot = min(
        1.0,
        max(
            -1.0,
            dot,
        ),
    )

    return math.degrees(
        math.acos(
            dot
        )
    )


def arc_length_antiderivative(
    theta: float,
) -> float:
    """Return an antiderivative of sqrt(theta^2+1)/theta^2."""
    if theta <= 0.0:
        raise ValueError(
            "theta must be strictly positive."
        )

    return (
        math.asinh(
            theta
        )
        - math.sqrt(
            theta
            * theta
            + 1.0
        )
        / theta
    )


def finite_arc_length(
    theta_outer: float,
    theta_inner: float,
) -> float:
    """Return planar arc length between two finite theta values."""
    if not (
        0.0
        < theta_outer
        < theta_inner
    ):
        raise ValueError(
            "Require 0 < theta_outer < theta_inner."
        )

    return (
        arc_length_antiderivative(
            theta_inner
        )
        - arc_length_antiderivative(
            theta_outer
        )
    )


def point_record(
    theta: float,
) -> dict[str, Any]:
    """Return a deterministic endpoint record."""
    x, y = gamma(
        theta
    )

    tangent = oriented_tangent_inner_to_outer(
        theta
    )

    radius = math.hypot(
        x,
        y,
    )

    return {
        "theta": theta,
        "radius": radius,
        "x": x,
        "y": y,
        "r_times_theta_residual": abs(
            radius
            * theta
            - 1.0
        ),
        "oriented_tangent_inner_to_outer": [
            tangent[0],
            tangent[1],
        ],
    }


manifest = read_manifest_row()

if not RAW_SOURCE_PATH.exists():
    raise RuntimeError(
        f"Missing locally preserved source PDF: {RAW_SOURCE_PATH}"
    )

source_sha256 = sha256_path(
    RAW_SOURCE_PATH
)

source_bytes = RAW_SOURCE_PATH.stat().st_size

if source_sha256 != EXPECTED_SHA256:
    raise RuntimeError(
        "The locally preserved source PDF differs from the frozen source."
    )

if source_bytes != EXPECTED_BYTES:
    raise RuntimeError(
        "The locally preserved source PDF has an unexpected byte size."
    )

outer_limit_records: list[
    dict[str, Any]
] = []

outer_limit_tangent = (
    1.0,
    0.0,
)

for theta in OUTER_LIMIT_SAMPLES:
    x, y = gamma(
        theta
    )

    tangent = oriented_tangent_inner_to_outer(
        theta
    )

    outer_limit_records.append(
        {
            "theta": theta,
            "x": x,
            "y": y,
            "absolute_y_minus_one": abs(
                y
                - 1.0
            ),
            "x_times_theta_minus_one": (
                x
                * theta
                - 1.0
            ),
            "tangent_angle_to_positive_x_degrees": (
                angle_degrees(
                    tangent,
                    outer_limit_tangent,
                )
            ),
        }
    )

theta_prose_inner = (
    3.0
    * math.pi
)

theta_diagram_outer = 1.0

theta_diagram_inner = (
    1.0
    + 3.0
    * math.pi
)

prose_inner = point_record(
    theta_prose_inner
)

diagram_outer = point_record(
    theta_diagram_outer
)

diagram_inner = point_record(
    theta_diagram_inner
)

prose_inner_tangent = tuple(
    prose_inner[
        "oriented_tangent_inner_to_outer"
    ]
)

diagram_outer_tangent = tuple(
    diagram_outer[
        "oriented_tangent_inner_to_outer"
    ]
)

diagram_inner_tangent = tuple(
    diagram_inner[
        "oriented_tangent_inner_to_outer"
    ]
)

prose_tangent_mismatch = angle_degrees(
    prose_inner_tangent,
    outer_limit_tangent,
)

diagram_tangent_mismatch = angle_degrees(
    diagram_inner_tangent,
    diagram_outer_tangent,
)

diagram_arc_length = finite_arc_length(
    theta_diagram_outer,
    theta_diagram_inner,
)

diagram_outer_y1_gap = abs(
    diagram_outer["y"]
    - 1.0
)

result: dict[str, Any] = {
    "source": {
        "asset_id": manifest["asset_id"],
        "canonical_url": EXPECTED_URL,
        "filename": RAW_SOURCE_PATH.name,
        "bytes": source_bytes,
        "sha256": source_sha256,
        "source_pages": [
            5,
            6,
            7,
        ],
    },
    "curve": {
        "name": "unitary reciprocal spiral",
        "polar_equation": "r*theta=1",
        "radius_function": "r(theta)=1/theta",
        "cartesian_parameterization": [
            "x(theta)=cos(theta)/theta",
            "y(theta)=sin(theta)/theta",
        ],
        "parameter_domain": "theta>0",
        "orientation_for_endpoint_tests": (
            "inner-to-outer, corresponding to decreasing theta"
        ),
    },
    "analytic_limits": {
        "theta_to_zero_positive": {
            "x": "positive infinity",
            "y": 1.0,
            "radius": "positive infinity",
            "oriented_tangent_inner_to_outer": [
                1.0,
                0.0,
            ],
            "planar_arc_length_to_limit": "diverges",
        },
        "theta_to_positive_infinity": {
            "x": 0.0,
            "y": 0.0,
            "radius": 0.0,
        },
        "numerical_outer_limit_samples": (
            outer_limit_records
        ),
    },
    "truncation_variants": {
        "AOG_PROSE": {
            "source_interpretation": (
                "the inner endpoint is 3*pi radians from "
                "the projected asymptotic outer end"
            ),
            "theta_outer": "0+",
            "theta_inner": theta_prose_inner,
            "angular_span_radians": (
                3.0
                * math.pi
            ),
            "turns": 1.5,
            "outer_endpoint": {
                "type": "asymptotic planar endpoint",
                "x": "positive infinity",
                "y": 1.0,
                "oriented_tangent_inner_to_outer": [
                    1.0,
                    0.0,
                ],
            },
            "inner_endpoint": prose_inner,
            "planar_arc_length": "infinite",
            "directed_planar_tangent_mismatch_degrees": (
                prose_tangent_mismatch
            ),
        },
        "AOG_DIAGRAM": {
            "source_interpretation": (
                "the marked unit point theta=1 begins a "
                "3*pi-radian finite interval"
            ),
            "theta_outer": theta_diagram_outer,
            "theta_inner": theta_diagram_inner,
            "angular_span_radians": (
                theta_diagram_inner
                - theta_diagram_outer
            ),
            "turns": (
                (
                    theta_diagram_inner
                    - theta_diagram_outer
                )
                / (
                    2.0
                    * math.pi
                )
            ),
            "outer_endpoint": diagram_outer,
            "inner_endpoint": diagram_inner,
            "finite_planar_arc_length": (
                diagram_arc_length
            ),
            "outer_endpoint_absolute_y_minus_one": (
                diagram_outer_y1_gap
            ),
            "directed_planar_tangent_mismatch_degrees": (
                diagram_tangent_mismatch
            ),
        },
    },
    "checks": {
        "source_identity_pass": True,
        "reciprocal_relation_max_residual": max(
            (
                prose_inner[
                    "r_times_theta_residual"
                ],
                diagram_outer[
                    "r_times_theta_residual"
                ],
                diagram_inner[
                    "r_times_theta_residual"
                ],
            )
        ),
        "outer_limit_y_convergence_pass": (
            outer_limit_records[-1][
                "absolute_y_minus_one"
            ]
            < 1.0e-12
        ),
        "outer_limit_tangent_convergence_pass": (
            outer_limit_records[-1][
                "tangent_angle_to_positive_x_degrees"
            ]
            < 1.0e-6
        ),
        "prose_angular_span_is_three_pi": True,
        "diagram_angular_span_is_three_pi": (
            abs(
                (
                    theta_diagram_inner
                    - theta_diagram_outer
                )
                - 3.0
                * math.pi
            )
            < 1.0e-14
        ),
        "variants_are_distinct": True,
    },
    "scope": {
        "self_embedment_verdict": None,
        "s1_endpoint_alignment_verdict": None,
        "s1_5_frame_alignment_verdict": None,
        "s2_recursive_nesting_verdict": None,
        "reason_no_self_embedment_verdict": (
            "the source-level claim concerns the compactified "
            "spherical or dimpled-surface construction, whose "
            "coordinate map has not yet been frozen"
        ),
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

report = rf"""# First Hand planar reciprocal-spiral audit

**Status:** Deterministic planar baseline  
**Primary source:** `{manifest["asset_id"]}`  
**Source SHA-256:** `{source_sha256}`  
**Result:** Planar generator reproduced; no self-embedment verdict

## Source-defined curve

The source identifies the unitary reciprocal spiral

\[
r\theta=1,
\qquad
r(\theta)=\frac{{1}}{{\theta}},
\qquad
\theta>0.
\]

In Cartesian coordinates:

\[
\gamma(\theta)
=
\left(
\frac{{\cos\theta}}{{\theta}},
\frac{{\sin\theta}}{{\theta}}
\right).
\]

All endpoint tangents below use the orientation from the inner spiral
end toward the outer end. Since the inner endpoint has larger
\(\theta\), this orientation corresponds to decreasing \(\theta\).

## Analytic asymptotes

As \(\theta\to0^+\):

```text
x(theta) -> +infinity
y(theta) -> 1
r(theta) -> +infinity
oriented tangent -> (+1, 0)
planar arc length -> infinity
```

As \(\theta\to+\infinity\):

```text
x(theta) -> 0
y(theta) -> 0
r(theta) -> 0
```

The paper's point-to-line description is therefore mathematically
correct for the planar reciprocal spiral.

## Frozen truncation A — prose/asymptotic reading

```text
outer theta:       0+  (asymptotic)
inner theta:       3*pi
angular span:      3*pi
turns:             1.5
inner radius:      {prose_inner["radius"]:.15g}
inner position:    ({prose_inner["x"]:.15g}, {prose_inner["y"]:.15g})
planar arc length: infinite
```

The directed planar endpoint-tangent mismatch is:

```text
{prose_tangent_mismatch:.12g} degrees
```

This is not a self-embedment result because the source explicitly
compactifies the outer end through a spherical projection.

## Frozen truncation B — diagram/unit-point reading

```text
outer theta:       1
inner theta:       1 + 3*pi = {theta_diagram_inner:.15g}
angular span:      3*pi
turns:             1.5
outer position:    ({diagram_outer["x"]:.15g}, {diagram_outer["y"]:.15g})
inner position:    ({diagram_inner["x"]:.15g}, {diagram_inner["y"]:.15g})
planar arc length: {diagram_arc_length:.15g}
```

The marked unit point has \(r=1\) and \(\theta=1\), but its Cartesian
height is

```text
y(1) = sin(1) = {diagram_outer["y"]:.15g}
|y(1)-1| = {diagram_outer_y1_gap:.15g}
```

It is therefore near, but not on, the asymptotic line \(y=1\).

The directed planar endpoint-tangent mismatch is:

```text
{diagram_tangent_mismatch:.12g} degrees
```

Again, this does not decide the spherical self-embedment claim.

## What has been established

- The planar equation is reproduced without fitted parameters.
- The point-to-line asymptotes are verified.
- Both source-supported intervals span exactly \(3\pi\), or 1.5 turns.
- The prose and diagram endpoint conventions define materially
  different finite curve segments.
- Their planar endpoint positions, tangents and arc lengths are now
  frozen for later spherical reconstruction.

## Scope boundary

No S1, S1.5 or S2 verdict is issued here.

The endpoint-alignment claim concerns the compactified spherical or
dimpled-surface construction. Testing it in the plane would answer a
different question and would unfairly reject a claim whose defining
operation has not yet been reconstructed.

The next phase must freeze candidate flat-to-sphere maps using the
source's great-circle constraints and page-7 diagram before inspecting
any self-embedment score.
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
print("FIRST HAND PLANAR RECIPROCAL-SPIRAL AUDIT")
print("=" * 78)
print(
    "Source:                         "
    f"{RAW_SOURCE_PATH.name}"
)
print(
    "AOG-PROSE inner theta:          "
    f"{theta_prose_inner:.12g}"
)
print(
    "AOG-PROSE tangent mismatch:     "
    f"{prose_tangent_mismatch:.12g} deg"
)
print(
    "AOG-DIAGRAM inner theta:        "
    f"{theta_diagram_inner:.12g}"
)
print(
    "AOG-DIAGRAM finite arc length:  "
    f"{diagram_arc_length:.12g}"
)
print(
    "AOG-DIAGRAM y=1 gap:            "
    f"{diagram_outer_y1_gap:.12g}"
)
print(
    "AOG-DIAGRAM tangent mismatch:   "
    f"{diagram_tangent_mismatch:.12g} deg"
)
print(
    "Self-embedment verdict:         "
    "DEFERRED TO SPHERICAL MAP"
)
print(
    f"Wrote {OUTPUT_PATH}"
)
print(
    f"Wrote {REPORT_PATH}"
)
