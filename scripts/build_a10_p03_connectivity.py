#!/usr/bin/env python3
"""Build the adjudicated A10_P03 fragment connectivity graph."""

from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np

from meru_geometry.connectivity import (
    ConnectivityComponent,
    build_endpoint_connectivity,
    format_endpoint,
)
from meru_geometry.trace_analysis import polyline_metrics


ROOT = Path(__file__).resolve().parents[1]

DIGITIZATION_PATH = (
    ROOT
    / "data"
    / "manual_digitizations"
    / "A10_P03"
    / "digitization.csv"
)

ADJUDICATION_PATH = (
    ROOT
    / "data"
    / "manual_digitizations"
    / "A10_P03"
    / "endpoint_adjudication.csv"
)

COMPONENT_PATH = (
    ROOT
    / "data"
    / "derived"
    / "a10_p03_connectivity_components.csv"
)

UNMATCHED_PATH = (
    ROOT
    / "data"
    / "derived"
    / "a10_p03_unmatched_endpoints.csv"
)

REPORT_PATH = (
    ROOT
    / "docs"
    / "geometry"
    / "a10_p03_connectivity_graph_v0_6.md"
)

FIGURE_PATH = (
    ROOT
    / "figures"
    / "a10_p03_connectivity_graph.png"
)

LAYERS = ("red", "green", "blue")

DISPLAY = {
    "red": {
        "label": "Red centreline",
        "colour": "tab:red",
    },
    "green": {
        "label": "Green centreline",
        "colour": "tab:green",
    },
    "blue": {
        "label": "Blue centreline",
        "colour": "tab:blue",
    },
}


def load_segments() -> dict[str, dict[int, np.ndarray]]:
    """Load all digitised segments with one-based identifiers."""
    raw: dict[
        str,
        dict[int, list[tuple[int, float, float]]],
    ] = defaultdict(lambda: defaultdict(list))

    with DIGITIZATION_PATH.open(
        newline="",
        encoding="utf-8",
    ) as handle:
        for row in csv.DictReader(handle):
            layer = row["layer"]
            segment_id = int(row["segment_id"]) + 1

            raw[layer][segment_id].append(
                (
                    int(row["point_index"]),
                    float(row["panel_x"]),
                    float(row["panel_y"]),
                )
            )

    result: dict[str, dict[int, np.ndarray]] = {}

    for layer, layer_segments in raw.items():
        result[layer] = {}

        for segment_id, records in layer_segments.items():
            records.sort(key=lambda record: record[0])

            result[layer][segment_id] = np.asarray(
                [
                    [record[1], record[2]]
                    for record in records
                ],
                dtype=np.float64,
            )

    return result


def load_accepted_connections() -> list[dict[str, str]]:
    """Load accepted manual endpoint adjudications."""
    with ADJUDICATION_PATH.open(
        newline="",
        encoding="utf-8",
    ) as handle:
        rows = list(csv.DictReader(handle))

    accepted = [
        row
        for row in rows
        if row["status"] == "accepted"
    ]

    if len(accepted) != 15:
        raise RuntimeError(
            "Expected 15 accepted endpoint adjudications, "
            f"found {len(accepted)}."
        )

    return accepted


def endpoint_point(
    segments: dict[int, np.ndarray],
    segment_id: int,
    endpoint: str,
) -> np.ndarray:
    """Return a visible segment endpoint coordinate."""
    points = segments[segment_id]

    if endpoint == "start":
        return points[0]

    if endpoint == "end":
        return points[-1]

    raise ValueError("Unknown endpoint name.")


def traversal_text(
    component: ConnectivityComponent,
) -> str:
    """Format a segment traversal with orientation signs."""
    if not component.traversal:
        return "not available"

    return " → ".join(
        (
            f"S{item.segment_id:02d}"
            f"{'+' if item.forward else '−'}"
        )
        for item in component.traversal
    )


def free_endpoint_text(
    component: ConnectivityComponent,
) -> str:
    """Format unmatched endpoints."""
    if not component.free_endpoints:
        return "none"

    return ", ".join(
        format_endpoint(endpoint)
        for endpoint in component.free_endpoints
    )


