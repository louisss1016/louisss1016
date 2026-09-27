#!/usr/bin/env python3
"""Generate an ASCII-art contribution graph (·░▒▓█ density ramp, terminal green).

Reads the user's real contribution calendar via GitHub GraphQL (gh api graphql),
maps each cell to a density character, and renders a green-on-black terminal SVG.
Runs both locally and inside GitHub Actions (GH_TOKEN is set there).
"""
import json
import os
import subprocess
import sys

MONO = "Consolas, 'Courier New', monospace"
WIDTH = 900
HEIGHT = 250


def fetch_data(login):
    query = (
        "query($login:String!){user(login:$login){contributionsCollection"
        "{contributionCalendar{totalContributions weeks{contributionDays"
        "{contributionCount}}}}}}"
    )
    r = subprocess.run(
        ["gh", "api", "graphql", "-f", f"query={query}", "-f", f"login={login}"],
        capture_output=True, text=True,
    )
    if r.returncode != 0:
        raise SystemExit(f"graphql failed: {r.stderr[:400]}")
    return json.loads(r.stdout)


def build_matrix(data):
    cal = data["data"]["user"]["contributionsCollection"]["contributionCalendar"]
    rows = [[] for _ in range(7)]
    for w in cal["weeks"]:
        days = list(w["contributionDays"])
        while len(days) < 7:  # the current (last) week may be partial
            days.append({"contributionCount": 0})
        for i, d in enumerate(days):
            rows[i].append(d["contributionCount"])
    return rows, cal["totalContributions"]


def level(count):
    if count == 0:
        return "\u00b7", "#103020"   # ·
    if count <= 4:
        return "\u2591", "#1E5A2A"   # ░
    if count <= 9:
        return "\u2592", "#2E8B3E"   # ▒
    if count <= 19:
        return "\u2593", "#40C463"   # ▓
    return "\u2588", "#00FF41"       # █


def gen_svg(rows, total):
    FONT = 15
    LINE_H = 18
    ncols = len(rows[0])
    char_w = FONT * 0.6
    graph_w = ncols * char_w
    x0 = round((WIDTH - graph_w) / 2)
    y0 = 78

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" '
        f'viewBox="0 0 {WIDTH} {HEIGHT}" role="img" aria-label="contribution graph">',
        "<defs>",
        '<pattern id="scan" width="1" height="4" patternUnits="userSpaceOnUse">',
        '<rect width="1" height="1.5" fill="#00FF41" fill-opacity="0.04"/>',
        "</pattern>",
        "</defs>",
        '<rect width="900" height="250" fill="#000000"/>',
        '<rect width="900" height="250" fill="url(#scan)"/>',
        f'<text x="40" y="46" font-family="{MONO}" font-size="13" fill="#00B32C">'
        f'$ contribution-graph  --year 1  (total {total})</text>',
    ]

    for r, row in enumerate(rows):
        y = y0 + r * LINE_H
        tspans = []
        for c in row:
            ch, color = level(c)
            tspans.append(f'<tspan fill="{color}">{ch}</tspan>')
        parts.append(
            f'<text x="{x0}" y="{y}" font-family="{MONO}" font-size="{FONT}" '
            f'xml:space="preserve">' + "".join(tspans) + "</text>"
        )

    parts.append(
        f'<text x="40" y="{y0 + 7 * LINE_H + 18}" font-family="{MONO}" font-size="12" '
        f'fill="#00B32C">less <tspan fill="#103020">\u00b7</tspan> '
        f'<tspan fill="#1E5A2A">\u2591</tspan> '
        f'<tspan fill="#2E8B3E">\u2592</tspan> '
        f'<tspan fill="#40C463">\u2593</tspan> '
        f'<tspan fill="#00FF41">\u2588</tspan> more</text>'
    )
    parts.append("</svg>")
    return "\n".join(parts)


def main():
    login = sys.argv[1] if len(sys.argv) > 1 else "louisss1016"
    data = fetch_data(login)
    rows, total = build_matrix(data)
    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "dist")
    os.makedirs(out_dir, exist_ok=True)
    out = os.path.join(out_dir, "ascii-contrib.svg")
    with open(out, "w", encoding="utf-8") as f:
        f.write(gen_svg(rows, total))
    print(f"wrote {out}  (weeks={len(rows[0])}, total={total})")


if __name__ == "__main__":
    main()
