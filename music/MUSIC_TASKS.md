# MUSIC_TASKS.md — the whole music job, start to finish

Every piece of work needed to go from where we are today to 500 finished songs the station can play.
Nothing is left for later; if it is not on this page it is not part of the music job.

**Created 2026-08-08 by operator instruction** (D-053). It exists outside the §32 document cap and
outside `TASKS.md`'s ten-item cap, because the music content track is one long sequence and cutting
it into ten-item windows is what made it impossible to follow.

**`TASKS.md` holds no music cards. This file holds them all.**

---

## Who does what

| Tag | Meaning |
|---|---|
| `[agent]` | An agent does it. You do nothing but read the result and say keep or redo. |
| `[you]` | Only you can do it. Suno, ears, and judgements about the real world. |

**One card at a time, top to bottom.** A `[you]` card and an `[agent]` card may run at the same
time; two `[agent]` cards may not.

---

## How to run a card

**Open a new session in this repo and say the number.** "Do M-01." That is the whole interface.

The agent reads this file, works that one card, and before it finishes: marks that card **DONE**,
marks the next one **NEXT**, updates the stage table above, and tells you what to check. If a card
needs a decision from you it stops and asks rather than guessing.

**One card per session.** Two cards in one session is how the thread gets lost.

If you do not know where you are, say "what's next in music". The answer is always the one card
marked **NEXT**.

---

## Where we are

| Stage | Cards | Status |
|---|---|---|
| 0 · Tooling | M-01 … M-06 | M-01, M-02 done · **M-03 next** (M-04–M-06 wait on audio) |
| 1 · The wiki — 8 genres | M-07 … M-15 | relay-pop already done |
| 2 · The pilot — 45 songs end to end | M-16 … M-19 | not started |
| 3 · Style cards — the other 20 bands | M-20 | not started |
| 4 · Lyrics and prompts — 51 albums | M-21 … M-29 | not started |
| 5 · Suno — 455 songs | M-30 … M-38 | not started |
| 6 · Measure, tag, hand over | M-39 … M-42 | not started |

**Totals when this file is finished:** 9 genres · 25 bands · ~55 albums · 500 playable songs ·
~1,200 more songs that exist as text only.

**M-19 is the decision point.** Everything after it assumes the pilot sounded right. If it did not,
stages 3–6 get rewritten before they run.

---

# Stage 0 · Tooling

Six pieces of code that remove work from you. All `[agent]`, all before the bulk starts.

### M-01 · `[agent]` Ids that cannot collide, and a `make check` that reads the wiki — **DONE 2026-08-09**
Goal: The second genre written cannot silently overwrite the first, and the command tells you when a
genre does not match the plan — instead of you counting 105 songs by hand.
Files: `src/station/music/check.py`, `wiki.py`, `tests/unit/test_brief.py`, `music/CONSTANTS.md`
Check: `make check` goes red, naming the genre and the number, on a wrong song count for a label, a
layer-A song with no fact, a layer-B song that has one, a release year off the eight anchors, or any
id used twice. It is green on relay-pop exactly as it stands today.
Note: no existing id is ever renumbered — COMMISSION §10 forbids it. The counter becomes derived and
duplicates become an error.
Depends on: —

### M-02 · `[agent]` Retire the paste loop — **DONE 2026-08-09**
Goal: Six music commands become two, and the runbook stops describing a process you no longer use.
Files: `Makefile`, `src/station/cli.py`, `src/station/music/brief.py`, `music/RUNBOOK.md`, `docs/ADMIN.md`
Check: `make music-brief`, `music-check`, `music-style` and `music-songs` are gone, along with
`music/briefs/`. `make check` and `make music-albums` remain and work. `RUNBOOK.md` part 1 no longer
describes copying anything to a clipboard.
Depends on: M-07 (the first agent-written genre proves the loop is unnecessary) — **done ahead of
it by operator instruction; the brief carried nothing an in-repo agent cannot read (D-055)**

### M-03 · `[agent]` Name screening against Wikidata — **NEXT**
Goal: You stop googling several hundred invented names one at a time.
Files: `src/station/music/screen.py`, `Makefile`, `docs/ADMIN.md`
Check: `make music-screen GENRE=<x>` reports every band, label, album, song title and person in that
genre that has an exact-title match on a real notable person or organisation, and says nothing about
the rest. Run against relay-pop it returns a short list you can read in two minutes.
Note: exact matches only. "Reads like a famous name with a letter changed" stays a human judgement —
the tool narrows the pile, it does not clear it.
Depends on: M-01

