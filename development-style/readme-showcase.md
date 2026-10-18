# README Showcase

How Obelisk repos dress their READMEs: an animated hero, the product working on screen, live counters and links to the rest of the family. This is the recipe used for obelisk-sky, the org profile, obelisk-design, obelisk-sfu, obelisk-agents and obelisk-apps (October 2026). Copy from those when in doubt; they are the reference.

What still has no real footage is tracked in [Real footage backlog](real-footage-backlog.md).

Tools live in [`tools/readme/`](../tools/readme/): `snap.cjs` (frame-by-frame SVG check) and `tour.py` (animated WebP screenshot tour).

## The page, top to bottom

1. **Hero SVG** (`docs/readme/hero.svg`), full width, linked to the live product. It names the product, says what it does in one line, and moves.
2. **Badges**: one row of `for-the-badge` live counters (status, stars, last commit, commit activity), one row of `flat-square` stack badges.
3. **Link bar**: `<h3>` with the live app, the landing page, obelisk.ar and a jump to "Run it yourself".
4. **Two short paragraphs**: what it is, and the trust boundary (who holds keys, what the server never does).
5. **Proof**: a screenshot tour (`tour.webp`) or an animated scene of the core idea.
6. **How it works**: one animated SVG of the real flow, then numbered steps in a 3-column table.
7. **Feature gallery**: a 2-column table of screenshots, caption row under each image row. Leftovers in a 3-column "…and also" table.
8. **Collapsed extras** in `<details>`: phone shots, controls, file map, Spanish summary.
9. **Run it yourself**: clone + install + dev in one block, then a command table.
10. **The Obelisk family** table, star history, credits, footer SVG.

Keep every existing fact. A runbook or long reference moves to `docs/` and is linked, never deleted.

## Truth rules

- Every claim comes from the repo: code, `AGENTS.md`, docs, commit messages, `package.json`. Event kinds, commands, bot names and file names get checked against the source, not against a brief or the repo description (both have been wrong).
- Animated scenes replay the real thing. Chain Reaction's board states came from porting `engine.ts`; bot replies use the bots' real reply formats; terminal output is the scripts' real output. Invented sample values (an npub, a group id) are fine when labelled as examples; invented features are not.
- No license badge without a LICENSE file. No "made in" line nothing in the repo says.
- Forks keep upstream's README.
- Old screenshots get a caption saying when they are from.

## Brand

| Token | Value | Use |
|---|---|---|
| Lime | `#c5ff6e` → `#b4f953` | The obelisk, accents, the dot in a caption pill |
| Lime shade | `#86c93a`, `#5a8f1f`, stroke `#4f8f1c` | Obelisk's dark face, "Sky" in titles, text on light backgrounds |
| Ink | `#0f2a44` | Text on light, badge `labelColor`, caption pills |
| Near-black | `#0a0a0a` | Dark heroes (org, design, sfu, agents, apps) |
| Sky (obelisk-sky only) | `#8fd3ff`, `#cfeaff`, `#ffffff`, muted `#4b6a88` | Sky's day palette |

