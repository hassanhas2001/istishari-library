#!/usr/bin/env python3
"""Build a right-to-left Arabic infographic as one self-contained HTML file.

Usage:
    python3 build_infographic.py spec.json out.html [--png out.png] [--font path.woff2]

The HTML has no external requests: no CDN, no web fonts, no icon service.
--font embeds a local font file (woff2/ttf) as a data URI; otherwise a system
Arabic font stack is used. --png renders a screenshot with Playwright if it is
installed; if not, the HTML is still written and a note is printed.
See ../references/spec.md for the spec format.
"""
import argparse
import base64
import html
import json
import pathlib
import sys

AR_DIGITS = str.maketrans("0123456789.,%", "٠١٢٣٤٥٦٧٨٩٫٬٪")
NEUTRAL = {"primary": "#1F4E79", "accent": "#C8962E", "text": "#1F2933",
           "muted": "#5F6673", "bg": "#FFFFFF", "panel": "#F3F5F8"}
FONT_STACK = "'IBM Plex Sans Arabic','Noto Sans Arabic','Tajawal','Segoe UI','Tahoma',sans-serif"
MISSING = "[يُستكمل]"


def esc(s):
    return html.escape(str(s)) if s is not None else ""


def fmt(value, digits):
    """Format a number with grouping; strings pass through. None -> MISSING."""
    if value is None or value == "":
        return None
    if isinstance(value, (int, float)):
        s = f"{value:,.0f}" if float(value).is_integer() else f"{value:,.1f}"
    else:
        s = str(value)
    return s.translate(AR_DIGITS) if digits == "arabic" else s


def val_html(item, digits, cls="value"):
    v = fmt(item.get("value"), digits)
    if v is None:
        return f'<span class="{cls} missing">{MISSING}</span>'
    unit = f'<span class="unit">{esc(item["unit"])}</span>' if item.get("unit") else ""
    return f'<span class="{cls}"><bdi>{esc(v)}</bdi>{unit}</span>'


def t_kpi(spec, d):
    cells = []
    for it in spec["items"]:
        note = f'<div class="note">{esc(it.get("note"))}</div>' if it.get("note") else ""
        cells.append(f'<div class="card">{val_html(it, d)}<div class="label">{esc(it["label"])}</div>{note}</div>')
    n = len(cells)
    cols = n if n <= 4 else (3 if n in (5, 6, 9) else 4)
    return f'<div class="kpi" style="grid-template-columns:repeat({cols},1fr)">{"".join(cells)}</div>'


def t_bars(spec, d):
    items = spec["items"]
    nums = [it["value"] for it in items if isinstance(it.get("value"), (int, float))]
    top = max(nums) if nums else 1
    rows = []
    for it in items:
        v = it.get("value")
        w = (v / top * 100) if isinstance(v, (int, float)) and top else 0
        rows.append(f'<div class="bar-row"><div class="bar-label">{esc(it["label"])}</div>'
                    f'<div class="track"><div class="fill" style="width:{w:.1f}%"></div></div>'
                    f'{val_html(it, d, "bar-value")}</div>')
    return f'<div class="bars">{"".join(rows)}</div>'


def t_steps(spec, d):
    items = spec["items"]
    vertical = len(items) > 5
    parts = []
    for i, it in enumerate(items, 1):
        num = str(i).translate(AR_DIGITS) if d == "arabic" else str(i)
        note = f'<div class="note">{esc(it.get("note"))}</div>' if it.get("note") else ""
        val = val_html(it, d) if "value" in it else ""
        parts.append(f'<div class="step"><div class="num">{num}</div><div class="label">{esc(it["label"])}</div>{val}{note}</div>')
    return f'<div class="steps{" vertical" if vertical else ""}">{"".join(parts)}</div>'


