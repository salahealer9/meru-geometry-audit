#!/usr/bin/env python3
"""Reproduce the complete A10_P03 global-cycle audit."""

from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D

from meru_geometry.global_cycle import (
    GlobalCycleAudit,
    Node,
    audit_global_cycle,
    format_segment_visit,
)


ROOT = Path(__file__).resolve().parents[1]

DATA_DIR = (
    ROOT
    / "data"
    / "manual_digitizations"
    / "A10_P03"
)

REPORT_PATH = (
    ROOT
    / "docs"
    / "geometry"
    / "a10_p03_global_cycle_v0_6.md"
)

FIGURE_PATH = (
    ROOT
    / "figures"
    / "a10_p03_global_cycle.png"
)

LAYERS = ("red", "green", "blue")

COLOURS = {
    "red": "tab:red",
    "green": "tab:green",
    "blue": "tab:blue",
}

EXPECTED_TRAVERSAL = (
    "R:S01+",
    "R:S02+",
    "R:S03+",
    "R:S04−",
    "R:S05+",
    "R:S06−",
    "R:S07+",
    "G:S11−",
    "G:S10−",
    "G:S09−",
    "G:S08−",
    "G:S07+",
    "G:S06−",
    "G:S05−",
    "G:S04−",
    "G:S03+",
    "G:S02−",
    "G:S01−",
    "B:S01+",
    "B:S02−",
    "B:S03+",
    "B:S04+",
    "B:S05+",
    "B:S06+",
)

EXPECTED_TRANSITIONS = (
    "X_RG_R_S07E_G_S11E",
    "X_GB_G_S01S_B_S01S",
    "X_RB_R_S01S_B_S06E",
)


def load_segments() -> dict[
    str,
    dict[int, np.ndarray],
]:
    """Load visible segment coordinates with one-based IDs."""
    raw: dict[
        str,
        dict[int, list[tuple[int, float, float]]],
    ] = defaultdict(
        lambda: defaultdict(list)
    )

    path = DATA_DIR / "digitization.csv"

    with path.open(
        newline="",
        encoding="utf-8",
    ) as handle:
        for row in csv.DictReader(handle):
            layer = row["layer"]

            if layer not in LAYERS:
                continue

            segment_id = (
                int(row["segment_id"]) + 1
            )

            raw[layer][segment_id].append(
                (
                    int(row["point_index"]),
                    float(row["panel_x"]),
                    float(row["panel_y"]),
                )
            )

    result: dict[
        str,
        dict[int, np.ndarray],
    ] = {}

    for layer, layer_segments in raw.items():
        result[layer] = {}

        for segment_id, records in layer_segments.items():
            records.sort(
                key=lambda record: record[0]
            )

            result[layer][segment_id] = (
                np.asarray(
                    [
                        [record[1], record[2]]
                        for record in records
                    ],
                    dtype=np.float64,
                )
            )

    return result


def load_accepted(
    filename: str,
) -> list[dict[str, str]]:
    """Load accepted rows from one review table."""
    path = DATA_DIR / filename

    with path.open(
        newline="",
        encoding="utf-8",
    ) as handle:
        return [
            row
            for row in csv.DictReader(handle)
            if row["status"] == "accepted"
        ]


def endpoint_coordinate(
    segments: dict[
        str,
        dict[int, np.ndarray],
    ],
    node: Node,
) -> np.ndarray:
    """Return the source coordinate of one endpoint node."""
    layer, segment_id, endpoint = node
    points = segments[layer][segment_id]

    if endpoint == "start":
        return points[0]

    if endpoint == "end":
        return points[-1]

    raise ValueError(
        f"Unsupported endpoint: {endpoint}"
    )


def validate_expected_result(
    audit: GlobalCycleAudit,
) -> None:
    """Freeze the exact v0.6 global-cycle invariants."""
    traversal = tuple(
        format_segment_visit(visit)
        for visit in audit.segment_traversal
    )

    assert audit.is_single_cycle
    assert audit.visible_segment_count == 24
    assert (
        audit.same_colour_connection_count
        == 21
    )
    assert (
        audit.cross_colour_transition_count
        == 3
    )
    assert audit.vertex_count == 48
    assert audit.edge_count == 48
    assert audit.component_count == 1
    assert audit.degree_map == {2: 48}
    assert traversal == EXPECTED_TRAVERSAL
    assert (
        audit.cross_colour_transitions
        == EXPECTED_TRANSITIONS
    )


