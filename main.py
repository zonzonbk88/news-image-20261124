"""Entry program for the make.fun bounty "news-image-20261124".

The repository holds a finished front-page image, entry.png, that sums up
the world news of Tuesday 24 November 2026: the COP31 climate talks
collapsing without a deal, Ukraine's claimed sinking of a Russian warship
off Libya, the Russian strike on Zaporizhzhia, Nvidia reinstating Jensen
Huang as CEO, Iran vowing to defy the US blockade, and the ICJ ruling
that Myanmar committed genocide against the Rohingya, plus a ticker of
the day's other stories. This program copies those exact bytes to the
output directory, so both grading runs write the same file.
"""

import os
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "entry.png"
OUTPUT_NAME = "entry.png"


def main() -> int:
    if not SOURCE.is_file():
        print(f"error: {SOURCE} is missing from the repository", file=sys.stderr)
        return 1
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / OUTPUT_NAME
    shutil.copyfile(SOURCE, target)
    if target.read_bytes() != SOURCE.read_bytes():
        print("error: copied image differs from the repository image",
              file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
