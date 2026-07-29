#!/usr/bin/env python3
"""Enumerate A10_P03 cross-colour matchings and score Gauss parity."""

from __future__ import annotations

import csv
from pathlib import Path

import numpy as np

from meru_geometry.endpoint_matching_search import (
    apply_exact_tie_reviews,
    enumerate_endpoint_perfect_matchings,
)
from meru_geometry.gauss_parity import (
    audit_gauss_parity,
)
from meru_geometry.gauss_visits import (
    build_crossing_visits,
    validate_complete_gauss_visits,
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

ENDPOINT_PATH = (
    DATA_DIR
    / "endpoint_adjudication.csv"
)

RESIDUAL_PATH = (
    DATA_DIR
    / "residual_endpoint_review.csv"
)

CROSS_COLOUR_PATH = (
    DATA_DIR
    / "cross_colour_endpoint_review.csv"
)

CROSSING_PATH = (
    DATA_DIR
    / "crossing_inventory.csv"
)

ORDER_REVIEW_PATH = (
    DATA_DIR
    / "gauss_order_review.csv"
)

DERIVED_PATH = (
    ROOT
    / "data"
    / "derived"
    / "a10_p03_cross_colour_matching_search.csv"
)

REPORT_PATH = (
    ROOT
    / "docs"
    / "geometry"
    / "a10_p03_cross_colour_matching_search_v0_7.md"
)

LAYERS = (
    "red",
    "green",
    "blue",
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
    """Load all one-based coloured trace fragments."""
    raw: dict[
        tuple[str, int],
        list[tuple[int, float, float]],
    ] = {}

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

        raw.setdefault(
            key,
            [],
        ).append(
            (
                int(row["point_index"]),
                float(row["panel_x"]),
                float(row["panel_y"]),
            )
        )

    result = {}

    for key, records in raw.items():
        records.sort(
            key=lambda value: value[0]
        )

        result[key] = np.asarray(
            [
                [value[1], value[2]]
                for value in records
            ],
            dtype=np.float64,
        )

    if len(result) != 24:
        raise RuntimeError(
            f"Expected 24 visible fragments; found {len(result)}."
        )

    return result


def accepted_rows(
    path: Path,
) -> list[dict[str, str]]:
    """Load accepted adjudication rows."""
    return [
        row
        for row in load_csv(path)
        if row["status"] == "accepted"
    ]


def parity_rows(
    visits,
) -> list[dict[str, object]]:
    """Convert ordered crossing visits into parity-audit rows."""
    return [
        {
            "order": order,
            "event_id": visit.event_id,
            "role": visit.role,
        }
        for order, visit in enumerate(
            visits,
            start=1,
        )
    ]


def write_csv(
    results: list[dict[str, object]],
) -> None:
    """Write the local derived search table."""
    DERIVED_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    fieldnames = [
        "matching_id",
        "is_frozen_baseline",
        "candidate_ids",
        "accepted_edge_count",
        "changed_edge_count",
        "total_score",
        "total_distance_px",
        "maximum_distance_px",
        "component_count",
        "is_single_cycle",
        "parity_violation_count",
        "passes_even_condition",
        "violating_events",
        "segment_traversal",
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
        writer.writerows(results)

    print(
        f"Wrote {DERIVED_PATH.relative_to(ROOT)}"
    )


def write_report(
    results: list[dict[str, object]],
) -> None:
    """Write the permanent matching-search report."""
    single_cycles = [
        result
        for result in results
        if result["is_single_cycle"]
    ]

    minimum_violations = min(
        int(
            result[
                "parity_violation_count"
            ]
        )
        for result in single_cycles
    )

    best = [
        result
        for result in single_cycles
        if int(
            result[
                "parity_violation_count"
            ]
        )
        == minimum_violations
    ]

    baseline = next(
        result
        for result in results
        if result["is_frozen_baseline"]
    )

    lines = [
        "# A10_P03 Cross-Colour Matching Search — v0.7",
        "",
        "## Purpose",
        "",
        "Enumerate every perfect matching of the six free "
        "cross-colour endpoints while preserving:",
        "",
        "- all accepted same-colour continuations;",
        "- the 31 reviewed crossing identities;",
        "- reviewed over-under assignments;",
        "- the source-derived crossing locations.",
        "",
        "The frozen Gauss and signed-Gauss snapshots are not modified.",
        "",
        "## Search space",
        "",
        f"- Cross-colour candidate edges: **12**",
        f"- Perfect matchings: **{len(results)}**",
        f"- Single-cycle matchings: **{len(single_cycles)}**",
        "",
        "## Result",
        "",
        f"- Frozen-baseline parity violations: "
        f"**{baseline['parity_violation_count']}**",
        f"- Minimum violations in the matching space: "
        f"**{minimum_violations}**",
        f"- Matchings attaining the minimum: "
        f"**{len(best)}**",
        "",
        "## Matching table",
        "",
        "| Matching | Baseline | Accepted edges | Changed edges | "
        "Score | Single cycle | Violations | Even pass |",
        "|---|---|---:|---:|---:|---|---:|---|",
    ]

    for result in sorted(
        results,
        key=lambda value: (
            int(
                value[
                    "parity_violation_count"
                ]
            )
            if value["is_single_cycle"]
            else 10**9,
            float(value["total_score"]),
        ),
    ):
        violations = (
            result[
                "parity_violation_count"
            ]
            if result["is_single_cycle"]
            else "—"
        )

        lines.append(
            f"| `{result['matching_id']}` | "
            f"{'yes' if result['is_frozen_baseline'] else 'no'} | "
            f"{result['accepted_edge_count']} | "
            f"{result['changed_edge_count']} | "
            f"{float(result['total_score']):.3f} | "
            f"{'yes' if result['is_single_cycle'] else 'no'} | "
            f"{violations} | "
            f"{'yes' if result['passes_even_condition'] else 'no'} |"
        )

    lines.extend(
        [
            "",
            "## Candidate details",
            "",
        ]
    )

    for result in results:
        lines.extend(
            [
                f"### {result['matching_id']}",
                "",
                f"- Frozen baseline: "
                f"`{result['is_frozen_baseline']}`",
                f"- Candidate edges: "
                f"`{result['candidate_ids']}`",
                f"- Total source score: "
                f"`{float(result['total_score']):.6f}`",
                f"- Parity violations: "
                f"`{result['parity_violation_count']}`",
                f"- Violating events: "
                f"`{result['violating_events'] or 'none'}`",
                f"- Traversal: "
                f"`{result['segment_traversal'] or 'not a single cycle'}`",
                "",
            ]
        )

    lines.extend(
        [
            "## Interpretation",
            "",
        ]
    )

    if minimum_violations == 0:
        lines.extend(
            [
                "At least one alternative cross-colour matching passes "
                "the necessary Gauss even condition.",
                "",
                "That matching is a computational candidate only. Its "
                "three transition edges must be returned to the source "
                "panel for targeted geometric review before replacing "
                "the frozen reconstruction.",
            ]
        )
    else:
        lines.extend(
            [
                "No cross-colour perfect matching removes all parity "
                "violations.",
                "",
                "Therefore the colour-transition matching alone is "
                "insufficient to explain the parity failure. The next "
                "search must expand to constrained crossing-order, "
                "crossing-identity or same-colour continuation "
                "alternatives.",
            ]
        )

    lines.extend(
        [
            "",
            "Passing this test would remain necessary but not sufficient "
            "for classical planar realizability.",
            "",
            "## Generated output",
            "",
            "- `data/derived/"
            "a10_p03_cross_colour_matching_search.csv` "
            "(local derived table)",
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
    """Run the complete cross-colour perfect-matching search."""
    segments = load_segments()

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
        accepted_rows(
            ENDPOINT_PATH
        )
        + accepted_rows(
            RESIDUAL_PATH
        )
    )

    cross_rows = load_csv(
        CROSS_COLOUR_PATH
    )

    crossing_rows = load_csv(
        CROSSING_PATH
    )

    order_reviews = load_csv(
        ORDER_REVIEW_PATH
    )

    matchings = (
        enumerate_endpoint_perfect_matchings(
            cross_rows
        )
    )

    if len(matchings) != 8:
        raise RuntimeError(
            f"Expected eight perfect matchings; found {len(matchings)}."
        )

    row_by_identifier = {
        row["candidate_id"]: row
        for row in cross_rows
    }

    baseline_ids = frozenset(
        row["candidate_id"]
        for row in cross_rows
        if row["status"] == "accepted"
    )

    results: list[
        dict[str, object]
    ] = []

    for matching in matchings:
        selected_rows = [
            row_by_identifier[
                identifier
            ]
            for identifier
            in matching.candidate_ids
        ]

        cycle = audit_global_cycle(
            segment_ids,
            same_colour,
            selected_rows,
        )

        violation_count = ""
        passes = False
        violating_events = ""
        traversal_text = ""

        if cycle.is_single_cycle:
            visits = build_crossing_visits(
                crossing_rows,
                segments,
                cycle.segment_traversal,
            )

            visits = apply_exact_tie_reviews(
                visits,
                order_reviews,
            )

            validate_complete_gauss_visits(
                visits,
                expected_event_count=31,
            )

            parity = audit_gauss_parity(
                parity_rows(visits)
            )

            violation_count = (
                parity.violation_count
            )

            passes = (
                parity.passes_even_condition
            )

            violating_events = " ".join(
                event.event_id
                for event
                in sorted(
                    parity.violating_events,
                    key=lambda event: int(
                        event.event_id[1:]
                    ),
                )
            )

            traversal_text = " → ".join(
                format_segment_visit(
                    visit
                )
                for visit
                in cycle.segment_traversal
            )

        results.append(
            {
                "matching_id": (
                    matching.matching_id
                ),
                "is_frozen_baseline": (
                    frozenset(
                        matching.candidate_ids
                    )
                    == baseline_ids
                ),
                "candidate_ids": " ".join(
                    matching.candidate_ids
                ),
                "accepted_edge_count": (
                    matching.accepted_edge_count
                ),
                "changed_edge_count": (
                    3
                    - matching.accepted_edge_count
                ),
                "total_score": (
                    matching.total_score
                ),
                "total_distance_px": (
                    matching.total_distance_px
                ),
                "maximum_distance_px": (
                    matching.maximum_distance_px
                ),
                "component_count": (
                    cycle.component_count
                ),
                "is_single_cycle": (
                    cycle.is_single_cycle
                ),
                "parity_violation_count": (
                    violation_count
                ),
                "passes_even_condition": (
                    passes
                ),
                "violating_events": (
                    violating_events
                ),
                "segment_traversal": (
                    traversal_text
                ),
            }
        )

    if sum(
        bool(
            result[
                "is_frozen_baseline"
            ]
        )
        for result in results
    ) != 1:
        raise RuntimeError(
            "The frozen baseline matching was not identified uniquely."
        )

    write_csv(results)
    write_report(results)

    print()
    print("A10_P03 cross-colour matching search")
    print("====================================")
    print(
        f"{'ID':<5}"
        f"{'Base':<7}"
        f"{'Score':>10}"
        f"{'Cycle':>8}"
        f"{'Violations':>12}"
    )

    for result in sorted(
        results,
        key=lambda value: (
            int(
                value[
                    "parity_violation_count"
                ]
            )
            if value["is_single_cycle"]
            else 10**9,
            float(value["total_score"]),
        ),
    ):
        violations = (
            str(
                result[
                    "parity_violation_count"
                ]
            )
            if result["is_single_cycle"]
            else "—"
        )

        print(
            f"{str(result['matching_id']):<5}"
            f"{('yes' if result['is_frozen_baseline'] else 'no'):<7}"
            f"{float(result['total_score']):>10.3f}"
            f"{('yes' if result['is_single_cycle'] else 'no'):>8}"
            f"{violations:>12}"
        )


if __name__ == "__main__":
    main()