def plot_global_cycle(
    segments: dict[
        str,
        dict[int, np.ndarray],
    ],
    audit: GlobalCycleAudit,
) -> None:
    """Plot visible paths and every accepted connection."""
    figure, axis = plt.subplots(
        figsize=(11, 9),
        constrained_layout=True,
    )

    traversal_order = {
        (
            visit.layer,
            visit.segment_id,
        ): index
        for index, visit in enumerate(
            audit.segment_traversal,
            start=1,
        )
    }

    for layer in LAYERS:
        for segment_id in sorted(
            segments[layer]
        ):
            points = segments[layer][
                segment_id
            ]

            axis.plot(
                points[:, 0],
                points[:, 1],
                color=COLOURS[layer],
                linewidth=2.2,
                marker="o",
                markersize=2.4,
                zorder=3,
            )

            midpoint = points[
                len(points) // 2
            ]

            order = traversal_order[
                (layer, segment_id)
            ]

            axis.annotate(
                str(order),
                midpoint,
                fontsize=7,
                fontweight="bold",
                ha="center",
                va="center",
                bbox={
                    "boxstyle": "circle,pad=0.15",
                    "facecolor": "white",
                    "edgecolor": COLOURS[layer],
                    "linewidth": 0.7,
                    "alpha": 0.9,
                },
                zorder=8,
            )

    for edge in audit.edges:
        if edge.kind == "visible_segment":
            continue

        point_a = endpoint_coordinate(
            segments,
            edge.node_a,
        )

        point_b = endpoint_coordinate(
            segments,
            edge.node_b,
        )

        if edge.kind == "same_colour":
            layer = edge.node_a[0]

            axis.plot(
                [point_a[0], point_b[0]],
                [point_a[1], point_b[1]],
                linestyle="--",
                linewidth=1.4,
                color=COLOURS[layer],
                alpha=0.75,
                zorder=2,
            )

        elif edge.kind == "cross_colour":
            axis.plot(
                [point_a[0], point_b[0]],
                [point_a[1], point_b[1]],
                linewidth=3.0,
                color="black",
                zorder=6,
            )

            axis.scatter(
                [point_a[0], point_b[0]],
                [point_a[1], point_b[1]],
                s=80,
                facecolors="white",
                edgecolors="black",
                linewidths=1.5,
                zorder=7,
            )

            midpoint = (
                point_a + point_b
            ) / 2.0

            axis.annotate(
                edge.identifier.replace(
                    "X_",
                    "",
                ),
                midpoint,
                xytext=(5, 5),
                textcoords="offset points",
                fontsize=7,
                color="black",
                zorder=9,
            )

    axis.set_aspect("equal")
    axis.invert_yaxis()
    axis.grid(True, alpha=0.18)
    axis.set_xlabel("Panel x (pixels)")
    axis.set_ylabel("Panel y (pixels)")

    axis.set_title(
        "A10_P03 source-derived global cycle\n"
        "24 visible fragments · "
        "21 same-colour continuations · "
        "3 colour transitions"
    )

    legend_handles = [
        Line2D(
            [0],
            [0],
            color="black",
            linewidth=2.2,
            label="Visible traced fragment",
        ),
        Line2D(
            [0],
            [0],
            color="black",
            linestyle="--",
            linewidth=1.4,
            label=(
                "Accepted same-colour "
                "occlusion"
            ),
        ),
        Line2D(
            [0],
            [0],
            color="black",
            linewidth=3.0,
            marker="o",
            markerfacecolor="white",
            label="Accepted colour transition",
        ),
    ]

    axis.legend(
        handles=legend_handles,
        loc="upper left",
    )

    figure.savefig(
        FIGURE_PATH,
        dpi=220,
    )

    plt.close(figure)

    print(
        f"Wrote {FIGURE_PATH.relative_to(ROOT)}"
    )


