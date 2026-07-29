#!/usr/bin/env python3
"""Audit whether incident Meru 10_3 mesh faces meet only in shared simplices."""

from __future__ import annotations

import csv
import hashlib
import itertools
import json
import math
import re
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]

MANIFEST = (
    ROOT
    / "data"
    / "source_manifests"
    / "meru_3_10_digital"
    / "official_asset_manifest.csv"
)

RAW = (
    ROOT
    / "data"
    / "source_snapshots"
    / "meru_3_10_digital"
    / "raw"
)

URL = "https://www.meru.org/compuimages/10_3.wrl"

EXPECTED_SHA256 = (
    "855c46cfeeb31e4394b7a4a294b397aa"
    "c4cbc14154e172a326e33243dd9e384b"
)

OUT = (
    ROOT
    / "data"
    / "derived"
    / "meru_3_10_digital"
    / "meru_10_3_surface_embedding_incident.json"
)

NUM = re.compile(
    r"[+-]?(?:(?:\d+\.\d*)|(?:\.\d+)|(?:\d+))"
    r"(?:[eE][+-]?\d+)?"
)

INT = re.compile(r"-?\d+")


def sha256(path: Path) -> str:
    """Return the SHA-256 digest of one file."""
    digest = hashlib.sha256()

    with path.open("rb") as handle:
        for block in iter(
            lambda: handle.read(1 << 20),
            b"",
        ):
            digest.update(block)

    return digest.hexdigest()


def strip_comments(text: str) -> str:
    """Remove VRML comments."""
    return "\n".join(
        line.split("#", 1)[0]
        for line in text.splitlines()
    )


def block(text: str, node: str) -> str:
    """Return the first brace-balanced VRML node."""
    match = re.search(
        rf"\b{re.escape(node)}\s*\{{",
        text,
    )

    if match is None:
        raise RuntimeError(
            f"Missing {node} node."
        )

    opening = text.find(
        "{",
        match.start(),
    )

    depth = 0

    for index in range(
        opening,
        len(text),
    ):
        if text[index] == "{":
            depth += 1
        elif text[index] == "}":
            depth -= 1

            if depth == 0:
                return text[
                    match.start():
                    index + 1
                ]

    raise RuntimeError(
        f"Unbalanced {node} node."
    )


def array(text: str, field: str) -> str:
    """Return one bracket-balanced VRML field."""
    match = re.search(
        rf"\b{re.escape(field)}\s*\[",
        text,
    )

    if match is None:
        raise RuntimeError(
            f"Missing {field} array."
        )

    opening = text.find(
        "[",
        match.start(),
    )

    depth = 0

    for index in range(
        opening,
        len(text),
    ):
        if text[index] == "[":
            depth += 1
        elif text[index] == "]":
            depth -= 1

            if depth == 0:
                return text[
                    opening + 1:
                    index
                ]

    raise RuntimeError(
        f"Unbalanced {field} array."
    )


def parse_mesh(
    text: str,
) -> tuple[np.ndarray, np.ndarray]:
    """Parse the first IndexedFaceSet."""
    indexed_face_set = block(
        text,
        "IndexedFaceSet",
    )

    coordinate = block(
        indexed_face_set,
        "Coordinate",
    )

    values = np.asarray(
        [
            float(value)
            for value in NUM.findall(
                array(
                    coordinate,
                    "point",
                )
            )
        ],
        dtype=np.float64,
    )

    vertices = values.reshape(
        -1,
        3,
    )

    polygons: list[list[int]] = []
    current: list[int] = []

    for value in (
        int(item)
        for item in INT.findall(
            array(
                indexed_face_set,
                "coordIndex",
            )
        )
    ):
        if value == -1:
            if current:
                polygons.append(
                    current
                )
                current = []
        else:
            current.append(
                value
            )

    if current:
        polygons.append(
            current
        )

    faces: list[tuple[int, int, int]] = []

    for polygon in polygons:
        if len(polygon) < 3:
            raise RuntimeError(
                "Face has fewer than three vertices."
            )

        for index in range(
            1,
            len(polygon) - 1,
        ):
            faces.append(
                (
                    polygon[0],
                    polygon[index],
                    polygon[index + 1],
                )
            )

    return (
        vertices,
        np.asarray(
            faces,
            dtype=np.int64,
        ),
    )


