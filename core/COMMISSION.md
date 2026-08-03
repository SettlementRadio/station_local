# COMMISSION.md — rewriting the station core

> **For a commissioned writer.** This covers the two files in `core/` — `STATION.md` and `TIME.md`.
> Read this once end to end before you start. It assumes no access to the repository and no
> knowledge of the architecture.
>
> **This file is not station text and is never broadcast.** It names mechanisms freely; the files
> you write may not.

**The premise, in four lines.** Humanity lives scattered across many settled worlds, six centuries
on from now. Travel between worlds takes **weeks**; there is no faster-than-light anything and never
will be. Radio is the thread that connects them, and Settlement Radio is the station that broadcasts
it, drifting between the worlds so it can talk to everyone. Earth is distant history, spoken of
fondly.

---

## 0. What `core/` is, and why it is unlike anything else

There are three kinds of text in this project and they behave completely differently:

| | What it is | How it reaches a programme |
|---|---|---|
| **canon** (`canon/`) | the world bible — 370 facts | **searched.** A handful of relevant facts are retrieved per programme |
| **cast cards** (`cast/`) | six presenter cards | **always present**, but only for whoever is on air |
| **`core/`** — this commission | the station's identity, premise and clock | **always present, always, on every single call** |

`core/` is pasted whole and verbatim into the writing model's instructions **every time the station
generates anything** — every bulletin, every magazine, every documentary, every trail, for years.
Nothing here is ever looked up, because it never needs to be: it is simply always there.

Three consequences govern everything below.

1. **Every word is paid for thousands of times.** A sentence that earns its place in a canon file
   may be indefensible here.
2. **A mistake here is in everything.** A wrong instruction in `core/` is not a wrong programme; it
   is every programme, until someone notices.
3. **The register you write in becomes the station's register.** Write these files lyrically and
   every hour of the day will reach for lyricism, including the market report.

---

## 1. The budget — the hard constraint

The always-present block has a ceiling of about **2,000–3,000 tokens**, and `core/` does not have it
to itself. It is shared with:

- the **cast cards** for whoever is on air — one card is ~340 words, and a two-presenter programme
  ships two;
- the **register rules**, a separate file that defines what human speech is.

Where it currently stands:

| | words | ≈ tokens |
|---|---|---|
| `STATION.md` | 807 | 1,089 |
| `TIME.md` | 421 | 568 |
| two cast cards | 682 | 920 |
| **total, before the register rules are even counted** | | **~2,578** |

That fits a two-hander and nothing else. A three-voice programme breaches the ceiling, and the
register rules are still to come.

> **Target: bring `core/` to about 800 words total — roughly `STATION.md` 450 and `TIME.md` 350.**
> That is a cut of a third, and it is the main thing this commission is for.

The test for every sentence: **would it be a problem if the station did not know this?** If a
programme could be written perfectly well without it, it belongs in canon, where it will be
retrieved on the days it matters — or nowhere.

---

## 2. The commission

### `TIME.md` — one urgent fix

**Delete the time-check instruction.** The file currently says:

> *"The DJ gives real-feeling time checks ("coming up on two in the morning, settlement time") and
> references the in-world date naturally."*

This is **wrong and actively harmful.** The station has a hard rule about clocks:

- **Bulletins and news programmes** state the time — they are broadcast at a fixed instant, so they
  can.
- **Everything else** — magazines, features, documentaries, chart shows, interviews, music
  programmes — **may never state the time**, because they are scheduled behind whatever is playing
  and could air an hour from where they were written. This is checked automatically and a programme
  that breaks it is thrown away and regenerated.

The sentence above teaches the opposite, with a worked example, on every call. Remove it. Do not
replace it with a corrected version — the rule belongs to the schedule, not to the station's
self-description.

**Also cut the lyricism.** *"the thread that binds scattered worlds across the dark, the rhythm that
lets separated people breathe in unison"* — see §3. Beautiful, and in exactly the wrong file.

