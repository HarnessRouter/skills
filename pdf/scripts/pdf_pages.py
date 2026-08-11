#!/usr/bin/env python3
"""Page-level PDF operations: info, merge, split, rotate, stamp."""
import argparse
import pathlib
import sys


def parse_pages(spec: str, total: int) -> list[int]:
    """'2-5,9' -> 0-based indices. Out of range is an error — see pdf_text.py."""
    out: list[int] = []
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
            out.append(n - 1)
    return out


def cmd_info(a) -> int:
    from pypdf import PdfReader
    r = PdfReader(a.pdf)
    print(f"{a.pdf}: {len(r.pages)} pages, encrypted={r.is_encrypted}")
    for i, p in enumerate(r.pages, 1):
        box = p.mediabox
        print(f"  page {i}: {float(box.width):.0f} x {float(box.height):.0f} pt"
              f"  rotation={p.get('/Rotate', 0)}")
    if r.metadata:
        for k, v in r.metadata.items():
            print(f"  {k}: {v}")
    return 0


def cmd_merge(a) -> int:
    from pypdf import PdfWriter
    w = PdfWriter()
    for f in a.inputs:
        if not pathlib.Path(f).is_file():
            print(f"error: no such file: {f}", file=sys.stderr)
            return 1
        w.append(f)
    with open(a.output, "wb") as fh:
        w.write(fh)
    print(f"wrote {a.output} — {len(w.pages)} pages from {len(a.inputs)} files")
    return 0


def cmd_split(a) -> int:
    from pypdf import PdfReader, PdfWriter
    r = PdfReader(a.pdf)
    idxs = parse_pages(a.pages, len(r.pages))
    w = PdfWriter()
    for i in idxs:
        w.add_page(r.pages[i])
    with open(a.output, "wb") as fh:
        w.write(fh)
    print(f"wrote {a.output} — {len(idxs)} of {len(r.pages)} pages")
    return 0


def cmd_rotate(a) -> int:
    from pypdf import PdfReader, PdfWriter
    if a.degrees % 90:
        raise SystemExit("error: --degrees must be a multiple of 90")
    r = PdfReader(a.pdf)
    idxs = set(parse_pages(a.pages, len(r.pages))) if a.pages else set(range(len(r.pages)))
    w = PdfWriter()
    for i, p in enumerate(r.pages):
        if i in idxs:
            p.rotate(a.degrees)
        w.add_page(p)
    with open(a.output, "wb") as fh:
        w.write(fh)
    print(f"wrote {a.output} — rotated {len(idxs)} page(s) by {a.degrees}°")
    return 0


def cmd_stamp(a) -> int:
    """Overlay text on every page. Built as its own one-page PDF and merged, rather than drawn on,
    so the original page content is untouched and the stamp can be a different size or angle."""
    import io
    from pypdf import PdfReader, PdfWriter
    from weasyprint import HTML

    r = PdfReader(a.pdf)
    first = r.pages[0].mediabox
    w_pt, h_pt = float(first.width), float(first.height)
    html = f"""<html><head><style>
      @page {{ size: {w_pt}pt {h_pt}pt; margin: 0; }}
      body {{ margin:0; height:{h_pt}pt; display:flex; align-items:center; justify-content:center; }}
      .s {{ font-family: 'DejaVu Sans', sans-serif; font-size:{a.size}pt; color:{a.color};
            opacity:{a.opacity}; transform: rotate(-30deg); letter-spacing:.08em; }}
    </style></head><body><div class="s">{a.text}</div></body></html>"""
    buf = io.BytesIO()
    HTML(string=html).write_pdf(buf)
    buf.seek(0)
    overlay = PdfReader(buf).pages[0]

    out = PdfWriter()
    for p in r.pages:
        p.merge_page(overlay)
        out.add_page(p)
    with open(a.output, "wb") as fh:
        out.write(fh)
    print(f"wrote {a.output} — stamped {len(r.pages)} page(s) with {a.text!r}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="Page-level PDF operations.")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("info"); p.add_argument("pdf"); p.set_defaults(fn=cmd_info)

    p = sub.add_parser("merge"); p.add_argument("inputs", nargs="+")
    p.add_argument("-o", "--output", required=True); p.set_defaults(fn=cmd_merge)

    p = sub.add_parser("split"); p.add_argument("pdf")
    p.add_argument("--pages", required=True); p.add_argument("-o", "--output", required=True)
    p.set_defaults(fn=cmd_split)

    p = sub.add_parser("rotate"); p.add_argument("pdf")
    p.add_argument("--pages", default=None); p.add_argument("--degrees", type=int, required=True)
    p.add_argument("-o", "--output", required=True); p.set_defaults(fn=cmd_rotate)

    p = sub.add_parser("stamp"); p.add_argument("pdf")
    p.add_argument("--text", required=True); p.add_argument("--size", type=int, default=72)
    p.add_argument("--color", default="#c00"); p.add_argument("--opacity", type=float, default=0.18)
    p.add_argument("-o", "--output", required=True); p.set_defaults(fn=cmd_stamp)

    a = ap.parse_args()
    if not pathlib.Path(getattr(a, "pdf", a.inputs[0] if a.cmd == "merge" else "")).is_file():
        print("error: input file not found", file=sys.stderr)
        return 1
    return a.fn(a)


if __name__ == "__main__":
    raise SystemExit(main())
