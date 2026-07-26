#!/usr/bin/env python3
"""Audit projection capacity under the tetrahedral rotation group."""

from __future__ import annotations

import csv
from pathlib import Path
from typing import NamedTuple

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np

from meru_geometry.embeddings import (
    candidate_reciprocal_torus_embedding,
)
from meru_geometry.projection_orbits import (
    camera_direction,
    camera_direction_classes,
    equivalence_classes_from_errors,
    pairwise_curve_alignment_errors,
)
from meru_geometry.projections import orthographic_project
from meru_geometry.rotations import tetrahedral_rotation_group
from meru_geometry.tetrahedron import regular_tetrahedron
from meru_geometry.torus import torus_knot


ROOT = Path(__file__).resolve().parents[1]
FIGURE_DIR = ROOT / "figures"
DERIVED_DIR = ROOT / "data" / "derived"
REPORT_PATH = (
    ROOT
    / "docs"
    / "geometry"
    / "projection_orbit_results_v0_5.md"
)
PAIRWISE_PATH = (
    DERIVED_DIR
    / "projection_orbit_pairwise_errors.csv"
)

EQUIVALENCE_TOLERANCE = 1.0e-8


class ObjectSpecification(NamedTuple):
    """Projected-object analysis settings."""

    name: str
    label: str
    points: np.ndarray
    closed: bool
    allow_reversal: bool


def diagnostic_probe() -> np.ndarray:
    """Return the asymmetric tetrahedral probe used in v0.3."""
    vertices = regular_tetrahedron()

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


def build_objects() -> tuple[ObjectSpecification, ...]:
    """Construct all objects used in the projection-orbit audit."""
    knot = torus_knot(
        3,
        10,
        major_radius=2.0,
        minor_radius=0.72,
        n_points=721,
    )

    candidate = candidate_reciprocal_torus_embedding(
        theta_start=0.5,
        toroidal_turns=1.5,
        poloidal_turns=1.0,
        major_radius=2.0,
        minor_radius=0.72,
        n_points=721,
    )

    return (
        ObjectSpecification(
            name="diagnostic_probe",
            label="Asymmetric diagnostic probe",
            points=diagnostic_probe(),
            closed=False,
            allow_reversal=False,
        ),
        ObjectSpecification(
            name="torus_knot_3_10",
            label=r"Canonical $(3,10)$ torus knot",
            points=knot,
            closed=True,
            allow_reversal=True,
        ),
        ObjectSpecification(
            name="candidate_c0",
            label="Candidate C0 reciprocal-torus curve",
            points=candidate.points,
            closed=False,
            allow_reversal=False,
        ),
    )


def format_classes(
    classes: tuple[tuple[int, ...], ...],
) -> str:
    """Format zero-based classes using one-based rotation labels."""
    formatted = []

    for group in classes:
        members = ", ".join(
            f"R{index + 1:02d}"
            for index in group
        )
        formatted.append("{" + members + "}")

    return ", ".join(formatted)


def class_id_map(
    classes: tuple[tuple[int, ...], ...],
) -> dict[int, int]:
    """Map each rotation index to its one-based class identifier."""
    mapping: dict[int, int] = {}

    for class_identifier, group in enumerate(
        classes,
        start=1,
    ):
        for rotation_index in group:
            mapping[rotation_index] = class_identifier

    return mapping


def write_pairwise_csv(
    results: dict[
        str,
        dict[str, np.ndarray],
    ],
) -> None:
    """Write all pairwise alignment errors to a local derived CSV."""
    DERIVED_DIR.mkdir(parents=True, exist_ok=True)

    with PAIRWISE_PATH.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as handle:
        writer = csv.writer(
            handle,
            lineterminator="\n",
        )

        writer.writerow(
            [
                "object",
                "equivalence_mode",
                "rotation_i",
                "rotation_j",
                "relative_rms",
            ]
        )

        for object_name, mode_results in results.items():
            for mode_name, matrix in mode_results.items():
                for first in range(matrix.shape[0]):
                    for second in range(
                        first + 1,
                        matrix.shape[1],
                    ):
                        writer.writerow(
                            [
                                object_name,
                                mode_name,
                                first + 1,
                                second + 1,
                                f"{matrix[first, second]:.17g}",
                            ]
                        )

    print(f"Wrote {PAIRWISE_PATH.relative_to(ROOT)}")