- Rendered obelisks are lime, never grey stone. Glow with a radial gradient `#d9ff9c → #b4f953 → transparent`, pulsing radius.
- Product marks come from [`design-system/logos/`](../design-system/logos/). Never instance icons (the purple "P" is a relay's icon, not a product).
- Badges: `color=b4f953&labelColor=0f2a44` (or `0a0a0a` on dark repos). Secondary counters use `8fd3ff`.
- Font stack in SVGs: `Inter, 'Segoe UI', system-ui, -apple-system, Helvetica, Arial, sans-serif`; mono: `ui-monospace, 'SFMono-Regular', Menlo, Consolas, monospace`. No webfonts: an SVG in `<img>` can't load them.

## Animated SVG rules

GitHub shows repo SVGs through `<img>`, so they run as images: SMIL (`<animate>`, `<animateTransform>`, `<animateMotion>`) and CSS `@keyframes` work; scripts, external images, webfonts and links inside the SVG don't.

- **One clock per scene.** Pick a loop length (12 s for a story, 24 s for a day) and give everything that changes together the same `dur` and `keyTimes`. Sky's hero uses `keyTimes="0;0.35;0.45;0.55;0.85;0.95;1"` for day, dusk, night, dawn on the sky, stars, windows, cloud opacity and wall colour alike.
- **Readable at every frame.** Put titles on a frosted card (white at 0.7–0.86) so they read at noon and at midnight.
- **Seamless drift:** a layer of clouds is drawn twice, the second copy offset by the width, and translated `0 → -width`.
- **Discrete swaps** (a counter going 21 → 22, a caption changing): two `<text>` elements with `calcMode="discrete"` opacity.
- **Typing:** a `clipPath` rect whose width animates from 0. Rotating taglines: per-line opacity + translate in their own slot of the loop.
- **Motion along a path:** `animateMotion` with `keyPoints` + `keyTimes` + `calcMode="linear"` to wait, walk, then hold.
- **Dark mode:** an SVG may carry `<style>@media (prefers-color-scheme: dark){…}</style>`; use it for text drawn straight on the page (taglines). Banners carry their own background instead.
- **Reuse with `<symbol>` + `<use>`**, and write both `href` and `xlink:href` for older renderers.
- Include `<title>`/`<desc>` (or `aria-label`) and a real `alt` on the `<img>`.

### Gotchas that bit us

- A gradient on a **zero-height or zero-width shape** (a horizontal `<line>`) vanishes with the default `objectBoundingBox` units. Use `gradientUnits="userSpaceOnUse"` with explicit coordinates.
- `<use>` instances share their symbol's animations: animating a symbol's fill animates every house at once (handy for night).
- Labels and speech bubbles collide in motion; check frames where things move, not just t=0.
- Emoji in SVG text depend on the viewer's fonts; keep them decorative.
- Embedded `data:` images in an SVG are risky under raw.githubusercontent's CSP. For a slideshow of screenshots use an animated WebP instead.

## Checking SVGs: `tools/readme/snap.cjs`

Seeks the SVG's SMIL clock and screenshots it at chosen seconds:

```bash
node tools/readme/snap.cjs docs/readme/hero.svg /tmp/hero 2 11 16 22
# writes /tmp/hero-2.png, /tmp/hero-11.png, …
```

Look at every PNG. Check each phase of the loop (day and night, before and after the walk, the last frame), then fix and re-snap. It needs Playwright with Chromium (`PLAYWRIGHT=/path/to/node_modules/playwright` if it isn't resolvable). On a small box, run it niced and one at a time; parallel agents share one lock:

```bash
flock /tmp/readme-chrome.lock nice node tools/readme/snap.cjs …
```

## Screenshot tour: `tools/readme/tour.py`

Builds `tour.webp`: shots cover-cropped to 16:10 inside a browser window on a sky gradient, a caption pill with a lime dot, progress dots, 2.6 s per shot and a 5-frame crossfade. Needs Pillow and an Inter TTF.

```bash
python3 tools/readme/tour.py tour.json docs/readme/tour.webp
```

`tour.json`:

```json
{
  "fonts": { "semibold": "/path/Inter-SemiBold.ttf", "regular": "/path/Inter-Regular.ttf" },
  "shots": [
    { "image": "docs/readme/shots/landing.jpg", "url": "sky.obelisk.ar", "caption": "Walk into Nostr conversations" },
    { "image": "docs/readme/shots/village.jpg", "url": "sky.obelisk.ar/app", "caption": "Every channel is a house." }
  ]
}
```

Nine shots at 1164×790 came to about 3.5 MB.

## Screenshots

- Use real captures of the live product. Before taking new ones, look in earlier sessions' scratchpads (`/tmp/claude-0/*/scratchpad/`) and the repo; most of what we needed already existed.
- Export as progressive JPG, quality ~84, max 1280 px wide, into `docs/readme/shots/` with descriptive names. Delete exports the README doesn't reference.
- Never ship a screenshot that shows a secret (an nsec on a "your new key" screen, a token).
- Repos that ignore `*.png` are fine: shots are `.jpg`, animations `.svg`/`.webp`.

## Counters and links

```markdown
<img src="https://img.shields.io/website?url=https%3A%2F%2Fsky.obelisk.ar%2Fhealthz&style=for-the-badge&label=island&up_message=floating&up_color=b4f953&down_message=sunk&down_color=ef4444&labelColor=0f2a44">
<img src="https://img.shields.io/github/stars/obelisk-app/REPO?style=for-the-badge&logo=github&label=stars&color=b4f953&labelColor=0f2a44">
<img src="https://img.shields.io/github/last-commit/obelisk-app/REPO?style=for-the-badge&color=8fd3ff&labelColor=0f2a44">
<img src="https://img.shields.io/github/commit-activity/m/obelisk-app/REPO?style=for-the-badge&color=8fd3ff&labelColor=0f2a44">
```

- A status badge pointing at a health endpoint, with a playful up/down message ("floating"/"sunk").
- Star history with light and dark versions:

```html
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=obelisk-app/REPO&type=Date&theme=dark">
  <img alt="Star history" src="https://api.star-history.com/svg?repos=obelisk-app/REPO&type=Date" width="640">
</picture>
```

- Assets from another repo by absolute URL: `https://raw.githubusercontent.com/obelisk-app/obelisk-sky/main/docs/readme/divider.svg`.
- Every README ends with the Obelisk family table; keep it in step with the [org profile](https://github.com/obelisk-app/.github/blob/main/profile/README.md).

## Shipping

- Work from a fresh clone; don't disturb a local checkout with work in progress.
- Push over HTTPS with the `gh` login.
- After pushing, check the files serve: `curl -sIL https://github.com/obelisk-app/REPO/raw/main/docs/readme/hero.svg | grep -i content-type` should say `image/svg+xml`. Then open the rendered page once and watch the animations play.
