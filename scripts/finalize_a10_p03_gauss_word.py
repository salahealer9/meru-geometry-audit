#!/usr/bin/env python3
"""Freeze the source-reviewed A10_P03 O/U Gauss word."""

from __future__ import annotations

import argparse
import csv
import hashlib
import textwrap
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

from meru_geometry.crossing_review import (
    validate_crossing_review_rows,
)
from meru_geometry.gauss_visits import (
    CrossingVisit,
    apply_order_reviews,
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

INVENTORY_PATH = (
    DATA_DIR
    / "crossing_inventory.csv"
)

ORDER_REVIEW_PATH = (
    DATA_DIR
    / "gauss_order_review.csv"
)

SNAPSHOT_PATH = (
    DATA_DIR
    / "gauss_word.csv"
)

HASH_PATH = (
    DATA_DIR
    / "gauss_word.sha256"
)

REPORT_PATH = (
    ROOT
    / "docs"
    / "geometry"
    / "a10_p03_gauss_word_v0_7.md"
)

LAYERS = (
    "red",
    "green",
    "blue",
)

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

SNAPSHOT_FIELDS = [
    "order",
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
    "order_basis",
    "review_id",
]


def load_csv(
    path: Path,
) -> list[dict[str, str]]:
    """Load one CSV table."""
    with path.open(
        newline="",
        encoding="utf-8",
    ) as handle:
        return list(csv.DictReader(handle))


def load_segments() -> dict[
    tuple[str, int],
    np.ndarray,
]:
    """Load one-based A10_P03 coloured centreline fragments."""
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

    result: dict[
        tuple[str, int],
        np.ndarray,
    ] = {}

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
    """Load accepted endpoint-review rows."""
    return [
        row
        for row in load_csv(
            DATA_DIR / filename
        )
        if row["status"] == "accepted"
    ]


def build_frozen_traversal(
    segments: dict[
        tuple[str, int],
        np.ndarray,
    ],
):
    """Rebuild and verify the frozen v0.6 global cycle."""
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
            "The reconstructed traversal differs from "
            "the frozen v0.6 traversal."
        )

    return audit


def validate_order_reviews(
    rows: list[dict[str, str]],
) -> None:
    """Require four complete high-confidence ordering decisions."""
    if len(rows) != 4:
        raise RuntimeError(
            f"Expected four order-review rows; found {len(rows)}."
        )

    identifiers = [
        row["review_id"]
        for row in rows
    ]

    if len(set(identifiers)) != len(identifiers):
        raise RuntimeError(
            "Order-review identifiers are not unique."
        )

    for row in rows:
        if row["status"] != "accepted":
            raise RuntimeError(
                f"{row['review_id']} is not accepted."
            )

        if row["confidence"] != "high":
            raise RuntimeError(
                f"{row['review_id']} is not high confidence."
            )

        if not row["reviewed_utc"].strip():
            raise RuntimeError(
                f"{row['review_id']} has no review timestamp."
            )

        if {
            row["accepted_first"],
            row["accepted_second"],
        } != {
            row["provisional_first"],
            row["provisional_second"],
        }:
            raise RuntimeError(
                f"{row['review_id']} changes the reviewed visit pair."
            )


def review_token_map(
    rows: list[dict[str, str]],
) -> dict[str, dict[str, str]]:
    """Map each manually reviewed token to its review record."""
    result: dict[
        str,
        dict[str, str],
    ] = {}

    for row in rows:
        for token in (
            row["accepted_first"],
            row["accepted_second"],
        ):
            if token in result:
                raise RuntimeError(
                    f"Visit token {token} occurs in multiple "
                    "order-review rows."
                )

            result[token] = row

    return result


def snapshot_rows(
    visits: tuple[CrossingVisit, ...],
    reviews: list[dict[str, str]],
) -> list[dict[str, object]]:
    """Build the canonical tracked snapshot rows."""
    token_reviews = review_token_map(
        reviews
    )

    rows: list[dict[str, object]] = []

    for order, visit in enumerate(
        visits,
        start=1,
    ):
        review = token_reviews.get(
            visit.token
        )

        if review is None:
            order_basis = (
                "derived_arc_order"
            )

            review_id = ""

        elif review["review_kind"] == "exact_tie":
            order_basis = (
                "manual_exact_tie_resolution"
            )

            review_id = review["review_id"]

        else:
            order_basis = (
                "manual_close_order_confirmation"
            )

            review_id = review["review_id"]

        rows.append(
            {
                "order": order,
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
                "order_basis": order_basis,
                "review_id": review_id,
            }
        )

    return rows


