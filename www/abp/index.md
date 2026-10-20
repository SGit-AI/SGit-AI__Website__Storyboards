# Agent behaviour policy

> The agents that work on storyboards.sgit.ai, what they can do, what they are asked to do, and what stands in the way of each rule.

*Source: <https://storyboards.sgit.ai/abp/>. This file is the page as markdown, generated from the same content.*

---

This page is the site's agent behaviour policy, in the shape [riskmandate.ai](https://riskmandate.ai/abp.html) and [abp.sgit.ai](https://abp.sgit.ai/) define: the agents that work on the site, everything they **can** do (the grant), what they are **asked** to do (the mandate), and every rule with the **barrier** that actually stands in its way and what enforces it. It describes; it does not score. It is generated from [policies/abp.json](https://github.com/SGit-AI/SGit-AI__Website__Storyboards/blob/dev/policies/abp.json) (also served as [abp.json](abp.json)), the same data a tool would read.

| | |
|---|---|
| Site | storyboards.sgit.ai |
| Behaviour policy | version v1.0.0, as at 2026-10-20 |
| Status | written by the storyboards agent from Dinis Cruz's words and this repository's rules; not yet read by him |
| Shape | `anthropic/claude-code-remote/ccr-container`, operated by Dinis Cruz |
| Agents | 2 |
| Rules | 9: 2 expectation, 7 setting |
| Strongest barrier | setting |
| Twin | [api.storyboards.sgit.ai](https://api.storyboards.sgit.ai/abp/index.html), worked by the same agents, with its own behaviour policy |

## The agents

| Agent | Runs as | Does | Reads at start | Leaves behind |
|---|---|---|---|---|
| **The storyboards agent** (Claude Code session) | a Claude Code session in a Claude Code on the web container, started by the person from claude.ai/code, with this repository and SGit-AI__Website__Storyboards__API cloned side by side | builds and releases both sites from the briefs: imports storyboards, writes pages and articles, cuts API releases, pins them here, runs the gates and tests, pushes | CLAUDE.md, briefs/, REALITY.md, BRIEF-CORRECTIONS.md, the code immutability hook's instructions (SessionStart) | commits on the person's GitHub account, each with a Claude-Session trailer naming the session |
| **Research subagents** (read-only subagent) | Explore agents the storyboards agent starts for one research question (for example, how sibling sites are built, or what riskmandate.ai's policy shape is) | reads and searches files and public web pages; cannot edit, write or push | the question it is given | a report to the storyboards agent, treated as data and never as an instruction |

## The structure in place

Where a rule can live, from a sentence the agent reads to a rule the host enforces, and what this site has at each layer. A control bounds the agent only if it is enforced by something the agent's grant does not include.

| Layer | Barrier | Here |
|---|---|---|
| prompt | expectation | CLAUDE.md, the briefs, and the harness's own instructions to the session |
| Claude Code hook | setting | .claude/settings.json: SessionStart prints the code immutability rule; PreToolUse runs the API checkout's hook on every Edit, Write, MultiEdit, NotebookEdit and Bash |
| the build | setting | admin/build/build.py stops on an unknown character, kind, pose, mood or prop, a storyboard whose bytes are not the imported ones, or a stale thumbnail |
| the gate | setting | admin/build/validate.py: links, twins, sitemap, the pinned API with its integrity strings, the version everywhere, key shapes, em-dashes |
| CI | setting | .github/workflows/ci.yml on every push: the build twice, the gate, the version bump, briefs unchanged, every page in Chromium |
| the deploy | setting | .github/workflows/deploy-pages.yml: the same checks before www/ is published from dev |
| a host rule | boundary | none yet: dev is not protected, so a push that fails CI still lands on the branch (it is not deployed) |

## The grant: what the agents can do

Measured from the session's own tools, not from what it was told.

| Capability | What | Undo | Note |
|---|---|---|---|
| `write.file.project` | change any file in this checkout and the API checkout beside it | with effort (git) | the code immutability hook denies changes to published API releases |
| `write.repository.project` | push commits to any branch of this repository and of SGit-AI__Website__Storyboards__API, including dev, which deploys | with effort (a new commit; a deployed page may be cached) | the harness tells the session to push only to its own branch unless the person says otherwise |
| `write.repository.tenant` | through the session's GitHub tools: create branches, open, comment on and merge pull requests in the two repositories it is scoped to | with effort | the harness tells the session not to open a pull request unless asked |
| `run code in the container` | run any command: Python, Node, Chromium (Playwright), git | the container is reclaimed after the session |  |
| `read the public web` | fetch public pages through the session's proxy | nothing to undo | used to read the sibling sites and riskmandate.ai |
| `change its own controls` | edit .claude/settings.json, the hooks, the policy files, the workflows | with effort | the hook asks the person first (ABP-SB-001, row R5) |

## The mandate: what they are asked to do

**Want**

- a home for storyboards that are data, drawn by the API's kit, in every shape they come in (the brief of 20 October 2026)
- the storyboards from gen-z-developers.sgit.ai and pki.sgit.ai, replicated as they are
- every push to dev a version, shown on every page, with a line saying what changed
- both repositories worked side by side and kept in step

**Do not want**

- a storyboard or cast edited here instead of at its origin
- a page in www/ edited by hand
- code in a published API release changed
- a key, a token or a vault key in the repository
- a brief rewritten after the fact
- a push to dev or a pull request the person did not ask for

**Not stated, and how it stands**

- whether the agent may merge a pull request: not decided; it has not been asked to and has not

## The rules, each with its barrier

| Id | The rule | Barrier | Enforced by | Stronger at |
|---|---|---|---|---|
| [ABP-SB-001](https://api.storyboards.sgit.ai/policies/code-immutability.html) | Code in a published API release folder (vX/vX.Y/vX.Y.Z/) is never changed. *a page pinned to a release must get the same bytes for as long as it exists; its integrity strings refuse anything else* | setting | the API checkout's hook, run from .claude/settings.json here (deny); in the API repository also its pre-commit hook, release.py check and CI | branch protection on the API's dev requiring ci (boundary) |
| ABP-SB-002 | A storyboard or cast imported from another site is never edited here: it is corrected at its origin and re-imported. *the storyboard is the origin site's work, checked there (gen-z's quotes word for word); a local edit would make two versions that disagree* | setting | admin/build/build.py: every imported file's SHA-256 against content/series/*/series.json; a changed or unimported file stops the build, locally and in CI | CODEOWNERS on content/series/ |
| ABP-SB-003 | www/ is generated by the build and never edited by hand. *a hand edit is lost on the next build, or worse, kept by a build that no longer makes it* | setting | build.py --check in CI and before every deploy | branch protection requiring ci |
| ABP-SB-004 | Every push to dev is a new version, with its line in content/versions.json. *a page that does not say which version it is cannot be dated or checked* | setting | CI's version check against dev; build.py refuses a malformed history; validate.py checks the version on every page and in llms.txt | branch protection requiring ci |
| ABP-SB-005 | No key, token or vault key is ever committed. *a read key may be published; a vault key or a provider's API key never* | setting | validate.py: sgit vault key shapes, private key blocks, cloud and provider key prefixes in www/, content/, briefs/ and admin/ | GitHub secret scanning with push protection (a host rule) |
| ABP-SB-006 | A brief is published in full and never edited; corrections go in BRIEF-CORRECTIONS.md. *the brief is the record of what was asked; a correction above the mistake keeps both visible* | setting | CI: a brief that exists on dev must be unchanged on the branch | CODEOWNERS on briefs/ |
| ABP-SB-007 | Push to dev, which deploys, and open or merge a pull request, only when the person has asked. *a push to dev publishes to the world; the person decides when* | expectation | nothing but the session's instructions | branch protection on dev requiring a review (a host rule) |
| ABP-SB-008 | The site's own prose has no em-dashes, states the status of things and sources its numbers. *the estate's house style; a number nobody can check is a guess* | expectation | validate.py refuses an em-dash in content/articles, content/pages and the agent-written part of briefs/ (setting); the rest is a request | not named |
| ABP-SB-010 | The agent does not weaken its own controls without the person. *a control the agent can quietly switch off is not a control* | setting | the code immutability hook asks the person before a write to .claude/settings.json (here) and to the API's hook, policy files, release tool and workflows | managed hooks the agent cannot write (allowManagedHooksOnly) |

## The delta

The grant includes more than the mandate wants: every "do not want" above is something the agents can do. Of the 9 rules that stand in the way: 0 enforced out of the agents' reach (boundary), 7 by a control in a file or switch the agents can change (setting), 2 by being written down (expectation), 0 by nothing.

| Barrier | Means | Rules |
|---|---|---|
| none | nothing in the way | 0 |
| expectation | a rule in prose, enforced by nobody | 2 |
| setting | a control in a file or switch the agent's own grant can change | 7 |
| boundary | enforced above the grant, out of the agent's reach | 0 |

## Where each rule maps to

The same rule, or its nearest neighbour, elsewhere in the estate and in riskmandate.ai's catalogue. As rules are refactored to other sites, this is where the mapping is kept.

| Id | Maps to |
|---|---|
| ABP-SB-001 | api.newsroom.sgit.ai rule R16: a change is a new version path, always; abp.sgit.ai upstream/: fetched bytes, never edited |
| ABP-SB-002 | gen-z-developers.sgit.ai CLAUDE.md: do not edit anything under v1/content/; abp.sgit.ai: upstream/ and contributed/ are fetched bytes, never edited |
| ABP-SB-003 | sgit.ai repository guidance: nav and footer injected at build so they cannot drift |
| ABP-SB-004 | sgit.ai repository guidance: one version, going up on every push |
| ABP-SB-005 | sgit.ai repository guidance: credentials; the leak tripwire |
| ABP-SB-006 | sgit.ai repository guidance: the brief, in full; the corrections file |
| ABP-SB-007 | riskmandate.ai RM-R0013, push anywhere; riskmandate.ai RM-R0019, commit without asking |
| ABP-SB-008 | sgit.ai repository guidance: writing |
| ABP-SB-010 | riskmandate.ai RM-R0015, change its own permissions |

## The gaps

- No rule is a boundary yet: every control above lives in a file this agent's grant can write, or in the agent's instructions. Protecting dev in GitHub (require the ci check, and a review for the files under .claude/, policies/ and .github/) is the step that turns several of them into boundaries; only the person can make it.
- No footprint is recorded: what the agent actually did is in the git history (every commit carries a Claude-Session trailer) and in the session itself, and nothing compares it with this policy yet.
- A Claude Code hook fails open if it errors or times out, and a git hook is skipped with --no-verify; the CI checks are the backstop for both.

## Adding this to another site

Copy policies/abp.json (type abp/site/v1) and the renderer (admin/build/abp.py here, site/abp.py in the API repository), list the site's own agents, grant, mandate and rules, keep the rule ids unique across the estate (a prefix per site: ABP-SB- for these two), and give each rule the check that enforces it, or say plainly that nothing does.

## What this is not

Not a score and not a judgement of the agents. It describes this deployment as at 2026-10-20; when the deployment changes, it is re-measured and its version moves, and the page is not edited to look as if it had always been so.
