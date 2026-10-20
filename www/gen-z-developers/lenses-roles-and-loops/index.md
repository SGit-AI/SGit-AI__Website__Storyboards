# Lenses, roles and loops

> How LLMs and agents work: a prompt as a lens, a role as a model with a description, an agent as a loop, tools as requests, no memory, compression, and focused threads. 13 panels.

Status: draft · By: gen-z.journalist, 18 October 2026, from Dinis's memo on LLMs and agents · 14 panels

*Drawn at <https://storyboards.sgit.ai/gen-z-developers/lenses-roles-and-loops/>; the data is [storyboard.json](storyboard.json), the cast [cast.json](../cast.json).*

*Every line the Guide says, and every quote card, is from the article 'Lenses, roles and loops', word for word; the build checks it. The five lenses on recursion, the weather question and the named threads are the storyboard's illustrations.*

## 1. Lenses, roles and loops

*cover*

It stops being magic when you see how it works.

- **Zara** (think, thinking)
- **The Agent** (wave, happy)
- **Priya** (stand, happy)
- **The Guide** (wave, happy)

The second half of the generative AI chapter: what happens when you use a model.

*Source: Lenses, roles and loops*

## 2. One idea, recursion, through five lenses

*spectrum*

- **The Guide** (point, happy)

Teenager (a meme of a meme) → Musician (a round, sung over itself) → Doctor (cells dividing into cells) → Football fan (the replay of the replay) → Portuguese (recursividade)

To a model, translating into another language is no different from translating for an audience: the prompt is the lens. The five analogies are the storyboard's, not the memo's.

*Source: Lenses, roles and loops, A prompt is a lens*

## 3. The wrong lens

*scene*

- **Priya** (shrug, worried) says: “I've always been bad at maths.”
- **The Guide** (point, happy) says: “The analogy is the reason someone understands something.”

Priya ran rotas, budgets and stock levels for years: maths all day, just not the kind school called maths.

*Source: Lenses, roles and loops, A prompt is a lens*

## 4. A role is a model with a description

*graph*

Graph: a raw model, role.md: who you are, what you refuse, a question, the editor, the publisher, the journalist

The same model behind every role on this site; what changes is the description and the question.

*Source: Lenses, roles and loops, A role is a model with a description*

## 5. An agent is a loop with a goal

*scene*

- **The Agent** (think, thinking)
- **The Guide** (point, happy) says: “Fundamentally the agent is simply a task: do this; then, are we done yet, or do we need to continue?”

And rinse and repeat. The loop is the skeleton; good agents add planning, checks and limits.

*Source: Lenses, roles and loops, An agent is a loop with a goal*

## 6. The loop, with one tool call

*graph*

Graph: the task, the model, a tool call: search the web, the harness runs it, the result, added, are we done?, the answer

The model never runs a tool: it writes a request; the program around it decides, runs it and sends the result back. If the answer to 'are we done?' is no, round again.

*Source: Lenses, roles and loops, Tools changed everything; Precisely*

## 7. What the next request carries

*spectrum*

- **Zara** (point, determined)

Your question (is it raining in Lisbon?) → Model asks (call the weather service) → Harness (calls it: 'light rain') → All of it, resent (question + call + result) → The answer (take an umbrella)

Two requests for one answer; the second holds everything the first did, plus the tool's result. (A made-up example.)

*Source: Lenses, roles and loops, Tools changed everything*

## 8. From training only, to tools

*spectrum*

- **The Guide** (stand, happy)

Nov 2022 (ChatGPT, no tools) → Mar 2023 (plugins) → Mid 2023 (functions for developers) → Nov 2024 (Model Context Protocol) → 2026 (the loop, many tools, hours)

Training is a compression of the world, frozen on the day it ended; tools let the model ask for what it does not hold.

*Source: Lenses, roles and loops, Tools changed everything*

## 9. It remembers nothing

*scene, setting: night*

- **Zara** (think, surprised) says: “So it doesn't remember what I said an hour ago?”
- **The Guide** (stand, happy) says: “There is no memory.”

Every request carries the whole conversation; that is why there is a context window, and why long chats get slower.

*Source: Lenses, roles and loops, It remembers nothing*

## 10. Long chats are compressed

*evidence*

- **The Agent** (think, thinking)

**What one summary keeps**

| | |
|---|---|
| the chat | 100% |
| its summary | 1.7% |

One session, one month: summarised eighteen times, each summary keeping on average 1.7% of what it replaced (re-anchoring, newsroom). What the summary leaves out is not forgotten; it was never given back.

*Source: Lenses, roles and loops, Long chats are compressed*

## 11. The newsroom's answer

*evidence*

- **The Guide** (point, happy)

> “The rules are restored, not remembered.”
>
> Source: Re-anchoring agent behaviour policies (newsroom)

The rules live in a file printed back after every summary.

*Source: Lenses, roles and loops, Long chats are compressed*

## 12. Many focused threads, each with a name

*graph*

Graph: a person, inbox.triage, inbox.drafts, gen-z.editor, gen-z.journalist, the files

One topic per session keeps what each model has to hold small; the sessions talk through files, never through memory. The thread names are illustrative.

*Source: Lenses, roles and loops, Many focused threads*

## 13. Where the memory is

*evidence*

- **Tomás** (think, thinking)

> “Nothing is remembered by the model between sessions. Everything is remembered by the files.”
>
> Source: Memory is not a spectator sport (newsroom)

The principle the threads rely on.

*Source: Lenses, roles and loops, Long chats are compressed*

## 14. Not magic: a lens, a role, a loop.

*punchline*

> **Not magic: a lens, a role, a loop.**

- **Zara** (arms-up, happy)
- **Priya** (stand, happy)
- **The Agent** (wave, happy)

Understand it, and you are the one who sets the constraints.

*Source: Lenses, roles and loops, Why this matters*
