#!/usr/bin/env python3
"""Derive and review ordered A10_P03 crossing visits."""

from __future__ import annotations

import csv
import textwrap
from collections import Counter, defaultdict
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

from meru_geometry.crossing_review import (
    validate_crossing_review_rows,
)
from meru_geometry.gauss_visits import (
    CrossingVisit,
    VisitOrderPair,
    build_crossing_visits,
    find_close_visit_pairs,
    find_order_ties,
    provisional_gauss_tokens,
)
from meru_geometry.global_cycle import (
    GlobalCycleAudit,
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

DIGITIZATION_PATH = (
    DATA_DIR
    / "digitization.csv"
)

INVENTORY_PATH = (
    DATA_DIR
    / "crossing_inventory.csv"
)

ORDER_REVIEW_PATH = (
    DATA_DIR
    / "gauss_order_review.csv"
)

SOURCE_PATH = (
    ROOT
    / "data"
    / "derived"
    / "source_inspection"
    / "panels"
    / "A10_P03.png"
)

VISIT_CSV_PATH = (
    ROOT
    / "data"
    / "derived"
    / "a10_p03_gauss_visits.csv"
)

REPORT_PATH = (
    ROOT
    / "docs"
    / "geometry"
    / "a10_p03_gauss_visit_census_v0_7.md"
)

REVIEW_FIGURE_PATH = (
    ROOT
    / "figures"
    / "a10_p03_gauss_order_review.png"
)

LAYERS = (
    "red",
    "green",
    "blue",
)

LAYER_CODE = {
    "red": "R",
    "green": "G",
    "blue": "B",
}

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

REVIEW_FIELDNAMES = [
    "review_id",
    "review_kind",
    "layer",
    "segment_id",
    "traversal_forward",
    "provisional_first",
    "provisional_second",
    "gap_fraction",
    "status",
    "accepted_first",
    "accepted_second",
    "confidence",
    "notes",
    "reviewed_utc",
]

MANUAL_REVIEW_FIELDS = (
    "status",
    "accepted_first",
    "accepted_second",
    "confidence",
    "notes",
    "reviewed_utc",
)


def load_csv(
    path: Path,
) -> list[dict[str, str]]:
    """Load one CSV file."""
    with path.open(
        newline="",
        encoding="utf-8",
    ) as handle:
        return list(csv.DictReader(handle))


def load_segments() -> dict[
    tuple[str, int],
    np.ndarray,
]:
    """Load one-based visible centreline segments."""
    raw: dict[
        tuple[str, int],
        list[tuple[int, float, float]],
    ] = defaultdict(list)

    for row in load_csv(
        DIGITIZATION_PATH
    ):
        layer = row["layer"]

        if layer not in LAYERS:
            continue

        key = (
            layer,
            int(row["segment_id"]) + 1,
        )

        raw[key].append(
            (
                int(row["point_index"]),
                float(row["panel_x"]),
                float(row["panel_y"]),
            )
        )

    result = {}

    for key, records in raw.items():
        records.sort(
            key=lambda record: record[0]
        )

        result[key] = np.asarray(
            [
                [record[1], record[2]]
                for record in records
            ],
            dtype=np.float64,
        )

    return result


def load_accepted(
    filename: str,
) -> list[dict[str, str]]:
    """Load accepted endpoint decisions."""
    return [
        row
        for row in load_csv(
            DATA_DIR / filename
        )
        if row["status"] == "accepted"
    ]


def build_global_audit(
    segments: dict[
        tuple[str, int],
        np.ndarray,
    ],
) -> GlobalCycleAudit:
    """Rebuild and validate the frozen v0.6 cycle."""
    segment_ids = {
        layer: sorted(
            segment_id
            for (
                segment_layer,
                segment_id,
            ) in segments
            if segment_layer == layer
        )
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

    traversal = tuple(
        format_segment_visit(visit)
        for visit in audit.segment_traversal
    )

    if not audit.is_single_cycle:
        raise RuntimeError(
            "The frozen global cycle no longer validates."
        )

    if traversal != EXPECTED_TRAVERSAL:
        raise RuntimeError(
            "The global traversal differs from the frozen "
            "v0.6 canonical traversal."
        )

    return audit


def tie_group_map(
    ties: tuple[
        tuple[CrossingVisit, ...],
        ...,
    ],
) -> dict[CrossingVisit, str]:
    """Assign stable identifiers to exact positional ties."""
    result: dict[
        CrossingVisit,
        str,
    ] = {}

    for index, group in enumerate(
        ties,
        start=1,
    ):
        identifier = f"T{index:02d}"

        for visit in group:
            result[visit] = identifier

    return result


def write_visit_csv(
    visits: tuple[CrossingVisit, ...],
    ties: tuple[
        tuple[CrossingVisit, ...],
        ...,
    ],
) -> None:
    """Write the derived 62-visit table."""
    VISIT_CSV_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    tie_ids = tie_group_map(ties)

    fieldnames = [
        "provisional_order",
        "event_id",
        "role",
        "token",
        "candidate_id",
        "segment_order",
        "layer",
        "segment_id",
        "traversal_forward",
        "source_fraction",
        "traversal_fraction",
        "global_position",
        "panel_x",
        "panel_y",
        "order_status",
        "tie_group_id",
    ]

    with VISIT_CSV_PATH.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=fieldnames,
            lineterminator="\n",
        )

        writer.writeheader()

        for index, visit in enumerate(
            visits,
            start=1,
        ):
            writer.writerow(
                {
                    "provisional_order": index,
                    "event_id": visit.event_id,
                    "role": visit.role,
                    "token": visit.token,
                    "candidate_id": (
                        visit.candidate_id
                    ),
                    "segment_order": (
                        visit.segment_order + 1
                    ),
                    "layer": visit.layer,
                    "segment_id": (
                        visit.segment_id
                    ),
                    "traversal_forward": (
                        visit.traversal_forward
                    ),
                    "source_fraction": (
                        visit.source_fraction
                    ),
                    "traversal_fraction": (
                        visit.traversal_fraction
                    ),
                    "global_position": (
                        visit.global_position
                    ),
                    "panel_x": visit.panel_x,
                    "panel_y": visit.panel_y,
                    "order_status": (
                        "tied"
                        if visit in tie_ids
                        else "unique"
                    ),
                    "tie_group_id": tie_ids.get(
                        visit,
                        "",
                    ),
                }
            )

    print(
        f"Wrote {VISIT_CSV_PATH.relative_to(ROOT)}"
    )


def review_identifier(
    pair: VisitOrderPair,
) -> str:
    """Return a stable review-row identifier."""
    return (
        "ORDER_"
        f"{LAYER_CODE[pair.first.layer]}_"
        f"S{pair.first.segment_id:02d}_"
        f"{pair.first.token}_"
        f"{pair.second.token}"
    )


def write_order_review(
    pairs: tuple[VisitOrderPair, ...],
) -> None:
    """Create or refresh the tracked ordering-review table."""
    existing = {}

    if ORDER_REVIEW_PATH.exists():
        existing = {
            row["review_id"]: row
            for row in load_csv(
                ORDER_REVIEW_PATH
            )
        }

    rows = []

    for pair in pairs:
        identifier = review_identifier(
            pair
        )

        row: dict[str, object] = {
            "review_id": identifier,
            "review_kind": (
                "exact_tie"
                if pair.gap_fraction
                <= 1.0e-12
                else "close_order"
            ),
            "layer": pair.first.layer,
            "segment_id": (
                pair.first.segment_id
            ),
            "traversal_forward": (
                pair.first.traversal_forward
            ),
            "provisional_first": (
                pair.first.token
            ),
            "provisional_second": (
                pair.second.token
            ),
            "gap_fraction": (
                pair.gap_fraction
            ),
            "status": "unreviewed",
            "accepted_first": "",
            "accepted_second": "",
            "confidence": "",
            "notes": "",
            "reviewed_utc": "",
        }

        previous = existing.get(
            identifier
        )

        if previous is not None:
            for field in MANUAL_REVIEW_FIELDS:
                row[field] = previous.get(
                    field,
                    row[field],
                )

        rows.append(row)

    with ORDER_REVIEW_PATH.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=REVIEW_FIELDNAMES,
            lineterminator="\n",
        )

        writer.writeheader()
        writer.writerows(rows)

    print(
        f"Wrote {ORDER_REVIEW_PATH.relative_to(ROOT)}"
    )