def token_digest(
    tokens: tuple[str, ...],
) -> str:
    """Hash the canonical newline-delimited token sequence."""
    payload = (
        "\n".join(tokens) + "\n"
    ).encode("utf-8")

    return hashlib.sha256(
        payload
    ).hexdigest()


def write_snapshot(
    rows: list[dict[str, object]],
    digest: str,
) -> None:
    """Write the canonical CSV and token-sequence digest."""
    with SNAPSHOT_PATH.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=SNAPSHOT_FIELDS,
            lineterminator="\n",
        )

        writer.writeheader()
        writer.writerows(rows)

    HASH_PATH.write_text(
        f"{digest}  gauss_word.tokens\n",
        encoding="utf-8",
    )

    print(
        f"Wrote {SNAPSHOT_PATH.relative_to(ROOT)}"
    )

    print(
        f"Wrote {HASH_PATH.relative_to(ROOT)}"
    )


def validate_snapshot(
    tokens: tuple[str, ...],
    digest: str,
) -> None:
    """Verify the computed word against the frozen snapshot."""
    if not SNAPSHOT_PATH.exists():
        raise RuntimeError(
            "The canonical Gauss-word snapshot does not exist. "
            "Run once with --update-snapshot after source review."
        )

    if not HASH_PATH.exists():
        raise RuntimeError(
            "The canonical Gauss-word digest does not exist."
        )

    existing_rows = load_csv(
        SNAPSHOT_PATH
    )

    existing_tokens = tuple(
        row["token"]
        for row in existing_rows
    )

    if existing_tokens != tokens:
        raise RuntimeError(
            "Computed Gauss word differs from the frozen snapshot. "
            "Do not update it without a documented source review."
        )

    recorded_digest = (
        HASH_PATH.read_text(
            encoding="utf-8"
        )
        .strip()
        .split()[0]
    )

    if recorded_digest != digest:
        raise RuntimeError(
            "Computed Gauss-word digest differs from "
            "the frozen digest."
        )

    print(
        "PASS: computed Gauss word matches the frozen snapshot."
    )


def wrapped_tokens(
    tokens: tuple[str, ...],
) -> str:
    """Format the Gauss word for reports and terminal output."""
    return "\n".join(
        textwrap.wrap(
            " ".join(tokens),
            width=100,
        )
    )


