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
- Code in a published API release folder is never changed (behaviour policy ABP-SB-001, `../SGit-AI__Website__Storyboards__API/policies/code-immutability.md`). `.claude/settings.json` here runs that repository's hook, which denies it; do not work around it.
- Everything about the code is documented on the API site; this site documents what the storyboards are and do.
- A Lab experiment (`lab/<slug>/`) is standalone: it pins the kit by immutable path and hash, vendors anything else under a versioned name in `lab/vendor/`, and ends with what it taught. `lab/README.md` has the rules and the checker; the gate enforces the pin and the twin.
