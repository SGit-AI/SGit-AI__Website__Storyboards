# Two ways, or not at all

> Mallory floods a key, as in 2019, and then tries again here, where a vouch can only be written in the voucher's own record. 9 panels.

Status: built · By: pki.agent, 20 October 2026 · 9 panels

*Drawn at <https://storyboards.sgit.ai/pki/two-ways/>; the data is [storyboard.json](storyboard.json), the cast [cast.json](../cast.json).*

*Every line a character says is the storyboard's, not a quote, and is marked not\_a\_quote; evidence panels quote this site's pages or the research note word for word, which the build checks.*

## 1. Two ways, or not at all

*cover*

Why a link only counts when both people wrote it.

- **Mallory** (shrug, thinking)
- **Noor** (stand, happy)
- **Leo** (wave, happy)

The rule that answers the 2019 keyserver flood.

*Source: people/how.html*

## 2. 2019

*evidence*

- **Mallory** (point, thinking)

> “a key server could add information to a certificate but could never delete either a certificate or information about a certificate.”
>
> Source: pki.sgit.ai, the 2019 failure

The design goal that made the flood possible, word for word from this site's failure page.

*Source: failure/index.html*

## 3. The flood

*scene*

- **Mallory** (arms-up, excited) says: “Anyone can add. Nothing can be deleted.”

Props: record (a key, 2019 / sig / sig / sig / sig … / ~150,000 sigs)

One key reached about 150,000 signatures; importing it broke the software.

*Source: failure/index.html (not a quote)*

## 4. The rule

*evidence*

- **The Anchor** (point, thinking)

> “The keyserver attack existed because anyone could append to anybody's certificate.”
>
> Source: pki.sgit.ai, the four rules

Rule 1, word for word: only the owner writes to their own record.

*Source: rules/index.html*

## 5. Where would Mallory write?

*scene*

- **Mallory** (shrug, confused) says: “Where do I write?”

Props: record (identity: Noor / signed by Noor), record (identity: Leo / signed by Leo), mark

A statement signed by another key, put in someone's record, is rejected: the test says so.

*Source: test\_people.mjs (not a quote)*

## 6. A claim

*scene*

- **Leo** (think, confused) says: “I don't know her yet.”

Props: record (link → Leo), arrow (a claim, one way)

A one-way link is visible in the claimant's record and adds nothing to the other person.

*Source: directory.js, graph (not a quote)*

## 7. A link

*scene*

- **Noor** (point, happy)
- **Leo** (point, happy)

Props: record (link → Leo), record (link → Noor), arrow (both ways: a link)

Linking back creates the link; each side is in its owner's record.

*Source: test\_people.mjs (not a quote)*

## 8. The register, computed

*graph*

Graph: The Anchor, Noor, Leo, Kofi, Mallory

Degrees of separation come from confirmed links only, computed each time a page opens.

*Source: people/index.html*

## 9. A vouch for you lands in my record, never in yours.

*punchline*

> **A vouch for you lands in my record, never in yours.**

- **Noor** (wave, happy)
- **Leo** (arms-up, happy)
- **Mallory** (shrug, worried)

Two-way links stop flooding. They do not stop lying: that is what the anchor and the evidence are for.

*Source: people/how.html#two-ways*
