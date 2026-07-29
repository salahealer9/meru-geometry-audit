#!/usr/bin/env python3
"""Search all reversals of reviewed A10_P03 local visit orders."""

from __future__ import annotations

import csv
from pathlib import Path

from meru_geometry.gauss_order_sensitivity import (
    OrderSensitivityResult,
    enumerate_reviewed_order_sensitivity,
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

REVIEW_PATH = (
    DATA_DIR
    / "gauss_order_review.csv"
)

DERIVED_PATH = (
    ROOT
    / "data"
    / "derived"
    / "a10_p03_reviewed_order_sensitivity.csv"
)

REPORT_PATH = (
    ROOT
    / "docs"
    / "geometry"
    / "a10_p03_reviewed_order_sensitivity_v0_7.md"
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


def write_csv(
    results: tuple[
        OrderSensitivityResult,
        ...,
    ],
) -> None:
    """Write the local exhaustive result table."""
    DERIVED_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    fieldnames = [
        "rank",
        "candidate_id",
        "is_frozen_baseline",
        "reversed_review_count",
        "reversed_review_ids",
        "parity_violation_count",
        "passes_even_condition",
        "violating_events",
        "visit_tokens",
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
                    "candidate_id": (
                        result.candidate_id
                    ),
                    "is_frozen_baseline": (
                        not result.reversed_review_ids
                    ),
                    "reversed_review_count": (
                        result.reversed_review_count
                    ),
                    "reversed_review_ids": " ".join(
                        result.reversed_review_ids
                    ),
                    "parity_violation_count": (
                        result.violation_count
                    ),
                    "passes_even_condition": (
                        result.passes_even_condition
                    ),
                    "violating_events": " ".join(
                        result.violation_event_ids
                    ),
                    "visit_tokens": " ".join(
                        result.visit_tokens
                    ),
                }
            )

    print(
        f"Wrote {DERIVED_PATH.relative_to(ROOT)}"
    )


def write_report(
    results: tuple[
        OrderSensitivityResult,
        ...,
    ],
) -> None:
    """Write the permanent sensitivity report."""
    baseline = next(
        result
        for result in results
        if not result.reversed_review_ids
    )

    minimum = min(
        result.violation_count
        for result in results
    )

    best = tuple(
        result
        for result in results
        if result.violation_count
        == minimum
    )

    zero_candidates = tuple(
        result
        for result in results
        if result.passes_even_condition
    )

    lines = [
        "# A10_P03 Reviewed Local-Order Sensitivity — v0.7",
        "",
        "## Purpose",
        "",
        "Test every reversal subset of the four accepted local "
        "Gauss-order decisions.",
        "",
        "This is a diagnostic sensitivity analysis. Reversing a pair "
        "does not replace or weaken its source review.",
        "",
        "## Search space",
        "",
        "- Accepted order decisions: **4**",
        f"- Reversal combinations: **{len(results)}**",
        "- Frozen snapshots modified: **no**",
        "",
        "## Result",
        "",
        f"- Frozen-baseline violations: "
        f"**{baseline.violation_count}**",
        f"- Minimum violations: **{minimum}**",
        f"- Candidates attaining the minimum: **{len(best)}**",
        f"- Zero-violation candidates: **{len(zero_candidates)}**",
        "",
        "## Exhaustive table",
        "",
        "| Rank | Candidate | Baseline | Reversed reviews | "
        "Violations | Even pass |",
        "|---:|---|---|---:|---:|---|",
    ]

    for rank, result in enumerate(
        results,
        start=1,
    ):
        lines.append(
            f"| {rank} | `{result.candidate_id}` | "
            f"{'yes' if not result.reversed_review_ids else 'no'} | "
            f"{result.reversed_review_count} | "
            f"{result.violation_count} | "
            f"{'yes' if result.passes_even_condition else 'no'} |"
        )

    lines.extend(
        [
            "",
            "## Best hypothetical result",
            "",
        ]
    )

    for result in best:
        lines.extend(
            [
                f"### {result.candidate_id}",
                "",
                "- Reversed accepted reviews:",
                "",
            ]
        )

        for review_id in result.reversed_review_ids:
            lines.append(
                f"  - `{review_id}`"
            )

        lines.extend(
            [
                "",
                "- Remaining violations:",
                "",
                "```text",
                " ".join(
                    result.violation_event_ids
                ),
                "```",
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
                "At least one hypothetical reversal combination passes "
                "the necessary even condition.",
                "",
                "Its reversed source decisions would require targeted "
                "manual reinspection before any reconstruction change.",
            ]
        )
    else:
        lines.extend(
            [
                "No combination of the four reviewed local-order "
                "reversals removes the parity failure.",
                "",
                "Therefore these local order decisions cannot, by "
                "themselves, explain the non-classical Gauss parity.",
                "",
                "The best hypothetical result still contradicts accepted "
                "high-confidence source reviews and retains unresolved "
                "parity violations.",
            ]
        )

    lines.extend(
        [
            "",
            "The next expansion should therefore examine same-colour "
            "continuation alternatives and crossing-inventory structure, "
            "rather than revisiting these four decisions in isolation.",
            "",
            "## Generated output",
            "",
            "- `data/derived/"
            "a10_p03_reviewed_order_sensitivity.csv` "
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
    """Run the complete reviewed-order sensitivity search."""
    results = (
        enumerate_reviewed_order_sensitivity(
            load_csv(
                GAUSS_PATH
            ),
            load_csv(
                REVIEW_PATH
            ),
        )
    )

    if len(results) != 16:
        raise RuntimeError(
            f"Expected 16 reversal combinations; found {len(results)}."
        )

    write_csv(
        results
    )

    write_report(
        results
    )

    baseline = next(
        result
        for result in results
        if not result.reversed_review_ids
    )

    minimum = min(
        result.violation_count
        for result in results
    )

    best = [
        result
        for result in results
        if result.violation_count
        == minimum
    ]

    print()
    print("A10_P03 reviewed-order sensitivity")
    print("==================================")
    print("Candidates:          ", len(results))
    print(
        "Baseline violations:",
        baseline.violation_count,
    )
    print("Minimum violations: ", minimum)
    print("Best candidates:    ", len(best))
    print()

    for result in best:
        print(
            f"{result.candidate_id}: "
            f"reverse "
            + (
                ", ".join(
                    result.reversed_review_ids
                )
                or "none"
            )
        )

        print(
            "Remaining:",
            " ".join(
                result.violation_event_ids
            ),
        )


if __name__ == "__main__":
    main()
