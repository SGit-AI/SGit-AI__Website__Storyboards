# Embed a storyboard

> Any storyboard on this site, or your own, on any page: one script tag pinned to an immutable release of the kit, and one element.

*Source: <https://storyboards.sgit.ai/embed/>. This file is the page as markdown, generated from the same content.*

---

## Two lines

```html
<script src="https://api.storyboards.sgit.ai/v0/v0.1/v0.1.0/embed.js" defer></script>
<sg-storyboard src="https://storyboards.sgit.ai/pki/the-first-key/bundle.json"></sg-storyboard>
```

The script is `embed.js` from release v0.1.0 of [api.storyboards.sgit.ai](https://api.storyboards.sgit.ai/). It loads the rest of that release (the fonts, the stylesheet, Rough.js, the drawing code and any prop pack the storyboard needs) from beside itself, once per page, and draws the storyboard in the element. Every storyboard page on this site has its own snippet under "Put it on your page".

## What you can ask for

| Attribute | Means | Default |
|---|---|---|
| `src` | a bundle: a storyboard with its cast and packs (every storyboard here has a `bundle.json`) | |
| `storyboard`, `cast` | two URLs instead of a bundle | |
| `view` | `deck` (one panel at a time), `grid`, `script` (as text) or `panel` (one still panel) | `deck` |
| `panel` | with `view="panel"`, which one, from 1 | `1` |
| `packs` | extra prop packs, comma separated (today: `security`) | the bundle's |

## Why the version is in the path

The address `https://api.storyboards.sgit.ai/v0/v0.1/v0.1.0/` is a release that never changes: not a fix, not a typo. An embed you write today draws the same panels for as long as the page exists. When a newer release is out, moving to it is changing that one line, on purpose. If you want the browser to refuse anything but the exact bytes, add the `integrity` string from the release's [manifest](https://api.storyboards.sgit.ai/v0/v0.1/v0.1.0/manifest.json) and `crossorigin="anonymous"` to the script tag; every page on this site does. [Every version is a folder](../articles/every-version-is-a-folder.html) explains the rule.

## Your own storyboard

A bundle is plain JSON: `{ "storyboard": {...}, "cast": {...}, "packs": [] }`, served from anywhere that sends `access-control-allow-origin` (GitHub Pages does). The shape of a storyboard and a cast is documented on [api.storyboards.sgit.ai](https://api.storyboards.sgit.ai/docs/format.html), and the 23 here are worked examples: open any `storyboard.json`. Making a storyboard on this site, and casts of your own, are on the list for later; for now the JSON is the editor.

## What embedding does to your page

The element draws into the page itself (no iframe, no shadow root), so your styles can dress it. In the deck view, the arrow keys move the deck and the panel number is written into the address bar's `#scene-N`, as on this site; use `view="panel"` or `view="grid"` where that would get in the way. Nothing is stored except the reader's viewing preferences (animation on or off, panels per row), in their own browser.