def cross2(
    first: np.ndarray,
    second: np.ndarray,
) -> float:
    """Return the scalar 2-D cross product."""
    return float(
        first[0] * second[1]
        - first[1] * second[0]
    )


def orient2(
    first: np.ndarray,
    second: np.ndarray,
    third: np.ndarray,
) -> float:
    """Return twice the signed triangle area in 2-D."""
    return cross2(
        second - first,
        third - first,
    )


def project_points(
    points: np.ndarray,
    normal: np.ndarray,
) -> np.ndarray:
    """Project 3-D points by dropping the dominant normal axis."""
    drop = int(
        np.argmax(
            np.abs(normal)
        )
    )

    return np.delete(
        points,
        drop,
        axis=1,
    )


def point_on_segment_2d(
    point: np.ndarray,
    first: np.ndarray,
    second: np.ndarray,
    length_tolerance: float,
    area_tolerance: float,
) -> bool:
    """Return whether a 2-D point lies on a closed segment."""
    if abs(
        orient2(
            first,
            second,
            point,
        )
    ) > area_tolerance:
        return False

    return bool(
        np.all(
            point
            >= np.minimum(
                first,
                second,
            )
            - length_tolerance
        )
        and np.all(
            point
            <= np.maximum(
                first,
                second,
            )
            + length_tolerance
        )
    )


def point_in_triangle_2d(
    point: np.ndarray,
    triangle: np.ndarray,
    area_tolerance: float,
) -> bool:
    """Return whether a point lies in or on a 2-D triangle."""
    values = [
        orient2(
            triangle[index],
            triangle[
                (index + 1) % 3
            ],
            point,
        )
        for index in range(3)
    ]

    has_positive = any(
        value > area_tolerance
        for value in values
    )

    has_negative = any(
        value < -area_tolerance
        for value in values
    )

    return not (
        has_positive
        and has_negative
    )


def segment_intersection_beyond_point_2d(
    first_a: np.ndarray,
    second_a: np.ndarray,
    first_b: np.ndarray,
    second_b: np.ndarray,
    permitted_point: np.ndarray,
    length_tolerance: float,
    area_tolerance: float,
) -> bool:
    """Detect a 2-D segment intersection away from one permitted point."""
    direction_a = (
        second_a
        - first_a
    )

    direction_b = (
        second_b
        - first_b
    )

    denominator = cross2(
        direction_a,
        direction_b,
    )

    displacement = (
        first_b
        - first_a
    )

    if abs(
        denominator
    ) > area_tolerance:
        parameter_a = (
            cross2(
                displacement,
                direction_b,
            )
            / denominator
        )

        parameter_b = (
            cross2(
                displacement,
                direction_a,
            )
            / denominator
        )

        parameter_tolerance = (
            length_tolerance
            / max(
                float(
                    np.linalg.norm(
                        direction_a
                    )
                ),
                float(
                    np.linalg.norm(
                        direction_b
                    )
                ),
                1.0,
            )
        )

        if (
            -parameter_tolerance
            <= parameter_a
            <= 1.0 + parameter_tolerance
            and
            -parameter_tolerance
            <= parameter_b
            <= 1.0 + parameter_tolerance
        ):
            intersection = (
                first_a
                + parameter_a
                * direction_a
            )

            return bool(
                np.linalg.norm(
                    intersection
                    - permitted_point
                )
                > length_tolerance
            )

        return False

    if abs(
        cross2(
            displacement,
            direction_a,
        )
    ) > area_tolerance:
        return False

    axis = int(
        np.argmax(
            np.abs(
                direction_a
            )
        )
    )

    if abs(
        direction_a[axis]
    ) <= length_tolerance:
        axis = int(
            np.argmax(
                np.abs(
                    direction_b
                )
            )
        )

    a_low, a_high = sorted(
        (
            float(first_a[axis]),
            float(second_a[axis]),
        )
    )

    b_low, b_high = sorted(
        (
            float(first_b[axis]),
            float(second_b[axis]),
        )
    )

    overlap_low = max(
        a_low,
        b_low,
    )

    overlap_high = min(
        a_high,
        b_high,
    )

    if (
        overlap_high
        < overlap_low
        - length_tolerance
    ):
        return False

    permitted_coordinate = float(
        permitted_point[axis]
    )

    farthest = max(
        abs(
            overlap_low
            - permitted_coordinate
        ),
        abs(
            overlap_high
            - permitted_coordinate
        ),
    )

    return (
        farthest
        > length_tolerance
    )


