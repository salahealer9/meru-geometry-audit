#!/usr/bin/env python3
"""Fetch local snapshots of the primary Meru web sources.

The snapshots are stored under data/raw/source_snapshots and are intentionally
excluded from Git. A reproducible metadata and checksum manifest is written
under references/.
"""

from __future__ import annotations

import csv
import hashlib
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]
SOURCE_MANIFEST = ROOT / "references" / "primary_sources.csv"
SNAPSHOT_DIR = ROOT / "data" / "raw" / "source_snapshots"
OUTPUT_MANIFEST = ROOT / "references" / "source_snapshot_manifest.csv"

USER_AGENT = (
    "Mozilla/5.0 (compatible; MeruGeometryAudit/0.2; "
    "+https://github.com/salahealer9/meru-geometry-audit)"
)


def choose_suffix(url: str, content_type: str) -> str:
    """Choose a stable suffix for a downloaded source."""
    suffix = Path(urlparse(url).path).suffix.lower()

    if suffix:
        return suffix

    if "html" in content_type.lower():
        return ".html"

    return ".bin"


def sha256_bytes(payload: bytes) -> str:
    """Return the hexadecimal SHA-256 digest of a byte string."""
    return hashlib.sha256(payload).hexdigest()


def main() -> None:
    """Download all sources and write a checksum manifest."""
    SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)

    with SOURCE_MANIFEST.open(newline="", encoding="utf-8") as handle:
        sources = list(csv.DictReader(handle))

    output_rows: list[dict[str, str | int]] = []
    failures: list[str] = []

    for source in sources:
        source_id = source["source_id"]
        requested_url = source["url"]

        request = Request(
            requested_url,
            headers={
                "User-Agent": USER_AGENT,
                "Accept": "text/html,application/xhtml+xml,*/*;q=0.8",
            },
        )

        print(f"Fetching {source_id}: {requested_url}")

        try:
            with urlopen(request, timeout=45) as response:
                payload = response.read()
                final_url = response.geturl()
                status = getattr(response, "status", 200)
                content_type = response.headers.get(
                    "Content-Type",
                    "application/octet-stream",
                )
        except (HTTPError, URLError, TimeoutError, OSError) as exc:
            failures.append(f"{source_id}: {exc}")
            print(f"  FAILED: {exc}")
            continue

        suffix = choose_suffix(final_url, content_type)
        destination = SNAPSHOT_DIR / f"{source_id}{suffix}"
        destination.write_bytes(payload)

        retrieved_utc = datetime.now(timezone.utc).replace(
            microsecond=0
        ).isoformat()

        digest = sha256_bytes(payload)

        output_rows.append(
            {
                "source_id": source_id,
                "title": source["title"],
                "requested_url": requested_url,
                "final_url": final_url,
                "retrieved_utc": retrieved_utc,
                "http_status": status,
                "content_type": content_type,
                "bytes": len(payload),
                "sha256": digest,
                "local_path": destination.relative_to(ROOT).as_posix(),
            }
        )

        print(
            f"  wrote {destination.relative_to(ROOT)} "
            f"({len(payload)} bytes, sha256={digest[:16]}...)"
        )

    fieldnames = [
        "source_id",
        "title",
        "requested_url",
        "final_url",
        "retrieved_utc",
        "http_status",
        "content_type",
        "bytes",
        "sha256",
        "local_path",
    ]

    with OUTPUT_MANIFEST.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=fieldnames,
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(output_rows)

    print(f"\nWrote {OUTPUT_MANIFEST.relative_to(ROOT)}")

    if failures:
        print("\nFailures:")
        for failure in failures:
            print(f"  {failure}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
