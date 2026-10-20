# Every version is a folder

> The kit that draws every storyboard is published at a path that names its version, /v0/v0.1/v0.1.0/, and nothing at that path ever changes. Why, how it is enforced, and what it costs.

*Source: <https://storyboards.sgit.ai/articles/every-version-is-a-folder.html>. This file is the page as markdown, generated from the same content.*

---

The brief's one engineering instruction was about versions: "use the file path as a way to version the JavaScript", publish every release as a new folder with every file in it, "and then you put the hashes". Then, a minute later, the decision that matters most: "every version is immutable. I think that's important."

## The rule

A release of the kit lives at `https://api.storyboards.sgit.ai/vMAJOR/vMAJOR.MINOR/vMAJOR.MINOR.PATCH/`. The first is [`/v0/v0.1/v0.1.0/`](https://api.storyboards.sgit.ai/v0/v0.1/v0.1.0/manifest.json). Inside it is every file the kit needs (the drawing code, its stylesheet, Rough.js, the two fonts, the prop pack, the formats, the exporter, the embed) and a `manifest.json` naming each file's size, SHA-256 and the `sha384-` string a browser checks in an `integrity` attribute.

Three things follow, and the tooling enforces each of them:

1. **Nothing at a published path changes.** `tools/release.py check` recomputes every hash of every release on every commit and fails if one moved. A fix is a new folder, `v0.1.1`, and `v0.1.0` stays exactly as it was.
2. **There is no `latest`.** No floating `/v0/` or `/v0.1/` alias. A page that wants the new version changes one line on purpose, and a page that does not want it never gets it by surprise. `releases.json` at the root lists every version, newest first, for a tool that wants to know.
3. **A new major starts from the last good release.** `tools/release.py major --from v0.1.3` copies that folder, byte for byte, into the working tree as `v1.0.0`. The difference between the last v0 and the first v1 is then only the change that made it a major, and both folders still exist to diff.

## Why a whole folder, not a version in the file name

Because the kit is several files that load each other. `embed.js` loads the stylesheet, the fonts, Rough.js and the drawing code *from beside itself*; `export.js` finds the fonts the same way. A folder is the unit that stays consistent: pin the folder and every relative path inside it resolves to the same release. A per-file version would let `storyboard.js` from one release meet `export.js` from another.

## Why it is affordable

The brief guessed it would be ("these are small, well, smaller JavaScript files"). Counted: release v0.1.0 is 13 files and about 234 KB, of which the two fonts are 75 KB and Rough.js is 28 KB. A hundred releases would be 23 MB of static files on a host that serves them for nothing. If that ever becomes a problem, it will be a good problem to have, and the answer will be to stop copying the vendored files that did not change, not to start changing published ones.

## What it buys

A storyboard embedded today draws the same panel in five years, because the code that draws it cannot change underneath it. A page can prove it is running the code it thinks it is running, because the browser refuses a file whose hash is not the one in the tag. And the history of the kit is a list of folders anyone can open, side by side.

## Where this came from

The newsroom's API moved its reading meter to versioned component paths ([`sg-meter/v1/v1.4/v1.4.0/`](https://api.newsroom.sgit.ai/)) and its releases to manifests with hashes. This site takes that one step further, as the brief asked: the whole release, not one component, is the folder, and every version of it, not only the majors.
