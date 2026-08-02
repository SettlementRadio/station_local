# COMMISSION.md — writing new canon for Settlement Radio

> **For a commissioned writer.** Everything you need to produce a canon file that loads, passes
> validation, and sounds like the world. Read this once end to end before you start, then
> [`SPIRIT.md`](SPIRIT.md) — the creative brief — which is what makes the writing *good*. This file
> only makes it correct.
>
> **This file is not world content.** It carries no frontmatter (see §2), so the loader skips it.

**The premise, in four lines.** Humanity lives scattered across many settled worlds, six centuries
on from now. Travel between worlds takes **weeks**; there is no faster-than-light anything and never
will be. Radio is the thread that connects them, and Settlement Radio is the station that broadcasts
it, drifting between the worlds so it can talk to everyone. Earth is distant history, spoken of
fondly.

---

## 1. What to write

**Six pieces remain.** Two are new files, four are top-ups to files that already exist. Take them
one at a time; do not attempt the world in one sitting.

> **Done and accepted: `72-celebrity.md`, `41-crime.md`, `36-logistics.md`.** Read all three before
> starting anything else — they are the standard to match.
>
> - All three handle named places exactly right, and each anchors an event to existing canon
>   **without using a year** — the hardest rule in §4A.
> - **`41-crime.md` and `36-logistics.md` are the models.** They carry their texture *into the fact
>   list* rather than leaving it in prose: the basket of dry socks by the tribunal door, the
>   children at Far Reach producing several container totals and no figure the loadmaster will
>   sign. Both are canon facts, so the station can actually say them. That is §3's rule working.
> - **`36-logistics.md` shows the best move available to you: extend, don't restate.** Its burn-day
>   section builds on a fact `70-music.md` had already established (lane-rock's great occasion) and
>   adds the freight crew's side of the same day. Reading the neighbouring files is not a
>   consistency chore — it is where the strongest material comes from.
> - `41-crime.md` also handles its domain's trap (no method detail, no glorification, no victims as
>   colour) more thoroughly than anything else in the bible.

### New files

| Filename | `id:` | `domain:` | What it covers | Target |
|---|---|---|---|---|
| `11-earth.md` | `earth` | `history` | Earth as memory — what is remembered, what is myth, what was carried and what was lost. | 10–12 facts |
| `12-crossings.md` | `crossings` | `history` | The migration and the founding: the generation-ships, the long scattering, settlements that failed. | 10–12 facts |

**Why two history files when history already has 21 facts.** History is the station's overnight
backbone, its strongest format, and the lead content for a very large pre-built archive — the
domain carrying the most hours on air has one of the smaller piles behind it. More history is always
the right answer.

### Top-ups to existing files

| File | Domain | Add | Note |
|---|---|---|---|
| `52-sports.md` | `sport` | +6 facts | A results desk needs persistent structure — leagues, standings, who plays whom. |
| `56-style.md` | `fashion` | +6 facts | Only works tied to material constraint. Cloth is scarce; salvage is an aesthetic. |
| `54-health.md` | `health` | +4 facts | Clinics, access, who gets care and who travels weeks for it. |
| `20-peoples.md` | `peoples` | +4 facts | Peoples shaped by the worlds they live on. |

Read the existing file first and match it. You are extending someone's world, not restarting it.

**Write texture, not just structure.** The one criticism of the accepted `72-celebrity.md` is that
it explains how its domain *works* — the customs, the rules, the institutions — more than it gives
the station things to actually *talk about*. Structure is necessary and it got that right. But a
domain also needs the small, concrete, human material a five-minute item is built from: the specific
quarrel, the daft tradition, the thing someone always gets wrong. Aim for both, and lean toward the
material.

---

## 2. The header block

**Every content file opens with this, before anything else. No blank line above it.**

```yaml
---
id: celebrity
domain: celebrity
scope: universe
status: active
supersedes: []
---
```

- **`id`** — the filename without its number and extension. Unique across the folder.
- **`domain`** — from the table in §1. **Copy it exactly.** There are seventeen domains in the whole
  system and they are a closed list; you cannot invent one, and a typo will fail the load.
- **`scope`** — always `universe` for everything in this commission.
- **`status`** — always `active`.
- **`supersedes`** — always `[]`.

**A file without this block is treated as a note, not as world content, and never reaches the
station.** That is the only thing marking the difference. The number in the filename (`41-`, `72-`)
is human reading order and carries no meaning — just don't reuse a number already in the folder.