def coplanar_shared_vertex_excess(
    triangle_a: np.ndarray,
    triangle_b: np.ndarray,
    shared_point: np.ndarray,
    normal: np.ndarray,
    length_tolerance: float,
    area_tolerance: float,
) -> bool:
    """Detect coplanar triangle overlap beyond a shared vertex."""
    combined = np.vstack(
        (
            triangle_a,
            triangle_b,
            shared_point[None, :],
        )
    )

    projected = project_points(
        combined,
        normal,
    )

    projected_a = projected[:3]
    projected_b = projected[3:6]
    projected_shared = projected[6]

    edges_a = [
        (
            projected_a[index],
            projected_a[
                (index + 1) % 3
            ],
        )
        for index in range(3)
    ]

    edges_b = [
        (
            projected_b[index],
            projected_b[
                (index + 1) % 3
            ],
        )
        for index in range(3)
    ]

    for edge_a in edges_a:
        for edge_b in edges_b:
            if segment_intersection_beyond_point_2d(
                edge_a[0],
                edge_a[1],
                edge_b[0],
                edge_b[1],
                projected_shared,
                length_tolerance,
                area_tolerance,
            ):
                return True

    for point in projected_a:
        if (
            np.linalg.norm(
                point
                - projected_shared
            )
            > length_tolerance
            and point_in_triangle_2d(
                point,
                projected_b,
                area_tolerance,
            )
        ):
            return True

    for point in projected_b:
        if (
            np.linalg.norm(
                point
                - projected_shared
            )
            > length_tolerance
            and point_in_triangle_2d(
                point,
                projected_a,
                area_tolerance,
            )
        ):
            return True

    return False


def plane_cut_endpoint(
    first: np.ndarray,
    second: np.ndarray,
    signed_first: float,
    signed_second: float,
    plane_tolerance: float,
) -> np.ndarray | None:
    """Return the non-shared endpoint of a triangle/plane cut."""
    if abs(
        signed_first
    ) <= plane_tolerance:
        return first

    if abs(
        signed_second
    ) <= plane_tolerance:
        return second

    if (
        signed_first
        * signed_second
        < 0.0
    ):
        parameter = (
            signed_first
            / (
                signed_first
                - signed_second
            )
        )

        return (
            first
            + parameter
            * (
                second
                - first
            )
        )

    return None


def shared_edge_has_excess(
    triangle_a: np.ndarray,
    triangle_b: np.ndarray,
    common_indices: set[int],
    face_a: np.ndarray,
    face_b: np.ndarray,
    angular_tolerance: float,
    area_tolerance: float,
) -> tuple[bool, bool, float]:
    """Check whether an incident edge pair overlaps beyond that edge."""
    common = sorted(
        common_indices
    )

    common_points = np.asarray(
        [
            vertices[index]
            for index in common
        ]
    )

    opposite_a = next(
        vertices[int(index)]
        for index in face_a
        if int(index) not in common_indices
    )

    opposite_b = next(
        vertices[int(index)]
        for index in face_b
        if int(index) not in common_indices
    )

    normal_a = np.cross(
        triangle_a[1]
        - triangle_a[0],
        triangle_a[2]
        - triangle_a[0],
    )

    normal_b = np.cross(
        triangle_b[1]
        - triangle_b[0],
        triangle_b[2]
        - triangle_b[0],
    )

    normal_a /= np.linalg.norm(
        normal_a
    )

    normal_b /= np.linalg.norm(
        normal_b
    )

    sine_dihedral = float(
        np.linalg.norm(
            np.cross(
                normal_a,
                normal_b,
            )
        )
    )

    if sine_dihedral > angular_tolerance:
        return (
            False,
            False,
            sine_dihedral,
        )

    projected = project_points(
        np.vstack(
            (
                common_points,
                opposite_a[None, :],
                opposite_b[None, :],
            )
        ),
        normal_a,
    )

    first = projected[0]
    second = projected[1]
    projected_a = projected[2]
    projected_b = projected[3]

    side_a = orient2(
        first,
        second,
        projected_a,
    )

    side_b = orient2(
        first,
        second,
        projected_b,
    )

    excess = not (
        abs(side_a) > area_tolerance
        and abs(side_b) > area_tolerance
        and side_a * side_b < 0.0
    )

    return (
        excess,
        True,
        min(
            abs(side_a),
            abs(side_b),
        ),
    )


