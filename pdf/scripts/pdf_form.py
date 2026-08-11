#!/usr/bin/env python3
"""List and fill PDF form fields.

`list` first, always. Field names are almost never the visible labels — a box captioned "Full name"
is as likely to be `topmostSubform[0].Page1[0].f1_01[0]`. Guessing produces a PDF that looks filled
in the code and is blank on screen.
"""
import argparse
import pathlib
import sys


def cmd_list(a) -> int:
    from pypdf import PdfReader
    r = PdfReader(a.pdf)
    fields = r.get_fields() or {}
    if not fields:
        print("no form fields — this PDF is not a fillable form. To put text on it, "
              "use pdf_pages.py stamp or rebuild the page from HTML.")
        return 0
    print(f"{len(fields)} field(s):")
    for name, f in fields.items():
        ftype = {"/Tx": "text", "/Btn": "button/checkbox", "/Ch": "choice"}.get(
            str(f.get("/FT")), str(f.get("/FT") or "?"))
        value = f.get("/V")
        line = f"  {name!r}  type={ftype}"
        if value not in (None, ""):
            line += f"  current={value!r}"
        states = f.get("/_States_")
        if states:
            line += f"  accepts={list(states)}"
        print(line)
    return 0


def cmd_fill(a) -> int:
    from pypdf import PdfReader, PdfWriter
    r = PdfReader(a.pdf)
    known = set((r.get_fields() or {}).keys())
    values: dict[str, str] = {}
    for pair in a.set:
        if "=" not in pair:
            raise SystemExit(f"error: --set expects NAME=VALUE, got {pair!r}")
        k, _, v = pair.partition("=")
        values[k] = v

    unknown = [k for k in values if k not in known]
    if unknown:
        # Silently writing a field that does not exist yields a PDF that looks filled to the code
        # and is blank to the reader. Refuse, and show what the real names are.
        print(f"error: no such field(s): {unknown}", file=sys.stderr)
        print(f"available: {sorted(known)}", file=sys.stderr)
        return 1

    w = PdfWriter(clone_from=str(a.pdf))
    for page in w.pages:
        w.update_page_form_field_values(page, values, auto_regenerate=True)
    if a.flatten:
        w.set_need_appearances_writer(False)
    else:
        w.set_need_appearances_writer(True)
    with open(a.output, "wb") as fh:
        w.write(fh)
    print(f"wrote {a.output} — set {len(values)} field(s): {', '.join(sorted(values))}")
    print("check it with: python3 scripts/pdf_preview.py " + a.output)
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="List and fill PDF form fields.")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("list"); p.add_argument("pdf"); p.set_defaults(fn=cmd_list)

    p = sub.add_parser("fill"); p.add_argument("pdf")
    p.add_argument("--set", action="append", default=[], metavar="NAME=VALUE")
    p.add_argument("--flatten", action="store_true",
                   help="bake values into the page appearance instead of leaving them as form data")
    p.add_argument("-o", "--output", required=True); p.set_defaults(fn=cmd_fill)

    a = ap.parse_args()
    if not pathlib.Path(a.pdf).is_file():
        print(f"error: no such file: {a.pdf}", file=sys.stderr)
        return 1
    return a.fn(a)


if __name__ == "__main__":
    raise SystemExit(main())
