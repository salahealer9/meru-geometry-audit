"""Synthetic tests for neutral X1 source-semantic review preparation."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]

SCRIPT = (
    ROOT
    / "scripts"
    / "prepare_first_hand_x1_source_semantic_review.py"
)


def load_module():
    spec = importlib.util.spec_from_file_location(
        "first_hand_x1_source_semantic_review_test",
        SCRIPT,
    )

    assert spec is not None
    assert spec.loader is not None

    module = importlib.util.module_from_spec(
        spec
    )

    sys.modules[spec.name] = module
    spec.loader.exec_module(module)

    return module


def row(
    x: float,
    y: float,
    segment: str = "S01",
    sequence: int = 0,
):
    return {
        "x_px": str(x),
        "y_px": str(y),
        "segment_id": segment,
        "sequence_index": str(sequence),
    }


def test_bounding_box_respects_padding_and_image_bounds():
    module = load_module()

    rows = [
        row(20, 30),
        row(80, 90),
    ]

    assert module.bounding_box(
        rows,
        width=100,
        height=100,
        padding=15,
    ) == (
        5,
        15,
        96,
        100,
    )


def test_grouped_segments_orders_by_sequence():
    module = load_module()

    rows = [
        row(0, 0, "S02", 2),
        row(0, 0, "S01", 3),
        row(0, 0, "S01", 1),
    ]

    groups = module.grouped_segments(
        rows
    )

    assert list(groups) == [
        "S01",
        "S02",
    ]

    assert [
        int(item["sequence_index"])
        for item in groups["S01"]
    ] == [
        1,
        3,
    ]


def test_marker_drawing_does_not_connect_points():
    module = load_module()

    image = Image.new(
        "RGB",
        (100, 100),
        "white",
    )

    rows = [
        row(20, 50, sequence=0),
        row(80, 50, sequence=1),
    ]

    module.draw_rows(
        image,
        rows,
        1,
    )

    # Midpoint must remain untouched because samples are not joined.
    assert image.getpixel(
        (50, 50)
    ) == (
        255,
        255,
        255,
    )


def test_pass_markers_are_distinct():
    module = load_module()

    a = Image.new(
        "RGB",
        (30, 30),
        "white",
    )

    b = a.copy()

    module.draw_marker(
        ImageDraw.Draw(a),
        15,
        15,
        1,
    )

    module.draw_marker(
        ImageDraw.Draw(b),
        15,
        15,
        2,
    )

    assert a.tobytes() != b.tobytes()


def test_source_contains_no_geometry_fitting_imports():
    source = SCRIPT.read_text(
        encoding="utf-8",
    )

    assert "scipy.optimize" not in source
    assert "least_squares" not in source
    assert "fit_circle(" not in source
    assert "fit_line(" not in source


def test_source_contains_no_theoretical_overlay_terms():
    source = SCRIPT.read_text(
        encoding="utf-8",
    )

    assert '"great_circle_overlay": False' in source
    assert '"scaffold_overlay": False' in source
    assert '"thirty_degree_guide": False' in source
    assert '"predicted_x1": False' in source
