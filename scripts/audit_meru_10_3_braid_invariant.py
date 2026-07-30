#!/usr/bin/env python3
"""Audit the three-strand braid and Alexander polynomial of Meru's 10_3 centreline."""

from __future__ import annotations

import csv
import hashlib
import itertools
import json
import math
import re
from pathlib import Path
from typing import Any

import numpy as np
import sympy as sp


ROOT = Path(__file__).resolve().parents[1]

MANIFEST_PATH = (
    ROOT
    / "data"
    / "source_manifests"
    / "meru_3_10_digital"
    / "official_asset_manifest.csv"
)

RAW_DIR = (
    ROOT
    / "data"
    / "source_snapshots"
    / "meru_3_10_digital"
    / "raw"
)

TARGET_URL = (
    "https://www.meru.org/compuimages/10_3.wrl"
)

EXPECTED_SHA256 = (
    "855c46cfeeb31e4394b7a4a294b397aa"
    "c4cbc14154e172a326e33243dd9e384b"
)

OUTPUT_PATH = (
    ROOT
    / "data"
    / "derived"
    / "meru_3_10_digital"
    / "meru_10_3_braid_invariant_audit.json"
)

SECTION_COUNT = 300
POINTS_PER_SECTION = 20
BRAID_STRANDS = 3
MAJOR_TURNS = 3

NUMBER_PATTERN = re.compile(
    r"[+-]?(?:(?:\d+\.\d*)|(?:\.\d+)|(?:\d+))"
    r"(?:[eE][+-]?\d+)?"
)


def sha256_path(path: Path) -> str:
    """Return a file's SHA-256 digest."""
    digest = hashlib.sha256()

    with path.open("rb") as handle:
        for block in iter(
            lambda: handle.read(1 << 20),
            b"",
        ):
            digest.update(block)

    return digest.hexdigest()


def remove_comments(text: str) -> str:
    """Remove VRML comments while preserving quoted text."""
    output: list[str] = []

    for line in text.splitlines():
        in_string = False
        escaped = False
        cut = len(line)

        for index, character in enumerate(line):
            if escaped:
                escaped = False
                continue

            if character == "\\" and in_string:
                escaped = True
                continue

            if character == '"':
                in_string = not in_string
                continue

            if character == "#" and not in_string:
                cut = index
                break

        output.append(line[:cut])

    return "\n".join(output)


def balanced_block(
    text: str,
    start: int,
) -> str:
    """Return a brace-balanced block beginning at one node."""
    opening = text.find(
        "{",
        start,
    )

    if opening < 0:
        raise RuntimeError(
            "Missing opening brace."
        )

    depth = 0
    in_string = False
    escaped = False

    for index in range(
        opening,
        len(text),
    ):
        character = text[index]

        if escaped:
            escaped = False
            continue

        if character == "\\" and in_string:
            escaped = True
            continue

        if character == '"':
            in_string = not in_string
            continue

        if in_string:
            continue

        if character == "{":
            depth += 1
        elif character == "}":
            depth -= 1

            if depth == 0:
                return text[
                    start:
                    index + 1
                ]

    raise RuntimeError(
        "Unbalanced VRML node."
    )


def first_block(
    text: str,
    node_type: str,
) -> str:
    """Return the first block of a VRML node type."""
    match = re.search(
        rf"\b{re.escape(node_type)}\s*\{{",
        text,
    )

    if match is None:
        raise RuntimeError(
            f"No {node_type} block found."
        )

    return balanced_block(
        text,
        match.start(),
    )


def first_array(
    text: str,
    field_name: str,
) -> str:
    """Return the first bracket-balanced field array."""
    match = re.search(
        rf"\b{re.escape(field_name)}\s*\[",
        text,
    )

    if match is None:
        raise RuntimeError(
            f"Missing {field_name!r} array."
        )

    opening = text.find(
        "[",
        match.start(),
    )

    depth = 0

    for index in range(
        opening,
        len(text),
    ):
        character = text[index]

        if character == "[":
            depth += 1
        elif character == "]":
            depth -= 1

            if depth == 0:
                return text[
                    opening + 1:
                    index
                ]

    raise RuntimeError(
        f"Unbalanced {field_name!r} array."
    )