def shared_vertex_has_excess(
    triangle_a: np.ndarray,
    triangle_b: np.ndarray,
    shared_point: np.ndarray,
    other_a: np.ndarray,
    other_b: np.ndarray,
    angular_tolerance: float,
    plane_tolerance: float,
    length_tolerance: float,
    area_tolerance: float,
) -> tuple[bool, bool, float]:
    """Check whether two faces meet beyond their shared vertex."""
    normal_a = np.cross(
        triangle_a[1]
        - triangle_a[0],
        triangle_a[2]
        - triangle_a[0],
    )

    normal_b = np.cross(
        triangle_b[1]
        - triangle_b[0],
        triangle_b[2]
        - triangle_b[0],
    )

    normal_a /= np.linalg.norm(
        normal_a
    )

    normal_b /= np.linalg.norm(
        normal_b
    )

    line = np.cross(
        normal_a,
        normal_b,
    )

    sine_angle = float(
        np.linalg.norm(
            line
        )
    )

    if sine_angle <= angular_tolerance:
        excess = coplanar_shared_vertex_excess(
            triangle_a,
            triangle_b,
            shared_point,
            normal_a,
            length_tolerance,
            area_tolerance,
        )

        return (
            excess,
            True,
            sine_angle,
        )

    line /= sine_angle

    signed_a = (
        other_a
        - shared_point
    ) @ normal_b

    signed_b = (
        other_b
        - shared_point
    ) @ normal_a

    if (
        (
            np.all(
                signed_a
                > plane_tolerance
            )
            or np.all(
                signed_a
                < -plane_tolerance
            )
        )
        or
        (
            np.all(
                signed_b
                > plane_tolerance
            )
            or np.all(
                signed_b
                < -plane_tolerance
            )
        )
    ):
        margin = max(
            min(
                abs(
                    signed_a
                )
            ),
            min(
                abs(
                    signed_b
                )
            ),
        )

        return (
            False,
            False,
            float(margin),
        )

    endpoint_a = plane_cut_endpoint(
        other_a[0],
        other_a[1],
        float(signed_a[0]),
        float(signed_a[1]),
        plane_tolerance,
    )

    endpoint_b = plane_cut_endpoint(
        other_b[0],
        other_b[1],
        float(signed_b[0]),
        float(signed_b[1]),
        plane_tolerance,
    )

    if (
        endpoint_a is None
        or endpoint_b is None
    ):
        return (
            False,
            False,
            0.0,
        )

    parameter_a = float(
        (
            endpoint_a
            - shared_point
        ) @ line
    )

    parameter_b = float(
        (
            endpoint_b
            - shared_point
        ) @ line
    )

    same_direction = (
        parameter_a
        * parameter_b
        > 0.0
    )

    common_extension = min(
        abs(
            parameter_a
        ),
        abs(
            parameter_b
        ),
    )

    excess = (
        same_direction
        and common_extension
        > length_tolerance
    )

    return (
        excess,
        False,
        common_extension,
    )


with MANIFEST.open(
    newline="",
    encoding="utf-8",
) as handle:
    rows = list(
        csv.DictReader(
            handle
        )
    )

matches = [
    row
    for row in rows
    if row["canonical_url"] == URL
]

if len(matches) != 1:
    raise SystemExit(
        f"Expected one manifest row for {URL}; found {len(matches)}."
    )

source = (
    RAW
    / matches[0]["snapshot_filename"]
)

source_hash = sha256(
    source
)

if source_hash != EXPECTED_SHA256:
    raise SystemExit(
        "10_3.wrl hash does not match the frozen source."
    )

vertices, faces = parse_mesh(
    strip_comments(
        source.read_text(
            encoding="utf-8",
            errors="replace",
        )
    )
)

if (
    vertices.shape
    != (6000, 3)
    or faces.shape
    != (12000, 3)
):
    raise SystemExit(
        "Unexpected native mesh dimensions."
    )

triangles = vertices[
    faces
]

areas = 0.5 * np.linalg.norm(
    np.cross(
        triangles[:, 1]
        - triangles[:, 0],
        triangles[:, 2]
        - triangles[:, 0],
    ),
    axis=1,
)

if np.any(
    areas <= 1.0e-14
):
    raise SystemExit(
        "The mesh contains a degenerate triangle."
    )

