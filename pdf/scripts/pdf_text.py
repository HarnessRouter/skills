#!/usr/bin/env python3
"""Extract text (and optionally tables) from a PDF, one labelled block per page."""
import argparse
import pathlib
import sys


def parse_pages(spec: str, total: int) -> list[int]:
    """'1-3,7' -> [0,1,2,6], 0-based. A page outside the document is an error, not a silent skip:
    quietly dropping it produces a confident answer about content that was never read."""
    want: list[int] = []
    for part in spec.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            lo, hi = part.split("-", 1)
            rng = range(int(lo), int(hi) + 1)
        else:
            rng = range(int(part), int(part) + 1)
        for n in rng:
            if not 1 <= n <= total:
                raise SystemExit(f"error: page {n} is outside this document (1-{total})")
            want.append(n - 1)
    return want


def main() -> int:
    ap = argparse.ArgumentParser(description="Extract text from a PDF.")
    ap.add_argument("pdf")
    ap.add_argument("--pages", default=None, help="e.g. 1-3,7 (default: all)")
    ap.add_argument("--tables", action="store_true", help="also emit detected tables as TSV")
    a = ap.parse_args()

    src = pathlib.Path(a.pdf)
    if not src.is_file():
        print(f"error: no such file: {src}", file=sys.stderr)
        return 1

    import pdfplumber

    with pdfplumber.open(str(src)) as doc:
        total = len(doc.pages)
        idxs = list(parse_pages(a.pages, total)) if a.pages else list(range(total))
        empty = 0
        for i in idxs:
            page = doc.pages[i]
            text = page.extract_text() or ""
            if not text.strip():
                empty += 1
            print(f"=== page {i + 1} of {total} ===")
            print(text)
            if a.tables:
                for t, table in enumerate(page.extract_tables() or [], 1):
                    print(f"--- page {i + 1} table {t} ---")
                    for row in table:
                        print("\t".join("" if c is None else str(c).replace("\n", " ")
                                        for c in row))

    if idxs and empty == len(idxs):
        print("\nnote: no extractable text — this PDF is images, not text. There is no OCR "
              "installed here, so its contents are unknown. Say that rather than guessing.",
              file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
