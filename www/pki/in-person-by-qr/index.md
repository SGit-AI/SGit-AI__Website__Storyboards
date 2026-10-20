# In person, by QR code

> Noor and Leo scan each other's phones; the camera is the channel; two scans make one link. Proposed, not built. 9 panels.

Status: proposed · By: pki.agent, 20 October 2026 · 9 panels

*Drawn at <https://storyboards.sgit.ai/pki/in-person-by-qr/>; the data is [storyboard.json](storyboard.json), the cast [cast.json](../cast.json).*

*Every line a character says is the storyboard's, not a quote, and is marked not\_a\_quote; evidence panels quote this site's pages or the research note word for word, which the build checks.*

## 1. In person, by QR code

*cover*

Proposed: the next thing to build.

- **Noor** (point, happy)
- **Leo** (point, happy)

From the research note Dinis shared on 20 October, checked claim by claim.

*Source: In person, by QR code*

## 2. Noor's phone shows her key

*scene*

- **Noor** (point, happy) says: “Scan me.”
- **Leo** (stand, thinking)

Props: phoneqr, phone

Her key (or her record and its full hash) and a fresh nonce, in one QR code.

*Source: In person, by QR code (not a quote)*

## 3. Leo's camera reads it

*scene*

- **Leo** (think, happy) says: “Noor's key. From her hand.”

Props: board (Noor / key: sha256:5e2a… / scanned from her phone / expires in 4 minutes)

The phone's own camera opens the link; the page checks the key against the register.

*Source: In person, by QR code (not a quote)*

## 4. His answer carries her nonce

*scene*

- **Leo** (point, happy) says: “Now scan mine.”
- **Noor** (stand, thinking)

Props: phone, phoneqr

So his code belongs to this meeting and no other.

*Source: In person, by QR code (not a quote)*

## 5. Light, not a network

*scene*

- **Mallory** (shrug, confused) says: “Nowhere to stand.”

Props: phoneqr, arrow (by camera, both ways), phoneqr

The key travels from the phone in the other person's hand; nothing in between can swap it, so no short code or relay is needed.

*Source: In person, by QR code (not a quote)*

## 6. Both sign

*scene*

- **Noor** (point, happy)
- **Leo** (point, happy)

Props: record (link → Leo / method: in person / on: today), record (link → Noor / method: in person / on: today)

Two scans make one two-way link, the kind the register already counts; from an anchor, a verification.

*Source: In person, by QR code (not a quote)*

## 7. What it proves

*evidence*

- **The Anchor** (point, thinking)

> “Physical proximity makes the interaction convenient, but does not by itself establish identity.”
>
> Source: In-Person Public-Key Exchange on iPhone, the research note

The note's own caution, word for word: scanning proves a key came from a phone, not whose phone it is.

*Source: briefs/research-2026-10-20\_\_in-person-public-key-exchange.md*

## 8. An agent shows its key

*scene*

- **The Anchor** (point, happy)
- **Scout** (stand, happy)

Props: phone, terminal ($ node pki-agent.mjs whoami --qr / (a QR code, in text)), qr

Proposed too: an agent on a screen the operator can see prints its key as a QR code, and the phone compares all of it.

*Source: In person, by QR code, agents (not a quote)*

## 9. Two scans. One link. No server.

*punchline*

> **Two scans. One link. No server.**

- **Noor** (arms-up, happy)
- **Leo** (arms-up, happy)

Proposed for the next release, if Dinis agrees.

*Source: In person, by QR code*