def plot_candidate_projections(
    projections: list[np.ndarray],
) -> Path:
    """Plot candidate C0 under all 12 tetrahedral rotations."""
    output_path = (
        FIGURE_DIR
        / "candidate_c0_tetrahedral_projections.png"
    )

    coordinate_limit = max(
        float(np.max(np.abs(projected)))
        for projected in projections
    )
    coordinate_limit *= 1.08

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
            linewidth=1.2,
        )

        axis.scatter(
            projected[0, 0],
            projected[0, 1],
            s=18,
            label="start",
        )

        axis.scatter(
            projected[-1, 0],
            projected[-1, 1],
            s=18,
            label="end",
        )

        axis.set_xlim(-coordinate_limit, coordinate_limit)
        axis.set_ylim(-coordinate_limit, coordinate_limit)
        axis.set_aspect("equal")
        axis.set_title(f"Rotation {index:02d}")
        axis.set_xticks([])
        axis.set_yticks([])

    fig.suptitle(
        "Orthographic projections of candidate C0\n"
        "under the 12 proper tetrahedral rotations"
    )

    axes.flat[0].legend(
        loc="upper right",
        fontsize=7,
    )

    fig.savefig(output_path, dpi=220)
    plt.close(fig)

    print(f"Wrote {output_path.relative_to(ROOT)}")
    return output_path


def plot_error_matrices(
    objects: tuple[ObjectSpecification, ...],
    results: dict[
        str,
        dict[str, np.ndarray],
    ],
) -> Path:
    """Plot SO(2) and O(2) pairwise relative-error matrices."""
    output_path = (
        FIGURE_DIR
        / "projection_orbit_error_matrices.png"
    )

    fig, axes = plt.subplots(
        len(objects),
        2,
        figsize=(10, 13),
        constrained_layout=True,
    )

    for row, specification in enumerate(objects):
        matrices = results[specification.name]

        for column, mode_name in enumerate(
            ("SO2", "O2"),
        ):
            axis = axes[row, column]
            matrix = matrices[mode_name]

            displayed = np.log10(
                np.maximum(matrix, 1.0e-16)
            )

            image = axis.imshow(
                displayed,
                origin="upper",
                vmin=-16.0,
                vmax=0.0,
            )

            axis.set_title(
                f"{specification.label}\n"
                f"{mode_name} equivalence"
            )
            axis.set_xlabel("Rotation")
            axis.set_ylabel("Rotation")
            axis.set_xticks(range(12))
            axis.set_yticks(range(12))
            axis.set_xticklabels(
                range(1, 13),
                fontsize=7,
            )
            axis.set_yticklabels(
                range(1, 13),
                fontsize=7,
            )

            colorbar = fig.colorbar(
                image,
                ax=axis,
                shrink=0.78,
            )
            colorbar.set_label(
                r"$\log_{10}$ relative RMS"
            )

    fig.savefig(output_path, dpi=220)
    plt.close(fig)

    print(f"Wrote {output_path.relative_to(ROOT)}")
    return output_path