def local_direction_arrow(
    points: np.ndarray,
    forward: bool,
    location: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    """Return one short arrow following traversal direction."""
    oriented = (
        points
        if forward
        else points[::-1]
    )

    nearest = int(
        np.argmin(
            np.linalg.norm(
                oriented - location,
                axis=1,
            )
        )
    )

    if nearest < len(oriented) - 1:
        return (
            oriented[nearest],
            oriented[nearest + 1],
        )

    return (
        oriented[nearest - 1],
        oriented[nearest],
    )


def plot_order_review(
    pairs: tuple[VisitOrderPair, ...],
    segments: dict[
        tuple[str, int],
        np.ndarray,
    ],
) -> None:
    """Plot the exact and close ordering cases."""
    with Image.open(SOURCE_PATH) as source:
        source_image = np.asarray(
            source.convert("RGB")
        )

    figure, axes = plt.subplots(
        2,
        2,
        figsize=(12, 11),
        constrained_layout=True,
    )

    for axis, pair in zip(
        axes.flat,
        pairs,
        strict=True,
    ):
        key = pair.first.segment_key
        points = segments[key]

        locations = np.asarray(
            [
                [
                    pair.first.panel_x,
                    pair.first.panel_y,
                ],
                [
                    pair.second.panel_x,
                    pair.second.panel_y,
                ],
            ],
            dtype=np.float64,
        )

        centre = locations.mean(axis=0)

        margin = 19.0

        axis.imshow(source_image)

        axis.plot(
            points[:, 0],
            points[:, 1],
            color=COLOURS[key[0]],
            linewidth=2.7,
            marker="o",
            markersize=2.5,
            alpha=0.9,
        )

        axis.scatter(
            locations[:, 0],
            locations[:, 1],
            s=[100, 100],
            marker="o",
            facecolors="white",
            edgecolors="black",
            linewidths=1.3,
            zorder=10,
        )

        axis.annotate(
            pair.first.token,
            locations[0],
            xytext=(6, 7),
            textcoords="offset points",
            fontsize=9,
            fontweight="bold",
        )

        axis.annotate(
            pair.second.token,
            locations[1],
            xytext=(6, -14),
            textcoords="offset points",
            fontsize=9,
            fontweight="bold",
        )

        arrow_start, arrow_end = (
            local_direction_arrow(
                points,
                pair.first.traversal_forward,
                centre,
            )
        )

        axis.annotate(
            "",
            xy=arrow_end,
            xytext=arrow_start,
            arrowprops={
                "arrowstyle": "->",
                "linewidth": 2.0,
                "color": "black",
            },
            zorder=12,
        )

        axis.set_xlim(
            float(locations[:, 0].min())
            - margin,
            float(locations[:, 0].max())
            + margin,
        )

        axis.set_ylim(
            float(locations[:, 1].max())
            + margin,
            float(locations[:, 1].min())
            - margin,
        )

        review_kind = (
            "EXACT TIE — order unresolved"
            if pair.gap_fraction
            <= 1.0e-12
            else "close derived order"
        )

        axis.set_title(
            f"{review_identifier(pair)}\n"
            f"{review_kind}; "
            f"gap={pair.gap_fraction:.6f}"
        )

        axis.set_aspect("equal")
        axis.set_xticks([])
        axis.set_yticks([])

    figure.suptitle(
        "A10_P03 Gauss-visit ordering review\n"
        "arrows show frozen global-cycle direction"
    )

    figure.savefig(
        REVIEW_FIGURE_PATH,
        dpi=220,
    )

    plt.close(figure)

    print(
        f"Wrote {REVIEW_FIGURE_PATH.relative_to(ROOT)}"
    )


def wrapped_sequence(
    tokens: tuple[str, ...],
) -> str:
    """Return a readable wrapped token sequence."""
    return "\n".join(
        textwrap.wrap(
            " ".join(tokens),
            width=100,
        )
    )


def write_report(
    audit: GlobalCycleAudit,
    visits: tuple[CrossingVisit, ...],
    ties: tuple[
        tuple[CrossingVisit, ...],
        ...,
    ],
    close_pairs: tuple[
        VisitOrderPair,
        ...,
    ],
) -> None:
    """Write the permanent visit-census report."""
    tokens = provisional_gauss_tokens(
        visits
    )

    role_counts = Counter(
        visit.role
        for visit in visits
    )

    lines = [
        "# A10_P03 Gauss-Visit Census — v0.7",
        "",
        "## Purpose",
        "",
        "Map both visits to every reviewed crossing onto the frozen "
        "v0.6 global-cycle traversal.",
        "",
        "## Invariants",
        "",
        f"- Crossing events: **{len(visits) // 2}**",
        f"- Total visits: **{len(visits)}**",
        f"- Over visits: **{role_counts.get('O', 0)}**",
        f"- Under visits: **{role_counts.get('U', 0)}**",
        f"- Frozen visible segments: "
        f"**{audit.visible_segment_count}**",
        f"- Exact unresolved positional ties: **{len(ties)}**",
        f"- Close consecutive visit pairs reviewed: "
        f"**{len(close_pairs)}**",
        "",
        "Every crossing event appears exactly twice: once as an "
        "over visit and once as an under visit.",
        "",
        "## Ordering method",
        "",
        "Each candidate-side location is converted from its polyline "
        "piece index and piece fraction into normalized polyline arc "
        "length.",
        "",
        "For reversed segments the local fraction is transformed by",
        "",
        r"\[",
        r"s_{\mathrm{traversal}}=1-s_{\mathrm{source}}.",
        r"\]",
        "",
        "Visits are then ordered first by frozen segment order and "
        "then by traversal-oriented arc fraction.",
        "",
        "## Frozen traversal",
        "",
        "```text",
        " → ".join(
            format_segment_visit(visit)
            for visit in audit.segment_traversal
        ),
        "```",
        "",
        "## Provisional O/U Gauss sequence",
        "",
        "```text",
        wrapped_sequence(tokens),
        "```",
        "",
        "Braces denote visits whose current digitized positions are "
        "exactly tied. Their order has deliberately not been inferred.",
        "",
        "## Exact unresolved ties",
        "",
        "| Tie | Segment | Visits | Fraction |",
        "|---|---|---|---:|",
    ]

    for index, group in enumerate(
        ties,
        start=1,
    ):
        first = group[0]

        lines.append(
            f"| `T{index:02d}` | "
            f"`{LAYER_CODE[first.layer]}:S"
            f"{first.segment_id:02d}` | "
            f"`{' / '.join(visit.token for visit in group)}` | "
            f"{first.traversal_fraction:.9f} |"
        )

    lines.extend(
        [
            "",
            "## Close-order review set",
            "",
            "| Review | Kind | Segment | Derived display order | "
            "Fractional gap |",
            "|---|---|---|---|---:|",
        ]
    )

    for pair in close_pairs:
        kind = (
            "exact tie"
            if pair.gap_fraction <= 1.0e-12
            else "close"
        )

        lines.append(
            f"| `{review_identifier(pair)}` | "
            f"{kind} | "
            f"`{LAYER_CODE[pair.first.layer]}:S"
            f"{pair.first.segment_id:02d}` | "
            f"`{pair.first.token} → {pair.second.token}` | "
            f"{pair.gap_fraction:.9f} |"
        )

    lines.extend(
        [
            "",
            "For the exact tie, the displayed order is merely "
            "deterministic table order and is not yet an accepted "
            "geometric order.",
            "",
            "## Interpretation boundary",
            "",
            "This census establishes 62 source-linked O/U visits and "
            "their segment-level placement.",
            "",
            "It does not yet establish:",
            "",
            "- a unique canonical Gauss word;",
            "- crossing signs;",
            "- a Dowker–Thistlethwaite code;",
            "- a knot polynomial;",
            "- equivalence with the canonical `(3,10)` torus knot.",
            "",
            "The exact tie must be resolved and the three close "
            "orders visually confirmed before the unique Gauss word "
            "is frozen.",
            "",
            "## Generated outputs",
            "",
            "- `data/derived/a10_p03_gauss_visits.csv` "
            "(local derived table)",
            "- `data/manual_digitizations/A10_P03/"
            "gauss_order_review.csv`",
            "- `figures/a10_p03_gauss_order_review.png`",
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
    """Run the complete A10_P03 crossing-visit census."""
    segments = load_segments()

    inventory = load_csv(
        INVENTORY_PATH
    )

    validate_crossing_review_rows(
        inventory
    )

    audit = build_global_audit(
        segments
    )

    visits = build_crossing_visits(
        inventory,
        segments,
        audit.segment_traversal,
    )

    ties = find_order_ties(
        visits
    )

    close_pairs = find_close_visit_pairs(
        visits,
        maximum_gap=0.03,
    )

    if len(visits) != 62:
        raise RuntimeError(
            f"Expected 62 visits; found {len(visits)}."
        )

    if len(ties) != 1:
        raise RuntimeError(
            f"Expected one exact order tie; found {len(ties)}."
        )

    if len(close_pairs) != 4:
        raise RuntimeError(
            "Expected four exact-or-close ordering pairs; "
            f"found {len(close_pairs)}."
        )

    write_visit_csv(
        visits,
        ties,
    )

    write_order_review(
        close_pairs
    )

    plot_order_review(
        close_pairs,
        segments,
    )

    write_report(
        audit,
        visits,
        ties,
        close_pairs,
    )

    roles = Counter(
        visit.role
        for visit in visits
    )

    print()
    print("A10_P03 Gauss-visit census")
    print("==========================")
    print("Crossing events:", len(visits) // 2)
    print("Total visits:   ", len(visits))
    print("Over visits:    ", roles.get("O", 0))
    print("Under visits:   ", roles.get("U", 0))
    print("Exact ties:     ", len(ties))
    print("Close pairs:    ", len(close_pairs))
    print()
    print("Provisional sequence:")
    print(
        wrapped_sequence(
            provisional_gauss_tokens(
                visits
            )
        )
    )
    print()
    print(
        "UNRESOLVED: a unique Gauss word must wait for "
        "the ordering review."
    )


if __name__ == "__main__":
    main()
