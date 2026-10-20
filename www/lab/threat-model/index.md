# A threat model, probed

> A data-flow diagram as data, drawn in the kit's ink; the attacker walks to each flow and asks a STRIDE question, the author's answer appears red (open) or green (mitigated), and the watcher's face follows.

*Source: <https://storyboards.sgit.ai/lab/threat-model/>. A standalone experiment of the Lab, status promising, pinned to api.storyboards.sgit.ai v0.1.0. The page is drawn by code; this file is what it says.*

---

**The question.** Can a threat model (a data-flow diagram and its STRIDE findings) be played as a storyboard instead of read as a table?

## What this taught us

- The attacker is the best narrator: a threat is a question somebody asks at a flow, and drawing the person asking turns a table row into a scene with a point of view.
- Open and mitigated are the only two moods a finding needs: red or green on the card, worried or calm on the watcher's face. A severity scale would have been a verdict.
- The DFD wants its own drawing vocabulary: entity, process, store, boundary are four shapes, all a prop pack away. This page draws them itself.
- A review is a path through the flows, like a flowchart's: the order the author probes them in is part of the argument and the data should carry it.
- A model this size fits a panel; a real one will not. Twelve flows need the camera and a chapter per boundary.

[The Lab](https://storyboards.sgit.ai/lab/index.md)
