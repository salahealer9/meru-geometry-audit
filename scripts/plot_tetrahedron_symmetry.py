#!/usr/bin/env python3
"""Visualise the regular tetrahedron and its proper rotations."""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np

from meru_geometry.projections import orthographic_project
from meru_geometry.rotations import tetrahedral_rotation_group
from meru_geometry.tetrahedron import (
    regular_tetrahedron,
    tetrahedron_edges,
)


ROOT = Path(__file__).resolve().parents[1]
FIGURE_DIR = ROOT / "figures"


def plot_regular_tetrahedron() -> Path:
    """Plot the normalised tetrahedron in three dimensions."""
    vertices = regular_tetrahedron()
    edges = tetrahedron_edges()

    output_path = FIGURE_DIR / "regular_tetrahedron_baseline.png"

    fig = plt.figure(figsize=(8, 7))
    ax = fig.add_subplot(111, projection="3d")

    for start, end in edges:
        segment = vertices[[start, end]]
        ax.plot(
            segment[:, 0],
            segment[:, 1],
            segment[:, 2],
            linewidth=1.5,
        )

    ax.scatter(
        vertices[:, 0],
        vertices[:, 1],
        vertices[:, 2],
        s=45,
    )

    for label, vertex in zip(
        ("A", "B", "C", "D"),
        vertices,
        strict=True,
    ):
        ax.text(
            vertex[0],
            vertex[1],
            vertex[2],
            f" {label}",
        )

    limit = 1.1
    ax.set_xlim(-limit, limit)
    ax.set_ylim(-limit, limit)
    ax.set_zlim(-limit, limit)
    ax.set_box_aspect((1, 1, 1))

    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")
    ax.set_title("Regular tetrahedron with unit circumradius")

    fig.tight_layout()
    fig.savefig(output_path, dpi=220)
    plt.close(fig)

    return output_path


def diagnostic_probe(
    vertices: np.ndarray,
) -> np.ndarray:
    """Construct a deterministic asymmetric polyline inside the tetrahedron."""
    barycentric_weights = np.asarray(
        [
            [0.58, 0.18, 0.14, 0.10],
            [0.24, 0.47, 0.19, 0.10],
            [0.12, 0.20, 0.53, 0.15],
            [0.10, 0.16, 0.25, 0.49],
        ],
        dtype=np.float64,
    )

    return barycentric_weights @ vertices


def plot_rotation_projections() -> Path:
    """Plot projections of an asymmetric probe under all 12 rotations."""
    vertices = regular_tetrahedron()
    edges = tetrahedron_edges()
    rotations = tetrahedral_rotation_group()
    probe = diagnostic_probe(vertices)

    output_path = (
        FIGURE_DIR / "tetrahedral_rotation_probe_projections.png"
    )

    all_projected = [
        orthographic_project(vertices, rotation=rotation)
        for rotation in rotations
    ]

    coordinate_limit = max(
        float(np.max(np.abs(projected)))
        for projected in all_projected
    )
    coordinate_limit *= 1.15

    fig, axes = plt.subplots(
        3,
        4,
        figsize=(12, 9),
        constrained_layout=True,
    )

    for index, (axis, rotation) in enumerate(
        zip(axes.flat, rotations, strict=True),
        start=1,
    ):
        projected_vertices = orthographic_project(
            vertices,
            rotation=rotation,
        )
        projected_probe = orthographic_project(
            probe,
            rotation=rotation,
        )

        for start, end in edges:
            segment = projected_vertices[[start, end]]
            axis.plot(
                segment[:, 0],
                segment[:, 1],
                linewidth=0.9,
            )

        axis.plot(
            projected_probe[:, 0],
            projected_probe[:, 1],
            marker="o",
            linewidth=1.5,
            markersize=3.5,
        )

        for label, point in zip(
            ("A", "B", "C", "D"),
            projected_vertices,
            strict=True,
        ):
            axis.text(
                point[0],
                point[1],
                label,
                fontsize=8,
            )

        axis.set_xlim(-coordinate_limit, coordinate_limit)
        axis.set_ylim(-coordinate_limit, coordinate_limit)
        axis.set_aspect("equal")
        axis.set_title(f"Rotation {index:02d}")
        axis.set_xticks([])
        axis.set_yticks([])

    fig.suptitle(
        "Orthographic projections of an asymmetric diagnostic probe\n"
        "under the 12 proper tetrahedral rotations"
    )

    fig.savefig(output_path, dpi=220)
    plt.close(fig)

    return output_path


def main() -> None:
    """Generate both tetrahedral baseline figures."""
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)

    for output_path in (
        plot_regular_tetrahedron(),
        plot_rotation_projections(),
    ):
        print(f"Wrote {output_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