---

## 3. Format

A file has two kinds of writing in it, and both are used.

### Prose sections — `## Some Topic`

Write **1,000–2,000 words** across two to five `## ` sections. This is where the world gets
described: how the thing works, how it feels, what it is like to live inside. Write it well; write
it evocatively. This prose is what a generated **domain summary** is built from, and that summary
is present in *every single thing the station makes*, so a domain written vaguely makes the whole
station vaguer.

### Canon facts — one `## Canon facts` section

At the end of the file, a numbered list:

```markdown
## Canon facts

1. Hollowball is the stations' own sport — five a side in the weightless hollow of a rotation hub,
   every station's court a different shape, so the home advantage is real and everyone accepts it.
2. Most sport is amateur: shift leagues, children's leagues, the crowded gymnasium after work, and
   wagering that is small, constant, and settled on reputation.
```

- **One atomic assertion each, 1–3 sentences.** Not a paragraph. Not a topic. One checkable thing
  the writers must stay consistent with.
- **This list is the only part of your file that can be quoted on air.** The prose shapes how the
  station understands the domain; the facts are what it can actually reach for and say. A detail
  left in a paragraph will colour the station's sense of the world and never be spoken. **If it
  should reach the microphone, make it a fact.**
- **Name things, and name them the same way twice.** Proper nouns are how the retrieval system finds
  anything — a world, a league, a ship, a company. Invent names freely; then be consistent.
- **Plain and concrete.** See §4G — this is the rule writers break most.

### Anchors

Put a `{#anchor}` on any **named thing the world will refer back to** — a faction, a named ship, an
institution, an observance, a legendary figure:

```markdown
### The Ashfall Minute {#the-ashfall-minute}
```

Lowercase, hyphens, no apostrophes. Once written, an anchor is permanent — the station may have
already broadcast something that points at it. Adding is free; renaming breaks continuity.

### Cross-references

Refer to another file plainly — `see 05-worlds.md`. Don't invent a linking syntax.

---

## 4. Never — the hard list

Everything here fails validation, gets a segment killed, or quietly rots the world. It is the most
important section in this document.

### A. No dates, no fixed years, no counted durations

The in-world year is **always the real year plus 600**, calculated fresh every time the station
speaks. It is never written down.

- ❌ `2627` · `In the year 2626…` · `by 2650`
- ❌ "three hundred years after the Founding" · "eleven years since the war"
- ❌ "The Lumen Festival falls on the 24th"
- ✅ "six centuries on" · "generations ago" · "within living memory" · "long enough that no one
  remembers starting it"

**A recurring thing is canon; a dated instance of it is not.** Write the festival — what it is, what
people do, what it means. The date it lands on this year is generated, not authored. Anything with a
date in it goes stale the moment the calendar moves past it, and the station will still be reading
it aloud.

### B. Nothing the world generates for itself

Canon is the **static substrate**. It changes only when you change it. If a thing could become
untrue without anyone editing a file, it is not canon:

| Don't write | Because it is |
|---|---|
| Living people, who currently holds an office | generated world state |
| Current disputes, ongoing storylines, "tensions are rising" | generated storylines |
| Prices, results, standings, chart positions | generated daily |
| "A ferry ran late", "the harvest was poor this year" | disposable one-day texture |

**Legendary and dead figures are canon. Living figures are not.** Write the pilot whose call-name
outlived her; do not write the pilot currently leading the circuit.

### C. Physics the world has already settled — these are fixed

The limits are the shape of this world, not obstacles awaiting a solution. Contradicting them
breaks the premise the whole station rests on:

- **No faster-than-light. Nothing that shortens a crossing.** No one is researching it; the universe
  has answered no. Weeks between worlds is load-bearing.
- **No instant communication.** Signals hop relay to relay — hours to the near worlds, a day or two
  to the frontier. The lag is the point, not a problem being fixed.
- **No medical miracles.** No regenerated limbs, no reversal of ageing, no copying a mind out of a
  body. Human bodies and lifespans are unchanged: illness happens, death comes.
- **Machine minds are tools, not persons**, by settled custom. Humanity is, so far as it knows,
  alone.

### D. No modern-AI futurism

This is classic mid-century science fiction, not a story about our present anxieties. Never:

- the singularity, superintelligence, "take-off", "the AI woke up"
- chatbot, large-language-model, or algorithmic-feed flavour of any kind
- uploading as salvation, digital afterlives
- surveillance-algorithm dystopia as the mood of the world

If thinking machines appear, treat them the mid-century way: capable tools, and the ethics puzzles
they raise. The wonder here is **human** — distances, letters, lamps, the radio, the night sky.

### E. Nothing real

No real place, nation, brand, corporation, religion, language, or living person, by name or by
thin disguise. **Earth is the single exception** — Earth and the pre-diaspora past are canon, and
are spoken of fondly and at a distance. See §5 for the IP rule, which is stricter still.

### F. The trap in each domain

Each of these kills a segment outright. If you are writing the domain, this line governs it:

| Domain | Never |
|---|---|
| `crime` | **No method detail. No glorification. No victims used as colour.** |
| `health` | **Never anything that reads as actionable medical advice.** In-world conditions and in-world treatments only. |
| `conflict` | Cover consequence and cost — never hardware, never tactics. **Nothing should read as thrilling.** |
| `religion` | Report belief as practice. No advocacy, no mockery. |
| `celebrity` | **In-world figures only, always.** No real-person analogues. |
| `fashion` | Tie it to material constraint. Style under scarcity is interesting; style in the abstract is not. |
| `sport` | Results mean nothing without persistent structure behind them. |
| `politics` | All process and no consequence is dead air. Reach someone it affects. |
| `finance` | Abstraction kills it. Prices are somebody's rent. |
| `logistics` | It is people and cargo and delay, not schedules. |

### G. Never write a fact in the station's poetic register

This one is invisible until it has ruined everything, so read it twice.

**Prose sections: write beautifully.** That is what they are for.

**Canon facts: write plainly.** Facts steer generation directly — the world's machinery imitates
them — so a bible full of luminous aphorisms produces a station where the sports desk and the
market report both talk like a poem at midnight. Validation measures this and will block work whose
epigram density is too high.

- ❌ "The relay is the thread of light that binds the lonely dark, and every soul leans toward it."
- ✅ "Relay maintenance is coordinated once a year; for six hours the far worlds hear nothing, and
  people plan sleep and gatherings around it."

Concrete stakes, everyday speech, opinions, mild complaints. The people in this world are not
elegising it at each other — they live in it.

---

## 5. IP — the one rule that governs everything

**Settlement Radio is a tribute to 20th-century science fiction, not a derivative of it.** Take the
spirit. Leave the stuff.

| ✅ Take | ❌ Never |
|---|---|
| Moods, themes, questions, the *feel* of a tradition | Any real author's, work's, or franchise's **name** |
| The *kind* of idea ("machine ethics as a moral puzzle") | **Named** characters, ships, planets, species, institutions |
| The emotional register — awe, melancholy, wonder | **Coined terms** an author invented (a specific word for FTL radio, a specific law of robotics) |
| The tradition of a movement — golden age, new wave | Plot beats, settings, or **quotable lines** from a real work |

**The litmus test: if a reader could name the source franchise or author from your fact, rewrite
it** until only the mood or idea is left, dressed in specifics you invented.

Also forbidden because they lean on someone else's world even when they sound generic: *core
worlds*, *outer worlds*, *the Federation*, *the Empire*, *terran*, *spice*, *ansible*, *foundation*.
Invent your own. Names like *Meridian*, *Cold Harbor* and *Ashfall* — already in this world — are
exactly the right instinct.

[`SPIRIT.md`](SPIRIT.md) §3 names the authors we draw on and, for each, what to take and what never
to touch. **That file is an internal brief and is never broadcast** — which is why it can name real
authors and your canon cannot.

---

## 6. Before you hand it back

- [ ] Frontmatter block at the very top, `domain` copied exactly from §1.
- [ ] 1,000–2,000 words of `## Topic` prose, plus one `## Canon facts` numbered list at the target
      count.
- [ ] Every fact is one assertion, 1–3 sentences, plainly written.
- [ ] `{#anchor}` on every named thing the world will refer back to.
- [ ] Searched your own file for a four-digit year. There are none.
- [ ] Nothing living, current, or dated. Nothing that could become untrue on its own.
- [ ] FTL, instant messaging and medical miracles all still absent.
- [ ] No real author, work, character, franchise, place, brand or person anywhere.
- [ ] Read the facts aloud. If they sound like poetry, rewrite them as speech.
- [ ] Read the neighbouring files and confirm you contradicted none of them.
