# A flowchart, explained

> Mermaid text in, a graph laid out by dagre and drawn in the kit's ink, and a character who walks it along the edges, lighting each node and saying what it is for.

*Source: <https://storyboards.sgit.ai/lab/flowchart/>. A standalone experiment of the Lab, status promising, pinned to api.storyboards.sgit.ai v0.1.0, using dagre-1.1.4.min.js. The page is drawn by code; this file is what it says.*

---

**The question.** Can a diagram people already write (Mermaid) become a storyboard that explains itself, node by node?

## What this taught us

- The notes are the storyboard: the chart's nodes are the settings, the %% note lines are the lines spoken. Writing them showed which nodes were two steps pretending to be one.
- Layout is somebody else's problem and should stay so: dagre placed every example first time; the kit should draw what a layout engine returns, not grow its own.
- A walker needs a path, not a graph: explaining is linear even when the chart is not, so %% path is the author's one story through the diagram.
- Mermaid's syntax is enough and already everywhere: a chart from a README can be explained without being redrawn.
- The camera wants to follow: on a tall chart the walker leaves the screen; zooming the viewBox to the current node is the next step.

[The Lab](https://storyboards.sgit.ai/lab/index.md)
