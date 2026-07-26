"""Regular-tetrahedron geometry."""

from __future__ import annotations

from itertools import combinations

import numpy as np
from numpy.typing import NDArray


_EDGE_INDICES = np.asarray(
    list(combinations(range(4), 2)),
    dtype=np.int64,
)


def regular_tetrahedron(
    circumradius: float = 1.0,
) -> NDArray[np.float64]:
    """Return a regular tetrahedron centred at the origin.

    The baseline vertices are the four alternating corners of a cube,
    normalised to lie on the unit sphere.

    Parameters
    ----------
    circumradius:
        Distance from the centroid to every vertex. Must be positive.

    Returns
    -------
    numpy.ndarray
        Array of shape ``(4, 3)`` containing the tetrahedron vertices.
    """
    if not np.isfinite(circumradius):
        raise ValueError("circumradius must be finite.")
    if circumradius <= 0.0:
        raise ValueError("circumradius must be positive.")

    vertices = np.asarray(
        [
            [1.0, 1.0, 1.0],
            [1.0, -1.0, -1.0],
            [-1.0, 1.0, -1.0],
            [-1.0, -1.0, 1.0],
        ],
        dtype=np.float64,
    )

    vertices /= np.sqrt(3.0)
    vertices *= circumradius

    return vertices


def tetrahedron_edges() -> NDArray[np.int64]:
    """Return the six unordered vertex-index pairs."""
    return _EDGE_INDICES.copy()


def _validated_vertices(
    vertices: NDArray[np.float64],
) -> NDArray[np.float64]:
    """Validate and return a floating-point tetrahedron array."""
    array = np.asarray(vertices, dtype=np.float64)

    if array.shape != (4, 3):
        raise ValueError("vertices must have shape (4, 3).")
    if not np.isfinite(array).all():
        raise ValueError("vertices must contain only finite values.")

    return array


def tetrahedron_centroid(
    vertices: NDArray[np.float64],
) -> NDArray[np.float64]:
    """Return the centroid of four tetrahedron vertices."""
    array = _validated_vertices(vertices)
    return np.mean(array, axis=0)


def tetrahedron_edge_lengths(
    vertices: NDArray[np.float64],
) -> NDArray[np.float64]:
    """Return the six tetrahedron edge lengths."""
    array = _validated_vertices(vertices)
    differences = array[_EDGE_INDICES[:, 0]] - array[_EDGE_INDICES[:, 1]]
    return np.linalg.norm(differences, axis=1)


def tetrahedron_volume(
    vertices: NDArray[np.float64],
) -> float:
    """Return the unsigned volume of a tetrahedron."""
    array = _validated_vertices(vertices)

    basis = np.column_stack(
        (
            array[1] - array[0],
            array[2] - array[0],
            array[3] - array[0],
        )
    )

    return float(abs(np.linalg.det(basis)) / 6.0)