def write_report(
    rotations: np.ndarray,
    signed_classes: tuple[tuple[int, ...], ...],
    axis_classes: tuple[tuple[int, ...], ...],
    objects: tuple[ObjectSpecification, ...],
    results: dict[
        str,
        dict[str, np.ndarray],
    ],
) -> None:
    """Write a reproducible Markdown report of the audit results."""
    signed_ids = class_id_map(signed_classes)
    axis_ids = class_id_map(axis_classes)

    lines = [
        "# Projection-Orbit Results — v0.5",
        "",
        "## Exact camera-direction orbit",
        "",
        "For each tetrahedral rotation, the viewing direction is",
        "",
        r"\[",
        r"n_i=R_i^\mathsf{T}\hat z.",
        r"\]",
        "",
        "| Rotation | Camera direction | Signed class | Axis class |",
        "|---:|---|---:|---:|",
    ]

    for index, rotation in enumerate(rotations):
        direction = camera_direction(rotation)

        direction_text = (
            f"({direction[0]:.0f}, "
            f"{direction[1]:.0f}, "
            f"{direction[2]:.0f})"
        )

        lines.append(
            f"| R{index + 1:02d} | `{direction_text}` | "
            f"{signed_ids[index]} | {axis_ids[index]} |"
        )

    lines.extend(
        [
            "",
            "### Exact class structure",
            "",
            f"- Signed camera-direction classes: "
            f"**{len(signed_classes)}**.",
            f"- Unoriented viewing-axis classes: "
            f"**{len(axis_classes)}**.",
            f"- Signed classes: {format_classes(signed_classes)}.",
            f"- Axis classes: {format_classes(axis_classes)}.",
            "",
            "Thus the 12 proper tetrahedral rotations provide at most "
            "**six front/back-sensitive views**, or **three viewing axes** "
            "when planar reflection is allowed.",
            "",
            "## Object-specific projection classes",
            "",
            "The table below uses a relative-RMS equivalence threshold of "
            f"`{EQUIVALENCE_TOLERANCE:.0e}`.",
            "",
            "| Object | SO(2) classes | O(2) classes | "
            "Closed shift/reversal handling |",
            "|---|---:|---:|---|",
        ]
    )

    object_class_results: dict[
        str,
        dict[str, tuple[tuple[int, ...], ...]],
    ] = {}

    for specification in objects:
        so2_classes = equivalence_classes_from_errors(
            results[specification.name]["SO2"],
            tolerance=EQUIVALENCE_TOLERANCE,
        )
        o2_classes = equivalence_classes_from_errors(
            results[specification.name]["O2"],
            tolerance=EQUIVALENCE_TOLERANCE,
        )

        object_class_results[specification.name] = {
            "SO2": so2_classes,
            "O2": o2_classes,
        }

        handling = (
            "Cyclic shifts and traversal reversal allowed"
            if specification.closed
            else "Open ordered curve; neither allowed"
        )

        lines.append(
            f"| {specification.label} | "
            f"{len(so2_classes)} | "
            f"{len(o2_classes)} | "
            f"{handling} |"
        )

    for specification in objects:
        classes = object_class_results[specification.name]

        lines.extend(
            [
                "",
                f"### {specification.label}",
                "",
                "**SO(2) classes:** "
                f"{format_classes(classes['SO2'])}.",
                "",
                "**O(2) classes:** "
                f"{format_classes(classes['O2'])}.",
            ]
        )

    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "The exact camera calculation establishes that the 12 group "
            "elements are not 12 independent directions. Rotations sharing "
            "a signed camera direction differ only by an in-plane rotation. "
            "Opposite directions along the same axis differ by an in-plane "
            "reflection.",
            "",
            "Any object-specific class count below six under SO(2), or below "
            "three under O(2), is caused by additional symmetry of the object.",
            "",
            "A literal claim that one fixed object generates 22 independent "
            "letterforms solely through the 12 proper rotations of one "
            "tetrahedron is therefore mathematically incomplete. Additional "
            "viewing, tracing, truncation, gesture, component-selection, or "
            "continuous-orientation rules would be required.",
            "",
            "This result does not determine which additional operations, if "
            "any, were intended in the historical Meru construction.",
            "",
            "## Generated outputs",
            "",
            "- `figures/candidate_c0_tetrahedral_projections.png`",
            "- `figures/projection_orbit_error_matrices.png`",
            "- `data/derived/projection_orbit_pairwise_errors.csv` "
            "(local reproducible output; ignored by Git)",
            "",
        ]
    )

    REPORT_PATH.write_text(
        "\n".join(lines),
        encoding="utf-8",
    )

    print(f"Wrote {REPORT_PATH.relative_to(ROOT)}")


def main() -> None:
    """Run the complete v0.5 projection-orbit audit."""
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)
    DERIVED_DIR.mkdir(parents=True, exist_ok=True)

    rotations = tetrahedral_rotation_group()

    signed_classes = camera_direction_classes(
        rotations,
        unoriented=False,
    )
    axis_classes = camera_direction_classes(
        rotations,
        unoriented=True,
    )

    objects = build_objects()

    results: dict[
        str,
        dict[str, np.ndarray],
    ] = {}

    projection_cache: dict[str, list[np.ndarray]] = {}

    for specification in objects:
        projections = [
            orthographic_project(
                specification.points,
                rotation=rotation,
            )
            for rotation in rotations
        ]

        projection_cache[specification.name] = projections

        so2_errors = pairwise_curve_alignment_errors(
            projections,
            closed=specification.closed,
            allow_reversal=specification.allow_reversal,
            allow_reflection=False,
            allow_scale=True,
        )

        o2_errors = pairwise_curve_alignment_errors(
            projections,
            closed=specification.closed,
            allow_reversal=specification.allow_reversal,
            allow_reflection=True,
            allow_scale=True,
        )

        results[specification.name] = {
            "SO2": so2_errors,
            "O2": o2_errors,
        }

    write_pairwise_csv(results)

    plot_candidate_projections(
        projection_cache["candidate_c0"]
    )

    plot_error_matrices(
        objects,
        results,
    )

    write_report(
        rotations,
        signed_classes,
        axis_classes,
        objects,
        results,
    )

    print()
    print(
        "Signed camera-direction classes:",
        len(signed_classes),
        format_classes(signed_classes),
    )
    print(
        "Unoriented viewing-axis classes:",
        len(axis_classes),
        format_classes(axis_classes),
    )

    for specification in objects:
        so2_classes = equivalence_classes_from_errors(
            results[specification.name]["SO2"],
            tolerance=EQUIVALENCE_TOLERANCE,
        )
        o2_classes = equivalence_classes_from_errors(
            results[specification.name]["O2"],
            tolerance=EQUIVALENCE_TOLERANCE,
        )

        print()
        print(specification.label)
        print(
            "  SO(2) classes:",
            len(so2_classes),
            format_classes(so2_classes),
        )
        print(
            "  O(2) classes:",
            len(o2_classes),
            format_classes(o2_classes),
        )


if __name__ == "__main__":
    main()
