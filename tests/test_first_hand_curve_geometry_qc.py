"""Boundary tests for the First Hand QC-sensitivity runner."""

from __future__ import annotations

import hashlib
import importlib.util
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

SCRIPT = (
    ROOT
    / "scripts"
    / "audit_first_hand_curve_geometry_qc.py"
)


def load_module():
    spec = importlib.util.spec_from_file_location(
        "first_hand_curve_geometry_qc_test",
        SCRIPT,
    )

    if (
        spec is None
        or spec.loader is None
    ):
        raise RuntimeError(
            "Could not load QC sensitivity module."
        )

    module = (
        importlib.util.module_from_spec(
            spec
        )
    )

    sys.modules[
        spec.name
    ] = module

    spec.loader.exec_module(
        module
    )

    return module


def test_qc_output_does_not_overwrite_primary() -> None:
    module = load_module()

    assert (
        module.OUTPUT_JSON
        != module.PRIMARY_RESULT
    )

    assert (
        "qc"
        in module.OUTPUT_JSON.parts
    )


def test_qc_pass2_is_distinct_from_raw_pass2() -> None:
    module = load_module()

    assert (
        module.QC_PASS2
        != module.RAW_PASS2
    )

    assert (
        module.QC_PASS2.name
        == "great_circle_segments_pass2_qc.csv"
    )


def test_qc_target_is_only_x1() -> None:
    module = load_module()

    assert (
        module.QC_TARGET_ID
        == "AOG-LM-P07-GC-X1"
    )


def test_checksum_verifier_accepts_synthetic_manifest(
    tmp_path: Path,
) -> None:
    module = load_module()

    payload = (
        tmp_path
        / "payload.txt"
    )

    payload.write_text(
        "synthetic\n",
        encoding="utf-8",
    )

    digest = hashlib.sha256(
        payload.read_bytes()
    ).hexdigest()

    manifest = (
        tmp_path
        / "manifest.sha256"
    )

    manifest.write_text(
        f"{digest}  payload.txt\n",
        encoding="utf-8",
    )

    result = (
        module.verify_sha256_manifest(
            manifest,
            root=tmp_path,
        )
    )

    assert result == {
        "payload.txt": digest
    }


def test_scope_boundary_is_explicit_in_source() -> None:
    source = SCRIPT.read_text(
        encoding="utf-8",
    )

    normalized = (
        source.lower()
        .replace(" ", "")
        .replace("\n", "")
    )

    for flag in (
        '"projective_map_fitted":false',
        '"projective_gauge_selected":false',
        '"spherical_scale_selected":false',
        '"great_circle_certification_issued":false',
        '"reciprocal_spiral_verdict_issued":false',
        '"s1_computed":false',
        '"s1_5_computed":false',
        '"s2_computed":false',
    ):
        assert flag in normalized


def test_direct_script_invocation_imports_from_repo_root() -> None:
    """Direct CLI execution must resolve the sibling scripts package."""
    import subprocess
    import sys

    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--help",
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, (
        result.stdout
        + "\n"
        + result.stderr
    )

    assert (
        "acquisition-QC"
        in result.stdout
    )
