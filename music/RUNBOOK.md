# RUNBOOK.md — making the music, step by step

> **For the operator. The writer never reads this.**
> Every step says who does it, what to paste, and how to check the answer before accepting it.
> Work top to bottom. You cannot get lost if you only ever do the next unticked step.

**The three files:**

| File | What it is | Who reads it |
|---|---|---|
| `COMMISSION.md` | the brief — the rules, the shape, the IP firewall | **the writer** |
| `CONSTANTS.md` | the fixed points — anchor years, session players, names used, id counters | you, pasted into every brief |
| `RUNBOOK.md` | this file — the procedure | you only |

---

## The words

**Slot** — one of the seven labels the catalogue needs. They are listed as a table in `COMMISSION.md`
§4: slot 1 is the old prestige label on Concordance, slot 2 the frontier label, and so on. You do not
invent labels; you pick a slot and the writer invents the label that fills it.

**Slot card** — ten lines you write describing one slot, before you brief the writer. Template and a
worked example are in Step 2 below. It is the only creative decision you make per batch.

**Batch** — everything belonging to one label. One batch ≈ one label ≈ 65–105 tracks. You finish a
batch before starting the next.

**Roster** — the writer's answer to Brief A: the label, its artists, its albums, and every track title.
No lyrics yet.

**Session player** — **not a band and not a solo artist.** A hired musician who plays on *other
people's* records — the bass player who turns up on forty albums by forty different artists. They
have **no albums of their own, no discography, and no singing voice in Suno.** They exist only as
credits on other people's tracks. Their entire job is to let a presenter say *"that's Ivena Sorn on
pipes — she's on half the Forge catalogue too."* You have eight of them and you will never do
anything with them except list them in briefs and put them in credits.

**Artist** — the opposite: a solo singer or a band, with albums, with a voice, with a career. These
are what the writer invents per label. **These get Suno voices; session players never do.**

**Persona** — Suno's feature for reusing a voice. One per *artist*, so all their albums sound like
the same singer.

**Anchor year** — one of eight in-world years where lots of records happen to have been released.
They are in `CONSTANTS.md`. They exist so the overnight show can do "one label or one year".

**"Search each one"** — literally: type the name into Google in quotes, e.g. `"Nessa Dray"`, and
check Wikipedia. You are looking for a *real, notable* person with that exact full name. See Step 1.

---

## Where you are

- [x] **Step 0** — the constants. Done; filed in `CONSTANTS.md`.
- [ ] **Step 1** — screen the eight session-player names.
- [ ] **Step 2** — write the slot 1 card.
- [ ] **Step 3** — Brief A: get the roster.
- [ ] **Step 4** — screen the roster.
- [ ] **Step 5** — assign ids and file paths.
- [ ] **Step 6** — Brief B: get one album's songs.
- [ ] **Step 7** — cast the artist's voice in Suno.
- [ ] **Step 8** — generate the album.
- [ ] **Step 9** — measure by ear.
- [ ] **Step 10** — close the batch.

Steps 6–9 repeat per album and per artist. Steps 2–10 repeat per label, seven times.

---

## Step 1 · Screen the eight session-player names
**You. Twenty minutes. Do this before anything else** — these eight appear on every label, so a
collision found later means editing credits across hundreds of tracks.

> ### Finding nothing is the result you want
>
> You are not looking something up. You are **checking that the name is not already taken** by a
> real famous person. An empty search means the name is genuinely invented, which is the whole
> point. **Silence is a pass.** Most of the eight will return nothing, and that is a good batch.

### DO

For each of the eight names in `CONSTANTS.md` §2:

1. Google the name **in quotes**: `"Ivena Sorn"`.
2. Check English Wikipedia for the exact full name.
3. Decide:

| What you find | Verdict |
|---|---|
| **Nothing at all** | ✅ **Keep.** This is the normal, expected result |
| Random noise — a LinkedIn profile, a forum user, a private person | ✅ **Keep.** Ordinary people share names; only *famous* ones matter |
| Only the **surname** matches something real | ✅ **Keep.** That is how surnames work. Note it and move on |
| A **real, notable person with that exact full name** — a Wikipedia article, ideally in several languages | ❌ **Reject.** Ask the writer for a replacement |

