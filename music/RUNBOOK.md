# RUNBOOK.md — making the music, step by step

> **For the operator. The writer never reads this.**
> Every step says who does it, what to paste, and how to check the answer before accepting it.
> Work top to bottom. **You cannot get lost if you only ever do the next unticked step.**

**The three files:**

| File | What it is | Who reads it |
|---|---|---|
| `COMMISSION.md` | the brief — what to write, how much, the IP rules | **the writer** |
| `CONSTANTS.md` | the fixed points — anchor years, session players, names used, tallies | you, pasted into every brief |
| `RUNBOOK.md` | this file — the procedure | you only |

---

## The shape of the work

**Two halves, and the first needs no music tool and no hardware.**

| Half | What | Needs an account? |
|---|---|---|
| **Half 1 — the wiki** | ~100 musicians, ~195 albums, ~1,700 song titles, two hundred years of a music industry, as text | **no — start today** |
| **Half 2 — the audio** | pick 500 songs from it, write their lyrics, generate, measure, tag | yes |

**Do half 1 completely before starting half 2.** The wiki is what makes the presenters worth
listening to; the audio is a sample of it. Building audio first is what produces a station that
plays songs and cannot talk about them.

---

## The words

**Layer A / B / C** — the three depths in `COMMISSION.md` §1. **A** is the 500 songs that become
audio. **B** is music that exists in the world but the station does not hold. **C** is history:
musicians whose recordings are lost. A presenter may discuss all three; the scheduler may only play A.

**Genre** — one of the eight fixed forms. **The wiki is written one genre at a time.**

**Label** — one of seven record companies. Bands belong to them. Labels matter because three show
formats are built on them, so layer-A bands must be spread to give each label enough depth.

**Band** — a solo singer or a group, with albums and a career. These are what the writer invents.

**Session player** — **not a band and not a solo artist.** A hired musician who plays on *other
people's* records. No albums of their own, no career of their own, no voice of their own. They exist
only as credits. Their whole job is to let a presenter say *"that's Ivena Sorn on pipes — she's on
half the Forge catalogue too."*

**Style card** — six lines fixing how a band sounds: voice, backing, instruments, production, tempo,
exclusions. Written once per layer-A band and reused in every generation prompt for them. **This
replaces any reliance on the tool's voice-cloning feature**, which is unreliable and tied to models
that get retired.

**Anchor year** — one of eight in-world years when a lot of records happened to come out. They let
the overnight show do "one label or one year".

**"Search each one"** — literally: type the name into Google in quotes and check Wikipedia. **Finding
nothing is the result you want.** See Step 2.

---

## Where you are

**Half 1 — the wiki**

- [x] **Step 0** — the constants. Done; in `CONSTANTS.md`.
- [ ] **Step 1** — replace Deym Rusk; get elders and dates.
- [ ] **Step 2** — screen the session-player names.
- [ ] **Step 3** — plan the eight genres across the seven labels.
- [ ] **Step 4** — write the wiki, one genre at a time. **×8**
- [ ] **Step 5** — screen every name in it.
- [ ] **Step 6** — check the whole wiki against the makeability rules.

**Half 2 — the audio**

- [ ] **Step 7** — pick the 500 and write the style cards.
- [ ] **Step 8** — lyrics and prompts, one album at a time.
- [ ] **Step 9** — generate.
- [ ] **Step 10** — measure by ear.
- [ ] **Step 11** — tag the files and file the licence evidence.

---

# Half 1 — the wiki

## Step 1 · Replace Deym Rusk, and get dates
**The writer.** One message.

### DO

```
Three fixes to the session players. Read COMMISSION.md first.

1. Replace "Deym Rusk". It reads as a filed-off Dean Rusk, a real and very
   well-known person. Same instrument, same character, new name.

2. Give each of the eight an active_from and active_to. They are one generation
   working roughly 2592–2626 (present = 2626). Vary the spans. One or two may
   have started very young in the late 2580s and still be working; say which.

3. Add three or four ELDERS — the players who worked before 2592. Same format,
   with dates. At least one should have taught or hired one of the eight, so the
   two generations connect.
```

### CHECK

- No career longer than about thirty-five years.
- Nobody credited before roughly age sixteen or after about eighty.
- The two oldest anchor years now have players who were working.
- At least one link between the generations.

### THEN

Update `CONSTANTS.md` §2.

---

## Step 2 · Screen the names
**You. Twenty minutes.**

> **Finding nothing is the result you want.** You are not looking something up — you are checking
> that a name is **not already taken** by a real famous person. An empty search is a pass, and most
> searches will be empty. That is a good batch.

### DO

Google each name **in quotes**, then check Wikipedia.

| What you find | Verdict |
|---|---|
| **Nothing at all** | ✅ Keep. The normal result |
| Noise — a LinkedIn profile, a forum user, a private person | ✅ Keep. Ordinary people share names |
| Only the **surname** matches something real | ✅ Keep. That is how surnames work |
| A **real notable person with that exact full name** — a Wikipedia article in several languages | ❌ Reject |
| A name that *reads as* a famous name with a letter changed | ❌ Reject. This is what caught Deym Rusk |

