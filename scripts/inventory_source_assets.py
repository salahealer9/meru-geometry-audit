#!/usr/bin/env python3
"""Inventory image and document assets linked from local source snapshots."""

from __future__ import annotations

import csv
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlparse


ROOT = Path(__file__).resolve().parents[1]
SNAPSHOT_MANIFEST = ROOT / "references" / "source_snapshot_manifest.csv"
OUTPUT_PATH = ROOT / "references" / "source_asset_inventory.csv"

ASSET_SUFFIXES = {
    ".gif",
    ".jpg",
    ".jpeg",
    ".png",
    ".webp",
    ".pdf",
    ".svg",
    ".wrl",
    ".vrml",
    ".mov",
    ".mp4",
}


class AssetParser(HTMLParser):
    """Collect linked images and other candidate research assets."""

    def __init__(self, base_url: str) -> None:
        super().__init__()
        self.base_url = base_url
        self.assets: list[dict[str, str]] = []

    def handle_starttag(
        self,
        tag: str,
        attrs: list[tuple[str, str | None]],
    ) -> None:
        attributes = dict(attrs)

        if tag.lower() == "img" and attributes.get("src"):
            raw_url = attributes["src"]
            assert raw_url is not None

            self.assets.append(
                {
                    "tag": "img",
                    "raw_url": raw_url,
                    "absolute_url": urljoin(self.base_url, raw_url),
                    "description": attributes.get("alt") or "",
                }
            )

        if tag.lower() == "a" and attributes.get("href"):
            raw_url = attributes["href"]
            assert raw_url is not None

            absolute_url = urljoin(self.base_url, raw_url)
            suffix = Path(urlparse(absolute_url).path).suffix.lower()

            if suffix in ASSET_SUFFIXES:
                self.assets.append(
                    {
                        "tag": "a",
                        "raw_url": raw_url,
                        "absolute_url": absolute_url,
                        "description": attributes.get("title") or "",
                    }
                )


def main() -> None:
    """Parse every downloaded HTML source and inventory its assets."""
    with SNAPSHOT_MANIFEST.open(newline="", encoding="utf-8") as handle:
        snapshots = list(csv.DictReader(handle))

    rows: list[dict[str, str]] = []
    seen: set[tuple[str, str, str]] = set()

    for snapshot in snapshots:
        local_path = ROOT / snapshot["local_path"]

        if local_path.suffix.lower() not in {".html", ".htm"}:
            continue

        parser = AssetParser(snapshot["final_url"])
        parser.feed(local_path.read_text(encoding="utf-8", errors="replace"))

        for asset in parser.assets:
            key = (
                snapshot["source_id"],
                asset["tag"],
                asset["absolute_url"],
            )

            if key in seen:
                continue

            seen.add(key)

            rows.append(
                {
                    "source_id": snapshot["source_id"],
                    "source_title": snapshot["title"],
                    "tag": asset["tag"],
                    "description": asset["description"],
                    "raw_url": asset["raw_url"],
                    "absolute_url": asset["absolute_url"],
                }
            )

    rows.sort(
        key=lambda row: (
            row["source_id"],
            row["absolute_url"],
            row["tag"],
        )
    )

    fieldnames = [
        "source_id",
        "source_title",
        "tag",
        "description",
        "raw_url",
        "absolute_url",
    ]

    with OUTPUT_PATH.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {OUTPUT_PATH.relative_to(ROOT)} with {len(rows)} assets")


if __name__ == "__main__":
    main()