def parse_vertices(text: str) -> np.ndarray:
    """Parse vertices from the first native IndexedFaceSet."""
    mesh = first_block(
        text,
        "IndexedFaceSet",
    )

    coordinate = first_block(
        mesh,
        "Coordinate",
    )

    values = np.asarray(
        [
            float(value)
            for value in NUMBER_PATTERN.findall(
                first_array(
                    coordinate,
                    "point",
                )
            )
        ],
        dtype=np.float64,
    )

    if values.size % 3:
        raise RuntimeError(
            "Coordinate count is not divisible by three."
        )

    return values.reshape(
        -1,
        3,
    )


def merge_sorted_values(
    values: list[float],
    tolerance: float,
) -> np.ndarray:
    """Merge nearly equal sorted scalar values."""
    if not values:
        return np.asarray(
            [],
            dtype=np.float64,
        )

    ordered = sorted(
        values
    )

    merged = [
        ordered[0]
    ]

    for value in ordered[1:]:
        if (
            value
            - merged[-1]
            > tolerance
        ):
            merged.append(
                value
            )
        else:
            merged[-1] = (
                merged[-1]
                + value
            ) / 2.0

    return np.asarray(
        merged,
        dtype=np.float64,
    )


def count_cycles(
    permutation: list[int],
) -> int:
    """Count cycles of a finite permutation."""
    visited = [
        False
    ] * len(
        permutation
    )

    cycle_count = 0

    for start in range(
        len(permutation)
    ):
        if visited[start]:
            continue

        cycle_count += 1
        current = start

        while not visited[current]:
            visited[current] = True
            current = permutation[current]

    return cycle_count


def cyclic_match(
    word: list[int],
    pattern: list[int],
) -> bool:
    """Return whether two equal-length words agree up to cyclic shift."""
    if len(word) != len(pattern):
        return False

    if not word:
        return True

    doubled = pattern + pattern

    return any(
        doubled[offset:offset + len(word)]
        == word
        for offset in range(
            len(pattern)
        )
    )


def normalized_laurent_polynomial(
    expression: sp.Expr,
    variable: sp.Symbol,
) -> sp.Poly:
    """Normalize a Laurent polynomial up to multiplication by a unit."""
    cancelled = sp.cancel(
        expression
    )

    numerator, denominator = sp.fraction(
        cancelled
    )

    denominator_poly = sp.Poly(
        denominator,
        variable,
        domain=sp.QQ,
    )

    denominator_terms = denominator_poly.terms()

    if len(denominator_terms) != 1:
        raise RuntimeError(
            "Alexander expression has a non-monomial denominator."
        )

    (
        denominator_exponent_tuple,
        denominator_coefficient,
    ) = denominator_terms[0]

    denominator_exponent = int(
        denominator_exponent_tuple[0]
    )

    numerator_poly = sp.Poly(
        numerator,
        variable,
        domain=sp.QQ,
    )

    numerator_exponents = [
        int(exponent_tuple[0])
        for exponent_tuple, _ in numerator_poly.terms()
    ]

    minimum_laurent_exponent = (
        min(numerator_exponents)
        - denominator_exponent
    )

    shift = max(
        0,
        -minimum_laurent_exponent,
    )

    shifted = sp.cancel(
        cancelled
        * variable ** shift
    )

    shifted_numerator, shifted_denominator = sp.fraction(
        shifted
    )

    shifted_denominator_poly = sp.Poly(
        shifted_denominator,
        variable,
        domain=sp.QQ,
    )

    shifted_denominator_terms = (
        shifted_denominator_poly.terms()
    )

    if len(shifted_denominator_terms) != 1:
        raise RuntimeError(
            "Shifted Alexander expression still has a non-monomial denominator."
        )

    (
        shifted_denominator_exponent_tuple,
        shifted_denominator_coefficient,
    ) = shifted_denominator_terms[0]

    shifted_denominator_exponent = int(
        shifted_denominator_exponent_tuple[0]
    )

    if shifted_denominator_exponent != 0:
        shifted_numerator = sp.expand(
            shifted_numerator
            * variable ** (
                -shifted_denominator_exponent
            )
        )

    rational_poly = sp.Poly(
        sp.expand(
            shifted_numerator
            / shifted_denominator_coefficient
        ),
        variable,
        domain=sp.QQ,
    )

    denominators = [
        coefficient.q
        for coefficient in rational_poly.all_coeffs()
    ]

    common_denominator = int(
        sp.ilcm(
            *denominators
        )
    )

    integer_poly = sp.Poly(
        sp.expand(
            rational_poly.as_expr()
            * common_denominator
        ),
        variable,
        domain=sp.ZZ,
    )

    coefficient_gcd = 0

    for coefficient in integer_poly.all_coeffs():
        coefficient_gcd = math.gcd(
            coefficient_gcd,
            abs(
                int(
                    coefficient
                )
            ),
        )

    if coefficient_gcd > 1:
        integer_poly = sp.Poly(
            integer_poly.as_expr()
            / coefficient_gcd,
            variable,
            domain=sp.ZZ,
        )

    if int(
        integer_poly.LC()
    ) < 0:
        integer_poly = sp.Poly(
            -integer_poly.as_expr(),
            variable,
            domain=sp.ZZ,
        )

    return integer_poly


