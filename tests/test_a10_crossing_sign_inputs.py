"""Integration checks for A10_P03 crossing-sign inputs."""

from __future__ import annotations

import importlib.util
from pathlib import Path
from types import ModuleType


ROOT = Path(__file__).resolve().parents[1]

SCRIPT_PATH = (
    ROOT
    / "scripts"
    / "derive_a10_p03_crossing_signs.py"
)


def load_sign_script() -> ModuleType:
    """Load the sign-census script as a testable module."""
    specification = (
        importlib.util.spec_from_file_location(
            "derive_a10_p03_crossing_signs",
            SCRIPT_PATH,
        )
    )

    if (
        specification is None
        or specification.loader is None
    ):
        raise RuntimeError(
            "Could not load the crossing-sign census script."
        )

    module = importlib.util.module_from_spec(
        specification
    )

    specification.loader.exec_module(
        module
    )

    return module


def test_all_digitized_segments_have_frozen_directions() -> None:
    """The direction map must not depend on crossing visits."""
    module = load_sign_script()

    segments = module.load_segments()

    directions = (
        module.load_traversal_directions(
            segments
        )
    )

    assert len(segments) == 24
    assert len(directions) == 24
    assert set(directions) == set(segments)
