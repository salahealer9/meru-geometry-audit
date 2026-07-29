#!/usr/bin/env python3
"""Audit the classical Gauss parity condition for A10_P03."""

from __future__ import annotations

import csv
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt

from meru_geometry.gauss_parity import (
    GaussParityAudit,
    audit_gauss_parity,
)


ROOT = Path(__file__).resolve().parents[1]

DATA_DIR = (
    ROOT
    / "data"
    / "manual_digitizations"
    / "A10_P03"
)

GAUSS_PATH = (
    DATA_DIR
    / "gauss_word.csv"
)

SIGNED_PATH = (
    DATA_DIR
    / "signed_gauss_word.csv"
)

DERIVED_PATH = (
    ROOT
    / "data"
    / "derived"
    / "a10_p03_gauss_parity_audit.csv"
)

REPORT_PATH = (
    ROOT
    / "docs"
    / "geometry"
    / "a10_p03_gauss_parity_audit_v0_7.md"
)

FIGURE_PATH = (
    ROOT
    / "figures"
    / "a10_p03_gauss_parity_audit.png"
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


def verify_signed_alignment(
    gauss_rows: list[dict[str, str]],
    signed_rows: list[dict[str, str]],
) -> None:
    """Verify that both frozen snapshots use one visit sequence."""
    unsigned = sorted(
        gauss_rows,
        key=lambda row: int(row["order"]),
    )

    signed = sorted(
        signed_rows,
        key=lambda row: int(row["order"]),
    )

    unsigned_tokens = [
        row["token"]
        for row in unsigned
    ]

    signed_unsigned_tokens = [
        row["unsigned_token"]
        for row in signed
    ]

    if unsigned_tokens != signed_unsigned_tokens:
        raise RuntimeError(
            "Signed and unsigned Gauss snapshots use "
            "different visit sequences."
        )


def write_csv(
    audit: GaussParityAudit,
) -> None:
    """Write the local derived parity table."""
    DERIVED_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    fieldnames = [
        "event_id",
        "first_order",
        "second_order",
        "first_role",
        "second_role",
        "visits_between",
        "opposite_position_parity",
        "interlacement_degree",
        "interlacement_degree_even",
        "passes_even_condition",
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

        for event in audit.events:
            writer.writerow(
                {
                    "event_id": event.event_id,
                    "first_order": (
                        event.first_order
                    ),
                    "second_order": (
                        event.second_order
                    ),
                    "first_role": (
                        event.first_role
                    ),
                    "second_role": (
                        event.second_role
                    ),
                    "visits_between": (
                        event.visits_between
                    ),
                    "opposite_position_parity": (
                        event.opposite_position_parity
                    ),
                    "interlacement_degree": (
                        event.interlacement_degree
                    ),
                    "interlacement_degree_even": (
                        event.interlacement_degree_even
                    ),
                    "passes_even_condition": (
                        event.passes_even_condition
                    ),
                }
            )

    print(
        f"Wrote {DERIVED_PATH.relative_to(ROOT)}"
    )


def plot_audit(
    audit: GaussParityAudit,
) -> None:
    """Plot visit intervals for every event."""
    figure, axis = plt.subplots(
        figsize=(14, 11),
        constrained_layout=True,
    )

    ordered_events = sorted(
        audit.events,
        key=lambda event: int(
            event.event_id[1:]
        ),
    )

    for row_index, event in enumerate(
        ordered_events
    ):
        line_style = (
            "-"
            if event.passes_even_condition
            else "--"
        )

        marker = (
            "o"
            if event.passes_even_condition
            else "x"
        )

        axis.plot(
            [
                event.first_order,
                event.second_order,
            ],
            [
                row_index,
                row_index,
            ],
            linestyle=line_style,
            linewidth=1.4,
        )

        axis.scatter(
            [
                event.first_order,
                event.second_order,
            ],
            [
                row_index,
                row_index,
            ],
            marker=marker,
            s=28,
        )

    axis.set_yticks(
        range(
            len(ordered_events)
        )
    )

    axis.set_yticklabels(
        [
            event.event_id
            for event in ordered_events
        ]
    )

    axis.set_xlim(
        0,
        audit.visit_count + 1,
    )

    axis.set_xlabel(
        "Position in frozen 62-visit Gauss word"
    )

    axis.set_ylabel(
        "Crossing event"
    )

    axis.grid(
        axis="x",
        alpha=0.2,
    )

    axis.set_title(
        "A10_P03 classical Gauss-parity audit\n"
        "solid/circle: passes; dashed/x: violates"
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
    audit: GaussParityAudit,
) -> None:
    """Write the permanent parity-audit report."""
    lines = [
        "# A10_P03 Classical Gauss-Parity Audit — v0.7",
        "",
        "## Purpose",
        "",
        "Test the frozen 62-visit A10_P03 Gauss word against the "
        "necessary even condition for a classical one-component "
        "planar knot diagram.",
        "",
        "## Necessary condition",
        "",
        "For every crossing event, the number of visits lying between "
        "its two occurrences must be even.",
        "",
        "Equivalent formulations are:",
        "",
        "- the two occurrences occupy opposite position parities;",
        "- the corresponding chord has even degree in the "
        "interlacement graph.",
        "",
        "This condition is necessary but not sufficient for classical "
        "planar realizability.",
        "",
        "## Result",
        "",
        f"- Frozen visits: **{audit.visit_count}**",
        f"- Crossing events: **{audit.event_count}**",
        f"- Events passing: **{len(audit.passing_events)}**",
        f"- Events violating: **{audit.violation_count}**",
        f"- Complete even-condition pass: "
        f"**{'yes' if audit.passes_even_condition else 'no'}**",
        "",
        "## Violating events",
        "",
        "| Event | First | Second | Between | Roles | "
        "Interlacement degree |",
        "|---|---:|---:|---:|---|---:|",
    ]

    for event in sorted(
        audit.violating_events,
        key=lambda event: int(
            event.event_id[1:]
        ),
    ):
        lines.append(
            f"| `{event.event_id}` | "
            f"{event.first_order} | "
            f"{event.second_order} | "
            f"{event.visits_between} | "
            f"`{event.first_role}/{event.second_role}` | "
            f"{event.interlacement_degree} |"
        )

    lines.extend(
        [
            "",
            "The violating event set is:",
            "",
            "```text",
            " ".join(
                event.event_id
                for event in sorted(
                    audit.violating_events,
                    key=lambda event: int(
                        event.event_id[1:]
                    ),
                )
            ),
            "```",
            "",
            "## Interpretation",
            "",
            "The current frozen sequence is therefore not eligible for "
            "direct conversion into a classical Dowker–Thistlethwaite "
            "code.",
            "",
            "This result does not determine which earlier reconstruction "
            "decision is responsible. Possible causes include:",
            "",
            "- an incorrect endpoint matching;",
            "- an incorrect local visit order;",
            "- two candidate rows representing one physical crossing;",
            "- a missed crossing;",
            "- an incorrect crossing-to-fragment assignment.",
            "",
            "The digitisation, crossing inventory, over-under review and "
            "signed sequence remain preserved as the reproducible "
            "baseline being tested.",
            "",
            "## Next computational stage",
            "",
            "Enumerate admissible endpoint matchings and constrained "
            "local-order alternatives, rebuild each candidate traversal "
            "and score it by:",
            "",
            "1. number of connected components;",
            "2. branching or unused endpoints;",
            "3. number of Gauss-parity violations;",
            "4. agreement with reviewed source evidence;",
            "5. number and cost of changed assumptions.",
            "",
            "A zero-violation result would pass this necessary condition "
            "but would still require stronger realizability tests.",
            "",
            "## Generated outputs",
            "",
            "- `data/derived/a10_p03_gauss_parity_audit.csv` "
            "(local derived table)",
            "- `figures/a10_p03_gauss_parity_audit.png`",
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
    """Run the frozen A10_P03 Gauss-parity audit."""
    gauss_rows = load_csv(
        GAUSS_PATH
    )

    signed_rows = load_csv(
        SIGNED_PATH
    )

    verify_signed_alignment(
        gauss_rows,
        signed_rows,
    )

    audit = audit_gauss_parity(
        gauss_rows
    )

    if audit.visit_count != 62:
        raise RuntimeError(
            f"Expected 62 visits; found {audit.visit_count}."
        )

    if audit.event_count != 31:
        raise RuntimeError(
            f"Expected 31 events; found {audit.event_count}."
        )

    write_csv(
        audit
    )

    plot_audit(
        audit
    )

    write_report(
        audit
    )

    print()
    print("A10_P03 Gauss-parity audit")
    print("==========================")
    print("Visits:              ", audit.visit_count)
    print("Crossing events:     ", audit.event_count)
    print(
        "Opposite-parity pairs:",
        len(audit.passing_events),
    )
    print(
        "Same-parity violations:",
        audit.violation_count,
    )
    print(
        "Classical even pass:",
        audit.passes_even_condition,
    )
    print()
    print(
        "Violating events:",
        " ".join(
            event.event_id
            for event in sorted(
                audit.violating_events,
                key=lambda event: int(
                    event.event_id[1:]
                ),
            )
        ),
    )


if __name__ == "__main__":
    main()
