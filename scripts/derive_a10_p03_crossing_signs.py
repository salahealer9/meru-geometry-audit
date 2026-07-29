#!/usr/bin/env python3
"""Derive the oriented A10_P03 crossing-sign census."""

from __future__ import annotations

import csv
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
from meru_geometry.crossing_signs import (
    CrossingSign,
    crossing_sign_stability,
    derive_crossing_signs,
    sign_counts,
    writhe,
)
from meru_geometry.global_cycle import (
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

GAUSS_WORD_PATH = (
    DATA_DIR
    / "gauss_word.csv"
)

REVIEW_PATH = (
    DATA_DIR
    / "crossing_sign_review.csv"
)

SOURCE_PATH = (
    ROOT
    / "data"
    / "derived"
    / "source_inspection"
    / "panels"
    / "A10_P03.png"
)

DERIVED_PATH = (
    ROOT
    / "data"
    / "derived"
    / "a10_p03_crossing_signs.csv"
)

FIGURE_PATH = (
    ROOT
    / "figures"
    / "a10_p03_crossing_sign_census.png"
)

REVIEW_FIGURE_PATH = (
    ROOT
    / "figures"
    / "a10_p03_crossing_sign_review.png"
)

REPORT_PATH = (
    ROOT
    / "docs"
    / "geometry"
    / "a10_p03_crossing_sign_census_v0_7.md"
)

PRIMARY_SPAN_PX = 6.0

SENSITIVITY_SPANS_PX = (
    2.0,
    4.0,
    6.0,
    8.0,
    10.0,
    12.0,
)

LOW_ANGLE_THRESHOLD_DEGREES = 25.0

LAYER_COLOURS = {
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

REVIEW_FIELDS = [
    "event_id",
    "candidate_id",
    "over_layer",
    "over_segment",
    "under_layer",
    "under_segment",
    "derived_sign",
    "primary_angle_deg",
    "minimum_angle_deg",
    "stable_across_spans",
    "status",
    "accepted_sign",
    "confidence",
    "notes",
    "reviewed_utc",
]

MANUAL_REVIEW_FIELDS = (
    "status",
    "accepted_sign",
    "confidence",
    "notes",
    "reviewed_utc",
)


def load_csv(
    path: Path,
) -> list[dict[str, str]]:
    """Load one CSV table."""
    with path.open(
        newline="",
        encoding="utf-8",
    ) as handle:
        return list(
            csv.DictReader(handle)
        )


def load_segments() -> dict[
    tuple[str, int],
    np.ndarray,
]:
    """Load one-based coloured centreline fragments."""
    raw: dict[
        tuple[str, int],
        list[tuple[int, float, float]],
    ] = defaultdict(list)

    for row in load_csv(
        DIGITIZATION_PATH
    ):
        layer = row["layer"]

        if layer not in LAYER_COLOURS:
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

    segments = {}

    for key, records in raw.items():
        records.sort(
            key=lambda record: record[0]
        )

        segments[key] = np.asarray(
            [
                [record[1], record[2]]
                for record in records
            ],
            dtype=np.float64,
        )

    return segments


def load_traversal_directions(
    segments: dict[
        tuple[str, int],
        np.ndarray,
    ],
) -> dict[
    tuple[str, int],
    bool,
]:
    """Rebuild all directions from the frozen v0.6 global cycle."""
    segment_ids = {
        layer: sorted(
            segment_id
            for (
                segment_layer,
                segment_id,
            ) in segments
            if segment_layer == layer
        )
        for layer in LAYER_COLOURS
    }

    def accepted_rows(
        filename: str,
    ) -> list[dict[str, str]]:
        return [
            row
            for row in load_csv(
                DATA_DIR / filename
            )
            if row["status"] == "accepted"
        ]

    same_colour = (
        accepted_rows(
            "endpoint_adjudication.csv"
        )
        + accepted_rows(
            "residual_endpoint_review.csv"
        )
    )

    cross_colour = accepted_rows(
        "cross_colour_endpoint_review.csv"
    )

    audit = audit_global_cycle(
        segment_ids,
        same_colour,
        cross_colour,
    )

    if not audit.is_single_cycle:
        raise RuntimeError(
            "The frozen v0.6 global cycle no longer validates."
        )

    formatted = tuple(
        format_segment_visit(visit)
        for visit in audit.segment_traversal
    )

    if formatted != EXPECTED_TRAVERSAL:
        raise RuntimeError(
            "The reconstructed traversal differs from the "
            "frozen v0.6 traversal."
        )

    result = {
        (
            visit.layer,
            visit.segment_id,
        ): visit.forward
        for visit in audit.segment_traversal
    }

    if len(result) != 24:
        raise RuntimeError(
            "Expected 24 traversal directions from the frozen "
            f"global cycle; found {len(result)}."
        )

    if set(result) != set(segments):
        missing = sorted(
            set(segments) - set(result)
        )

        unexpected = sorted(
            set(result) - set(segments)
        )

        raise RuntimeError(
            "Traversal and digitization segment sets differ. "
            f"Missing: {missing}; unexpected: {unexpected}."
        )

    return result


def sign_symbol(
    sign: int,
) -> str:
    """Return a readable sign symbol."""
    if sign > 0:
        return "+"

    if sign < 0:
        return "−"

    return "0"


def minimum_angles(
    inventory: list[dict[str, str]],
    segments: dict[
        tuple[str, int],
        np.ndarray,
    ],
    directions: dict[
        tuple[str, int],
        bool,
    ],
) -> dict[str, float]:
    """Return the minimum tangent angle over all sensitivity spans."""
    result: dict[
        str,
        float,
    ] = {}

    for span in SENSITIVITY_SPANS_PX:
        signs = derive_crossing_signs(
            inventory,
            segments,
            directions,
            span_px=span,
        )

        for sign in signs:
            current = result.get(
                sign.event_id,
                float("inf"),
            )

            result[sign.event_id] = min(
                current,
                sign.crossing_angle_degrees,
            )

    return result


def write_derived_csv(
    signs: tuple[CrossingSign, ...],
    stability: dict[
        str,
        tuple[int, ...],
    ],
    minimum: dict[str, float],
) -> None:
    """Write the local derived sign census."""
    DERIVED_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    fieldnames = [
        "event_id",
        "candidate_id",
        "sign",
        "sign_symbol",
        "determinant",
        "primary_angle_deg",
        "minimum_angle_deg",
        "stable_across_spans",
        "over_layer",
        "over_segment",
        "under_layer",
        "under_segment",
        "over_tangent_x",
        "over_tangent_y",
        "under_tangent_x",
        "under_tangent_y",
        "primary_span_px",
    ]

    with DERIVED_PATH.open(
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

        for sign in signs:
            event_stability = stability[
                sign.event_id
            ]

            writer.writerow(
                {
                    "event_id": sign.event_id,
                    "candidate_id": (
                        sign.candidate_id
                    ),
                    "sign": sign.sign,
                    "sign_symbol": (
                        sign_symbol(sign.sign)
                    ),
                    "determinant": (
                        sign.determinant
                    ),
                    "primary_angle_deg": (
                        sign.crossing_angle_degrees
                    ),
                    "minimum_angle_deg": (
                        minimum[sign.event_id]
                    ),
                    "stable_across_spans": (
                        len(set(event_stability))
                        == 1
                    ),
                    "over_layer": (
                        sign.over_key[0]
                    ),
                    "over_segment": (
                        sign.over_key[1]
                    ),
                    "under_layer": (
                        sign.under_key[0]
                    ),
                    "under_segment": (
                        sign.under_key[1]
                    ),
                    "over_tangent_x": (
                        sign.over_tangent[0]
                    ),
                    "over_tangent_y": (
                        sign.over_tangent[1]
                    ),
                    "under_tangent_x": (
                        sign.under_tangent[0]
                    ),
                    "under_tangent_y": (
                        sign.under_tangent[1]
                    ),
                    "primary_span_px": (
                        sign.tangent_span_px
                    ),
                }
            )

    print(
        f"Wrote {DERIVED_PATH.relative_to(ROOT)}"
    )


def write_review_table(
    signs: tuple[CrossingSign, ...],
    stability: dict[
        str,
        tuple[int, ...],
    ],
    minimum: dict[str, float],
) -> list[dict[str, object]]:
    """Create or refresh the low-angle manual review table."""
    existing = {}

    if REVIEW_PATH.exists():
        existing = {
            row["event_id"]: row
            for row in load_csv(
                REVIEW_PATH
            )
        }

    review_signs = [
        sign
        for sign in signs
        if minimum[sign.event_id]
        < LOW_ANGLE_THRESHOLD_DEGREES
    ]

    rows: list[
        dict[str, object]
    ] = []

    for sign in review_signs:
        row: dict[str, object] = {
            "event_id": sign.event_id,
            "candidate_id": (
                sign.candidate_id
            ),
            "over_layer": (
                sign.over_key[0]
            ),
            "over_segment": (
                sign.over_key[1]
            ),
            "under_layer": (
                sign.under_key[0]
            ),
            "under_segment": (
                sign.under_key[1]
            ),
            "derived_sign": (
                sign.sign
            ),
            "primary_angle_deg": (
                sign.crossing_angle_degrees
            ),
            "minimum_angle_deg": (
                minimum[sign.event_id]
            ),
            "stable_across_spans": (
                len(
                    set(
                        stability[sign.event_id]
                    )
                )
                == 1
            ),
            "status": "unreviewed",
            "accepted_sign": "",
            "confidence": "",
            "notes": "",
            "reviewed_utc": "",
        }

        previous = existing.get(
            sign.event_id
        )

        if previous is not None:
            for field in MANUAL_REVIEW_FIELDS:
                row[field] = previous.get(
                    field,
                    row[field],
                )

        rows.append(row)

    rows.sort(
        key=lambda row: int(
            str(row["event_id"])[1:]
        )
    )

    with REVIEW_PATH.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=REVIEW_FIELDS,
            lineterminator="\n",
        )

        writer.writeheader()
        writer.writerows(rows)

    print(
        f"Wrote {REVIEW_PATH.relative_to(ROOT)}"
    )

    return rows


def plot_census(
    signs: tuple[CrossingSign, ...],
) -> None:
    """Plot all signed crossings over the source panel."""
    with Image.open(
        SOURCE_PATH
    ) as source:
        source_image = np.asarray(
            source.convert("RGB")
        )

    inventory = {
        row["event_id"]: row
        for row in load_csv(
            INVENTORY_PATH
        )
        if row["status"] == "crossing"
    }

    figure, axis = plt.subplots(
        figsize=(11, 9),
        constrained_layout=True,
    )

    axis.imshow(
        source_image
    )

    for sign in signs:
        row = inventory[
            sign.event_id
        ]

        x = float(
            row["panel_x"]
        )

        y = float(
            row["panel_y"]
        )

        axis.scatter(
            x,
            y,
            s=58,
            facecolors="white",
            edgecolors="black",
            linewidths=1.0,
            zorder=10,
        )

        axis.annotate(
            f"{sign.event_id}{sign_symbol(sign.sign)}",
            (x, y),
            xytext=(4, 4),
            textcoords="offset points",
            fontsize=7,
            fontweight="bold",
            color="black",
            zorder=11,
        )

    axis.set_aspect("equal")
    axis.set_xlim(0, 190)
    axis.set_ylim(165, 0)
    axis.set_xticks([])
    axis.set_yticks([])

    axis.set_title(
        "A10_P03 oriented crossing-sign census\n"
        "ε = sign det(t_over, t_under); "
        "Cartesian y points upward"
    )

    figure.savefig(
        FIGURE_PATH,
        dpi=220,
    )

    plt.close(figure)

    print(
        f"Wrote {FIGURE_PATH.relative_to(ROOT)}"
    )


def plot_review(
    signs: tuple[CrossingSign, ...],
    minimum: dict[str, float],
) -> None:
    """Plot the four lowest-angle sign cases."""
    with Image.open(
        SOURCE_PATH
    ) as source:
        source_image = np.asarray(
            source.convert("RGB")
        )

    inventory = {
        row["event_id"]: row
        for row in load_csv(
            INVENTORY_PATH
        )
        if row["status"] == "crossing"
    }

    review_signs = sorted(
        (
            sign
            for sign in signs
            if minimum[sign.event_id]
            < LOW_ANGLE_THRESHOLD_DEGREES
        ),
        key=lambda sign: minimum[
            sign.event_id
        ],
    )

    if len(review_signs) != 4:
        raise RuntimeError(
            "Expected four low-angle sign-review events; "
            f"found {len(review_signs)}."
        )

    figure, axes = plt.subplots(
        2,
        2,
        figsize=(12, 11),
        constrained_layout=True,
    )

    for axis, sign in zip(
        axes.flat,
        review_signs,
        strict=True,
    ):
        row = inventory[
            sign.event_id
        ]

        x = float(
            row["panel_x"]
        )

        y = float(
            row["panel_y"]
        )

        axis.imshow(
            source_image
        )

        arrow_length = 13.0

        # Convert Cartesian tangent y back to image y-down.
        over_dx = (
            arrow_length
            * sign.over_tangent[0]
        )

        over_dy = (
            -arrow_length
            * sign.over_tangent[1]
        )

        under_dx = (
            arrow_length
            * sign.under_tangent[0]
        )

        under_dy = (
            -arrow_length
            * sign.under_tangent[1]
        )

        axis.annotate(
            "",
            xy=(
                x + over_dx,
                y + over_dy,
            ),
            xytext=(
                x - over_dx,
                y - over_dy,
            ),
            arrowprops={
                "arrowstyle": "->",
                "linewidth": 2.8,
                "color": LAYER_COLOURS[
                    sign.over_key[0]
                ],
            },
            zorder=12,
        )

        axis.annotate(
            "",
            xy=(
                x + under_dx,
                y + under_dy,
            ),
            xytext=(
                x - under_dx,
                y - under_dy,
            ),
            arrowprops={
                "arrowstyle": "->",
                "linewidth": 2.0,
                "linestyle": "--",
                "color": LAYER_COLOURS[
                    sign.under_key[0]
                ],
            },
            zorder=11,
        )

        margin = 25.0

        axis.set_xlim(
            x - margin,
            x + margin,
        )

        axis.set_ylim(
            y + margin,
            y - margin,
        )

        axis.set_aspect("equal")
        axis.set_xticks([])
        axis.set_yticks([])

        axis.set_title(
            f"{sign.event_id}: "
            f"derived sign {sign_symbol(sign.sign)}\n"
            f"over={sign.over_key[0]} "
            f"S{sign.over_key[1]:02d}; "
            f"under={sign.under_key[0]} "
            f"S{sign.under_key[1]:02d}; "
            f"min angle={minimum[sign.event_id]:.2f}°"
        )

    figure.suptitle(
        "A10_P03 low-angle crossing-sign review\n"
        "solid arrow: over-strand; "
        "dashed arrow: under-strand"
    )

    figure.savefig(
        REVIEW_FIGURE_PATH,
        dpi=220,
    )

    plt.close(figure)

    print(
        f"Wrote {REVIEW_FIGURE_PATH.relative_to(ROOT)}"
    )


def write_report(
    signs: tuple[CrossingSign, ...],
    stability: dict[
        str,
        tuple[int, ...],
    ],
    minimum: dict[str, float],
    review_rows: list[
        dict[str, object]
    ],
) -> None:
    """Write the permanent sign-census report."""
    counts = sign_counts(
        signs
    )

    stable_count = sum(
        len(set(values)) == 1
        for values in stability.values()
    )

    lines = [
        "# A10_P03 Oriented Crossing-Sign Census — v0.7",
        "",
        "## Purpose",
        "",
        "Assign an oriented sign to every source-reviewed crossing "
        "using the frozen global-cycle direction and reviewed "
        "over-under order.",
        "",
        "## Coordinate and sign convention",
        "",
        "The source image uses coordinates with positive `y` downward. "
        "Tangents are converted to a right-handed Cartesian image plane:",
        "",
        r"\[",
        r"(x,y)=(x_{\mathrm{image}},-y_{\mathrm{image}}).",
        r"\]",
        "",
        "With `+z` pointing toward the viewer, the crossing sign is",
        "",
        r"\[",
        r"\varepsilon="
        r"\operatorname{sign}\det"
        r"(\mathbf t_{\mathrm{over}},"
        r"\mathbf t_{\mathrm{under}}).",
        r"\]",
        "",
        "Under this convention, reversing the orientation of the entire "
        "cycle preserves every crossing sign. Mirroring the diagram "
        "reverses every sign.",
        "",
        "## Tangent estimation",
        "",
        f"- Primary secant span: **{PRIMARY_SPAN_PX:.1f} px**",
        "- Sensitivity spans: "
        + ", ".join(
            f"`{span:.0f} px`"
            for span in SENSITIVITY_SPANS_PX
        ),
        "- Endpoint tangents are estimated one-sidedly.",
        "- Every tangent is oriented along the frozen cycle traversal.",
        "",
        "## Census result",
        "",
        f"- Crossing events: **{len(signs)}**",
        f"- Positive crossings: **{counts.get(1, 0)}**",
        f"- Negative crossings: **{counts.get(-1, 0)}**",
        f"- Degenerate signs: **{counts.get(0, 0)}**",
        f"- Writhe: **{writhe(signs)}**",
        f"- Stable signs across all spans: "
        f"**{stable_count}/{len(signs)}**",
        "",
        "## Event signs",
        "",
        "| Event | Sign | Over-strand | Under-strand | "
        "Primary angle | Minimum angle | Stable |",
        "|---|---:|---|---|---:|---:|---|",
    ]

    for sign in signs:
        event_stability = stability[
            sign.event_id
        ]

        lines.append(
            f"| `{sign.event_id}` | "
            f"`{sign_symbol(sign.sign)}` | "
            f"{sign.over_key[0].capitalize()} "
            f"S{sign.over_key[1]:02d} | "
            f"{sign.under_key[0].capitalize()} "
            f"S{sign.under_key[1]:02d} | "
            f"{sign.crossing_angle_degrees:.3f}° | "
            f"{minimum[sign.event_id]:.3f}° | "
            f"{'yes' if len(set(event_stability)) == 1 else 'no'} |"
        )

    lines.extend(
        [
            "",
            "## Low-angle review set",
            "",
            f"Events whose minimum sensitivity angle is below "
            f"`{LOW_ANGLE_THRESHOLD_DEGREES:.1f}°` are placed into "
            "manual review.",
            "",
            "| Event | Derived sign | Minimum angle |",
            "|---|---:|---:|",
        ]
    )

    for row in review_rows:
        lines.append(
            f"| `{row['event_id']}` | "
            f"`{sign_symbol(int(row['derived_sign']))}` | "
            f"{float(row['minimum_angle_deg']):.3f}° |"
        )

    lines.extend(
        [
            "",
            "## Interpretation boundary",
            "",
            "The unanimous sign result is a strong structural property "
            "of this reviewed planar projection under the documented "
            "convention.",
            "",
            "It does not by itself establish:",
            "",
            "- the canonical knot type;",
            "- equivalence with the `(3,10)` torus knot;",
            "- minimal crossing number;",
            "- a unique three-dimensional embedding.",
            "",
            "The four lowest-angle events must be visually reviewed "
            "before the signed Gauss word is frozen.",
            "",
            "## Generated outputs",
            "",
            "- `data/derived/a10_p03_crossing_signs.csv` "
            "(local derived table)",
            "- `data/manual_digitizations/A10_P03/"
            "crossing_sign_review.csv`",
            "- `figures/a10_p03_crossing_sign_census.png`",
            "- `figures/a10_p03_crossing_sign_review.png`",
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
    """Run the complete A10_P03 crossing-sign census."""
    inventory = load_csv(
        INVENTORY_PATH
    )

    validate_crossing_review_rows(
        inventory
    )

    segments = load_segments()

    directions = (
        load_traversal_directions(
            segments
        )
    )

    signs = derive_crossing_signs(
        inventory,
        segments,
        directions,
        span_px=PRIMARY_SPAN_PX,
    )

    if len(signs) != 31:
        raise RuntimeError(
            f"Expected 31 crossing signs; found {len(signs)}."
        )

    stability = crossing_sign_stability(
        inventory,
        segments,
        directions,
        spans_px=SENSITIVITY_SPANS_PX,
    )

    minimum = minimum_angles(
        inventory,
        segments,
        directions,
    )

    write_derived_csv(
        signs,
        stability,
        minimum,
    )

    review_rows = write_review_table(
        signs,
        stability,
        minimum,
    )

    plot_census(
        signs
    )

    plot_review(
        signs,
        minimum,
    )

    write_report(
        signs,
        stability,
        minimum,
        review_rows,
    )

    counts = sign_counts(
        signs
    )

    stable_count = sum(
        len(set(values)) == 1
        for values in stability.values()
    )

    print()
    print("A10_P03 crossing-sign census")
    print("============================")
    print("Crossings:       ", len(signs))
    print("Positive:        ", counts.get(1, 0))
    print("Negative:        ", counts.get(-1, 0))
    print("Degenerate:      ", counts.get(0, 0))
    print("Writhe:          ", writhe(signs))
    print(
        "Stable over spans:",
        f"{stable_count}/{len(signs)}",
    )
    print(
        "Review events:   ",
        " ".join(
            str(row["event_id"])
            for row in review_rows
        ),
    )


if __name__ == "__main__":
    main()