### M-04 · `[agent]` `make music-analyse` — the three numbers, measured not estimated
Goal: You never hand-time 500 intro ramps.
Files: `src/station/music/analyse.py`, `Makefile`, `pyproject.toml`, `docs/ADMIN.md`
Check: `make music-analyse` reads every file under `music/audio/` and writes each song's duration,
seconds until the first sung word, and outro type (`cold`/`fade`/`sustain`). On the pilot's 45 songs
its ramp figures are within half a second of your ear on a spot-check of ten.
Note: ARCHITECTURE:1008 already specifies this pass and says onset detection gets the ballpark while
the last half-second is a listening judgement. So the tool measures and flags the borderline ones;
you re-listen only to those.
Depends on: M-18 (needs real audio to run against)

### M-05 · `[agent]` `make music-tag` — licence and compliance into every file
Goal: 500 files carry their own licence period, generation date, model version and AI marker without
you touching one.
Files: `src/station/music/tag.py`, `Makefile`, `docs/ADMIN.md`
Check: Every file under `music/audio/` carries all four tags. Reading any one file's tags tells you
what licence it was made under and that it is machine-generated.
Depends on: M-04

### M-06 · `[agent]` `music/catalogue.yaml` — the file the station reads
Goal: The wiki, the lyrics and the audio become the one file the station's database ingests. **This
is what makes a DJ able to say a fact about a record.** Without it the whole wiki is inert.
Files: `src/station/music/catalogue.py`, `music/catalogue.yaml`, `Makefile`, `docs/ADMIN.md`
Check: `make music-catalogue` produces `music/catalogue.yaml` in the shape ARCHITECTURE §17
specifies — labels, artists, albums, tracks with `file`, `category`, `mood`, `intro_ramp_sec`,
`outro_type`, `licence_note` — covering every playable song, and layer-B titles as unplayable rows.
`make check` validates it.
Note: the database ingest (`make music-sync`) belongs to the phase that has a database. This card
produces the file; nothing here needs Postgres.
Depends on: M-04, M-05

---

# Stage 1 · The wiki — the eight remaining genres

**One genre at a time, in this order.** The order matters: ids and the used-names list only stay
unique in sequence, and the biggest genres first means a problem shows up while it is cheap.

Each card is the same three steps — agent writes the file, `make check` counts it, you screen the
names. relay-pop is already done: 105 songs, 5 bands, 11 albums.

### M-07 · `[agent]` lane-rock — 75 songs, 4 bands
Files: `music/wiki/lane-rock.yaml`, `music/CONSTANTS.md`
Check: 75 playable songs split 10 / 35 / 30 across labels 2, 4 and 5; 4 layer-A bands; about 7
layer-B bands and 4 layer-C figures. `make check` green. Names screened and recorded.
Depends on: M-01

### M-08 · `[agent]` deck-talk — 70 songs, 3 bands
Check: 70 playable songs split 25 / 20 / 25 across labels 2, 4 and 5; 3 layer-A bands; ~7 layer-B,
~4 layer-C. `make check` green. Names screened.
Depends on: M-07

### M-09 · `[agent]` frontier-reels — 65 songs, 3 bands
Check: 65 playable songs split 30 / 15 / 20 across labels 2, 4 and 5; 3 layer-A bands; ~6 layer-B,
~4 layer-C. `make check` green. Names screened.
Depends on: M-08

### M-10 · `[agent]` old-system-sessions — 60 songs, 3 bands
Check: 60 playable songs, all on label 7; 3 layer-A bands; ~5 layer-B, ~4 layer-C. `make check`
green. Names screened.
Note: §10 forbids presenting an old-system record as archive. These are current releases that took a
long time to arrive.
Depends on: M-09

### M-11 · `[agent]` pulse-dance — 60 songs, 2 bands
Check: 60 playable songs, all on label 3; 2 layer-A bands; ~5 layer-B, ~3 layer-C. `make check`
green. Names screened.
Depends on: M-10

### M-12 · `[agent]` void-lounge — 40 songs, 3 bands
Check: 40 playable songs split 10 / 30 across labels 1 and 6; 3 layer-A bands; ~4 layer-B, ~3
layer-C. `make check` green. Names screened.
Note: label 6 folded in 2612 with a disputed catalogue — that dispute is the retrospective, so it
has to be in the album notes here.
Depends on: M-11

