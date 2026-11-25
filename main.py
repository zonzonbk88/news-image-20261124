#!/usr/bin/env python3
"""Publish the news-image entry to the output directory.

The image itself (entry.png) lives next to this script. This program
copies it to the location make.fun expects — $MAKEFUN_OUTPUT_DIR/entry.png
when that variable is set, otherwise /output/entry.png — and then checks
the copy is a valid, complete PNG before reporting success.

Only the standard library is used.
"""

import os
import shutil
import sys
from pathlib import Path

# First eight bytes of every PNG file.
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"

# Fallback output location when the harness does not set one.
DEFAULT_OUTPUT_DIR = "/output"


def locate_source() -> Path:
    """Return the entry.png sitting beside this script, or fail loudly."""
    source = Path(__file__).resolve().parent / "entry.png"
    if not source.is_file():
        print(f"error: entry image not found: {source}", file=sys.stderr)
        sys.exit(1)
    return source


def destination_path() -> Path:
    """Pick the output directory from the environment and build the path."""
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or DEFAULT_OUTPUT_DIR
    return Path(out_dir) / "entry.png"


def check_png(path: Path, expected_size: int) -> None:
    """Confirm the file at `path` is a PNG of the expected size."""
    with open(path, "rb") as handle:
        header = handle.read(len(PNG_SIGNATURE))
    if header != PNG_SIGNATURE:
        print(f"error: {path} is not a PNG file", file=sys.stderr)
        sys.exit(1)
    actual_size = path.stat().st_size
    if actual_size != expected_size:
        print(
            f"error: size mismatch for {path}: "
            f"got {actual_size} bytes, expected {expected_size}",
            file=sys.stderr,
        )
        sys.exit(1)


def main() -> None:
    source = locate_source()
    destination = destination_path()

    # Never copy a file onto itself (e.g. MAKEFUN_OUTPUT_DIR pointing at
    # the repo directory): that would truncate the entry image.
    try:
        same_file = source.samefile(destination)
    except FileNotFoundError:
        same_file = False
    if same_file:
        print(
            f"error: source and destination are the same file: {source}",
            file=sys.stderr,
        )
        sys.exit(1)

    destination.parent.mkdir(parents=True, exist_ok=True)

    shutil.copyfile(source, destination)

    expected = source.stat().st_size
    check_png(destination, expected)
    print(f"Copied {expected} bytes to {destination} (PNG verified)")


if __name__ == "__main__":
    main()
