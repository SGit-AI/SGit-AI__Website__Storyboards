# One storyboard, seven shapes

> The brief listed the shapes a storyboard should come in: JSON, markup, a semantic graph, JPEG, SVG, animated and a thumbnail. Here is each one, where it comes from, and why only two of them are committed images.

*Source: <https://storyboards.sgit.ai/articles/one-storyboard-seven-shapes.html>. This file is the page as markdown, generated from the same content.*

---

"Then we'll have the JSON version, the markup version, the semantic graph version ... the JPEG version, so the SVG version, the animated version ... and the thumbnail version." That is the brief's list, and every storyboard on this site now comes in each of them. They are not seven things to keep in step. They are one thing, the JSON, and six ways of reading it.

| Shape | Where it is | Made by | When |
|---|---|---|---|
| The deck, grid and script | the storyboard's page | the kit, `storyboard.js` | in your browser, as you look |
| JSON | `storyboard.json`, and `bundle.json` with its cast | a person or an agent | written by hand, imported unchanged |
| Markdown (the script) | `index.md` | the kit's `formats.js`, run by this site's build | at build |
| A semantic graph | `graph.json` | `formats.js` | at build |
| SVG, and animated SVG | the buttons under the deck | the kit's `export.js` | in your browser, when you press it |
| PNG and JPEG | the same buttons | `export.js`, through a canvas | in your browser |
| A thumbnail and a link preview | `thumb.jpg`, `og.jpg` | `export.js`, in headless Chromium, through the API's `tools/render.mjs` | when the storyboard changes, committed |

## The same code in the build and in the browser

The markdown and the graph are made by the API's `formats.js`, the same file a reader's browser can load. This site's build does not have its own idea of what a storyboard's script looks like: it fetches `formats.js` from the pinned release, checks its hash, and runs it under Node. So an embed that offers "download the script" and this site's `index.md` are the same bytes from the same data.

## The graph

`graph.json` is the storyboard as nodes and edges, in the spirit of [graphs.sgit.ai](https://graphs.sgit.ai/): "A node is just a node. Meaning lives in the edges." The nodes are the storyboard, its panels, the characters, the props, the settings and the sources; the edges are verbs: a storyboard *has_panel*, a panel is *next* to the following one, a panel *features* a character in a pose and a mood, a character *says* a line in a panel, a panel *quotes* or is *drawn_from* a source, *shows* a prop and is *set_in* a setting. Across 23 storyboards that is enough to ask which characters share panels, which sources a series leans on, or which props never appear.

## Why most pictures are not files

Every picture is a copy of the data, and the data is what gets corrected. A storyboard with 15 panels would carry 15 SVGs of about 100 KB each, 15 PNGs of about 200 KB and 15 animated SVGs, all of which go stale the moment one line of dialogue changes. So the pictures are drawn when someone asks for one, by the same code and the same seeds as the deck, and they are exactly the panel on the screen. The two exceptions are the ones a page needs before any code runs: the thumbnail on a shelf and the image a chat app shows when a link is shared. Those are committed, and the build refuses to publish a storyboard whose thumbnail was drawn from older data.
