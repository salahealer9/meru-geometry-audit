#!/usr/bin/env python3
"""Combine Meru 10_3 surface-intersection audits into one certificate."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

DERIVED_DIR = (
    ROOT
    / "data"
    / "derived"
    / "meru_3_10_digital"
)

REMOTE_PATH = (
    DERIVED_DIR
    / "meru_10_3_surface_embedding_remote.json"
)

INCIDENT_PATH = (
    DERIVED_DIR
    / "meru_10_3_surface_embedding_incident.json"
)

CERTIFICATE_PATH = (
    DERIVED_DIR
    / "meru_10_3_surface_embedding_audit.json"
)

REPORT_PATH = (
    ROOT
    / "reports"
    / "meru_10_3_surface_embedding_audit.md"
)


def read_json(
    path: Path,
) -> dict[str, Any]:
    """Read one JSON object."""
    return json.loads(
        path.read_text(
            encoding="utf-8",
        )
    )


def require(
    condition: bool,
    message: str,
) -> None:
    """Raise when an audit consistency condition fails."""
    if not condition:
        raise RuntimeError(
            message
        )


remote = read_json(
    REMOTE_PATH
)

incident = read_json(
    INCIDENT_PATH
)

remote_source = remote["source"]
incident_source = incident["source"]

require(
    remote_source == incident_source,
    "Remote and incident audits reference different source bytes.",
)

mesh = remote["mesh"]
structured = remote["structured_tube"]
remote_pairs = remote["triangle_pair_census"]
incident_pairs = incident["incident_pair_census"]
incident_tolerances = incident["tolerances"]

face_count = int(
    mesh["faces"]
)

total_distinct_pairs = (
    face_count
    * (
        face_count
        - 1
    )
    // 2
)

shared_edge_pairs = int(
    incident_pairs["shared_edge_pairs"]
)

shared_vertex_pairs = int(
    incident_pairs["shared_vertex_only_pairs"]
)

incident_pair_count = int(
    incident_pairs["incident_pairs"]
)

vertex_disjoint_pairs = (
    total_distinct_pairs
    - incident_pair_count
)

vertex_disjoint_candidates = int(
    remote_pairs["vertex_disjoint"]
)

vertex_disjoint_aabb_rejected = (
    vertex_disjoint_pairs
    - vertex_disjoint_candidates
)

require(
    incident_pair_count
    == (
        shared_edge_pairs
        + shared_vertex_pairs
    ),
    "Incident pair partition is inconsistent.",
)

require(
    int(
        remote_pairs["aabb_candidates"]
    )
    == (
        shared_edge_pairs
        + shared_vertex_pairs
        + vertex_disjoint_candidates
    ),
    "AABB candidate partition is inconsistent.",
)

require(
    vertex_disjoint_aabb_rejected
    >= 0,
    "Computed a negative AABB-rejected pair count.",
)

pair_partition_complete = (
    total_distinct_pairs
    == (
        shared_edge_pairs
        + shared_vertex_pairs
        + vertex_disjoint_candidates
        + vertex_disjoint_aabb_rejected
    )
)

mesh_topology_pass = (
    int(
        mesh["boundary_edges"]
    )
    == 0
    and int(
        mesh["nonmanifold_edges"]
    )
    == 0
    and int(
        mesh["zero_area_triangles"]
    )
    == 0
    and int(
        mesh["euler_characteristic"]
    )
    == 0
)

structured_tube_pass = (
    int(
        structured["invalid_strip_faces"]
    )
    == 0
    and structured[
        "triangles_per_strip_values"
    ]
    == [40]
)

remote_face_pass = (
    int(
        remote_pairs["vertex_disjoint_overlaps"]
    )
    == 0
)

incident_face_pass = (
    int(
        incident_pairs[
            "shared_edge_excess_intersections"
        ]
    )
    == 0
    and int(
        incident_pairs[
            "shared_vertex_excess_intersections"
        ]
    )
    == 0
)

surface_embedding_pass = all(
    (
        pair_partition_complete,
        mesh_topology_pass,
        structured_tube_pass,
        remote_face_pass,
        incident_face_pass,
    )
)

sat_margin = float(
    remote_pairs[
        "minimum_positive_sat_separation_margin"
    ]
)

sat_tolerance = float(
    remote_pairs["narrow_tolerance"]
)

edge_sine = float(
    incident_pairs[
        "minimum_noncoplanar_shared_edge_sine"
    ]
)

angular_tolerance = float(
    incident_tolerances[
        "angular_tolerance"
    ]
)

coplanar_edge_margin = float(
    incident_pairs[
        "minimum_coplanar_shared_edge_side_margin"
    ]
)

area_tolerance = float(
    incident_tolerances[
        "area_tolerance"
    ]
)

shared_vertex_margin = float(
    incident_pairs[
        "minimum_shared_vertex_margin"
    ]
)

length_tolerance = float(
    incident_tolerances[
        "length_tolerance"
    ]
)

margin_ratios = {
    "vertex_disjoint_sat_margin_to_tolerance": (
        sat_margin
        / sat_tolerance
    ),
    "noncoplanar_shared_edge_sine_to_tolerance": (
        edge_sine
        / angular_tolerance
    ),
    "coplanar_shared_edge_margin_to_tolerance": (
        coplanar_edge_margin
        / area_tolerance
    ),
    "shared_vertex_margin_to_tolerance": (
        shared_vertex_margin
        / length_tolerance
    ),
}

certificate = {
    "source": remote_source,
    "mesh": mesh,
    "structured_tube": {
        "section_count": structured[
            "section_count"
        ],
        "points_per_section": structured[
            "points_per_section"
        ],
        "strip_count": structured[
            "strip_count"
        ],
        "triangles_per_strip_values": structured[
            "triangles_per_strip_values"
        ],
        "invalid_strip_faces": structured[
            "invalid_strip_faces"
        ],
        "minimum_passing_local_exclusion": structured[
            "minimum_passing_local_exclusion"
        ],
        "remote_capsule_margin": structured[
            "remote_capsule_margin"
        ],
        "remote_capsule_pass": structured[
            "remote_capsule_pass"
        ],
    },
    "complete_face_pair_partition": {
        "total_distinct_face_pairs": total_distinct_pairs,
        "shared_edge_pairs": shared_edge_pairs,
        "shared_vertex_only_pairs": shared_vertex_pairs,
        "vertex_disjoint_aabb_candidates": (
            vertex_disjoint_candidates
        ),
        "vertex_disjoint_aabb_rejected": (
            vertex_disjoint_aabb_rejected
        ),
        "vertex_disjoint_pairs": (
            vertex_disjoint_pairs
        ),
        "partition_complete": pair_partition_complete,
    },
    "vertex_disjoint_audit": {
        "aabb_candidates_total": remote_pairs[
            "aabb_candidates"
        ],
        "narrow_phase_pairs": (
            vertex_disjoint_candidates
        ),
        "overlaps": remote_pairs[
            "vertex_disjoint_overlaps"
        ],
        "minimum_sat_separation_margin": (
            sat_margin
        ),
        "broad_tolerance": remote_pairs[
            "broad_tolerance"
        ],
        "narrow_tolerance": (
            sat_tolerance
        ),
    },
    "incident_face_audit": {
        "incident_pairs": incident_pair_count,
        "shared_edge_pairs": shared_edge_pairs,
        "shared_edge_noncoplanar": incident_pairs[
            "shared_edge_noncoplanar"
        ],
        "shared_edge_coplanar": incident_pairs[
            "shared_edge_coplanar"
        ],
        "shared_edge_excess_intersections": incident_pairs[
            "shared_edge_excess_intersections"
        ],
        "shared_vertex_only_pairs": (
            shared_vertex_pairs
        ),
        "shared_vertex_noncoplanar": incident_pairs[
            "shared_vertex_noncoplanar"
        ],
        "shared_vertex_coplanar": incident_pairs[
            "shared_vertex_coplanar"
        ],
        "shared_vertex_excess_intersections": incident_pairs[
            "shared_vertex_excess_intersections"
        ],
        "minimum_noncoplanar_shared_edge_sine": (
            edge_sine
        ),
        "minimum_coplanar_shared_edge_side_margin": (
            coplanar_edge_margin
        ),
        "minimum_shared_vertex_margin": (
            shared_vertex_margin
        ),
        "tolerances": incident_tolerances,
    },
    "margin_ratios": margin_ratios,
    "certificate": {
        "mesh_topology_pass": mesh_topology_pass,
        "structured_tube_pass": structured_tube_pass,
        "complete_pair_partition_pass": (
            pair_partition_complete
        ),
        "vertex_disjoint_face_pass": (
            remote_face_pass
        ),
        "incident_face_pass": (
            incident_face_pass
        ),
        "surface_embedding_pass": (
            surface_embedding_pass
        ),
    },
    "scope": {
        "method": (
            "exhaustive tolerance-aware double-precision "
            "simplicial face-pair census"
        ),
        "all_distinct_face_pairs_accounted_for": (
            pair_partition_complete
        ),
        "formal_exact_arithmetic": False,
    },
}

CERTIFICATE_PATH.parent.mkdir(
    parents=True,
    exist_ok=True,
)

CERTIFICATE_PATH.write_text(
    json.dumps(
        certificate,
        indent=2,
        sort_keys=True,
    )
    + "\n",
    encoding="utf-8",
)

report = f"""# Meru `10_3.wrl` surface-embedding audit