### CHECK

Or hand it to an AI with web access:

```
For each name, tell me only whether a real, notable person exists with that
EXACT full name — someone with a Wikipedia article, ideally in more than one
language. Also flag any name that reads as a well-known name with a letter or
two changed. Ignore surname-only matches and fictional characters.

Answer as a list: NAME — CLEAR or COLLISION (with a link).
Most should be CLEAR. Do not suggest replacements.
```

### THEN

Move cleared names into `CONSTANTS.md` §3. Record rejections there too, so the same collision is
never proposed twice.

---

## Step 3 · Plan the genres across the labels
**You. Thirty minutes, once.** This is the only planning step, and it prevents the one failure that
cannot be fixed later.

**The problem it solves.** The wiki is written genre by genre, but three show formats need *label*
depth — each label needs ≥3 layer-A bands and ≥40 playable songs. Write eight genres independently
and the bands scatter across seven labels with none of them deep enough.

### DO

Fill this in before briefing anything. Layer A only — 25 bands, 500 songs.

```
Label 1 (Concordance, prestige)   bands: __  songs: __   forms: Core Harmonies, relay-pop
Label 2 (Cold Harbor, frontier)   bands: __  songs: __   forms: Frontier Reels, Void Ballads
Label 3 (Meridian, dance)         bands: __  songs: __   forms: pulse-dance
Label 4 (Forge, industrial)       bands: __  songs: __   forms: lane-rock, Core Harmonies
Label 5 (haulers, co-op)          bands: __  songs: __   forms: lane-rock, relay-pop
Label 6 (late-club, folded 2612)  bands: __  songs: __   forms: void-lounge
Label 7 (old-system importer)     bands: __  songs: __   forms: old-system sessions
                                  TOTAL 25       TOTAL 500
```

### CHECK

- Every label: **≥3 bands and ≥40 songs.**
- Genre totals match `COMMISSION.md` §2.
- Relay-pop appears on ≥4 labels, lane-rock on ≥3, Frontier Reels on ≥3.

### THEN

Paste this table into `CONSTANTS.md` §5 as the running tally. **Tick off bands and songs as each
genre lands**, so you can see the shortfall before it is expensive.

---

## Step 4 · Write the wiki, one genre at a time
**The writer. Eight rounds.** This is the bulk of the work and all of it is text.

### DO

Start a fresh conversation. Paste `COMMISSION.md` whole and say *"This is the brief. Read it. Don't
write anything yet."* Then, per genre:

```
Write the <GENRE> section of the wiki.

Layer A — <N> bands, <M> songs, on labels <list from Step 3>.
  Full bios, full album stories, every song with its one fact, playable: true.

Layer B — about <N×2> bands. Two-sentence bios, one-line album notes,
  song titles only, playable: false.

Layer C — about <N/2> figures from 2426–2546. Three sentences each.
  No albums, no track lists.

Return YAML. No lyrics, no prompts, no style cards, no durations.

Anchor years:      <paste CONSTANTS §1>
Session players:   <paste CONSTANTS §2>
Names already used: <paste CONSTANTS §3>
```

### CHECK

Paste the answer into a **different** conversation, with `COMMISSION.md`, and this:

```
You are checking one genre of a music wiki against the brief. Report only
failures, as a numbered list. Do not rewrite anything and do not be encouraging.

1.  Band, album and song counts per layer against what was asked.
2.  Every layer-A song has a playable flag set true and exactly one concrete,
    sayable fact. Not a mood, not a summary.
3.  No layer-B song has a fact. No layer-C figure has an album or track list.
4.  Release years fall on the anchor years, or have a stated reason.
5.  No age, no relative date, no "recently", no "last year".
6.  Every band has active years. No career exceeds about 35 years.
7.  No session player is credited outside their active years.
8.  No real artist, band, label, album or song name anywhere.
9.  No name repeats one from the used-names list.
10. Bios are plain speech, not lyrical.
11. No song is about leaving Earth, the crossing or the long dark.

End with PASS or FAIL.
```

Send failures back. Re-check. Only then continue.

### THEN

Save as `music/wiki/<genre>.yaml`. Update the tally in `CONSTANTS.md` §5. **Then the next genre.**

---

## Step 5 · Screen every name
**You, or an AI with web access.** After each genre, not at the end of all eight.

Use the Step 2 prompt on every band, label, album title and song title in the genre you just
received. Add one line:

```
Also flag any album or song title that exactly matches a well-known real record
or song. Ignore common short phrases. Flag, do not reject.
```

Add cleared names to `CONSTANTS.md` §3. Send rejections back in **one** message.

---

## Step 6 · Check the whole wiki
**You. Once, after all eight genres.** The per-genre checker cannot see across genres; these rules
only exist at the whole-catalogue level.

