# Pixel pack

> The lab cast as 16 by 24 pixel sprites on a canvas, coloured from the cast's look fields, with a four-frame walk and three moods.

*Source: <https://storyboards.sgit.ai/lab/pixel-pack/>. A standalone experiment of the Lab, status exploring, pinned to api.storyboards.sgit.ai v0.1.0. The page is drawn by code; this file is what it says.*

---

**The question.** What survives of a cast when each character is a 16 by 24 pixel sprite generated from a few lines of text?

## What this taught us

- Sixteen by twenty-four carries a skin, a hair shape, a shirt and a trouser colour, and three moods, because each needs only the eyes and a two-pixel mouth. The kit's other seven moods need brows, and there is no row for a brow between the hair and the eyes. Headphones read, because two accent-coloured blocks beside the head are unmistakable; the lanyard reads as a stripe with a card, which is enough; glasses were a dark bar across the eyes until the lenses got white pixels, which costs three rows of a nine-row face and pushes the eyes a pixel apart, so a character with glasses is a different face, not the same face with glasses.
- The walk is a front-view walk: one foot lifts, then the other. It reads as walking because the figure also moves, not because the legs convince. A side-view stride would need a second drawing of every character, and the kit's seven poses would each need their own frames, so the pose vocabulary did not survive the trip at all.
- A game engine could eat these as they are: every frame is a fixed 16 by 24 cell, the frames strip is already a sprite sheet, and KAPLAY or Phaser load a sheet by giving a frame size and a frame count. The text description is the format Bitsy and PICO-8 sprites use, so the cast could be edited in any of those. Status: not tried here; the lab vendors KAPLAY, so that is the next experiment.
- Only the look data crossed over. The drawing shares nothing with the kit, and the sprite needs an idle and a walk that the cast file does not know about. If the cast JSON is the contract between packs, a pack has to invent what the file does not say and the file must not mind.

[The Lab](https://storyboards.sgit.ai/lab/index.md)
