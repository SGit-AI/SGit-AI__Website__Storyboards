# Brief corrections

Where [the brief](briefs/2026-10-20__storyboards-sgit-ai.md) turned out to be wrong, ambiguous, or was read one way when it could have been read another: what was found, and what was done instead. The brief itself is never edited.

| Date | The brief says | What was found | What was done |
|---|---|---|---|
| 2026-10-20 | "the website called Storyboards.ai" and "the API. Storyboard Skit AI" | The repositories' READMEs name the hosts `storyboards.sgit.ai` and `api.storyboards.sgit.ai` | Built for those two hosts. If storyboards.ai is wanted as well, it is a DNS and CNAME change, not a code change |
| 2026-10-20 | First, versioned folders on the major only, minors overwritable; then "can you do that for every minor version? ... every version is immutable" | The two halves disagree; the second is the later and the more emphatic | Every release, patch included, is its own immutable folder. There are no floating aliases (`/v0/`, `/v0.1/`) at all, since an alias is a path whose bytes change |
| 2026-10-20 | "v 04 slash v 0.14 slash" | Read as `/vMAJOR/vMAJOR.MINOR/` with the full version inside: `/v0/v0.1/v0.1.0/` | That path shape, the same as api.newsroom.sgit.ai's components |
| 2026-10-20 | "make, share, sell"; "commercialization" | Nothing to sell yet, and the brief says to replicate what exists first | Not built; stated on the about page |
| 2026-10-20 | "allow people to create their own casts" | Marked "eventually" in the brief | Not built; the JSON format is documented and an embed takes any bundle from any host, which is the first step |
| 2026-10-20 | The JPEG, SVG, animated and thumbnail versions of every storyboard | Committing every panel in every image format would be about 50 MB that goes stale with any line of dialogue | Thumbnails and link previews are committed (the page needs them before code runs); SVG, animated SVG, PNG and JPEG of any panel are drawn in the browser on request by the API's export.js |
