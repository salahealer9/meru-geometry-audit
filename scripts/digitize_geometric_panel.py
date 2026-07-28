#!/usr/bin/env python3
"""Interactively digitise colour and boundary layers from a source panel."""

from __future__ import annotations

import argparse
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backend_bases import MouseButton
from PIL import Image

from meru_geometry.digitization import (
    DEFAULT_LAYER_SPECS,
    PanelGeometry,
    load_digitization_state,
    load_panel_geometry,
    new_digitization_state,
    save_digitization_state,
)


ROOT = Path(__file__).resolve().parents[1]

PANEL_MANIFEST = (
    ROOT
    / "references"
    / "geometric_panel_crop_manifest.csv"
)

OUTPUT_ROOT = (
    ROOT
    / "data"
    / "manual_digitizations"
)

PREVIEW_ROOT = (
    ROOT
    / "data"
    / "derived"
    / "source_inspection"
    / "digitizations"
)

BACKUP_ROOT = (
    ROOT
    / "data"
    / "derived"
    / "digitization_backups"
)

LAYER_KEYS = {
    "1": "red",
    "2": "green",
    "3": "blue",
    "4": "outer_boundary",
    "5": "dimple_boundary",
    "6": "winding_landmarks",
}


def utc_now() -> str:
    """Return a second-resolution UTC timestamp."""
    return datetime.now(timezone.utc).replace(
        microsecond=0
    ).isoformat()


def point_count(state: dict[str, Any]) -> int:
    """Return the total number of digitised points."""
    return sum(
        len(segment)
        for layer in state["layers"].values()
        for segment in layer["segments"]
    )


def back_up_existing(
    panel_id: str,
    paths: tuple[Path, ...],
) -> None:
    """Copy existing digitisation files to the ignored backup directory."""
    existing = [
        path
        for path in paths
        if path.exists()
    ]

    if not existing:
        return

    stamp = datetime.now(timezone.utc).strftime(
        "%Y%m%dT%H%M%SZ"
    )

    destination_dir = BACKUP_ROOT / panel_id / stamp
    destination_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    for path in existing:
        shutil.copy2(
            path,
            destination_dir / path.name,
        )

    print(
        "Backed up existing state to "
        f"{destination_dir.relative_to(ROOT)}"
    )


