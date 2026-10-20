# Dialogue engine

> A visual-novel scene on a kit panel: typed-out lines in a seeded Rough.js bubble, a branching script as data, and the reader's choices as buttons.

*Source: <https://storyboards.sgit.ai/lab/dialogue/>. A standalone experiment of the Lab, status exploring, pinned to api.storyboards.sgit.ai v0.1.0. The page is drawn by code; this file is what it says.*

---

**The question.** What happens to a storyboard when the reader chooses the next line and the text types itself out?

## What this taught us

- A reader's choice turns a storyboard from a sequence into a graph, and the panel stops being the unit: the unit becomes the node (who, what, mood, pose) and a panel is whatever nodes the reader passed through. The log under the panel is the storyboard the reader wrote; two readers get two storyboards from the same script. For a deck, that means the still pictures cannot be rendered ahead of time unless every path is rendered, which for ten nodes with two forks is four strips.
- Typed text changes the pacing from the reader's to the author's. At 40 characters a second a line of 90 characters takes a little over two seconds to appear, and the reader waits for it; in a drawn bubble they read it in under a second and move on. The waiting is the point when a line should land (Oto's interruption reads better typed), and a cost everywhere else, which is why skip has to be one key and one click. Status: exploring.
- The data needs less than expected: an id, who speaks, the text, a mood and a pose, and either a next or a list of choices. What it also needs, and this page checks on apply, is a validator: a choice that points at a missing node is the error a reader hits last and an author hits first. What the data does not say yet, and would have to, is where people stand and when they enter; Oto's entrance is hard-coded here.
- The kit draws the people but not the bubble, so the bubble here is the page's own (a rounded rectangle and a tail, in the kit's ink, with the same Rough.js seed each redraw so the box does not boil while the text types). Changing a character's mood means redrawing the whole character with the same seed, which is quick but visible as a flicker on slow machines; a bubble and a face that could be updated in place are the two things to lift into a release.

[The Lab](https://storyboards.sgit.ai/lab/index.md)
