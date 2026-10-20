# storyboards.sgit.ai: for the agent working here

Read first: `briefs/` (the brief), `REALITY.md` (what exists), `BRIEF-CORRECTIONS.md`, then `README.md`.

This repository has a twin, `SGit-AI__Website__Storyboards__API` (api.storyboards.sgit.ai), normally checked out beside it. The two are worked together: a change that needs the kit changed is a new API release first (never an edit to a published folder there), then a re-pin here (`build.py --pin`), in the same session.

Rules:
- The storyboards in `content/series/*/NN__*.json` and `cast.json` are their origin site's files. Re-import with `admin/build/import_series.py`; do not edit them here. What this site adds goes in `series.json`.
- `www/` is generated: never edit it by hand. `build.py --check` fails if you do.
- Every push to dev (the release branch) is a version: add the row to `content/versions.json` first (the next patch unless told otherwise), commit subject `site vX.Y.Z: what changed`.
- Before pushing: `render.py` (if a storyboard, cast or the pin changed), `build.py`, `validate.py`, `node tests/test_site.mjs`. All must pass.
- Prose: no em-dashes, sentences with verbs, state the status of things, source every number. Characters use the pronouns their cast file gives.
- Never commit a key, a token or a vault key; the gate scans for key shapes.