class PanelDigitizer:
    """Keyboard-driven source-panel digitiser."""

    def __init__(
        self,
        panel: PanelGeometry,
        state: dict[str, Any],
        json_path: Path,
        csv_path: Path,
        preview_path: Path,
    ) -> None:
        self.panel = panel
        self.state = state
        self.json_path = json_path
        self.csv_path = csv_path
        self.preview_path = preview_path

        with Image.open(panel.local_path) as source:
            source.seek(0)
            self.image = np.asarray(
                source.convert("RGB")
            )

        self.figure, self.axis = plt.subplots(
            figsize=(12, 9)
        )

        self.initial_draw = True

        self.figure.canvas.mpl_connect(
            "button_press_event",
            self.on_click,
        )

        self.figure.canvas.mpl_connect(
            "key_press_event",
            self.on_key,
        )

        self.figure.canvas.mpl_connect(
            "close_event",
            self.on_close,
        )

        self.draw()
        self.print_help()

    @property
    def active_layer(self) -> str:
        return str(self.state["active_layer"])

    @property
    def active_segment_index(self) -> int:
        return int(
            self.state["active_segment"][
                self.active_layer
            ]
        )

    @property
    def active_segment(self) -> list[dict[str, float]]:
        return self.state["layers"][
            self.active_layer
        ]["segments"][self.active_segment_index]

    def draw(self) -> None:
        """Redraw all layers while preserving the current zoom."""
        previous_xlim = (
            self.axis.get_xlim()
            if not self.initial_draw
            else None
        )

        previous_ylim = (
            self.axis.get_ylim()
            if not self.initial_draw
            else None
        )

        self.axis.clear()

        self.axis.imshow(
            self.image,
            origin="upper",
            interpolation="nearest",
        )

        for layer_name, specification in DEFAULT_LAYER_SPECS.items():
            layer = self.state["layers"][layer_name]
            colour = str(
                specification["display_colour"]
            )
            connect = bool(specification["connect"])

            for segment_index, segment in enumerate(
                layer["segments"]
            ):
                if not segment:
                    continue

                coordinates = np.asarray(
                    [
                        [point["x"], point["y"]]
                        for point in segment
                    ],
                    dtype=np.float64,
                )

                is_active = (
                    layer_name == self.active_layer
                    and segment_index
                    == self.active_segment_index
                )

                if connect:
                    self.axis.plot(
                        coordinates[:, 0],
                        coordinates[:, 1],
                        marker="o",
                        markersize=(
                            4.5 if is_active else 3.0
                        ),
                        linewidth=(
                            2.0 if is_active else 1.2
                        ),
                        color=colour,
                        alpha=0.95,
                    )
                else:
                    self.axis.scatter(
                        coordinates[:, 0],
                        coordinates[:, 1],
                        s=(
                            42 if is_active else 28
                        ),
                        color=colour,
                        edgecolors="black",
                        linewidths=0.5,
                    )

                    for point_index, coordinate in enumerate(
                        coordinates,
                        start=1,
                    ):
                        self.axis.text(
                            coordinate[0] + 1.5,
                            coordinate[1] - 1.5,
                            str(point_index),
                            fontsize=7,
                            color=colour,
                        )

        if previous_xlim is None or previous_ylim is None:
            self.axis.set_xlim(
                -0.5,
                self.panel.width_px - 0.5,
            )
            self.axis.set_ylim(
                self.panel.height_px - 0.5,
                -0.5,
            )
        else:
            self.axis.set_xlim(previous_xlim)
            self.axis.set_ylim(previous_ylim)

        layer_label = DEFAULT_LAYER_SPECS[
            self.active_layer
        ]["label"]

        self.axis.set_title(
            f"{self.panel.panel_id} — {self.panel.title}\n"
            f"Active: {layer_label}; "
            f"segment {self.active_segment_index + 1}; "
            f"points {point_count(self.state)}"
        )

        self.axis.set_xlabel(
            "Panel x coordinate (pixels)"
        )
        self.axis.set_ylabel(
            "Panel y coordinate (pixels)"
        )

        self.initial_draw = False
        self.figure.canvas.draw_idle()

    def save(self) -> None:
        """Save state, flat coordinates, and a local overlay preview."""
        self.state["updated_utc"] = utc_now()

        save_digitization_state(
            self.state,
            self.panel,
            self.json_path,
            self.csv_path,
        )

        self.preview_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.figure.savefig(
            self.preview_path,
            dpi=180,
            bbox_inches="tight",
        )

        print(
            f"Saved {point_count(self.state)} points to "
            f"{self.json_path.relative_to(ROOT)}"
        )

    def add_point(
        self,
        x: float,
        y: float,
    ) -> None:
        """Append a point to the active layer and segment."""
        point = {
            "x": round(float(x), 4),
            "y": round(float(y), 4),
        }

        self.active_segment.append(point)
        self.save()
        self.draw()

    def undo(self) -> None:
        """Remove the last point in the active segment."""
        if self.active_segment:
            removed = self.active_segment.pop()
            print(
                f"Removed ({removed['x']}, {removed['y']})"
            )
            self.save()
            self.draw()
            return

        if self.active_segment_index > 0:
            segments = self.state["layers"][
                self.active_layer
            ]["segments"]

            segments.pop(self.active_segment_index)

            self.state["active_segment"][
                self.active_layer
            ] = self.active_segment_index - 1

            print("Removed empty segment")
            self.save()
            self.draw()
            return

        print("Nothing to undo in the active segment")

    def new_segment(self) -> None:
        """Start a new disconnected segment in the active layer."""
        if not self.active_segment:
            print("Current segment is already empty")
            return

        segments = self.state["layers"][
            self.active_layer
        ]["segments"]

        segments.append([])

        self.state["active_segment"][
            self.active_layer
        ] = len(segments) - 1

        self.save()
        self.draw()

        print(
            f"Started segment {len(segments)} "
            f"for {self.active_layer}"
        )

    def change_segment(self, step: int) -> None:
        """Move to another segment within the active layer."""
        segments = self.state["layers"][
            self.active_layer
        ]["segments"]

        current = self.active_segment_index
        requested = current + step

        if not 0 <= requested < len(segments):
            print("No segment in that direction")
            return

        self.state["active_segment"][
            self.active_layer
        ] = requested

        self.save()
        self.draw()

    def switch_layer(self, layer_name: str) -> None:
        """Switch the active tracing layer."""
        self.state["active_layer"] = layer_name
        self.save()
        self.draw()

        print(
            "Active layer:",
            DEFAULT_LAYER_SPECS[layer_name]["label"],
        )

    def on_click(self, event: Any) -> None:
        """Handle point entry and right-click undo."""
        if event.inaxes is not self.axis:
            return

        toolbar = getattr(
            self.figure.canvas,
            "toolbar",
            None,
        )

        if (
            toolbar is not None
            and getattr(toolbar, "mode", "")
        ):
            return

        if event.button == MouseButton.RIGHT:
            self.undo()
            return

        if event.button != MouseButton.LEFT:
            return

        if event.xdata is None or event.ydata is None:
            return

        if not (
            0.0 <= event.xdata < self.panel.width_px
            and 0.0 <= event.ydata < self.panel.height_px
        ):
            return

        self.add_point(
            event.xdata,
            event.ydata,
        )

    def on_key(self, event: Any) -> None:
        """Handle keyboard layer and editing controls."""
        key = event.key

        if key in LAYER_KEYS:
            self.switch_layer(
                LAYER_KEYS[key]
            )
        elif key in {"u", "backspace"}:
            self.undo()
        elif key == "n":
            self.new_segment()
        elif key == "[":
            self.change_segment(-1)
        elif key == "]":
            self.change_segment(1)
        elif key == "s":
            self.save()
        elif key == "h":
            self.print_help()
        elif key == "q":
            self.save()
            plt.close(self.figure)

    def on_close(self, _event: Any) -> None:
        """Autosave when the graphical window closes."""
        self.save()

    @staticmethod
    def print_help() -> None:
        """Print keyboard controls."""
        print(
            """
Digitiser controls
-------------------
Left click       add point
Right click      undo last point in active segment
1                red centreline
2                green centreline
3                blue centreline
4                outer boundary
5                dimple boundary
6                winding landmarks
n                start a new disconnected segment
[ / ]            previous / next segment
u or Backspace   undo
s                save
h                print controls
q                save and quit

Use the Matplotlib toolbar to zoom or pan. Points are not added while
zoom or pan mode is active.
""".strip()
        )


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=__doc__,
    )

    parser.add_argument(
        "--panel-id",
        default="A10_P03",
        help="Panel identifier from the crop manifest.",
    )

    parser.add_argument(
        "--new",
        action="store_true",
        help=(
            "Start a new state after backing up any existing "
            "digitisation."
        ),
    )

    return parser.parse_args()


