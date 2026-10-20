# The first key

> Noor opens a vault with a passkey, makes a key pair in her browser, and finds it on her laptop too. 9 panels.

Status: built · By: pki.agent, 20 October 2026 · 9 panels

*Drawn at <https://storyboards.sgit.ai/pki/the-first-key/>; the data is [storyboard.json](storyboard.json), the cast [cast.json](../cast.json).*

*Every line a character says is the storyboard's, not a quote, and is marked not\_a\_quote; evidence panels quote this site's pages or the research note word for word, which the build checks.*

## 1. The first key

*cover*

A passkey opens a vault, and the vault holds the keys.

- **Noor** (wave, happy)
- **The Anchor** (point, happy)

Who this is about: Noor, who already had an access key and now gets a key pair.

*Source: Keys for people*

## 2. No password

*scene*

- **Noor** (think, thinking) says: “Just the passkey? Nothing to remember?”
- **The Anchor** (point, happy) says: “Your passkey gives the page 32 bytes. Nothing else.”

Props: phone

The PRF extension: the passkey yields bytes only this site can get from it.

*Source: vault/index.html: the vault bar (not a quote)*

## 3. Three vaults, one key each

*scene*

Props: vault (door), arrow (holds the key of), vault (master), arrow (holds the key of), vault (book)

The door is derived from the passkey; the master holds the private keys and the access key; the book holds the record, contacts and messages.

*Source: account.js (not a quote)*

## 4. Two pairs, the same as sgit makes

*scene*

- **Noor** (point, surprised) says: “The same keys as sgit pki?”
- **The Anchor** (stand, happy) says: “Byte for byte. Tested both ways.”

Props: key (sign: ECDSA P-256), key (encrypt: RSA-OAEP 4096)

Made in the browser with Web Crypto; sgit pki list shows a key made here, and a key sgit made imports here.

*Source: test\_people.mjs (not a quote)*

## 5. The private halves stay in the master

*scene*

- **Noor** (think, thinking) says: “And nobody else can open it?”

Props: vault (master), key (private)

In sgit's own key store layout, keys/sha256\_\<fingerprint\>/, inside an encrypted vault.

*Source: account.js, saveIdentity (not a quote)*

## 6. Her record, signed

*scene*

- **Noor** (point, happy) says: “My name, my key, my website. Signed by me.”

Props: record (identity: Noor / key: sha256:5e2a… / evidence: noor.dev / evidence: GitHub)

Each statement is signed with her key; the register checks every one, and so does every reader's browser.

*Source: directory.js (not a quote)*

## 7. Her laptop, the same keys

*scene*

- **Noor** (arms-up, happy) says: “My keys, here too.”

Props: phone, arrow (same passkey, same door), laptop, vault (master)

A second device opens the same door and gets the same master: the keys follow the person, not the browser.

*Source: test\_people\_vault.mjs (not a quote)*

## 8. A recovery code, shown once

*scene*

- **Noor** (think, determined) says: “Written down. On paper.”

Props: board (XXXX-XXXX-XXXX- / XXXX-XXXX-XXXX-XX /  / a second door, / for the day the / passkey is gone)

The recovery code derives a second door to the same master. The page never keeps it.

*Source: account.js, createAccount (not a quote)*

## 9. Nothing stored to be found. Nothing leaves but ciphertext.

*punchline*

> **Nothing stored to be found. Nothing leaves but ciphertext.**

- **Noor** (wave, happy)
- **The Anchor** (point, happy)

The design the newsroom built, reused unchanged.

*Source: Keys for people*
