# The Lab: standalone experiments in drawing, moving and laying out storyboards

`lab/<slug>/index.html` is one experiment: a single self-contained HTML page (its CSS and JavaScript inline), published as
it is at `https://storyboards.sgit.ai/lab/<slug>/`. The build copies this folder into `www/lab/` unchanged (except
`tools/` and this file), generates `lab/index.html` from every `lab/<slug>/experiment.json`, and writes each page's
markdown twin from the same file. Nothing here is promised to the kit: a thing that works is lifted into
api.storyboards.sgit.ai as a new release; a thing that does not stays here with what it taught us.

## The rules of an experiment

1. **Standalone, and pinned.** The kit is loaded from an immutable release by its full path with integrity strings (the
   tags below), never from a floating path, and never from `../assets/`. Any other library is vendored in `lab/vendor/`
   under a versioned file name (`matter-0.20.0.min.js`) with its licence beside it, and loaded with a relative path.
   The page must keep working when the site re-pins the kit or deletes another experiment.
2. **Programmatic.** Every picture is drawn by code from data; no image files, no image models. Rough.js wobble must be
   seeded so a frame is the same picture twice.
3. **Nothing fetched from a third party at run time.** `node lab/tools/check.mjs lab/<slug>/index.html` fails on any
   request to a host other than the two sites, on any page error and on any console error; run it before you are done,
   and look at the screenshot it writes (`SHOT=/path.png`).
4. **The page says what it is.** It carries the site's inline icon (copy the `<link rel="icon" href="data:image/svg+xml,...">` line from any experiment), so the browser does not ask the host for a favicon.ico it does not have. A header strip with the title, the track and `lab · experiment · pinned to kit v0.1.0`,
   a link back to `../index.html`, the thing itself, then a section headed "What this taught us" with two to five short
   findings, plain and honest (what worked, what did not, what to lift into the kit, what to try next).
5. **A reader can play.** Controls are real buttons, sliders and text fields with labels; keyboard handlers ignore keys
   typed into a field; `prefers-reduced-motion` turns animation into stills. Touch targets 44px.