def burau_alexander(
    word: list[int],
) -> tuple[sp.Poly, sp.Expr]:
    """Compute the Alexander polynomial from a three-braid word."""
    variable = sp.symbols(
        "t"
    )

    sigma_1 = sp.Matrix(
        [
            [
                -variable,
                1,
            ],
            [
                0,
                1,
            ],
        ]
    )

    sigma_2 = sp.Matrix(
        [
            [
                1,
                0,
            ],
            [
                variable,
                -variable,
            ],
        ]
    )

    matrix = sp.eye(
        2
    )

    for generator in word:
        base = (
            sigma_1
            if abs(
                generator
            )
            == 1
            else sigma_2
        )

        if generator < 0:
            base = base.inv()

        matrix = sp.simplify(
            matrix
            * base
        )

    expression = sp.cancel(
        (
            1
            - variable
        )
        / (
            1
            - variable ** BRAID_STRANDS
        )
        * (
            sp.eye(
                2
            )
            - matrix
        ).det()
    )

    return (
        normalized_laurent_polynomial(
            expression,
            variable,
        ),
        expression,
    )


with MANIFEST_PATH.open(
    newline="",
    encoding="utf-8",
) as handle:
    manifest_rows = list(
        csv.DictReader(
            handle
        )
    )

matches = [
    row
    for row in manifest_rows
    if row["canonical_url"] == TARGET_URL
]

if len(matches) != 1:
    raise SystemExit(
        f"Expected one manifest row for {TARGET_URL}; "
        f"found {len(matches)}."
    )

manifest = matches[0]

source_path = (
    RAW_DIR
    / manifest["snapshot_filename"]
)

source_hash = sha256_path(
    source_path
)

if source_hash != EXPECTED_SHA256:
    raise SystemExit(
        "The local 10_3.wrl SHA-256 does not match the frozen source."
    )

text = remove_comments(
    source_path.read_text(
        encoding="utf-8",
        errors="replace",
    )
)

vertices = parse_vertices(
    text
)

expected_vertices = (
    SECTION_COUNT
    * POINTS_PER_SECTION
)

if len(vertices) != expected_vertices:
    raise SystemExit(
        f"Expected {expected_vertices} vertices; found {len(vertices)}."
    )

centreline = vertices.reshape(
    SECTION_COUNT,
    POINTS_PER_SECTION,
    3,
).mean(
    axis=1
)

theta = np.unwrap(
    np.arctan2(
        centreline[:, 2],
        centreline[:, 0],
    )
)

orientation_reversed = False

if float(
    np.median(
        np.diff(
            theta
        )
    )
) < 0.0:
    centreline = centreline[::-1].copy()

    theta = np.unwrap(
        np.arctan2(
            centreline[:, 2],
            centreline[:, 0],
        )
    )

    orientation_reversed = True

