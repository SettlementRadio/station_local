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

**This file is the standing brief.** Sections 2–6 are the contract and do not change between
commissions. §2's domain list is closed, so a commission is always *more depth in an existing
domain*, never a new one.

The first commission — five new files and four top-ups — brought every one of the seventeen domains
to at least twelve facts, the number the station can draw on for a single programme. **This second
one is about variation rather than coverage.**

### The current commission — two top-ups

| File | Domain | Now | Target | Add |
|---|---|---|---|---|
| ~~`30-polities.md`~~ | `politics` | ~~13~~ **22** | ~22 | **done — accepted** |
| `45-conflict.md` | `conflict` | 12 | ~22 | **+8, up to +10** |

> **`30-polities.md` is the model for the remaining file.** It answered its trap — *all process, no
> consequence* — not by mentioning people occasionally but by building the rule into the
> institutions themselves. The Burden Note requires every tariff proposal to name who absorbs it:
> the shipper, the port, the settlement store, or the person at the counter. *"A committee may
> choose the burden; it may not call the burden nobody's."* Every one of its nine new facts reaches
> somebody it affects.
>
> Do the same for conflict. Its trap is **spectacle**, so build the restraint into how the world
> works: what a blockade does to a clinic's stores, what a veteran came back to, who waits for the
> patrol that did not report. Never the hardware, never the tactics.

**Why these two, and why so many.** Both are **fast** domains in the station's schedule — politics
runs in the morning *and* evening magazines, conflict in the evening magazine — so they are drawn on
almost daily, while a slow domain with the same number of facts is used weekly. Twelve facts stops a
domain repeating itself; it does not give it *variety*. Each of these domains has about five
sub-areas, and at thirteen facts there are only two or three per area, so a programme about tariffs
and one about appointments reach for nearly the same material. At around twenty-two, each sub-area
has its own cluster.

That number is not a guess: `41-crime.md` and `36-logistics.md` were built from almost nothing in
the first commission and landed at 27 and 22 facts without anyone specifying a target. That is what
a properly written domain turns out to weigh.

**Format:** these are top-ups, not new files. Add new `## ` prose sections and append new numbered
facts to the existing list. You may edit the facts already there if the new material needs it — see
the mechanical notes below.

### What each domain covers, and the trap in it

**`30-polities.md` — politics.** Council votes, tariffs, appointments, factional manoeuvre,
settlement autonomy.
> **The trap: all process, no consequence.** Every political item must reach someone it affects. A
> fact about a procedure is worth little; a fact about what the procedure does to a person is worth
> a programme.

**`45-conflict.md` — conflict and military.** Border disputes, blockades, patrol incidents,
veterans, the aftermath of the old war. **This domain is sensitive.**
> **The trap: spectacle.** Cover consequence and cost — never hardware, never tactics. **Nothing
> here should read as thrilling.** The strongest form this domain takes is oral history: what the
> old war did to the people who came back, and to the places that waited. Write that.

---

### What the first commission established — read these before writing

`72-celebrity.md` · `41-crime.md` · `36-logistics.md` · `11-earth.md` · `12-crossings.md` ·
and the top-ups to `52-sports.md`, `56-style.md`, `54-health.md`, `20-peoples.md`.

Five lessons came out of them, in the order they matter:

1. **Put the texture in the fact list, not the prose.** The fact list is the only part of a file the
   station can quote (§3). `41-crime.md` made the basket of dry socks by the tribunal door a *fact*,
   so the tribunal can be described on air; `72-celebrity.md` left its best details in paragraphs,
   where they shape the domain summary and are never spoken.

2. **Extend a neighbouring fact; never restate it.** `36-logistics.md` took burn day — already
   established in `70-music.md` as lane-rock's great occasion — and wrote the freight crew's side of
   the same day. `12-crossings.md` made Brekka Voss's rediscovery (`15-figures.md`) the *reason*
   historians keep *unknown* distinct from *dead*. Reading the neighbouring files is not a
   consistency chore; it is where the strongest material comes from.

3. **Write the system, not the procedure.** Every domain has a trap (§4F). `54-health.md` must never
   read as medical advice, and it sidesteps that completely by writing about access rather than
   treatment — who gets seen, who travels, who goes with them, where they stay. Not one line of
   medicine, and still the most affecting file in the bible.

4. **Anchor to canon without using a year.** `11-earth.md` and `72-celebrity.md` both date a figure
   against Breathe Easy's unreliable first air plant (`06-gazetteer.md`) rather than a date. That is
   the hardest rule in §4A and it is always solvable this way.

5. **Ground the abstract in a named place.** `20-peoples.md` had ten facts about categories of
   human; its top-up added four customs belonging to four specific worlds — Meridian's storm-kin,
   Cold Harbor's Night Answer, the Forge knock, Ashfall's Second Address. A custom a world actually
   keeps is worth more than a paragraph about what its people are like.

**On real subjects:** `11-earth.md` cleared the hardest bar in this document. Earth is the one
real-world subject §5 permits, and the file names no real nation, city, person, institution or work
anywhere — every hook is an invented in-world artefact. That is how to write about something real.

**Two mechanical notes.** A top-up may **edit** the facts already there, not only append; editing is
safe because a fact's identity is fixed and only its text changes. And **match the existing file's
line wrapping** — roughly 100 characters. `52-sports.md` came back with 800-character paragraphs,
which load fine but make every future one-word change look like a full rewrite in version control.

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
- **Extend a neighbouring fact; never restate it.** Before writing, search the other files for your
  subject. If canon already establishes something, do not say it again in your own words — add the
  part nobody has written yet. `36-logistics.md` is the model: `70-music.md` had already made burn
  day the great occasion of lane-rock, so the logistics file left that alone and wrote the freight
  crew's side of the same day — the restraint checks, the meal, the object that escaped across the
  common room.

  This matters more than it sounds. Two facts saying the same thing do not contradict each other, so
  validation will not catch them, and both then compete for the same twelve retrieval seats — so a
  restatement quietly costs the domain a slot forever. **A fact that is already true somewhere in
  canon is not yours to write.**
- **Name things, and name them the same way twice.** Proper nouns are how the retrieval system finds
  anything — a world, a league, a ship, a company. Invent names freely; then be consistent.
- **Plain and concrete.** See §4G — this is the rule writers break most.

### Anchors

Put a `{#anchor}` on any **named thing the world will refer back to** — an institution, an
observance, a legendary figure, a named ship, a faction:

```markdown
### The Ashfall Minute {#the-ashfall-minute}
```

Lowercase, hyphens, no apostrophes. Once written, an anchor is permanent — the station may have
already broadcast something that points at it. Adding is free; renaming breaks continuity.

**Two kinds of thing take a prefix.** Named **ships** and **factions** are the only entities the
validator resolves by pattern, because everything else it checks is a database row and these are
not. Give them `ship:` or `faction:` before the slug — the one place a colon belongs in an anchor:

```markdown
### The Long Patience {#ship:long-patience}
### The Halcyon Compact {#faction:halcyon-compact}
```

`12-crossings.md` has the first of these. If you name a vessel or an organised group the world will
mention again, use the prefix; if you are unsure whether something counts, a plain anchor is safe.

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
- [ ] Read the neighbouring files. Confirm you contradicted none of them — **and that you restated
      none of them either.** Where canon already covers your subject, you extended it.
