---
title: About storyboards.sgit.ai
nav: About
summary: What this site is, who it is by, how it is built and released, and what it does not do yet.
---

storyboards.sgit.ai is a home for storyboards that are data: short strips of panels, each one a JSON file naming who is in the panel, their pose and mood, what they say, the evidence and its source, drawn by code in the reader's browser. It was started on 20 October 2026 from [a voice memo](../brief/2026-10-20__storyboards-sgit-ai.html), published in full, and is part of the [sgit.ai network](https://sgit.ai/network/index.html).

## Two sites

| | Does | Repository |
|---|---|---|
| storyboards.sgit.ai | the storyboards, their pages and every shape they come in, the articles, the brief | [SGit-AI__Website__Storyboards](https://github.com/SGit-AI/SGit-AI__Website__Storyboards) |
| [api.storyboards.sgit.ai](https://api.storyboards.sgit.ai/) | the kit that draws them, in immutable versioned folders, and its documentation | [SGit-AI__Website__Storyboards__API](https://github.com/SGit-AI/SGit-AI__Website__Storyboards__API) |

This site uses the API exactly as any other site would: from the pinned release {{API_RELEASE}}, with the hash of every file it loads. Everything about the code (the guides, the reference, a live gallery of everything the kit draws, how it works inside, every release with its diff, and the behaviour policy that keeps published code immutable) is on [the developer site](https://api.storyboards.sgit.ai/docs/index.html).

## How it is built

`admin/build/build.py` turns `content/` into `www/`, which is committed and deployed by GitHub Pages on every push to `dev`. The build validates every storyboard against the kit's vocabulary (an unknown character, kind, pose, mood, setting or prop stops it), writes every page and its markdown twin, and refuses a storyboard whose committed thumbnail is stale. CI runs the build again and fails if `www/` is not what it makes, then runs `admin/build/validate.py`: every internal link resolves, every page has its twin and is in the sitemap, every script from the API is the pinned path with its integrity string, the version agrees everywhere, and no key shapes appear anywhere.

## What it does not do yet

- Let you make a storyboard or a cast on the site. The brief puts it later; the JSON is the editor for now.
- Sell anything. The brief mentions commercialisation; nothing here is for sale.
- Carry the `review/` folder the [sgit.ai guidance](https://sgit.ai/docs/guidance/repositories.html) asks of a new repository: a gap, recorded in the repository's reality file.
- Run the gen-z quote check here. Those boards were checked word for word against the book's files by gen-z-developers.sgit.ai's build at the commit they were imported from; the files are in that repository, and each board links to its source.

Content is CC BY 4.0; code is Apache-2.0. [The participant disclosure](participant.html).