### M-13 · `[agent]` core-harmonies — 15 songs, 1 band
Check: 15 playable songs on label 1; 1 layer-A band; ~1 layer-B, ~2 layer-C. `make check` green.
Names screened.
Note: Odessa Vail's *Lanternlight* is fixed canon and sits in deep layer B; later performances of it
may be layer A.
Depends on: M-12

### M-14 · `[agent]` void-ballads — 10 songs, 1 band
Check: 10 playable songs on label 2; 1 layer-A band; ~1 layer-B, ~1 layer-C. `make check` green.
Names screened.
Note: Corin Hale's *Station Cycles* is fixed canon and belongs here.
Depends on: M-13

### M-15 · `[agent]` The catalogue-wide pass — and the wiki freezes
Goal: The three rules that are properties of the whole catalogue, not of one genre, are satisfied.
These cannot be checked a genre at a time, and fixing them is free now and expensive once songs
exist against them.
Files: `music/wiki/*.yaml`, `music/CONSTANTS.md`
Check: All nine files together give exactly 500 playable songs and 25 layer-A bands. Every one of
the eight anchor years carries ≥25 playable songs across ≥4 bands and ≥2 labels. There are 6–8
cornerstone albums of 12–14 songs. Every label has ≥3 bands, ≥6 albums and ≥40 songs. At least four
bands have ≥18 songs. Every session player appears across ≥3 labels and inside their active years.
`make check` green on all of it.
Note: fixes here are edits to release years and label assignments — text only, no lyrics affected.
**The wiki freezes when this card closes.** No lyrics are written before it does.
Depends on: M-14

---

# Stage 2 · The pilot — 45 songs, end to end

The point of this stage is to find out whether the approach works while it costs four albums to
redo, not 470 songs. It uses relay-pop's four Concordance albums, which are already written.

### M-16 · `[agent]` Style cards for relay-pop's five bands
Goal: Each band has the six lines that make it sound like the same band across three albums.
Files: `music/production/styles.yaml`
Check: `b_001`–`b_005` each have voice / backing / instruments / production / tempo range / exclude,
built from the line-ups already in the wiki. `make music-albums` shows `yes` in the STYLE column for
every relay-pop album.
Note: the voice line is fixed for the life of the band and never changes between albums.
Depends on: M-01

### M-17 · `[agent]` Lyrics and prompts — al_001 … al_004, 45 songs
Goal: Four complete albums of words, each song fitting the fact the wiki already states about it.
Files: `music/production/lyrics/al_001.yaml` … `al_004.yaml`
Check: 45 songs, each with lyrics opening on an instrumental-intro tag, a generation prompt built
from the band's style card plus that song's mood and one arrangement note, and an exclude line.
Every lyric passes the swap-the-nouns test. Nothing about leaving Earth. Every song has a vocal.
Note: written a whole album at a time, never song by song — one band, one room, one year.
Depends on: M-16

### M-18 · `[you]` Suno — Measure Kindly and Open Parallax, 45 songs
Goal: The pilot's audio exists.
Files: `music/audio/`
Check: 45 keeper takes downloaded and named `music/audio/<label>/<album>/NN.mp3`. Each album's
lyrics file records the exact prompt used, the attempt count, the model version and the date.
Note: Custom mode only — never let Suno write the lyrics. Finish each band in as few sittings as
possible; a band split across two model versions will not sound like one band.
Depends on: M-17

### M-19 · `[you]` The fourteen-song listen — the decision point
Goal: Decide whether this approach is worth 455 more songs.
Check: You have listened to fourteen of the pilot's songs back to back, as if it were the hour, and
written down what you thought. **That listen decides everything after this card.**
Note: this is the only quality gate in the project. Nothing automated grades the product.
Depends on: M-18

---

# Stage 3 · Style cards for the rest

### M-20 · `[agent]` Style cards for the other 20 bands
Goal: Every layer-A band in the catalogue has a fixed voice.
Files: `music/production/styles.yaml`
Check: All 25 layer-A bands have a six-line card. `make music-albums` shows `yes` in the STYLE
column for every playable album in every genre.
Depends on: M-15, M-19

---

# Stage 4 · Lyrics and prompts — the remaining 51 albums

One card per genre. Each writes every album in that genre, one album per pass.

### M-21 · `[agent]` relay-pop — the remaining 7 albums, 60 songs
Files: `music/production/lyrics/al_005.yaml` … `al_011.yaml`
Check: 60 songs with lyrics, prompts and exclude lines. Swap-the-nouns test passes on all of them.
Depends on: M-20

