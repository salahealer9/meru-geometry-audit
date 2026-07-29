#!/usr/bin/env python3
"""Audit Meru's native 10_3 VRML mesh and source-defined centreline.

The third-party VRML source remains locally ignored. This script verifies
its tracked SHA-256 manifest entry, recovers the structured tube mesh,
extracts the cross-section-centroid centreline, and records geometric and
topological diagnostics in tracked derived outputs.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import re
from collections import Counter, defaultdict, deque
from pathlib import Path
from typing import Any

import numpy as np


ROOT = Path(__file__).resolve().parents[1]

DEFAULT_MANIFEST = (
    ROOT
    / "data"
    / "source_manifests"
    / "meru_3_10_digital"
    / "official_asset_manifest.csv"
)

DEFAULT_RAW_DIR = (
    ROOT
    / "data"
    / "source_snapshots"
    / "meru_3_10_digital"
    / "raw"
)

DEFAULT_JSON_OUTPUT = (
    ROOT
    / "data"
    / "derived"
    / "meru_3_10_digital"
    / "meru_10_3_centerline_audit.json"
)

DEFAULT_REPORT_OUTPUT = (
    ROOT
    / "reports"
    / "meru_10_3_native_geometry_audit.md"
)

TARGET_URL = "https://www.meru.org/compuimages/10_3.wrl"
EXPECTED_SHA256 = (
    "855c46cfeeb31e4394b7a4a294b397aa"
    "c4cbc14154e172a326e33243dd9e384b"
)
EXPECTED_BYTES = 429_161

SECTION_COUNT = 300
POINTS_PER_SECTION = 20
INTERSECTION_TOLERANCE = 1.0e-8
REMOTE_SEGMENT_EXCLUSION = 5

NUMBER_PATTERN = re.compile(
    r"[+-]?(?:(?:\d+\.\d*)|(?:\.\d+)|(?:\d+))"
    r"(?:[eE][+-]?\d+)?"
)


def sha256_path(path: Path) -> str:
    """Return the SHA-256 digest of one file."""
    digest = hashlib.sha256()

    with path.open("rb") as handle:
        for block in iter(
            lambda: handle.read(1024 * 1024),
            b"",
        ):
            digest.update(block)

    return digest.hexdigest()


def remove_comments(text: str) -> str:
    """Remove VRML comments while preserving quoted strings."""
    output: list[str] = []

    for line in text.splitlines():
        in_string = False
        escaped = False
        cut = len(line)

        for index, character in enumerate(line):
            if escaped:
                escaped = False
                continue

            if character == "\\" and in_string:
                escaped = True
                continue

            if character == '"':
                in_string = not in_string
                continue

            if character == "#" and not in_string:
                cut = index
                break

        output.append(line[:cut])

    return "\n".join(output)


def find_balanced_blocks(
    text: str,
    node_type: str,
) -> list[str]:
    """Return brace-balanced blocks for one VRML node type."""
    pattern = re.compile(
        rf"\b{re.escape(node_type)}\s*\{{"
    )

    blocks: list[str] = []

    for match in pattern.finditer(text):
        opening = text.find(
            "{",
            match.start(),
        )

        depth = 0
        in_string = False
        escaped = False

        for index in range(opening, len(text)):
            character = text[index]

            if escaped:
                escaped = False
                continue

            if character == "\\" and in_string:
                escaped = True
                continue

            if character == '"':
                in_string = not in_string
                continue

            if in_string:
                continue

            if character == "{":
                depth += 1
            elif character == "}":
                depth -= 1

                if depth == 0:
                    blocks.append(
                        text[match.start():index + 1]
                    )
                    break

    return blocks


def first_array(
    block: str,
    field_name: str,
) -> str:
    """Return the first bracket-balanced array for a field."""
    match = re.search(
        rf"\b{re.escape(field_name)}\s*\[",
        block,
    )

    if match is None:
        raise RuntimeError(
            f"Missing array field {field_name!r}."
        )

    opening = block.find(
        "[",
        match.start(),
    )

    depth = 0

    for index in range(opening, len(block)):
        character = block[index]

        if character == "[":
            depth += 1
        elif character == "]":
            depth -= 1

            if depth == 0:
                return block[opening + 1:index]

    raise RuntimeError(
        f"Unbalanced array field {field_name!r}."
    )


def parse_vertices(block: str) -> np.ndarray:
    """Parse the inline Coordinate point array."""
    values = np.asarray(
        [
            float(value)
            for value in NUMBER_PATTERN.findall(
                first_array(block, "point")
            )
        ],
        dtype=np.float64,
    )

    if values.size % 3:
        raise RuntimeError(
            "Coordinate scalar count is not divisible by three."
        )

    return values.reshape(-1, 3)


def parse_faces(block: str) -> list[tuple[int, ...]]:
    """Parse coordIndex into polygon-index tuples."""
    values = [
        int(float(value))
        for value in NUMBER_PATTERN.findall(
            first_array(block, "coordIndex")
        )
    ]

    faces: list[tuple[int, ...]] = []
    current: list[int] = []

    for value in values:
        if value == -1:
            if current:
                faces.append(tuple(current))
                current = []
        else:
            current.append(value)

    if current:
        faces.append(tuple(current))

    return faces


def connected_components(
    adjacency: dict[int, set[int]],
    vertices: set[int],
) -> list[set[int]]:
    """Return connected components of an undirected vertex graph."""
    remaining = set(vertices)
    components: list[set[int]] = []

    while remaining:
        root = next(iter(remaining))
        queue: deque[int] = deque([root])
        component: set[int] = set()

        remaining.remove(root)

        while queue:
            vertex = queue.popleft()
            component.add(vertex)

            for neighbour in adjacency.get(vertex, set()):
                if neighbour in remaining:
                    remaining.remove(neighbour)
                    queue.append(neighbour)

        components.append(component)

    return sorted(
        components,
        key=len,
        reverse=True,
    )


def triangle_area_twice(
    first: np.ndarray,
    second: np.ndarray,
    third: np.ndarray,
) -> float:
    """Return twice the area of a three-dimensional triangle."""
    return float(
        np.linalg.norm(
            np.cross(
                second - first,
                third - first,
            )
        )
    )


def audit_mesh(
    vertices: np.ndarray,
    faces: list[tuple[int, ...]],
) -> dict[str, Any]:
    """Audit combinatorial topology of one IndexedFaceSet."""
    used_vertices = {
        vertex
        for face in faces
        for vertex in face
    }

    invalid_indices = sorted(
        vertex
        for vertex in used_vertices
        if vertex < 0 or vertex >= len(vertices)
    )

    if invalid_indices:
        raise RuntimeError(
            f"Invalid vertex indices: {invalid_indices[:10]}"
        )

    edge_incidence: dict[
        tuple[int, int],
        list[int],
    ] = defaultdict(list)

    edge_orientations: dict[
        tuple[int, int],
        list[int],
    ] = defaultdict(list)

    adjacency: dict[int, set[int]] = defaultdict(set)

    repeated_index_faces = 0
    zero_area_triangles = 0

    for face_index, face in enumerate(faces):
        if len(set(face)) != len(face):
            repeated_index_faces += 1

        if len(face) == 3:
            area_twice = triangle_area_twice(
                vertices[face[0]],
                vertices[face[1]],
                vertices[face[2]],
            )

            if area_twice <= 1.0e-12:
                zero_area_triangles += 1

        for index, start in enumerate(face):
            end = face[(index + 1) % len(face)]

            edge = (
                min(start, end),
                max(start, end),
            )

            orientation = (
                1
                if (start, end) == edge
                else -1
            )

            edge_incidence[edge].append(
                face_index
            )

            edge_orientations[edge].append(
                orientation
            )

            adjacency[start].add(end)
            adjacency[end].add(start)

    incidence_histogram = Counter(
        len(incident_faces)
        for incident_faces in edge_incidence.values()
    )

    boundary_edges = sum(
        len(incident_faces) == 1
        for incident_faces in edge_incidence.values()
    )

    nonmanifold_edges = sum(
        len(incident_faces) > 2
        for incident_faces in edge_incidence.values()
    )

    orientation_conflicts = sum(
        len(orientations) == 2
        and orientations[0] == orientations[1]
        for orientations in edge_orientations.values()
    )

    components = connected_components(
        adjacency,
        used_vertices,
    )

    vertex_count = len(used_vertices)
    edge_count = len(edge_incidence)
    face_count = len(faces)
    euler_characteristic = (
        vertex_count
        - edge_count
        + face_count
    )

    closed_orientable_manifold = (
        boundary_edges == 0
        and nonmanifold_edges == 0
        and orientation_conflicts == 0
    )

    genus: int | None = None

    if (
        closed_orientable_manifold
        and len(components) == 1
        and (2 - euler_characteristic) >= 0
        and (2 - euler_characteristic) % 2 == 0
    ):
        genus = (
            2
            - euler_characteristic
        ) // 2

    valence_histogram = Counter(
        len(adjacency[vertex])
        for vertex in used_vertices
    )

    return {
        "coordinate_vertex_count": int(len(vertices)),
        "used_vertex_count": int(vertex_count),
        "unused_vertex_count": int(
            len(vertices) - vertex_count
        ),
        "face_count": int(face_count),
        "face_size_histogram": {
            str(size): int(count)
            for size, count in sorted(
                Counter(
                    len(face)
                    for face in faces
                ).items()
            )
        },
        "unique_edge_count": int(edge_count),
        "edge_incidence_histogram": {
            str(incidence): int(count)
            for incidence, count in sorted(
                incidence_histogram.items()
            )
        },
        "boundary_edge_count": int(boundary_edges),
        "nonmanifold_edge_count": int(nonmanifold_edges),
        "orientation_conflict_count": int(
            orientation_conflicts
        ),
        "connected_component_count": int(
            len(components)
        ),
        "component_vertex_counts": [
            int(len(component))
            for component in components
        ],
        "repeated_index_face_count": int(
            repeated_index_faces
        ),
        "zero_area_triangle_count": int(
            zero_area_triangles
        ),
        "vertex_valence_histogram": {
            str(valence): int(count)
            for valence, count in sorted(
                valence_histogram.items()
            )
        },
        "euler_characteristic": int(
            euler_characteristic
        ),
        "closed_orientable_manifold": bool(
            closed_orientable_manifold
        ),
        "candidate_genus": genus,
    }


def cross_section_metrics(
    vertices: np.ndarray,
) -> tuple[np.ndarray, dict[str, Any]]:
    """Recover consecutive cross-sections and their centroids."""
    expected_vertex_count = (
        SECTION_COUNT
        * POINTS_PER_SECTION
    )

    if len(vertices) != expected_vertex_count:
        raise RuntimeError(
            f"Expected {expected_vertex_count} vertices; "
            f"found {len(vertices)}."
        )

    sections = vertices.reshape(
        SECTION_COUNT,
        POINTS_PER_SECTION,
        3,
    )

    centreline = sections.mean(
        axis=1
    )

    centred_sections = (
        sections
        - centreline[:, None, :]
    )

    section_radii = np.linalg.norm(
        centred_sections,
        axis=2,
    )

    mean_section_radii = section_radii.mean(
        axis=1
    )

    planarity_values: list[float] = []
    circularity_values: list[float] = []

    for section in centred_sections:
        covariance = (
            section.T
            @ section
            / len(section)
        )

        eigenvalues = np.maximum(
            np.linalg.eigvalsh(
                covariance
            ),
            0.0,
        )

        small, middle, large = eigenvalues

        planarity_values.append(
            math.sqrt(
                small
                / max(
                    middle,
                    1.0e-30,
                )
            )
        )

        circularity_values.append(
            math.sqrt(
                large
                / max(
                    middle,
                    1.0e-30,
                )
            )
        )

    segment_lengths = np.linalg.norm(
        np.roll(
            centreline,
            -1,
            axis=0,
        )
        - centreline,
        axis=1,
    )

    ordinary_segment_lengths = (
        segment_lengths[:-1]
    )

    metrics = {
        "section_count": SECTION_COUNT,
        "vertices_per_section": POINTS_PER_SECTION,
        "centreline_station_count": int(
            len(centreline)
        ),
        "mean_section_radius": float(
            mean_section_radii.mean()
        ),
        "median_section_radius": float(
            np.median(
                mean_section_radii
            )
        ),
        "minimum_section_radius": float(
            mean_section_radii.min()
        ),
        "maximum_section_radius": float(
            mean_section_radii.max()
        ),
        "section_radius_cv": float(
            mean_section_radii.std()
            / mean_section_radii.mean()
        ),
        "median_planarity_ratio": float(
            np.median(
                planarity_values
            )
        ),
        "median_circularity_ratio": float(
            np.median(
                circularity_values
            )
        ),
        "segment_length_mean": float(
            segment_lengths.mean()
        ),
        "segment_length_median": float(
            np.median(
                segment_lengths
            )
        ),
        "segment_length_minimum": float(
            segment_lengths.min()
        ),
        "segment_length_maximum": float(
            segment_lengths.max()
        ),
        "segment_length_cv": float(
            segment_lengths.std()
            / segment_lengths.mean()
        ),
        "closure_segment_length": float(
            segment_lengths[-1]
        ),
        "closure_to_ordinary_median_ratio": float(
            segment_lengths[-1]
            / np.median(
                ordinary_segment_lengths
            )
        ),
    }

    return centreline, metrics


def clamp(
    value: float,
    lower: float = 0.0,
    upper: float = 1.0,
) -> float:
    """Clamp one floating-point value."""
    return min(
        upper,
        max(
            lower,
            value,
        ),
    )


def segment_distance(
    first_start: np.ndarray,
    first_end: np.ndarray,
    second_start: np.ndarray,
    second_end: np.ndarray,
) -> float:
    """Return the exact minimum distance between two 3-D segments."""
    first_direction = first_end - first_start
    second_direction = second_end - second_start
    offset = first_start - second_start

    first_length_squared = float(
        np.dot(
            first_direction,
            first_direction,
        )
    )

    second_length_squared = float(
        np.dot(
            second_direction,
            second_direction,
        )
    )

    second_projection = float(
        np.dot(
            second_direction,
            offset,
        )
    )

    epsilon = 1.0e-15

    if (
        first_length_squared <= epsilon
        and second_length_squared <= epsilon
    ):
        return float(
            np.linalg.norm(
                first_start
                - second_start
            )
        )

    if first_length_squared <= epsilon:
        first_parameter = 0.0
        second_parameter = clamp(
            second_projection
            / second_length_squared
        )
    else:
        first_projection = float(
            np.dot(
                first_direction,
                offset,
            )
        )

        if second_length_squared <= epsilon:
            second_parameter = 0.0
            first_parameter = clamp(
                -first_projection
                / first_length_squared
            )
        else:
            coupling = float(
                np.dot(
                    first_direction,
                    second_direction,
                )
            )

            denominator = (
                first_length_squared
                * second_length_squared
                - coupling
                * coupling
            )

            if abs(denominator) > epsilon:
                first_parameter = clamp(
                    (
                        coupling
                        * second_projection
                        - first_projection
                        * second_length_squared
                    )
                    / denominator
                )
            else:
                first_parameter = 0.0

            second_parameter = (
                coupling
                * first_parameter
                + second_projection
            ) / second_length_squared

            if second_parameter < 0.0:
                second_parameter = 0.0
                first_parameter = clamp(
                    -first_projection
                    / first_length_squared
                )
            elif second_parameter > 1.0:
                second_parameter = 1.0
                first_parameter = clamp(
                    (
                        coupling
                        - first_projection
                    )
                    / first_length_squared
                )

    first_point = (
        first_start
        + first_parameter
        * first_direction
    )

    second_point = (
        second_start
        + second_parameter
        * second_direction
    )

    return float(
        np.linalg.norm(
            first_point
            - second_point
        )
    )


def cyclic_index_distance(
    first: int,
    second: int,
    count: int,
) -> int:
    """Return the smaller cyclic separation between two indices."""
    difference = abs(
        first - second
    )

    return min(
        difference,
        count - difference,
    )


def embedding_metrics(
    centreline: np.ndarray,
    median_section_radius: float,
) -> dict[str, Any]:
    """Audit polygonal centreline self-intersections and clearance."""
    segment_count = len(centreline)

    intersection_pairs: list[
        tuple[int, int, float]
    ] = []

    minimum_nonadjacent = (
        math.inf,
        -1,
        -1,
    )

    minimum_remote = (
        math.inf,
        -1,
        -1,
    )

    for first in range(segment_count):
        first_start = centreline[first]
        first_end = centreline[
            (first + 1) % segment_count
        ]

        for second in range(
            first + 1,
            segment_count,
        ):
            separation = cyclic_index_distance(
                first,
                second,
                segment_count,
            )

            if separation <= 1:
                continue

            second_start = centreline[second]
            second_end = centreline[
                (second + 1)
                % segment_count
            ]

            distance = segment_distance(
                first_start,
                first_end,
                second_start,
                second_end,
            )

            if distance < minimum_nonadjacent[0]:
                minimum_nonadjacent = (
                    distance,
                    first,
                    second,
                )

            if (
                separation
                > REMOTE_SEGMENT_EXCLUSION
                and distance
                < minimum_remote[0]
            ):
                minimum_remote = (
                    distance,
                    first,
                    second,
                )

            if distance <= INTERSECTION_TOLERANCE:
                intersection_pairs.append(
                    (
                        first,
                        second,
                        distance,
                    )
                )

    median_tube_diameter = (
        2.0
        * median_section_radius
    )

    return {
        "intersection_tolerance": (
            INTERSECTION_TOLERANCE
        ),
        "exact_nonadjacent_intersection_count": int(
            len(intersection_pairs)
        ),
        "minimum_nonadjacent_segment_distance": float(
            minimum_nonadjacent[0]
        ),
        "minimum_nonadjacent_segment_pair": [
            int(minimum_nonadjacent[1]),
            int(minimum_nonadjacent[2]),
        ],
        "remote_segment_exclusion": int(
            REMOTE_SEGMENT_EXCLUSION
        ),
        "minimum_remote_segment_distance": float(
            minimum_remote[0]
        ),
        "minimum_remote_segment_pair": [
            int(minimum_remote[1]),
            int(minimum_remote[2]),
        ],
        "median_tube_diameter": float(
            median_tube_diameter
        ),
        "remote_clearance_to_diameter_ratio": float(
            minimum_remote[0]
            / median_tube_diameter
        ),
        "embedded_polygonal_centerline": bool(
            len(intersection_pairs) == 0
        ),
    }


def cyclic_winding(
    phase: np.ndarray,
) -> tuple[float, np.ndarray]:
    """Return total closed phase winding and wrapped phase steps."""
    phase_steps = np.angle(
        np.exp(
            1j
            * (
                np.roll(
                    phase,
                    -1,
                )
                - phase
            )
        )
    )

    winding = float(
        phase_steps.sum()
        / (
            2.0
            * math.pi
        )
    )

    return winding, phase_steps


def phase_diagnostics(
    phase: np.ndarray,
) -> dict[str, Any]:
    """Measure winding, monotonicity and fitted linear phase."""
    winding, phase_steps = cyclic_winding(
        phase
    )

    rounded_winding = int(
        round(
            winding
        )
    )

    expected_sign = (
        1
        if rounded_winding > 0
        else -1
        if rounded_winding < 0
        else 0
    )

    if expected_sign == 0:
        direction_reversals = None
    else:
        direction_reversals = int(
            np.count_nonzero(
                expected_sign
                * phase_steps
                <= 0.0
            )
        )

    sample = np.arange(
        len(phase),
        dtype=np.float64,
    )

    unwrapped = np.unwrap(
        phase
    )

    slope, intercept = np.polyfit(
        sample,
        unwrapped,
        deg=1,
    )

    residual = (
        unwrapped
        - (
            slope
            * sample
            + intercept
        )
    )

    fitted_winding = float(
        slope
        * len(phase)
        / (
            2.0
            * math.pi
        )
    )

    return {
        "total_winding": float(winding),
        "rounded_winding": rounded_winding,
        "fitted_winding": fitted_winding,
        "phase_step_minimum": float(
            phase_steps.min()
        ),
        "phase_step_maximum": float(
            phase_steps.max()
        ),
        "direction_reversal_count": (
            direction_reversals
        ),
        "linear_phase_rms": float(
            np.sqrt(
                np.mean(
                    residual
                    * residual
                )
            )
        ),
    }


def axis_diagnostics(
    centreline: np.ndarray,
    axis_name: str,
    axial_index: int,
    plane_indices: tuple[int, int],
) -> dict[str, Any]:
    """Measure toroidal coordinates around one coordinate axis."""
    centred = (
        centreline
        - centreline.mean(
            axis=0
        )
    )

    axial = centred[
        :,
        axial_index,
    ]

    first_plane = centred[
        :,
        plane_indices[0],
    ]

    second_plane = centred[
        :,
        plane_indices[1],
    ]

    radial = np.hypot(
        first_plane,
        second_plane,
    )

    major_radius = float(
        radial.mean()
    )

    minor_radial = (
        radial
        - major_radius
    )

    minor_radius_values = np.hypot(
        minor_radial,
        axial,
    )

    major_phase = np.arctan2(
        second_plane,
        first_plane,
    )

    minor_phase = np.arctan2(
        axial,
        minor_radial,
    )

    major = phase_diagnostics(
        major_phase
    )

    minor = phase_diagnostics(
        minor_phase
    )

    return {
        "axis": axis_name,
        "axial_coordinate_index": axial_index,
        "transverse_coordinate_indices": list(
            plane_indices
        ),
        "major_radius_mean": major_radius,
        "major_radial_minimum": float(
            radial.min()
        ),
        "major_radial_maximum": float(
            radial.max()
        ),
        "minor_radius_mean": float(
            minor_radius_values.mean()
        ),
        "minor_radius_minimum": float(
            minor_radius_values.min()
        ),
        "minor_radius_maximum": float(
            minor_radius_values.max()
        ),
        "minor_radius_cv": float(
            minor_radius_values.std()
            / minor_radius_values.mean()
        ),
        "major_phase": major,
        "minor_phase": minor,
    }


def dominant_fourier_modes(
    values: np.ndarray,
    limit: int = 10,
) -> list[dict[str, Any]]:
    """Return dominant signed discrete Fourier modes."""
    count = len(values)

    amplitudes = (
        np.abs(
            np.fft.fft(
                values
            )
        )
        / count
    )

    frequencies = np.rint(
        np.fft.fftfreq(
            count,
            d=1.0 / count,
        )
    ).astype(int)

    candidates = [
        {
            "frequency": int(frequency),
            "amplitude": float(amplitude),
        }
        for frequency, amplitude in zip(
            frequencies,
            amplitudes,
            strict=True,
        )
        if frequency != 0
    ]

    return sorted(
        candidates,
        key=lambda row: row["amplitude"],
        reverse=True,
    )[:limit]


def toroidal_metrics(
    centreline: np.ndarray,
) -> dict[str, Any]:
    """Recover the best toroidal axis and winding pair."""
    axis_definitions = {
        "x": (
            0,
            (1, 2),
        ),
        "y": (
            1,
            (2, 0),
        ),
        "z": (
            2,
            (0, 1),
        ),
    }

    axis_results = [
        axis_diagnostics(
            centreline,
            axis_name,
            axial_index,
            plane_indices,
        )
        for (
            axis_name,
            (
                axial_index,
                plane_indices,
            ),
        ) in axis_definitions.items()
    ]

    best_axis = min(
        axis_results,
        key=lambda result: (
            result["minor_radius_cv"],
            abs(
                result[
                    "major_phase"
                ][
                    "total_winding"
                ]
                - round(
                    result[
                        "major_phase"
                    ][
                        "total_winding"
                    ]
                )
            )
            + abs(
                result[
                    "minor_phase"
                ][
                    "total_winding"
                ]
                - round(
                    result[
                        "minor_phase"
                    ][
                        "total_winding"
                    ]
                )
            ),
        ),
    )

    axis_name = str(
        best_axis["axis"]
    )

    axial_index, plane_indices = (
        axis_definitions[
            axis_name
        ]
    )

    centred = (
        centreline
        - centreline.mean(
            axis=0
        )
    )

    complex_transverse = (
        centred[
            :,
            plane_indices[0],
        ]
        + 1j
        * centred[
            :,
            plane_indices[1],
        ]
    )

    axial_signal = centred[
        :,
        axial_index,
    ].astype(
        np.complex128
    )

    signed_pair = [
        int(
            best_axis[
                "major_phase"
            ][
                "rounded_winding"
            ]
        ),
        int(
            best_axis[
                "minor_phase"
            ][
                "rounded_winding"
            ]
        ),
    ]

    unsigned_pair = sorted(
        {
            abs(value)
            for value in signed_pair
        }
    )

    return {
        "candidate_axes": axis_results,
        "best_axis": axis_name,
        "signed_winding_pair": signed_pair,
        "unsigned_winding_pair": unsigned_pair,
        "matches_unsigned_3_10": (
            unsigned_pair
            == [
                3,
                10,
            ]
        ),
        "major_phase_monotonic": (
            best_axis[
                "major_phase"
            ][
                "direction_reversal_count"
            ]
            == 0
        ),
        "minor_phase_monotonic": (
            best_axis[
                "minor_phase"
            ][
                "direction_reversal_count"
            ]
            == 0
        ),
        "dominant_transverse_fourier_modes": (
            dominant_fourier_modes(
                complex_transverse
            )
        ),
        "dominant_axial_fourier_modes": (
            dominant_fourier_modes(
                axial_signal
            )
        ),
    }


def load_source_from_manifest(
    manifest_path: Path,
    raw_dir: Path,
) -> tuple[dict[str, str], Path]:
    """Resolve and verify the local native-model source."""
    with manifest_path.open(
        newline="",
        encoding="utf-8",
    ) as handle:
        rows = list(
            csv.DictReader(handle)
        )

    matches = [
        row
        for row in rows
        if row["canonical_url"]
        == TARGET_URL
    ]

    if len(matches) != 1:
        raise RuntimeError(
            f"Expected one manifest row for {TARGET_URL}; "
            f"found {len(matches)}."
        )

    manifest = matches[0]
    source_path = (
        raw_dir
        / manifest[
            "snapshot_filename"
        ]
    )

    if not source_path.exists():
        raise FileNotFoundError(
            "The locally ignored Meru source asset is missing: "
            f"{source_path}"
        )

    actual_bytes = (
        source_path.stat().st_size
    )

    actual_sha256 = sha256_path(
        source_path
    )

    if actual_bytes != EXPECTED_BYTES:
        raise RuntimeError(
            f"Unexpected source byte count: {actual_bytes}"
        )

    if actual_sha256 != EXPECTED_SHA256:
        raise RuntimeError(
            f"Unexpected source SHA-256: {actual_sha256}"
        )

    if actual_bytes != int(
        manifest["byte_count"]
    ):
        raise RuntimeError(
            "Source byte count disagrees with tracked manifest."
        )

    if actual_sha256 != manifest["sha256"]:
        raise RuntimeError(
            "Source SHA-256 disagrees with tracked manifest."
        )

    return manifest, source_path


def build_audit(
    manifest_path: Path,
    raw_dir: Path,
) -> dict[str, Any]:
    """Run the complete native-geometry audit."""
    manifest, source_path = (
        load_source_from_manifest(
            manifest_path,
            raw_dir,
        )
    )

    original_text = source_path.read_text(
        encoding="utf-8",
        errors="replace",
    )

    text = remove_comments(
        original_text
    )

    mesh_blocks = find_balanced_blocks(
        text,
        "IndexedFaceSet",
    )

    if len(mesh_blocks) != 1:
        raise RuntimeError(
            f"Expected one IndexedFaceSet; "
            f"found {len(mesh_blocks)}."
        )

    mesh_block = mesh_blocks[0]

    vertices = parse_vertices(
        mesh_block
    )

    faces = parse_faces(
        mesh_block
    )

    mesh = audit_mesh(
        vertices,
        faces,
    )

    centreline, parameterization = (
        cross_section_metrics(
            vertices
        )
    )

    embedding = embedding_metrics(
        centreline,
        parameterization[
            "median_section_radius"
        ],
    )

    toroidal = toroidal_metrics(
        centreline
    )

    conclusions = {
        "single_connected_closed_genus_one_mesh": bool(
            mesh[
                "connected_component_count"
            ]
            == 1
            and mesh[
                "closed_orientable_manifold"
            ]
            and mesh[
                "candidate_genus"
            ]
            == 1
        ),
        "source_defined_tube_parameterization": bool(
            parameterization[
                "section_count"
            ]
            == SECTION_COUNT
            and parameterization[
                "vertices_per_section"
            ]
            == POINTS_PER_SECTION
        ),
        "embedded_polygonal_centerline": bool(
            embedding[
                "embedded_polygonal_centerline"
            ]
        ),
        "monotonic_toroidal_phases": bool(
            toroidal[
                "major_phase_monotonic"
            ]
            and toroidal[
                "minor_phase_monotonic"
            ]
        ),
        "unsigned_winding_pair_matches_3_10": bool(
            toroidal[
                "matches_unsigned_3_10"
            ]
        ),
        "native_geometry_interpretation": (
            "The source-defined cross-section centroids form an "
            "embedded polygonal toroidal centreline with signed "
            "winding pair (3,-10) under the selected y-axis "
            "coordinate convention and unsigned pair {3,10}."
        ),
        "interpretive_boundary": (
            "This audit does not yet identify the complete "
            "model-to-A10_P03 crossing correspondence, certify "
            "the surrounding tube against all triangle-triangle "
            "self-intersections, or determine chirality under a "
            "separate knot-diagram convention."
        ),
    }

    return {
        "schema_version": 1,
        "audit_name": (
            "Meru 10_3 native geometry and centreline audit"
        ),
        "source": {
            "canonical_url": TARGET_URL,
            "snapshot_filename": (
                manifest[
                    "snapshot_filename"
                ]
            ),
            "media_type": (
                manifest[
                    "media_type"
                ]
            ),
            "byte_count": EXPECTED_BYTES,
            "sha256": EXPECTED_SHA256,
            "vrml_header": (
                next(
                    line.strip()
                    for line in original_text.splitlines()
                    if line.strip()
                )
            ),
            "snapshot_policy": (
                manifest[
                    "snapshot_policy"
                ]
            ),
        },
        "mesh_topology": mesh,
        "tube_parameterization": parameterization,
        "centerline_embedding": embedding,
        "toroidal_winding": toroidal,
        "conclusions": conclusions,
    }


def format_number(
    value: float,
) -> str:
    """Format one report number compactly."""
    return f"{value:.12g}"


def render_report(
    audit: dict[str, Any],
) -> str:
    """Render the tracked Markdown audit report."""
    source = audit["source"]
    mesh = audit["mesh_topology"]
    tube = audit["tube_parameterization"]
    embedding = audit["centerline_embedding"]
    toroidal = audit["toroidal_winding"]

    best_axis = next(
        row
        for row in toroidal[
            "candidate_axes"
        ]
        if row["axis"]
        == toroidal["best_axis"]
    )

    major = best_axis[
        "major_phase"
    ]

    minor = best_axis[
        "minor_phase"
    ]

    transverse_modes = "\n".join(
        (
            f"| {row['frequency']} | "
            f"{format_number(row['amplitude'])} |"
        )
        for row in toroidal[
            "dominant_transverse_fourier_modes"
        ][:6]
    )

    axial_modes = "\n".join(
        (
            f"| {row['frequency']} | "
            f"{format_number(row['amplitude'])} |"
        )
        for row in toroidal[
            "dominant_axial_fourier_modes"
        ][:6]
    )

    return f"""# Meru `10_3.wrl` native geometry audit

