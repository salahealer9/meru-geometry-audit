#!/usr/bin/env python3
"""Search every provisional A10_P03 endpoint perfect matching."""

from __future__ import annotations

import csv
import hashlib
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

from meru_geometry.endpoint_matching_search import (
    apply_exact_tie_reviews,
    endpoint_pair,
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

ENDPOINT_PATHS = (
    DATA_DIR
    / "endpoint_adjudication.csv",
    DATA_DIR
    / "residual_endpoint_review.csv",
    DATA_DIR
    / "cross_colour_endpoint_review.csv",
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
    / "a10_p03_full_endpoint_matching_search.csv"
)

REPORT_PATH = (
    ROOT
    / "docs"
    / "geometry"
    / "a10_p03_full_endpoint_matching_search_v0_7.md"
)

LAYERS = (
    "red",
    "green",
    "blue",
)

EXPECTED_MATCHING_COUNT = 28


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


def load_candidate_rows() -> list[
    dict[str, str]
]:
    """Load all endpoint candidates and retain source provenance."""
    rows: list[
        dict[str, str]
    ] = []

    identifiers: set[str] = set()

    for path in ENDPOINT_PATHS:
        for raw_row in load_csv(path):
            row = dict(raw_row)

            identifier = row[
                "candidate_id"
            ]

            if identifier in identifiers:
                raise RuntimeError(
                    "Duplicate endpoint candidate: "
                    f"{identifier}"
                )

            identifiers.add(
                identifier
            )

            row["_source_table"] = (
                path.name
            )

            rows.append(row)

    if len(rows) != 47:
        raise RuntimeError(
            f"Expected 47 endpoint candidates; found {len(rows)}."
        )

    return rows


def load_segments() -> dict[
    tuple[str, int],
    np.ndarray,
]:
    """Load all 24 one-based visible trace fragments."""
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
                [
                    record[1],
                    record[2],
                ]
                for record in records
            ],
            dtype=np.float64,
        )

    if len(result) != 24:
        raise RuntimeError(
            f"Expected 24 fragments; found {len(result)}."
        )

    return result


def candidate_layers(
    row: dict[str, str],
) -> tuple[str, str]:
    """Return layers under either endpoint-table schema."""
    layer_a = row.get(
        "layer_a",
        "",
    ).strip()

    layer_b = row.get(
        "layer_b",
        "",
    ).strip()

    if layer_a and layer_b:
        return layer_a, layer_b

    layer = row.get(
        "layer",
        "",
    ).strip()

    if layer:
        return layer, layer

    raise RuntimeError(
        f"{row['candidate_id']}: no layer information."
    )


def parity_rows(
    visits,
) -> list[dict[str, object]]:
    """Convert crossing visits to the parity-audit schema."""
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


def event_sort_key(
    event_id: str,
) -> tuple[str, int, str]:
    """Naturally order identifiers such as E01 through E31."""
    split_index = len(
        event_id
    )

    while (
        split_index > 0
        and event_id[
            split_index - 1
        ].isdigit()
    ):
        split_index -= 1

    suffix = event_id[
        split_index:
    ]

    return (
        event_id[
            :split_index
        ],
        int(suffix)
        if suffix
        else -1,
        event_id,
    )


def reason_profile(
    rows: list[dict[str, str]],
) -> str:
    """Summarise selected reason codes."""
    counts = Counter(
        row.get(
            "reason_code",
            "",
        ).strip()
        or "unspecified"
        for row in rows
    )

    return ";".join(
        f"{reason}:{count}"
        for reason, count
        in sorted(
            counts.items()
        )
    )


def word_digest(
    visits,
) -> str:
    """Hash one newline-delimited unsigned visit sequence."""
    payload = (
        "\n".join(
            visit.token
            for visit in visits
        )
        + "\n"
    ).encode("utf-8")

    return hashlib.sha256(
        payload
    ).hexdigest()