scale = float(
    np.linalg.norm(
        vertices.max(
            axis=0
        )
        - vertices.min(
            axis=0
        )
    )
)

length_tolerance = (
    scale
    * 1.0e-10
)

plane_tolerance = (
    scale
    * 1.0e-10
)

area_tolerance = (
    scale
    * scale
    * 1.0e-10
)

angular_tolerance = 1.0e-10

vertex_to_faces: dict[
    int,
    list[int],
] = defaultdict(
    list
)

for face_index, face in enumerate(
    faces
):
    for vertex_index in face:
        vertex_to_faces[
            int(vertex_index)
        ].append(
            face_index
        )

incident_pairs: set[
    tuple[int, int]
] = set()

for face_indices in vertex_to_faces.values():
    for first, second in itertools.combinations(
        sorted(
            face_indices
        ),
        2,
    ):
        incident_pairs.add(
            (
                first,
                second,
            )
        )

counts = Counter(
    {
        "incident_pairs": 0,
        "shared_edge_pairs": 0,
        "shared_edge_noncoplanar": 0,
        "shared_edge_coplanar": 0,
        "shared_edge_excess_intersections": 0,
        "shared_vertex_only_pairs": 0,
        "shared_vertex_noncoplanar": 0,
        "shared_vertex_coplanar": 0,
        "shared_vertex_excess_intersections": 0,
    }
)

examples: list[
    dict[str, object]
] = []

minimum_noncoplanar_edge_sine = math.inf
minimum_coplanar_edge_side_margin = math.inf
minimum_vertex_margin = math.inf

for pair_index, (
    first_face,
    second_face,
) in enumerate(
    sorted(
        incident_pairs
    ),
    start=1,
):
    counts[
        "incident_pairs"
    ] += 1

    face_a = faces[
        first_face
    ]

    face_b = faces[
        second_face
    ]

    common = (
        set(
            map(
                int,
                face_a,
            )
        )
        & set(
            map(
                int,
                face_b,
            )
        )
    )

    triangle_a = triangles[
        first_face
    ]

    triangle_b = triangles[
        second_face
    ]

    if len(common) == 2:
        counts[
            "shared_edge_pairs"
        ] += 1

        excess, coplanar, margin = (
            shared_edge_has_excess(
                triangle_a,
                triangle_b,
                common,
                face_a,
                face_b,
                angular_tolerance,
                area_tolerance,
            )
        )

        if coplanar:
            counts[
                "shared_edge_coplanar"
            ] += 1

            minimum_coplanar_edge_side_margin = min(
                minimum_coplanar_edge_side_margin,
                margin,
            )
        else:
            counts[
                "shared_edge_noncoplanar"
            ] += 1

            minimum_noncoplanar_edge_sine = min(
                minimum_noncoplanar_edge_sine,
                margin,
            )

        if excess:
            counts[
                "shared_edge_excess_intersections"
            ] += 1

            if len(examples) < 20:
                examples.append(
                    {
                        "face_pair": [
                            first_face,
                            second_face,
                        ],
                        "shared_vertex_indices": sorted(
                            common
                        ),
                        "shared_simplex": "edge",
                        "coplanar": coplanar,
                        "margin": margin,
                    }
                )

    elif len(common) == 1:
        counts[
            "shared_vertex_only_pairs"
        ] += 1

        shared_index = next(
            iter(
                common
            )
        )

        shared_point = vertices[
            shared_index
        ]

        other_a = np.asarray(
            [
                vertices[
                    int(index)
                ]
                for index in face_a
                if int(index)
                != shared_index
            ]
        )

        other_b = np.asarray(
            [
                vertices[
                    int(index)
                ]
                for index in face_b
                if int(index)
                != shared_index
            ]
        )

        excess, coplanar, margin = (
            shared_vertex_has_excess(
                triangle_a,
                triangle_b,
                shared_point,
                other_a,
                other_b,
                angular_tolerance,
                plane_tolerance,
                length_tolerance,
                area_tolerance,
            )
        )

        if coplanar:
            counts[
                "shared_vertex_coplanar"
            ] += 1
        else:
            counts[
                "shared_vertex_noncoplanar"
            ] += 1

        minimum_vertex_margin = min(
            minimum_vertex_margin,
            margin,
        )

        if excess:
            counts[
                "shared_vertex_excess_intersections"
            ] += 1

            if len(examples) < 20:
                examples.append(
                    {
                        "face_pair": [
                            first_face,
                            second_face,
                        ],
                        "shared_vertex_indices": [
                            shared_index
                        ],
                        "shared_simplex": "vertex",
                        "coplanar": coplanar,
                        "margin": margin,
                    }
                )

    else:
        raise RuntimeError(
            "Incident-face pair has an unexpected common-simplex size."
        )

    if (
        pair_index
        % 12000
        == 0
    ):
        print(
            "Incident audit: "
            f"{pair_index:5d}/"
            f"{len(incident_pairs)} pairs"
        )

