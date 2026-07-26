"""Reproducible geometry tools for the Meru Foundation audit."""

from meru_geometry.projections import orthographic_project
from meru_geometry.reciprocal_spiral import reciprocal_spiral
from meru_geometry.rotations import (
    apply_rotation,
    is_rotation_matrix,
    tetrahedral_rotation_group,
    tetrahedral_rotation_permutations,
)
from meru_geometry.tetrahedron import (
    regular_tetrahedron,
    tetrahedron_centroid,
    tetrahedron_edge_lengths,
    tetrahedron_edges,
    tetrahedron_volume,
)

__version__ = "0.3.0"

__all__ = [
    "apply_rotation",
    "is_rotation_matrix",
    "orthographic_project",
    "reciprocal_spiral",
    "regular_tetrahedron",
    "tetrahedral_rotation_group",
    "tetrahedral_rotation_permutations",
    "tetrahedron_centroid",
    "tetrahedron_edge_lengths",
    "tetrahedron_edges",
    "tetrahedron_volume",
]
