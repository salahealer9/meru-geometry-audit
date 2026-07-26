#!/usr/bin/env python3
"""Fetch and inventory key Meru geometric source images.

Original images remain local and are excluded from Git. The committed output is
a metadata and SHA-256 manifest.
"""

from __future__ import annotations

import csv
import hashlib
import io
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen

from PIL import Image, UnidentifiedImageError


ROOT = Path(__file__).resolve().parents[1]
INPUT_PATH = ROOT / "references" / "key_geometric_assets.csv"
ASSET_DIR = ROOT / "data" / "raw" / "geometric_assets"
OUTPUT_PATH = (
    ROOT
    / "references"
    / "geometric_asset_snapshot_manifest.csv"
)

USER_AGENT = (
    "Mozilla/5.0 (compatible; MeruGeometryAudit/0.6; "
    "+https://github.com/salahealer9/meru-geometry-audit)"
)


def safe_suffix(url: str, image_format: str) -> str:
    """Return a stable image suffix."""
    suffix = Path(urlparse(url).path).suffix.lower()

    if suffix in {".gif", ".jpg", ".jpeg", ".png", ".webp"}:
        return suffix

    format_suffixes = {
        "GIF": ".gif",
        "JPEG": ".jpg",
        "PNG": ".png",
        "WEBP": ".webp",
    }

    return format_suffixes.get(image_format.upper(), ".img")


def sha256_bytes(payload: bytes) -> str:
    """Return the SHA-256 digest of a payload."""
    return hashlib.sha256(payload).hexdigest()


def inspect_image(
    payload: bytes,
) -> tuple[str, str, int, int, int]:
    """Return format, mode, width, height, and frame count."""
    with Image.open(io.BytesIO(payload)) as image:
        image_format = image.format or "UNKNOWN"
        mode = image.mode
        width, height = image.size
        frames = int(getattr(image, "n_frames", 1))

    return image_format, mode, width, height, frames


def main() -> None:
    """Download each registered asset and write its manifest."""
    ASSET_DIR.mkdir(parents=True, exist_ok=True)

    with INPUT_PATH.open(newline="", encoding="utf-8") as handle:
        assets = list(csv.DictReader(handle))

    rows: list[dict[str, str | int]] = []
    failures: list[str] = []

    for asset in assets:
        asset_id = asset["asset_id"]
        url = asset["url"]
        referer = asset["source_page"]

        print(f"Fetching {asset_id}: {url}")

        request = Request(
            url,
            headers={
                "User-Agent": USER_AGENT,
                "Referer": referer,
                "Accept": (
                    "image/avif,image/webp,image/apng,"
                    "image/svg+xml,image/*,*/*;q=0.8"
                ),
                "Cache-Control": "no-cache",
            },
        )

        row: dict[str, str | int] = {
            "asset_id": asset_id,
            "related_source": asset["related_source"],
            "title": asset["title"],
            "requested_url": url,
            "source_page": referer,
            "final_url": "",
            "retrieved_utc": "",
            "http_status": "",
            "content_type": "",
            "format": "",
            "mode": "",
            "width_px": "",
            "height_px": "",
            "frames": "",
            "bytes": "",
            "sha256": "",
            "local_path": "",
            "status": "failed",
            "error": "",
        }

        try:
            with urlopen(request, timeout=60) as response:
                payload = response.read()
                final_url = response.geturl()
                status = getattr(response, "status", 200)
                content_type = response.headers.get(
                    "Content-Type",
                    "application/octet-stream",
                )

            (
                image_format,
                mode,
                width,
                height,
                frames,
            ) = inspect_image(payload)

            suffix = safe_suffix(final_url, image_format)
            filename = (
                f"{asset_id}_"
                f"{Path(urlparse(url).path).stem}"
                f"{suffix}"
            )
            destination = ASSET_DIR / filename
            destination.write_bytes(payload)

            retrieved = datetime.now(timezone.utc).replace(
                microsecond=0
            ).isoformat()

            row.update(
                {
                    "final_url": final_url,
                    "retrieved_utc": retrieved,
                    "http_status": int(status),
                    "content_type": content_type,
                    "format": image_format,
                    "mode": mode,
                    "width_px": width,
                    "height_px": height,
                    "frames": frames,
                    "bytes": len(payload),
                    "sha256": sha256_bytes(payload),
                    "local_path": (
                        destination.relative_to(ROOT).as_posix()
                    ),
                    "status": "success",
                    "error": "",
                }
            )

            print(
                f"  wrote {destination.relative_to(ROOT)} "
                f"({width}x{height}, {image_format}, "
                f"{len(payload)} bytes)"
            )

        except (
            HTTPError,
            URLError,
            TimeoutError,
            OSError,
            UnidentifiedImageError,
        ) as exc:
            message = f"{type(exc).__name__}: {exc}"
            row["error"] = message
            failures.append(f"{asset_id}: {message}")
            print(f"  FAILED: {message}")

        rows.append(row)

    fieldnames = [
        "asset_id",
        "related_source",
        "title",
        "requested_url",
        "source_page",
        "final_url",
        "retrieved_utc",
        "http_status",
        "content_type",
        "format",
        "mode",
        "width_px",
        "height_px",
        "frames",
        "bytes",
        "sha256",
        "local_path",
        "status",
        "error",
    ]

    with OUTPUT_PATH.open(
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

    print(f"\nWrote {OUTPUT_PATH.relative_to(ROOT)}")

    if failures:
        print("\nFailed assets:")
        for failure in failures:
            print(f"  {failure}")

        raise SystemExit(1)


if __name__ == "__main__":
    main()
