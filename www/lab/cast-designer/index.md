# Cast designer

> A live character designer on the kit's drawCharacter: every look field as a control, two previews that redraw as you type, a random button, and the cast JSON ready to copy.

*Source: <https://storyboards.sgit.ai/lab/cast-designer/>. A standalone experiment of the Lab, status promising, pinned to api.storyboards.sgit.ai v0.1.0. The page is drawn by code; this file is what it says.*

---

**The question.** Which look fields make a character, and what does a cast file need that the drawing does not?

## What this taught us

- The fields that matter, in order, at panel size: the shirt colour (the biggest flat area), the hair shape (the silhouette), the skin, then the accessory. Trousers barely register, because the legs are thin strokes; a height of 0.8 against 1.2 only reads when two people stand side by side. Two people with the same shirt colour and hair shape are one person.
- A cast file needs what the drawing never reads: id, name, pronouns, role. The drawing reads what nobody would write by hand: height to two decimals. The designer writes exactly the cast format so the file is the only contract, and it hides hatColour unless the hair is a beanie and accentColour unless there are headphones or a lanyard, which the format itself does not.
- Random is only plausible with palettes. A random hex for skin makes a green person and a random shirt on random trousers makes a clown, so the random button draws from six skins, eight hair colours and ten shirts that live in this page. Those palettes belong in the kit as data, so a story can ask for a plausible stranger with one call.
- The second preview catches what the first hides. Ines, with long near-black hair, loses raised brows (surprised, worried) against the fringe, because the kit draws brows in ink over hair of almost the same colour; a thinking hand sits in front of a lanyard's cord. The small figure at another pose and mood showed both. One preview is not a check; the model sheet is.

[The Lab](https://storyboards.sgit.ai/lab/index.md)
