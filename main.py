#!/usr/bin/env python3
"""Entrypoint: place the pre-rendered broadsheet at /output/entry.png.

Standard library only. The grading sandbox ships no Pillow and no fonts,
so this program does not draw anything: it only validates the bundled
PNG's header and copies it byte-identical. The image itself is produced
locally by build_entry.py (Pillow), which is part of this repository.
"""

import os
import shutil
import struct
import sys

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
WANT_WIDTH = 1024
WANT_HEIGHT = 1024


def png_dimensions(path):
    """Return (width, height) from a PNG's IHDR chunk, or raise ValueError."""
    with open(path, "rb") as handle:
        head = handle.read(33)
    if len(head) < 33 or head[:8] != PNG_MAGIC:
        raise ValueError("not a PNG file: %s" % path)
    if head[12:16] != b"IHDR":
        raise ValueError("first PNG chunk is not IHDR: %s" % path)
    width, height = struct.unpack(">II", head[16:24])
    return width, height


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, "entry.png")
    width, height = png_dimensions(source)
    if (width, height) != (WANT_WIDTH, WANT_HEIGHT):
        raise SystemExit("entry.png is %dx%d, expected %dx%d"
                         % (width, height, WANT_WIDTH, WANT_HEIGHT))
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "output")
    os.makedirs(out_dir, exist_ok=True)
    dest = os.path.join(out_dir, "entry.png")
    shutil.copyfile(source, dest)
    print("copied entry.png (%dx%d) to %s" % (width, height, dest))
    return 0


if __name__ == "__main__":
    sys.exit(main())