### M-22 · `[agent]` lane-rock — 75 songs
### M-23 · `[agent]` deck-talk — 70 songs
### M-24 · `[agent]` frontier-reels — 65 songs
### M-25 · `[agent]` old-system-sessions — 60 songs
### M-26 · `[agent]` pulse-dance — 60 songs
### M-27 · `[agent]` void-lounge — 40 songs
### M-28 · `[agent]` core-harmonies — 15 songs
### M-29 · `[agent]` void-ballads — 10 songs

Each of M-22 … M-29: one file per album under `music/production/lyrics/`, every song with lyrics, a
prompt and an exclude line, every lyric passing the swap-the-nouns test, every song with a vocal.
Each depends on the one before it, and M-22 depends on M-21.

**Extra passes go to the cornerstone albums.** Six to eight of them each carry a whole 56-minute
programme; the rest are rotation and nobody leans in. Weight the effort accordingly.

---

# Stage 5 · Suno — the remaining 455 songs

One card per genre, worked **one band at a time** — Suno retires its models, and a band split across
two versions will not sound like one band. 23 bands left after the pilot.

### M-30 · `[you]` relay-pop — the remaining 3 bands, 60 songs
### M-31 · `[you]` lane-rock — 4 bands, 75 songs
### M-32 · `[you]` deck-talk — 3 bands, 70 songs
### M-33 · `[you]` frontier-reels — 3 bands, 65 songs
### M-34 · `[you]` old-system-sessions — 3 bands, 60 songs
### M-35 · `[you]` pulse-dance — 2 bands, 60 songs
### M-36 · `[you]` void-lounge — 3 bands, 40 songs
### M-37 · `[you]` core-harmonies — 1 band, 15 songs
### M-38 · `[you]` void-ballads — 1 band, 10 songs

Each: every song in that genre has a keeper take, downloaded and named
`music/audio/<label>/<album>/NN.mp3`, with the prompt, attempts, model version and date recorded in
the album's lyrics file. Custom mode only.

**These are the long cards.** The pilot (M-19) tells you how long 45 songs take you; multiply.

---

# Stage 6 · Measure, tag, hand over

### M-39 · `[agent]` Measure and tag every song
Goal: All 500 songs carry a real duration, a measured intro ramp, an outro type and their licence
tags. Run after each genre's audio lands rather than once at the end.
Check: `make music-analyse` and `make music-tag` cover all 500. No song is missing a ramp. The
distribution matches COMMISSION §7 — ≥40% of songs have ≥8 seconds before the first sung word, ≥15%
have ≥15 seconds, roughly 30% cold / 45% fade / 25% sustain, average duration near 3:30.
Note: where the distribution misses, the fix is choosing different takes, not editing the numbers.
Depends on: M-05, M-38

### M-40 · `[you]` Licence evidence
Goal: Rights attach at the moment of generation, so the evidence is per month, not per project.
Files: `music/licence-evidence/`
Check: For every calendar month in which any song was generated, that month's Suno commercial-use
terms are saved as a dated PDF.
Note: do this at the **start** of each month you generate in. It cannot be reconstructed later.
Depends on: M-18

### M-41 · `[agent]` The catalogue file, complete
Goal: The station has one file it can ingest, covering everything.
Check: `make music-catalogue` produces `music/catalogue.yaml` with all 500 playable tracks — each
with its file path, category, mood tags, measured ramp, outro type and licence note — plus every
layer-B title as an unplayable row. `make check` green.
Depends on: M-06, M-39

### M-42 · `[you]` The full listen
Goal: Confirm the catalogue works as an hour, not as a spreadsheet.
Check: You have listened to fourteen consecutive songs from three different hours — a label
retrospective, an anchor year, and a plain music sequence — and each held up.
Note: if it does not hold up, the fix is more songs or different takes, not a different tool.
Depends on: M-41

---

## When this file is finished

- [ ] 9 genres written, checked and screened — ~1,700 songs of text
- [ ] 25 bands with a fixed voice
- [ ] ~55 albums with lyrics and prompts in git
- [ ] 500 songs with audio, a measured ramp, a duration and an outro type
- [ ] Every audio file carrying its own licence tags
- [ ] `music/catalogue.yaml` complete and validated
- [ ] Licence evidence for every month generated in
- [ ] You have listened, twice — at M-19 and at M-42

Then the music job is done, and it hands over to the phase that has a database.
