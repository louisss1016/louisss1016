# Profile artwork

The second design uses an editorial layout: large outlined lettering, charcoal and warm white surfaces, a restrained vermilion accent, and geometric illustrations related to each project's purpose.

## Assets

`assets/studio/` contains twelve SVG files: cover, radar and navigator, each in dark/light and desktop/mobile variants. The README's picture sources select the appropriate variant. All essential meaning is also present in native text or image alternatives.

- Desktop cover: 1000 × 460.
- Mobile cover: 600 × 560, with a separate composition.
- Desktop project covers: 1000 × 235.
- Mobile project covers: 600 × 300.
- Accent: #f26048; charcoal: #111113; warm white: #f1f0ea.
- Display lettering is outlined, so remote rendering does not depend on installed fonts.

The loop is a projected torus. The radar represents contribution discovery; the layered planes represent staged agent workflows. The images are static, with no external requests or scripts. Links and disclosures use native GitHub controls.

## Rebuild

Install fontTools in your local Python environment, then provide a font directory containing `arial.ttf`, `arialbd.ttf`, and `georgiai.ttf`:

```sh
python scripts/render_profile.py --font-dir /path/to/fonts
```

Font files are not included in this repository. Rendering writes only to `assets/studio/`. The existing contribution-calendar workflow remains independent.

## Validation

The SVGs were parsed as XML, all README image references were checked, and the GitHub Markdown renderer preserved the picture sources and three disclosures. Desktop dark/light and the separate mobile composition were inspected in a browser. The contributions reference previously verified merged PRs.
