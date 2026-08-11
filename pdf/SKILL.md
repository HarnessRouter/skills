---
name: pdf
description: "Use this skill whenever a PDF is the input or the output. Creating one — a one-pager, report, invoice, brochure, résumé, certificate, handout, or anything the user asks for \"as a PDF\". Reading one — extracting text or tables, answering questions about a document's contents, summarising it. Changing one — merging, splitting, extracting or rotating pages, adding a watermark, filling a fillable form, or rendering pages to images. Trigger on any mention of a .pdf filename, or on a request to produce a printable or shareable document. Do NOT trigger when the deliverable is a Word document, a spreadsheet, a slide deck, or a web page — those have their own skills."
license: Apache-2.0
---

# PDF

## Pick the approach from the task

| Task | Approach |
|---|---|
| Create a PDF | Write HTML + CSS, render with `scripts/html_to_pdf.py` |
| Create from an existing .docx/.xlsx/.pptx | `soffice --headless --convert-to pdf --outdir . FILE` |
| Read text or tables | `scripts/pdf_text.py` |
| Merge, split, rotate, watermark | `scripts/pdf_pages.py` |
| Fill a fillable form | `scripts/pdf_form.py` |
| Look at the result | `scripts/pdf_preview.py` |

Do not place text at absolute coordinates to build a document. The renderer here is a browser
engine, so ordinary HTML and CSS work, and every layout problem you would otherwise solve by hand
— wrapping, table widths, keeping a heading with its paragraph — is already solved.

## Creating a PDF

Write an `.html` file, then:

```bash
python3 scripts/html_to_pdf.py page.html out.pdf
```

It prints the page count. That matters: "make it one page" is the most common instruction for this
kind of document and the one thing you cannot check by reading your own HTML.

Control paper and margins with `@page`. This single rule is most of the difference between a
document that looks designed and one that looks like a default:

```css
@page { size: Letter; margin: 16mm 15mm; }
```

Use `size: A4` outside the US. `@page { size: Letter landscape; }` for wide tables.

**Read `references/design.md` before writing the HTML.** It has the type scale, spacing, and colour
rules that make the difference, plus a one-pager skeleton to start from.

**Fonts.** Only what is installed will render: DejaVu Sans, DejaVu Serif, DejaVu Sans Mono,
Liberation Sans, Liberation Serif, Liberation Mono. Name one explicitly with a generic fallback —
an unnamed font is not a design decision. There is no network access at render time, so a Google
Fonts `@import` silently falls back.

### Fitting one page

If the page count comes back above 1, cut or tighten in this order: drop the least important
section, shorten prose, reduce `margin` on `@page` to 12mm, tighten `line-height` toward 1.35.
Shrinking body text below 9pt to force a fit is the most obvious sign a document was generated —
do that last, and prefer cutting content.

To keep a block from splitting across pages: `break-inside: avoid;`.

## Reading a PDF

```bash
python3 scripts/pdf_text.py in.pdf                 # all pages, one labelled block each
python3 scripts/pdf_text.py in.pdf --pages 1-3,7
python3 scripts/pdf_text.py in.pdf --tables        # detected tables as TSV
```

If it returns nothing, the PDF is images rather than text. There is no OCR installed here. Say
that plainly instead of guessing at the contents — a confident summary of a document you could not
read is worse than reporting that you could not read it.

## Changing pages

```bash
python3 scripts/pdf_pages.py info    in.pdf
python3 scripts/pdf_pages.py merge   a.pdf b.pdf -o out.pdf
python3 scripts/pdf_pages.py split   in.pdf --pages 2-5   -o out.pdf
python3 scripts/pdf_pages.py rotate  in.pdf --pages 1 --degrees 90 -o out.pdf
python3 scripts/pdf_pages.py stamp   in.pdf --text DRAFT  -o out.pdf
```

## Forms

```bash
python3 scripts/pdf_form.py list in.pdf                          # field names, types, current values
python3 scripts/pdf_form.py fill in.pdf -o out.pdf --set Name="Ada Lovelace" --set Agree=Yes
```

`list` first, always — field names are rarely what the visible labels say. Filled values are
flattened into the page appearance so they show in every viewer, not only ones that honour form
data.

## Check the result before saying it is done

```bash
python3 scripts/pdf_preview.py out.pdf --outdir preview
```

Then **read the PNGs**. After writing the HTML you will see what you intended rather than what
rendered. Look for:

- text overflowing or clipped at a boundary — the most common defect, and always visible to the user
- content colliding with the page margin, or a footer overlapping the body
- a table wider than the page, silently cut off at the right edge
- an orphaned heading alone at the bottom, or a single line stranded on a second page
- low-contrast text (pale grey on white reads as broken, not subtle)

## Where to write files

Write to the working directory. Files there are collected and returned to the user; anything in
`/tmp` is lost when the task ends.

## Dependencies

Installed in the image: `weasyprint` (HTML→PDF), `pypdf` (pages, forms), `pdfplumber` (text and
tables), `pdftoppm` from poppler-utils (page images), LibreOffice (`soffice`, other formats→PDF).
