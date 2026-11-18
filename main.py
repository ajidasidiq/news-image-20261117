#!/usr/bin/env python3
"""Entry for make.fun competition news-image-20261117.

Writes the pre-drawn front-page image (entry.png, in this repository) to
$MAKEFUN_OUTPUT_DIR/entry.png, or /output/entry.png when unset.
Standard library only; deterministic: the same bytes every run.
"""

import os
import shutil
import sys

ASSET = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")


def main():
    if not os.path.isfile(ASSET):
        raise SystemExit("missing image asset: %s" % ASSET)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(ASSET, os.path.join(out_dir, "entry.png"))


if __name__ == "__main__":
    sys.exit(main())
