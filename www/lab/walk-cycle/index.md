# Walk cycle

> An 11-joint rig posed by parametric walk, run, jump and idle cycles, then the same bones dressed in Oto's colours.

*Source: <https://storyboards.sgit.ai/lab/walk-cycle/>. A standalone experiment of the Lab, status exploring, pinned to api.storyboards.sgit.ai v0.1.0. The page is drawn by code; this file is what it says.*

---

**The question.** Can a stick-figure rig driven by a phase give a storyboard character a walk, a run and a jump, and still look like the kit?

## What this taught us

- A rig gives you every in-between for free: the four gaits here are four small functions of a phase, and speed, stride and direction are numbers, where the kit's seven drawn poses are seven fixed pictures with nothing between them. The cost is that a rig only knows what its functions know: a pose that is not on a cycle (think, shrug, sit) still has to be authored.
- A walk reads as a walk from two positions, not from the whole cycle: the contact (both legs straight and apart, the body at its lowest, phase 0.25 and 0.75 here) and the passing (the swinging leg bent under a body at its highest, phase 0 and 0.5). Get those two right and the in-betweens can be plain sine waves.
- Three things break it: the feet slide if the distance travelled per cycle does not match the stride (fixed by deriving the distance from the thigh swing); a run with the same bob as a walk looks like a fast walk (a run needs a flight phase, a forward lean and bent arms); and Rough.js redrawn every frame boils even with a fixed seed, because the wobble is proportional to a geometry that changes each frame.
- The costume over the bones is thick strokes in the shirt and trousers colours plus a skin circle and the beanie, with flat fills rather than the kit's hachure; it reads as the same character at a glance. Lifting this into the kit would mean drawing a character from a joint list instead of fixed offsets, a new release of drawCharacter, not a patch. Status: exploring.

[The Lab](https://storyboards.sgit.ai/lab/index.md)
