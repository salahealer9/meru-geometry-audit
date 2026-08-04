"""Tests for the preregistered First Hand curve-geometry analysis."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

PROTOCOL_PATH = (
    ROOT
    / "docs"
    / "first_hand_curve_geometry_protocol.md"
)


def protocol_text() -> str:
    """Return whitespace-normalized lowercase protocol text."""
    return " ".join(
        PROTOCOL_PATH.read_text(
            encoding="utf-8",
        )
        .lower()
        .split()
    )


def test_protocol_freezes_equal_pass_weighting() -> None:
    """Unequal click density must not alter pass weight."""
    text = protocol_text()

    assert "weight(pass 1) = 0.5" in text
    assert "weight(pass 2) = 0.5" in text
    assert "raw click count is not an evidential weight" in text
    assert "proportional to visible polyline arc length" in text


def test_protocol_preserves_segment_occlusions() -> None:
    """Visible fragments may not be bridged observationally."""
    text = protocol_text()

    assert "observed polyline itself is never bridged" in text
    assert "filled nodes" in text
    assert "spiral occlusions" in text
    assert "ambiguous crossings" in text


def test_protocol_does_not_force_segment_correspondence() -> None:
    """Independent passes must not gain artificial correspondence."""
    text = protocol_text()

    assert (
        "does not require s01 in one pass to match s01 in the other"
        in text
    )
    assert (
        "may not be imposed to improve agreement"
        in text
    )


def test_protocol_freezes_agreement_statistics() -> None:
    """Agreement metrics must be fixed before coordinates are analysed."""
    text = protocol_text()

    assert "pass 1 -> pass 2" in text
    assert "pass 2 -> pass 1" in text
    assert "median" in text
    assert "rms" in text
    assert "95th percentile" in text
    assert "maximum" in text
    assert "median nearest-curve disagreement > 12 px" in text


def test_protocol_freezes_resampling_sensitivity() -> None:
    """Click density must be removed by arc-length resampling."""
    text = protocol_text()

    assert "2 px" in text
    assert "1 px" in text
    assert "4 px" in text
    assert "uniformly in image-space arc length" in text


def test_protocol_keeps_scaffold_as_holdout() -> None:
    """The unlabelled scaffold curve cannot calibrate the map."""
    text = protocol_text()

    assert (
        "aog-lm-p07-gc-scaffold-ur-uc-x1ll-ll"
        in text
    )
    assert "independent holdout" in text
    assert (
        "must not be used to select a projective map"
        in text
    )


def test_protocol_is_pre_projective_and_pre_self_embedment() -> None:
    """This checkpoint must stay model-neutral."""
    text = protocol_text()

    assert "great-circle certification" in text
    assert "no self-embedment quantity may enter this stage" in text

    assert "it must not produce:" in text
    assert "a preferred historical projection formula" in text
    assert "s1;" in text
    assert "s1.5;" in text
    assert "s2." in text


def test_protocol_preserves_hand_drawn_boundary() -> None:
    """Image-space residuals must respect source drafting uncertainty."""
    text = protocol_text()

    assert "page-7 source is a hand drawing" in text
    assert "cannot certify exact mathematical incidence" in text


def test_limb_dewarp_is_secondary_and_frozen() -> None:
    """Internal curves may not determine their own image dewarp."""
    text = protocol_text()

    assert (
        "primary analysis is performed in raw prepared-crop coordinates"
        in text
    )
    assert "secondary sensitivity analysis" in text
    assert (
        "transform must not be re-estimated from the five internal curves"
        in text
    )