theta_steps = np.diff(
    theta
)

if np.any(
    theta_steps
    <= 0.0
):
    raise SystemExit(
        "The centreline azimuth is not strictly monotone around the y-axis."
    )

period = (
    2.0
    * math.pi
    * MAJOR_TURNS
)

theta_start_native = float(
    theta[0]
)

theta_closure = (
    theta_start_native
    + period
)

if theta_closure <= float(
    theta[-1]
):
    raise SystemExit(
        "The exact three-turn closure angle does not follow the final sample."
    )

radius = np.hypot(
    centreline[:, 0],
    centreline[:, 2],
)

axial = centreline[:, 1]

theta_cycle = np.concatenate(
    (
        theta,
        np.asarray(
            [
                theta_closure
            ]
        ),
    )
)

radius_cycle = np.concatenate(
    (
        radius,
        np.asarray(
            [
                radius[0]
            ]
        ),
    )
)

axial_cycle = np.concatenate(
    (
        axial,
        np.asarray(
            [
                axial[0]
            ]
        ),
    )
)

theta_extended = np.concatenate(
    (
        theta_cycle,
        theta_cycle[1:]
        + period,
    )
)

radius_extended = np.concatenate(
    (
        radius_cycle,
        radius_cycle[1:],
    )
)

axial_extended = np.concatenate(
    (
        axial_cycle,
        axial_cycle[1:],
    )
)


def strand_values(
    phase: float,
    braid_start: float,
) -> tuple[np.ndarray, np.ndarray]:
    """Return projected and depth coordinates for all three strands."""
    targets = (
        braid_start
        + phase
        + 2.0
        * math.pi
        * np.arange(
            BRAID_STRANDS,
            dtype=np.float64,
        )
    )

    projected = np.interp(
        targets,
        theta_extended,
        axial_extended,
    )

    depth = np.interp(
        targets,
        theta_extended,
        radius_extended,
    )

    return (
        projected,
        depth,
    )


candidate_offsets = (
    np.arange(
        1440,
        dtype=np.float64,
    )
    + 0.5
) * (
    2.0
    * math.pi
    / 1440.0
)

offset_scores: list[
    tuple[float, float]
] = []

for offset in candidate_offsets:
    projected, _ = strand_values(
        0.0,
        theta_start_native
        + float(
            offset
        ),
    )

    separations = [
        abs(
            float(
                projected[first]
                - projected[second]
            )
        )
        for first, second in itertools.combinations(
            range(
                BRAID_STRANDS
            ),
            2,
        )
    ]

    offset_scores.append(
        (
            min(
                separations
            ),
            float(
                offset
            ),
        )
    )

start_margin, selected_offset = max(
    offset_scores,
    key=lambda item: (
        item[0],
        -item[1],
    ),
)

braid_start = (
    theta_start_native
    + selected_offset
)

raw_breakpoints = [
    0.0,
    2.0
    * math.pi,
]

for strand in range(
    BRAID_STRANDS
):
    for theta_value in theta_extended:
        phase = (
            float(
                theta_value
            )
            - braid_start
            - 2.0
            * math.pi
            * strand
        )

        if (
            0.0
            < phase
            < 2.0
            * math.pi
        ):
            raw_breakpoints.append(
                phase
            )

breakpoints = merge_sorted_values(
    raw_breakpoints,
    tolerance=1.0e-12,
)

if (
    abs(
        float(
            breakpoints[0]
        )
    )
    > 1.0e-12
    or abs(
        float(
            breakpoints[-1]
        )
        - 2.0
        * math.pi
    )
    > 1.0e-12
):
    raise SystemExit(
        "The braid interval endpoints are missing."
    )

breakpoint_crossing_margin = math.inf

for phase in breakpoints:
    projected, _ = strand_values(
        float(
            phase
        ),
        braid_start,
    )

    for first, second in itertools.combinations(
        range(
            BRAID_STRANDS
        ),
        2,
    ):
        breakpoint_crossing_margin = min(
            breakpoint_crossing_margin,
            abs(
                float(
                    projected[first]
                    - projected[second]
                )
            ),
        )

