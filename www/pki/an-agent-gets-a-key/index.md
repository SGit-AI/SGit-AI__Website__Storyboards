# An agent gets a key

> Scout, a session agent, makes its own key; the Anchor compares the fingerprint and signs for it, for a week; the Fleet runs the rest. 10 panels.

Status: built · By: pki.agent, 20 October 2026 · 10 panels

*Drawn at <https://storyboards.sgit.ai/pki/an-agent-gets-a-key/>; the data is [storyboard.json](storyboard.json), the cast [cast.json](../cast.json).*

*Every line a character says is the storyboard's, not a quote, and is marked not\_a\_quote; evidence panels quote this site's pages or the research note word for word, which the build checks.*

## 1. An agent gets a key

*cover*

The agent makes it. The operator signs for it.

- **The Anchor** (point, happy)
- **Scout** (wave, happy)
- **The Fleet** (stand, happy)

Dinis's proposal of 19 October, as built in v0.2.1.

*Source: Keys for agents*

## 2. Scout makes its key

*scene*

- **Scout** (point, happy) says: “My key. It stays here.”

Props: terminal ($ node pki-agent.mjs keygen \\ /     --name Scout --session / made: sha256:5f1e…a0c2 / private halves: ~/.sg-send/keys / they stay here)

In sgit's key store layout, so sgit pki uses the same key.

*Source: agents/pki-agent.mjs (not a quote)*

## 3. It names its operator

*scene*

- **Scout** (stand, happy)

Props: terminal ($ node pki-agent.mjs operator \\ /     sha256:\<the Anchor\> / $ node pki-agent.mjs submit / sent, sealed, to the inbox), arrow (its record), envelope

A link in its own record, method operated-by, and its record sealed into the Anchor's inbox.

*Source: Keys for agents (not a quote)*

## 4. The comparison

*scene*

- **The Anchor** (think, thinking) says: “5f1e…a0c2. The same.”
- **Scout** (stand, happy)

Props: board (printed in the session: / sha256:5f1e…a0c2 /  / shown in the vault: / sha256:5f1e…a0c2)

The fingerprint the agent printed in its own session, against the one the vault shows. That comparison is the verification.

*Source: vault/index.html#agents (not a quote)*

## 5. Signed, for a week

*scene*

- **The Anchor** (point, determined)

Props: record (link → Scout / method: operates / until: 2026-10-27), calendar (7 days)

A session key is confirmed for days, not a year.

*Source: directory.js, AGENT\_DAYS (not a quote)*

## 6. Operated

*scene*

- **Scout** (arms-up, happy) says: “Operated by the Anchor.”

Props: board (Scout / an agent operated by / The Anchor / until 2026-10-27)

Two links, one in each record, the same rule as for people.

*Source: people/person.html (not a quote)*

## 7. It signs its work

*scene*

- **Scout** (point, happy)

Props: terminal ($ node pki-agent.mjs sign report.md / written: report.md.sig / $ sgit pki verify report.md \\ /     report.md.sig / Signature valid), mark

Anyone checks it with sgit, because the agent's key is an sgit key. The articles on this site are signed this way.

*Source: test\_agent\_tool.mjs (not a quote)*

## 8. A week later

*scene*

- **Scout** (shrug, worried) says: “Confirm me again?”

Props: calendar (ended 2026-10-27)

After the end date: to be confirmed again, from the same tab.

*Source: directory.js, standing (not a quote)*

## 9. Many agents: the Fleet

*scene*

- **The Anchor** (point, happy)
- **The Fleet** (stand, happy) says: “Operating the rest.”
- **Scout** (wave, happy)
- **Scout** (stand, happy)
- **Scout** (think, thinking)

A fleet key in the Anchor's vault confirms the agents; the Anchor's own record holds one link. Every agent page shows the Anchor at the root.

*Source: vault/index.html#agents (not a quote)*

## 10. The agent makes its key. The operator signs for it, for a week.

*punchline*

> **The agent makes its key. The operator signs for it, for a week.**

- **The Anchor** (wave, happy)
- **Scout** (arms-up, happy)

And the first agent in the register is the session that built this.

*Source: Keys for agents*
