# Profile design

## Current layout

The current README keeps a short introduction and uses a compact native GitHub table for contributions, following the user's supplied reference. Rows contain the repository owner's avatar, a short project description, repository stars, primary language, and the author's merged upstream PR count. Five repositories are visible, sorted by stars; the remaining three are inside a native disclosure. Language badges are local SVG assets from Shields.io; repository avatars are served by GitHub.

Data was verified on 2026-10-26 using GitHub search (`is:pr author:louisss1016 is:merged -user:louisss1016`) and repository metadata: 10 merged PRs across 8 external repositories. Counts link to the matching per-repository search. The README displays its snapshot date; stars represent each repository's popularity, while the merged column represents this author's contributions. The supplied example's counts were not copied.

Reference profiles reviewed on 2026-10-26:

- [MagicCube](https://github.com/MagicCube): concise identity and native pinned repositories.
- [AnnaSuSu](https://github.com/AnnaSuSu): specific contribution summaries with primary evidence links; the main structural reference.
- [LofiSu](https://github.com/LofiSu): compact professional experience and open-source history.

Only information verified for louisss1016 is used; reference authors' credentials are not copied. The old artwork below is retained as an archive and is no longer embedded in the README.

## Archived artwork

The second design uses an editorial layout: large outlined lettering, charcoal and warm white surfaces, a restrained vermilion accent, and geometric illustrations related to each project's purpose.

## Assets

`assets/studio/` now uses sixteen SVG files: the cover and three merged-contribution cards, each in dark/light and desktop/mobile variants. Earlier project artwork is retained but is not displayed. The README's picture sources select the appropriate variant. All essential meaning is also present in native text or image alternatives.

- Desktop cover: 1000 × 460.
- Mobile cover: 600 × 560, with a separate composition.
- Desktop contribution cards: 1000 × 260.
- Mobile contribution cards: 600 × 340.
- Accent: #f26048; charcoal: #111113; warm white: #f1f0ea.
- Display lettering is outlined, so remote rendering does not depend on installed fonts.

The loop is a projected torus. Contribution artwork illustrates a bounded pytest environment, data-provider failover, and stage-specific model selection. The images are static, with no external requests or scripts. Links and disclosures use native GitHub controls.

## Rebuild

Install fontTools in your local Python environment, then provide a font directory containing `arial.ttf`, `arialbd.ttf`, and `georgiai.ttf`:

```sh
python scripts/render_profile.py --font-dir /path/to/fonts
```

Font files are not included in this repository. Rendering writes only to `assets/studio/`. The existing contribution-calendar workflow remains independent.

## Validation

The SVGs were parsed as XML, all README image references were checked, and the GitHub Markdown renderer preserved the picture sources and six disclosures. Desktop dark/light and the separate mobile contribution artwork were rendered and visually inspected. The contributions reference previously verified merged PRs.

## Contribution selection

The profile now leads with merged contributions instead of the two personal skills. The selection balances cross-platform diagnosis and regression CI (deer-flow #6439), backend resilience design (folio #72), and configuration precedence across agent backends (ouroboros #2462). Merge state, authorship and changed code were checked on 2026-10-26. PR descriptions provide historical test reports; these are not presented as newly rerun upstream tests. Each image links to the relevant PR, with scope and verification notes in a native disclosure.
