#!/usr/bin/env python3
"""Render PDF pages to PNGs so the result can actually be looked at.

This exists because reading your own generating code shows you what you meant, not what rendered.
Text overflowing its box, a table cut off at the right edge, a footer colliding with the body — none
of these are visible in the HTML, and all of them are obvious in the image.
"""
import argparse
import pathlib
import shutil
import subprocess
import sys


def main() -> int:
    ap = argparse.ArgumentParser(description="Render PDF pages to PNG images.")
    ap.add_argument("pdf")
    ap.add_argument("--outdir", default="preview")
    ap.add_argument("--dpi", type=int, default=110, help="110 is enough to read body text")
    ap.add_argument("--pages", default=None, help="e.g. 1-3 (default: all)")
    a = ap.parse_args()

    src = pathlib.Path(a.pdf)
    if not src.is_file():
        print(f"error: no such file: {src}", file=sys.stderr)
        return 1
    if not shutil.which("pdftoppm"):
        print("error: pdftoppm not found (poppler-utils)", file=sys.stderr)
        return 1

    outdir = pathlib.Path(a.outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    cmd = ["pdftoppm", "-png", "-r", str(a.dpi)]
    if a.pages:
        lo, _, hi = a.pages.partition("-")
        cmd += ["-f", lo.strip(), "-l", (hi or lo).strip()]
    cmd += [str(src), str(outdir / src.stem)]

    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(f"error: pdftoppm failed: {r.stderr.strip()[:400]}", file=sys.stderr)
        return 1

    pngs = sorted(outdir.glob(f"{src.stem}*.png"))
    for p in pngs:
        print(p)
    print(f"\n{len(pngs)} image(s) in {outdir}/ — now READ them. Look for text overflowing or "
          f"clipped at a boundary, content colliding with the margin, a table cut off at the "
          f"right edge, an orphaned heading, and low-contrast text.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
