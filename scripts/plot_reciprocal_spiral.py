"""Plot the baseline reciprocal spiral."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt

from meru_geometry.reciprocal_spiral import reciprocal_spiral


OUTPUT_PATH = Path("figures/reciprocal_spiral_baseline.png")


def main() -> None:
    """Generate and save the baseline reciprocal-spiral figure."""
    points = reciprocal_spiral()

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(7, 7))
    ax.plot(points[:, 0], points[:, 1])
    ax.set_aspect("equal")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title(r"Baseline reciprocal spiral: $r = 1/\theta$")
    ax.grid(True, alpha=0.25)

    fig.tight_layout()
    fig.savefig(OUTPUT_PATH, dpi=200)
    plt.close(fig)

    print(f"Wrote {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
