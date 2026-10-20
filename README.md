# SGit-AI__Website__Storyboards

The repository of **[storyboards.sgit.ai](https://storyboards.sgit.ai)**: a home for storyboards that are data (one JSON file per storyboard, one per cast), drawn by code in the reader's browser, in every shape a storyboard comes in. Its twin is **[api.storyboards.sgit.ai](https://api.storyboards.sgit.ai)** ([SGit-AI__Website__Storyboards__API](https://github.com/SGit-AI/SGit-AI__Website__Storyboards__API)), which serves the code that draws them in immutable versioned folders. The two are built side by side, by one agent, from [the brief](briefs/2026-10-20__storyboards-sgit-ai.md).

## Layout

| Path | What |
|---|---|
| `briefs/` | the brief, in full: the voice memo as transcribed, and the brief an agent drafted from it |
| `content/series/<series>/` | `NN__<slug>.json` storyboards and `cast.json`, imported byte for byte from their origin site by `admin/build/import_series.py`; `series.json`, everything this site adds (title, blurb, shelves, stances, the origin commit) |
| `content/articles/`, `content/pages/` | markdown with front matter |
| `content/versions.json` | the release history; the newest row is the site's version |
| `admin/build/api.json` | the pinned release of api.storyboards.sgit.ai and the hash of every file in it |
| `admin/build/build.py` | `content/` to `www/`; `--check` fails if `www/` is not what it makes; `--pin DIR` moves the pin |
| `admin/build/render.py` | draws each storyboard's `thumb.jpg` and `og.jpg` with the API's `tools/render.mjs`; records them in `renders.json` |
| `admin/build/validate.py` | the gate |
| `admin/assets/` | the site's own CSS and JS, copied to `www/assets/` |
| `www/` | the site, generated and committed; GitHub Pages serves it from `dev`, the default and release branch |
| `tests/test_site.mjs` | every page in Chromium, both hosts routed to the local checkouts |

## The agent behaviour policy

`policies/abp.json` (type `abp/site/v1`) describes the agents that work on this repository, what they can do, what they are asked to do, and every rule with its barrier and what enforces it. It is rendered as the site's top-level Behaviour policy page, `/abp/`, by the renderer shared with the twin repository, and is the shape to copy to every other site.

## Release

```bash
# the API checkout beside this one (or STORYBOARDS_API=path)
python3 admin/build/render.py          # only if a storyboard, a cast or the pin changed
# add a row to content/versions.json (the next patch: v0.1.1, v0.1.2 ...)
python3 admin/build/build.py && python3 admin/build/validate.py && node tests/test_site.mjs
git commit -am "site v0.1.1: what changed" && git push
```

A release is done when https://storyboards.sgit.ai serves the new version (`<meta name="site-version">`).

## Moving to a new API release

`python3 admin/build/build.py --pin ../SGit-AI__Website__Storyboards__API`, then `render.py --all`, build, gate, test. The pin is one file; every page loads the kit from that exact path with its `integrity` string.

Licence: code Apache-2.0, content CC BY 4.0. The storyboards are their origin sites' work, as each `series.json` records.