events: list[
    dict[str, Any]
] = []

for interval_index in range(
    len(
        breakpoints
    )
    - 1
):
    left = float(
        breakpoints[
            interval_index
        ]
    )

    right = float(
        breakpoints[
            interval_index
            + 1
        ]
    )

    projected_left, _ = strand_values(
        left,
        braid_start,
    )

    projected_right, _ = strand_values(
        right,
        braid_start,
    )

    for first, second in itertools.combinations(
        range(
            BRAID_STRANDS
        ),
        2,
    ):
        difference_left = float(
            projected_left[first]
            - projected_left[second]
        )

        difference_right = float(
            projected_right[first]
            - projected_right[second]
        )

        if (
            difference_left
            * difference_right
            >= 0.0
        ):
            continue

        root_fraction = (
            -difference_left
            / (
                difference_right
                - difference_left
            )
        )

        phase = (
            left
            + root_fraction
            * (
                right
                - left
            )
        )

        projected, depth = strand_values(
            phase,
            braid_start,
        )

        crossing_coordinate = float(
            (
                projected[first]
                + projected[second]
            )
            / 2.0
        )

        third = next(
            strand
            for strand in range(
                BRAID_STRANDS
            )
            if strand not in (
                first,
                second,
            )
        )

        depth_gap = abs(
            float(
                depth[first]
                - depth[second]
            )
        )

        third_gap = abs(
            float(
                projected[third]
                - crossing_coordinate
            )
        )

        interval_width = (
            right
            - left
        )

        epsilon = min(
            interval_width
            * 0.1,
            max(
                1.0e-10,
                min(
                    phase
                    - left,
                    right
                    - phase,
                )
                * 0.25,
            ),
        )

        before_phase = max(
            left
            + interval_width
            * 1.0e-9,
            phase
            - epsilon,
        )

        after_phase = min(
            right
            - interval_width
            * 1.0e-9,
            phase
            + epsilon,
        )

        projected_before, _ = strand_values(
            before_phase,
            braid_start,
        )

        projected_after, _ = strand_values(
            after_phase,
            braid_start,
        )

        order_before = list(
            np.argsort(
                -projected_before
            )
        )

        order_after = list(
            np.argsort(
                -projected_after
            )
        )

        position_before = {
            int(
                strand
            ): position
            for position, strand in enumerate(
                order_before
            )
        }

        position_after = {
            int(
                strand
            ): position
            for position, strand in enumerate(
                order_after
            )
        }

        if abs(
            position_before[first]
            - position_before[second]
        ) != 1:
            raise RuntimeError(
                "A crossing pair is not adjacent immediately before the event."
            )

        if abs(
            position_after[first]
            - position_after[second]
        ) != 1:
            raise RuntimeError(
                "A crossing pair is not adjacent immediately after the event."
            )

        expected_after = (
            order_before.copy()
        )

        lower_position = min(
            position_before[first],
            position_before[second],
        )

        expected_after[
            lower_position
        ], expected_after[
            lower_position
            + 1
        ] = (
            expected_after[
                lower_position
                + 1
            ],
            expected_after[
                lower_position
            ],
        )

        if expected_after != order_after:
            raise RuntimeError(
                "The projected strand order changes by more than one adjacent swap."
            )

        generator_index = (
            lower_position
            + 1
        )

        over_strand = (
            first
            if depth[first]
            > depth[second]
            else second
        )

        under_strand = (
            second
            if over_strand
            == first
            else first
        )

        exponent = (
            1
            if position_before[over_strand]
            < position_before[under_strand]
            else -1
        )

        event_to_breakpoint = min(
            phase
            - left,
            right
            - phase,
        )

        events.append(
            {
                "phase_radians": phase,
                "phase_fraction": (
                    phase
                    / (
                        2.0
                        * math.pi
                    )
                ),
                "interval_index": interval_index,
                "strand_pair": [
                    first,
                    second,
                ],
                "third_strand": third,
                "generator_index": generator_index,
                "exponent": exponent,
                "signed_generator": (
                    generator_index
                    * exponent
                ),
                "over_strand": over_strand,
                "under_strand": under_strand,
                "depth_gap": depth_gap,
                "third_strand_projection_gap": third_gap,
                "event_to_breakpoint_margin": (
                    event_to_breakpoint
                ),
                "order_before": [
                    int(
                        value
                    )
                    for value in order_before
                ],
                "order_after": [
                    int(
                        value
                    )
                    for value in order_after
                ],
            }
        )