def write_csv(
    results: list[dict[str, object]],
) -> None:
    """Write the local exhaustive search table."""
    DERIVED_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    fieldnames = [
        "rank",
        "matching_id",
        "is_frozen_baseline",
        "accepted_edge_count",
        "changed_edge_count",
        "selected_rejected_edge_count",
        "selected_rejected_reason_codes",
        "selected_rejected_candidate_ids",
        "candidate_ids",
        "total_score",
        "total_distance_px",
        "maximum_distance_px",
        "component_count",
        "is_single_cycle",
        "parity_violation_count",
        "passes_even_condition",
        "violating_events",
        "gauss_word_sha256",
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

        for rank, result in enumerate(
            results,
            start=1,
        ):
            writer.writerow(
                {
                    "rank": rank,
                    **result,
                }
            )

    print(
        f"Wrote {DERIVED_PATH.relative_to(ROOT)}"
    )


def write_report(
    results: list[dict[str, object]],
) -> None:
    """Write the permanent full-matching search report."""
    baseline = next(
        result
        for result in results
        if result["is_frozen_baseline"]
    )

    single_cycles = [
        result
        for result in results
        if result["is_single_cycle"]
    ]

    if not single_cycles:
        raise RuntimeError(
            "No candidate matching forms a single cycle."
        )

    minimum = min(
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
        == minimum
    ]

    zero_candidates = [
        result
        for result in single_cycles
        if result[
            "passes_even_condition"
        ]
    ]

    syndromes = {
        str(
            result[
                "violating_events"
            ]
        )
        for result in single_cycles
    }

    lines = [
        "# A10_P03 Full Endpoint-Matching Search — v0.7",
        "",
        "## Purpose",
        "",
        "Enumerate all provisional perfect matchings in the combined "
        "same-colour and cross-colour endpoint-candidate graph.",
        "",
        "The search preserves:",
        "",
        "- all 24 digitized visible fragments;",
        "- all 31 reviewed crossing identities;",
        "- all reviewed over-under assignments;",
        "- all source-derived crossing locations;",
        "- the manually resolved exact visit-order tie.",
        "",
        "The frozen Gauss snapshots are not modified.",
        "",
        "## Search boundary",
        "",
        "Rejected endpoint rows are included as hypothetical graph "
        "alternatives. They are not treated as evidentially equivalent "
        "to accepted rows.",
        "",
        "Several rejected rows carry substantive reasons such as "
        "`different_feature`, `colour_intersection`, "
        "`crossing_conflict`, or `colour_transition_conflict`.",
        "",
        "## Search-space census",
        "",
        "- Endpoint nodes: **48**",
        "- Candidate edges: **47**",
        f"- Perfect matchings: **{len(results)}**",
        f"- Single-cycle matchings: **{len(single_cycles)}**",
        f"- Distinct parity syndromes: **{len(syndromes)}**",
        "",
        "## Result",
        "",
        f"- Frozen-baseline violations: "
        f"**{baseline['parity_violation_count']}**",
        f"- Minimum violations: **{minimum}**",
        f"- Candidates attaining the minimum: **{len(best)}**",
        f"- Zero-violation candidates: **{len(zero_candidates)}**",
        "",
        "## Exhaustive table",
        "",
        "| Rank | Matching | Baseline | Accepted edges | "
        "Changed edges | Components | Single cycle | "
        "Violations | Even pass |",
        "|---:|---|---|---:|---:|---:|---|---:|---|",
    ]

    for rank, result in enumerate(
        results,
        start=1,
    ):
        violations = (
            result[
                "parity_violation_count"
            ]
            if result[
                "is_single_cycle"
            ]
            else "—"
        )

        lines.append(
            f"| {rank} | `{result['matching_id']}` | "
            f"{'yes' if result['is_frozen_baseline'] else 'no'} | "
            f"{result['accepted_edge_count']} | "
            f"{result['changed_edge_count']} | "
            f"{result['component_count']} | "
            f"{'yes' if result['is_single_cycle'] else 'no'} | "
            f"{violations} | "
            f"{'yes' if result['passes_even_condition'] else 'no'} |"
        )

    lines.extend(
        [
            "",
            "## Best candidate details",
            "",
        ]
    )

    for result in best:
        lines.extend(
            [
                f"### {result['matching_id']}",
                "",
                f"- Frozen baseline: "
                f"`{result['is_frozen_baseline']}`",
                f"- Accepted edges retained: "
                f"`{result['accepted_edge_count']}/24`",
                f"- Changed endpoint edges: "
                f"`{result['changed_edge_count']}`",
                f"- Selected rejected-edge reasons: "
                f"`{result['selected_rejected_reason_codes'] or 'none'}`",
                f"- Selected rejected candidates: "
                f"`{result['selected_rejected_candidate_ids'] or 'none'}`",
                f"- Parity violations: "
                f"`{result['parity_violation_count']}`",
                f"- Violating events: "
                f"`{result['violating_events'] or 'none'}`",
                "",
            ]
        )

    lines.extend(
        [
            "## Interpretation",
            "",
        ]
    )

    if zero_candidates:
        lines.extend(
            [
                "At least one provisional endpoint matching passes the "
                "necessary Gauss even condition.",
                "",
                "Its changed edges must be returned to the source panel "
                "for targeted review before it can replace the frozen "
                "reconstruction.",
            ]
        )
    else:
        lines.extend(
            [
                "No provisional endpoint perfect matching removes the "
                "Gauss-parity failure.",
                "",
                "Therefore endpoint connectivity, across both same-colour "
                "and cross-colour alternatives currently represented in "
                "the candidate graph, is insufficient to explain the "
                "failure.",
                "",
                "The next audit must move to the crossing inventory "
                "itself: missed crossings, duplicated crossing events, "
                "or incorrect crossing-to-fragment assignments.",
            ]
        )

    lines.extend(
        [
            "",
            "Even a zero-violation result would provide only a necessary, "
            "not sufficient, classical-realizability condition.",
            "",
            "## Generated output",
            "",
            "- `data/derived/"
            "a10_p03_full_endpoint_matching_search.csv` "
            "(local exhaustive table)",
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
    """Run the complete 28-matching endpoint search."""
    candidate_rows = (
        load_candidate_rows()
    )

    matchings = (
        enumerate_endpoint_perfect_matchings(
            candidate_rows
        )
    )

    if len(matchings) != (
        EXPECTED_MATCHING_COUNT
    ):
        raise RuntimeError(
            f"Expected {EXPECTED_MATCHING_COUNT} perfect matchings; "
            f"found {len(matchings)}."
        )

    row_by_identifier = {
        row["candidate_id"]: row
        for row in candidate_rows
    }

    accepted_ids = frozenset(
        row["candidate_id"]
        for row in candidate_rows
        if row["status"]
        == "accepted"
    )

    if len(accepted_ids) != 24:
        raise RuntimeError(
            f"Expected 24 accepted endpoint edges; "
            f"found {len(accepted_ids)}."
        )

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

    crossing_rows = load_csv(
        CROSSING_PATH
    )

    order_reviews = load_csv(
        ORDER_REVIEW_PATH
    )

    raw_results: list[
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

        same_colour = []
        cross_colour = []

        for row in selected_rows:
            layer_a, layer_b = (
                candidate_layers(row)
            )

            if layer_a == layer_b:
                same_colour.append(row)
            else:
                cross_colour.append(row)

        cycle = audit_global_cycle(
            segment_ids,
            same_colour,
            cross_colour,
        )

        is_baseline = (
            frozenset(
                matching.candidate_ids
            )
            == accepted_ids
        )

        rejected_rows = [
            row
            for row in selected_rows
            if row["status"]
            != "accepted"
        ]

        result: dict[
            str,
            object,
        ] = {
            "matching_id": (
                matching.matching_id
            ),
            "is_frozen_baseline": (
                is_baseline
            ),
            "accepted_edge_count": (
                matching.accepted_edge_count
            ),
            "changed_edge_count": (
                24
                - matching.accepted_edge_count
            ),
            "selected_rejected_edge_count": (
                len(rejected_rows)
            ),
            "selected_rejected_reason_codes": (
                reason_profile(
                    rejected_rows
                )
            ),
            "selected_rejected_candidate_ids": (
                " ".join(
                    sorted(
                        row["candidate_id"]
                        for row
                        in rejected_rows
                    )
                )
            ),
            "candidate_ids": " ".join(
                matching.candidate_ids
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
            "parity_violation_count": "",
            "passes_even_condition": False,
            "violating_events": "",
            "gauss_word_sha256": "",
            "segment_traversal": "",
        }

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

            result[
                "parity_violation_count"
            ] = parity.violation_count

            result[
                "passes_even_condition"
            ] = parity.passes_even_condition

            result[
                "violating_events"
            ] = " ".join(
                event.event_id
                for event in sorted(
                    parity.violating_events,
                    key=lambda event: (
                        event_sort_key(
                            event.event_id
                        )
                    ),
                )
            )

            result[
                "gauss_word_sha256"
            ] = word_digest(
                visits
            )

            result[
                "segment_traversal"
            ] = " → ".join(
                format_segment_visit(
                    visit
                )
                for visit
                in cycle.segment_traversal
            )

        raw_results.append(
            result
        )

    baseline_rows = [
        result
        for result in raw_results
        if result[
            "is_frozen_baseline"
        ]
    ]

    if len(baseline_rows) != 1:
        raise RuntimeError(
            "The accepted endpoint baseline was not identified uniquely."
        )

    if (
        baseline_rows[0][
            "parity_violation_count"
        ]
        != 16
    ):
        raise RuntimeError(
            "The accepted baseline no longer reproduces "
            "the frozen 16-violation result."
        )

    results = sorted(
        raw_results,
        key=lambda result: (
            0
            if result[
                "is_single_cycle"
            ]
            else 1,
            int(
                result[
                    "parity_violation_count"
                ]
            )
            if result[
                "is_single_cycle"
            ]
            else 10**9,
            int(
                result[
                    "changed_edge_count"
                ]
            ),
            float(
                result[
                    "total_score"
                ]
            ),
            str(
                result[
                    "matching_id"
                ]
            ),
        ),
    )

    write_csv(
        results
    )

    write_report(
        results
    )

    single_cycles = [
        result
        for result in results
        if result[
            "is_single_cycle"
        ]
    ]

    minimum = min(
        int(
            result[
                "parity_violation_count"
            ]
        )
        for result in single_cycles
    )

    print()
    print("A10_P03 full endpoint-matching search")
    print("=====================================")
    print("Perfect matchings:", len(results))
    print("Single cycles:    ", len(single_cycles))
    print("Minimum violations:", minimum)
    print()

    print(
        f"{'Rank':>4} "
        f"{'ID':<5}"
        f"{'Base':<7}"
        f"{'Keep':>6}"
        f"{'Change':>8}"
        f"{'Comp':>6}"
        f"{'Cycle':>8}"
        f"{'Violations':>12}"
    )

    for rank, result in enumerate(
        results,
        start=1,
    ):
        violations = (
            str(
                result[
                    "parity_violation_count"
                ]
            )
            if result[
                "is_single_cycle"
            ]
            else "—"
        )

        print(
            f"{rank:>4} "
            f"{str(result['matching_id']):<5}"
            f"{('yes' if result['is_frozen_baseline'] else 'no'):<7}"
            f"{int(result['accepted_edge_count']):>6}"
            f"{int(result['changed_edge_count']):>8}"
            f"{int(result['component_count']):>6}"
            f"{('yes' if result['is_single_cycle'] else 'no'):>8}"
            f"{violations:>12}"
        )


if __name__ == "__main__":
    main()
