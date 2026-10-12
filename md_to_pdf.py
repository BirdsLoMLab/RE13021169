#!/usr/bin/env python3
"""Render a repo markdown doc to a single print-ready PDF.

Usage: python3 md_to_pdf.py <input.md> <output.pdf> [--title "..."] [--subtitle "..."]
"""
import argparse, re, html as _html
import markdown
from weasyprint import HTML, CSS

CSS_TEXT = """
@page {
  size: letter;
  margin: 18mm 16mm 16mm 16mm;
  @top-right  { content: string(doctitle); font: 8pt "DejaVu Sans"; color: #8a8f98; }
  @bottom-right { content: counter(page) " / " counter(pages);
                  font: 8pt "DejaVu Sans"; color: #8a8f98; }
}
@page :first { @top-right { content: ""; } }

body { font-family: "DejaVu Sans", sans-serif; font-size: 9.3pt; line-height: 1.5;
       color: #14181f; }
code, pre { font-family: "DejaVu Sans Mono", monospace; }

h1 { string-set: doctitle content(); font-size: 19pt; line-height: 1.25; margin: 0 0 4pt;
     color: #0f1b33; border-bottom: 2.5pt solid #1f3864; padding-bottom: 7pt; }
h2 { font-size: 13pt; color: #1f3864; margin: 20pt 0 6pt;
     border-bottom: 0.6pt solid #c9d2e3; padding-bottom: 3pt;
     break-after: avoid; break-inside: avoid; }
h3 { font-size: 10.6pt; color: #27406b; margin: 13pt 0 4pt; break-after: avoid; }
h4 { font-size: 9.6pt; color: #3c4a63; margin: 10pt 0 3pt; break-after: avoid; }
p, li { orphans: 2; widows: 2; }
p { margin: 0 0 6pt; }
ul, ol { margin: 0 0 7pt; padding-left: 17pt; }
li { margin-bottom: 2.5pt; }

/* lead-in blockquote: sources / question block */
blockquote { margin: 9pt 0 14pt; padding: 8pt 11pt; background: #f4f6fa;
             border-left: 2.5pt solid #1f3864; font-size: 8.5pt; color: #39414f; }
blockquote p { margin: 0 0 4pt; }
blockquote p:last-child { margin-bottom: 0; }

pre { background: #f6f7f9; border: 0.5pt solid #dde1e8; border-left: 2.5pt solid #7f8da8;
      padding: 7pt 9pt; font-size: 7.6pt; line-height: 1.42; margin: 7pt 0 9pt;
      white-space: pre-wrap; word-wrap: break-word; break-inside: avoid; }
:not(pre) > code { background: #eef1f6; padding: 0.5pt 2.5pt; border-radius: 2pt;
                   font-size: 8.2pt; color: #1d2b45; }

table { border-collapse: collapse; width: 100%; margin: 7pt 0 11pt; font-size: 8.1pt;
        break-inside: avoid; }
th { background: #1f3864; color: #fff; text-align: left; padding: 4.5pt 6pt;
     font-weight: bold; }
td { padding: 4pt 6pt; border-bottom: 0.4pt solid #dde1e8; vertical-align: top; }
tbody tr:nth-child(even) { background: #f6f8fb; }

hr { border: none; border-top: 0.5pt solid #d8dde6; margin: 15pt 0; }
a { color: #1f3864; text-decoration: none; }
.subtitle { color: #6b7280; font-size: 9pt; margin: 0 0 2pt; }
"""


def build(src_path, out_path, title=None, subtitle=None):
    text = open(src_path, encoding="utf-8").read()

    # the doc's own H1 becomes the PDF title; keep it, drop a duplicate if --title given
    if title:
        text = re.sub(r"\A#\s+.*\n", "", text, count=1)

    body = markdown.markdown(
        text,
        extensions=["tables", "fenced_code", "sane_lists", "attr_list"],
        output_format="html5",
    )

    head = ""
    if title:
        head += f"<h1>{_html.escape(title)}</h1>"
    if subtitle:
        head += f'<p class="subtitle">{_html.escape(subtitle)}</p>'

    doc = f"<!doctype html><html><head><meta charset='utf-8'></head><body>{head}{body}</body></html>"
    HTML(string=doc, base_url=str(src_path)).write_pdf(out_path, stylesheets=[CSS(string=CSS_TEXT)])
    return out_path


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("input")
    ap.add_argument("output")
    ap.add_argument("--title")
    ap.add_argument("--subtitle")
    a = ap.parse_args()
    print("wrote", build(a.input, a.output, a.title, a.subtitle))