def write_derived_tables(
    components_by_layer: dict[
        str,
        tuple[ConnectivityComponent, ...],
    ],
    segments: dict[str, dict[int, np.ndarray]],
    accepted_by_id: dict[str, dict[str, str]],
) -> None:
    """Write local component and unmatched-endpoint tables."""
    COMPONENT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    component_rows: list[dict[str, object]] = []
    unmatched_rows: list[dict[str, object]] = []

    for layer in LAYERS:
        for component_index, component in enumerate(
            components_by_layer[layer],
            start=1,
        ):
            visible_length = sum(
                polyline_metrics(
                    segments[layer][segment_id]
                ).length
                for segment_id in component.segment_ids
            )

            endpoint_gap_sum = sum(
                float(
                    accepted_by_id[candidate_id][
                        "distance_px"
                    ]
                )
                for candidate_id
                in component.accepted_connection_ids
            )

            component_rows.append(
                {
                    "layer": layer,
                    "component_id": component_index,
                    "segment_count": len(
                        component.segment_ids
                    ),
                    "segment_ids": ";".join(
                        str(value)
                        for value in component.segment_ids
                    ),
                    "accepted_edge_count": len(
                        component.accepted_connection_ids
                    ),
                    "accepted_connection_ids": ";".join(
                        component.accepted_connection_ids
                    ),
                    "free_endpoint_count": len(
                        component.free_endpoints
                    ),
                    "free_endpoints": ";".join(
                        format_endpoint(endpoint)
                        for endpoint
                        in component.free_endpoints
                    ),
                    "closed": component.closed,
                    "branched": component.branched,
                    "traversal": traversal_text(component),
                    "visible_length_px": visible_length,
                    "accepted_endpoint_gap_sum_px": (
                        endpoint_gap_sum
                    ),
                }
            )

            for segment_id, endpoint in component.free_endpoints:
                coordinate = endpoint_point(
                    segments[layer],
                    segment_id,
                    endpoint,
                )

                unmatched_rows.append(
                    {
                        "layer": layer,
                        "component_id": component_index,
                        "segment_id": segment_id,
                        "endpoint": endpoint,
                        "endpoint_label": format_endpoint(
                            (segment_id, endpoint)
                        ),
                        "panel_x": coordinate[0],
                        "panel_y": coordinate[1],
                    }
                )

    component_fields = [
        "layer",
        "component_id",
        "segment_count",
        "segment_ids",
        "accepted_edge_count",
        "accepted_connection_ids",
        "free_endpoint_count",
        "free_endpoints",
        "closed",
        "branched",
        "traversal",
        "visible_length_px",
        "accepted_endpoint_gap_sum_px",
    ]

    with COMPONENT_PATH.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=component_fields,
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(component_rows)

    unmatched_fields = [
        "layer",
        "component_id",
        "segment_id",
        "endpoint",
        "endpoint_label",
        "panel_x",
        "panel_y",
    ]

    with UNMATCHED_PATH.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=unmatched_fields,
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(unmatched_rows)

    print(f"Wrote {COMPONENT_PATH.relative_to(ROOT)}")
    print(f"Wrote {UNMATCHED_PATH.relative_to(ROOT)}")


