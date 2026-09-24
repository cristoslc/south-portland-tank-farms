#!/usr/bin/env python3
"""Build unified PDF binder: report + fact-check + dataset + official source docs."""
import os, json, datetime
import pymupdf

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # repo root
OUT = os.path.join(HERE, "outputs")
DATA = os.path.join(HERE, "data")
os.chdir(OUT)
OUT_FILE = "SouthPortland_TankFarms_Binder.pdf"

import markdown
md = markdown.Markdown(extensions=["tables", "smarty"])

def md_to_pdf(md_path, out_pdf, title):
    out_pdf = md_path.replace(".md", "_render.pdf")
    text = open(md_path, encoding="utf-8").read()
    html_body = md.reset().convert(text)
    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
body {{ font-family: Georgia, 'Times New Roman', serif; font-size: 10.5pt; line-height: 1.45; color: #1a1a1a; margin: 0; }}
h1 {{ font-size: 17pt; color: #1a3a5c; border-bottom: 2px solid #1a3a5c; padding-bottom: 4px; margin-top: 22px; }}
h2 {{ font-size: 13.5pt; color: #1a3a5c; margin-top: 18px; }}
h3 {{ font-size: 11.5pt; color: #2c5580; }}
table {{ border-collapse: collapse; width: 100%; font-size: 8.5pt; margin: 10px 0; font-family: Helvetica, Arial, sans-serif; }}
th, td {{ border: 1px solid #999; padding: 3px 5px; text-align: left; vertical-align: top; }}
th {{ background: #e8eef4; }}
blockquote {{ border-left: 4px solid #1a3a5c; margin: 10px 0; padding: 6px 12px; background: #f2f6fa; }}
code {{ font-family: 'Courier New', monospace; font-size: 8.5pt; background: #f4f4f4; }}
pre {{ background: #f4f4f4; padding: 8px; font-size: 8.5pt; white-space: pre-wrap; }}
@media print {{ @page {{ size: Letter; margin: 0.75in; }} }}
</style></head><body>{html_body}</body></html>"""
    open("binder_tmp.html", "w", encoding="utf-8").write(html)
    story = pymupdf.Story(html=html, archive=pymupdf.Archive("."), em=12)
    writer = pymupdf.DocumentWriter(out_pdf)
    mediabox = pymupdf.paper_rect("letter")
    where = mediabox + (54, 54, -54, -54)
    more = True
    while more:
        dev = writer.begin_page(mediabox)
        more, _ = story.place(where)
        story.draw(dev)
        writer.end_page()
    story = None
    writer.close()
    n = pymupdf.open(out_pdf).page_count
    print(f"{md_path} -> {n} pages")
    return out_pdf, n

# ---------- 1. render markdown docs ----------
docs = []  # (title, path, pagecount)
t, n = md_to_pdf("TANK_FARM_RECEPTOR_AND_PERMIT_MEMO.md", "memo.pdf", "Report")
docs.append(("1. Research Report (memo + methodology + references)", t, n))
t, n = md_to_pdf("FACTCHECK.md", "fc.pdf", "Fact-check")
docs.append(("2. Fact-Check Log", t, n))

# ---------- 2. assemble binder ----------
DOCSETS = []

out = pymupdf.open()
toc = []  # (level, title, page)
cover = pymupdf.open()
page = cover.new_page(width=612, height=792)
page.insert_font(fontname="helv", fontfile=None) if False else None
page.insert_text((72, 200), "SOUTH PORTLAND TANK FARMS", fontsize=26, fontname="hebo", color=(0.1,0.23,0.36))
page.insert_text((72, 235), "Sensitive Receptors & Permit Renewals", fontsize=17, fontname="helv", color=(0.2,0.2,0.2))
page.insert_text((72, 260), "Unified Evidence Binder", fontsize=17, fontname="helv", color=(0.2,0.2,0.2))
page.draw_line((72, 280), (540, 280), color=(0.1,0.23,0.36), width=2)
lines = [
    "Prepared for: Protect South Portland",
    "Compiled: September 24, 2026",
    "",
    "Contents:",
    "  1. Research report (executive summary, findings, methodology)",
    "  2. Fact-check log (claim-by-claim verification with direct evidence)",
    "",
    "Source documents are not appended; every source is cited in the report's",
    "References section with its DEP archive URL or official provenance, and the",
    "fact-check log quotes the direct evidence relied on for each claim.",
    "",
    "AI disclosure: research compiled by an AI agent under human steering;",
    "all findings verified against the primary documents cited in References.",
]
y = 320
for ln in lines:
    fs = 11 if ln.startswith("Contents") else 10.5
    page.insert_text((72 if not ln.startswith("  ") else 90, y), ln, fontsize=fs, fontname="helv", color=(0.15,0.15,0.15))
    y += 20
page.insert_text((72, 720), "protectsouthportland.com  |  fact-check log & datasets: projects/psp/sleuthing-tank-farms/", fontsize=8, fontname="helv", color=(0.4,0.4,0.4))
out.insert_pdf(cover)
toc.append((1, "Cover", 1))
pageno = 2

# dividers + docs
def divider(title, subtitle=""):
    d = pymupdf.open()
    p = d.new_page(width=612, height=792)
    p.insert_text((72, 340), title[:80], fontsize=18, fontname="hebo", color=(0.1,0.23,0.36))
    p.insert_text((72, 372), "official source documents - appended", fontsize=10, fontname="helv", color=(0.4,0.4,0.4))
    return d

for title, path, n in docs:
    src = pymupdf.open(path)
    out.insert_pdf(src)
    toc.append((1, title, pageno))
    pageno += n
    src.close()

for bm, label, files in DOCSETS:
    if not files:
        continue
    d = divider(bm)
    out.insert_pdf(d)
    toc.append((1, bm, pageno))
    pageno += 1
    d.close()
    for ftitle, fpath in files:
        src = pymupdf.open(fpath)
        n = src.page_count
        out.insert_pdf(src)
        toc.append((2, f"{ftitle}  [{n} pp]", pageno))
        pageno += n
        src.close()

out.set_toc(toc)
out.set_metadata({"title": "South Portland Tank Farms: Sensitive Receptors & Permit Renewals - Evidence Binder",
                  "author": "Protect South Portland (compiled with AI assistance, human-steered)",
                  "subject": "Receptor proximity analysis, permit renewal dates, source documents",
                  "keywords": "South Portland, tank farms, VOC, HAP, air licenses, receptors"})
out.save(os.path.join(OUT, OUT_FILE), deflate=True, garbage=3)
for f in ["binder_tmp.html", "binder_tmp.pdf", "memo.pdf", "fc.pdf", "dataset.md", "TANK_FARM_RECEPTOR_AND_PERMIT_MEMO_render.pdf", "FACTCHECK_render.pdf"]:
    fp = os.path.join(OUT, f)
    if os.path.exists(fp):
        os.remove(fp)
print(f"\nBinder: {out.page_count} pages, {len(toc)} bookmarks -> outputs/{OUT_FILE}")