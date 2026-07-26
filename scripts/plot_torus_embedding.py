#!/usr/bin/env python3
"""Visualise the canonical torus, (3,10) knot, and C0 candidate."""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np

from meru_geometry.embeddings import (
    candidate_reciprocal_torus_embedding,
)
from meru_geometry.projections import orthographic_project
from meru_geometry.rotations import tetrahedral_rotation_group
from meru_geometry.torus import torus_knot, torus_surface


ROOT = Path(__file__).resolve().parents[1]
FIGURE_DIR = ROOT / "figures"

MAJOR_RADIUS = 2.0
MINOR_RADIUS = 0.72


def torus_mesh() -> np.ndarray:
    """Return a plotting mesh for the canonical torus."""
    u = np.linspace(
        0.0,
        2.0 * np.pi,
        140,
        endpoint=True,
    )
    v = np.linspace(
        0.0,
        2.0 * np.pi,
        70,
        endpoint=True,
    )

    u_grid, v_grid = np.meshgrid(
        u,
        v,
        indexing="ij",
    )

    return torus_surface(
        u_grid,
        v_grid,
        major_radius=MAJOR_RADIUS,
        minor_radius=MINOR_RADIUS,
    )


def configure_3d_axis(
    axis: plt.Axes,
    title: str,
) -> None:
    """Apply common limits and labels to a 3D torus plot."""
    extent = MAJOR_RADIUS + MINOR_RADIUS + 0.15

    axis.set_xlim(-extent, extent)
    axis.set_ylim(-extent, extent)
    axis.set_zlim(-extent, extent)
    axis.set_box_aspect((1, 1, 1))

    axis.set_xlabel("x")
    axis.set_ylabel("y")
    axis.set_zlabel("z")
    axis.set_title(title)


def plot_torus_and_knot() -> Path:
    """Plot the canonical torus and standard (3,10) knot."""
    surface = torus_mesh()

    knot = torus_knot(
        3,
        10,
        major_radius=MAJOR_RADIUS,
        minor_radius=MINOR_RADIUS,
        n_points=6001,
    )

    output_path = (
        FIGURE_DIR / "canonical_torus_and_3_10_knot.png"
    )

    fig = plt.figure(figsize=(9, 8))
    axis = fig.add_subplot(111, projection="3d")

    axis.plot_surface(
        surface[..., 0],
        surface[..., 1],
        surface[..., 2],
        alpha=0.18,
        linewidth=0.0,
        antialiased=True,
    )

    axis.plot(
        knot[:, 0],
        knot[:, 1],
        knot[:, 2],
        linewidth=1.8,
    )

    axis.scatter(
        knot[0, 0],
        knot[0, 1],
        knot[0, 2],
        s=35,
        label="t = 0",
    )

    configure_3d_axis(
        axis,
        r"Canonical ring torus and $(3,10)$ torus knot",
    )
    axis.legend()

    fig.tight_layout()
    fig.savefig(output_path, dpi=220)
    plt.close(fig)

    return output_path


def plot_candidate_embedding() -> Path:
    """Plot candidate C0 on the canonical torus."""
    surface = torus_mesh()

    candidate = candidate_reciprocal_torus_embedding(
        theta_start=0.5,
        toroidal_turns=1.5,
        poloidal_turns=1.0,
        major_radius=MAJOR_RADIUS,
        minor_radius=MINOR_RADIUS,
        n_points=4000,
    )

    output_path = (
        FIGURE_DIR / "candidate_c0_reciprocal_torus_embedding.png"
    )

    fig = plt.figure(figsize=(9, 8))
    axis = fig.add_subplot(111, projection="3d")

    axis.plot_surface(
        surface[..., 0],
        surface[..., 1],
        surface[..., 2],
        alpha=0.18,
        linewidth=0.0,
        antialiased=True,
    )

    axis.plot(
        candidate.points[:, 0],
        candidate.points[:, 1],
        candidate.points[:, 2],
        linewidth=2.0,
    )

    axis.scatter(
        candidate.points[0, 0],
        candidate.points[0, 1],
        candidate.points[0, 2],
        s=40,
        label="start",
    )

    axis.scatter(
        candidate.points[-1, 0],
        candidate.points[-1, 1],
        candidate.points[-1, 2],
        s=40,
        label="end",
    )

    configure_3d_axis(
        axis,
        "Candidate C0: reciprocal-radius-to-poloidal-angle embedding",
    )
    axis.legend()

    fig.tight_layout()
    fig.savefig(output_path, dpi=220)
    plt.close(fig)

    return output_path


def plot_knot_projections() -> Path:
    """Plot the (3,10) knot under all proper tetrahedral rotations."""
    knot = torus_knot(
        3,
        10,
        major_radius=MAJOR_RADIUS,
        minor_radius=MINOR_RADIUS,
        n_points=6001,
    )

    rotations = tetrahedral_rotation_group()

    projections = [
        orthographic_project(
            knot,
            rotation=rotation,
        )
        for rotation in rotations
    ]

    coordinate_limit = max(
        float(np.max(np.abs(projected)))
        for projected in projections
    )
    coordinate_limit *= 1.08

    output_path = (
        FIGURE_DIR
        / "torus_knot_3_10_tetrahedral_projections.png"
    )

    fig, axes = plt.subplots(
        3,
        4,
        figsize=(12, 9),
        constrained_layout=True,
    )

    for index, (axis, projected) in enumerate(
        zip(axes.flat, projections, strict=True),
        start=1,
    ):
        axis.plot(
            projected[:, 0],
            projected[:, 1],
            linewidth=0.8,
        )

        axis.scatter(
            projected[0, 0],
            projected[0, 1],
            s=12,
        )

        axis.set_xlim(-coordinate_limit, coordinate_limit)
        axis.set_ylim(-coordinate_limit, coordinate_limit)
        axis.set_aspect("equal")
        axis.set_title(f"Rotation {index:02d}")
        axis.set_xticks([])
        axis.set_yticks([])

    fig.suptitle(
        r"Orthographic projections of the $(3,10)$ torus knot"
        "\nunder the 12 proper tetrahedral rotations"
    )

    fig.savefig(output_path, dpi=220)
    plt.close(fig)

    return output_path


def main() -> None:
    """Generate all v0.4 torus-baseline figures."""
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)

    output_paths = (
        plot_torus_and_knot(),
        plot_candidate_embedding(),
        plot_knot_projections(),
    )

    for output_path in output_paths:
        print(f"Wrote {output_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
