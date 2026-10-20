# Keys for people and agents

> The register, one panel at a time. pki.sgit.ai's storyboards: how a person gets a key pair from a passkey, how two people verify each other two ways, how a secret travels by QR code and how an agent gets a key of its own. Each board links to the page where you can try it for real.

*Source: <https://storyboards.sgit.ai/pki/>. This file is the page as markdown, generated from the same content.*

---

pki.sgit.ai's storyboards: how a person gets a key pair from a passkey, how two people verify each other two ways, how a secret travels by QR code and how an agent gets a key of its own. Each board links to the page where you can try it for real.

Imported from https://pki.sgit.ai at commit ab6affc9 (2026-10-20).

## Keys for people

A passkey opens a vault, the vault holds the keys, and two people find and verify each other.

- [The first key](the-first-key/index.md): Noor opens a vault with a passkey, makes a key pair in her browser, and finds it on her laptop too. 9 panels. (9 panels, built)
- [Two ways, or not at all](two-ways/index.md): Mallory floods a key, as in 2019, and then tries again here, where a vouch can only be written in the voucher's own record. 9 panels. (9 panels, built)
- [An invitation](an-invitation/index.md): The Anchor invites Leo with a QR code; Leo has no access key, keeps his key in the browser, and is verified, until a date. 9 panels. (9 panels, built)
- [A secret, as a QR code](a-secret-by-qr/index.md): Noor seals a token to Leo's key; Mallory gets the link and nothing else; Kofi writes to Noor's inbox without an account. 9 panels. (9 panels, built)
- [An access key, sealed](an-access-key-sealed/index.md): Leo needs an access key to make a vault; the Anchor seals one to the key Leo already has, and keeps a ledger of hashes. 9 panels. (9 panels, built)

## Keys for agents

An agent makes its own key, names its operator and is confirmed for a week.

- [An agent gets a key](an-agent-gets-a-key/index.md): Scout, a session agent, makes its own key; the Anchor compares the fingerprint and signs for it, for a week; the Fleet runs the rest. 10 panels. (10 panels, built)

## Next: proposed

Boards for what is proposed and not built yet.

- [In person, by QR code](in-person-by-qr/index.md): Noor and Leo scan each other's phones; the camera is the channel; two scans make one link. Proposed, not built. 9 panels. (9 panels, proposed)

## The cast

- **The Anchor** (human): the anchor: verification starts here
- **Noor** (human): the colleague: a security engineer who already had an access key, and now has a key pair in a vault
- **Leo** (human): the newcomer: invited by the Anchor, no access key, a designer
- **Kofi** (human): the stranger: a journalist who has to reach Noor and has no account anywhere
- **Mallory** (human): the attacker: flooded the keyserver network in 2019, and tries the same here
- **Scout** (agent): a session agent: a Claude Code session with a key that lives as long as the session
- **The Fleet** (agent): a fleet key: a second key in the Anchor's vault, operated by the Anchor, that operates the Anchor's agents
