"""Render the profile's original vector artwork. Requires fontTools.

Usage: python scripts/render_profile.py --font-dir C:/Windows/Fonts
Fonts are used to outline display lettering; no font files are distributed.
"""
from pathlib import Path
import argparse
import math
from html import escape
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets' / 'studio'
INK, PAPER, RED = '#111113', '#f1f0ea', '#f26048'


class Artwork:
    def __init__(self, width, height, title, bg):
        self.parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="{escape(title)}">', f'<title>{escape(title)}</title>', f'<rect width="{width}" height="{height}" fill="{bg}"/>']

    def add(self, element):
        self.parts.append(element)

    def line(self, x1, y1, x2, y2, color, width=1, opacity=1):
        self.add(f'<path d="M{x1} {y1}L{x2} {y2}" fill="none" stroke="{color}" stroke-width="{width}" opacity="{opacity}"/>')

    def label(self, value, x, y, size=12, color='#969690', spacing=1.4):
        self.add(f'<text x="{x}" y="{y}" fill="{color}" font-family="Arial,Helvetica,sans-serif" font-size="{size}" letter-spacing="{spacing}">{escape(value)}</text>')

    def lettering(self, value, x, y, size, font, color, tracking=0):
        gs = font.getGlyphSet()
        cmap = font.getBestCmap()
        scale = size / font['head'].unitsPerEm
        cursor = 0
        paths = []
        for char in value:
            glyph = gs[cmap[ord(char)]]
            pen = SVGPathPen(gs)
            glyph.draw(pen)
            paths.append(f'<path transform="translate({cursor:.2f} 0)" d="{pen.getCommands()}"/>')
            cursor += glyph.width + tracking / scale
        self.add(f'<g fill="{color}" transform="translate({x} {y}) scale({scale:.6f} {-scale:.6f})">'+''.join(paths)+'</g>')

    def save(self, name):
        OUT.mkdir(parents=True, exist_ok=True)
        (OUT / name).write_text('\n'.join(self.parts + ['</svg>']), encoding='utf-8')


def sculpture(a, cx, cy, scale=1, dark=True):
    """Projected torus: many meridians, each with depth-weighted line opacity."""
    pieces = []
    for j in range(64):
        u = 2 * math.pi * j / 64
        points, depths = [], []
        for k in range(81):
            v = 2 * math.pi * k / 80
            # A pinched inner radius creates a sculptural, asymmetric silhouette.
            r = 78 + 33 * math.cos(v)
            x, y, z = r * math.cos(u), r * math.sin(u), 33 * math.sin(v)
            ay = 0.68
            x, z = x * math.cos(ay) + z * math.sin(ay), -x * math.sin(ay) + z * math.cos(ay)
            ax = 0.88
            y, z = y * math.cos(ax) - z * math.sin(ax), y * math.sin(ax) + z * math.cos(ax)
            az = -0.38
            x, y = x * math.cos(az) - y * math.sin(az), x * math.sin(az) + y * math.cos(az)
            points.append(f'{cx+x*scale:.2f},{cy+y*scale:.2f}')
            depths.append(z)
        depth = sum(depths) / len(depths)
        opacity = 0.22 + (depth + 90) / 180 * 0.65
        color = PAPER if dark else INK
        pieces.append((depth, f'<polyline points="{" ".join(points)}" fill="none" stroke="{color}" stroke-width="0.9" opacity="{opacity:.3f}"/>'))
    for _, path in sorted(pieces):
        a.add(path)


def cover(fonts, theme, mobile=False):
    dark = theme == 'dark'
    bg, fg, muted, line = (INK, PAPER, '#b3b3ab', '#363638') if dark else (PAPER, INK, '#5c5c56', '#cecec6')
    w, h = (600, 560) if mobile else (1000, 460)
    a = Artwork(w, h, 'Louisss — Backend engineering, AI agent systems, open source.', bg)
    pad = 40 if mobile else 48
    a.add(f'<path d="M{pad} 30v18h18M{pad+6} 30v12h12" fill="none" stroke="{RED}" stroke-width="3"/>')
    a.label('LOUISSS / ENGINEERING', pad+32, 43, 12, fg, 1.3)
    if not mobile:
        a.label('BACKEND · AGENTS · OPEN SOURCE', 665, 43, 11, muted, 1.3)
    a.line(pad, 66, w-pad, 66, line)
    a.lettering('LOUISSS', pad-5, 175 if mobile else 211, 111 if mobile else 190, fonts['bold'], fg, -5 if mobile else -8)
    a.add(f'<rect x="{508 if mobile else 846}" y="{162 if mobile else 192}" width="{13 if mobile else 19}" height="{13 if mobile else 19}" fill="{RED}"/>')
    if mobile:
        a.label('JAVA / PYTHON / AI SYSTEMS', pad, 218, 15, muted, 1.8)
        sculpture(a, 400, 370, 1.18, dark)
        a.lettering('Built with', pad, 306, 35, fonts['regular'], fg, -1)
        a.lettering('intent.', pad, 350, 42, fonts['italic'], fg, -0.6)
        a.line(pad, 502, w-pad, 502, line)
        a.label('BUILD QUIETLY. SHIP OFTEN.', pad, 534, 12, muted, 1.4)
        a.label('01 / INDEX', 456, 534, 11, muted, 0.5)
    else:
        a.lettering('Built with', pad, 302, 48, fonts['regular'], fg, -1.4)
        a.lettering('intent.', pad+221, 302, 53, fonts['italic'], fg, -1)
        a.label('Backend engineering. AI agent systems.', pad, 343, 18, muted, 0)
        a.label('Reliable systems. Real contributions.', pad, 372, 18, muted, 0)
        sculpture(a, 775, 314, 1.05, dark)
        a.line(pad, 421, w-pad, 421, line)
        a.label('BUILD QUIETLY. SHIP OFTEN.', pad, 445, 10, muted, 1.5)
        a.label('JAVA / PYTHON', 443, 445, 10, muted, 1.5)
        a.label('01 / PERSONAL INDEX', 809, 445, 10, muted, 1)
    a.save(f'cover-{theme}{"-mobile" if mobile else ""}.svg')