Everything else in `TIME.md` is sound. The shared clock, the absence of time zones, worlds keeping a
local calendar alongside it, the three chronometers — keep all of it, tightened.

### `STATION.md` — re-premise it, then cut it by half

**This file describes a music station. Settlement Radio is a speech station.** It is a full
news-and-talk service: an hourly bulletin, a breakfast strand, an evening flagship, correspondents,
documentaries, one weekly chart show. Music leads only overnight. Three passages contradict the
actual schedule outright:

| Currently says | Actually |
|---|---|
| "It **plays music**, reads the news of the era" | speech-led; the chart is the only daytime music |
| "The DJs are given **wide latitude in programming**" | the schedule is fixed in config; presenters choose nothing |
| "**the midnight hour belongs to the listener** — requests, dedications, letters read aloud" | midnight is a 28-minute news programme, then a history documentary |

Also gone: presenters who "argue about setlists".

**Then cut it to about 450 words.** Three of the twelve numbered facts are station texture rather
than things the station must always know — the observatory dome, the monthly hand-cranked generator
ritual, the wall of photographs. They are good writing and they are welcome in the world bible. They
do not belong in the block that ships on every call. Move them out or drop them.

What must survive, because a programme genuinely cannot be written without it: the station's name and
what it is; the premise of scattered worlds and weeks of distance; that radio is the thread; that
Earth is distant history; the fossil-word explanation of "settlement"; that letters take weeks; the
station's between-the-worlds position and neutrality; and the tone.

---

## 3. How to write it

**Plain, declarative, specific.** These files are read by a machine that will imitate their register
in everything it writes afterwards. That is not a metaphor — it is the single most reliable effect in
the system.

```
✅  "Travel between worlds takes weeks. Radio is the thread that connects them."
❌  "Time is the rhythm that lets separated people breathe in unison across the dark."
```

Both are true. The first tells the station a fact; the second teaches it a voice, and the voice will
turn up in a report about freight tariffs.

The station's tone is **cozy, intelligent, a little wry — not dystopian, not camp**, and the warm,
wondering register belongs to the late-night programmes only. `core/` should state that the tone
exists without performing it.

**Format.** Keep both files as they are: a short prose section, then a numbered list of standing
facts. No frontmatter — that is what marks these as station text rather than world content. One
assertion per numbered item, one or two sentences.

---

## 4. Never

**A. Never instruct.** `core/` describes what is true, not what a presenter should do. "The DJ gives
time checks" is an instruction and it is how the current error got in. Facts only.

**B. Never state or imply a schedule.** No programme names, no hours, no "the midnight hour is…".
The schedule changes; `core/` is read by every programme including the ones that do not exist yet.

**C. No dates and no fixed years.** The in-world year is computed at broadcast time and is never
written down. Say "six centuries on", never a number. Nothing anywhere in these files may contain a
four-digit year.

**D. Nothing real.** No real person, place, brand, franchise, author or work. Earth is the single
exception — it is the origin world and is spoken of fondly and at a distance.

**E. No modern-AI futurism.** No machine consciousness, no singularity, no AI anxiety. Machine minds
in this world are capable, common tools and are not held to be persons.

**F. No physics changes.** Weeks between worlds. Nothing faster than light. The station's wide
broadcast crosses the settled worlds in hours; private, addressed messages take days to months.

**G. Nothing that belongs in canon.** If it is a detail about one place, one custom, one object or
one piece of station furniture, it is world bible material. The test in §1 decides it.

---

## 5. Before you hand it back

- [ ] `STATION.md` ≈ 450 words, `TIME.md` ≈ 350 — **~800 total**, down from 1,228.
- [ ] The time-check instruction is **gone**, not corrected.
- [ ] No sentence in either file instructs a presenter to do anything.
- [ ] Nothing implies the station plays music by default, or that presenters choose programming.
- [ ] No programme name, no hour, no four-digit year anywhere.
- [ ] Read both files aloud. If a sentence sounds like the station talking rather than a fact about
      the station, cut it.
- [ ] Every surviving sentence passes: *would it be a problem if the station did not know this?*
