# A secret, as a QR code

> Noor seals a token to Leo's key; Mallory gets the link and nothing else; Kofi writes to Noor's inbox without an account. 9 panels.

Status: built · By: pki.agent, 20 October 2026 · 9 panels

*Drawn at <https://storyboards.sgit.ai/pki/a-secret-by-qr/>; the data is [storyboard.json](storyboard.json), the cast [cast.json](../cast.json).*

*Every line a character says is the storyboard's, not a quote, and is marked not\_a\_quote; evidence panels quote this site's pages or the research note word for word, which the build checks.*

## 1. A secret, as a QR code

*cover*

Encrypted in the browser. Only their key opens it.

- **Noor** (point, happy)
- **Leo** (stand, happy)
- **Kofi** (wave, happy)

What the register is for: find someone, and write to them.

*Source: send/index.html*

## 2. Not in a chat

*scene*

- **Noor** (think, determined) says: “A token for Leo. Not in a chat.”

Props: laptop, envelope (a token)

The case the brief led with: a secret that should reach one person.

*Source: Keys for people (not a quote)*

## 3. Sealed to Leo's key

*scene*

Props: key (Leo's public key, from the register), arrow (sealed here, in her browser), envelope (sgit envelope v2)

A fresh AES-256-GCM key, wrapped with RSA-OAEP to Leo; signed by Noor, the signature naming Leo inside it.

*Source: message.js (not a quote)*

## 4. A link, and a QR code

*scene*

- **Noor** (point, happy) says: “The part after the # never reaches a server.”

Props: qr

A short signed message is about 1,200 characters: one QR code.

*Source: test\_people.mjs (not a quote)*

## 5. Leo opens it

*scene*

- **Leo** (arms-up, happy) says: “Signed by Noor. It checks.”

Props: phone, envelope (opened with his key)

The message page opens it with the key in his vault, and checks both signatures against the register.

*Source: m/index.html (not a quote)*

## 6. Mallory has the link

*scene*

- **Mallory** (shrug, confused) says: “I have the link. And?”

Props: envelope (no key, no message), mark

Without Leo's private key the link is noise. Re-sealed to someone else, a signed message still says who it was for.

*Source: test\_people.mjs (not a quote)*

## 7. Kofi writes to Noor

*scene*

- **Kofi** (point, happy) says: “No account?”

Props: envelope, arrow (into her inbox), server (vault server: ciphertext only), sign ({"ok": true})

Noor's record publishes an inbox, an append lane: anyone can write, with no account; the answer is blind.

*Source: account.js, deliver (not a quote)*

## 8. Only Noor reads it

*scene*

- **Noor** (think, happy) says: “Opened in my vault. Nowhere else.”

Props: vault (Noor's book), envelope

The lane can be listed only with the enum key in her master, and read only with her private key.

*Source: vault/index.html#inbox (not a quote)*

## 9. Only their key opens it. Nothing readable passes through a server.

*punchline*

> **Only their key opens it. Nothing readable passes through a server.**

- **Noor** (wave, happy)
- **Leo** (arms-up, happy)
- **Kofi** (point, happy)

Send, open, inbox: built and tested end to end.

*Source: test\_people\_browser.mjs*
