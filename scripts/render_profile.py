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
        a.label('Small tools. Real contributions.', pad, 372, 18, muted, 0)
        sculpture(a, 775, 314, 1.05, dark)
        a.line(pad, 421, w-pad, 421, line)
        a.label('BUILD QUIETLY. SHIP OFTEN.', pad, 445, 10, muted, 1.5)
        a.label('JAVA / PYTHON', 443, 445, 10, muted, 1.5)
        a.label('01 / PERSONAL INDEX', 809, 445, 10, muted, 1)
    a.save(f'cover-{theme}{"-mobile" if mobile else ""}.svg')


def project(fonts, kind, theme, mobile=False):
    dark = theme == 'dark'
    bg, fg, muted, line = ('#171719', PAPER, '#aaa9a2', '#39393c') if dark else ('#e9e8e1', INK, '#62625b', '#c5c5be')
    w, h = (600, 300) if mobile else (1000, 235)
    a = Artwork(w, h, 'Contrib Radar — discover worthwhile open-source contributions' if kind=='radar' else 'Vibecoding Navigator — plan, build, verify and ship', bg)
    p = 32 if mobile else 38
    a.label('01 / OPEN-SOURCE INTELLIGENCE' if kind=='radar' else '02 / AGENT WORKFLOW', p, 34, 11 if mobile else 12, muted, 1.4)
    title = 'Contrib Radar' if kind=='radar' else 'Vibecoding Navigator'
    a.lettering(title, p-2, 93 if mobile else 104, 37 if mobile else 48, fonts['bold'], fg, -1.3 if mobile else -1.9)
    a.label('Find the right problem.' if kind=='radar' else 'From intent to implementation.', p, 131 if mobile else 145, 20, muted, 0)
    a.label('DISCOVER / EVALUATE / CONTRIBUTE' if kind=='radar' else 'PLAN / BUILD / VERIFY / SHIP', p, 265 if mobile else 201, 11, muted, 1)
    # Actual click target is the enclosing README link, not a script in this image.
    a.add(f'<path d="M{w-56} 38h17v17m-18 1 18-18" fill="none" stroke="{fg}" stroke-width="2"/>')
    if mobile:
        cx, cy, s = 465, 204, .62
    else:
        cx, cy, s = 818, 125, .83
    a.add(f'<g transform="translate({cx} {cy}) scale({s})">')
    if kind == 'radar':
        for r in [28, 55, 82]:
            a.add(f'<circle r="{r}" fill="none" stroke="{line}" stroke-width="1"/>')
        a.line(-100,0,100,0,line)
        a.line(0,-95,0,95,line)
        a.add(f'<path d="M0 0 70-43A82 82 0 0 1 80 18Z" fill="{RED}" opacity="0.1"/>')
        a.line(0,0,70,-43,RED,1.5)
        for x,y in [(-31,18),(-42,-44),(58,44)]:
            a.add(f'<circle cx="{x}" cy="{y}" r="3" fill="{muted}"/>')
        a.add(f'<circle cx="49" cy="-30" r="5" fill="{RED}"/><circle cx="49" cy="-30" r="10" fill="none" stroke="{RED}" stroke-width="1"/>')
    else:
        for offset,fill in [(33,bg),(0,bg),(-33,bg)]:
            a.add(f'<path d="M0 {offset-40} 88 {offset} 0 {offset+40}-88 {offset}Z" fill="{fill}" stroke="{line}" stroke-width="1.5"/>')
        a.add(f'<path d="M-48-33 0-55 48-33 0-11Z" fill="none" stroke="{RED}" stroke-width="1.5"/>')
        a.add(f'<path d="M0-11V73" stroke="{RED}" stroke-width="1.5" stroke-dasharray="3 5"/>')
        a.add(f'<circle cy="73" r="4" fill="{RED}"/>')
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
            for kind in ['radar','navigator']:
                project(fonts, kind, theme, mobile)
    print('Rendered 12 original SVG assets (desktop/mobile, dark/light).')


if __name__ == '__main__':
    main()