def write_report(
    audit: GlobalCycleAudit,
) -> None:
    """Write the permanent v0.6 global-cycle report."""
    traversal = tuple(
        format_segment_visit(visit)
        for visit in audit.segment_traversal
    )

    lines = [
        "# A10_P03 Global Cycle Audit — v0.6",
        "",
        "## Result",
        "",
        "All 24 visible coloured fragments form one connected, "
        "non-branched closed cycle under the manually adjudicated "
        "source continuations.",
        "",
        "## Graph invariants",
        "",
        "| Quantity | Value |",
        "|---|---:|",
        f"| Visible segment edges | "
        f"{audit.visible_segment_count} |",
        f"| Same-colour connection edges | "
        f"{audit.same_colour_connection_count} |",
        f"| Cross-colour transition edges | "
        f"{audit.cross_colour_transition_count} |",
        f"| Endpoint vertices | "
        f"{audit.vertex_count} |",
        f"| Total graph edges | "
        f"{audit.edge_count} |",
        f"| Connected components | "
        f"{audit.component_count} |",
        f"| Degree-two vertices | "
        f"{audit.degree_map.get(2, 0)} |",
        "",
        "The graph satisfies",
        "",
        r"\[",
        r"|V|=48,\qquad |E|=48,\qquad "
        r"\deg(v)=2\ \text{for every }v,\qquad c=1.",
        r"\]",
        "",
        "A finite connected graph in which every vertex has degree "
        "two is a single cycle. The equality \\(|E|=|V|\\) is "
        "consistent with the same result.",
        "",
        "## Canonical traversal",
        "",
        "Starting at the beginning of red segment S01 and traversing "
        "its visible edge first gives:",
        "",
        "```text",
        " → ".join(traversal),
        "```",
        "",
        "Every visible segment appears exactly once in the traversal.",
        "",
        "## Cross-colour transitions",
        "",
    ]

    for identifier in (
        audit.cross_colour_transitions
    ):
        lines.append(f"- `{identifier}`")

    lines.extend(
        [
            "",
            "The transitions occur at the three manually reviewed "
            "equatorial colour junctions. Together they connect the "
            "red, green and blue open chains into one closed cycle.",
            "",
            "## Evidence chain",
            "",
            "The global result combines:",
            "",
            "1. the manual A10_P03 trace;",
            "2. 15 first-stage accepted occlusion continuations;",
            "3. 6 accepted residual same-colour continuations;",
            "4. 3 accepted cross-colour transitions;",
            "5. an exact endpoint graph audit.",
            "",
            "No endpoint is used by more than one adjudicated "
            "connection, and no endpoint remains free.",
            "",
            "## Interpretation boundary",
            "",
            "This result establishes source-supported "
            "two-dimensional connectivity.",
            "",
            "It does not establish:",
            "",
            "- the exact shape of each hidden interpolation;",
            "- complete over-under depth information;",
            "- a unique three-dimensional embedding;",
            "- a unique dimpled-surface equation;",
            "- equivalence with a canonical \\((3,10)\\) torus knot;",
            "- the claimed Hebrew-letter projection system.",
            "",
            "## Generated output",
            "",
            "- `figures/a10_p03_global_cycle.png`",
            "",
        ]
    )

    REPORT_PATH.write_text(
        "\n".join(lines),
        encoding="utf-8",
    )

    print(
        f"Wrote {REPORT_PATH.relative_to(ROOT)}"
    )


def main() -> None:
    """Run the complete reproducible global-cycle audit."""
    segments = load_segments()

    segment_ids = {
        layer: segments[layer].keys()
        for layer in LAYERS
    }

    same_colour = (
        load_accepted(
            "endpoint_adjudication.csv"
        )
        + load_accepted(
            "residual_endpoint_review.csv"
        )
    )

    cross_colour = load_accepted(
        "cross_colour_endpoint_review.csv"
    )

    audit = audit_global_cycle(
        segment_ids,
        same_colour,
        cross_colour,
    )

    validate_expected_result(audit)
    plot_global_cycle(segments, audit)
    write_report(audit)

    print()
    print("Global graph audit")
    print("==================")
    print(
        "Visible segments:         ",
        audit.visible_segment_count,
    )
    print(
        "Same-colour connections:  ",
        audit.same_colour_connection_count,
    )
    print(
        "Cross-colour transitions: ",
        audit.cross_colour_transition_count,
    )
    print(
        "Endpoint vertices:        ",
        audit.vertex_count,
    )
    print(
        "Total graph edges:        ",
        audit.edge_count,
    )
    print(
        "Connected components:     ",
        audit.component_count,
    )
    print(
        "Vertex degrees:            ",
        audit.degree_map,
    )
    print()
    print("Cycle traversal:")
    print(
        " → ".join(
            format_segment_visit(visit)
            for visit
            in audit.segment_traversal
        )
    )
    print()
    print("Cross-colour transitions:")

    for identifier in (
        audit.cross_colour_transitions
    ):
        print(" ", identifier)

    print()
    print(
        "PASS: all 24 visible fragments form one "
        "connected, non-branched closed cycle."
    )


if __name__ == "__main__":
    main()