**In practice you will reject roughly none of them.** The screen exists for the one time in fifty
that a writer lands on a real musician's name by accident, and that one time is worth the twenty
minutes.

### CHECK

Paste to an AI with web access:

```
For each of these names, tell me only whether a real, notable person exists with
that EXACT full name — someone with a Wikipedia article, ideally in more than one
language. Ignore surname-only matches and fictional characters.

Answer as a list: NAME — CLEAR or COLLISION (with the link).
Do not suggest replacements.

<paste the eight names>
```

### THEN

Move cleared names in `CONSTANTS.md` §3 from **pending screen** to **screened and cleared**. Put any
rejection under **rejected on screen** so it is never proposed again. Tick Step 1 above.

---

## Step 1b · Brief 0b — the elders, and dates for everyone
**The writer.** One message. Do it while you are waiting on the Deym Rusk replacement.

### DO

```
Two follow-ups on the session players. Read COMMISSION.md first.

1. Give each of the eight an active_from and active_to. They are one generation,
   working roughly 2592–2626 (present = 2626). Vary the spans — some just
   starting, some near the end. One or two may have started very young in the
   late 2580s and still be working; say which.

2. Add three or four ELDERS — the players who worked the old-standards window,
   2546–2591. Same format: name, instrument, one line of character, active_from,
   active_to. At least one should have taught or hired one of the eight, so the
   two generations connect.
```

### CHECK

- No player's span is longer than about thirty-five years.
- Nobody is credited before roughly age sixteen or after about eighty.
- The 2559 and 2583 anchor years now have players who were alive and working.
- At least one link between the two generations.

### THEN

Add the elders and all the dates to `CONSTANTS.md` §2. **Screen the new names** the same way as
Step 1.

---

## Step 2 · Write the slot 1 card
**You. Ten minutes.** Eight of the ten lines are copied from `COMMISSION.md`; only two are yours.

### DO

Copy this and fill in the two lines marked `<yours>`.

```
1  Slot            1 — flagship, core prestige
2  Home            Concordance
3  Forms           Core Harmonies ~40 (the whole world's supply — this is its home)
                   relay-pop ~45 (its commercial half)
                   void-lounge ~20 (the core's late clubs)
4  Era             Old. Founded generations back, still running, still the incumbent
5  Roster          5 artists · 2–3 albums each · 8–12 tracks · ~105 tracks total
                   at least 2 artists with 18+ tracks (artist profiles)
                   at least 1 cornerstone album of 12–14 (album story)
6  House style     <yours — one concrete phrase an engineer could act on>
7  Standing        Purist by conviction and Synthesist in practice; they deny this
8  Its trouble     <yours — what is going wrong for this label right now>
9  Anchor years    2559 (Vail première) · 2624 (hall reopening) · plus 2619
10 Must unlock     one label retrospective · two artist profiles · one album story
```

**Eight of those ten lines are already written above.** Copy them as they are. You are writing
**two sentences**, and that is the entire creative task.

#### Line 6 — house style

**The question it answers: what does every record on this label have in common, in the room?**

Not a mood. A *working method* — something you could hold a finished track against and say yes or
no. Real-world labels, purely to show you the shape (these are illustrations of form, not
suggestions to copy):

- *"one house band, one room, everything mixed to sound good on a car radio"*
- *"cut live at night, one rehearsal, microphones out in the room"*
- *"everyone facing each other, no written charts, first good take wins"*

Notice what those have in common: **a way of working, which produces a sound.** That is what steers
both the writer and Suno. "Warm", "timeless" and "high quality" steer nothing.

**Your test:** hand line 6 to a stranger with two finished tracks. Could they tell you which one
belongs to this label? If not, rewrite.

#### Line 8 — its trouble

**The question it answers: what is going wrong here right now?**

