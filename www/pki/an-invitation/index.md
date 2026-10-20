# An invitation

> The Anchor invites Leo with a QR code; Leo has no access key, keeps his key in the browser, and is verified, until a date. 9 panels.

Status: built · By: pki.agent, 20 October 2026 · 9 panels

*Drawn at <https://storyboards.sgit.ai/pki/an-invitation/>; the data is [storyboard.json](storyboard.json), the cast [cast.json](../cast.json).*

*Every line a character says is the storyboard's, not a quote, and is marked not\_a\_quote; evidence panels quote this site's pages or the research note word for word, which the build checks.*

## 1. An invitation

*cover*

A QR code with the link printed above it.

- **The Anchor** (point, happy)
- **Leo** (wave, happy)

How the register grows: person to person.

*Source: invite/index.html*

## 2. Scan this

*scene*

- **The Anchor** (point, happy) says: “Scan it with your camera.”
- **Leo** (stand, thinking)

Props: phoneqr, phone

The invitation is signed by the Anchor's key and names nobody: Leo has no key yet.

*Source: message.js, invite (not a quote)*

## 3. Who is inviting me?

*scene*

- **Leo** (think, thinking) says: “Signed by them. It checks.”

Props: board (Invited by: The Anchor / signature: checks / valid until 2026-11-19)

The join page checks the invitation against the inviter's key in the register.

*Source: join/index.html (not a quote)*

## 4. No access key

*scene*

- **Leo** (shrug, worried) says: “I don't have an access key.”
- **The Anchor** (point, happy) says: “You don't need one to start.”

Creating vaults needs an SG/Send access key; joining does not.

*Source: join/index.html, step 1 (not a quote)*

## 5. A key in the browser

*scene*

- **Leo** (think, determined) says: “A passphrase, then. A long one.”

Props: laptop, key (private, encrypted)

Kept in the browser's storage, its private halves encrypted with a passphrase in sgit's own format; it moves into a vault later.

*Source: ui.js, keepInBrowser (not a quote)*

## 6. His record

*scene*

- **Leo** (point, happy)

Props: record (identity: Leo / link → The Anchor / method: invitation)

His first link points at whoever invited him; it waits for them to link back.

*Source: join/index.html, step 4 (not a quote)*

## 7. Verified, on a call

*scene*

- **The Anchor** (point, determined) says: “On a video call. Today. For a year.”

Props: record (link → Leo / method: video call / on: 2026-10-20), calendar (until 2027-10-20)

An anchor's link that names a method is a verification; the details stay in the anchor's vault.

*Source: vault/index.html#links (not a quote)*

## 8. A year later

*scene*

- **The Anchor** (think, thinking) says: “Time to check again.”

Props: calendar (expired 2027-10-20), mark

After its end date Leo is still linked, both ways, but no longer verified; the anchor's vault lists who is due.

*Source: directory.js, validUntil (not a quote)*

## 9. Verified: by whom, how, and until when.

*punchline*

> **Verified: by whom, how, and until when.**

- **The Anchor** (wave, happy)
- **Leo** (arms-up, happy)

Dinis's decision of 19 October: a verification has a date, and is done again.

*Source: Keys for people*