def t_chain(spec, d):
    # Results chain read right to left: first item (e.g. inputs) on the right, impact on the left.
    parts = []
    for it in spec["items"]:
        note = f'<div class="note">{esc(it.get("note"))}</div>' if it.get("note") else ""
        val = val_html(it, d) if "value" in it else ""
        parts.append(f'<div class="link"><div class="label">{esc(it["label"])}</div>{val}{note}</div>')
    return f'<div class="chain">{"".join(parts)}</div>'


def t_compare(spec, d):
    items = spec["items"]
    cols = 2 if len(items) in (2, 4) else len(items)
    boxes = []
    for i, it in enumerate(items):
        pts = "".join(f"<li>{esc(p)}</li>" for p in it.get("points", []))
        boxes.append(f'<div class="box b{i % 4}"><div class="box-h">{esc(it["label"])}</div><ul>{pts}</ul></div>')
    return f'<div class="compare" style="grid-template-columns:repeat({cols},1fr)">{"".join(boxes)}</div>'


TEMPLATES = {"kpi": t_kpi, "bars": t_bars, "steps": t_steps, "chain": t_chain, "compare": t_compare}

CSS = """
*{box-sizing:border-box;margin:0;padding:0}
body{background:var(--bg);color:var(--text);font-family:var(--font);}
.ig{width:var(--w);padding:48px 56px;background:var(--bg)}
h1{font-size:34px;font-weight:700;color:var(--primary);line-height:1.4}
.sub{font-size:19px;color:var(--muted);margin-top:6px}
.body{margin-top:36px}
.src{margin-top:32px;font-size:14px;color:var(--muted);border-top:1px solid var(--panel);padding-top:12px}
.value{display:block;font-size:44px;font-weight:700;color:var(--primary);line-height:1.2}
.unit{font-size:.5em;font-weight:500;margin-inline-start:6px;color:var(--muted)}
.missing{color:var(--muted);font-size:22px;font-weight:500}
.label{font-size:20px;font-weight:700;margin-top:6px;line-height:1.5}
.note{font-size:16px;color:var(--muted);margin-top:4px;line-height:1.6}
.kpi{display:grid;gap:20px}
.card{background:var(--panel);border-radius:14px;padding:24px;border-top:5px solid var(--primary)}
.card:nth-child(even){border-top-color:var(--accent)}
.bars{display:flex;flex-direction:column;gap:18px}
.bar-row{display:flex;align-items:center;gap:16px}
.bar-label{width:24%;font-size:19px;font-weight:700}
.track{flex:1;height:30px;background:var(--panel);border-radius:6px;overflow:hidden}
.fill{height:100%;background:var(--primary);border-radius:6px}
.bar-value{width:14%;font-size:22px;font-weight:700;color:var(--primary)}
.steps{display:flex;gap:16px;align-items:stretch}
.step{flex:1;position:relative;background:var(--panel);border-radius:14px;padding:22px 20px}
.steps:not(.vertical) .step:not(:last-child)::after{content:"";position:absolute;inset-inline-end:-14px;top:50%;
 border:8px solid transparent;border-inline-start-color:var(--accent);transform:translateY(-50%)}
.steps.vertical{flex-direction:column}
.num{width:42px;height:42px;border-radius:50%;background:var(--primary);color:#fff;font-weight:700;
 font-size:20px;display:flex;align-items:center;justify-content:center}
.steps .value{font-size:30px;margin-top:8px}
.chain{display:flex;gap:0;align-items:stretch}
.link{flex:1;background:var(--primary);color:#fff;padding:22px 34px 22px 26px;position:relative;
 clip-path:polygon(100% 0,14px 0,0 50%,14px 100%,100% 100%,calc(100% - 14px) 50%)}
.link:first-child{clip-path:polygon(100% 0,14px 0,0 50%,14px 100%,100% 100%)}
.link .note,.link .value,.link .unit{color:#fff}
.link:nth-child(even){background:var(--accent);color:var(--text)}
.link:nth-child(even) .note,.link:nth-child(even) .value,.link:nth-child(even) .unit{color:var(--text)}
.link .value{font-size:28px}
.compare{display:grid;gap:18px}
.box{background:var(--panel);border-radius:14px;padding:22px;border-inline-start:6px solid var(--primary)}
.box.b1,.box.b3{border-inline-start-color:var(--accent)}
.box-h{font-size:21px;font-weight:700;margin-bottom:10px}
.box ul{padding-inline-start:22px;font-size:17px;line-height:1.9}
"""