Not necessarily failure. Trouble is what gives the world something to *do* with the label — a beat,
an anniversary, an argument, a reason a 56-minute retrospective exists. Shapes that work:

- someone central is ill, or leaving, and nobody will say so
- the best act just went to a rival
- they own the catalogue but not the recordings, and it is in dispute
- they are not failing at all, just complacent — an ageing roster, and the young acts sign elsewhere

**Your test:** could a news bulletin report something about this label next month? If nothing could
ever happen to it, it has no trouble.

### CHECK

Two questions, both about your own two lines:

1. Could someone else tell whether a finished record obeys line 6?
2. Could something happen to this label next month because of line 8?

If both are yes, the card is done. That is the whole check.

---

## Step 3 · Brief A — get the roster
**The writer.** One message.

### DO

Start a fresh conversation. Paste, in this order:

1. The whole of `COMMISSION.md`, and *"This is the brief. Read it. Don't write anything yet."*
2. Then:

```
Write batch 01: label slot 1.

<paste your slot card from Step 2>

Return YAML only, in the §17a shape: one label, its artists, its albums, and every
track with title, track_no, and its one-fact line. Follow §3 for release years and
§5 for how deep the roster has to be. No lyrics, no prompts, no durations.

Anchor years — put most releases on these:
<paste CONSTANTS.md §1>

Session players available to credit:
<paste CONSTANTS.md §2>

Names already used, do not reuse or echo:
<paste CONSTANTS.md §3>
```

### CHECK

**Do not skip this.** Paste the writer's answer into a *different* conversation, with
`COMMISSION.md`, and this:

```
You are checking a music catalogue batch against the brief. Report only failures,
as a numbered list. Do not rewrite anything and do not be encouraging.

Check:
1.  Artist, album and track counts against §1 for this tier.
2.  At least two artists with 18 or more tracks.
3.  At least one album of 12–14 tracks.
4.  Every track has exactly one fact, and each fact is concrete and sayable
    on air — not a mood, not a summary.
5.  Release years fall on the anchor years given, or have a stated reason.
6.  No age, no relative date, no "recently", no "last year".
7.  Form mix and track counts match the slot card.
8.  No real artist, band, label, album or song name anywhere.
9.  No name repeats one from the used-names list.
10. Bios are plain speech, not lyrical.

End with PASS or FAIL.
```

Send failures back to the writer. Re-check. Only then continue.

### THEN

Save as `music/batches/01-<label>/catalogue.yaml`.

---

## Step 4 · Screen the roster names
**You.** Same as Step 1, on a bigger list: the label name, every artist and band name, every album
title, every track title.

### DO

Use the Step 1 CHECK prompt, with one addition for titles:

```
Also flag any album or song title that exactly matches a well-known real record
or song. Ignore common short phrases. Flag, do not reject.
```

### THEN

Add every cleared name to `CONSTANTS.md` §3. Ask the writer to replace anything rejected — **one
message, listing all of them at once.**

---

## Step 5 · Assign ids and file paths
**You, or an AI. Mechanical.**

### DO

```
Add to each entry in this YAML:
- a unique id: labels/artists/albums as short slugs, tracks as t_0001 upward,
  continuing from <next free id in CONSTANTS.md §4>
- a file path for each track: music/<label>/<album>/NN.mp3 where NN is track_no
  zero-padded to two digits
Change nothing else. Return the full YAML.
```

### THEN

Update the id counter in `CONSTANTS.md` §4.

---

## Step 6 · Brief B — one album's songs
**The writer.** Back in the Brief A conversation, so they still have the roster.

### DO

```
Album: <title>, <artist>, <year>, <form>.

For each track return:
  1. lyrics — §6's subject rules and the swap-the-nouns test.
     Open with an instrumental-intro tag before the first verse.
  2. a Suno style prompt from the §2 palette for this form, and an
     exclude-styles line.

Every track has a vocal. Nothing about leaving Earth. Keep the label's
house style audible across all of them — this is one label's record.
```

