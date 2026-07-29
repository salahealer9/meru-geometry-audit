#!/usr/bin/env python3
"""Freeze the source-reviewed signed A10_P03 O/U Gauss word."""

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
from meru_geometry.crossing_signs import (
    crossing_sign_stability,
    derive_crossing_signs,
    writhe,
)
from meru_geometry.global_cycle import (
    audit_global_cycle,
    format_segment_visit,
)
from meru_geometry.signed_gauss import (
    SignedGaussVisit,
    build_signed_gauss_visits,
    validate_signed_gauss_visits,
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

SIGN_REVIEW_PATH = (
    DATA_DIR
    / "crossing_sign_review.csv"
)

SNAPSHOT_PATH = (
    DATA_DIR
    / "signed_gauss_word.csv"
)

HASH_PATH = (
    DATA_DIR
    / "signed_gauss_word.sha256"
)

REPORT_PATH = (
    ROOT
    / "docs"
    / "geometry"
    / "a10_p03_signed_gauss_word_v0_7.md"
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
    "crossing_sign",
    "event_token",
    "signed_token",
    "unsigned_token",
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
    "order_review_id",
    "sign_basis",
    "sign_review_id",
]


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
    """Load all 24 one-based coloured centreline fragments."""
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

    if len(result) != 24:
        raise RuntimeError(
            f"Expected 24 digitized segments; found {len(result)}."
        )

    return result


def accepted_rows(
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


def build_frozen_directions(
    segments: dict[
        tuple[str, int],
        np.ndarray,
    ],
) -> dict[
    tuple[str, int],
    bool,
]:
    """Rebuild all directions from the frozen v0.6 cycle."""
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
            "The reconstructed traversal differs from "
            "the frozen v0.6 traversal."
        )

    directions = {
        (
            visit.layer,
            visit.segment_id,
        ): visit.forward
        for visit in audit.segment_traversal
    }

    if set(directions) != set(segments):
        raise RuntimeError(
            "Frozen traversal and digitized segment sets differ."
        )

    return directions


def derive_reviewed_event_signs(
    inventory: list[dict[str, str]],
    segments: dict[
        tuple[str, int],
        np.ndarray,
    ],
    directions: dict[
        tuple[str, int],
        bool,
    ],
    review_rows: list[dict[str, str]],
) -> tuple[
    dict[str, int],
    dict[str, str],
    tuple,
]:
    """Derive every sign and validate the manual low-angle review."""
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

    unstable = [
        event_id
        for event_id, values in stability.items()
        if len(set(values)) != 1
    ]

    if unstable:
        raise RuntimeError(
            "Crossing signs are unstable across tangent spans: "
            + ", ".join(unstable)
        )

    minimum_angles: dict[
        str,
        float,
    ] = {}

    for span in SENSITIVITY_SPANS_PX:
        span_signs = derive_crossing_signs(
            inventory,
            segments,
            directions,
            span_px=span,
        )

        for result in span_signs:
            minimum_angles[result.event_id] = min(
                minimum_angles.get(
                    result.event_id,
                    float("inf"),
                ),
                result.crossing_angle_degrees,
            )

    expected_review_events = {
        event_id
        for event_id, angle in minimum_angles.items()
        if angle < LOW_ANGLE_THRESHOLD_DEGREES
    }

    review_by_event = {
        row["event_id"]: row
        for row in review_rows
    }

    if len(review_by_event) != len(review_rows):
        raise RuntimeError(
            "Crossing-sign review event identifiers are not unique."
        )

    if set(review_by_event) != expected_review_events:
        raise RuntimeError(
            "Tracked sign-review events differ from the "
            "derived low-angle review set."
        )

    derived_map = {
        result.event_id: result.sign
        for result in signs
    }

    sign_basis: dict[
        str,
        str,
    ] = {}

    for event_id in derived_map:
        review = review_by_event.get(
            event_id
        )

        if review is None:
            sign_basis[event_id] = (
                "derived_stable_all_spans"
            )
            continue

        if review["status"] != "accepted":
            raise RuntimeError(
                f"{event_id}: sign review is not accepted."
            )

        if review["confidence"] != "high":
            raise RuntimeError(
                f"{event_id}: sign review is not high confidence."
            )

        if not review["reviewed_utc"].strip():
            raise RuntimeError(
                f"{event_id}: sign review has no timestamp."
            )

        accepted_sign = int(
            review["accepted_sign"]
        )

        if accepted_sign != derived_map[event_id]:
            raise RuntimeError(
                f"{event_id}: accepted sign differs from "
                "the derived sign."
            )

        if not review["notes"].strip():
            raise RuntimeError(
                f"{event_id}: sign-review notes are missing."
            )

        sign_basis[event_id] = (
            "manual_low_angle_review"
        )

    if any(
        sign not in {-1, 1}
        for sign in derived_map.values()
    ):
        raise RuntimeError(
            "A degenerate crossing sign remains unresolved."
        )

    return (
        derived_map,
        sign_basis,
        signs,
    )


def snapshot_rows(
    gauss_rows: list[dict[str, str]],
    visits: tuple[SignedGaussVisit, ...],
    sign_basis: dict[str, str],
) -> list[dict[str, object]]:
    """Combine the frozen O/U rows with their reviewed signs."""
    ordered_rows = sorted(
        gauss_rows,
        key=lambda row: int(row["order"]),
    )

    rows: list[
        dict[str, object]
    ] = []

    for gauss_row, visit in zip(
        ordered_rows,
        visits,
        strict=True,
    ):
        if gauss_row["token"] != visit.unsigned_token:
            raise RuntimeError(
                "Signed and unsigned Gauss rows are misaligned."
            )

        basis = sign_basis[
            visit.event_id
        ]

        rows.append(
            {
                "order": visit.order,
                "event_id": visit.event_id,
                "role": visit.role,
                "crossing_sign": (
                    visit.crossing_sign
                ),
                "event_token": (
                    visit.event_token
                ),
                "signed_token": (
                    visit.signed_token
                ),
                "unsigned_token": (
                    visit.unsigned_token
                ),
                "candidate_id": (
                    gauss_row["candidate_id"]
                ),
                "segment_order": (
                    gauss_row["segment_order"]
                ),
                "layer": gauss_row["layer"],
                "segment_id": (
                    gauss_row["segment_id"]
                ),
                "traversal_forward": (
                    gauss_row["traversal_forward"]
                ),
                "source_fraction": (
                    gauss_row["source_fraction"]
                ),
                "traversal_fraction": (
                    gauss_row["traversal_fraction"]
                ),
                "global_position": (
                    gauss_row["global_position"]
                ),
                "panel_x": gauss_row["panel_x"],
                "panel_y": gauss_row["panel_y"],
                "order_basis": (
                    gauss_row["order_basis"]
                ),
                "order_review_id": (
                    gauss_row["review_id"]
                ),
                "sign_basis": basis,
                "sign_review_id": (
                    visit.event_id
                    if basis
                    == "manual_low_angle_review"
                    else ""
                ),
            }
        )

    return rows


def token_digest(
    tokens: tuple[str, ...],
) -> str:
    """Hash the canonical newline-delimited signed tokens."""
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
    """Write the canonical signed-word snapshot and digest."""
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
        f"{digest}  signed_gauss_word.tokens\n",
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
    """Validate the reconstruction against the frozen snapshot."""
    if not SNAPSHOT_PATH.exists():
        raise RuntimeError(
            "The signed Gauss-word snapshot is missing. "
            "Run once with --update-snapshot."
        )

    if not HASH_PATH.exists():
        raise RuntimeError(
            "The signed Gauss-word digest is missing."
        )

    existing_rows = load_csv(
        SNAPSHOT_PATH
    )

    existing_tokens = tuple(
        row["signed_token"]
        for row in existing_rows
    )

    if existing_tokens != tokens:
        raise RuntimeError(
            "Computed signed Gauss word differs from "
            "the frozen snapshot."
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
            "Computed signed Gauss-word digest differs from "
            "the frozen digest."
        )

    print(
        "PASS: computed signed Gauss word matches "
        "the frozen snapshot."
    )


def wrapped_tokens(
    tokens: tuple[str, ...],
) -> str:
    """Format a readable signed token sequence."""
    return "\n".join(
        textwrap.wrap(
            " ".join(tokens),
            width=100,
        )
    )


def write_report(
    visits: tuple[SignedGaussVisit, ...],
    sign_basis: dict[str, str],
    signs,
    digest: str,
) -> None:
    """Write the permanent signed-word report."""
    tokens = tuple(
        visit.signed_token
        for visit in visits
    )

    event_signs = {
        visit.event_id: visit.crossing_sign
        for visit in visits
    }

    counts = Counter(
        event_signs.values()
    )

    manually_reviewed = sorted(
        (
            event_id
            for event_id, basis in sign_basis.items()
            if basis == "manual_low_angle_review"
        ),
        key=lambda event_id: int(
            event_id[1:]
        ),
    )

    lines = [
        "# A10_P03 Source-Reviewed Signed Gauss Word — v0.7",
        "",
        "## Result",
        "",
        "The frozen 62-visit O/U Gauss word has been combined with "
        "the reviewed oriented sign of every crossing event.",
        "",
        f"- Crossing events: **{len(visits) // 2}**",
        f"- Signed visits: **{len(visits)}**",
        f"- Positive events: **{counts.get(1, 0)}**",
        f"- Negative events: **{counts.get(-1, 0)}**",
        f"- Writhe: **{writhe(signs)}**",
        "- Degenerate signs: **0**",
        "- Unresolved order decisions: **0**",
        "- Unresolved sign decisions: **0**",
        f"- Signed-token SHA-256: `{digest}`",
        "",
        "## Notation",
        "",
        "Each ASCII token has the form:",
        "",
        "```text",
        "E<event><O-or-U><crossing-sign>",
        "```",
        "",
        "For example, `E13O-` denotes the over-strand visit to "
        "negative crossing event E13.",
        "",
        "This is an explicit project notation rather than an assertion "
        "that every published Gauss-code convention uses the same "
        "token layout.",
        "",
        "## Canonical signed O/U Gauss word",
        "",
        "```text",
        wrapped_tokens(tokens),
        "```",
        "",
        "Every event occurs exactly twice, once as `O` and once as `U`, "
        "and both visits carry the same oriented event sign.",
        "",
        "## Sign evidence",
        "",
        f"- Signs stable across all tangent spans: "
        f"**{len(sign_basis)}/{len(sign_basis)}**",
        "- Primary tangent span: **6 px**",
        "- Sensitivity spans: **2, 4, 6, 8, 10 and 12 px**",
        "- Manually reviewed low-angle events: "
        + ", ".join(
            f"`{event_id}`"
            for event_id in manually_reviewed
        ),
        "",
        "The remaining events use the basis "
        "`derived_stable_all_spans`.",
        "",
        "## Reproducibility boundary",
        "",
        "The signed sequence is frozen in:",
        "",
        "- `data/manual_digitizations/A10_P03/"
        "signed_gauss_word.csv`;",
        "- `data/manual_digitizations/A10_P03/"
        "signed_gauss_word.sha256`.",
        "",
        "Normal execution validates the reconstruction against these "
        "files. Replacing them requires the explicit "
        "`--update-snapshot` option.",
        "",
        "## Interpretation boundary",
        "",
        "This result establishes a source-reviewed signed O/U Gauss "
        "word for the reconstructed A10_P03 planar diagram under the "
        "documented coordinate and sign convention.",
        "",
        "It does not yet establish:",
        "",
        "- equivalence with a canonical `(3,10)` torus knot;",
        "- minimal crossing number;",
        "- a canonical Dowker–Thistlethwaite representation;",
        "- an Alexander or Jones polynomial;",
        "- a unique three-dimensional embedding.",
        "",
        "The next stage is to derive a convention-explicit Dowker-style "
        "code and independently validate that it reconstructs the same "
        "signed Gauss data.",
        "",
    ]

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
            "Create or replace the signed Gauss-word snapshot. "
            "Use only after documented source review."
        ),
    )

    return parser.parse_args()


