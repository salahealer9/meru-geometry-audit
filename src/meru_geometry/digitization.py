"""Data structures and persistence for manual source-image digitisation."""

from __future__ import annotations

import csv
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np


SCHEMA_VERSION = "1.0"

DEFAULT_LAYER_SPECS: dict[str, dict[str, object]] = {
    "red": {
        "label": "Red centreline",
        "closed": False,
        "connect": True,
        "display_colour": "tab:red",
    },
    "green": {
        "label": "Green centreline",
        "closed": False,
        "connect": True,
        "display_colour": "tab:green",
    },
    "blue": {
        "label": "Blue centreline",
        "closed": False,
        "connect": True,
        "display_colour": "tab:blue",
    },
    "outer_boundary": {
        "label": "Outer dimpled-sphere boundary",
        "closed": True,
        "connect": True,
        "display_colour": "magenta",
    },
    "dimple_boundary": {
        "label": "Central dimple boundary",
        "closed": True,
        "connect": True,
        "display_colour": "cyan",
    },
    "winding_landmarks": {
        "label": "Numbered or winding landmarks",
        "closed": False,
        "connect": False,
        "display_colour": "gold",
    },
}


@dataclass(frozen=True)
class PanelGeometry:
    """Geometry and provenance of a cropped source panel."""

    panel_id: str
    asset_id: str
    title: str
    source_sha256: str
    crop_sha256: str
    x0: int
    y0: int
    x1: int
    y1: int
    width_px: int
    height_px: int
    local_path: Path


def load_panel_geometry(
    manifest_path: Path,
    panel_id: str,
    repository_root: Path | None = None,
) -> PanelGeometry:
    """Load one panel definition from the crop manifest."""
    manifest = Path(manifest_path)

    if repository_root is None:
        repository_root = manifest.resolve().parents[1]

    with manifest.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))

    matching = [
        row
        for row in rows
        if row["panel_id"] == panel_id
    ]

    if len(matching) != 1:
        raise ValueError(
            f"Expected exactly one manifest row for {panel_id}, "
            f"found {len(matching)}."
        )

    row = matching[0]

    panel = PanelGeometry(
        panel_id=row["panel_id"],
        asset_id=row["asset_id"],
        title=row["title"],
        source_sha256=row["source_sha256"],
        crop_sha256=row["sha256"],
        x0=int(row["x0"]),
        y0=int(row["y0"]),
        x1=int(row["x1"]),
        y1=int(row["y1"]),
        width_px=int(row["width_px"]),
        height_px=int(row["height_px"]),
        local_path=repository_root / row["local_path"],
    )

    if panel.x1 - panel.x0 != panel.width_px:
        raise ValueError("Panel width is inconsistent with crop bounds.")

    if panel.y1 - panel.y0 != panel.height_px:
        raise ValueError("Panel height is inconsistent with crop bounds.")

    return panel


def panel_to_source_coordinates(
    x: float,
    y: float,
    panel: PanelGeometry,
) -> tuple[float, float]:
    """Convert crop-panel coordinates to original source-image coordinates."""
    return panel.x0 + float(x), panel.y0 + float(y)


def source_to_panel_coordinates(
    x: float,
    y: float,
    panel: PanelGeometry,
) -> tuple[float, float]:
    """Convert original source-image coordinates to crop-panel coordinates."""
    return float(x) - panel.x0, float(y) - panel.y0


def new_digitization_state(
    panel: PanelGeometry,
    created_utc: str,
) -> dict[str, Any]:
    """Create an empty digitisation state for a panel."""
    layers: dict[str, dict[str, Any]] = {}

    for name, specification in DEFAULT_LAYER_SPECS.items():
        layers[name] = {
            "label": specification["label"],
            "closed": specification["closed"],
            "connect": specification["connect"],
            "segments": [[]],
        }

    return {
        "schema_version": SCHEMA_VERSION,
        "panel_id": panel.panel_id,
        "asset_id": panel.asset_id,
        "panel_title": panel.title,
        "source_sha256": panel.source_sha256,
        "crop_sha256": panel.crop_sha256,
        "crop_bounds": {
            "x0": panel.x0,
            "y0": panel.y0,
            "x1": panel.x1,
            "y1": panel.y1,
        },
        "panel_dimensions": {
            "width_px": panel.width_px,
            "height_px": panel.height_px,
        },
        "coordinate_convention": (
            "Pixel-centre coordinates; origin at panel upper-left; "
            "x increases rightward and y increases downward."
        ),
        "created_utc": created_utc,
        "updated_utc": created_utc,
        "active_layer": "red",
        "active_segment": {
            name: 0
            for name in DEFAULT_LAYER_SPECS
        },
        "layers": layers,
    }