def _lum(hex_):
    h = hex_.lstrip("#")
    c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    c = [x / 12.92 if x <= 0.03928 else ((x + 0.055) / 1.055) ** 2.4 for x in c]
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]


def contrast(a, b):
    la, lb = sorted((_lum(a), _lum(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def check_contrast(theme):
    pairs = [("primary", "#FFFFFF", "white text on primary"), ("text", "accent", "text on accent"),
             ("text", "panel", "text on panel"), ("primary", "panel", "values on panel")]
    for a, b, what in pairs:
        ca, cb = theme.get(a, a), theme.get(b, b)
        try:
            r = contrast(ca, cb)
        except (ValueError, IndexError):
            continue
        if r < 4.5:
            print(f"Contrast warning: {what} is {r:.1f}:1 (needs 4.5:1)", file=sys.stderr)


def build(spec, font_path=None):
    if spec.get("template") not in TEMPLATES:
        raise SystemExit(f"template must be one of {sorted(TEMPLATES)}")
    if not spec.get("items"):
        raise SystemExit("items is empty")
    theme = {**NEUTRAL, **spec.get("theme", {})}
    check_contrast(theme)
    font_css, family = "", theme.get("font") or FONT_STACK
    if font_path:
        p = pathlib.Path(font_path)
        mime = "font/woff2" if p.suffix == ".woff2" else "font/ttf"
        b64 = base64.b64encode(p.read_bytes()).decode()
        font_css = f"@font-face{{font-family:'EmbeddedArabic';src:url(data:{mime};base64,{b64})}}"
        family = "'EmbeddedArabic'," + FONT_STACK
    d = spec.get("digits", "keep")
    width = int(spec.get("width", 1200))
    vars_ = (f":root{{--w:{width}px;--font:{family};" +
             "".join(f"--{k}:{v};" for k, v in theme.items() if k != "font") + "}")
    sub = f'<div class="sub">{esc(spec["subtitle"])}</div>' if spec.get("subtitle") else ""
    src = f'<div class="src">المصدر: {esc(spec["source"])}</div>' if spec.get("source") else ""
    body = TEMPLATES[spec["template"]](spec, d)
    return (f'<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8">'
            f'<meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>{esc(spec.get("title", "إنفوجرافيك"))}</title>'
            f'<style>{font_css}{vars_}{CSS}</style></head><body>'
            f'<div class="ig" id="infographic"><h1>{esc(spec.get("title", ""))}</h1>{sub}'
            f'<div class="body">{body}</div>{src}</div></body></html>')


def to_png(html_path, png_path):
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("Playwright not installed: HTML written, PNG skipped.", file=sys.stderr)
        return False
    with sync_playwright() as p:
        b = p.chromium.launch()
        page = b.new_page(device_scale_factor=2)
        page.goto(pathlib.Path(html_path).resolve().as_uri())
        page.evaluate("document.fonts.ready")
        page.locator("#infographic").screenshot(path=png_path)
        b.close()
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("spec")
    ap.add_argument("out")
    ap.add_argument("--png")
    ap.add_argument("--font")
    a = ap.parse_args()
    spec = json.loads(pathlib.Path(a.spec).read_text(encoding="utf-8"))
    pathlib.Path(a.out).write_text(build(spec, a.font), encoding="utf-8")
    print(f"HTML: {a.out}")
    if a.png and to_png(a.out, a.png):
        print(f"PNG: {a.png}")


if __name__ == "__main__":
    main()