def main() -> None:
    """Construct and freeze the signed A10_P03 Gauss word."""
    arguments = parse_arguments()

    inventory = load_csv(
        INVENTORY_PATH
    )

    validate_crossing_review_rows(
        inventory
    )

    gauss_rows = load_csv(
        GAUSS_WORD_PATH
    )

    review_rows = load_csv(
        SIGN_REVIEW_PATH
    )

    segments = load_segments()

    directions = build_frozen_directions(
        segments
    )

    (
        event_signs,
        sign_basis,
        signs,
    ) = derive_reviewed_event_signs(
        inventory,
        segments,
        directions,
        review_rows,
    )

    visits = build_signed_gauss_visits(
        gauss_rows,
        event_signs,
    )

    validate_signed_gauss_visits(
        visits,
        expected_event_count=31,
    )

    if len(visits) != 62:
        raise RuntimeError(
            f"Expected 62 signed visits; found {len(visits)}."
        )

    tokens = tuple(
        visit.signed_token
        for visit in visits
    )

    digest = token_digest(
        tokens
    )

    rows = snapshot_rows(
        gauss_rows,
        visits,
        sign_basis,
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
        visits,
        sign_basis,
        signs,
        digest,
    )

    counts = Counter(
        event_signs.values()
    )

    print()
    print("A10_P03 signed Gauss word")
    print("=========================")
    print("Crossing events:", len(event_signs))
    print("Signed visits:  ", len(visits))
    print("Positive:       ", counts.get(1, 0))
    print("Negative:       ", counts.get(-1, 0))
    print("Writhe:         ", writhe(signs))
    print("Unresolved:     ", 0)
    print("SHA-256:        ", digest)
    print()
    print(
        wrapped_tokens(tokens)
    )


if __name__ == "__main__":
    main()
