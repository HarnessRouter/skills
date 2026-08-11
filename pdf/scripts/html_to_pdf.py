#!/usr/bin/env python3
"""Render an HTML file to PDF and report the page count.

The page count is the reason this prints anything at all. "Make it one page" is the most common
instruction for a document like this, and it is the one thing that cannot be checked by reading
the HTML you just wrote.
"""
import argparse
import pathlib
import sys


def main() -> int:
    ap = argparse.ArgumentParser(description="Render an HTML file to PDF.")
    ap.add_argument("html", help="input .html file")
    ap.add_argument("pdf", help="output .pdf file")
    ap.add_argument("--base-url", default=None,
                    help="base for resolving relative images and CSS "
                         "(default: the HTML file's own directory)")
    a = ap.parse_args()

    src = pathlib.Path(a.html)
    if not src.is_file():
        print(f"error: no such file: {src}", file=sys.stderr)
        return 1

    from weasyprint import HTML   # imported late so --help works without the dependency

    doc = HTML(filename=str(src), base_url=a.base_url or str(src.parent)).render()
    doc.write_pdf(a.pdf)

    out = pathlib.Path(a.pdf)
    pages = len(doc.pages)
    print(f"wrote {out} — {pages} page{'s' if pages != 1 else ''}, {out.stat().st_size:,} bytes")
    if pages > 1:
        print("note: more than one page. To reach one, cut the least important section, shorten "
              "prose, or reduce the @page margin — shrinking body text below 9pt to force a fit "
              "is the most obvious sign a document was generated.", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