6. **House style.** Paper `#fbf7ee`, ink `#23262b`, marker `#fde68a`, accent `#0f766e`, red `#dc2626`, page `#f7f3ea`,
   dim `#5b6169`; titles in Caveat and hand text in Patrick Hand (from the kit's `fonts.css`), body text in system-ui.
   British spelling. No em-dashes in prose. Say the status of things.
7. **`experiment.json` beside the page**, exactly this shape:

```json
{
  "slug": "stage",
  "title": "Stage",
  "track": "motion",
  "question": "Can a storyboard's actors be directed like a game, from a script of verbs?",
  "summary": "One sentence for the card on the lab index.",
  "kit": "v0.1.0",
  "libraries": ["anime-3.2.2.min.js"],
  "order": 50,
  "status": "exploring",
  "date": "2026-10-20",
  "learnt": ["Two to five findings, the same ones the page shows."]
}
```

Tracks: `characters`, `motion`, `layout`, `deeper`, `engines`. Status: `exploring`, `promising`, `parked`, `lifted`. `libraries` lists only files in `lab/vendor/` (the kit is implied by `kit`). `order` sorts the cards within a track (lower first, default 50).

## The kit, pinned (release v0.1.0): paste these tags, in this order, as the page needs them

```html
<link rel="stylesheet" href="https://api.storyboards.sgit.ai/v0/v0.1/v0.1.0/fonts.css" integrity="sha384-ep4bdPYRUzquMICQMhuOkSZ/CB1FnMh6qnGWS1F74VepoLOlw9JGK+Zg+E6/t9dD" crossorigin="anonymous">
<link rel="stylesheet" href="https://api.storyboards.sgit.ai/v0/v0.1/v0.1.0/storyboard.css" integrity="sha384-NGJqtVi+93pE7lBuwFU0RQWhqnQVLR33Wp8AYH1iAeyC2A7h2ijgU4bEKF5HIKIf" crossorigin="anonymous">
<script src="https://api.storyboards.sgit.ai/v0/v0.1/v0.1.0/vendor/rough-4.6.6.js" integrity="sha384-XPr5sCJfqHMzoJ8Cn1UYdXXD+XvRi0yoZm3W0yVJ24QP0ps8SYUskiXqnl4yqWlc" crossorigin="anonymous"></script>
<script src="https://api.storyboards.sgit.ai/v0/v0.1/v0.1.0/props/security.js" integrity="sha384-IkxAFhrp5pQhBSjFCLMEA+1iqFHJ6xPRLeO2n9g478h7Z8hW9cUyvza3PuOtmsOx" crossorigin="anonymous"></script>
<script src="https://api.storyboards.sgit.ai/v0/v0.1/v0.1.0/storyboard.js" integrity="sha384-3xZhCe5dUdBXMwV57gyscmlqdIjzz9L6huUkcuiEyC0V3jfrlQEdyEhvvF4kCeOa" crossorigin="anonymous"></script>
<script src="https://api.storyboards.sgit.ai/v0/v0.1/v0.1.0/export.js" integrity="sha384-AZlBi+8U84fchjU5NkLWax6WlMqeEdfDT8jW+Rkjr7MYfrYxE9qfvToj6ekYas4M" crossorigin="anonymous"></script>
<script src="https://api.storyboards.sgit.ai/v0/v0.1/v0.1.0/formats.js" integrity="sha384-5+Nd7LBeUw3ULihUHo2pdWbGrMYeK6K1o++7A5QBRyPhCIFNJ4xqjp7ULIfgz8IX" crossorigin="anonymous"></script>
```

(`embed.js` exists too; it loads the rest from beside itself, so a page that uses it needs no other tag.)

## What the kit gives a page (`window.StoryboardKit`, after `storyboard.js` loads)

| | |
|---|---|
| `drawScene(svg, scene, cast, { seed, footer })` | draws one 1600 by 1000 panel into an `<svg>`: paper, setting, props, people, bubbles, caption |
| `drawCharacter(g, rc, who, x, floor, { pose, mood, flip, scale })` | one character into an SVG `<g>`, standing on `floor` (panel units, the panel's floor is 900); returns `{ headX, headTop }`; `rc = rough.svg(svgEl, { options: { seed, roughness: 1, bowing: 1.2 } })` |
| `play(panelEl)` | plays a panel's arrival once (`panelEl` has class `sb-panel` and holds the svg); strokes draw themselves, `.actor` and `.pop` groups arrive at their `--d` delay |
| `VOCAB` | `{ kinds, poses, moods, settings, props() }` |
| `POSES` | stand, point, wave, arms-up, shrug, think, sit |
| `MOODS` | neutral, happy, excited, calm, worried, sad, surprised, thinking, confused, determined |
| `W`, `H`, `PAPER`, `INK` | 1600, 1000, `#fbf7ee`, `#23262b` |
| `addProps(pack)`, `wire(root)`, `sceneText(scene, cast)` | a prop pack, the page wiring, a panel as text |

A character: `{ id, name, kind: "human"|"agent", look }`; a human's look `{ skin, hair: short|long|curly|bun|beanie|bald,
hairColour, hatColour, shirt, trousers, accessory: glasses|headphones|lanyard|none, accentColour, height }`; an
agent's `{ colour }`. A scene's props: `{ kind, x (0..1), y (panel units, the line it stands on), scale, label, ... }`;
the kit's props are laptop, desk, book, board, phone, sign; the security pack adds key, vault, qr, envelope, record,
server, arrow, mark, calendar, terminal, phoneqr, padlock. `window.StoryboardExport.svg/image/sheet` export a panel.

What the kit does not export (draw your own in the experiment): the speech bubble, the caption box, the setting and the
props as functions. Draw them with the same Rough.js canvas, in the same ink, with `rc.path`, `rc.rectangle`,
`rc.ellipse`, `rc.line`, `rc.curve`; text with an SVG `<text>` in `font-family: 'Patrick Hand'`.

## The lab cast (copy it into the page; do not fetch it)

```json
{
 "what": "The lab's own cast: three people and an agent, invented for the experiments.",
 "characters": [
  { "id": "ines", "name": "Ines", "kind": "human", "pronouns": "they/them", "role": "the one who asks",
    "look": { "skin": "#c68642", "hair": "long", "hairColour": "#2b1d14", "shirt": "#0f766e", "trousers": "#1f2937", "accessory": "glasses", "height": 1.0 } },
  { "id": "oto", "name": "Oto", "kind": "human", "pronouns": "they/them", "role": "the one who tries things",
    "look": { "skin": "#f1c27d", "hair": "beanie", "hatColour": "#b91c1c", "hairColour": "#111827", "shirt": "#7c3aed", "trousers": "#334155", "accessory": "headphones", "accentColour": "#f59e0b", "height": 0.96 } },
  { "id": "vex", "name": "Vex", "kind": "human", "pronouns": "they/them", "role": "the one who breaks things",
    "look": { "skin": "#e0ac69", "hair": "short", "hairColour": "#6b7280", "shirt": "#374151", "trousers": "#111827", "accessory": "none", "height": 1.02 } },
  { "id": "unit", "name": "Unit", "kind": "agent", "pronouns": "it/its", "role": "the agent", "look": { "colour": "#1d4ed8" } }
 ]
}
```

## Checking a page

```bash
SHOT=/tmp/claude-0/.../stage.png node lab/tools/check.mjs lab/stage/index.html --wait 3000
```

It routes `https://storyboards.sgit.ai/` to this checkout and `https://api.storyboards.sgit.ai/` to the API checkout beside
it, so the pinned tags resolve exactly as they will live. Then look at the screenshot.