def validate_digitization_state(
    state: dict[str, Any],
    panel: PanelGeometry,
) -> None:
    """Validate a digitisation state against its panel."""
    if state.get("schema_version") != SCHEMA_VERSION:
        raise ValueError("Unsupported digitisation schema version.")

    if state.get("panel_id") != panel.panel_id:
        raise ValueError("Digitisation panel ID does not match.")

    if state.get("asset_id") != panel.asset_id:
        raise ValueError("Digitisation asset ID does not match.")

    layers = state.get("layers")

    if not isinstance(layers, dict):
        raise ValueError("Digitisation layers must be a mapping.")

    if set(layers) != set(DEFAULT_LAYER_SPECS):
        raise ValueError("Digitisation layer set is incomplete.")

    active_segments = state.get("active_segment")

    if not isinstance(active_segments, dict):
        raise ValueError("active_segment must be a mapping.")

    for layer_name in DEFAULT_LAYER_SPECS:
        layer = layers[layer_name]
        segments = layer.get("segments")

        if not isinstance(segments, list) or not segments:
            raise ValueError(
                f"{layer_name}: segments must be a non-empty list."
            )

        active_index = active_segments.get(layer_name)

        if (
            not isinstance(active_index, int)
            or not 0 <= active_index < len(segments)
        ):
            raise ValueError(
                f"{layer_name}: invalid active segment index."
            )

        for segment_index, segment in enumerate(segments):
            if not isinstance(segment, list):
                raise ValueError(
                    f"{layer_name}/{segment_index}: segment must be a list."
                )

            for point_index, point in enumerate(segment):
                if not isinstance(point, dict):
                    raise ValueError(
                        f"{layer_name}/{segment_index}/{point_index}: "
                        "point must be a mapping."
                    )

                x = float(point["x"])
                y = float(point["y"])

                if not np.isfinite([x, y]).all():
                    raise ValueError("Digitised coordinates must be finite.")

                if not 0.0 <= x < panel.width_px:
                    raise ValueError(
                        f"Panel x coordinate {x} lies outside the crop."
                    )

                if not 0.0 <= y < panel.height_px:
                    raise ValueError(
                        f"Panel y coordinate {y} lies outside the crop."
                    )


def flatten_digitization_state(
    state: dict[str, Any],
    panel: PanelGeometry,
) -> list[dict[str, object]]:
    """Flatten digitisation segments into tabular point records."""
    validate_digitization_state(state, panel)

    rows: list[dict[str, object]] = []

    for layer_name, specification in DEFAULT_LAYER_SPECS.items():
        layer = state["layers"][layer_name]

        for segment_index, segment in enumerate(layer["segments"]):
            for point_index, point in enumerate(segment):
                panel_x = float(point["x"])
                panel_y = float(point["y"])

                source_x, source_y = panel_to_source_coordinates(
                    panel_x,
                    panel_y,
                    panel,
                )

                rows.append(
                    {
                        "panel_id": panel.panel_id,
                        "asset_id": panel.asset_id,
                        "layer": layer_name,
                        "layer_label": specification["label"],
                        "segment_id": segment_index,
                        "point_index": point_index,
                        "panel_x": panel_x,
                        "panel_y": panel_y,
                        "source_x": source_x,
                        "source_y": source_y,
                        "closed_layer": specification["closed"],
                        "connected_layer": specification["connect"],
                    }
                )

    return rows


def save_digitization_state(
    state: dict[str, Any],
    panel: PanelGeometry,
    json_path: Path,
    csv_path: Path,
) -> None:
    """Atomically save JSON state and flattened CSV coordinates."""
    validate_digitization_state(state, panel)

    json_path.parent.mkdir(parents=True, exist_ok=True)
    csv_path.parent.mkdir(parents=True, exist_ok=True)

    temporary_json = json_path.with_suffix(".json.tmp")
    temporary_json.write_text(
        json.dumps(
            state,
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    temporary_json.replace(json_path)

    rows = flatten_digitization_state(state, panel)

    fieldnames = [
        "panel_id",
        "asset_id",
        "layer",
        "layer_label",
        "segment_id",
        "point_index",
        "panel_x",
        "panel_y",
        "source_x",
        "source_y",
        "closed_layer",
        "connected_layer",
    ]

    temporary_csv = csv_path.with_suffix(".csv.tmp")

    with temporary_csv.open(
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
        writer.writerows(rows)

    temporary_csv.replace(csv_path)


def load_digitization_state(
    json_path: Path,
    panel: PanelGeometry,
) -> dict[str, Any]:
    """Load and validate an existing digitisation state."""
    state = json.loads(
        json_path.read_text(encoding="utf-8")
    )

    validate_digitization_state(state, panel)
    return state