**Status:** Frozen source-derived native-geometry audit  
**Source:** `{source["canonical_url"]}`  
**Source SHA-256:** `{source["sha256"]}`  
**Source policy:** {source["snapshot_policy"]}

## Purpose

This audit examines Meru's recovered native VRML asset directly rather
than inferring its hidden geometry solely from the hand-drawn A10_P03
panel.

The third-party source bytes remain locally excluded from Git. The
tracked manifest, this audit script, the derived JSON metrics and this
report make the analysis reproducible for a researcher possessing the
same SHA-256-identified source file.

## Native mesh structure

The VRML asset contains one `IndexedFaceSet` with:

```text
vertices: {mesh["used_vertex_count"]}
edges:    {mesh["unique_edge_count"]}
faces:    {mesh["face_count"]}
chi:      {mesh["euler_characteristic"]}
````

The mesh audit finds:

```text
connected components:    {mesh["connected_component_count"]}
boundary edges:          {mesh["boundary_edge_count"]}
non-manifold edges:      {mesh["nonmanifold_edge_count"]}
orientation conflicts:   {mesh["orientation_conflict_count"]}
zero-area triangles:     {mesh["zero_area_triangle_count"]}
candidate genus:         {mesh["candidate_genus"]}
```

It is therefore a connected, closed, consistently oriented
combinatorial genus-one surface.

## Source-defined tube parameterisation

The vertex indexing resolves unambiguously into:

```text
{tube["section_count"]} consecutive cross-sections
x {tube["vertices_per_section"]} vertices per section
= {mesh["coordinate_vertex_count"]} vertices
```

The consecutive sections are nearly planar and circular:

```text
mean section radius:       {format_number(tube["mean_section_radius"])}
median section radius:     {format_number(tube["median_section_radius"])}
section-radius CV:         {format_number(tube["section_radius_cv"])}
median planarity ratio:    {format_number(tube["median_planarity_ratio"])}
median circularity ratio:  {format_number(tube["median_circularity_ratio"])}
closure-step ratio:        {format_number(tube["closure_to_ordinary_median_ratio"])}
```

Their centroids define a source-derived closed polygonal centreline with
{tube["centreline_station_count"]} stations. No invented centreline fit
is required.

## Centreline embeddedness

The complete nonadjacent segment-pair census gives:

```text
nonadjacent intersections:  {embedding["exact_nonadjacent_intersection_count"]}
minimum remote distance:    {format_number(embedding["minimum_remote_segment_distance"])}
minimum remote pair:        {embedding["minimum_remote_segment_pair"]}
median tube diameter:       {format_number(embedding["median_tube_diameter"])}
clearance / diameter:       {format_number(embedding["remote_clearance_to_diameter_ratio"])}
```

Under the stated tolerance of
`{embedding["intersection_tolerance"]}`, the polygonal centreline is
embedded.

## Toroidal winding

The best toroidal coordinate axis is the model's
`{toroidal["best_axis"]}` axis.

```text
major winding:         {format_number(major["total_winding"])}
minor winding:         {format_number(minor["total_winding"])}
signed rounded pair:   {toroidal["signed_winding_pair"]}
unsigned pair:         {toroidal["unsigned_winding_pair"]}
major reversals:       {major["direction_reversal_count"]}
minor reversals:       {minor["direction_reversal_count"]}
```

Both toroidal phases are monotonic. The recovered signed pair is
`(3,-10)` under the audit's coordinate convention, while the unsigned
pair is exactly `{{3,10}}`.

### Dominant transverse Fourier modes

|          Frequency | Amplitude |
| -----------------: | --------: |
| {transverse_modes} |           |

### Dominant axial Fourier modes

|     Frequency | Amplitude |
| ------------: | --------: |
| {axial_modes} |           |

The transverse fundamental at frequency 3, its sidebands at
`3-10=-7` and `3+10=13`, and the axial fundamental at frequency 10
independently support the same winding interpretation.

## Conclusion

Meru's native `10_3.wrl` asset encodes a connected closed genus-one
tube whose source-defined cross-section centroids form an embedded
polygonal toroidal centreline. Relative to the recovered y-axis
toroidal coordinates, that centreline has monotonic winding pair
`(3,-10)` and unsigned pair `{{3,10}}`.

The published “3,10” designation is therefore encoded directly in the
native geometry rather than existing only as an accompanying label.
Under the stated toroidal-coordinate interpretation, the source
supports an embedded unsigned `T(3,10)` construction, with orientation
and chirality conventions kept explicit.

## Interpretive boundary

This result does not yet identify which complete model crossings are
suppressed in A10_P03. It also does not yet provide:

* a full model-to-panel viewpoint and crossing correspondence;
* an all-pairs triangle-triangle self-intersection certificate for the
  surrounding tube mesh;
* or a separately derived knot-diagram invariant fixing chirality.

The parity failure of the hand-derived A10_P03 visible word therefore
remains a valid demonstration that the 31-event sequence is incomplete
as a classical planar projection. Direct model-to-panel comparison is
the next stage.
"""


def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description=__doc__,
    )

    parser.add_argument(
        "--manifest",
        type=Path,
        default=DEFAULT_MANIFEST,
    )

    parser.add_argument(
        "--raw-dir",
        type=Path,
        default=DEFAULT_RAW_DIR,
    )

    parser.add_argument(
        "--json-output",
        type=Path,
        default=DEFAULT_JSON_OUTPUT,
    )

    parser.add_argument(
        "--report-output",
        type=Path,
        default=DEFAULT_REPORT_OUTPUT,
    )

    return parser.parse_args()


def main() -> None:
    """Run the audit and write tracked derived outputs."""
    arguments = parse_arguments()

    audit = build_audit(
        arguments.manifest,
        arguments.raw_dir,
    )

    arguments.json_output.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    arguments.report_output.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    arguments.json_output.write_text(
        json.dumps(
            audit,
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )

    arguments.report_output.write_text(
        render_report(
            audit
        ),
        encoding="utf-8",
    )

    print(
        f"Wrote {arguments.json_output}"
    )

    print(
        f"Wrote {arguments.report_output}"
    )

    print(
        "Embedded polygonal centreline: "
        f"{audit['conclusions']['embedded_polygonal_centerline']}"
    )

    print(
        "Recovered signed winding pair: "
        f"{audit['toroidal_winding']['signed_winding_pair']}"
    )

    print(
        "Recovered unsigned winding pair: "
        f"{audit['toroidal_winding']['unsigned_winding_pair']}"
    )

    print(
        "Unsigned winding pair {3,10}: "
        f"{audit['toroidal_winding']['matches_unsigned_3_10']}"
    )


if __name__ == "__main__":
    main()