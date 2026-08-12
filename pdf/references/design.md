# Designing a document that does not look generated

The default rendering of unstyled HTML is instantly recognisable: Times New Roman, full-width
lines, uniform spacing, no hierarchy. Fixing that is about six decisions, and they are all below.

## The page

```css
@page { size: Letter; margin: 16mm 15mm; }
```

`A4` outside the US. Margins under 12mm look cramped and risk being clipped by physical printers;
over 25mm wastes a one-pager's most valuable resource. Add `landscape` after the size for wide
tables.

## Type

Pick **one** family and vary weight and size. Two families is a design decision that needs a reason;
three is a mistake.

| Role | Size | Weight | Notes |
|---|---|---|---|
| Document title | 22–28pt | 700 | Once, at the top |
| Section heading | 11–13pt | 600 | Often uppercase with `letter-spacing: .08em` |
| Body | 9.5–10.5pt | 400 | Below 9pt reads as "made it fit" |
| Caption / footer | 8–8.5pt | 400 | Muted colour, never below 7.5pt |

`line-height: 1.45` for body. Tighter than 1.3 looks cramped; looser than 1.6 wastes a page.

Set `max-width: 68ch` on running prose, or use columns. A full-width line at 10pt on Letter is
roughly 110 characters, and the eye loses its place returning to the next line.

Available families — nothing else is installed, and a remote font fetch fails open (the page
renders without it rather than erroring), so name one of these:

```css
font-family: 'DejaVu Sans', 'Liberation Sans', sans-serif;   /* body */
font-family: 'DejaVu Serif', 'Liberation Serif', serif;      /* editorial */
font-family: 'DejaVu Sans Mono', monospace;                  /* code, figures */
```

## Colour

One accent, one near-black for text, two greys. Resist more.

```css
:root {
  --ink:    #16181d;   /* body text — not #000, which is harsh on paper */
  --muted:  #6b7280;   /* captions, labels, secondary */
  --rule:   #e5e7eb;   /* hairlines */
  --accent: #1f4ed8;   /* headings, key figures — pick ONE */
}
```

Grey text below `#8a8f98` on white fails contrast in print. Never put body text on a coloured
background at this size.

## Space

Space is what makes a document look considered. The most common failure is uniform spacing
everywhere, which reads as undifferentiated.

- Space *above* a heading should be roughly double the space below it — that is what binds a
  heading to the text it introduces rather than letting it float.
- One clear band of space between major sections beats a horizontal rule. If you use a rule, make
  it 1px in `--rule`, not a heavy black line.
- Never centre body text. Centre a title only if the whole document is centred.

## Tables

```css
table { width: 100%; border-collapse: collapse; font-size: 9.5pt; }
th { text-align: left; font-weight: 600; border-bottom: 1.5px solid var(--ink); padding: 6px 8px; }
td { border-bottom: 1px solid var(--rule); padding: 6px 8px; }
td.num { text-align: right; font-variant-numeric: tabular-nums; }
```

Right-align numbers and use `tabular-nums` so digits line up in a column. Grid lines on every cell
are a spreadsheet's look, not a document's — horizontal rules alone are almost always better.

## Keeping things together

```css
h2, h3 { break-after: avoid; }        /* never a heading alone at the foot of a page */
tr, li, .card { break-inside: avoid; }
```

## A one-pager skeleton

Start here and replace the content.

```html
<!doctype html>
<meta charset="utf-8">
<style>
  @page { size: Letter; margin: 15mm 14mm; }
  :root { --ink:#16181d; --muted:#6b7280; --rule:#e5e7eb; --accent:#1f4ed8; }
  * { box-sizing: border-box; }
  body { margin:0; font-family:'DejaVu Sans','Liberation Sans',sans-serif;
         font-size:10pt; line-height:1.45; color:var(--ink); }
  header { border-bottom:2px solid var(--ink); padding-bottom:8px; margin-bottom:14px;
           display:flex; align-items:baseline; justify-content:space-between; gap:16px; }
  /* Without these the title column shrinks to its content box and a two-word title wraps with
     half the page still empty. flex-basis auto + a non-shrinking date is what keeps it on one line. */
  header > div:first-child { flex:1 1 auto; min-width:0; }
  header > .kicker { flex:0 0 auto; white-space:nowrap; }
  h1 { font-size:24pt; font-weight:700; margin:0; letter-spacing:-.01em; text-wrap:balance; }
  .kicker { font-size:8.5pt; color:var(--muted); text-transform:uppercase; letter-spacing:.1em; }
  h2 { font-size:11pt; font-weight:600; text-transform:uppercase; letter-spacing:.08em;
       color:var(--accent); margin:16px 0 6px; break-after:avoid; }
  p { margin:0 0 8px; max-width:68ch; }
  .lede { font-size:11.5pt; color:#333; margin-bottom:14px; }
  .cols { display:grid; grid-template-columns:1fr 1fr; gap:14px 22px; }
  .stat { border-left:3px solid var(--accent); padding-left:10px; break-inside:avoid; }
  .stat .n { font-size:19pt; font-weight:700; font-variant-numeric:tabular-nums; }
  .stat .l { font-size:8.5pt; color:var(--muted); text-transform:uppercase; letter-spacing:.06em; }
  footer { margin-top:16px; padding-top:8px; border-top:1px solid var(--rule);
           font-size:8pt; color:var(--muted); display:flex; justify-content:space-between; }
</style>

<header>
  <div>
    <div class="kicker">Quarterly summary</div>
    <h1>Document title</h1>
  </div>
  <div class="kicker">August 2026</div>
</header>

<p class="lede">One sentence that says the single most important thing. If a reader stops here,
this is what they leave with.</p>

<div class="cols">
  <div class="stat"><div class="n">18%</div><div class="l">Revenue growth</div></div>
  <div class="stat"><div class="n">1,204</div><div class="l">Active accounts</div></div>
</div>

<h2>Section</h2>
<p>Body copy.</p>

<footer><span>Prepared for …</span><span>Page 1 of 1</span></footer>
```

## Before you call it done

Render it, then look at it:

```bash
python3 scripts/html_to_pdf.py page.html out.pdf
python3 scripts/pdf_preview.py out.pdf --outdir preview
```

Read the PNG. The defects that matter are visual and none of them appear in the HTML: text
overflowing its container, a table wider than the page, a heading stranded at the bottom, a footer
overlapping the body, one line spilling onto a second page, and **a heading wrapping to a second
line while the space beside it sits empty** — a flex container that shrank around its content is
the usual cause.
