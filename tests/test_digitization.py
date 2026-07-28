"""Tests for source-panel digitisation persistence."""

from __future__ import annotations

from pathlib import Path

import pytest

from meru_geometry.digitization import (
    DEFAULT_LAYER_SPECS,
    PanelGeometry,
    flatten_digitization_state,
    load_digitization_state,
    new_digitization_state,
    panel_to_source_coordinates,
    save_digitization_state,
    source_to_panel_coordinates,
    validate_digitization_state,
)


@pytest.fixture
def panel(tmp_path: Path) -> PanelGeometry:
    return PanelGeometry(
        panel_id="A10_P03",
        asset_id="A10",
        title="Test panel",
        source_sha256="source-digest",
        crop_sha256="crop-digest",
        x0=385,
        y0=355,
        x1=575,
        y1=520,
        width_px=190,
        height_px=165,
        local_path=tmp_path / "panel.png",
    )


def test_coordinate_round_trip(
    panel: PanelGeometry,
) -> None:
    source = panel_to_source_coordinates(
        12.5,
        34.25,
        panel,
    )

    assert source == pytest.approx(
        (397.5, 389.25)
    )

    recovered = source_to_panel_coordinates(
        *source,
        panel,
    )

    assert recovered == pytest.approx(
        (12.5, 34.25)
    )


def test_new_state_contains_all_layers(
    panel: PanelGeometry,
) -> None:
    state = new_digitization_state(
        panel,
        "2026-07-26T14:00:00+00:00",
    )

    assert set(state["layers"]) == set(
        DEFAULT_LAYER_SPECS
    )

    validate_digitization_state(state, panel)


def test_flattening_preserves_segments_and_offsets(
    panel: PanelGeometry,
) -> None:
    state = new_digitization_state(
        panel,
        "2026-07-26T14:00:00+00:00",
    )

    state["layers"]["red"]["segments"][0] = [
        {"x": 10.0, "y": 20.0},
        {"x": 15.5, "y": 25.25},
    ]

    state["layers"]["red"]["segments"].append(
        [{"x": 30.0, "y": 40.0}]
    )

    state["active_segment"]["red"] = 1

    rows = flatten_digitization_state(
        state,
        panel,
    )

    red_rows = [
        row
        for row in rows
        if row["layer"] == "red"
    ]

    assert len(red_rows) == 3
    assert red_rows[2]["segment_id"] == 1
    assert red_rows[2]["source_x"] == pytest.approx(415.0)
    assert red_rows[2]["source_y"] == pytest.approx(395.0)


def test_save_and_load_round_trip(
    panel: PanelGeometry,
    tmp_path: Path,
) -> None:
    state = new_digitization_state(
        panel,
        "2026-07-26T14:00:00+00:00",
    )

    state["layers"]["blue"]["segments"][0] = [
        {"x": 22.0, "y": 33.0}
    ]

    json_path = tmp_path / "digitization.json"
    csv_path = tmp_path / "digitization.csv"

    save_digitization_state(
        state,
        panel,
        json_path,
        csv_path,
    )

    loaded = load_digitization_state(
        json_path,
        panel,
    )

    assert loaded == state
    assert csv_path.exists()
    assert "source_x" in csv_path.read_text(
        encoding="utf-8"
    )


def test_out_of_bounds_point_is_rejected(
    panel: PanelGeometry,
) -> None:
    state = new_digitization_state(
        panel,
        "2026-07-26T14:00:00+00:00",
    )

    state["layers"]["green"]["segments"][0] = [
        {"x": 190.0, "y": 20.0}
    ]

    with pytest.raises(
        ValueError,
        match="outside the crop",
    ):
        validate_digitization_state(
            state,
            panel,
        )
