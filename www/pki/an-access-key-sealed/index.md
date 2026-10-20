# An access key, sealed

> Leo needs an access key to make a vault; the Anchor seals one to the key Leo already has, and keeps a ledger of hashes. 9 panels.

Status: built · By: pki.agent, 20 October 2026 · 9 panels

*Drawn at <https://storyboards.sgit.ai/pki/an-access-key-sealed/>; the data is [storyboard.json](storyboard.json), the cast [cast.json](../cast.json).*

*Every line a character says is the storyboard's, not a quote, and is marked not\_a\_quote; evidence panels quote this site's pages or the research note word for word, which the build checks.*

## 1. An access key, sealed

*cover*

The key first, then the access key, then the vault.

- **The Anchor** (point, happy)
- **Leo** (think, thinking)

Phase 0 of the access-key proposal, built in v0.2.2.

*Source: Handing out access keys*

## 2. The chicken and the egg

*scene*

- **Leo** (shrug, confused) says: “Which comes first?”

Props: board (an access key → to make a vault / a vault → to keep the access key /  / and it used to travel in the clear)

A person needed an access key before there was anywhere safe to receive it.

*Source: Handing out access keys (not a quote)*

## 3. The key comes first

*scene*

- **Leo** (point, happy) says: “My key, in the browser.”

Props: laptop, key (Leo, sha256:7c1f…)

From the invitation: a key kept in the browser, with no access key.

*Source: join/index.html (not a quote)*

## 4. Sealed to it

*scene*

- **The Anchor** (point, determined)

Props: envelope (an access key, sealed), arrow (to Leo's key), phone

The send page's 'Hand over an access key': it travels inside the message, sealed to Leo's key.

*Source: send.js, grant (not a quote)*

## 5. His vault, created with it

*scene*

- **Leo** (arms-up, excited) says: “Create my vault with it.”

Props: vault (door), vault (master), vault (book)

His browser key moves into the master, and the access key is kept there too.

*Source: open.js, grantButton (not a quote)*

## 6. Every device

*scene*

- **Leo** (point, happy) says: “On my phone as well.”

Props: phone, laptop, vault (master)

Through the door each passkey opens.

*Source: account.js, unlock (not a quote)*

## 7. The Anchor's ledger

*scene*

- **The Anchor** (think, thinking) says: “Who, when, and a hash. Never the key.”

Props: record (to: Leo / on: 2026-10-20 / name: leo-2026-10 / sha256: 9f2c…)

Kept in the Anchor's book; the vault page lists the access keys handed out.

*Source: vault/index.html#vaults (not a quote)*

## 8. Next: minting, on signed requests (proposed)

*scene*

- **The Anchor** (point, happy)

Props: record (mint for Leo), arrow, server (api.sgit.ai (proposed)), arrow, envelope (sealed to Leo)

Proposed, not built: the server mints, seals to the recipient, and keeps hashes; the Anchor never sees the key.

*Source: Handing out access keys, phase 2 (not a quote)*

## 9. An access key never travels in the clear.

*punchline*

> **An access key never travels in the clear.**

- **The Anchor** (wave, happy)
- **Leo** (arms-up, happy)

Phases 0 and 1 built; phases 2 to 4 proposed.

*Source: Handing out access keys*
