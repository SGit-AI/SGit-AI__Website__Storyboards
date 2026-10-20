---
title: The formats
nav: Formats
summary: Every storyboard comes in seven shapes, made from one JSON file. Where each one lives, at which address, and what makes it.
---

For a storyboard at `{{SITE}}/<series>/<slug>/`:

| Shape | Address | What it is |
|---|---|---|
| The page | `index.html` | the deck (one panel at a time, swipeable, full screen), the grid and the script, with notes and sources |
| JSON | `storyboard.json` | the storyboard, unchanged from the file its origin site wrote |
| Bundle | `bundle.json` | the storyboard, its cast and the prop packs it needs, in one file: what an embed fetches |
| Markdown | `index.md` | the script: every panel as text, who says what, in what pose and mood, the evidence and its source |
| Semantic graph | `graph.json` | nodes (the storyboard, panels, characters, props, sources, settings) and the edges that carry the meaning (has_panel, next, features, says, quotes, shows, set_in) |
| Thumbnail | `thumb.jpg` | the cover panel, 480 by 300 |
| Link preview | `og.jpg` | the cover panel, 1200 by 750 |
| SVG | a button on the page | any panel, as a standalone SVG that links the fonts from the kit's release |
| Animated SVG | a button on the page | the same, drawing itself when opened (CSS inside the file, no script) |
| PNG, JPEG | buttons on the page | any panel at 1600 by 1000, fonts embedded |
| Contact sheet | a button on the page | every panel on one SVG, four per row |

For the whole site: [`catalogue.json`]({{SITE}}/catalogue.json) lists every storyboard with the address of each shape and its embed snippet, and [`llms.txt`]({{SITE}}/llms.txt) is the same for an agent that reads prose. A series' cast is at `<series>/cast.json`.

## What makes each one

The JSON is written by a person or an agent. The markdown and the graph are made at build by `formats.js`, the API's own file, fetched from the pinned release {{API_RELEASE}} and checked against its hash before it runs, so a reader's browser running the same file gets the same bytes. The pictures are drawn by `export.js` with the same seeds as the deck, so an exported panel is the panel on the screen. Only the thumbnail and the link preview are committed as images, because a page needs them before any code runs; the build refuses a storyboard whose images were drawn from older data. [One storyboard, seven shapes](../articles/one-storyboard-seven-shapes.html) has the reasons.