events.sort(
    key=lambda event: event[
        "phase_radians"
    ]
)

word = [
    int(
        event[
            "signed_generator"
        ]
    )
    for event in events
]

permutation = list(
    range(
        BRAID_STRANDS
    )
)

for generator in word:
    index = (
        abs(
            generator
        )
        - 1
    )

    permutation[index], permutation[index + 1] = (
        permutation[index + 1],
        permutation[index],
    )

component_count = count_cycles(
    permutation
)

alexander_polynomial, raw_alexander_expression = (
    burau_alexander(
        word
    )
)

variable = sp.symbols(
    "t"
)

expected_torus_polynomial = (
    normalized_laurent_polynomial(
        (
            variable ** 30
            - 1
        )
        * (
            variable
            - 1
        )
        / (
            (
                variable ** 3
                - 1
            )
            * (
                variable ** 10
                - 1
            )
        ),
        variable,
    )
)

positive_pattern = [
    1,
    2,
] * 10

negative_pattern = [
    -1,
    -2,
] * 10

positive_torus_pattern = (
    cyclic_match(
        word,
        positive_pattern,
    )
    or cyclic_match(
        word,
        [
            2,
            1,
        ] * 10,
    )
)

negative_torus_pattern = (
    cyclic_match(
        word,
        negative_pattern,
    )
    or cyclic_match(
        word,
        [
            -2,
            -1,
        ] * 10,
    )
)

all_positive = bool(
    word
    and all(
        generator > 0
        for generator in word
    )
)

all_negative = bool(
    word
    and all(
        generator < 0
        for generator in word
    )
)

minimum_depth_gap = (
    min(
        float(
            event[
                "depth_gap"
            ]
        )
        for event in events
    )
    if events
    else None
)

minimum_third_gap = (
    min(
        float(
            event[
                "third_strand_projection_gap"
            ]
        )
        for event in events
    )
    if events
    else None
)

minimum_event_to_breakpoint = (
    min(
        float(
            event[
                "event_to_breakpoint_margin"
            ]
        )
        for event in events
    )
    if events
    else None
)

alexander_match = (
    alexander_polynomial
    == expected_torus_polynomial
)

determinant = abs(
    int(
        alexander_polynomial.eval(
            -1
        )
    )
)