result = {
    "source": {
        "canonical_url": URL,
        "filename": source.name,
        "sha256": source_hash,
    },
    "mesh": {
        "vertices": len(
            vertices
        ),
        "triangles": len(
            faces
        ),
        "minimum_triangle_area": float(
            areas.min()
        ),
    },
    "tolerances": {
        "scale": scale,
        "length_tolerance": length_tolerance,
        "plane_tolerance": plane_tolerance,
        "area_tolerance": area_tolerance,
        "angular_tolerance": angular_tolerance,
    },
    "incident_pair_census": {
        **{
            key: int(
                value
            )
            for key, value in counts.items()
        },
        "minimum_noncoplanar_shared_edge_sine": (
            None
            if not math.isfinite(
                minimum_noncoplanar_edge_sine
            )
            else minimum_noncoplanar_edge_sine
        ),
        "minimum_coplanar_shared_edge_side_margin": (
            None
            if not math.isfinite(
                minimum_coplanar_edge_side_margin
            )
            else minimum_coplanar_edge_side_margin
        ),
        "minimum_shared_vertex_margin": (
            None
            if not math.isfinite(
                minimum_vertex_margin
            )
            else minimum_vertex_margin
        ),
        "excess_intersection_examples": examples,
    },
    "scope": {
        "shared_edge_pairs_must_meet_only_in_their_edge": True,
        "shared_vertex_pairs_must_meet_only_in_their_vertex": True,
        "formal_exact_arithmetic": False,
    },
}

OUT.parent.mkdir(
    parents=True,
    exist_ok=True,
)

OUT.write_text(
    json.dumps(
        result,
        indent=2,
        sort_keys=True,
    )
    + "\n",
    encoding="utf-8",
)

print()
print("=" * 78)
print("MERU 10_3 INCIDENT-FACE PROBE")
print("=" * 78)
print(
    "Source:                              "
    f"{source.name}"
)
print(
    "Incident face pairs:                 "
    f"{counts['incident_pairs']:,}"
)
print(
    "Shared-edge pairs:                   "
    f"{counts['shared_edge_pairs']:,}"
)
print(
    "  noncoplanar / coplanar:            "
    f"{counts['shared_edge_noncoplanar']:,} / "
    f"{counts['shared_edge_coplanar']:,}"
)
print(
    "  excess intersections:              "
    f"{counts['shared_edge_excess_intersections']:,}"
)
print(
    "Shared-vertex-only pairs:             "
    f"{counts['shared_vertex_only_pairs']:,}"
)
print(
    "  noncoplanar / coplanar:             "
    f"{counts['shared_vertex_noncoplanar']:,} / "
    f"{counts['shared_vertex_coplanar']:,}"
)
print(
    "  excess intersections:              "
    f"{counts['shared_vertex_excess_intersections']:,}"
)

if math.isfinite(
    minimum_noncoplanar_edge_sine
):
    print(
        "Minimum noncoplanar edge sine:       "
        f"{minimum_noncoplanar_edge_sine:.12g}"
    )

if math.isfinite(
    minimum_coplanar_edge_side_margin
):
    print(
        "Minimum coplanar edge side margin:   "
        f"{minimum_coplanar_edge_side_margin:.12g}"
    )

if math.isfinite(
    minimum_vertex_margin
):
    print(
        "Minimum shared-vertex margin:        "
        f"{minimum_vertex_margin:.12g}"
    )

incident_simplex_certificate = (
    counts["shared_edge_excess_intersections"] == 0
    and counts["shared_vertex_excess_intersections"] == 0
)

print(
    "Incident simplex certificate:         "
    f"{incident_simplex_certificate}"
)

print(
    f"Wrote {OUT}"
)