**On an artist's first album only, add:** `Order the tracks so the first three are the most typical
of this singer.`

### CHECK

```
Check these lyrics and prompts against the brief. Report only failures, numbered.

1.  Every track has a vocal. No instrumentals.
2.  No lyric is about leaving Earth, the crossing, the cradle or the long dark.
3.  The swap-the-nouns test: would each lyric still work with the science-fiction
    words replaced by ordinary ones? Name any that would collapse.
4.  No real person, brand, company, franchise or work named in any lyric.
5.  Every track opens with an instrumental-intro tag.
6.  Every style prompt uses only the palette for this form, and has an
    exclude-styles line.
7.  No style prompt names a real artist, band, producer or record.

End with PASS or FAIL.
```

### THEN

Save into `music/batches/01-<label>/production.md`. **Lyrics and prompts never go in
`catalogue.yaml`.**

---

## Step 7 · Cast the artist's voice
**You, in Suno. Once per artist, on their first album only.**

### DO

1. Generate the **first three tracks** of the album in custom mode — your lyrics, your style prompt.
2. Play them and pick the best **voice**. You are casting a singer, not picking a single.
3. Make that take into a **persona**. Name it exactly the artist's id.

### CHECK

Play the three back to back. Ask: *does this sound like one person who could plausibly have a
career?* If two of them sound like different singers, the style prompt is fighting the voice —
narrow the prompt and redo.

### THEN

Write the persona name into `production.md`. **This is the setting that makes or breaks the artist
profile show.** Losing it later means re-recording that artist's entire catalogue.

---

## Step 8 · Generate the album
**You, in Suno.**

### DO

Generate the remaining tracks with the persona applied, varying the style prompt only slightly per
track. **The moment a take is a keeper, in this order:**

1. Download and **rename it to its assigned path immediately** — `music/<label>/<album>/03.mp3`.
   Suno's own filenames are unusable and after forty tracks you will not know which is which.
2. Paste the exact prompt and exclude line into `production.md`.
3. Add the log row: `| track id | title | attempts | persona | model ver | date | licence period |`

**Finish an artist inside one Suno model version.** If Suno upgrades mid-artist, finish on the old
version rather than starting their next album on the new one.

### CHECK

Every keeper has: a renamed file, a prompt in `production.md`, and a log row. If any of the three is
missing, it is not done.

---

## Step 9 · Measure by ear
**You. Nothing else can do this.**

### DO

Play each keeper with a stopwatch or the player's own timer and write down:

- **duration** — real length in seconds
- **intro ramp** — seconds from the start until the **first sung word**
- **outro type** — `cold` (stops dead), `fade`, or `sustain` (rings out)

### CHECK

Across the finished album: is at least 40% of the batch at an intro ramp of 8 seconds or more? If
not, add longer instrumental-intro tags on the next album — you cannot fix this later.

### THEN

Put these three numbers into `catalogue.yaml`. **Never estimate the intro ramp.** Two seconds too
long clips a vocal on air, on every play, forever.

---

## Step 10 · Close the batch
**You.**

- [ ] Every name screened, every rejection recorded in `CONSTANTS.md`.
- [ ] Every track has audio, a measured ramp, a duration and an outro type.
- [ ] Every track has its one fact.
- [ ] `catalogue.yaml` contains no prompt text and no real genre word.
- [ ] `production.md` contains every prompt, persona and date, plus one line stating that no real
      artist, work, band, label or voice was named, referenced or uploaded in this batch.
- [ ] `CONSTANTS.md` updated: names used, id counter, label claimed.
- [ ] **You have listened to fourteen tracks back to back as if it were the hour.**

That last one is the only quality gate in this project. Nothing automated grades the product.

---

## Do the pilot before committing

**Finish slot 1 — about 105 tracks — then build one label retrospective hour from it and listen to
it.** Everything about the remaining 435 tracks should be decided by that hour. If the palette is
wrong it is one label's work to redo instead of seven.

And before even that: **run Steps 3 and 6 for a single album with a new writer** before commissioning
a whole label from them. That tells you whether they can do the job for the price of one message.