```
Check this complete music wiki. Report only failures, numbered.

1.  Exactly 500 songs marked playable: true.
2.  Each of the seven labels has >=3 layer-A bands, >=6 albums, >=40 playable songs.
3.  At least four bands have >=18 playable songs.
4.  Six to eight albums have 12-14 playable songs.
5.  Every anchor year carries >=25 playable songs across >=4 bands and >=2 labels.
6.  Half of all playable songs fall in the last eight years (2619-2626).
7.  Genre proportions match COMMISSION.md section 2.
8.  Relay-pop appears on >=4 labels, lane-rock >=3, Frontier Reels >=3.
9.  Every session player appears on >=3 labels, within their active years.
10. No duplicate band, album or song titles anywhere.

End with PASS or FAIL.
```

**Fix everything this finds before touching the audio.** A structural hole is cheap now and expensive
after 500 songs exist.

---

# Half 2 — the audio

## Step 7 · Pick the 500 and write the style cards
**You and the writer.**

The 500 are already chosen — they are the songs marked `playable: true`. What is missing is how each
band sounds.

### DO

```
Write a style card for each layer-A band. Six lines, the format in COMMISSION.md
section 7:

voice / backing / instruments / production / tempo range / exclude

The voice line is fixed for the life of the band and never changes between
albums. Use the production palette for the band's form.
```

### CHECK

- Every layer-A band has one.
- No two bands on the same label have near-identical cards — that is the label's house style doing
  too much work.
- **The style cards go in `music/production/`, never in the wiki.** They contain real genre words.

---

## Step 8 · Lyrics and prompts, one album at a time
**The writer.**

```
Album: <title>, <band>, <year>, <form>.
Band style card: <paste>

For each song return:
  1. lyrics — COMMISSION.md section 3 subject rules and the swap-the-nouns test.
     Open with an instrumental-intro tag before the first verse.
  2. a generation prompt: the style card plus this song's mood, tempo and
     arrangement note, and an exclude line.

Every song has a vocal. Nothing about leaving Earth.
```

### CHECK

```
Check these lyrics and prompts. Report only failures, numbered.

1. Every song has a vocal. No instrumentals.
2. No lyric is about leaving Earth, the crossing, the cradle or the long dark.
3. Swap-the-nouns test: would each lyric still work with the science-fiction
   words replaced by ordinary ones? Name any that would collapse.
4. No real person, brand, company, franchise or work in any lyric.
5. Every song opens with an instrumental-intro tag.
6. Every prompt matches the band's style card, especially the voice line.
7. No prompt names a real artist, band, producer or record.

End with PASS or FAIL.
```

---

## Step 9 · Generate
**You.**

### DO

Custom mode — your lyrics, your prompt. **Finish a band in as few sittings as possible**: the current
models are being retired, and a band whose albums straddle two model versions will not sound like one
band.

The moment a take is a keeper, in this order:

1. **Download and rename to its path immediately** — `music/audio/<label>/<album>/03.mp3`. The tool's
   own filenames are unusable and after forty songs you will not know which is which.
2. Paste the exact prompt into the production sheet.
3. Add the log row: `| song id | title | attempts | model ver | date | licence period |`

### CHECK

Every keeper has all three: renamed file, prompt on file, log row. Missing one means it is not done.

---

## Step 10 · Measure by ear
**You. Nothing else can do this.**

Play each keeper and write down:

- **duration** — real length in seconds
- **intro ramp** — seconds until the **first sung word**
- **outro type** — `cold`, `fade` or `sustain`

**Check across the album:** is 40% of it at an 8-second ramp or longer? If not, lengthen the
instrumental-intro tags on the next album. You cannot fix this afterwards.

**Never estimate the intro ramp.** Two seconds too long clips a vocal on air, on every play, forever.

---

## Step 11 · Tag the files and file the evidence
**You. Do not leave this to the end of the project.**

### DO

- Write into each audio file's own tags: **licence period · generation date · model version · an
  AI-generated marker.** The audio will get separated from the wiki eventually — by a backup, a move,
  a hand-off — and the file has to carry its own provenance.
- **At the start of every month you generate in**, save the vendor's commercial-use terms as a dated
  PDF into `music/licence-evidence/`. Rights attach at the moment of generation under an active paid
  plan, so the evidence is per period, not per project.
- One line per batch stating that no real artist, work, band, label or voice was named, referenced or
  uploaded.

That line and the prompts under it are what the legal review actually reads.

---

## Done when

- [ ] All eight genres written, checked and screened.
- [ ] The whole-wiki check in Step 6 passes.
- [ ] 500 songs have audio, a measured ramp, a duration and an outro type.
- [ ] Every audio file carries its own licence tags.
- [ ] Licence evidence on file for every month generated in.
- [ ] `CONSTANTS.md` tallies complete and names all screened.
- [ ] **You have listened to fourteen songs back to back as if it were the hour.**

That last one is the only quality gate in this project. Nothing automated grades the product.

---

## Start small, twice

**Before commissioning a whole genre**, run Step 4 for one genre's layer A only — four or five bands —
and read it. That tells you whether this writer can do the job for the price of one message.

**Before generating 500 songs**, do one album end to end: style card, lyrics, generate, measure. Then
build a single retrospective hour and *listen to it*. Everything about the other 480 songs should be
decided by that hour.