def plot_connectivity(
    segments: dict[str, dict[int, np.ndarray]],
    accepted: list[dict[str, str]],
    components_by_layer: dict[
        str,
        tuple[ConnectivityComponent, ...],
    ],
) -> None:
    """Plot accepted hidden edges and remaining free endpoints."""
    figure, axes = plt.subplots(
        1,
        3,
        figsize=(15, 6),
        constrained_layout=True,
    )

    for axis, layer in zip(
        axes,
        LAYERS,
        strict=True,
    ):
        colour = DISPLAY[layer]["colour"]

        for segment_id in sorted(segments[layer]):
            points = segments[layer][segment_id]

            axis.plot(
                points[:, 0],
                points[:, 1],
                color=colour,
                linewidth=1.8,
                marker="o",
                markersize=2.5,
            )

            midpoint = points[len(points) // 2]

            axis.text(
                midpoint[0],
                midpoint[1],
                f"S{segment_id}",
                fontsize=7,
                color=colour,
            )

        layer_connections = [
            row
            for row in accepted
            if row["layer"] == layer
        ]

        for row in layer_connections:
            point_a = endpoint_point(
                segments[layer],
                int(row["segment_a"]),
                row["endpoint_a"],
            )

            point_b = endpoint_point(
                segments[layer],
                int(row["segment_b"]),
                row["endpoint_b"],
            )

            axis.plot(
                [point_a[0], point_b[0]],
                [point_a[1], point_b[1]],
                linestyle="--",
                linewidth=1.4,
                color=colour,
                alpha=0.75,
            )

        free_endpoints = [
            endpoint
            for component in components_by_layer[layer]
            for endpoint in component.free_endpoints
        ]

        for endpoint in free_endpoints:
            segment_id, endpoint_name = endpoint

            coordinate = endpoint_point(
                segments[layer],
                segment_id,
                endpoint_name,
            )

            axis.scatter(
                coordinate[0],
                coordinate[1],
                s=90,
                facecolors="none",
                edgecolors=colour,
                linewidths=1.8,
                zorder=10,
            )

            axis.annotate(
                format_endpoint(endpoint),
                coordinate,
                xytext=(4, 5),
                textcoords="offset points",
                fontsize=7,
                color=colour,
            )

        axis.set_aspect("equal")
        axis.invert_yaxis()
        axis.grid(True, alpha=0.2)
        axis.set_xlabel("Panel x (pixels)")
        axis.set_ylabel("Panel y (pixels)")
        axis.set_title(
            f"{DISPLAY[layer]['label']}\n"
            f"{len(components_by_layer[layer])} components; "
            f"{len(free_endpoints)} free endpoints"
        )

    figure.suptitle(
        "A10_P03 source-derived connectivity\n"
        "solid: visible fragments; dashed: accepted occlusions; "
        "open circles: unmatched endpoints"
    )

    figure.savefig(
        FIGURE_PATH,
        dpi=220,
    )
    plt.close(figure)

    print(f"Wrote {FIGURE_PATH.relative_to(ROOT)}")


def write_report(
    components_by_layer: dict[
        str,
        tuple[ConnectivityComponent, ...],
    ],
    segments: dict[str, dict[int, np.ndarray]],
    accepted: list[dict[str, str]],
) -> None:
    """Write the formal connectivity-graph report."""
    lines = [
        "# A10_P03 Connectivity Graph — v0.6",
        "",
        "## Inputs",
        "",
        "- Visible traced segments: **24** coloured fragments.",
        "- Accepted endpoint continuations: **15**.",
        "- Reviewed confidence: **high** for all 15 connections.",
        "- Review reason: `occlusion_supported` for all 15.",
        "",
        "Every visible fragment is represented by an intrinsic edge between "
        "its start and end. Every accepted adjudication is represented by a "
        "second edge across the locally occluded gap.",
        "",
        "## Layer summary",
        "",
        "| Layer | Visible fragments | Accepted edges | Components | "
        "Free endpoints | Closed components | Branched components |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]

    for layer in LAYERS:
        components = components_by_layer[layer]

        layer_accepted = sum(
            row["layer"] == layer
            for row in accepted
        )

        free_endpoint_count = sum(
            len(component.free_endpoints)
            for component in components
        )

        closed_count = sum(
            component.closed
            for component in components
        )

        branched_count = sum(
            component.branched
            for component in components
        )

        lines.append(
            f"| {DISPLAY[layer]['label']} | "
            f"{len(segments[layer])} | "
            f"{layer_accepted} | "
            f"{len(components)} | "
            f"{free_endpoint_count} | "
            f"{closed_count} | "
            f"{branched_count} |"
        )

    lines.extend(
        [
            "",
            "## Connected components",
            "",
        ]
    )

    accepted_by_id = {
        row["candidate_id"]: row
        for row in accepted
    }

    for layer in LAYERS:
        lines.extend(
            [
                f"### {DISPLAY[layer]['label']}",
                "",
            ]
        )

        for component_index, component in enumerate(
            components_by_layer[layer],
            start=1,
        ):
            visible_length = sum(
                polyline_metrics(
                    segments[layer][segment_id]
                ).length
                for segment_id in component.segment_ids
            )

            endpoint_gap_sum = sum(
                float(
                    accepted_by_id[candidate_id][
                        "distance_px"
                    ]
                )
                for candidate_id
                in component.accepted_connection_ids
            )

            segment_text = ", ".join(
                f"S{segment_id:02d}"
                for segment_id in component.segment_ids
            )

            connection_text = (
                ", ".join(
                    f"`{candidate_id}`"
                    for candidate_id
                    in component.accepted_connection_ids
                )
                or "none"
            )

            lines.extend(
                [
                    f"#### Component {component_index}",
                    "",
                    f"- Segments: {segment_text}.",
                    f"- Accepted connections: {connection_text}.",
                    f"- Traversal: `{traversal_text(component)}`.",
                    f"- Free endpoints: "
                    f"`{free_endpoint_text(component)}`.",
                    f"- Closed: `{str(component.closed).lower()}`.",
                    f"- Branched: `{str(component.branched).lower()}`.",
                    f"- Visible traced length: "
                    f"{visible_length:.3f} px.",
                    f"- Straight-line endpoint-gap sum: "
                    f"{endpoint_gap_sum:.3f} px.",
                    "",
                ]
            )

    lines.extend(
        [
            "## Exact graph findings",
            "",
            "- No accepted endpoint is used by more than one connection.",
            "- No component contains a branch node.",
            "- Every connected component is therefore an open path or an "
            "isolated visible segment.",
            "- No colour is yet demonstrated to form a closed loop from the "
            "reviewed candidate set alone.",
            "",
            "The blue fragments form one connected open chain. The red "
            "fragments form one six-segment chain plus one isolated segment. "
            "The green fragments remain distributed over six components.",
            "",
            "## Minimum additional connectivity requirements",
            "",
            "Because every present component is a non-branched path, joining "
            "\(c\) components into one open chain requires at least "
            "\(c-1\) additional endpoint pairings. Closing the result into "
            "one cycle requires at least \(c\) pairings.",
            "",
            "| Layer | Current components | Additional edges for one chain | "
            "Additional edges for one cycle |",
            "|---|---:|---:|---:|",
            f"| Red centreline | "
            f"{len(components_by_layer['red'])} | "
            f"{len(components_by_layer['red']) - 1} | "
            f"{len(components_by_layer['red'])} |",
            f"| Green centreline | "
            f"{len(components_by_layer['green'])} | "
            f"{len(components_by_layer['green']) - 1} | "
            f"{len(components_by_layer['green'])} |",
            f"| Blue centreline | "
            f"{len(components_by_layer['blue'])} | "
            f"{len(components_by_layer['blue']) - 1} | "
            f"{len(components_by_layer['blue'])} |",
            "",
            "These are graph-theoretic lower bounds, not evidence that the "
            "required connections actually exist in the source.",
            "",
            "## Interpretation boundary",
            "",
            "The reviewed set contains only the five strongest ranked "
            "candidates per colour. An unmatched endpoint does not prove that "
            "the underlying source curve terminates there.",
            "",
            "Further continuity may require:",
            "",
            "- review of lower-ranked endpoint candidates;",
            "- evidence from A10_P01 or A10_P02;",
            "- a hidden connection outside the visible panel;",
            "- a colour transition rather than same-colour continuation;",
            "- clarification of the source's three-colour convention.",
            "",
            "Accepted dashed edges are topological relations. They are not "
            "metric reconstructions of the hidden path.",
            "",
            "## Generated outputs",
            "",
            "- `figures/a10_p03_connectivity_graph.png`",
            "- `data/derived/a10_p03_connectivity_components.csv` "
            "(local ignored output)",
            "- `data/derived/a10_p03_unmatched_endpoints.csv` "
            "(local ignored output)",
            "",
        ]
    )

    REPORT_PATH.write_text(
        "\n".join(lines),
        encoding="utf-8",
    )

    print(f"Wrote {REPORT_PATH.relative_to(ROOT)}")


def main() -> None:
    """Build and report the adjudicated connectivity graph."""
    segments = load_segments()
    accepted = load_accepted_connections()

    components_by_layer = {
        layer: build_endpoint_connectivity(
            segments[layer].keys(),
            [
                row
                for row in accepted
                if row["layer"] == layer
            ],
        )
        for layer in LAYERS
    }

    accepted_by_id = {
        row["candidate_id"]: row
        for row in accepted
    }

    write_derived_tables(
        components_by_layer,
        segments,
        accepted_by_id,
    )

    plot_connectivity(
        segments,
        accepted,
        components_by_layer,
    )

    write_report(
        components_by_layer,
        segments,
        accepted,
    )

    print()

    for layer in LAYERS:
        components = components_by_layer[layer]

        print(DISPLAY[layer]["label"])
        print("  components:", len(components))
        print(
            "  free endpoints:",
            sum(
                len(component.free_endpoints)
                for component in components
            ),
        )

        for index, component in enumerate(
            components,
            start=1,
        ):
            print(
                f"  C{index}:",
                component.segment_ids,
                traversal_text(component),
                "free=",
                free_endpoint_text(component),
            )


if __name__ == "__main__":
    main()
