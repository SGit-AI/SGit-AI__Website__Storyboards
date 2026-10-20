# Reality: what exists, as of site v0.1.3 (20 October 2026)

A feature not in this file does not exist. Updated by whoever ships.

## Exists, and was checked

- 23 storyboards, 254 panels, 2 series (gen-z-developers: 16 boards, 7 characters, from commit e2a71808; pki: 7 boards, 7 characters, from commit ab6affc9), byte for byte as their origin sites wrote them.
- Per storyboard at `/<series>/<slug>/`: the page (deck, grid, script; the kit's own viewer), `storyboard.json`, `bundle.json`, `index.md` (the script, made by the API's formats.js), `graph.json` (made by formats.js), `thumb.jpg` and `og.jpg` (drawn by the API's export.js in headless Chromium), in-browser exports of SVG, animated SVG, PNG, JPEG and a contact sheet, and an embed snippet.
- Per series: the shelf, every panel on one page, the model sheet, `cast.json`.
- Home, embed, formats, about, participant disclosure, three articles, the brief in full, release history, `catalogue.json`, `llms.txt`, markdown twins of every page, `sitemap.xml`, `robots.txt`, `404.html`.
- Every page loads the kit from `https://api.storyboards.sgit.ai/v0/v0.1/v0.1.0/` with SRI integrity strings from the pinned manifest.
- The gate (`admin/build/validate.py`) and `build.py --check`, both passing; `tests/test_site.mjs` opens all 43 pages in Chromium with no errors (run locally, both hosts routed to the checkouts).

- `.claude/settings.json` runs the API checkout's code immutability hook (ABP-SB-001) on SessionStart and PreToolUse.
- Both sites are live: storyboards.sgit.ai and api.storyboards.sgit.ai, deployed from `dev`.

- The Behaviour policy page (`/abp/`), from `policies/abp.json`: 2 agents, the layers of control, the grant, the mandate, 9 rules (ABP-SB-001 to 008 and 010), 7 of them rated setting (a check that runs) and 2 expectation. The build now refuses an imported storyboard whose bytes changed (ABP-SB-002); CI refuses an edit to a brief already on dev (ABP-SB-006).

- The Lab (`/lab/`): standalone experiments (counted by the build, listed in `lab/experiments.json`), each pinned to kit v0.1.0 with integrity strings, other libraries vendored (matter.js 0.20.0, anime.js 3.2.2, kaplay 3001.0.19, dagre 1.1.4, each with its licence), an index generated from each `experiment.json`, a markdown twin per experiment, a Chromium checker that refuses errors and third-party requests.

## Does not exist yet

- An architecture review as a storyboard: on the Lab's list, not built; the camera over a world of panels is the nearest thing.
- Lifting anything from the Lab into the kit: no experiment has been promoted to a release yet.

- Making a storyboard or a cast on the site; any commercial feature.
- The `review/` folder the sgit.ai repository guidance asks for (section 7). A gap.
- A listing on sgit.ai's network page: the entry is drafted in `admin/network-entry.md` for the sgit.ai site to take.
- The origin sites (gen-z-developers, pki) still carry their own copies of the kit; moving them to the API is their change to make.
- Tests in Firefox and WebKit: only Chromium has been run.
- The gen-z word-for-word quote check: it ran on the origin site at the imported commit; the source files are not in this repository.
