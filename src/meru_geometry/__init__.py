"""Reproducible geometry tools for the Meru Foundation audit."""

from meru_geometry.embeddings import (
    ReciprocalTorusCandidate,
    candidate_reciprocal_torus_embedding,
)
from meru_geometry.projection_orbits import (
    PlanarAlignment,
    best_curve_alignment,
    camera_direction,
    camera_direction_classes,
    equivalence_classes_from_errors,
    frame_planar_transform,
    pairwise_curve_alignment_errors,
    planar_similarity_alignment,
)
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
from meru_geometry.torus import (
    torus_implicit_residual,
    torus_knot,
    torus_surface,
)

__version__ = "0.6.0"

__all__ = [
    "PlanarAlignment",
    "ReciprocalTorusCandidate",
    "apply_rotation",
    "best_curve_alignment",
    "camera_direction",
    "camera_direction_classes",
    "candidate_reciprocal_torus_embedding",
    "equivalence_classes_from_errors",
    "frame_planar_transform",
    "is_rotation_matrix",
    "orthographic_project",
    "pairwise_curve_alignment_errors",
    "planar_similarity_alignment",
    "reciprocal_spiral",
    "regular_tetrahedron",
    "tetrahedral_rotation_group",
    "tetrahedral_rotation_permutations",
    "tetrahedron_centroid",
    "tetrahedron_edge_lengths",
    "tetrahedron_edges",
    "tetrahedron_volume",
    "torus_implicit_residual",
    "torus_knot",
    "torus_surface",
]