def main() -> None:
    """Launch the interactive digitiser."""
    arguments = parse_arguments()

    panel = load_panel_geometry(
        PANEL_MANIFEST,
        arguments.panel_id,
        repository_root=ROOT,
    )

    if not panel.local_path.exists():
        raise SystemExit(
            "Panel crop not found. Run "
            "scripts/build_geometric_panel_crops.py first."
        )

    output_dir = OUTPUT_ROOT / panel.panel_id
    json_path = output_dir / "digitization.json"
    csv_path = output_dir / "digitization.csv"

    preview_path = (
        PREVIEW_ROOT
        / f"{panel.panel_id}_overlay.png"
    )

    if arguments.new:
        back_up_existing(
            panel.panel_id,
            (json_path, csv_path),
        )

        state = new_digitization_state(
            panel,
            utc_now(),
        )
    elif json_path.exists():
        state = load_digitization_state(
            json_path,
            panel,
        )

        print(
            f"Loaded {point_count(state)} existing points from "
            f"{json_path.relative_to(ROOT)}"
        )
    else:
        state = new_digitization_state(
            panel,
            utc_now(),
        )

    digitizer = PanelDigitizer(
        panel=panel,
        state=state,
        json_path=json_path,
        csv_path=csv_path,
        preview_path=preview_path,
    )

    digitizer.save()
    plt.show()


if __name__ == "__main__":
    main()