CONTRIBUTIONS = {
    'deerflow': ('01 / BYTEDANCE', 'deer-flow', 'Windows-safe test isolation.', 'PYTHON / CROSS-PLATFORM CI', '6439'),
    'folio': ('02 / HELSOME', 'folio', 'Resilience at the data layer.', 'TYPESCRIPT / PROVIDER RELIABILITY', '72'),
    'ouroboros': ('03 / Q00', 'ouroboros', 'The right model, at the right stage.', 'PYTHON / AGENT CONFIGURATION', '2462'),
}


def contribution(fonts, kind, theme, mobile=False):
    dark = theme == 'dark'
    bg, fg, muted, line = ('#171719', PAPER, '#aaa9a2', '#454548') if dark else ('#e9e8e1', INK, '#62625b', '#b7b7af')
    owner, name, title, category, number = CONTRIBUTIONS[kind]
    w, h = (600, 340) if mobile else (1000, 260)
    a = Artwork(w, h, f'{owner.split(" / ")[1]}/{name} — {title} Merged PR #{number}.', bg)
    p = 32 if mobile else 38
    a.label(owner, p, 35, 12, muted, 1.5)
    a.label(f'MERGED / #{number}', w-215, 35, 12, RED, 1)
    a.add(f'<path d="M{w-55} 22h16v16m-17 1 17-17" fill="none" stroke="{fg}" stroke-width="1.7"/>')
    a.lettering(name, p-2, 109, 56 if mobile else 58, fonts['bold'], fg, -2.2)
    a.label(title, p, 150, 23 if mobile else 25, fg, -.3)
    a.label(category, p, h-27, 11 if mobile else 12, muted, 1)
    cx, cy, scale = (412, 238, .78) if mobile else (804, 148, 1)
    a.add(f'<g transform="translate({cx} {cy}) scale({scale})">')

    def box(x, y, width, height, label, accent=False):
        stroke = RED if accent else line
        a.add(f'<rect x="{x}" y="{y}" width="{width}" height="{height}" rx="3" fill="{bg}" stroke="{stroke}"/>')
        a.label(label, x+10, y+height/2+4, 11, fg if accent else muted, .7)

    def connector(d, accent=False):
        a.add(f'<path d="{d}" fill="none" stroke="{RED if accent else line}" stroke-width="1.3"/>')

    if kind == 'deerflow':
        # A bounded child environment and its five policy checks.
        a.add(f'<rect x="-120" y="-57" width="240" height="112" rx="4" fill="none" stroke="{line}" stroke-dasharray="3 5"/>')
        box(-104, -41, 83, 32, 'BASE ENV')
        connector('M-21-25H18', True)
        box(18, -41, 86, 32, 'PYTEST', True)
        connector('M61-9V11H-83V24')
        for x in [-83,-42,-1,40,81]:
            connector(f'M{x} 11V24')
            a.add(f'<rect x="{x-9}" y="24" width="18" height="18" rx="2" fill="{bg}" stroke="{line}"/>')
            connector(f'M{x-4} 32l3 3 5-6',True)
    elif kind == 'folio':
        box(-131,-48,86,32,'REQUEST')
        connector('M-45-32H-13')
        box(-13,-48,83,32,'PRIMARY')
        connector('M70-32H114V39H70',True)
        box(-13,23,83,32,'BACKUP',True)
        connector('M-13 39H-88V-16',True)
        a.add(f'<circle cx="114" cy="-32" r="4" fill="{RED}"/>')
        a.label('FAILOVER', -3, 2, 9, muted, 1.2)
    else:
        box(-132,-49,77,30,'ENV')
        box(-132,19,77,30,'CONFIG')
        connector('M-55-34H-32V0H-9M-55 34H-32V0')
        box(-9,-18,88,36,'EXECUTE',True)
        connector('M79 0H104V-36H134M104 0V36H134',True)
        a.add(f'<circle cx="138" cy="-36" r="4" fill="{RED}"/><circle cx="138" cy="36" r="4" fill="{RED}"/>')
        a.label('CLI', 106, -48, 10, muted, .5)
        a.label('API', 106, 58, 10, muted, .5)
    a.add('</g>')
    a.save(f'{kind}-{theme}{"-mobile" if mobile else ""}.svg')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--font-dir', type=Path, required=True)
    args = parser.parse_args()
    fonts = {key: TTFont(args.font_dir / file) for key, file in {'bold':'arialbd.ttf','regular':'arial.ttf','italic':'georgiai.ttf'}.items()}
    for theme in ['dark','light']:
        for mobile in [False,True]:
            cover(fonts, theme, mobile)
            for kind in CONTRIBUTIONS:
                contribution(fonts, kind, theme, mobile)
    print('Rendered 16 profile assets (cover and three contributions, desktop/mobile, dark/light).')


if __name__ == '__main__':
    main()