result = {
    "source": {
        "canonical_url": TARGET_URL,
        "filename": source_path.name,
        "sha256": source_hash,
    },
    "centreline": {
        "section_count": SECTION_COUNT,
        "points_per_section": POINTS_PER_SECTION,
        "orientation_reversed_for_increasing_phase": (
            orientation_reversed
        ),
        "minimum_azimuth_step": float(
            theta_steps.min()
        ),
        "maximum_azimuth_step": float(
            theta_steps.max()
        ),
        "exact_major_turns_used_for_closure": (
            MAJOR_TURNS
        ),
    },
    "braid_projection": {
        "axis": "y",
        "phase_coordinate": "atan2(z,x)",
        "diagram_coordinate": "y",
        "depth_coordinate": "sqrt(x^2+z^2)",
        "viewer_convention": (
            "larger radial coordinate is over"
        ),
        "strand_order_convention": (
            "descending y before each crossing"
        ),
        "positive_generator_convention": (
            "the upper strand before the crossing passes over "
            "the lower strand"
        ),
        "selected_phase_offset_radians": (
            selected_offset
        ),
        "start_projection_margin": (
            start_margin
        ),
        "piecewise_linear_breakpoint_count": int(
            len(
                breakpoints
            )
        ),
        "minimum_crossing_margin_at_breakpoints": (
            breakpoint_crossing_margin
        ),
        "crossing_count": len(
            events
        ),
        "minimum_depth_gap": (
            minimum_depth_gap
        ),
        "minimum_third_strand_projection_gap": (
            minimum_third_gap
        ),
        "minimum_event_to_breakpoint_margin": (
            minimum_event_to_breakpoint
        ),
    },
    "braid": {
        "signed_word": word,
        "word_text": " ".join(
            (
                f"sigma_{abs(generator)}"
                if generator > 0
                else f"sigma_{abs(generator)}^-1"
            )
            for generator in word
        ),
        "writhe": sum(
            1
            if generator > 0
            else -1
            for generator in word
        ),
        "induced_permutation": permutation,
        "closure_component_count": (
            component_count
        ),
        "all_positive": all_positive,
        "all_negative": all_negative,
        "positive_3_10_torus_pattern_up_to_cyclic_shift": (
            positive_torus_pattern
        ),
        "negative_3_10_torus_pattern_up_to_cyclic_shift": (
            negative_torus_pattern
        ),
    },
    "alexander": {
        "raw_burau_expression": str(
            raw_alexander_expression
        ),
        "computed_polynomial": str(
            alexander_polynomial.as_expr()
        ),
        "expected_T_3_10_polynomial": str(
            expected_torus_polynomial.as_expr()
        ),
        "matches_T_3_10": (
            alexander_match
        ),
        "degree": int(
            alexander_polynomial.degree()
        ),
        "determinant_absolute_delta_minus_one": (
            determinant
        ),
    },
    "events": events,
    "scope": {
        "projection_is_piecewise_linear": True,
        "crossing_roots_enumerated_on_every_piecewise_linear_interval": (
            True
        ),
        "alexander_polynomial_distinguishes_mirror_image": (
            False
        ),
        "chirality_evidence_comes_from_signed_braid_word": (
            True
        ),
        "formal_exact_arithmetic": False,
    },
}

OUTPUT_PATH.parent.mkdir(
    parents=True,
    exist_ok=True,
)

OUTPUT_PATH.write_text(
    json.dumps(
        result,
        indent=2,
        sort_keys=True,
    )
    + "\n",
    encoding="utf-8",
)

print()
print("=" * 78)
print("MERU 10_3 BRAID / KNOT-INVARIANT PROBE")
print("=" * 78)
print(
    "Source:                         "
    f"{source_path.name}"
)
print(
    "Orientation reversed:           "
    f"{orientation_reversed}"
)
print(
    "Phase offset:                   "
    f"{selected_offset:.12g} rad"
)
print(
    "Start projection margin:        "
    f"{start_margin:.12g}"
)
print(
    "Piecewise-linear breakpoints:   "
    f"{len(breakpoints):,}"
)
print(
    "Crossings:                      "
    f"{len(events)}"
)
print(
    "Signed braid word:              "
    f"{word}"
)
print(
    "Writhe:                         "
    f"{result['braid']['writhe']}"
)
print(
    "Induced permutation:            "
    f"{permutation}"
)
print(
    "Closure components:             "
    f"{component_count}"
)
print(
    "Positive (sigma1 sigma2)^10:    "
    f"{positive_torus_pattern}"
)
print(
    "Negative inverse pattern:       "
    f"{negative_torus_pattern}"
)
print(
    "Minimum depth gap:              "
    f"{minimum_depth_gap:.12g}"
)
print(
    "Minimum third-strand gap:       "
    f"{minimum_third_gap:.12g}"
)
print(
    "Minimum event/breakpoint gap:   "
    f"{minimum_event_to_breakpoint:.12g}"
)
print(
    "Alexander polynomial:           "
    f"{alexander_polynomial.as_expr()}"
)
print(
    "Matches T(3,10):                "
    f"{alexander_match}"
)
print(
    "Alexander degree:               "
    f"{alexander_polynomial.degree()}"
)
print(
    "Determinant |Delta(-1)|:        "
    f"{determinant}"
)
print(
    f"Wrote {OUTPUT_PATH}"
)
