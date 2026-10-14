"""Gantt chart with Arabic labels, right-to-left by default.

Usage:
    python gantt.py plan.json out.png [--font PATH] [--ltr] [--reshape]

plan.json:
{
  "title": "",                         # optional
  "phases": {"المرحلة الأولى": "#1F3A5F", "المرحلة الثانية": "#8A6D3B"},
  "tasks": [
    {"name": "تحليل الوضع الراهن", "start": "2026-01-01", "end": "2026-03-01", "phase": "المرحلة الأولى"}
  ],
  "milestones": [{"name": "اعتماد المجلس", "date": "2026-07-15"}],
  "date_format": "%m/%Y"               # optional tick format
}

--reshape: only for older matplotlib that does not shape Arabic by itself.
Render once without it and look at the image: if letters are disconnected, re-run with it.
"""
import json
import sys
import argparse
from datetime import date

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib import font_manager as fm
from matplotlib.patches import Patch


def main():
    p = argparse.ArgumentParser()
    p.add_argument("plan")
    p.add_argument("out")
    p.add_argument("--font", default=None)
    p.add_argument("--ltr", action="store_true", help="time flows left to right")
    p.add_argument("--reshape", action="store_true")
    a = p.parse_args()

    plan = json.load(open(a.plan, encoding="utf-8"))
    fp = fm.FontProperties(fname=a.font) if a.font else fm.FontProperties(family="IBM Plex Sans Arabic")

    if a.reshape:
        import arabic_reshaper
        from bidi.algorithm import get_display
        ar = lambda s: get_display(arabic_reshaper.reshape(s))
    else:
        ar = lambda s: s

    tasks = plan.get("tasks", [])
    miles = plan.get("milestones", [])
    phases = plan.get("phases", {})
    rows = [t["name"] for t in tasks] + [m["name"] for m in miles]
    n = len(rows)

    fig, ax = plt.subplots(figsize=(10, 0.55 * n + 1.4), dpi=200)
    for i, t in enumerate(tasks):
        s, e = date.fromisoformat(t["start"]), date.fromisoformat(t["end"])
        ax.barh(n - 1 - i, (e - s).days, left=mdates.date2num(s), height=0.5,
                color=phases.get(t.get("phase"), "#1F3A5F"))
    for j, m in enumerate(miles):
        ax.plot(mdates.date2num(date.fromisoformat(m["date"])), n - 1 - len(tasks) - j,
                marker="D", color="#B03A2E", markersize=9)

    ax.set_yticks(range(n))
    ax.set_yticklabels([ar(r) for r in reversed(rows)], fontproperties=fp, fontsize=11)
    if not a.ltr:
        ax.yaxis.tick_right()
        ax.invert_xaxis()
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter(plan.get("date_format", "%m/%Y")))
    for lbl in ax.get_xticklabels():
        lbl.set_fontproperties(fp)
    ax.grid(axis="x", color="#E3E7EB")
    ax.set_axisbelow(True)
    for s in ["top", "left" if not a.ltr else "right", "bottom"]:
        ax.spines[s].set_visible(False)
    if phases:
        ax.legend(handles=[Patch(color=c, label=ar(k)) for k, c in phases.items()],
                  prop=fp, loc="upper left" if not a.ltr else "upper right", frameon=False)
    if plan.get("title"):
        ax.set_title(ar(plan["title"]), fontproperties=fp, fontsize=13,
                     loc="right" if not a.ltr else "left")
    plt.tight_layout()
    plt.savefig(a.out, facecolor="white")
    print("saved", a.out)


if __name__ == "__main__":
    main()