def write_report(
    visits: tuple[CrossingVisit, ...],
    reviews: list[dict[str, str]],
    audit,
    digest: str,
) -> None:
    """Write the permanent source-reviewed Gauss-word report."""
    tokens = tuple(
        visit.token
        for visit in visits
    )

    role_counts = Counter(
        visit.role
        for visit in visits
    )

    by_segment: dict[
        tuple[str, int],
        list[str],
    ] = defaultdict(list)

    for visit in visits:
        by_segment[
            visit.segment_key
        ].append(
            visit.token
        )

    lines = [
        "# A10_P03 Source-Reviewed O/U Gauss Word — v0.7",
        "",
        "## Result",
        "",
        "The completed A10_P03 crossing inventory and four manual "
        "visit-order decisions define one unique O/U Gauss word along "
        "the frozen v0.6 global-cycle traversal.",
        "",
        f"- Crossing events: **{len(visits) // 2}**",
        f"- Total visits: **{len(visits)}**",
        f"- Over visits: **{role_counts.get('O', 0)}**",
        f"- Under visits: **{role_counts.get('U', 0)}**",
        "- Unresolved visit-order ties: **0**",
        "- Ambiguous crossing assignments: **0**",
        f"- Token-sequence SHA-256: `{digest}`",
        "",
        "## Canonical O/U Gauss word",
        "",
        "```text",
        wrapped_tokens(tokens),
        "```",
        "",
        "Every event label appears exactly twice: once with `O` and "
        "once with `U`.",
        "",
        "## Manual order resolutions",
        "",
        "| Review | Segment | Accepted order | Confidence |",
        "|---|---|---|---|",
    ]

    for row in reviews:
        lines.append(
            f"| `{row['review_id']}` | "
            f"{row['layer'].capitalize()} "
            f"S{int(row['segment_id']):02d} | "
            f"`{row['accepted_first']} → "
            f"{row['accepted_second']}` | "
            f"{row['confidence'].capitalize()} |"
        )

    lines.extend(
        [
            "",
            "The red S01 decision resolves an exact positional tie "
            "caused by both visits being represented at the same "
            "digitized fragment endpoint. The other three reviews "
            "confirm close but already distinct arc-length orders.",
            "",
            "## Visits grouped by frozen segment",
            "",
            "| Traversal segment | Visits in accepted order |",
            "|---|---|",
        ]
    )

    for segment_visit in audit.segment_traversal:
        key = (
            segment_visit.layer,
            segment_visit.segment_id,
        )

        segment_tokens = by_segment.get(
            key,
            [],
        )

        lines.append(
            f"| `{format_segment_visit(segment_visit)}` | "
            f"`{' '.join(segment_tokens) or '—'}` |"
        )

    lines.extend(
        [
            "",
            "## Reproducibility boundary",
            "",
            "The canonical token sequence is frozen in:",
            "",
            "- `data/manual_digitizations/A10_P03/gauss_word.csv`;",
            "- `data/manual_digitizations/A10_P03/gauss_word.sha256`.",
            "",
            "A normal execution validates the reconstructed word "
            "against these files. Replacing the snapshot requires the "
            "explicit `--update-snapshot` option.",
            "",
            "## Interpretation boundary",
            "",
            "This result establishes a unique source-reviewed O/U "
            "Gauss word for the reconstructed planar cycle.",
            "",
            "It does not yet establish:",
            "",
            "- oriented crossing signs;",
            "- a signed Gauss code;",
            "- a Dowker–Thistlethwaite code;",
            "- an Alexander or Jones polynomial;",
            "- equivalence with the canonical `(3,10)` torus knot;",
            "- a unique three-dimensional embedding.",
            "",
            "The next stage is to calculate an oriented tangent at "
            "both branches of every crossing and assign crossing "
            "signs under one documented coordinate convention.",
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


def parse_arguments() -> argparse.Namespace:
    """Parse snapshot-update control."""
    parser = argparse.ArgumentParser(
        description=__doc__,
    )

    parser.add_argument(
        "--update-snapshot",
        action="store_true",
        help=(
            "Create or replace the frozen Gauss-word snapshot. "
            "Use only after documented source review."
        ),
    )

    return parser.parse_args()


def main() -> None:
    """Construct and freeze the unique A10_P03 O/U Gauss word."""
    arguments = parse_arguments()

    segments = load_segments()

    inventory = load_csv(
        INVENTORY_PATH
    )

    validate_crossing_review_rows(
        inventory
    )

    reviews = load_csv(
        ORDER_REVIEW_PATH
    )

    validate_order_reviews(
        reviews
    )

    audit = build_frozen_traversal(
        segments
    )

    provisional_visits = build_crossing_visits(
        inventory,
        segments,
        audit.segment_traversal,
    )

    final_visits = apply_order_reviews(
        provisional_visits,
        reviews,
        require_complete=True,
    )

    validate_complete_gauss_visits(
        final_visits,
        expected_event_count=31,
    )

    if len(final_visits) != 62:
        raise RuntimeError(
            f"Expected 62 visits; found {len(final_visits)}."
        )

    tokens = tuple(
        visit.token
        for visit in final_visits
    )

    digest = token_digest(
        tokens
    )

    rows = snapshot_rows(
        final_visits,
        reviews,
    )

    if arguments.update_snapshot:
        write_snapshot(
            rows,
            digest,
        )
    else:
        validate_snapshot(
            tokens,
            digest,
        )

    write_report(
        final_visits,
        reviews,
        audit,
        digest,
    )

    print()
    print("A10_P03 source-reviewed Gauss word")
    print("==================================")
    print("Crossing events:", len(final_visits) // 2)
    print("Total visits:   ", len(final_visits))
    print("Unresolved ties:", 0)
    print("SHA-256:        ", digest)
    print()
    print(wrapped_tokens(tokens))


if __name__ == "__main__":
    main()