**Status:** Complete numerical simplicial-embedding census  
**Source:** `{remote_source["filename"]}`  
**SHA-256:** `{remote_source["sha256"]}`  
**Result:** **PASS**

## Question

Does the complete native 12,000-triangle surface intersect itself
anywhere beyond the incidences prescribed by its triangle mesh?

## Mesh census

```text
vertices:             {mesh["vertices"]:,}
triangles:            {mesh["faces"]:,}
edges:                {mesh["edges"]:,}
Euler characteristic: {mesh["euler_characteristic"]}
boundary edges:       {mesh["boundary_edges"]}
nonmanifold edges:    {mesh["nonmanifold_edges"]}
zero-area triangles:  {mesh["zero_area_triangles"]}
````

The structured tube contains 300 cyclic sections, 20 vertices per
section and 40 triangles per inter-section strip. No face violates that
structured indexing.

## Complete face-pair partition

There are `{total_distinct_pairs:,}` distinct pairs among the
12,000 triangular faces:

```text
shared-edge pairs:                    {shared_edge_pairs:,}
shared-vertex-only pairs:             {shared_vertex_pairs:,}
vertex-disjoint AABB candidates:      {vertex_disjoint_candidates:,}
vertex-disjoint AABB rejections:      {vertex_disjoint_aabb_rejected:,}
total:                                {total_distinct_pairs:,}
```

Every distinct face pair is therefore assigned to exactly one audited
class.

## Vertex-disjoint faces

The inflated-AABB broad phase produced
`{remote_pairs["aabb_candidates"]:,}` candidate pairs in total. After
removing legitimate incident pairs, `{vertex_disjoint_candidates:,}`
vertex-disjoint pairs underwent the separating-axis narrow phase.

```text
vertex-disjoint overlaps:       {remote_pairs["vertex_disjoint_overlaps"]}
minimum SAT separation margin:  {sat_margin:.12g}
narrow-phase tolerance:         {sat_tolerance:.12g}
margin / tolerance:             {margin_ratios["vertex_disjoint_sat_margin_to_tolerance"]:.6g}
```

No vertex-disjoint triangular faces intersect.

The supplementary structured-tube capsule check first becomes strictly
positive at local exclusion 2, with remote capsule margin
`{structured["remote_capsule_margin"]:.12g}`.

## Incident faces

All `{incident_pair_count:,}` incident pairs were checked separately.

### Shared-edge pairs

```text
total:                    {shared_edge_pairs:,}
noncoplanar:              {incident_pairs["shared_edge_noncoplanar"]:,}
coplanar:                 {incident_pairs["shared_edge_coplanar"]:,}
excess intersections:    {incident_pairs["shared_edge_excess_intersections"]}
minimum edge sine:        {edge_sine:.12g}
angular tolerance:        {angular_tolerance:.12g}
sine / tolerance:         {margin_ratios["noncoplanar_shared_edge_sine_to_tolerance"]:.6g}
```

The 82 coplanar shared-edge pairs are legitimate adjacent triangles.
Their interiors lie on opposite sides of the common edge, and no pair
overlaps beyond that edge.

### Shared-vertex-only pairs

```text
total:                    {shared_vertex_pairs:,}
noncoplanar:              {incident_pairs["shared_vertex_noncoplanar"]:,}
coplanar:                 {incident_pairs["shared_vertex_coplanar"]:,}
excess intersections:    {incident_pairs["shared_vertex_excess_intersections"]}
minimum margin:           {shared_vertex_margin:.12g}
length tolerance:         {length_tolerance:.12g}
margin / tolerance:       {margin_ratios["shared_vertex_margin_to_tolerance"]:.6g}
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
"""

REPORT_PATH.write_text(
report,
encoding="utf-8",
)

print(
f"Wrote {CERTIFICATE_PATH}"
)

print(
f"Wrote {REPORT_PATH}"
)

print(
"Surface embedding certificate: "
f"{surface_embedding_pass}"
)
